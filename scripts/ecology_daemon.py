#!/usr/bin/env python3
"""
P2.8 — Ecology Lifecycle Daemon (HOT/WARM/COLD)
=================================================
Background monitor evaluating skill health index:
  H = (Success_Count / Total_Invocations) × exp(-Avg_Latency / 5000)

State transitions:
  H >= 0.95 + invocations >= 10 → HOT  (instant recall, no search needed)
  H < 0.40 or 3 consecutive failures → COLD (pruned from active context)
  Otherwise → WARM (search-accessible)

Runs as a systemd timer every 5 minutes.
Reads skill-mesh records via FederationMemory.recall (class=skill_mesh),
writes ecology state transitions to the federation_shared memory class
with ecology-specific tags (alignment doctrine §4 — agents never touch
the vector store directly).

Forged: 2026-08-10 by 333-AGI under F13 directive.
Migrated 2026-09-12 to federation_memory_adapter (F13 SOVEREIGN
directive — /root/AAA/governance/FEDERATION_MEMORY_ALIGNMENT_DOCTRINE.md).
"""

import json
import math
import os
import time
import sys
from pathlib import Path
from datetime import datetime, timezone

_FEDERATION_DIR = Path(__file__).resolve().parents[1] / "federation"
if str(_FEDERATION_DIR) not in sys.path:
    sys.path.insert(0, str(_FEDERATION_DIR))

from federation_memory_adapter import FederationMemory

# ── Config ────────────────────────────────────────────────────────
READ_CLASS = "skill_mesh"          # health stats live in the skill mesh
WRITE_CLASS = "federation_shared"  # ecology observations are federation-shared
MEMORY_TIER = "canon"
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


def _extract_records(recall_result) -> list[dict]:
    """Best-effort extraction of memory records from an adapter recall receipt.

    The kernel receipt shape is not fixed by the adapter surface, so accept
    the common containers: {"results": [...]}, a bare list, or a single dict.
    """
    if isinstance(recall_result, dict):
        for key in ("results", "memories", "items", "hits", "data"):
            val = recall_result.get(key)
            if isinstance(val, list):
                return val
        return [recall_result]
    if isinstance(recall_result, list):
        return recall_result
    return []


def _record_payload(record) -> dict:
    """Extract the payload dict from a single recall record."""
    if isinstance(record, dict):
        for key in ("payload", "content", "metadata", "memory"):
            val = record.get(key)
            if isinstance(val, dict):
                return val
        return record
    return {}


def main(dry_run: bool = False):
    fm = FederationMemory(
        actor_id="aaa-ecology-daemon",
        session_id=os.getenv("ARIFOS_SESSION_ID", "system"),
    )

    # Recall skill-mesh records (kernel embeds the query server-side)
    recall_result = fm.recall(
        query="skill mesh capability affordance health stats",
        collection_class=READ_CLASS,
        top_k=200,
    )
    records = _extract_records(recall_result)

    transitions = {"HOT": 0, "WARM": 0, "COLD": 0}
    health_scores = {}
    now = datetime.now(timezone.utc).isoformat()

    for record in records:
        p = _record_payload(record)
        if not p:
            continue
        skill_id = p.get("skill_id", p.get("name", "unknown"))
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
                # Ecology transitions are federation-shared observations,
                # tagged for ecology (alignment doctrine §4 task mapping).
                fm.store(
                    content={
                        "skill_id": skill_id,
                        "previous_state": current_state,
                        "ecology_state": new_state,
                        "health_index": h,
                        "total_invocations": total,
                        "success_count": success,
                        "avg_latency_ms": latency,
                        "last_evaluated": now,
                    },
                    tier=MEMORY_TIER,
                    collection_class=WRITE_CLASS,
                    tags=["ecology", "skill-mesh", "ecology-transition", f"state:{new_state}"],
                    source_type="ecology_probe",
                )

    # Persist state
    report = {
        "evaluated_at": now,
        "skills_total": len(records),
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
