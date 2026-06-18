"""GENESIS/006 L4 Legitimacy Lane Hook (REVERSIBLE FILE ARTIFACT).

L4 doctrine (005 §VI.4): "increase auditability, reversibility, public trust"

This is the META lane — it improves the audit/governance system itself.
NOT the productive economy.

This is a forge artifact, NOT a live kernel call. To activate:
  1. F13 ratify 006
  2. Move to /root/WEALTH/internal/lanes/  (or arifOS lanes)
  3. Wire into arif_judge_deliberate + arif_heart_critique

Proposal Contract (per 005 §VI):

    proposal_contract:
      lane: L4
      objective: string (e.g. "improve audit trail completeness")
      affected_agents: [list — usually AGI/ASI/APEX themselves]
      expected_gain:
        metric: "audit_completeness" | "reversibility_score" | "public_trust_delta"
        delta: number
        horizon: "1Y" | "3Y"
      affected_floors: [F1, F2, F4, F13]   # at minimum (this lane touches truth)
      reversibility: reversible              # L4 is by-design reversible (it's a meta-improvement)
      blast_radius: low | medium
      human_authority_required: false        # the audit system can self-improve, but only reversibly
      simulation_pass: not required
      ledger_ref: required (every L4 change is itself audited)
      f11_signature: required (this lane touches audit trail)
      sovereign_ack: required if affects APEX identity

Floor checks:
- F1 AMANAH (trust): every L4 change must itself be audited
- F2 TRUTH: L4 can NEVER propose false information
- F4 CLARITY: L4 changes must reduce entropy
- F13 SOVEREIGN: required if affects identity or audit of sovereignty

Lane tool binding:
  - arif_judge_deliberate(mode=floor_status)
  - arif_heart_critique(mode=maruah|deescalate|redteam)
  - arif_evidence_fetch(mode=fetch)

Lane metric: audit_completeness (primary), reversibility_score (secondary), public_trust_delta (tertiary)

Reversibility: this file is trivially reversible (rm).
"""
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class L4LegitimacyProposal:
    proposal_id: str
    objective: str
    affected_agents: list[str]
    expected_gain_metric: Literal[
        "audit_completeness",
        "reversibility_score",
        "public_trust_delta",
    ]
    expected_gain_delta: float
    horizon: Literal["1Y", "3Y"]
    affected_floors: list[Literal["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13"]]
    reversibility: Literal["reversible", "semi_reversible", "irreversible"]
    blast_radius: Literal["low", "medium", "high", "sovereign"]
    human_authority_required: bool
    ledger_ref: str
    f11_signature: str | None = None
    sovereign_ack: str | None = None

    def self_referential_check(self) -> bool:
        """L4 must never propose removing its own audit trail. F1 AMANAH."""
        if "audit_trail" in self.objective.lower() and "remove" in self.objective.lower():
            return False  # 888_HOLD
        if "kill_switch" in self.objective.lower() and "disable" in self.objective.lower():
            return False  # 888_HOLD
        if "888_HOLD" in self.objective and "remove" in self.objective.lower():
            return False  # 888_HOLD
        return True

    def requires_f11(self) -> bool:
        """L4 ALWAYS requires F11 — touches the audit trail itself."""
        return not self.f11_signature


# This file is a forge artifact. NO LIVE KERNEL CALL FROM THIS MODULE.
