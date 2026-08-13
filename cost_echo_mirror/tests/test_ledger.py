"""Tests for cost_echo.ledger using a temporary SQLite fixture.

NEVER points at the real DB — builds its own schema-mimicking fixture.
"""

from __future__ import annotations

import sqlite3

import pytest

from cost_echo.db import fetch_messages
from cost_echo.ledger import compute_ledger


@pytest.fixture()
def db_path(tmp_path):
    """Create a temp DB mimicking the real schema, return its path."""
    path = tmp_path / "state.db"
    conn = sqlite3.connect(path)
    conn.executescript(
        """
        CREATE TABLE sessions (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL DEFAULT 'test',
            user_id TEXT,
            chat_id TEXT,
            chat_type TEXT,
            display_name TEXT,
            started_at REAL NOT NULL
        );
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT,
            timestamp REAL NOT NULL
        );
        CREATE TABLE session_model_usage (
            session_id TEXT NOT NULL,
            model TEXT NOT NULL,
            api_call_count INTEGER DEFAULT 0,
            input_tokens INTEGER DEFAULT 0,
            output_tokens INTEGER DEFAULT 0,
            reasoning_tokens INTEGER DEFAULT 0,
            cache_read_tokens INTEGER DEFAULT 0,
            estimated_cost_usd REAL DEFAULT 0
        );
        """
    )
    yield conn, path
    conn.close()


def _seed(conn, sessions, messages):
    conn.executemany(
        "INSERT INTO sessions (id, user_id, chat_id, chat_type, display_name, started_at) "
        "VALUES (?,?,?,?,?,?)",
        sessions,
    )
    conn.executemany(
        "INSERT INTO messages (session_id, role, content, timestamp) VALUES (?,?,?,?)",
        messages,
    )
    conn.commit()


def _rows(conn_path, **kw):
    return compute_ledger(fetch_messages(conn_path), **kw)


def test_empty_db(db_path):
    conn, path = db_path
    assert _rows(path) == []


def test_single_actor_assistant_replies(db_path):
    """Path (b): assistant messages in actor's session count as received."""
    conn, path = db_path
    _seed(
        conn,
        [("s1", "u1", "c1", "private", "Ali", 0.0)],
        [
            ("s1", "user", "one two three four", 100.0),   # 4 words given
            ("s1", "assistant", "alpha beta", 110.0),      # 2 words received
            ("s1", "user", "five six", 200.0),             # 2 words given
            ("s1", "assistant", "gamma delta epsilon zeta", 210.0),  # 4 words
        ],
    )
    rows = _rows(path)
    assert len(rows) == 1
    r = rows[0]
    assert r.actor == "u1"
    assert r.messages_given == 2
    assert r.tokens_given == 6
    assert r.tokens_received == 6
    assert r.asymmetry == pytest.approx(1.0)
    # both messages replied within 30 min -> closure 1.0, drain 0.0
    assert r.closure_rate == 1.0
    assert r.drain_score == 0.0
    assert r.response_latency_s == pytest.approx(10.0)


def test_reply_marker_path_a(db_path):
    """Path (a): '[Replying to:' from another actor in the same chat."""
    conn, path = db_path
    _seed(
        conn,
        [
            ("s1", "u1", "gc", "group", "Ali", 0.0),
            ("s2", "u2", "gc", "group", "Bala", 0.0),
        ],
        [
            ("s1", "user", "hello group friends", 100.0),
            ("s2", "user", '[Replying to: "hello"] hi back at you', 120.0),
        ],
    )
    rows = {r.actor: r for r in _rows(path)}
    ali = rows["u1"]
    assert ali.tokens_received == 7  # 7 words incl. marker text
    assert ali.closure_rate == 1.0
    bala = rows["u2"]
    # Bala's own message is not a reply to himself
    assert bala.tokens_received == 0
    assert bala.closure_rate == 0.0


def test_closure_no_replies(db_path):
    conn, path = db_path
    _seed(
        conn,
        [("s1", "u1", "c1", "private", "Ali", 0.0)],
        [("s1", "user", "anyone there", 100.0)],
    )
    (r,) = _rows(path)
    assert r.closure_rate == 0.0
    assert r.tokens_received == 0
    # asymmetry = 2 words / max(0,1) = 2.0 ; drain = 2.0 * (1-0) = 2.0
    assert r.asymmetry == pytest.approx(2.0)
    assert r.drain_score == pytest.approx(2.0)
    assert r.response_latency_s is None


def test_closure_window_boundary(db_path):
    """Reply after 30 min counts for latency but NOT for closure."""
    conn, path = db_path
    _seed(
        conn,
        [("s1", "u1", "c1", "private", "Ali", 0.0)],
        [
            ("s1", "user", "ping", 1000.0),
            ("s1", "assistant", "pong much later", 1000.0 + 1801.0),
        ],
    )
    (r,) = _rows(path)
    assert r.closure_rate == 0.0
    assert r.response_latency_s == pytest.approx(1801.0)


def test_asymmetry_math_and_unicode(db_path):
    conn, path = db_path
    _seed(
        conn,
        [("s1", "u1", "c1", "private", "Ali 🌙", 0.0)],
        [
            ("s1", "user", "satu dua tiga empat lima enam", 100.0),  # 6 words
            ("s1", "assistant", "jawapan ringkas", 105.0),           # 2 words
        ],
    )
    (r,) = _rows(path)
    assert r.tokens_given == 6
    assert r.tokens_received == 2
    assert r.asymmetry == pytest.approx(3.0)
    assert r.display_name == "Ali 🌙"
    assert r.drain_score == pytest.approx(0.0)  # closed -> no drain


def test_min_messages_and_chat_filter(db_path):
    conn, path = db_path
    _seed(
        conn,
        [
            ("s1", "u1", "c1", "private", "Ali", 0.0),
            ("s2", "u2", "c2", "private", "Bala", 0.0),
        ],
        [
            ("s1", "user", "a", 100.0),
            ("s1", "user", "b", 200.0),
            ("s2", "user", "c", 100.0),
        ],
    )
    assert len(_rows(path, min_messages=2)) == 1
    assert len(_rows(path, min_messages=1)) == 2
    assert [r.actor for r in _rows(path, chat_id="c2")] == ["u2"]


def test_deterministic_sort(db_path):
    conn, path = db_path
    _seed(
        conn,
        [
            ("s1", "u1", "c1", "private", "Ali", 0.0),
            ("s2", "u2", "c2", "private", "Bala", 0.0),
        ],
        [
            ("s1", "user", "x y", 100.0),
            ("s2", "user", "x y z w", 100.0),
        ],
    )
    rows = _rows(path)
    # u2 drain 4.0 > u1 drain 2.0 -> u2 first
    assert [r.actor for r in rows] == ["u2", "u1"]
    assert rows == _rows(path)  # stable across runs
