"""GENESIS/006 L2 Distribution Lane Hook (REVERSIBLE FILE ARTIFACT).

L2 doctrine (005 §VI.2): "prevent wealth capture and dignity collapse"

This is a forge artifact, NOT a live kernel call. To activate:
  1. F13 ratify 006
  2. Move to /root/WEALTH/internal/lanes/
  3. Wire into wealth_inequality_kernel dispatcher

Proposal Contract (per 005 §VI):

    proposal_contract:
      lane: L2
      objective: string
      affected_agents: [list]
      expected_gain:
        metric: "gini_delta" | "mobility_index" | "bottom_quintile_runway"
        delta: number
        horizon: "1Y" | "3Y" | "10Y"
      affected_floors: [F6, F9, F13]   # at minimum
      reversibility: reversible          # L2 is by-design reversible
      blast_radius: medium | high        # dignity effects can be high
      human_authority_required: true
      simulation_pass: required (dignity_impact + inequality impact)
      ledger_ref: required
      f11_signature: required if reversibility != reversible

Floor checks:
- F6 MARUAH (dignity): distribution gain must protect bottom quintile
- F9 ANTI-HANTU (no covert extraction): L2 is the primary anti-hantu lane
- F13 SOVEREIGN: required for any irreversible distribution change

Lane tool binding: wealth_inequality_kernel(mode=analyze, domain=distribution, preset=malaysia)
Lane metric: gini_delta (primary), mobility_index (secondary), bottom_quintile_runway (tertiary)

Reversibility: this file is trivially reversible (rm).
"""
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class L2DistributionProposal:
    proposal_id: str
    objective: str
    affected_agents: list[str]
    expected_gain_metric: Literal["gini_delta", "mobility_index", "bottom_quintile_runway"]
    expected_gain_delta: float
    horizon: Literal["1Y", "3Y", "10Y"]
    affected_floors: list[Literal["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13"]]
    reversibility: Literal["reversible", "semi_reversible", "irreversible"]
    blast_radius: Literal["low", "medium", "high", "sovereign"]
    human_authority_required: bool
    rollback_plan_steps: list[str]
    simulation_pass: dict
    f11_signature: str | None = None
    sovereign_ack: str | None = None

    def anti_extraction_check(self) -> bool:
        """L2 must NEVER propose covert extraction. If gini_delta > 0.0, fails."""
        if self.expected_gain_metric == "gini_delta" and self.expected_gain_delta > 0.0:
            return False  # 888_HOLD: gini must DECREASE for distribution gain
        return True

    def requires_f13(self) -> bool:
        return self.reversibility == "irreversible" and not self.sovereign_ack


# This file is a forge artifact. To activate, instantiate + run anti_extraction_check
# + arif_forge_execute(mode=preflight). NO LIVE KERNEL CALL FROM THIS MODULE.
