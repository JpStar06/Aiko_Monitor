import asyncio
import os
import aiohttp

MONITOR_URL = os.getenv("MONITOR_URL")
MONITOR_TOKEN = os.getenv("MONITOR_TOKEN")


async def heartbeat():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    MONITOR_URL,
                    headers={
                        "Authorization": f"Bearer {MONITOR_TOKEN}"
                    },
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status != 200:
                        print(
                            f"[AikoMonitor] heartbeat HTTP {response.status}"
                        )

        except Exception as exc:
            print(f"[AikoMonitor] falha no heartbeat: {exc}")

        await asyncio.sleep(30)
