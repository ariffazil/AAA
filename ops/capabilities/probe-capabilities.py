#!/usr/bin/env python3
"""
Capability Reachability Probe Harness v0.1.0
=============================================
Read-only, deterministic probes for the arifOS capability ledger.

Usage:
    python3 probe-capabilities.py --list                    # List all capabilities
    python3 probe-capabilities.py --capability weather.current.kl  # Probe one
    python3 probe-capabilities.py --all                     # Probe all reachable candidates
    python3 probe-capabilities.py --validate                # Validate ledger schema

Contract:
    - Input: capability ID or --list/--all/--validate
    - Output: one JSON evidence record per probe (stdout)
    - Action: read-only bounded health check
    - Timeout: explicit per probe
    - Retries: bounded (0 or 1)
    - Secrets: never printed
    - Exit code: non-zero only for harness/probe failure

Results written to: probe-results/<capability_id>_<timestamp>.jsonl
"""

import argparse
import fcntl
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

LEDGER_PATH = Path(__file__).parent / "capability-ledger.yaml"
LEDGER_LOCK_PATH = Path(__file__).parent / "capability-ledger.lock"
RESULTS_DIR = Path(__file__).parent / "probe-results"
MYT = timezone(timedelta(hours=8))


# ── YAML Loader (minimal, no PyYAML dependency) ─────────────


def load_ledger():
    """Load the capability ledger. Uses PyYAML if available, falls back to json."""
    try:
        import yaml

        with open(LEDGER_PATH, "r") as f:
            return yaml.safe_load(f)
    except ImportError:
        # Fallback: try JSON (for testing)
        with open(LEDGER_PATH, "r") as f:
            return json.load(f)


class LedgerLock:
    """Exclusive writer lock for the capability ledger.

    The two-writer race (2026-09-12): a concurrent writer — Hermes's full-file
    re-dump or a second probe — could clobber a surgical edit between this
    function's read_text() and write_text(). flock serializes the read-modify-write
    so the source-of-truth cannot silently revert to falsehood under concurrent
    access. Same pattern as carry_forward.py's CarryLock.
    """

    def __init__(self):
        self.lock_path = LEDGER_LOCK_PATH
        self.fd = None

    def __enter__(self):
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        self.fd = open(self.lock_path, "a+")
        fcntl.flock(self.fd, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc):
        if self.fd is not None:
            fcntl.flock(self.fd, fcntl.LOCK_UN)
            self.fd.close()
        return False


def persist_probe_result(cap_id, now_iso, result):
    """Update last_probe_at/last_probe_status for one capability via targeted text edit.

    The ledger is hand-formatted YAML; a full round-trip (pyyaml/ruamel) would
    reformat comments and alignment. This does a surgical line replacement that
    touches only the two timestamp fields of the probed capability's reachability
    block, preserving every other byte.

    The read-modify-write runs under an exclusive flock so no concurrent writer
    (probe harness or Hermes write-back) can clobber the edit mid-flight. The
    file is written atomically (tmp + os.replace) so a crash never leaves a
    half-written ledger.
    """
    with LedgerLock():
        lines = LEDGER_PATH.read_text().splitlines()
        target_idx = None
        for i, line in enumerate(lines):
            if line.strip() == f"- id: {cap_id}":
                target_idx = i
                break
        if target_idx is None:
            return  # capability absent; never rewrite the ledger
        updated_at = updated_status = False
        for i in range(target_idx, len(lines)):
            line = lines[i]
            indent = line[: len(line) - len(line.lstrip())]
            s = line.strip()
            if s.startswith("last_probe_at:") and not updated_at:
                lines[i] = f'{indent}last_probe_at: "{now_iso}"'
                updated_at = True
            elif s.startswith("last_probe_status:") and not updated_status:
                lines[i] = f'{indent}last_probe_status: "{result}"'
                updated_status = True
            if updated_at and updated_status:
                break
        if updated_at or updated_status:
            tmp = LEDGER_PATH.with_suffix(".tmp")
            tmp.write_text("\n".join(lines) + "\n")
            os.replace(tmp, LEDGER_PATH)


# ── Probe Implementations ───────────────────────────────────


