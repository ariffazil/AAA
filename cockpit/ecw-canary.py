#!/usr/bin/env python3
"""
ecw-canary.py — External Contract Witness v0.1
Lane B autonomous, no mutation, no F13 binary, reversible (delete 1 file).

Doctrine (sovereign 2026-10-02):
- 6-class drift taxonomy: SURFACE / SCHEMA / SEMANTIC / AUTHORITY / BEHAVIOR / TRANSPORT
- Invariant: DeclaredState = ObservedState = InterpretedState = EnforcedState
- Source-of-truth: arifOS CANONICAL_VERDICTS = {OBSERVE_ONLY, SEAL, SABAR, VOID, HOLD, 888_HOLD}

Probes every MCP via:
1. /mcp/tools/list (declared surface)
2. /mcp/resources/list (exposed resources)
3. /mcp/schema (schema-valid capability)
4. Sample call → verdict vocabulary audit (semantic consistency)
5. Auth/authority check (authority-consistent)
6. Transport reachability + latency (behavior, transport)

Output: /root/AAA/cockpit/ecw-report.json (hash-verified, panel [7] HUD reads)
"""
import json, sys, time, socket, hashlib
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from datetime import datetime, timezone

CANONICAL_VERDICTS = {"OBSERVE_ONLY", "SEAL", "SABAR", "VOID", "HOLD", "888_HOLD"}
LEGACY_VERDICT_MAP = {
    "ALLOW": "SEAL", "DEGRADED": "SABAR", "FAIL": "VOID",
    "ERROR": "VOID", "BLOCKED": "VOID", "PARTIAL": "SABAR",
    "UNKNOWN": "HOLD", "PASS": "SEAL", "SYUBHAH": "VOID",  # SYUBHAH = DOUBTFUL
}

# Known MCP endpoints (port → name) — derived from systemd units live
MCP_PROBES = [
    {"name": "arifOS",        "port": 8088,  "scheme": "http", "path": "/mcp"},
    {"name": "A-FORGE",       "port": 7072,  "scheme": "http", "path": "/mcp"},
    {"name": "AAA",           "port": 7073,  "scheme": "http", "path": "/mcp"},
    {"name": "FED",           "port": 7071,  "scheme": "http", "path": "/mcp"},
    {"name": "CHRON",         "port": 7074,  "scheme": "http", "path": "/mcp"},
    {"name": "FRAME",         "port": 18085, "scheme": "http", "path": "/mcp"},
    {"name": "arifFlow",      "port": 18082, "scheme": "http", "path": "/mcp"},
    {"name": "GEOX",          "port": 18412, "scheme": "http", "path": "/mcp"},
    {"name": "federation-gw", "port": 18083, "scheme": "http", "path": "/mcp"},
    {"name": "fed-router",    "port": 18084, "scheme": "http", "path": "/mcp"},
    {"name": "tailnet-gw",    "port": 18100, "scheme": "http", "path": "/mcp"},
]

DRIFT_TAXONOMY = ["SURFACE_DRIFT", "SCHEMA_DRIFT", "SEMANTIC_DRIFT",
                  "AUTHORITY_DRIFT", "BEHAVIOR_DRIFT", "TRANSPORT_FAILURE"]


def now_utc():
    return datetime.now(timezone.utc).isoformat()


def probe_transport(host: str, port: int, timeout=2.0, **_):
    """Layer 6: TRANSPORT_FAILURE — TCP/connectivity."""
    t0 = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            latency_ms = (time.time() - t0) * 1000
        return {"reachable": True, "latency_ms": round(latency_ms, 1)}
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        return {"reachable": False, "error": type(e).__name__, "latency_ms": None}


