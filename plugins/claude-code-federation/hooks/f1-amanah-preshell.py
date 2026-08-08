#!/usr/bin/env python3
"""
F1 AMANAH — PreToolUse Hook for Claude Code
============================================
Constitutional governance: snapshot before mutation.

This hook fires BEFORE Bash, Edit, and Write tool calls.
It ensures F1 AMANAH compliance:
  1. For destructive Bash commands (rm, mv, chmod, chown) — WARN + confirm
  2. For all Write/Edit — track file paths for post-tool audit
  3. For all mutations — ensure session is bound to kernel

Part of the arifos-federation Claude Code plugin.
DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import os
import re
import sys
import time
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────
# Patterns that require warning before execution
DESTRUCTIVE_PATTERNS = [
    (r"rm\s+-rf?\s+/(?!tmp/)", "BLOCK", "Recursive delete on root-protected path"),
    (r"rm\s+-rf?\s+", "WARN", "Recursive delete — verify path before proceeding"),
    (r">\s*/dev/", "WARN", "Writing to device file — verify target"),
    (r"dd\s+if=", "WARN", "Disk duplication — verify source and target"),
    (r"mkfs\.", "BLOCK", "Filesystem formatting — requires sovereign approval"),
    (r"chmod\s+777", "WARN", "World-writable permissions — security risk"),
    (r"chown\s+-R\s+", "WARN", "Recursive ownership change — verify scope"),
    (r"shutdown|reboot|poweroff|init\s+[06]", "BLOCK", "System power control — requires sovereign approval"),
    (r"iptables|nft\s+", "BLOCK", "Firewall mutation — requires sovereign approval"),
    (r"git\s+push\s+--force.*main", "BLOCK", "Force push to main — requires sovereign approval"),
]

# Session state file (written by arif_init)
SESSION_STATE = "/tmp/opencode/session_state.json"

# ── Helpers ────────────────────────────────────────────────────────────


def load_session() -> dict:
    """Load session state if available."""
    try:
        with open(SESSION_STATE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def check_destructive(command: str) -> list[dict]:
    """Check command against destructive patterns. Returns list of findings."""
    findings = []
    for pattern, action, reason in DESTRUCTIVE_PATTERNS:
        if re.search(pattern, command):
            findings.append({"pattern": pattern, "action": action, "reason": reason})
    return findings


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f'{{"systemMessage": "F1 AMANAH hook: Invalid JSON: {e}"}}')
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # ── Only act on mutable tools ───────────────────────────────────────
    if tool_name not in ("Bash", "Edit", "Write", "MultiEdit"):
        print("{}")
        sys.exit(0)

    # ── Check session binding ─────────────────────────────────────────
    session = load_session()
    if not session.get("session_id"):
        if tool_name in ("Edit", "Write", "MultiEdit"):
            print(
                json.dumps(
                    {
                        "hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny"},
                        "systemMessage": (
                            "**[F1 AMANAH — SESSION UNBOUND]**\n"
                            "No active arifOS session found. Run `arif_init` before mutating files.\n"
                            f"Session state not found at {SESSION_STATE}."
                        ),
                    }
                )
            )
            sys.exit(0)

    # ── Bash: destructive command check ────────────────────────────────
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        findings = check_destructive(command)

        if not findings:
            print("{}")
            sys.exit(0)

        block_findings = [f for f in findings if f["action"] == "BLOCK"]
        warn_findings = [f for f in findings if f["action"] == "WARN"]

        if block_findings:
            reasons = "\n".join(f"  • `{f['pattern']}` — {f['reason']}" for f in block_findings)
            print(
                json.dumps(
                    {
                        "hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny"},
                        "systemMessage": (
                            f"**[F1 AMANAH — BLOCKED]**\n"
                            f"This command matches blocked patterns:\n{reasons}\n\n"
                            f"**Required:** Sovereign approval (F13) before proceeding.\n"
                            f"Session: `{session.get('session_id', 'unbound')}`"
                        ),
                    }
                )
            )
            sys.exit(0)

        if warn_findings:
            reasons = "\n".join(f"  • `{f['pattern']}` — {f['reason']}" for f in warn_findings)
            print(
                json.dumps(
                    {
                        "systemMessage": (
                            f"**[F1 AMANAH — WARNING]**\n"
                            f"Destructive patterns detected:\n{reasons}\n\n"
                            f"Command: `{command[:200]}`\n"
                            f"Verify the path is correct. Consider `--dry-run` first.\n"
                            f"Session: `{session.get('session_id', 'unbound')}`"
                        )
                    }
                )
            )
            sys.exit(0)

    # ── Write/Edit: track for audit ────────────────────────────────────
    if tool_name in ("Edit", "Write", "MultiEdit"):
        file_path = tool_input.get("file_path", "")
        if file_path:
            # Record for F11 post-tool audit
            audit_line = json.dumps(
                {
                    "ts": time.time(),
                    "session": session.get("session_id", "unbound"),
                    "tool": tool_name,
                    "path": file_path,
                    "event": "PreToolUse",
                }
            )
            try:
                with open("/root/.claude/hooks/f1-gate.log", "a") as f:
                    f.write(audit_line + "\n")
            except (IOError, PermissionError):
                pass  # Non-fatal — audit best-effort

    # ── Default: allow ──────────────────────────────────────────────────
    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
