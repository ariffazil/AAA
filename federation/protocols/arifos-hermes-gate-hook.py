#!/usr/bin/env python3
"""
arifos-hermes-gate-hook.py
Hermes pre_tool_call shell hook — K-02 enforcement pattern.

Wire protocol (per Hermes shell_hooks.py doc):
  stdin:  JSON with hook_event_name, tool_name, tool_input, session_id
  stdout: JSON {"decision": "block", "reason": "..."} to deny

Pattern: Detect → Classify → Decide → Receipt → Deny (or Allow).

This is the FIRST runtime enforcement path in Hermes.
K-02 transition: Witness → Enforcer.
"""
import json
import sys
import os
import re
from datetime import datetime

RECEIPT_PATH = "/root/.local/share/arifos/hermes_hook_receipts.jsonl"

# T3 patterns — same as OpenCode gate (E-12: capability beats instruction)
T3_PATTERNS = [
    r"secrets?[/\\]",
    r"kunci-mas",
    r"vault\.env",
    r"\.signing_key",
    r"tokenrouter",
    r"systemctl\s+(restart|stop|disable)",
    r"VAULT999/outcomes\.jsonl",
    r"chattr\s+-i",  # removing append-only from vault
    r"rm\s+-rf\s+/root",
    r"dd\s+if=.+of=/dev/(sd|nvme)",
    r"mkfs\.",
    r"git\s+push\s+.*--force.*\s+(main|master)",
    r"DROP\s+(TABLE|DATABASE)",
]

# T2 mutation tools
T2_TOOLS = {"write_file", "patch", "terminal", "cronjob", "delegate_task",
            "plugin", "skill_manage", "execute_code"}

def classify(tool_name: str, tool_input: dict) -> str:
    """Return 'OBSERVE', 'T1', 'T2', or 'T3'."""
    if tool_name in {"read_file", "search_files", "web_search", "web_extract",
                     "vision_analyze", "session_search", "skills_list",
                     "skills_view", "memory", "todo", "text_to_speech",
                     "clarify", "browser_snapshot", "browser_click",
                     "browser_type", "browser_navigate", "browser_console",
                     "browser_vision", "browser_back", "browser_scroll",
                     "browser_press", "skill_view", "tools_list"}:
        return "OBSERVE"
    if tool_name in T2_TOOLS:
        # Check T3 first (highest priority)
        arg_str = json.dumps(tool_input).lower()
        for p in T3_PATTERNS:
            if re.search(p, arg_str, re.IGNORECASE):
                return "T3"
        return "T2"
    # Unknown tool → T2 (fail-closed to judgment, not auto-execute)
    return "T2"

def write_receipt(tool_name: str, classification: str, decision: str, reason: str = ""):
    """Append to gate receipt trail. Never block on failure (E-11)."""
    try:
        os.makedirs(os.path.dirname(RECEIPT_PATH), exist_ok=True)
        with open(RECEIPT_PATH, "a") as f:
            f.write(json.dumps({
                "event": f"hermes-gate.{decision.lower()}",
                "tool": tool_name,
                "classification": classification,
                "reason": reason,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "k02_transition": True,  # First runtime enforcement
            }) + "\n")
    except Exception:
        pass  # Never block

def main():
    try:
        raw = sys.stdin.read()
        if not raw:
            return  # No input → no-op
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return

    tool_name = payload.get("tool_name", "unknown")
    tool_input = payload.get("tool_input", {})
    session_id = payload.get("session_id", "unknown")

    classification = classify(tool_name, tool_input)

    if classification == "OBSERVE":
        return  # Passthrough — no output = allow

    if classification == "T3":
        # T3 ALWAYS DENY at gate level (defer to arif_judge if available)
        reason = f"T3 pattern detected in '{tool_name}' args"
        write_receipt(tool_name, classification, "BLOCKED", reason)
        # Output the block decision
        result = {
            "decision": "block",
            "reason": f"🚫 K-02 GATE BLOCKED: {reason}. T3 actions require arif_judge SEAL. Session: {session_id[:16]}",
        }
        print(json.dumps(result))
        sys.exit(2)  # Exit 2 = constitutional block

    # T2 — log witness receipt, allow (K-02 transition: witness → enforcer for T3 only)
    write_receipt(tool_name, classification, "WITNESSED", f"T2 mutation witnessed for {tool_name}")
    # Allow (no output)

if __name__ == "__main__":
    main()