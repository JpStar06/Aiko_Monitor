import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import aiohttp
from fastapi import FastAPI, Header, HTTPException

from app.database import init_db, get_state, save_heartbeat, set_status, record_event
from app.discord_status import DiscordStatus

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("AikoMonitor")

MONITOR_TOKEN = os.getenv("MONITOR_TOKEN")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))
OFFLINE_AFTER = int(os.getenv("OFFLINE_AFTER", "90"))

if not MONITOR_TOKEN:
    raise RuntimeError("MONITOR_TOKEN não foi configurado.")

discord_status = DiscordStatus()


def utcnow():
    return datetime.now(timezone.utc)


async def monitor_loop():
    log.info(
        "Monitor iniciado | check=%ss | offline_after=%ss",
        CHECK_INTERVAL,
        OFFLINE_AFTER,
    )

    while True:
        try:
            state = await get_state()

            if state["last_heartbeat"] is not None:
                last = datetime.fromisoformat(state["last_heartbeat"])
                age = (utcnow() - last).total_seconds()

                if age > OFFLINE_AFTER and state["status"] == "online":
                    await set_status("offline")
                    await record_event("offline", age)

                    log.warning("AikoBot detectado como OFFLINE (%.0fs sem heartbeat).", age)
                    await discord_status.send_offline(age)

            await asyncio.sleep(CHECK_INTERVAL)

        except asyncio.CancelledError:
            raise
        except Exception:
            log.exception("Erro no ciclo do monitor.")
            await asyncio.sleep(CHECK_INTERVAL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    task = asyncio.create_task(monitor_loop())

    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="AikoMonitor",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"service": "AikoMonitor", "status": "online"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/heartbeat")
async def heartbeat(authorization: str | None = Header(default=None)):
    if authorization != f"Bearer {MONITOR_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    state = await get_state()
    previous_status = state["status"]

    await save_heartbeat(utcnow())

    if previous_status == "offline":
        await set_status("online")
        await record_event("online", None)

        log.info("AikoBot voltou ONLINE.")
        await discord_status.send_online()

    elif previous_status == "unknown":
        await set_status("online")
        await record_event("online", None)

        log.info("Primeiro heartbeat recebido. AikoBot ONLINE.")
        await discord_status.send_online()

    return {"status": "ok"}
