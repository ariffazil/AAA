#!/usr/bin/env python3
"""CHRON Event Timers — OPEC, BNM MPC, FOMC, and EIA Storage Calendar.

Manages scheduled macro risk event timers:
  - FOMC Rate Decision & Press Conference (8 meetings/year)
  - BNM Monetary Policy Committee (MPC) OPR Statement (6 meetings/year)
  - OPEC+ Ministerial Meetings (JMMC / ONOMM)
  - EIA Weekly Natural Gas Storage (Every Thursday 10:30 ET / 22:30 MYT)
  - EIA Weekly Petroleum Status Report (Every Wednesday 10:30 ET / 22:30 MYT)

Computes temporal proximity, pre-event drift windows, and volatility expansion warnings.
Helps CHRON and WEALTH transition to "EVENT_RISK_ACTIVE" / SABAR state prior to high-impact releases.

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

MYT = timezone(timedelta(hours=8))
UTC = timezone.utc


@dataclass
class MacroEvent:
    event_id: str
    category: str  # FOMC | BNM | OPEC | EIA_GAS | EIA_OIL
    title: str
    scheduled_at_utc: str
    impacted_instruments: list[str]
    pre_event_window_hours: int = 12  # Hours before event where volatility warning triggers
    post_event_window_hours: int = 4   # Hours after event where price digest occurs
    description: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# Canonical 2026 Scheduled Events (FOMC, BNM, OPEC)
EVENT_REGISTRY: list[MacroEvent] = [
    # ── FOMC Meetings 2026 ──────────────────────────────────────────
    MacroEvent("FOMC_2026_09", "FOMC", "FOMC Rate Decision & Press Conference", "2026-09-16T18:00:00Z", ["GOLD", "USMYR", "OIL", "KLCI"], 24, 6, "Federal Reserve Interest Rate Decision"),
    MacroEvent("FOMC_2026_11", "FOMC", "FOMC Rate Decision & Press Conference", "2026-11-04T19:00:00Z", ["GOLD", "USMYR", "OIL", "KLCI"], 24, 6, "Federal Reserve Interest Rate Decision"),
    MacroEvent("FOMC_2026_12", "FOMC", "FOMC Rate Decision & Economic Projections", "2026-12-16T19:00:00Z", ["GOLD", "USMYR", "OIL", "KLCI"], 24, 6, "Year-end Fed Rate Decision & Dot Plot"),

    # ── BNM MPC Meetings 2026 ───────────────────────────────────────
    MacroEvent("BNM_2026_09", "BNM", "BNM Monetary Policy Committee (MPC) Statement", "2026-09-03T07:00:00Z", ["USMYR", "KLCI"], 12, 4, "Bank Negara Malaysia OPR Decision"),
    MacroEvent("BNM_2026_11", "BNM", "BNM Monetary Policy Committee (MPC) Statement", "2026-11-05T07:00:00Z", ["USMYR", "KLCI"], 12, 4, "Bank Negara Malaysia OPR Decision"),

    # ── OPEC+ Meetings 2026 ─────────────────────────────────────────
    MacroEvent("OPEC_2026_10", "OPEC", "OPEC+ Joint Ministerial Monitoring Committee (JMMC)", "2026-10-02T11:00:00Z", ["OIL", "GAS", "USMYR", "KLCI"], 48, 12, "OPEC+ Output Quota Review"),
    MacroEvent("OPEC_2026_12", "OPEC", "OPEC and non-OPEC Ministerial Meeting (Full)", "2026-12-01T10:00:00Z", ["OIL", "GAS", "USMYR", "KLCI"], 72, 24, "OPEC+ Annual Production Agreement"),

    # ── National Budget ─────────────────────────────────────────────
    MacroEvent("MY_BUDGET_2027", "BUDGET", "Belanjawan 2027 National Budget Announcement", "2026-10-09T08:00:00Z", ["KLCI", "USMYR", "OIL"], 24, 12, "Malaysian Parliament 2027 Fiscal Budget Delivery"),
]


def next_weekly_eia(category: str, from_dt: Optional[datetime] = None) -> MacroEvent:
    """Calculate the next recurring EIA release (Gas: Thu 10:30 ET; Oil: Wed 10:30 ET)."""
    if from_dt is None:
        from_dt = datetime.now(UTC)

    target_weekday = 2 if category == "EIA_OIL" else 3  # Wed=2, Thu=3
    days_ahead = target_weekday - from_dt.weekday()
    if days_ahead < 0 or (days_ahead == 0 and from_dt.hour >= 15):  # 10:30 ET is ~14:30 or 15:30 UTC
        days_ahead += 7

    target_date = from_dt.date() + timedelta(days=days_ahead)
    target_utc_str = f"{target_date.isoformat()}T14:30:00Z"

    if category == "EIA_GAS":
        return MacroEvent(
            event_id=f"EIA_GAS_{target_date.isoformat()}",
            category="EIA_GAS",
            title="EIA Weekly Natural Gas Storage Report",
            scheduled_at_utc=target_utc_str,
            impacted_instruments=["GAS"],
            pre_event_window_hours=4,
            post_event_window_hours=2,
            description="Weekly working gas in underground storage compared to 5-yr avg"
        )
    else:
        return MacroEvent(
            event_id=f"EIA_OIL_{target_date.isoformat()}",
            category="EIA_OIL",
            title="EIA Weekly Petroleum Status Report",
            scheduled_at_utc=target_utc_str,
            impacted_instruments=["OIL"],
            pre_event_window_hours=4,
            post_event_window_hours=2,
            description="Weekly US commercial crude and fuel stockpiles"
        )


def get_active_and_upcoming_events(
    now_dt: Optional[datetime] = None,
    lookahead_days: int = 30
) -> list[dict]:
    """Return all events within lookahead window or currently in risk window."""
    if now_dt is None:
        now_dt = datetime.now(UTC)

    events = list(EVENT_REGISTRY)
    # Add next weekly recurring EIA events
    events.append(next_weekly_eia("EIA_GAS", now_dt))
    events.append(next_weekly_eia("EIA_OIL", now_dt))

    results = []
    for ev in events:
        try:
            ev_dt = datetime.fromisoformat(ev.scheduled_at_utc.replace("Z", "+00:00"))
        except Exception:
            continue

        delta = ev_dt - now_dt
        hours_to_event = delta.total_seconds() / 3600.0

        # State determination
        if -ev.post_event_window_hours <= hours_to_event <= 0:
            status = "POST_EVENT_DIGEST"
        elif 0 < hours_to_event <= ev.pre_event_window_hours:
            status = "PRE_EVENT_RISK_ACTIVE"
        elif 0 <= delta.days <= lookahead_days:
            status = "UPCOMING"
        else:
            continue

        res = ev.to_dict()
        res["hours_until"] = round(hours_to_event, 1)
        res["status"] = status
        results.append(res)

    results.sort(key=lambda x: x["hours_until"])
    return results


def check_instrument_event_risk(instrument: str, now_dt: Optional[datetime] = None) -> dict:
    """Check if a specific instrument is currently under an active macro risk window."""
    inst = instrument.upper()
    if inst == "XAUUSD":
        inst = "GOLD"
    upcoming = get_active_and_upcoming_events(now_dt, lookahead_days=7)
    
    active_risks = [
        ev for ev in upcoming 
        if inst in ev["impacted_instruments"] and ev["status"] in ("PRE_EVENT_RISK_ACTIVE", "POST_EVENT_DIGEST")
    ]
    
    imminent = [
        ev for ev in upcoming
        if inst in ev["impacted_instruments"] and ev["hours_until"] > 0
    ]

    return {
        "instrument": inst,
        "risk_active": len(active_risks) > 0,
        "active_events": active_risks,
        "next_event": imminent[0] if imminent else None,
    }


if __name__ == "__main__":
    now = datetime.now(UTC)
    print(f"=== CHRON Macro Event Timers (UTC: {now.strftime('%Y-%m-%d %H:%M')}) ===")
    events = get_active_and_upcoming_events(now, lookahead_days=45)
    for ev in events:
        print(f"[{ev['status']}] {ev['title']} ({ev['scheduled_at_utc']})")
        print(f"  Target: {', '.join(ev['impacted_instruments'])} | Hours to event: {ev['hours_until']}h")
