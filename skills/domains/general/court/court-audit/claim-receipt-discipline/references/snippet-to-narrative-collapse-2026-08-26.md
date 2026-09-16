# Snippet-to-Narrative Collapse — Worked Example & Fix Landscape (2026-08-26)

## The failure, end to end

1. Arif: "explore reddit page something we lack of. Pure exploration mode."
2. Agent routes to Reddit. Every full-content path fails:
   - `curl old.reddit.com/*.json` → HTTP 403 (VPS IP blocked)
   - `curl_cffi` with `impersonate="chrome"` → still 403
   - `firecrawl_scrape` on reddit.com → "we do not support this site"
   - Composio `REDDIT_SEARCH_ACROSS_SUBREDDITS` → "No connected account found"
   - browser tool → hung on debug output
3. One path DID work: `mcp__social_mcp__web_search_social` (platform=reddit) → returned
   title + ~200-char description per result. Tier-2 evidence only.
4. Agent emitted "GAP 1–6" synthesis with flat confidence.
5. Arif: "Are u sure about ur system intel?" → honest post-hoc ladder.
6. Arif: "Ai agent do fill in the gaps with magic!!! SO BANGANG!!! Deep research how to solve this."

## Audit of the six "gaps"

| Gap | Claim | Tier at emission | Post-hoc |
|---|---|---|---|
| 1 MCP CVEs | CVE-2025-49596, -30615, -30623 real | T1 after NVD check | VERIFIED |
| 1 AVE-2026-00002 | "tool description injection" taxonomy | T2 (snippet) | UNVERIFIED body |
| 2 Hindsight | "open source agent memory" | T4 relayed | exists (21k stars) but claim unverified at emission |
| 3 Subconductor | "persistent task tracking pattern" | T2 | exists (2 stars, TS MCP) |
| 4 XAUUSD bot | "+$4k/30% in 6 days" | T4 relayed, unflagged | poster's own claim |
| 5 context breakage | "agents break under long convos" | T2 | thread exists, body unverified |
| 6 MCP stateless | "initialize handshake gone" | T3 inferred | I did NOT read the spec diff |

Result: 2 T1, 3 T2, 1 T4, 1 T3 — but all six emitted with equal narrative weight. Cite
density ≈ 33% (below the 50% FM9 floor).

## Working verification oracles (reuse these; do NOT re-derive)

CVE existence + description (primary source, no auth):
```bash
curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-YYYY-NNNNN"
# → {"vulnerabilities":[{"cve":{"id":...,"published":...,"descriptions":[...]}}]}
#   200 + totalResults:1 = real. Confirm "MCP"/"Model Context Protocol" appears in the description.
```

MCP spec version timeline (primary source, no auth):
```bash
curl -sL "https://modelcontextprotocol.io/specification" -H "User-Agent: Mozilla/5.0" \
  | grep -oE "20[0-9]{2}-[0-9]{2}-[0-9]{2}" | sort -u
# → lists released spec dates. Presence of a date ≠ reading the diff. Read the diff before
#   claiming WHAT changed ("handshake gone", etc.).
```

GitHub repo receipts (stars/recency/liveness — the bare-URL probe pattern):
```bash
curl -s https://api.github.com/repos/OWNER/REPO | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['stargazers_count'],d['created_at'],d['pushed_at'],d['description'])"
```

Reddit snippets when full content is blocked:
- `mcp__social_mcp__web_search_social(platform="reddit", query=...)` → title+description only.
- Full bodies need Reddit OAuth (Composio connected account) OR the zero-config
  `reddit-mcp-ai` MCP server (Arctic Shift archive + DDG fallback), NOT the .json endpoint
  from a datacenter IP.

## Research landscape (2025–2026), condensed

Papers:
- **One Gate Is Not Enough** (arxiv 2608.18360, Aug 2026) — agentic pre-action controls compose
  authority + resource + evidence gates; remediation by one gate can invalidate another's
  judgment; single gates are unsound. Directly supports the "compose gates, don't add one
  prompt rule" conclusion.
- **FactScore** (Min et al. 2023) — decompose output into atomic claims, verify each against a
  source, score precision. Blueprint for claim-level verification.
- **SelfCheckGPT** (2023) — sample N responses, measure agreement; divergence → drop confidence.
- **Teaching Models to Express Uncertainty** (Lin et al. 2022) — calibrate per-sentence
  confidence markers.

Tools:
- **Guardrails AI** `ProvenanceV1` validator — every sentence must trace to a retrieved chunk;
  `on_fail="fix"|"block"`. Closest off-the-shelf evidence gate.
- **Subconductor** (`PaulBenchea/mcp-subconductor`) — persistent state machine; externalizes task
  state into a manifest so agents don't drift from context. Mirrors our FM3a fix (probe, don't
  remember).
- **Hindsight** (`vectorize-io/hindsight`, 21k★) — agent memory with provenance, MIT.
- **LMQL** — constrained generation; force structured output (`{claim, evidence|null,
  confidence}`) so null evidence cannot masquerade as fact.

## Structural fix sketch (evidence-gate middleware)

```python
def evidence_gate(output, retrieval_set) -> str:
    claims = extract_atomic_claims(output)          # FactScore-style
    tiers = [classify(c, retrieval_set) for c in claims]  # T1..T4 ladder
    verified = sum(1 for t in tiers if t == "T1")
    if verified / len(claims) < 0.5:
        return "INSUFFICIENT_EVIDENCE — cannot verify majority of claims. Stopping."
    return format_structured(claims, tiers)          # every claim carries its tier
```

Wire at output layer (post-generation) AND input layer (retrieval-constrained generation).
Honor-system prompt rules drift; a regex/interceptor at the bridge cannot.

## One-line takeaway

Snippet ≠ evidence. When full-content retrieval fails, degrade to "snippets only — cannot
synthesize" and offer an alternative path. Never let tier-2/3/4 claims wear tier-1 confidence.
