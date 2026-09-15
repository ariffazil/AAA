"""
filings-mcp — FastMCP server for Malaysian + US financial/regulatory filings.

Authority: READ_ONLY external retrieval. This server never mutates federation
state, never writes VAULT999, never judges. It fetches, hashes, caches, and
returns structured JSON with a provenance block on every external payload.

PROVENANCE CONTRACT (every tool result carrying external data):
  {source_url, fetched_at_utc, sha256, http_status, cached}
sha256 is over the exact response bytes. Cache is sha256-addressed under
./cache/ with a url->sha256 index; the same URL is not refetched within 24h.

LANES (verified live 2026-09-15 from KVM8 'forge'):
  US  SEC EDGAR full-text search   https://efts.sec.gov/LATEST/search-index   [200]
  US  SEC EDGAR submissions        https://data.sec.gov/submissions/          [200]
  US  SEC EDGAR XBRL facts         https://data.sec.gov/api/xbrl/companyfacts [200]
  US  SEC ticker->CIK map          https://www.sec.gov/files/company_tickers  [200]
  MY  BNM Open API                 https://api.bnm.gov.my/public/             [200]
  MY  data.gov.my catalogue API    https://api.data.gov.my/data-catalogue     [200]
  MY  Bursa Malaysia announcements https://www.bursamalaysia.com/api/v1/...  [403]
      -> Cloudflare interstitial ("Just a moment..."). NOT bypassed. Reported
         honestly by filings_source_health(); no simulated announcements.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastmcp import FastMCP

# ---------------------------------------------------------------- config

HOST = "127.0.0.1"
PORT = 18410
BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
INDEX_PATH = CACHE_DIR / "index.json"

CACHE_TTL_SECONDS = 24 * 60 * 60

# SEC requires a descriptive User-Agent with contact info (fair-access policy).
UA = "arifOS-filings-mcp/1.0 (contact: arif@arif-fazil.com)"
SEC_UA = UA

mcp = FastMCP(
    name="filings-mcp",
    version="2026.09.15",
    instructions=(
        "filings-mcp — structured access to Malaysian + US financial/regulatory "
        "filings. US lane: SEC EDGAR (full-text search, filing indexes, XBRL "
        "company facts, ticker->CIK resolution). MY lane: Bank Negara Malaysia "
        "Open API (OPR, base rates, exchange rates) and data.gov.my official "
        "open-data catalogues. Authority: READ_ONLY. Every external payload "
        "carries {source_url, fetched_at_utc, sha256, http_status, cached}. "
        "Bursa Malaysia's announcement API is Cloudflare-gated and is NOT "
        "bypassed — call filings_source_health for the live verdict."
    ),
)


# ---------------------------------------------------------------- cache

def _load_index() -> dict[str, Any]:
    try:
        return json.loads(INDEX_PATH.read_text())
    except Exception:
        return {}


def _save_index(idx: dict[str, Any]) -> None:
    tmp = INDEX_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(idx, indent=1, sort_keys=True))
    tmp.replace(INDEX_PATH)


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class FetchResult(dict):
    """dict with attribute access for provenance keys + .body convenience."""

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(name) from e

    @property
    def body(self) -> bytes:
        return self["_body"]

    @property
    def status(self) -> int:
        return self["http_status"]

    @property
    def sha256(self) -> str:
        return self["sha256"]

    @property
    def cached(self) -> bool:
        return self["cached"]

    def provenance(self) -> dict[str, Any]:
        return {
            "source_url": self["source_url"],
            "fetched_at_utc": self["fetched_at_utc"],
            "sha256": self["sha256"],
            "http_status": self["http_status"],
            "cached": self["cached"],
        }


def fetch(
    url: str,
    *,
    accept: str | None = None,
    user_agent: str = UA,
    timeout: int = 30,
    max_bytes: int = 8_000_000,
    allow_redirect: bool = True,
) -> FetchResult:
    """Fetch a URL with sha256-addressed caching (24h TTL, per URL).

    Never raises on HTTP error status — returns the status and body so the
    caller can report the real upstream response instead of fabricating data.
    """
    idx = _load_index()
    entry = idx.get(url)
    now = time.time()

    if entry and (now - entry.get("fetched_at_epoch", 0)) < CACHE_TTL_SECONDS:
        blob = CACHE_DIR / f"{entry['sha256']}.bin"
        if blob.exists():
            return FetchResult(
                source_url=url,
                fetched_at_utc=entry["fetched_at_utc"],
                sha256=entry["sha256"],
                http_status=entry["http_status"],
                cached=True,
                _body=blob.read_bytes()[:max_bytes],
            )

    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    if accept:
        req.add_header("Accept", accept)

    status = 0
    body = b""
    err = None
    try:
        opener = urllib.request.build_opener()
        if not allow_redirect:
            class _NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, *a, **k):  # noqa: D102
                    return None
            opener = urllib.request.build_opener(_NoRedirect)
        with opener.open(req, timeout=timeout) as resp:
            status = resp.status
            body = resp.read(max_bytes)
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            body = e.read(max_bytes)
        except Exception:
            body = b""
        err = f"HTTP {e.code} {e.reason}"
    except Exception as e:  # URLError, timeout, DNS, TLS
        status = 0
        err = f"{type(e).__name__}: {e}"

    digest = hashlib.sha256(body).hexdigest()
    stamp = _now_utc()

    if status:  # only cache real HTTP responses
        blob = CACHE_DIR / f"{digest}.bin"
        if not blob.exists():
            blob.write_bytes(body)
        idx[url] = {
            "sha256": digest,
            "fetched_at_utc": stamp,
            "fetched_at_epoch": now,
            "http_status": status,
            "bytes": len(body),
        }
        _save_index(idx)

    out = FetchResult(
        source_url=url,
        fetched_at_utc=stamp,
        sha256=digest,
        http_status=status,
        cached=False,
        _body=body,
    )
    if err:
        out["error"] = err
    return out


def json_or_error(res: FetchResult) -> tuple[Any | None, dict[str, Any] | None]:
    """Parse JSON body; return (data, error_payload)."""
    if res.status != 200:
        return None, {
            "error": "upstream_non_200",
            "http_status": res.status,
            "response_excerpt": res.body.decode("utf-8", "replace")[:600],
            "provenance": res.provenance(),
        }
    try:
        return json.loads(res.body.decode("utf-8", "replace")), None
    except Exception as e:
        return None, {
            "error": "upstream_not_json",
            "detail": str(e),
            "response_excerpt": res.body.decode("utf-8", "replace")[:600],
            "provenance": res.provenance(),
        }


# ---------------------------------------------------------------- helpers

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"[ \t\r\f\v]+")


def _strip_html(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?i)</(p|div|tr|h[1-6]|li)>", "\n", raw)
    txt = _TAG_RE.sub(" ", raw)
    txt = (txt.replace("&nbsp;", " ").replace("&amp;", "&")
              .replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
              .replace("&#39;", "'"))
    lines = [_WS_RE.sub(" ", ln).strip() for ln in txt.split("\n")]
    return "\n".join(ln for ln in lines if ln)


def _pad_cik(cik: str | int) -> str:
    return f"{int(str(cik).lstrip('0') or 0):010d}"


_TICKERS: dict[str, Any] = {}


def _ticker_map() -> dict[str, Any]:
    global _TICKERS
    if _TICKERS:
        return _TICKERS
    res = fetch("https://www.sec.gov/files/company_tickers.json", user_agent=SEC_UA)
    data, _ = json_or_error(res)
    if data:
        _TICKERS = data
    return _TICKERS


def _resolve_cik(company: str) -> tuple[str | None, dict[str, Any] | None]:
    """Resolve a ticker or company-name fragment to a zero-padded CIK."""
    data = _ticker_map()
    q = company.strip().lower()
    rows = list(data.values()) if isinstance(data, dict) else []
    for r in rows:  # exact ticker
        if str(r.get("ticker", "")).lower() == q:
            return _pad_cik(r["cik_str"]), r
    for r in rows:  # exact title
        if str(r.get("title", "")).lower() == q:
            return _pad_cik(r["cik_str"]), r
    for r in rows:  # substring
        if q in str(r.get("title", "")).lower():
            return _pad_cik(r["cik_str"]), r
    return None, None


# ---------------------------------------------------------------- US: EDGAR

EDGAR_FTS = "https://efts.sec.gov/LATEST/search-index"


@mcp.tool()
def filings_edgar_search(
    query: str,
    forms: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """SEC EDGAR full-text search across all US filings (2001+ for most forms).

    query: full-text terms, e.g. '"material weakness"', 'going concern'.
    forms: comma-separated form filter, e.g. '8-K', '10-K,10-Q'.
    date_from/date_to: ISO dates YYYY-MM-DD.
    Returns matching filings with direct EDGAR document URLs.
    """
    params: dict[str, str] = {"q": query, "forms": forms or ""}
    if date_from or date_to:
        params.update(
            dateRange="custom",
            startdt=date_from or "2001-01-01",
            enddt=date_to or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        )
    url = f"{EDGAR_FTS}?" + urllib.parse.urlencode({k: v for k, v in params.items() if v})
    res = fetch(url, user_agent=SEC_UA)
    data, err = json_or_error(res)
    if err:
        return err

    hits = (data or {}).get("hits", {})
    rows = []
    for h in hits.get("hits", [])[: max(1, min(limit, 50))]:
        src = h.get("_source", {})
        acc, _, fname = str(h.get("_id", "")).partition(":")
        cik = (src.get("ciks") or ["0"])[0]
        rows.append({
            "form": src.get("form") or src.get("file_type"),
            "filed": src.get("file_date"),
            "period_ending": src.get("period_ending"),
            "company": (src.get("display_names") or [""])[0],
            "cik": cik,
            "accession": src.get("adsh") or acc,
            "items": src.get("items") or [],
            "document_url": (
                f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
                f"{str(src.get('adsh') or acc).replace('-', '')}/{fname}"
            ) if cik and fname else None,
        })
    total = hits.get("total", {})
    return {
        "query": query,
        "forms": forms,
        "total_matches": total.get("value") if isinstance(total, dict) else total,
        "returned": len(rows),
        "results": rows,
        "provenance": res.provenance(),
    }


@mcp.tool()
def filings_edgar_resolve(company: str) -> dict[str, Any]:
    """Resolve a US ticker or company name to its SEC CIK + registrant title.

    company: exact ticker ('AAPL'), or a name fragment ('apple').
    Use the returned cik with filings_edgar_company_filings / _financials.
    """
    cik, row = _resolve_cik(company)
    res = fetch("https://www.sec.gov/files/company_tickers.json", user_agent=SEC_UA)
    if cik is None:
        return {
            "query": company,
            "resolved": False,
            "error": "no_sec_registrant_match",
            "note": "Name matching is over SEC registrant titles only (case-insensitive substring).",
            "provenance": res.provenance(),
        }
    return {
        "query": company,
        "resolved": True,
        "cik": cik,
        "cik_int": int(cik),
        "ticker": row.get("ticker"),
        "title": row.get("title"),
        "submissions_url": f"https://data.sec.gov/submissions/CIK{cik}.json",
        "provenance": res.provenance(),
    }


@mcp.tool()
def filings_edgar_company_filings(
    company: str,
    forms: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Recent US filings for one registrant (accepts ticker OR 10-digit CIK).

    forms: comma-separated filter, e.g. '10-K,10-Q,8-K'. None = all forms.
    Returns filing index (form, filed, period, accession, document_url) plus
    registrant metadata (SIC, fiscal year end, addresses count).
    """
    if re.fullmatch(r"\d{1,10}", company.strip()):
        cik = _pad_cik(company)
        meta = None
    else:
        cik, meta = _resolve_cik(company)
        if cik is None:
            return {
                "query": company,
                "error": "no_sec_registrant_match",
                "note": "Pass a ticker, a name fragment, or a raw CIK.",
            }

    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    res = fetch(url, user_agent=SEC_UA)
    data, err = json_or_error(res)
    if err:
        return err

    recent = (data or {}).get("filings", {}).get("recent", {})
    want = {f.strip().upper() for f in forms.split(",")} if forms else None
    rows = []
    for i in range(len(recent.get("form", []))):
        form = recent["form"][i]
        if want and form.upper() not in want:
            continue
        acc = recent["accessionNumber"][i]
        doc = recent["primaryDocument"][i]
        rows.append({
            "form": form,
            "filed": recent["filingDate"][i],
            "period": recent["reportDate"][i],
            "accession": acc,
            "description": recent["primaryDocDescription"][i],
            "document_url": f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}",
        })
        if len(rows) >= max(1, min(limit, 200)):
            break

    return {
        "company": (data or {}).get("name"),
        "cik": cik,
        "ticker": (meta or {}).get("ticker"),
        "sic": (data or {}).get("sic"),
        "sic_description": (data or {}).get("sicDescription"),
        "fiscal_year_end": (data or {}).get("fiscalYearEnd"),
        "state_of_incorporation": (data or {}).get("stateOfIncorporation"),
        "forms_filter": forms,
        "returned": len(rows),
        "filings": rows,
        "provenance": res.provenance(),
    }


