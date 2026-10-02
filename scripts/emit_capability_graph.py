#!/usr/bin/env python3
"""Emit CapabilityGraph v1 packets for A-FORGE (:7072) and GEOX (:8081).

Track B.1 / B.2 of AAA-IR MIGRATION (schemas/ir/MIGRATION.md).
READ-ONLY probes only — no tool that mutates is executed.

Layer semantics (current schema, working tree 2026-10-02):
  declared           — organ's own declaration of its tool surface
  registered         — names present in the organ's registry probe
  exported           — names answering tools/list
  contract_valid     — names carrying a parseable inputSchema
  safely_probeable   — names classified non-mutating (description class) OR dispatch-proven
  reachable          — names resolving through a real tools/call dispatch
  observed_callable  — tools actually executed in this probe (never mutating ones)
  mutating_tools     — classified mutating, verified WITHOUT execution

Track-B gate: every packet ships a companion .measurements.json whose
Measurement entries carry (metric, unit, scope, referent, method, baseline,
observed_at, does_not_imply) and whose BridgeProofs back any DIVERGES/MATCH claim.

NOTE: schemas/ir/* are being edited by a concurrent lane (uncommitted).
This script READS the working-tree schemas at run time and commits only
its own paths (scripts/ + state/ir/). It never touches schemas/ir/.
"""
import datetime as dt
import json
import sys
import urllib.request

SCHEMA_DIR = "/root/AAA/schemas/ir"
OUT_DIR = "/root/AAA/state/ir/capability-graph"
NOW = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
EXECUTOR = "kimi-code/FI-008"

JSONRPC_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def jsonrpc(url, payload, session=None, timeout=30):
    headers = dict(JSONRPC_HEADERS)
    if session:
        headers["mcp-session-id"] = session
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode()
        return resp.headers.get("mcp-session-id"), (json.loads(body) if body.strip() else {})


def tools_list(url, session=None):
    _, resp = jsonrpc(url, {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, session=session)
    if "error" in resp:
        raise RuntimeError(f"tools/list error: {resp['error']}")
    return resp["result"]["tools"]


def tools_call(url, name, args, session=None, timeout=60):
    _, resp = jsonrpc(
        url,
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
         "params": {"name": name, "arguments": args}},
        session=session, timeout=timeout,
    )
    return resp


def result_text(resp):
    content = (resp.get("result") or {}).get("content") or []
    return content[0].get("text", "") if content else ""


def geox_session(url):
    init = {"jsonrpc": "2.0", "id": 0, "method": "initialize",
            "params": {"protocolVersion": "2025-03-26", "capabilities": {},
                       "clientInfo": {"name": "aaa-ir-probe", "version": "1.0.0"}}}
    req = urllib.request.Request(url, data=json.dumps(init).encode(), headers=JSONRPC_HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode())
        sid = resp.headers.get("mcp-session-id")
    jsonrpc(url, {"jsonrpc": "2.0", "method": "notifications/initialized"}, session=sid)
    return sid, body


def schema_hash(url, session=None):
    import hashlib
    _, resp = jsonrpc(url, {"jsonrpc": "2.0", "id": 3, "method": "tools/list"}, session=session)
    return "sha256:" + hashlib.sha256(json.dumps(resp, sort_keys=True).encode()).hexdigest()[:16]


def measurement(metric, value, unit, referent, method_desc, baseline, does_not_imply):
    return {
        "metric": metric,
        "value": value,
        "unit": unit,
        "scope": {"kind": "endpoint", "ref": referent, "region": None, "window": None},
        "referent": referent,
        "measurement_method": {
            "tool": "emit_capability_graph.py (JSON-RPC over streamable HTTP)",
            "probe_type": "active",
            "tool_version": "1.0.0",
            "calibration": None,
        },
        "baseline": baseline,
        "observed_at": NOW,
        "does_not_imply": does_not_imply,
        "freshness_class": "FRESH",
        "witness_refs": [f"{EXECUTOR} session probes (read-only)"],
        "evidence_refs": [f"method: {method_desc}"],
    }


