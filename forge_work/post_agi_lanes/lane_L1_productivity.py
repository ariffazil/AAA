"""GENESIS/006 L1 Productivity Lane Hook (REVERSIBLE FILE ARTIFACT).

L1 doctrine (005 §VI.1): "increase output per unit compute, energy, capital"

This is a forge artifact, NOT a live kernel call. To activate:
  1. F13 ratify 006
  2. Move to /root/WEALTH/internal/lanes/
  3. Wire into wealth_omni_wisdom(mode=synthesize) dispatcher

Proposal Contract (per 005 §VI, enforced by arif_forge_execute(mode=preflight)):

    proposal_contract:
      proposal_id: "prop_<ulid>"
      lane: L1
      objective: string
      affected_agents: [list of agent IDs]
      expected_gain:
        metric: "output_per_joule" | "output_per_capital" | "compute_efficiency"
        delta: number
        horizon: "1Y" | "3Y" | "10Y"
      affected_floors: [F6, F7, F13]   # at minimum
      reversibility: reversible | semi_reversible | irreversible
      blast_radius: low | medium | high | sovereign
      rollback_plan: required
      human_authority_required: true   # productivity gains can affect labor
      simulation_pass:
        scenarios: ["baseline", "downside", "upside", "tail"]
        monte_carlo_runs: 1000
        p10_p50_p90: {p10: number, p50: number, p90: number}
      ledger_ref: "outcomes.jsonl#<line>"
      f11_signature: "<ed25519>"        # required if reversibility != reversible
      sovereign_ack: "<id>"              # required if blast_radius == sovereign

Floor checks:
- F6 MARUAH (dignity): productivity gain must not push job-displacement above lane threshold
- F7 HUMILITY: must be reversible OR carry explicit F11 signature
- F13 SOVEREIGN: required if blast_radius >= high

Lane tool binding: wealth_omni_wisdom(mode=synthesize, decision_context.lane="L1_productivity")
Lane metric: output_per_joule (primary), output_per_capital (secondary), compute_efficiency (tertiary)

Reversibility: this file is trivially reversible (rm).
"""
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class L1ProductivityProposal:
    proposal_id: str
    objective: str
    affected_agents: list[str]
    expected_gain_metric: Literal["output_per_joule", "output_per_capital", "compute_efficiency"]
    expected_gain_delta: float
    horizon: Literal["1Y", "3Y", "10Y"]
    affected_floors: list[Literal["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "F13"]]
    reversibility: Literal["reversible", "semi_reversible", "irreversible"]
    blast_radius: Literal["low", "medium", "high", "sovereign"]
    human_authority_required: bool
    rollback_plan_steps: list[str]
    max_rollback_time_hours: int
    simulation_pass: dict
    f11_signature: str | None = None
    sovereign_ack: str | None = None

    def requires_sovereign(self) -> bool:
        return self.blast_radius == "sovereign" and not self.sovereign_ack

    def requires_f11(self) -> bool:
        return self.reversibility != "reversible" and not self.f11_signature


# This file is a forge artifact. To activate, instantiate the dataclass
# with full proposal_contract and call arif_forge_execute(mode=preflight, proposal=this).
# NO LIVE KERNEL CALL FROM THIS MODULE. NO VAULT WRITES.
