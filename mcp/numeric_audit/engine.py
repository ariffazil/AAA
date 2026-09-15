"""
numeric_audit.engine — deterministic numeric audit engine.

Design constraints (binding):
  * Exact arithmetic only. All money / capital / ratio values are decimal.Decimal.
    Floats are never used for any value that participates in a computation.
  * Pure functions. No network. No filesystem writes. No clock. Same input -> same output.
  * Every claim is compared against a RECOMPUTATION with a declared method, never a vibe.

Authority: ANALYSIS_ONLY. This engine re-computes and reports. It never judges a
bank, never seals, never writes VAULT999.

DITEMPA BUKAN DIBERI.
"""

from __future__ import annotations

import json
import os
from decimal import Decimal, ROUND_HALF_UP, getcontext
from typing import Any, Iterable, Sequence

getcontext().prec = 60

_RULES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules", "bnm_capital_rwa.json")

# ---------------------------------------------------------------------------
# Decimal helpers
# ---------------------------------------------------------------------------

def D(value: Any) -> Decimal:
    """Parse to Decimal without ever transiting through binary float.

    Accepts Decimal, int, str (including '12.02', '12.02%', 'RM3.23bn'),
    and rejects float outright so a float can never silently drift money.
    """
    if isinstance(value, Decimal):
        return value
    if isinstance(value, bool):
        raise TypeError("bool is not a number")
    if isinstance(value, int):
        return Decimal(value)
    if isinstance(value, float):
        raise TypeError(
            "float input rejected — money/ratio values must be Decimal, int or str "
            "so no binary-float drift can enter the audit"
        )
    if isinstance(value, str):
        s = value.strip()
        for token in ("RM", "rm", "%", ",", " ", "bn", "BN", "bn.", "million", "mil"):
            s = s.replace(token, "")
        if s in ("", "-"):
            raise ValueError(f"cannot parse number from {value!r}")
        return Decimal(s)
    raise TypeError(f"unsupported numeric type {type(value).__name__}")


def Q(value: Decimal, places: int = 6) -> Decimal:
    """Quantize for display, half-up."""
    exp = Decimal(1).scaleb(-places)
    return value.quantize(exp, rounding=ROUND_HALF_UP)