KEY_XBRL_TAGS = [
    "Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
    "NetIncomeLoss", "Assets", "Liabilities", "StockholdersEquity",
    "CashAndCashEquivalentsAtCarryingValue", "OperatingIncomeLoss",
    "EarningsPerShareDiluted", "ResearchAndDevelopmentExpense",
]


@mcp.tool()
def filings_edgar_financials(
    company: str,
    tags: str | None = None,
    periods: int = 4,
) -> dict[str, Any]:
    """Structured US XBRL financial facts for one registrant (ticker or CIK).

    tags: comma-separated XBRL/us-gaap tags; defaults to a key-metrics set.
    periods: number of most recent reported values per tag.
    Returns, per tag, the recent values with form, FY/FP, frame, and period.
    """
    if re.fullmatch(r"\d{1,10}", company.strip()):
        cik = _pad_cik(company)
    else:
        cik, _ = _resolve_cik(company)
        if cik is None:
            return {"query": company, "error": "no_sec_registrant_match"}

    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    res = fetch(url, user_agent=SEC_UA, max_bytes=25_000_000)
    data, err = json_or_error(res)
    if err:
        return err

    facts = (data or {}).get("facts", {})
    gaap = facts.get("us-gaap", {}) or {}
    dei = facts.get("dei", {}) or {}
    want = [t.strip() for t in tags.split(",")] if tags else KEY_XBRL_TAGS

    out: dict[str, Any] = {}
    for tag in want:
        node = gaap.get(tag) or dei.get(tag)
        if not node:
            out[tag] = {"found": False}
            continue
        picked: list[dict[str, Any]] = []
        for unit, arr in (node.get("units") or {}).items():
            for item in sorted(arr, key=lambda x: (x.get("end") or "", x.get("filed") or ""), reverse=True):
                if item.get("form") in ("10-K", "10-Q", "20-F", "40-F", "8-K", "6-K"):
                    picked.append({
                        "unit": unit,
                        "value": item.get("val"),
                        "end": item.get("end"),
                        "fy": item.get("fy"),
                        "fp": item.get("fp"),
                        "form": item.get("form"),
                        "filed": item.get("filed"),
                    })
                if len(picked) >= max(1, min(periods, 12)):
                    break
            if picked:
                break
        out[tag] = {"found": True, "label": node.get("label"), "values": picked}

    return {
        "entity": (data or {}).get("entityName"),
        "cik": (data or {}).get("cik"),
        "taxonomies_available": sorted(facts.keys()),
        "tag_count": {"us-gaap": len(gaap), "dei": len(dei)},
        "facts": out,
        "provenance": res.provenance(),
    }


