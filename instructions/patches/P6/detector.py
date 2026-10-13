"""
hermes_contradiction_scan — PATCH 6 (REVISED 2026-10-11)

Additive detector. Pure-function module. Read-only. No canonical-store mutation.
No verdict semantics, no authorization authority, no governance output.

Inputs: a list of atomic claims with stable IDs and structured fields.
Output: list of contradiction rows, each labelled by class and status.

This module is deliberately framework-free (no FastMCP decorators here) so it
can be unit-tested in isolation. The MCP tool wrapper that imports this module
lives in server.py. Backup of pre-patch server.py at:
  /root/AAA/instructions/.patch-receipts/P6_server.py.before.md
Pre-SHA: 1d441f7ee65c58743f528a1bd9d68b14e2a2defbb7234297640543feddf3b798
"""

from __future__ import annotations
import re
import json
from typing import Any, Dict, List, Optional, Tuple

# Allowed classes and status (closed enums — never widen without a contract bump).
CLASSES = {
    "SCOPE",
    "DENOMINATOR",
    "SOURCE",
    "TEMPORAL",
    "MODEL_VERSUS_MODEL",
    "MODEL_VERSUS_REALITY",
    "MEASUREMENT_VERSUS_INTERPRETATION",
    "FORECAST_VERSUS_OUTCOME",
    "HEADLINE_VERSUS_BODY",
    "UNKNOWN",
}
STATUSES = {"RESOLVED_BY_SCOPE", "PARTIALLY_RECONCILED", "OPEN", "UNKNOWN"}

# Numeric patterns for MYR/USD/bbl/percent/date.
_MONEY_RE = re.compile(r"RM\s?(\d+(?:\.\d+)?)\s?(b|m|million|billion|k)?", re.I)
_USD_RE = re.compile(r"USD\s?(\d+(?:\.\d+)?)(?:\s?/bbl)?", re.I)
_PCT_RE = re.compile(r"(\d+(?:\.\d+)?)\s?(?:%|percent\b)", re.I)
_BBL_RE = re.compile(r"(\d+(?:\.\d+)?)\s?(?:MM)?bbl", re.I)
_FCAST_HINTS = ("forecast", "target", "estimate", "expected", "expected to", "projection", "will ", " 2027", "2028")
_REPORT_HINTS = ("announced", "tabled", "stated", "told parliament", "reported", "released", "confirmed", "today")
_DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2}|20\d{2}/\d{2}/\d{2})\b")


def _norm_money(n: float, unit: Optional[str]) -> Tuple[float, str]:
    """Normalize money to RM-billions as a comparable scalar."""
    u = (unit or "b").lower()
    if u in ("b", "billion"): return n, "RM_b"
    if u in ("m", "million"):  return n / 1000.0, "RM_b"
    if u == "k":               return n / 1_000_000.0, "RM_b"
    return n, "RM_" + (u or "b")


