#!/usr/bin/env python3
"""Scheduler Registry drift detector — Law 1 enforcement (P1-2).

Compares live sweep vs the registry desired-state file. Emits:
  - ghost:    live execution obligation not represented in registry
  - phantom:  registry unit absent from live runtime
  - publisher_duplication: logical human lane with >1 active delivery path
  - weekly metrics (measurable subset; N/A explicit otherwise)

Read-only. Zero mutation. Owner-named findings.

333-AGI 2026-09-17 · DITEMPA BUKAN DIBERI
"""

import sys
import json
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
REGISTRY = Path("/root/AAA/registries/scheduler/scheduled_units.yaml")
OBLOG = Path("/root/AAA/registries/scheduler/logical_obligations.yaml")


def live_sweep():
    import sweep_scheduled_units as sweep

    units = []
    sweep.sweep_root_crontab(units)
    sweep.sweep_cron_d(units)
    sweep.sweep_systemd(units)
    sweep.sweep_hermes(units)
    return units


def main():
    if not REGISTRY.exists():
        print(json.dumps({"error": f"registry missing: {REGISTRY}", "finding": "run sweep first"}))
        return 1
    declared = yaml.safe_load(REGISTRY.read_text())
    declared_ids = {u["id"] for u in declared.get("units", [])}
    live = live_sweep()
    live_ids = {u["id"] for u in live}

    ghosts = [u for u in live if u["id"] not in declared_ids]
    phantoms = [u for u in declared.get("units", []) if u["id"] not in live_ids]

    # publisher duplication: hermes human deliveries + root-cron delivery lanes
    publishers = {}
    for u in live:
        if u.get("delivery") == "telegram" or "cron-deliver" in str(u.get("command_head", "")):
            publishers.setdefault("telegram_lanes", []).append(u["id"])
    dup = []
    obl = yaml.safe_load(OBLOG.read_text()) if OBLOG.exists() else {}
    for o in obl.get("obligations", []):
        n = len([p for p in o.get("publisher", []) if p.get("status") == "active"])
        legacy = [l for l in o.get("legacy_paths", []) if l.get("action") == "retired"]
        if n > 1:
            dup.append({"obligation": o.get("logical_id"), "active_publishers": n})

    metrics = {
        "denominator_drift": len(ghosts) + len(phantoms),
        "ghost_count": len(ghosts),
        "phantom_count": len(phantoms),
        "publisher_duplication": len(dup),
        "false_zero_rate": "N/A — requires per-report audit",
        "receipt_identity_completeness": "N/A — acceptance v2 pending",
        "orphan_automation_rate": "N/A — consumer field rollout pending",
        "unreviewed_disabled_jobs": "N/A — tombstones.jsonl now covers hermes fleet",
        "meta_depth": "N/A — chain audit pending",
        "high_frequency_justification": "N/A — proof artifacts pending",
    }
    report = {
        "checked_at": declared.get("meta", {}).get("generated_at", "?"),
        "registry_total": len(declared_ids),
        "live_total": len(live_ids),
        "ghosts": [{"id": g["id"], "surface": g["surface"]} for g in ghosts][:25],
        "phantoms": [{"id": p["id"], "surface": p.get("surface")} for p in phantoms][:25],
        "publisher_duplication": dup,
        "metrics": metrics,
        "owner_of_next_action": "333-AGI triage; F13 for any human-lane change",
    }
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
