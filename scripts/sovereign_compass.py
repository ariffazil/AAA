#!/usr/bin/env python3
"""
Sovereign Compass — ATLAS333 Decision Navigation for 888 (Arif)

Reads both paradox ledgers (kernel SQLite + membrane JSONL) and produces
a pre-decision terrain report. Shows what paradoxes are active, which are
maturing toward EUREKA, what the zone profile looks like, and what patterns
recur before SEAL-grade decisions.

PURE READ. Zero F1 risk. Never mutates state.

Usage:
    python3 sovereign_compass.py                     # Full dashboard
    python3 sovereign_compass.py --before-seal       # Pre-SEAL decision report
    python3 sovereign_compass.py --eureka            # EUREKA candidates only
    python3 sovereign_compass.py --zones             # Zone activation heatmap
    python3 sovereign_compass.py --recent N          # Last N paradox events

DITEMPA BUKAN DIBERI — Forged 2026-08-05 by 333-AGI Δ MIND
"""

import json
import os
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ── Ledger Paths ────────────────────────────────────────────────────
SQLITE_LEDGER = "/root/.local/share/arifos/atlas333/atlas_ledger.db"
MEMBRANE_LEDGER = "/root/.local/share/arifos/atlas333/membrane_paradox_ledger.jsonl"
MEMBRANE_LOG = "/root/.local/share/arifos/membrane-crossings.jsonl"

# ── ATLAS333 Constants ──────────────────────────────────────────────
PARADOX_NAMES: dict[int, str] = {
    1: "recollection vs discovery",
    2: "forgetting vs remembering",
    3: "horizon vs blindness",
    4: "vastness vs opacity",
    5: "epistemic hunger vs discipline",
    6: "stability vs rigidity",
    7: "power vs restraint",
    8: "temporal distance vs epistemic quality",
    9: "knowledge vs belief",
    10: "epistemic humility vs paralysis",
    11: "forgetting as health vs remembering as duty",
    12: "confidence vs competence",
    13: "epistemic certainty vs pragmatic certainty",
    14: "methodological doubt vs operational trust",
    15: "examination vs action",
    16: "certainty vs learning",
    17: "every model wrong, some useful",
    18: "false negative vs false positive",
    19: "metacognition vs meta-uncertainty",
    20: "ataraxia vs responsibility",
    21: "foundational certainty vs fallibility",
    22: "silence vs attempt",
    23: "providence vs agency",
    24: "order vs power",
    25: "law as civilizer vs law as weapon",
    26: "comprehensiveness vs decidability",
    27: "non-retaliation vs justified coercion",
    28: "ex ante clarity vs ex post knowledge",
    29: "social contract vs power asymmetry",
    30: "legality vs fairness",
    31: "permanence vs reversibility",
    32: "care vs computability",
    33: "expertise vs authoritarianism",
    34: "root access vs kernel governance",
    35: "positive test vs defensive closure",
}

ZONES: dict[str, str] = {
    "I": "Truth Territory",
    "II": "Risk Frontier",
    "III": "Care Basin",
    "IV": "Meaning Meridian",
    "V": "Discovery Ridge",
    "VI": "Governance Spine",
    "VII": "Sovereign Apex",
}

EUREKA_SESSION_THRESHOLD = 3
RECURRENCE_WINDOW = 10  # sessions to analyze for pattern detection


# ── Data Loading ────────────────────────────────────────────────────


def load_sqlite_events() -> list[dict]:
    """Load paradox events from the kernel SQLite ledger."""
    try:
        if not os.path.exists(SQLITE_LEDGER):
            return []
        conn = sqlite3.connect(SQLITE_LEDGER, timeout=2.0)
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM paradox_events ORDER BY timestamp DESC LIMIT 500").fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def load_membrane_events() -> list[dict]:
    """Load paradox events from the membrane JSONL ledger."""
    events = []
    try:
        if not os.path.exists(MEMBRANE_LEDGER):
            return events
        with open(MEMBRANE_LEDGER) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return events[-500:]  # Last 500
    except Exception:
        return events


def load_membrane_crossings() -> list[dict]:
    """Load raw membrane crossing logs."""
    crossings = []
    try:
        if not os.path.exists(MEMBRANE_LOG):
            return crossings
        with open(MEMBRANE_LOG) as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        crossings.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return crossings[-200:]
    except Exception:
        return crossings


