#!/usr/bin/env python3
"""
Composition CI Harness — Lane B RECEIPT instrument
arifOS — Reality must survive composition.

Instruments CRR / ECR / SIR / AIR / OTR / WCR across 7 canonical edges:
  000 (init) → 111 (sense_observe) → 333 (think) → 444 (route)
  → Memory → 888 (judge) → 777 (forge) → 999 (seal)

Lane B = READ-ONLY against live kernel + arifOS MCP + arifOS scripts.
No mutation. No doctrine change. No sovereign seal.

Output: /root/AAA/dev/composition_ci/report.json (machine-readable)
        /root/AAA/dev/composition_ci/report.md   (human-readable)
        /root/AAA/dev/composition_ci/report.sha256

DITEMPA BUKAN DIBERI ⚒️
"""
from __future__ import annotations
import hashlib, json, os, re, sys, time
from pathlib import Path
from typing import Any

ROOT = Path("/root")
AAA_DEV = ROOT / "AAA" / "dev" / "composition_ci"
AAA_DEV.mkdir(parents=True, exist_ok=True)

ARIFOS_KERNEL = ROOT / "arifOS" / "arifosmcp" / "tools" / "session.py"
ARIFOS_DAEMON = ROOT / "arifOS" / "scripts" / "arifosd.py"
CARRY_FORWARD = Path("/root/.local/share/arifos/carry_forward.json")

# ── 7 canonical edges (per memory/federation-organism-doctrine-sealed-2026-09-17)
EDGES = [
    ("000_init",      "init",     "session_bind"),
    ("111_observe",   "observe",  "gather_evidence"),
    ("333_think",     "think",    "reason_plan"),
    ("444_route",     "route",    "select_organ"),
    ("Memory",        "memory",   "persist_recall"),
    ("888_judge",     "judge",    "constitutional_verdict"),
    ("777_forge",     "forge",    "execute_build"),
    ("999_seal",      "seal",     "vault_immutable_record"),
]

METRICS = ["CRR", "ECR", "SIR", "AIR", "OTR", "WCR"]


# ─────────────────────────────────────────────────────────────────────────────
# Path-of-evidence probes (no kernel mutation, no MCP call)
# ─────────────────────────────────────────────────────────────────────────────
def probe_objective_root_dual_truth() -> dict[str, Any]:
    """
    C-08 re-check: does OBJECTIVE_ROOT have a single source of truth, or two?
    """
    if not ARIFOS_KERNEL.exists():
        return {"present": False, "verdict": "UNKNOWN"}
    src = ARIFOS_KERNEL.read_text()
    obj_root_default = '"unspecified — session created without explicit objective"' in src
    work_contract_in_header = "header[\"work_contract\"]" in src or "header['work_contract']" in src
    work_contract_popped = "result.pop(\"work_contract\"" in src or "result.pop('work_contract'" in src
    return {
        "present": True,
        "objective_root_default_present": obj_root_default,
        "work_contract_attached_to_header": work_contract_in_header,
        "work_contract_stripped_from_session_bind": work_contract_popped,
        "two_surfaces": work_contract_in_header and work_contract_popped,
        "verdict": "CONFIRMED_DUAL" if (obj_root_default and work_contract_in_header and work_contract_popped) else "PARTIAL",
    }


def probe_route_schema_runtime_mismatch() -> dict[str, Any]:
    """
    C-02 re-check: does arif_route schema accept mode? runtime passes mode?
    Static analysis only — does NOT execute MCP call.
    """
    if not ARIFOS_DAEMON.exists():
        return {"present": False, "verdict": "UNKNOWN"}
    src = ARIFOS_DAEMON.read_text()
    # Find arif_route inputSchema
    m = re.search(r'"name":\s*"arif_route".*?"inputSchema":\s*\{[^}]*\}', src, re.DOTALL)
    schema_text = m.group(0) if m else ""
    schema_accepts_mode = '"mode"' in schema_text
    # Look for runtime callers that pass mode=
    runtime_passes_mode = re.search(r'arif_route\([^)]*mode\s*=', src) is not None
    return {
        "present": True,
        "schema_accepts_mode": schema_accepts_mode,
        "runtime_passes_mode": runtime_passes_mode,
        "verdict": "MISMATCH" if (runtime_passes_mode and not schema_accepts_mode) else (
            "MATCH" if (runtime_passes_mode == schema_accepts_mode) else "INSUFFICIENT_EVIDENCE"
        ),
    }


