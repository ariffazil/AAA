#!/usr/bin/env python3
"""Federated scheduler substrate sweep -- read-only.

Enumerates ALL four places scheduled work can live, so "is cron running?" is
answered from evidence rather than from one host's local book:

  1. local Hermes gateway book  (~/.hermes/cron/jobs.json) + state/paused_reason
  2. this host's scheduler      (hermes cron status)
  3. system cron                (/etc/cron.d, crontab -l)
  4. proof of life              (journalctl CMD histogram for today)

Substrate 4 cannot lie: a configured entry with no CMD line in today's journal
never ran. Peer hosts may be passed as arguments to read their job books and
check whether their gateway unit is supervised.

Usage:
    python3 scheduler_substrate_sweep.py
    python3 scheduler_substrate_sweep.py 100.64.0.5 100.64.0.4
"""

from __future__ import annotations

import collections
import json
import os
import pathlib
import re
import subprocess
import sys

BOOK = pathlib.Path(os.path.expanduser("~/.hermes/cron/jobs.json"))
SSH_OPTS = ["-o", "BatchMode=yes", "-o", "ConnectTimeout=8"]


def run(cmd: list[str], timeout: int = 45) -> str:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (p.stdout or "") + (p.stderr or "")
    except Exception as e:  # missing binary, timeout, ssh refusal
        return f"<{type(e).__name__}: {e}>"


def summarize(doc, label: str) -> None:
    jobs = doc if isinstance(doc, list) else (doc or {}).get("jobs", [])
    if not jobs:
        print(f"  {label}: no jobs in this book")
        return
    on = sum(1 for j in jobs if j.get("enabled"))
    print(f"  {label}: {len(jobs)} jobs, {on} enabled")
    for j in jobs:
        flag = "ON " if j.get("enabled") else "off"
        state = str(j.get("state"))[:20]
        name = str(j.get("name"))[:40]
        why = j.get("paused_reason") or ""
        print(f"  {flag} {state:21} {name:42} {why}")


def main() -> None:
    peers = sys.argv[1:]
    print(f"=== scheduler sweep at {run(['date', '-Is']).strip()} ===\n")

    print("--- 1. local gateway book ---")
    try:
        summarize(json.loads(BOOK.read_text()), str(BOOK))
    except Exception as e:
        print(f"  unreadable at {BOOK} ({type(e).__name__}: {e})")

    print("\n--- 2. this host's scheduler ---")
    print("  " + run(["hermes", "cron", "status"]).strip().replace("\n", "\n  "))

    print("\n--- 3. system cron ---")
    cd = pathlib.Path("/etc/cron.d")
    names = sorted(p.name for p in cd.iterdir()) if cd.is_dir() else []
    print("  /etc/cron.d: " + (", ".join(names) if names else "(absent or empty)"))
    print("  crontab -l: " + (run(["crontab", "-l"]).strip() or "(empty)"))

    print("\n--- 4. proof of life (what actually forked today) ---")
    journal = run(["journalctl", "-u", "cron", "--since", "today", "--no-pager"], timeout=60)
    hist = collections.Counter(re.findall(r"CMD \((.*?)\)", journal))
    if hist:
        for cmd, n in hist.most_common(20):
            print(f"  {n:4}  {cmd[:110]}")
    else:
        print("  (no CMD entries -- cron forked nothing today, or the journal is unreadable)")

    for peer in peers:
        print(f"\n--- peer {peer}: gateway book ---")
        raw = run(["ssh", *SSH_OPTS, peer, "cat /root/.hermes/cron/jobs.json"])
        try:
            summarize(json.loads(raw), f"{peer}:~/.hermes/cron/jobs.json")
        except Exception:
            print(f"  could not read/parse ({raw.strip()[:160]})")
        print(f"--- peer {peer}: supervision + heartbeat ---")
        unit = run(["ssh", *SSH_OPTS, peer, "systemctl is-enabled hermes-gateway 2>&1 || true"]).strip()
        print(f"  systemctl is-enabled hermes-gateway: {unit or '(no output)'}")
        hb = run(["ssh", *SSH_OPTS, peer,
                  "stat -c '%y %n' /root/.hermes/cron/ticker_heartbeat 2>/dev/null || echo '(no heartbeat file)'"]).strip()
        print(f"  heartbeat: {hb}")

    print("\nReminder: substrate 4 is authoritative for \"did it run\". A configured entry with")
    print("no CMD line today never ran, regardless of what any status command reports.")


if __name__ == "__main__":
    main()
