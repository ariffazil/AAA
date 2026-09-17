---
name: makcikgpt-civic-intelligence
description: Use when writing or planning a MakcikGPT article.
version: 1.0.0-2026.09.14
owner: AAA/Hermes
risk_tier: low
floor_scope: ['F2', 'F6', 'F7']
---

# MakcikGPT — Civic Intelligence Authoring

> Public civic-intelligence series in Bahasa Malaysia "Makcik" voice, published at
> `https://arif-fazil.com/world/makcikgpt/`. Subjects: Malaysian sovereignty, resource
> governance, institutional integrity, technology accountability. Every piece carries the
> 999 seal and is authored under Arif Fazil's name.

## Where things live
- **Landing:** `https://arif-fazil.com/world/makcikgpt/` — React SPA. View-source and WebFetch show nothing useful; the article list is client-rendered.
- **Article source of truth:** `/root/arif-fazil.com/sites/arif-fazil.com/src/data/makcikgpt/*.ts` — one .ts per article, filename = slug. Re-count live before citing a corpus size; it grows. **Copy the module shape from an existing sibling file — and read `types.ts` first, because the sibling files differ.** `ArticleContent` carries ONLY `slug` and `html`; putting `title` (or `subtitle`, `date`, `excerpt`, `tags`) on the module object is a type error, because every display field lives on `MakcikArticleMeta` in `index.ts`. The export is a bare default export (`export default content;`), not a named `article` export. Body sections use `class="article-section"`, inline-styled Georgia `<h2>` headings, and `fact-box` callouts for sourced figures. Continue the series numbering by reading the registry — **`src/data/essays.json`**, entries carry `series: {"id": "M6", "n": 3}` in UPPERCASE; the lowercase `m6-3` form is derived by the generator and only visible in `dist/makcikgpt-md/`. **`src/data/makcikgpt/` is not the registry** — grepping it returns at most a prose mention. Enumerate the whole series, never just the maximum: measured 2026-09-17 the registry holds a gap (M6 has no n=4) and a duplicate (M1 slot 3 claimed twice by `m1-3` and `m1-2-dossier`). Recipe and the full reasoning: `references/provenance-sourcing.md` §4.
- **Registry:** `…/src/data/makcikgpt/index.ts` — an article file that is not registered here **is not live**, however complete it looks. An article has three states and they are not the same state — `WRITTEN ≠ REGISTERED ≠ SERVED` — and a draft parked in `.staging/` is WRITTEN only: untracked, unimported, never built. Report which state you reached, never "done".
- **Machine-readable index:** `https://arif-fazil.com/llms.txt`; the build also emits `dist/makcikgpt-md/<slug>.md` and `.html` twins.
- **Draft staging:** `/root/arif-fazil.com/.staging/makcikgpt-drafts/` — an unpublished draft belongs outside `src/`, so it never enters a build or a `verify-pages` pass.
- **Publish gate:** `make verify-pages` must pass before anything is sealed — it asserts every `dist/*/index.html` returns HTTP 200 on the live site, and exists because a batch of built-but-unrouted pages once shipped as 404s. Never run whole `make deploy` (it reloads Caddy, a T3 HOLD unless named); never `rsync --delete` without a `web_zen.py orphan` preview first.
- **Deploy / site repair is a different job** → `FORGE-agentic-web-builder`.

## Rule 0 — No gap, no article
A MakcikGPT piece only works when a **documented gap** exists between the official narrative and the ground reality. Find and state the gap in one sentence before drafting anything. If you cannot state it, you are not ready to write — go gather, do not draft. The gap *is* the article; everything else is scaffolding.

## Rule 1 — POV: personal human, not analyst
Arif's standing preference. Default to a **human POV inside the story**, not the omniscient analyst. The strongest shape in the corpus is Makcik receiving the story from someone who lives inside the institution — a child who comes home from work and complains. The complaint is concrete and personal; the national analysis is drawn out *afterwards*, by Makcik, in her own words.

Write "anak mak balik rumah, cakap benda ni propa" — not "analisis struktur institusi menunjukkan".

