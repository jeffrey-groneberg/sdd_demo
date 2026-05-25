"""SQLite persistence layer for Shortly.

Per Constitution II we use the stdlib `sqlite3` module — no ORM.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

DB_PATH = Path("shortly.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS urls (
    code        TEXT PRIMARY KEY,
    url         TEXT NOT NULL,
    clicks      INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_urls_created ON urls (created_at DESC);
"""


def _connect(path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db(path: Path = DB_PATH) -> None:
    with _connect(path) as conn:
        conn.executescript(SCHEMA)


@contextmanager
def get_conn(path: Path = DB_PATH) -> Iterator[sqlite3.Connection]:
    conn = _connect(path)
    try:
        yield conn
    finally:
        conn.close()


def insert_url(conn: sqlite3.Connection, code: str, url: str, created_at: str) -> bool:
    """Insert; return False on collision."""
    try:
        conn.execute(
            "INSERT INTO urls (code, url, clicks, created_at) VALUES (?, ?, 0, ?)",
            (code, url, created_at),
        )
        return True
    except sqlite3.IntegrityError:
        return False


def get_url(conn: sqlite3.Connection, code: str) -> sqlite3.Row | None:
    cur = conn.execute("SELECT code, url, clicks, created_at FROM urls WHERE code = ?", (code,))
    return cur.fetchone()


def increment_clicks(conn: sqlite3.Connection, code: str) -> None:
    conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE code = ?", (code,))


def list_recent(conn: sqlite3.Connection, limit: int = 10) -> list[sqlite3.Row]:
    cur = conn.execute(
        "SELECT code, url, clicks, created_at FROM urls ORDER BY created_at DESC LIMIT ?",
        (limit,),
    )
    return list(cur.fetchall())
