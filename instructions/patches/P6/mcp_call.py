"""Issue a JSON-RPC call to hermes_contradiction_scan via MCP/HTTP at :18420."""
import json, urllib.request, sys

PAYLOAD = {
    "jsonrpc": "2.0", "id": "p6-fixture-1", "method": "tools/call",
    "params": {
        "name": "hermes_contradiction_scan",
        "arguments": {"claims": [
            {"id": "C1", "text": "Federal spending 2027 totals RM510 billion including statutory and PPP investment",
             "source": "mof.gov.my/belanjawan2027", "principal": "federal_budget_total",
             "geography": "MY", "kind": "REPORTED"},
            {"id": "C2", "text": "Federal operating spending 2027 totals RM459.8 billion",
             "source": "Reuters world/asia-pacific 2026-10-09", "principal": "federal_budget_total",
             "geography": "MY", "kind": "REPORTED"},
            {"id": "C3", "text": "PETRONAS dividend to federal government 2027 will be RM32 billion",
             "source": "mof fiscal outlook 2027", "principal": "petronas_dividend",
             "geography": "MY", "kind": "FORECAST"},
            {"id": "C4", "text": "Petronas dividend to federal government 2027 estimated around RM25 billion",
             "source": "CIMB research The Edge 2026-10-07", "principal": "petronas_dividend",
             "geography": "MY", "kind": "FORECAST"},
            {"id": "C5", "text": "2027 deficit target is 3.3 percent of GDP",
             "source": "mof budget speech 2027", "principal": "deficit_pct_gdp",
             "geography": "MY", "kind": "FORECAST"},
            {"id": "C6", "text": "Deficit could remain at 3.6 percent of GDP in 2027",
             "source": "OCBC research Business Today 2026-09-25", "principal": "deficit_pct_gdp",
             "geography": "MY", "kind": "FORECAST"},
            {"id": "C7", "text": "Government subsidies, aid and incentives for 2027 exceed RM80 billion including fuel subsidy about RM40 billion",
             "source": "mof budget speech 2027", "principal": "subsidy_total",
             "geography": "MY", "kind": "REPORTED"},
            {"id": "C8", "text": "Subsidy spend falls marginally to RM72.7 billion in 2027",
             "source": "Reuters world/asia-pacific 2026-10-09", "principal": "subsidy_total",
             "geography": "MY", "kind": "REPORTED"},
            {"id": "C9", "text": "Brent crude traded at about USD85 per barrel as the 2026 average assumption",
             "source": "mof fiscal outlook 2027", "principal": "oil_assumption",
             "geography": "MY", "kind": "FORECAST"},
            {"id": "C10", "text": "Brent crude spot price USD101 per barrel reported on 11 September",
             "source": "The Star 2026-09-11", "principal": "oil_spot_observation",
             "geography": "MY", "kind": "REPORTED"},
            {"id": "C11", "text": "Federal deficit 1H 2026 about 4.2 percent and well below targeted 3.5 percent",
             "source": "The Star column via Webull 2026-09-27", "principal": "deficit_pct_gdp",
             "geography": "MY", "kind": "REPORTED"},
        ]}
    }
}

data = json.dumps(PAYLOAD).encode("utf-8")
req = urllib.request.Request("http://127.0.0.1:18420", data=data,
                              headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=8) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        print("HTTP", resp.status)
        try:
            j = json.loads(body)
            # unwrap typical MCP content wrappers
            content = j.get("result", j)
            if isinstance(content, dict) and "content" in content:
                c0 = content["content"][0]
                if isinstance(c0, dict) and c0.get("type") == "text":
                    inner = json.loads(c0["text"])
                    print("ok:", inner.get("ok"))
                    print("count:", len(inner.get("contradictions", [])))
                    classes = {}
                    for r in inner.get("contradictions", []):
                        classes[r["class"]] = classes.get(r["class"], 0) + 1
                    print("classes:", json.dumps(classes))
                else:
                    print(json.dumps(content)[:600])
            else:
                print(json.dumps(content)[:600])
        except Exception as e:
            print("PARSE-FAIL", e)
            print(body[:1000])
except Exception as e:
    print(f"HTTP-FAIL: {e}")
    sys.exit(1)
