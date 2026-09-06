#!/usr/bin/env python3
"""
fed_health_set.py — canonical probe→health writer (Phase 0 fix #1, 2026-09-07)

SCAR-context: probes historically wrote findings into providers.notes only.
The router's health gate reads route_health — so a probed-dead provider kept
rendering LIVE (witnessed: qwen-token-plan-team ranked #2 while quota EXHAUSTED).
This tool is THE one-liner probes/agents must use to record probe truth:

    python3 fed_health_set.py qwen-token-plan-team probe DEAD "monthly quota exhausted"
    python3 fed_health_set.py minimax probe LIVE "resubscribed 2026-09-06"
    python3 fed_health_set.py deepseek deepseek-v4-pro RATE_LIMITED "429 window"

Writes route_health (status + last_checked) AND appends a PROBED_ note to
providers.notes atomically. Fail-closed on bad status.
"""
import sqlite3
import sys
from datetime import datetime, timezone

FED_STATE_DB = "/root/.local/share/arifos/token_bank.db"
VALID_STATUS = {"LIVE", "DEGRADED", "RATE_LIMITED", "DEAD", "AUTH_FAIL"}


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    provider, model, status = sys.argv[1], sys.argv[2], sys.argv[3].upper()
    note = sys.argv[4] if len(sys.argv) > 4 else ""
    if status not in VALID_STATUS:
        print(f"FAIL-CLOSED: status must be one of {sorted(VALID_STATUS)}, got {status}")
        return 2
    now = datetime.now(timezone.utc).isoformat()
    stamp = f"PROBED_{now[:10]}: {status}"
    if note:
        stamp += f" — {note}"
    with sqlite3.connect(FED_STATE_DB) as conn:
        conn.execute(
            """INSERT INTO route_health (provider_name, model_id, status, last_checked)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(provider_name, model_id)
               DO UPDATE SET status=excluded.status, last_checked=excluded.last_checked""",
            (provider, model, status, now),
        )
        conn.execute(
            "UPDATE providers SET notes = COALESCE(notes,'') || ' | ' || ? WHERE provider_name = ?",
            (stamp, provider),
        )
    print(f"OK: route_health[{provider}/{model}] = {status}; note appended.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
