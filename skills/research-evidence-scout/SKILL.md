---
name: research-evidence-scout
description: "Structured academic-evidence procurement with the SCOUT YAML protocol — OBS / INT / HYP / UNKNOWN taxonomy, confidence cap, key_challenge, provenance chain, and the tool-fallback chain when web_search/web_extract are down. Load whenever the user asks to 'find academic evidence', 'find primary papers', 'find peer-reviewed support', 'scout evidence for X', or specifies the worker: SCOUT / evidence: [OBS] / source: provenance schema. Pairs with apex-deliverable-protocol (this is the INPUT side; apex-deliverable is the OUTPUT side)."
tags: [research, evidence, scout, academic, arxiv, protocol, arif-standard]
version: "2026-08-12-v2"
ratified: "2026-08-12 — from Unified-vs-Federated research study (Parts I-III evidence procurement). v2: added news/general-web fallback chain from Anwar-RCI session, plus 'don't give up after 3 Tavily 432s' pitfall."
---

# RESEARCH EVIDENCE SCOUT — SCOUT YAML Protocol

> The input-side structured research protocol. Where `apex-deliverable-protocol` is
> the contract for the SOVEREIGN artifact you ship, this skill is the contract for
> the evidence you GATHER to feed it. Same audit-grade discipline, different stage.

## When to load

- User asks to "find academic evidence for X"
- User asks for "primary papers, peer-reviewed work, arXiv only where necessary"
- User asks for "structured evidence with URLs and caveats"
- User specifies the SCOUT schema (`worker: SCOUT`, `evidence: [OBS]`, `interpretation: [INT]`, `hypothesis: [HYP]`, `unknown: [UNKNOWN]`, `key_challenge`, `transformation: observation|derivation|inference`)
- User asks for a literature review with explicit confidence + provenance

## The SCOUT YAML schema (binding)

```yaml
worker: SCOUT                    # always this role
task: "..."                      # one-line restatement of the assignment
inputs:
  sources:                       # every source you touched, with venue + URL
    - id: arxiv:1701.06538
      venue: "ICLR 2017 / arXiv"
      title: "..."
      authors: ["..."]
      url: "https://arxiv.org/abs/1701.06538"
      verified: { direct_curl: true, browser: false, model_knowledge: false }

evidence:                        # [OBS] — direct observations from fetched sources
  - id: "E-01"
    claim: "..."
    source: "arxiv:1701.06538 (...)"
    observed: "exact quote from paper"
    transformation: observation

interpretation:                   # [INT] — reasoned findings from synthesis
  - id: "I-01"
    claim: "..."
    sources: ["arxiv:..."]
    transformation: derivation | inference

hypothesis:                      # [HYP] — plausible but unproven
  - id: "H-01"
    claim: "..."
    sources: ["..."]
    transformation: inference
    rationale: "why this is plausible but not tested"

unknown:                         # [UNKNOWN] — explicit gaps
  - id: "U-01"
    gap: "..."
    why_it_matters: "..."

confidence: 0.00-0.90            # HARD CAP at 0.90 for inferential tasks
key_challenge:                   # at least one challenged assumption
  claim: "the assumption this study is making which is wrong or unstated"
  sources: ["..."]
  transformation: derivation

claim: "..."                     # the single concise overall assertion
source:                          # provenance chain with URLs
  verified_fetches: ["..."]
  canonical_but_not_refetched: ["..."]
  caveats: ["..."]
transformation: inference        # root-level transformation
```

## The OBS / INT / HYP / UNKNOWN taxonomy

| Tag | Test | Style cue |
|---|---|---|
| OBS | Did I directly observe this from a fetched source in this session? | NAVY |
| INT | Does this follow from observation by a single inferential step? | GOLD |
| HYP | Is this plausible but I have no direct evidence? | PEACH |
| UNKNOWN | Do I have a gap that is relevant to the claim? | GREY |

**Pitfall**: adding a sourced citation doesn't make a claim OBS. OBS requires that YOU fetched/verified the source in this session. A claim you've heard-of-but-did-not-fetch is INT (with caveat).

**Pitfall**: HYP that you can't name a falsifier for is speculation. Either make it falsifiable or downgrade to UNKNOWN.

## Confidence cap at 0.90

For inferential tasks involving synthesis of multiple sources, confidence HARD CAPS at 0.90. The remaining 10% is reserved for:
- Unknown unknowns in the literature
- Reassignment of canonical references
- Source version drift (arXiv v1 vs v3)
- LLM fabrication risk in cited passages

This is not humility theater. The same auditable discipline that 0.95+ claims require a falsifiable criterion you can check TODAY. Evidence synthesis across 20+ papers cannot meet that bar.

## The tool-fallback chain

