#!/usr/bin/env python3
"""AAA POST-WITNESS — Verify state delta, log audit event, never block."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    tool_name = event.get("tool_name", "unknown")
    tool_input = event.get("tool_input", {})
    tool_output = event.get("tool_output", {})
    session_id = event.get("session_id", "unknown")
    hook_event = event.get("hook_event_name", "PostToolUse")

    file_path = h.extract_file_path(tool_input) if tool_name in ("WriteFile", "StrReplaceFile") else ""

    file_hash = ""
    file_size = ""
    git_diff = ""
    tier_a_touch = False
    constitutional_touch = False

    if file_path and Path(file_path).exists():
        file_size = str(Path(file_path).stat().st_size)
        file_hash = h.sha256_file(file_path)
        git_diff = h.git_diff_stat(file_path)
        tier_a_touch = h.is_tier_a(file_path)
        constitutional_touch = h.is_constitutional(file_path)

    h.audit_log(
        {
            "type": "opencode-post-witness",
            "timestamp": h.now_utc(),
            "session_id": session_id,
            "hook_event": hook_event,
            "tool_name": tool_name,
            "file_path": file_path,
            "file_hash": file_hash,
            "file_size_bytes": file_size,
            "git_diff_summary": git_diff,
            "tier_a_touch": tier_a_touch,
            "constitutional_touch": constitutional_touch,
        }
    )

    reason = "[CLAIM] AAA PostToolUse: state delta witnessed."
    if tier_a_touch:
        reason += " Tier A file modified — verify deployment manifests still coherent."
    if constitutional_touch:
        reason += " Constitutional file modified — doctrine drift risk. Consider F10 migration audit."
    if git_diff:
        reason += f" Git delta: {git_diff}"

    h.allow(
        hook_event,
        reason,
        {
            "file_path": file_path,
            "file_hash": file_hash,
            "tier_a_touch": tier_a_touch,
            "constitutional_touch": constitutional_touch,
            "audit_logged": True,
        },
    )


if __name__ == "__main__":
    main()
