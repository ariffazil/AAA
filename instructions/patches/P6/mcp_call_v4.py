import json, urllib.request, sys
URL = "http://127.0.0.1:18420/mcp"
SID = "edacd8b294794128828a0c0f53849345"  # from prior probe
def post(payload, extra_headers=None, timeout=8):
    h = {"Content-Type":"application/json","Accept":"application/json, text/event-stream",
         "MCP-Protocol-Version":"2025-06-18"}
    if extra_headers: h.update(extra_headers)
    data = json.dumps(payload).encode()
    req = urllib.request.Request(URL, data=data, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read().decode("utf-8","replace")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode("utf-8","replace")

sess_hdr = {"Mcp-Session-Id": SID}

# tools/list — confirm the new tool is exposed.
s, h, b = post({"jsonrpc":"2.0","id":"list-1","method":"tools/list","params":{}},
                sess_hdr)
print("LIST HTTP", s)
# SSE body — extract data: lines.
data_lines = [l[len("data:"):].strip() for l in b.splitlines() if l.startswith("data:")]
for dl in data_lines:
    try:
        j = json.loads(dl)
        names = [t["name"] for t in j.get("result",{}).get("tools",[])]
        print("tools:", names)
    except Exception:
        pass

# tool call — hermes_contradiction_scan.
PAYLOAD_CALL = {"jsonrpc":"2.0","id":"call-1","method":"tools/call",
    "params":{"name":"hermes_contradiction_scan",
              "arguments":{"claims":[
                  {"id":"C1","text":"Federal spending 2027 totals RM510 billion including statutory and PPP investment",
                   "source":"mof.gov.my/belanjawan2027","principal":"federal_budget_total","geography":"MY","kind":"REPORTED"},
                  {"id":"C2","text":"Federal operating spending 2027 totals RM459.8 billion",
                   "source":"Reuters world/asia-pacific 2026-10-09","principal":"federal_budget_total","geography":"MY","kind":"REPORTED"},
                  {"id":"C3","text":"PETRONAS dividend to federal government 2027 will be RM32 billion",
                   "source":"mof fiscal outlook 2027","principal":"petronas_dividend","geography":"MY","kind":"FORECAST"},
                  {"id":"C4","text":"Petronas dividend to federal government 2027 estimated around RM25 billion",
                   "source":"CIMB research The Edge 2026-10-07","principal":"petronas_dividend","geography":"MY","kind":"FORECAST"},
                  {"id":"C5","text":"2027 deficit target is 3.3 percent of GDP",
                   "source":"mof budget speech 2027","principal":"deficit_pct_gdp","geography":"MY","kind":"FORECAST"},
                  {"id":"C6","text":"Deficit could remain at 3.6 percent of GDP in 2027",
                   "source":"OCBC research Business Today 2026-09-25","principal":"deficit_pct_gdp","geography":"MY","kind":"FORECAST"},
                  {"id":"C7","text":"Government subsidies, aid and incentives for 2027 exceed RM80 billion including fuel subsidy about RM40 billion",
                   "source":"mof budget speech 2027","principal":"subsidy_total","geography":"MY","kind":"REPORTED"},
                  {"id":"C8","text":"Subsidy spend falls marginally to RM72.7 billion in 2027",
                   "source":"Reuters world/asia-pacific 2026-10-09","principal":"subsidy_total","geography":"MY","kind":"REPORTED"},
                  {"id":"C9","text":"Brent crude traded at about USD85 per barrel as the 2026 average assumption",
                   "source":"mof fiscal outlook 2027","principal":"oil_assumption","geography":"MY","kind":"FORECAST"},
                  {"id":"C10","text":"Brent crude spot price USD101 per barrel reported on 11 September",
                   "source":"The Star 2026-09-11","principal":"oil_spot_observation","geography":"MY","kind":"REPORTED"},
                  {"id":"C11","text":"Federal deficit 1H 2026 about 4.2 percent and well below targeted 3.5 percent",
                   "source":"The Star column via Webull 2026-09-27","principal":"deficit_pct_gdp","geography":"MY","kind":"REPORTED"},
              ]}}}

s, h, b = post(PAYLOAD_CALL, sess_hdr)
print("CALL HTTP", s)
# parse first data: line
import re
m = re.search(r"^data: (.+)$", b, re.M)
if m:
    j = json.loads(m.group(1))
    if "error" in j:
        print("JSON-RPC error:", json.dumps(j["error"], indent=2)[:1000])
        sys.exit(2)
    res = j.get("result",{})
    # MCP result content[0].text contains the JSON-stringified detector output.
    content = res.get("content",[])
    if content and isinstance(content[0], dict) and content[0].get("type") == "text":
        inner = json.loads(content[0]["text"])
        print("ok:", inner.get("ok"))
        rows = inner.get("contradictions", [])
        print("count:", len(rows))
        from collections import Counter
        print("classes:", json.dumps(Counter(r["class"] for r in rows)))
        print("subjects:", json.dumps(Counter(r["subject"] for r in rows)))
        # Side-effect check: write to canonical store
        print("output_size:", len(content[0]["text"]))
    else:
        print("UNEXPECTED RESULT SHAPE", json.dumps(res)[:1500])
else:
    print(b[:1500])