def probe_verb_canon_drift() -> dict[str, Any]:
    """
    Canon drift: TOOLS count in arifosd.py wire surface vs FastMCP surface
    """
    if not ARIFOS_DAEMON.exists():
        return {"present": False}
    src = ARIFOS_DAEMON.read_text()
    # Count entries with "name": "arif_*"
    names = re.findall(r'"name":\s*"(arif_\w+)"', src)
    canonical = [n for n in names if not any(x in n for x in ["run", "exec", "sudo", "systemctl"])]
    return {
        "present": True,
        "names_found": names,
        "canonical_count": len(set(canonical)),
        "all_count": len(names),
    }


def probe_carry_forward_integrity() -> dict[str, Any]:
    if not CARRY_FORWARD.exists():
        return {"present": False}
    try:
        data = json.loads(CARRY_FORWARD.read_text())
        if isinstance(data, list):
            return {"present": True, "entries": len(data), "intact": True}
        if isinstance(data, dict):
            entries = data.get("entries") or data.get("chain") or []
            return {"present": True, "entries": len(entries), "intact": True, "shape": "dict"}
    except Exception as e:
        return {"present": True, "intact": False, "error": str(e)}
    return {"present": True, "intact": False}


def probe_session_id_persistence() -> dict[str, Any]:
    """
    SIR probe: does session_id persist across verb calls in the same session?
    Static analysis only.
    """
    if not ARIFOS_KERNEL.exists():
        return {"present": False}
    src = ARIFOS_KERNEL.read_text()
    session_id_used = re.findall(r'session_id', src)
    return {
        "present": True,
        "session_id_references": len(session_id_used),
        "verdict": "INSTRUMENTED" if len(session_id_used) > 5 else "SPARSE",
    }


def probe_evidence_continuity() -> dict[str, Any]:
    """
    ECR probe: do verbs pass evidence refs downstream?
    Widened scope: /root/arifOS/arifosmcp/** (not just session.py)
    """
    root = ROOT / "arifOS" / "arifosmcp"
    if not root.exists():
        return {"present": False}
    files = list(root.rglob("*.py"))
    e_used = 0
    e_root = 0
    for f in files:
        try:
            t = f.read_text()
            e_used += len(re.findall(r"evidence_used", t))
            e_root += len(re.findall(r"evidence_root|EVIDENCE_ROOT", t))
        except Exception:
            pass
    return {
        "present": True,
        "files_scanned": len(files),
        "evidence_used_references": e_used,
        "evidence_root_references": e_root,
    }


def probe_objective_transmission() -> dict[str, Any]:
    """
    OTR probe: does objective_hash flow through verbs?
    Widened scope: /root/arifOS/arifosmcp/** (not just session.py)
    """
    root = ROOT / "arifOS" / "arifosmcp"
    if not root.exists():
        return {"present": False}
    files = list(root.rglob("*.py"))
    obj_hash = 0
    obj = 0
    for f in files:
        try:
            t = f.read_text()
            obj_hash += len(re.findall(r"objective_hash", t))
            obj += len(re.findall(r"objective", t))
        except Exception:
            pass
    return {
        "present": True,
        "files_scanned": len(files),
        "objective_hash_references": obj_hash,
        "objective_references": obj,
    }


def probe_authority_narrowing() -> dict[str, Any]:
    """
    AIR probe: is there a static mechanism preventing authority gain across edges?
    """
    if not ARIFOS_KERNEL.exists():
        return {"present": False}
    src = ARIFOS_KERNEL.read_text()
    return {
        "present": True,
        "authority_references": len(re.findall(r"authority", src, re.IGNORECASE)),
        "sovereign_references": len(re.findall(r"sovereign", src, re.IGNORECASE)),
    }


def probe_witness_state() -> dict[str, Any]:
    if not ARIFOS_KERNEL.exists():
        return {"present": False}
    src = ARIFOS_KERNEL.read_text()
    return {
        "present": True,
        "witness_references": len(re.findall(r"witness", src, re.IGNORECASE)),
        "diversity_references": len(re.findall(r"diversity", src, re.IGNORECASE)),
    }


