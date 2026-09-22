#!/usr/bin/env python3
"""fed_witness_decay.py — Witness Decay (F13 verdict 2026-09-22): old truth is drift.
Materializes witness_freshness on every route_health row:
  FRESH <=15m | STALE <=60m | AGING <=24h | EXPIRED >24h
Basis: witness_time, else last_checked (UNATTESTED_LEGACY ages the same).
Idempotent. Cron: */15 * * * *  (ranker enforces EXPIRED at read time)."""
import sqlite3
from datetime import datetime, timezone
DB="/root/.local/share/arifos/token_bank.db"
def classify(ts):
    if not ts: return "EXPIRED"
    try: t=datetime.fromisoformat(ts.replace("Z","+00:00"))
    except ValueError: return "EXPIRED"
    m=(datetime.now(timezone.utc)-t).total_seconds()/60
    return "FRESH" if m<=15 else "STALE" if m<=60 else "AGING" if m<=1440 else "EXPIRED"
def main():
    with sqlite3.connect(DB) as c:
        rows=c.execute("SELECT id, witness_time, last_checked, witness_freshness FROM route_health").fetchall()
        counts={}
        for rid, wt, lc, cur in rows:
            f=classify(wt or lc)
            counts[f]=counts.get(f,0)+1
            if f!=cur:
                c.execute("UPDATE route_health SET witness_freshness=? WHERE id=?",(f,rid))
    print("witness_decay:", counts)
if __name__=="__main__":
    main()