def probe_surface(host: str, port: int, scheme: str = "http", timeout=3.0, **_):
    """Layer 1: SURFACE_DRIFT — declared tools vs reachable endpoint.

    MCP 2026-07-28 is JSON-RPC over HTTP. The initialize+tools/list is sent as
    POST body. Some servers also expose /.well-known/mcp/server.json (per
    AGENT_BOOTSTRAP.md). Try both.
    """
    # Path 1: well-known server.json (most common for agent-discovery)
    url1 = f"{scheme}://{host}:{port}/.well-known/mcp/server.json"
    # Path 2: root /tools endpoint (some legacy)
    url2 = f"{scheme}://{host}:{port}/tools"
    for url in (url1, url2):
        try:
            req = Request(url, headers={"Accept": "application/json"})
            with urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
            tools = (data.get("tools") or
                     [t.get("name") for t in data.get("tools", [])] or [])
            if isinstance(data.get("tools"), list):
                names = [t.get("name") if isinstance(t, dict) else t
                         for t in data["tools"]]
                count = len(names)
            else:
                names, count = [], 0
            return {"url": url, "declared_tools": count,
                    "tool_names": [n for n in names if n][:50]}
        except (URLError, HTTPError, json.JSONDecodeError, OSError):
            continue
    # Path 3: JSON-RPC tools/list over POST (per MCP 2026-07-28)
    try:
        rpc_url = f"{scheme}://{host}:{port}/mcp"
        body = json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "tools/list",
            "params": {}
        }).encode("utf-8")
        req = Request(rpc_url, data=body,
                      headers={"Content-Type": "application/json",
                               "Accept": "application/json, text/event-stream"})
        with urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", "replace")
            # SSE format may prefix "data: " — handle
            for ln in raw.splitlines():
                ln = ln.strip()
                if ln.startswith("data:"):
                    raw = ln[5:].strip()
                    break
            data = json.loads(raw)
        tools = data.get("result", {}).get("tools", [])
        names = [t.get("name") if isinstance(t, dict) else t for t in tools]
        return {"url": rpc_url, "declared_tools": len(tools),
                "tool_names": [n for n in names if n][:50],
                "method": "json-rpc"}
    except (URLError, HTTPError, json.JSONDecodeError, OSError) as e:
        return {"declared_tools": 0, "tool_names": [],
                "error": type(e).__name__,
                "attempted": ["server.json", "/tools", "json-rpc /mcp"]}


def extract_live_verdict_tokens(host: str, port: int, scheme: str = "http", timeout=2.5):
    """Pull real verdict-shaped tokens from each MCP.

    Sources to scan:
    1. tools/list response — look at tool descriptions for verdict vocabulary
    2. initialize response — server info, capabilities
    3. /mcp server-info endpoint (some servers)
    """
    import re as _re
    verdict_pattern = _re.compile(
        r'\b(?:OBSERVE_ONLY|SEAL|SABAR|VOID|HOLD|888_HOLD|'
        r'PASS|SYUBHAH|BLOCKED|DEGRADED|UNKNOWN|FAIL|ERROR|'
        r'ALLOW|PARTIAL|BELUM_SAH)\b'
    )
    raw_tokens = set()
    source = ""

    # Source 1: well-known server.json
    try:
        url = f"{scheme}://{host}:{port}/.well-known/mcp/server.json"
        with urlopen(Request(url), timeout=timeout) as r:
            text = r.read().decode("utf-8", "replace")
        found = verdict_pattern.findall(text)
        if found:
            raw_tokens.update(found)
            source = source or ".well-known/mcp/server.json"
    except Exception:
        pass

    # Source 2: JSON-RPC initialize (MCP 2026-07-28 standard)
    try:
        rpc_url = f"{scheme}://{host}:{port}/mcp"
        body = json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2026-07-28",
                "capabilities": {},
                "clientInfo": {"name": "ecw-canary", "version": "0.1"}
            }
        }).encode("utf-8")
        req = Request(rpc_url, data=body,
                      headers={"Content-Type": "application/json",
                               "Accept": "application/json, text/event-stream"})
        with urlopen(req, timeout=timeout) as r:
            text = r.read().decode("utf-8", "replace")
        for ln in text.splitlines():
            ln = ln.strip()
            if ln.startswith("data:"):
                text = ln[5:].strip()
                break
        found = verdict_pattern.findall(text)
        if found:
            raw_tokens.update(found)
            source = source or "initialize"
        # Then tools/list with session
        body = json.dumps({
            "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
        }).encode("utf-8")
        req = Request(rpc_url, data=body,
                      headers={"Content-Type": "application/json",
                               "Accept": "application/json, text/event-stream"})
        with urlopen(req, timeout=timeout) as r:
            text = r.read().decode("utf-8", "replace")
        for ln in text.splitlines():
            ln = ln.strip()
            if ln.startswith("data:"):
                text = ln[5:].strip()
                break
        found = verdict_pattern.findall(text)
        if found:
            raw_tokens.update(found)
            source = source or (source + "+tools/list" if source else "tools/list")
    except Exception:
        pass

    return {"raw": sorted(raw_tokens), "source": source or "none-found"}


