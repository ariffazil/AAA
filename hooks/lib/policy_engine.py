#!/usr/bin/env python3
"""
policy_engine.py — Policy Evaluation Engine for AAA Hook Events
Canonical Path: /root/AAA/hooks/lib/policy_engine.py
Authority: AAA-HOOK-FORGE-V1.0 · Section 6.2, 7 & governance/AAA-HOOK-POLICY-V1.yaml

Evaluates canonical HookEvents against constitutional floors and risk ceilings,
returning a deterministic HookDecision adhering to the monotonic restriction ladder.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from event_schema import (
    BLOCKING_EVENTS,
    CANONICAL_EVENTS,
    RISK_CLASSES,
    VERDICT_LADDER,
    VERDICT_RANK,
)
from decision_schema import HookDecision, make_decision, validate_decision, compose_chain

POLICY_YAML_PATH = Path("/root/AAA/governance/AAA-HOOK-POLICY-V1.yaml")

# Canonical source of truth: hooks/lib/federation_hook_engine.py
# Do NOT re-declare this list. scripts/hook_mesh_check.py fails the build if the
# enumerated fail-safe classes are duplicated or drift from
# governance/AGENTIC-HOOK-MESH-V1.yaml (separation_of_powers.enumerated_fail_safe_classes).
from federation_hook_engine import FORBIDDEN_MUTATION_TARGETS as _FORBIDDEN_CANON

FORBIDDEN_MUTATION_TARGETS: Set[str] = set(_FORBIDDEN_CANON)

# Unconditional read-only / bootstrap pass tools
UNCONDITIONAL_PASS_TOOLS: Set[str] = {
    "arif_init",
    "read",
    "view_file",
    "glob",
    "grep",
    "grep_search",
    "find_by_name",
    "list_dir",
    "duckdb_describe",
    "duckdb_list_approved_datasets",
    "forge_probe",
    "forge_scan",
    "forge_status",
    "forge_registry_status",
    "read_url_content",
    "search_web",
    "list_resources",
    "read_resource",
    "manage_task",
}


class PolicyEngine:
    """Evaluates canonical events against AAA constitutional policies."""

    def __init__(self, policy_path: Optional[Path] = None):
        self.policy_path = policy_path or POLICY_YAML_PATH
        self.forbidden_targets = set(FORBIDDEN_MUTATION_TARGETS)
        self.unconditional_pass = set(UNCONDITIONAL_PASS_TOOLS)

    def evaluate(self, event: HookEvent) -> HookDecision:
        """Evaluates an event and produces a monotonic HookDecision."""
        event_name = event.event_name
        tool_name = event.action.tool_name if event.action else ""
        target_path = event.action.target_path if event.action else ""
        risk_class = event.risk_class or "R1"

        # Non-blocking events always pass with ALLOW
        if event_name not in BLOCKING_EVENTS:
            return HookDecision(
                event_id=event.event_id,
                verdict="ALLOW",
                reason_codes=["NON_BLOCKING_EVENT"],
                risk_class=risk_class,
                constitutional_floors=["F4"],
                message=f"Event {event_name} is non-blocking",
            )

        # Policy violation events always HOLD or DENY
        if event_name == "aaa.policy.violation":
            return HookDecision(
                event_id=event.event_id,
                verdict="HOLD",
                reason_codes=["POLICY_VIOLATION_TRIGGERED"],
                risk_class="R3",
                constitutional_floors=["F1", "F13"],
                message="Policy violation signaled; execution held",
            )

        # 1. Unconditional Pass Gate (F4/F8: Zero friction on read/probe/init)
        if tool_name in self.unconditional_pass:
            return HookDecision(
                event_id=event.event_id,
                verdict="ALLOW",
                reason_codes=["UNCONDITIONAL_PASS_TOOL"],
                risk_class="R0",
                constitutional_floors=["F4", "F8"],
                message=f"Tool {tool_name} is in unconditional pass allowlist",
            )

        # 2. Hard Security Boundaries (F13 SOVEREIGN / F1 AMANAH)
        if target_path:
            norm_target = os.path.normpath(target_path)
            for forbidden in self.forbidden_targets:
                if (
                    forbidden in target_path
                    or forbidden in norm_target
                    or norm_target.startswith(forbidden)
                    or norm_target.endswith(forbidden.lstrip("/"))
                ):
                    return HookDecision(
                        event_id=event.event_id,
                        verdict="DENY",
                        reason_codes=["FORBIDDEN_MUTATION_TARGET"],
                        risk_class="R4",
                        constitutional_floors=["F1", "F13"],
                        message=f"Mutation target {target_path} is strictly forbidden",
                    )

        # 3. Risk Class Floor Evaluation
        if risk_class in ("R3", "R4"):
            # High risk or irreversible production mutations require 888_HOLD
            return HookDecision(
                event_id=event.event_id,
                verdict="HOLD",
                reason_codes=["HIGH_RISK_REQUIRE_HOLD"],
                risk_class=risk_class,
                constitutional_floors=["F1", "F4", "F13"],
                message=f"Risk class {risk_class} exceeds autonomous execution threshold",
            )

        if risk_class == "R2":
            # Reversible local write with constraints
            return HookDecision(
                event_id=event.event_id,
                verdict="ALLOW_WITH_CONSTRAINTS",
                reason_codes=["CONSTRAINED_LOCAL_MUTATION"],
                risk_class="R2",
                constitutional_floors=["F1", "F4"],
                message="Reversible local mutation permitted with rollback checkpointing",
            )

        # R0 and R1 are unconditionally ALLOW for local digital work
        return HookDecision(
            event_id=event.event_id,
            verdict="ALLOW",
            reason_codes=["LOCAL_DIGITAL_WORK_MUBAH"],
            risk_class=risk_class,
            constitutional_floors=["F1", "F4", "F8"],
            message="Digital work is MUBAH; autonomous execution permitted",
        )
