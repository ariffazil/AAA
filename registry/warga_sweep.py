#!/usr/bin/env python3
"""
Warga Lifecycle Sweep — Cron-triggered lifecycle checks
========================================================
Run periodically to:
  1. Check for agents past their review deadline
  2. Prune TTL-expired records
  3. Emit summary for Hermes cron output

Usage:
  python3 warga_sweep.py            # full sweep
  python3 warga_sweep.py --reviews  # review queue only
  python3 warga_sweep.py --prune    # prune candidates only
"""

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add registry dir to path
sys.path.insert(0, str(Path(__file__).parent))
from warga_manager import (
    list_agents,
    lifecycle_prune,
    GOSSIP_FILE,
    WARGA_FILE,
    _read_jsonl,
)


def check_review_queue() -> dict:
    """Check for agents due for review."""
    agents = list_agents()
    now = datetime.now(UTC)

    overdue = []
    upcoming = []
    for a in agents:
        next_review = a.get("next_review")
        if not next_review:
            continue
        try:
            dt = datetime.fromisoformat(next_review)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=UTC)
            days_until = (dt - now).days
            entry = {
                "agent_id": a["id"],
                "stage": a.get("stage"),
                "authority_band": a.get("authority_band"),
                "days_until_review": days_until,
                "next_review": next_review[:10],
            }
            if days_until < 0:
                overdue.append(entry)
            elif days_until <= 7:
                upcoming.append(entry)
        except (ValueError, TypeError):
            continue

    return {
        "overdue": sorted(overdue, key=lambda x: x["days_until_review"]),
        "upcoming_soon": sorted(upcoming, key=lambda x: x["days_until_review"]),
        "total_agents": len(agents),
    }


def check_prune_candidates() -> dict:
    """Check for TTL-expired records."""
    return lifecycle_prune(dry_run=True)


def check_gossip_freshness() -> dict:
    """Check gossip event freshness."""
    records = _read_jsonl(GOSSIP_FILE)
    now = datetime.now(UTC)

    recent_voids = []
    for rec in records:
        if rec.get("gossip_type") == "VOID":
            broadcast_at = rec.get("broadcast_at")
            if broadcast_at:
                try:
                    dt = datetime.fromisoformat(broadcast_at)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=UTC)
                    days_ago = (now - dt).days
                    if days_ago <= 30:
                        recent_voids.append({
                            "agent_id": rec.get("agent_id"),
                            "days_ago": days_ago,
                            "detail": rec.get("detail", "")[:80],
                            "acks": len(rec.get("acknowledged_by", [])),
                        })
                except (ValueError, TypeError):
                    continue

    return {
        "recent_voids_30d": recent_voids,
        "total_gossip_events": len(records),
    }


def full_sweep() -> str:
    """Run full sweep and return formatted report."""
    reviews = check_review_queue()
    prunes = check_prune_candidates()
    gossip = check_gossip_freshness()

    lines = ["═══ WARGA LIFECYCLE SWEEP ═══", f"  {datetime.now(UTC).isoformat()[:19]}", ""]

    # Review queue
    if reviews["overdue"]:
        lines.append(f"  ⚠️  {len(reviews['overdue'])} OVERDUE reviews:")
        for r in reviews["overdue"]:
            lines.append(f"    {r['agent_id']:20s} │ {r['days_until_review']}d overdue │ {r['stage']}/{r['authority_band']}")
    else:
        lines.append("  ✅ No overdue reviews")

    if reviews["upcoming_soon"]:
        lines.append(f"  📋 {len(reviews['upcoming_soon'])} reviews due within 7 days:")
        for r in reviews["upcoming_soon"]:
            lines.append(f"    {r['agent_id']:20s} │ {r['days_until_review']}d │ {r['stage']}/{r['authority_band']}")

    lines.append(f"  Total agents: {reviews['total_agents']}")
    lines.append("")

    # Prune candidates
    if prunes["candidates"]:
        lines.append(f"  🗑️  {prunes['candidates_found']} prune candidates:")
        for c in prunes["candidates"]:
            lines.append(f"    {c['agent_id']:20s} │ {c['days_overdue']}d overdue │ {c['stage']}")
    else:
        lines.append("  ✅ No prune candidates")

    lines.append("")

    # Gossip
    if gossip["recent_voids_30d"]:
        lines.append(f"  ⚠️  {len(gossip['recent_voids_30d'])} VOID events in last 30 days:")
        for v in gossip["recent_voids_30d"]:
            ack_status = "ACKED" if v["acks"] > 0 else "UNACKED"
            lines.append(f"    {v['agent_id']:20s} │ {v['days_ago']}d ago │ {ack_status} │ {v['detail'][:40]}")
    else:
        lines.append("  ✅ No recent VOID events")

    lines.append(f"  Total gossip events: {gossip['total_gossip_events']}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Warga Lifecycle Sweep")
    parser.add_argument("--reviews", action="store_true", help="Review queue only")
    parser.add_argument("--prune", action="store_true", help="Prune candidates only")
    args = parser.parse_args()

    if args.reviews:
        result = check_review_queue()
        print(json.dumps(result, indent=2))
    elif args.prune:
        result = check_prune_candidates()
        print(json.dumps(result, indent=2))
    else:
        print(full_sweep())


if __name__ == "__main__":
    main()
