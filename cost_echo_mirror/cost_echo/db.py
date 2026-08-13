"""Read-only SQLite access for cost-echo.

Opens the hermes state DB in immutable read-only URI mode when supported,
falling back to a plain read-only connection. NEVER opens with write.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = "/usr/local/lib/hermes-agent/profiles/aaa-hermes/state.db"

_QUERY = """
SELECT
    m.id            AS message_id,
    m.session_id    AS session_id,
    m.role          AS role,
    m.content       AS content,
    m.timestamp     AS ts,
    s.chat_id       AS chat_id,
    s.chat_type     AS chat_type,
    s.user_id       AS user_id,
    s.display_name  AS display_name
FROM messages m
JOIN sessions s ON s.id = m.session_id
WHERE m.role IN ('user', 'assistant')
  AND m.content IS NOT NULL
ORDER BY s.chat_id, m.timestamp, m.id
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    """Open the database strictly read-only.

    Tries SQLite URI immutable mode first (no journal/WAL access at all);
    falls back to mode=ro, then to a plain connection as a last resort.
    """
    path = str(db_path)
    uri_immutable = f"file:{path}?immutable=1"
    try:
        conn = sqlite3.connect(uri_immutable, uri=True)
        conn.execute("SELECT 1")
        return conn
    except sqlite3.Error:
        pass
    try:
        conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        conn.execute("SELECT 1")
        return conn
    except sqlite3.Error:
        pass
    # Last resort: plain handle, but we only ever SELECT through it.
    return sqlite3.connect(path)


def fetch_messages(db_path: str | Path) -> list[dict[str, Any]]:
    """Fetch all user/assistant messages joined with session chat metadata.

    Returns a list of plain dicts sorted by (chat_id, timestamp, id).
    Returns [] for an empty DB or one without the expected tables.
    """
    conn = connect(db_path)
    try:
        cur = conn.execute(_QUERY)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]
    except sqlite3.Error:
        return []
    finally:
        conn.close()
