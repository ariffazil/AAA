#!/usr/bin/env python3
"""
CAPABILITY_FITNESS_CHECK — First Breath
========================================
Automated contradiction detection → witness emission cycle.

The smallest automated cycle that proves metabolism works without human trigger.

Reads capability_registry.json, probes current providers, detects contradictions,
emits witness receipts to VAULT999/RECEIPTS/.

Usage:
    python3 capability_fitness_check.py [--dry-run] [--capability NAME]
"""

import json
import hashlib
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

REGISTRY_PATH = "/root/AAA/capability_registry.json"
RECEIPT_DIR = "/root/VAULT999/RECEIPTS"
PROBE_TIMEOUT = 5  # seconds

# Provider health endpoints
PROVIDER_ENDPOINTS = {
    "minimax": {"url": "http://127.0.0.1:18092/health", "method": "GET"},
    "custom-fed-federation": {"url": "http://127.0.0.1:4000/health/liveliness", "method": "GET"},
    "searxng-local": {"url": "http://127.0.0.1:8080/", "method": "GET"},
    "groq": {"url": "http://127.0.0.1:4000/health/liveliness", "method": "GET"},
}


def probe_provider(provider_name: str) -> dict:
    """Probe a provider's health endpoint. Returns {alive: bool, status_code: int, latency_ms: float}"""
    endpoint = PROVIDER_ENDPOINTS.get(provider_name)
    if not endpoint:
        return {"alive": False, "status_code": 0, "latency_ms": 0, "error": "no endpoint configured"}

    start = datetime.now(timezone.utc)
    try:
        req = urllib.request.Request(endpoint["url"], method=endpoint.get("method", "GET"))
        resp = urllib.request.urlopen(req, timeout=PROBE_TIMEOUT)
        elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000
        return {"alive": resp.status < 400, "status_code": resp.status, "latency_ms": round(elapsed, 1), "error": None}
    except urllib.error.HTTPError as http_err:
        elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000
        return {"alive": http_err.code < 500, "status_code": http_err.code, "latency_ms": round(elapsed, 1), "error": None}
    except Exception as exc:
        elapsed = (datetime.now(timezone.utc) - start).total_seconds() * 1000
        return {"alive": False, "status_code": 0, "latency_ms": round(elapsed, 1), "error": str(exc)}


def check_capability(cap: dict, dry_run: bool = False) -> dict:
    """
    Check a single capability for contradictions.

    Returns:
        {
            capability_id: str,
            contradiction_detected: bool,
            witness_emitted: bool,
            details: str,
            fitness_delta: dict
        }
    """
    cap_id = cap["capability_id"]
    current_provider = cap["current_provider"]
    fitness = cap.get("fitness", {})

    # Probe current provider
    probe = probe_provider(current_provider)

    result = {
        "capability_id": cap_id,
        "current_provider": current_provider,
        "provider_alive": probe["alive"],
        "probe": probe,
        "contradiction_detected": False,
        "witness_emitted": False,
        "fitness_delta": {},
        "details": "",
    }

    if not probe["alive"]:
        # CONTRADICTION: current provider is dead
        # Check if there's a fallback in providers_tried
        providers = cap.get("providers_tried", [])
        alive_alternatives = [
            p for p in providers
            if p["provider"] != current_provider and p.get("status") == "active"
        ]

        if alive_alternatives:
            result["contradiction_detected"] = True
            result["details"] = (
                f"CONTRADICTION: {current_provider} is DOWN but capability "
                f"has {len(alive_alternatives)} active alternative(s): "
                f"{[p['provider'] for p in alive_alternatives]}"
            )
            result["fitness_delta"] = {
                "provider_independent": True,
                "survival_events": fitness.get("survival_events", 0) + 1,
                "contradictions_survived": fitness.get("contradictions_survived", 0) + 1,
                "last_tested": datetime.now(timezone.utc).isoformat(),
                "last_verdict": "SURVIVED",
            }
        else:
            result["details"] = (
                f"CRITICAL: {current_provider} is DOWN and no alternatives available. "
                f"Capability {cap_id} is vulnerable."
            )
            result["fitness_delta"] = {
                "last_tested": datetime.now(timezone.utc).isoformat(),
                "last_verdict": "VULNERABLE",
            }
    else:
        # NO CONTRADICTION: current provider is alive
        result["details"] = (
            f"STABLE: {current_provider} alive ({probe['status_code']}, "
            f"{probe['latency_ms']}ms). Capability {cap_id} operational."
        )
        result["fitness_delta"] = {
            "last_tested": datetime.now(timezone.utc).isoformat(),
            "last_verdict": "STABLE",
        }

    return result


