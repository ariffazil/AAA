# Tool-Fallback Pivot Chain — Reproduction Recipe

> When web_search / web_extract are unavailable, escalate through this chain. Source:
> 2026-08-12 SCOUT session for the Unified-vs-Federated research study (Parts I-III).

## Symptom

- `web_search` returns 4+ consecutive failures with HTTP 432 (Tavily down) or HTTP 429 (rate-limited)
- `web_extract` returns 432 / 429 similarly
- Tool loop warning fires: "same_tool_failure_warning; count=N"

## Tier 1 — Direct curl to known arXiv URLs

Works against `https://arxiv.org/abs/<id>` even when Tavily is fully down. arXiv HTML
serves stable metadata to any compliant user-agent.

```bash
# Single-paper metadata extraction
curl -sS -L --max-time 15 -A "Mozilla/5.0" \
  "https://arxiv.org/abs/1701.06538" \
  | grep -oE '<meta name="citation_(title|abstract|author)_" content="[^"]+"' \
  | sed 's/<meta name="citation_/  /'
```

Batch up to 5 IDs at a time. If a call fails with timeout, retry with a fresh
connection — arXiv rate-limits by IP, not by URL.

## Tier 2 — arXiv export API for SEARCH by title

Use when you know the paper exists but not the canonical ID.

```bash
curl -sS -L --max-time 15 -A "Mozilla/5.0" \
  "https://export.arxiv.org/api/query?search_query=ti:\"Reluplex\"+AND+ti:\"neural\"&max_results=3" \
  | grep -oE 'arxiv.org/abs/[0-9]+\.[0-9]+|<title>[^<]+</title>'
```

**Caveats**:
- Single quotes inside the title need care; use `+` for spaces and `%22` for embedded quotes.
- Add 2s minimum between calls — arXiv will throttle without warning.
- If the API times out (no bytes received), fall back to Tier 3.

## Tier 3 — Browser

When both curl + export API are slow/unavailable, use the browser to navigate
to arXiv's search UI:

```
https://arxiv.org/search/?query=%22<title-fragment>%22&searchtype=all
```

Or for direct paper access:
```
https://arxiv.org/abs/<id>
```

The browser is slower but more reliable than the export API for title searches.

## Tier 4 — Model knowledge with explicit caveat

When the live path is unreachable and you only have training-knowledge of the paper:

- Mark the claim as `[INT]` (or `[HYP]` if uncertain), NEVER `[OBS]`.
- Cite by venue (conference/journal) rather than the arXiv ID if you have any
  reassignment doubt.
- Add a caveat to `source.caveats` listing which sources were model-knowledge-only.

## Escalation log (template)

```yaml
source:
  caveats:
    - "Tavily web_search / web_extract returned HTTP 432 throughout this session"
    - "Semantic Scholar API rate-limited (HTTP 429)"
    - "arXiv export API timed out"
    - "Evidence procured via direct curl + browser fallback"
```

## Real session log (2026-08-12)

1. Started with web_search for Krogh-Vedelsby, Kuncheva, Chen-More-Agents, etc.
   → 4 consecutive HTTP 432 from Tavily.
2. Pivoted to web_extract with 5 paper URLs.
   → 3 consecutive HTTP 432.
3. Pivoted to direct curl for arXiv HTML.
   → Worked first try. 15 papers verified.
4. Tried arXiv export API for Self-Refine / Looking Before You Leap.
   → Timed out intermittently.
5. Used browser to search arXiv by title.
   → Worked but found that the original Madaan-Self-Refine arXiv ID
     (2303.02381) was permanently reassigned to a quant-ph paper.
6. Confirmed via direct curl that the title at 2303.02381 was NOT Madaan's.
   → Cited Self-Refine by NeurIPS 2023 venue instead.

## Hazards

- **Don't trust your own model knowledge as [OBS]**. You didn't fetch it. It's [INT].
- **Don't cite a reassigned ID silently**. The reader will click through and land
  on a physics paper. Cite by venue.
- **Don't loop on the same failing tool**. After 3 failures, switch tiers.
- **Don't recommend "Tavily doesn't work"** as a durable rule. Tavily will be back up
  tomorrow. The durable lesson is the pivot chain, not the failure.
