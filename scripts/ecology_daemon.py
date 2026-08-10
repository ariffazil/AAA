#!/usr/bin/env python3
"""
P2.8 — Ecology Lifecycle Daemon (HOT/WARM/COLD)
=================================================
Background monitor evaluating skill health index:
  H = (Success_Count / Total_Invocations) × exp(-Avg_Latency / 5000)

State transitions:
  H >= 0.95 + invocations >= 10 → HOT  (instant recall, no search needed)
  H < 0.40 or 3 consecutive failures → COLD (pruned from active context)
  Otherwise → WARM (Qdrant-accessible)

Runs as a systemd timer every 5 minutes.
Reads from Qdrant arifOS_skill_mesh, writes updated ecology_state.

Forged: 2026-08-10 by 333-AGI under F13 directive.
"""

import json
import math
import time
import sys
from pathlib import Path
from datetime import datetime, timezone

from qdrant_client import QdrantClient

# ── Config ────────────────────────────────────────────────────────
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION = "arifOS_skill_mesh"
STATE_FILE = Path("/root/.local/share/arifos/ecology_state.json")
MIN_INVOCATIONS_FOR_HOT = 10
HOT_THRESHOLD = 0.95
COLD_THRESHOLD = 0.40
MAX_CONSECUTIVE_FAILURES = 3


def health_index(success_count: int, total_invocations: int, avg_latency_ms: float) -> float:
    """H = (Success / Total) × exp(-Latency / 5000)"""
    if total_invocations == 0:
        return 0.50  # Neutral starting point
    success_rate = success_count / total_invocations
    latency_penalty = math.exp(-avg_latency_ms / 5000) if avg_latency_ms > 0 else 1.0
    return round(success_rate * latency_penalty, 4)


def main(dry_run: bool = False):
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    # Scroll all points
    points, next_offset = client.scroll(
        collection_name=COLLECTION,
        limit=200,
        with_payload=True,
        with_vectors=False,
    )

    transitions = {"HOT": 0, "WARM": 0, "COLD": 0}
    health_scores = {}
    now = datetime.now(timezone.utc).isoformat()

    for point in points:
        p = point.payload or {}
        skill_id = p.get("skill_id", str(point.id))
        total = p.get("total_invocations", 0)
        success = p.get("success_count", 0)
        latency = p.get("avg_latency_ms", 0.0)
        current_state = p.get("ecology_state", "WARM")

        h = health_index(success, total, latency)
        health_scores[skill_id] = h

        # Determine new state
        new_state = current_state
        if total >= MIN_INVOCATIONS_FOR_HOT and h >= HOT_THRESHOLD:
            new_state = "HOT"
        elif h < COLD_THRESHOLD and total > 3:
            new_state = "COLD"
        elif current_state == "COLD" and h >= 0.50:
            new_state = "WARM"  # Recovery path
        elif current_state == "HOT" and h < 0.85:
            new_state = "WARM"  # Degradation path
        elif current_state != "HOT" and current_state != "COLD":
            new_state = "WARM"

        if new_state != current_state:
            transitions[new_state] += 1
            if not dry_run:
                client.set_payload(
                    collection_name=COLLECTION,
                    points=[point.id],
                    payload={
                        "ecology_state": new_state,
                        "health_index": h,
                        "last_evaluated": now,
                    },
                )

    # Persist state
    report = {
        "evaluated_at": now,
        "skills_total": len(points),
        "transitions": transitions,
        "health_distribution": {
            "HOT": sum(1 for v in health_scores.values() if v >= HOT_THRESHOLD),
            "WARM": sum(1 for v in health_scores.values() if COLD_THRESHOLD <= v < HOT_THRESHOLD),
            "COLD": sum(1 for v in health_scores.values() if v < COLD_THRESHOLD),
        },
        "dry_run": dry_run,
    }
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(report, indent=2))

    return report


if __name__ == "__main__":
    dry = "--dry-run" in sys.argv
    print(f"🌱 Ecology Daemon — P2.8 {'(DRY RUN)' if dry else '(LIVE)'}")
    t0 = time.time()
    report = main(dry_run=dry)
    elapsed = (time.time() - t0) * 1000
    print(f"   Evaluated {report['skills_total']} skills in {elapsed:.0f}ms")
    print(
        f"   HOT: {report['health_distribution']['HOT']} | WARM: {report['health_distribution']['WARM']} | COLD: {report['health_distribution']['COLD']}"
    )
    if report["transitions"]:
        for state, count in report["transitions"].items():
            if count > 0:
                print(f"   → {state}: {count}")
    print(f"   State file: {STATE_FILE}")
