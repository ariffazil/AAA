#!/usr/bin/env python3
"""
cron_failure_autopause.py — Loop 1 Closer
═══════════════════════════════════════════
Gives reality authority over cron jobs.

Reads failure_streak from federated-recurrence.yaml.
When failure_streak >= failure_pause_threshold → pauses the job.

This closes Loop 1: Cron failure → auto-pause.
Reality observed → Reality has authority → Behavior changes.

ZEN_KERNEL: Reality must have authority over future behavior.
DITEMPA BUKAN DIBERI.
"""

import os
import sys
import yaml
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = Path("/root/AAA/registries/federated-recurrence.yaml")
HERMES_CRON_DIR = Path(os.path.expanduser("~/.hermes/cron"))
LOG_PATH = Path("/root/scripts/logs/cron_autopause.log")


def log(msg: str):
    """Append to autopause log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    line = f"[{ts}] {msg}\n"
    with open(LOG_PATH, "a") as f:
        f.write(line)
    print(line.strip())


def load_registry() -> dict:
    """Load federated-recurrence.yaml."""
    if not REGISTRY_PATH.exists():
        log("ERROR: Registry not found at {REGISTRY_PATH}")
        sys.exit(1)
    with open(REGISTRY_PATH) as f:
        return yaml.safe_load(f)


def pause_hermes_job(job_id: str) -> bool:
    """Pause a hermes-cron job by ID."""
    jobs_file = HERMES_CRON_DIR / "jobs.json"
    if not jobs_file.exists():
        log(f"WARNING: Hermes cron jobs.json not found")
        return False

    with open(jobs_file) as f:
        jobs = json.load(f)

    for job in jobs:
        if job.get("id") == job_id or job.get("job_id") == job_id:
            if job.get("paused"):
                return False  # Already paused
            job["paused"] = True
            job["paused_at"] = datetime.now(timezone.utc).isoformat()
            job["paused_reason"] = "cron_failure_autopause: failure_streak >= threshold"
            log(f"PAUSED: {job_id}")
            with open(jobs_file, "w") as f:
                json.dump(jobs, f, indent=2)
            return True

    log(f"WARNING: Job {job_id} not found in hermes-cron")
    return False


def pause_cron_entry(entry_id: str, schedule: str) -> bool:
    """Pause a system cron entry by commenting it out."""
    cron_files = [
        Path("/etc/cron.d/" + f)
        for f in os.listdir("/etc/cron.d/")
        if f.startswith("arif") or f.startswith("aaa") or f.startswith("fed")
    ]
    cron_files.append(Path("/var/spool/cron/crontabs/root"))

    for cron_file in cron_files:
        if not cron_file.exists():
            continue
        try:
            with open(cron_file) as f:
                lines = f.readlines()

            modified = False
            for i, line in enumerate(lines):
                if entry_id in line and not line.strip().startswith("#"):
                    lines[i] = f"# PAUSED_BY_AUTOPAUSE: {line}"
                    modified = True
                    log(f"PAUSED cron entry: {entry_id} in {cron_file}")

            if modified:
                with open(cron_file, "w") as f:
                    f.writelines(lines)
                return True
        except PermissionError:
            log(f"WARNING: No permission to modify {cron_file}")

    return False


def emit_witness(entry_id: str, adapter: str, failure_streak: int, threshold: int):
    """Emit witness to arifFlow about the autopause."""
    try:
        payload = {
            "actor_id": "cron_failure_autopause",
            "session_id": f"autopause-{entry_id}",
            "step_type": "Barrier",
            "epistemic_label": "Observation",
            "floor_verdict": "Hold",
            "payload": {
                "event": "cron_autopause",
                "entry_id": entry_id,
                "adapter": adapter,
                "failure_streak": failure_streak,
                "threshold": threshold,
                "action": "paused",
                "reason": "reality_has_authority",
            },
        }
        # Try arifFlow ingest
        subprocess.run(
            [
                "curl",
                "-sf",
                "-X",
                "POST",
                "http://127.0.0.1:7073/ingest",
                "-H",
                "Content-Type: application/json",
                "-d",
                json.dumps(payload),
            ],
            capture_output=True,
            timeout=5,
        )
    except Exception as e:
        log(f"WARNING: Could not emit witness: {e}")


def main():
    log("=== Cron Failure Autopause — Loop 1 Closer ===")

    registry = load_registry()
    events = registry.get("events", [])
    policies = registry.get("policies", {})

    default_threshold = policies.get("failure_pause_threshold", 3)
    paused_count = 0

    for event in events:
        entry_id = event.get("id", "unknown")
        adapter = event.get("adapter", "unknown")
        failure_streak = event.get("failure_streak", 0)
        threshold = default_threshold
        status = event.get("status", "ok")

        # Check if already paused
        if event.get("paused"):
            continue

        # Check if failure_streak exceeds threshold
        if failure_streak >= threshold and status == "error":
            log(
                f"TRIGGER: {entry_id} failure_streak={failure_streak} >= threshold={threshold}"
            )

            if adapter == "hermes-cron":
                job_id = event.get("job_id")
                if job_id:
                    if pause_hermes_job(job_id):
                        paused_count += 1
                        emit_witness(entry_id, adapter, failure_streak, threshold)
            elif adapter == "cron":
                schedule = event.get("schedule", "")
                if pause_cron_entry(entry_id, schedule):
                    paused_count += 1
                    emit_witness(entry_id, adapter, failure_streak, threshold)

    if paused_count > 0:
        log(f"ACTION: Paused {paused_count} jobs. Reality has authority.")
    else:
        log("OK: No jobs exceed failure threshold. All healthy.")

    log("=== Done ===")
    return paused_count


if __name__ == "__main__":
    count = main()
    sys.exit(0 if count == 0 else 1)
