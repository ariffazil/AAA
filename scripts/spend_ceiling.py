#!/usr/bin/env python3
"""spend_ceiling.py — U14 metered daily spend ceiling guard (sovereign-curated).

Gate-2 item 6 (FEDERATION-CONSTITUTIONAL-INVARIANTS-v1.1 U14, 2026-09-12).
Meters what already exists: token_bank.db/token_bank_spend carries per-call
rows with agent_id attribution + estimated_cost_usd (FED lane's own metering).
What was missing: a per-agent daily ceiling with alert semantics.

CONSTITUTIONAL SHAPE — the mechanism is the tool; the VALUES are sovereign
policy (U19: risk appetite belongs to F13). Ceilings live in
/root/AAA/governance/SPEND-CEILINGS.json and are set by F13 directive only
(empty = observe-only mode; nothing blocks).

Semantics:
  report                 today's spend by agent + model, unknown-attribution share
  check --agent A        rc=0 under/no-ceiling, rc=2 OVER ceiling (alert logged
                         to the sentinel's own fed_alerts.log surface)
Hard enforcement at the FED boundary + delegation_depth in ACT are scoped to
FED/kernel lanes (UL-007 do-not-cascade).

DITEMPA BUKAN DIBERI.
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

DB = "/root/.local/share/arifos/token_bank.db"
CEILINGS = Path("/root/AAA/governance/SPEND-CEILINGS.json")
ALERTS = Path("/root/.local/share/arifos/fed_alerts.log")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_ceilings():
    if not CEILINGS.exists():
        return None
    try:
        cfg = json.loads(CEILINGS.read_text())
    except json.JSONDecodeError as e:
        print(f"ERR ceilings config unparseable: {e}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(cfg.get("agents", {}), dict):
        print("ERR ceilings config: 'agents' must be an object", file=sys.stderr)
        sys.exit(1)
    for agent, cap in cfg.get("agents", {}).items():
        if not isinstance(cap, (int, float)) or cap < 0:
            print(f"ERR ceilings config: agent '{agent}' cap must be a non-negative number", file=sys.stderr)
            sys.exit(1)
    return cfg


def q(sql, params=()):
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    try:
        return con.execute(sql, params).fetchall()
    finally:
        con.close()


def do_report():
    last = q("SELECT MAX(called_at) FROM token_bank_spend")[0][0]
    by_agent = q(
        "SELECT agent_id, COUNT(*), ROUND(SUM(estimated_cost_usd),6) "
        "FROM token_bank_spend WHERE date(called_at)=? GROUP BY agent_id ORDER BY 3 DESC",
        (TODAY,),
    )
    by_model = q(
        "SELECT model_id, COUNT(*), ROUND(SUM(estimated_cost_usd),6) "
        "FROM token_bank_spend WHERE date(called_at)=? GROUP BY model_id ORDER BY 3 DESC LIMIT 10",
        (TODAY,),
    )
    total = q(
        "SELECT COUNT(*), ROUND(COALESCE(SUM(estimated_cost_usd),0),6) "
        "FROM token_bank_spend WHERE date(called_at)=?",
        (TODAY,),
    )[0]
    unknown = [r for r in by_agent if r[0] in (None, "", "unknown")]
    unknown_share = (unknown[0][2] if unknown else 0) / total[1] if total[1] else 0
    print(f"SPEND REPORT {TODAY} (UTC) — {total[0]} calls, ${total[1]:.4f} total")
    if not last:
        print("VOID GUARD — meter has NEVER ingested; $0 is absence of data, not absence of spend")
    else:
        age_h = None
        try:
            last_dt = datetime.fromisoformat(str(last).replace("Z", "+00:00"))
            age_h = (datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
        except ValueError:
            pass
        if age_h is None or age_h > 24:
            print(f"VOID GUARD — METER STALE: last ingest {last} (~{age_h:.0f}h ago)" if age_h is not None else f"VOID GUARD — METER STALE: last ingest {last}")
            print("  today's $0 reflects absence of DATA, not absence of spend (U13/U17)")
    print("by agent:")
    for a, n, c in by_agent:
        print(f"  {a or 'unknown':28} {n:5} calls  ${c:.4f}")
    print("by model (top 10):")
    for m, n, c in by_model:
        print(f"  {m:44} {n:5} calls  ${c:.4f}")
    if unknown_share > 0.2:
        print(f"WARN {unknown_share:.0%} of spend carries unknown/no attribution — ceiling per agent is partial until attribution is complete")


def do_check(agent):
    spent = q(
        "SELECT ROUND(COALESCE(SUM(estimated_cost_usd),0),6) FROM token_bank_spend "
        "WHERE date(called_at)=? AND agent_id=?",
        (TODAY, agent),
    )[0][0]
    cfg = load_ceilings()
    cap = (cfg or {}).get("agents", {}).get(agent)
    if cap is None:
        cap = (cfg or {}).get("default_daily_usd_cap") if cfg else None
    if cap is None:
        print(f"OBSERVE-ONLY — agent '{agent}' spent ${spent:.4f} today; no ceiling set (sovereign policy: SPEND-CEILINGS.json)")
        return 0
    if spent > cap:
        msg = f"[{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}] SPEND-CEILING BREACH agent={agent} spent=${spent:.4f} cap=${cap:.4f} (U14)"
        ALERTS.parent.mkdir(parents=True, exist_ok=True)
        with open(ALERTS, "a") as f:
            f.write(msg + "\n")
        print(msg)
        print("BLOCK-CLASS: over ceiling — reconcile with F13 before further spend (hard enforcement at FED boundary is the scoped kernel/FED work item)")
        return 2
    print(f"OK — agent '{agent}' spent ${spent:.4f} / ${cap:.4f} today ({100 * spent / cap:.0f}%)")
    return 0


def main():
    p = argparse.ArgumentParser(description="U14 daily spend ceiling guard (sovereign-curated values)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report")
    c = sub.add_parser("check")
    c.add_argument("--agent", required=True)
    args = p.parse_args()
    if args.cmd == "report":
        do_report()
    else:
        sys.exit(do_check(args.agent))


if __name__ == "__main__":
    main()
