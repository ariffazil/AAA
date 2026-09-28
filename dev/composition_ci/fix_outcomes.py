#!/usr/bin/env python3
"""
fix_outcomes.py — Measure actual deltas from the 5-fix forge plan.

Lane B RECEIPT — no kernel mutation, no doctrine change.

Measures:
  Fix #1 — evidence param now in _synthesize_async (function signature check)
  Fix #2 — arif_route(mode=...) remaining in code source (should be 0 in code,
           5 in published JSON which is out of Lane B scope)
  Fix #3 — _MUTATION_TOOLS frozenset present + passive bypass
  Fix #4 — witness_state on front line in canonical_envelope
  Fix #5 — canonical_envelope byte size vs legacy _inject_nine_signal estimate
"""
from __future__ import annotations
import hashlib, importlib, json, sys
from pathlib import Path

ROOT = Path("/root")
REPORT_PATH = ROOT / "AAA" / "dev" / "composition_ci" / "fix_outcomes.json"
REPORT_MD = ROOT / "AAA" / "dev" / "composition_ci" / "fix_outcomes.md"


def m1_evidence_param_present() -> dict:
    """Fix #1: _synthesize_async must accept evidence= param."""
    try:
        from arifosmcp.runtime.tools import _synthesize_async
        import inspect
        sig = inspect.signature(_synthesize_async)
        params = list(sig.parameters.keys())
        return {"present": "evidence" in params, "params": params, "verdict": "PASS" if "evidence" in params else "FAIL"}
    except Exception as e:
        return {"present": False, "error": str(e), "verdict": "UNKNOWN"}


def m2_route_mode_references_remaining() -> dict:
    """Fix #2: count remaining arif_route(mode=...) refs in PYTHON code only."""
    import re
    root = ROOT / "arifOS" / "arifosmcp"
    refs = []
    for f in root.rglob("*.py"):
        try:
            t = f.read_text()
            for m in re.finditer(r'arif_route\s*\(\s*[^)]*mode\s*=', t):
                line = t[:m.start()].count('\n') + 1
                refs.append({"file": str(f.relative_to(ROOT)), "line": line})
        except Exception:
            pass
    # also check arifosd.py
    ad = ROOT / "arifOS" / "scripts" / "arifosd.py"
    if ad.exists():
        t = ad.read_text()
        for m in re.finditer(r'arif_route\s*\(\s*[^)]*mode\s*=', t):
            line = t[:m.start()].count('\n') + 1
            refs.append({"file": "arifOS/scripts/arifosd.py", "line": line})
    return {"remaining_in_python": len(refs), "refs": refs, "verdict": "PASS" if len(refs) == 0 else "PARTIAL"}


def m3_mutation_set_present() -> dict:
    """Fix #3: _MUTATION_TOOLS frozenset + passive bypass in _membrane_scan."""
    try:
        from arifosmcp.runtime import tools as T
        import inspect
        src = inspect.getsource(T)
        has_set = "_MUTATION_TOOLS" in src and "frozenset" in src
        has_bypass = "if tool not in _MUTATION_TOOLS" in src
        return {"present": has_set and has_bypass, "has_set": has_set, "has_bypass": has_bypass, "verdict": "PASS" if (has_set and has_bypass) else "FAIL"}
    except Exception as e:
        return {"present": False, "error": str(e), "verdict": "UNKNOWN"}


def m4_witness_state_present() -> dict:
    """Fix #4: witness_state surfaced in envelope."""
    try:
        from arifosmcp.federation.federation_envelope import apex_witness_state, finalize_response_envelope
        w = apex_witness_state()
        env = finalize_response_envelope({"status": "OK"}, envelope=None, organ_status="ok", provenance="test")
        present_in_env = "witness_state" in env.get("response", {})
        return {
            "apex_witness_state_returns": isinstance(w, dict) and "status" in w,
            "witness_state_in_finalize": present_in_env,
            "default_status": w.get("status"),
            "verdict": "PASS" if (present_in_env and w.get("status") == "SOLO_UNVERIFIED") else "PARTIAL"
        }
    except Exception as e:
        return {"present": False, "error": str(e), "verdict": "UNKNOWN"}


