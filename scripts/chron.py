#!/usr/bin/env python3
"""chron — the clock that matters. Ranked temporal intelligence, computed live.

SINGLE STORE (2026-10-19):
  This script reads the canonical CHRON event store at /root/chron/chron_events.json
  and writes the canonical delivery ledger at /root/chron/data/chron_delivery.json.
  It no longer owns a copy. /root/AAA/scripts/chron_events.json is a symlink to the
  canonical store so old evidence paths still resolve to the same bytes.

WHAT CHANGED AND WHY
  v1 held three hardcoded milestones in Python and printed them in date order.
  That is a footer, not an intelligence surface. Three defects followed from it:

    1. Nearest-date ordering is not relevance. A trivial deadline three days out
       outranked a consequential one three weeks out.
    2. Nothing expired. A passed event would sit in the list until someone edited
       the file by hand.
    3. No audience field, so a private deadline could surface in a card the OTHER
       person reads. In a two-person group that is a disclosure, not a feature.

  v2 reads a canonical event store, computes every delta at render time, drops
  what has passed, and ranks by urgency x consequence x actionability.

THE LAW
  Never store "21 days". Store the date; compute the delta. A stored day-count is
  wrong the moment the file is not regenerated, and it fails silently — the card
  keeps saying 21 days a month later.

  Every event carries a source. A date with no provenance does not ship.

SHADOW GUARD (Phase 1 fix, 2026-09-21)
  chron.py is a SCRIPT, not a module. If any code in /root/AAA/scripts/ imports
  this file as `import chron`, it shadows the canonical chron package at
  /root/chron/ (the time-axis organ). The hermes cron jobs invoke this script
  via `python3 /root/AAA/scripts/chron.py` (script mode) so the shadow does not
  fire in production. But latent risk exists if a future script accidentally
  `import chron` from /root/AAA/scripts/ — it would load this file and miss
  chron_store, chron_prediction, etc.

  The guard below refuses module-mode import.   To get the canonical chron
  package, scripts in /root/AAA/scripts/ MUST set PYTHONPATH=/root so the
  package resolves to /root/chron/__init__.py.
"""

from __future__ import annotations

# Phase 1 — refuse module-mode import (shadow guard)
# See SHADOW GUARD docstring above. Only allow script-mode execution.
if __name__ != "__main__":
    raise RuntimeError(
        "/root/AAA/scripts/chron.py is a SCRIPT — module-mode import is refused.\n"
        "Reason: it would shadow the canonical chron package at /root/chron/.\n"
        "Fix: invoke as `python3 /root/AAA/scripts/chron.py` (script mode), "
        "or set PYTHONPATH=/root so `import chron` resolves to /root/chron/__init__.py."
    )

import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
STORE = Path("/root/chron/chron_events.json")
LEDGER = Path("/root/chron/data/chron_delivery.json")

# Default news window. An event that HAPPENED is news only while it is younger
# than this. Six hours is the honest default: half a waking day. A result that
# lands at 22:00 is still news at 07:00 the next morning; a result from the
# night before yesterday is not news, it is archive.
DEFAULT_DELIVERY_WINDOW_H = 6.0

CONSEQUENCE_W = {"HIGH": 3.0, "MEDIUM": 2.0, "LOW": 1.0}
ACTION_W = {"ACT_NOW": 3.0, "PREPARE": 2.0, "WATCH": 1.0}
CONFIDENCE_W = {"CONFIRMED": 1.0, "ANNOUNCED": 0.85, "TENTATIVE": 0.6}


def _today() -> date:
    return datetime.now().date()


def load(path: Path = STORE) -> list[dict]:
    try:
        d = json.loads(path.read_text())
        return d.get("events", [])
    except Exception as exc:  # noqa: BLE001
        print(f"chron: cannot read event store ({exc})", file=sys.stderr)
        return []


def urgency(days: int) -> float:
    """Low urgency far out, steep inside a week, saturating at the date.

    Deliberately not linear: a 10-day and an 11-day event are not meaningfully
    different, but a 1-day and a 10-day event are.
    """
    if days <= 0:
        return 4.0
    if days <= 3:
        return 3.5
    if days <= 7:
        return 3.0
    if days <= 14:
        return 2.4
    if days <= 30:
        return 1.8
    if days <= 90:
        return 1.2
    return 0.7


