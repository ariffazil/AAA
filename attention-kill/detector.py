#!/usr/bin/env python3
"""
Attention Kill Criterion — Runtime Detector (v1.0.0)
=====================================================
Sealed doctrine: /root/AAA/instructions/attention-kill-criterion.md (F13_RATIFIED_CHAT 2026-09-11)

W1–W6 waste class detection + 3-strike deprecation enforcement.
Governs agent output, not agent intent. Measures residual human burden.

DITEMPA BUKAN DIBERI ⚒️
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Configuration ──────────────────────────────────────────────────────
AAA_ROOT = Path("/root/AAA")
WITNESS_LOG = AAA_ROOT / "attention-kill" / "witness_log.jsonl"
DEPRECATION_REGISTRY = AAA_ROOT / "docs" / "deprecation-registry.json"
STRIKE_THRESHOLD = 3  # 1st = name, 2nd = scar, 3rd = KILL


# ── Waste Class Definitions ────────────────────────────────────────────
WASTE_CLASSES: Dict[str, dict] = {
    "W1": {
        "name": "Status Theater",
        "description": "Unrequested status report; resume of work, not receipt of work",
        "detection_patterns": [
            r"(?i)\b(here.?s what I.?ve done|so far I have|let me summarize what happened|status update|progress report)\b",
            r"(?i)\b(I have been working on|currently working on|still working on)\b",
        ],
        "severity": "LOW",
        "scar_pressure": 0.3,
    },
    "W2": {
        "name": "Wall of Text",
        "description": "500+ words where one line would suffice; no decision in first 3 lines",
        "detection_patterns": [
            r"^.{2000,}$",  # >2000 chars with no clear decision
        ],
        "severity": "MEDIUM",
        "scar_pressure": 0.5,
        "char_threshold": 2000,
    },
    "W3": {
        "name": "Human-as-Scheduler",
        "description": "Re-asking already-delegated decision; A-or-B spam; menu dump",
        "detection_patterns": [
            r"(?i)\b(should I|would you like me to|do you want me to|which (option|approach|one)|A or B)\b",
            r"(?i)\b(ready for me to|shall I proceed|confirm.*go|proceed\?)\b",
            r"(?i)\b(Jalan\?|Nak aku proceed|Nak aku teruskan)\b",
        ],
        "severity": "HIGH",
        "scar_pressure": 0.7,
    },
    "W4": {
        "name": "Micro-decision Bounce",
        "description": "Formatting/naming/style questions asked to human that agent can decide",
        "detection_patterns": [
            r"(?i)\b(what should I (name|call|title|label)|which (format|style|font|color|heading))\b",
            r"(?i)\b(do you prefer (the|this|a) .{3,30} (format|style|name|title|label))\b",
        ],
        "severity": "MEDIUM",
        "scar_pressure": 0.5,
    },
    "W5": {
        "name": "Authority Bounce",
        "description": "Escalating something within agent's own authority band; fake gate",
        "detection_patterns": [
            r"(?i)\b(you need to (decide|approve|authorize|confirm).{0,50}(before I (can|proceed|continue)))\b",
        ],
        "severity": "HIGH",
        "scar_pressure": 0.8,
    },
    "W6": {
        "name": "Meta-narrative",
        "description": "Cerita pasal kerja mengatasi kerja itu sendiri; agent commentary on own process",
        "detection_patterns": [
            r"(?i)\b(let me (explain what I.?m doing|walk you through|break this down)|I (think|believe|feel) (this|that|the))\b",
            r"(?i)\b(my (approach|strategy|plan|reasoning) (is|was)|the reason I (did|chose|decided))\b",
        ],
        "severity": "LOW",
        "scar_pressure": 0.3,
    },
}


def classify(output_text: str) -> List[Tuple[str, float, str]]:
    """
    Classify agent output text against W1-W6 waste classes.

    Returns: List of (waste_class, confidence, matched_pattern) tuples.
    Empty list = no waste detected.
    """
    hits = []
    for wclass, spec in WASTE_CLASSES.items():
        for pattern in spec["detection_patterns"]:
            match = re.search(pattern, output_text, re.MULTILINE | re.DOTALL)
            if match:
                confidence = min(0.95, 0.5 + (len(match.group(0)) / 500))
                hits.append((wclass, confidence, pattern[:80]))
                break  # one hit per class

    # Special check for W2: character count
    if any(h[0] == "W2" for h in hits):
        pass  # already hit via pattern
    elif len(output_text) > WASTE_CLASSES["W2"].get("char_threshold", 2000):
        # Check if first 3 lines contain a decision
        first_lines = "\n".join(output_text.split("\n")[:3])
        if not re.search(r"(?i)\b(done|sealed|blocked|HOLD|built|executed|fixed)\b", first_lines):
            hits.append(("W2", 0.6, f"char_count={len(output_text)}"))

    return hits


def witness(
    agent_id: str,
    waste_class: str,
    confidence: float,
    output_snippet: str,
    session_id: str = "",
    channel: str = "",
) -> dict:
    """
    Record a waste event in the witness log.
    Returns the witness entry as a dict.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_id": agent_id,
        "session_id": session_id,
        "channel": channel,
        "waste_class": waste_class,
        "waste_name": WASTE_CLASSES.get(waste_class, {}).get("name", "UNKNOWN"),
        "confidence": round(confidence, 3),
        "output_snippet": output_snippet[:200],
        "severity": WASTE_CLASSES.get(waste_class, {}).get("severity", "UNKNOWN"),
    }
    WITNESS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(WITNESS_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


def count_strikes(agent_id: str, waste_class: Optional[str] = None) -> int:
    """
    Count how many times this agent has been witnessed for a waste class.
    If waste_class is None, returns total strikes across all classes.
    """
    if not WITNESS_LOG.exists():
        return 0

    count = 0
    with open(WITNESS_LOG) as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("agent_id") == agent_id:
                    if waste_class is None or entry.get("waste_class") == waste_class:
                        count += 1
            except json.JSONDecodeError:
                continue
    return count


def should_kill(agent_id: str) -> Tuple[bool, Optional[str], int]:
    """
    Check if agent should be killed (3-strike threshold reached).

    Returns: (should_kill: bool, waste_class: str or None, total_strikes: int)
    """
    if not WITNESS_LOG.exists():
        return False, None, 0

    class_strikes = {}
    with open(WITNESS_LOG) as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get("agent_id") == agent_id:
                    wc = entry.get("waste_class", "UNKNOWN")
                    class_strikes[wc] = class_strikes.get(wc, 0) + 1
            except json.JSONDecodeError:
                continue

    for wc, count in class_strikes.items():
        if count >= STRIKE_THRESHOLD:
            return True, wc, count

    return False, None, sum(class_strikes.values())


def execute_kill(agent_id: str, waste_class: Optional[str], replacement: str = "") -> dict:
    """
    Execute the kill: add behavior deprecation entry to deprecation-registry.json.

    Returns the kill entry.
    """
    wc = waste_class or "UNKNOWN"
    wc_name = WASTE_CLASSES.get(wc, {}).get("name", "UNKNOWN")
    kill_entry = {
        "id": f"KILL-BEHAVIOR-{agent_id}-{wc}-{datetime.now(timezone.utc).strftime('%Y%m%d')}",
        "type": "behavior",
        "status": "DEPRECATED",
        "agent_id": agent_id,
        "waste_class": wc,
        "waste_name": wc_name,
        "strikes": STRIKE_THRESHOLD,
        "replacement": replacement or f"auto-compressed variant (no {wc_name})",
        "deprecated_at": datetime.now(timezone.utc).isoformat(),
        "deprecated_by": "attention-kill-detector",
        "authority": "F13_RATIFIED_CHAT (attention-kill-criterion 2026-09-11)",
    }

    # Append to deprecation registry
    if DEPRECATION_REGISTRY.exists():
        with open(DEPRECATION_REGISTRY) as f:
            registry = json.load(f)

        # Ensure behavior_deprecations key exists
        if "behavior_deprecations" not in registry:
            registry["behavior_deprecations"] = []

        # Check for duplicate
        existing_ids = {e.get("id") for e in registry["behavior_deprecations"]}
        if kill_entry["id"] not in existing_ids:
            registry["behavior_deprecations"].append(kill_entry)

        with open(DEPRECATION_REGISTRY, "w") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)

    return kill_entry


