"""
acd_memory.py — ACD memory contract enforcement (acd.memory.v1)
Constitution Articles 10-13: ACD is a consumer and producer of governed
memory — never the memory authority. SIMULATED never becomes OBSERVED.
Pure stdlib. No execution capability. Fail closed.
"""

from __future__ import annotations

ZONES = {
    "evidence_context": {
        "realm": "AAA.CANON-ADJACENT",
        "default_ontology": ("OBSERVED", "INFERRED"),
        "acd_write": "none",
        "description": "Retrieved observations, prior sealed receipts, validated constraints.",
    },
    "possibility_quarantine": {
        "realm": "AAA.POSSIBILITY",
        "default_ontology": ("SIMULATED",),
        "acd_write": "request-only",
        "description": "Dream seeds, branch graphs, counterfactuals, stress cases.",
    },
    "ratified_learning": {
        "realm": "AAA.CANON",
        "default_ontology": ("OBSERVED",),
        "acd_write": "never-direct",
        "description": "Outcome-tested lesson from a witnessed consequence. arifOS governs; ACD petitions.",
    },
}

FORBIDDEN_TRANSITIONS = (
    ("SIMULATED", "OBSERVED"),
    ("SIMULATED", "CANON"),
    ("SIMULATED", "RATIFIED"),
    ("SIMULATED", "AAA.CANON"),
)

DEFAULT_RECALL_ONTOLOGY = ("OBSERVED", "INFERRED", "NORMATIVE")
SCENARIO_SCOPES = ("scenario", "explicit_acd_or_scenario_scope", "acd", "dream")


class ForbiddenTransition(PermissionError):
    """Raised when a transition violates Articles 10-13. Fails closed."""


def assert_transition_allowed(from_ontology: str, to_ontology: str) -> bool:
    """Raise ForbiddenTransition for any forbidden ontology transition."""
    pair = (str(from_ontology).upper(), str(to_ontology).upper())
    if pair in FORBIDDEN_TRANSITIONS:
        raise ForbiddenTransition(
            f"{pair[0]} -> {pair[1]} is forbidden (Article 12). "
            "SIMULATED material requires external witness, adjudication and human confirmation."
        )
    return True


def recall_filter(materials: list, scope: str | None = None) -> list:
    """Conservative default retrieval: SIMULATED material is excluded unless the
    calling context explicitly allows scenario scope. Ordinary factual recall
    must never return dream content."""
    allow_simulated = scope in SCENARIO_SCOPES
    out = []
    for item in materials:
        ontology = str(item.get("ontology", "UNKNOWN")).upper()
        if ontology == "SIMULATED" and not allow_simulated:
            continue
        out.append(item)
    return out


def attempt_self_promotion(*_args, **_kwargs):
    """ACD cannot self-promote. Fail closed. Article 9 / Article 13."""
    raise ForbiddenTransition(
        "ACD_SELF_PROMOTION_FORBIDDEN: promotion requires arif_judge verdict, "
        "AIO/governance review and human sovereignty. ACD may only petition."
    )
