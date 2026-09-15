---
name: mcp-sota-shopping-list
description: Reference for MCP server procurement decisions. Use when evaluating new MCP servers, comparing options, or planning capability expansion.
---

# MCP SOTA Shopping List — 2026-09

**Full report:** `/root/reports/MCP-SOTA-SHOPPING-LIST-2026-09.md` (34 KB, 244 lines)

## Critical Context: MCP Context Tax

Every installed MCP server's tool descriptions load at session start. With 15+ servers, **30–40% of the session window is consumed before any work starts**. Skills resolve to 30–50 tokens at rest; MCP schemas preload 10,000+.

**Rule:** Install MCPs for *state or data an agent cannot reach from a shell* (graph memory, cloud browsers, SaaS APIs). Do NOT install MCPs wrapping local CLIs (`git`, `docker`, `psql`, `gh`, `ffmpeg`).

## Top Recommendations (from full report)

### Memory / Context
| Tool | Why | Status |
|---|---|---|
| **Graphiti** | Bi-temporal KG, edges invalidated not deleted. FalkorDB already in stack. | Config exists at `deploy/graphiti-config.yaml` |
| **mcp-compressor** | 70–97% token reduction on tool descriptions. Wraps any existing server. | Not installed |
| **mem0** | Already the provider. Extraction + dedup + update-on-write. | LIVE |

### Browser / Web
| Tool | Why | Status |
|---|---|---|
| **Firecrawl v2** | Already installed. Scrape/crawl/map/agent. Audio lane for YouTube. | LIVE |
| **Playwright MCP** | Accessibility-tree snapshots, no vision model needed. | Not installed |
| **Steel.dev** | Only fully self-hostable browser infrastructure (Apache-2.0). | Not installed |

### Code / Dev
| Tool | Why | Status |
|---|---|---|
| **Serena** | LSP-native coding agent, MCP server, works with any LSP language server. | Not installed |
| **Desktop Commander** | File + terminal + browser control in one MCP. | Not installed |

### Search / Research
| Tool | Why | Status |
|---|---|---|
| **Brave Search** | Already installed. Free 2k/mo. | LIVE |
| **Exa** | Already installed. Semantic search. | LIVE |
| **Context7** | Library docs on demand. | LIVE |

## YouTube Extraction (datacenter IP)

**Full lanes:** `/root/youtube-extraction-lanes-2026.md` (18 lanes tested)
**Skill:** `youtube-extraction-datacenter-ip` (in shared AAA skills)

Top 3 lanes:
1. **Firecrawl API** — `formats:["markdown"]` (1 credit) / `["audio"]` (5 credits). Already keyed. ✅ FULL PASS
2. **SerpApi** — `youtube_video_transcript`, 250 free/mo. ✅ PASS
3. **Hybrid: yt-dlp browse/search → Firecrawl per-video** — near-zero cost. ✅ BOTH HALVES PASS

Root cause: IP-level player-endpoint flag, NOT a PO-token problem. No local tool fixes it.

## Google Workspace

**Full doc:** `/root/docs/google-ecosystem-wiring.md`
**Skill:** `forge-google-workspace` (shared AAA location)
**CLI:** `gws` v0.22.5 installed at `/usr/bin/gws`

Verified live: Drive, Gmail, Calendar. Auth via OAuth2 refresh token.
