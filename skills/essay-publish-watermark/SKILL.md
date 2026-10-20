---
name: essay-publish-watermark
description: Header/footer metadata conventions for /words/writing/ essays and MakcikGPT articles (Arif Fazil Doctrine — header banner removed, ARIF FAZIL footer block)
version: 1.1.0
triggers:
  - publish or revise an essay on /words/writing/
  - publish or revise a MakcikGPT article
  - reorganize header metadata in essay bodies
  - add or update the metadata suffix strip in the essay footer (999 METERAI · INT · tags · read time · sections)
  - user complains "human attention got distracted" by chips or metadata above the title
---

# Essay Header/Footer Convention (Arif Fazil Doctrine 2026-08-07)

## The Rule

**NO author-byline banner at the top of essays.** The body opens with the essay content directly. Header metadata (author, role, publication date, epistemic tag, seal) belongs at the **FOOTER**, as the last thing the reader sees.

Why: human attention and LLM extraction passes are highest at the very first and very last positions on a page. The opening should be the EYE-CATCHING title + lead. The closing should be the high-signal author identity block.

## /words/writing/ essays (Constitutional Surface)

Article body should NOT contain a `<div class="paper-header mb-12">` block (with `<div class="paper-authors">` + `<div class="paper-meta">` lines). The SPA `EssayPage.tsx` component renders a clean hero from `essay.title`, `essay.date`, `essay.tags` — those are the metadata fields. The footer block (with author identity, publication, epistemic, pairing) goes at the bottom.

