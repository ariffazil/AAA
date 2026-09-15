#!/usr/bin/env python3
"""filings-mcp smoke test — real MCP streamable-http client, real tool calls.

Asserts live data + provenance on at least 5 tools. Exits 0 on pass, 1 on fail.
Run via ./smoke_test.sh (starts the server, runs this, stops the server).
"""
from __future__ import annotations

import asyncio
import json
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = "http://127.0.0.1:18410/mcp"

FAILURES: list[str] = []
REPORT: dict = {"tools": [], "checks": []}


def check(name: str, ok: bool, detail=None) -> None:
    REPORT["checks"].append({"check": name, "ok": bool(ok), "detail": detail})
    if not ok:
        FAILURES.append(f"{name}: {detail}")
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + ("" if ok else f"  -> {detail}"))


def has_provenance(d: dict) -> bool:
    p = d.get("provenance") or {}
    return all(k in p for k in ("source_url", "fetched_at_utc", "sha256", "http_status"))


async def main() -> int:
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as s:
            await s.initialize()

            tools = await s.list_tools()
            names = sorted(t.name for t in tools.tools)
            REPORT["tools"] = names
            print(f"TOOLS REGISTERED ({len(names)}): {', '.join(names)}\n")
            check("tool_count>=8", len(names) >= 8, names)
            check("all tools prefixed filings_", all(n.startswith("filings_") for n in names), names)

            # ---- 1. US: EDGAR full-text search
            r = await s.call_tool("filings_edgar_search",
                                  {"query": '"material weakness"', "forms": "10-K", "limit": 3})
            d = json.loads(r.content[0].text)
            REPORT["edgar_search"] = {k: d.get(k) for k in ("total_matches", "returned")}
            REPORT["edgar_search_sample"] = (d.get("results") or [{}])[0]
            check("edgar_search http 200", d.get("provenance", {}).get("http_status") == 200, d.get("provenance"))
            check("edgar_search has hits", (d.get("returned") or 0) > 0, d.get("returned"))
            check("edgar_search provenance", has_provenance(d), d.get("provenance"))
            check("edgar_search doc url", bool((d.get("results") or [{}])[0].get("document_url")))

            # ---- 2. US: filing index for one registrant
            r = await s.call_tool("filings_edgar_company_filings",
                                  {"company": "AAPL", "forms": "10-K,10-Q", "limit": 3})
            d = json.loads(r.content[0].text)
            REPORT["aapl"] = {"company": d.get("company"), "cik": d.get("cik"),
                              "sic_description": d.get("sic_description"), "returned": d.get("returned"),
                              "first": (d.get("filings") or [{}])[0]}
            check("apple resolved", d.get("cik") == "0000320193", d.get("cik"))
            check("apple filings present", (d.get("returned") or 0) > 0, d.get("returned"))
            check("apple provenance", has_provenance(d))

            # ---- 3. US: XBRL financials
            r = await s.call_tool("filings_edgar_financials",
                                  {"company": "AAPL", "tags": "Revenues,NetIncomeLoss", "periods": 2})
            d = json.loads(r.content[0].text)
            rev = (d.get("facts") or {}).get("Revenues", {})
            REPORT["xbrl"] = {"entity": d.get("entity"), "revenues": rev.get("values", [])[:2]}
            check("xbrl entity", d.get("entity") == "Apple Inc.", d.get("entity"))
            check("xbrl revenues found", rev.get("found") is True)
            check("xbrl provenance", has_provenance(d))

            # ---- 4. MY: BNM regulatory data
            r = await s.call_tool("filings_bnm_rates", {"indicator": "opr"})
            d = json.loads(r.content[0].text)
            REPORT["bnm_opr"] = d.get("data")
            check("bnm opr http 200", d.get("provenance", {}).get("http_status") == 200, d.get("provenance"))
            check("bnm opr has level", isinstance(d.get("data"), dict) and "new_opr_level" in d["data"], d.get("data"))
            check("bnm opr provenance", has_provenance(d))

            r = await s.call_tool("filings_bnm_rates", {"indicator": "exchange-rate"})
            d2 = json.loads(r.content[0].text)
            REPORT["bnm_fx"] = {"n": len(d2.get("data") or []), "usd": next(
                (x for x in (d2.get("data") or []) if x.get("currency_code") == "USD"), None)}
            check("bnm fx http 200", d2.get("provenance", {}).get("http_status") == 200)
            check("bnm fx has USD", REPORT["bnm_fx"]["usd"] is not None)

            # ---- 5. MY: data.gov.my official catalogue
            r = await s.call_tool("filings_my_dataset", {"dataset_id": "fuelprice", "limit": 2})
            d = json.loads(r.content[0].text)
            REPORT["my_dataset"] = {"dataset_id": d.get("dataset_id"), "rows": d.get("rows")}
            check("my dataset http 200", d.get("provenance", {}).get("http_status") == 200, d.get("provenance"))
            check("my dataset rows", (d.get("returned") or 0) > 0, d.get("returned"))

            # ---- 6. live lane health (the honest witness)
            r = await s.call_tool("filings_source_health", {})
            d = json.loads(r.content[0].text)
            REPORT["health"] = {"reachable": d.get("reachable"), "total": d.get("total"),
                                "blocked_lanes": d.get("blocked_lanes"),
                                "lanes": [{"lane": l["lane"][:46], "status": l["http_status"]} for l in d["lanes"]]}
            check("6+ lanes reachable", (d.get("reachable") or 0) >= 6, REPORT["health"])
            check("bursa block reported honestly",
                  any("Bursa" in b for b in (d.get("blocked_lanes") or [])), d.get("blocked_lanes"))

            # ---- 7. document fetch + hash
            url = (REPORT.get("edgar_search_sample") or {}).get("document_url")
            if url:
                r = await s.call_tool("filings_edgar_document", {"url": url, "max_chars": 400})
                d = json.loads(r.content[0].text)
                REPORT["doc"] = {"url": url, "bytes": d.get("document_bytes"),
                                 "chars": d.get("extracted_chars"), "sha256": (d.get("provenance") or {}).get("sha256")}
                check("doc fetched", d.get("document_bytes", 0) > 0, REPORT["doc"])
                check("doc sha256 present", len((d.get("provenance") or {}).get("sha256") or "") == 64)

    print("\n--- SMOKE TEST SUMMARY ---")
    print(json.dumps(REPORT, indent=1)[:2600])
    print(f"\nchecks: {len(REPORT['checks'])}  failures: {len(FAILURES)}")
    if FAILURES:
        print("FAILED:", *FAILURES, sep="\n  ")
        return 1
    print("SMOKE TEST: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
