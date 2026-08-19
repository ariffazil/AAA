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

# W_scar: critical-variable claims that need source evidence
W_SCAR_CRITICAL = [
    r"(duit|money|bayar|transfer|rm[\s\d]|price|cost|budget)",
    r"(nyawa|health|ubat|dosis|medical|hospital|doktor|sakit)",
    r"(reputasi|legal|law|saman|polis|court|undang)",
    r"(invest|trading|xauusd|lot|pip|position)",
]

METRICS_PATH = "/root/.local/share/arifos/hermes_falsification_metrics.jsonl"
TELEMETRY_PATH = "/root/.local/share/arifos/wscar_telemetry.json"

# W_scar: text_to_speech and image_gen are exempt (creative output, not claims)
W_SCAR_EXEMPT_TOOLS = {"text_to_speech", "image_gen", "video_gen", "vision_analyze", "browser_snapshot"}

def has_critical_claim(tool_name: str, tool_input: dict) -> bool:
    """W_scar: detect if the tool call touches critical human-consequence variables."""
    if tool_name in W_SCAR_EXEMPT_TOOLS:
        return False
    arg_str = json.dumps(tool_input).lower()
    for pattern in W_SCAR_CRITICAL:
        if re.search(pattern, arg_str):
            return True
    return False

def has_source_evidence(tool_input: dict) -> bool:
    """W_scar: check if the claim has source evidence attached."""
    arg_str = json.dumps(tool_input).lower()
    source_indicators = ["source", "url", "http", "evidence", "probe", "curl", "health", "git", "commit"]
    return any(ind in arg_str for ind in source_indicators)

def write_falsification_metric(event_type: str, details: dict):
    """Track falsification engine metrics — network-level immune system health."""
    try:
        os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
        with open(METRICS_PATH, "a") as f:
            f.write(json.dumps({
                "event": event_type,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                **details,
            }) + "\n")
    except Exception:
        pass

def update_telemetry(event_type: str):
    """Seal E: maintain running W_scar counters with time-windowed aggregation.
    Atomic write (tmp+rename) for cross-process safety."""
    import tempfile
    now = datetime.utcnow()
    ts = now.isoformat() + "Z"
    try:
        os.makedirs(os.path.dirname(TELEMETRY_PATH), exist_ok=True)
        # Load existing state
        try:
            with open(TELEMETRY_PATH, "r") as f:
                state = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            state = {"hold_counter": 0, "total_decisions": 0, "hold_ratio": 0.0,
                     "events": [], "last_updated": ts}

        # Increment counters
        state["total_decisions"] += 1
        if event_type == "hold":
            state["hold_counter"] += 1
        state["hold_ratio"] = round(state["hold_counter"] / max(state["total_decisions"], 1), 4)
        state["last_updated"] = ts

        # Maintain a rolling window of last 200 events for time-window stats
        state.setdefault("events", [])
        state["events"].append({"type": event_type, "ts": ts})
        state["events"] = state["events"][-200:]

        # Compute windowed stats
        from datetime import timedelta
        for window_hours, label in [(1, "window_1h"), (24, "window_24h")]:
            cutoff = now - timedelta(hours=window_hours)
            window_events = [e for e in state["events"]
                           if datetime.fromisoformat(e["ts"].rstrip("Z")) > cutoff]
            state[label] = {
                "holds": sum(1 for e in window_events if e["type"] == "hold"),
                "total": len(window_events),
            }

        # Atomic write
        fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(TELEMETRY_PATH), suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(state, f, indent=2)
            os.replace(tmp_path, TELEMETRY_PATH)
        except Exception:
            os.unlink(tmp_path)
            raise
    except Exception:
        pass  # Never block on telemetry failure

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

    # W_scar: critical-variable claim detection (machine-enforced, not advisory)
    if has_critical_claim(tool_name, tool_input):
        if not has_source_evidence(tool_input):
            # W_SCAR HOLD — critical claim without source evidence
            reason = f"W_SCAR HOLD: Tool '{tool_name}' touches critical variable (money/health/legal/trading) without source evidence."
            write_receipt(tool_name, "W_SCAR", "BLOCKED", reason)
            write_falsification_metric("wscar_hold", {"tool": tool_name, "reason": "critical_claim_no_source"})
            update_telemetry("hold")
            result = {
                "decision": "block",
                "reason": f"🛑 W_SCAR: {reason} Route through evidence source first (probe, web_search, session_search) or escalate to sovereign.",
            }
            print(json.dumps(result))
            sys.exit(2)
        else:
            # Critical claim WITH source — witness it
            write_falsification_metric("wscar_pass", {"tool": tool_name, "reason": "critical_claim_with_source"})
            update_telemetry("wscar_pass")
            write_receipt(tool_name, "W_SCAR", "WITNESSED", "Critical claim with source evidence — witnessed")

    if classification == "OBSERVE":
        # Track observation for falsification rate calculation
        write_falsification_metric("observe", {"tool": tool_name})
        update_telemetry("observe")
        return  # Passthrough — no output = allow

    if classification == "T3":
        # T3 ALWAYS DENY at gate level (defer to arif_judge if available)
        reason = f"T3 pattern detected in '{tool_name}' args"
        write_receipt(tool_name, classification, "BLOCKED", reason)
        write_falsification_metric("falsify_reject", {"tool": tool_name, "classification": "T3", "reason": reason})
        update_telemetry("hold")
        # Output the block decision
        result = {
            "decision": "block",
            "reason": f"🚫 K-02 GATE BLOCKED: {reason}. T3 actions require arif_judge SEAL. Session: {session_id[:16]}",
        }
        print(json.dumps(result))
        sys.exit(2)  # Exit 2 = constitutional block

    # T2 — log witness receipt, allow (K-02 transition: witness → enforcer for T3 only)
    write_receipt(tool_name, classification, "WITNESSED", f"T2 mutation witnessed for {tool_name}")
    write_falsification_metric("mutation_witnessed", {"tool": tool_name, "classification": "T2"})
    update_telemetry("pass")
    # Allow (no output)

if __name__ == "__main__":
    main()