Footer template (rendered by SPA EssayPage OR injected via `<!--AUTHOR-FORGED-FOOTER-->` marker in the `.ts` file's `html:` field, immediately before the closing `</article>`):

```html
<!--AUTHOR-FORGED-FOOTER-->
<hr class="my-12 border-forge-iron" />
<section class="my-12 pt-8 border-t-2 border-forge-gold bg-forge-steel/40 -mx-6 px-6">
  <div class="mb-10">
    <div class="font-mono text-[0.6rem] text-forge-gold uppercase tracking-widest mb-2">Forged by</div>
    <div class="font-display text-3xl md:text-4xl font-black italic uppercase tracking-tighter text-forge-white leading-none">ARIF FAZIL</div>
    <div class="font-mono text-sm text-forge-gold mt-1">Muhammad Arif bin Fazil</div>
  </div>
  <div class="grid md:grid-cols-3 gap-6 mb-10">
    <div>
      <div class="font-mono text-[0.65rem] text-forge-orange uppercase tracking-widest mb-2">Identity</div>
      <p class="font-mono text-sm text-forge-dim leading-relaxed">
        <strong class="text-forge-white">Muhammad Arif bin Fazil</strong><br />
        Geoscientist · Architect, arifOS<br />
        Petronas Carigali<br />
        UW–Madison '13<br />
        Penang, Malaysia
      </p>
    </div>
    <div>
      <div class="font-mono text-[0.65rem] text-forge-orange uppercase tracking-widest mb-2">Publication</div>
      <p class="font-mono text-sm text-forge-dim leading-relaxed">
        Published: {essay.date}<br />
        Direct Publication<br />
        <a href="/words/" class="text-forge-gold hover:underline">/words/</a> context<br />
        Sealed 999 · Ditempa Bukan Diberi
      </p>
    </div>
    <div>
      <div class="font-mono text-[0.65rem] text-forge-orange uppercase tracking-widest mb-2">Epistemic Stance</div>
      <p class="font-mono text-sm text-forge-dim leading-relaxed">
        Epistemic Tag: INT — {epistemic-blurb}
      </p>
    </div>
  </div>
  <!-- Optional pairs-with list per slug mapping -->
  <p><strong class="text-forge-white">Pairs with:</strong></p>
  <ul class="list-disc pl-6 mb-3">
    <li><a href="/words/writing/<companion-slug>/" class="text-forge-gold hover:text-forge-white transition-colors">{title}</a></li>
  </ul>
  <div class="mt-12 pt-6 border-t border-forge-iron/40 text-center">
    <div class="font-display text-lg font-black italic uppercase tracking-tighter text-forge-gold">Ditempa Bukan Diberi</div>
    <div class="font-mono text-[0.65rem] text-forge-dim uppercase tracking-widest mt-1">Forged, not given · ARIF FAZIL · arif-fazil.com · 2026</div>
  </div>
</section>
```

Curated pairings (only the August 2026 trilogy):
- `the-agi-paradox-why-bigger-models-wont-save-us` ↔ `truth-is-not-cheap-...` ↔ `the-third-axis-of-failure-what-acemoglu-missed`
- All other essays: empty pairing list

Per-essay epistemic blurbs (in EssayPage.tsx `EPISTEMIC_BLURB` map):
- See src/pages/EssayPage.tsx — fallback is "interpretive synthesis across AI governance, constitutional AI, and AGI risk"

## MakcikGPT articles (/world/makcikgpt/<slug>/)

Already built with:
- Hero (title + subtitle + date + tag pills + seal)
- Body: Bahasa Makcik content
- Evidence Drawer (claim register + source ledger) — auto-present if `claim_register` + `source_ledger` fields present in `.ts`
- Footer: published + epistemic tag + pairs with + site links

The `bangang` tag appears legitimately in Bahasa Makcik — do NOT replace (it's an in-essay term, not a placeholder).
The MakcikGPT articles are prerendered by `scripts/prerender-articles.cjs` (puppeteer-based) which writes to /var/www/html/arif/world/makcikgpt/<slug>/index.html.

## Common mistakes when patching essay bodies

| Mistake | Where | Fix |
|---|---|---|
| `<div class="paper-header mb-12">` block at top of `.ts` html body | /words/writing/ essays | Strip the opening div block (header + paper-authors + paper-meta); the SPA/prerender will rebuild it as a hero |
| Standalone `<p>` byline like `<p>By Arif Fazil</p>` | /words/writing/ essays | Strip (regex `<p[^>]*font-mono[^>]*>[\s\S]{0,200}?by Arif Fazil[\s\S]{0,200}?</p>`) |
| `<p>MUHAMMAD ARIF BIN FAZIL · PENANG · 2026 · 999 SEAL</p>` | /words/writing/ essays | Strip |
| `<!-- in-body byline removed — byline lives in the page footer -->` leftover | All essays | Clean up dead comments |
| `"bangang"` used in English prose essays | English body text (e.g. "Why Institutions Become Stupid") | Use `stupid` — Arif correction 2026-08-07: "BANGANG and stupid is different meaning" |
| `"Muhammad Arif bin Fazil"` used as top-line brand (masthead, nav, hero) | Top-level brand surface | Use `ARIF FAZIL` (uppercase) — full legal name only in the identity footer block |

## User preference: ARIF FAZIL brand (Arif correction 2026-08-07)

Arif explicitly said: *"I prefer. ARIF FAZIL"* — the brand on all pages is **ARIF FAZIL** (uppercase, as the masthead wordmark, nav logo, and footer anchor). The full legal name "Muhammad Arif bin Fazil" appears ONLY inside the identity footer block (the 3-column "Forged by" section at the bottom). Never in body headers, nav links, or the hero.

## User preference: "bangang" vs "stupid" (Arif correction 2026-08-07)

Arif corrected: *"I mean change on the site. BANGANG and stupid is different meaning"*

The rule:
- **English prose essays** (all `/words/writing/` essays): use **`stupid`** (standard English). "Bangang" is Bahasa Malay slang and does not belong in English body text. Earlier sibling-agent runs had silently substituted "bangang" into English prose ("Why Institutions Become Bangang") — strip and restore "stupid".
- **Bahasa Makcik essays** (`/world/makcikgpt/`): **`bangang` is correct** — it is the author's intentional voice (BM civic journalism). Do NOT replace with "stupid" in MakcikGPT body text or tag names. Some MakcikGPT slugs legitimately contain "bangang" (e.g. `chennah-bangang`, `dap-8-tahun-bangang`) — those are author-named and stay.

## How to clean a new essay safely

1. Read the current state of the `.ts` file from `src/data/essays/NN-<slug>.ts`.
2. Identify the body block: `<article> ... <!-- Title Block --> <div class="paper-header mb-12"> ... </div> ... </article>`.
3. Use depth-tracked div nesting to find the matching `</div>` of the paper-header.
4. Replace the div with empty string (just keep `<article> ... -->` and the `<hr/>` or first `<h2>` that follows).
5. Inject the FORGED footer template immediately before `</article>``,\n};` close.
6. Sanity-check: `grep -c "paper-header" file.ts` should be 0; `grep -c "AUTHOR-FORGED-FOOTER" file.ts` should be 1.

## Hero chrome discipline — keep payload, strip chips (Arif 2026-08-07)

**Arif's exact feedback (verbatim):** *"999 METERAI · INT · ~5 MIN READ · 13 SECTIONS · #ai-governance · #agi · #arifos · #capability-token · #naming · #evolution-of-agents · #authority · #truth-provenance — Published: 7 August 2026 · Direct Publication · /words/ context · Epistemic Tag: INT — interpretive synthesis across AI governance, constitutional AI, and AGI risk · Pair: S4 / n=4 · Governance Canon — Please Make all Pages more Clarity by putting this subfix?? To footer. Human attention Got Distracted Looking at this."*

**Rule (binding for all `/words/writing/` essays):**

| Surface | Hero keeps | Hero removes | Footer (or below-fold) gets |
|---|---|---|---|
| Title | yes | — | — |
| Subtitle / lead | yes | — | — |
| Date | yes (via time element in breadcrumb) | — | — |
| **999 METERAI** | yes (functional authority marker) | — | — |
| **Epistemic chip (INT/OBS/DER/UNK)** | yes (epistemic tag is the floor signal) | — | — |
| Tag chips (`#ai-governance` etc.) | — | yes — strip from hero | move to footer |
| `~X MIN READ` | — | yes — strip from hero | move to footer |
| `N SECTIONS` | — | yes — strip from hero | move to footer |
| Published line (long form) | — | yes — strip from hero | move to footer (already there in identity block) |
| Pair / series chip | — | yes — strip from hero | move to footer |
| Author identity | — | yes | full 3-column "Forged by" footer |

**Why:** human + LLM peak attention is the opening. Decorative chips compete with the essay thesis for that anchor. Strip them so the title and lead win the hero.

**Implementation (two paths depending on render surface):**

1. **SPA-rendered essays** (`/words/writing/<slug>/` via `EssayPage.tsx`) — update the hero block in `src/pages/EssayPage.tsx` to keep only the date + 999 METERAI + epistemic chip; move tags/min-read/sections below into the footer chrome strip. Currently the `<div className="flex flex-wrap items-center gap-3 font-mono text-xs mb-8">` block in EssayPage.tsx renders the metadata strip; remove the per-chip spans and leave only `{date} · 999 METERAI · {epistemic}`.

2. **Static-shell essays** (under `dist/words/writing/<slug>/index.html` after build) — drop the chip block entirely from the rendered HTML; the body opens directly with the `<h1>`.

**Footer suffix template (binding):**
```html
<div class="essay-meta-strip mt-8 pt-6 border-t border-forge-iron/40">
  <div class="flex flex-wrap gap-2 mb-3 items-center">
    <span class="…METERAI…">999 METERAI</span>
    <span class="…epistemic…">{INT|OBS|DER|UNK|SPEC}</span>
    <span class="…read…">~{N} MIN READ</span>
    <span class="…sections…">{N} SECTIONS</span>
  </div>
  <div class="flex flex-wrap gap-x-3 gap-y-1 mb-4 font-mono text-[0.7rem] text-forge-gold">
    {#tag-1}  {#tag-2}  {#tag-3}  …
  </div>
  <div class="font-mono text-xs text-forge-dim leading-relaxed mb-2">
    Published: {date} · Direct Publication · <a href="/words/">/words/</a> context
  </div>
  <div class="font-mono text-xs text-forge-dim leading-relaxed mb-2">
    Epistemic Tag: {INT|OBS|DER} — {blurb}
  </div>
  {f'<div class="…pair…">Pair: {series}</div>' if series else ''}
</div>
```

**Read-time calculation:** words / 250 wpm, rounded to nearest minute, minimum 3 (Arif's essays never read faster than 3 min).

**Section count:** `<h2>` and `<h3>` tags inside the body html. Essay 27 has 13 H2s → "13 SECTIONS".

**Common mistake:** rendering the suffix strip in BOTH hero and footer (creates duplicate chip row). Pick one — footer only.

### Duplicate-detection trap — probe existing `.ts` files before creating new (2026-08-07)

When Arif asks to publish a new essay, **first probe whether the slug or body already exists under any NN prefix**:

```bash
ls src/data/essays/ | grep -iE "i-didnt-invent|your-topic-keywords"
grep -l "title.*<the new essay title>" src/data/essays/*.ts
grep "<the new slug>" src/data/essays/articles.json
```

If a file exists with the same essay body (or close to it), a sibling agent may have already shipped it during an earlier session. Adding a new file at `NN-<different-slug>.ts` creates a **duplicate** that:

1. Breaks the dedup-by-filename-length rule (shorter filename wins → sibling's version displaces yours at listing).
2. Shows TWO essay cards on `/words/writing/` listing if dedup misses either.
3. Wastes an import line in `src/data/essays/index.ts` and burns a slot in the canonical numbering.

**Verified pattern (2026-08-07):** Arif pasted essay 27 ("I'm Not a Programmer") asking to publish under `/words/writing/i-am-not-a-programmer-i-accidentally-invented-a-new-question-for-ai/`. Probe found `27-i-didnt-invent-a-token-i-invented-a-question.ts` already exists with the SAME title and body (sibling-shipped earlier). New file deleted; existing file's body upgraded to the AUTHOR-FORGED-FOOTER block; meta entries added to `index.ts`, `articles.json`, and `EssayPage.tsx` `EPISTEMIC_BLURB`. Single commit, no duplicate.

**Number-collision rules:**
- If a sibling file exists at `27-<topic>.ts` and you want to publish under essay 28: don't conflict — rename your file to `28-<unique-topic>.ts` with a distinct slug, OR upgrade the existing 27 in-place.
- `wc -l src/data/essays/2?-*.ts` reveals the existing 28+ entries before you commit a new essay number.
- `git ls-files src/data/essays/` on the canonical branch is the canonical "what's already published" view — but local may be ahead of remote; check `git fetch --all` first.

## Internal Vocabulary Discipline at the Human Boundary (Arif correction 2026-08-13)

**Arif's exact feedback (verbatim):** *"WITNESS REQUIRED implies attestation... a witness document without witness material."* And: *"Internal governance vocabulary mesti ditranslate di boundary. Kalau tidak, reader nampak bahasa yang bukan untuk mereka — dan artifact lose kreadibiliti."*

**The rule:** When generating any public-facing artifact (essays, PPT, PDF, web pages), **never** use internal arifOS/governance vocabulary unless translated for human readers. Terms like `WITNESS REQUIRED`, `888_HOLD`, `SEAL`, `F1–F13`, `VAULT999` are internal agent vocabulary. They mean something inside the federation but mean nothing (or imply false authority) to external readers.

| Internal Term | Public Translation | Risk if leaked |
|---|---|---|
| `WITNESS REQUIRED` | `NOT EVERYTHING SHOULD BE CLOSED` | Reader sees authority claim without basis |
| `888_HOLD` | `PENDING REVIEW` | Reader cannot decode |
| `SEAL` | `Published` or `Attested` | Reader assumes legal seal |
| `F1–F13` | Remove entirely | Meaningless noise |
| `VAULT999` | Remove entirely | Meaningless noise |

**Iron rule:** Every artifact that crosses the agent→human boundary must pass: *"If a stranger reads only this artifact, does every word mean what it appears to mean?"* If any term is opaque or implies authority the artifact doesn't carry → replace or remove.

**The scar:** Forged from "The Cost of a Forgotten Well" PPT/PDF (2026-08-13). Footer originally read `WITNESS REQUIRED` — an arifOS internal sigil. Arif caught it: first-time reader sees an authority claim without attestation material. Fixed to `NOT EVERYTHING SHOULD BE CLOSED`.

**Recovery from a duplicate you accidentally committed:**
```bash
# 1. Delete your file
rm src/data/essays/28-<your-slug>.ts
# 2. Remove its import + meta entry from index.ts (or edit the existing 27's meta in place)
# 3. Remove its entry from articles.json
# 4. Re-build to confirm listing shows ONE entry, not two
npm run build
```

<!-- SKILL-WITNESS-NOTE (auto, additive-only) -->
Witnessed reality moved this skill's selection to **ROUTE or MERGE**.
Scar signatures: 2026-09-07-w3-degradation-during-doctrine-writing
Do not treat this skill as neutral until the signatures are resolved.
<!-- /SKILL-WITNESS-NOTE -->
