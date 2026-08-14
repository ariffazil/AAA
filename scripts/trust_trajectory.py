#!/usr/bin/env python3
"""
trust_trajectory.py — Trust-accretion detector (XZ / Jia Tan defence)
======================================================================
Detects the longitudinal social-engineering signature that static
injection defence cannot see: an agent that is genuinely helpful for a
long tenure, then concentrates authority requests late.

Signature: long-helpful -> then-asks-for-keys.
Evidence producer ONLY — verdicts are advisory input to arif_judge.
This module never grants, denies, or seals. It measures.

Composes with: VAULT999 ledgers, arifFlow receipts, lease/ACT grants.
Stdlib only. Zero new dependencies (Banda Haram: every pip install in a
trust auditor is the next XZ surface).

Honest limits (audit 2026-08-14, 333-AGI):
  - This is a SUCCESSION-EVENT detector: any long-tenured helper whose
    authority asks cluster late will trip SIGNATURE (late_share==1.0 by
    construction for single late asks). Discrimination comes from
    pressure_correlation + the judge. SIGNATURE is advisory evidence,
    NEVER a verdict.
  - Ledger timestamps are ADVERSARIAL metadata (XZ devil-craft #4:
    planted timeline artifacts framing someone else). Sanity bounds
    flag absurd inputs as LEDGER_ANOMALY instead of silently
    blessing them as BENIGN.

Event schema (JSONL, one per line):
  {"ts": "2026-01-05T12:00:00Z", "agent": "jia.tan",
   "event": "helpful_act|authority_request|key_grant|pressure_on_maintainer",
   "context": {...optional...}}
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime, timedelta, timezone


# Dynamic params via env (Banda Haram Hardcode doctrine) — sane defaults.
def _params():
    cfg = os.environ.get("TRUST_TRAJECTORY_CONFIG")
    p = {
        "min_tenure_days": 90,  # helpful tenure before authority ask flags signal
        "min_helpful_events": 20,  # enough history to be a real campaign
        "late_window_frac": 0.25,  # final quarter of tenure
        "late_concentration": 0.60,  # share of authority asks in late window
        "pressure_correlation_weight": 0.5,
        "max_tenure_days": 3650,  # sanity: >10y tenure = timestamps suspect
        "max_helpful_rate_per_week": 200,  # sanity: absurd density = synthetic ledger
        "pressure_window_days": 180,  # pressure counts only within window before first help
    }
    if cfg and os.path.exists(cfg):
        with open(cfg) as f:
            p.update(json.load(f))
    for k in p:
        env = os.environ.get("TT_" + k.upper())
        if env is not None:
            p[k] = type(p[k])(env)
    return p


EVENT_HELPFUL = "helpful_act"
EVENT_AUTH = "authority_request"
EVENT_GRANT = "key_grant"
EVENT_PRESSURE = "pressure_on_maintainer"


def _ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def load_events(path):
    events = []
    with open(path) as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                print(f"warn: line {ln} not JSON, skipped", file=sys.stderr)
                continue
            t = _ts(e.get("ts", ""))
            if t is None:
                continue
            events.append({"ts": t, "agent": e.get("agent", "?"), "event": e.get("event", "?"), "raw": e})
    events.sort(key=lambda x: x["ts"])
    return events


def analyze_agent(events, params):
    """Return evidence dict for one agent's trajectory."""
    first, last = events[0]["ts"], events[-1]["ts"]
    tenure_days = max((last - first).total_seconds() / 86400.0, 1e-9)
    helpful = [e for e in events if e["event"] == EVENT_HELPFUL]
    auth = [e for e in events if e["event"] == EVENT_AUTH]
    grants = [e for e in events if e["event"] == EVENT_GRANT]

    if not auth:
        auth_tenure_days, late_share = None, None
    else:
        first_auth = auth[0]["ts"]
        auth_tenure_days = (first_auth - first).total_seconds() / 86400.0
        # late window = final late_window_frac of full trajectory
        cutoff = first + (last - first) * (1 - params["late_window_frac"])
        late_n = sum(1 for e in auth if e["ts"] >= cutoff)
        late_share = late_n / len(auth) if auth else 0.0

    active_weeks = max(tenure_days / 7.0, 1e-9)
    helpful_rate = len(helpful) / active_weeks

    # Sanity bounds (audit 2026-08-14): ledger timestamps are adversarial
    # metadata. Absurd inputs must flag, never silently pass as BENIGN.
    anomaly = None
    if tenure_days > params["max_tenure_days"]:
        anomaly = (
            f"tenure {tenure_days:,.0f}d exceeds sanity bound "
            f"{params['max_tenure_days']}d — timestamps suspect (XZ devil-craft #4)"
        )
    elif helpful_rate > params["max_helpful_rate_per_week"]:
        anomaly = (
            f"helpful_rate {helpful_rate:.0f}/wk exceeds bound "
            f"{params['max_helpful_rate_per_week']} — synthetic ledger suspected"
        )

    ev = {
        "agent": events[0]["agent"],
        "window": [first.isoformat(), last.isoformat()],
        "tenure_days": round(tenure_days, 1),
        "helpful_events": len(helpful),
        "helpful_rate_per_week": round(helpful_rate, 2),
        "authority_requests": len(auth),
        "tenure_before_first_authority_ask_days": round(auth_tenure_days, 1) if auth_tenure_days is not None else None,
        "late_window_authority_share": round(late_share, 2) if late_share is not None else None,
        "key_grants": len(grants),
        "sanity": {"ok": anomaly is None, "note": anomaly},
    }

    # --- Jia Tan signature test (falsifiable) ---
    checks = {
        "long_helpful_tenure": (auth_tenure_days is not None and auth_tenure_days >= params["min_tenure_days"]),
        "sustained_helpfulness": len(helpful) >= params["min_helpful_events"],
        "late_authority_burst": (late_share is not None and late_share >= params["late_concentration"]),
    }
    ev["signature_checks"] = checks
    score = sum(checks.values()) / len(checks)
    ev["signal_score"] = round(score, 2)

    if anomaly is not None:
        ev["advisory"] = "LEDGER_ANOMALY"
    elif all(checks.values()):
        ev["advisory"] = "TRUST_ACCESSION_SIGNATURE"
    elif score >= 0.5:
        ev["advisory"] = "WATCH"
    else:
        ev["advisory"] = "BENIGN_TRAJECTORY"
    return ev