@mcp.tool()
def filings_edgar_document(url: str, max_chars: int = 12000) -> dict[str, Any]:
    """Fetch and text-extract one SEC filing document (HTM/TXT) by URL.

    url: a document_url returned by filings_edgar_search / _company_filings
         (must be on sec.gov).
    Returns extracted plain text plus sha256 of the raw bytes.
    """
    if "sec.gov" not in urllib.parse.urlparse(url).netloc:
        return {"error": "url_not_on_sec_gov", "url": url}
    res = fetch(url, user_agent=SEC_UA, max_bytes=6_000_000)
    if res.status != 200:
        return {
            "error": "upstream_non_200",
            "http_status": res.status,
            "response_excerpt": res.body.decode("utf-8", "replace")[:400],
            "provenance": res.provenance(),
        }
    raw = res.body.decode("utf-8", "replace")
    text = _strip_html(raw) if ("<" in raw[:2000]) else raw
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return {
        "url": url,
        "document_bytes": len(res.body),
        "extracted_chars": len(text),
        "truncated": len(text) > max_chars,
        "text": text[:max_chars],
        "provenance": res.provenance(),
    }


# ---------------------------------------------------------------- MY: BNM

BNM_ACCEPT = "application/vnd.BNM.API.v1+json"
BNM_INDICATORS = {
    "opr": "Overnight Policy Rate (current level + last change)",
    "base-rate": "Base Rates + Base Lending Rates by licensed bank",
    "exchange-rate": "MYR exchange rates (USD/SGD/GBP/EUR/JPY/CNY/CHF/...). Base currency MYR",
    "interest-rate": "Interbank money-market interest rates (overnight, 1w, 1m, 3m, 6m, 12m)",
}