def merge_events(sqlite: list[dict], membrane: list[dict]) -> list[dict]:
    """Merge both ledgers, normalize fields, sort by timestamp."""
    merged = []

    for e in sqlite:
        merged.append(
            {
                "timestamp": e.get("timestamp", ""),
                "session_id": e.get("session_id", "unknown"),
                "lane": e.get("lane", "UNKNOWN"),
                "tau": e.get("tau", 0.5),
                "kappa": e.get("kappa", 0.5),
                "rho": e.get("rho", 0.0),
                "paradox_ids": [e.get("paradox_id", "").replace("P", "")],
                "zone": e.get("zone", ""),
                "source": "kernel",
            }
        )

    for e in membrane:
        pids = e.get("paradox_ids", [])
        merged.append(
            {
                "timestamp": e.get("timestamp", ""),
                "session_id": e.get("session_id", "unknown"),
                "lane": e.get("lane", "UNKNOWN"),
                "tau": e.get("tau", 0.5),
                "kappa": e.get("kappa", 0.5),
                "rho": e.get("rho", 0.0),
                "paradox_ids": [str(p) for p in pids] if isinstance(pids, list) else [],
                "zone": e.get("zone_id", ""),
                "source": "membrane",
                "organ": e.get("organ", "UNKNOWN"),
                "eureka_fired": e.get("eureka_fired", False),
            }
        )

    merged.sort(key=lambda x: x.get("timestamp", ""))
    return merged


# ── Analysis ────────────────────────────────────────────────────────


def compute_eureka_candidates(events: list[dict]) -> list[dict]:
    """Find paradoxes with 3+ distinct sessions."""
    sessions_by_paradox: dict[str, set] = defaultdict(set)
    for e in events:
        for pid in e.get("paradox_ids", []):
            pid_str = str(pid)
            sid = e.get("session_id", "unknown")
            # Skip placeholder sessions
            if sid.startswith("phi_") or sid == "unknown":
                continue
            sessions_by_paradox[pid_str].add(sid)

    candidates = []
    for pid, sessions in sessions_by_paradox.items():
        if len(sessions) >= EUREKA_SESSION_THRESHOLD:
            pid_int = int(pid)
            candidates.append(
                {
                    "paradox_id": pid_int,
                    "name": PARADOX_NAMES.get(pid_int, f"paradox {pid_int}"),
                    "distinct_sessions": len(sessions),
                    "activation_count": sum(1 for e in events if pid in [str(p) for p in e.get("paradox_ids", [])]),
                    "zone": _paradox_zone(pid_int),
                }
            )

    candidates.sort(key=lambda c: c["distinct_sessions"], reverse=True)
    return candidates


def compute_zone_profile(events: list[dict]) -> dict[str, float]:
    """Compute zone activation heatmap."""
    zone_counts: Counter = Counter()
    for e in events:
        zone = e.get("zone", "")
        if zone and zone in ZONES:
            zone_counts[zone] += 1
    return dict(zone_counts.most_common())


def compute_active_now(events: list[dict], n_recent: int = 10) -> list[dict]:
    """Get paradoxes from the most recent events."""
    recent = events[-n_recent:] if events else []
    paradox_counter: Counter = Counter()
    for e in recent:
        for pid in e.get("paradox_ids", []):
            paradox_counter[int(pid)] += 1

    active = []
    for pid, count in paradox_counter.most_common(10):
        active.append(
            {
                "paradox_id": pid,
                "name": PARADOX_NAMES.get(pid, f"paradox {pid}"),
                "recent_activations": count,
                "zone": _paradox_zone(pid),
            }
        )
    return active


def detect_recurrence_patterns(events: list[dict]) -> list[dict]:
    """Detect paradoxes that frequently co-activate (pair patterns)."""
    pairs: Counter = Counter()
    for e in events:
        pids = sorted([int(p) for p in e.get("paradox_ids", [])])
        for i, p1 in enumerate(pids):
            for p2 in pids[i + 1 :]:
                pairs[(p1, p2)] += 1

    patterns = []
    for (p1, p2), count in pairs.most_common(10):
        if count >= 3:
            patterns.append(
                {
                    "paradox_pair": (p1, p2),
                    "pair_names": (
                        PARADOX_NAMES.get(p1, f"P{p1}"),
                        PARADOX_NAMES.get(p2, f"P{p2}"),
                    ),
                    "co_activations": count,
                    "interpretation": _interpret_pair(p1, p2),
                }
            )

    return patterns


