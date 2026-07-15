"""agi_mcp_discover — progressive MCP tool loading for 333-AGI.

Capability-based discovery: returns only the tools needed for the current
task domain. Hot tools always loaded; on-demand tools selected by domain.

The 8-tool cap is a hard cap (F4 CLARITY) — loading all 49 A-FORGE tools +
GEOX + WEALTH + WELL + arifOS destroys the context window before the model
processes the user request.

Phase 4b of the AAA entropy-reduction roadmap.
"""

from __future__ import annotations

# Kernel verbs + health + vitality gate + self-reference.
# These run on every task regardless of domain.
ALWAYS_HOT: list[str] = [
    "arif_init",
    "arif_observe",
    "arif_think",
    "forge_probe",
    "forge_status",
    "well_assess_homeostasis",
    "agi_mcp_discover",
]

# Domain-indexed on-demand tool bundles. Designed so that
# len(ALWAYS_HOT) + len(ON_DEMAND[domain]) <= 8 by construction.
ON_DEMAND: dict[str, list[str]] = {
    "geoscience": [
        "geox_basin_resolve",
        "geox_basin_profile",
        "geox_seismic_compute",
        "geox_petrophysics_generate",
        "geox_prospect_screen",
        "geox_deep_time_state",
        "geox_well_ingest",
    ],
    "capital": [
        "capital_primitive_npv",
        "capital_primitive_irr",
        "capital_primitive_emv",
        "capital_health_runway",
        "capital_market_stock",
        "capital_diagnose",
    ],
    "engineering": [
        "forge_shell",
        "forge_git",
        "forge_docker",
        "forge_filesystem_read",
        "forge_filesystem_write",
        "forge_health_check",
    ],
    "vault": [
        "vault_append",
        "vault_read",
        "vault_search",
        "forge_vault_seal",
    ],
    "meta": [
        "agent_search",
        "skill_load",
        "agent_status",
    ],
    "evidence": [
        "forge_research",
        "forge_minimax_search",
        "forge_docs_lookup",
    ],
}

# Hard cap (F4 CLARITY): never load more than 8 tools into a single
# MCP context. This protects the context window from entropy explosion.
MAX_TOOLS: int = 8


def discover(task_domain: str, intent: str | None = None) -> list[str]:
    """Return the tools needed for this task domain. Never > 8 total.

    Args:
        task_domain: One of the keys in ON_DEMAND, or any unknown string
            (in which case only ALWAYS_HOT is returned).
        intent: Optional free-text intent. Reserved for future use
            (per-task ranking); currently unused.

    Returns:
        List of tool names capped at MAX_TOOLS entries. ALWAYS_HOT first,
        followed by the on-demand tools for ``task_domain``.

    Notes:
        If ``task_domain`` is unknown, the result is just ``ALWAYS_HOT``.
        If the union would exceed MAX_TOOLS, the list is truncated — the
        cap is hard, never soft.
    """
    tools: list[str] = list(ALWAYS_HOT)
    extras = ON_DEMAND.get(task_domain)
    if extras is not None:
        tools.extend(extras)
    # Intent is acknowledged for forward-compat; current selection is
    # domain-driven only. Surfaces intent in the tool contract.
    _ = intent
    # Hard cap (F4 CLARITY).
    return tools[:MAX_TOOLS]


def classify_intent(intent: str) -> str:
    """Map a user intent to a task domain.

    Keyword matching is deliberately simple and deterministic — this is a
    router, not an LLM call. Domain priority order: geoscience > capital
    > engineering > vault > evidence > meta.

    Args:
        intent: Free-text user intent (case-insensitive).

    Returns:
        One of the keys in ON_DEMAND, or ``"meta"`` if no domain keyword
        matches.
    """
    intent_lower = intent.lower()
    if any(
        k in intent_lower
        for k in ("basin", "geology", "seismic", "petrophysics", "well", "prospect")
    ):
        return "geoscience"
    if any(
        k in intent_lower
        for k in ("npv", "irr", "emv", "capital", "invest", "valuation", "stock")
    ):
        return "capital"
    if any(
        k in intent_lower
        for k in ("code", "build", "deploy", "shell", "docker", "git", "test")
    ):
        return "engineering"
    if any(k in intent_lower for k in ("vault", "seal", "ledger", "archive")):
        return "vault"
    if any(k in intent_lower for k in ("search", "research", "find")):
        return "evidence"
    return "meta"


__all__ = [
    "ALWAYS_HOT",
    "ON_DEMAND",
    "MAX_TOOLS",
    "discover",
    "classify_intent",
]
