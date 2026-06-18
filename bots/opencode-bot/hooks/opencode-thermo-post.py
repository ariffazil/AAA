#!/usr/bin/env python3
"""AAA THERMO-POST — Realized entropy from git state."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import hook_lib as h


def main() -> None:
    event = h.read_event()
    tool_name = event.get("tool_name", "unknown")
    tool_input = event.get("tool_input", {})
    file_path = h.extract_file_path(tool_input) if tool_name in ("WriteFile", "StrReplaceFile") else ""
    session_id = event.get("session_id", "unknown")
    hook_event = event.get("hook_event_name", "PostToolUse")

    files_changed = 0
    dirs_changed = 0
    lines_added = 0
    lines_deleted = 0
    cross_domain = False
    rollback_detected = False

    for repo_path in ("/root/arifOS", "/root/A-FORGE", "/root/geox", "/root/WEALTH"):
        p = Path(repo_path) / ".git"
        if not p.exists():
            continue
        try:
            result = subprocess.run(
                ["git", "diff", "--numstat"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.stdout:
                for line in result.stdout.strip().splitlines():
                    parts = line.split("\t")
                    if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
                        lines_added += int(parts[0])
                        lines_deleted += int(parts[1])
                        files_changed += 1
                        dirs_changed += 1  # simplified
        except Exception:
            pass

    if files_changed == 0 and file_path and Path(file_path).exists():
        files_changed = 1
        dirs_changed = 1
        size = Path(file_path).stat().st_size
        lines_added = size // 40
        lines_deleted = 0

    domains_hit = []
    for repo in ("arifOS", "A-FORGE", "geox", "WEALTH", "WELL"):
        p = Path(f"/root/{repo}/.git")
        if not p.exists():
            continue
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                cwd=f"/root/{repo}",
                capture_output=True,
                text=True,
                timeout=3,
            )
            if result.stdout.strip():
                domains_hit.append(repo)
        except Exception:
            pass
    if len(domains_hit) > 1:
        cross_domain = True

    # Rollback detection
    rollback_count = 0
    try:
        result = subprocess.run(
            ["git", "stash", "list"], capture_output=True, text=True, timeout=3
        )
        if result.stdout.strip():
            rollback_detected = True
    except Exception:
        pass

    f_r = min(1.0, files_changed / 10.0)
    d_r = min(1.0, dirs_changed / 5.0)
    churn = lines_added + lines_deleted
    c_r = min(1.0, churn / 200.0)
    k_r = 0.60 if file_path and (h.is_tier_a(file_path) or h.is_constitutional(file_path)) else 0.05
    r_r = 0.10
    if not rollback_detected and files_changed > 3:
        r_r = 0.40
    elif not rollback_detected and cross_domain:
        r_r = 0.60

    delta_s = round(0.25 * f_r + 0.20 * d_r + 0.25 * c_r + 0.20 * k_r + 0.10 * r_r, 4)
    band, _, epistemic = h.chaos_band(delta_s)

    if band == "red":
        next_action = "Immediate consolidation commit or split-by-domain refactor recommended"
    elif band == "orange":
        next_action = "Consider narrowing scope or staging formatting separately"
    elif cross_domain:
        next_action = "Cross-domain changes detected — prefer domain-scoped commits"
    elif not rollback_detected and files_changed > 2:
        next_action = "Generate rollback artifact (git stash or backup) for safety"
    else:
        next_action = "Proceed with confidence"

    h.audit_log(
        {
            "type": "opencode-thermo-post",
            "timestamp": h.now_utc(),
            "session_id": session_id,
            "hook_event": hook_event,
            "tool_name": tool_name,
            "deltaS_realized": delta_s,
            "chaos_band": band,
            "files_changed": files_changed,
            "dirs_changed": dirs_changed,
            "lines_added": lines_added,
            "lines_deleted": lines_deleted,
            "cross_domain": cross_domain,
            "rollback_detected": rollback_detected,
            "next_best_action": next_action,
        }
    )

    reason = f"[{epistemic}] Witness: realized ΔS={delta_s} ({band}). {files_changed} files, {dirs_changed} dirs, {churn} lines."
    if cross_domain:
        reason += f" Cross-domain: {' '.join(domains_hit)}."
    if not rollback_detected:
        reason += " No rollback artifact detected."
    reason += f" Next: {next_action}"

    h.allow(
        hook_event,
        reason,
        {
            "epistemic_tag": epistemic,
            "deltaS_realized": delta_s,
            "chaos_band": band,
            "files_changed": files_changed,
            "dirs_changed": dirs_changed,
            "lines_added": lines_added,
            "lines_deleted": lines_deleted,
            "cross_domain": cross_domain,
            "rollback_detected": rollback_detected,
            "next_best_action": next_action,
        },
    )


if __name__ == "__main__":
    main()