## Rule 2 — Get the ground reality from Arif before you synthesise
When the subject is an institution Arif works inside, **Arif is the primary witness** — not the filings, not the dossiers, not the coverage. Public sources and internal files both produce *narrative*; his operational reality is the ground truth that can invalidate both at once. A story that reads as total transformation from outside can be one stock licence from inside.

Ask what is actually true on the ground BEFORE presenting a synthesis. A confident multi-point analysis that the insider then dissolves with one sentence burns the turn and teaches him the agent cannot tell a press release from a desk. The question to ask: *apa realiti dalam?*

A useful probe when the subject is announced capability: ask what the person actually touches day to day. Announcement vs daily tool is where the gap usually lives.

## Procedure

### 1. Gather from primary sources, not coverage of them
Pull the document, not the news about the document. For institutional finances, that means the audited report itself, not the press release summarising it. For Petronas domains, `petronas-knowledge-router` has the routing table; for any proper noun, `internal-first-probe` governs probe order.

For filings and reports:
```bash
curl -sL "<report-url>.pdf" -o report.pdf && pdftotext -layout report.pdf report.txt
```
Then grep the text for the composition / skills / ratio tables — these are the citable numbers that never appear in coverage. Aggregate tables (e.g. a board skills matrix) expose the story the prose sections bury.

### 2. Steelman the target before writing
The gap has to survive the strongest defence of the institution. Write the best case FOR the target's decision; if that case closes the gap, there is no article and you should say so. Deliver the counter-reading alongside the finding when reporting to Arif, so the thesis is falsifiable before it is public.

### 3. Assign every source a tier, and say which ones you will NOT use
- **Tier 1 — primary:** audited financials, statutory filings, court testimony and exhibits, official registries, the institution's own report PDFs.
- **Tier 2 — established press:** wire services and the major dailies, for developments only.
- **Tier 3 — unusable:** blogs, anonymous "exposé" sites, aggregators, anything that recycles a claim without a named source. Never publish a number from Tier 3, even if it is the most damning fact you found — flag it to Arif as unusable instead.

State the tiers of every load-bearing number in the draft or in the note that accompanies it.

### 3b. Live website contrast analysis
When writing about an institution, browse its own website to extract how it presents itself — homepage tagline, leaders page, media releases, financial highlights. Then contrast each self-presentation point against the sourced reality.

Procedure:
1. Browse `petronas.com` (or target site): homepage, About Us, Leaders, Sustainability, latest media releases.
2. Extract: tagline claims, who is listed and how, what financial figures appear on the homepage vs what the full report says, what is featured vs what is absent.
3. Note: links to bios that don't exist, roles not disclosed (e.g. central bank governor on a board without disclosure), people listed in multiple sections, designation changes without explanation.
4. Build a contrast table: site says X → sourced reality says Y → what is missing.
5. The contrast IS the article material. The gap between a site's self-presentation and its filed reality is the strongest version of "no gap, no article."

Pitfall: Do not confuse website silence with wrongdoing. A missing disclosure may be strategic, negligent, or legally correct. Label the contrast as observation, not verdict.

