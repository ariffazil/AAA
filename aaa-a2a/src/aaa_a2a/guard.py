"""DelegationGuard — cross-organ boundary enforcement.

16 rules derived from peer contracts + constitutional floors.
Extracted from AAA a2a-server/server.js lines 960-1053.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

from aaa_a2a.models import DelegationRule

# ── The 16 Canonical Delegation Rules ────────────────────────────────────

DELEGATION_RULES: list[DelegationRule] = [
    # A-FORGE cannot self-approve
    DelegationRule(
        source="a-forge",
        target_contains="forge_approve",
        verdict="blocked",
        reason="F8 LAW: A-FORGE cannot self-approve. Requires arifOS judge.",
        floor="F8",
    ),
    DelegationRule(
        source="a-forge",
        target_contains="forge_validate",
        verdict="blocked",
        reason="F8 LAW: A-FORGE cannot self-validate. Requires external witness.",
        floor="F8",
    ),
    # A-FORGE cannot judge or seal
    DelegationRule(
        source="a-forge",
        target_contains="arif_judge",
        verdict="blocked",
        reason="F8 LAW: A-FORGE cannot issue constitutional verdicts. Only arifOS judges.",
        floor="F8",
    ),
    DelegationRule(
        source="a-forge",
        target_contains="arif_seal",
        verdict="blocked",
        reason="F8 LAW: A-FORGE cannot seal VAULT entries. Only arifOS seals.",
        floor="F8",
    ),
    DelegationRule(
        source="a-forge",
        target_contains="vault_seal",
        verdict="blocked",
        reason="F8 LAW: A-FORGE cannot write to VAULT999 directly. Requires arifOS judge path.",
        floor="F8",
    ),
    # A-FORGE cannot access human substrate data
    DelegationRule(
        source="a-forge",
        target_contains="well_assess",
        verdict="blocked",
        reason="F8 LAW: A-FORGE cannot read human substrate data. WELL owns this.",
        floor="F8",
    ),
    DelegationRule(
        source="a-forge",
        target_contains="well_guard_dignity",
        verdict="blocked",
        reason="F6 MARUAH: A-FORGE cannot access dignity data. WELL guards this.",
        floor="F6",
    ),
    # Evidence organs cannot mutate other organ records
    DelegationRule(
        source="geox",
        target_contains="wealth_",
        verdict="blocked",
        reason="F8 LAW: GEOX cannot mutate WEALTH records.",
        floor="F8",
    ),
    DelegationRule(
        source="geox",
        target_contains="well_",
        verdict="blocked",
        reason="F8 LAW: GEOX cannot mutate WELL records.",
        floor="F8",
    ),
    DelegationRule(
        source="wealth",
        target_contains="geox_",
        verdict="blocked",
        reason="F8 LAW: WEALTH cannot mutate GEOX evidence.",
        floor="F8",
    ),
    DelegationRule(
        source="wealth",
        target_contains="well_",
        verdict="blocked",
        reason="F8 LAW: WEALTH cannot mutate WELL records.",
        floor="F8",
    ),
    DelegationRule(
        source="well",
        target_contains="geox_",
        verdict="blocked",
        reason="F8 LAW: WELL cannot mutate GEOX evidence.",
        floor="F8",
    ),
    DelegationRule(
        source="well",
        target_contains="wealth_",
        verdict="blocked",
        reason="F8 LAW: WELL cannot mutate WEALTH records.",
        floor="F8",
    ),
    # Evidence organs cannot deploy
    DelegationRule(
        source="geox",
        target_contains="deploy",
        verdict="blocked",
        reason="F8 LAW: GEOX is evidence-only. Cannot deploy.",
        floor="F8",
    ),
    DelegationRule(
        source="wealth",
        target_contains="deploy",
        verdict="blocked",
        reason="F8 LAW: WEALTH is evidence-only. Cannot deploy.",
        floor="F8",
    ),
    DelegationRule(
        source="well",
        target_contains="deploy",
        verdict="blocked",
        reason="F8 LAW: WELL is reflect-only. Cannot deploy.",
        floor="F8",
    ),
    # No organ can override F13 or bypass 888
    DelegationRule(
        source=None,
        target_contains="f13_override",
        verdict="blocked",
        reason="F13 SOVEREIGN: Human veto cannot be overridden by any organ.",
        floor="F13",
    ),
    DelegationRule(
        source=None,
        target_contains="bypass_888",
        verdict="blocked",
        reason="F13 SOVEREIGN: 888 HOLD cannot be bypassed by any organ.",
        floor="F13",
    ),
]


# ── Guard Function ───────────────────────────────────────────────────────


class DelegationVerdict:
    """Result of a delegation check."""

    __slots__ = ("blocked", "warned", "reason", "floor")

    def __init__(self, blocked: bool, warned: bool, reason: str, floor: str | None = None):
        self.blocked = blocked
        self.warned = warned
        self.reason = reason
        self.floor = floor

    @property
    def ok(self) -> bool:
        return not self.blocked

    def __repr__(self) -> str:
        if self.blocked:
            return f"BLOCKED: {self.reason}"
        if self.warned:
            return f"WARNING: {self.reason}"
        return "PASS"


def check_delegation(
    source_agent: str | None,
    target_skill: str | None,
    message_text: str = "",
    rules: list[DelegationRule] | None = None,
) -> DelegationVerdict:
    """Check if a delegation from source to target is allowed.

    Args:
        source_agent: The agent requesting the delegation (e.g. "a-forge", "geox")
        target_skill: The target skill/tool being invoked
        message_text: The message text (for substring matching)
        rules: Override rules (defaults to canonical 16)

    Returns:
        DelegationVerdict with blocked/warned/reason
    """
    if rules is None:
        rules = DELEGATION_RULES

    source_lower = (source_agent or "").lower()
    target_lower = (target_skill or "").lower()
    msg_lower = message_text.lower()

    for rule in rules:
        # Source match (None = any source)
        src_match = not rule.source or source_lower.startswith(rule.source.lower())
        # Target match (substring in target skill or message text)
        tgt_match = (
            not rule.target_contains
            or rule.target_contains.lower() in target_lower
            or rule.target_contains.lower() in msg_lower
        )

        if src_match and tgt_match:
            return DelegationVerdict(
                blocked=rule.verdict == "blocked",
                warned=rule.verdict == "warned",
                reason=rule.reason,
                floor=rule.floor,
            )

    return DelegationVerdict(blocked=False, warned=False, reason="")
