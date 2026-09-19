#!/usr/bin/env python3
"""Attention signal — only fire when Arif actually needs to decide something.

Triggers (real, not pattern-matching):
- JITU TRIPPED (sovereign breaker active)
- Any organ DOWN for >2 probes (real outage, not 1 hiccup)
- Failed seal attempt (arifOS judge returned VOID with no fallback)
- Empty receipt trail for >2h during active session (silent death)

Output: single line, BM, includes the action Arif needs to take.
Nothing else. No narration. No "everything is fine". No noise.
"""
from __future__ import annotations
import json, subprocess, sys, urllib.request, time
from pathlib import Path
from datetime import datetime, timezone

def jitu_state():
    try:
        out = subprocess.check_output(["python3", "/root/AAA/federation/kernel/jitu.py", "status"], text=True, timeout=5)
        return "TRIPPED" if "tripped" in out.lower() and "idle" not in out.lower() else "IDLE"
    except Exception:
        return "UNKNOWN"

def probe(url, timeout=2):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r: return r.status
    except Exception: return None

def main():
    signals = []
    # 1. JITU
    jitu = jitu_state()
    if jitu == "TRIPPED":
        signals.append("🛑 JITU tripped — ada agent tengah halt. Lihat /root/.local/share/arifos/jitu/trip.json")
    # 2. Organs (2 consecutive failures)
    organs = {"arifOS":8088,"A-FORGE":7071,"GEOX":8081,"WEALTH":18082,"WELL":18083,"arifFlow":7073,"AAA":3001,"FRAME":18085}
    dead = [n for n,p in organs.items() if probe(f"http://127.0.0.1:{p}/health") != 200]
    if dead:
        signals.append(f"🔴 Down: {', '.join(dead)} — federation degraded")
    # 3. Empty trail (signal: agents silently dying)
    trail = Path("/root/.local/share/arifos/hermes_hook_receipts.jsonl")
    if trail.exists():
        mtime = trail.stat().st_mtime
        age_min = (time.time() - mtime) / 60
        if age_min > 120:
            signals.append(f"⚠️  Trail stale {age_min:.0f}m — agent mungkin silent. Cek organ.")
    # Output
    if not signals:
        print(f"✅ {datetime.now(timezone.utc).strftime('%H:%M UTC')} — diam. Tiada apa Arif kena buat.")
        return 0
    print(f"📢 {datetime.now(timezone.utc).strftime('%H:%M UTC')} — Arif decide:")
    for s in signals: print(f"  {s}")
    return 1

if __name__ == "__main__":
    sys.exit(main())
