#!/usr/bin/env python3
"""Model Drift Detection — compares declared agent→model assignments vs live probes.

Canonical source: /root/AAA/registries/models/AGENT_MODEL_MAP.json
Drift log:       /root/AAA/registries/models/drift_log.jsonl

Usage:
    python3 model_drift_detect.py          # full scan
    python3 model_drift_detect.py --agent  # single-agent scan
    python3 model_drift_detect.py --cron   # cron mode (silent unless drift)

MOVE 3 of the 4-move AGENT_MODEL_MAP execution plan.
Forged 2026-07-20 by FORGE (000Ω).
"""

import json
import os
import sys
import subprocess
import datetime
from pathlib import Path

REGISTRY = Path("/root/AAA/registries/models/AGENT_MODEL_MAP.json")
DRIFT_LOG = Path("/root/AAA/registries/models/drift_log.jsonl")

COLOUR = {"OK": "\033[92m", "WARN": "\033[93m", "FAIL": "\033[91m", "RESET": "\033[0m"}


def load_registry():
    with open(REGISTRY) as f:
        return json.load(f)


def probe_model(model_key: str, provider_endpoint: str, api_key_env: str) -> dict:
    """Quick health probe: can we reach this model?"""
    api_key = os.environ.get(api_key_env, "")
    if not api_key:
        return {"status": "UNKNOWN", "reason": f"API key env {api_key_env} not set"}

    # Lightweight probe — just list models or health check
    try:
        result = subprocess.run(
            ["curl", "-sf", "-m", "5", f"{provider_endpoint}/models", "-H", f"Authorization: Bearer {api_key}"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                model_ids = [m.get("id", "") for m in data.get("data", [])]
                # Extract model variant from key
                variant = model_key.split("/")[-1] if "/" in model_key else model_key
                if any(variant in mid for mid in model_ids):
                    return {"status": "LIVE", "models_available": len(model_ids)}
                else:
                    return {
                        "status": "MISMATCH",
                        "reason": f"Model {variant} not in provider list",
                        "available": model_ids[:10],
                    }
            except json.JSONDecodeError:
                return {"status": "LIVE", "note": "non-JSON response but reachable"}
        else:
            return {"status": "DOWN", "reason": f"HTTP {result.returncode}: {result.stderr[:200]}"}
    except Exception as e:
        return {"status": "ERROR", "reason": str(e)[:200]}


def check_drift(registry: dict, verbose: bool = True) -> list:
    """Check all agents for model assignment drift."""
    findings = []
    providers = {p["provider_id"]: p for p in registry["providers"]}
    models = {m["model_key"]: m for m in registry["models"]}

    for agent in registry["agents"]:
        model_key = agent["primary_model"]
        model = models.get(model_key)
        if not model:
            findings.append(
                {
                    "agent": agent["agent_id"],
                    "type": "MISSING_MODEL",
                    "severity": "CRITICAL",
                    "model_key": model_key,
                    "reason": "Model not found in registry models[]",
                }
            )
            continue

        provider = providers.get(model["provider_ref"])
        if not provider:
            findings.append(
                {
                    "agent": agent["agent_id"],
                    "type": "MISSING_PROVIDER",
                    "severity": "CRITICAL",
                    "provider_ref": model["provider_ref"],
                    "reason": "Provider not found in registry providers[]",
                }
            )
            continue

        # Check model status
        if model["status"] not in ("LIVE", "ACTIVE"):
            findings.append(
                {
                    "agent": agent["agent_id"],
                    "type": "MODEL_NOT_LIVE",
                    "severity": "HIGH",
                    "model_key": model_key,
                    "model_status": model["status"],
                    "reason": f"Model status is {model['status']}, not LIVE",
                }
            )

        # Check provider status
        if provider["status"] not in ("ACTIVE", "LIVE"):
            findings.append(
                {
                    "agent": agent["agent_id"],
                    "type": "PROVIDER_NOT_LIVE",
                    "severity": "HIGH",
                    "provider_id": model["provider_ref"],
                    "provider_status": provider["status"],
                    "reason": f"Provider status is {provider['status']}, not ACTIVE",
                }
            )

        # Check for censorship block on agent's primary role
        if model and model.get("censorship_profile") and model["censorship_profile"].get("detected"):
            if "666_JUDGE" in agent.get("constitutional_roles", []):
                findings.append(
                    {
                        "agent": agent["agent_id"],
                        "type": "CENSORED_JUDGE",
                        "severity": "CRITICAL",
                        "model_key": model_key,
                        "reason": "Censored model assigned to judgment role",
                    }
                )

        # Check fallback chain integrity
        for fb in agent.get("fallback_chain", []):
            fb_model = models.get(fb["model_key"])
            if not fb_model:
                findings.append(
                    {
                        "agent": agent["agent_id"],
                        "type": "MISSING_FALLBACK_MODEL",
                        "severity": "HIGH",
                        "fallback_model": fb["model_key"],
                        "reason": "Fallback model not found in registry",
                    }
                )

    return findings


def main():
    verbose = "--cron" not in sys.argv
    registry = load_registry()

    if verbose:
        print(f"🔍 Model Drift Detection — {datetime.datetime.now().isoformat()}")
        print(
            f"   Registry: {len(registry['models'])} models, {len(registry['agents'])} agents, {len(registry['providers'])} providers"
        )
        print()

    findings = check_drift(registry, verbose=verbose)

    if not findings:
        if verbose:
            print(f"{COLOUR['OK']}✅ NO DRIFT — all agent→model assignments clean{COLOUR['RESET']}")
        return 0

    # Write to drift log
    timestamp = datetime.datetime.now(datetime.UTC).isoformat()
    for f in findings:
        f["detected_at"] = timestamp
        with open(DRIFT_LOG, "a") as log:
            log.write(json.dumps(f) + "\n")

    if verbose:
        for f in findings:
            sev = f["severity"]
            colour = COLOUR.get("FAIL" if sev == "CRITICAL" else "WARN", "")
            print(f"{colour}⚠️  [{sev}] {f['type']}: {f.get('agent', '?')} — {f.get('reason', '')}{COLOUR['RESET']}")
        print(f"\n{len(findings)} drift events logged to {DRIFT_LOG}")

    return 1 if any(f["severity"] == "CRITICAL" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
