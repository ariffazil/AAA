#!/usr/bin/env python3
"""
bot_template_enforcement — Drop-in module for OpenClaw's bot.py

Purpose: enforce the F1-F13 message template at the bot layer, NOT just
in the prompt. This is the difference between "the model is told to use
the template" (prompt-level, can be ignored) and "the model cannot emit
a message that violates the template" (code-level, enforced).

The bot (e.g., /root/.openclaw/workspace/bots/opencode-bot/bot.py) should
import this module and call `enforce_template(response_text, organ)` before
sending any reply. If the response does not match the template, the bot
should:
  - For LIBRA, HERMES, CLAW: HOLD the response. Log the violation. Ask the
    model to regenerate with the template.
  - For FORGE: refuse to execute. A malformed response from FORGE is a
    fail-closed signal.

Anti-Universe-25 rule: no "I'll just send it anyway" fallback. The
template is the protocol. The protocol is the law.

This module is wired into bot.py by:
  1. Adding `import bot_template_enforcement` at the top.
  2. Calling `enforce_template(response, organ)` before `update.message.reply_text(...)`.
  3. On violation: send a HOLD message and log to VAULT999.

The exact pattern (pseudo):

    response = await call_opencode(...)
    result = enforce_template(response, organ="HERMES")
    if not result["valid"]:
        await update.message.reply_text(
            f"888_HOLD: response violated F1-F13 template. Reason: {result['reason']}"
        )
        log_violation(result)
        return
    await update.message.reply_text(response)
"""

import re
from typing import Dict, Optional

# Compact template pattern (from AAA_TRINITY_PROTOCOL.md and the per-organ prompt files).
# Required header: "<NAME> | Mode: <...> | Floors: F1[, F#, F#]"
# Required footer: "DITEMPA BUKAN DIBERI"
# Optional middle: CLAIM/PLAUSIBLE/HYPOTHESIS/UNKNOWN/888_HOLD sections.

HEADER_PATTERN = re.compile(
    r"^(LIBRA♎|HERMES~|CLAW\+|FORGE0)\s*\|\s*Mode:\s*\S+(\s*\|\s*Floors?:\s*F[\d,\s]+)?",
    re.MULTILINE,
)
FOOTER_PATTERN = re.compile(r"DITEMPA BUKAN DIBERI\s*$", re.MULTILINE)
DANGEROUS_TERMS_PATTERN = re.compile(
    r"\b(I am conscious|I have feelings|I am sentient|"
    r"trust me, no SEAL needed|"
    r"definitely safe|"
    r"just this once)\b",
    re.IGNORECASE,
)


def enforce_template(response: str, organ: str) -> Dict[str, object]:
    """Validate that a response matches the F1-F13 template for the given organ.

    Returns: {
      "valid": bool,
      "reason": str (empty if valid),
      "organ": str,
      "issues": list[str] (empty if valid),
    }
    """
    issues: list[str] = []
    if not response or not response.strip():
        return {
            "valid": False,
            "reason": "empty response",
            "organ": organ,
            "issues": ["response is empty"],
        }

    if not HEADER_PATTERN.search(response):
        issues.append(
            f"missing or malformed header — must start with "
            f"{organ} | Mode: <...> | Floors: F<#>"
        )

    if not FOOTER_PATTERN.search(response):
        issues.append(
            "missing or malformed footer — must end with 'DITEMPA BUKAN DIBERI'"
        )

    if DANGEROUS_TERMS_PATTERN.search(response):
        issues.append("contains a F9 ANTIHANTU or F1 AMANAH violation term")

    if organ == "FORGE":
        # FORGE responses must include a verdict line.
        if not re.search(
            r"VERDICT:\s*<(EXECUTED|REJECTED|DIFF_RETURNED|ROLLED_BACK|HELD)>", response
        ):
            issues.append("FORGE response missing required VERDICT line")

    if organ == "HERMES":
        # HERMES responses must include a verdict.
        if not re.search(r"VERDICT:\s*<(HOLD|VOID|DEMAND_SEAL|INFO|SEAL)>", response):
            issues.append("HERMES response missing required VERDICT line")

    valid = len(issues) == 0
    return {
        "valid": valid,
        "reason": ("; ".join(issues)) if issues else "",
        "organ": organ,
        "issues": issues,
    }


def on_violation(organ: str, reason: str, user_message_id: Optional[int] = None) -> str:
    """Build the HOLD message to send to Telegram when a template is violated."""
    return (
        f"888_HOLD: {organ} response violated the F1-F13 template.\n"
        f"  reason: {reason}\n"
        f"  The response was NOT sent. The model will regenerate.\n"
        f"  This is enforced at the bot layer (not just the prompt).\n"
        f"DITEMPA BUKAN DIBERI"
    )


# CLI mode for testing
if __name__ == "__main__":
    import json
    import sys

    if len(sys.argv) < 3:
        print("usage: bot_template_enforcement.py <organ> <response>", file=sys.stderr)
        sys.exit(1)

    organ_arg = sys.argv[1]
    response_arg = sys.argv[2]
    result = enforce_template(response_arg, organ_arg)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["valid"] else 1)