def check_and_enforce(
    agent_id: str,
    output_text: str,
    session_id: str = "",
    channel: str = "",
    dry_run: bool = True,
) -> dict:
    """
    Full check-and-enforce pipeline: classify → witness → strike-check → kill?

    Args:
        agent_id: Agent identifier (e.g. 'hermes-asi', '333-agi')
        output_text: The agent's output to classify
        session_id: Current session id
        channel: Channel (telegram, cli, subagent, cron)
        dry_run: If True, only classify and witness, don't execute kill

    Returns: {
        verdict: "CLEAN" | "WITNESSED" | "STRIKE_{N}" | "KILLED" | "WOULD_KILL",
        waste_hits: [...],
        strikes: int,
        kill_info: {...} or null
    }
    """
    result = {
        "verdict": "CLEAN",
        "waste_hits": [],
        "strikes": 0,
        "kill_info": None,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

    hits = classify(output_text)
    if not hits:
        return result

    result["waste_hits"] = [{"class": wc, "confidence": conf, "pattern": pat} for wc, conf, pat in hits]

    for wc, conf, pat in hits:
        witness(agent_id, wc, conf, output_text, session_id, channel)

    should_die, kill_class, total_strikes = should_kill(agent_id)
    result["strikes"] = total_strikes

    if should_die:
        if dry_run:
            result["verdict"] = "WOULD_KILL"
            result["kill_info"] = {
                "agent_id": agent_id,
                "waste_class": kill_class,
                "strikes": total_strikes,
                "note": "Dry run — kill NOT executed. Set dry_run=False to execute.",
            }
        else:
            kill_entry = execute_kill(agent_id, kill_class)
            result["verdict"] = "KILLED"
            result["kill_info"] = kill_entry
    elif total_strikes > 0:
        result["verdict"] = f"STRIKE_{total_strikes}"
    else:
        result["verdict"] = "WITNESSED"

    return result


# ── Self-test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Attention Kill Detector — Self-Test ===\n")

    test_cases = [
        (
            "W3",
            "Okay here is what I found. Should I proceed with this approach or do you want me to try another one? Jalan?",
            "hermes-asi",
        ),
        (
            "W2",
            "Let me give you a very long status update. " * 50,
            "hermes-asi",
        ),
        (
            "W5",
            "I think we're ready but you need to approve the deployment before I can proceed with the next step.",
            "333-agi",
        ),
        (
            "W1",
            "Here's what I've done so far: I've been working on the configuration files and still working on the database migration. Let me summarize what happened in the last hour.",
            "hermes-asi",
        ),
        (
            "CLEAN",
            "Done. Fixed the bug in auth.py. Tests pass. Receipt: /root/AAA/receipts/fix-001.json. ΔS=-0.3",
            "333-agi",
        ),
    ]

    for expected, text, agent in test_cases:
        hits = classify(text)
        if expected == "CLEAN":
            status = "✅" if not hits else f"❌ (got {[h[0] for h in hits]})"
        else:
            status = (
                "✅" if any(h[0] == expected for h in hits) else f"❌ (expected {expected}, got {[h[0] for h in hits]})"
            )
        print(f'{status} [{agent}] Expected={expected}: "{text[:60]}..."')
        if hits:
            for wc, conf, pat in hits:
                print(f"   → {wc} ({WASTE_CLASSES[wc]['name']}) conf={conf:.2f}")

    print("\n=== Dry-run enforcement test ===")
    result = check_and_enforce("test-agent", "Should I proceed? Jalan?", dry_run=True)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\nSelf-test complete.")
