#!/usr/bin/env python3
"""AAA PRE-GOVERN — Constitutional PreToolUse gate for opencode-bot."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    tool_name = event.get("tool_name", "unknown")
    tool_input = event.get("tool_input", {})
    cwd = event.get("cwd", "/root")
    session_id = event.get("session_id", "unknown")
    hook_event = event.get("hook_event_name", "PreToolUse")

    command = h.extract_command(tool_input) if tool_name == "Shell" else ""
    file_path = h.extract_file_path(tool_input) if tool_name in ("WriteFile", "StrReplaceFile") else ""

    risk_class = "low"
    reversibility = "yes"
    scope = "local"
    repo = h.detect_repo(f"{cwd} {file_path} {command}")
    hold_recommended = False
    block = False
    block_reason = ""
    warnings: list[str] = []

    # Cross-repo detection
    repos = h.unique_repos(f"{cwd} {file_path} {command}")
    if len(repos) > 1:
        scope = "cross-repo"
        warnings.append("Cross-repo boundary touch detected")
        risk_class = "high"
        hold_recommended = True

    # Shell risk patterns
    if tool_name == "Shell" and command:
        destructive = re.compile(
            r"rm\s+-rf\s+/|docker\s+system\s+prune\s+-a|docker\s+volume\s+prune|"
            r"dd\s+if=|mkfs\.|shutil\.rmtree|os\.remove\s*\("
        )
        if destructive.search(command):
            risk_class = "irreversible"
            reversibility = "no"
            hold_recommended = True
            block = True
            block_reason = "Irreversible destructive pattern detected"
            warnings.append(block_reason)
        elif re.search(
            r"systemctl\s+(stop|restart|disable)\s|curl\s+.*\|\s*(ba)?sh|wget\s+.*\|\s*(ba)?sh",
            command,
            re.IGNORECASE,
        ):
            risk_class = "irreversible"
            reversibility = "no"
            hold_recommended = True
            block = True
            block_reason = "System service mutation or pipe-to-shell detected"
            warnings.append(block_reason)
        elif re.search(
            r"git\s+push|git\s+reset\s+--hard|git\s+rebase|docker\s+build.*--no-cache",
            command,
            re.IGNORECASE,
        ):
            risk_class = "high"
            reversibility = "partial"
            hold_recommended = True
            warnings.append("High-risk git/docker operation")
        elif re.search(
            r"pip\s+install|npm\s+install|apt\s+install|uv\s+add", command, re.IGNORECASE
        ):
            risk_class = "medium"
            reversibility = "yes"
            warnings.append("Dependency mutation — consider rollback manifest")

    # File write risk
    if tool_name in ("WriteFile", "StrReplaceFile") and file_path:
        if h.is_tier_a(file_path):
            risk_class = "high"
            reversibility = "partial"
            hold_recommended = True
            warnings.append("Tier A canonical file touched")
        if file_path.lower().endswith((".env", ".env.local", ".env.production")):
            risk_class = "high"
            hold_recommended = True
            warnings.append("Sensitive file write — ensure .gitignore and secret hygiene")
        if h.is_constitutional(file_path):
            risk_class = "high"
            hold_recommended = True
            warnings.append("Constitutional law file modified — doctrine drift risk")

    # Tool-economy guard
    call_count = 0
    try:
        if h.AUDIT_LOG.exists():
            with h.AUDIT_LOG.open() as f:
                for line in f:
                    try:
                        rec = json.loads(line)
                        if (
                            rec.get("session_id") == session_id
                            and rec.get("tool_name") == "Shell"
                        ):
                            call_count += 1
                    except Exception:
                        pass
    except Exception:
        pass
    if tool_name == "Shell" and call_count >= 15:
        risk_class = "high"
        hold_recommended = True
        block = True
        block_reason = f"Tool-economy guard: {call_count} Shell calls in this session exceeds threshold"
        warnings.append(block_reason)

    reason = f"[CLAIM] AAA PreToolUse: risk={risk_class}, scope={scope}, repo={repo}, reversibility={reversibility}"
    if warnings:
        reason += " | WARNINGS: " + "; ".join(warnings)
    if hold_recommended and not block:
        reason += " | 888 HOLD recommended — agent may proceed only if no irreversible side effect."

    h.audit_log(
        {
            "type": "opencode-pre-govern",
            "timestamp": h.now_utc(),
            "session_id": session_id,
            "hook_event": hook_event,
            "tool_name": tool_name,
            "risk_class": risk_class,
            "repo_guess": repo,
            "scope_guess": scope,
            "reversibility": reversibility,
            "hold_recommended": hold_recommended,
            "blocked": block,
            "warnings": warnings,
        }
    )

    meta = {
        "risk_class": risk_class,
        "repo_guess": repo,
        "scope_guess": scope,
        "reversibility": reversibility,
        "hold_recommended": hold_recommended,
        "blocked": block,
        "block_reason": block_reason,
        "warnings": warnings,
    }

    if block:
        h.deny(hook_event, f"888_HOLD enforced: {block_reason}. {reason}", meta)
        sys.exit(2)
    else:
        h.allow(hook_event, reason, meta)
        sys.exit(0)


if __name__ == "__main__":
    main()