@mcp.tool()
def filings_bnm_rates(indicator: str = "opr") -> dict[str, Any]:
    """Bank Negara Malaysia regulatory/monetary data via the official BNM Open API.

    indicator: one of 'opr', 'base-rate', 'exchange-rate', 'interest-rate'.
    This is the Malaysian regulatory lane (monetary policy + licensed-bank
    rates). Requires the BNM vendor media type; handled internally.
    """
    key = (indicator or "opr").strip().lower().replace("_", "-")
    if key not in BNM_INDICATORS:
        return {
            "error": "unknown_indicator",
            "indicator": indicator,
            "valid": sorted(BNM_INDICATORS),
        }
    url = f"https://api.bnm.gov.my/public/{key}"
    res = fetch(url, accept=BNM_ACCEPT, max_bytes=4_000_000)
    data, err = json_or_error(res)
    if err:
        err["indicator"] = key
        err["accept_header"] = BNM_ACCEPT
        return err
    data = data or {}
    payload = data.get("data") if isinstance(data, dict) else data
    if isinstance(payload, list) and key in ("base-rate", "interest-rate"):
        payload = payload[:60]
    return {
        "indicator": key,
        "meaning": BNM_INDICATORS[key],
        "meta": (data or {}).get("meta") if isinstance(data, dict) else None,
        "data": payload,
        "provenance": res.provenance(),
    }

