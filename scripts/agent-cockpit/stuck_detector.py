#!/usr/bin/env python3
"""Stuck-agent detector — catches the 'bangang' pattern (agent looping tanpa progress).

Detection rule (simple, not smart):
- Look at /root/.claude/sessions/<active>/.jsonl OR Hermes trail
- If same tool_name appears ≥3 times in last 2 minutes AND no T2 success receipt between
  → SIGNAL: "agent mungkin stuck"
- That's it. Don't try to be clever.

Output: appends to /root/.local/share/arifos/stuck_signals.jsonl
        emits single-line BM summary to stdout
"""
from __future__ import annotations
import json, time
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter, deque

RECEIPTS = Path("/root/.local/share/arifos/hermes_hook_receipts.jsonl")
SIGNALS  = Path("/root/.local/share/arifos/stuck_signals.jsonl")
WINDOW_SEC = 120   # 2 min
REPEAT_THRESHOLD = 3

def main():
    if not RECEIPTS.exists():
        print("✅ No trail — nothing to detect")
        return 0
    now = time.time()
    recent = deque()
    with open(RECEIPTS) as f:
        # tail last 200 lines (cheap, bounded)
        lines = deque(f, maxlen=200)
    for line in lines:
        try:
            d = json.loads(line)
            ts_str = d.get("timestamp","")
            if not ts_str: continue
            ts = datetime.fromisoformat(ts_str.replace("Z","+00:00")).timestamp()
            if now - ts > WINDOW_SEC: continue
            recent.append(d)
        except Exception: pass
    # Count repeats by (tool, classification) — same tool alone ≠ stuck (could be normal ops)
    pairs = Counter((r.get("tool","?"), r.get("classification","?")) for r in recent)
    # stuck = same pair ≥3 AND every intervening event is a block/hold (no pass between)
    stuck = []
    for (tool, cls), n in pairs.items():
        if n < REPEAT_THRESHOLD or tool == "?": continue
        # Check if any pass receipt exists in window for this tool
        passes = sum(1 for r in recent if r.get("tool")==tool and r.get("event","").endswith("witnessed") and "blocked" not in r.get("event",""))
        if passes == 0 and n >= REPEAT_THRESHOLD:
            stuck.append((tool, cls, n))
    if not stuck:
        print(f"✅ {datetime.now(timezone.utc).strftime('%H:%M UTC')} — agent aktif normal")
        return 0
    # Signal!
    msg = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "stuck": [{"tool": t, "classification": c, "count": n} for t,c,n in stuck],
        "window_sec": WINDOW_SEC
    }
    with open(SIGNALS, "a") as f:
        f.write(json.dumps(msg) + "\n")
    print(f"⚠️  {datetime.now(timezone.utc).strftime('%H:%M UTC')} — Agent mungkin stuck")
    for tool, cls, n in stuck:
        print(f"   {tool} ({cls}): {n}× tanpa pass dalam {WINDOW_SEC}s")
    return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
