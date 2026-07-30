"""
Capability Resolver — Maps semantic capabilities to registered, callable tools.

Consumes the Federation Registry Spine. Never consults connector metadata.
Capabilities are STABLE. Tool names are FLUID. Rename a tool, mission doesn't break.
"""

import json
from pathlib import Path

from .schemas import (
    OrganName, ExecutionMode, CapabilityRef, PipelineStage,
    MISSION_CAPABILITY_MAP, MissionState,
)

SPINE_PATH = Path("/root/AAA/contracts/federation-registry-spine.json")
CALLABILITY_PATH = Path("/root/AAA/contracts/federation-callability-matrix.json")

# ── Capability → Tool Resolution Table ────────────────────────────
# Each semantic capability maps to one or more registered tools.
# The resolver picks the healthiest, most appropriate match.
# When tools are renamed/merged/retired, ONLY THIS TABLE changes.
# Missions and pipelines DO NOT.

CAPABILITY_TOOL_MAP: dict[str, list[dict]] = {
    # ── arifOS capabilities ──
    "system_health": [
        {"organ": "arifOS", "tool": "arif_observe", "mode": "health", "priority": 1},
    ],
    "structured_reasoning": [
        {"organ": "arifOS", "tool": "arif_think", "mode": "reason", "priority": 1},
    ],
    "constitutional_judgment": [
        {"organ": "arifOS", "tool": "arif_judge", "mode": "evaluate", "priority": 1},
    ],
    "authority_validation": [
        {"organ": "arifOS", "tool": "arif_judge", "mode": "authority_check", "priority": 1},
    ],
    "governed_recall": [
        {"organ": "arifOS", "tool": "arif_memory", "mode": "recall", "priority": 1},
    ],
    "delta_report": [
        {"organ": "arifOS", "tool": "arif_observe", "mode": "delta", "priority": 1},
    ],
    "verification": [
        {"organ": "arifOS", "tool": "arif_observe", "mode": "verify", "priority": 1},
    ],

    # ── GEOX capabilities ──
    "data_query": [
        {"organ": "GEOX", "tool": "geox_surface_status", "priority": 1},
    ],
    "domain_interpretation": [
        {"organ": "GEOX", "tool": "geox_basin", "priority": 2},
        {"organ": "GEOX", "tool": "geox_sequence", "priority": 2},
        {"organ": "GEOX", "tool": "geox_seismic_interpret", "priority": 2},
        {"organ": "GEOX", "tool": "geox_physical_reality_interpret", "priority": 1},
    ],
    "prospect_evaluation": [
        {"organ": "GEOX", "tool": "geox_prospect", "priority": 1},
        {"organ": "GEOX", "tool": "geox_subsurface_model", "priority": 2},
    ],
    "falsification": [
        {"organ": "GEOX", "tool": "geox_doctrine", "priority": 1},
        {"organ": "GEOX", "tool": "geox_claim", "priority": 2},
        {"organ": "GEOX", "tool": "geox_evidence", "priority": 2},
    ],
    "contradiction_scan": [
        {"organ": "GEOX", "tool": "geox_doctrine", "priority": 1},
        {"organ": "GEOX", "tool": "geox_claim", "priority": 2},
    ],
    "consequence_modeling": [
        {"organ": "GEOX", "tool": "geox_basin", "priority": 1},
        {"organ": "GEOX", "tool": "geox_prospect", "priority": 2},
    ],

    # ── WEALTH capabilities ──
    "market_query": [
        {"organ": "WEALTH", "tool": "wealth_market_reality_loop", "priority": 1},
    ],
    "capital_diagnosis": [
        {"organ": "WEALTH", "tool": "wealth_capital_diagnosis_loop", "priority": 1},
    ],
    "capital_exposure": [
        {"organ": "WEALTH", "tool": "wealth_risk_downside_loop", "priority": 1},
        {"organ": "WEALTH", "tool": "wealth_institutional_stress_index", "priority": 2},
    ],
    "market_health": [
        {"organ": "WEALTH", "tool": "wealth_reality_intake_loop", "priority": 1},
    ],

    # ── WELL capabilities ──
    "human_readiness": [
        {"organ": "WELL", "tool": "well_signal_coverage", "priority": 1},
        {"organ": "WELL", "tool": "well_registry_status", "priority": 2},
    ],
    "machine_health": [
        {"organ": "WELL", "tool": "well_system_registry_status", "priority": 1},
    ],

    # ── A-FORGE capabilities ──
    "execution_planning": [
        {"organ": "A-FORGE", "tool": "a-forge-plan", "priority": 1},
    ],
    "forge_execute": [
        {"organ": "A-FORGE", "tool": "a-forge-execute", "priority": 1},
    ],

    # ── VAULT999 capabilities ──
    "immutable_record": [
        {"organ": "VAULT999", "tool": "arif_seal", "priority": 1},
    ],
    "chain_verification": [
        {"organ": "VAULT999", "tool": "arif_seal", "mode": "verify", "priority": 1},
    ],
}


