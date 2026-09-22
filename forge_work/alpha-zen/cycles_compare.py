#!/usr/bin/env python3
"""cycles_compare.py — drift detector for ALPHA-ZEN cycles.jsonl

Appends a compact diff to cycles_diff.jsonl, one line per compare run.

Each line answers:
  What changed between today's card and the reference card?

References: N-1 (yesterday same mode), N-7 (week ago), N-30 (month ago).
Only compares when reference exists. Skips silently otherwise.

This is NOT a calibration oracle. It is a core-sample.
Drift in source_count, signal_count, gate, render dimensions = real change.
Drift in label/subject = rhetorical change (often noise; rarely signal).
"""

from __future__ import annotations
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

CYCLES = Path("/root/AAA/forge_work/alpha-zen/cycles.jsonl")
DIFF = Path("/root/AAA/forge_work/alpha-zen/cycles_diff.jsonl")

# Only fields where drift = real signal
HARD_FIELDS = ("source_count", "signal_count", "selected_count",
               "render_status", "gate", "dimensions", "rejection_tracking")
SOFT_FIELDS = ("style",)  # mode+date are key


def load() -> list[dict]:
    if not CYCLES.exists():
        return []
    out = []
    for line in CYCLES.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def find(cycles: list[dict], mode: str, target: date) -> dict | None:
    """Find the cycle closest to (mode, target date)."""
    best = None
    best_delta = None
    for c in cycles:
        if c.get("mode") != mode:
            continue
        rt = c.get("render_time", "")
        try:
            d = datetime.fromisoformat(rt.replace("Z", "+00:00")).date()
        except Exception:
            continue
        delta = abs((d - target).days)
        if best is None:
            best = c
            best_delta = delta
        elif best_delta is None or delta < best_delta:
            best = c
            best_delta = delta
    if best is not None and best_delta is not None and best_delta <= 35:
        return best
    return None


def diff(today: dict, ref: dict, window: str) -> dict:
    """Compact diff: only flag changes."""
    changes = {}
    for f in HARD_FIELDS + SOFT_FIELDS:
        if today.get(f) != ref.get(f):
            changes[f] = {"today": today.get(f), "ref": ref.get(f)}
    return {
        "window": window,
        "today_cycle": today.get("cycle_id"),
        "ref_cycle": ref.get("cycle_id"),
        "today_render_time": today.get("render_time"),
        "ref_render_time": ref.get("render_time"),
        "changes": changes,
        "drift_score": len(changes),
    }


def main() -> int:
    cycles = load()
    if not cycles:
        print("cycles.jsonl empty or missing — nothing to compare")
        return 0
    today = cycles[-1]
    mode = today.get("mode")
    if mode is None:
        print("today has no mode; abort")
        return 1
    mode = str(mode)
    rt = today.get("render_time", "")
    try:
        today_date = datetime.fromisoformat(rt.replace("Z", "+00:00")).date()
    except Exception:
        print("today has no parseable render_time; abort")
        return 1

    out: list[dict] = []
    for days_back, window in [(1, "N-1"), (7, "N-7"), (30, "N-30")]:
        ref = find(cycles, mode, today_date - timedelta(days=days_back))
        if ref is None:
            out.append({
                "window": window,
                "today_cycle": today.get("cycle_id"),
                "today_render_time": today.get("render_time"),
                "ref_cycle": None,
                "changes": {},
                "drift_score": 0,
                "note": "no reference",
            })
            continue
        out.append(diff(today, ref, window))

    line = json.dumps({
        "diff_run_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "today_cycle": today.get("cycle_id"),
        "diffs": out,
    }, ensure_ascii=False)
    with DIFF.open("a") as fh:
        fh.write(line + "\n")
    print(f"diff logged → {DIFF}")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())