def components(e: dict, days: int) -> dict:
    """The score, DISASSEMBLED. Truth and time must not collapse into one number.

    WHY THIS EXISTS
      score() below returns a single float, and a single float cannot distinguish
      "urgent but trivial" from "calm but consequential" — both can land on the
      same value from opposite directions. A reader, or a later learner, then has
      no way to recover which one it was looking at.

      The seal: truth_score is independent, relevance is principal-specific, and
      urgency is time-specific. They may be COMBINED for ordering, but the parts
      must survive the combination.

      Nothing here changes ranking. it only stops the ranking from destroying
      information that the ranking was not entitled to consume.
    """
    return {
        # truth-shaped: does the claim hold, and how strongly
        "truth_score": (
            CONSEQUENCE_W.get(e.get("consequence", "LOW"), 1.0)
            * CONFIDENCE_W.get(e.get("confidence", "CONFIRMED"), 1.0)
        ),
        # time-shaped: how soon, and does it demand action
        "urgency_score": (urgency(days) * ACTION_W.get(e.get("actionability", "WATCH"), 1.0)),
        "consequence": e.get("consequence", "LOW"),
        "confidence": e.get("confidence", "CONFIRMED"),
        "actionability": e.get("actionability", "WATCH"),
        "days": days,
    }


def score(e: dict, days: int) -> float:
    """Ordering value, built from the exposed components. Never the only output."""
    c = components(e, days)
    return round(c["truth_score"] * c["urgency_score"], 4)


def active(events: list[dict], *, who: str | None = None) -> list[dict]:
    """Unexpired, unretired events visible to `who`, ranked.

    An event with audience 'arif' is invisible when rendering for the shared
    card. That filtering is the privacy contract, enforced here rather than
    trusted to whoever writes the prompt.
    """
    out = []
    today = _today()
    for e in events:
        if e.get("state", "ACTIVE") != "ACTIVE":
            continue
        if e.get("audience", "both") == "arif" and who != "arif":
            continue
        if e.get("audience") == "syed" and who != "syed":
            continue
        try:
            d = datetime.strptime(e["target_date"], "%Y-%m-%d").date()
        except (KeyError, ValueError):
            continue
        days = (d - today).days
        if days < 0:
            continue  # expired: no stale countdown, ever
        comp = components(e, days)
        out.append({**e, "days": days, "score": score(e, days), **comp})
    out.sort(key=lambda x: (-x["score"], x["days"]))
    return out


# ─────────────────────────────────────────────────────────────────────────────
# FRESHNESS — the other half of time
#
# WHY THIS EXISTS (failure observed, 2026-10-19, F13 verdict "Lambat la berita")
#   `active()` above answers one question only: how long UNTIL. It drops
#   anything with days < 0, so a thing that HAS happened has no home in the
#   store at all. Megat's Pro Card landed at ~22:00 on 18 Oct. The tracker
#   delivered it at 09:00 on 19 Oct, eleven hours later, in a group that had
#   already discussed it — and presented it as news.
#
#   That is not a scheduling bug. It is a missing axis. Time runs both ways,
#   and this store only knew one direction.
#
# THE LAW
#   An event that OCCURRED carries `occurred_at`, not only `target_date`.
#   Freshness is COMPUTED from occurred_at at read time — never stored as
#   "this is new". Age beyond the window is STALE, and STALE does not ship.
#   Delivery is recorded in a ledger so the same event is never "news" twice.
#
#   Age is measured to the second, in UTC. A news claim without a timestamp
#   is an opinion about recency, and opinions about recency are what failed.
# ─────────────────────────────────────────────────────────────────────────────


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def parse_when(raw: str) -> datetime | None:
    """Accept ISO-8601 with or without offset. Naive input is read as +08:00.

    The federation's humans live in Asia/Kuala_Lumpur and every human-authored
    timestamp in this store is local wall-clock. Treating a naive string as UTC
    would shift it eight hours into the future and make stale news look fresh —
    the exact defect this module exists to prevent. So: naive means +08:00.
    """
    if not raw or not isinstance(raw, str):
        return None
    s = raw.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))
    return dt.astimezone(timezone.utc)


