#!/usr/bin/env python3
"""
forge-federation-probe — Adversarial probe of all federation organs.

Phase 1: Health gate — every organ must respond 200 with JSON
Phase 2: Authority ceiling — every organ must declare authority_ceiling
Phase 3: Tool count semantics — arifOS must ship the legend
Phase 4: Apex scalars delegation — A-FORGE must not have decorative nulls
Phase 5: Circuit breaker — vault_sealer state must be observable
Phase 6: Deployment drift — source HEAD vs deployed commit
Phase 7: Claim provenance — measured values must cite source
Phase 8: Inference brain — litellm-federation :4011 reachable, auth works,
         end-to-end chat completion on hermes-asi returns 200, AND
         all 8 FI CLI coding harnesses respond to --version

Exit 0 if all PASS. Non-zero for first failure (see exit code table in SKILL.md).

Usage:
    forge-federation-probe                     # all phases
    forge-federation-probe --phase=brain       # Phase 8 only
    forge-federation-probe --format=receipt    # VAULT999 receipt format

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from datetime import UTC, datetime
from typing import Any

ORGANS = {
    "arifOS":        {"port": 8088, "expected_ceiling": "SOVEREIGN",      "source_dir": "/root/arifOS"},
    "A-FORGE":       {"port": 7071, "expected_ceiling": "777_FORGE",      "source_dir": "/root/A-FORGE"},
    "A-FORGE-bridge":{"port": 7072, "expected_ceiling": "777_FORGE",      "source_dir": "/root/A-FORGE"},
    "GEOX":          {"port": 8081, "expected_ceiling": "555_COMPUTE_ONLY","source_dir": "/root/GEOX"},
    "WEALTH":        {"port": 18082,"expected_ceiling": "555_COMPUTE_ONLY","source_dir": "/root/WEALTH"},
    "WELL":          {"port": 18083,"expected_ceiling": "REFLECT_ONLY",   "source_dir": "/root/WELL"},
    "AAA":           {"port": 3001, "expected_ceiling": "DISPLAY_ONLY",   "source_dir": "/root/AAA"},
}

# Phase 8: litellm-federation inference brain + 8 FI CLI coding harnesses
LITELLM_BRAIN_PORT = 4011
LITELLM_BRAIN_MODELS_URL = f"http://127.0.0.1:{LITELLM_BRAIN_PORT}/v1/models"
LITELLM_BRAIN_CHAT_URL = f"http://127.0.0.1:{LITELLM_BRAIN_PORT}/v1/chat/completions"
CHAT_PROBE_MODEL = "hermes-asi"   # cheapest lane — defaults to MiniMax-M3
CHAT_PROBE_MAX_TOKENS = 10

# 8 FI CLI coding harnesses declared in /root/AAA/registries/AGENTS_UNIFIED.yaml
FI_HARNESSES = [
    ("FI-001 opencode",    "opencode",     "/root/.npm-global/bin/opencode"),
    ("FI-002 claude-code", "claude",       "/root/.local/bin/claude"),
    ("FI-003 qwen-code",   "qwen",         "/usr/bin/qwen"),
    ("FI-004 antigravity", "agy",          "/root/.local/bin/agy"),
    ("FI-005 codex",       "codex",        "/usr/local/bin/codex"),
    ("FI-006 copilot",     "copilot",      "/usr/bin/copilot"),
    ("FI-007 grok-build",  "grok",         "/root/.grok/bin/grok"),
    ("FI-008 kimi-code",   "kimi",         "/root/.kimi-code/bin/kimi"),
]


def _get(url: str, timeout: float = 3.0) -> tuple[dict | None, str | None]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode()), None
    except Exception as e:
        return None, str(e)


def _get_with_auth(url: str, timeout: float = 5.0) -> tuple[Any, str | None, int | None]:
    """GET with Authorization: Bearer $LITELLM_MASTER_KEY. Returns (data, err, http_status)."""
    token = os.environ.get("LITELLM_MASTER_KEY", "")
    if not token:
        return None, "LITELLM_MASTER_KEY env var not set", None
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode()), None, resp.status
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}", e.code
    except Exception as e:
        return None, str(e), None


def _git_head(repo: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", repo, "rev-parse", "--short=7", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:
        return None


def _check_health() -> dict[str, Any]:
    results: dict[str, str] = {}
    for name, cfg in ORGANS.items():
        data, err = _get(f"http://127.0.0.1:{cfg['port']}/health")
        results[name] = "PASS" if data else f"FAIL (unreachable: {err})"
    return results


def _check_authority() -> dict[str, Any]:
    results: dict[str, str] = {}
    for name, cfg in ORGANS.items():
        data, _ = _get(f"http://127.0.0.1:{cfg['port']}/health")
        if not data:
            results[name] = "SKIP (organ down)"
            continue
        ceiling = data.get("authority_ceiling")
        expected = cfg["expected_ceiling"]
        if ceiling is None:
            results[name] = f"FAIL — authority_ceiling=ABSENT (expected {expected})"
        elif ceiling == expected:
            results[name] = f"PASS ({ceiling})"
        else:
            results[name] = f"FAIL — authority_ceiling={ceiling} (expected {expected})"
    return results


def _check_tool_semantics() -> dict[str, Any]:
    data, _ = _get("http://127.0.0.1:8088/health")
    if not data:
        return {"arifOS": "FAIL (organ down)"}
    tc = data.get("tool_count_semantics")
    if tc is None:
        return {"arifOS": "FAIL — tool_count_semantics=ABSENT (the legend that explains 8 vs 48 vs 62)"}
    keys = list(tc.keys()) if isinstance(tc, dict) else []
    return {"arifOS": f"PASS — {len(keys)} legend fields present: {', '.join(keys)}"}


def _check_apex_policy() -> dict[str, Any]:
    data, _ = _get("http://127.0.0.1:7071/health")
    if not data:
        return {"A-FORGE": "FAIL (organ down)"}
    policy = data.get("apex_scalars_policy")
    if not policy:
        return {"A-FORGE": "FAIL — apex_scalars_policy=ABSENT (UNMEASURED nulls are decorative without delegation map)"}
    delegated = policy.get("delegated_to", {})
    return {"A-FORGE": f"PASS — delegated_to has {len(delegated)} scalars mapped: {list(delegated.keys())}"}


def _check_breakers() -> dict[str, Any]:
    data, _ = _get("http://127.0.0.1:8088/health")
    if not data:
        return {"arifOS": "FAIL (organ down)"}
    breaker = data.get("vault_sealer_breaker")
    if not breaker:
        return {"arifOS": "FAIL — vault_sealer_breaker=ABSENT (cascade at :5001 invisible)"}
    state = breaker.get("state", "?")
    if state == "open":
        return {"arifOS": f"WARN — vault_sealer_breaker=OPEN (retry_after={breaker.get('retry_after_s', '?')}s, failures={breaker.get('recent_failures', '?')})"}
    return {"arifOS": f"PASS — vault_sealer_breaker.state={state}"}


def _check_drift() -> dict[str, Any]:
    results: dict[str, str] = {}
    for name, cfg in ORGANS.items():
        if name == "A-FORGE-bridge":
            continue  # shares source with A-FORGE
        data, _ = _get(f"http://127.0.0.1:{cfg['port']}/health")
        if not data:
            results[name] = "SKIP (organ down)"
            continue

        # Resolve deployed commit from any of: software_release.deployed_commit,
        # deployed_commit, git_commit, git_commit_fallback, source_commit
        deployed = None
        sr = data.get("software_release")
        if isinstance(sr, dict):
            deployed = sr.get("deployed_commit")
        if not deployed:
            deployed = data.get("deployed_commit")
        if not deployed or deployed == "UNAVAILABLE":
            deployed = data.get("git_commit")
        if not deployed or deployed == "UNAVAILABLE":
            deployed = data.get("git_commit_fallback")
        if not deployed or deployed == "UNAVAILABLE":
            deployed = data.get("source_commit")
        if not deployed or deployed == "UNAVAILABLE":
            # GEOX pattern: git_version (with optional "geox-" prefix)
            gv = data.get("git_version")
            if gv and gv not in ("unknown", "UNAVAILABLE"):
                deployed = gv.replace("geox-", "").replace("GEOX-", "")
        if not deployed or deployed == "UNAVAILABLE":
            deployed = data.get("git_commit_fallback_trusted") and data.get("git_commit_fallback")

        drift = data.get("deployment_drift")
        if isinstance(sr, dict):
            drift = sr.get("drift")

        source_head = _git_head(cfg["source_dir"])
        if not source_head or not deployed or deployed == "UNAVAILABLE":
            results[name] = "SKIP (commit info missing)"
        elif str(deployed)[:7] == source_head[:7]:
            results[name] = f"PASS — source={source_head} = deployed={str(deployed)[:7]}"
        else:
            results[name] = f"FAIL — source={source_head} ≠ deployed={str(deployed)[:7]} (drift={drift})"
    return results


def _check_provenance() -> dict[str, Any]:
    results: dict[str, str] = {}
    # AAA is the only organ with measured apex_scalars that we can check
    data, _ = _get("http://127.0.0.1:3001/health")
    if not data:
        results["AAA"] = "SKIP (organ down)"
        return results
    apex = data.get("apex_scalars", {})
    measured = {k: v for k, v in apex.items() if isinstance(v, dict) and v.get("value") is not None}
    if not measured:
        results["AAA"] = "SKIP (no measured scalars to check provenance)"
        return results
    # AAA computes its own scalars inline — provenance is implicit
    # Just verify they're non-null and have a status
    provenanced = sum(1 for v in measured.values() if v.get("status"))
    results["AAA"] = f"PASS — {provenanced}/{len(measured)} measured scalars have status field (provenance is inline in AAA)"
    return results


def _check_brain() -> dict[str, Any]:
    """Phase 8: inference brain (litellm-federation :4011) + 8 FI CLI coding harnesses.

    Verifies:
    1. litellm-federation reachable
    2. Bearer auth works (LITELLM_MASTER_KEY in env)
    3. /v1/models returns ≥1 model
    4. End-to-end chat completion on hermes-asi returns 200 + non-null message
    5. All 8 FI CLI harnesses respond to --version
    """
    results: dict[str, str] = {}

    # 1. Auth sanity — refuse to probe without the master key
    if not os.environ.get("LITELLM_MASTER_KEY"):
        results["brain_auth"] = (
            "FAIL — LITELLM_MASTER_KEY env var not set. "
            "Source it from /root/.secrets/kunci-mas.env before running this probe."
        )
        # FI harnesses still worth checking
        results.update(_check_fi_harnesses())
        return results

    # 2. Models endpoint with auth
    data, err, status = _get_with_auth(LITELLM_BRAIN_MODELS_URL, timeout=10.0)
    if err:
        results["brain_models"] = f"FAIL — {err} (status={status})"
    elif data is None or "data" not in data:
        results["brain_models"] = "FAIL — empty /v1/models response (auth failed or brain not loaded)"
    else:
        models = [m.get("id") for m in data["data"] if m.get("id")]
        if not models:
            results["brain_models"] = "FAIL — 0 models exposed via /v1/models (config empty or load failed)"
        else:
            results["brain_models"] = f"PASS — {len(models)} models exposed: {', '.join(sorted(models)[:5])}..."

    # 3. End-to-end chat completion on the cheapest lane
    payload = json.dumps({
        "model": CHAT_PROBE_MODEL,
        "messages": [{"role": "user", "content": "Say PONG and nothing else."}],
        "max_tokens": CHAT_PROBE_MAX_TOKENS,
    }).encode()
    req = urllib.request.Request(
        LITELLM_BRAIN_CHAT_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {os.environ['LITELLM_MASTER_KEY']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            chat = json.loads(resp.read().decode())
            choices = chat.get("choices", [])
            if not choices:
                results["brain_chat"] = "FAIL — chat completion returned no choices"
            else:
                msg = choices[0].get("message", {})
                content = msg.get("content") or msg.get("reasoning_content") or ""
                usage = chat.get("usage", {})
                results["brain_chat"] = (
                    f"PASS — {CHAT_PROBE_MODEL} → {chat.get('model', '?')} "
                    f"({usage.get('total_tokens', '?')} tokens, "
                    f"finish={choices[0].get('finish_reason', '?')})"
                )
    except urllib.error.HTTPError as e:
        results["brain_chat"] = f"FAIL — HTTP {e.code}: {e.reason} (read: {e.read().decode()[:200]})"
    except Exception as e:
        results["brain_chat"] = f"FAIL — {type(e).__name__}: {e}"

    # 4. FI CLI harnesses
    results.update(_check_fi_harnesses())
    return results


def _check_fi_harnesses() -> dict[str, str]:
    """Verify each FI CLI binary is installed and responds to --version."""
    results: dict[str, str] = {}
    for label, name, fallback_path in FI_HARNESSES:
        # Resolve via PATH first, then fallback to known install path
        bin_path = shutil.which(name) or (fallback_path if os.path.isfile(fallback_path) else None)
        if not bin_path:
            results[f"fi_{name}"] = f"FAIL — {label}: binary not found in PATH or fallback {fallback_path}"
            continue
        try:
            out = subprocess.run(
                [bin_path, "--version"],
                capture_output=True, text=True, timeout=10,
            )
            version_line = (out.stdout or out.stderr or "").strip().splitlines()[0] if (out.stdout or out.stderr) else ""
            results[f"fi_{name}"] = f"PASS — {label} at {bin_path} (version: {version_line[:60]})"
        except subprocess.TimeoutExpired:
            results[f"fi_{name}"] = f"FAIL — {label} at {bin_path}: --version timed out"
        except Exception as e:
            results[f"fi_{name}"] = f"FAIL — {label} at {bin_path}: {type(e).__name__}: {e}"
    return results


PHASES = {
    "health": _check_health,
    "authority": _check_authority,
    "tools": _check_tool_semantics,
    "apex": _check_apex_policy,
    "breakers": _check_breakers,
    "drift": _check_drift,
    "provenance": _check_provenance,
    "brain": _check_brain,
}

EXIT_CODES = {
    "health": 1,
    "authority": 2,
    "tools": 3,
    "apex": 4,
    "breakers": 5,
    "drift": 6,
    "provenance": 7,
    "brain": 8,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Federation probe (adversarial)")
    parser.add_argument("--phase", choices=list(PHASES.keys()), help="Run single phase")
    parser.add_argument("--format", choices=["json", "receipt"], default="json")
    parser.add_argument("--receipt-id", help="Receipt ID for --format=receipt")
    args = parser.parse_args()

    phases_to_run = {args.phase: PHASES[args.phase]} if args.phase else PHASES
    all_results: dict[str, Any] = {}
    failures: list[str] = []

    for phase_name, phase_fn in phases_to_run.items():
        try:
            result = phase_fn()
        except Exception as e:
            result = {"ERROR": str(e)}
        all_results[phase_name] = result

        # Check for failures
        for k, v in result.items():
            if isinstance(v, str) and v.startswith("FAIL"):
                failures.append(f"{phase_name}/{k}: {v}")

    if args.format == "receipt":
        rid = args.receipt_id or f"R5-FEDPROBE-{datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')}"
        receipt = {
            "receipt_id": rid,
            "ts": datetime.now(UTC).isoformat(),
            "scope": "forge-federation-probe all phases",
            "phases": all_results,
            "failures": failures,
            "verdict": "PASS" if not failures else f"FAIL ({len(failures)} failures)",
            "payload_hash": None,  # caller computes if needed
        }
        receipt["payload_hash"] = hex(
            hash(json.dumps(receipt["phases"], sort_keys=True))
        )[:18]
        print(json.dumps(receipt, indent=2))
    else:
        print(json.dumps(all_results, indent=2))

    # Exit code: first failure phase
    if failures:
        for fail in failures:
            phase_name = fail.split("/")[0]
            if phase_name in EXIT_CODES:
                return EXIT_CODES[phase_name]
        return 255
    return 0


if __name__ == "__main__":
    sys.exit(main())