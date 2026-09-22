#!/usr/bin/env python3
"""CHRON Personal Edge — 13:15 MYT ARIF EDGE.

Purpose: WORLD x ARIF -> DECISION
Question: "Apa yang dunia pagi tadi dah jadi kepada hidup aku sekarang?"

Reads the morning M cycle, checks what materially changed since06:00,
which signals are still relevant, which became stale, which deadlines
moved closer, and what Arif actually did or reported.

Delivery policy:
  FULL   = >=3 material changes (send DM)
  PULSE  = 1-2 material changes (send DM, shorter)
  SILENT = 0 material changes (write receipt/state only, no DM)

Shadow mode: SHADOW = write all files but never send DM.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Allow import from same directory
sys.path.insert(0, str(Path(__file__).parent))

from shared import (
    MYT, STATE_DIR, today_str,
    now_myt, write_cycle, latest_m_cycle,
    git_activity_since, activity_count,
    federation_status, get_flow_health, carry_forward_entries,
    send_telegram,
)

# Delivery mode: SHADOW = no DM, CANARY = real delivery
# Set to CANARY after 3 clean shadow days
DELIVERY_MODE = "SHADOW"

# Materiality thresholds
MATERIAL_THRESHOLD_FULL = 3
MATERIAL_THRESHOLD_PULSE = 1


def gather_signals(m_cycle: dict | None) -> dict:
    """Gather midday data sources."""
    git = git_activity_since(since_hours=8)
    fed_alive, fed_total, fed_down = federation_status()
    flow = get_flow_health()
    cf = carry_forward_entries(hours=8)

    morning_signals = []
    if m_cycle:
        morning_signals = m_cycle.get("signals", [])
        morning_prediction_count = len(m_cycle.get("predictions", []))
    else:
        morning_prediction_count = 0

    return {
        "git": git,
        "git_count": activity_count(git),
        "fed_alive": fed_alive,
        "fed_total": fed_total,
        "fed_down": fed_down,
        "flow": flow,
        "carry_forward": cf,
        "morning_signals": morning_signals,
        "morning_prediction_count": morning_prediction_count,
        "m_cycle": m_cycle,
    }


def classify_changes(signals: dict) -> tuple[list[str], list[str], str]:
    """Classify what changed into material/non-material, determine mode.

    Returns: (material_changes, non_material_changes, delivery_mode)
    """
    material = []
    non_material = []

    # 1. Federation organ state change
    fed_down = signals["fed_down"]
    if fed_down:
        material.append(f"Federation DOWN: {', '.join(fed_down)}")
    else:
        non_material.append(f"Federation {signals['fed_alive']}/{signals['fed_total']} hidup")

    # 2. Git activity — meaningful commits vs noise
    git = signals["git"]
    git_count = signals["git_count"]
    if git_count >= 5:
        material.append(f"Active development: {git_count} commits across {len(git)} repos")
        # Name the repos
        for repo, commits in git.items():
            if len(commits) >= 2:
                material.append(f"  {repo}: {commits[0][:60]}")
    elif git_count >= 1:
        non_material.append(f"Light activity: {git_count} commits")

    # 3. Carry-forward events (explicit Arif actions or system events)
    for entry in signals["carry_forward"][:3]:
        # Anything in carry_forward is by definition noteworthy
        if any(kw in entry.lower() for kw in ["down", "fail", "error", "block", "urgent", "hold"]):
            material.append(f"CF alert: {entry[:80]}")
        else:
            non_material.append(f"CF: {entry[:60]}")

    # 4. FQ anomaly
    flow = signals.get("flow")
    if flow:
        fq = flow.get("fq", {})
        diag = fq.get("diagnosis", "")
        if diag and any(word in diag.lower() for word in ["pathological", "held", "critical", "collapse"]):
            material.append(f"FQ anomaly: {diag}")

    # 5. Morning signal staleness check
    # (signals that predicted something for today — are they still valid?)
    # For v0.1, just count — deeper verification comes with graph data

    # Determine delivery mode
    if len(material) >= MATERIAL_THRESHOLD_FULL:
        mode = "FULL"
    elif len(material) >= MATERIAL_THRESHOLD_PULSE:
        mode = "PULSE"
    else:
        mode = "SILENT"

    return material, non_material, mode


def build_message(signals: dict, material: list, non_material: list, mode: str) -> str:
    """Compose the midday message for Arif's DM."""
    now = now_myt()
    header = f"⚡ CHRON EDGE · {now.strftime('%H:%M')}"

    if mode == "FULL":
        lines = [header, ""]
        lines.append("↻ Perubahan sejak pagi:")
        for m in material:
            lines.append(f"  ▸ {m}")
        if non_material:
            lines.append("")
            lines.append("— lain-lain:")
            for nm in non_material[:3]:
                lines.append(f"  · {nm}")
    elif mode == "PULSE":
        lines = [header, ""]
        for m in material:
            lines.append(f"▸ {m}")
    else:
        # Should not be called in SILENT mode, but safety
        lines = [header, "", "Tiada perubahan material."]

    # Open loops — what to watch
    fed_down = signals.get("fed_down", [])
    if fed_down:
        lines.append("")
        lines.append(f"👁 Open loop: organ DOWN ({', '.join(fed_down)})")

    lines.append("")
    lines.append(f"— M→E bridge · {mode} · sumber lokal sahaja")

    return "\n".join(lines)


def run() -> int:
    """Execute the midday ARIF EDGE pulse."""
    date_str = today_str()
    now = now_myt()

    # Read morning cycle
    m_cycle = latest_m_cycle()

    # Gather and classify
    signals = gather_signals(m_cycle)
    material, non_material, mode = classify_changes(signals)

    # Build cycle state
    cycle = {
        "date": date_str,
        "slot": "E",
        "cycle_id": f"E-{date_str}",
        "parent_cycle_id": m_cycle.get("cycle_id") if m_cycle else None,
        "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "event_time": now.isoformat(timespec="seconds"),
        "principal_scope": "arif",
        "privacy_scope": "personal_dm",
        "delivery_mode": DELIVERY_MODE,
        "computed_mode": mode,
        "signals": {
            "git_activity": {repo: len(commits) for repo, commits in signals["git"].items()},
            "git_count": signals["git_count"],
            "federation_down": signals["fed_down"],
            "material_changes": material,
            "non_material_changes": non_material,
            "morning_signal_count": len(signals["morning_signals"]),
            "carry_forward_count": len(signals["carry_forward"]),
        },
        "provenance": {
            "source": "chron-edge-midday",
            "version": "0.1.0",
            "delivery_mode": DELIVERY_MODE,
        },
    }

    # Persist cycle state
    write_cycle(cycle)

    # Log to console
    print(f"CHRON EDGE {date_str} — mode={mode}, delivery={DELIVERY_MODE}")
    print(f"  material: {len(material)}, non_material: {len(non_material)}")
    for m in material:
        print(f"  ▸ {m}")

    # Delivery
    if DELIVERY_MODE == "SHADOW":
        print("  [SHADOW] No DM sent. Cycle state written.")
        return 0

    if mode == "SILENT":
        print("  [SILENT] No material changes. No DM sent.")
        return 0

    # Build and send message
    msg = build_message(signals, material, non_material, mode)
    ok, detail = send_telegram(msg)
    print(f"  [DM] {'OK' if ok else 'FAIL'}: {detail}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(run())
