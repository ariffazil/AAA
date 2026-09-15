#!/usr/bin/env python3
"""atoms.py — capability atoms + capability graph. The unit of learning.

Doctrine (F13 2026-09-15, verdict PARTIAL-SEAL):
    Experience → Scar → Pattern → Capability → Policy → Judgment.
    Skill is the adapter, not the intelligence. Skill Accumulation Without
    Capability Compression = entropy disguised as learning.
    So the atom is a CAPABILITY atom, never a bare "new skill" record.

An atom is the smallest surviving unit of experience that changes future
behaviour. It is only real if it carries: evidence at the same layer as its
claim, a falsifier, and a measured survival history.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from typing import Any

STATE = "/root/AAA/rsi/state"
ATOMS = os.path.join(STATE, "atoms.jsonl")
GRAPH = os.path.join(STATE, "capability-graph.json")
PROPOSALS = os.path.join(STATE, "proposals.jsonl")
LEDGER = os.path.join(STATE, "loop-ledger.jsonl")
RECEIPTS = os.path.join(STATE, "receipts")
CURSOR = os.path.join(STATE, "cursor.json")

SCHEMA = "arifos.rsi.atom.v1"
GRAPH_SCHEMA = "arifos.rsi.capability_graph.v1"

# Capability layers, lowest → highest. Selection pressure rises with the layer.
LAYERS = ("skill", "capability", "policy", "judgment", "governance")

# Closed taxonomy of failure/learning patterns. Extend only by F13 edit.
PATTERN_TYPES = (
    "PATH_DRIFT",            # two names/paths for one thing; case, symlink, legacy dir
    "REGISTRY_MISMATCH",     # declared surface != live surface
    "DUPLICATE_SOT",         # two sources of truth for one fact
    "DEAD_POINTER",          # a cited artifact no longer resolves
    "QUEUE_BLOCKED",         # ingest/loop jammed, retrying the same unit forever
    "SILENT_FAIL",           # failure swallowed by a default/fallback
    "SELF_EVAL",             # producer grades its own output
    "PROXY_REALITY",         # secondary representation treated as primary ground truth
    "LAYER_MISMATCH",        # claim layer != evidence layer
    "HUMAN_BURDEN",          # work collapsed back onto the sovereign
    "RESOURCE_WASTE",        # paid/idle capability not used (F2: ignorance of inventory)
    "PERMISSION_DRIFT",      # config allow-list != intended authority
    "TRUNCATION_LOSS",       # silent head/tail cut mistaken for the whole
    "UNCLASSIFIED",
)

# Evidence classes. A claim may only be answered by its own class.
LAYER_OF_EVIDENCE = {
    "runtime": ("pid", "socket", "process", "curl", "lsof", "live_probe"),
    "visual": ("frame", "image", "vlm", "screenshot"),
    "operational": ("health", "canary", "probe", "endpoint"),
    "security": ("patch", "test_pass", "remediation"),
    "completion": ("receipt", "seal", "ledger_entry"),
    "authority": ("f13", "sovereign_signal", "bound_proxy"),
    "identity": ("auth", "delegation", "proof"),
    "artifact": ("file", "hash", "sha256", "git_commit"),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def ensure_state() -> None:
    os.makedirs(STATE, exist_ok=True)
    os.makedirs(RECEIPTS, exist_ok=True)
    for p in (ATOMS, PROPOSALS, LEDGER):
        if not os.path.exists(p):
            open(p, "a").close()


def atom_id(signature: str) -> str:
    return "ATOM-" + hashlib.sha256(signature.encode()).hexdigest()[:12]


def append_jsonl(path: str, obj: dict) -> None:
    ensure_state()
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


def read_jsonl(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out


def load_atoms() -> dict[str, dict]:
    """Latest state per atom_id (append-only store, folded on read)."""
    folded: dict[str, dict] = {}
    for row in read_jsonl(ATOMS):
        aid = row.get("atom_id")
        if aid:
            folded[aid] = {**folded.get(aid, {}), **row}
    return folded


def make_atom(
    *,
    signature: str,
    pattern_type: str,
    layer: str,
    claim: str,
    evidence: list[dict],
    falsifier: str,
    actor: str,
    session_ids: list[str],
    frequency: int = 1,
    impact: str = "unknown",
    target: str | None = None,
) -> dict:
    return {
        "schema": SCHEMA,
        "atom_id": atom_id(signature),
        "ts": now_iso(),
        "signature": signature,
        "pattern_type": pattern_type,
        "layer": layer,
        "claim": claim,
        "evidence": evidence,
        "evidence_layer": dominant_layer(evidence),
        "falsifier": falsifier,
        "frequency": frequency,
        "impact": impact,
        "actor": actor,
        "sessions": session_ids[:20],
        "target": target,
        "status": "candidate",       # candidate → verified | rejected
        "survived_verification": False,
        "promotion": None,
        "survival_events": [],
    }


def dominant_layer(evidence: list[dict]) -> str:
    """Claim layer must equal evidence layer — so evidence declares its own."""
    classes = [str(e.get("layer", "")).lower() for e in evidence if e.get("layer")]
    if not classes:
        return "unknown"
    for name in LAYER_OF_EVIDENCE:
        if name in classes:
            return name
    return classes[0]


def parse_frequency(text: str) -> int:
    """Frequency is a measured count, never an adjective."""
    m = re.search(r"\b(\d{1,5})\s*(?:x|times|kali|occurrences|hits)\b", text, re.I)
    return int(m.group(1)) if m else 1


# ── capability graph ─────────────────────────────────────────────────────────

def load_graph() -> dict:
    if os.path.exists(GRAPH):
        try:
            return json.load(open(GRAPH, encoding="utf-8"))
        except Exception:
            pass
    return {
        "schema": GRAPH_SCHEMA,
        "created": now_iso(),
        "updated": now_iso(),
        "doctrine": "Capability → Organ → Tool → Skill. Selection pressure lives "
                    "at the capability layer; skills are adapters.",
        "nodes": {},
        "edges": [],
    }


def save_graph(g: dict) -> None:
    ensure_state()
    g["updated"] = now_iso()
    tmp = GRAPH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(g, fh, indent=2, ensure_ascii=False)
    os.replace(tmp, GRAPH)


def upsert_capability(g: dict, atom: dict) -> tuple[str, bool]:
    """Attach an atom to the capability graph. Returns (capability_id, created)."""
    cap_id = atom.get("target") or f"capability.{atom['pattern_type'].lower()}"
    created = cap_id not in g["nodes"]
    node = g["nodes"].get(cap_id, {
        "id": cap_id,
        "title": cap_id.split(".")[-1].replace("_", " ").title(),
        "layer": atom["layer"],
        "created": now_iso(),
        "atoms": [],
        "exposures": 0,
        "survivals": 0,
        "contradictions_survived": 0,
        "contradictions_failed": 0,
        "fitness_score": None,
        "status": "PROVISIONAL",
    })
    if atom["atom_id"] not in node["atoms"]:
        node["atoms"].append(atom["atom_id"])
    # Measurement discipline: exposures/survivals count VERIFICATION EVENTS.
    # Raw recurrence lives in `occurrences` — mixing the two inflates the
    # denominator and makes every capability look like it is failing.
    node["occurrences"] = node.get("occurrences", 0) + max(1, atom.get("frequency", 1))
    node.setdefault("exposures", 0)
    g["nodes"][cap_id] = node
    if not any(e.get("from") == atom["atom_id"] and e.get("to") == cap_id for e in g["edges"]):
        g["edges"].append({
            "from": atom["atom_id"], "to": cap_id,
            "relation": "evidences", "ts": now_iso(),
        })
    return cap_id, created


def record_survival(g: dict, cap_id: str, survived: bool, evidence: str) -> None:
    node = g["nodes"].get(cap_id)
    if not node:
        return
    node["exposures"] = node.get("exposures", 0) + 1
    if survived:
        node["survivals"] = node.get("survivals", 0) + 1
        node["contradictions_survived"] = node.get("contradictions_survived", 0) + 1
    else:
        node["contradictions_failed"] = node.get("contradictions_failed", 0) + 1
    exp = max(1, node["exposures"])
    node["fitness_score"] = round(node["survivals"] / exp, 4)
    node["status"] = ("ACTIVE" if node["fitness_score"] >= 0.8
                      else "DEGRADED" if node["fitness_score"] >= 0.5 else "AT_RISK")
    node.setdefault("survival_events", []).append(
        {"ts": now_iso(), "survived": survived, "evidence": evidence[:240]}
    )
    node["survival_events"] = node["survival_events"][-50:]


def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    k = max(0, min(len(s) - 1, int(round(p * (len(s) - 1)))))
    return s[k]


def ranking_report(g: dict) -> dict:
    """Layer 4 (judgment) artefact — PROPOSE ONLY. Never auto-applied."""
    fits = {k: v.get("fitness_score") or 0.0 for k, v in g["nodes"].items()}
    if not fits:
        return {"n": 0, "median_fitness": 0.0, "ranking": []}
    med = percentile(list(fits.values()), 0.5)
    order = sorted(fits.items(), key=lambda kv: -kv[1])
    return {
        "n": len(fits),
        "median_fitness": med,
        "ranking": [{"capability": k, "fitness": v, "below_median": v < med}
                    for k, v in order],
        "note": "Proposal surface only. Changing the ranking function is F13 territory.",
    }
