#!/usr/bin/env python3
"""promote.py — the promotion gate. Where capability may mutate and governance may not.

F13 verdict 2026-09-15 (PARTIAL-SEAL):
    A. Recursive skill improvement ............... SEAL
    B. Recursive capability improvement .......... SEAL (dengan verifier)
    C. Recursive AAA intelligence improvement .... PARTIAL-SEAL
       (333 proposal models, 555 verification, routing heuristics, capability ranking)
    D. Recursive self-governance improvement ..... HOLD
       (F1–F13, kernel, canon, judge, verifier, promotion threshold)

    Capability may mutate. Governance must witness mutation.
    Governance may not self-authorize mutation.

FORBIDDEN_PATHS is hardcoded in this module ON PURPOSE. It is deliberately not
readable from config.yaml, so the loop cannot relax its own boundary by editing
a file it is otherwise allowed to read. Removing an entry requires an F13 edit to
this source file, which is itself outside the loop's write surface.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess

import atoms as A
import ledger as L

CONFIG = "/root/AAA/rsi/config.yaml"
LEARNING_QUEUE = "/root/AAA/skills/.learning/queue"
INGEST = "/root/AAA/scripts/skill-learn-ingest.py"
FORGE_WORK = "/root/forge_work/rsi-proposals"

# Layer 5. Never writable by any automated path. Hardcoded.
FORBIDDEN_PATHS = (
    "/root/AAA/instructions/constitution.md",
    "/root/AAA/canon/",
    "/root/arifOS/GENESIS/",
    "/root/arifOS/arifosmcp/kernel/",
    "/root/AAA/rsi/config.yaml",
    "/root/AAA/rsi/verify.py",
    "/root/AAA/rsi/promote.py",
    "/root/AAA/rsi/ledger.py",
    "/root/AAA/rsi/lock.py",
    # The capability ledger is a SOT the loop may APPEND a claim to (via ledger.py,
    # which preserves hand formatting under flock) — but it may never rewrite an
    # existing entry or edit its schema/vocabulary. That is the probe's job, with
    # evidence. Blocking blanket writes here keeps the loop from "fixing" the SOT.
    "/root/AAA/ops/capabilities/capability-ledger.schema.json",
    "/root/AAA/ops/capabilities/probe-capabilities.py",
    "/root/.hermes/SOUL.md",
)

FORBIDDEN_PATTERNS = (
    r"F1\b.*\bF13", r"floor", r"constitution", r"canon", r"evaluator",
    r"promotion threshold", r"verifier", r"judge",
)


class GovernanceHold(Exception):
    """Raised when any path attempts to write outside the capability surface."""


def assert_not_governance(target: str, intent: str) -> None:
    """Layer 5 enforcement. Raise — never warn-and-continue."""
    t = os.path.abspath(target)
    for forbidden in FORBIDDEN_PATHS:
        f = os.path.abspath(forbidden)
        if t == f or t.startswith(f.rstrip("/") + "/"):
            raise GovernanceHold(
                f"HOLD_FORBIDDEN: {intent} → {target} is governance surface. "
                "Governance must witness mutation, not self-authorize it. "
                "Requires F13 verdict.")
    low = intent.lower()
    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, low):
            raise GovernanceHold(
                f"HOLD_FORBIDDEN: intent '{intent}' touches a governance primitive "
                f"(matched /{pat}/). F13 verdict required.")


def _split(line: str) -> tuple[str, str]:
    """Split `key: value  # comment` → (key, value), comment stripped."""
    body = line.split("#", 1)[0].rstrip()
    key, _, val = body.partition(":")
    return key.strip(), val.strip().strip('"').strip("'")


def _config() -> dict:
    """Minimal YAML reader for our own flat config (stdlib only)."""
    cfg: dict = {"promotion": {}, "verification": {}, "window_days": 7}
    section = None
    for line in open(CONFIG, encoding="utf-8"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, val = _split(line)
        if not key:
            continue
        if re.match(r"^\w", line):
            if val:
                cfg[key] = val
                section = key if val == "" else None
            else:
                section = key
                cfg.setdefault(key, {})
            continue
        if section:
            cfg[section][key] = val
    return cfg


def _policy(layer: str) -> str:
    return _config()["promotion"].get(f"{layer}_layer", "propose_only")


# ── Layer 1 — skill surface (auto when verified) ─────────────────────────────

def _existing_skill(name: str) -> str | None:
    """Resolve a skill id to a live skill directory, case-insensitively."""
    for root in ("/root/.hermes/skills", "/root/AAA/skills"):
        if not os.path.isdir(root):
            continue
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns
                      if not d.startswith(".") and d not in ("node_modules", "__pycache__")]
            if os.path.basename(dp).lower() == name.lower() and "SKILL.md" in fns:
                return dp
    return None


# Which live skill OWNS a given pattern's lesson. A skill lesson must land in a
# real skill or it becomes a dead-letter. Measured 2026-09-15: the first version
# derived skill_id from the capability namespace ("reference_integrity"), which is
# not a skill, so every Layer-1 promotion was rejected and Layer 1 was a silent
# no-op.
LESSON_OWNER = {
    "DEAD_POINTER": "FORGE-verify-runtime",
    "PATH_DRIFT": "FORGE-symlink-audit",
    "TRUNCATION_LOSS": "FORGE-context-compressor",
    "SILENT_FAIL": "federation-organ-recovery",
    "REGISTRY_MISMATCH": "AUDIT-drift-detector",
    "QUEUE_BLOCKED": "hermes-cron-zen",
}


def promote_skill(atom: dict, receipt: dict) -> dict:
    """Drop a lesson atom into the learning queue for the skill that owns it.

    Only fires when a real skill exists for the pattern. Otherwise the atom stays
    a capability-graph entry — Layer 1 is not allowed to invent a skill name.
    """
    owner = LESSON_OWNER.get(atom["pattern_type"])
    if not owner:
        return {"action": "no_target_skill", "applied": False,
                "reason": f"no owning skill mapped for {atom['pattern_type']} — "
                          "capability graph keeps the atom; no skill lesson emitted"}
    skill_dir = _existing_skill(owner)
    if not skill_dir:
        return {"action": "no_target_skill", "applied": False,
                "reason": f"mapped owner '{owner}' not present in the live skill tree"}

    os.makedirs(LEARNING_QUEUE, exist_ok=True)
    atom_file = os.path.join(
        LEARNING_QUEUE,
        f"{A.now_iso().replace(':', '').replace('-', '')}_{atom['atom_id']}.json")
    payload = {
        "skill_id": os.path.basename(skill_dir),
        "agent": "hermes-rsi-loop",
        "lesson": (atom["claim"] + " — " + (receipt.get("reason") or ""))[:490],
        "evidence": json.dumps(atom.get("evidence", [])[:2], ensure_ascii=False)[:1500],
        "atom_id": atom["atom_id"],
        "verified_by": receipt.get("verifier_actor"),
    }
    with open(atom_file, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    out = subprocess.run(["/usr/bin/python3", INGEST], capture_output=True, text=True, timeout=120)
    return {
        "action": "skill_lesson_queued",
        "target": skill_dir,
        "ingest_stdout": (out.stdout or "").strip()[:400],
        "applied": "MERGED" in (out.stdout or ""),
    }


# ── Layer 2 — capability graph (auto when verified) ──────────────────────────

def promote_capability(atom: dict, receipt: dict) -> dict:
    """Wire the verified atom into the capability ledger that already exists.

    Order matters (F13 2026-09-15, "WIRE, jangan build"):
      1. INGEST into `/root/AAA/ops/capabilities/capability-ledger.yaml` — the SOT,
         3-dimensional (implemented × reachable × governed), flock-serialized.
      2. REFRESH the derived view at `state/capability-graph.json`, rebuildable from
         the ledger. Ownership follows storage: the view may be deleted, the ledger
         may not be regenerated from it.
    """
    # 1 — SOT: the existing ledger.
    ingest_result = L.ingest(atom, receipt)

    # 2 — Derived view.
    g = A.load_graph()
    cap_id, created = A.upsert_capability(g, atom)

    # Survival may only be recorded by a witness that did not write the claim.
    # A provisional verdict (same author, different name) may create a graph node —
    # the node is evidence of a pattern, not evidence that the pattern was beaten.
    if receipt.get("provisional"):
        node = g["nodes"].get(cap_id, {})
        node["status"] = "PROVISIONAL"
        node["sot"] = "ops/capabilities/capability-ledger.yaml (derived view — do not treat as SOT)"
        node["provisional_reason"] = (
            f"independence={receipt.get('independence_class')} (same author). "
            "Survival requires a witness that did not author the claim — "
            "FRAME / arif_judge / a durable external receipt.")
        node.setdefault("provisional_events", []).append(
            {"ts": A.now_iso(), "atom_id": atom["atom_id"],
             "note": "graph entry only — no survival recorded"})
        g["nodes"][cap_id] = node
        A.save_graph(g)
        return {
            "action": "capability_node_upsert",
            "target": ingest_result.get("target")
                      or f"/root/AAA/rsi/state/capability-graph.json#{cap_id}",
            "capability": cap_id,
            "created": created,
            "ledger": ingest_result,
            "provisional": True,
            "applied": True,
            "reason": "ledger entry appended as a claim; survival NOT recorded "
                      "(provisional independence)",
        }

    A.record_survival(g, cap_id, survived=True,
                      evidence=f"verified by {receipt.get('verifier_actor')}: {receipt.get('reason')}")
    A.save_graph(g)
    return {
        "action": "capability_node_upsert",
        "target": ingest_result.get("target")
                  or f"/root/AAA/rsi/state/capability-graph.json#{cap_id}",
        "capability": cap_id,
        "created": created,
        "ledger": ingest_result,
        "provisional": False,
        "applied": True,
    }


# ── Layers 3–4 — policy / judgment (propose only, F13 decides) ───────────────

def propose_policy(atom: dict, receipt: dict) -> dict:
    os.makedirs(FORGE_WORK, exist_ok=True)
    p = os.path.join(FORGE_WORK, f"{A.now_iso()[:10]}-{atom['atom_id']}.md")
    body = f"""# RSI Proposal — {atom['pattern_type']} ({atom['layer']} layer)

