#!/usr/bin/env python3
"""
REALITY QUOTIENTS — HQ / WQ / CQ advisory over the LIVE arifFlow receipt stream.

REFERENCE: APEX::TRI_REALITY_GOVERNANCE_ACTIVATION::2026-09-13 · ARIFLOW DIRECTIVE
DOCTRINE : "Current: FQ (Execute vs Verify). Add: HQ (Human Attention Quotient),
            WQ (World Constraint Quotient), CQ (Consequence Quotient).
            Future optimization target: Reality, Attention, Consequence —
            not merely Execute, Verify."

WHY THIS IS A SEPARATE ADVISORY AND NOT A DAEMON PATCH
------------------------------------------------------
Grounding probe (2026-09-13) found:
  · FQ is computed in RUST: /root/arifFlow/src/receipt.rs:410 (FlowQuotient::compute)
    and /root/arifFlow/src/governance/invariants.rs:289 (per-actor). Modifying it
    requires recompile + daemon restart on a live :7073 service.
  · /health ALREADY returns a 7-dimension vector:
      fq, g, j, w3, c_dark, ds, omega   (metric_frame.formula_version qg.v0.3.1-vector)
    so HQ/WQ/CQ extend an EXISTING multi-dimension frame, not a new concept.
  · CQ ALREADY EXISTS under another name: POST /consequences reads payload.consequence
    (lineage_query.rs:501-524, schema arifflow.consequences/v1).
  · Receipts live at /var/lib/arifflow/receipts.jsonl (29 keys), read-only here.

Therefore: measure first, in advisory mode, with ZERO mutation of the live daemon.
Fidelity per quotient is declared honestly (FULL / PARTIAL / ABSENT) rather than
inventing precision the data does not carry.

Exit: 0 always (advisory). Non-zero only on a hard read failure.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

RECEIPTS = Path("/var/lib/arifflow/receipts.jsonl")
FALLBACK = Path("/root/VAULT999/arifflow_sealed.jsonl")
HEALTH = "http://127.0.0.1:7073/health"
CONSEQUENCES = "http://127.0.0.1:7073/consequences"

HUMAN_FACING_ACTORS = {"hermes", "arif", "human", "arif-fazil", "i-arif"}


def sh(cmd: str, timeout: int = 12) -> str:
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=timeout).stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


def tail_receipts(path: Path, n: int) -> list[dict]:
    if not path.exists():
        return []
    out: list[dict] = []
    with path.open("rb") as fh:
        fh.seek(0, 2)
        size = fh.tell()
        block = 1 << 20
        data = b""
        while size > 0 and data.count(b"\n") <= n:
            size -= block
            if size < 0:
                size = 0
            fh.seek(size)
            data = fh.read(block) + data
    for line in data.decode("utf-8", "replace").splitlines()[-n:]:
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:  # noqa: BLE001
            continue
    return out


def live_health() -> dict:
    raw = sh(f"curl -s --max-time 8 {HEALTH}")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:  # noqa: BLE001
        return {}


def compute(rows: list[dict], max_scan: int) -> dict:
    rows = rows[-max_scan:]
    n = len(rows)
    if n == 0:
        return {"error": "no receipts readable"}

    step = Counter(r.get("step_type") for r in rows)
    verify, execute = step.get("Verify", 0), step.get("Execute", 0)

    # HQ — Human Attention Quotient (PARTIAL fidelity)
    # proxy: share of steps that are human-facing OR carry human/organ witness, plus
    # the fraction of wall-clock cost spent on verified (attention-honouring) steps.
    human_actor = sum(1 for r in rows if str(r.get("actor_id", "")).lower() in HUMAN_FACING_ACTORS)
    witnessed = sum(1 for r in rows if r.get("witness_organs"))
    total_cost = sum(int(r.get("cost_ns") or 0) for r in rows)
    verify_cost = sum(int(r.get("cost_ns") or 0) for r in rows if r.get("step_type") == "Verify")
    hq = ((human_actor + witnessed) / (2 * n)) if n else 0.0

    # WQ — World Constraint Quotient (ABSENT fidelity today)
    # a step is world-bound if its free-form payload carries an explicit world constraint ref.
    wro_ref = 0
    for r in rows:
        pl = r.get("payload")
        if isinstance(pl, dict):
            keys = {k.lower() for k in pl}
            if keys & {"wro", "wro_id", "world_constraint", "world_reality", "constraint_ref"}:
                wro_ref += 1
    wq = wro_ref / n if n else 0.0

    # CQ — Consequence Quotient (field already exists: payload.consequence)
    cq_ref = 0
    for r in rows:
        pl = r.get("payload")
        if isinstance(pl, dict) and pl.get("consequence") is not None:
            cq_ref += 1
    cq = cq_ref / n if n else 0.0

    fq = (verify / execute) if execute else None

    def band(v, good=0.30):
        return "OK" if v >= good else ("WEAK" if v > 0 else "ABSENT")

    return {
        "receipts_scanned": n,
        "step_type_mix": dict(step.most_common(6)),
        "FQ": {"value": round(fq, 4) if fq is not None else None,
               "formula": "verify_count / execute_count", "source": "computed here (live)",
               "fidelity": "FULL"},
        "HQ": {"value": round(hq, 4), "band": band(hq),
               "fidelity": "PARTIAL",
               "derived_from": ["actor_id ∈ human-facing set", "witness_organs non-null"],
               "missing_field": "no first-class human-attention field on a receipt",
               "extra": {"human_facing_steps": human_actor, "witnessed_steps": witnessed,
                         "verify_cost_share": round(verify_cost / total_cost, 4) if total_cost else None}},
        "WQ": {"value": round(wq, 4), "band": band(wq),
               "fidelity": "ABSENT",
               "derived_from": ["payload.{wro,wro_id,world_constraint,world_reality,constraint_ref}"],
               "missing_field": "no world-constraint field exists; free-form payload only",
               "world_bound_steps": wro_ref},
        "CQ": {"value": round(cq, 4), "band": band(cq),
               "fidelity": "FULL-in-principle (field exists; use may be sparse)",
               "derived_from": ["payload.consequence"],
               "consequence_bound_steps": cq_ref,
               "native_endpoint": "POST /consequences (schema arifflow.consequences/v1)"},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="HQ/WQ/CQ advisory from arifFlow receipts")
    ap.add_argument("--scan", type=int, default=5000, help="receipts to scan (tail)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = tail_receipts(RECEIPTS, args.scan)
    src = str(RECEIPTS)
    if not rows:
        rows = tail_receipts(FALLBACK, args.scan)
        src = str(FALLBACK)
    if not rows:
        print(f"FATAL: no receipts readable at {RECEIPTS} or {FALLBACK}", file=sys.stderr)
        return 2

    h = live_health()
    res = compute(rows, args.scan)
    res.update({
        "reference": "APEX::TRI_REALITY_GOVERNANCE_ACTIVATION::2026-09-13 · ARIFLOW DIRECTIVE",
        "receipt_source": src,
        "daemon_health": {"status": h.get("status"),
                          "receipts_reported": h.get("receipts"),
                          "fq_from_daemon": (h.get("fq") or {}).get("quotient"),
                          "vector_dimensions": list(((h.get("vector") or {}).get("dimensions") or {}).keys()),
                          "formula_version": (h.get("metric_frame") or {}).get("formula_version")},
        "advisory_only": True,
        "daemon_mutated": False,
        "observed_at": datetime.now(timezone.utc).isoformat(),
    })

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print("REALITY QUOTIENTS — advisory (daemon untouched)")
        print("=" * 68)
        print(f"source            : {src}")
        print(f"daemon            : {res['daemon_health']['status']} · "
              f"fq={res['daemon_health']['fq_from_daemon']} · "
              f"vector={res['daemon_health']['vector_dimensions']}")
        print(f"scanned           : {res['receipts_scanned']} receipts")
        for k in ("FQ", "HQ", "WQ", "CQ"):
            q = res[k]
            print(f"  {k} = {q['value']:<8} band={q.get('band','-'):<7} fidelity={q['fidelity']}")
        print("=" * 68)
        print(f"HQ gap  : {res['HQ']['missing_field']}")
        print(f"WQ gap  : {res['WQ']['missing_field']}")
        print(f"CQ note : {res['CQ']['native_endpoint']}")
        if res["WQ"]["value"] == 0.0:
            print("\nFINDING: WQ = 0 — no execution step in the scanned window is bound to a")
            print("world constraint. The federation currently executes with zero R0 binding.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
