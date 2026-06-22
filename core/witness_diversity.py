"""
Witness Diversity — F3 TRI-WITNESS enforcement at the session level.
====================================================================

Tracks how many distinct witness types are active in a session.
Enforces the Byzantine consensus requirement: Human+AI+Earth+Verifier ≥ 0.75.

The Opus-Kimi shadow transcript exposed the structural gap:
  - Two LLMs debating each other + one human amplifying = 2/5 witness types
  - No Earth measurement, no independent human = Mode-3 collapse
  - Each recursion layer feels more rigorous; it's the same substrate

Witness types:
  HUMAN               — the sovereign operator (Arif)
  AI_MODEL_A          — primary LLM
  AI_MODEL_B          — secondary/verifier LLM
  EARTH_MEASUREMENT   — live tool call result, sensor reading, database query
  INDEPENDENT_HUMAN   — non-sovereign human reader/reviewer

Scoring:
  5/5 = FULL_WITNESS   — all types active, F3 satisfied
  4/5 = STRONG         — one missing, acceptable
  3/5 = MINIMAL        — bare threshold, caution
  2/5 = DEGRADED       — AI-judging-AI, HOLD recommended
  1/5 = COLLAPSED      — single witness, VOID

Thresholds:
  ≥ 3 → F3 PASS
  = 2 → F3 CAUTION, auto-HOLD on irreversible actions
  ≤ 1 → F3 VOID

Integration:
  - AAA session state: session.witness_diversity
  - A-FORGE pre-flight: refuse MUTATE unless ≥ 3
  - arifOS kernel: F3 enforcement uses this score

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

# ── Constants ──────────────────────────────────────────────────────────────────

class WitnessType:
    HUMAN = "HUMAN"
    AI_MODEL_A = "AI_MODEL_A"
    AI_MODEL_B = "AI_MODEL_B"
    EARTH_MEASUREMENT = "EARTH_MEASUREMENT"
    INDEPENDENT_HUMAN = "INDEPENDENT_HUMAN"

ALL_WITNESS_TYPES = [
    WitnessType.HUMAN,
    WitnessType.AI_MODEL_A,
    WitnessType.AI_MODEL_B,
    WitnessType.EARTH_MEASUREMENT,
    WitnessType.INDEPENDENT_HUMAN,
]

class DiversityLevel:
    FULL_WITNESS = "FULL_WITNESS"     # 5/5
    STRONG = "STRONG"                  # 4/5
    MINIMAL = "MINIMAL"                # 3/5
    DEGRADED = "DEGRADED"              # 2/5
    COLLAPSED = "COLLAPSED"            # 1/5
    VOID = "VOID"                      # 0/5

class F3Verdict:
    PASS = "PASS"
    CAUTION = "CAUTION"
    HOLD = "HOLD"
    VOID = "VOID"

DIVERSITY_LEVEL_MAP = {
    5: DiversityLevel.FULL_WITNESS,
    4: DiversityLevel.STRONG,
    3: DiversityLevel.MINIMAL,
    2: DiversityLevel.DEGRADED,
    1: DiversityLevel.COLLAPSED,
    0: DiversityLevel.VOID,
}

F3_VERDICT_MAP = {
    5: F3Verdict.PASS,
    4: F3Verdict.PASS,
    3: F3Verdict.PASS,
    2: F3Verdict.CAUTION,
    1: F3Verdict.HOLD,
    0: F3Verdict.VOID,
}


# ── Session Witness State ─────────────────────────────────────────────────────

class SessionWitnessState:
    """
    Tracks witness diversity for a single AAA session.

    Each witness type has:
      - active: bool — is this witness present?
      - last_seen: ISO timestamp — when was it last active?
      - evidence_ref: str — what tool call / event proved it was active?
    """

    def __init__(self, session_id: str = ""):
        self.session_id = session_id
        self.witnesses: dict[str, dict] = {
            wt: {"active": False, "last_seen": "", "evidence_ref": ""}
            for wt in ALL_WITNESS_TYPES
        }
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = self.created_at
        self._event_log: list[dict] = []

    def register(
        self,
        witness_type: str,
        evidence_ref: str = "",
    ) -> None:
        """
        Register a witness as active.

        Args:
            witness_type: One of WitnessType.*
            evidence_ref: What proved this witness is active (tool call, event, etc.)
        """
        if witness_type not in self.witnesses:
            raise ValueError(f"Unknown witness type: {witness_type}")

        was_active = self.witnesses[witness_type]["active"]
        self.witnesses[witness_type] = {
            "active": True,
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "evidence_ref": evidence_ref,
        }
        self.updated_at = datetime.now(timezone.utc).isoformat()

        if not was_active:
            self._log_event("ACTIVATE", witness_type, evidence_ref)

    def register_earth_measurement(self, tool_name: str, evidence_ref: str = "") -> None:
        """Convenience: register an Earth measurement witness."""
        ref = evidence_ref or f"tool:{tool_name}"
        self.register(WitnessType.EARTH_MEASUREMENT, ref)

    def register_model_output(self, model_id: str, is_primary: bool = True) -> None:
        """Convenience: register a model output witness."""
        wt = WitnessType.AI_MODEL_A if is_primary else WitnessType.AI_MODEL_B
        self.register(wt, f"model:{model_id}")

    def register_human(self, evidence_ref: str = "session:sovereign") -> None:
        """Convenience: register the human sovereign."""
        self.register(WitnessType.HUMAN, evidence_ref)

    def deregister(self, witness_type: str) -> None:
        """Mark a witness as inactive (e.g., tool call timed out)."""
        if witness_type not in self.witnesses:
            raise ValueError(f"Unknown witness type: {witness_type}")

        was_active = self.witnesses[witness_type]["active"]
        self.witnesses[witness_type]["active"] = False
        self.updated_at = datetime.now(timezone.utc).isoformat()

        if was_active:
            self._log_event("DEACTIVATE", witness_type, "")

    def active_count(self) -> int:
        """How many witness types are currently active?"""
        return sum(1 for w in self.witnesses.values() if w["active"])

    def active_types(self) -> list[str]:
        """List of currently active witness type names."""
        return [wt for wt, data in self.witnesses.items() if data["active"]]

    def missing_types(self) -> list[str]:
        """List of missing witness type names."""
        return [wt for wt, data in self.witnesses.items() if not data["active"]]

    def diversity_level(self) -> str:
        """DiversityLevel string for current state."""
        return DIVERSITY_LEVEL_MAP.get(self.active_count(), DiversityLevel.VOID)

    def f3_verdict(self) -> str:
        """F3 constitutional verdict based on witness diversity."""
        return F3_VERDICT_MAP.get(self.active_count(), F3Verdict.VOID)

    def is_mode3_collapse(self) -> bool:
        """
        Detect Mode-3 collapse: AI-judging-AI with no Earth witness.
        This is exactly the pattern Opus exposed in the shadow transcript.
        """
        has_human = self.witnesses[WitnessType.HUMAN]["active"]
        has_model_a = self.witnesses[WitnessType.AI_MODEL_A]["active"]
        has_model_b = self.witnesses[WitnessType.AI_MODEL_B]["active"]
        has_earth = self.witnesses[WitnessType.EARTH_MEASUREMENT]["active"]

        # Mode-3: >= 2 AI models + human, but NO earth measurement
        model_count = sum([has_model_a, has_model_b])
        return model_count >= 2 and has_human and not has_earth

    def time_since_earth_measurement(self) -> Optional[float]:
        """Seconds since last Earth measurement. None if never measured."""
        earth = self.witnesses[WitnessType.EARTH_MEASUREMENT]
        if not earth["last_seen"]:
            return None
        last = datetime.fromisoformat(earth["last_seen"])
        return (datetime.now(timezone.utc) - last).total_seconds()

    def _log_event(self, event: str, witness_type: str, evidence: str) -> None:
        self._event_log.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "witness_type": witness_type,
            "evidence_ref": evidence,
        })

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "witnesses": self.witnesses,
            "active_count": self.active_count(),
            "active_types": self.active_types(),
            "missing_types": self.missing_types(),
            "diversity_level": self.diversity_level(),
            "f3_verdict": self.f3_verdict(),
            "mode3_collapse": self.is_mode3_collapse(),
            "earth_measurement_age_seconds": self.time_since_earth_measurement(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def summary(self) -> str:
        """One-line summary for cockpit display."""
        return (
            f"Witnesses: {self.active_count()}/5 [{self.diversity_level()}] "
            f"F3: {self.f3_verdict()} "
            f"Mode-3: {'⚠️ YES' if self.is_mode3_collapse() else '✓ no'} "
            f"Earth age: {self.time_since_earth_measurement() or 'never'}s"
        )


# ── Witness Diversity Score (standalone) ──────────────────────────────────────

def compute_witness_score(
    human_active: bool = True,
    model_a_active: bool = True,
    model_b_active: bool = False,
    earth_active: bool = False,
    independent_human_active: bool = False,
) -> dict:
    """
    Compute witness diversity score without requiring a session object.
    Useful for quick pre-flight checks.

    Returns dict with score, level, verdict, and recommendation.
    """
    active = sum([human_active, model_a_active, model_b_active, earth_active, independent_human_active])
    level = DIVERSITY_LEVEL_MAP.get(active, DiversityLevel.VOID)
    verdict = F3_VERDICT_MAP.get(active, F3Verdict.VOID)

    # Mode-3 detection
    model_count = sum([model_a_active, model_b_active])
    mode3 = model_count >= 2 and human_active and not earth_active

    recommendations = []
    if mode3:
        recommendations.append("MODE3_COLLAPSE: AI-judging-AI without Earth witness. Add a live measurement or independent human review.")
    if active < 3:
        recommendations.append(f"LOW_DIVERSITY: {active}/5 witness types. Minimum 3 required for F3 PASS.")
    if not earth_active:
        recommendations.append("NO_EARTH: No measurement or tool result in session. All claims are ungrounded.")
    if model_count >= 2 and not independent_human_active:
        recommendations.append("AI_AI_LOOP: Two models in conversation without independent oversight.")

    return {
        "score": active,
        "max_score": 5,
        "level": level,
        "f3_verdict": verdict,
        "mode3_collapse": mode3,
        "active_witnesses": {
            "HUMAN": human_active,
            "AI_MODEL_A": model_a_active,
            "AI_MODEL_B": model_b_active,
            "EARTH_MEASUREMENT": earth_active,
            "INDEPENDENT_HUMAN": independent_human_active,
        },
        "recommendations": recommendations,
        "computed_at": datetime.now(timezone.utc).isoformat(),
    }


# ── Pre-Forge Witness Gate ────────────────────────────────────────────────────

def pre_forge_witness_gate(
    witness_state: SessionWitnessState,
    action_class: str,
    required_diversity: int = 3,
) -> dict:
    """
    Pre-forge gate: refuse MUTATE/ATOMIC if witness diversity < threshold.

    This operationalizes F3 at the forge level.
    Before A-FORGE executes, call this gate.

    Args:
        witness_state: Current session witness state.
        action_class: observe | propose | mutate | deploy | communicate | allocate.
        required_diversity: Minimum witness types needed (default 3).

    Returns:
        dict with:
        - allowed: bool
        - verdict: PASS | HOLD | VOID
        - reason: explanation
    """
    # OBSERVE and PROPOSE always allowed (reversible)
    if action_class in ("observe", "propose"):
        return {
            "allowed": True,
            "verdict": "PASS",
            "reason": f"Action class '{action_class}' is reversible — witness gate bypassed",
            "witness_summary": witness_state.summary(),
        }

    # MUTATE, DEPLOY, ALLOCATE, COMMUNICATE require diversity
    count = witness_state.active_count()

    if witness_state.is_mode3_collapse():
        return {
            "allowed": False,
            "verdict": "HOLD",
            "reason": (
                f"F3 Mode-3 collapse detected: {count}/5 witnesses active. "
                "AI-judging-AI without Earth measurement. "
                "Add a live tool call or independent human review before MUTATE."
            ),
            "witness_summary": witness_state.summary(),
            "required_action": "Register EARTH_MEASUREMENT or INDEPENDENT_HUMAN witness",
        }

    if count < required_diversity:
        return {
            "allowed": False,
            "verdict": "HOLD",
            "reason": (
                f"F3 TRI-WITNESS: {count}/5 witness types active, "
                f"{required_diversity} required for {action_class}. "
                f"Missing: {witness_state.missing_types()}"
            ),
            "witness_summary": witness_state.summary(),
            "required_action": f"Activate at least {required_diversity - count} more witness types",
        }

    return {
        "allowed": True,
        "verdict": "PASS",
        "reason": f"F3 TRI-WITNESS satisfied: {count}/5 witnesses active",
        "witness_summary": witness_state.summary(),
    }


# ── Self-test ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Witness Diversity Self-Test ===\n")

    # Test 1: Full witness diversity
    print("Test 1: Full witness diversity (5/5)")
    state = SessionWitnessState("test-session-1")
    state.register_human()
    state.register_model_output("deepseek-v4-pro", is_primary=True)
    state.register_model_output("claude-opus-4-8", is_primary=False)
    state.register_earth_measurement("brave_web_search", "query:test")
    state.register(WitnessType.INDEPENDENT_HUMAN, "reviewer:alice")
    assert state.active_count() == 5
    assert state.diversity_level() == DiversityLevel.FULL_WITNESS
    assert state.f3_verdict() == F3Verdict.PASS
    assert not state.is_mode3_collapse()
    print(f"  PASS: {state.summary()}")

    # Test 2: Mode-3 collapse (Arif + 2 LLMs, no Earth)
    print("\nTest 2: Mode-3 collapse detection")
    state2 = SessionWitnessState("test-session-2")
    state2.register_human()
    state2.register_model_output("deepseek-v4-pro", is_primary=True)
    state2.register_model_output("claude-opus-4-8", is_primary=False)
    # No Earth measurement
    assert state2.active_count() == 3
    assert state2.is_mode3_collapse()
    print(f"  PASS: {state2.summary()}")
    print("  Mode-3 collapse correctly detected")

    # Test 3: Standalone score function
    print("\nTest 3: Standalone compute_witness_score")
    score = compute_witness_score(
        human_active=True,
        model_a_active=True,
        model_b_active=True,
        earth_active=False,
        independent_human_active=False,
    )
    assert score["mode3_collapse"]
    assert score["score"] == 3
    assert score["f3_verdict"] == F3Verdict.PASS  # 3/5 = MINIMAL but still PASS
    assert len(score["recommendations"]) >= 2
    print(f"  Score: {score['score']}/5, Level: {score['level']}, Verdict: {score['f3_verdict']}")
    print(f"  Recommendations: {score['recommendations']}")

    # Test 4: Pre-forge gate on MUTATE with Mode-3
    print("\nTest 4: Pre-forge gate — MUTATE blocked by Mode-3")
    gate_result = pre_forge_witness_gate(state2, "mutate")
    assert not gate_result["allowed"]
    assert gate_result["verdict"] == "HOLD"
    print(f"  Allowed: {gate_result['allowed']}")
    print(f"  Verdict: {gate_result['verdict']}")
    print(f"  Reason: {gate_result['reason']}")

    # Test 5: Pre-forge gate on OBSERVE always allowed
    print("\nTest 5: Pre-forge gate — OBSERVE always allowed")
    gate_result2 = pre_forge_witness_gate(state2, "observe")
    assert gate_result2["allowed"]
    print(f"  Allowed: {gate_result2['allowed']}")

    # Test 6: Degraded (2/5) — no Earth, no independent human
    print("\nTest 6: Degraded state (2/5)")
    state3 = SessionWitnessState("test-session-3")
    state3.register_human()
    state3.register_model_output("deepseek-v4-pro", is_primary=True)
    assert state3.active_count() == 2
    assert state3.diversity_level() == DiversityLevel.DEGRADED
    assert state3.f3_verdict() == F3Verdict.CAUTION
    print(f"  PASS: {state3.summary()}")

    print("\n=== Witness Diversity Self-Test PASSED ===")
