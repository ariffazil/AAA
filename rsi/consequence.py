#!/usr/bin/env python3
"""consequence.py — PERSISTENCE OF CONSEQUENCE. The question the federation
has never been able to answer automatically:

    "Apa tingkah laku masa depan yang berubah akibat scar ini?"

F13 synthesis 2026-09-15:
    "Hermes bukan action-poor. Hermes juga bukan idea-poor.
     Hermes sebenarnya verification-poor … 424 patch seminggu kelihatan seperti
     diari … belum ada organ yang boleh menjawab soalan paling penting."
    "h(t) bukan learning metric — h(t) ialah Consequence Retention Metric.
     Adakah reality berjaya menginvois sistem?"

Method (falsifiable, no self-report):

  At promotion time, for each capability, record a BASELINE:
    occurrences of that pattern in the observation window immediately before.

  On every later run, re-measure the SAME pattern in the window AFTER promotion
  and compare. A promotion that does not move the recurrence of its own pattern
  produced no consequence, regardless of how good the receipt looked.

  | Verdict      | Condition                                  |
  |--------------|--------------------------------------------|
  | PERSISTED    | recurrence fell ≥ 50%                      |
  | PARTIAL      | recurrence fell, but < 50%                 |
  | NO_EFFECT    | recurrence unchanged (±10%)                |
  | REGRESSED    | recurrence rose                            |
  | PENDING      | less than one full observation window elapsed |

This is not a new organ. It is the arrow from promotion back to reality.
"""
from __future__ import annotations

import os

import atoms as A

CONSEQUENCE = os.path.join(A.STATE, "consequence.jsonl")
BASELINES = os.path.join(A.STATE, "baselines.json")
MIN_ELAPSED_FRACTION = 1.0   # must see ≥1 full window after the promotion


def _load_baselines() -> dict:
    import json
    if os.path.exists(BASELINES):
        try:
            return json.load(open(BASELINES, encoding="utf-8"))
        except Exception:
            pass
    return {}


def _save_baselines(b: dict) -> None:
    import json
    tmp = BASELINES + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(b, fh, indent=2, ensure_ascii=False)
    os.replace(tmp, BASELINES)


def _occurrences(store: dict, pattern_type: str, ts_from: str | None = None,
                 ts_to: str | None = None) -> int:
    """Measured recurrence of a pattern, optionally bounded by ISO timestamps."""
    total = 0
    for a in store.values():
        if a.get("pattern_type") != pattern_type:
            continue
        t = a.get("ts", "")
        if ts_from and t < ts_from:
            continue
        if ts_to and t > ts_to:
            continue
        total += max(1, a.get("frequency", 1))
    return total


def capture(atom: dict, store: dict, promotion_ts: str, window_days: int) -> dict:
    """Record the baseline the promotion will later be judged against.

    Only the FIRST promotion of a capability sets a baseline: re-baselining on
    every run would let the system quietly move its own goalposts.
    """
    cap = atom.get("target") or f"capability.{atom['pattern_type'].lower()}"
    baselines = _load_baselines()
    if cap in baselines:
        return baselines[cap]
    record = {
        "capability": cap,
        "pattern_type": atom["pattern_type"],
        "promoted_at": promotion_ts,
        "window_days": window_days,
        "baseline_occurrences": _occurrences(store, atom["pattern_type"]),
        "atom_id": atom["atom_id"],
        "layer": atom["layer"],
        "status": "PENDING",
    }
    baselines[cap] = record
    _save_baselines(baselines)
    A.append_jsonl(CONSEQUENCE, {"ts": promotion_ts, "event": "baseline_captured", **record})
    return record