def S(value: Decimal, places: int = 6) -> str:
    """Stable string form of a quantized Decimal (trailing zeros trimmed, never float)."""
    q = Q(value, places)
    s = format(q, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s or "0"


def pct_to_fraction(pct: Decimal) -> Decimal:
    return pct / Decimal(100)


def rel_diff(claimed: Decimal, recomputed: Decimal) -> Decimal | None:
    """Relative difference vs the recomputed value. None when recomputed is zero."""
    if recomputed == 0:
        return None
    return (claimed - recomputed) / recomputed


# ---------------------------------------------------------------------------
# Rule registry
# ---------------------------------------------------------------------------

def load_registry(path: str | None = None) -> dict[str, Any]:
    with open(path or _RULES_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# Derivation replay
# ---------------------------------------------------------------------------

_OPS = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
    "div": lambda a, b: a / b,
    "pct_of": lambda a, b: a * b / Decimal(100),          # a is base, b is pct
    "rwa_from": lambda a, b: a * b / Decimal(100),         # exposure_rm * risk_weight_pct -> RWA
    "capital_from_rwa": lambda a, b: a * b / Decimal(100),  # rwa_rm * ratio_pct -> capital
    "ratio_from": lambda a, b: a / b * Decimal(100),        # capital / rwa * 100 -> pct
    "rwa_from_ratio": lambda a, b: a / (b / Decimal(100)),  # capital / (ratio_pct) -> implied RWA
}


def replay_derivation(
    inputs: dict[str, Any],
    steps: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    """Replay a named derivation chain exactly.

    inputs: {"equity_rm": "3.23", "cet1_pct": "12.02", ...}
    steps:  [{"id":"rwa","op":"rwa_from_ratio","args":["equity_rm","cet1_pct"]},
             {"id":"delta","op":"mul","args":["add_rm","delta_weight_pp"]}, ...]
    Any arg that is not an input id or earlier step id is parsed as a literal.

    Returns an auditable trace: every step, its operands (as strings), and its
    exact result. A reader can re-run the trace by hand.
    """
    env: dict[str, Decimal] = {}
    trace: list[dict[str, Any]] = []

    for k, v in (inputs or {}).items():
        env[k] = D(v)

    for step in steps or []:
        sid = step.get("id") or f"step{len(trace) + 1}"
        op = step.get("op")
        if op not in _OPS:
            raise ValueError(f"unknown op {op!r}; known ops: {sorted(_OPS)}")
        args = step.get("args", [])
        if len(args) != 2:
            raise ValueError(f"step {sid!r}: op {op!r} needs exactly 2 args, got {len(args)}")
        resolved: list[Decimal] = []
        for a in args:
            key = a if isinstance(a, str) else a.get("ref")
            if isinstance(key, str) and key in env:
                resolved.append(env[key])
            elif isinstance(a, dict) and "value" in a:
                resolved.append(D(a["value"]))
            elif isinstance(a, str):
                resolved.append(D(a))
            else:
                resolved.append(D(a))
        a0, a1 = resolved
        if op == "div" and a1 == 0:
            raise ZeroDivisionError(f"step {sid!r}: division by zero")
        out = _OPS[op](a0, a1)
        env[sid] = out
        trace.append({
            "id": sid,
            "op": op,
            "operands": [S(a0), S(a1)],
            "result": S(out),
            "note": step.get("note", ""),
        })

    return {
        "trace": trace,
        "results": {k: S(v) for k, v in env.items()},
        "arithmetic": "exact (decimal.Decimal, prec=60) — no float transit",
    }


# ---------------------------------------------------------------------------
# Unit / scale checks
# ---------------------------------------------------------------------------

_UNIT_FAMILIES: dict[str, list[tuple[str, Decimal]]] = {
    "ratio_pct": [("%", Decimal(1)), ("pct", Decimal(1)), ("bps", Decimal("0.01")), ("fraction", Decimal(100))],
    "currency": [("RM", Decimal(1)), ("RM'mil", Decimal("0.001")), ("RM_bn", Decimal(1)), ("RM_bil", Decimal(1)),
                 ("RM_mn", Decimal("0.001")), ("RM_mil", Decimal("0.001")), ("RM_m", Decimal("0.000001")),
                 ("RM_tn", Decimal(1000)), ("RM_b", Decimal(1))],
}


def check_units_scale(claims: Sequence[dict[str, Any]], tolerance_rel: str = "0.01") -> dict[str, Any]:
    """Lint a set of numeric claims for unit and scale inconsistencies.

    Each claim: {"id":..., "value":"12.02", "unit":"%", "as_of":"...", "basis":"..."}
    Checks performed:
      * unit parseable and known family
      * percent-vs-fraction plausibility (a 12.02 'fraction' is flagged, a 1202% is flagged)
      * percent-vs-basis-point confusion (a 'bps' value that only makes sense as %)
      * cross-claim identity conflicts: two claims that should be the same quantity
        (same quantity_key) but differ by more than tolerance_rel
      * billion/million scale drift: values that differ by ~1000x within one family
      * unquantified basis: a ratio computed from a capital measure whose definition
        (CET1 capital vs shareholders' equity) is not declared
    """
    tol = D(tolerance_rel)
    findings: list[dict[str, Any]] = []
    parsed: list[dict[str, Any]] = []

    for c in claims or []:
        cid = c.get("id", "?")
        unit = str(c.get("unit", "")).strip()
        try:
            val = D(c.get("value"))
        except Exception as exc:  # noqa: BLE001
            findings.append({"check": "unit.parse", "claim": cid, "severity": "P1",
                             "detail": f"value not parseable as an exact decimal: {exc}"})
            continue
        family = None
        factor = None
        for fam, units in _UNIT_FAMILIES.items():
            for u, f in units:
                if unit.lower() == u.lower():
                    family, factor = fam, f
                    break
            if family:
                break
        if family is None:
            findings.append({"check": "unit.known", "claim": cid, "severity": "P2",
                             "detail": f"unit {unit!r} not in known families; scale cannot be verified"})
        rec = {"id": cid, "value": val, "unit": unit, "family": family,
               "basis": c.get("basis"), "quantity_key": c.get("quantity_key"),
               "normalized": val * factor if factor is not None else None}
        parsed.append(rec)

        if family == "ratio_pct":
            if unit.lower() == "fraction" and abs(val) > Decimal(1):
                findings.append({"check": "unit.fraction_range", "claim": cid, "severity": "P1",
                                 "detail": f"declared a fraction but value {S(val)} > 1; did you mean {S(val / 100)} as a fraction, or {S(val)} %?"})
            if unit.lower() in ("%", "pct") and abs(val) > Decimal(100):
                findings.append({"check": "unit.percent_range", "claim": cid, "severity": "P1",
                                 "detail": f"declared percent with value {S(val)} > 100; check for a 100x scale error"})
            if unit.lower() == "bps" and abs(val) < Decimal(1):
                findings.append({"check": "unit.bps_plausibility", "claim": cid, "severity": "P2",
                                 "detail": f"declared bps with value {S(val)} (< 100 bps is 1%); confirm percent/bps confusion"})

    # cross-claim identity conflicts
    by_key: dict[str, list[dict[str, Any]]] = {}
    for r in parsed:
        if r.get("quantity_key"):
            by_key.setdefault(r["quantity_key"], []).append(r)
    for key, group in by_key.items():
        if len(group) < 2:
            continue
        vals = [g["value"] for g in group]
        lo, hi = min(vals), max(vals)
        if lo != 0:
            span = (hi - lo) / lo
            if span > tol:
                findings.append({
                    "check": "unit.identity_conflict", "severity": "P0",
                    "detail": (f"same quantity_key {key!r} carries different values across claims: "
                               f"{[S(v) for v in vals]} (relative spread {S(span, 6)} > tol {tolerance_rel})"),
                })
            if Decimal("900") < hi / lo < Decimal("1100") if lo > 0 else False:
                findings.append({"check": "unit.thousand_fold", "severity": "P0",
                                 "detail": f"quantity_key {key!r} differs by ~1000x: {S(lo)} vs {S(hi)} — million/billion scale drift"})

    # basis declaration
    for r in parsed:
        if r["family"] == "ratio_pct" and not r.get("basis"):
            findings.append({"check": "unit.basis_undeclared", "claim": r["id"], "severity": "P1",
                             "detail": ("ratio has no declared basis. A CET1 ratio divides CET1 CAPITAL; if it was "
                                        "derived from shareholders' equity the numerator is a different quantity and "
                                        "the implied RWA is not the regulator's RWA.")})

    p0 = sum(1 for f in findings if f["severity"] == "P0")
    p1 = sum(1 for f in findings if f["severity"] == "P1")
    verdict = "CLEAN" if not findings else ("SCALE_ERROR" if p0 else "ATTENTION")
    return {"verdict": verdict, "findings": findings, "counts": {"P0": p0, "P1": p1, "P2": len(findings) - p0 - p1},
            "claims_parsed": len(parsed)}


# ---------------------------------------------------------------------------
# Sensitivity-table recomputation
# ---------------------------------------------------------------------------

def recompute_sensitivity(
    increments_rm: Sequence[Any],
    base_rwa_rm: Any,
    base_capital_rm: Any,
    applied_weight_pct: Any,
    target_ratio_pct: Any,
    replacement_weight_pct: Any = "0",
    retained_share_pct: Any = "100",
    mitigant_factor: Any = "1",
    claimed_rows: Sequence[dict[str, Any]] | None = None,
    tolerance_rm: Any = "0.1",
) -> dict[str, Any]:
    """Recompute a capital-sensitivity table from a DECLARED derivation rule.

    added_rwa_rm   = increment * (applied_weight - replacement_weight)/100
                     * retained_share/100 * mitigant_factor
    total_rwa_rm   = base_rwa_rm + added_rwa_rm
    required_cap   = total_rwa_rm * target_ratio/100
    new_capital_rm = required_cap - base_capital_rm

    `replacement_weight_pct` is the weight the SAME exposure already carried before
    conversion. Leaving it at 0 means gross basis; setting it to the prevailing
    weight means net/incremental basis. A published table that reports a
    net-of-replacement number without declaring it is a hidden derivation step.

    If claimed_rows is supplied each row is compared and the row verdict recorded.
    """
    base_rwa = D(base_rwa_rm)
    base_cap = D(base_capital_rm)
    w_after = D(applied_weight_pct)
    w_before = D(replacement_weight_pct)
    target = D(target_ratio_pct)
    retained = D(retained_share_pct)
    mitig = D(mitigant_factor)
    tol = D(tolerance_rm)

    rows: list[dict[str, Any]] = []
    for i, inc in enumerate(increments_rm or []):
        inc_d = D(inc)
        delta_pp = w_after - w_before
        added = inc_d * delta_pp / Decimal(100) * retained / Decimal(100) * mitig
        total = base_rwa + added
        required = total * target / Decimal(100)
        new_cap = required - base_cap
        marginal_per_bn = (D(1) * delta_pp / Decimal(100) * retained / Decimal(100) * mitig
                           * target / Decimal(100)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)
        row: dict[str, Any] = {
            "increment_rm": S(inc_d),
            "delta_weight_pp": S(delta_pp),
            "added_rwa_rm": S(added),
            "implied_rwa_rm": S(total),
            "required_capital_rm": S(required),
            "new_capital_rm": S(new_cap),
            "marginal_new_capital_rm_per_rm1bn": S(marginal_per_bn),
            "claim_check": None,
        }
        if claimed_rows and i < len(claimed_rows):
            claimed = claimed_rows[i]
            cmp_out: dict[str, Any] = {}
            for field, key in (("implied_rwa_rm", "implied_rwa_rm"), ("new_capital_rm", "new_capital_rm")):
                if key in claimed:
                    cv = D(claimed[key])
                    rv = row[field] if field in ("implied_rwa_rm",) else row[field]
                    rv_d = D(rv)
                    diff = cv - rv_d
                    cmp_out[field] = {
                        "claimed": S(cv), "recomputed": S(rv_d), "diff": S(diff),
                        "match": abs(diff) <= tol,
                    }
            row["claim_check"] = cmp_out
        rows.append(row)

    mismatches = []
    for r in rows:
        cc = r.get("claim_check") or {}
        for f, d in cc.items():
            if not d["match"]:
                mismatches.append({"increment_rm": r["increment_rm"], "field": f,
                                   "claimed": d["claimed"], "recomputed": d["recomputed"], "diff": d["diff"]})
    rows_match = all(d["match"] for r in rows for d in (r.get("claim_check") or {}).values())

    return {
        "method": {
            "added_rwa_rm": "increment_rm * (applied_weight_pct - replacement_weight_pct)/100 * retained_share_pct/100 * mitigant_factor",
            "implied_rwa_rm": "base_rwa_rm + added_rwa_rm",
            "required_capital_rm": "implied_rwa_rm * target_ratio_pct/100",
            "new_capital_rm": "required_capital_rm - base_capital_rm",
        },
        "inputs": {
            "base_rwa_rm": S(base_rwa), "base_capital_rm": S(base_cap),
            "applied_weight_pct": S(w_after), "replacement_weight_pct": S(w_before),
            "target_ratio_pct": S(target), "retained_share_pct": S(retained), "mitigant_factor": S(mitig),
            "basis": "net_of_replacement" if w_before > 0 else "gross",
        },
        "rows": rows,
        "internal_consistency": "MATCH" if rows_match else "MISMATCH",
        "mismatches": mismatches,
        "arithmetic": "exact (decimal.Decimal, prec=60)",
    }


# ---------------------------------------------------------------------------
# Scope check — the error-class catcher
# ---------------------------------------------------------------------------

def _predicate_matches(pred: dict[str, Any], scope: dict[str, Any]) -> tuple[bool, list[str]]:
    """A predicate matches only if every key it names is declared in scope AND covered.

    Undeclared scope keys make a predicate UNMATCHED and are reported as gaps —
    never silently assumed. Silence is not consent.
    """
    gaps: list[str] = []
    for key, allowed in pred.items():
        declared = scope.get(key)
        if declared is None:
            gaps.append(f"{key} not declared")
            continue
        declared_list = declared if isinstance(declared, list) else [declared]
        if not any(d in allowed for d in declared_list):
            return False, gaps
    return True, gaps


def scope_check(
    figure_pct: Any,
    scope: dict[str, Any],
    basis: str | None = None,
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Decide whether a claimed figure is being applied INSIDE its canonical scope.

    This is the primary detector for the error class:
        "a figure lifted from secondary literature and applied outside its actual scope".

    figure_pct : the number as claimed, e.g. "400" for 400%.
    scope      : declared scope using the registry vocabulary, e.g.
                 {"contract":"musyarakah_butanaqisah","exposure_basis":"profit_and_loss_sharing_financing",
                  "position":"banking_book","listing":"not_applicable","counterparty":"retail"}
    basis      : how the figure is being applied — "flat_all", "category_dependent",
                 "counterparty_dependent", or None (undeclared).

    Verdicts:
      IN_SCOPE              — figure is a prescribed figure whose predicate matches the
                              declared scope and the declared basis is compatible.
      IN_SCOPE_CONDITIONAL  — figure applies only if stated conditions are met, or the
                              declared basis discards a required schedule.
      OUT_OF_SCOPE_FIGURE   — the registry knows this figure, but only under predicates
                              that the declared scope does NOT satisfy. <-- the error class
      FIGURE_NOT_IN_REGISTRY— cannot verify; reported as UNVERIFIED, never as OK.
    """
    reg = registry or load_registry()
    claimed = D(figure_pct)
    out: dict[str, Any] = {"figure_pct": S(claimed), "declared_scope": scope, "declared_basis": basis}

    applicable: list[dict[str, Any]] = []
    carriers: list[dict[str, Any]] = []
    scope_gaps: list[str] = []

    for rule in reg["rules"]:
        figs = [D(f) for f in rule.get("figures_pct", [])]
        is_carrier = claimed in figs
        matched_any = False
        rule_gaps: list[str] = []
        for pred in rule.get("applies_to", []):
            m, gaps = _predicate_matches(pred, scope or {})
            if m:
                matched_any = True
                break
            rule_gaps.extend(gaps)
        if is_carrier:
            carriers.append({"rule_id": rule["rule_id"], "canonical_scope": rule["canonical_scope"],
                             "in_scope_for_declared": matched_any, "source": rule["source"],
                             "basis": rule["basis"], "conditions": rule.get("conditions", [])})
        if matched_any:
            applicable.append(rule)
        elif is_carrier:
            scope_gaps.extend(rule_gaps)

    out["carriers_of_figure"] = carriers
    out["rules_applicable_to_declared_scope"] = [
        {"rule_id": r["rule_id"], "figures_pct": r.get("figures_pct", []),
         "canonical_scope": r["canonical_scope"], "basis": r["basis"],
         "clause": r["source"].get("clause"), "conditions": r.get("conditions", [])}
        for r in applicable
    ]

    app_figs: list[Decimal] = sorted({D(f) for r in applicable for f in r.get("figures_pct", [])})
    resolved_via: list[str] = []
    if not app_figs:
        by_id = {r["rule_id"]: r for r in reg["rules"]}
        for r in applicable:
            for rid in r.get("resolves_via", []):
                rr = by_id.get(rid)
                if not rr:
                    continue
                resolved_via.append(rid)
                app_figs.extend(D(f) for f in rr.get("figures_pct", []))
        app_figs = sorted(set(app_figs))
    if resolved_via:
        out["in_scope_weights_resolved_via"] = resolved_via
    out["in_scope_weight_range_pct"] = ([S(app_figs[0]), S(app_figs[-1])] if app_figs else None)
    out["in_scope_weights_pct"] = [S(f) for f in app_figs]
    out["in_scope_is_range_not_single"] = any(r.get("figures_are_range") for r in applicable)
    if not app_figs:
        out["gap"] = ("scope resolves to a weight that this registry does not carry as a number "
                      "(counterparty / rating / slotting dependent). UNVERIFIED — do not fill the gap "
                      "with a figure borrowed from another exposure class.")

    in_scope_carrier = any(c["in_scope_for_declared"] for c in carriers)

    if not carriers:
        out["verdict"] = "FIGURE_NOT_IN_REGISTRY"
        out["confidence"] = "UNVERIFIED"
        out["reason"] = ("figure is not a prescribed figure in the registry. An unregistered figure "
                         "cannot be blessed by silence — it must be traced to a clause before use.")
        return out

    if in_scope_carrier:
        mismatched_basis = []
        for c in carriers:
            if not c["in_scope_for_declared"]:
                continue
            if basis and c["basis"] and basis != c["basis"]:
                mismatched_basis.append({"rule_id": c["rule_id"], "rule_basis": c["basis"],
                                         "declared_basis": basis, "conditions": c["conditions"]})
        if mismatched_basis:
            out["verdict"] = "IN_SCOPE_CONDITIONAL"
            out["confidence"] = "DER"
            out["reason"] = ("the figure is in scope for this exposure class, but the declared application basis "
                             "discards the schedule the rule requires. Applying it flatly is a scope error even "
                             "though the number itself is correct.")
            out["basis_conflicts"] = mismatched_basis
        else:
            cond = [c for c in carriers if c["in_scope_for_declared"] and c["conditions"]]
            if cond:
                out["verdict"] = "IN_SCOPE_CONDITIONAL"
                out["confidence"] = "DER"
                out["reason"] = "figure is in scope; conditions must be shown to be met."
                out["conditions_to_satisfy"] = cond
            else:
                out["verdict"] = "IN_SCOPE"
                out["confidence"] = "DER"
                out["reason"] = "figure matches a prescribed figure whose predicate covers the declared scope, with no unmet conditions."
        out["citations"] = [c["source"] for c in carriers if c["in_scope_for_declared"]]
        return out

    # carriers exist but none is in scope -> the error class
    out["verdict"] = "OUT_OF_SCOPE_FIGURE"
    out["confidence"] = "DER"
    loaned_from = carriers[0]["canonical_scope"] if len(carriers) == 1 else " / ".join(c["canonical_scope"] for c in carriers)
    out["reason"] = (
        f"{S(claimed)}% is a prescribed figure, but only under a scope the declared exposure does not satisfy. "
        f"It has been borrowed from: {loaned_from}. "
        + (f"The scope of {S(claimed)}% as applied is unreconciled: {sorted(set(scope_gaps))}. " if scope_gaps else "")
    )
    out["figure_actually_applies_to"] = [c["canonical_scope"] for c in carriers]
    out["citations"] = [c["source"] for c in carriers]
    out["in_scope_citations"] = [r["source"] for r in applicable]

    if app_figs:
        hi = app_figs[-1]
        out["overstatement_factor_vs_max_in_scope"] = (S(claimed / hi, 4) if hi != 0 else None)
        out["understatement_if_any"] = S(claimed) < S(app_figs[0])
    if claimed in (f for f in [D(x) for x in reg.get("confusable_figures", {})]):
        out["discriminator"] = reg["confusable_figures"][S(claimed)].get("discriminator")
    return out


# ---------------------------------------------------------------------------
# Claim vs recomputation comparison
# ---------------------------------------------------------------------------

def audit_claim(
    claim_value: Any,
    recomputed_value: Any,
    unit: str = "",
    tolerance_rel: Any = "0.01",
    tolerance_abs: Any | None = None,
    scope_verdict: str | None = None,
) -> dict[str, Any]:
    """Compare a published claim against an independently recomputed value.

    A numeric match never overrides a scope failure: if the derivation is
    arithmetically right but the input was out of scope, the claim is
    ARITHMETIC_OK_SCOPE_FAIL. That distinction is the whole point of this server.
    """
    c = D(claim_value)
    r = D(recomputed_value)
    diff = c - r
    rd = rel_diff(c, r)
    rel_ok = rd is not None and abs(rd) <= D(tolerance_rel)
    abs_ok = tolerance_abs is not None and abs(diff) <= D(tolerance_abs)
    if rel_ok or abs_ok:
        num_verdict = "MATCH"
    else:
        num_verdict = "MISMATCH"

    if num_verdict == "MATCH" and scope_verdict and scope_verdict.startswith("OUT_OF_SCOPE"):
        verdict = "ARITHMETIC_OK_SCOPE_FAIL"
    elif num_verdict == "MISMATCH" and scope_verdict and scope_verdict.startswith("OUT_OF_SCOPE"):
        verdict = "ARITHMETIC_AND_SCOPE_FAIL"
    else:
        verdict = num_verdict

    return {
        "unit": unit,
        "claimed": S(c),
        "recomputed": S(r),
        "absolute_diff": S(diff),
        "relative_diff": (S(rd, 6) if rd is not None else None),
        "tolerance_rel": str(tolerance_rel),
        "numeric_verdict": num_verdict,
        "scope_verdict": scope_verdict,
        "verdict": verdict,
    }
