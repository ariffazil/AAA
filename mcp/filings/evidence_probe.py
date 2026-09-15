import asyncio, json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def c(s, name, args):
    r = await s.call_tool(name, args)
    return json.loads(r.content[0].text)

async def main():
    async with streamablehttp_client("http://127.0.0.1:18410/mcp") as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            d = await c(s, "filings_source_health", {})
            print("### SOURCE HEALTH:", d["reachable"], "/", d["total"], "reachable")
            for l in d["lanes"]:
                print(f'  {l["http_status"]:>3}  {l["lane"][:44]:<44} cached={l["cached"]}  {l["excerpt"][:70]!r}')
            d = await c(s, "filings_edgar_search", {"query": '"material weakness"', "forms": "10-K", "limit": 2})
            print(f'\n### EDGAR FTS total={d["total_matches"]} http={d["provenance"]["http_status"]} sha={d["provenance"]["sha256"][:16]}')
            print("   ", json.dumps(d["results"][0])[:400])
            d = await c(s, "filings_edgar_company_filings", {"company": "AAPL", "forms": "10-K,10-Q", "limit": 2})
            print(f'\n### AAPL cik={d["cik"]} name={d["company"]} sic={d["sic_description"]} http={d["provenance"]["http_status"]}')
            for f in d["filings"]:
                print("   ", f["form"], f["filed"], f["period"], f["document_url"][:95])
            d = await c(s, "filings_edgar_financials", {"company": "AAPL", "tags": "Revenues,NetIncomeLoss", "periods": 2})
            print(f'\n### XBRL entity={d["entity"]} http={d["provenance"]["http_status"]}')
            for t, v in d["facts"].items():
                print("   ", t, [(x["value"], x["end"], x["form"]) for x in v.get("values", [])])
            d = await c(s, "filings_bnm_rates", {"indicator": "opr"})
            print(f'\n### BNM OPR {json.dumps(d["data"])} http={d["provenance"]["http_status"]} sha={d["provenance"]["sha256"][:16]}')
            d = await c(s, "filings_bnm_rates", {"indicator": "exchange-rate"})
            usd = [x for x in d["data"] if x["currency_code"] == "USD"][0]
            print(f'### BNM FX n={len(d["data"])} USD={json.dumps(usd)}')
            d = await c(s, "filings_my_dataset", {"dataset_id": "fuelprice", "limit": 1})
            print(f'\n### data.gov.my fuelprice http={d["provenance"]["http_status"]} sha={d["provenance"]["sha256"][:16]} rows={json.dumps(d["rows"])[:200]}')
            d = await c(s, "filings_my_dataset", {"dataset_id": "ssm_company", "limit": 1})
            print("### unknown-catalogue honesty:", json.dumps({k: d[k] for k in ("error", "http_status", "response_excerpt") if k in d})[:220])
            d = await c(s, "filings_edgar_search", {"query": '"material weakness"', "forms": "10-K", "limit": 2})
            print(f'\n### CACHE PROOF (same query twice): cached={d["provenance"]["cached"]} sha_matches={d["provenance"]["sha256"][:16]}')

asyncio.run(main())