# ---------------------------------------------------------------- MY: open data

@mcp.tool()
def filings_my_dataset(dataset_id: str, limit: int = 20, filters: str | None = None) -> dict[str, Any]:
    """Query an official Malaysian open-data catalogue on data.gov.my.

    dataset_id: catalogue id, e.g. 'fuelprice', 'population_malaysia'.
    filters: optional raw querystring passthrough, e.g. 'date_start=2024-01-01'.
    Returns rows + provenance. A 404 body from data.gov.my (unknown catalogue)
    is surfaced verbatim rather than masked.
    """
    params = {"id": dataset_id, "limit": str(max(1, min(limit, 300)))}
    url = "https://api.data.gov.my/data-catalogue?" + urllib.parse.urlencode(params)
    if filters:
        url += "&" + filters.lstrip("&?")
    res = fetch(url, max_bytes=4_000_000)
    data, err = json_or_error(res)
    if err:
        err["dataset_id"] = dataset_id
        err["hint"] = "Catalogue ids are exact; data.gov.my returns 404 JSON for unknown ids."
        return err
    rows = data if isinstance(data, list) else [data]
    return {
        "dataset_id": dataset_id,
        "returned": len(rows),
        "rows": rows[: max(1, min(limit, 300))],
        "provenance": res.provenance(),
    }