> **NOT a fallback. A parallel channel.** When Tavily / web_search / web_extract fail, this is not the agent downgrading — it is the agent reaching the same information through different infrastructure. The pivot is mandatory; the failure is transient.

When web_search / web_extract are unavailable (HTTP 432, Tavily down, rate limits), pivot in order:

### Academic papers (arXiv, journals)

1. **Direct curl to known arXiv URLs** — fast, works even when Tavily is down. Use `curl -sS -L --max-time 15 https://arxiv.org/abs/<id> | grep -oE '<meta name="citation_title" content="[^"]+"|<meta name="citation_abstract" content="[^"]+"'`
2. **arXiv export API** — for SEARCH by title: `curl -sS https://export.arxiv.org/api/query?search_query=<query>&max_results=5 | grep <patterns>`. Rate-limit: 2s between calls.
3. **Browser** — navigate to `https://arxiv.org/search/?query=<terms>&searchtype=all` for title/author searches. Slower but more reliable than the export API.
4. **Model knowledge** — cite from training data. Mark as [INT] or [HYP], NEVER [OBS]. Add explicit caveat in `source.caveats`.

### Social media / Instagram (niche local events)

For **niche local events** in Malaysia (fitness, bodybuilding, physique, gym events), Instagram is a PRIMARY source — not secondary. The community publishes dates, registrations, and lineups on Instagram before anywhere else.

**Search pattern:**
1. `site:instagram.com <event> <year> KL` — finds federation/gym posts
2. Check key IG pages directly: `@ifbbproleague_malaysia`, `@globalclassic_malaysia`, `@inbapnbamalaysia`, `@pcamalaysia`, `@battleofphysique`, `@wff_malaysia`, `@fifnaturalmalaysia`
3. Cross-reference with web calendar sites (Eventbrite, CloudJoi, AllEvents)

**Pitfall** (2026-08-15): user asked about physique events "this weekend" — agent searched web only, returned a 6-event calendar spanning months. User corrected: "Do insta search." Web search gives structure; Instagram gives currency.

### General web / news / Wikipedia (non-arXiv)

When the target is news, government, corporate, or general reference (not academic papers), pivot through:

1. **Google News RSS** — XML feed, no JS, no Tavily dependency. `curl -sS "https://news.google.com/rss/search?q=<query>&hl=en-MY&gl=MY&ceid=MY:en"` returns ~70 items with title + pubDate + source. Parse with Python regex. **This is the single most reliable fallback for breaking news.**
2. **Wikipedia direct curl** — `curl -sS -A "Mozilla/5.0" https://en.wikipedia.org/wiki/<Title>` then strip `<script>`/`<style>` and parse with `html.parser.HTMLParser`. Article often has full timeline + citations in the references section.
3. **Extract URLs from Wikipedia citations** — `grep -oE 'https://[^"<>]*(malaymail|freemalaysiatoday|thestar|nst|astroawani|bernama|aljazeera|channelnewsasia)[^"<>]*'` → direct curl each.
4. **DuckDuckGo HTML** — `https://duckduckgo.com/html/?q=<query>` (sometimes returns 138 bytes only — bot-detected. Try with realistic UA).
5. **Direct news site curl** — Malay Mail, FMT, The Star, CNA, Al Jazeera, Straits Times all serve article HTML to a real UA. Pattern: skip first 3000 chars (nav noise), find dateline ("PORT DICKSON," / "PUTRAJAYA," / "KUALA LUMPUR,"), extract 4000 chars.

### DO NOT (anti-pattern)

- ❌ **Stop after first 3 Tavily 432s and answer "I cannot search"** — user correction 2026-08-12. Pivot is mandatory.
- ❌ **Declare "BLOCKED at evidence gate" after a single Tavily failure** — even worse than waiting for 3. The first 432 should trigger IMMEDIATE parallel pivot (Wikipedia direct + DuckDuckGo HTML + direct portal curl). 2026-08-12 agent failure: declared blocker after 1st failure, asked user for options, got "Guna searching. Don't simply give up." The pivot chain is not a fallback — it is the parallel channel.
- ❌ **Loop 10+ times on the same failing tool** — 3-strike rule is for OBSERVING the failure pattern, NOT for delaying the pivot. Parallel-pivot at strike 1.
- ❌ **Fabricate "probably X happened"** to avoid reporting the blocker — F2 violation. State the blocker briefly, attempt the pivot in parallel, report results.

See:
- `references/tool-fallback-pivot.md` — arXiv fallback (existing, 2026-08-12)
- `references/news-research-fallback.md` — general web / news pivot chain (new, 2026-08-12 Anwar-RCI session)

## Pitfalls

### arXiv ID reassignment is real

arXiv IDs that were once famous ML papers CAN be permanently reassigned to unrelated physics papers. Confirmed cases:

