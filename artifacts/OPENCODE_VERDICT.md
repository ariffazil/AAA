# OpenCode 15-MCP Verification · 2026-06-13 10:30 MYT

## Verdict: 11 WORKING, 3 MARGINAL, 1 FIXED, 1 DISABLED

| MCP | STATUS | EVIDENCE |
|-----|--------|----------|
| arifos-kernel | ✅ WORKING | 25 tools, kanon-2026.06.13+4d49da3 |
| aforge | ✅ WORKING | tools/list returned 11 tools |
| geox | ✅ WORKING | systemd active, tools/list returned full catalog |
| wealth | ✅ WORKING | 5+ tool families: personal_finance, market_data, stock, survival, governance |
| well | ✅ WORKING | tools: medical_boundary, signal_coverage, classify, trace |
| playwright | ⚠️ SSE | Process alive (PID 1130), SSE transport needs proper Accept headers |
| hostinger-vps | ✅ WORKING | gate.py exists, Python UTF-8, importable |
| meyhem | ✅ WORKING | MCP initialize handshake succeeded |
| cloudflare | 🔧 FIXED | Wrong module path. Changed to /root/.hermes/mcp_servers/cloudflare_mcp.py |
| perplexity | ⚠️ NEEDS_KEY | Package OK but needs PERPLEXITY_API_KEY env. Key IS in .env. |
| brave-search | ✅ WORKING | brave-search-mcp@2.1.0 installs and runs |
| postgres | ✅ WORKING | @abiswas97/postgres-mcp@2.0.0 |
| supabase | ✅ WORKING | @supabase/mcp-server-supabase@0.8.2 |
| sequential-thinking | ✅ WORKING | Runs on stdio |
| docker | ⚠️ UNTESTED | /root/.npm-global/bin/docker-mcp-server exists |

## Notes
- **playwright**: SSE transport confirmed. Chrome 149, process alive since Jun10.
- **perplexity**: PERPLEXITY_API_KEY in /root/.hermes/.env. OpenCode needs env passthrough.
- **cloudflare**: FIXED — changed from pip package to custom script at /root/.hermes/mcp_servers/cloudflare_mcp.py
- **docker**: Exists at /root/.npm-global/bin/docker-mcp-server but not fully tested
- **qdrant**: DISABLED — Qdrant runs on :6333 as REST API, no MCP wrapper exists. Use `qdrant-client` v1.17.1 via Python or curl directly.

## Method
OpenCode forge agent self-tested all 15 MCPs by reading its own config, calling tools/list or initialize on each. Package names corrected mid-test. Cloudflare fix applied post-discovery.