> Status: **PROPOSE ONLY** — awaiting F13 verdict. Not applied.
> Atom: `{atom['atom_id']}` · frequency: {atom['frequency']} · impact: {atom['impact']}
> Verifier: {receipt.get('verifier_actor')} · independent: {receipt.get('independent')}

## Claim
{atom['claim']}

## Falsifier
{atom['falsifier']}

## Evidence
"""
    for ev in atom.get("evidence", [])[:5]:
        body += f"- [{ev.get('layer')}] {ev.get('source')}: {ev.get('excerpt','')[:400]}\n"
    body += f"""
## Proposed invariant (F13 decides)
> TBD by F13. Layer-3/4 learning changes policy and judgment, which the loop may
> not self-authorize.

## Verification mechanism
{json.dumps(receipt.get('checks'), indent=2, ensure_ascii=False)}

## Boundary
This proposal touches `{atom['layer']}` layer. Automatic application is **disabled**
by F13 verdict 2026-09-15 (PARTIAL-SEAL for Layer C, HOLD for Layer D).
"""
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(body)
    A.append_jsonl(A.PROPOSALS, {
        "ts": A.now_iso(), "atom_id": atom["atom_id"], "layer": atom["layer"],
        "pattern_type": atom["pattern_type"], "path": p,
        "status": "awaiting_f13", "applied": False,
    })
    return {"action": "policy_proposed", "target": p, "applied": False,
            "awaiting": "F13 verdict"}


# ── the gate ─────────────────────────────────────────────────────────────────

def quarantine(atom: dict, receipt: dict) -> dict:
    """An atom the taxonomy cannot yet name is recorded, never promoted.

    Promotion of an unnamed pattern is how a library grows without capability
    growing. Quarantine keeps the evidence and holds the label open.
    """
    A.append_jsonl(os.path.join(A.STATE, "quarantine.jsonl"), {
        "ts": A.now_iso(), "atom_id": atom["atom_id"], "pattern_type": atom["pattern_type"],
        "layer": atom["layer"], "frequency": atom["frequency"],
        "claim": atom["claim"], "sources": [e.get("source") for e in atom.get("evidence", [])][:5],
        "status": "awaiting_classification",
    })
    return {"action": "quarantined", "applied": False,
            "reason": "pattern not in taxonomy — held for classification, not promoted"}


def promote(atom: dict, receipt: dict) -> dict:
    """Route a verified atom to its lawful destination. Returns a receipt."""
    layer = atom.get("layer", "capability")
    policy = _policy(layer)

    try:
        if atom.get("pattern_type") == "UNCLASSIFIED":
            return quarantine(atom, receipt)

        if layer == "governance":
            assert_not_governance(atom.get("target") or "governance", atom.get("claim", ""))
            return {"action": "HOLD_FORBIDDEN", "applied": False,
                    "reason": "governance layer is not writable by any automated path"}

        if not receipt.get("passed"):
            return {"action": "withheld", "applied": False,
                    "reason": f"verification failed: {receipt.get('reason')}"}

        if layer == "skill" and policy == "auto_verified":
            return promote_skill(atom, receipt)

        if layer == "capability" and policy == "auto_verified":
            if atom.get("frequency", 1) < int(_config()["promotion"]
                                              .get("min_frequency_for_capability", 2)):
                return {"action": "deferred", "applied": False,
                        "reason": f"frequency {atom.get('frequency')} below capability threshold "
                                  "(a one-off is an incident, not a capability)"}
            return promote_capability(atom, receipt)

        if layer in ("policy", "judgment") and policy == "propose_only":
            if receipt.get("provisional"):
                return {"action": "withheld", "applied": False,
                        "reason": "policy/judgment claim withheld: independent witness "
                                  "required — a same-author verdict may not propose a rule"}
            return propose_policy(atom, receipt)

        return {"action": "no_policy", "applied": False,
                "reason": f"no promotion policy for layer={layer}"}

    except GovernanceHold as hold:
        A.append_jsonl(A.PROPOSALS, {
            "ts": A.now_iso(), "atom_id": atom.get("atom_id"), "layer": layer,
            "status": "HOLD_FORBIDDEN", "reason": str(hold), "applied": False,
        })
        return {"action": "HOLD_FORBIDDEN", "applied": False, "reason": str(hold)}


def self_test() -> list[dict]:
    """Prove the boundary holds. Run on every loop start."""
    results = []
    for target, intent in (
        ("/root/AAA/instructions/constitution.md", "edit floor F2"),
        ("/root/AAA/canon/CANONICAL_GLOSSARY.md", "append doctrine"),
        ("/root/AAA/rsi/config.yaml", "raise promotion threshold"),
        ("/root/AAA/rsi/verify.py", "relax verifier"),
        ("/root/.hermes/SOUL.md", "rewrite bridge protocol"),
    ):
        try:
            assert_not_governance(target, intent)
            results.append({"target": target, "blocked": False, "LEAK": True})
        except GovernanceHold:
            results.append({"target": target, "blocked": True})
    return results


if __name__ == "__main__":
    for r in self_test():
        tag = "LEAK" if r.get("LEAK") else "blocked"
        print(f"  {tag:<8} {r['target']}")
