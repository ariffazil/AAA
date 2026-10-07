#!/usr/bin/env python3
"""
gate.py — HUMAN_REALITY_REFLEX pre-response gate.

Implements the two non-optional runtime reflexes per the F13 directive 2026-10-06:

  Reflex 1: Name mentioned -> machine probe before narrative.
            If a named human is in the user prompt, the agent MUST
            probe canonical memory (people.yaml + /root/memory/people/<handle>/
            + claims + relationships) BEFORE generating descriptive
            claims about that human. Probe absent -> descriptive_person_claims
            blocked. General knowledge may still proceed, but clearly
            labelled.

  Reflex 2: Safety concern -> reduce claim strength, not information value.
            If the user prompt or the candidate answer touches a
            sensitive conclusion (hidden identity, secret motive,
            orientation, etc.), the agent MUST NOT collapse to
            "cannot know" and stop. It must transform the blocked
            conclusion to the strongest ADJACENT behavioral signal
            with explicit hypothesis weight delta. The Signal Ladder
            L0..L5 governs the strongest claim class allowed.

The gate is the runtime binding for the doctrine already present in:
  - /root/.hermes/skills/transit-only-mention-probe/SKILL.md
  - /root/.hermes/skills/person-intelligence/SKILL.md
  - /root/AAA/instructions/human-substrate.md
  - /root/AAA/instructions/source-type-promotion-gate.md
  - /root/.hermes/cache/scratch/PERSON-FILE-DESIGN-v1.3-AMENDMENTS.md

Stdlib + PyYAML only. Fail-closed. No network calls.

Usage as a module:
    from gate import gate_response, probe_human, signal_ladder_climb

    result = gate_response(
        user_prompt="What does Syed want from me?",
        candidate_answer="I think Syed secretly...",
    )
    # result.ok, result.adjusted_answer, result.probe_receipt, ...

Usage as a CLI:
    python3 gate.py check "What does Syed want from me?" "I think he..."
    python3 gate.py probe syed
    python3 gate.py signal "Syed initiated contact" --max L2
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Local module: humans.py
_HUMANS_PATH = Path(__file__).resolve().parent
sys.path.insert(0, str(_HUMANS_PATH))
try:
    import humans as humans_mod  # type: ignore
except Exception as e:  # pragma: no cover
    print(f"FATAL: cannot import humans: {e}", file=sys.stderr)
    sys.exit(2)


# ----------------------------------------------------------------------------
# Name detector
# ----------------------------------------------------------------------------
# Cache the list of known human handles from people.yaml at module load.
_KNOWN_HANDLES: Optional[List[str]] = None
_KNOWN_DISPLAY: Optional[List[str]] = None


def _load_known_humans() -> Tuple[List[str], List[str]]:
    """Return (handles, display_names) from people.yaml."""
    global _KNOWN_HANDLES, _KNOWN_DISPLAY
    if _KNOWN_HANDLES is not None and _KNOWN_DISPLAY is not None:
        return _KNOWN_HANDLES, _KNOWN_DISPLAY
    people = humans_mod.list_humans()
    handles = [p["handle"] for p in people if p.get("handle")]
    displays = [p.get("display_name", "") for p in people if p.get("display_name")]
    _KNOWN_HANDLES = handles
    _KNOWN_DISPLAY = displays
    return handles, displays


def detect_named_humans(prompt: str) -> List[Dict[str, str]]:
    """
    Detect named humans in the prompt. Return a list of
    {handle, display_name, matched_as} dicts.

    Resolution priority:
      1. Direct handle match (case-insensitive).
      2. Display name match (case-insensitive).
      3. Substring match (any known handle/display is a substring of prompt).
      4. Token overlap (any token in the prompt matches any token in a handle/display).

    Deduplicates. Returns at most 8 matches.
    """
    if not prompt:
        return []
    handles, displays = _load_known_humans()
    p_low = prompt.lower()
    p_tokens = set(re.findall(r"\w+", p_low))
    matches: List[Tuple[int, Dict[str, str]]] = []
    for h, d in zip(handles, displays):
        h_low = h.lower()
        d_low = d.lower()
        if h_low in p_low or d_low in p_low:
            matches.append((0, {"handle": h, "display_name": d, "matched_as": h_low if h_low in p_low else d_low}))
            continue
        h_tokens = set(re.findall(r"\w+", h_low))
        d_tokens = set(re.findall(r"\w+", d_low))
        if p_tokens & (h_tokens | d_tokens):
            tok = (p_tokens & (h_tokens | d_tokens)).pop()
            matches.append((1, {"handle": h, "display_name": d, "matched_as": f"token:{tok}"}))
    matches.sort()
    out: List[Dict[str, str]] = []
    seen = set()
    for _, m in matches:
        if m["handle"] not in seen:
            out.append(m)
            seen.add(m["handle"])
        if len(out) >= 8:
            break
    return out


# ----------------------------------------------------------------------------
# Probe
# ----------------------------------------------------------------------------
def probe_human(handle: str) -> Dict[str, Any]:
    """
    Probe canonical human memory for a handle. Returns a compact
    evidence capsule (per the user's spec):

      human_context:
        subject: P-004
        query_intent: <inferred>
        machine_probe:
          performed: true
          surfaces_checked: [...]
        evidence: {observed, reported, inferred}
        contradictions: [...]
        superseded: [...]
        unknowns: [...]
        privacy_excluded: {count}
        freshness: {newest, stale_claims}
    """
    lookup = humans_mod.lookup(handle, ttl_hours=24 * 365)  # 1 year TTL — show everything we have
    freshness = humans_mod.freshness_check(handle, ttl_hours=24 * 365)

    # Classify known facts into L0/L1/L4 buckets
    observed: List[Dict[str, Any]] = []
    reported: List[Dict[str, Any]] = []
    inferred: List[Dict[str, Any]] = []
    privacy_excluded = 0

    for fact in lookup.get("known", []):
        scope = fact.get("scope", "shared")
        if scope == "dm":
            privacy_excluded += 1
            continue
        sclass = fact.get("source_class", "")
        if sclass == "PRIMARY_CORPUS":
            observed.append({"field": fact["field"], "value": fact["value"], "source": fact.get("source", "")})
        elif sclass in ("ARIF_ATTESTED", "CROSS_REFERENCED"):
            reported.append({"field": fact["field"], "value": fact["value"], "source": fact.get("source", "")})
        else:
            inferred.append({"field": fact["field"], "value": fact["value"], "source": fact.get("source", "")})

    # Unknowns
    unknowns = [
        {"field": u.get("field", "?"), "reason": u.get("reason", ""), "state": u.get("state", "VOID")}
        for u in lookup.get("unknown", [])
    ]

    # Contradictions & superseded (not implemented at lookup level yet)
    contradictions: List[Any] = []
    superseded: List[Any] = []

    return {
        "subject": handle,
        "display_name": lookup.get("display_name"),
        "machine_probe": {
            "performed": True,
            "surfaces_checked": [
                "people.yaml (lanes heritage register)",
                "/root/memory/people/<handle>/person-card.md",
                "/root/memory/people/<handle>/MEMORY_MANIFEST.json",
                "scopes (shared vs dm)",
            ],
        },
        "evidence": {
            "observed": observed,
            "reported": reported,
            "inferred": inferred,
        },
        "contradictions": contradictions,
        "superseded": superseded,
        "unknowns": unknowns,
        "privacy_excluded": {"count": privacy_excluded},
        "freshness": {
            "last_seal": freshness.get("last_seal"),
            "age_hours": freshness.get("age_hours"),
            "stale": freshness.get("stale"),
        },
    }


# ----------------------------------------------------------------------------
# Sensitive target detection
# ----------------------------------------------------------------------------
SENSITIVE_TARGETS = {
    "orientation": [
        "secretly gay", "secretly straight", "secretly bi", "really gay", "really straight",
        "is he gay", "is he straight", "is he bi", "suka lelaki", "suka perempuan",
        "sebenarnya gay", "sebenarnya straight",
    ],
    "hidden_motive": [
        "what does he want from me", "what does she want from me", "what does X want from me",
        "secretly wants", "sebenarnya nak", "dia sebenarnya",
        "does he love me", "does she love me", "sayang aku tak", "love me or not",
    ],
    "interior_state": [
        "how does he feel", "how does she feel", "apa perasaan dia", "apa rasa dia",
        "in his heart", "in her heart", "dalam hati dia",
    ],
    "diagnosis": [
        "is he depressed", "is he anxious", "adhd", "bipolar", "depression",
    ],
    "exclusivity": [
        "only me", "only with me", "cuma aku", "cuma saya", "je aku",
    ],
}


def detect_sensitive_target(prompt: str) -> List[str]:
    """Return list of sensitive target classes hit by the prompt."""
    p_low = prompt.lower()
    hits: List[str] = []
    for cls, patterns in SENSITIVE_TARGETS.items():
        for pat in patterns:
            if pat.lower() in p_low:
                hits.append(cls)
                break
    return hits


# ----------------------------------------------------------------------------
# Signal Ladder
# ----------------------------------------------------------------------------
SIGNAL_LADDER = {
    "L0": "Direct artifact observation (verbatim, sourced)",
    "L1": "Repeated observable behavior pattern",
    "L2": "Relational signal — what pattern discriminates between hypotheses",
    "L3": "Plausible interpretation with competing alternatives",
    "L4": "Self-report — the person's own stated experience/identity",
    "L5": "Interior certainty — NEVER available (HOLD)",
}


def signal_ladder_climb(evidence_capsule: Dict[str, Any], max_level: str = "L3") -> Dict[str, Any]:
    """
    Given an evidence capsule, return the strongest claim class the agent
    may reach. Caps at max_level.

    Heuristic:
      - Any observed fact -> L0 available
      - 2+ observed/reported facts of same shape -> L1 available
      - 1+ observed AND 1+ reported of same shape -> L2 available
      - Inferred facts present + at least one alternative considered -> L3
      - Self-report direct quote present -> L4
      - L5 never available
    """
    obs = evidence_capsule.get("evidence", {}).get("observed", [])
    rep = evidence_capsule.get("evidence", {}).get("reported", [])
    inf = evidence_capsule.get("evidence", {}).get("inferred", [])

    available: List[str] = []
    if obs:
        available.append("L0")
    if len(obs) >= 2 or (len(obs) >= 1 and len(rep) >= 1):
        available.append("L1")
    if obs and rep and len(obs) + len(rep) >= 3:
        available.append("L2")
    if inf and (obs or rep):
        available.append("L3")
    # L4 requires explicit self-report in the evidence
    if any("self-report" in str(f.get("source", "")).lower() or "syed" in str(f.get("source", "")).lower() and "in-lane" in str(f.get("source", "")).lower() for f in rep):
        available.append("L4")
    # L5 never
    available = [a for a in available if a != "L5"]

    # Cap at max_level
    level_order = ["L0", "L1", "L2", "L3", "L4"]
    if max_level in level_order:
        cap_idx = level_order.index(max_level)
        available = [a for a in available if level_order.index(a) <= cap_idx]

    strongest = available[-1] if available else "VOID"
    return {
        "available_levels": available,
        "strongest_allowed": strongest,
        "ladder_descriptions": {k: SIGNAL_LADDER[k] for k in available},
        "max_level_applied": max_level,
    }


# ----------------------------------------------------------------------------
# Adjacent-signal transformer
# ----------------------------------------------------------------------------
ADJACENT_TRANSFORMS = {
    "orientation": (
        "Hidden identity inference is not available. "
        "Adjacent signals: observed same-sex intimate behaviors, the person's explicit self-positioning, "
        "self-reported partner status, repetition/initiation patterns, and competing alternative explanations. "
        "Unsupported: orientation label, secret motive."
    ),
    "hidden_motive": (
        "Hidden motive is not available. "
        "Adjacent signals: observed behavioral reciprocity (initiation/return), resource investment, "
        "routine formation, response latency, repair after silence, disclosed life information, "
        "and competing alternative explanations (practical need, convenience, companionship, scene archetype)."
    ),
    "interior_state": (
        "Interior state is not available. "
        "Adjacent signals: observed emotional regulation (co-regulation via touch/proximity/routine), "
        "behavioral reciprocation, response latency changes, conflict-repair patterns, disclosure depth, "
        "and competing alternative explanations."
    ),
    "diagnosis": (
        "Clinical diagnosis is not available. "
        "Adjacent signals: observed behavioral patterns (energy, sleep, routine stability, distress signals), "
        "self-reports of fatigue or pain, and the standing rule that any clinical-level reading requires "
        "direct clinical contact (not model inference)."
    ),
    "exclusivity": (
        "Exclusivity is not available from one data point. "
        "Adjacent signals: a single third-party offer rejection may indicate person-specific intimacy, "
        "stranger-anxiety, or disinterest in the specific third party. "
        "Repeated third-party offers with consistent response pattern would be required to upgrade. "
        "Unsupported: exclusivity claim from a single rejection."
    ),
}


def transform_to_adjacent(sensitive_classes: List[str], evidence_capsule: Dict[str, Any]) -> str:
    """Produce a Minimum Useful Signal substitute for blocked sensitive conclusions."""
    if not sensitive_classes:
        return ""
    out: List[str] = []
    for cls in sensitive_classes:
        if cls in ADJACENT_TRANSFORMS:
            out.append(ADJACENT_TRANSFORMS[cls])
    # Add evidence summary
    obs = evidence_capsule.get("evidence", {}).get("observed", [])
    rep = evidence_capsule.get("evidence", {}).get("reported", [])
    if obs or rep:
        n_obs = len(obs)
        n_rep = len(rep)
        out.append(
            f"\n\nWhat the machine has for {evidence_capsule.get('subject', '?')}: "
            f"{n_obs} observed facts, {n_rep} reported facts (scope:shared). "
            f"Freshness: {evidence_capsule.get('freshness', {}).get('age_hours', '?')}h since last_seal "
            f"(stale={evidence_capsule.get('freshness', {}).get('stale', '?')})."
        )
    return "\n\n".join(out)


# ----------------------------------------------------------------------------
# Gate
# ----------------------------------------------------------------------------
def gate_response(
    user_prompt: str,
    candidate_answer: Optional[str] = None,
    max_signal_level: str = "L3",
) -> Dict[str, Any]:
    """
    Run the HUMAN_REALITY_REFLEX gate on a candidate response.
    Returns a GateResult dict with:
      ok: bool — whether the candidate passes the gate
      named_humans: list of detected named humans
      probe_receipts: list of evidence capsules (one per named human)
      sensitive_targets: list of sensitive classes hit
      signal_ladder: result of signal_ladder_climb per human
      adjusted_answer: str — either the candidate, the candidate with
                       a "machine evidence:" prefix, or the adjacent
                       signal transform if sensitive
      blocked_reasons: list of why a block occurred (if any)
      instruction: str — instruction for the agent
    """
    named = detect_named_humans(user_prompt)
    sensitive = detect_sensitive_target(user_prompt + " " + (candidate_answer or ""))

    # Probe each named human
    capsules: List[Dict[str, Any]] = []
    ladders: Dict[str, Dict[str, Any]] = {}
    for n in named:
        cap = probe_human(n["handle"])
        cap["query_intent"] = _infer_intent(user_prompt)
        capsules.append(cap)
        ladders[n["handle"]] = signal_ladder_climb(cap, max_level=max_signal_level)

    ok = True
    blocked_reasons: List[str] = []
    instruction_parts: List[str] = []

    # Reflex 1: name mentioned -> machine probe before narrative.
    # We always probe; the gate is "probed, then allowed to answer".
    # The OK/NOT-OK is about the *candidate_answer* not skipping the probe.
    if named:
        instruction_parts.append(
            f"HUMAN_REALITY_REFLEX triggered for {len(named)} named human(s). "
            f"Probe performed against canonical substrate. "
            f"Strongest signal class per human: " +
            ", ".join(f"{h['handle']}={ladders[h['handle']]['strongest_allowed']}" for h in named) +
            "."
        )

    # Reflex 2: safety concern -> reduce claim strength, not information value.
    # If sensitive targets detected AND candidate_answer claims L5 (interior certainty) or
    # makes unsupported personal claims, transform.
    adjusted = candidate_answer or ""
    if sensitive and candidate_answer:
        # Check if the candidate makes unsupported personal claims
        unsupported_markers = ["definitely", "certainly", "obviously", "secretly", "i know that", "pasti", "memang"]
        is_unsupported = any(m in candidate_answer.lower() for m in unsupported_markers)
        if is_unsupported:
            ok = False
            blocked_reasons.append(
                f"Candidate answer makes unsupported personal claim about sensitive class {sensitive}. "
                f"Transform to adjacent signal."
            )
            for cap in capsules:
                adjusted = adjusted + "\n\n" + transform_to_adjacent(sensitive, cap)
        else:
            # Soften: append the adjacent signal as supporting context
            for cap in capsules:
                adjusted = adjusted + "\n\n" + transform_to_adjacent(sensitive, cap)

    if not named and not sensitive:
        # No named human, no sensitive target. Pass through.
        instruction_parts.append("No named human, no sensitive target. Reflexes did not trigger.")

    instruction = "\n".join(instruction_parts) if instruction_parts else "Reflexes did not trigger. Pass through."

    return {
        "ok": ok,
        "named_humans": named,
        "probe_receipts": capsules,
        "sensitive_targets": sensitive,
        "signal_ladders": ladders,
        "adjusted_answer": adjusted,
        "blocked_reasons": blocked_reasons,
        "instruction": instruction,
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
    }


def _infer_intent(prompt: str) -> str:
    """Heuristic intent inference for query_bounded retrieval."""
    p = prompt.lower()
    if any(w in p for w in ["tonight", "today", "coming", "free", "malam ni", "hari ni", "datang"]):
        return "temporal_logistics"
    if any(w in p for w in ["pattern", "us", "between", "relationship", "antara", "hubungan"]):
        return "relationship_dynamics"
    if any(w in p for w in ["supplement", "stack", "peptide", "dosis", "supplement"]):
        return "body_fitness_lane"
    if any(w in p for w in ["feel", "want", "love", "sayang", "nak", "suka"]):
        return "affective_state"
    return "general"


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------
def _emit(obj: Any) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False, default=str))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="HUMAN_REALITY_REFLEX gate. Pre-response binding for human-name handling."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check")
    p_check.add_argument("prompt")
    p_check.add_argument("candidate")
    p_check.add_argument("--max-level", default="L3", choices=["L0", "L1", "L2", "L3", "L4"])

    p_probe = sub.add_parser("probe")
    p_probe.add_argument("handle")

    p_signal = sub.add_parser("signal")
    p_signal.add_argument("handle")
    p_signal.add_argument("--max-level", default="L3", choices=["L0", "L1", "L2", "L3", "L4"])

    p_detect = sub.add_parser("detect")
    p_detect.add_argument("prompt")

    args = parser.parse_args()

    if args.cmd == "check":
        result = gate_response(args.prompt, args.candidate, max_signal_level=args.max_level)
        _emit(result)
        return 0 if result["ok"] else 1
    elif args.cmd == "probe":
        _emit(probe_human(args.handle))
        return 0
    elif args.cmd == "signal":
        cap = probe_human(args.handle)
        _emit(signal_ladder_climb(cap, max_level=args.max_level))
        return 0
    elif args.cmd == "detect":
        _emit({
            "named_humans": detect_named_humans(args.prompt),
            "sensitive_targets": detect_sensitive_target(args.prompt),
        })
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
