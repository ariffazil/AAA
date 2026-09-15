"""Real MCP client smoke test for doc-tables-mcp over streamable-http.

Calls EVERY registered tool through an actual MCP ClientSession and prints observed
output. This is the deliverable proof, not a direct function call.
"""
import asyncio
import json
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = "http://127.0.0.1:38500/mcp"


def show(title, payload, limit=1800):
    print("=" * 78)
    print("###", title)
    txt = json.dumps(payload, indent=2, default=str)
    print(txt[:limit] + ("\n... [truncated]" if len(txt) > limit else ""))


async def call(session, name, args):
    res = await session.call_tool(name, args)
    print("=" * 78)
    print(f"### TOOL CALL: {name}({json.dumps(args)[:220]})")
    if getattr(res, "isError", False):
        print("!! MCP ERROR:", res.content)
        return None
    # prefer structuredContent when FastMCP provides it, else parse the text block
    sc = getattr(res, "structuredContent", None)
    if sc:
        return sc
    for blk in res.content:
        if getattr(blk, "type", None) == "text":
            try:
                return json.loads(blk.text)
            except Exception:
                return {"_raw": blk.text[:2000]}
    return None


async def main():
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            info = await session.initialize()
            print("server:", info.serverInfo.name, info.serverInfo.version,
                  "| protocol:", info.protocolVersion)
            tools = await session.list_tools()
            names = [t.name for t in tools.tools]
            print("tools advertised:", names)
            assert set(names) == {
                "doc_tables_health", "doc_tables_list", "doc_tables_extract",
                "doc_tables_reconcile", "doc_tables_text_mangle_check",
            }, f"unexpected tool set: {names}"

            # 1. health
            h = await call(session, "doc_tables_health", {})
            show("doc_tables_health", h, 1200)

            # 2. list — slotting table page
            l = await call(session, "doc_tables_list", {"source": "/tmp/cafib.pdf", "page": 397})
            show("doc_tables_list (cafib p397)", l, 1500)

            # 3. extract — the canonical supervisory slotting risk weights
            e = await call(session, "doc_tables_extract",
                           {"source": "/tmp/cafib.pdf", "page": 397, "min_rows": 2, "min_cols": 2})
            t0 = e["tables"][0]
            print("PROOF — table_count:", e["table_count"], "| best table shape:", t0["shape"],
                  "| strategy:", t0["strategy"], "| page:", t0["page"], "| bbox:", t0["bbox"])
            print("PROOF — caption:", t0["caption"])
            print("PROOF — markdown:\n" + t0["markdown"])
            print("PROOF — cells:", json.dumps(t0["cells"]))

            # 3b. extract from the second fixture — the musyarakah/mudarabah capital
            #     treatment table (Nov 2024 CAF Standardised Approach, p36)
            e2 = await call(session, "doc_tables_extract",
                            {"source": "/tmp/sa2024.pdf", "page": 36,
                             "min_rows": 2, "min_cols": 2})
            print("PROOF sa2024 tables:", e2["table_count"])
            for t in e2["tables"][:2]:
                print(f"  p{t['page']} {t['shape']} {t['strategy']} caption={t['caption']}")
                print("  " + t["markdown"].replace("\n", "\n  ")[:700])

            # 4. reconcile — printed total vs derived total (the anti-fabrication gate)
            rec = await call(session, "doc_tables_reconcile",
                             {"source": "/tmp/cafib.pdf", "page": 425, "table_index": 0})
            show("doc_tables_reconcile (cafib p425 worked example)", rec, 4000)

            # 4b. reconcile an HTML table
            rec_h = await call(session, "doc_tables_reconcile", {"source": "/tmp/t.html"})
            show("doc_tables_reconcile (/tmp/t.html)", rec_h, 1500)

            # 4c. negative control: reconcile the slotting table (no printed total present)
            rec_n = await call(session, "doc_tables_reconcile",
                               {"source": "/tmp/cafib.pdf", "page": 397})
            show("doc_tables_reconcile negative control (cafib p397, no total)", rec_n, 900)

            # 5. the failure-mode witness
            m = await call(session, "doc_tables_text_mangle_check",
                           {"source": "/tmp/cafib.pdf", "page": 425})
            show("doc_tables_text_mangle_check (cafib p425)", m, 1800)

            print("=" * 78)
            print("SMOKE TEST COMPLETE — all 5 tools called through MCP client.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        print("SMOKE TEST FAILED:", type(exc).__name__, exc)
        sys.exit(1)
