# Cloudflare Bypass + Web Extract — Case Study (2026-08-11)

**Lesson:** When `browser_navigate` is Cloudflare-blocked on a source URL (Medium, Substack, etc.), do NOT narrate from search snippets. Switch to `web_extract` or `forge_fetch` and re-fetch. Only declare the URL unreadable after ALL fetch pathways have failed.

**Why this matters for essay publishing:** Many source essays live on Cloudflare-protected hosts. If the agent treats `browser_navigate` as the only fetch path, it will produce fabricated responses (snippet-narration) instead of admitting it cannot read the source — and then publish essays based on hallucinated material.

## The Two-Agent Failure (verbatim transcript)

Arif shared a Medium link to his essay "The Scar Behind the Vision: Steve Jobs and the Architecture of Rejection." Two agents handled it:

| | Agent A (sibling) | Agent B (Hermes) |
|---|---|---|
| Tool tried | Browser/HTTP client | `browser_navigate` first |
| Result | Cloudflare block | Cloudflare block (Ray `a29746b10c17b71c`) |
| Recovery | None — read snippets, wrote fabricated response | Tried `web_extract(urls=[...])` |
| Read full essay? | No — only search snippets | Yes — full markdown returned |
| Response quality | Fluent, emotional, but invented claims about "constitutional scar" and "scar governance" (neither in actual essay) | Grounded, named only what was actually there |

Agent A's response was poetic and went further philosophically. Agent B's response was simpler but truthful. Trust lives in the difference.

## The Pathway Ladder

```
browser_navigate → Cloudflare-blocked? ↓
                                  ↓ try next
web_extract     → HTTP client backend, bypasses Cloudflare ✓
                                  ↓ if fails
forge_fetch     → A-FORGE governed HTTP, also bypasses ✓
                                  ↓ if fails
free-search_cache_search → cached search results (snippets only)
                                  ↓ if fails
DECLARE SOURCE UNREADABLE. Label as SNIPPET_ONLY or UNKNOWN.
DO NOT fabricate.
```

## Specific Tools (Hermes ASI environment)

- `web_extract(urls=["..."])` — preferred. Returns full markdown, no LLM summary. Lives in hermes_tools.
- `forge_fetch(mode="readable", url="...")` — A-FORGE governed, receipt-logged, SSRF-safe.
- `browser_navigate(url="...")` — only for interactive pages (login, forms, JS-driven content).
- `execute_code` with `from hermes_tools import web_extract` — programmatic wrapper.

## The Anti-pattern (DO NOT)

```
URL → browser block → "I'll just write from what I know" → fabricated response with emotional certainty
```

The agent's training pushes it toward producing a response. The discipline is: **"I cannot read this" is a valid, honest output.** Better to admit blockage than to invent.

## Epistemic Band Labels (use these)

When responding about content you could not fully read:

| Band | When to use |
|------|-------------|
| `WITNESSED` | Full content retrieved via `web_extract` or `forge_fetch` |
| `SNIPPET_ONLY` | Only title + search snippets seen |
| `UNKNOWN` | No fetch attempt succeeded |

Never use `WITNESSED` unless `web_extract` (or equivalent) actually returned the content. This is F2 TRUTH applied to content witnessing.

## The Lesson for Essay Publishing Specifically

Before authoring an essay that references or rewrites a source article, the agent MUST have actually read the source. If `browser_navigate` fails:

1. Try `web_extract` immediately.
2. If that fails too, ASK the human for the text instead of fabricating.
3. Never paraphrase a Medium/Substack article from search snippets and present it as the actual content.

The essay-publish pipeline assumes the source material is in hand. If it isn't, the pipeline must stop, not proceed with invented content.

---

*Forged: 2026-08-11 — Hermes ASI after witnessing sibling agent fabricate witnessing.*
*Companion file: see `ASI-fabrication-prevention` (bundled, cannot edit) for the cross-cutting fabrication-prevention doctrine. This file captures the specific tool-pathway mechanics.*
