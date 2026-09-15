#!/usr/bin/env python3
"""Curator-loop meter — does the Hermes self-improvement loop actually learn, or pose?

Three axes, three sources, no new state invented:
  ATTEMPTS  gateway journal    -- refusals + their reason class (rate of blocked work)
  BLOCKED   skill ledger       -- action="refused" rows: WHICH skill was blocked, durably
  LANDED    skill ledger       -- create/patch/write_file rows: what the curator really changed

Usage:
  python3 /root/AAA/scripts/curator-loop-meter.py            # today (MYT), human summary
  python3 /root/AAA/scripts/curator-loop-meter.py --days 3   # wider journal window
  python3 /root/AAA/scripts/curator-loop-meter.py --json     # machine-readable

Exit code is 1 when a blocked target REPEATS within the window (the falsifiable test:
a repeating target means the loop is posing, and the boundary declaration needs fixing,
not the counter).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

LEDGER = Path("/root/.hermes/skills/.curator_ledger.jsonl")
PENDING_MEM = Path("/root/.hermes/pending/memory")
SERVICE = "hermes-asi-gateway"
MYT = timezone(timedelta(hours=8))
MUTATIONS = {"create", "patch", "write_file", "edit", "delete", "remove_file", "rollback"}


def pending_memory() -> dict:
    """Staged memory proposals awaiting a human decision.

    This pile is invisible in every other readout and grows silently: 122 proposals
    accumulated in 5 days before anyone looked. Surface it on every run so the
    approval gate stays a queue instead of a landfill.
    """
    files = [p for p in PENDING_MEM.glob("*.json")] if PENDING_MEM.exists() else []
    if not files:
        return {"count": 0, "oldest_days": 0.0, "targets": {}}
    now = datetime.now(timezone.utc).timestamp()
    ages = [(now - p.stat().st_mtime) / 86400 for p in files]
    targets: Counter = Counter()
    for p in files:
        try:
            targets[(json.loads(p.read_text(encoding="utf-8")).get("payload") or {}).get("target", "?")] += 1
        except Exception:
            targets["unreadable"] += 1
    return {"count": len(files), "oldest_days": round(max(ages), 1), "targets": dict(targets)}


def journal_scan(since: str) -> tuple[Counter, Counter, Counter]:
    """Refusal reason classes, offending skill names, and landed reviews from the journal."""
    out = subprocess.run(["journalctl", "-u", SERVICE, "--since", since, "--no-pager"],
                         capture_output=True, text=True, errors="replace").stdout
    reasons: Counter = Counter()
    targets: Counter = Counter()
    reviews: Counter = Counter()
    for line in out.splitlines():
        if "Self-improvement review:" in line:
            for skill in _review_skills(line):
                reviews[skill] += 1
        if "Refusing background curator" not in line:
            continue
        if "for bundled skill" in line:
            reasons["bundled"] += 1
        elif "not curator-managed" in line:
            reasons["user_owned"] += 1
        elif "for pinned skill" in line:
            reasons["pinned"] += 1
        elif "hub-installed" in line:
            reasons["hub"] += 1
        else:
            reasons["other"] += 1
        if "skill '" in line:
            target = line.split("skill '", 1)[-1].split("'", 1)[0]
            if target:
                targets[target] += 1
    return reasons, targets, reviews


def _review_skills(line: str) -> set[str]:
    """Skill names off a 'Self-improvement review: ...' summary line."""
    body = line.split("Self-improvement review:", 1)[-1]
    names: set[str] = set()
    for chunk in body.split("·"):
        if "'" in chunk:
            names.add(chunk.split("'")[1])
    return names


def ledger_rows() -> tuple[Counter, Counter, Counter]:
    """Blocked targets (refused rows) and landed work (mutation rows) from the ledger."""
    refused: Counter = Counter()
    landed: Counter = Counter()
    actions: Counter = Counter()
    if not LEDGER.exists():
        return refused, landed, actions
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        action = row.get("action", "?")
        actions[action] += 1
        if action == "refused":
            refused[row.get("skill", "?")] += 1
        elif action in MUTATIONS:
            landed[row.get("skill", "?")] += 1
    return refused, landed, actions


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=float, default=1.0, help="journal window, days back (default 1)")
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    ap.add_argument("--write", metavar="PATH", help="also write the full report to PATH")
    args = ap.parse_args()

    hours = max(1, int(round(args.days * 24)))
    reasons, attempted, reviews = journal_scan(f"-{hours}h")
    refused, landed, actions = ledger_rows()
    pending = pending_memory()

    report = {
        "captured_at_myt": datetime.now(MYT).isoformat(timespec="seconds"),
        "window": f"-{hours}h on service {SERVICE}",
        "attempts_refused_in_window": sum(reasons.values()),
        "attempts_by_reason": dict(reasons),
        "attempted_targets_journal": dict(attempted.most_common()),
        "reviews_landed_in_window": sum(reviews.values()),
        "reviews_by_skill_journal": dict(reviews.most_common(15)),
        "blocked_targets_ledger_all_time": dict(refused.most_common()),
        "landed_skills_ledger_all_time": {k: v for k, v in landed.most_common(10)},
        "ledger_actions": dict(actions),
        "pending_memory_proposals": pending,
        "repeating_targets": {k: v for k, v in attempted.items() if v > 1},
        "verdict": ("POSING — a blocked target repeated in the window; fix the boundary "
                    "declaration, not the counter"
                    if any(v > 1 for v in attempted.values()) else "OK — no repeated targets"),
    }
    if pending["count"] > 20 or pending["oldest_days"] > 7:
        report["verdict"] += (f" · ATTENTION: {pending['count']} memory proposals staged, "
                              f"oldest {pending['oldest_days']}d — run the redemption procedure")

    if args.write:
        Path(args.write).write_text(json.dumps(report, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"curator-loop meter · {report['captured_at_myt']} · window {report['window']}")
        print(f"  reviews landed   : {report['reviews_landed_in_window']}")
        print(f"  attempts refused : {report['attempts_refused_in_window']}  "
              f"{dict(reasons) if reasons else ''}")
        print(f"  blocked (ledger) : {sum(refused.values())} rows "
              f"{dict(refused.most_common(6))}")
        print(f"  landed (ledger)  : {sum(landed.values())} mutations on {len(landed)} skills")
        print(f"  memory proposals : {pending['count']} staged "
              f"(oldest {pending['oldest_days']}d) {pending['targets'] or ''}")
        print(f"  repeating targets: {report['repeating_targets'] or 'none'}")
        print(f"  verdict          : {report['verdict']}")
        if args.write:
            print(f"  written          : {args.write}")
    return 1 if report["repeating_targets"] else 0


if __name__ == "__main__":
    sys.exit(main())
