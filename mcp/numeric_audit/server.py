"""
numeric-audit-mcp — deterministic numeric re-computation and audit of intelligence briefs.

Purpose: catch one specific real error class —
    a figure lifted from secondary literature and applied outside its actual scope.

Method: every claim is compared against an INDEPENDENT RECOMPUTATION with a declared
derivation rule and a scope-tagged rule registry. Arithmetic is exact (decimal.Decimal,
prec=60) — money and capital numbers never transit through binary float.

Authority: ANALYSIS_ONLY. Re-computes and reports. Never judges a bank. Never seals.
Never writes VAULT999.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

from fastmcp import FastMCP

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import (  # type: ignore[import-not-found]  # noqa: E402
    audit_claim,
    check_units_scale,
    load_registry,
    recompute_sensitivity,
    replay_derivation,
    scope_check,
)

mcp = FastMCP(
    name="numeric-audit-mcp",
    version="2026.09.15",
    instructions=(
        "Deterministic numeric audit for intelligence briefs. "
        "Replays derivations with exact decimal arithmetic, lints unit/scale consistency, "
        "recomputes sensitivity tables from a declared method, and checks whether a cited "
        "figure is being applied INSIDE its canonical scope. "
        "Primary detector: a risk weight or ratio lifted from secondary literature and applied "
        "outside the exposure class it is actually defined for. "
        "Authority: ANALYSIS_ONLY — re-computes and reports; never seals, never judges a bank."
    ),
)


# ---------------------------------------------------------------------------
# 1. Registry
# ---------------------------------------------------------------------------

@mcp.tool()
def numeric_rule_lookup(
    figure_pct: str | None = None,
    contract: str | None = None,
    clause: str | None = None,
    rule_id: str | None = None,
) -> dict[str, Any]:
    """Look up the scope-tagged risk-weight registry.

    Every prescribed figure carries its CANONICAL SCOPE, its application basis, its
    conditions and a citation with document, clause, date, extrated-text file and line.

    args:
      figure_pct : e.g. "400" -> every rule that carries 400% AND what 400% actually covers.
      contract   : filter rules whose predicates cover a contract, e.g. "musyarakah_mutanaqisah".
      clause     : filter by source clause, e.g. "2.87".
      rule_id    : fetch one rule exactly.
    """
    reg = load_registry()
    rules = reg["rules"]
    if rule_id:
        rules = [r for r in rules if r["rule_id"] == rule_id]
    if clause:
        rules = [r for r in rules if clause in str(r["source"].get("clause", ""))]
    if figure_pct is not None:
        rules = [r for r in rules if figure_pct in r.get("figures_pct", [])]
    if contract:
        rules = [r for r in rules
                 if any(contract in (p.get("contract") or []) for p in r.get("applies_to", []))
                 or not any("contract" in p for p in r.get("applies_to", []))]

    out: dict[str, Any] = {
        "registry_id": reg["registry_id"],
        "version": reg["version"],
        "matched": len(rules),
        "rules": [
            {
                "rule_id": r["rule_id"],
                "figures_pct": r.get("figures_pct", []),
                "canonical_scope": r["canonical_scope"],
                "applies_to": r.get("applies_to", []),
                "basis": r["basis"],
                "conditions": r.get("conditions", []),
                "source": r["source"],
                "evidence_state": r.get("evidence_state"),
            }
            for r in rules
        ],
    }
    if figure_pct is not None:
        out["confusable_figures"] = reg.get("confusable_figures", {}).get(figure_pct,
                                                                          reg.get("confusable_figures", {}).get(str(figure_pct)))
    if not rules:
        out["note"] = ("no rule matched. An unmatched figure is UNVERIFIED, not approved — "
                       "trace it to a clause before it enters a brief.")
    return out


# ---------------------------------------------------------------------------
# 2. Derivation replay
# ---------------------------------------------------------------------------

@mcp.tool()
def numeric_replay_derivation(
    inputs: dict[str, Any],
    steps: list[dict[str, Any]],
) -> dict[str, Any]:
    """Replay a derivation chain with exact decimal arithmetic and return the full trace.

    ops: add, sub, mul, div, pct_of, rwa_from (exposure*weight%), capital_from_rwa (rwa*ratio%),
         ratio_from (capital/rwa*100), rwa_from_ratio (capital/(ratio%) -> implied RWA).

    inputs: {"equity_rm":"3.23","cet1_pct":"12.02"}
    steps : [{"id":"implied_rwa","op":"rwa_from_ratio","args":["equity_rm","cet1_pct"]}]

    Every operand and result is returned as an exact string so the trace can be
    re-run by hand on paper. Floats are rejected at the door.
    """
    result = replay_derivation(inputs, steps)
    result["ops"] = sorted([
        "add", "sub", "mul", "div", "pct_of", "rwa_from", "capital_from_rwa",
        "ratio_from", "rwa_from_ratio",
    ])
    return result


# ---------------------------------------------------------------------------
# 3. Units and scale
# ---------------------------------------------------------------------------

@mcp.tool()
def numeric_check_units_scale(
    claims: list[dict[str, Any]],
    tolerance_rel: str = "0.01",
) -> dict[str, Any]:
    """Lint numeric claims for unit/scale inconsistencies before they reach a reader.

    claim: {"id":"cet1","value":"12.02","unit":"%","basis":"CET1 capital / RWA",
            "quantity_key":"bank.cet1_ratio"}

    Detects: percent-vs-fraction confusion, bps/percent confusion, ~1000x million/billion
    drift, two claims of the same quantity that disagree beyond tolerance, and ratios
    whose basis is undeclared (CET1 capital vs shareholders' equity is not the same number).
    """
    return check_units_scale(claims, tolerance_rel=tolerance_rel)


# ---------------------------------------------------------------------------
# 4. Sensitivity-table recomputation
# ---------------------------------------------------------------------------

@mcp.tool()
def numeric_recompute_sensitivity(
    increments_rm: list[Any],
    base_rwa_rm: Any,
    base_capital_rm: Any,
    applied_weight_pct: Any,
    target_ratio_pct: Any,
    replacement_weight_pct: Any = "0",
    retained_share_pct: Any = "100",
    mitigant_factor: Any = "1",
    claimed_rows: list[dict[str, Any]] | None = None,
    tolerance_rm: Any = "0.1",
) -> dict[str, Any]:
    """Recompute a capital-sensitivity table from an explicitly declared derivation rule.

    added_rwa = increment * (applied_weight - replacement_weight)/100 * retained/100 * mitigant
    total_rwa = base_rwa + added_rwa
    required  = total_rwa * target_ratio/100
    new_cap   = required - base_capital

    replacement_weight_pct is the weight the same exposure ALREADY carried. 0 = gross basis;
    the prevailing weight = net/incremental basis. A table reporting a net-of-replacement number
    without declaring that step is hiding a derivation step, and this tool makes it visible.

    Pass claimed_rows (list of {"increment_rm","implied_rwa_rm","new_capital_rm"}) to get a
    row-by-row match/mismatch against the published table.
    """
    return recompute_sensitivity(
        increments_rm=increments_rm,
        base_rwa_rm=base_rwa_rm,
        base_capital_rm=base_capital_rm,
        applied_weight_pct=applied_weight_pct,
        target_ratio_pct=target_ratio_pct,
        replacement_weight_pct=replacement_weight_pct,
        retained_share_pct=retained_share_pct,
        mitigant_factor=mitigant_factor,
        claimed_rows=claimed_rows,
        tolerance_rm=tolerance_rm,
    )


# ---------------------------------------------------------------------------
# 5. Scope check — the error-class catcher
# ---------------------------------------------------------------------------

@mcp.tool()
def numeric_scope_check(
    figure_pct: str,
    scope: dict[str, Any],
    basis: str | None = None,
) -> dict[str, Any]:
    """Decide whether a cited figure is being applied INSIDE its canonical scope.

    This is the primary detector for the error class. A figure can be perfectly
    quoted and still be wrong, because it belongs to a different exposure class.

    scope vocab: contract (musyarakah|musyarakah_mutanaqisah|mudarabah|murabahah|tawarruq|
                 ijarah|unspecified), exposure_basis (profit_and_loss_sharing_financing|
                 equity_holding|project_financing|sub_contract|real_estate_residential|
                 real_estate_commercial|specialised_financing|retail_other|corporate),
                 position (banking_book|trading_book), listing (publicly_traded|
                 non_publicly_traded|not_applicable), counterparty (retail|corporate|sme|fi|
                 sovereign|not_applicable)
    basis: flat_all | category_dependent | counterparty_dependent | pass_through |
           discretionary_increase | None (undeclared)

    Verdicts: IN_SCOPE | IN_SCOPE_CONDITIONAL | OUT_OF_SCOPE_FIGURE | FIGURE_NOT_IN_REGISTRY.
    An out-of-scope figure returns the in-scope weight range and the overstatement factor.
    """
    return scope_check(figure_pct, scope, basis=basis)


# ---------------------------------------------------------------------------
# 6. Claim vs recomputation
# ---------------------------------------------------------------------------

@mcp.tool()
def numeric_audit_claim(
    claim_value: str,
    recomputed_value: str,
    unit: str = "",
    tolerance_rel: str = "0.01",
    tolerance_abs: str | None = None,
    scope_verdict: str | None = None,
) -> dict[str, Any]:
    """Compare a published claim against an independently recomputed value.

    A numeric match NEVER overrides a scope failure. If the arithmetic is right but the
    input was out of scope the verdict is ARITHMETIC_OK_SCOPE_FAIL — arithmetic agreement
    is not corroboration.
    """
    kw: dict[str, Any] = {}
    if tolerance_abs is not None:
        kw["tolerance_abs"] = tolerance_abs
    return audit_claim(claim_value, recomputed_value, unit=unit,
                       tolerance_rel=tolerance_rel, scope_verdict=scope_verdict, **kw)


# ---------------------------------------------------------------------------
# 7. Composite brief audit
# ---------------------------------------------------------------------------

@mcp.tool()
def numeric_audit_brief(payload: dict[str, Any]) -> dict[str, Any]:
    """Run the full audit on a brief fragment: scope + derivation + sensitivity, in one packet.

    payload:
    {
      "label": "...",
      "claims": [ {"id","value","unit","basis","quantity_key"} ... ],          # optional
      "derivation": {"inputs": {...}, "steps": [...]},                          # optional
      "scope_checks": [ {"figure_pct","scope","basis","applies_to_label"} ],    # optional
      "sensitivity": {"increments_rm":[...], "base_rwa_rm":"26.9", "base_capital_rm":"3.23",
                      "applied_weight_pct":"400", "target_ratio_pct":"15",
                      "replacement_weight_pct":"100", "claimed_rows":[...]},   # optional
      "numeric_claims_to_compare": [ {"label","claimed","recomputed","unit","scope_verdict"} ]  # optional
    }

    Returns a single verdict packet: NOT_ZERO_BLOCKER / SCOPE_FAIL / ARITHMETIC_FAIL / CLEAN,
    with each finding carrying the clause that decides it.
    """
    payload = payload or {}
    out: dict[str, Any] = {"label": payload.get("label", "unnamed"), "authority": "ANALYSIS_ONLY"}

    if payload.get("claims"):
        out["units_scale"] = check_units_scale(payload["claims"])
    if payload.get("derivation"):
        d = payload["derivation"]
        out["derivation"] = replay_derivation(d.get("inputs", {}), d.get("steps", []))
    if payload.get("scope_checks"):
        out["scope_checks"] = []
        for sc in payload["scope_checks"]:
            res = scope_check(sc["figure_pct"], sc.get("scope", {}), basis=sc.get("basis"))
            res["applies_to_label"] = sc.get("applies_to_label")
            out["scope_checks"].append(res)
    if payload.get("sensitivity"):
        s = payload["sensitivity"]
        out["sensitivity"] = recompute_sensitivity(
            increments_rm=s["increments_rm"],
            base_rwa_rm=s.get("base_rwa_rm"),
            base_capital_rm=s.get("base_capital_rm"),
            applied_weight_pct=s["applied_weight_pct"],
            target_ratio_pct=s["target_ratio_pct"],
            replacement_weight_pct=s.get("replacement_weight_pct", "0"),
            retained_share_pct=s.get("retained_share_pct", "100"),
            mitigant_factor=s.get("mitigant_factor", "1"),
            claimed_rows=s.get("claimed_rows"),
            tolerance_rm=s.get("tolerance_rm", "0.1"),
        )
    if payload.get("numeric_claims_to_compare"):
        out["claim_comparisons"] = [
            audit_claim(c["claimed"], c["recomputed"], unit=c.get("unit", ""),
                        tolerance_rel=c.get("tolerance_rel", "0.01"),
                        scope_verdict=c.get("scope_verdict"))
            for c in payload["numeric_claims_to_compare"]
        ]

    blockers: list[dict[str, Any]] = []
    for sc in out.get("scope_checks", []):
        if sc["verdict"] == "OUT_OF_SCOPE_FIGURE":
            blockers.append({"class": "SCOPE_OUT_OF_RANGE", "label": sc.get("applies_to_label"),
                             "figure_pct": sc["figure_pct"],
                             "in_scope_weight_range_pct": sc.get("in_scope_weight_range_pct"),
                             "overstatement_factor": sc.get("overstatement_factor_vs_max_in_scope")})
        elif sc["verdict"] == "FIGURE_NOT_IN_REGISTRY":
            blockers.append({"class": "FIGURE_UNVERIFIED", "label": sc.get("applies_to_label"),
                             "figure_pct": sc["figure_pct"]})
    for cm in out.get("claim_comparisons", []):
        if cm["verdict"] != "MATCH":
            blockers.append({"class": cm["verdict"], "claimed": cm["claimed"],
                             "recomputed": cm["recomputed"], "unit": cm.get("unit")})
    for f in (out.get("units_scale") or {}).get("findings", []):
        if f.get("severity") == "P0":
            blockers.append({"class": "UNIT_SCALE_" + f["check"], "detail": f["detail"]})
    if (out.get("sensitivity") or {}).get("internal_consistency") == "MISMATCH":
        blockers.append({"class": "SENSITIVITY_TABLE_MISMATCH",
                         "mismatches": out["sensitivity"]["mismatches"]})

    classes = {b["class"] for b in blockers}
    if any(c.startswith("UNIT_SCALE") or c.startswith("ARITHMETIC_") for c in classes):
        verdict = "NOT_ZERO_BLOCKER"
    elif "SCOPE_OUT_OF_RANGE" in classes or "ARITHMETIC_OK_SCOPE_FAIL" in classes:
        verdict = "SCOPE_FAIL"
    elif "MISMATCH" in classes or "SENSITIVITY_TABLE_MISMATCH" in classes:
        verdict = "ARITHMETIC_FAIL"
    elif "FIGURE_UNVERIFIED" in classes:
        verdict = "HOLD_UNVERIFIED"
    else:
        verdict = "CLEAN"

    out["verdict"] = verdict
    out["blockers"] = blockers
    out["arithmetic"] = "exact (decimal.Decimal, prec=60) — no float transit"
    return out


@mcp.resource("numeric-audit://registry")
def registry_resource() -> str:
    """The full scope-tagged risk-weight rule registry (JSON)."""
    return json.dumps(load_registry(), indent=2, sort_keys=True)


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=3013)
