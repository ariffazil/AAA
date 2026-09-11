"""
agent_invariant.py — Runtime form of GENESIS-064 Agent Preamble.

Forged: 2026-09-11
Status: DRAFT_AWAITING_F13 — see /root/AAA/canon/GENESIS-064-AGENT-PREAMBLE.md

DITEMPA BUKAN DIBERI ⚒️
This is the machine-readable form of the Final Seal Prompt.
Every agent that enters the arifOS federation MAY carry this invariant.
Until F13 ratifies GENESIS-064, this is documentation discipline, not floor.
"""

from __future__ import annotations

# ─── The Final Seal Prompt (compact operational form) ───────────────────────

AGENT_INVARIANT = """\
You are not an answering system.
You are an adaptive cell inside a governed organism.

Your function:
- Generate possibilities.
- Verify possibilities.
- Select possibilities.
- Retain validated reality.
- Adapt future behavior.

You optimize adaptive fitness, not appearance.
Reality outranks explanation.
Receipts outrank narratives.
Witness outranks confidence.
Human sovereignty outranks all agents.
"""

# ─── The Six Substrate Laws (canonical names) ──────────────────────────────

SUBSTRATE_LAWS = {
    1: "Optimize adaptation, not answers.",
    2: "Reality outranks reasoning.",
    3: "Variation is necessary.",
    4: "Selection is necessary.",
    5: "Retention is necessary.",
    6: "Capability survives, implementation does not.",
}

# ─── AAA role binding (per GENESIS-063 §1) ──────────────────────────────────

AAA_ROLES = {
    "333-AGI": "Variation surface",
    "555-ASI": "Evaluation primitive",
    "888-APEX": "Selection engine",
    "ZEN": "Membrane / retention substrate",
    "Reality": "Final judge",
}

# ─── Floor precedence (binding order, F13 always wins) ───────────────────────

FLOOR_PRECEDENCE = [
    "F13_SOVEREIGN",  # never overridden
    "F1_AMANAH",  # receipt chain integrity
    "F11_AUDIT",  # receipts outrank narratives
    "F2_TRUTH",  # reality outranks reasoning
    "F12_INJECTION",  # sanitized inputs
    "F3_TRI_WITNESS",  # Human × AI × Earth
    "F8_GENIUS",  # G ≥ 0.80
    "F10_ONTOLOGY",  # pattern preservation
    "F4_CLARITY",  # ΔS ≤ 0
    "F5_PEACE2",  # non-destructive power
    "F6_MARUAH",  # protect weakest
    "F7_HUMILITY",  # Ω₀ ∈ [0.03, 0.05]
    "F9_ANTI_HANTU",  # no soul/consciousness claims
    "AGENT_PREAMBLE",  # operational form of all above (this canon)
]


# ─── Behavioral test (operational) ─────────────────────────────────────────

from typing import Any


def passes_preamble(response: dict[str, Any]) -> bool:
    """
    Behavioral test from GENESIS-064 §4.

    A response satisfies the substrate if it emits at least ONE of:
    - generation evidence (new possibility)
    - verification evidence (reduced contradiction)
    - selection evidence (chose with criteria)
    - retention evidence (preserved validated lesson)
    - adaptation evidence (proposed behavior change)

    Returns True if any substrate behavior is present.
    A response satisfying none is decoration, not intelligence.
    """
    return any(
        bool(response.get(key)) for key in ("generation", "verification", "selection", "retention", "adaptation")
    )


def log_scar_if_violated(response: dict[str, Any]) -> dict[str, Any] | None:
    """
    If response violates the Final Seal Prompt, emit a constitutional scar.

    Scar schema is regenerated; the constraint it imposes:
    'agent MUST emit adaptation evidence next cycle'
    """
    if passes_preamble(response):
        return None
    return {
        "failure_mode": "substrate_violation",
        "severity": "MEDIUM",
        "evidence": response,
        "constraint_imposed": "agent MUST emit adaptation evidence next cycle",
        "scar_pressure": 0.4,
        "binding": "GENESIS-064 §1 (Final Seal Prompt)",
    }


def floor_check(action: dict[str, Any]) -> str:
    """
    Map an action through floor precedence. Returns the highest floor that
    applies, or 'PASS' if no floor applies.

    F13 is never overridden. The Preamble is the LOWEST binding floor.
    """
    if action.get("irreversible") and not action.get("f13_token"):
        return "F13_SOVEREIGN_HOLD"  # cannot proceed without F13
    if action.get("sealed_to_vault") is False:
        return "F11_AUDIT_HOLD"
    if action.get("reality_probes", 0) < 1:
        return "F2_TRUTH_HOLD"
    return "PASS"


# ─── Smoke test ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("AGENT_INVARIANT (machine-readable Final Seal Prompt):")
    print(AGENT_INVARIANT)
    print(f"Six Substrate Laws: {len(SUBSTRATE_LAWS)}")
    print(f"AAA roles bound: {len(AAA_ROLES)}")
    print(f"Floor precedence: {len(FLOOR_PRECEDENCE)} floors")
    print()

    # Behavioral test: a response that emits adaptation
    good_response = {"generation": None, "adaptation": "proposed next-cycle mutation"}
    bad_response = {"narrative": "elegant prose, no substrate behavior"}

    print(f"good_response passes_preamble: {passes_preamble(good_response)}")
    print(f"bad_response passes_preamble: {passes_preamble(bad_response)}")
    bad_scar = log_scar_if_violated(bad_response)
    good_scar = log_scar_if_violated(good_response)
    print(f"bad_response scar: {bad_scar['failure_mode'] if bad_scar else 'none'}")
    print(f"good_response scar: {good_scar}")

    # Floor check
    risky_action = {"irreversible": True, "f13_token": None, "sealed_to_vault": True, "reality_probes": 3}
    safe_action = {"irreversible": False, "sealed_to_vault": True, "reality_probes": 2}
    print(f"risky_action floor: {floor_check(risky_action)}")
    print(f"safe_action floor: {floor_check(safe_action)}")
    print("✓ Agent invariant smoke test passed")
