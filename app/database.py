import asyncio
import os
import sqlite3
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "data/monitor.db")
_lock = asyncio.Lock()


def _connect():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


async def init_db():
    async with _lock:
        conn = _connect()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS monitor_state (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    status TEXT NOT NULL,
                    last_heartbeat TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    duration_seconds REAL
                )
            """)
            row = conn.execute("SELECT id FROM monitor_state WHERE id = 1").fetchone()
            if row is None:
                conn.execute("INSERT INTO monitor_state (id, status, last_heartbeat) VALUES (1, 'unknown', NULL)")
            conn.commit()
        finally:
            conn.close()


async def get_state():
    async with _lock:
        conn = _connect()
        try:
            row = conn.execute("SELECT status, last_heartbeat FROM monitor_state WHERE id = 1").fetchone()
            return dict(row)
        finally:
            conn.close()


async def save_heartbeat(timestamp: datetime):
    async with _lock:
        conn = _connect()
        try:
            conn.execute("UPDATE monitor_state SET last_heartbeat = ? WHERE id = 1", (timestamp.isoformat(),))
            conn.commit()
        finally:
            conn.close()


async def set_status(status: str):
    async with _lock:
        conn = _connect()
        try:
            conn.execute("UPDATE monitor_state SET status = ? WHERE id = 1", (status,))
            conn.commit()
        finally:
            conn.close()


async def record_event(event: str, duration_seconds: float | None):
    async with _lock:
        conn = _connect()
        try:
            conn.execute(
                "INSERT INTO events (event, created_at, duration_seconds) VALUES (?, ?, ?)",
                (event, datetime.now().astimezone().isoformat(), duration_seconds),
            )
            conn.commit()
        finally:
            conn.close()
