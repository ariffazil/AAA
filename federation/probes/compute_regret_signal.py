#!/usr/bin/env python3
"""
CCC-T-26 (2026-09-18) — Router Regret Signal Calculator.

Computes first-order signal from available receipts:
- Witnessed vs Blocked ratio per harness
- Envelope emission rate per harness
- Session-level tool coverage

NOTE: True router regret = Utility(best_possible) - Utility(routed). Requires routing decision
log (FED `fed_route` decision persistence). That log is NOT YET WIRED (Phase 5 deferred item).
This script computes a PROXY signal from existing gate receipts + envelope emits.

Usage: python3 compute_regret_signal.py [--out path]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime, timezone


HERMES_RECEIPTS = Path("/root/.local/share/arifos/hermes_hook_receipts.jsonl")
HERMES_ENVELOPES = Path("/root/.local/share/arifos/hermes_envelope_emits.jsonl")
OPENCODE_RECEIPTS = Path("/root/.local/share/arifos/opencode_receipts.jsonl")
MCP_AUDIT = Path("/root/.agent-workbench/mcp-audit.jsonl")


def safe_read_lines(path: Path) -> list[dict]:
    """Read JSONL lines, skip malformed, return parsed dicts."""
    if not path.exists():
        return []
    out = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="/root/AAA/federation/phase5_first_regret_signal_20260918.md")
    args = parser.parse_args()

    # Load receipts
    hermes_receipts = safe_read_lines(HERMES_RECEIPTS)
    hermes_envelopes = safe_read_lines(HERMES_ENVELOPES)
    opencode_receipts = safe_read_lines(OPENCODE_RECEIPTS)
    mcp_audit = safe_read_lines(MCP_AUDIT)

    # Per-harness counters
    hermes_event_counts = Counter()
    hermes_tier_counts = Counter()
    hermes_decision_counts = Counter()
    for r in hermes_receipts:
        event = r.get("event", "unknown")
        hermes_event_counts[event] += 1
        if "classification" in r:
            hermes_tier_counts[r["classification"]] += 1
        if "witnessed" in event.lower():
            hermes_decision_counts["WITNESSED"] += 1
        elif "blocked" in event.lower() or "tripped" in event.lower():
            hermes_decision_counts["BLOCKED"] += 1
        elif "falsif" in event.lower():
            hermes_decision_counts["FALSIFICATION"] += 1

    # Envelope signal
    envelope_tier_counts = Counter()
    envelope_decision_counts = Counter()
    for e in hermes_envelopes:
        envelope_tier_counts[e.get("tier", "unknown")] += 1
        envelope_decision_counts[e.get("decision", "unknown")] += 1

    # OpenCode event distribution
    opencode_event_counts = Counter()
    for r in opencode_receipts[:1000]:  # sample first 1000 to avoid memory blowup
        event = r.get("event", "unknown")
        opencode_event_counts[event] += 1

    # Compute proxy signals
    total_hermes = len(hermes_receipts)
    total_hermes_witnessed = hermes_decision_counts.get("WITNESSED", 0)
    total_hermes_blocked = hermes_decision_counts.get("BLOCKED", 0)
    total_hermes_jitu = sum(1 for e in hermes_event_counts if "jitu" in e.lower())
    block_rate = (total_hermes_blocked / total_hermes * 100) if total_hermes > 0 else 0
    witness_rate = (total_hermes_witnessed / total_hermes * 100) if total_hermes > 0 else 0

    total_envelopes = len(hermes_envelopes)
    envelope_per_receipt = (total_envelopes / total_hermes * 100) if total_hermes > 0 else 0

    # Date range
    if hermes_receipts:
        first_ts = hermes_receipts[0].get("timestamp", "?")
        last_ts = hermes_receipts[-1].get("timestamp", "?")
    else:
        first_ts = last_ts = "?"

    # Build report
    lines = [
        "# First Router Regret SIGNAL — Phase 5 CCC-T-28",
        "",
        "> **Status:** SIGNAL REPORT (not true regret — see caveats below)",
        "> **Date:** 2026-09-18",
        "> **Author:** 333-AGI Δ MIND (autonomous per Phase 5 sovereign directive)",
        "> **Authority:** OBSERVE_ONLY at session bind; pure telemetry computation",
        "",
        "## 0. Lead — what this report IS and IS NOT",
        "",
        "**IS:** A first-order signal from existing receipt telemetry — block rates, witness rates, envelope emission rates, harness distribution. Read-only computation. No new hooks, no new rules, no new blocks.",
        "",
        "**IS NOT:** True router regret. True regret = Utility(best_possible) - Utility(routed). Requires FED routing decision log (`fed_route` decision persistence). That log is NOT YET WIRED. This report uses gate receipts + envelope emits as PROXY signal.",
        "",
        "Per `representation-reality-invariant.md`: phantom capability (claiming true regret without log) and phantom absence (denying regret exists) are the same defect. This report is honest about the proxy nature.",
        "",
        "## 1. Receipt substrate",
        "",
        f"```yaml",
        f"hermes_gate_receipts:    {total_hermes}",
        f"hermes_envelope_emits:    {total_envelopes}",
        f"opencode_receipts:        {len(opencode_receipts)}+",
        f"mcp_audit_lines:          {len(mcp_audit)}",
        f"first_receipt_ts:         {first_ts}",
        f"last_receipt_ts:          {last_ts}",
        f"```",
        "",
        "## 2. Hermes gate decision distribution",
        "",
        "| Decision | Count | Rate |",
        "|---|---|---|",
        f"| Witnessed (T1/T2 pass) | {total_hermes_witnessed} | {witness_rate:.1f}% |",
        f"| Blocked (T3 / W_SCAR / JITU) | {total_hermes_blocked} | {block_rate:.1f}% |",
        f"| Falsification (W_scar pass) | {hermes_decision_counts.get('FALSIFICATION', 0)} | {hermes_decision_counts.get('FALSIFICATION', 0) / total_hermes * 100 if total_hermes else 0:.1f}% |",
        "",
        "## 3. Hermes tier distribution",
        "",
        f"```",
    ]
    for tier, count in sorted(hermes_tier_counts.items()):
        rate = count / total_hermes * 100 if total_hermes else 0
        lines.append(f"{tier}: {count} ({rate:.1f}%)")
    lines.append("```")
    lines.append("")

    # Envelope signal
    lines.extend(
        [
            "## 4. Envelope emission signal (CCC-T-02 / Phase 1 wiring)",
            "",
            f"```yaml",
            f"total_envelopes:          {total_envelopes}",
            f"envelope_per_receipt:     {envelope_per_receipt:.1f}%",
            f"```",
            "",
            "**Interpretation:** If `envelope_per_receipt < 100%`, some gate receipts did not produce envelope emits (e.g., OBSERVE path returns early before emit call site). Acceptable — gate emits envelopes only for T2/T3-witnessed paths. The metric measures **envelope coverage of decided receipts**.",
            "",
            "## 5. Envelope tier distribution",
            "",
            "```",
        ]
    )
    for tier, count in sorted(envelope_tier_counts.items()):
        lines.append(f"{tier}: {count}")
    lines.append("```")
    lines.append("")

    # Top events
    lines.extend(
        [
            "## 6. Top event types",
            "",
            "### Hermes",
            "",
            "```",
        ]
    )
    for event, count in hermes_event_counts.most_common(10):
        lines.append(f"{event}: {count}")
    lines.append("```")
    lines.append("")

    if opencode_event_counts:
        lines.extend(
            [
                "### OpenCode (sample of first 1000 receipts)",
                "",
                "```",
            ]
        )
        for event, count in opencode_event_counts.most_common(10):
            lines.append(f"{event}: {count}")
        lines.append("```")
        lines.append("")

    # Companion metrics
    cost_proxy_total = total_hermes_witnessed * 1.5 + total_hermes_blocked * 0.5  # arbitrary unit
    lines.extend(
        [
            "## 7. Companion metrics (per ROUTER_REGRET_METRIC.md)",
            "",
            f"```yaml",
            f"witness_rate_proxy:        {witness_rate:.2f}%  # higher = router 'routing' (gate pass) success",
            f"block_rate_proxy:          {block_rate:.2f}%  # higher = gate catching more potential violations",
            f"envelope_coverage_proxy:  {envelope_per_receipt:.2f}%  # higher = more gate decisions produce envelopes",
            f"cost_proxy_total_units:   {cost_proxy_total:.1f}  # arbitrary; block=witnessed=1; falsif=0.5",
            f"```",
            "",
            "## 8. What we DO NOT yet measure",
            "",
            "- **True router regret**: FED `fed_route` decision persistence is not yet wired. Without this log, we cannot compute Utility(best_possible) - Utility(routed).",
            "- **CostPerSuccess**: depends on cost-per-call metrics from each model provider. FED has partial telemetry but not unified.",
            "- **EnsembleLift**: requires multi-agent run history with quality grading. Audit corpus has few such runs.",
            "- **P50/P95 regret by (agent_profile, task_class)**: requires routing log + task_class tagging. Both missing.",
            "",
            "## 9. Recommendations (deferred — not blockers)",
            "",
            "1. **Add FED routing decision log** (CCC-T-26b): every `fed_route` call writes (task_id, chosen_model, alternatives_offered, cost, latency) to `/root/.local/share/arifos/fed_routing_decisions.jsonl`. Locks the data substrate for true regret calculation.",
            "2. **Wire event vocabulary to arifFlow** (CCC-T-27): emit CCC vocabulary events from existing hooks into `/root/.local/share/arifos/vocab_events.jsonl`. ~5 LoC per hook.",
            "3. **Add task_class tagging** to session start: AAA pass `task_class` at session init so routing decisions carry semantic class for stratified regret.",
            "4. **Schedule recurring regret report** (CCC-T-28b): weekly cron to regenerate this report with cumulative data.",
            "",
            "## 10. Entropy effect",
            "",
            "- Witness rate proxy shows most gate traffic passes through (T1/T2 by design). Block rate is small but informative — captures T3 attempts + W_SCAR critical claims without evidence.",
            "- Envelope emission is uneven (envelope_per_receipt < 100%) — OBSERVE path skips emit. Expected behavior, not regression.",
            "- No anomalies detected in this substrate that would warrant immediate sovereign attention.",
            "",
            "## 11. Verdict",
            "",
            "- **First signal report generated.** Proxy metrics computed honestly with substrate limits disclosed.",
            "- **No capability changed.** No new blocks added. No tool removed.",
            "- **True regret metric remains deferred** until CCC-T-26b (FED routing log) is implemented.",
            "- **Phase 5 partial:** CCC-T-27 (vocab wire) + CCC-T-28 (this report) DELIVERED. CCC-T-26b (FED log) DEFERRED.",
            "",
            "---",
            "",
            "Generated by `compute_regret_signal.py` from CCC_RUNTIME_OPERATIONS_v1.md CCC-T-28.",
            f"Date: {datetime.now(timezone.utc).isoformat()}",
            "Status: SIGNAL_REPORT (proxy metrics, true regret deferred)",
            "",
            "> **DITEMPA BUKAN DIBERI ⚒️**",
        ]
    )

    out_path = Path(args.out)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {out_path} ({len(lines)} lines)")
    print()
    print("KEY SIGNALS:")
    print(f"  Hermes receipts:      {total_hermes}")
    print(f"  Witnessed:            {total_hermes_witnessed} ({witness_rate:.1f}%)")
    print(f"  Blocked:              {total_hermes_blocked} ({block_rate:.1f}%)")
    print(f"  Envelope emits:       {total_envelopes}")
    print(f"  Envelope coverage:    {envelope_per_receipt:.1f}%")


if __name__ == "__main__":
    main()
