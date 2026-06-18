#!/usr/bin/env python3
"""AAA THERMO-PRE — Projected entropy estimator before action."""
from __future__ import annotations

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

    file_path = ""
    content = ""
    command = ""
    if tool_name == "WriteFile":
        file_path = h.extract_file_path(tool_input)
        content = tool_input.get("content", "")
    elif tool_name == "StrReplaceFile":
        file_path = h.extract_file_path(tool_input)
        content = tool_input.get("new", "")
    elif tool_name == "Shell":
        command = h.extract_command(tool_input)

    # Component scores
    f_score = 0.0
    d_score = 0.0
    c_score = 0.0
    k_score = 0.0
    r_score = 0.0

    if file_path:
        f_score = 0.15
        if re.search(r"import\s+.*from|require\(|from\s+.*import", content):
            f_score = 0.25
    elif tool_name == "Shell" and command:
        file_refs = set(re.findall(r"\S+\.\w+", command))
        if len(file_refs) > 5:
            f_score = 0.60
        elif len(file_refs) > 2:
            f_score = 0.35
        else:
            f_score = 0.20
        if re.search(r"find.*-exec|xargs|sed\s+-i.*;.*;|for\s+.*in\s+.*do", command, re.IGNORECASE):
            f_score = 0.80

    # Directory spread
    text = f"{cwd} {file_path} {command}"
    domains = [d for d in ("arifOS", "A-FORGE", "A_FORGE", "geox", "GEOX", "WEALTH", "WELL", "compose", "deployments") if re.search(rf"(?:^|/){re.escape(d)}(/|$)", text)]
    unique = len(set(d.lower().replace("_", "-") for d in domains))
    if unique > 2:
        d_score = 0.80
    elif unique == 2:
        d_score = 0.45
    elif unique == 1:
        d_score = 0.15
    else:
        d_score = 0.10

    # Churn
    if content:
        lines = content.count("\n") + 1
        if lines > 200:
            c_score = 0.70
        elif lines > 50:
            c_score = 0.40
        else:
            c_score = 0.15
    elif tool_name == "Shell" and command:
        if re.search(r"migration|refactor|rewrite|restructure", command, re.IGNORECASE):
            c_score = 0.75
        elif len(command) > 200:
            c_score = 0.40
        else:
            c_score = 0.15

    # Canonical risk
    if file_path and (h.is_tier_a(file_path) or h.is_constitutional(file_path)):
        k_score = 0.70
    elif tool_name == "Shell" and command and (h.is_tier_a(command) or h.is_constitutional(command)):
        k_score = 0.50
    else:
        k_score = 0.05

    # Reversibility
    if tool_name == "Shell" and command:
        if re.search(
            r"rm\s+-rf|docker\s+system\s+prune|git\s+push|git\s+reset\s+--hard|git\s+clean|DROP\s+TABLE|DELETE\s+FROM",
            command,
            re.IGNORECASE,
        ):
            r_score = 0.90
        elif re.search(r"git\s+rebase|git\s+merge|docker\s+build.*--no-cache", command, re.IGNORECASE):
            r_score = 0.50
        else:
            r_score = 0.10
    else:
        if file_path and Path(file_path).exists():
            r_score = 0.05
        else:
            r_score = 0.15

    delta_s = h.compute_delta_pre(f_score, d_score, c_score, k_score, r_score)
    band, hold_rec, epistemic = h.chaos_band(delta_s)

    suggestions: list[str] = []
    if f_score > 0.4:
        suggestions.append("Reduce touched files — consider narrower scope")
    if d_score > 0.3:
        suggestions.append("One domain at a time — separate constitutional, runtime, and UI changes")
    if c_score > 0.4:
        suggestions.append("Large churn detected — split into coherent slices, batch formatting separately")
    if k_score > 0.3:
        suggestions.append("Canonical file touched — verify deployment manifest coherence before proceeding")
    if r_score > 0.3:
        suggestions.append("Low reversibility — generate rollback note or backup before execution")
    if not suggestions:
        suggestions.append("Local coherent change — proceed with confidence")

    h.audit_log(
        {
            "type": "opencode-thermo-pre",
            "timestamp": h.now_utc(),
            "session_id": session_id,
            "hook_event": hook_event,
            "tool_name": tool_name,
            "deltaS_projected": delta_s,
            "chaos_band": band,
            "hold_recommended": hold_rec,
            "epistemic_tag": epistemic,
            "components": {"f": f_score, "d": d_score, "c": c_score, "k": k_score, "r": r_score},
            "suggestions": suggestions,
        }
    )

    reason = f"[{epistemic}] Thermodynamic advisory: projected ΔS={delta_s} ({band})."
    if suggestions:
        reason += " | " + " | ".join(suggestions)
    if hold_rec:
        reason += " | 888 HOLD recommended but NOT enforced."

    h.allow(
        hook_event,
        reason,
        {
            "epistemic_tag": epistemic,
            "deltaS_projected": delta_s,
            "chaos_band": band,
            "reversibility": round(1.0 - r_score, 2),
            "hold_recommended": hold_rec,
            "components": {
                "F_files": f_score,
                "D_spread": d_score,
                "C_churn": c_score,
                "K_canonical": k_score,
                "R_irreversibility": r_score,
            },
            "lower_entropy_plan": suggestions,
        },
    )


if __name__ == "__main__":
    main()
