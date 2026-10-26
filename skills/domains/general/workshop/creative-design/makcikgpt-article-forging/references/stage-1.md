# Stage 1 — full text (moved verbatim 2026-10-23, surgical compression)

## Stage 1: OBSERVE — Research

**Rule: 3+ searches minimum. Breadth before depth.**

**Primary research tool: A-FORGE MCP `forge_search`** (Brave API, port 7072). More reliable than Tavily/web_search which frequently 432 or CAPTCHA. **Streamable-http handshake required (2026-08-21):** POST `initialize` → `notifications/initialized` → `tools/call`, all to `http://127.0.0.1:7072/mcp` with `Accept: application/json, text/event-stream`. Without handshake: `Missing tool name` error. Caveat: forge_search sometimes returns the same generic results regardless of query — treat as one source, never the only one.

**Search-failure fallback chain (proven 2026-08-21 — SearXNG junk, firecrawl credits out, browser_exec crash, Reuters 401, Al Jazeera 404):**
1. **News articles:** `curl -sL -A "Mozilla/5.0" <url>` then extract `<title>` / `og:title` / `og:description` / meta description — most news sites (The Edge included) put the full lede in `og:description` even when body extraction fails.
2. **Biography/background:** Wikipedia API (`action=parse&prop=wikitext` for full text with regex ref/`{{}}`/`[[]]` stripping; `action=query&prop=extracts&explaintext=1` for summaries; `section=N` for one era at a time). Also pull the *family members'* pages (father, spouse, children) — the father's Malay-Wikipedia page carried facts the English main page didn't.
3. **Federation archives first:** `search_files` over `/root/_archive`, `/root/petronas` for insider signal files before the web.
4. **Delegate the grind:** background subagent with `output_schema` — it burns its own context on fallbacks and returns a verified, sourced briefing file (322-line briefing in ~27 min while the main thread kept working).

Search strategy:
- Surface data (what happened)
- Structural data (why it matters)
- Shadow data (who benefits, who loses)

Use `forge_search` for breadth. Use `forge_fetch` or `forge_fetch_url` for depth on specific articles.

Use `forge_search` or `web_search` for breadth. Use `web_extract` or `forge_fetch` for depth on specific articles.

**LinkedIn as primary source for corporate profiles:** When BANGANG profiling a named executive, LinkedIn is the MOST reliable source for career history. Web search often returns only news articles (which carry PR framing). Go direct to LinkedIn via browser. Extract: every title, employer, duration, description. Cross-check against Wikipedia (company fate) and The Edge (financial data). Pitfall: LinkedIn "about" sections are self-authored PR — read them for WHAT they claim, not what's true.

Use `forge_search` or `web_search` for breadth. Use `web_extract` or `forge_fetch_url` for depth on specific articles.

**Evidence tagging:** Every data point gets OBS/INT/SPEC/SHADOW tag INTERNALLY during research. But: **do NOT put epistemic labels in the article text for relatable/rakyat-marhaen articles.** Arif explicitly rejected: "The moment aku nampak epistemik. Aku dah down. Malas nak baca." Epistemic discipline is for the forge process, not the reader output. For kutuk-mode essays targeting informed audiences, epistemic labels are acceptable. For rakyat marhaen articles — strip them completely.

**Number verification (MANDATORY):** Before publishing any financial claim, cross-check against primary sources (PETRONAS IR, FRED, BNM). In session 2026-07-13, FY2022 PAT was incorrectly stated as RM55b (actual: RM101.6b per IR2025 five-year table). Gemini external audit caught it. Always verify year-attribution: don't mix FY2024 numbers with FY2022 narrative. Pitfall: PETRONAS Group reports HALF-YEARLY, not quarterly. There is no "PETRONAS Group Q1 2026" — only 1H 2026 (expected Aug-Sep 2026). Listed subsidiaries (PGB, PCG, PETDAG) report quarterly.

---

