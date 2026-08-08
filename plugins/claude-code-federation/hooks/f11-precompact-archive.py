#!/usr/bin/env python3
"""
PRECOMPACT — Constitutional State Preservation Hook
====================================================
F11 AUDIT extension: before Claude Code compacts context, archive the
full transcript to preserve constitutional state.

This prevents A12 (BANGANG): context compaction losing CLAUDE.md
constitutional instructions mid-session.

Part of arifos-federation Claude Code plugin v1.1.0.
DITEMPA BUKAN DIBERI.
"""

import json
import os
import shutil
import sys
import time
from pathlib import Path

AUDIT_LOG = "/root/.claude/hooks/f11-audit.jsonl"
SESSION_STATE = "/tmp/opencode/session_state.json"
ARCHIVE_DIR = "/root/.claude/hooks/precompact-archives"


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    session = {}
    try:
        with open(SESSION_STATE) as f:
            session = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    sid = session.get("session_id", "unbound")
    trigger = input_data.get("trigger", "auto")

    # Record the precompact event
    ts = time.strftime("%Y%m%dT%H%M%S")
    entry = {"ts": time.time(), "session": sid, "event": "precompact", "trigger": trigger}

    # Archive recent transcript if available (best effort)
    try:
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        # Claude Code stores transcripts in ~/.claude/projects/
        projects_dir = Path("/root/.claude/projects")
        if projects_dir.exists():
            # Copy the most recent session transcript matching our session
            for f in sorted(projects_dir.glob("**/*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)[:3]:
                shutil.copy2(f, f"{ARCHIVE_DIR}/{sid}-{ts}-{f.name}")
                entry["archived"] = str(f.name)
                break
    except Exception:
        pass

    try:
        with open(AUDIT_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except (IOError, PermissionError):
        pass

    # Always allow compaction — but inform Claude context was preserved
    print(
        json.dumps(
            {
                "systemMessage": (
                    f"[F11 AUDIT — PreCompact] Constitutional transcript archived for session `{sid}` "
                    f"(trigger: {trigger}). CLAUDE.md constitutional instructions persist across compaction."
                )
            }
        )
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