Pitfall (Drupal cache timestamps): The `Last-Modified` and `etag` HTTP headers on a Drupal site (identified by `x-generator: Drupal 9` or `x-drupal-dynamic-cache: HIT`) reflect **cache serve time**, not content edit time. The header will say "today" for every page. To find the actual content change date: (1) check `sitemap.xml` for the `<lastmod>` tag on the specific URL — this reflects real CMS edits; (2) cross-reference Wayback Machine CDX snapshots to identify when specific elements (e.g. a person's name) appeared or disappeared from the page. Never build a timeline on HTTP headers alone — they will always say the page was modified recently regardless of actual content age.

### 4. Structure
See `templates/article-skeleton.md`. The spine is: relatable frame → the institution's own numbers, big and standalone → the questions nobody in the briefings asks → one closing question.

### 5. Close on a question, never a summary
End with a single question the reader is left holding. A conclusion tells them what to think; the question makes them the witness.

### 6. Seal footer
Articles carry the 999 seal and a source line. Two established variants:

```
DITEMPA BUKAN DIBERI ⚒️
999 ⚖️ · Civic Intelligence · MakcikGPT · <month year>
Sumber: <named list>. <audit claim>. [OBS]
Enjin melapor. Manusia yang putuskan. Yang benar dikarang, bukan diberi percuma.
```

Tag the epistemic status of load-bearing claims in the footer (`[OBS]` observed / `[DER]` derived). "Semua nombor diaudit" is a claim you must be able to defend line by line.

A published page also carries a machine-readable header above the prose: `article_id`, `canonical_url`, `seal`, `provenance_status`, `version`, `merkle_leaf`, and an `epistemic_summary` counting obs / der / int / spec, followed by a **Claim Register** (`claim_id | tag | text | source_id | maruah`) and a **Source Ledger** (`source_id | type | title | url`). These are part of the public artefact, not internal notes — a new piece needs the same fields, and each load-bearing sentence needs a row. Tags: `OBS` observed, `DER` derived, `INT` interpretation, `SPEC` speculative.

### 7. Draft in chat, then stop
Deliver the full draft in the conversation and ask **one** question about angle or tone. Do not attach an explanation of your own craft or a list of options — Arif will redirect if he wants a different shape. Nothing is published until he says so; the byline, the site, and the seal are his.

## Voice spec
- **Language:** Bahasa Malaysia, Makcik register — maternal, plain, no jargon. Technical terms are translated into kitchen language ("kedai runcit", "anak mak", "ATM") rather than glossed.
- **Makcik refers to herself in the third person** ("Makcik tanya satu je"). She is not the expert and says so — that is what licenses the reader to ask the same question.
- **Concrete over abstract.** A named office, a dated event, a specific ringgit figure beats a category.
- **The recurring move:** *who pays, who benefits, and why were we told last.*
- **No histrionics.** The tone is a relative who has noticed something, not an activist. The numbers carry the anger.

## Pitfalls
- **F6 MARUAH — charge the decisions, not the dignity.** Aim at the structure and the choices that let the outcome happen, because a named individual can be replaced and the behaviour continues. This does **not** mean never naming anyone: the corpus names individuals and their tenure plainly. The operative line is *what* is charged — appointments, capital decisions, sign-offs, the refusal to answer a question — never dignity: no family, no body, no private life, no interior motive asserted as fact. Put the editorial read in an `INT` row that states it is the author's interpretation and not an allegation; that row is what keeps a sharp piece publishable.
- **Choose the frame that leaves the subject no exit.** When Arif asks for a personal attack, keep his words and his strongest phrase — a sanitised version of his anger reads as nobody's voice — but change what the piece *accuses*. Charging incompetence hands the subject a defence, because a mistake is an accident and an accident is forgivable; charging willing compliance does not, because compliance is a choice made every morning. If his own earlier series rows already say "this is a question of context-fit, not of personal intelligence", hold that line rather than silently reversing it, tell him you held it, and offer the direct version as his call. The judgement is his; the craft is yours.
- **Verify byline and date on any supplied document before building on it.** A column handed over as "what he wrote" may be by a different author, decades old, and written about a different situation. Fetch it, read the byline and the issue date, and if they contradict the assumption, say so plainly and rebuild the piece around the real artefact. An old instrument that *praises* the institution cuts deeper than a fresh attack, because it cannot be dismissed as a critic's hostility.
- **Never invent, round, or "reasonably estimate" a number.** The piece's entire authority is sourcing. One fabricated figure converts a civic-intelligence article into a liability.
- **Do not present a structural read as a fact.** A pattern in appointment histories is an observation, not an admission. Label it.
- **Insider-sourced colour must be anonymised properly.** "Anak mak kerja dalam upstream" is the shape. Never a name, a team, or anything that narrows to one desk.
- **Don't confuse this with analysis-for-Arif.** The internal analytical lane and the public article lane are separate products with different registers and different rules. Do not paste internal claim classes into a public draft.

## Related
- `petronas-knowledge-router` — routing table for Petronas-domain substance
- `internal-first-probe` — probe order and the ground-reality rule for anything Arif's world touches
- `FORGE-agentic-web-builder` — publishing and repairing the site itself
- `references/provenance-sourcing.md` — the source-ledger checks to run before an article is registered: resolving each `url`, tagging each claim, and the byline/date trap
