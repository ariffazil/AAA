"""
action_taxonomy.py — 8-class action taxonomy + 333 FORGE cycle for opencode-bot.
Owner: arif
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ActionClass(str, Enum):
    OBSERVE = "OBSERVE"
    SUGGEST = "SUGGEST"
    SIMULATE = "SIMULATE"
    DRAFT = "DRAFT"
    QUEUE = "QUEUE"
    EXECUTE_REVERSIBLE = "EXECUTE_REVERSIBLE"
    EXECUTE_HIGH_IMPACT = "EXECUTE_HIGH_IMPACT"
    IRREVERSIBLE = "IRREVERSIBLE"


# Map to constitutional decision classes
CLASS_TO_DECISION = {
    ActionClass.OBSERVE: "C1",
    ActionClass.SUGGEST: "C2",
    ActionClass.SIMULATE: "C2",
    ActionClass.DRAFT: "C3",
    ActionClass.QUEUE: "C3",
    ActionClass.EXECUTE_REVERSIBLE: "C4",
    ActionClass.EXECUTE_HIGH_IMPACT: "C4",
    ActionClass.IRREVERSIBLE: "C5",
}


@dataclass
class ActionVerdict:
    action_class: ActionClass
    decision_class: str
    reason: str
    needs_judge: bool
    needs_substrate: bool
    needs_explicit_ack: bool


IRREVERSIBLE_PATTERNS = re.compile(
    r"\b(rm\s+-rf|drop\s+(table|database)|delete\s+from|truncate\s+table|"
    r"git\s+push\s+.*--force|git\s+push\s+.*\s+-f\b|git\s+reset\s+--hard|"
    r"git\s+clean\s+-fd|docker\s+system\s+prune|docker\s+volume\s+prune|"
    r"mkfs\.|fdisk|parted|dd\s+if=)\b",
    re.IGNORECASE,
)

HIGH_IMPACT_PATTERNS = re.compile(
    r"\b(git\s+push|git\s+merge|git\s+rebase|docker\s+compose\s+up|"
    r"docker\s+compose\s+restart|systemctl\s+restart|systemctl\s+stop|"
    r"npm\s+install|pip\s+install|uv\s+add|apt\s+install)\b",
    re.IGNORECASE,
)

REVERSIBLE_PATTERNS = re.compile(
    r"\b(write|edit|modify|create|add|update|fix|refactor|test|format|lint|"
    r"ruff|black|prettier|pytest|make\s+test|make\s+build)\b",
    re.IGNORECASE,
)

SIMULATE_PATTERNS = re.compile(
    r"\b(simulate|dry.run|what.if|preview|plan|propose|draft.plan)\b",
    re.IGNORECASE,
)

QUEUE_PATTERNS = re.compile(
    r"\b(queue|defer|stage|schedule|later|tomorrow|hold\s+for)\b",
    re.IGNORECASE,
)

OBSERVE_PATTERNS = re.compile(
    r"\b(read|explain|show|status|health|audit|list|describe|what|how|why|"
    r"translate|summarize|check)\b",
    re.IGNORECASE,
)


def classify(prompt: str) -> ActionVerdict:
    """Classify a sovereign prompt into the 8-class taxonomy."""
    p = prompt.lower()

    if IRREVERSIBLE_PATTERNS.search(prompt):
        return ActionVerdict(
            action_class=ActionClass.IRREVERSIBLE,
            decision_class="C5",
            reason="Irreversible/destructive pattern detected",
            needs_judge=True,
            needs_substrate=True,
            needs_explicit_ack=True,
        )

    if SIMULATE_PATTERNS.search(prompt):
        return ActionVerdict(
            action_class=ActionClass.SIMULATE,
            decision_class="C2",
            reason="Dry-run / simulation requested",
            needs_judge=False,
            needs_substrate=False,
            needs_explicit_ack=False,
        )

    if QUEUE_PATTERNS.search(prompt):
        return ActionVerdict(
            action_class=ActionClass.QUEUE,
            decision_class="C3",
            reason="Work queued for later sovereign approval",
            needs_judge=False,
            needs_substrate=False,
            needs_explicit_ack=False,
        )

    if OBSERVE_PATTERNS.search(prompt):
        return ActionVerdict(
            action_class=ActionClass.OBSERVE,
            decision_class="C1",
            reason="Read-only observation",
            needs_judge=False,
            needs_substrate=False,
            needs_explicit_ack=False,
        )

    if HIGH_IMPACT_PATTERNS.search(prompt):
        return ActionVerdict(
            action_class=ActionClass.EXECUTE_HIGH_IMPACT,
            decision_class="C4",
            reason="High-impact reversible operation",
            needs_judge=True,
            needs_substrate=True,
            needs_explicit_ack=False,
        )

    if REVERSIBLE_PATTERNS.search(prompt):
        return ActionVerdict(
            action_class=ActionClass.EXECUTE_REVERSIBLE,
            decision_class="C4",
            reason="Reversible file/system mutation",
            needs_judge=True,
            needs_substrate=True,
            needs_explicit_ack=False,
        )

    # Default ambiguous prompt → suggest
    return ActionVerdict(
        action_class=ActionClass.SUGGEST,
        decision_class="C2",
        reason="Ambiguous prompt — default to suggestion/plan",
        needs_judge=False,
        needs_substrate=False,
        needs_explicit_ack=False,
    )


class ForgePhase(str, Enum):
    PREPARE = "PREPARE"
    EXECUTE = "EXECUTE"
    VERIFY = "VERIFY"


FORGE_CYCLE = {
    ForgePhase.PREPARE: ["classify", "pre-govern", "substrate", "thermo-pre"],
    ForgePhase.EXECUTE: ["judge", "opencode", "post-witness", "thermo-post"],
    ForgePhase.VERIFY: ["diff", "vault-seal", "nats-publish", "session-summary"],
}
