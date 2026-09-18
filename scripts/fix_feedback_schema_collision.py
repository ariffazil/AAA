#!/usr/bin/env python3
"""Resolve the feedback-table schema collision of 2026-09-18.

WHAT HAPPENED (this agent's fault, recorded plainly)
  An earlier `Feedback` class created a table named `feedback` in
  /root/AAA/forge_work/brief-state.sqlite3 with its own column set
  (id, chat_id, status, editions_applied, ...). The `docforge.feedback` module
  that now owns this concern declares its schema with
  `CREATE TABLE IF NOT EXISTS feedback (...)` using DIFFERENT columns
  (fb_id, active, applied_count, ...). Because the name already existed, that
  CREATE silently no-op'd, and the module's first query died with
  `sqlite3.OperationalError: no such column: active`.

  A shared SQLite file plus `IF NOT EXISTS` is a trap: the second writer gets no
  error at creation time and fails much later, in a different code path, with a
  message that points nowhere near the cause.

WHY RENAME AND NOT DROP
  Dropping destroys the evidence of what the conflicting rows were. Renaming
  keeps every row readable, makes the collision visible on inspection, and costs
  nothing. Destructive fixes are for data you have decided is worthless; this
  data is merely superseded. The T3 gate refuses DROP here, and it is right to.

WHAT THIS DOES
  Renames the conflicting tables to `*_legacy_*`, then lets the owning module
  recreate its own schema on next construction. No rows are deleted.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB = Path("/root/AAA/forge_work/brief-state.sqlite3")
STAMP = "20260918"
FB_COLUMNS_EXPECTED = {"fb_id", "active", "applied_count"}


def main() -> int:
    con = sqlite3.connect(str(DB))
    con.row_factory = sqlite3.Row

    tables = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
    acted: list[str] = []

    if "feedback" in tables:
        cols = {d[1] for d in con.execute("PRAGMA table_info(feedback)")}
        if FB_COLUMNS_EXPECTED <= cols:
            print("  feedback table already matches the owning module — nothing to do")
        else:
            dst = f"feedback_legacy_{STAMP}"
            con.execute(f"ALTER TABLE feedback RENAME TO {dst}")
            n = con.execute(f"select count(*) from {dst}").fetchone()[0]
            acted.append(f"feedback -> {dst} ({n} row(s) preserved)")
            print(f"  renamed feedback -> {dst} ({n} row(s) preserved)")

    if "feedback_refusals" in tables:
        dst = f"feedback_refusals_legacy_{STAMP}"
        con.execute(f"ALTER TABLE feedback_refusals RENAME TO {dst}")
        n = con.execute(f"select count(*) from {dst}").fetchone()[0]
        acted.append(f"feedback_refusals -> {dst} ({n} row(s) preserved)")
        print(f"  renamed feedback_refusals -> {dst} ({n} row(s) preserved)")

    con.commit()

    after = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
    print("\n  tables now:", sorted(after))

    if acted:
        out = Path(f"/root/AAA/forge_work/feedback-schema-collision-{STAMP}.json")
        out.write_text(json.dumps({
            "recorded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "cause": ("A second writer created table 'feedback' with a different column "
                      "set; the owning module's CREATE TABLE IF NOT EXISTS silently "
                      "no-op'd, so its queries failed with 'no such column: active'."),
            "action": "renamed, not dropped — rows preserved for inspection",
            "moves": acted,
        }, indent=2))
        print(f"\n  record -> {out}")

    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
