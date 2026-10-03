#!/usr/bin/env python3
"""
shadow_evidence_gate.py — makes the shadow falsification doctrine executable
════════════════════════════════════════════════════════════════════════════
The rule has existed as prose since 2026-08-26 (MODEL_SHADOWS.md §"For shadow
updates"):

    "After 5+ observations, promote from HYPOTHESIS to CONFIRMED.
     After a model version upgrade, reset to HYPOTHESIS and re-observe."

It was unexecutable because the YAML schema carried no numeric evidence_count
and no last_confirmed — there was no counter able to reach 5. So 107 shadow
entries sat at whatever label their author chose, and nothing checked.

This gate derives both fields from the evidence actually present in each entry
(it never invents a count), applies the promotion rule, and reports
contradictions in BOTH directions:

  OVER-CLAIM   status/provenance asserts CONFIRMED/VERIFIED/OBSERVED but fewer
               than PROMOTE_AT dated evidence items exist. This is the dangerous
               direction — it is how a hypothesis acquires authority.
  UNDER-CLAIM  labelled HYPOTHESIS/PRIOR yet carries dated, receipted evidence.
               Safe but wasteful: real knowledge cannot be promoted.

Read-only by design. It does NOT rewrite the registry YAMLs — those files carry
doctrine headers and provenance comments that a yaml.dump round-trip would
destroy. The gate reports; a human or a targeted patch edits.

Exit codes: 0 = no over-claim, 1 = over-claim present (usable as a CI/cron gate),
2 = could not read a registry (fail-closed: never silently pass).

Forged 2026-10-03 by FI-003 (F13 order "fix D3 and D4"). DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import shadow_fq_physics as fqx
    FQ_PHYSICS_AVAILABLE = True
    FQ_IMPORT_ERROR = None
except Exception as _e:  # noqa: BLE001 — a missing physics layer must not blind the gate
    fqx = None
    FQ_PHYSICS_AVAILABLE = False
    FQ_IMPORT_ERROR = f"{type(_e).__name__}: {_e}"

REGISTRIES = {
    "harness": Path("/root/AAA/registries/harnesses"),
    "model": Path("/root/AAA/registries/models"),
}
GLOB = "*_shadow.yaml"

PROMOTE_AT = 5  # the doctrine's N>=5, now a constant something can enforce

# Labels that assert a measurement happened.
ASSERTED_LABELS = {"CONFIRMED", "VERIFIED", "OBSERVED", "SOVEREIGN_WITNESS"}
# Labels that assert no measurement happened.
UNASSERTED_LABELS = {"HYPOTHESIS", "PRIOR_ONLY", "PRIOR", "VENDOR_CLAIM", "INFERRED", "DECLARED"}

ISO_DATE = re.compile(r"(20\d{2})-(\d{2})-(\d{2})")


def _walk_entries(node: Any) -> list[dict]:
    """Find every dict that looks like a shadow entry, at any nesting depth.

    The two registries do not share a schema: harness files use a top-level
    `shadow:` list; model files nest entries under family/version keys. Walking
    generically means the gate does not silently skip a whole file whose shape
    it was not taught — an unvisited entry would read as "no violation".
    """
    found: list[dict] = []
    if isinstance(node, dict):
        if "id" in node and ("severity" in node or "provenance" in node or "status" in node
                             or "evidence" in node or "pattern" in node):
            found.append(node)
        for v in node.values():
            found.extend(_walk_entries(v))
    elif isinstance(node, list):
        for v in node:
            found.extend(_walk_entries(v))
    return found


def _evidence_items(entry: dict) -> list[Any]:
    ev = entry.get("evidence")
    if isinstance(ev, list):
        return ev
    if isinstance(ev, dict):
        return [ev]
    if isinstance(ev, str) and ev.strip():
        return [ev]
    return []


def _dates_in(blob: Any) -> list[str]:
    """Every ISO date mentioned anywhere in the evidence, newest-normalised."""
    out = []
    for m in ISO_DATE.finditer(json.dumps(blob, default=str)):
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            datetime(y, mo, d)  # reject 2026-13-45 style false positives
        except ValueError:
            continue
        out.append(m.group(0))
    return sorted(set(out))


def assess_entry(entry: dict, registry: str, fname: str) -> dict:
    eid = str(entry.get("id", "?"))
    items = _evidence_items(entry)

    # evidence_count = items that carry a DATE. An undated "structural_analysis"
    # or "architectural reasoning" blob is an assertion, not an observation, and
    # must not be allowed to satisfy N>=5.
    dated = [it for it in items if _dates_in(it)]
    evidence_count = len(dated)
    all_dates = _dates_in(items)
    last_confirmed = all_dates[-1] if all_dates else None

    labels = set()
    for k in ("status", "provenance"):
        v = entry.get(k)
        if isinstance(v, str):
            labels.add(v.strip().upper())

    # ── SCHEMA SPLIT (measured 2026-10-03) ─────────────────────────────
    # The 8 harness files do not agree on where provenance lives:
    #   entry-level only : claude-code, grok-build, hermes-asi, qwen-code
    #   evidence-level   : aforge, frame, well      <-- 12 entries
    #   both             : kimi-code
    # Reading only the entry level left those 12 as NO-LABEL, i.e. ungateable —
    # and an ungateable entry reads as a clean entry, which is the silent-hole
    # failure mode. So read both, and RECORD which convention was used so the
    # split stays visible instead of being quietly absorbed.
    #
    # Deliberately NOT normalised by writing a derived label back into the YAML:
    # that would put the same fact in two places in one file and create a second
    # source of truth free to drift — the exact defect class this gate exists to
    # catch. Derive at read time; report the divergence; let a human settle it.
    ev_labels = set()
    for it in items:
        if isinstance(it, dict):
            for k in ("provenance", "status"):
                pv = it.get(k)
                if isinstance(pv, str) and pv.strip():
                    ev_labels.add(pv.strip().upper())

    if labels and ev_labels:
        convention = "both"
    elif labels:
        convention = "entry-level"
    elif ev_labels:
        convention = "evidence-level"
    else:
        convention = "none"

    # The entry asserts the STRONGEST label anywhere inside it. Citing an
    # OBSERVED evidence item IS a claim of observation, so the over-claim test
    # must confront it rather than let it hide one level down.
    labels |= ev_labels
    declared_conf = entry.get("confidence")

    asserted = labels & ASSERTED_LABELS
    unasserted = labels & UNASSERTED_LABELS

    if asserted and evidence_count < PROMOTE_AT:
        verdict = "OVER-CLAIM"
        reason = (f"asserts {'/'.join(sorted(asserted))} with {evidence_count} "
                  f"dated evidence item(s); doctrine requires {PROMOTE_AT}")
    elif unasserted and not asserted and evidence_count >= PROMOTE_AT:
        verdict = "UNDER-CLAIM"
        reason = (f"labelled {'/'.join(sorted(unasserted))} but carries {evidence_count} "
                  f"dated evidence item(s) — eligible for promotion")
    elif unasserted and not asserted and evidence_count > 0:
        verdict = "OK-UNPROMOTED"
        reason = f"{evidence_count}/{PROMOTE_AT} dated items; correctly not yet CONFIRMED"
    elif not labels:
        verdict = "NO-LABEL"
        reason = "entry carries neither status nor provenance — cannot be gated"
    else:
        verdict = "OK"
        reason = f"{evidence_count} dated item(s), label consistent"

    return {
        "registry": registry,
        "file": fname,
        "id": eid,
        "name": entry.get("name"),
        "severity": entry.get("severity"),
        "labels": sorted(labels),
        "schema_convention": convention,
        "evidence_level_labels": sorted(ev_labels),
        "declared_confidence": declared_conf,
        "evidence_items": len(items),
        "evidence_count": evidence_count,
        "last_confirmed": last_confirmed,
        "derived_status": "CONFIRMED" if evidence_count >= PROMOTE_AT else "HYPOTHESIS",
        "verdict": verdict,
        "reason": reason,
    }


def _actor_from_file(fname: str) -> str:
    """claude-code_harness_shadow.yaml -> claude-code"""
    return fname.replace("_harness_shadow.yaml", "").replace("_shadow.yaml", "")


def _signature_of(entry: dict) -> tuple[str, str]:
    """Return (candidates, display).

    `candidates` joins BOTH semantic fields with '|' because the registries
    disagree about which one carries the meaning: SHADOW-HA-001 has
    name=bridge_volume_overload but failure_signature=execute_volume_dwarfs_verify.
    Passing only one silently made the federation's best-evidenced shadow
    untestable. `display` prefers the human-readable name for the report table.
    """
    parts = []
    for k in ("name", "failure_signature"):
        v = entry.get(k)
        if isinstance(v, str) and v.strip():
            parts.append(v.strip())
    display = parts[0] if parts else ""
    return "|".join(parts), display


def attach_fq_evidence(rows: list[dict], entries_by_row: list[dict]) -> dict:
    """Read the live FQ series and let measurement speak for each entry.

    This is the joint that was missing: an entry could assert `VERIFIED` on the
    strength of one prose line while arifFlow held 65 days of receipts that
    either supported or refuted it. The gate could not see them, so the ledger's
    own evidence was invisible and the prose was the only witness.

    Only HARNESS entries are testable — a model shadow has no actor identity in
    the receipt ledger, so mapping one would manufacture evidence. Entries whose
    signature predicts no metabolic direction are reported NOT_FQ_TESTABLE
    rather than forced onto the observable.
    """
    if not FQ_PHYSICS_AVAILABLE:
        return {"available": False, "error": FQ_IMPORT_ERROR}

    harness_rows = [
        (r, e) for r, e in zip(rows, entries_by_row)
        if r["registry"] == "harness"
    ]
    if not harness_rows:
        return {"available": True, "tested": 0, "meta": {}}

    actors = {_actor_from_file(r["file"]) for r, _ in harness_rows}
    buckets, meta = fqx.load_counts(actors)
    days = fqx.span_days(meta)

    tested = confirmed = refuted = untestable = no_receipts = 0
    for r, entry in harness_rows:
        actor = _actor_from_file(r["file"])
        sig, sig_display = _signature_of(entry)
        v = fqx.assess(actor, sig, buckets, prior=0.5, severity=r.get("severity") or "MEDIUM")
        tested += 1

        r["fq_actor"] = actor
        r["fq_signature"] = sig_display
        r["fq_candidates"] = sig
        r["fq_predicted"] = v.predicted
        r["fq_verdict"] = v.verdict
        r["fq_reason"] = v.reason
        r["fq_windows_used"] = v.windows_used
        r["fq_pooled"] = round(v.pooled_fq, 4) if v.pooled_fq is not None else None
        r["fq_pooled_se"] = round(v.pooled_se, 4) if v.pooled_se is not None else None
        r["fq_z"] = round(v.z_vs_fixed_point, 3) if v.z_vs_fixed_point is not None else None
        r["fq_i_squared"] = round(v.i_squared, 2) if v.i_squared is not None else None
        r["fq_concordance"] = f"{v.concordant}/{v.windows_used}" if v.windows_used else None
        r["fq_binom_p"] = round(v.binom_p, 5) if v.binom_p is not None else None
        r["fq_posterior"] = round(v.posterior, 4) if v.posterior is not None else None
        r["fq_model"] = v.model
        r["fq_magnitude_stable"] = v.magnitude_stable

        CONFIRMING = ("CONFIRMED_MEASURED", "CONFIRMED_DIRECTION_HETEROGENEOUS")
        if v.verdict == "NOT_FQ_TESTABLE":
            untestable += 1
        elif v.verdict == "NO_RECEIPTS":
            no_receipts += 1
        elif v.verdict in CONFIRMING:
            confirmed += 1
            # A measured attractor IS the observation the prose was approximating.
            # Promote on measurement, and stop calling the entry an over-claim:
            # it was under-evidenced in prose, not wrong.
            r["derived_status"] = "CONFIRMED"
            r["confirmed_by"] = (f"live FQ series — {v.verdict}, "
                                 f"{v.windows_used} daily windows, log-space inverse-variance pooled")
            if r["verdict"] == "OVER-CLAIM":
                r["verdict"] = "SUPPORTED_BY_MEASUREMENT"
                r["reason"] = (f"prose carries {r['evidence_count']} dated item(s) but the "
                               f"ledger confirms the attractor: {v.reason}")
        elif v.verdict == "REFUTED":
            refuted += 1
            r["refuted_by"] = "live FQ series"
            if r["verdict"] in ("OK", "OK-UNPROMOTED"):
                r["verdict"] = "REFUTED_BY_MEASUREMENT"
                r["reason"] = f"ledger contradicts this shadow: {v.reason}"
        elif v.verdict == "NO_STABLE_ATTRACTOR":
            # Explicitly NOT a refutation. High heterogeneity means the actor is
            # not in one state, so the entry stays and gets flagged as episodic
            # rather than being deleted on a statistic that cannot bear that weight.
            r["episodic"] = True
            if r["verdict"] == "OVER-CLAIM":
                r["reason"] += (" | ledger: NO_STABLE_ATTRACTOR — episodic, not a fixed "
                                "attractor; entry retained, not refuted")

        # APEX — rank what to instrument next, not what to re-assert.
        rate = fqx.daily_rate(buckets, actor, days)
        r["apex"] = fqx.apex_voi(v, r.get("severity") or "MEDIUM", rate)

    return {
        "available": True,
        "tested": tested,
        "confirmed": confirmed,
        "refuted": refuted,
        "not_testable": untestable,
        "no_receipts": no_receipts,
        "meta": meta,
        "span_days": days,
        "buckets": buckets,
    }


def main() -> int:
    rows: list[dict] = []
    entries: list[dict] = []  # parallel to rows: the raw YAML entry behind each
    unreadable: list[str] = []

    for registry, root in REGISTRIES.items():
        if not root.is_dir():
            unreadable.append(str(root))
            continue
        files = sorted(root.glob(GLOB))
        if not files:
            unreadable.append(f"{root} (no {GLOB})")
            continue
        for f in files:
            try:
                doc = yaml.safe_load(f.read_text())
            except Exception as e:  # noqa: BLE001
                unreadable.append(f"{f.name}: {type(e).__name__}: {e}")
                continue
            for entry in _walk_entries(doc):
                rows.append(assess_entry(entry, registry, f.name))
                entries.append(entry)

    # ── The live FQ series gets a vote. Runs AFTER the prose pass so that a
    #    measurement can rescue an under-evidenced claim or refute a confident
    #    one. Verdicts below are computed after this, never before.
    fq_info = attach_fq_evidence(rows, entries)

    if unreadable:
        print("# ⚠ SHADOW EVIDENCE GATE — could not read every registry")
        for u in unreadable:
            print(f"#   UNREADABLE: {u}")
        print("# Fail-closed: an unreadable registry is not a passing registry.")

    over = [r for r in rows if r["verdict"] == "OVER-CLAIM"]
    under = [r for r in rows if r["verdict"] == "UNDER-CLAIM"]
    nolabel = [r for r in rows if r["verdict"] == "NO-LABEL"]
    supported = [r for r in rows if r["verdict"] == "SUPPORTED_BY_MEASUREMENT"]
    refuted = [r for r in rows if r["verdict"] == "REFUTED_BY_MEASUREMENT"]
    promotable = [r for r in rows if r["derived_status"] == "CONFIRMED"]

    print("# Shadow Evidence Gate  v2 (prose + live FQ series)")
    print(f"# Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(f"# Rule: CONFIRMED requires >= {PROMOTE_AT} DATED prose items, OR a measured")
    print("#       attractor in the live FQ series (significant displacement from FQ*=1")
    print("#       AND temporal stability AND sign concordance).")
    print(f"# Sources: {' + '.join(str(p) for p in REGISTRIES.values())}")
    print(f"#          + {fqx.RECEIPTS if FQ_PHYSICS_AVAILABLE else 'FQ PHYSICS UNAVAILABLE'}")
    print()
    print(f"Entries assessed:            {len(rows)}")
    print(f"  harness registry:          {sum(1 for r in rows if r['registry'] == 'harness')}")
    print(f"  model registry:            {sum(1 for r in rows if r['registry'] == 'model')}")
    print(f"Eligible for CONFIRMED:      {len(promotable)}")
    print(f"OVER-CLAIM (dangerous):      {len(over)}")
    print(f"SUPPORTED_BY_MEASUREMENT:    {len(supported)}   (prose thin; ledger confirmed)")
    print(f"REFUTED_BY_MEASUREMENT:      {len(refuted)}   (ledger contradicts registry)")
    print(f"UNDER-CLAIM (wasted):        {len(under)}")
    print(f"NO-LABEL (ungateable):       {len(nolabel)}")
    print()

    # ── Schema conformance: the split is reported, never silently absorbed ──
    conv: dict[str, dict[str, int]] = {}
    for r in rows:
        f = conv.setdefault(r["file"], {"n": 0, "entry-level": 0, "evidence-level": 0,
                                        "both": 0, "none": 0})
        f["n"] += 1
        f[r.get("schema_convention", "none")] += 1
    split = {k: v for k, v in conv.items()
             if sum(v[c] for c in ("entry-level", "evidence-level", "both")) and
             not v["entry-level"] == v["n"]}
    print("## Schema conformance — where does each file put `provenance`?")
    print(f"  {'file':<40}{'entries':>8}{'entry':>7}{'evid':>6}{'both':>6}{'none':>6}")
    for fname in sorted(conv):
        v = conv[fname]
        print(f"  {fname[:39]:<40}{v['n']:>8}{v['entry-level']:>7}"
              f"{v['evidence-level']:>6}{v['both']:>6}{v['none']:>6}")
    conventions = {r.get("schema_convention") for r in rows}
    if len(conventions - {"none"}) > 1:
        print(f"  ⚠ SPLIT SCHEMA: {len(conv)} files use {sorted(conventions)} — the gate reads")
        print("    all of them, but one registry should have one convention. Settling it is a")
        print("    canonical-file mutation (F13), not something a reader should paper over.")
    print()

    if not fq_info.get("available"):
        print(f"## ⚠ FQ SERIES UNAVAILABLE — {fq_info.get('error')}")
        print("## Prose-only gating. The pre-v2 blind spot, reported not hidden.")
        print()
    else:
        m = fq_info.get("meta", {})
        print("## Live FQ series — the shadow as a measurable attractor")
        print(f"  ledger rows={m.get('rows')} parsed={m.get('parsed')} unparsed={m.get('unparsed')}")
        print(f"  span={m.get('span_min')} -> {m.get('span_max')} ({fq_info.get('span_days')} days)")
        print(f"  harness entries tested={fq_info.get('tested')} "
              f"confirmed={fq_info.get('confirmed')} refuted={fq_info.get('refuted')} "
              f"not_testable={fq_info.get('not_testable')} no_receipts={fq_info.get('no_receipts')}")
        print()
        hdr = (f"  {'actor':<13}{'signature':<28}{'pred':<7}{'n':>3}{'FQ(geo)':>9}"
               f"{'SE(ln)':>8}{'Z':>9}{'I2%':>7}{'concord':>9}{'binom p':>9}  verdict")
        print(hdr)
        print("  " + "-" * (len(hdr) - 2))
        for r in sorted([x for x in rows if x.get("fq_verdict") not in (None, "NOT_FQ_TESTABLE")],
                        key=lambda x: (x["fq_verdict"] != "CONFIRMED_MEASURED", x["fq_actor"])):
            pf = f"{r['fq_pooled']:.3f}" if r.get("fq_pooled") is not None else "—"
            se = f"{r['fq_pooled_se']:.3f}" if r.get("fq_pooled_se") is not None else "—"
            z = f"{r['fq_z']:+.2f}" if r.get("fq_z") is not None else "—"
            i2 = f"{r['fq_i_squared']:.1f}" if r.get("fq_i_squared") is not None else "—"
            bp = f"{r['fq_binom_p']:.4f}" if r.get("fq_binom_p") is not None else "—"
            print(f"  {r['fq_actor']:<13}{r['fq_signature'][:27]:<28}{r['fq_predicted']:<7}"
                  f"{r.get('fq_windows_used', 0):>3}{pf:>10}{se:>8}{z:>8}{i2:>7}"
                  f"{str(r.get('fq_concordance') or '—'):>9}{bp:>9}  {r['fq_verdict']}")
        print()
        nt = [r for r in rows if r.get("fq_verdict") == "NOT_FQ_TESTABLE"]
        if nt:
            sigs = sorted({r["fq_signature"] for r in nt if r.get("fq_signature")})
            print(f"  NOT_FQ_TESTABLE ({len(nt)}): behavioural shadows this observable cannot see —")
            print("    " + ", ".join(sigs[:12]))
            print("  Reported, not forced onto the metric: a wrong observable is worse than none.")
            print()

    if supported:
        print("## SUPPORTED_BY_MEASUREMENT — prose under-evidenced, ledger confirms")
        for r in supported:
            print(f"  {r['fq_actor']} :: {r['id']} ({r['name']})")
            print(f"      {r['fq_reason']}")
        print()

    if refuted:
        print("## REFUTED_BY_MEASUREMENT — the ledger contradicts the registry")
        for r in refuted:
            print(f"  {r['fq_actor']} :: {r['id']} ({r['name']})")
            print(f"      {r['fq_reason']}")
        print()

    if over:
        print("## OVER-CLAIM — asserted measurement, and the ledger does not rescue it")
        for r in sorted(over, key=lambda x: (x["registry"], x["file"], x["id"])):
            fqnote = f" | fq: {r['fq_verdict']}" if r.get("fq_verdict") else ""
            print(f"  [{r['registry']}] {r['file']} :: {r['id']} ({r['name']}) — {r['reason']}{fqnote}")
        print()

    if under:
        print("## UNDER-CLAIM — real receipts stuck behind a weak label")
        for r in sorted(under, key=lambda x: -x["evidence_count"]):
            print(f"  [{r['registry']}] {r['file']} :: {r['id']} — {r['reason']}")
        print()

    if promotable:
        print("## Promotion candidates (derived_status == CONFIRMED)")
        for r in promotable:
            via = r.get("confirmed_by") or f"prose N>={PROMOTE_AT}"
            print(f"  [{r['registry']}] {r['id']} — prose_items={r['evidence_count']} "
                  f"last_confirmed={r['last_confirmed']} via={via}")
        print()

    ranked = [r for r in rows if r.get("apex") and r["apex"]["voi"] > 0]
    if ranked:
        ranked.sort(key=lambda x: -x["apex"]["voi"])
        print("## APEX — value of measurement (uncertainty reduction per unit waiting time)")
        print("##   VoI = severity x H(posterior)/ln2 x daily_receipt_rate")
        print("##   Settled entries sink to the bottom: no attention spent on closed questions.")
        print(f"  {'#':<4}{'entry':<40}{'sev':<9}{'post':>7}{'H':>7}{'rate/d':>9}{'VoI':>9}")
        for i, r in enumerate(ranked[:10], 1):
            a = r["apex"]
            print(f"  {i:<4}{r['id'][:38]:<40}{str(r.get('severity')):<9}"
                  f"{a['posterior']:>7.3f}{a['entropy_norm']:>7.3f}"
                  f"{a['daily_receipt_rate']:>9.1f}{a['voi']:>9.2f}")
        print()

    receipt = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "gate_version": "2-fq-series",
        "promote_at": PROMOTE_AT,
        "entries_assessed": len(rows),
        "over_claim": len(over),
        "under_claim": len(under),
        "no_label": len(nolabel),
        "supported_by_measurement": len(supported),
        "refuted_by_measurement": len(refuted),
        "promotion_candidates": len(promotable),
        "unreadable_registries": unreadable,
        "fq_series": {
            "available": fq_info.get("available", False),
            "error": fq_info.get("error"),
            "ledger_rows": fq_info.get("meta", {}).get("rows"),
            "parsed": fq_info.get("meta", {}).get("parsed"),
            "span_min": fq_info.get("meta", {}).get("span_min"),
            "span_max": fq_info.get("meta", {}).get("span_max"),
            "span_days": fq_info.get("span_days"),
            "tested": fq_info.get("tested"),
            "confirmed": fq_info.get("confirmed"),
            "refuted": fq_info.get("refuted"),
            "not_testable": fq_info.get("not_testable"),
            "no_receipts": fq_info.get("no_receipts"),
        },
        "apex_ranking": [
            {"id": r["id"], "actor": r.get("fq_actor"),
             "severity": r.get("severity"), **r["apex"]}
            for r in ranked[:10]
        ],
        "rows": rows,
    }
    out = Path("/root/AAA/cockpit/shadow-matrix/evidence-gate-latest.json")
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(receipt, indent=2, default=str) + "\n")
        print(f"Receipt: {out}")
    except OSError as e:
        print(f"⚠ could not write receipt: {e}")

    if unreadable:
        return 2
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main())
