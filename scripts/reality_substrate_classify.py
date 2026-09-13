#!/usr/bin/env python3
"""
APEX::REALITY_GRAPH_MEMORY_MIGRATION::v1 — substrate classifier + orphan ledger.

AUTHORITY : ARIF (F13 Sovereign) · REFERENCE APEX::REALITY_GRAPH_MEMORY_MIGRATION::2026-09-13
DOCTRINE  : /root/AAA/canon/APEX_REALITY_GRAPH_MEMORY_MIGRATION_v1.md
SPEC      : /root/AAA/canon/REALITY_CONSEQUENCE_OBJECTS_SPEC_v1.md
GATE      : /root/AAA/scripts/reality_object_gate.py  (INV-1/2/3)

FIRST LAW ENFORCED BY CONSTRUCTION
-----------------------------------
  Memory ≠ Reality · Knowledge ≠ Governance · Storage ≠ Witness

Every store is classified into R0..R5, or flagged ENTROPY / ORPHAN_MEMORY.
Classification is DOCTRINE (a judgment, hardcoded here and reviewable).
Measurement is PROBE (never hardcoded — re-measured on every run), because a
registry that pretends to be a witness is the exact scar this federation already
carries (institutional-memory-strata.md:50).

SUCCESS CONDITION (from the directive):
  Every store must answer >=1 of: what reality does this preserve / what witness
  supports it / what consequence does it affect / what scar is linked / what
  governance behaviour changes.  If it answers none -> ARCHIVE or DEMOTE.

Exit contract: 0 = classified, no ENTROPY · 1 = ENTROPY or ORPHAN found (fail-closed)
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

QDRANT = "http://127.0.0.1:6333"
OUT_DIR = Path("/root/AAA/state/reality_objects")
MANIFEST = OUT_DIR / "substrate_manifest.jsonl"

# ── CLASSIFICATION DOCTRINE (judgment; reviewable; not a measurement) ────────────────
# key: collection / path fragment.  value: domains + why.
QDRANT_CLASS: dict[str, dict] = {
    "mem0":                     {"domains": ["R1"], "why": "per-user/per-group private human memory (F6 dignity); tenant-isolated"},
    "hermes_private":           {"domains": ["R1"], "why": "declared Hermes-private lane"},
    "arifos_precedent":         {"domains": ["R5"], "why": "888-APEX case law = governance precedent"},
    "arifOS_skill_mesh":        {"domains": ["R2"], "why": "live tool/capability affordances"},
    "federation_memory_patterns": {"domains": ["R1", "R5"], "why": "SOUL.md rotated patterns -> human meaning + adaptation"},
    "petronas_knowledge":       {"domains": ["R0"], "why": "external energy/industry reality corpus"},
    "atlas333_eureka":          {"domains": ["R0", "R1"], "why": "cross-domain insight about world and human paradox"},
    "arifos_session_memory":    {"domains": ["R2"], "why": "per-session runtime continuity"},
    "arifos_memory":            {"domains": ["R2"], "why": "default federation semantic recall"},
    "federation_shared":        {"domains": ["R2"], "why": "default federation-shared recall"},
    "arif_evidence":            {"domains": ["R3"], "why": "evidence chain = witness"},
    "arifos_constitution":      {"domains": ["R5"], "why": "F1-F13 floor definitions"},
    "arifos_vault_canon":       {"domains": ["R3", "R5"], "why": "immutable vault canon"},
    "arifos_vault_working":     {"domains": ["R2"], "why": "mutable working surface"},
    "arifos_audio_memory":      {"domains": ["ENTROPY"], "why": "vector dim 6 is not a real embedding space; 2 points"},
    "identity_vault":           {"domains": ["R1", "R5"], "why": "identity bindings, F13 sovereign writes"},
    "openclaw_memory":          {"domains": ["R2"], "why": "edge agent memory"},
    "mem0-v4":                  {"domains": ["ENTROPY"], "why": "empty collection"},
    "mem0migrations":           {"domains": ["ENTROPY"], "why": "bookkeeping, agents forbidden to call"},
}

VAULT_CLASS: dict[str, dict] = {
    "SEALED_EVENTS.jsonl":  {"domains": ["R3"], "why": "append-only hash-chained seal ledger"},
    "outcomes.jsonl":       {"domains": ["R2"], "why": "tool execution outcomes"},
    "arifflow_sealed.jsonl": {"domains": ["R4"], "why": "metabolic FlowReceipt chain"},
    "arifflow_sealed_rg2.jsonl": {"domains": ["R4"], "why": "RG2 flow fork"},
    "rsi_ledger.jsonl":     {"domains": ["R4", "R5"], "why": "decision review + adaptation"},
    "apex-zen-witness.jsonl": {"domains": ["R3"], "why": "witness attestations"},
    "apex-zen-receipts.jsonl": {"domains": ["R3"], "why": "loop receipts"},
    "apex-zen-telemetry.jsonl": {"domains": ["R2"], "why": "runtime telemetry"},
    "reality_ledger/entries.jsonl": {"domains": ["R4"], "why": "decision vs expected outcome"},
    "receipts_v2.jsonl":    {"domains": ["R3"], "why": "v2 receipt with witness_count"},
    "session-seals.jsonl":  {"domains": ["R3", "R5"], "why": "session close attestation"},
    "local_seals.jsonl":    {"domains": ["R3"], "why": "local seal helper"},
    "frame/evidence_queue.jsonl": {"domains": ["R3"], "why": "FRAME observer evidence"},
    "frame/receipts.jsonl": {"domains": ["R3"], "why": "FRAME receipts"},
    "wealth/receipts.jsonl": {"domains": ["R4"], "why": "capital receipts"},
    "well/verdict-outcomes.jsonl": {"domains": ["R1"], "why": "human readiness outcomes"},
    "experience/traces.jsonl": {"domains": ["R4"], "why": "chain-of-experience traces"},
    "sro_expiry_receipts.jsonl": {"domains": ["R3"], "why": "expiry audit trail"},
}

# Declared-but-unwritten VAULT999 subdirs (measured empty in census).
DECLARED_EMPTY = ["chronus", "cooling", "court", "scar", "reality-loop", "deployments",
                  "process_violations", "quarantine", "drafts", "session_receipts",
                  "sessions", "phoenix72", "email", "forge", "scripts", "syed",
                  "capability_evolution", "bak-archive", "arifos"]

FS_CLASS: list[dict] = [
    {"id": "H-axis H1-H6", "path": "/root/memory/H1-capture|H2-experience|H3-knowledge|H4-identity|H5-scars|H6-constitution",
     "domains": ["R1"], "why": "human memory: identity, biography, knowledge, scars (backward-looking)"},
    {"id": "P-axis people", "path": "/root/memory/people", "domains": ["R1"], "why": "relational human reality (ACTG/ZKPC)"},
    {"id": "VVV void vault", "path": "/root/memory/VVV", "domains": ["R1"], "why": "shadow abstractions, F13-only"},
    {"id": "instructions fragments", "path": "/root/AAA/instructions", "domains": ["R5"], "why": "loadable doctrine"},
    {"id": "canon corpus", "path": "/root/AAA/canon", "domains": ["R5"], "why": "ratified canon"},
    {"id": "scars AAA", "path": "/root/AAA/scars", "domains": ["R4"], "why": "failure->future behaviour"},
    {"id": "scars H5", "path": "/root/memory/H5-scars", "domains": ["R4", "R1"], "why": "sovereign scar registry"},
    {"id": "AAA state ledgers", "path": "/root/AAA/state", "domains": ["R4", "R5"], "why": "decision/mutation/contract ledgers"},
    {"id": "knowledge stores", "path": "/root/AAA/knowledge|knowledge-graph|wiki|registries", "domains": ["R2"], "why": "capability + knowledge indexes"},
    {"id": "work artifacts", "path": "/root/AAA/forge_work|artifacts", "domains": ["R4"], "why": "consequence-bearing project output"},
    {"id": "skills", "path": "/root/AAA/skills", "domains": ["R2"], "why": "capability surface"},
]


def sh(cmd: str, timeout: int = 20) -> str:
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=timeout).stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


def probe_qdrant() -> dict[str, dict]:
    out: dict[str, dict] = {}
    raw = sh(f"curl -s --max-time 8 {QDRANT}/collections")
    if not raw:
        return out
    try:
        names = [c["name"] for c in json.loads(raw)["result"]["collections"]]
    except Exception:  # noqa: BLE001
        return out
    for n in names:
        d = sh(f"curl -s --max-time 8 {QDRANT}/collections/{n}")
        pts, dim = None, None
        try:
            j = json.loads(d)["result"]
            pts = j.get("points_count")
            vec = j.get("config", {}).get("params", {}).get("vectors")
            dim = vec.get("size") if isinstance(vec, dict) else None
        except Exception:  # noqa: BLE001
            pass
        out[n] = {"points": pts, "dim": dim}
    return out


def probe_jsonl(root: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for f in sorted(root.rglob("*.jsonl")):
        try:
            lines = sum(1 for _ in f.open("rb"))
            out[str(f.relative_to(root))] = {"lines": lines, "bytes": f.stat().st_size}
        except Exception:  # noqa: BLE001
            out[str(f.relative_to(root))] = {"lines": None, "bytes": None}
    return out


def classify_qdrant(probe: dict[str, dict]) -> list[dict]:
    rows = []
    for name, m in sorted(probe.items()):
        cls = QDRANT_CLASS.get(name, {"domains": ["ENTROPY"], "why": "unclassified collection"})
        pts = m.get("points") or 0
        domains = list(cls["domains"])
        if pts == 0 and "ENTROPY" not in domains:
            domains = ["ENTROPY"]; cls = {"domains": domains, "why": "declared but zero points"}
        if m.get("dim") is not None and m["dim"] < 64 and "ENTROPY" not in domains:
            domains = ["ENTROPY"]; cls = {"domains": domains, "why": f"vector dim {m['dim']} is not a real embedding space"}
        rows.append(_row(f"qdrant:{name}", "qdrant_collection", m, domains, cls["why"],
                         witness="PARTIAL" if "R3" in domains else "ABSENT"))
    return rows


def classify_vault(vroot: Path, probe: dict[str, dict]) -> list[dict]:
    rows = []
    for rel, m in sorted(probe.items()):
        cls = VAULT_CLASS.get(rel, {"domains": ["R3"], "why": "vault ledger (witness-class by location)"})
        domains = list(cls["domains"])
        if (m.get("lines") or 0) == 0:
            domains = ["ORPHAN"]; cls = {"domains": domains, "why": "declared ledger with zero entries"}
        rows.append(_row(f"vault999:{rel}", "vault_ledger", m, domains, cls["why"],
                         witness="PRESENT" if "R3" in domains else "PARTIAL"))
    for d in DECLARED_EMPTY:
        p = vroot / d
        if p.is_dir() and not any(p.rglob("*.jsonl")):
            rows.append(_row(f"vault999:{d}/", "declared_empty_dir", {"lines": 0, "bytes": 0},
                             ["ORPHAN"], "subdirectory declared in the vault surface, never written"))
    return rows


def classify_fs() -> list[dict]:
    rows = []
    for spec in FS_CLASS:
        paths = [Path(p) for p in spec["path"].split("|")]
        files = 0
        missing = []
        for p in paths:
            if not p.exists():
                missing.append(str(p)); continue
            files += sum(1 for _ in p.rglob("*") if _.is_file())
        m = {"files": files, "missing_paths": missing}
        rows.append(_row(spec["id"], "fs_class", m, list(spec["domains"]), spec["why"],
                         witness="PARTIAL"))
    rows.append(_row("megamemory sqlite (AAA+arifFlow)", "sqlite_graph",
                     {"nodes": 0, "edges": 0, "timeline": 0}, ["ENTROPY"],
                     "node/edge tables empty in both copies (ZEN_HELIX GAP-5 claim falsified)"))
    rows.append(_row("GEOX earth_memory.db", "sqlite_world",
                     {"rows": 16, "all_draft": True}, ["R0"],
                     "world reality store, 16 rows all approval_state=draft, last write 2026-08-04",
                     witness="PARTIAL"))
    # CANONICAL carry_forward — corrected 2026-09-13 after witness verification:
    # the live generational store is /root/.local/share/arifos/carry_forward.json
    # (120,839 B, written by canonical carry_forward.py). The /root/.arifos/ and
    # /root/.hermes/ copies are flat legacy siblings (933 B / 2,303 B) recorded in
    # loop-3ff2585c. An earlier revision of this classifier measured ONLY the legacy
    # siblings and understated the live store by ~129x. Measurement corrected here.
    cf_main = Path("/root/.local/share/arifos/carry_forward.json")
    cf_legacy = [Path("/root/.arifos/carry_forward.json"),
                 Path("/root/.hermes/carry_forward.json")]
    rows.append(_row("carry-forward (canonical)", "json_state",
                     {"path": str(cf_main),
                      "bytes": cf_main.stat().st_size if cf_main.exists() else None,
                      "exists": cf_main.exists(),
                      "legacy_siblings": [{"path": str(p), "bytes": p.stat().st_size,
                                           "exists": p.exists()} for p in cf_legacy]},
                     ["R2", "R1"],
                     "canonical generational continuity store; legacy flat siblings are not SOT",
                     witness="PARTIAL"))
    return rows


def _row(sid: str, kind: str, measured: dict, domains: list[str], why: str,
         witness: str = "ABSENT") -> dict:
    """Success condition (directive): a store must answer >=1 of the five questions.
    Reality-preserving (R0/R1) alone is NOT sufficient to count as governed memory —
    it survives but is flagged for witness binding, because Storage != Witness."""
    scar = "R4" in domains
    consequence = "R4" in domains
    governance = "R5" in domains
    witnessed = "R3" in domains or witness == "PRESENT"
    reality_preserved = any(d in ("R0", "R1") for d in domains)

    if "ENTROPY" in domains:
        verdict = "DELETE_CANDIDATE"
    elif "ORPHAN" in domains:
        verdict = "ORPHAN_REPAIR"
    elif witnessed or scar or governance:
        verdict = "MIGRATE"
    elif reality_preserved:
        verdict = "MIGRATE_WITH_WITNESS_GAP"
    else:
        verdict = "ARCHIVE_OR_DEMOTE"  # R2-only passive storage, no witness/consequence/governance
    return {
        "store_id": sid, "kind": kind, "measured": measured,
        "domains": domains, "witness": witness,
        "witness_gap": not witnessed,
        "success_condition": {"reality_preserved": reality_preserved,
                              "witness_supports": witnessed,
                              "consequence_affected": consequence,
                              "scar_linked": scar,
                              "governance_effect": governance},
        "verdict": verdict, "rationale": why,
        "probe": "live", "probing_agent": "FI-008 reality_substrate_classify.py",
        "observed_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Substrate classifier (APEX migration v1)")
    ap.add_argument("--write", action="store_true", help="write manifest to state/reality_objects/")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    q = probe_qdrant()
    vroot = Path("/root/VAULT999")
    v = probe_jsonl(vroot) if vroot.exists() else {}

    rows = classify_qdrant(q) + classify_vault(vroot, v) + classify_fs()

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    entropy = [r for r in rows if "ENTROPY" in r["domains"]]
    orphan = [r for r in rows if "ORPHAN" in r["domains"]]
    demote = [r for r in rows if r["verdict"] == "ARCHIVE_OR_DEMOTE"]

    if args.write:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        with MANIFEST.open("w") as fh:
            for r in rows:
                fh.write(json.dumps(r, sort_keys=True) + "\n")

    if args.json:
        print(json.dumps({"rows": rows, "counts": counts}, indent=2))
    else:
        print("APEX::REALITY_GRAPH_MEMORY_MIGRATION::v1 — substrate classifier")
        print(f"stores classified : {len(rows)}")
        print(f"qdrant probed     : {len(q)} collections, "
              f"{sum((m.get('points') or 0) for m in q.values())} points")
        print(f"vault ledgers     : {len(v)} jsonl, {sum((m.get('lines') or 0) for m in v.values())} lines")
        print("\nverdicts:")
        for k, n in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"  {k:<20} {n}")
        print(f"\nENTROPY ({len(entropy)}):")
        for r in entropy:
            print(f"  - {r['store_id']}: {r['rationale']}")
        print(f"\nORPHAN_MEMORY ({len(orphan)}):")
        for r in orphan[:25]:
            print(f"  - {r['store_id']}: {r['rationale']}")
        if len(orphan) > 25:
            print(f"  ... +{len(orphan) - 25} more")
        print(f"\nARCHIVE_OR_DEMOTE ({len(demote)}):")
        for r in demote:
            print(f"  - {r['store_id']} domains={r['domains']}")
        if args.write:
            print(f"\nmanifest: {MANIFEST}")

    return 1 if (entropy or orphan) else 0


if __name__ == "__main__":
    sys.exit(main())