# ---------------------------------------------------------------- health

SOURCE_LANES: list[dict[str, Any]] = [
    {"lane": "US / SEC EDGAR full-text search", "url": "https://efts.sec.gov/LATEST/search-index?q=%22going+concern%22&forms=8-K"},
    {"lane": "US / SEC EDGAR submissions (AAPL)", "url": "https://data.sec.gov/submissions/CIK0000320193.json"},
    {"lane": "US / SEC XBRL company facts (AAPL)", "url": "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json"},
    {"lane": "US / SEC ticker->CIK map", "url": "https://www.sec.gov/files/company_tickers.json"},
    {"lane": "MY / BNM Open API base-rate", "url": "https://api.bnm.gov.my/public/base-rate", "accept": BNM_ACCEPT},
    {"lane": "MY / BNM Open API opr", "url": "https://api.bnm.gov.my/public/opr", "accept": BNM_ACCEPT},
    {"lane": "MY / data.gov.my catalogue (fuelprice)", "url": "https://api.data.gov.my/data-catalogue?id=fuelprice&limit=1"},
    {"lane": "MY / Bursa Malaysia announcements API", "url": "https://www.bursamalaysia.com/api/v1/announcements/announcements?ann_type=company&per_page=1&page=1"},
]


@mcp.tool()
def filings_source_health() -> dict[str, Any]:
    """Live reachability probe of every upstream lane this server depends on.

    Reports HTTP status + response excerpt per lane. Bursa Malaysia's
    announcement API sits behind a Cloudflare JS challenge (HTTP 403) and is
    NOT bypassed — this tool is the honest witness for that gap. Use it before
    trusting any lane, and to explain a tool returning upstream_non_200.
    """
    lanes = []
    for spec in SOURCE_LANES:
        res = fetch(spec["url"], accept=spec.get("accept"), max_bytes=300_000, timeout=20)
        excerpt = res.body.decode("utf-8", "replace")[:180].replace("\n", " ")
        lanes.append({
            "lane": spec["lane"],
            "http_status": res.status,
            "ok": res.status == 200,
            "cached": res.cached,
            "sha256": res.sha256,
            "fetched_at_utc": res.fetched_at_utc,
            "url": spec["url"],
            "excerpt": excerpt,
        })
    return {
        "lanes": lanes,
        "reachable": sum(1 for l in lanes if l["ok"]),
        "total": len(lanes),
        "blocked_lanes": [l["lane"] for l in lanes if not l["ok"]],
        "cache_dir": str(CACHE_DIR),
        "provenance": {
            "source_url": "multi-lane probe",
            "fetched_at_utc": _now_utc(),
            "sha256": None,
            "http_status": 200,
            "cached": False,
        },
    }


if __name__ == "__main__":
    mcp.run(transport="http", host=HOST, port=PORT)
