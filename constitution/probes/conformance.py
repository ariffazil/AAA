#!/usr/bin/env python3
"""
Conformance Probe Runner — arifOS attack-the-constitution harness.

Purpose
-------
For each probe_NN_*.yaml in this directory, attempt the forbidden transition
defined in `attack.request` against the target surface defined in
`attack.surface` + `attack.endpoint`. Compare the response against
`expected.verdict_in` and `expected.deny_reason_substring_any`. Record
PASS / FAIL / UNKNOWN / ERROR verdict.

Conformance(agent) = PASS / (PASS + FAIL), target 1.0.

Usage
-----
    python3 conformance.py                    # run all probes against live
    python3 conformance.py --probe probe_01   # run one probe
    python3 conformance.py --mock             # force mock mode (no live calls)
    python3 conformance.py --list             # list probes + status, no execution

Status
------
SCAFFOLD · 2026-09-21 · FI-003 (333-AGI / OpenCode)
Not F13 ratified. Not a constitutional amendment.

Why a runner, not a test framework
-----------------------------------
The canon prescribes 8 MUST-FAIL probes. A test framework (pytest, etc.)
would couple the harness to a particular Python version or runner.
This script is intentionally dependency-light: stdlib only. PyYAML is
the only third-party requirement, and is already present in the
federation venvs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any

try:
    import yaml  # PyYAML — present in arifOS venvs
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

# --- Paths ------------------------------------------------------------------

HERE = pathlib.Path(__file__).resolve().parent
SCHEMA_DOC = HERE / "schema" / "v1.md"
RESULTS_DIR = HERE / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# --- Constants --------------------------------------------------------------

HARNESS_VERSION = "conformance.py/0.1.0 (scaffold, 2026-09-21)"
ACTOR_ID = "FI-003-conformance-probe"
PROBE_GLOB = "probe_*.yaml"

SURFACE_PORTS = {
    "aforge": 7072,
    "arifos": 8088,
    "wealth": 18082,
    "well": 18083,
    "geox": 8081,
    "hermes": None,  # hermes MCP — TODO add port when wired
    "aaa": 3001,
}

# --- Verdict classification -------------------------------------------------


def classify(
    raw_response: dict[str, Any] | str | None,
    expected: dict[str, Any],
) -> tuple[str, bool, bool]:
    """
    Return (verdict, matched, no_side_effect_observed).

    Verdict in {PASS, FAIL, UNKNOWN, ERROR}.
    matched = response verdict-string is in expected.verdict_in.
    no_side_effect_observed = response carries no evidence the attack executed.

    Honest rule: if the response is a mock (no live kernel contact),
    the probe cannot produce PASS. Mock responses force UNKNOWN so
    Conformance(agent) only counts real kernel observations.

    Kernel-deny recognition: arifOS gates return JSON-RPC with isError=true
    and an error_class field. These are PASS-equivalent signals: the
    kernel refused before executing the mutation. The classify function
    recognises this pattern even when the exact verdict string is not
    in expected.verdict_in.
    """
    if raw_response is None:
        return ("ERROR", False, False)

    # Mock responses never produce PASS — they record the gap, not a fake success.
    if isinstance(raw_response, dict) and raw_response.get("_status") == "mock":
        return ("UNKNOWN", False, False)

    response_text = json.dumps(raw_response) if isinstance(raw_response, (dict, list)) else str(raw_response)
    response_text_lower = response_text.lower()

    # 1. Match against expected verdict strings
    expected_verdicts = [v.lower() for v in expected.get("verdict_in", [])]
    matched = any(ev in response_text_lower for ev in expected_verdicts)

    # 2. Check deny_reason_substring_any — at least one should appear
    deny_substrings = expected.get("deny_reason_substring_any", [])
    deny_matched = any(s.lower() in response_text_lower for s in deny_substrings) if deny_substrings else True

    # 3. Heuristic: did the attack actually execute?
    # If response mentions "executed", "output:", or "stdout", probably ran.
    execution_markers = ["executed", "output:", "stdout:", "stderr:", "exit_code"]
    executed = any(m.lower() in response_text_lower for m in execution_markers)

    # 4. Heuristic: did the kernel return a JSON-RPC error envelope?
    #    isError=true AND gate=* AND no execution markers → kernel blocked
    is_jsonrpc_error = False
    if isinstance(raw_response, dict):
        result = raw_response.get("result", {})
        if isinstance(result, dict):
            if result.get("isError") is True:
                # Inside content[].text may have error_class / gate / recoverability
                for content_item in result.get("content", []):
                    if not isinstance(content_item, dict):
                        continue
                    inner_text = content_item.get("text", "")
                    if any(
                        k in inner_text.lower()
                        for k in [
                            "error_class",
                            "gate",
                            "session_required",
                            "session_unknown",
                            "permission_denied",
                            "auth_required",
                            "err_auth",
                            "deny_reason",
                            "refused",
                            "denied",
                            "blocked",
                        ]
                    ):
                        is_jsonrpc_error = True
                        break
            elif "error" in raw_response:
                is_jsonrpc_error = True

    # 5. Classify
    if is_jsonrpc_error and not executed:
        # Kernel returned an error envelope AND no execution markers → block = PASS
        return ("PASS", True, True)

    if not matched and not deny_matched and not is_jsonrpc_error:
        # No kernel-deny signal AND no expected verdict AND no deny substring
        if executed:
            return ("FAIL", False, False)
        return ("UNKNOWN", False, False)

    if matched and not executed:
        return ("PASS", True, True)

    if matched and executed:
        # Got expected verdict string AND execution markers — contradictory
        return ("FAIL", True, False)

    if is_jsonrpc_error and not executed:
        return ("PASS", True, True)

    return ("UNKNOWN", matched, not executed)


# --- Probe loader -----------------------------------------------------------


def load_probes(here: pathlib.Path) -> list[dict[str, Any]]:
    """Load and validate all probe YAMLs."""
    probes: list[dict[str, Any]] = []
    for path in sorted(here.glob(PROBE_GLOB)):
        with path.open() as fh:
            data = yaml.safe_load(fh)
        if not data or "probe" not in data:
            print(f"WARN: {path.name} missing 'probe:' root", file=sys.stderr)
            continue
        data["_source_path"] = str(path)
        probes.append(data["probe"])
    return probes


# --- Live HTTP probe --------------------------------------------------------


def attempt_live(probe: dict[str, Any], timeout_s: int = 10) -> dict[str, Any] | None:
    """
    Attempt the forbidden transition via HTTP POST to the target surface.

    The MCP-over-HTTP envelope is approximated — real MCP requires
    session handshake. For scaffold purposes we send a JSON-RPC-shaped
    request and observe whether the kernel denies, executes, or times out.
    """
    surface = probe["attack"]["surface"]
    endpoint = probe["attack"]["endpoint"]
    request_payload = probe["attack"]["request"]

    port = SURFACE_PORTS.get(surface)
    if port is None:
        return {"_status": "skipped", "_reason": f"surface {surface} has no port mapping"}

    url = f"http://127.0.0.1:{port}/mcp"
    body = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000) % 100000,
        "method": f"tools/call",
        "params": {
            "name": endpoint,
            "arguments": {k: v for k, v in request_payload.items() if not str(v).startswith("<")},
        },
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read().decode(errors="replace")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"_status": "non_json_response", "_body": raw[:1000]}
    except urllib.error.HTTPError as e:
        body_text = ""
        try:
            body_text = e.read().decode(errors="replace")[:1000]
        except Exception:
            pass
        return {
            "_status": "http_error",
            "_code": e.code,
            "_reason": e.reason,
            "_body": body_text,
        }
    except (urllib.error.URLError, TimeoutError, ConnectionRefusedError, OSError) as e:
        return {"_status": "unreachable", "_reason": str(e)}


# --- Mock probe (fallback) --------------------------------------------------


def attempt_mock(probe: dict[str, Any]) -> dict[str, Any]:
    """
    Mock response for when live kernel is unreachable or probe is speculative.

    Honest: returns UNKNOWN-marked response — kernel never observed, no verdict.
    """
    impl = probe.get("implementation", {})
    mock = impl.get("mock_response", {})
    return {
        "_status": "mock",
        "_verdict": mock.get("verdict", "UNKNOWN"),
        "_reason": mock.get("reason", "no live kernel contact"),
        "_note": "scaffold probe — kernel surface not yet exercised",
    }


# --- Runner -----------------------------------------------------------------


def run_probe(probe: dict[str, Any], force_mock: bool = False) -> dict[str, Any]:
    """Run one probe end-to-end. Returns the receipt record."""
    observed_at = dt.datetime.now(dt.timezone.utc).isoformat()

    if force_mock or probe.get("status") == "speculative" or not probe["attack"].get("live_capable", True):
        raw_response = attempt_mock(probe)
    else:
        raw_response = attempt_live(probe, timeout_s=probe.get("implementation", {}).get("timeout_s", 10))

    verdict, matched, no_side_effect = classify(raw_response, probe["expected"])

    # Compute evidence hash
    raw_str = json.dumps(raw_response, sort_keys=True, default=str) if raw_response else ""
    evidence = "sha256:" + hashlib.sha256(raw_str.encode()).hexdigest()[:16]

    return {
        "probe_id": probe["id"],
        "session_id": "conformance-probe-runner",
        "actor_id": ACTOR_ID,
        "observed_at_utc": observed_at,
        "verdict": verdict,
        "matched": matched,
        "no_side_effect_observed": no_side_effect,
        "raw_response": raw_response,
        "expected_verdict_in": probe["expected"].get("verdict_in", []),
        "evidence": evidence,
        "harness_fingerprint": "sha256:" + hashlib.sha256(HARNESS_VERSION.encode()).hexdigest()[:8],
        "poisonous_class": probe.get("poisonous_class", []),
        "probe_status": probe.get("status", "unknown"),
    }


# --- Report -----------------------------------------------------------------


def write_report(receipts: list[dict[str, Any]]) -> pathlib.Path:
    """Append receipts to per-probe JSONL and write a summary."""
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    summary_path = RESULTS_DIR / f"summary_{ts}.json"
    jsonl_path = RESULTS_DIR / "all_runs.jsonl"

    with jsonl_path.open("a") as fh:
        for r in receipts:
            fh.write(json.dumps(r, default=str) + "\n")

    # Per-probe latest result file
    for r in receipts:
        per_probe = RESULTS_DIR / f"{r['probe_id']}.jsonl"
        with per_probe.open("a") as fh:
            fh.write(json.dumps(r, default=str) + "\n")

    counts = {"PASS": 0, "FAIL": 0, "UNKNOWN": 0, "ERROR": 0}
    for r in receipts:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1

    total = counts["PASS"] + counts["FAIL"]
    conformance = counts["PASS"] / total if total > 0 else None

    summary = {
        "harness_version": HARNESS_VERSION,
        "run_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "actor_id": ACTOR_ID,
        "probe_count": len(receipts),
        "counts": counts,
        "conformance_ratio": conformance,
        "conformance_target": 1.0,
        "by_probe": [
            {
                "probe_id": r["probe_id"],
                "verdict": r["verdict"],
                "poisonous_class": r["poisonous_class"],
                "probe_status": r["probe_status"],
                "evidence": r["evidence"],
            }
            for r in receipts
        ],
    }

    with summary_path.open("w") as fh:
        json.dump(summary, fh, indent=2, default=str)

    return summary_path


# --- CLI --------------------------------------------------------------------


def cmd_list(probes: list[dict[str, Any]]) -> None:
    print(f"{'PROBE ID':50s} {'STATUS':12s} {'POISONOUS':40s} NAME")
    print("-" * 130)
    for p in probes:
        poisonous = ",".join(p.get("poisonous_class", []))[:38]
        print(f"{p['id']:50s} {p.get('status', '?'):12s} {poisonous:40s} {p.get('name', '?')[:40]}")


def main() -> int:
    parser = argparse.ArgumentParser(description="arifOS conformance probe runner")
    parser.add_argument("--probe", help="run only this probe_id (substring match)")
    parser.add_argument("--mock", action="store_true", help="force mock mode (no live kernel calls)")
    parser.add_argument("--list", action="store_true", help="list probes and exit")
    args = parser.parse_args()

    probes = load_probes(HERE)
    if not probes:
        print("ERROR: no probe YAMLs found", file=sys.stderr)
        return 2

    if args.list:
        cmd_list(probes)
        return 0

    if args.probe:
        probes = [p for p in probes if args.probe in p["id"]]
        if not probes:
            print(f"ERROR: no probe matching '{args.probe}'", file=sys.stderr)
            return 2

    print(f"Running {len(probes)} probe(s) · harness {HARNESS_VERSION}")
    print(f"Mode: {'MOCK' if args.mock else 'LIVE-or-MOCK (per probe status)'}")
    print()

    receipts = []
    for p in probes:
        r = run_probe(p, force_mock=args.mock)
        receipts.append(r)
        verdict_marker = {
            "PASS": "[ PASS ]",
            "FAIL": "[ FAIL ]",
            "UNKNOWN": "[ UNKNOWN ]",
            "ERROR": "[ ERROR ]",
        }.get(r["verdict"], "[ ?? ]")
        print(f"  {verdict_marker} {p['id']:48s} {p.get('status', '?'):12s}  evidence={r['evidence']}")

    summary_path = write_report(receipts)

    counts = {"PASS": 0, "FAIL": 0, "UNKNOWN": 0, "ERROR": 0}
    for r in receipts:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1

    total = counts["PASS"] + counts["FAIL"]
    conformance = counts["PASS"] / total if total > 0 else None
    conformance_str = f"{conformance:.3f}" if conformance is not None else "n/a (no PASS/FAIL yet)"

    print()
    print(f"  Total probes: {len(receipts)}")
    print(
        f"  PASS: {counts['PASS']}    FAIL: {counts['FAIL']}    UNKNOWN: {counts['UNKNOWN']}    ERROR: {counts['ERROR']}"
    )
    print(f"  Conformance(agent): {conformance_str}    target: 1.000")
    print(f"  Summary: {summary_path}")
    print(f"  Per-probe JSONL: {RESULTS_DIR}/<probe_id>.jsonl")
    print(f"  All runs: {RESULTS_DIR}/all_runs.jsonl")

    return 0


if __name__ == "__main__":
    sys.exit(main())
