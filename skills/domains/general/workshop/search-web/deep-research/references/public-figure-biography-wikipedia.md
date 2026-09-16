# Public-Figure Biography Research via Wikipedia Article-Graph (verified 2026-08-21)

Pattern for "deep research on [public figure]'s full life story" requests —
especially when the deliverable must VERIFY or DISPROVE a user's claim about
the person (wealth, class background, persona-vs-reality). Proven with the
Anwar Ibrahim briefing (childhood→PM, 9 mandated areas, 13 sources, 322 lines).

## Why Wikipedia-first beats search for biographies

Search engines surface news fragments; Wikipedia already aggregates and
footnoted them. For any figure with an encyclopedic footprint, walking the
article graph is faster AND better sourced than SERP. Start here even when
search works; fall back to search only for post-cutoff news.

## The article-graph walk

Don't stop at the main article. The main article's **table of contents names
every sub-article you need**. Fetch them all (plain curl, Mozilla UA, never
gated):

- Spouse article (family background, education, career — often richer on
  early life than the subject's own article)
- Children articles (each child's entry confirms names/dates independently)
- Event articles (trials, movements, scandals — 3–5× the detail of the summary
  in the main article)
- Organisation articles (ABIM-style bodies: founding dates, leadership
  successions, official reactions)
- School article (institution class markers — "Eton of the East" etc.)
- Cultural-depiction articles (films list the full family cast = independent
  name confirmation for children)

Worked example: Anwar main article + sodomy-trials + Wan Azizah + Nurul
Izzah + Reformasi + ABIM + MCKK + the 2023 biopic = 8 articles, one session.

## Cross-language pivot (highest-value trick)

English Wikipedia is not the ceiling. Two mechanisms:

1. **`{{ill|Name|ms|Title}}` interlanguage templates** in infoboxes literally
   name the language wiki + title that HAS the article when EN doesn't.
   `{{ill|Ibrahim Abdul Rahman|ms|Ibrahim Abdul Rahman}}` → fetch
   `ms.wikipedia.org/wiki/Ibrahim_Abdul_Rahman`.
2. **API-search the other wiki in its own language**:
   `https://ms.wikipedia.org/w/api.php?action=query&list=search&srsearch=<BM query>&format=json`

Malaysia rule of thumb: **EN wiki = political career arc; MS wiki = family,
occupation timelines, local events, kampung-level detail.** The father's
hospital-porter→MP trajectory, second wife, Country Heights residence, and
all six grandchildren by name existed ONLY in MS wiki. The 1974 Baling
demonstration detail (arrest dates, rubber price figures) likewise.

## Infobox Parsoid fragments = free structured data

Wikipedia HTML (non-linted output) embeds infobox data as JSON `wt` fields.
Before the prose even starts you get: birth date/place, parents, spouse,
marriage year, children count, alma mater, occupation, residence. Grep these
first to scaffold the briefing, then confirm in prose.

## Claim-verification output shape

When the task is "verify/disprove [user's claim]" (e.g., "rich kid pretending
to be poor"):

1. Collect **evidence for** the claim (MCKK = elite school; father MP;
   Country Heights residence; wife's Ireland medical degree).
2. Collect **evidence against** (father literally started as hospital porter;
   rural birthplace; Malay-medium primaries; ISA detention at 27).
3. Deliver the **nuanced verdict as facts**: "two-generation ascension
   family — working-class origins, political class by the subject's teens."
   No opinions; let the two evidence columns do the work.
4. Flag oversimplification explicitly when the claim is directionally
   partially true ("oversimplification" is a factual observation about the
   evidence shape, not an opinion).

This mirrors the mandatory counter-narrative rule in the main skill: every
claim analysis presents both sides or it's propaganda.

## Source labelling when news portals are dead

Wikipedia reference lists cite BBC/NST/Amnesty/Bloomberg. When the originals
are unreachable, cite as `"BBC News, 3 Aug 2005" (via Wikipedia ref list)` —
label the indirection honestly in the source section rather than implying a
direct fetch. Premium reference sites behind Cloudflare (Britannica) resolve
via Wayback `/web/<year>/<url>`.

## Local HTML→text converter

Convert each fetched page once, grep the corpus forever:

```python
import re, html
raw = open(p, encoding='utf-8', errors='ignore').read()
raw = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw, flags=re.S|re.I)
raw = re.sub(r'<h([1-6])[^>]*>', lambda m: '\n\n## H'+m.group(1)+': ', raw)
raw = re.sub(r'</t[dh]>', ' | ', raw)
txt = html.unescape(re.sub(r'<[^>]+>', '', raw))
txt = re.sub(r'\[\s*\d+\s*\]', '', txt)  # strip [n] markers
```

Locate sections via heading offsets, facts via regex across all files.
Skip the first ~18KB of each file (nav chrome); the ToC duplicate lists
section names at a lower offset than the body — use `find()` occurrences
beyond the first for the real body.
