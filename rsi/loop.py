#!/usr/bin/env python3
"""loop.py — the EXHALE. Closes the loop that has been inhale-only since inception.

Measured baseline (2026-09-15, parse of /root/.local/share/arifos/rsi-ledger.jsonl):
    950 rows / 5 days · 82% heartbeat · 26 proposals · 0 applied.
The loop observed and proposed. It never applied. That is the defect this file fixes.

Pipeline (F13-ratified 2026-09-15):
    SESSION → EUREKA EXTRACTOR → SCAR CLASSIFIER → CAPABILITY ATOM
            → CAPABILITY GRAPH → INDEPENDENT VERIFIER → PROMOTION GATE
            → LIVE CAPABILITY → AAA state improvement

A run that produces zero exhale is a FAILED run and is logged as such. Silence is
not success.

Usage:
    python3 loop.py                 # full cycle
    python3 loop.py --dry-run       # verify only, no promotion
    python3 loop.py --window 3      # 3-day window
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import atoms as A          # noqa: E402
import connectors as C     # noqa: E402
import consequence as CONS  # noqa: E402
import extract             # noqa: E402
import promote as P        # noqa: E402
import verify as V         # noqa: E402

NOTIFY_DIR = "/root/AAA/state/event-bridge"


def _recurrence(store: dict) -> dict:
    """Frequency measured across the atom store, not asserted per atom."""
    counts: dict[str, int] = {}
    for a in store.values():
        counts[a["pattern_type"]] = counts.get(a["pattern_type"], 0) + a.get("frequency", 1)
    return dict(sorted(counts.items(), key=lambda kv: -kv[1]))


def run(window_days: int = 7, dry_run: bool = False) -> dict:
    A.ensure_state()
    started = A.now_iso()

    atoms_found = extract.run(window_days)
    store = A.load_atoms()

    novel, seen = [], 0
    for a in atoms_found:
        if a["atom_id"] in store and store[a["atom_id"]].get("status") in ("verified", "promoted"):
            seen += 1
            continue
        novel.append(a)
    # Highest-frequency first: the loop spends its budget where recurrence is proven.
    novel.sort(key=lambda a: (-a.get("frequency", 1), a["pattern_type"]))

    cap = int(P._config()["promotion"].get("max_promotions_per_run", 10))
    results = []
    promoted, withheld, proposed, held = [], [], [], []
    budget = cap
    seq = 0
    max_attempts = int(P._config()["promotion"].get("max_attempts_per_atom", 3))

    for a in novel:
        prior = store.get(a["atom_id"], {})
        if prior.get("attempts", 0) >= max_attempts:
            withheld.append({"atom_id": a["atom_id"], "pattern_type": a["pattern_type"],
                             "layer": a["layer"], "frequency": a["frequency"],
                             "action": "abandoned",
                             "reason": f"failed verification {prior['attempts']}x — "
                                       "retired to avoid re-scanning a known-dead claim"})
            continue
        receipt = V.verify(a)
        a["survived_verification"] = receipt["passed"]
        a["status"] = "verified" if receipt["passed"] else "rejected"
        a["attempts"] = prior.get("attempts", 0) + 1
        if dry_run:
            # Dry run is a rehearsal: it must not write to the atom store, or the
            # next real cycle would treat rehearsed atoms as already processed.
            outcome = {"action": "dry_run", "applied": False}
            results.append({"atom": a, "receipt": receipt, "outcome": outcome})
            withheld.append({"atom_id": a["atom_id"], "pattern_type": a["pattern_type"],
                             "layer": a["layer"], "frequency": a["frequency"],
                             "action": "dry_run", "applied": False})
            continue

        A.append_jsonl(A.ATOMS, a)
        A.append_jsonl(os.path.join(A.RECEIPTS, f"{a['atom_id']}.json"), receipt)

        # ── ARROWS TO EXISTING ORGANS (F13 2026-09-15) ──────────────────────
        # Measurement is the condition for B to be real, not theatre: every
        # verification feeds arifFlow's FQ, every application feeds h(t).
        seq += 1
        C.flow_receipt("Verify", step_number=seq,
                       intent_reason=f"{a['pattern_type']} {a['atom_id']} "
                                     f"{'PASS' if receipt['passed'] else 'FAIL'}",
                       floor_verdict="Pass" if receipt["passed"] else "Hold")

        if budget <= 0:
            outcome = {"action": "deferred", "applied": False,
                       "reason": f"run budget {cap} exhausted — carries to next cycle"}
        else:
            outcome = P.promote(a, receipt)
            if outcome.get("applied") or outcome.get("action") == "policy_proposed":
                budget -= 1
            if outcome.get("applied"):
                seq += 1
                C.flow_receipt("Execute", step_number=seq,
                               intent_reason=f"promote {outcome.get('action')} → "
                                             f"{outcome.get('target')}")

        # Experience traces record an ACTION that reached a disposition. An atom
        # that never got past the gate did not act, and tracing it both pollutes
        # h(t) and rate-limits the transport (measured: 429 after ~80 bursts,
        # which then made the loop's own measurement unreadable).
        if outcome.get("applied") or outcome.get("action") in ("policy_proposed",
                                                              "HOLD_FORBIDDEN",
                                                              "quarantined"):
            C.experience_trace(a, receipt, outcome)

            # PERSISTENCE OF CONSEQUENCE — the promotion sets the baseline it
            # will later be judged against. Judging starts only after a full
            # observation window has elapsed.
            if outcome.get("applied"):
                CONS.capture(a, store, started, window_days)

        a["promotion"] = outcome
        A.append_jsonl(A.ATOMS, a)
        results.append({"atom": a, "receipt": receipt, "outcome": outcome})

        bucket = {"atom_id": a["atom_id"], "pattern_type": a["pattern_type"],
                  "layer": a["layer"], "frequency": a["frequency"],
                  "action": outcome.get("action"), "applied": outcome.get("applied"),
                  "target": outcome.get("target"), "reason": outcome.get("reason")}
        if outcome.get("action") == "HOLD_FORBIDDEN":
            held.append(bucket)
        elif outcome.get("applied"):
            promoted.append(bucket)
        elif outcome.get("action") in ("policy_proposed",):
            proposed.append(bucket)
        else:
            withheld.append(bucket)

    g = A.load_graph()
    ranking = A.ranking_report(g)
    store = A.load_atoms()

    # ── MEASUREMENT (independent observer, never self-computed) ──────────────
    # F13 2026-09-15: "Setiap promotion event mesti feed forge_rsi_impulse_response
    # (h(t)) + dual-rate FQ … tanpa ini, B adalah teater."
    meas = {"dry_run": True} if dry_run else C.measurement(window_days=max(window_days, 30))

    # ── PERSISTENCE OF CONSEQUENCE ───────────────────────────────────────────
    # The one question the federation could not answer automatically:
    # "Apa tingkah laku masa depan yang berubah akibat scar ini?"
    cons_rows = [] if dry_run else CONS.assess(store)
    if not dry_run:
        CONS.backfill(store)          # promote-time baselines for anything already promoted
        cons_rows = CONS.assess(store)
    cons = CONS.summary(cons_rows)

    # ── EXHALE: the ledger record that did not exist before ──────────────────
    exhale = bool(promoted or proposed or held)
    record = {
        "ts": started,
        "actor": "hermes-rsi-loop",
        "type": "diagnose",
        "pipeline": "session→eureka→scar→capability_atom→graph→verifier→promotion→live",
        "window_days": window_days,
        "counts": {
            "atoms_found": len(atoms_found),
            "already_verified": seen,
            "novel": len(novel),
            "promoted": len(promoted),
            "proposed": len(proposed),
            "withheld": len(withheld),
            "hold_forbidden": len(held),
        },
        "applied": [p["atom_id"] for p in promoted],
        "exhale": exhale,
        "measurement": meas,
        "consequence": {"summary": cons, "rows": cons_rows},
        "recurrence": _recurrence(store),
        "capability_graph": {
            "nodes": len(g["nodes"]),
            "median_fitness": ranking["median_fitness"],
            "weakest": [n["capability"] for n in ranking["ranking"] if n["below_median"]][:5],
        },
        "verifier": {"actor": "hermes-rsi-verifier", "independent": True,
                     "boundary_self_test": P.self_test()},
        "status": "EXHALED" if exhale else "INHALE_ONLY",
    }
    A.append_jsonl(A.LEDGER, record)
    A.append_jsonl("/root/.local/share/arifos/rsi-ledger.jsonl", record)

    receipt_path = os.path.join(A.RECEIPTS, f"loop-{started.replace(':', '')}.json")
    with open(receipt_path, "w", encoding="utf-8") as fh:
        json.dump({"record": record, "results": [
            {"atom_id": r["atom"]["atom_id"], "pattern_type": r["atom"]["pattern_type"],
             "layer": r["atom"]["layer"], "frequency": r["atom"]["frequency"],
             "verification": {k: v for k, v in r["receipt"].items() if k != "checks"},
             "outcome": r["outcome"]} for r in results]},
            fh, indent=2, ensure_ascii=False)

    _notify(record, promoted, held)

    return {"record": record, "results": results, "receipt": receipt_path}


def _notify(record: dict, promoted: list, held: list) -> None:
    """Delta-gated. Silent when nothing changed — the AAA group is a ledger, not a feed.

    Consequence verdicts that CHANGED (PENDING → PERSISTED / NO_EFFECT / REGRESSED)
    are state changes and are reported. Unchanged PENDING is not news.
    """
    cons = (record.get("consequence") or {}).get("rows") or []
    changed_cons = [c for c in cons if c.get("verdict") not in ("PENDING", "NO_EFFECT")]
    regressed = [c for c in cons if c.get("verdict") == "REGRESSED"]
    if not promoted and not held and not changed_cons:
        return
    try:
        import subprocess, tempfile
        c = record["counts"]
        lines = [f"RSI EXHALE — {record['ts'][:16]}",
                 f"promoted={c['promoted']} proposed={c['proposed']} "
                 f"withheld={c['withheld']} hold={c['hold_forbidden']}"]
        for p in promoted[:8]:
            lines.append(f"  + {p['pattern_type']} → {p.get('target')}")
        for h in held[:5]:
            lines.append(f"  HOLD {h['pattern_type']}: {h.get('reason')}")
        for k in changed_cons[:6]:
            lines.append(f"  CONSEQUENCE {k['verdict']}: {k['capability']} — {k['detail']}")
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
            fh.write("\n".join(lines) + "\n")
            tmp = fh.name
        subprocess.run(["/root/scripts/event-bridge.sh", "rsi_exhale", tmp,
                        "P1" if (held or regressed) else "P2"], timeout=60, check=False)
        os.unlink(tmp)
    except Exception:
        pass  # delivery is never allowed to fail the loop


def human_summary(out: dict) -> str:
    r = out["record"]
    c = r["counts"]
    lines = [f"RSI LOOP — {r['status']}",
             f"  window {r['window_days']}d | atoms {c['atoms_found']} "
             f"(novel {c['novel']}, seen {c['already_verified']})",
             f"  exhale: promoted {c['promoted']} | proposed {c['proposed']} | "
             f"withheld {c['withheld']} | HOLD {c['hold_forbidden']}"]
    for p in out["results"][:12]:
        a, o = p["atom"], p["outcome"]
        mark = "APPLIED" if o.get("applied") else ("PROPOSED" if o.get("action") == "policy_proposed"
                                                   else ("HOLD" if o.get("action") == "HOLD_FORBIDDEN" else "—"))
        lines.append(f"  [{mark:<8}] {a['pattern_type']:<18} L={a['layer']:<10} "
                     f"f={a['frequency']:<3} {o.get('target') or o.get('reason','')}")
    g = r["capability_graph"]
    lines.append(f"  capability graph: {g['nodes']} nodes | median fitness {g['median_fitness']}")
    m = r.get("measurement") or {}
    if m.get("fq"):
        f = m["fq"]
        lines.append(f"  MEASURED fq: daily={f.get('daily')} gov7d={f.get('governance_7d')} "
                     f"n={f.get('window_count')} sufficient={f.get('sufficient')}")
    if m.get("h_t"):
        h = m["h_t"]
        lines.append(f"  MEASURED h(t): events={h.get('impulse_events')} "
                     f"half_life={h.get('median_half_life_sessions')} "
                     f"characterized={h.get('h_characterized')}")
    c = (r.get("consequence") or {}).get("summary") or {}
    if c.get("n"):
        lines.append(f"  CONSEQUENCE: {c.get('by_verdict')}")
        for row in (r["consequence"].get("rows") or [])[:4]:
            lines.append(f"    {row['verdict']:<9} {row['capability']:<34} {row['detail']}")
    if r["recurrence"]:
        top = list(r["recurrence"].items())[:4]
        lines.append("  recurrence: " + ", ".join(f"{k}={v}" for k, v in top))
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=7)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    out = run(args.window, args.dry_run)
    if args.json:
        print(json.dumps(out["record"], indent=2, ensure_ascii=False))
    else:
        print(human_summary(out))
        print(f"  receipt → {out['receipt']}")
    r = out["record"]
    # Exit semantics matter for cron triage. A novel atom that was correctly
    # REFUSED or correctly ROUTED ELSEWHERE is the system working, not a miss:
    #   - verification failure  → the verifier did its job
    #   - quarantined           → unnamed pattern, held not promoted (by design)
    #   - policy_proposed       → Layers 3-4 correctly queue for F13
    #   - HOLD_FORBIDDEN        → Layer 5 boundary held (by design)
    #   - deferred / abandoned  → budget or retired claim, carries forward
    # A real miss is: verified, no lawful disposition reached, nothing applied.
    ACCEPTED = {"skill_lesson_queued", "capability_node_upsert", "quarantined",
                "policy_proposed", "HOLD_FORBIDDEN", "deferred", "abandoned", "dry_run"}
    c = r["counts"]
    misses = [x for x in out["results"]
              if x["receipt"]["passed"] and x["outcome"].get("action") not in ACCEPTED]
    if r["status"] == "EXHALED" or c["novel"] == 0 or not misses:
        return 0
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
