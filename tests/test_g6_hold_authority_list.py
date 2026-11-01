#!/usr/bin/env python3
"""G6 — HOLD_AUTHORITY list in the agent boot canon (HUMAN_RASA P0 REMEDIATION).

Gap: session connectors (Gmail send_message/forward/reply, Drive share_file,
Calendar create_event with attendees) reach outside the conversation and bypass
arifOS + A-FORGE gates. The agent instruction canon must name them and state
the hold rule.

Docs-only static check: the list exists in the boot-loaded canon and names each
tool. No runtime gate is added or weakened by this test.
"""

from pathlib import Path

# The file agents load at boot (project context injected at session start).
BOOT_CANON = Path(__file__).resolve().parent.parent / "AGENTS.md"

REQUIRED_SUBSTRINGS = [
    # the list heading
    "HOLD_AUTHORITY",
    # surfaces
    "Gmail",
    "Drive",
    "Calendar",
    # Gmail tools
    "send_message",
    "forward",
    "reply",
    # Drive tools
    "share_file",
    # Calendar tools
    "create_event",
    # the rule itself
    "current turn",
    "ARIF",
]

# Every tool the audit names must appear as an explicitly held tool.
REQUIRED_TOOLS = [
    "send_message",
    "forward",
    "reply",
    "share_file",
    "create_event",
]


def test_boot_canon_exists():
    assert BOOT_CANON.is_file(), f"boot canon missing: {BOOT_CANON}"


def test_hold_authority_list_present():
    text = BOOT_CANON.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SUBSTRINGS if s not in text]
    assert not missing, f"{BOOT_CANON} is missing HOLD_AUTHORITY content: {missing}"


def test_each_connector_tool_named():
    text = BOOT_CANON.read_text(encoding="utf-8")
    # Scope the check to the HOLD_AUTHORITY section so unrelated prose cannot
    # accidentally satisfy it.
    start = text.find("HOLD_AUTHORITY")
    assert start != -1, "HOLD_AUTHORITY section not found"
    section = text[start : start + 4000]
    missing = [t for t in REQUIRED_TOOLS if t not in section]
    assert not missing, f"HOLD_AUTHORITY section does not name: {missing}"


def test_rule_requires_per_action_instruction_in_current_turn():
    text = BOOT_CANON.read_text(encoding="utf-8")
    start = text.find("HOLD_AUTHORITY")
    section = text[start : start + 4000]
    assert "per-action" in section, "must require a per-action instruction"
    assert "current turn" in section, "must bind the instruction to the current turn"
