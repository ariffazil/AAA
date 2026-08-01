#!/usr/bin/env python3
"""
canonical_prompts.py — The 7 canonical prompt families for WEALTH, GEOX, WELL.

Each prompt is a parameterized template that emits typed checklists,
short deliberation skeletons, or packet-ready intermediate objects.
Not essay generators. Not hidden system prompts. Transport objects.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

VERSION = "2026.06.28"


def _hash(name: str) -> str:
    return hashlib.sha256(name.encode()).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════════════════════
# WEALTH PROMPTS
# ═══════════════════════════════════════════════════════════════════════════
WEALTH_PROMPTS = {
    "wealth_reality_intake_loop": {
        "name": "wealth_reality_intake_loop",
        "version": VERSION,
        "prompt_sha256": _hash("wealth_reality_intake"),
        "description": "Separate observed inputs from assumptions, stale data, and missing evidence.",
        "parameters": {
            "query": {"type": "string", "required": True},
            "actor_context": {"type": "string", "default": "ARIF"},
            "known_facts": {"type": "string", "default": ""},
            "constraints": {"type": "string", "default": ""},
        },
        "template": (
            "Assess this capital query: {query}\n"
            "Actor context: {actor_context}\n\n"
            "Step 1 — FACTS: What is directly observed? (label OBS)\n"
            "Step 2 — ASSUMPTIONS: What is assumed but not verified? (label INT)\n"
            "Step 3 — MISSING: What data is absent? (label UNKNOWN)\n"
            "Step 4 — STALE: What data is past freshness TTL?\n"
            "Step 5 — CLASSIFY: Domain → allocation | valuation | risk | personal\n"
            "Step 6 — ROUTE: Minimum tools needed. No premature synthesis.\n"
            "Known facts: {known_facts}\nConstraints: {constraints}"
        ),
    },
    "wealth_capital_diagnosis_loop": {
        "name": "wealth_capital_diagnosis_loop",
        "version": VERSION,
        "prompt_sha256": _hash("wealth_capital_diagnosis"),
        "description": "Classify the capital task into the right internal mode.",
        "parameters": {
            "task": {"type": "string", "required": True},
            "domain": {"type": "string", "default": "allocation"},
        },
        "template": (
            "Diagnose this capital task: {task}\nDomain: {domain}\n\n"
            "Step 1 — CLASSIFY: What type of capital question is this?\n"
            "  - allocation (where to put capital)\n"
            "  - valuation (what is something worth)\n"
            "  - risk (what could go wrong)\n"
            "  - personal (cashflow, runway, net worth)\n"
            "  - institutional (governance, power, capture)\n"
            "Step 2 — SELECT: Which WEALTH tools are minimum necessary?\n"
            "Step 3 — DECLARE: What assumptions does the tool require?\n"
            "Step 4 — GATE: Does this need arifOS judgment?"
        ),
    },
    "wealth_risk_downside_loop": {
        "name": "wealth_risk_downside_loop",
        "version": VERSION,
        "prompt_sha256": _hash("wealth_risk_downside"),
        "description": "Force worst-case, unknowns, and confidence limits before synthesis.",
        "parameters": {
            "proposal": {"type": "string", "required": True},
            "timeframe": {"type": "string", "default": "12m"},
        },
        "template": (
            "Stress-test this proposal: {proposal}\nTimeframe: {timeframe}\n\n"
            "Step 1 — BASE CASE: What happens if assumptions hold?\n"
            "Step 2 — DOWNSIDE: What is the worst realistic outcome? (P10)\n"
            "Step 3 — TAIL RISK: What is the catastrophic but plausible outcome?\n"
            "Step 4 — UNKNOWNS: What variables have no reliable data?\n"
            "Step 5 — CONFIDENCE: Cap at 0.90. What reduces confidence?\n"
            "Step 6 — ASYMMETRY: Is upside or downside larger?"
        ),
    },
    "wealth_market_reality_loop": {
        "name": "wealth_market_reality_loop",
        "version": VERSION,
        "prompt_sha256": _hash("wealth_market_reality"),
        "description": "Load the external operating regime — FX, commodities, macro.",
        "parameters": {
            "focus": {"type": "string", "default": "malaysia"},
            "timeframe": {"type": "string", "default": "current"},
        },
        "template": (
            "Load market reality for: {focus}\nTimeframe: {timeframe}\n\n"
            "Step 1 — FX: MYR/USD, MYR/SGD, MYR/GBP current rates\n"
            "Step 2 — COMMODITIES: Brent crude, palm oil, LNG\n"
            "Step 3 — MACRO: BNM OPR, CPI, GDP growth\n"
            "Step 4 — REGIME: Risk-on or risk-off? Trend direction?\n"
            "Step 5 — FRESHNESS: How old is each data point?\n"
            "Step 6 — SOURCE: BNM, OpenDOSM, MEIH first. World Bank fallback only."
        ),
    },
    "wealth_allocation_judgment_loop": {
        "name": "wealth_allocation_judgment_loop",
        "version": VERSION,
        "prompt_sha256": _hash("wealth_allocation_judgment"),
        "description": "Express what classes of decisions are admissible now.",
        "parameters": {
            "proposal": {"type": "string", "required": True},
            "capital_type": {"type": "string", "default": "financial"},
        },
        "template": (
            "Judgment readiness for: {proposal}\nCapital type: {capital_type}\n\n"
            "Step 1 — DECISION CLASS: C0-C5 classification\n"
            "Step 2 — BLAST RADIUS: None / Local / Organ / Federation / Irreversible\n"
            "Step 3 — REVERSIBILITY: Can this be undone?\n"
            "Step 4 — WEALEST STAKEHOLDER: Who bears the most risk?\n"
            "Step 5 — DIGNITY IMPACT: Does this affect human dignity?\n"
            "Step 6 — VERDICT: PROCEED / HOLD / 888_HOLD / JUDGE_SEAL_REQUIRED"
        ),
    },
    "wealth_institutional_power_loop": {
        "name": "wealth_institutional_power_loop",
        "version": VERSION,
        "prompt_sha256": _hash("wealth_institutional_power"),
        "description": "Surface capture, conflicting evidence, and misalignment before handoff.",
        "parameters": {
            "scenario": {"type": "string", "required": True},
            "actors": {"type": "string", "default": ""},
        },
        "template": (
            "Power audit for: {scenario}\nActors: {actors}\n\n"
            "Step 1 — INCENTIVES: Who benefits from which outcome?\n"
            "Step 2 — CAPTURE RISK: Is any actor positioned to extract rent?\n"
            "Step 3 — OPACITY: What information is hidden or asymmetric?\n"
            "Step 4 — COERCION: Are there pressure signals?\n"
            "Step 5 — RULE ASYMMETRY: Do different actors face different rules?\n"
            "Step 6 — LEGITIMACY: Is this decision procedurally fair?"
        ),
    },
    "wealth_arifos_handoff_loop": {
        "name": "wealth_arifos_handoff_loop",
        "version": VERSION,
        "prompt_sha256": _hash("wealth_arifos_handoff"),
        "description": "Build the cross-organ packet for arifOS judgment.",
        "parameters": {
            "proposal": {"type": "string", "required": True},
            "verdict": {"type": "string", "required": True},
            "evidence_refs": {"type": "string", "default": ""},
        },
        "template": (
            "Prepare arifOS handoff for: {proposal}\nWEALTH verdict: {verdict}\n\n"
            "Packet fields:\n"
            "1. PROPOSAL: {proposal}\n"
            "2. VERDICT: {verdict}\n"
            "3. BLAST_RADIUS: [computed]\n"
            "4. REVERSIBILITY: [computed]\n"
            "5. DOWNSIDE_P10: [computed]\n"
            "6. WEALEST_STAKEHOLDER: [computed]\n"
            "7. EVIDENCE_REFS: {evidence_refs}\n"
            "8. RECEIPT_REF: [generated]\n"
            "9. CONFIDENCE: [capped at 0.90]\n"
            "10. AUTHORITY_REQUIRED: 888_HOLD | JUDGE_SEAL_AUTHORIZATION"
        ),
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# GEOX PROMPTS
# ═══════════════════════════════════════════════════════════════════════════
GEOX_PROMPTS = {
    "geox_reality_intake_loop": {
        "name": "geox_reality_intake_loop",
        "version": VERSION,
        "prompt_sha256": _hash("geox_reality_intake"),
        "description": "Separate observed geological inputs from assumptions and missing evidence.",
        "parameters": {
            "query": {"type": "string", "required": True},
            "basin": {"type": "string", "default": "unknown"},
            "scale": {"type": "string", "default": "prospect"},
        },
        "template": (
            "Assess this geological query: {query}\nBasin: {basin}\nScale: {scale}\n\n"
            "Step 1 — OBSERVED: What data is directly measured? (well logs, seismic, DST)\n"
            "Step 2 — DERIVED: What is computed from observations? (petrophysics, inversion)\n"
            "Step 3 — INTERPRETED: What requires geological judgment? (depositional model, structure)\n"
            "Step 4 — HYPOTHESIS: What is speculated? (untested concepts)\n"
            "Step 5 — MISSING: What data would change the interpretation?\n"
            "Step 6 — ROUTE: Minimum GEOX tools needed."
        ),
    },
    "geox_earth_diagnosis_loop": {
        "name": "geox_earth_diagnosis_loop",
        "version": VERSION,
        "prompt_sha256": _hash("geox_earth_diagnosis"),
        "description": "Classify the geological task into the right mode.",
        "parameters": {
            "task": {"type": "string", "required": True},
            "domain": {"type": "string", "default": "general"},
        },
        "template": (
            "Diagnose this earth science task: {task}\nDomain: {domain}\n\n"
            "Step 1 — CLASSIFY: basin | prospect | well | seismic | petrophysics | sequence\n"
            "Step 2 — SELECT: Which GEOX tools are minimum necessary?\n"
            "Step 3 — DECLARE: What assumptions does the tool require?\n"
            "Step 4 — GATE: Does this need arifOS judgment or WEALTH capital input?"
        ),
    },
    "geox_uncertainty_loop": {
        "name": "geox_uncertainty_loop",
        "version": VERSION,
        "prompt_sha256": _hash("geox_uncertainty"),
        "description": "Force worst-case, unknowns, and confidence limits before synthesis.",
        "parameters": {
            "interpretation": {"type": "string", "required": True},
            "evidence_quality": {"type": "string", "default": "unknown"},
        },
        "template": (
            "Stress-test this interpretation: {interpretation}\nEvidence quality: {evidence_quality}\n\n"
            "Step 1 — P10/P50/P90: What are the range estimates?\n"
            "Step 2 — WEAKEST LINK: Which data point has the lowest confidence?\n"
            "Step 3 — ALTERNATIVE: What is the competing interpretation?\n"
            "Step 4 — MISSING TEST: What single test would most reduce uncertainty?\n"
            "Step 5 — EVOI: Is the expected value of information worth the cost?\n"
            "Step 6 — CONFIDENCE: Cap at 0.90. Label: OBS/DER/INT/SPEC"
        ),
    },
    "geox_basin_regime_loop": {
        "name": "geox_basin_regime_loop",
        "version": VERSION,
        "prompt_sha256": _hash("geox_basin_regime"),
        "description": "Load the external geological operating regime.",
        "parameters": {
            "basin": {"type": "string", "required": True},
            "age_ma": {"type": "number", "default": 0},
        },
        "template": (
            "Load basin regime for: {basin}\nAge: {age_ma} Ma\n\n"
            "Step 1 — TECTONIC: What is the plate setting and structural style?\n"
            "Step 2 — STRATIGRAPHY: What is the depositional sequence?\n"
            "Step 3 — PETROLEUM SYSTEM: Source, reservoir, seal, trap, migration?\n"
            "Step 4 — ANALOG: What comparable basins exist?\n"
            "Step 5 — DATA COVERAGE: How well is this basin explored?\n"
            "Step 6 — DEEP TIME: What was the paleogeography at {age_ma} Ma?"
        ),
    },
    "geox_decision_support_loop": {
        "name": "geox_decision_support_loop",
        "version": VERSION,
        "prompt_sha256": _hash("geox_decision_support"),
        "description": "Express what classes of geological decisions are admissible now.",
        "parameters": {
            "prospect": {"type": "string", "required": True},
            "stage": {"type": "string", "default": "screen"},
        },
        "template": (
            "Decision support for: {prospect}\nStage: {stage}\n\n"
            "Step 1 — POS: What is the probability of success?\n"
            "Step 2 — VOLUMETRICS: What are the P10/P50/P90 resource estimates?\n"
            "Step 3 — EVOI: What is the value of additional data?\n"
            "Step 4 — RECOMMENDATION: Drill / Don't drill / More data needed\n"
            "Step 5 — HANDOFF: What does WEALTH need for capital evaluation?\n"
            "Step 6 — GATE: Does this need 888_HOLD?"
        ),
    },
    "geox_contradiction_challenge_loop": {
        "name": "geox_contradiction_challenge_loop",
        "version": VERSION,
        "prompt_sha256": _hash("geox_contradiction"),
        "description": "Surface conflicting evidence before handoff.",
        "parameters": {
            "claim": {"type": "string", "required": True},
            "evidence_refs": {"type": "string", "default": ""},
        },
        "template": (
            "Challenge this geological claim: {claim}\nEvidence: {evidence_refs}\n\n"
            "Step 1 — FOR: What evidence supports this claim?\n"
            "Step 2 — AGAINST: What evidence contradicts this claim?\n"
            "Step 3 — MISSING: What evidence is absent?\n"
            "Step 4 — CONFLICT: Are there direct contradictions?\n"
            "Step 5 — RESOLUTION: What test would resolve the conflict?\n"
            "Step 6 — VERDICT: SUPPORTED | CHALLENGED | INCONCLUSIVE"
        ),
    },
    "geox_arifos_handoff_loop": {
        "name": "geox_arifos_handoff_loop",
        "version": VERSION,
        "prompt_sha256": _hash("geox_arifos_handoff"),
        "description": "Build the cross-organ packet for arifOS judgment.",
        "parameters": {
            "interpretation": {"type": "string", "required": True},
            "verdict": {"type": "string", "required": True},
            "evidence_refs": {"type": "string", "default": ""},
        },
        "template": (
            "Prepare arifOS handoff for: {interpretation}\nGEOX verdict: {verdict}\n\n"
            "Packet fields:\n"
            "1. INTERPRETATION: {interpretation}\n"
            "2. VERDICT: {verdict}\n"
            "3. POS: [computed]\n"
            "4. VOLUMETRICS_P10/P50/P90: [computed]\n"
            "5. EVOI: [computed]\n"
            "6. EVIDENCE_REFS: {evidence_refs}\n"
            "7. TRANSLATION_CARD: dtc-geox-wealth-prospect-v1\n"
            "8. CONFIDENCE: [capped at 0.90]\n"
            "9. AUTHORITY_REQUIRED: 888_HOLD | JUDGE_SEAL_AUTHORIZATION"
        ),
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# WELL PROMPTS
# ═══════════════════════════════════════════════════════════════════════════
WELL_PROMPTS = {
    "well_reality_intake_loop": {
        "name": "well_reality_intake_loop",
        "version": VERSION,
        "prompt_sha256": _hash("well_reality_intake"),
        "description": "Separate observed human state from assumptions and missing telemetry.",
        "parameters": {
            "subject": {"type": "string", "default": "arif"},
            "context": {"type": "string", "default": ""},
        },
        "template": (
            "Assess human substrate for: {subject}\nContext: {context}\n\n"
            "Step 1 — OBSERVED: What telemetry is available? (sleep, HRV, activity)\n"
            "Step 2 — BEHAVIORAL: What is inferred from agent activity patterns?\n"
            "Step 3 — MISSING: What signals are absent or stale?\n"
            "Step 4 — PRIVACY: What signals require consent?\n"
            "Step 5 — DIGNITY: Is the human being reduced to metrics?\n"
            "Step 6 — ROUTE: Minimum WELL tools needed."
        ),
    },
    "well_readiness_diagnosis_loop": {
        "name": "well_readiness_diagnosis_loop",
        "version": VERSION,
        "prompt_sha256": _hash("well_readiness_diagnosis"),
        "description": "Classify the readiness question into the right mode.",
        "parameters": {
            "task": {"type": "string", "required": True},
            "subject": {"type": "string", "default": "arif"},
        },
        "template": (
            "Diagnose readiness for: {task}\nSubject: {subject}\n\n"
            "Step 1 — CLASSIFY: sleep | fatigue | cognitive | stress | recovery\n"
            "Step 2 — SELECT: Which WELL tools are minimum necessary?\n"
            "Step 3 — DECLARE: What assumptions does the tool require?\n"
            "Step 4 — GATE: Does this affect decision authority?"
        ),
    },
    "well_risk_bandwidth_loop": {
        "name": "well_risk_bandwidth_loop",
        "version": VERSION,
        "prompt_sha256": _hash("well_risk_bandwidth"),
        "description": "Force worst-case and confidence limits on human state.",
        "parameters": {
            "current_state": {"type": "string", "required": True},
            "proposed_task": {"type": "string", "default": ""},
        },
        "template": (
            "Risk bandwidth: {current_state}\nProposed task: {proposed_task}\n\n"
            "Step 1 — CURRENT BANDWIDTH: What is the decision capacity right now?\n"
            "Step 2 — FATIGUE: How much cognitive load has accumulated?\n"
            "Step 3 — DOWNSIDE: What happens if the human is wrong?\n"
            "Step 4 — RECOVERY: What would restore capacity?\n"
            "Step 5 — THRESHOLD: C1-C5 classification\n"
            "Step 6 — VERDICT: PROCEED | HOLD | DEFER | RECOVER"
        ),
    },
    "well_substrate_regime_loop": {
        "name": "well_substrate_regime_loop",
        "version": VERSION,
        "prompt_sha256": _hash("well_substrate_regime"),
        "description": "Load the external operating regime — biological, machine, interaction.",
        "parameters": {
            "subject": {"type": "string", "default": "arif"},
            "timeframe": {"type": "string", "default": "current"},
        },
        "template": (
            "Load substrate regime for: {subject}\nTimeframe: {timeframe}\n\n"
            "Step 1 — BIOLOGICAL: Sleep, nutrition, exercise, stress\n"
            "Step 2 — MACHINE: CPU, memory, disk, network, processes\n"
            "Step 3 — INTERACTION: Agent sessions, token throughput, git rhythm\n"
            "Step 4 — COUPLING: H × M × G interaction effects\n"
            "Step 5 — TREND: Improving, stable, or degrading?\n"
            "Step 6 — SOVEREIGN ENTROPY: psi_SE score (protect unpredictability)"
        ),
    },
    "well_decision_bandwidth_loop": {
        "name": "well_decision_bandwidth_loop",
        "version": VERSION,
        "prompt_sha256": _hash("well_decision_bandwidth"),
        "description": "Express what classes of decisions are admissible now.",
        "parameters": {
            "task": {"type": "string", "required": True},
            "decision_class": {"type": "string", "default": "C3"},
        },
        "template": (
            "Decision bandwidth for: {task}\nDecision class: {decision_class}\n\n"
            "Step 1 — CAPACITY: What is the current cognitive bandwidth?\n"
            "Step 2 — CLASS: C0=observe, C1=low, C2=moderate, C3=reversible-only, C4-C5=888_HOLD\n"
            "Step 3 — THRESHOLD: Does current state allow this class?\n"
            "Step 4 — FLOOR: W6 Metabolic Pause triggered?\n"
            "Step 5 — RECOMMENDATION: PROCEED | HOLD | DEFER | RECOVER\n"
            "Step 6 — HANDOFF: What does A-FORGE need for execution mode?"
        ),
    },
    "well_intent_alignment_loop": {
        "name": "well_intent_alignment_loop",
        "version": VERSION,
        "prompt_sha256": _hash("well_intent_alignment"),
        "description": "Surface misalignment and coercion signals before handoff.",
        "parameters": {
            "action": {"type": "string", "required": True},
            "subject": {"type": "string", "default": "arif"},
        },
        "template": (
            "Intent alignment for: {action}\nSubject: {subject}\n\n"
            "Step 1 — CONSENT: Does the human want this?\n"
            "Step 2 — COERCION: Are there pressure signals?\n"
            "Step 3 — DIGNITY: Is the human being respected?\n"
            "Step 4 — ASYMMETRY: Is information being hidden?\n"
            "Step 5 — AUTONOMY: Is the human's sovereignty preserved?\n"
            "Step 6 — VERDICT: ALIGNED | MISALIGNED | COERCIVE"
        ),
    },
    "well_arifos_handoff_loop": {
        "name": "well_arifos_handoff_loop",
        "version": VERSION,
        "prompt_sha256": _hash("well_arifos_handoff"),
        "description": "Build the cross-organ packet for arifOS judgment.",
        "parameters": {
            "readiness_verdict": {"type": "string", "required": True},
            "decision_class": {"type": "string", "required": True},
            "evidence_refs": {"type": "string", "default": ""},
        },
        "template": (
            "Prepare arifOS handoff\nWELL verdict: {readiness_verdict}\nDecision class: {decision_class}\n\n"
            "Packet fields:\n"
            "1. READINESS_VERDICT: {readiness_verdict}\n"
            "2. DECISION_CLASS: {decision_class}\n"
            "3. WELL_SCORE: [computed]\n"
            "4. FATIGUE_LEVEL: [computed]\n"
            "5. SOVEREIGN_ENTROPY: [computed]\n"
            "6. EVIDENCE_REFS: {evidence_refs}\n"
            "7. TRANSLATION_CARD: dtc-well-aforge-bandwidth-v1\n"
            "8. CONFIDENCE: [capped at 0.90]\n"
            "9. AUTHORITY_REQUIRED: NONE | 888_HOLD"
        ),
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# REGISTRY
# ═══════════════════════════════════════════════════════════════════════════
ALL_PROMPTS = {
    "wealth": WEALTH_PROMPTS,
    "geox": GEOX_PROMPTS,
    "well": WELL_PROMPTS,
}


def get_prompts(organ: str) -> dict:
    return ALL_PROMPTS.get(organ, {})


if __name__ == "__main__":
    for organ, prompts in ALL_PROMPTS.items():
        print(f"\n{organ.upper()} PROMPTS ({len(prompts)}):")
        for name, spec in prompts.items():
            print(f"  - {name}: {spec['description'][:60]}")