def probe_weather_kl():
    """Probe Open-Meteo for KL current weather."""
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        "latitude=3.139&longitude=101.6869"
        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        "precipitation,weather_code,wind_speed_10m"
        "&timezone=Asia/Kuala_Lumpur&forecast_days=1"
    )
    timeout_seconds = 8

    start = time.monotonic()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "arifOS-capability-probe/0.1"})
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            latency_ms = int((time.monotonic() - start) * 1000)
            body = json.loads(resp.read().decode())

        # Validate required fields
        required_current = ["temperature_2m", "weather_code"]
        current = body.get("current", {})
        missing = [f for f in required_current if f not in current]

        return {
            "result": "reachable" if not missing else "degraded",
            "route_type": "direct_https",
            "latency_ms": latency_ms,
            "source_timestamp": current.get("time"),
            "evidence": {
                "http_status": 200,
                "schema_valid": len(missing) == 0,
                "required_fields_present": [f for f in required_current if f in current],
                "missing_fields": missing,
                "temperature_c": current.get("temperature_2m"),
                "humidity_pct": current.get("relative_humidity_2m"),
            },
            "degraded": len(missing) > 0,
            "error_class": None,
            "error_message_safe": None,
        }
    except urllib.error.URLError as e:
        latency_ms = int((time.monotonic() - start) * 1000)
        return {
            "result": "degraded",
            "route_type": "direct_https",
            "latency_ms": latency_ms,
            "source_timestamp": None,
            "evidence": None,
            "degraded": True,
            "error_class": "network_error",
            "error_message_safe": f"Open-Meteo unreachable: {type(e).__name__}",
        }
    except Exception as e:
        latency_ms = int((time.monotonic() - start) * 1000)
        return {
            "result": "degraded",
            "route_type": "direct_https",
            "latency_ms": latency_ms,
            "source_timestamp": None,
            "evidence": None,
            "degraded": True,
            "error_class": type(e).__name__,
            "error_message_safe": f"Probe failed: {type(e).__name__}",
        }


def probe_youtube_transcript():
    """Probe youtube-transcript-api against a known public video."""
    test_video_id = "dQw4w9WgXcQ"  # Rick Astley — universally available captions
    timeout_seconds = 10

    start = time.monotonic()
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(test_video_id)
        entries = list(transcript)
        latency_ms = int((time.monotonic() - start) * 1000)

        has_entries = len(entries) > 0
        first_text = entries[0].text[:80] if has_entries else None
        return {
            "result": "reachable" if has_entries else "degraded",
            "route_type": "local_python_package",
            "latency_ms": latency_ms,
            "source_timestamp": None,
            "evidence": {
                "package_importable": True,
                "api_method": "fetch",
                "transcript_entries": len(entries),
                "first_entry_preview": first_text,
                "test_video_id": test_video_id,
            },
            "degraded": not has_entries,
            "error_class": None,
            "error_message_safe": None,
        }
    except ImportError:
        latency_ms = int((time.monotonic() - start) * 1000)
        return {
            "result": "unreachable",
            "route_type": "local_python_package",
            "latency_ms": latency_ms,
            "source_timestamp": None,
            "evidence": None,
            "degraded": True,
            "error_class": "ImportError",
            "error_message_safe": "youtube_transcript_api not importable in current environment",
        }
    except Exception as e:
        latency_ms = int((time.monotonic() - start) * 1000)
        return {
            "result": "degraded",
            "route_type": "local_python_package",
            "latency_ms": latency_ms,
            "source_timestamp": None,
            "evidence": None,
            "degraded": True,
            "error_class": type(e).__name__,
            "error_message_safe": f"Transcript probe failed: {type(e).__name__}",
        }


def probe_telegram_config():
    """Validate Telegram gateway config without sending messages."""
    config_paths = [
        "/root/.hermes/config.yaml",
        "/root/.hermes/config.json",
    ]
    found = None
    for p in config_paths:
        if os.path.exists(p):
            found = p
            break

    if not found:
        return {
            "result": "degraded",
            "route_type": "hermes_telegram_gateway",
            "latency_ms": 0,
            "source_timestamp": None,
            "evidence": {
                "config_found": False,
                "config_paths_checked": config_paths,
            },
            "degraded": True,
            "error_class": "config_missing",
            "error_message_safe": "No Hermes config file found",
        }

    return {
        "result": "reachable",
        "route_type": "hermes_telegram_gateway",
        "latency_ms": 0,
        "source_timestamp": None,
        "evidence": {
            "config_found": True,
            "config_path": found,
            "note": "Config exists; actual send not tested (read-only probe)",
        },
        "degraded": False,
        "error_class": None,
        "error_message_safe": None,
    }


# ── Probe Registry ──────────────────────────────────────────

PROBES = {
    "weather.current.kl": probe_weather_kl,
    "content.youtube.transcript": probe_youtube_transcript,
    "messaging.telegram.notify": probe_telegram_config,
}


# ── Ledger Operations ───────────────────────────────────────


def list_capabilities(ledger):
    """Print all capabilities in a readable table."""
    caps = ledger.get("capabilities", [])
    print(f"{'ID':<40} {'Lifecycle':<12} {'Impl':<20} {'Reach':<30}")
    print("-" * 102)
    for cap in caps:
        cid = cap["id"]
        lc = cap["lifecycle"]
        impl = cap.get("implementation", {}).get("state", "?")
        reach = cap.get("reachability", {}).get("state", "?")
        print(f"{cid:<40} {lc:<12} {impl:<20} {reach:<30}")
    print(f"\nTotal: {len(caps)} capabilities")