class CapabilityResolver:
    """Resolves semantic capabilities to registered, callable, healthy tools."""

    def __init__(self, spine_path: Path | None = None):
        self.spine_path = spine_path or SPINE_PATH
        self.spine: dict = {}
        self.callability: dict = {}
        self._loaded = False

    def load(self) -> None:
        """Load registry spine and callability matrix. Fails closed."""
        if not self.spine_path.exists():
            raise FileNotFoundError(f"Registry spine not found: {self.spine_path}")

        with open(self.spine_path) as f:
            self.spine = json.load(f)

        callability_path = self.spine_path.parent / "federation-callability-matrix.json"
        if callability_path.exists():
            with open(callability_path) as f:
                self.callability = json.load(f)

        self._loaded = True

    def _get_organ_health(self, organ: str) -> dict:
        """Get organ health from the spine."""
        organs = self.spine.get("organs", {})
        return organs.get(organ, {})

    def _is_tool_deprecated(self, organ: str, tool_name: str) -> bool:
        """Check if a tool is in the DEPRECATED list."""
        organ_data = self.spine.get("organs", {}).get(organ, {})
        tools = organ_data.get("tools", {})
        deprecated = tools.get("DEPRECATED", [])
        return any(t.get("name") == tool_name for t in deprecated)

    def _is_tool_internal(self, organ: str, tool_name: str) -> bool:
        """Check if a tool is INTERNAL_CALLABLE (not on public surface)."""
        organ_data = self.spine.get("organs", {}).get(organ, {})
        tools = organ_data.get("tools", {})
        internal = tools.get("INTERNAL_CALLABLE", [])
        return any(t.get("name") == tool_name for t in internal)

    def resolve_capability(self, cap_ref: CapabilityRef, step: int) -> list[PipelineStage]:
        """Resolve a semantic capability to one or more pipeline stages with concrete tools."""
        stages: list[PipelineStage] = []
        capability = cap_ref.capability
        organ = cap_ref.organ.value if isinstance(cap_ref.organ, OrganName) else cap_ref.organ

        # Look up in the capability→tool map
        candidates = CAPABILITY_TOOL_MAP.get(capability, [])
        if not candidates:
            # Try partial match
            for key in CAPABILITY_TOOL_MAP:
                if capability in key or key in capability:
                    candidates = CAPABILITY_TOOL_MAP[key]
                    break

        if not candidates:
            # No tool mapped — record as unresolved
            stages.append(PipelineStage(
                step=step,
                organ=cap_ref.organ,
                capability=capability,
                mode=cap_ref.mode,
                resolved_tool=None,
                resolved_tool_healthy=False,
                selection_reason=f"No tool mapped for capability '{capability}' — HOLD required",
            ))
            return stages

        # Filter to matching organ
        organ_candidates = [c for c in candidates if c["organ"] == organ]
        if not organ_candidates:
            organ_candidates = candidates  # fallback: any organ

        # Sort by priority (lower = better)
        organ_candidates.sort(key=lambda c: c.get("priority", 99))

        # Pick the best candidate
        best = organ_candidates[0]
        tool_name = best["tool"]

        # Validate against registry
        organ_health = self._get_organ_health(organ)
        is_deprecated = self._is_tool_deprecated(organ, tool_name)
        is_internal = self._is_tool_internal(organ, tool_name)

        if is_deprecated:
            # Try next candidate
            for alt in organ_candidates[1:]:
                if not self._is_tool_deprecated(organ, alt["tool"]):
                    best = alt
                    tool_name = alt["tool"]
                    is_deprecated = False
                    break

        healthy = organ_health.get("status") == "healthy" and not is_deprecated

        stages.append(PipelineStage(
            step=step,
            organ=cap_ref.organ,
            capability=capability,
            mode=cap_ref.mode,
            resolved_tool=tool_name,
            resolved_tool_healthy=healthy,
            selection_reason=cap_ref.reason,
            fallback_tool=organ_candidates[1]["tool"] if len(organ_candidates) > 1 else None,
            fallback_healthy=healthy,  # approximate
        ))

        return stages

    def resolve_mission(self, mission: MissionState) -> list[PipelineStage]:
        """Resolve all capabilities for a mission into a pipeline."""
        if not self._loaded:
            self.load()

        capabilities = MISSION_CAPABILITY_MAP.get(mission, [])
        all_stages: list[PipelineStage] = []
        step = 0

        for cap_ref in capabilities:
            stages = self.resolve_capability(cap_ref, step)
            all_stages.extend(stages)
            step += 1

        # Set up dependencies (each stage depends on the previous)
        for i in range(1, len(all_stages)):
            if not all_stages[i].depends_on:
                all_stages[i].depends_on = [all_stages[i-1].step]

        return all_stages

    def validate_pipeline(self, stages: list[PipelineStage]) -> list[str]:
        """Validate pipeline against router invariants. Returns list of violations."""
        violations: list[str] = []

        for stage in stages:
            # 1. No unregistered tool
            if stage.resolved_tool is None:
                violations.append(f"[{stage.step}] {stage.capability}: No tool resolved — HOLD")

            # 2. Deprecated tool detected
            organ_key = stage.organ.value if isinstance(stage.organ, OrganName) else stage.organ
            if stage.resolved_tool and self._is_tool_deprecated(organ_key, stage.resolved_tool):
                violations.append(f"[{stage.step}] {stage.resolved_tool}: Tool is DEPRECATED")

            # 3. Read-only missions cannot mutate
            if stage.mode == ExecutionMode.MUTATE and stage.organ != OrganName.AFORGE:
                violations.append(f"[{stage.step}] {stage.capability}: MUTATE mode requires A-FORGE")

        return violations