def compute_organ_visibility(crossings: list[dict]) -> dict:
    """Analyze organ visibility from raw membrane crossings."""
    organs: Counter = Counter()
    for c in crossings:
        organ = c.get("organ", "UNKNOWN")
        organs[organ] += 1

    total = sum(organs.values()) or 1
    return {
        "total_crossings": total,
        "organ_distribution": dict(organs.most_common()),
        "unknown_pct": round(organs.get("UNKNOWN", 0) / total * 100, 1),
    }


def compute_summary(events: list[dict], crossings: list[dict]) -> dict:
    """Full compass summary."""
    sqlite_events = load_sqlite_events()
    membrane_events = load_membrane_events()
    events = merge_events(sqlite_events, membrane_events)

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ledger_sources": {
            "kernel_sqlite_events": len(sqlite_events),
            "membrane_jsonl_events": len(membrane_events),
            "membrane_crossings_logged": len(crossings),
        },
        "active_paradoxes": compute_active_now(events),
        "eureka_candidates": compute_eureka_candidates(events),
        "zone_profile": compute_zone_profile(events),
        "recurrence_patterns": detect_recurrence_patterns(events),
        "organ_visibility": compute_organ_visibility(crossings),
    }


# ── Helpers ──────────────────────────────────────────────────────────


def _paradox_zone(pid: int) -> str:
    """Get zone name for a paradox ID."""
    zone_map = {
        1: "I",
        2: "I",
        3: "I",
        4: "I",
        5: "IV",
        6: "II",
        7: "II",
        8: "II",
        9: "II",
        10: "II",
        11: "III",
        12: "I",
        13: "I",
        14: "I",
        15: "III",
        16: "III",
        17: "III",
        18: "IV",
        19: "V",
        20: "IV",
        21: "V",
        22: "V",
        23: "II",
        24: "IV",
        25: "V",
        26: "VI",
        27: "VI",
        28: "VI",
        29: "VII",
        30: "VI",
        31: "VII",
        32: "III",
        33: "VII",
        34: "VII",
        35: "VII",
    }
    zid = zone_map.get(pid, "I")
    return ZONES.get(zid, f"Zone {zid}")


def _interpret_pair(p1: int, p2: int) -> str:
    """Generate a human-readable interpretation of a co-activation pair."""
    pairs = {
        (29, 31): "Sovereignty tension: authority vs permanence — classic SEAL-decision pattern",
        (16, 17): "Epistemic tension: certainty vs model limits — building with imperfect knowledge",
        (26, 28): "Governance tension: rules vs adaptation — the gate that protects also blocks",
        (34, 35): "Kernel tension: root power vs constitutional defense — the foundation paradox",
        (6, 24): "Stability tension: order vs power — protecting structure vs enabling change",
        (30, 33): "Audit tension: legality vs expertise — who decides what is right",
    }
    for key in [(p1, p2), (p2, p1)]:
        if key in pairs:
            return pairs[key]
    return "Co-activation pattern — investigate structural relationship"


# ── Renderers ────────────────────────────────────────────────────────