def validate_ledger(ledger):
    """Validate ledger structure (lightweight, no jsonschema dependency)."""
    errors = []
    required_top = ["ledger_version", "capabilities"]
    for field in required_top:
        if field not in ledger:
            errors.append(f"Missing top-level field: {field}")

    valid_impl_states = {
        "absent",
        "partial",
        "implemented",
        "retired",
        "vendor_candidate",
        "implemented_or_claimed",
        "external_institutional_api",
    }
    valid_reach_states = {
        "unreachable",
        "not_wired",
        "working_unprobed",
        "reachable",
        "degraded",
        "pending_production_probe",
        "intentionally_unreachable",
        "unknown_by_governed_probe",
    }
    valid_auth = {"observe", "draft", "external_write", "financial_write", "admin_write"}
    valid_lifecycle = {"active", "partial", "deferred", "retired", "blocked"}

    for i, cap in enumerate(ledger.get("capabilities", [])):
        prefix = f"capabilities[{i}]"
        for field in ["id", "title", "domain", "lifecycle", "implementation", "reachability", "governance"]:
            if field not in cap:
                errors.append(f"{prefix}: missing required field '{field}'")

        if "lifecycle" in cap and cap["lifecycle"] not in valid_lifecycle:
            errors.append(f"{prefix}: invalid lifecycle '{cap['lifecycle']}'")

        impl = cap.get("implementation", {})
        if "state" in impl and impl["state"] not in valid_impl_states:
            errors.append(f"{prefix}.implementation.state: invalid '{impl['state']}'")

        reach = cap.get("reachability", {})
        if "state" in reach and reach["state"] not in valid_reach_states:
            errors.append(f"{prefix}.reachability.state: invalid '{reach['state']}'")

        gov = cap.get("governance", {})
        if "authority" in gov and gov["authority"] not in valid_auth:
            errors.append(f"{prefix}.governance.authority: invalid '{gov['authority']}'")

    if errors:
        print(f"VALIDATION FAILED ({len(errors)} errors):")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print(f"VALIDATION PASSED ({len(ledger.get('capabilities', []))} capabilities)")
        return True


def probe_capability(cap_id, ledger):
    """Run a probe for a specific capability."""
    caps = ledger.get("capabilities", [])
    cap = next((c for c in caps if c["id"] == cap_id), None)
    if not cap:
        print(json.dumps({"error": f"Capability '{cap_id}' not found in ledger"}))
        sys.exit(1)

    # Extract governance for the record
    gov = cap.get("governance", {})
    reach = cap.get("reachability", {})

    # Check if a live probe exists
    probe_fn = PROBES.get(cap_id)

    if probe_fn:
        # Run the actual probe
        probe_result = probe_fn()
    else:
        # Return truthful non-error from ledger state
        probe_result = {
            "result": reach.get("state", "unknown"),
            "route_type": reach.get("route_type", "none"),
            "latency_ms": None,
            "source_timestamp": None,
            "evidence": None,
            "degraded": reach.get("state")
            in {"unreachable", "intentionally_unreachable", "not_wired", "unknown_by_governed_probe"},
            "error_class": None,
            "error_message_safe": reach.get("reason"),
        }
        if reach.get("blocker"):
            probe_result["blocker"] = reach["blocker"]

    # Build the full probe record
    now = datetime.now(MYT)
    record = {
        "probe_id": cap_id,
        "capability_title": cap.get("title"),
        "lifecycle": cap.get("lifecycle"),
        "governance_authority": gov.get("authority"),
        "activation_gate": gov.get("activation_gate"),
        "timestamp": now.isoformat(),
        "harness_version": "0.1.0",
        **probe_result,
    }

    # Write result to JSONL
    RESULTS_DIR.mkdir(exist_ok=True)
    result_file = RESULTS_DIR / f"{cap_id.replace('.', '_')}_{now.strftime('%Y%m%d_%H%M%S')}.jsonl"
    with open(result_file, "w") as f:
        f.write(json.dumps(record) + "\n")

    # Persist reachability timestamps back to the ledger (targeted edit, formatting-preserving)
    persist_probe_result(cap_id, now.isoformat(), record["result"])

    # Print to stdout
    print(json.dumps(record, indent=2))
    return record


def probe_all(ledger):
    """Probe all capabilities that have live probe implementations."""
    caps = ledger.get("capabilities", [])
    results = []
    for cap in caps:
        if cap["id"] in PROBES:
            result = probe_capability(cap["id"], ledger)
            results.append(result)
            print()
    return results


# ── Main ────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Capability Reachability Probe Harness v0.1.0")
    parser.add_argument("--list", action="store_true", help="List all capabilities")
    parser.add_argument("--capability", type=str, help="Probe a specific capability by ID")
    parser.add_argument("--all", action="store_true", help="Probe all capabilities with live probes")
    parser.add_argument("--validate", action="store_true", help="Validate ledger schema")
    args = parser.parse_args()

    if not any([args.list, args.capability, args.all, args.validate]):
        parser.print_help()
        sys.exit(1)

    ledger = load_ledger()

    if args.list:
        list_capabilities(ledger)
    elif args.validate:
        valid = validate_ledger(ledger)
        sys.exit(0 if valid else 1)
    elif args.capability:
        probe_capability(args.capability, ledger)
    elif args.all:
        probe_all(ledger)


if __name__ == "__main__":
    main()