def freshness(e: dict, *, now: datetime | None = None,
              default_window_h: float | None = None) -> dict | None:
    """Age in hours and whether the occurrence is still news. None if it never happened."""
    when = parse_when(e.get("occurred_at", ""))
    if when is None:
        return None
    now = now or _utcnow()
    window = e.get("delivery_window_hours")
    window = float(window) if window is not None else (
        default_window_h if default_window_h is not None else DEFAULT_DELIVERY_WINDOW_H
    )
    age_h = (now - when).total_seconds() / 3600.0
    if age_h < 0:
        # Occurrence in the future — cannot be news yet, and must not be
        # reported as though it already happened.
        state = "PENDING"
    elif age_h <= window:
        state = "FRESH"
    else:
        state = "STALE"
    return {
        "occurred_at_utc": when.isoformat(),
        "age_hours": round(age_h, 2),
        "window_hours": window,
        "state": state,
    }


def load_ledger(path: Path = LEDGER) -> list[dict]:
    try:
        d = json.loads(path.read_text())
        return d.get("deliveries", [])
    except Exception:  # noqa: BLE001 — a missing ledger is an empty ledger, not a crash
        return []


def save_ledger(deliveries: list[dict], path: Path = LEDGER) -> None:
    payload = {
        "_comment": "Append-only record of what CHRON has already told a human. "
                    "Presence here means the event is no longer news.",
        "deliveries": deliveries,
    }
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    tmp.replace(path)


def fresh_events(events: list[dict], *, who: str | None = None,
                 now: datetime | None = None,
                 default_window_h: float | None = None,
                 deliveries: list[dict] | None = None) -> list[dict]:
    """Occurrences that are still news: young enough, not yet delivered, visible to `who`."""
    seen = {d.get("event_id") for d in (deliveries if deliveries is not None else load_ledger())}
    now = now or _utcnow()
    out = []
    for e in events:
        f = freshness(e, now=now, default_window_h=default_window_h)
        if f is None or f["state"] != "FRESH":
            continue
        if e.get("id") in seen:
            continue
        if e.get("audience", "both") == "arif" and who != "arif":
            continue
        if e.get("audience") == "syed" and who != "syed":
            continue
        out.append({**e, "freshness": f})
    # youngest first: the newest thing is the most defensible "news"
    out.sort(key=lambda x: x["freshness"]["age_hours"])
    return out


def fmt(days: int) -> str:
    if days == 0:
        return "HARI NI"
    if days == 1:
        return "esok"
    if days < 31:
        return f"{days} hari"
    if days < 550:
        return f"{days // 30} bulan ({days} hari)"
    return f"{days / 365.25:.1f} tahun ({days} hari)"


def render(who: str | None = None, n: int = 3) -> str:
    evs = active(load(), who=who)
    if not evs:
        return "Tiada tarikh berhampiran disimpan."
    lines = [f"{e['title']} — {fmt(e['days'])}" for e in evs[:n]]
    return "\n".join(lines)