def render_dashboard(summary: dict) -> str:
    """Render full Sovereign Compass dashboard."""
    lines = []
    lines.append("")
    lines.append("╔═══════════════════════════════════════════════════════════════╗")
    lines.append("║         ATLAS333 SOVEREIGN COMPASS — Terrain Report          ║")
    lines.append("╠═══════════════════════════════════════════════════════════════╣")
    lines.append(f"║ Generated: {summary['generated_at'][:19]} UTC                       ║")

    # Ledger sources
    src = summary["ledger_sources"]
    lines.append("╠═══════════════════════════════════════════════════════════════╣")
    lines.append("║ SOURCES                                                      ║")
    lines.append(f"║   Kernel SQLite:  {src['kernel_sqlite_events']:>5} events                     ║")
    lines.append(f"║   Membrane JSONL: {src['membrane_jsonl_events']:>5} events                     ║")
    lines.append(f"║   Membrane Log:   {src['membrane_crossings_logged']:>5} crossings                   ║")
    lines.append("╠═══════════════════════════════════════════════════════════════╣")

    # Organ visibility
    vis = summary["organ_visibility"]
    lines.append("║ MEMBRANE VISIBILITY                                          ║")
    lines.append(f"║   Total crossings: {vis['total_crossings']}                                        ║")
    for organ, count in vis.get("organ_distribution", {}).items():
        pct = round(count / max(vis["total_crossings"], 1) * 100)
        lines.append(f"║   {organ:.<12} {count:>5} ({pct}%)                                    ║")
    lines.append(f"║   {'BLIND (UNKNOWN)':.<12} {vis['unknown_pct']}% of traffic                              ║")
    lines.append("╠═══════════════════════════════════════════════════════════════╣")

    # Active paradoxes
    lines.append("║ ACTIVE PARADOXES (most recent events)                         ║")
    for p in summary["active_paradoxes"][:8]:
        lines.append(f"║   P{p['paradox_id']:>2} [{p['zone'][:12]:>12}] {p['name'][:40]:<40} ║")
    lines.append("╠═══════════════════════════════════════════════════════════════╣")

    # EUREKA candidates
    candidates = summary["eureka_candidates"]
    lines.append(f"║ EUREKA CANDIDATES (≥3 sessions, route to 888-APEX)    {len(candidates):>3}   ║")
    if candidates:
        for c in candidates[:5]:
            lines.append(f"║   ⚡ P{c['paradox_id']:>2} {c['name'][:42]:<42} ║")
            lines.append(
                f"║      {c['distinct_sessions']} sessions, {c['activation_count']} activations, zone={c['zone'][:20]} ║"
            )
    else:
        lines.append("║   No paradoxes have matured yet.                              ║")
    lines.append("╠═══════════════════════════════════════════════════════════════╣")

    # Zone profile
    lines.append("║ ZONE ACTIVATION HEATMAP                                      ║")
    zones = summary["zone_profile"]
    max_zc = max(zones.values()) if zones else 1
    for zone_id, zone_name in sorted(ZONES.items()):
        count = zones.get(zone_id, 0)
        bar_len = min(30, int(count / max_zc * 30)) if max_zc else 0
        bar = "█" * bar_len + "░" * (30 - bar_len)
        lines.append(f"║   Zone {zone_id} {zone_name[:15]:<15} {bar} {count:>4} ║")
    lines.append("╠═══════════════════════════════════════════════════════════════╣")

    # Recurrence patterns
    patterns = summary["recurrence_patterns"]
    lines.append(f"║ RECURRENCE PATTERNS (paradox pairs)                    {len(patterns):>3}   ║")
    if patterns:
        for pat in patterns[:5]:
            lines.append(
                f"║   P{pat['paradox_pair'][0]}+P{pat['paradox_pair'][1]} ({pat['co_activations']}×): {pat['interpretation'][:42]:<42} ║"
            )
    else:
        lines.append("║   No recurrence patterns detected yet.                        ║")
    lines.append("╠═══════════════════════════════════════════════════════════════╣")

    # Decision guidance
    if candidates:
        lines.append("║ ⚠️  DECISION GUIDANCE                                         ║")
        lines.append("║   EUREKA candidates pending 888-APEX review.                   ║")
        lines.append("║   Route each candidate: SEAL (ratify scar) │ HOLD (more        ║")
        lines.append("║   evidence) │ VOID (dismiss).                                 ║")
        lines.append("║   The Compass DETECTS. The Sovereign DECIDES.                 ║")
    lines.append("╚═══════════════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append("DITEMPA BUKAN DIBERI — The map is alive. The terrain is yours.")
    lines.append("")

    return "\n".join(lines)


def render_pre_seal(summary: dict) -> str:
    """Render a pre-SEAL decision report."""
    lines = []
    candidates = summary["eureka_candidates"]
    patterns = summary["recurrence_patterns"]

    lines.append("")
    lines.append("┌──────────────────────────────────────────────────────────────┐")
    lines.append("│   PRE-SEAL TERRAIN REPORT — Before Irreversible Action       │")
    lines.append("├──────────────────────────────────────────────────────────────┤")

    if candidates:
        lines.append(f"│ ⚠️  {len(candidates)} EUREKA CANDIDATES pending review                      │")
        for c in candidates[:5]:
            lines.append(f"│   P{c['paradox_id']:>2}: {c['name'][:42]:<42} │")
            lines.append(f"│       {c['distinct_sessions']} sessions, zone {c['zone'][:20]}                    │")
    else:
        lines.append("│ ✅ No matured paradoxes — cognitive terrain is clear.       │")

    lines.append("├──────────────────────────────────────────────────────────────┤")

    if patterns:
        lines.append(f"│ PATTERNS: {len(patterns)} recurring paradox pairs                     │")
        for pat in patterns[:3]:
            lines.append(
                f"│   P{pat['paradox_pair'][0]}+P{pat['paradox_pair'][1]} ({pat['co_activations']}×)                               │"
            )

    # Risk estimate
    zones = summary["zone_profile"]
    high_risk_zones = sum(zones.get(z, 0) for z in ["VI", "VII"])
    total = sum(zones.values()) or 1
    risk_pct = round(high_risk_zones / total * 100)
    lines.append("├──────────────────────────────────────────────────────────────┤")
    lines.append(f"│ RISK ESTIMATE: {risk_pct}% of activations in Governance/Sovereign zones  │")
    lines.append(f"│ VERDICT: SEAL {'⚠️  WITH CAUTION' if candidates else '✅ CLEAR'}                     │")
    lines.append("└──────────────────────────────────────────────────────────────┘")
    lines.append("")

    return "\n".join(lines)


def render_eureka(summary: dict) -> str:
    """Render EUREKA candidates only."""
    candidates = summary["eureka_candidates"]
    lines = []
    lines.append(f"\n⚡ EUREKA777 — {len(candidates)} CANDIDATES\n")

    if not candidates:
        lines.append("  No paradoxes have crossed the maturity threshold (3+ distinct sessions).")
        lines.append("  The cognitive terrain is calm.")
    else:
        for c in candidates:
            lines.append(f"  P{c['paradox_id']:>2} | {c['name'][:50]}")
            lines.append(
                f"     Sessions: {c['distinct_sessions']} | Activations: {c['activation_count']} | Zone: {c['zone']}"
            )
            lines.append(f"     ACTION: Route to 888-APEX → SEAL (scar) │ HOLD (evidence) │ VOID (dismiss)")
            lines.append("")

    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────────────────────


def main():
    import argparse

    parser = argparse.ArgumentParser(description="ATLAS333 Sovereign Compass — Decision Terrain Navigation")
    parser.add_argument("--before-seal", action="store_true", help="Pre-SEAL decision report")
    parser.add_argument("--eureka", action="store_true", help="EUREKA candidates only")
    parser.add_argument("--zones", action="store_true", help="Zone activation heatmap")
    parser.add_argument("--recent", type=int, default=0, help="Show last N paradox events")
    parser.add_argument("--json", action="store_true", help="Output as JSON (machine-readable)")
    args = parser.parse_args()

    # Load data
    sqlite_events = load_sqlite_events()
    membrane_events = load_membrane_events()
    crossings = load_membrane_crossings()
    events = merge_events(sqlite_events, membrane_events)
    summary = compute_summary(events, crossings)

    # Render
    if args.json:
        print(json.dumps(summary, indent=2, default=str))
    elif args.eureka:
        print(render_eureka(summary))
    elif args.before_seal:
        print(render_pre_seal(summary))
    elif args.zones:
        print("\nZone Activation Heatmap:")
        for zone_id, zone_name in sorted(ZONES.items()):
            count = summary["zone_profile"].get(zone_id, 0)
            bar = "█" * min(50, count)
            print(f"  Zone {zone_id} {zone_name:<20} {bar} ({count})")
        print()
    elif args.recent > 0:
        print(f"\nLast {args.recent} paradox events:")
        for e in events[-args.recent :]:
            pids = e.get("paradox_ids", [])
            ts = e.get("timestamp", "")[:19]
            print(f"  {ts} | {e.get('lane', '?'):<7} | zone={e.get('zone', '?')} | {len(pids)}p: {pids[:5]}")
        print()
    else:
        print(render_dashboard(summary))


if __name__ == "__main__":
    main()