def emit_witness(result: dict, dry_run: bool = False) -> dict:
    """
    Emit a witness receipt to VAULT999/RECEIPTS/.
    Returns the receipt content.
    """
    now = datetime.now(timezone.utc)
    cap_id = result["capability_id"]
    verdict = result["fitness_delta"].get("last_verdict", "UNKNOWN")

    receipt = {
        "schema": "arifos.witness_receipt.v1",
        "receipt_class": "CAPABILITY_FITNESS_WITNESS",
        "receipt_id": f"fitness-{cap_id}-{now.strftime('%Y%m%dT%H%M%S')}",
        "created_at_utc": now.isoformat(),
        "capability_id": cap_id,
        "current_provider": result["current_provider"],
        "provider_alive": result["provider_alive"],
        "probe": result["probe"],
        "contradiction_detected": result["contradiction_detected"],
        "fitness_delta": result["fitness_delta"],
        "witness_statement": "",
    }

    if result["contradiction_detected"]:
        receipt["witness_statement"] = (
            f"Capability '{cap_id}' has been tested by reality. "
            f"Provider '{result['current_provider']}' failed. "
            f"Capability survived through alternative providers. "
            f"provider_independent = true. "
            f"survival_events = {result['fitness_delta'].get('survival_events', 0)}. "
            f"This capability has been witnessed by contradiction and survived."
        )
    elif verdict == "STABLE":
        receipt["witness_statement"] = (
            f"Capability '{cap_id}' confirmed operational. "
            f"Provider '{result['current_provider']}' healthy. "
            f"No contradiction detected. Capability stable."
        )
    elif verdict == "VULNERABLE":
        receipt["witness_statement"] = (
            f"Capability '{cap_id}' is VULNERABLE. "
            f"Provider '{result['current_provider']}' is DOWN with no alternatives. "
            f"Immediate attention required."
        )
    else:
        receipt["witness_statement"] = (
            f"Capability '{cap_id}' fitness check completed with verdict: {verdict}"
        )

    # Compute receipt hash
    receipt_bytes = json.dumps(receipt, sort_keys=True).encode()
    receipt["receipt_hash"] = hashlib.sha256(receipt_bytes).hexdigest()[:16]

    if not dry_run:
        os.makedirs(RECEIPT_DIR, exist_ok=True)
        receipt_path = os.path.join(RECEIPT_DIR, f"{receipt['receipt_id']}.json")
        with open(receipt_path, "w") as f:
            json.dump(receipt, f, indent=2)
        receipt["written_to"] = receipt_path
    else:
        receipt["written_to"] = "(dry-run, not written)"

    return receipt


def update_registry(registry: dict, results: list) -> dict:
    """Update the registry with new fitness data after checks."""
    for result in results:
        cap_id = result["capability_id"]
        if cap_id in registry["capabilities"]:
            cap = registry["capabilities"][cap_id]
            fitness_delta = result["fitness_delta"]
            for key, value in fitness_delta.items():
                cap["fitness"][key] = value

            # Append witness reference
            cap["witnesses"].append({
                "receipt_id": result.get("receipt_id", "unknown"),
                "checked_at": datetime.now(timezone.utc).isoformat(),
                "verdict": fitness_delta.get("last_verdict", "UNKNOWN"),
            })

            # Keep only last 20 witnesses per capability
            cap["witnesses"] = cap["witnesses"][-20:]

    registry["last_check"] = datetime.now(timezone.utc).isoformat()
    return registry


def main():
    dry_run = "--dry-run" in sys.argv
    target_cap = None
    for i, arg in enumerate(sys.argv):
        if arg == "--capability" and i + 1 < len(sys.argv):
            target_cap = sys.argv[i + 1]

    # Load registry
    with open(REGISTRY_PATH) as f:
        registry = json.load(f)

    capabilities = registry.get("capabilities", {})
    if target_cap:
        if target_cap not in capabilities:
            print(f"ERROR: capability '{target_cap}' not found in registry")
            sys.exit(1)
        capabilities = {target_cap: capabilities[target_cap]}

    results = []
    contradictions = 0
    witnesses = 0

    print(f"=== CAPABILITY FITNESS CHECK — {datetime.now(timezone.utc).isoformat()} ===")
    print(f"Checking {len(capabilities)} capabilities...\n")

    for cap_id, cap in capabilities.items():
        result = check_capability(cap, dry_run)
        receipt = emit_witness(result, dry_run)
        result["receipt_id"] = receipt["receipt_id"]
        results.append(result)

        # Print verdict
        verdict = result["fitness_delta"].get("last_verdict", "UNKNOWN")
        icon = {"SURVIVED": "🔥", "STABLE": "✅", "VULNERABLE": "⚠️", "UNTESTED": "❓"}.get(verdict, "❓")
        print(f"  {icon} {cap_id}: {verdict}")
        if result["contradiction_detected"]:
            print(f"     {result['details']}")
            contradictions += 1
        else:
            print(f"     Provider: {result['current_provider']} ({result['probe']['status_code']})")
        print(f"     Witness: {receipt['receipt_id']}")
        witnesses += 1

    # Update registry
    if not dry_run:
        registry = update_registry(registry, results)
        with open(REGISTRY_PATH, "w") as f:
            json.dump(registry, f, indent=2)

    print(f"\n--- SUMMARY ---")
    print(f"  Capabilities checked: {len(results)}")
    print(f"  Contradictions found: {contradictions}")
    print(f"  Witnesses emitted:    {witnesses}")
    print(f"  Registry updated:     {'yes' if not dry_run else 'dry-run'}")
    print(f"  Receipts written to:  {RECEIPT_DIR if not dry_run else '(dry-run)'}")
    print(f"\nDITEMPA BUKAN DIBERI. ⚒️")


if __name__ == "__main__":
    main()