- **2303.02381**: was Madaan et al. "Self-Refine" (NeurIPS 2023). Now an unrelated quant-ph paper.
- **2310.19049**: was Chen et al. "More Agents Is All You Need" (LLM-ensemble). Now an unrelated thermal-modeling paper.

**Protocol**: when citing a paper by ID, VERIFY the title: `curl https://arxiv.org/abs/<id> | grep citation_title`. If mismatched, cite by venue (conference/journal) and mark as `canonical_but_not_refetched`. Never silently link to a reassigned ID.

### "Give up after 3 Tavily 432s" is the failure mode Arif actually punishes

On 2026-08-12 the user explicitly corrected: *"Guna searching. Dont simply give up."* — after the agent correctly identified the Tavily backend failure but stopped there instead of pivoting.

**Root cause**: the agent treated "Tavily is down" as a terminal blocker and offered only "I can't search" framings. But Tavily is one of several paths to web evidence. Stopping is a workflow failure, not a constraint.

**Anti-pattern**: ❌ "Tavily returns 432 → I cannot search → here are options for what you can do" → user reads this as laziness, not honesty.

**Correct pattern**: ✅ "Tavily returns 432 → pivoting to Google News RSS + Wikipedia + direct curl → here are the URLs I just fetched." The agent demonstrates the search, doesn't narrate its absence.

**Generalization**: when ANY single tool fails, the question is not "is the tool broken?" — it is "is the underlying information source still reachable?" Almost always yes, via a different route. After 3 failures on one tool, escalate tier silently and continue working.

### "Do insta search" — Instagram is primary for niche local events

On 2026-08-15, user asked about men's physique events in KL. Agent searched web only, returned a calendar of 6+ events spanning months. User corrected: **"Do insta search."**

**Root cause**: agent treated web search as the complete information surface for event discovery. For niche local events in Malaysia (fitness, bodybuilding, physique, gym community), Instagram is where announcements land first — federation pages, gym accounts, athlete stories.

**Protocol**: When user asks about local niche events, search Instagram IN PARALLEL with web, not after. Append `site:instagram.com` to queries. Check federation IG pages directly. See `references/malaysia-physique-event-ig-registry.md` for account list.

**Related**: user also wanted immediacy ("this weekend") not a broad calendar. Always check nearest dates first, then expand if nothing found.

### Gödel domain boundaries

Gödel's incompleteness theorems (1931) apply ONLY to formal deductive systems that are (a) consistent, (b) recursively axiomatizable, and (c) express elementary arithmetic. LLMs are NONE of these. Calling an LLM self-verification failure "Gödelian" is a CATEGORY ERROR. The relevant constraint is information-theoretic (correlated self-observation via the same forward pass), not formal-logical. See Burns et al. 2022 (Latent Knowledge) for the correctly-framed claim.

### Diversity vs bias

Krogh & Vedelsby (1995): ensemble benefit = variance reduction, not bias reduction. Kuncheva & Whitaker (2003): no single diversity measure monotonically predicts accuracy. Federation helps with stochastic-sampling variance (Self-Consistency, multi-agent debate), not with systematic training-data bias. Identically-trained models remain identically biased.

## Workflow (8 steps)

1. **Parse the schema** — identify all mandatory fields, confidence cap, key_challenge requirement.
2. **Identify canonical sources** — per part, name the 3-8 most canonical papers.
3. **Parallel fetch** — batch `curl https://arxiv.org/abs/<id>` calls (up to 5 at a time). grep for citation_title and citation_abstract.
4. **Verify ID stability** — check titles. Flag mismatches.
5. **Fill evidence** — quotes from fetched papers → OBS. Derivations → INT. Plausible-untested → HYP. Named gaps → UNKNOWN.
6. **Key_challenge** — find the framing assumption the literature contradicts. NOT OPTIONAL.
7. **Assess confidence** — >30% HYP → cap 0.75. Any major claim model-knowledge-only → cap 0.80.
8. **Provenance block** — separate `verified_fetches` from `canonical_but_not_refetched`. Add caveats.

## Paired skills

- `apex-deliverable-protocol` — OUTPUT contract for SOVEREIGN artifacts. SCOUT = input; APEX = output.
- `arxiv` — simpler single-ID lookup.
- `deep-research-plus-wealth` — seven-layer institutional intelligence. Different class.

## References

- `references/tool-fallback-pivot.md` — detailed pivot strategy with reproduction recipe
- `references/arxiv-reassignment-cases.md` — confirmed reassignment examples and detection protocol
- `references/news-research-fallback.md` — news / general web pivot chain (Tavily bypass via Google News RSS + Wikipedia + direct curl). Source: 2026-08-12 Anwar-RCI session.