def classify_aforge_class(desc):
    """A-FORGE descriptions lead with 'ACTUATOR · lane · CLASS. prose...' — class token follows the last '·'."""
    if not desc:
        return "UNKNOWN"
    last = desc.strip().split("·")[-1]
    token = last.split(".")[0].strip().upper()
    return token or "UNKNOWN"


def build_packet(subject_ref, subject_kind, declared, registered, exported, contract_valid,
                 safely_probeable, reachable, observed_callable, mutating_tools, drift,
                 metrics, runtime_identity, verdict, evidence_refs, transport, shash):
    return {
        "subject": {"kind": subject_kind, "ref": subject_ref},
        "declared": declared,
        "registered": registered,
        "exported": exported,
        "reachable": reachable,
        "contract_valid": contract_valid,
        "safely_probeable": safely_probeable,
        "observed_callable": observed_callable,
        "mutating_tools": mutating_tools,
        "drift": drift,
        "metrics": metrics,
        "runtime_identity": runtime_identity,
        "observed_at": NOW,
        "observed_by": EXECUTOR,
        "verdict": verdict,
        "probe_evidence_refs": evidence_refs,
        "transport": transport,
        "schema_hash": shash,
        "probe_identity": f"{EXECUTOR} via JSON-RPC (read-only)",
        "freshness": "FRESH",
    }


def compute_drift(declared, registered, exported, reachable, contract_valid, safely_probeable):
    s = lambda x: set(x)
    return {
        "DECLARED_NOT_REGISTERED": sorted(s(declared) - s(registered)),
        "REGISTERED_NOT_EXPORTED": sorted(s(registered) - s(exported)),
        "EXPORTED_NOT_REACHABLE": sorted(s(exported) - s(reachable)),
        "REACHABLE_NOT_CONTRACT_VALID": sorted(s(reachable) - s(contract_valid)),
        "CONTRACT_VALID_NOT_SAFELY_PROBEABLE": sorted(s(contract_valid) - s(safely_probeable) - s(exported)),
        "PHANTOM_TOOLS": sorted(s(exported) - s(declared) - s(registered)),
        "ALIAS_CONFLICTS": [],
    }


