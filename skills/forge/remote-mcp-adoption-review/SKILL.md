---
name: remote-mcp-adoption-review
description: "Vet a hosted MCP server live before recommending it."
version: 1.0.0
owner: HERMES
tags: [mcp, remote, hosted, evaluation, adoption, evidence]
---

# Remote MCP adoption review

Scope: someone hands you a link to a third-party MCP server (directory listing, registry entry, `npx add-mcp '<url>'`) and asks *test this* / *is this useful* / *why do we need it*. The deliverable is a live probe plus an honest adoption verdict — not a feature list copied from the marketing page.

Protocol conformance belongs to `FORGE-mcp-probe`; federation supply-chain scoring to `FORGE-mcp-registry-ops`. This skill is the human-facing judgement: does it work, is the data behind it real, and what does adopting it cost the person you are recommending it to.

## Procedure

### 1. Get the endpoint, not the brochure

Directory pages (`mcpservers.org`, `agent-ready-directory.com`) are Cloudflare-walled to a headless browser — do not burn calls fighting the interstitial. Fetch the listing as text (Exa/fetch) and lift three facts: the `npx add-mcp '<url>'` line (the endpoint), the registry name `domain/name`, and the publisher repo. The listing's protocol version and tool count are claims to test against, never the answer — they lag the live server.

### 2. Handshake and surface, no install

```bash
curl -sS -X POST "$URL" -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}'

curl -sS -X POST "$URL" -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
```

For repeated calls, use a small Python client that keeps the session id and parses SSE: POST with the same two headers plus `Mcp-Session-Id`, read every line starting `data: `, `json.loads` each frame, and print `result.content[*].text`. Set a browser `User-Agent` on the request.

Read the `instructions` field in the initialize result closely — well-built servers encode their own semantics and citation rules there ("high evidence = well studied, not effective"). That paragraph usually tells you how to interpret every score the server returns.

### 3. Call one real tool with a real question

A tool list proves reachability only. Query something the user would actually ask and inspect the shape of the answer: sourced text, or three lines of marketing? Then query at the edge (a niche term, a known-bad product) — good servers get sharper at the edges, thin ones collapse.

### 4. Read the evidence layer, not the scores

Scores are the publisher's opinion; the fields beside them are the substance: number of studies, study type (RCT vs animal vs case series), dates, named trial registries, regulatory status (approval, WADA/banned lists, market withdrawal). A score reported without the underlying study count is decoration.

### 5. Score the adoption cost, out loud

- **Language** — a corpus in German/Chinese/etc. means every query and answer needs translation. Test one non-native query: many servers fail with a tool error rather than an empty result.
- **Funding** — affiliate links or ads on the same site do not invalidate the data, but the *shopping* pages are not neutral. Say so before the user finds it.
- **What it withholds** — some servers deliberately omit dosing, sourcing, or legal advice. If the person's real question is "what do I take", a server answering "here is the evidence status" is a partial fit, and that must be stated upfront.

### 6. Report

Plain human language, no label blocks, no menus. Structure that works: what you actually ran → two or three concrete findings with the numbers → the honest weaknesses → one recommendation for the specific person, or *no recommendation* if the costs outweigh it.

## Pitfalls

- **`403 Forbidden` from Python but not from `curl`** — Cloudflare rejects the default User-Agent. Set a browser UA before concluding the endpoint is down or the publisher misrepresented it.
- Responses are `text/event-stream`: strip the `data: ` prefix before `json.loads`. Piping the raw body into `jq` fails even when the call succeeded.
- **`-32602 … has an output schema but no structured content was provided` usually means ZERO RESULTS**, not a broken tool: nothing matched, so nothing structured was emitted. Re-query in the corpus's own vocabulary before marking the server defective.
- Argument keys belong to the server: one probe call, read `Required at <field>`, fix the key once. Guessing the schema twice burns the user's patience, not just yours.
- Do not present a probe of the tool surface as a test of the content. "18 tools, all responsive" is infrastructure; the question was whether the answers are worth anything.

## Known servers

**Biohacking Kompakt** — `https://mcp.biohackingkompakt.de/mcp`, Streamable HTTP, no auth, Cloudflare fronted; publisher `github.com/phoeser/biohacking-kompakt`, registry `de.biohackingkompakt/biohacking-kompakt`. Handshake: server `biohacking-kompakt-mcp-server`, protocol `2025-06-18`, 18 tools — registry page says 8, so trust the probe.
Tools: `bk_search_topics`, `bk_get_topic` (full page: mechanism, evidence, risks, legal status, sources), `bk_list_scores`, `bk_compare_topics` (arg key **`ids`**), `bk_search_studien`, `bk_search_inhalte`, `bk_search_blutwerte`, `bk_get_signalweg`, `bk_list_erfahrungen`, `bk_get_zitierregeln` (site citation rules — call before quoting).
Score axes 0-10: human evidence · direction · safety-data status · application experience · mechanism · hype distance. High evidence = *well studied*, not effective; high safety data = well studied, not harmless.
Limits: German corpus (small `/en/` subset; Malay queries return the zero-results error), no dosing or sourcing by policy, affiliate codes for supplement shops on the same site.
Good for: fast reality check on gym/peptide claims — study counts by type, whether human RCTs exist at all, regulatory status, and where the data stop.
