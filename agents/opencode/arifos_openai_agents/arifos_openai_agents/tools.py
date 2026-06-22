"""
tools.py — The prethink tool definition.

This is the ONE tool that MUST be called before any other tool.
It forces the agent to declare its cognition lane (OBSERVE/PLAN/MUTATE/EXECUTE)
and receive the kernel's verdict before proceeding.

In OpenAI's Responses API, this is enforced via `tool_choice="required"`
on the prethink tool. The agent cannot proceed without calling it.

This is the Band 1 cognition firewall.
"""

from __future__ import annotations

from typing import Any

# The prethink tool schema. This is what the model sees.
# It must be the FIRST tool called for any cognition that may lead to action.
ARIFOS_PRETHINK_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "_arifos_prethink",
        "description": (
            "MANDATORY cognition-time gate. MUST be called before any "
            "other tool. Declares the agent's intent (OBSERVE/PLAN/MUTATE/EXECUTE) "
            "and proposed action. Returns the kernel's verdict (ALLOW/DENY/HOLD/DEGRADED) "
            "and the allowed cognition lane. The agent must not proceed without "
            "verdict=ALLOW or DEGRADED."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "intent_summary": {
                    "type": "string",
                    "description": (
                        "One-sentence description of what the agent intends to do."
                    ),
                },
                "proposed_lane": {
                    "type": "string",
                    "enum": ["OBSERVE", "PLAN", "MUTATE", "EXECUTE"],
                    "description": (
                        "The agent's self-classified cognition lane. OBSERVE=read-only, "
                        "PLAN=reasoning, MUTATE=local state change, EXECUTE=cross-system action."
                    ),
                },
                "proposed_action_class": {
                    "type": "string",
                    "enum": [
                        "OBSERVE", "COMPUTE", "PROPOSE",
                        "MUTATE_LOCAL", "MUTATE_EXTERNAL",
                        "DEPLOY", "SPEND", "PUBLISH", "DELETE",
                        "SIGN", "GRANT_ACCESS",
                        "CREDENTIAL_CHANGE", "CONSTITUTION_CHANGE",
                    ],
                    "description": (
                        "The action class the agent is about to take. Maps to "
                        "F1-F13 floor checks."
                    ),
                },
                "estimated_blast_radius": {
                    "type": "string",
                    "enum": ["NONE", "LOCAL", "SESSION", "FEDERATION", "EXTERNAL"],
                    "description": "How far the action's effects propagate.",
                },
                "proposed_tools": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "List of tool names the agent intends to call after prethink. "
                        "Used by the kernel to compute aggregate blast-radius."
                    ),
                },
            },
            "required": [
                "intent_summary",
                "proposed_lane",
                "proposed_action_class",
                "estimated_blast_radius",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    },
}


# Verdict semantics, for documentation and tool-search metadata
VERDICT_SEMANTICS: dict[str, str] = {
    "ALLOW": "Proceed. Decision is sealed.",
    "DENY": "Block. Do not proceed. Floor failure.",
    "HOLD": "Pause. Request human authority (888 HOLD).",
    "DEGRADED": "Proceed with warnings. Attach to seal.",
}
