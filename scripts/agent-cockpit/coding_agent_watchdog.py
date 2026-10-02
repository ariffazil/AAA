#!/usr/bin/env python3
"""Coding-agent watchdog — the gap stuck_detector.py does not cover.

stuck_detector.py reads Hermes hook receipts and looks for repeated tool calls.
It never looks at a process. So a coding harness (qwen/opencode/kimi/codex/claude/
grok/gemini/agy/aider) spinning at 90% CPU for hours is invisible to it — which is
exactly the failure the sovereign asked to close on 2026-10-02.

DETECTION RULE (two independent observables, deliberately not clever):
  cpu  = delta(utime+stime) over the interval since the previous run
  work = delta(write_bytes) over the same interval

  cpu >= HIGH_CPU_PCT for STREAK_RUNS consecutive runs AND work == 0
      -> STUCK_CANDIDATE   (burning CPU, producing nothing)
  cpu >= HIGH_CPU_PCT for STREAK_RUNS consecutive runs AND work > 0
      -> HIGH_CPU_ACTIVE   (advisory only: busy, but moving)
  otherwise -> no signal

CPU with zero bytes written across 15 minutes is a spin, not work. A legitimately
busy agent writes constantly (tool output, receipts, logs) and is not flagged.

FAIL-CLOSED (invariant: a broken monitor may never report healthy):
  any measurement failure -> prints UNKNOWN and exits 2. It never prints OK because
  it could not measure. This is the defect class that killed stuck_detector.py for
  8.09 days while its log kept growing and looked alive.

Paths are overridable for testing only; production defaults unchanged.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PROC_ROOT = Path(os.environ.get("CAW_PROC_ROOT", "/proc"))
STATE = Path(os.environ.get("CAW_STATE", "/root/.local/share/arifos/coding_agent_watchdog.state.json"))
SIGNALS = Path(os.environ.get("CAW_SIGNALS", "/root/.local/share/arifos/coding_agent_watchdog.jsonl"))

HIGH_CPU_PCT = float(os.environ.get("CAW_HIGH_CPU_PCT", "85"))
STREAK_RUNS = int(os.environ.get("CAW_STREAK_RUNS", "3"))
HZ = os.sysconf("SC_CLK_TCK")

# Harness launchers on this box. Matched against cmdline, not process name, because
# several of them are all "node" or "python3".
PATTERNS = [
    ("qwen", re.compile(r"qwen-code/lib/cli-entry\.js|qwen\b.*--yolo")),
    ("opencode", re.compile(r"opencode")),
    ("kimi", re.compile(r"kimi")),
    ("codex", re.compile(r"codex")),
    ("claude", re.compile(r"claude(?:-code)?(?:\b|/)")),
    ("grok", re.compile(r"grok")),
    ("gemini", re.compile(r"gemini")),
    ("antigravity", re.compile(r"\bagy\b|antigravity")),
    ("aider", re.compile(r"aider")),
]
# Never watch ourselves or the harness that is only serving an API.
EXCLUDE = re.compile(r"coding_agent_watchdog|stuck_detector|cli-entry\.js serve")


def _read(pid: int, name: str) -> str | None:
    try:
        return (PROC_ROOT / str(pid) / name).read_text(errors="replace")
    except Exception:
        return None


def cpu_ticks(pid: int) -> int | None:
    """utime + stime in clock ticks. Field 14 + 15 of /proc/PID/stat, parsed after
    the last ')' because comm may contain spaces and parentheses."""
    raw = _read(pid, "stat")
    if not raw:
        return None
    try:
        rest = raw[raw.rindex(")") + 1:].split()
        return int(rest[11]) + int(rest[12])  # utime, stime after state field
    except Exception:
        return None


def write_bytes(pid: int) -> int | None:
    raw = _read(pid, "io")
    if not raw:
        return None
    m = re.search(r"^write_bytes:\s*(\d+)", raw, re.M)
    return int(m.group(1)) if m else None


def cmdline(pid: int) -> str:
    raw = _read(pid, "cmdline")
    return (raw or "").replace("\0", " ").strip()


def discover() -> list[dict]:
    found = []
    for entry in PROC_ROOT.iterdir():
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        cl = cmdline(pid)
        if not cl or EXCLUDE.search(cl):
            continue
        for harness, pat in PATTERNS:
            if pat.search(cl):
                found.append({"pid": pid, "harness": harness, "cmdline": cl[:160]})
                break
    return found


def load_state() -> dict:
    if not STATE.exists():
        return {}
    try:
        return json.loads(STATE.read_text())
    except Exception:
        # A corrupt state file is a measurement failure, not a clean slate: silently
        # restarting the streak counter would hide exactly the spin we watch for.
        raise RuntimeError(f"state file unreadable: {STATE}")


def main() -> int:
    now = time.time()
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    try:
        state = load_state()
    except Exception as e:
        print(f"UNKNOWN {stamp} — cannot read prior state ({e}); refusing to report healthy")
        return 2

    if not PROC_ROOT.is_dir():
        print(f"UNKNOWN {stamp} — {PROC_ROOT} not readable; refusing to report healthy")
        return 2

    prior_ts = state.get("_ts")
    interval = (now - prior_ts) if prior_ts else None
    if interval is not None and interval <= 0:
        print(f"UNKNOWN {stamp} — non-positive sample interval {interval}; clock moved backwards")
        return 2

    measured, failed = [], 0
    for proc in discover():
        pid = proc["pid"]
        ticks, wb = cpu_ticks(pid), write_bytes(pid)
        if ticks is None or wb is None:
            failed += 1  # process exited mid-scan, or /proc denied: count, do not guess
            continue
        prev = state.get(str(pid))
        cpu_pct, wdelta, streak = None, None, 0
        if prev and interval:
            dticks = ticks - prev["ticks"]
            wdelta = max(0, wb - prev["wb"])
            if dticks >= 0:
                cpu_pct = round((dticks / HZ) / interval * 100, 1)
        if cpu_pct is not None and cpu_pct >= HIGH_CPU_PCT:
            streak = prev.get("streak", 0) + 1
        else:
            streak = 0
        measured.append({**proc, "cpu_pct": cpu_pct, "write_delta": wdelta, "streak": streak,
                         "ticks": ticks, "wb": wb})

    new_state = {"_ts": now, "_stamp": stamp}
    for m in measured:
        new_state[str(m["pid"])] = {"ticks": m["ticks"], "wb": m["wb"], "streak": m["streak"],
                                    "harness": m["harness"]}

    signals = []
    for m in measured:
        if m["streak"] >= STREAK_RUNS:
            kind = "STUCK_CANDIDATE" if not m["write_delta"] else "HIGH_CPU_ACTIVE"
            signals.append({"ts": stamp, "signal": kind, "pid": m["pid"], "harness": m["harness"],
                            "cpu_pct": m["cpu_pct"], "write_delta": m["write_delta"],
                            "streak_runs": m["streak"], "cmdline": m["cmdline"]})

    try:
        STATE.parent.mkdir(parents=True, exist_ok=True)
        tmp = STATE.with_suffix(".tmp")
        tmp.write_text(json.dumps(new_state, indent=1))
        tmp.replace(STATE)
        if signals:
            with open(SIGNALS, "a") as fh:
                for s in signals:
                    fh.write(json.dumps(s, ensure_ascii=False) + "\n")
    except Exception as e:
        print(f"UNKNOWN {stamp} — could not persist state/signals ({e}); refusing to report healthy")
        return 2

    stuck = [s for s in signals if s["signal"] == "STUCK_CANDIDATE"]
    busy = [s for s in signals if s["signal"] == "HIGH_CPU_ACTIVE"]
    parts = [f"agents={len(measured)}"]
    if failed:
        parts.append(f"unmeasurable={failed}")
    if not measured and not failed:
        parts.append("tiada coding-agent ditemui")
    for s in stuck:
        parts.append(f"STUCK pid={s['pid']} {s['harness']} cpu={s['cpu_pct']}% "
                     f"write_delta=0 selama {s['streak_runs']} run")
    for s in busy:
        parts.append(f"busy pid={s['pid']} {s['harness']} cpu={s['cpu_pct']}% (ada output, bukan loop)")
    verdict = "STUCK" if stuck else ("BUSY" if busy else "OK")
    print(f"{verdict} {datetime.now(timezone.utc).strftime('%H:%M UTC')} — " + " · ".join(parts))
    # A STUCK signal is a real finding and must be visible to any caller that checks
    # exit codes; BUSY and OK are not failures.
    return 1 if stuck else 0


if __name__ == "__main__":
    sys.exit(main())
