"""GENESIS/006 L3 Sovereignty Lane Hook (REVERSIBLE FILE ARTIFACT).

L3 doctrine (005 §VI.3): "reduce foreign dependency"

This is a forge artifact, NOT a live kernel call. To activate:
  1. F13 ratify 006
  2. Move to /root/WEALTH/internal/lanes/
  3. Wire into wealth_field_macro + wealth_conservation_capital

Proposal Contract (per 005 §VI):

    proposal_contract:
      lane: L3
      objective: string
      affected_agents: [list — usually energy/compute/data providers]
      expected_gain:
        metric: "foreign_model_dependency_delta" | "chip_dependency_delta" | "data_residency_score"
        delta: number
        horizon: "3Y" | "10Y" | "perpetual"
      affected_floors: [F8, F11, F12, F13]   # at minimum
      reversibility: semi_reversible | irreversible   # compute sovereignty = civilizational
      blast_radius: high | sovereign
      human_authority_required: true
      simulation_pass: required (compute, energy, geopolitical scenarios)
      ledger_ref: required
      f11_signature: required (this lane ALWAYS touches identity)
      sovereign_ack: required for blast_radius == sovereign

Floor checks:
- F8 SOVEREIGN_BOUNDARY: no opaque foreign control surface
- F11 IDENTITY: every sovereignty change seals to VAULT999
- F12 LAW: every sovereignty change must respect data residency / export law
- F13 SOVEREIGN: required for blast_radius >= high

Lane tool binding:
  - wealth_field_macro(mode=sovereignty)
  - wealth_conservation_capital(mode=sovereign_assets)
  - wealth_omni_wisdom(mode=hysteresis, path_params=sovereignty_state)

Lane metric: foreign_model_dependency_delta (primary), chip_dependency_delta (secondary),
             data_residency_score (tertiary)

Reversibility: this file is trivially reversible (rm).
"""
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class L3SovereigntyProposal:
    proposal_id: str
    objective: str
    affected_agents: list[str]
    expected_gain_metric: Literal[
        "foreign_model_dependency_delta",
        "chip_dependency_delta",
        "data_residency_score",
    ]
    expected_gain_delta: float
    horizon: Literal["3Y", "10Y", "perpetual"]
    affected_floors: list[Literal["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13"]]
    reversibility: Literal["reversible", "semi_reversible", "irreversible"]
    blast_radius: Literal["low", "medium", "high", "sovereign"]
    human_authority_required: bool
    rollback_plan_steps: list[str]
    simulation_pass: dict
    f11_signature: str | None = None
    sovereign_ack: str | None = None

    def requires_f11(self) -> bool:
        """L3 ALWAYS requires F11 — sovereignty touches identity."""
        return not self.f11_signature

    def requires_f13(self) -> bool:
        return self.blast_radius == "sovereign" and not self.sovereign_ack


# This file is a forge artifact. NO LIVE KERNEL CALL FROM THIS MODULE.