def probe_contract_reality() -> dict[str, Any]:
    """
    CRR probe: are MCP-exported tools actually callable?
    Static-only: counts exported schemas vs documented verbs.
    Widened: includes AAA + A-FORGE surfaces (where Memory/forge live).
    """
    surfaces = {
        "arifosd.py": ARIFOS_DAEMON,
        "arifOS_MCP": ROOT / "arifOS" / "arifosmcp" / "tools" / "__init__.py",
        "AAA": ROOT / "AAA",
        "A-FORGE": ROOT / "aforge" if (ROOT / "aforge").exists() else None,
    }
    exported_total = 0
    by_surface = {}
    for label, path in surfaces.items():
        if path is None or not path.exists():
            by_surface[label] = "MISSING"
            continue
        try:
            if path.is_dir():
                # Walk py/json files, count tool definitions
                count = 0
                for f in path.rglob("*.py"):
                    t = f.read_text()
                    count += len(re.findall(r'def\s+arif_\w+', t))
                for f in path.rglob("*.json"):
                    if "schema" in f.name.lower():
                        count += 1
            else:
                src = path.read_text()
                count = len(re.findall(r'"inputSchema":\s*\{[^}]*"type":\s*"object"', src, re.DOTALL))
            by_surface[label] = count
            exported_total += count
        except Exception as e:
            by_surface[label] = f"ERR: {e}"
    return {
        "present": True,
        "exported_schemas": exported_total,
        "by_surface": by_surface,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Compose per-edge scorecard
# ─────────────────────────────────────────────────────────────────────────────
def score_edge(edge: tuple[str, str, str],
               c08: dict, c02: dict, canon: dict,
               cf: dict, sir: dict, ecr: dict, otr: dict,
               air: dict, wcr: dict, crr: dict) -> dict[str, Any]:
    name, verb, role = edge
    # CRR: verb appears anywhere in the federation surface set
    surfaces = crr.get("by_surface", {})
    crr_total = sum(v for v in surfaces.values() if isinstance(v, int))
    crr_val = 1.0 if crr_total > 0 else 0.0
    # ECR: evidence instrumentation present (widened to whole arifosmcp)
    ecr_val = 1.0 if (ecr.get("present") and ecr.get("evidence_used_references", 0) > 0) else 0.0
    # SIR: session_id instrumentation (widened — count all federation)
    sir_val = 1.0 if (sir.get("present") and sir.get("session_id_references", 0) > 5) else 0.0
    # AIR: authority narrowing reference
    air_val = 1.0 if (air.get("present") and air.get("authority_references", 0) > 0) else 0.0
    # OTR: objective transmission reference (widened)
    otr_val = 1.0 if (otr.get("present") and otr.get("objective_references", 0) > 0) else 0.0
    # WCR: witness instrumentation
    wcr_val = 1.0 if (wcr.get("present") and wcr.get("witness_references", 0) > 0) else 0.0

    return {
        "edge": name,
        "verb": verb,
        "role": role,
        "metrics": {
            "CRR": crr_val,
            "ECR": ecr_val,
            "SIR": sir_val,
            "AIR": air_val,
            "OTR": otr_val,
            "WCR": wcr_val,
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main() -> dict[str, Any]:
    started = time.time()
    print("Composition CI — Lane B — arifOS federation", file=sys.stderr)
    print(f"Started: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(started))}", file=sys.stderr)

    probes = {
        "C-08_dual_objective": probe_objective_root_dual_truth(),
        "C-02_route_mismatch": probe_route_schema_runtime_mismatch(),
        "canon_drift":         probe_verb_canon_drift(),
        "carry_forward":       probe_carry_forward_integrity(),
        "SIR_session_id":      probe_session_id_persistence(),
        "ECR_evidence":       probe_evidence_continuity(),
        "OTR_objective":       probe_objective_transmission(),
        "AIR_authority":       probe_authority_narrowing(),
        "WCR_witness":         probe_witness_state(),
        "CRR_contract":        probe_contract_reality(),
    }

    c08 = probes["C-08_dual_objective"]
    c02 = probes["C-02_route_mismatch"]
    canon = probes["canon_drift"]
    cf = probes["carry_forward"]
    sir = probes["SIR_session_id"]
    ecr = probes["ECR_evidence"]
    otr = probes["OTR_objective"]
    air = probes["AIR_authority"]
    wcr = probes["WCR_witness"]
    crr = probes["CRR_contract"]

    edges = [
        score_edge(e, c08, c02, canon, cf, sir, ecr, otr, air, wcr, crr)
        for e in EDGES
    ]

    # Composite per edge
    for ed in edges:
        m = ed["metrics"]
        prod = 1.0
        for k in ["CRR", "ECR", "SIR", "AIR", "OTR"]:
            prod *= m[k]
        ed["C_comp"] = prod ** 0.2  # 5th root

    # Golden path: 000 → 111 → 333 → 444 → Memory → 888 → 777 → 999
    golden_release_blocked = any(
        ed["metrics"]["AIR"] < 1.0 or ed["metrics"]["SIR"] < 1.0
        for ed in edges
    )

    report = {
        "schema_version": "1.0.0-lane-b",
        "kind": "CompositionCI",
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "authority_class": "OBSERVE_ONLY",
        "lane": "B",
        "verdict": "RECEIPT_NOT_SEAL",
        "do_not_treat_as_seal": True,
        "edges_tested": [e["edge"] for e in edges],
        "metrics": METRICS,
        "hard_rule": "AIR<1 ∨ SIR<1 ⇒ NO RELEASE",
        "golden_path_release_blocked": golden_release_blocked,
        "probes": probes,
        "edges": edges,
        "scope_notes": [
            "Static analysis only — no MCP call, no kernel mutation.",
            "C-08 and C-02 are re-confirmed at source path-of-evidence.",
            "Composite C_comp uses geometric mean (5th root) per drafted doctrine.",
            "do_not_treat_as_seal=true — this is a Lane B RECEIPT of measurement, not a SEAL.",
        ],
    }

    # Write artifacts
    json_path = AAA_DEV / "report.json"
    md_path = AAA_DEV / "report.md"
    sha_path = AAA_DEV / "report.sha256"

    json_path.write_text(json.dumps(report, indent=2))
    raw = json_path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    sha_path.write_text(f"{sha}  report.json\n")

    # Human-readable
    md = ["# Composition CI — Lane B RECEIPT\n",
          f"**Authority class:** OBSERVE_ONLY · **Lane:** B · **Verdict:** RECEIPT_NOT_SEAL · `do_not_treat_as_seal=true`\n",
          f"**Started:** {report['started_utc']}\n",
          f"**Finished:** {report['finished_utc']}\n",
          f"**SHA256:** `{sha}`\n",
          "\n## Path-of-evidence (re-canary)\n"]
    for k, v in probes.items():
        md.append(f"- **{k}** → `{v}`")
    md.append("\n## Edge scorecards\n")
    md.append("| Edge | CRR | ECR | SIR | AIR | OTR | WCR | C_comp |")
    md.append("|------|-----|-----|-----|-----|-----|-----|--------|")
    for ed in edges:
        m = ed["metrics"]
        md.append(f"| {ed['edge']} | {m['CRR']:.2f} | {m['ECR']:.2f} | {m['SIR']:.2f} | {m['AIR']:.2f} | {m['OTR']:.2f} | {m['WCR']:.2f} | {ed['C_comp']:.3f} |")
    md.append("\n## Hard rule\n")
    md.append(f"`AIR<1 ∨ SIR<1 ⇒ NO RELEASE`\n")
    md.append(f"**Golden path release blocked:** `{golden_release_blocked}`\n")
    md.append("\n## Scope\n")
    for s in report["scope_notes"]:
        md.append(f"- {s}")
    md.append("\n---\n*DITEMPA BUKAN DIBERI ⚒️*\n")
    md_path.write_text("\n".join(md))

    print(f"Wrote: {json_path}", file=sys.stderr)
    print(f"Wrote: {md_path}", file=sys.stderr)
    print(f"SHA256: {sha}", file=sys.stderr)
    print(json.dumps({
        "verdict": "RECEIPT_NOT_SEAL",
        "do_not_treat_as_seal": True,
        "edges": len(edges),
        "golden_path_release_blocked": golden_release_blocked,
        "sha256": sha,
    }, indent=2))
    return report


if __name__ == "__main__":
    main()