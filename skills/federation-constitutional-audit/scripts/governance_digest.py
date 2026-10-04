#!/usr/bin/env python3
"""
governance_digest.py — T2-2 Human Return Path

Produces a daily governance digest for the operator: what the system
did on their behalf today. Designed for cron delivery via Telegram.

Reads:
- /var/lib/arifflow/receipts.jsonl (governance receipts)
- /var/lib/arifflow/override_log.jsonl (override events)
- http://127.0.0.1:7073/health (daemon state)

Outputs a human-readable Telegram-formatted digest to stdout.

Usage:
  python3 governance_digest.py                    # default 24h lookback
  DIGEST_LOOKBACK_HOURS=12 python3 governance_digest.py  # custom lookback

Cron: register with `cronjob action=create schedule="0 22 * * *"` for
nightly delivery. The cron agent runs this script and delivers output.

The acceptance test: can the operator understand what happened in 60 seconds
without grep/cat/tail/journalctl? If yes → loop is closed.

DITEMPA BUKAN DIBERI
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen

RECEIPTS_PATH = "/var/lib/arifflow/receipts.jsonl"
OVERRIDES_PATH = "/var/lib/arifflow/override_log.jsonl"
HEALTH_URL = "http://127.0.0.1:7073/health"
LOOKBACK_HOURS = int(os.environ.get("DIGEST_LOOKBACK_HOURS", "24"))


def load_jsonl(path, since):
    entries = []
    if not os.path.exists(path):
        return entries
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                    ts = r.get("created_at") or r.get("timestamp")
                    if ts:
                        entry_time = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        if entry_time >= since:
                            entries.append(r)
                    else:
                        entries.append(r)
                except Exception:
                    continue
    except Exception:
        pass
    return entries


def get_daemon_health():
    try:
        with urlopen(HEALTH_URL, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return {"status": "unreachable"}


def format_digest(receipts, overrides, health):
    now = datetime.now(timezone(timedelta(hours=8)))
    fq = health.get("fq", {})
    invariants = health.get("invariants", {})
    lines = []
    lines.append(f"**arifFLOW Governance Digest**")
    lines.append(f"_{now.strftime('%A %d %B %Y, %H:%M MYT')}_")
    lines.append("")
    lines.append("**System Pulse**")
    if health.get("status") == "ok":
        lines.append(f"* FQ: {fq.get('quotient', 0):.3f} ({fq.get('verdict', 'UNKNOWN')})")
        lines.append(f"* Receipts: {health.get('receipts', 0)} in-memory")
        lines.append(f"* Enforcement: {invariants.get('cycle_count', 0)} cycles, "
                      f"{invariants.get('hold_count', 0)} holds, "
                      f"{invariants.get('throttle_count', 0)} throttles")
    else:
        lines.append("* Daemon unreachable")
    lines.append("")
    event_count = len(receipts) + len(overrides)
    if event_count == 0:
        lines.append("**Governance Events (24h):** None — system idle.")
    else:
        lines.append(f"**Governance Events ({event_count} in {LOOKBACK_HOURS}h)**")
        lines.append("")
        if receipts:
            by_step = {}
            by_actor = {}
            for r in receipts:
                st = r.get("step_type", "Unknown")
                by_step[st] = by_step.get(st, 0) + 1
                actor = r.get("actor_id", "unknown")
                by_actor[actor] = by_actor.get(actor, 0) + 1
            lines.append("* Receipts:")
            for st, count in sorted(by_step.items()):
                lines.append(f"  - {st}: {count}")
            lines.append("* Top actors:")
            for actor, count in sorted(by_actor.items(), key=lambda x: -x[1])[:5]:
                lines.append(f"  - {actor}: {count} steps")
            with_intent = [r for r in receipts if r.get("intent_reason")]
            if with_intent:
                lines.append("")
                lines.append("**WHY Bridge (receipts with intent):**")
                for r in with_intent[:5]:
                    lines.append(f"* {r.get('actor_id', '?')}: _{r.get('intent_reason', '')}_")
        if overrides:
            lines.append("")
            lines.append("* **Override Events:**")
            for o in overrides:
                lines.append(f"  - {o.get('timestamp', '?')}: {o.get('reason', '?')[:60]}")
                lines.append(f"    Expires: {o.get('expiry', '?')}")
    lines.append("")
    lines.append("*DITEMPA BUKAN DIBERI*")
    return "\n".join(lines)


def main():
    since = datetime.now(timezone.utc) - timedelta(hours=LOOKBACK_HOURS)
    receipts = load_jsonl(RECEIPTS_PATH, since)
    overrides = load_jsonl(OVERRIDES_PATH, since)
    health = get_daemon_health()
    print(format_digest(receipts, overrides, health))


if __name__ == "__main__":
    main()