def year_shape() -> str:
    t = _today()
    doy = t.timetuple().tm_yday
    total = 366 if (t.year % 4 == 0 and (t.year % 100 != 0 or t.year % 400 == 0)) else 365
    return f"{t.year} dah {100.0 * doy / total:.0f}% habis — tinggal {total - doy} hari, minggu ke-{t.isocalendar()[1]}"


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--help":
        print(__doc__)
        print(
            "\nMODES\n"
            "  (no args)            ranked upcoming countdowns for the shared view\n"
            "  <who>                same, filtered to that audience\n"
            "  --json               machine-readable countdown payload\n"
            "  --fresh [--who X] [--window H] [--all]\n"
            "                       occurrences that are still NEWS: younger than the\n"
            "                       window, not yet delivered, visible to X. Exit 1 when\n"
            "                       there is nothing fresh — a cron can gate on it.\n"
            "                       --window sets the default for events that do not\n"
            "                       carry their own delivery_window_hours.\n"
            "  --mark-delivered ID [--channel C]\n"
            "                       record that ID has been told; it will never be\n"
            "                       reported as news again\n"
            "  --ledger             show what has already been delivered\n"
            "  --self-test          prove separation, expiry, privacy and freshness\n"
        )
        return 0
    if argv and argv[0] == "--fresh":
        who = None
        window = None
        show_all = False
        rest = argv[1:]
        i = 0
        while i < len(rest):
            if rest[i] == "--who" and i + 1 < len(rest):
                who = rest[i + 1]; i += 2
            elif rest[i] == "--window" and i + 1 < len(rest):
                window = float(rest[i + 1]); i += 2
            elif rest[i] == "--all":
                show_all = True; i += 1
            else:
                i += 1
        evs = fresh_events(load(), who=who, default_window_h=window)
        print(
            json.dumps(
                {
                    "as_of_utc": _utcnow().isoformat(),
                    "default_window_hours": window if window is not None else DEFAULT_DELIVERY_WINDOW_H,
                    "count": len(evs),
                    "fresh": [
                        {
                            k: e.get(k)
                            for k in ("id", "title", "kind", "audience", "source", "note")
                        }
                        | {"freshness": e["freshness"]}
                        for e in evs
                    ],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        # Non-zero when nothing is fresh: the honest answer to "what's new" is
        # sometimes "nothing", and a caller that cannot tell the difference will
        # invent content to fill the silence.
        return 0 if evs else 1
    if argv and argv[0] == "--mark-delivered":
        if len(argv) < 2:
            print("chron: --mark-delivered needs an event id", file=sys.stderr)
            return 2
        event_id = argv[1]
        channel = None
        if "--channel" in argv:
            idx = argv.index("--channel")
            if idx + 1 < len(argv):
                channel = argv[idx + 1]
        known = {e.get("id") for e in load()}
        if event_id not in known:
            print(f"chron: unknown event id {event_id!r} — refusing to ledger it", file=sys.stderr)
            return 2
        d = load_ledger()
        if any(x.get("event_id") == event_id for x in d):
            print(f"chron: {event_id} already delivered — no duplicate written", file=sys.stderr)
            return 0
        e = next(x for x in load() if x.get("id") == event_id)
        f = freshness(e) or {}
        d.append(
            {
                "event_id": event_id,
                "delivered_at_utc": _utcnow().isoformat(),
                "channel": channel or "unspecified",
                "age_hours_at_delivery": f.get("age_hours"),
                "freshness_state_at_delivery": f.get("state"),
            }
        )
        save_ledger(d)
        print(f"chron: marked {event_id} delivered ({len(d)} total)")
        return 0
    if argv and argv[0] == "--ledger":
        d = load_ledger()
        print(json.dumps({"count": len(d), "deliveries": d}, indent=2, ensure_ascii=False))
        return 0
    if argv and argv[0] == "--json":
        evs = active(load())
        print(
            json.dumps(
                {
                    "as_of": _today().isoformat(),
                    "year": year_shape(),
                    "ranked": [
                        {
                            k: e[k]
                            for k in (
                                "id",
                                "title",
                                "target_date",
                                "days",
                                "audience",
                                "kind",
                                "confidence",
                                "consequence",
                                "actionability",
                                "score",
                                "truth_score",
                                "urgency_score",
                            )
                        }
                        for e in evs
                    ],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0
    if argv and argv[0] == "--self-test":
        evs = load()
        print(f"events loaded      : {len(evs)}")
        print(f"active (shared)    : {len(active(evs))}")
        print(f"active (arif)      : {len(active(evs, who='arif'))}")
        print(f"active (syed)      : {len(active(evs, who='syed'))}")

        # Truth and time must be SEPARABLE. Two events can share one blended
        # score from opposite directions; if the parts were destroyed by the
        # blend, a reader cannot tell which is which. This test constructs that
        # exact collision and requires the components to resolve it.
        urgent_trivial = {
            "id": "a",
            "title": "urgent trivial",
            "target_date": "2099-01-01",
            "consequence": "LOW",
            "confidence": "CONFIRMED",
            "actionability": "ACT_NOW",
        }
        calm_weighty = {
            "id": "b",
            "title": "calm weighty",
            "target_date": "2099-01-01",
            "consequence": "HIGH",
            "confidence": "CONFIRMED",
            "actionability": "WATCH",
        }
        ca = components(urgent_trivial, 1)
        cb = components(calm_weighty, 28)
        assert ca["truth_score"] < cb["truth_score"], "truth not exposed"
        assert ca["urgency_score"] > cb["urgency_score"], "urgency not exposed"
        print(
            f"separation test    : PASS (truth {ca['truth_score']} vs {cb['truth_score']}, "
            f"urgency {ca['urgency_score']} vs {cb['urgency_score']})"
        )

        # prove expiry works without touching the store
        past = [
            {
                "id": "x",
                "title": "past",
                "target_date": "2020-01-01",
                "audience": "both",
                "kind": "DEADLINE",
                "source": "synthetic",
            }
        ]
        assert active(past) == [], "expiry failed"
        print("expiry test        : PASS (a past event is dropped)")
        # prove the privacy filter works
        priv = [
            {
                "id": "p",
                "title": "private",
                "target_date": "2099-01-01",
                "audience": "arif",
                "kind": "PERSONAL_SAFE",
                "source": "synthetic",
            }
        ]
        assert active(priv) == [], "privacy filter failed for shared view"
        assert len(active(priv, who="arif")) == 1, "owner view lost the event"
        print("privacy test       : PASS (arif-only hidden from the shared card)")

        # ── freshness: the exact failure this axis was built for ──────────────
        # Megat's Pro Card landed ~22:00 on 18 Oct; the tracker spoke at 09:00
        # on 19 Oct. Eleven hours. Under a 6h window that must read STALE.
        one = {
            "id": "megat-procard",
            "title": "Megat Pro Card",
            "occurred_at": "2026-10-18T22:00:00+08:00",
            "kind": "PUBLIC_EVENT",
            "audience": "both",
            "source": "IFBB Pro winners page, 18 Oct 2026",
        }
        at_0900_next_day = datetime(2026, 10, 19, 1, 0, tzinfo=timezone.utc)  # 09:00 MYT
        f_stale = freshness(one, now=at_0900_next_day)
        assert f_stale["state"] == "STALE", f"11h-old news read as {f_stale['state']}"
        print(
            f"freshness (late)   : PASS (11h old -> {f_stale['state']}, "
            f"age {f_stale['age_hours']}h > window {f_stale['window_hours']}h)"
        )

        at_same_night = datetime(2026, 10, 18, 14, 30, tzinfo=timezone.utc)  # 22:30 MYT
        f_fresh = freshness(one, now=at_same_night)
        assert f_fresh["state"] == "FRESH", f"30min-old news read as {f_fresh['state']}"
        print(f"freshness (same day): PASS (0.5h old -> {f_fresh['state']})")

        # naive timestamps are local wall-clock, not UTC. If this were read as
        # UTC the occurrence would jump 8h into the future and never go stale.
        naive = {**one, "occurred_at": "2026-10-18T22:00:00"}
        assert freshness(naive, now=at_0900_next_day)["state"] == "STALE", "naive TZ mishandled"
        print("freshness (naive TZ): PASS (naive read as +08:00, still goes stale)")

        # a delivered event is never news twice
        got = fresh_events([one], now=at_same_night, deliveries=[])
        assert len(got) == 1, "fresh event not surfaced"
        got2 = fresh_events(
            [one], now=at_same_night,
            deliveries=[{"event_id": "megat-procard"}],
        )
        assert got2 == [], "delivered event resurfaced as news"
        print("delivery ledger    : PASS (delivered event does not resurface)")

        # an occurrence in the future is not news yet
        fut = {**one, "occurred_at": "2026-10-25T22:00:00+08:00"}
        assert freshness(fut, now=at_same_night)["state"] == "PENDING", "future occurrence shipped as news"
        print("freshness (future) : PASS (not-yet-happened is PENDING, never FRESH)")
        print()
        print("RENDER (shared view):")
        print(render())
        print()
        print(year_shape())
        return 0
    who = argv[0] if argv else None
    print(render(who))
    print(year_shape())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