def m5_canonical_envelope_size() -> dict:
    """Fix #5: canonical_envelope vs legacy 9-signal stack size."""
    try:
        from arifosmcp.federation.federation_envelope import canonical_envelope
        env = canonical_envelope(
            session_id="sess-test",
            actor_id="arif",
            authority="OBSERVE_ONLY",
            synthesis="this is a test synthesis for measurement purposes only",
            confidence=0.42,
            evidence_items=[{"label": "OBS-1", "content": "first observation"}],
            next_action="probe next",
        )
        canonical_bytes = len(json.dumps(env, separators=(",", ":")))

        # Simulate legacy envelope stack (nine_signal + live_envelope + v2_envelope + federation_envelope + kernel_envelope)
        # Use a realistic minimal shape for each layer.
        legacy = {
            "nine_signal": {
                "rosak": 0, "lapuk": 0, "karat": 0, "bengkok": 0, "hilang": 0,
                "pecah": 0, "retak": 0, "lengai": 0, "sedar": 1,
                "weights": {"rosak": 0.11, "lapuk": 0.11, "karat": 0.11, "bengkok": 0.11, "hilang": 0.11, "pecah": 0.11, "retak": 0.11, "lengai": 0.11, "sedar": 0.11},
                "_source": "nine_signal_v1",
            },
            "live_envelope": {
                "request_hash": "abc123" * 10,  # 240 char SHA
                "normalized_payload_hash": "def456" * 10,
                "raw_request_hash": "ghi789" * 10,
                "live_probe": {"geox": "OK", "wealth": "OK", "well": "DEGRADED", "aaa": "OK", "arifOS": "OK"},
                "federation_chain": ["a", "b", "c", "d", "e", "f", "g", "h"],
                "_source": "live_envelope_v1",
            },
            "v2_envelope": {
                "schema_version": "2.0.0",
                "target_organ": "arifOS",
                "target_tool": "arif_think",
                "actor": {"id": "arif", "verified": False},
                "session": {"id": "sess-test", "epoch": 5},
                "constitutional_intent": {"L01": True, "L02": True, "L03": False, "L04": True, "L07": True},
                "_source": "v2_envelope",
            },
            "federation_envelope": {
                "schema_version": "ws9-v1",
                "request": {"request_hash": "x" * 64, "normalized_payload_hash": "y" * 64},
                "response": {"organ_status": "OK", "response_hash": "z" * 64, "raw_request_hash": "x" * 64, "normalized_payload_hash": "y" * 64, "request_hash": "x" * 64, "target_organ": "arifOS", "target_tool": "arif_think"},
                "_source": "federation_envelope",
            },
            "kernel_envelope": {
                "kernel_mode": "OBSERVE_ONLY",
                "degradation": None,
                "trace_parent": "00-aaaa-bbbb-01",
                "_source": "kernel_envelope",
            },
        }
        legacy_bytes = len(json.dumps(legacy, separators=(",", ":")))

        reduction_pct = (1 - canonical_bytes / legacy_bytes) * 100 if legacy_bytes > 0 else 0
        return {
            "canonical_bytes": canonical_bytes,
            "legacy_bytes_estimated": legacy_bytes,
            "reduction_pct": round(reduction_pct, 1),
            "verdict": "PASS" if reduction_pct > 30 else "PARTIAL"
        }
    except Exception as e:
        return {"present": False, "error": str(e), "verdict": "UNKNOWN"}


def main() -> dict:
    results = {
        "schema_version": "1.0.0-lane-b",
        "kind": "FixOutcomes",
        "authority_class": "OBSERVE_ONLY",
        "lane": "B",
        "verdict": "RECEIPT_NOT_SEAL",
        "do_not_treat_as_seal": True,
        "Fix_1_evidence_param":   m1_evidence_param_present(),
        "Fix_2_route_mode_refs":  m2_route_mode_references_remaining(),
        "Fix_3_mutation_set":     m3_mutation_set_present(),
        "Fix_4_witness_state":    m4_witness_state_present(),
        "Fix_5_envelope_size":    m5_canonical_envelope_size(),
    }

    REPORT_PATH.write_text(json.dumps(results, indent=2))
    raw = REPORT_PATH.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()

    md = ["# Fix Outcomes — Lane B RECEIPT (2026-09-27)\n",
          f"**Authority:** OBSERVE_ONLY · **Lane:** B · **Verdict:** RECEIPT_NOT_SEAL · `do_not_treat_as_seal=true`\n",
          f"**SHA256:** `{sha}`\n",
          "\n## Per-fix outcomes\n"]
    for k, v in results.items():
        if k.startswith("Fix_"):
            md.append(f"- **{k}** → `{v}`")
    md.append("\n## Verdict matrix\n")
    md.append("| Fix | Verdict | Notes |")
    md.append("|-----|---------|-------|")
    md.append(f"| #1 evidence param | {results['Fix_1_evidence_param']['verdict']} | param in sig: {results['Fix_1_evidence_param'].get('present')} |")
    md.append(f"| #2 route mode refs | {results['Fix_2_route_mode_refs']['verdict']} | remaining in .py: {results['Fix_2_route_mode_refs']['remaining_in_python']} |")
    md.append(f"| #3 mutation set | {results['Fix_3_mutation_set']['verdict']} | set={results['Fix_3_mutation_set'].get('has_set')} bypass={results['Fix_3_mutation_set'].get('has_bypass')} |")
    md.append(f"| #4 witness state | {results['Fix_4_witness_state']['verdict']} | default={results['Fix_4_witness_state'].get('default_status')} |")
    f5 = results['Fix_5_envelope_size']
    md.append(f"| #5 envelope size | {f5['verdict']} | canonical={f5.get('canonical_bytes')}B, legacy={f5.get('legacy_bytes_estimated')}B, reduction={f5.get('reduction_pct')}% |")
    md.append("\n---\n*DITEMPA BUKAN DIBERI ⚒️*\n")
    REPORT_MD.write_text("\n".join(md))

    print(f"Wrote: {REPORT_PATH}", file=sys.stderr)
    print(f"SHA256: {sha}", file=sys.stderr)
    print(json.dumps({"verdict": results["verdict"], "sha256": sha,
                       "fix_5_reduction_pct": f5.get("reduction_pct")}, indent=2))
    return results


if __name__ == "__main__":
    main()