def backfill(store: dict | None = None, now_ts: str | None = None) -> list[dict]:
    """Give every promoted capability a baseline, including ones promoted before
    this instrument existed.

    Honesty rule: a backfilled baseline is marked `backfilled: true` and its
    promoted_at is the backfill time, not the original promotion. A backfilled
    capability can therefore never claim a full-window consequence verdict for
    the period before its instrumentation existed — the window starts late.
    """
    import json
    from datetime import datetime, timezone

    store = store if store is not None else A.load_atoms()
    now = (datetime.fromisoformat(now_ts) if now_ts
           else datetime.now(timezone.utc).astimezone())
    g = A.load_graph()
    baselines = _load_baselines()
    made = []

    for cap, node in g["nodes"].items():
        if cap in baselines:
            continue
        atoms = [store[a] for a in node.get("atoms", []) if a in store]
        if not atoms:
            continue
        pattern = atoms[0]["pattern_type"]
        record = {
            "capability": cap,
            "pattern_type": pattern,
            "promoted_at": now.isoformat(timespec="seconds"),
            "window_days": 7,
            "baseline_occurrences": _occurrences(store, pattern),
            "atom_id": atoms[0]["atom_id"],
            "layer": node.get("layer", "capability"),
            "backfilled": True,
            "status": "PENDING",
        }
        baselines[cap] = record
        A.append_jsonl(CONSEQUENCE, {"ts": record["promoted_at"],
                                     "event": "baseline_backfilled", **record})
        made.append(record)

    if made:
        _save_baselines(baselines)
    return made


def assess(store: dict | None = None, now_ts: str | None = None) -> list[dict]:
    """Re-measure every baselined capability against the recurrence that followed.

    Called on every loop run. This is the only function in the loop that can
    answer "did the future change?" without asking the agent that made the change.
    """
    from datetime import datetime, timedelta, timezone

    store = store if store is not None else A.load_atoms()
    now = (datetime.fromisoformat(now_ts) if now_ts
           else datetime.now(timezone.utc).astimezone())
    baselines = _load_baselines()
    results = []

    for cap, b in baselines.items():
        promoted = datetime.fromisoformat(b["promoted_at"])
        window = timedelta(days=b["window_days"])
        elapsed = now - promoted

        if elapsed < window * MIN_ELAPSED_FRACTION:
            verdict, detail = "PENDING", (
                f"{elapsed.total_seconds()/86400:.2f}d elapsed of "
                f"{b['window_days']}d window — consequence not yet observable")
            after = None
        else:
            after = _occurrences(store, b["pattern_type"],
                                 ts_from=b["promoted_at"], ts_to=now.isoformat())
            before = max(1, b["baseline_occurrences"])
            delta = (after - before) / before
            if delta <= -0.5:
                verdict = "PERSISTED"
            elif delta < -0.1:
                verdict = "PARTIAL"
            elif delta <= 0.1:
                verdict = "NO_EFFECT"
            else:
                verdict = "REGRESSED"
            detail = (f"recurrence {before}→{after} ({delta:+.0%}) over "
                      f"{elapsed.total_seconds()/86400:.1f}d")

        row = {
            "ts": now.isoformat(timespec="seconds"),
            "capability": cap,
            "pattern_type": b["pattern_type"],
            "promoted_at": b["promoted_at"],
            "baseline_occurrences": b["baseline_occurrences"],
            "after_occurrences": after,
            "elapsed_days": round(elapsed.total_seconds() / 86400, 2),
            "verdict": verdict,
            "detail": detail,
        }
        results.append(row)
        b["status"] = verdict
        b["last_assessed"] = row["ts"]

    _save_baselines(baselines)
    if results:
        A.append_jsonl(CONSEQUENCE, {"ts": now.isoformat(timespec="seconds"),
                                     "event": "consequence_assessed",
                                     "results": results})
    return results


def summary(results: list[dict]) -> dict:
    from collections import Counter
    c = Counter(r["verdict"] for r in results)
    if not results:
        answer = "no capability baselined yet — consequence unmeasurable"
    elif set(c) == {"PENDING"}:
        answer = ("all baselines PENDING — no capability has yet been observed "
                  "long enough to prove a change in future behaviour")
    elif c.get("PERSISTED") or c.get("PARTIAL"):
        answer = "consequence proven: recurrence of the governing pattern fell"
    elif c.get("REGRESSED"):
        answer = "consequence negative: the governing pattern recurred more often after promotion"
    else:
        answer = "promotions applied, but no measurable change in future behaviour"
    return {"n": len(results), "by_verdict": dict(c), "answer": answer}


if __name__ == "__main__":
    import json
    rows = assess()
    print(json.dumps(summary(rows), indent=2))
    for r in rows:
        print(f"  {r['verdict']:<10} {r['capability']:<40} {r['detail']}")