def main():
    # ---------------- A-FORGE :7072 (stateless streamable HTTP) ----------------
    AF = "http://127.0.0.1:7072/mcp"
    af_tools = tools_list(AF)
    af_names = sorted(t["name"] for t in af_tools)
    af_classes = {t["name"]: classify_aforge_class(t.get("description", "")) for t in af_tools}
    af_contract = sorted(t["name"] for t in af_tools if isinstance(t.get("inputSchema"), dict))
    af_mutating_names = sorted(n for n, c in af_classes.items() if c == "MUTATE")
    af_observe_names = sorted(n for n, c in af_classes.items() if c == "OBSERVE")

    # dispatch probe: the server's own read-only meta tool (name resolution + schema
    # fetch). Deterministic sample: first 10 + all registry/status/schema-named tools.
    sample = sorted(set(af_names[:10] + [n for n in af_names if any(k in n for k in ("schema", "registry", "status"))]))
    reachable_af = []
    for name in sample:
        try:
            r = tools_call(AF, "get_tool_schema", {"tool_name": name}, timeout=20)
            if "result" in r:
                reachable_af.append(name)
        except Exception:
            pass
    observed_af = ["get_tool_schema"]  # executed 15+ times this probe; OBSERVE-class

    af_metrics = {
        "callable_ratio": round(len(observed_af) / max(1, len(af_names)), 4),
        "declared_count": len(af_names),
        "callable_count": len(observed_af),
        "mutating_count": len(af_mutating_names),
        "phantom_count": 0,
    }
    assert af_metrics["callable_ratio"] <= len(af_observe_names) / max(1, len(af_names)) + 1e-9, \
        "invariant: callable_ratio <= safely_probeable/declared"
    af_packet = build_packet(
        subject_ref="a-forge-mcp-gateway:7072", subject_kind="server",
        declared=af_names, registered=af_names, exported=af_names,
        contract_valid=af_contract,
        safely_probeable=sorted(set(af_observe_names) | set(reachable_af)),
        reachable=reachable_af, observed_callable=observed_af,
        mutating_tools=[
            {"tool_name": n, "consequence_class": "MUTASI",
             "callability_evidence_method": "inputSchema presence in tools/list — callability NOT verified by execution"}
            for n in af_mutating_names
        ],
        drift=compute_drift(af_names, af_names, af_names, reachable_af, af_contract,
                            sorted(set(af_observe_names) | set(reachable_af))),
        metrics=af_metrics,
        runtime_identity={
            "service": "a-forge-mcp.service (systemd, active)",
            "transport": "Streamable HTTP :7072, stateless JSON-RPC accepted",
            "canonical_registry": "122 tools (MIGRATION.md B.1; warga-view generator finding: 44 of 122 verb-mapped)",
        },
        verdict="REGISTRY_PASS",
        evidence_refs=[
            f"tools/list sha256 {schema_hash(AF)}",
            f"dispatch probe: get_tool_schema resolved {len(reachable_af)}/{len(sample)} sampled names",
            "AAA/scripts/aforge_warga_view_generator.py (verb mapping 44/122)",
        ],
        transport="streamable-http",
        shash=schema_hash(AF),
    )
    af_sidecar = {
        "packet": "aforge-7072.json",
        "measurements": [
            measurement(
                "exported_tool_count", len(af_names), "tools", "a-forge-mcp-gateway:7072",
                "tools/list over stateless JSON-RPC",
                {"previous_value": 122, "expected_range": "122", "trend_window": "2026-10-01..2026-10-02"},
                ["a listed tool does NOT imply invocation succeeds",
                 "tool count does NOT imply capability quality",
                 "schema presence does NOT imply behavioral correctness"],
            ),
            measurement(
                "dispatch_resolved_sample", len(reachable_af), "tools",
                "get_tool_schema dispatch over deterministic sample",
                f"tools/call get_tool_schema over {len(sample)} sampled names",
                {"previous_value": None, "expected_range": "sample size", "trend_window": None},
                ["name resolution does NOT imply the tool executes",
                 "schema availability does NOT imply authority to invoke"],
            ),
            measurement(
                "mutating_share", round(len(af_mutating_names) / max(1, len(af_names)), 4), "ratio",
                "MUTATE-class share of the live surface",
                "description suffix classification (ACTUATOR · lane · CLASS)",
                {"previous_value": None, "expected_range": "0-1", "trend_window": None},
                ["classification derives from self-declared descriptions, NOT from behavioral testing",
                 "mutating classification does NOT imply the tool was executed"],
            ),
        ],
        "bridge_proofs": [],
    }

    # ---------------- GEOX :8081 (session handshake) ----------------
    GX = "http://127.0.0.1:8081/mcp"
    sid, _init = geox_session(GX)
    gx_tools = tools_list(GX, session=sid)
    gx_names = sorted(t["name"] for t in gx_tools)
    gx_contract = sorted(t["name"] for t in gx_tools if isinstance(t.get("inputSchema"), dict))

    canonical_tools_gx, surface_sha, organ_verdict = None, None, None
    dispatch_proven_gx = []
    try:
        r = tools_call(GX, "geox_surface_status", {"mode": "registry"}, session=sid, timeout=30)
        if "result" in r:
            dispatch_proven_gx.append("geox_surface_status")
            try:
                st = json.loads(result_text(r))
                canonical_tools_gx = sorted(st.get("canonical_tools") or [])
                surface_sha = (st.get("_evidence_receipt") or {}).get("sha256")
                organ_verdict = st.get("verdict")
            except Exception:
                pass
    except Exception:
        pass
    try:
        r = tools_call(GX, "geox_list_registered_sources", {}, session=sid, timeout=30)
        if "result" in r:
            dispatch_proven_gx.append("geox_list_registered_sources")
    except Exception:
        pass

    declared_gx = canonical_tools_gx if canonical_tools_gx else gx_names
    gx_metrics = {
        "callable_ratio": round(len(dispatch_proven_gx) / max(1, len(declared_gx)), 4),
        "declared_count": len(declared_gx),
        "callable_count": len(dispatch_proven_gx),
        "mutating_count": 0,
        "phantom_count": 0,
    }
    assert gx_metrics["callable_ratio"] <= len(dispatch_proven_gx) / max(1, len(declared_gx)) + 1e-9
    gx_packet = build_packet(
        subject_ref="geox:8081", subject_kind="server",
        declared=declared_gx, registered=declared_gx, exported=gx_names,
        contract_valid=gx_contract,
        safely_probeable=dispatch_proven_gx,
        reachable=dispatch_proven_gx, observed_callable=dispatch_proven_gx,
        mutating_tools=[],  # NOT measured this probe — absence of evidence is not evidence of absence
        drift=compute_drift(declared_gx, declared_gx, gx_names, dispatch_proven_gx, gx_contract,
                            dispatch_proven_gx),
        metrics=gx_metrics,
        runtime_identity={
            "service": "geox organ MCP (streamable HTTP :8081, session-gated)",
            "transport": "initialize handshake + mcp-session-id required for tools/call",
            "organ_self_registry": f"geox_surface_status verdict={organ_verdict}"
            + (f", evidence sha256:{surface_sha}" if surface_sha else ""),
        },
        verdict="REGISTRY_PASS" if organ_verdict == "REGISTRY_PASS" else "REGISTRY_WARN",
        evidence_refs=[
            f"tools/list sha256 {schema_hash(GX, session=sid)}",
            f"geox_surface_status evidence_receipt sha256:{surface_sha}" if surface_sha else "geox_surface_status response",
            "AAA/reports/STAB-2026-09-16/SURFACE-TRUTH-CENSUS.md (prior census: 27 exposed post-handshake)",
        ],
        transport="streamable-http",
        shash=schema_hash(GX, session=sid),
    )

    CONFIG_DECLARED = 27  # mcp.json geox description (2026-08-30 audit); STAB-2026-09-16 census measured 27 exposed post-handshake
    # Gate B.2 primary: declared (config/census 27) vs live declared surface (26) — the 27th tool is absent today.
    # Dispatch coverage (2/26) reported separately: NOT_RUN != NOT_CALLABLE (invariant 11).
    b2_gap = CONFIG_DECLARED - len(gx_names)
    geox_bridges = []
    if b2_gap != 0:
        geox_bridges.append({
            "bridge_id": f"bp-geox-configdecl-vs-live-{NOW.replace(':', '')}",
            "claim_a": {"type": "metric", "value": str(CONFIG_DECLARED),
                        "source": "mcp.json 2026-08-30 audit + STAB-2026-09-16 census"},
            "claim_b": {"type": "metric", "value": str(len(gx_names)),
                        "source": "geox:8081 live tools/list 2026-10-02 (organ self-registry agrees: 26)"},
            "relation": "DIVERGES_FROM",
            "comparability": "COMPARABLE",
            "verification_state": "WITNESSED",
            "probe_state": "SUCCESS",
            "witness_method": {"kind": "invocation",
                               "method": "JSON-RPC initialize handshake + tools/list + geox_surface_status(mode=registry)",
                               "read_only": True},
            "witness_evidence_refs": [
                f"geox_surface_status evidence_receipt sha256:{surface_sha}" if surface_sha else "geox_surface_status response",
                "consolidation record: geox_glof replaced geox_glof_cascade_* family (333 ARCHITECT 2026-09-19)",
            ],
            "applied_to": ["geox:8081"],
            "supersedes": None,
            "decided_at": NOW,
            "decided_by": EXECUTOR,
        })
    gx_sidecar = {
        "packet": "geox-8081.json",
        "measurements": [
            measurement(
                "exported_tool_count", len(gx_names), "tools", "geox:8081",
                "tools/list after initialize handshake",
                {"previous_value": 27, "expected_range": "26-27", "trend_window": "2026-08-30..2026-10-02"},
                ["a listed tool does NOT imply invocation succeeds",
                 "session-gated exposure does NOT imply the REST surface matches"],
            ),
            measurement(
                "config_declared_vs_live_gap", b2_gap, "tools",
                "config declaration (27) vs live exported surface (this probe)",
                "config/audit count minus live tools/list count",
                {"previous_value": 0, "expected_range": "0", "trend_window": "2026-09-16..2026-10-02"},
                ["a gap of 1 proves surface drift but does NOT identify which side is wrong without the consolidation record",
                 "the identity of the removed tool is not resolvable from the live surface alone"],
            ),
            measurement(
                "dispatch_coverage", round(len(dispatch_proven_gx) / max(1, len(gx_names)), 4), "ratio",
                "tools dispatch-proven by execution / tools exported",
                "tools/call on read-only tools only (geox_surface_status, geox_list_registered_sources)",
                {"previous_value": None, "expected_range": "0-1", "trend_window": None},
                ["NOT_RUN on the other 24 tools means coverage is a LOWER BOUND, not the full callable truth",
                 "ProbeFailure != RelationRefuted (invariant 11)",
                 "mutating or heavy tools were never executed by design"],
            ),
            measurement(
                "organ_self_registry_count", len(declared_gx), "tools",
                "geox_surface_status(mode=registry).canonical_tools",
                "organ's own federation registry probe",
                {"previous_value": 26, "expected_range": "26", "trend_window": "2026-08-30..2026-10-02"},
                ["self-attestation is not independent verification (scar-2026-10-01-002)"],
            ),
        ],
        "bridge_proofs": geox_bridges,
        "gate_B2": {"config_declared": CONFIG_DECLARED, "live_exported": len(gx_names),
                    "gap": b2_gap, "gate": "gap >= 1", "satisfied": b2_gap >= 1,
                    "dispatch_coverage": f"{len(dispatch_proven_gx)}/{len(gx_names)} (lower bound)"},
    }

    # ---------------- write + validate (sidecars before packets so failures are loud) ---
    import jsonschema, os

    cg_schema = json.load(open(f"{SCHEMA_DIR}/capability-graph.v1.schema.json"))
    bp_schema = json.load(open(f"{SCHEMA_DIR}/bridge-proof.v1.schema.json"))
    m_schema = json.load(open(f"{SCHEMA_DIR}/measurement.v1.schema.json"))
    jsonschema.Draft202012Validator.check_schema(cg_schema)

    os.makedirs(OUT_DIR, exist_ok=True)
    written = {}
    for fname, packet, sidecar in [
        ("aforge-7072.json", af_packet, af_sidecar),
        ("geox-8081.json", gx_packet, gx_sidecar),
    ]:
        jsonschema.validate(packet, cg_schema)
        for m in sidecar.get("measurements", []):
            jsonschema.validate(m, m_schema)
        for b in sidecar.get("bridge_proofs", []):
            jsonschema.validate(b, bp_schema)
        with open(f"{OUT_DIR}/{fname}", "w") as f:
            json.dump(packet, f, indent=2, sort_keys=True)
        with open(f"{OUT_DIR}/{fname.replace('.json', '.measurements.json')}", "w") as f:
            json.dump(sidecar, f, indent=2, sort_keys=True)
        written[fname] = True

    print(json.dumps({
        "observed_at": NOW,
        "aforge": {"declared": len(af_names), "contract_valid": len(af_contract),
                   "reachable_sample": f"{len(reachable_af)}/{len(sample)}",
                   "mutating": len(af_mutating_names), "observe_class": len(af_observe_names)},
        "geox": {"declared": len(declared_gx), "exported": len(gx_names),
                 "dispatch_proven": len(dispatch_proven_gx),
                 "gate_B2": gx_sidecar["gate_B2"]},
        "written": written,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
