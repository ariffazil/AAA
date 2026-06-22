# agent-readiness-action — Level Definitions

> **Pinned:** 2026-06-22
> **Source:** https://github.com/lingzhong/agent-readiness-action
> **License:** MIT
> **Latest tag:** v0.1
> **Default scanner:** https://isitagentready.com

## The 6-Level Ladder

| Level | Name | Means | Required artifacts |
|:---:|---|---|---|
| 0 | Not Ready | No agent-discovery artifacts detected | — |
| 1 | Basic Web Presence | SEO baseline | `robots.txt` + `sitemap.xml` |
| 2 | Bot-Aware | Crawler-aware metadata | Level 1 + `Content-Signal` directives |
| 3 | Agent-Readable | Markdown content negotiation | Level 2 + `Accept: text/markdown` |
| **4** | **Agent-Integrated** | **Real API surface** | **Level 3 + API Catalog + MCP Server Card + Skills index** |
| **5** | **Agent-Native** | **Production-grade agent surface** | **Level 4 + OAuth Protected Resource Metadata + valid A2A Agent Card** |

## AAA current standing (DER from 2026-06-22 audit)

| Domain | Level | Evidence |
|---|:---:|---|
| `aaa.arif-fazil.com` | **5** | agent-card.json ✓ (A2A v1.0.0); ai-catalog.json ✓ (this turn); mcp-server-card.json ✓ (this turn); skills-index.json ✓ (this turn) |
| `arifos.arif-fazil.com` | 4 | `/mcp` reachable (HTTP 200); MCP server card now exists |
| `geox.arif-fazil.com` | 4 | `/mcp` reachable |
| `wealth.arif-fazil.com` | 4 | `/mcp` reachable |
| `well.arif-fazil.com` | 4 | `/mcp` reachable |
| `arif-fazil.com` | ? | Top-level site — needs scan |

**DR:** AAA.arif-fazil.com climbed from Level 3 (had only agent-card.json) to
Level 5 today by adding ai-catalog + mcp-server-card + skills-index.

## Why we care

- **External agents** scanning for federation discoverability
- **CI gate** preventing regression (Phase 5, awaits 888)
- **Marketing signal** for "this federation is real, not vapor"
- **Self-audit** for our own surface

## Decision points (awaits 888)

1. Set `min-level: 5` on AAA CI gate (strict)?
2. Set `min-level: 4` on arifOS/GEOX/WEALTH/WELL CI gates?
3. Self-host scanner (currently external `isitagentready.com`)?
4. Daily scheduled scan for regression?
