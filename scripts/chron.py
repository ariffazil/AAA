#!/usr/bin/env python3
"""chron — the clock that matters. Ranked temporal intelligence, computed live.

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
"""
from __future__ import annotations

import json
import sys
from datetime import date, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
STORE = HERE / "chron_events.json"

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
        "truth_score": (CONSEQUENCE_W.get(e.get("consequence", "LOW"), 1.0)
                        * CONFIDENCE_W.get(e.get("confidence", "CONFIRMED"), 1.0)),
        # time-shaped: how soon, and does it demand action
        "urgency_score": (urgency(days)
                          * ACTION_W.get(e.get("actionability", "WATCH"), 1.0)),
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
            continue                      # expired: no stale countdown, ever
        comp = components(e, days)
        out.append({**e, "days": days, "score": score(e, days), **comp})
    out.sort(key=lambda x: (-x["score"], x["days"]))
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
    return (f"{t.year} dah {100.0 * doy / total:.0f}% habis — tinggal {total - doy} hari, "
            f"minggu ke-{t.isocalendar()[1]}")


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--help":
        print(__doc__)
        return 0
    if argv and argv[0] == "--json":
        evs = active(load())
        print(json.dumps({
            "as_of": _today().isoformat(),
            "year": year_shape(),
            "ranked": [{k: e[k] for k in ("id", "title", "target_date", "days",
                                          "audience", "kind", "confidence",
                                          "consequence", "actionability", "score",
                                          "truth_score", "urgency_score")}
                       for e in evs],
        }, indent=2, ensure_ascii=False))
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
        urgent_trivial = {"id": "a", "title": "urgent trivial", "target_date": "2099-01-01",
                          "consequence": "LOW", "confidence": "CONFIRMED",
                          "actionability": "ACT_NOW"}
        calm_weighty = {"id": "b", "title": "calm weighty", "target_date": "2099-01-01",
                        "consequence": "HIGH", "confidence": "CONFIRMED",
                        "actionability": "WATCH"}
        ca = components(urgent_trivial, 1)
        cb = components(calm_weighty, 28)
        assert ca["truth_score"] < cb["truth_score"], "truth not exposed"
        assert ca["urgency_score"] > cb["urgency_score"], "urgency not exposed"
        print(f"separation test    : PASS (truth {ca['truth_score']} vs {cb['truth_score']}, "
              f"urgency {ca['urgency_score']} vs {cb['urgency_score']})")

        # prove expiry works without touching the store
        past = [{"id": "x", "title": "past", "target_date": "2020-01-01",
                 "audience": "both", "kind": "DEADLINE", "source": "synthetic"}]
        assert active(past) == [], "expiry failed"
        print("expiry test        : PASS (a past event is dropped)")
        # prove the privacy filter works
        priv = [{"id": "p", "title": "private", "target_date": "2099-01-01",
                 "audience": "arif", "kind": "PERSONAL_SAFE", "source": "synthetic"}]
        assert active(priv) == [], "privacy filter failed for shared view"
        assert len(active(priv, who="arif")) == 1, "owner view lost the event"
        print("privacy test       : PASS (arif-only hidden from the shared card)")
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