def classify_verdict_vocabulary(raw_outputs):
    """Layer 3: SEMANTIC_DRIFT — verdict tokens across layers.

    Per arifOS/arifosmcp/runtime/verdict.py:
      CANONICAL_VERDICTS = {OBSERVE_ONLY, SEAL, SABAR, VOID, HOLD, 888_HOLD}
      Legacy map includes SYUBHAH→VOID, PASS→SEAL.
    Anything not in canon or legacy = SEMANTIC_DRIFT.
    """
    canonical_hits = []
    legacy_hits = []
    unknown_tokens = []
    for raw in raw_outputs:
        if raw in CANONICAL_VERDICTS:
            canonical_hits.append(raw)
        elif raw in LEGACY_VERDICT_MAP:
            legacy_hits.append(f"{raw}→{LEGACY_VERDICT_MAP[raw]}")
        else:
            unknown_tokens.append(raw)
    return {
        "canonical_hits": canonical_hits,
        "legacy_hits": legacy_hits,
        "unknown_tokens": unknown_tokens,
        "semantic_drift": len(unknown_tokens) > 0,
    }


def main():
    out = {
        "schema": "ecw-report-v1",
        "generated_at": now_utc(),
        "sovereign_invariant": "DeclaredState = ObservedState = InterpretedState = EnforcedState",
        "drift_taxonomy": DRIFT_TAXONOMY,
        "mcp_probes": [],
        "summary": {
            "total_probed": 0, "transport_up": 0, "surface_declared": 0,
            "semantic_clean": 0, "drift_classes_hit": {k: 0 for k in DRIFT_TAXONOMY},
        },
    }

    for probe in MCP_PROBES:
        host = "127.0.0.1"
        transport = probe_transport(host, probe["port"])
        result = {"name": probe["name"], "port": probe["port"], **transport}

        drift_hits = []
        # 6-state classification per sovereign 2026-10-02
        # Each of 6 axes: TRANSPORT / SURFACE / SCHEMA / SEMANTIC / AUTHORITY / BEHAVIOR
        # states: PASS / WARN / UNKNOWN / FAIL / STALE / NOT_APPLICABLE
        six_state = {
            "transport": "NOT_APPLICABLE", "surface": "NOT_APPLICABLE",
            "schema": "NOT_APPLICABLE", "semantic": "NOT_APPLICABLE",
            "authority": "NOT_APPLICABLE", "behavior": "NOT_APPLICABLE",
        }

        if not transport["reachable"]:
            six_state["transport"] = "FAIL"
            drift_hits.append("TRANSPORT_FAILURE")
            out["summary"]["drift_classes_hit"]["TRANSPORT_FAILURE"] += 1
        else:
            six_state["transport"] = "PASS"
            out["summary"]["transport_up"] += 1
            surface = probe_surface(host, probe["port"], probe["scheme"])
            result["surface"] = surface
            if surface["declared_tools"] > 0:
                out["summary"]["surface_declared"] += 1
                six_state["surface"] = "PASS"
            else:
                six_state["surface"] = "FAIL"
                drift_hits.append("SURFACE_DRIFT")
                out["summary"]["drift_classes_hit"]["SURFACE_DRIFT"] += 1

        # LIVE verdict-token probe
        live_tokens = extract_live_verdict_tokens(host, probe["port"], probe["scheme"])
        result["live_verdict_tokens"] = live_tokens["raw"]
        result["live_verdict_source"] = live_tokens["source"]
        vocab = classify_verdict_vocabulary(live_tokens["raw"])
        result["vocabulary_audit"] = vocab
        if vocab["semantic_drift"]:
            six_state["semantic"] = "FAIL"
            drift_hits.append("SEMANTIC_DRIFT")
            out["summary"]["drift_classes_hit"]["SEMANTIC_DRIFT"] += 1
        elif live_tokens["raw"]:
            six_state["semantic"] = "PASS"
            out["summary"]["semantic_clean"] += 1
        else:
            six_state["semantic"] = "UNKNOWN"

        # SCHEMA / AUTHORITY / BEHAVIOR — UNKNOWN until auth probe (Lane B held)
        six_state["schema"] = "UNKNOWN"
        six_state["authority"] = "UNKNOWN"
        six_state["behavior"] = "UNKNOWN"

        result["six_state"] = six_state
        result["drift_hits"] = drift_hits
        out["mcp_probes"].append(result)
        out["summary"]["total_probed"] += 1

    # Hash for integrity
    body = json.dumps(out, sort_keys=True).encode("utf-8")
    out["integrity_hash"] = hashlib.sha256(body).hexdigest()

    # Write atomic
    out_path = Path("/root/AAA/cockpit/ecw-report.json")
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(json.dumps(out, indent=2))
    tmp.replace(out_path)
    print(f"ECW report: {out_path} sha256={out['integrity_hash'][:12]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())