def _extract_numbers(text: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    money = []
    for m in _MONEY_RE.finditer(text):
        v = float(m.group(1))
        u = (m.group(2) or "b")
        money.append({"raw": m.group(0), "value_b_RM": _norm_money(v, u)[0]})
    usd = []
    for m in _USD_RE.finditer(text):
        usd.append({"raw": m.group(0), "value_usd": float(m.group(1))})
    pct = [float(m.group(1)) for m in _PCT_RE.finditer(text)]
    bbl = [float(m.group(1)) for m in _BBL_RE.finditer(text)]
    if money: out["money_RM_b"] = money
    if usd:   out["usd"] = usd
    if pct:   out["pct"] = pct
    if bbl:   out["bbl"] = bbl
    return out


def _tense(text: str) -> str:
    t = text.lower()
    if any(h in t for h in _FCAST_HINTS): return "FORECAST"
    if any(h in t for h in _REPORT_HINTS): return "REPORTED"
    return "AMBIGUOUS"


def _first_date(text: str) -> Optional[str]:
    m = _DATE_RE.search(text)
    return m.group(1) if m else None


def _norm(s: Optional[str]) -> str:
    return (s or "").strip().lower()


def _source_cluster_id(source: Optional[str]) -> str:
    """
    Cluster sources on domain-of-origin. A syndicated wire under three
    publishers is ONE cluster, not three independent corroborations.
    cluster_id('Reuters …') == 'reuters_wire'
    """
    s = _norm(source)
    if not s: return "unknown"
    if "reuters" in s:    return "reuters_wire"
    if "thestar" in s or "the star" in s: return "thestar"
    if "nst" in s:        return "nst"
    if "theedgemalaysia" in s or "edge" in s: return "edge"
    if "federated" in s or "mof" in s or "treasury" in s or "belanjawan" in s: return "mof_primary"
    if "bernam" in s:     return "bernama_wire"
    if "malaymail" in s:  return "malaymail"
    if "channelnewsasia" in s or "cna" in s:  return "cna"
    if "freemalaysia" in s or "fmt" in s:    return "fmt"
    if "malaysiakini" in s: return "malaysiakini"
    return s.split("@")[-1].split(".")[-2] if "." in s else "unknown"


def _row(counter: int, klass: str, a: Dict[str, Any], b: Dict[str, Any],
        subject: str, unit: str, denom_a: Optional[str], denom_b: Optional[str],
        source_a: Optional[str], source_b: Optional[str],
        status: str, evidence: str, reconciliation: str, decision: str) -> Dict[str, Any]:
    if klass not in CLASSES:  raise ValueError(f"illegal class {klass!r}")
    if status not in STATUSES: raise ValueError(f"illegal status {status!r}")
    return {
        "contradiction_id": f"cscan-{counter:04d}",
        "claim_a_id": a.get("id"),
        "claim_b_id": b.get("id"),
        "class": klass,
        "source_a": source_a,
        "source_b": source_b,
        "subject": subject,
        "unit": unit,
        "temporal_scope": {"a": _first_date(a.get("text", "")),
                           "b": _first_date(b.get("text", ""))},
        "geographic_scope": a.get("geography") or "MY",
        "denominator_a": denom_a,
        "denominator_b": denom_b,
        "possible_reconciliation": reconciliation,
        "evidence_needed": evidence,
        "decision_impact": decision,
        "status": status,
        "limitations": ["hermes_contradiction_scan is semantic evidence only; "
                        "no authority effect, no canonical-store mutation"],
    }


def scan(claims: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Public entrypoint. Accepts a list of claim dicts:
        {id, text, source, time, principal, geography, kind}
    Returns {"ok": True, "contradictions": [...], "source_clusters": {...}}.
    NEVER writes to canonical store. NEVER returns a verdict.
    """
    if not isinstance(claims, list):
        return {"ok": False, "error": "claims must be a list", "contradictions": []}

    # Step 0: cluster sources up front. Independent corroboration requires distinct clusters.
    cluster_for = {c.get("id"): _source_cluster_id(c.get("source")) for c in claims}

    rows: List[Dict[str, Any]] = []
    counter = 1

    # Track per-claim numeric facts so we can compare across all pairings.
    parsed = []
    for c in claims:
        nums = _extract_numbers(c.get("text", ""))
        parsed.append({
            "claim": c,
            "nums": nums,
            "tense": _tense(c.get("text", "")),
            "kind": c.get("kind"),
            "principal": c.get("principal"),
        })

    def same_principal(a, b):
        if not a.get("principal") or not b.get("principal"): return True
        return _norm(a["principal"]) == _norm(b["principal"])

    def same_geography(a, b):
        return _norm(a.get("claim").get("geography") or "MY") == _norm(b.get("claim").get("geography") or "MY")

    def same_unit(a, b):
        if not a.get("nums") or not b.get("nums"): return False
        # Compatible only if both have at least one money, OR pct, OR usd, OR bbl.
        ak = set(a["nums"].keys())
        bk = set(b["nums"].keys())
        return bool(ak & bk)

    # -------------------------------------------------------------------------
    # A. SCOPE — different money totals that both reference the same subject;
    #    explanation is perimeter difference (e.g. RM510b vs RM459.8b).
    # -------------------------------------------------------------------------
    for i, a in enumerate(parsed):
        for j, b in enumerate(parsed):
            if j <= i: continue
            if not same_principal(a, b): continue
            if not same_geography(a, b): continue
            am = a["nums"].get("money_RM_b", [])
            bm = b["nums"].get("money_RM_b", [])
            if not am or not bm: continue
            av = am[0]["value_b_RM"]; bv = bm[0]["value_b_RM"]
            if abs(av - bv) < 1e-9: continue  # identical
            txt_a = (a["claim"].get("text") or "").lower()
            txt_b = (b["claim"].get("text") or "").lower()
            # Heuristic: if either side mentions "off-budget" or "GLIC" or "PPP" or
            # "statutory" we accept scope reconciliation; otherwise flag SOURCE.
            off_a = any(h in txt_a for h in ("off-budget", "glic", "statutory", "ppp", "investment"))
            off_b = any(h in txt_b for h in ("off-budget", "glic", "statutory", "ppp", "investment"))
            if off_a or off_b:
                rows.append(_row(
                    counter, "SCOPE", a["claim"], b["claim"],
                    subject=str(_norm(a["claim"].get("principal")) or "amount"),
                    unit="RM_b", denom_a="claims_with_investment_units" if off_a else "claims_alone",
                    denom_b="claims_with_investment_units" if off_b else "claims_alone",
                    source_a=a["claim"].get("source"),
                    source_b=b["claim"].get("source"),
                    status="RESOLVED_BY_SCOPE",
                    evidence="explicit perimeter token on at least one side",
                    reconciliation="one totals federal alone; the other adds statutory/off-budget",
                    decision="treat the smaller figure as the federal operating budget"))
                counter += 1
            else:
                rows.append(_row(
                    counter, "SOURCE", a["claim"], b["claim"],
                    subject=str(_norm(a["claim"].get("principal")) or "amount"),
                    unit="RM_b", denom_a=None, denom_b=None,
                    source_a=a["claim"].get("source"),
                    source_b=b["claim"].get("source"),
                    status="OPEN",
                    evidence="no perimeter token; cannot tell whether scope or source divergence",
                    reconciliation="verify whether b excludes statutory/off-budget categories",
                    decision="do not pick either figure as 'true' budget size"))
                counter += 1

    # -------------------------------------------------------------------------
    # B. MODEL_VERSUS_MODEL / MODEL_VERSUS_REALITY — same quantity, model vs world.
    # -------------------------------------------------------------------------
    for i, a in enumerate(parsed):
        for j, b in enumerate(parsed):
            if j <= i: continue
            if not same_principal(a, b): continue
            if not same_geography(a, b): continue
            at = a["tense"]; bt = b["tense"]
            if at == "FORECAST" and bt == "FORECAST":
                # Two competing forecasters.
                if cluster_for.get(a["claim"].get("id")) == cluster_for.get(b["claim"].get("id")):
                    continue  # same wire → not independent
                if same_unit(a, b):
                    rows.append(_row(
                        counter, "MODEL_VERSUS_MODEL", a["claim"], b["claim"],
                        subject=str(_norm(a["claim"].get("principal")) or "forecast"),
                        unit="mixed", denom_a=None, denom_b=None,
                        source_a=a["claim"].get("source"),
                        source_b=b["claim"].get("source"),
                        status="OPEN",
                        evidence="two independent forecasting sources, conflicting values",
                        reconciliation="requires outturn or pre-budget update to converge",
                        decision="treat as forecast band, not point estimate"))
                    counter += 1
            if (at == "FORECAST" and bt == "REPORTED") or (at == "REPORTED" and bt == "FORECAST"):
                if not same_unit(a, b): continue
                rows.append(_row(
                    counter, "FORECAST_VERSUS_OUTCOME", a["claim"], b["claim"],
                    subject=str(_norm(a["claim"].get("principal")) or "quantity"),
                    unit="mixed", denom_a=None, denom_b=None,
                    source_a=a["claim"].get("source"),
                    source_b=b["claim"].get("source"),
                    status="OPEN",
                    evidence="forecast tense vs reported tense on same quantity",
                    reconciliation="compare predicted value against most recent outturn",
                    decision="do not collapse the band"))
                counter += 1

    # -------------------------------------------------------------------------
    # C. MODEL_VERSUS_REALITY — model oil assumption vs reported spot.
    # -------------------------------------------------------------------------
    oil_assumption = [p for p in parsed if "usd" in p["nums"] and "oil" in (p["claim"].get("principal") or "")]
    oil_spot       = [p for p in parsed if "usd" in p["nums"] and ("spot" in (p["claim"].get("text", "").lower())
                                                   or "brent" in (p["claim"].get("text", "").lower()))]
    for a in oil_assumption:
        for b in oil_spot:
            av = a["nums"]["usd"][0]["value_usd"]
            bv = b["nums"]["usd"][0]["value_usd"]
            if abs(av - bv) < 1: continue
            rows.append(_row(
                counter, "MODEL_VERSUS_REALITY", a["claim"], b["claim"],
                subject="oil_assumption_vs_spot", unit="USD_per_bbl",
                denom_a=None, denom_b=None,
                source_a=a["claim"].get("source"), source_b=b["claim"].get("source"),
                status="OPEN",
                evidence=f"model={av} vs spot={bv} (gap > 1 USD)",
                reconciliation="report actual average over the same period the model applies to",
                decision="until reconciled, do not credit the model assumption as observed reality"))
            counter += 1

    # -------------------------------------------------------------------------
    # D. DENOMINATOR — same quantity, different scope (subsidy scope class).
    # -------------------------------------------------------------------------
    subsidy_claims = [p for p in parsed if "subsid" in (p["claim"].get("text", "").lower())]
    for i, a in enumerate(subsidy_claims):
        for j, b in enumerate(subsidy_claims):
            if j <= i: continue
            am = a["nums"].get("money_RM_b", [])
            bm = b["nums"].get("money_RM_b", [])
            if not am or not bm: continue
            av = am[0]["value_b_RM"]; bv = bm[0]["value_b_RM"]
            if abs(av - bv) < 1e-9: continue
            ta = (a["claim"].get("text") or "").lower()
            tb = (b["claim"].get("text") or "").lower()
            sa = any(k in ta for k in ("fuel", "ron95", "diesel", "petrol"))
            sb = any(k in tb for k in ("fuel", "ron95", "diesel", "petrol"))
            rows.append(_row(
                counter, "DENOMINATOR", a["claim"], b["claim"],
                subject="subsidy_total", unit="RM_b",
                denom_a="fuel-only" if sa else "subsidies+incentives",
                denom_b="fuel-only" if sb else "subsidies+incentives",
                source_a=a["claim"].get("source"),
                source_b=b["claim"].get("source"),
                status="PARTIALLY_RECONCILED" if (sa != sb) else "OPEN",
                evidence="different sub-basket coverage between two sources",
                reconciliation="request Fiscal Outlook Section 3 for the canonical denominator",
                decision="do not present either as 'the' subsidy figure until reconciled"))
            counter += 1

    # -------------------------------------------------------------------------
    # E. MEASUREMENT_VERSUS_INTERPRETATION — same period percent on conflicting base.
    # -------------------------------------------------------------------------
    pct_claims = [p for p in parsed if p["nums"].get("pct")]
    for i, a in enumerate(pct_claims):
        for j, b in enumerate(pct_claims):
            if j <= i: continue
            ap = a["nums"]["pct"]; bp = b["nums"]["pct"]
            if abs(ap[0] - bp[0]) < 0.05: continue
            ta = (a["claim"].get("text") or "").lower()
            tb = (b["claim"].get("text") or "").lower()
            if "below" in ta or "below" in tb or "under" in tb or "above" in ta:
                rows.append(_row(
                    counter, "MEASUREMENT_VERSUS_INTERPRETATION", a["claim"], b["claim"],
                    subject="deficit_period_measurement", unit="pct",
                    denom_a=None, denom_b=None,
                    source_a=a["claim"].get("source"),
                    source_b=b["claim"].get("source"),
                    status="OPEN",
                    evidence="percentage quoted both 'above X%' and 'below X%' for similar period",
                    reconciliation="request the underlying monthly deficit number",
                    decision="do not pick which percentage is correct; preserve both"))
                counter += 1

    # -------------------------------------------------------------------------
    # F. SELF-INCONSISTENT WORDING — within a single claim, two distinct percentages
    #    BOTH compared to a target with directional words in non-monotonic order.
    #    E.g. "1H 4.2 percent ... well below ... 3.5 percent" — the higher 1H figure
    #    cannot be "well below" the lower target; text is internally inconsistent.
    # -------------------------------------------------------------------------
    _ABOVE_WORDS = ("above ", "above ", "exceeds ", "above ", "more than ")
    _BELOW_WORDS = ("below", "below", "under", "less than", "smaller than")
    for c in parsed:
        t = c["claim"].get("text", "")
        tl = t.lower()
        if len(c["nums"].get("pct", [])) < 2: continue
        # For each percentage in text, capture the window of 30 chars after it
        # and label it (above | below | neutral).
        items = []
        for m in _PCT_RE.finditer(t):
            v = float(m.group(1))
            window = tl[m.end(): m.end() + 30]
            if any(w in window for w in _ABOVE_WORDS):  label = "ABOVE"
            elif any(w in window for w in _BELOW_WORDS): label = "BELOW"
            else:                                       label = "NEUTRAL"
            items.append((m.start(), v, label))
        # Two-percent comparison across windows: if a higher value is labeled BELOW
        # a lower target, the text incommensurately compares percentages.
        sorted_by_pos = sorted(items, key=lambda x: x[0])
        if len(sorted_by_pos) >= 2:
            v_first, l_first = sorted_by_pos[0][1], sorted_by_pos[0][2]
            v_second, l_second = sorted_by_pos[1][1], sorted_by_pos[1][2]
            if v_first > v_second and l_first == "BELOW":
                # "X.X% ... below ... Y.Y% (Y < X)"; claim is internally inconsistent.
                rows.append(_row(
                    counter, "MEASUREMENT_VERSUS_INTERPRETATION", c["claim"], c["claim"],
                    subject="self_inconsistent_period_percentage", unit="pct",
                    denom_a=None, denom_b=None,
                    source_a=c["claim"].get("source"),
                    source_b=c["claim"].get("source"),
                    status="OPEN",
                    evidence=f"text says {v_first}% is BELOW {v_second}%; numerically larger number reported as smaller",
                    reconciliation="ask source to clarify whether 1H figure or target is the correct numerator",
                    decision="do not pick which percentage is correct; preserve both as written"))
                counter += 1

    # Deduplicate identical rows (same pair, same class, same status).
    dedup = []
    seen = set()
    for r in rows:
        k = (r["claim_a_id"], r["claim_b_id"], r["class"], r["status"])
        if k in seen: continue
        seen.add(k)
        dedup.append(r)

    return {
        "ok": True,
        "contradictions": dedup,
        "source_clusters": {c.get("id"): cluster_for.get(c.get("id")) for c in claims},
        "limitations": [
            "deterministic numeric parser; figures written as words ('RM ten billion') are not extracted",
            "percent symbol (%) and word 'percent of GDP' are both extracted",
            "does not weight sources; agents must apply judgment off this surface",
            "does not persist; passing claims to the detector twice produces the same output"
        ],
    }


def fixture_eight_claims() -> List[Dict[str, Any]]:
    """
    Eight-claim Budget 2027 fixture used by the retest. The function preserves
    stable IDs so retests stay comparable.
    """
    return [
        {"id": "C1", "text": "Federal spending 2027 totals RM510 billion including statutory and PPP investment",
         "source": "mof.gov.my/belanjawan2027", "principal": "federal_budget_total",
         "geography": "MY", "kind": "REPORTED", "time": "2026-10-09"},
        {"id": "C2", "text": "Federal operating spending 2027 totals RM459.8 billion",
         "source": "Reuters world/asia-pacific 2026-10-09", "principal": "federal_budget_total",
         "geography": "MY", "kind": "REPORTED", "time": "2026-10-09"},
        {"id": "C3", "text": "PETRONAS dividend to federal government 2027 will be RM32 billion",
         "source": "mof fiscal outlook 2027",
         "principal": "petronas_dividend", "geography": "MY", "kind": "FORECAST", "time": "2026-10-09"},
        {"id": "C4", "text": "Petronas dividend to federal government 2027 estimated around RM25 billion",
         "source": "CIMB research The Edge 2026-10-07",
         "principal": "petronas_dividend", "geography": "MY", "kind": "FORECAST", "time": "2026-10-07"},
        {"id": "C5", "text": "2027 deficit target is 3.3 percent of GDP",
         "source": "mof budget speech 2027",
         "principal": "deficit_pct_gdp", "geography": "MY", "kind": "FORECAST", "time": "2026-10-09"},
        {"id": "C6", "text": "Deficit could remain at 3.6 percent of GDP in 2027",
         "source": "OCBC research Business Today 2026-09-25",
         "principal": "deficit_pct_gdp", "geography": "MY", "kind": "FORECAST", "time": "2026-09-25"},
        {"id": "C7", "text": "Government subsidies, aid and incentives for 2027 exceed RM80 billion including fuel subsidy about RM40 billion",
         "source": "mof budget speech 2027",
         "principal": "subsidy_total", "geography": "MY", "kind": "REPORTED", "time": "2026-10-09"},
        {"id": "C8", "text": "Subsidy spend falls marginally to RM72.7 billion in 2027",
         "source": "Reuters world/asia-pacific 2026-10-09",
         "principal": "subsidy_total", "geography": "MY", "kind": "REPORTED", "time": "2026-10-09"},
        {"id": "C9", "text": "Brent crude traded at about USD85 per barrel as the 2026 average assumption",
         "source": "mof fiscal outlook 2027",
         "principal": "oil_assumption", "geography": "MY", "kind": "FORECAST", "time": "2026-10-09"},
        {"id": "C10", "text": "Brent crude spot price USD101 per barrel reported on 11 September",
         "source": "The Star 2026-09-11",
         "principal": "oil_spot_observation", "geography": "MY", "kind": "REPORTED", "time": "2026-09-11"},
        {"id": "C11", "text": "Federal deficit 1H 2026 about 4.2 percent and well below targeted 3.5 percent",
         "source": "The Star column via Webull 2026-09-27",
         "principal": "deficit_pct_gdp", "geography": "MY", "kind": "REPORTED", "time": "2026-09-27"},
    ]
