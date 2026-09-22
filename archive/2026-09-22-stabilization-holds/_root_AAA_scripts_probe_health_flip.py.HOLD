#!/usr/bin/env python3
"""
probe_health_flip.py — Loop 2 Closer (P0.2)
═════════════════════════════════════════════
Gives reality authority over FED routing.

Reads provider health from fed_state.db.
When probe detects 429/401 → flips route_health to 'dead'.

This closes Loop 2: Dead route → route_health flip.
Reality observed → Reality has authority → Routing changes.

ZEN_KERNEL: Reality must have authority over future behavior.
DITEMPA BUKAN DIBERI.
"""

import os
import sys
import json
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path

FED_DB = Path("/root/.local/share/arifos/fed_state.db")
FED_MODELS = Path("/root/.config/federation-models.json")
LOG_PATH = Path("/root/scripts/logs/probe_health_flip.log")


def log(msg: str):
    """Append to health flip log."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat()
    line = f"[{ts}] {msg}\n"
    with open(LOG_PATH, "a") as f:
        f.write(line)
    print(line.strip())


def probe_provider(name: str, base_url: str) -> dict:
    """Probe a provider's health endpoint."""
    result = {"name": name, "status": "unknown", "notes": ""}

    try:
        # Try /health endpoint
        resp = subprocess.run(
            ["curl", "-sf", "--max-time", "5", f"{base_url}/health"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if resp.returncode == 0:
            try:
                data = json.loads(resp.stdout)
                result["status"] = "live"
                result["notes"] = data.get("notes", "")
            except json.JSONDecodeError:
                result["status"] = "live"
        else:
            result["status"] = "dead"
            result["notes"] = "health_endpoint_unreachable"
    except Exception as e:
        result["status"] = "dead"
        result["notes"] = str(e)

    return result


def check_quota_signals(name: str, notes: str) -> bool:
    """Check if notes indicate quota exhaustion."""
    quota_signals = [
        "429",
        "insufficient_quota",
        "EXHAUSTED",
        "quota",
        "rate_limit",
        "credits",
        "401",
        "CreditsError",
        "drained",
    ]
    notes_lower = notes.lower()
    return any(signal.lower() in notes_lower for signal in quota_signals)


def flip_route_health(provider: str, new_health: str, reason: str):
    """Update route_health in fed_state.db."""
    if not FED_DB.exists():
        log(f"ERROR: FED DB not found at {FED_DB}")
        return False

    try:
        conn = sqlite3.connect(str(FED_DB))
        cursor = conn.cursor()

        # Check if provider exists
        cursor.execute("SELECT route_health FROM providers WHERE name = ?", (provider,))
        row = cursor.fetchone()

        if row is None:
            log(f"WARNING: Provider {provider} not in fed_state.db")
            conn.close()
            return False

        old_health = row[0]
        if old_health == new_health:
            conn.close()
            return False  # No change needed

        # Update route_health
        cursor.execute(
            "UPDATE providers SET route_health = ?, updated_at = ? WHERE name = ?",
            (new_health, datetime.now(timezone.utc).isoformat(), provider),
        )
        conn.commit()
        conn.close()

        log(
            f"FLIP: {provider} route_health {old_health} → {new_health} (reason: {reason})"
        )
        return True
    except Exception as e:
        log(f"ERROR: Could not update {provider}: {e}")
        return False


def emit_witness(provider: str, old_health: str, new_health: str, reason: str):
    """Emit witness to arifFlow about the health flip."""
    try:
        payload = {
            "actor_id": "probe_health_flip",
            "session_id": f"health-flip-{provider}",
            "step_type": "Barrier",
            "epistemic_label": "Observation",
            "floor_verdict": "Hold",
            "payload": {
                "event": "route_health_flip",
                "provider": provider,
                "old_health": old_health,
                "new_health": new_health,
                "reason": reason,
                "action": "flipped",
                "source": "probe_health_flip_p0.2",
            },
        }
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


def load_providers() -> list:
    """Load provider list from federation-models.json."""
    if not FED_MODELS.exists():
        log(f"ERROR: federation-models.json not found")
        return []

    with open(FED_MODELS) as f:
        data = json.load(f)

    providers = []
    for provider in data.get("providers", []):
        providers.append(
            {
                "name": provider.get("name", "unknown"),
                "base_url": provider.get("base_url", ""),
                "notes": provider.get("notes", ""),
                "route_health": provider.get("route_health", "unknown"),
            }
        )

    return providers


def main():
    log("=== Probe Health Flip — Loop 2 Closer (P0.2) ===")

    providers = load_providers()
    if not providers:
        log("ERROR: No providers found")
        sys.exit(1)

    flipped_count = 0

    for provider in providers:
        name = provider["name"]
        base_url = provider["base_url"]
        notes = provider["notes"]
        current_health = provider["route_health"]

        # Check notes for quota signals (from previous probes)
        if check_quota_signals(name, notes):
            if current_health != "dead":
                if flip_route_health(
                    name, "dead", f"quota_signal_in_notes: {notes[:100]}"
                ):
                    flipped_count += 1
                    emit_witness(name, current_health, "dead", "quota_exhausted")
            continue

        # Live probe
        if base_url:
            probe_result = probe_provider(name, base_url)
            if probe_result["status"] == "dead" and current_health != "dead":
                if flip_route_health(name, "dead", "probe_unreachable"):
                    flipped_count += 1
                    emit_witness(name, current_health, "dead", "probe_unreachable")
            elif probe_result["status"] == "live" and current_health == "dead":
                # Recovery: provider came back
                if flip_route_health(name, "live", "probe_recovered"):
                    flipped_count += 1
                    emit_witness(name, current_health, "live", "probe_recovered")

    if flipped_count > 0:
        log(f"ACTION: Flipped {flipped_count} providers. Reality has authority.")
    else:
        log("OK: All provider health consistent with reality.")

    log("=== Done ===")
    return flipped_count


if __name__ == "__main__":
    count = main()
    sys.exit(0 if count == 0 else 1)
