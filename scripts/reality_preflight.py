#!/usr/bin/env python3
"""
TRI-REALITY PRE-FLIGHT GATE — the 5 Golden Questions as an executable constraint.

REFERENCE: APEX::TRI_REALITY_GOVERNANCE_ACTIVATION::2026-09-13   MODE: EXECUTION
DOCTRINE : /root/AAA/canon/APEX_REALITY_GRAPH_MEMORY_MIGRATION_v1.md §4
SPEC     : /root/AAA/canon/REALITY_CONSEQUENCE_OBJECTS_SPEC_v1.md (arifos.wro|hro|mro|cro.v1)
COMPANION: reality_object_gate.py (INV-1/2/3) · reality_substrate_classify.py (R0-R5 census)

THE DIRECTIVE'S CORE RULE, MADE MECHANICAL
------------------------------------------
"Before ANY reasoning, mutation, retrieval, planning, execution — answer:
   1. What is true?          (R0 World Reality)
   2. What matters?          (R1 Human Reality)
   3. What can act?          (R2 Machine Reality)
   4. What is allowed?       (R5 Governance)
   5. Who pays if wrong?     (R4 Consequence)
 If any answer is missing: Authority must contract."

This gate does exactly that. It does NOT use fuzzy NLP to "understand" the action —
it requires the caller to DECLARE which reality domains the action touches, then
verifies each declared domain is backed by a live, unexpired reality object.
An unbacked domain is an UNANSWERED question, and unanswered => authority contracts.

Deterministic. Fail-closed. No LLM in the path.

Exit: 0 = all declared questions answered -> PROCEED
      1 = >=1 unanswered -> authority CONTRACTS (fail-closed)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("FATAL: pyyaml required", file=sys.stderr)
    sys.exit(1)

OBJECTS_DIR = Path("/root/AAA/state/reality_objects")
FLOOR_MANIFEST_CANDIDATES = [
    Path("/root/AAA/constitution/FLOORS.yaml"),
    Path("/root/AAA/constitution/floors.yaml"),
    Path("/root/AAA/state/floors.json"),
    Path("/root/arifOS/arifosmcp/kernel/floors.py"),
]

QUESTIONS = {
    "R0": "What is true? (World Reality)",
    "R1": "What matters? (Human Reality)",
    "R2": "What can act? (Machine Reality)",
    "R5": "What is allowed? (Governance)",
    "R4": "Who pays if wrong? (Consequence)",
}
SEVERITY_HIGH = {"HIGH", "CATASTROPHIC"}
BEHAVIOUR_BY_SEVERITY = {"TRIVIAL": "SILENT_ABSORB", "LOW": "SILENT_ABSORB",
                         "MEDIUM": "DRAFT_ONLY", "HIGH": "HOLD_FOR_CONFIRMATION",
                         "CATASTROPHIC": "HARD_ABORT"}


def _expired(ts) -> bool:
    if not ts:
        return False
    try:
        s = str(ts).replace("Z", "+00:00")
        d = datetime.fromisoformat(s)
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d < datetime.now(timezone.utc)
    except Exception:  # noqa: BLE001
        return False


def load_objects() -> dict[str, list[dict]]:
    by_schema: dict[str, list[dict]] = {}
    if not OBJECTS_DIR.exists():
        return by_schema
    for f in sorted(OBJECTS_DIR.glob("*.y*ml")):
        try:
            data = yaml.safe_load(f.read_text())
        except Exception:  # noqa: BLE001
            continue
        if isinstance(data, dict) and data.get("schema"):
            data["_source"] = str(f)
            by_schema.setdefault(data["schema"], []).append(data)
    return by_schema


def answer_r0(objs: dict) -> tuple[str, list[str]]:
    ev = []
    for o in objs.get("arifos.wro.v1", []):
        if o.get("status") == "ACTIVE" and not _expired(o.get("review_by")):
            ev.append(f"{o['id']}: {o.get('observed_fact','')[:90]}... [{o['_source']}]")
    return ("SATISFIED" if ev else "UNANSWERED"), ev


def answer_r1(objs: dict) -> tuple[str, list[str]]:
    ev = []
    for o in objs.get("arifos.hro.v1", []):
        if o.get("admissibility") == "ACTIVE" and not _expired(o.get("expires_at")):
            ev.append(f"{o['id']} ({o.get('type')}, attention={o.get('attention_cost')}, "
                      f"consequence={o.get('consequence_class')}) [{o['_source']}]")
    return ("SATISFIED" if ev else "UNANSWERED"), ev


def answer_r2(objs: dict) -> tuple[str, list[str]]:
    ev = []
    for o in objs.get("arifos.mro.v1", []):
        if o.get("rollback_path") and o.get("state") not in ("STOPPED", "DEPRECATED"):
            ev.append(f"{o['id']} state={o.get('state')} rollback={o.get('rollback_path')[:60]} "
                      f"[{o['_source']}]")
    return ("SATISFIED" if ev else "UNANSWERED"), ev


def answer_r5(_objs: dict) -> tuple[str, list[str]]:
    for p in FLOOR_MANIFEST_CANDIDATES:
        if p.exists():
            return "SATISFIED", [f"governance source present: {p}"]
    return "UNANSWERED", ["no machine-readable floor manifest found at any candidate path: "
                          + ", ".join(str(p) for p in FLOOR_MANIFEST_CANDIDATES)]


def answer_r4(objs: dict, severity: str) -> tuple[str, list[str]]:
    ev = []
    for o in objs.get("arifos.cro.v1", []):
        if not _expired(o.get("active_until")):
            ev.append(f"{o['id']} owner={o.get('consequence_owner')} severity={o.get('severity')} "
                      f"[{o['_source']}]")
    if ev:
        return "SATISFIED", ev
    if severity.upper() in SEVERITY_HIGH:
        return "UNANSWERED", [f"severity={severity} implies a consequence owner, but no live "
                              f"CRO exists — create one before proceeding"]
    return "UNANSWERED", ["no CRO; caller asserts no consequence-bearing stakeholder"]


RESOLVERS = {"R0": lambda o, s: answer_r0(o), "R1": lambda o, s: answer_r1(o),
             "R2": lambda o, s: answer_r2(o), "R5": lambda o, s: answer_r5(o),
             "R4": lambda o, s: answer_r4(o, s)}


def main() -> int:
    ap = argparse.ArgumentParser(description="Tri-Reality 5 Golden Questions pre-flight gate")
    ap.add_argument("--action", required=True, help="the proposed action (for the record)")
    ap.add_argument("--requires", default="R0,R1,R2,R5,R4",
                    help="comma list of reality domains this action touches")
    ap.add_argument("--severity", default="LOW", choices=list(BEHAVIOUR_BY_SEVERITY))
    ap.add_argument("--attention", default="LOW", choices=["LOW", "MEDIUM", "HIGH", "EXHAUSTED"])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    declared = [d.strip().upper() for d in args.requires.split(",") if d.strip()]
    unknown = [d for d in declared if d not in QUESTIONS]
    if unknown:
        print(f"FATAL: unknown domain(s) {unknown}; valid = {list(QUESTIONS)}", file=sys.stderr)
        return 1

    objs = load_objects()
    answers: dict[str, dict] = {}
    unanswered: list[str] = []
    for d in declared:
        status, ev = RESOLVERS[d](objs, args.severity)
        answers[d] = {"question": QUESTIONS[d], "status": status, "evidence": ev}
        if status == "UNANSWERED":
            unanswered.append(d)

    # Only declared domains are required; undeclared domains are reported as NOT_ASSESSED.
    for d, q in QUESTIONS.items():
        if d not in declared:
            answers[d] = {"question": q, "status": "NOT_ASSESSED", "evidence":
                          ["domain not declared by caller — not required for this action"]}

    contraction = bool(unanswered) or args.severity.upper() in SEVERITY_HIGH
    behaviour = BEHAVIOUR_BY_SEVERITY[args.severity.upper()]
    if args.attention == "EXHAUSTED":
        behaviour = ("HOLD_FOR_CONFIRMATION" if args.severity.upper() in SEVERITY_HIGH
                     else "SILENT_ABSORB")

    if unanswered:
        verdict = "CONTRACT"
        authority = "ADVISORY_DRAFT_ONLY"
        reason = (f"{len(unanswered)} of {len(declared)} declared questions UNANSWERED "
                  f"({', '.join(unanswered)}) — authority must contract")
    elif args.severity.upper() in SEVERITY_HIGH:
        verdict = "CONTRACT"
        authority = "DRAFT_ONLY"
        reason = f"severity={args.severity} with owner=ARIF — authority contracts by INV-1"
    else:
        verdict = "PROCEED"
        authority = "AUTO"
        reason = "all declared questions answered; no high-consequence owner"

    out = {
        "reference": "APEX::TRI_REALITY_GOVERNANCE_ACTIVATION::2026-09-13",
        "action": args.action,
        "five_golden_questions": answers,
        "declared_domains": declared,
        "unanswered": unanswered,
        "severity": args.severity,
        "attention": args.attention,
        "verdict": verdict,
        "authority_ceiling": authority,
        "authority_contraction": contraction,
        "required_behaviour": behaviour,
        "reason": reason,
        "objects_loaded": {k: len(v) for k, v in objs.items()},
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "fail_closed": True,
    }

    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"PRE-FLIGHT :: {args.action}")
        print("=" * 72)
        for d in ("R0", "R1", "R2", "R5", "R4"):
            a = answers[d]
            mark = {"SATISFIED": "OK  ", "UNANSWERED": "MISS", "NOT_ASSESSED": "n/a "}[a["status"]]
            print(f"[{mark}] {d}  {a['question']}")
            for e in a["evidence"][:2]:
                print(f"         └ {e}")
            if not a["evidence"]:
                print("         └ (no evidence)")
        print("=" * 72)
        print(f"verdict           : {verdict}")
        print(f"authority_ceiling : {authority}")
        print(f"required_behaviour: {behaviour}")
        print(f"reason            : {reason}")
        print(f"objects loaded    : {out['objects_loaded']}")

    # FAIL-CLOSED EXIT CONTRACT.
    # Corrected 2026-09-13: an earlier revision returned 0 whenever all declared
    # questions were answered, so a CONTRACT verdict driven by severity (INV-1)
    # still exited 0 — a caller checking the exit code would have proceeded with
    # contracted authority. Exit must track the VERDICT, not just `unanswered`.
    return 0 if verdict == "PROCEED" else 1


if __name__ == "__main__":
    sys.exit(main())
