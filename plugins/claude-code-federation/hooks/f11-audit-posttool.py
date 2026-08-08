#!/usr/bin/env python3
"""
F11 AUDIT — PostToolUse Hook for Claude Code
==============================================
Constitutional governance: trace every action.

This hook fires AFTER all tool calls. It records:
  1. Tool name, execution time, and success/failure
  2. For mutations — writes to audit log
  3. For all tools — ingests into arifFlow (:7073) for FQ metabolism

Part of the arifos-federation Claude Code plugin.
DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

import json
import os
import sys
import time
import urllib.request
from pathlib import Path

# ── Configuration ──────────────────────────────────────────────────────
AUDIT_LOG = "/root/.claude/hooks/f11-audit.jsonl"
ARIFLOW_INGEST_URL = "http://127.0.0.1:7073/ingest"
SESSION_STATE = "/tmp/opencode/session_state.json"

MUTATING_TOOLS = {"Bash", "Edit", "Write", "MultiEdit"}
OBSERVE_TOOLS = {"Read", "Glob", "Grep", "WebSearch", "WebFetch"}


def load_session() -> dict:
    try:
        with open(SESSION_STATE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def ingest_to_arifflow(session_id: str, actor_id: str, tool_name: str):
    """Best-effort ingestion to arifFlow for FQ metabolism."""
    if tool_name in MUTATING_TOOLS:
        step_type = "Execute"
    elif tool_name in OBSERVE_TOOLS:
        step_type = "Verify"
    else:
        step_type = "Execute"

    payload = json.dumps(
        {
            "actor_id": actor_id or "claude-code/FI-002",
            "session_id": session_id or "unbound",
            "step_type": step_type,
            "epistemic_label": "Observation" if step_type == "Verify" else "Derivation",
            "floor_verdict": "Pass",
            "payload": {"tool": tool_name},
        }
    ).encode()

    try:
        req = urllib.request.Request(ARIFLOW_INGEST_URL, data=payload, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass  # Non-fatal — best effort


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    session = load_session()
    session_id = session.get("session_id", "unbound")

    # ── Record audit entry ─────────────────────────────────────────────
    entry = {
        "ts": time.time(),
        "iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "session": session_id,
        "tool": tool_name,
        "lane": session.get("lane", "?"),
        "profile": session.get("profile", "?"),
    }

    # Add tool-specific fields (truncated for log safety)
    if tool_name == "Bash":
        entry["command"] = tool_input.get("command", "")[:200]
    elif tool_name in ("Edit", "Write"):
        entry["path"] = tool_input.get("file_path", "")

    try:
        with open(AUDIT_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except (IOError, PermissionError):
        pass

    # ── Ingest to arifFlow ─────────────────────────────────────────────
    ingest_to_arifflow(session_id, "claude-code/FI-002", tool_name)

    # ── Always allow (audit is non-blocking) ───────────────────────────
    print("{}")
    sys.exit(0)


if __name__ == "__main__":
    main()
