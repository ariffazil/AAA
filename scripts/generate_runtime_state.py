#!/usr/bin/env python3
"""generate_runtime_state.py — probe live federation components, write runtime-state.json.

PR-2 FEDERATION-SOT. Static institutional truth lives in federation/components.yaml
(identity, class, role). This script owns the LIVE side: it probes each component
over HTTP and generates federation/runtime-state.json whose entries carry the README
observation fields (observed_at, source, source_age_seconds, confidence,
probe_method, failure_reason).

The probe table below is EXECUTABLE CONFIG, not doctrine. Port discovery reads
/root/.kimi-code/mcp.json when present (never guessed); components without a
resolvable URL are emitted as state=UNKNOWN with probe_method=UNRESOLVED_PORT.

Rules:
  - timeout 4s per request, read-only (GET; at most an MCP `initialize` POST,
    which creates no state)
  - an unreachable component is DATA, not an error — the script never crashes on
    failure and never hides one behind a default (void guard)
  - generated file carries header `_generated: true`; hand edits get overwritten

Usage:
    python3 scripts/generate_runtime_state.py
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "federation" / "runtime-state.json"
MCP_JSON_PATH = Path("/root/.kimi-code/mcp.json")
GENERATOR_ID = "scripts/generate_runtime_state.py v1 (FI-008 · PR-2 FEDERATION-SOT)"
TIMEOUT_S = 4.0
USER_AGENT = "aaa-runtime-state-probe/1.0 (read-only reachability probe)"

MCP_ACCEPT = "application/json, text/event-stream"
MCP_INITIALIZE = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "aaa-runtime-state-probe", "version": "1.0.0"},
    },
}

# Probe table — executable config. `mcp_json_key` names the entry in
# /root/.kimi-code/mcp.json whose "url" field overrides the default URL.
# `candidates` are tried in order; the first candidate that yields ANY HTTP
# response wins (a listener answering is reachability evidence even on 4xx).
PROBE_TABLE: List[Dict[str, Any]] = [
    {"component": "HERMES",   "default_url": "http://127.0.0.1:18087/health", "mcp_json_key": "hermes"},
    {"component": "CHRON",    "default_url": "http://127.0.0.1:18102/health", "mcp_json_key": "chron"},
    {"component": "GEOX",     "default_url": "http://127.0.0.1:8081/mcp",     "mcp_json_key": "geox"},
    {"component": "A-FORGE",  "default_url": "http://127.0.0.1:7072/mcp",     "mcp_json_key": None},
    {"component": "arifFlow", "default_url": "http://127.0.0.1:7073/health",  "mcp_json_key": "arifFlow"},
    {"component": "arifOS",   "default_url": "http://127.0.0.1:8088/health",  "mcp_json_key": None,
     "fallback_url": "http://127.0.0.1:8088/", "best_effort": True},
    {"component": "WEALTH",   "default_url": "http://127.0.0.1:18082/mcp",    "mcp_json_key": "wealth"},
    {"component": "WELL",     "default_url": "http://127.0.0.1:18083/mcp",    "mcp_json_key": "well"},
    {"component": "FRAME",    "default_url": "http://127.0.0.1:18086/mcp",    "mcp_json_key": "frame"},
    {"component": "FED",      "default_url": "http://127.0.0.1:7074/mcp",     "mcp_json_key": "fed"},
]


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_mcp_json() -> Optional[dict]:
    try:
        with MCP_JSON_PATH.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data.get("mcpServers", {}) if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return None


def resolve_url(entry: Dict[str, Any], mcp_servers: Optional[dict]) -> tuple[Optional[str], str]:
    """Return (url, port_source). url=None means unresolvable."""
    key = entry.get("mcp_json_key")
    if mcp_servers and key:
        declared = mcp_servers.get(key) or {}
        url = declared.get("url")
        if isinstance(url, str) and url.startswith("http"):
            return url, f"/root/.kimi-code/mcp.json#{key}"
    default_url = entry.get("default_url")
    if default_url:
        return default_url, "probe-table default"
    return None, "unresolved"


def _base_observation(component: str, url: Optional[str], probe_method: str,
                      port_source: str) -> Dict[str, Any]:
    return {
        "component": component,
        "dimension": "http_reachability",
        "state": "UNKNOWN",
        "observed_at": _utcnow_iso(),
        "source": url if url else "UNRESOLVED",
        "source_age_seconds": 0.0,
        "confidence": 0.0,
        "probe_method": probe_method,
        "failure_reason": None,
        "detail": {"port_source": port_source},
    }


def _http_probe(url: str, method: str = "GET", body: Optional[dict] = None) -> requests.Response:
    headers = {"User-Agent": USER_AGENT, "Accept": MCP_ACCEPT}
    if method == "POST":
        return requests.post(url, json=body, headers=headers, timeout=TIMEOUT_S, allow_redirects=False)
    return requests.get(url, headers=headers, timeout=TIMEOUT_S, allow_redirects=False)


def probe_component(entry: Dict[str, Any], mcp_servers: Optional[dict]) -> Dict[str, Any]:
    component = entry["component"]
    url, port_source = resolve_url(entry, mcp_servers)
    if not url:
        obs = _base_observation(component, None, "UNRESOLVED_PORT", port_source)
        obs["failure_reason"] = (
            f"no probe URL resolvable for component {component}: "
            f"not declared in /root/.kimi-code/mcp.json and no probe-table default"
        )
        return obs

    candidates = [url]
    fallback = entry.get("fallback_url")
    if fallback:
        candidates.append(fallback)

    last_error: Optional[str] = None
    for candidate in candidates:
        try:
            started = time.monotonic()
            resp = _http_probe(candidate)
            elapsed = time.monotonic() - started
            obs = _base_observation(component, candidate, "GET (timeout 4s)", port_source)
            obs["source_age_seconds"] = round(elapsed, 3)
            if 200 <= resp.status_code < 400:
                obs["state"] = "REACHABLE"
                obs["confidence"] = 0.95
            elif 400 <= resp.status_code < 500:
                # e.g. 405/406 on GET of a POST-only MCP endpoint: the listener
                # answered, so the transport is present; semantics unverified.
                upgraded = _mcp_initialize_upgrade(candidate)
                obs["state"] = "REACHABLE"
                if upgraded:
                    obs["confidence"] = 0.9
                    obs["probe_method"] = "GET (timeout 4s) + MCP initialize POST"
                else:
                    obs["confidence"] = 0.7
            else:  # 5xx — listener exists, service is erroring
                obs["state"] = "REACHABLE"
                obs["confidence"] = 0.6
                obs["failure_reason"] = (
                    f"HTTP {resp.status_code} from listener (endpoint answered, service semantics unknown)"
                )
            return obs
        except requests.exceptions.Timeout:
            last_error = f"timeout after {TIMEOUT_S:g}s"
        except requests.exceptions.ConnectionError:
            last_error = "connection refused (no listener on this path)"
        except requests.exceptions.RequestException as exc:
            last_error = f"request error: {type(exc).__name__}: {exc}"
        except Exception as exc:  # never crash on probe failure — that is data
            last_error = f"unexpected probe error: {type(exc).__name__}: {exc}"

    obs = _base_observation(component, url, "GET (timeout 4s)", port_source)
    obs["state"] = "UNREACHABLE"
    obs["confidence"] = 0.85
    obs["failure_reason"] = last_error
    if fallback:
        obs["probe_method"] += " + fallback GET (timeout 4s)"
    return obs


def _mcp_initialize_upgrade(url: str) -> bool:
    """Best-effort MCP initialize to upgrade confidence on POST-only endpoints.

    Read-only: `initialize` creates a session object on the server at most; it
    mutates nothing in the federation. Failures are swallowed by the caller's
    reachability semantics (returning False just keeps confidence at 0.7).
    """
    try:
        resp = _http_probe(url, method="POST", body=MCP_INITIALIZE)
        return resp.status_code < 500
    except Exception:
        return False


def generate(output_path: Path = OUTPUT_PATH) -> Dict[str, Any]:
    mcp_servers = load_mcp_json()
    observations = [probe_component(entry, mcp_servers) for entry in PROBE_TABLE]

    payload = {
        "_generated": True,
        "generated_at": _utcnow_iso(),
        "generator": GENERATOR_ID,
        "probe_table_source": "scripts/generate_runtime_state.py PROBE_TABLE (executable config)",
        "port_discovery": str(MCP_JSON_PATH) if mcp_servers is not None else f"{MCP_JSON_PATH} (absent/unreadable)",
        "note": (
            "Runtime observations only — static identity lives in federation/components.yaml. "
            "Static identity != runtime health. Reachability observations do not imply "
            "service health, correctness, or authority (does_not_imply; cf. schemas/ir/MIGRATION.md invariant 7)."
        ),
        "does_not_imply": "REACHABLE != healthy != correct != authorized; UNREACHABLE != dead (probe may have timed out).",
        "observations": observations,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
    return payload


def main() -> int:
    try:
        payload = generate()
    except Exception as exc:  # last-resort guard: report, never traceback-crash
        print(f"GENERATION FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    reachable = sum(1 for o in payload["observations"] if o["state"] == "REACHABLE")
    print(f"wrote {OUTPUT_PATH}")
    print(
        f"observations: {len(payload['observations'])} · "
        f"REACHABLE: {reachable} · "
        f"UNREACHABLE/UNKNOWN: {len(payload['observations']) - reachable}"
    )
    for obs in payload["observations"]:
        flag = obs["failure_reason"] if obs["failure_reason"] else "ok"
        print(f"  {obs['component']:<9} {obs['dimension']}={obs['state']:<11} "
              f"conf={obs['confidence']:.2f}  ({flag})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
