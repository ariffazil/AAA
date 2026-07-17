> ⚠️ SUPERSEDED by docs/ZEN99.md (2026-07-17). Read ZEN99.md first.

# SEARCH-ZEN — Web Search Tool Map

> **One map. All search tools. Route by intent, not habit.**
> Last verified: 2026-07-02 · FORGE (000Ω)

---

## Quick Routing Table

| Intent | Best Tool | Fallback | Why |
|--------|-----------|----------|-----|
| Fast keyword lookup | `forge_search` | `brave_web_search` | Brave = fast, cheap, reliable |
| Alternative keyword search | `minimax-code_web_search` | `forge_minimax_search` | MiniMax engine, direct access |
| Deep multi-source research | `forge_research` | `perplexity_research` | Agentic depth, citations |
| Quick AI answer with citations | `perplexity_ask` | `forge_minimax_search` | Sonar Pro = grounded Q&A |
| Step-by-step reasoning + web | `perplexity_reason` | `sequential-thinking` + search | Chain-of-thought + web |
| Ranked results with feedback | `meyhem_search` | `brave_web_search` | Feedback loop improves over time |
| Full page content extraction | `exa_web_fetch_exa` | `webfetch` | Clean markdown, batch URLs |
| Semantic search (meaning-based) | `exa_web_search_exa` | `perplexity_ask` | Embeddings, not keywords |
| Image search | `brave_image_search` | — | Only image search available |
| Video search | `brave_video_search` | — | Only video search available |
| News/trending | `brave_news_search` | `perplexity_search` w/ recency | Freshness filter built-in |
| Local business/place | `brave_local_search` | — | Only local search available |
| Deep page context extraction | `brave_llm_context_search` | `exa_web_fetch_exa` | Snippets + full text |
| Find MCP tool for task | `meyhem_find_capability` | `arif_retrieve_tools` | Cross-ecosystem discovery |
| Find MCP server for task | `meyhem_find_server` | — | Server-level discovery |
| URL fetch (any page) | `webfetch` | `exa_web_fetch_exa` | Simple, always works |

---

## Tool Inventory (20 search-capable tools)

### Tier 1: Primary Search (use these first)

| # | Tool | Source | Transport | Cost | Strength |
|---|------|--------|-----------|------|----------|
| 1 | `forge_search` | A-FORGE → Brave | stdio | Free (Brave free tier) | Fast keyword search, governed |
| 2 | `forge_research` | A-FORGE → multi | stdio | Free | Multi-source, depth control, citations |
| 3 | `forge_minimax_search` | A-FORGE → MiniMax | stdio | MiniMax credits | Alternative engine |
| 4 | `perplexity_ask` | Perplexity MCP | local | Perplexity sub | Quick AI-grounded answer |
| 5 | `perplexity_search` | Perplexity MCP | local | Perplexity sub | Ranked results, no synthesis |
| 6 | `meyhem_search` | Meyhem MCP | remote | Free | Feedback-ranked, improves over time |
| 7 | `minimax-code_web_search` | MiniMax-Code MCP | :18091 | MiniMax credits | Google-like keyword search |

### Tier 2: Specialized Search

| # | Tool | Source | Transport | Cost | Strength |
|---|------|--------|-----------|------|----------|
| 8 | `perplexity_reason` | Perplexity MCP | local | Perplexity sub | Chain-of-thought + web |
| 9 | `perplexity_research` | Perplexity MCP | local | Perplexity sub | Deep multi-source (30s+) |
| 10 | `exa_web_search_exa` | Exa MCP | local | Exa credits | Semantic/embeddings search |
| 11 | `exa_web_fetch_exa` | Exa MCP | local | Exa credits | Full page extraction, batch |
| 12 | `brave_web_search` | Brave MCP | local | Free | Raw Brave API |
| 13 | `brave_llm_context_search` | Brave MCP | local | Free | Context extraction with snippets |

### Tier 3: Media & Local Search

| # | Tool | Source | Transport | Cost | Strength |
|---|------|--------|-----------|------|----------|
| 14 | `brave_image_search` | Brave MCP | local | Free | Image search |
| 15 | `brave_video_search` | Brave MCP | local | Free | Video search |
| 16 | `brave_news_search` | Brave MCP | local | Free | News with freshness filter |
| 17 | `brave_local_search` | Brave MCP | local | Free | Local businesses/places |

### Tier 4: Discovery & Fetch

| # | Tool | Source | Transport | Cost | Strength |
|---|------|--------|-----------|------|----------|
| 18 | `meyhem_find_capability` | Meyhem MCP | remote | Free | Find tools across ecosystems |
| 19 | `meyhem_find_server` | Meyhem MCP | remote | Free | Find MCP servers |
| 20 | `webfetch` | Native | local | Free | Simple URL → markdown |

---

## Duplicate Map (where tools overlap)

| Overlap | Tools | Winner | Why |
|---------|-------|--------|-----|
| Keyword search | `forge_search` vs `brave_web_search` | `forge_search` | Governed, auto-receipt |
| AI answer | `perplexity_ask` vs `forge_research` | Context-dependent | Quick=ask, depth=research |
| Page fetch | `webfetch` vs `exa_web_fetch_exa` | `webfetch` (simple), `exa` (batch/quality) | Exa for structured extraction |
| Web search | `forge_minimax_search` vs `brave_web_search` | `forge_search` | MiniMax is fallback engine |
| Deep research | `perplexity_research` vs `forge_research` | `forge_research` (governed), `perplexity` (quality) | Perplexity has better synthesis |

---

## Decision Flowchart

```
Need to search the web?
│
├─ Quick fact? → perplexity_ask
├─ Fast lookup? → forge_search
├─ Deep research? → forge_research or perplexity_research
├─ Semantic/similar? → exa_web_search_exa
├─ Need full page text? → webfetch or exa_web_fetch_exa
├─ Image/video/local? → brave_*_search
├─ Find a tool? → meyhem_find_capability
└─ Ranked + feedback? → meyhem_search
```

---

## Engine Characteristics

| Engine | Method | Best For | Limitation |
|--------|--------|----------|------------|
| **Brave** | Keyword + Web Graph | Fast factual lookups | No semantic understanding |
| **Exa** | Embeddings + Keyword ("auto") | Meaning-based discovery | Credits required |
| **Perplexity** | Sonar models + web | Grounded AI answers | Subscription cost |
| **MiniMax** | Web search API | Alternative coverage | Less mature |
| **Meyhem** | Feedback-ranked aggregation | Improving over time | Remote dependency |

---

## F2 TRUTH Labels

All search results are **OBSERVED** (from external source). Never label search results as DERIVED or INTERPRETED without explicit reasoning. Citations mandatory for any claim sourced from search.

---

*Forged: 2026-07-02 · FORGE (000Ω)*
*DITEMPA BUKAN DIBERI*
