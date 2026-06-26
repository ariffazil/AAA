"""GENESIS/006 L5 Ecology Lane Hook (REVERSIBLE FILE ARTIFACT).

L5 doctrine (005 §VI.5): "prevent energy, water, carbon, mineral overshoot"

This is a forge artifact, NOT a live kernel call. To activate:
  1. F13 ratify 006
  2. Move to /root/WEALTH/internal/lanes/
  3. Wire into wealth_energy_productivity dispatcher

Proposal Contract (per 005 §VI):

    proposal_contract:
      lane: L5
      objective: string
      affected_agents: [list — usually compute, energy, mining providers]
      expected_gain:
        metric: "joules_per_dollar_value" | "kg_co2_per_value_unit" | "grid_stress_delta"
        delta: number
        horizon: "1Y" | "3Y" | "10Y"
      affected_floors: [F7, F13]   # at minimum (ecology is binding)
      reversibility: reversible | semi_reversible   # operational; damage itself is irreversible
      blast_radius: low | medium | high
      human_authority_required: true
      simulation_pass: required (ecological load model)
      ledger_ref: required
      f11_signature: required if reversibility != reversible
      sovereign_ack: required for blast_radius == sovereign

Floor checks:
- F7 HUMILITY: ecology is binding — lane proposals must respect hard limits
- F13 SOVEREIGN: required for any irreversible ecological change (e.g. mining permits)

Lane tool binding:
  - wealth_energy_productivity(mode=load)
  - wealth_energy_productivity(mode=carbon)
  - wealth_energy_productivity(mode=pi)

Lane metric: joules_per_dollar_value (primary), kg_co2_per_value_unit (secondary),
             grid_stress_delta (tertiary)

Reversibility: this file is trivially reversible (rm).
"""
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class L5EcologyProposal:
    proposal_id: str
    objective: str
    affected_agents: list[str]
    expected_gain_metric: Literal[
        "joules_per_dollar_value",
        "kg_co2_per_value_unit",
        "grid_stress_delta",
    ]
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

    def ecological_load_check(self, current_kg_co2_per_year: float, hard_cap_kg_co2_per_year: float) -> bool:
        """L5 must NEVER exceed hard cap. F7 HUMILITY."""
        return current_kg_co2_per_year <= hard_cap_kg_co2_per_year

    def requires_f13(self) -> bool:
        return self.blast_radius == "sovereign" and not self.sovereign_ack


# This file is a forge artifact. NO LIVE KERNEL CALL FROM THIS MODULE.
