#!/usr/bin/env python3
"""Morning brief — one-line status Arif actually reads.

Design principle: ZERO noise. If nothing needs Arif's attention, say so.
If something does, name it concretely. Never narrate. Never pad.

Output: short BM, max 4 lines. Plain text, ready to paste anywhere.
"""
from __future__ import annotations
import json, subprocess, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

RECEIPTS = Path("/root/.local/share/arifos/hermes_hook_receipts.jsonl")
METRICS  = Path("/root/.local/share/arifos/hermes_falsification_metrics.jsonl")
JITU     = "/root/AAA/federation/kernel/jitu.py"

def probe(url, timeout=2):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status, r.read()[:200].decode(errors="ignore")
    except Exception as e:
        return None, str(e)[:60]

def jitu_status():
    try:
        out = subprocess.check_output(["python3", JITU, "status"], text=True, timeout=5)
        return "TRIPPED" if "tripped" in out.lower() and "idle" not in out.lower() else "idle"
    except Exception:
        return "UNKNOWN"

def tail_count(path, predicate, default=0):
    if not path.exists(): return default
    try:
        n = 0
        with open(path) as f:
            for line in f:
                try:
                    if predicate(json.loads(line)): n += 1
                except Exception: pass
        return n
    except Exception: return default

def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    # Organs
    organs = {
        "arifOS":8088, "A-FORGE":7071, "GEOX":8081,
        "WEALTH":18082, "WELL":18083, "arifFlow":7073, "AAA":3001, "FRAME":18085,
        "CHRON":18102
    }
    up, down = [], []
    for name, port in organs.items():
        code, _ = probe(f"http://127.0.0.1:{port}/health")
        (up if code==200 else down).append(name)
    # Receipts (last 1h, derived from file size + recent lines)
    recent_t3 = tail_count(METRICS, lambda d: d.get("event")=="t3_witnessed_audit_only")
    recent_wscar = tail_count(METRICS, lambda d: d.get("event")=="wscar_witnessed_no_block")
    # JITU
    jitu = jitu_status()
    # Build message
    print(f"📡 {now}")
    print(f"Organs: {len(up)}/{len(organs)} live", end="")
    if down: print(f" — down: {', '.join(down)}", end="")
    print()
    print(f"JITU: {jitu}", end="")
    if jitu != "idle":
        print(" ⚠️  Arif decide", end="")
    print()
    if recent_t3 == 0 and recent_wscar == 0:
        print("Audit (all-time): 0 T3, 0 W_scar witnessed-demoted. Tiada apa Arif kena tahu.")
    else:
        print(f"Audit witnessed: {recent_t3} T3, {recent_wscar} W_scar (no-block, log only)")
        if recent_t3 > 0:
            print(f"⚠️  {recent_t3} T3 attempts — review /root/.local/share/arifos/hermes_hook_receipts.jsonl")

if __name__ == "__main__":
    main()
