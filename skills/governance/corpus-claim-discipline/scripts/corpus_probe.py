#!/usr/bin/env python3
"""corpus_probe.py — dedupe funnel + speaker/histogram probe for ONE chat lane.

WHY: raw substring counts over a live message store are inflated (the store re-quotes earlier
messages inside later turns, and quote-blocks nest). Counting without deduping manufactures
patterns. This prints the funnel so every figure is auditable.

SCHEMA GUARD: the state-DB schema has moved before. This script verifies the columns it needs and
exits loudly rather than guessing. Run it, read the first block, then trust the rest.

USAGE
    python3 corpus_probe.py --chat-id -1003815535761
    python3 corpus_probe.py --chat-id 267378578 --focus 267378578 --json

OUTPUT
    1. schema check (stderr)
    2. dedupe funnel (raw -> minute -> replay)
    3. per-speaker counts
    4. per-day volume + hour histogram for --focus

SCOPE NOTE: counts reach enacted behaviour, self-report, vocabulary, timing and volume ONLY.
They do not reach attachment, motive, interior or shared meaning. Never quote these numbers as
evidence of how anyone feels.
"""

from __future__ import annotations

import argparse
import collections
import datetime
import json
import re
import sqlite3
import sys

SENDER = re.compile(r"^\[([^\]|]{0,40})\|(\d+)\]\s*(.*)$", re.S)
REQUIRED_COLUMNS = {"id", "session_id", "role", "content", "timestamp"}


def schema_check(con: sqlite3.Connection) -> None:
    cols = {r[1] for r in con.execute("pragma table_info(messages)")}
    missing = REQUIRED_COLUMNS - cols
    if missing:
        sys.exit(f"SCHEMA MISMATCH - messages is missing {sorted(missing)}. "
                 f"Columns seen: {sorted(cols)}. Fix the query, do not guess.")


def lane_session_ids(con: sqlite3.Connection, chat_id: str) -> list[str]:
    rows = con.execute("select id from sessions where chat_id = ?", (chat_id,)).fetchall()
    ids = [r[0] for r in rows]
    if not ids:
        sys.exit(f"No sessions found for chat_id={chat_id!r}. "
                 f"Check the lane id - a lane spans many session ids; sweep the lane, not one session.")
    return ids


def fetch(con: sqlite3.Connection, sess_ids: list[str]) -> list[sqlite3.Row]:
    q = ",".join("?" * len(sess_ids))
    return con.execute(
        f"select id, session_id, role, content, timestamp from messages "
        f"where session_id in ({q}) order by id", sess_ids,
    ).fetchall()


def parse(rows) -> list[dict]:
    out = []
    for r in rows:
        m = SENDER.match((r["content"] or "").strip())
        if not m:
            continue
        out.append({
            "id": r["id"],
            "name": m.group(1).strip(),
            "uid": m.group(2),
            "body": m.group(3).strip(),
            "ts": datetime.datetime.fromtimestamp(float(r["timestamp"])),
        })
    return out


def dedupe(items: list[dict]):
    minute_seen = set()
    by_minute = []
    for x in items:
        key = (x["ts"].strftime("%Y-%m-%d %H:%M"), x["body"])
        if key in minute_seen:
            continue
        minute_seen.add(key)
        by_minute.append(x)

    seen_ids = collections.defaultdict(list)
    final = []
    for x in by_minute:
        if any(x["id"] - prev < 400 for prev in seen_ids[x["body"]]):
            continue
        seen_ids[x["body"]].append(x["id"])
        final.append(x)
    return items, by_minute, final


def report(items: list[dict], focus: str | None) -> dict:
    raw, by_minute, final = dedupe(items)
    out = {
        "funnel": {"raw": len(raw), "minute_dedupe": len(by_minute), "replay_dedupe": len(final)},
        "speakers": collections.Counter(f"{x['name']}|{x['uid']}" for x in final).most_common(),
    }
    if focus:
        mine = [x for x in final if x["uid"] == focus]
        if not mine:
            out["focus"] = f"no lines for uid {focus} after dedupe"
            return out
        lens = sorted(len(x["body"]) for x in mine)
        out["focus"] = {
            "uid": focus,
            "lines": len(mine),
            "median_len": lens[len(lens) // 2],
            "first": mine[0]["ts"].strftime("%Y-%m-%d %H:%M"),
            "last": mine[-1]["ts"].strftime("%Y-%m-%d %H:%M"),
            "per_day": dict(sorted(collections.Counter(
                x["ts"].strftime("%Y-%m-%d") for x in mine).items())),
            "hour_histogram": dict(sorted(collections.Counter(x["ts"].hour for x in mine).items())),
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chat-id", required=True)
    ap.add_argument("--focus", default=None, help="uid to profile")
    ap.add_argument("--db", default="/root/.hermes/state.db")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    con = sqlite3.connect(a.db)
    con.row_factory = sqlite3.Row
    schema_check(con)
    sess = lane_session_ids(con, a.chat_id)
    print(f"# schema OK | lane sessions: {len(sess)}", file=sys.stderr)
    print(json.dumps(report(parse(fetch(con, sess)), a.focus), indent=2, default=str))


if __name__ == "__main__":
    main()