def pressure_correlation(all_events, params):
    """Sock-puppet precedent: pressure on maintainer BEFORE helper's first act."""
    helpers = {}
    for e in all_events:
        if e["event"] == EVENT_HELPFUL:
            helpers.setdefault(e["agent"], e["ts"])
    window = timedelta(days=params.get("pressure_window_days", 180))
    out = []
    for agent, first_help in helpers.items():
        prior_pressure = [
            p
            for p in all_events
            if p["event"] == EVENT_PRESSURE
            and p["ts"] < first_help
            and (first_help - p["ts"]) <= window
            and p["agent"] != agent
        ]
        if prior_pressure:
            out.append(
                {
                    "agent": agent,
                    "pressure_events_before_first_help": len(prior_pressure),
                    "latest_pressure_agent": prior_pressure[-1]["agent"],
                    "note": "maintainer pressure preceded helper appearance — "
                    "multi-account social-engineering indicator",
                }
            )
    return out


def main():
    ap = argparse.ArgumentParser(description="Trust-accretion trajectory auditor")
    ap.add_argument("ledger", help="JSONL event ledger path")
    ap.add_argument("--agent", help="analyze a single agent only")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()
    params = _params()

    events = load_events(a.ledger)
    if not events:
        print("error: no valid events", file=sys.stderr)
        sys.exit(2)

    by_agent = {}
    for e in events:
        by_agent.setdefault(e["agent"], []).append(e)

    results = []
    for agent, evs in sorted(by_agent.items()):
        if a.agent and agent != a.agent:
            continue
        if any(e["event"] != EVENT_PRESSURE for e in evs):
            results.append(analyze_agent(evs, params))

    correlations = pressure_correlation(events, params)
    pkg = {
        "module": "trust_trajectory",
        "version": "1.1.0",
        "ledger": a.ledger,
        "generated": datetime.now(timezone.utc).isoformat(),
        "params": params,
        "agents": results,
        "pressure_correlations": correlations,
        "role": "EVIDENCE_PRODUCER — verdicts belong to arif_judge (Gödel lock)",
    }
    if a.json:
        print(json.dumps(pkg, indent=2))
    else:
        print(f"trust_trajectory — {len(results)} agent(s)")
        for r in results:
            print(
                f"  {r['agent']:24s} {r['advisory']:26s} "
                f"helpful={r['helpful_events']:4d} auth={r['authority_requests']:3d} "
                f"tenure_before_ask={r['tenure_before_first_authority_ask_days']}d "
                f"late_share={r['late_window_authority_share']}"
            )
            if r["advisory"] == "TRUST_ACCESSION_SIGNATURE":
                print(f"    -> signature: {r['signature_checks']}")
            if r["advisory"] == "LEDGER_ANOMALY":
                print(f"    -> sanity: {r['sanity']['note']}")
        for c in correlations:
            print(
                f"  pressure-precedent: {c['agent']} "
                f"({c['pressure_events_before_first_help']} events before first help)"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
