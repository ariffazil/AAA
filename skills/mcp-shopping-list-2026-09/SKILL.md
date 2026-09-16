---
name: mcp-shopping-list-2026-09
description: Canonical 2026-09 MCP/tool acquisition research for the federation — TOP 12 ranked installs, context-bloat counter-thesis, staged install commands. Use when "install MCP", "add tool server", "mcp bloat", "which MCP server", "serena", "graphiti", "mcp-compressor", "postgres pro".
---

# MCP / Agent-Tool SOTA Shopping List — 2026-09 (canonical pointer)

**Full report:** `/root/reports/MCP-SOTA-SHOPPING-LIST-2026-09.md` (34KB, sourced 2026-09-16)
**Companion YouTube lanes research:** `/root/youtube-extraction-lanes-2026.md`

## The counter-thesis (hold this before installing anything)

1. **MCP servers are a context tax at session start** — 15+ servers = 30-40% of session window gone before first token. `aforge` (130 tools) is our largest line item.
2. **Skills+CLI beat MCP 17-32x on cost** where a good local CLI exists. Only install MCPs whose value is *state or data a shell cannot reach* (graph memory, cloud browsers, SaaS APIs, traces).

## TOP 12 (ranked) — install status

| # | Tool | Verdict for us | Status 2026-09-16 |
|---|------|----------------|-------------------|
| 1 | **Graphiti MCP** (bi-temporal memory, FalkorDB local) | Correct add — fills temporal invalidation gap | FalkorDB UP; graphiti service NOT installed; opencode config staged `enabled:false` @ :8000. Install: clone getzep/graphiti → `cd mcp_server && uv sync` → stdio + `OPENAI_BASE_URL=http://127.0.0.1:4000/v1` |
| 2 | **mcp-compressor** (Atlassian, wraps any server, 70-97% schema-token cut) | Highest ROI — target `aforge` 130 tools | NOT installed. `mcp-compressor -c medium -- <server cmd>`; requires deliberate cutover of aforge surface |
| 3 | **Serena** (symbol-level LSP, 60+ langs) | Already configured | `/root/.claude/mcp-launchers/serena.sh` in opencode config — verify enabled per harness |
| 4 | **Steel Browser** (self-hosted browser profiles) | Sovereign browser lane | NOT installed — needs docker run + npx (T2) |
| 5 | **DeepWiki MCP** (`mcp.deepwiki.com/mcp`) | Free, no key, instant public-repo architecture comprehension | Wire = one remote HTTP entry |
| 6 | **Langfuse MCP** (native; read own traces) | We run Langfuse | Wire with Basic auth header to local instance |
| 7 | **Postgres MCP Pro** (crystaldba) | Strict upgrade over thin postgres server | `docker run crystaldba/postgres-mcp --access-mode=restricted` |
| 8 | **DuckDB/MotherDuck MCP** | Zero-infra analytics over Parquet/CSV | `uvx mcp-server-motherduck` |
| 9 | **paper-search-mcp** | arXiv+PubMed+OpenAlex+…+PDF in one | `uvx paper-search-mcp` |
| 10 | **OpenBB MCP** | Institutional financial data | `pip install openbb-mcp-server` + data keys (T2/T3) |
| 11 | **computer-use-linux + mobile-mcp** | Real GUI + Android via ADB | ydotool setup required (T2) |
| 12 | **fal or ElevenLabs MCP** | Media generation / TTS production | Usage-based → T3 (paid) |

**NOT recommended:** Hyperbrowser (abandoned), Snowflake/ClickHouse/dbt (no infra), local-CLI wrappers (17-32x penalty), generic any-API MCPs, Telegram MCP (Hermes owns that surface).

## Install discipline

- Every MCP add = context tax for ALL agents on the harness → justify against the counter-thesis first.
- T2 announce before service installs; paid APIs → T3 (Arif).
- After add: `capability-index_capability_reindex` + update this table's Status column.

## Genuine gaps (build, don't buy — we are the only real capability)

Geoscience at scale (geox is unique) · OR/solvers · Linux desktop CUA · MY/ASEAN official data MCPs · agent regression testing · A2A-over-MCP.
