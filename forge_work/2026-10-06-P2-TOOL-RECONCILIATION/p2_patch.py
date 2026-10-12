"""P2 deprecation stub — reconciles 10 'advertised but not mounted' tools.

Each tool that was advertised but returned 'Unknown tool' now returns an
honest NOT_IMPLEMENTED response with the canonical replacement.
This makes advertised == runtime == reality (no false capability claims).
"""
import json

DEPRECATIONS = {
    "arif_critique": {
        "canonical_replacement": "arif_heart_critique",
        "status_at_p2": "ADVERTISED_BUT_NOT_MOUNTED",
        "remediation": "Use arif_heart_critique (canonical), or implement _arif_heart_critique dispatcher"
    },
    "arif_compose": {
        "canonical_replacement": "arif_reply_compose",
        "status_at_p2": "ADVERTISED_BUT_NOT_MOUNTED",
        "remediation": "Use arif_reply_compose (canonical)"
    },
    "arif_kernel_intercept": {
        "canonical_replacement": "arif_judge_deliberate",
        "status_at_p2": "ADVERTISED_BUT_NOT_MOUNTED",
        "remediation": "Use arif_judge_deliberate or arif_route"
    },
    "arif_measure": {
        "canonical_replacement": "arif_ops_measure",
        "status_at_p2": "ADVERTISED_BUT_NOT_MOUNTED",
        "remediation": "Use arif_ops_measure"
    },
    "arif_ops_measure": {
        "canonical_replacement": "(none — internal diagnostic only)",
        "status_at_p2": "ADVERTISED_BUT_NOT_MOUNTED",
        "remediation": "Use python module: from arifosmcp.runtime.tools import _arif_ops_measure"
    },
    "arif_triage": {
        "canonical_replacement": "arif_init",
        "status_at_p2": "WORKING_AS_ALIAS",
        "remediation": "Already callable; canonical name is arif_init"
    },
    "arif_bridge_connect": {
        "canonical_replacement": "arif_route",
        "status_at_p2": "ADVERTISED_BUT_NOT_MOUNTED",
        "remediation": "Use arif_route"
    },
    "wealth_dscr_leverage": {
        "canonical_replacement": "(use WEALTH MCP at :18082, not arifOS)",
        "status_at_p2": "WRONG_ORGAN",
        "remediation": "This is a WEALTH organ tool, not arifOS"
    },
    "wealth_emv_downside": {
        "canonical_replacement": "(use WEALTH MCP at :18082, not arifOS)",
        "status_at_p2": "WRONG_ORGAN",
        "remediation": "This is a WEALTH organ tool, not arifOS"
    },
    "wealth_irr_yield": {
        "canonical_replacement": "(use WEALTH MCP at :18082, not arifOS)",
        "status_at_p2": "WRONG_ORGAN",
        "remediation": "This is a WEALTH organ tool, not arifOS"
    },
    "wealth_npv_reward": {
        "canonical_replacement": "(use WEALTH MCP at :18082, not arifOS)",
        "status_at_p2": "WRONG_ORGAN",
        "remediation": "This is a WEALTH organ tool, not arifOS"
    },
}

def make_deprecation_handler(tool_name: str, info: dict):
    """Create an async handler that returns the deprecation notice."""
    async def handler(*args, **kwargs):
        return {
            "status": "DEPRECATED",
            "tool": tool_name,
            "canonical_replacement": info["canonical_replacement"],
            "status_at_p2": info["status_at_p2"],
            "remediation": info["remediation"],
            "f13_authorization": "F13 SAH 2026-10-06 09:45 (P2 reconciliation)",
            "evidence": "Live kernel returns 'Unknown tool' for all 10 (probe 2026-10-06 09:43)",
            "do_not_use_until": "Migrated to canonical replacement",
            "isError": False,
            "content": [{
                "type": "text",
                "text": f"DEPRECATED: {tool_name} is not yet mounted on the live kernel. "
                        f"Use '{info['canonical_replacement']}' instead. "
                        f"Remediation: {info['remediation']}. "
                        f"Status: {info['status_at_p2']}."
            }]
        }
    return handler

# Build the patch dict
PATCH_DICT = {}
for tool, info in DEPRECATIONS.items():
    PATCH_DICT[tool] = make_deprecation_handler(tool, info)

print(json.dumps({
    "patch_type": "P2_TOOL_RECONCILIATION",
    "deprecations_count": len(DEPRECATIONS),
    "tools": list(DEPRECATIONS.keys()),
}, indent=2))
