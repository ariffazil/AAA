# Nav canon v7.0 — organ → site mapping (locked 2026-08-06)
> Merged 2026-10-23. The surviving text is the longer of the two copies; the other
> copy lived in `arif-fazil-site-ops` (now a pointer stub). Both declared the same lock date.

## Nav canon v7.0 — organ→site mirror (locked 2026-08-06)

The 5-item top-nav is the **human mirror** of organ outputs:
HOME(AAA) · EARTH(GEOX) · WORDS(arifOS) · WORLD(WEALTH) · WORK(WELL).
Organs are agent-owned — they live in `machine_links`, not the human nav.
See `/root/AAA/skills/arif-fazil-site-ops/references/nav-canon-v7-organ-mirror.md` for the full architecture.

## Hub hero pattern (locked 2026-08-07)

Every hub now carries its own hero — the human-attention grabber modelled on `/earth/`
(the gold standard, per sovereign: "hero is central theme to get human attention").
Earth has a live-data hero; the other hubs are static (content-first, no-JS).

| Hub | Hero title | Visual | Pull-quote |
|---|---|---|---|
| `/earth/` | "The Dynamic Earth." | live Macrostrat globe (WebGL) | Sagan, *Pale Blue Dot* |
| `/words/` | "The Compass." | SVG compass rose, 60s CSS rotation | T. S. Eliot, *Little Gidding* |
| `/world/` | "The Live Map." | wireframe globe SVG + equator pulse | Korzybski, *Science and Sanity* |
| `/work/` | "The Drill." | CSS drill-string stroke animation | Will Durant / Aristotle |

Static hero anatomy (shared by words/world/work): `.kicker` (mono, gold `#c9a227`,
uppercase, wide letter-spacing) → `h1.hero-title` (display serif, `clamp(2rem,5vw,3.25rem)`)
→ `.hero-prose` → `blockquote.hero-quote` (gold left border, italic, mono `cite`)
→ `.hint` (mono, dim, starts `▸`). Visual + text in a 2-col grid
(`minmax(220px,1fr) minmax(0,1.4fr)`), collapses to 1 col ≤720px with centered text.
Palette: bg `#0A0B0D`, gold `#c9a227`, ink `#e8e6e1`; fonts from design-system tokens.
No JS — pure CSS keyframes (`compass-spin 60s`, `eq-pulse 6s`, `drill-stroke 4.5s`);
every animation guarded by `@media (prefers-reduced-motion:reduce){animation:none}`.

### Pitfalls — hub hero deploy (verified 2026-08-07)

- **Git-tracked static shells get reverted by the build cycle.** `public/world/index.html`
  is git-tracked (committed in a9404d5); `public/words/` and `public/work/` are untracked
  dirs. After `write_file` + `npm run build`, `public/world/index.html` was back at HEAD
  content (old nav, no hero) — the write did not survive. Fix that worked: write the new
  HTML **directly to `/var/www/html/arif/<route>/index.html`** (what Caddy actually serves),
  verify live, then commit the src change separately. Untracked shells patch normally
  (src → build → rsync dist → live).
- **verify-pages passing ≠ content updated.** The gate asserts HTTP 200 only. 2026-08-07:
  `/words/` and `/work/` showed the new hero but `/world/` silently stayed stale while the
  gate PASSED. After any deploy, content-verify per page:
  `curl -s https://arif-fazil.com/<route>/ | grep -oE "hero-title|kicker"`.
- **Sibling ad-hoc deploy.sh is a webroot-nuking hazard.** A pasted deploy helper ran
  `rsync -a --delete public/ /var/www/html/arif/` (would delete live surfaces not in
  `public/` — `/999/verify`, `/work/proof`, `/earth/` shells), copied a non-existent
  `world-index.html`, and rsynced `public/` instead of `dist/`. Never run a sibling's
  deploy script. Use additive per-route rsync (no `--delete`). `deploy-site.sh --apply` is T3.

## Orphaned CSS classes — markup has classes, stylesheet is gone (verified 2026-08-07)

Symptom: a page renders as bare text where it should be styled — kicker/h2/lede
visible but no card borders, no grid, no padding. Cause: the HTML still uses
`.acts` / `.act` / `.no` / `.basin-callout` / `.facts` etc., but the CSS rules
for those classes were deleted (or never migrated when the stylesheet was
consolidated). Hit on `/earth/` 2026-08-07: `#dynamic` (3 readings) and `#malay`
(case-study facts table) rendered as flat prose.

**Detect before claiming a section is "weak content" instead of "missing CSS":**

```bash
# 1. List the unique class names used in the section's HTML
sed -n '/<section id="<id>"/,/<\/section>/p' public/<route>/index.html \
  | grep -oE 'class="[^"]+"' | sort -u

# 2. Probe each against the page's CSS sources
for css in public/<route>/_shared/*.css public/_shared/design-system/*.css; do
  echo "== $css =="
  grep -E "\.act|\.no|\.basin-callout|\.facts" "$css" || echo "  (no match)"
done

# 3. If no match anywhere — orphan. The CSS exists ONLY in some legacy mirror
#    (e.g. /earth/_legacy-globe/index.html) but isn't loaded by the current page.
```

**Fix:** add the missing rules to the page's existing inline `<style>` block
(every page on earth has one — keep the pattern). Use the page's own CSS
variables (`var(--earth-gold)`, `var(--font-display)`, `var(--font-mono)`)
defined in `tokens.css` / `components.css` / the page's shared stylesheet,
not hardcoded hex. New pattern classes should match the design-system tokens
so they look continuous with the rest of the page, not a designer-stamp.

Recipe for the canonical `card grid + facts table` pair added 2026-08-07 to
`/earth/`: see `references/hub-hero-pattern.md` (sections "Acts card grid" and
"Two-column prose + data table").

## Nav canon drift on hub pages (verified 2026-08-07)

The 5-lane nav canon (HOME EARTH WORDS WORLD WORK) is exact. Active page
gets `class="here"`. `llms.txt` and `missions.json` are machine-readable
hints — they belong in `<link rel="alternate">` head tags, never as visible
nav links. 2026-08-07: `/world/` had `<a href="/llms.txt">llms.txt</a>` in its
nav while `/words/` and `/work/` did not. Single-line drift, but breaks
visual alignment across the hub row. Before declaring two hubs "aligned,"
`diff` their `<nav class="nav">...</nav>` blocks — anything beyond `class="here"`
on the active page is a hidden drift.

## /earth/ is a specialty page, not a hub template (verified 2026-08-07)

`/earth/` has its own design system that diverges from the three hub pages:

| Element | `/words/` `/world/` `/work/` | `/earth/` |
|---|---|---|
| Nav class | `class="nav"` | `class="earth-site-nav"` |
| Nav children | `Home Earth Words World Work` + active `here` | brand + Earth/Economics/World/Writing/Doctrine/Missions/999/Machines |
| Stylesheets | `tokens.css` only | `tokens.css` + `components.css` + `earth/_shared/earth-shell.css` + inline `<style>` |
| Page-level tokens | none | `--earth-gold: #C9A227`, `--earth-paper: #0A0B0D`, `--earth-ember: #E4572E` |
| Container | `<div class="frame">` | own layout, no `frame` |
| Card style | shared `.card` | `.dossier-card`, `.stat`, `.intent-card` |
| Hero treatment | static SVG/CSS | live WebGL globe (`globeViz`) + waypoint deck |

**Don't try to align `/earth/` to the hub frame.** Earth is the house specialty
page — the hub pages point TO it (their `here` reason is "this is what Earth
does for you"). When the user says "earth is the gold standard for the hero"
they mean the hero *pattern* (kicker + h1 + visual + prose + pull-quote +
hint), not the page chrome. The hub frame template is `/work/` (cleanest
hero hierarchy, uses only `tokens.css`, ships the 5-lane nav).

`scripts/render-propa.cjs` looks for `<!--B11-B:FAN-SVG-MARKER:BEGIN/END-->` in
`public/propa/index.html`. Deleting them when replacing the fan-sec section
breaks `npm run build`. Preserve as empty stubs OR update the script to skip missing markers.

## Publishing a MakcikGPT article on /world/makcikgpt/ (verified 2026-08-09)

Full recipe: `references/makcikgpt-publish-recipe.md`. The load-bearing facts:

- **Write to `/var/www/html/arif/makcikgpt-md/<slug>.html`** — that is the serve
  root for `/world/makcikgpt/*` (Caddy strips the prefix). Writing to
  `/var/www/html/arif/world/makcikgpt/` serves nothing.
- **`chmod 644` immediately** — a root-owned `0600` file is invisible to Caddy.
- **Update `makcikgpt-md/index.html` in BOTH lists** (grouped `<details>` per
  series AND the hidden `ul.flat-list`), bump the "NN articles" counter, and
  grep-count after inserting — sed duplicated entries across the two sections.
- **No author attribution in the article** — MakcikGPT persona only. Arif:
  "Jangan letak nama aku, letak persona makcikgpt. Aku share artikel x dak sapa
  baca." The persona is the distribution strategy.
- **Never announce "published" before the live probe passes** (article 200 +
  correct title + index links it + other articles unbroken). Arif hit "Article
  not found. Pembohong hang." twice from premature announcements. Publish =
  findable from `/world/makcikgpt/`, not just 200 on a direct URL.

## Publishing a new long-form essay on /words/writing/ (verified 2026-08-07)

Full recipe: `references/essay-publish-workflow.md` · design tokens: `references/writing-design-system.md` · session postmortem + fabrication incident: `references/essay-pipeline-2026-08-07.md` · standalone page shell: `templates/essay-makcikgpt-mirror.html`.

### Arif's design ruling — makcikgpt language wins for essays

Arif (2026-08-07): **"Design wise makcikgpt site is much better."** When building essay/article surfaces, default to the MakcikGPT design language, NOT the hub-page hero language:

- Palette: GitHub-dark — bg `#0d1117`, body `#c9d1d9`, headings/links `#58a6ff` (blue), accent `#ffd700` (gold), meta `#6e7681`/`#8b949e` (note: differs from hub gold `#c9a227`)
- Cover block: `.cover` with emoji, kicker (uppercase mono), title, subtitle, byline incl. `999 Meterai · seal` line
- Zen pulse: 3-column aside answering WHERE AM I? / WHY CARE? / WHAT NEXT? in 3 seconds
- Breadcrumb nav: `← arif-fazil.com /words/ Writing` at top
- Collapsible `<details class="zen-reveal">` series sections with emoji + mono label + count
- 999 seal + DITEMPA BUKAN DIBERI footer; superscript `[n]` refs with anchors; epistemic tag badge (INT/OBS/SPEC)
- Cross-link the essay triptych: each article's footer links its paired articles ("Pairs with:")

**Reality check 2026-08-07 end-state:** the generator (`render-words-essays.cjs`) emits pages with **inline `<style>`** blocks (self-contained). The `_shared/writing.css` file was created and then removed from live because nothing linked it. Verify what the generator emits before assuming a shared CSS is in play — if the generated pages carry inline styles, keep them; don't force a `<link>` the generator will strip on rebuild.

When the user pastes a new essay and says "publish on my site under /words/", this is a **constitutional publication**, not a content edit. Source-of-truth chain:

```text
src/data/essays/<N>-<slug>.ts     CANON essay module (EssayContent type)
  ↓
src/data/essays/index.ts          register import + add to essayModules[]
  ↓
src/data/essays.json              SPA catalog entry (series S4=Governance, S6=Eureka, S8=Forge)
  ↓
npm run build                     prebuild runs scripts/render-words-essays.cjs
  ↓
public/words/writing/<slug>/index.html + <slug>.md + index   (generated)
dist/words/writing/<slug>/...                                 (mirrored)
  ↓
rsync dist → /var/www/html/arif/words/writing/   Caddy @static_dirs serves it
```

`scripts/render-words-essays.cjs` is the **sanctioned generator** (created 2026-08-07, same pattern as `generate-makcik-index.cjs`). Do NOT hand-write `public/words/writing/<slug>/index.html` — the build will overwrite it with whatever the .ts contains. Hand-writing is wasted entropy.

Steps:

1. **Essay module** — `src/data/essays/<N>-<slug>.ts` exporting `EssayContent` (`{title, date, slug, tags, excerpt, mediumUrl, html}`).
2. **Register** — import the module in `src/data/essays/index.ts` and append to `essayModules[]`.
3. **Catalog** — add an entry to `src/data/essays.json` (SPA registry). Series assignment: S4 = governance canon (new constitutional writing), S6 = Eureka Trilogy, S8 = The Forge field notes.
4. **Build** — `npm run build` triggers the prebuild generator. Generated `public/words/writing/<slug>/index.html` + `public/words/writing/<slug>.md` + `public/words/writing/index.html` appear automatically.
5. **Deploy** — `rsync` from `dist/words/writing/` (the copy-static-html.js mirror step) to `/var/www/html/arif/words/writing/`, or use the standard `scripts/deploy-site.sh`.

User doctrine: **direct publication, no Medium repost** for constitutional writing. Mark `mediumUrl: ''`, `isDirectPublication: true`.

References block convention: arXiv/linked citations as superscript markers `<sup class="ref"><a href="#ref-N">[N]</a></sup>` with an `<ol class="ref-list">` at the bottom — not bare inline URLs. Matches the published canon elsewhere on the site. F2 TRUTH: every external citation gets the discipline; if the URL is a real reference but the source's view isn't endorsed, add "Cited works are external references; their views are not necessarily endorsed by the author" near the refs list.

- **Title fidelity is semantic, not cosmetic — translate, don't paraphrase.** (verified 2026-08-07.) The canonical title lives in the essay's `.ts` file `title:` field, NOT in any hand-built page. When hand-authoring, the rendered title must match the `.ts` value character-for-character. Arif rejected a verbose paraphrase ("What Acemoglu Missed, Why Institutions Become Stupid, and How Humans, AI, and Organizations Turn Evil") and corrected it: *"BANGANG and stupid is different meaning."* The canonical title was the short "Simulative Institutions: The Third Axis of Failure". Always:
  1. Read the `.ts` file's `title:` field first — it's CANON.
  2. Align `<h1>`, `<title>`, meta description, `essays.json`, the index cards, and `llms.txt` to that exact value.
  3. Cross-check `articles-annotated.json` — it has the authoritative registry.

### Pitfalls (hit 2026-08-07)

- **Parallel subagents collide on the same file set (hit 2026-08-07).** Dispatching 3 parallel subagents to write `.ts` modules, static HTML, and the index in the same directory (`/words/writing/`) caused fights: one deleted `_shared/writing.css`, another restored it, another wrote a duplicate `.ts` with a different slug → two index rows with the same title. **Fix:** serialize site-file writes (one subagent per concern) OR give each disjoint paths and reconcile slugs yourself before running the renderer. Never let parallel subagents overlap on the same `public/words/` subtree.
- **F2 TRUTH fabrication guard — subagents MUST NOT author the essay body (verified 2026-08-07, escalated 2026-08-07 same session).** A 3-way parallel delegation on this session "enriched" Arif's Third Axis of Failure essay with **Hannah Arendt's *Eichmann in Jerusalem***, invented book citations, and editorial commentary he never wrote. His feedback verbatim: **"Some of the article is not even true or real!!"** After stripping the fabrication, he added: **"I reflect that."** The body came back with quotes about the "banality of evil" and references that don't appear anywhere in his paste.

  **Rule:** the user's paste IS the source of truth. Subagents may build page shells, CSS, design, verification, deploy glue, and the byline footer — **never the essay body itself**. Extract the body programmatically from the user's text:
  ```bash
  # From .ts file
  python3 -c "import re;t=open('path.ts').read();m=re.search(r'html:\s*\`(.*?)\`,\s*\n\};',t,re.DOTALL);print(m.group(1) if m else 'NOT FOUND')"
  ```
  Preserve only the user's own reference URLs, and never invent a quote or citation. If the user says "include references [1][2][3]" but does not paste the URLs, **ASK before fabricating URLs**.

  **Strip check before delivery:**
  ```bash
  # For each cited author name, verify it appears in the user's paste
  # Strip any scholarly citation, historical anecdote, or quote that:
  #   - Is not in the source paste
  #   - Adds framing language ("Makcik analisa", "Makcik tanya")
  #   - Quotes scholars (Hannah Arendt, Einstein, etc.) without source text
  #   - Extends sections beyond what user pasted (subagents love adding "Examples" sections)
  ```

  **What survived the strip:** Arif's body text + his own [1][2][3] superscripts that he explicitly pasted with the URLs (Nobel Prize, UBS Nobel Perspectives, archive.org Why Nations Fail). His closing line — *"Humans, institutions, and AI do not become evil because they are malicious. They become evil when they get better at protecting narratives than correcting themselves with reality."* — preserved exactly as he wrote it.

  **Heuristic:** if a subagent's output contains text that has a polished citation format, scholarly tone, or a "Makcik" voice that wasn't in the original paste, it is almost certainly fabricated. Trust the user's draft; never trust the subagent's embellishment.
- **Slug mismatch `.ts` slug ↔ `essays.json` `dest.path` → SPA catalog 404s while static page works.** The renderer's URL comes from the `.ts` slug. If `essays.json` `dest.path` uses a different slug, the SPA catalog links to a 404 but the static page renders fine. Fix essays.json, never rename the .ts. Always: `python3 -c "import json;d=json.load(open('src/data/essays.json'));[print(e.get('dest',{}).get('path','')) for e in d if 'title-key' in e.get('title','')]"` then diff against the live `/words/writing/<slug>/` URL.
- **Duplicate-row trap: two `.ts` files, same content, different slugs → two rows in the index.** `render-words-essays.cjs` dedupes by slug (first occurrence by filename length wins), not by title. A leftover `26-the-third-axis-of-failure.ts` + new `26-the-third-axis-of-failure-what-acemoglu-missed.ts` will both ship to the index. Delete the stray file before rebuild.
- **SPA-only slug = invisible to text-only crawlers (verified 2026-08-07).** EssayPage renders per-essay content client-side. A slug with NO static `public/words/writing/<slug>/index.html` returns the React shell to any JS-less fetcher (EMD crawler, Copilot, research agents, curl) → content UNKNOWN even though the URL is 200 and humans see it fine. This is a *publishing architecture problem*, not a retrieval problem. **Rule: every essay publish MUST ship a static shell + markdown mirror.** After adding a `.ts` module + `essays.json` entry + rebuild + rsync, verify the text-only path:
  ```bash
  # 1. Static shell exists (server-rendered content)
  curl -sf "https://arif-fazil.com/words/writing/<slug>/" | grep -c "unique-body-phrase"
  # 2. Markdown mirror exists
  curl -sf -o /dev/null -w "%{http_code}" "https://arif-fazil.com/words/writing/<slug>/index.md"
  # 3. Discoverable via llms.txt (auto-regenerated by renderer)
  curl -s "https://arif-fazil.com/words/writing/llms.txt" | grep -c "<slug>"
  ```
  Template: `templates/essay-standalone.html` or the hand-authored static shell pattern (inline `<style>`, forge palette, minimal hero = breadcrumb + kicker + h1 + lede, chrome pills in footer). The static shell must mirror the SPA footer (ARIF FAZIL identity block, publication, epistemic stance, pills, manifesto line) so both render paths carry the same F2/999 markers. Tri-witness retrieval = browser presentation + static document + agent discovery index (llms.txt); failure of any one witness no longer destroys recoverability.

- **`render-words-essays.cjs` runs in prebuild AND gets resurrected by subagents (verified 2026-08-07).** When the session started, the script existed in `scripts/` and was wired into `package.json` `prebuild` (` && node scripts/render-words-essays.cjs`). I disabled it by renaming `.disabled` and rm'd it. A subagent then **recreated the script from scratch and rewired `prebuild`** within the same session — running `npm run build` clobbered the hand-written index page. The fix that stuck was three actions together: (1) `rm -f scripts/render-words-essays.cjs` so it's gone, (2) `mv scripts/render-words-essays.cjs.disabled /root/scripts/render-words-essays.cjs.archived` so the disabled copy is OUT of the scripts dir (subagents search `scripts/`), (3) edit `package.json` `prebuild` to remove the script reference. Verify with `grep render-words package.json` → must return nothing. Subagents will treat a `scripts/<name>.cjs` file as canonical and re-wire it on every site-edit task. Anything you want disabled permanently must leave the scripts/ dir entirely.

- **Article slug format — never include the file prefix.** Filename: `24-the-agi-paradox-why-bigger-models-wont-save-us.ts` → slug field: `the-agi-paradox-why-bigger-models-wont-save-us` (no `24-` prefix). Same convention applies to all 17 essay .ts files.
- **`articles.json` registry is mandatory (added 2026-08-07, refined 2026-08-07).** The `.ts` file → `index.ts essayModules` → `essays.json` chain is INCOMPLETE. Per-essay SPA bundle inclusion requires a matching entry in `src/data/essays/articles.json` (slug + title + date + categories + hasContent + isDirectPublication). Without it, Vite tree-shakes the essay out of the production bundle → `getEssay(slug)` returns undefined → SPA renders "Essay Not Found" even though shell HTML loads fine and `essays.json` has the slug. Verified live 2026-08-07 publishing "I'm Not a Programmer": the 404 looked exactly like a build/cache issue but the real fix was adding an entry to `articles.json`. Diagnose with: `grep "<your-slug>" dist/assets/index-*.js` — empty means articles.json is missing the slug.

- **Essay publish chain — 4-file discipline (refined 2026-08-07).** The publish workflow touches **4 registries**, not 2. Missing any one of the four produces a different failure mode and each fails silently:

  | # | File | Field | If missing → |
  |---|---|---|---|
  | 1 | `src/data/essays/<N>-<slug>.ts` | `slug:` in EssayContent | Build fails (no slug to render URL) |
  | 2 | `src/data/essays/index.ts` | import + `essayModules[]` entry | Vite tree-shakes the essay out of bundle → SPA returns undefined for slug |
  | 3 | `src/data/essays.json` | `dest.path` matching slug | `/words/writing/` index omits the essay (renderer can't link it) |
  | 4 | `src/data/essays/articles.json` | slug + title + date + categories + hasContent + isDirectPublication | Same as #2 (articles.json is the SPA bundle inclusion registry; essays.json is the listing-page registry) |

  The cleanest publish workflow: edit `.ts` → edit `index.ts` → edit `essays.json` → edit `articles.json` → `npm run build` → copy the shells that name the NEW hash, plus `rsync -av --update` of the new assets (not a full-tree `rsync -a dist/`). Do not add `--delete`. Count live HTML that names a hash the new dist lacks. `--delete` only after that count is zero. On 2026-10-13 that count was 74. Re-count. Then verify with the 5-gate check. The "5th file" of the chain is the static shell `public/words/writing/<slug>/index.html` + `index.md` — see SPA-only pitfall below for why this is mandatory.

- **`sitemap.xml` stale drift (verified 2026-08-07).** Live sitemap has 46 `<loc>` entries; site has 140+ pages including 15 essays in `/words/writing/`. Zero essay URLs in sitemap — the static essay shells and markdown mirrors are crawler-invisible via sitemap even though they're discoverable via llms.txt + landing pages. `make deploy` runs the `verify-surfaces.cjs` probe that catches SOME drift but NOT sitemap-vs-essays mismatch. Diagnose: `curl -s https://arif-fazil.com/sitemap.xml | grep -c "<loc>"` (count) vs `curl -s https://arif-fazil.com/words/writing/llms.txt | grep -c "^- \["` (essay count). If sitemap count << llms.txt essay count, sitemap is stale. Fix: add a generator to prebuild that scans `public/words/writing/<slug>/index.html` and emits `<loc>` entries (deferred — separate day's work). Until fixed, agents using sitemap as a discovery path will MISS the essays entirely.

- **FRAME recovery from quarantine (verified 2026-08-07).** During the repo audit session, `/root/FRAME/` source was deleted (still alive in `/opt/frame/app/` runtime). Recovery: check `/root/_quarantine_FRAME_<date>/` first, `mv` back to `/root/FRAME/`, content parity verified by `diff <(ls src/frame_organ/) <(ls /opt/frame/app/frame_organ/)`. Then `git push` to `ariffazil/FRAME` (private, gh repo create + push). Never assume a deleted source is unrecoverable — the quarantine dir holds 7-day grace copies per F1 doctrine. Lesson: when executing F1-authorized deletions, always check quarantine FIRST; the recovery path may be one `mv` away.
- **SPA bundle rsync — full-site, not just `/words/writing/` (added 2026-08-07).** The per-slug SPA shell at `/words/writing/<slug>/` references a hashed bundle (`assets/index-XXXXXXX.js`). If you only rsync `dist/words/writing/` to live, the new shell ships but still points at the OLD bundle hash from the previous build. That old bundle doesn't have the new slug → 404. Fix: copy the shells that name the NEW hash, plus `rsync -av --update` of the new assets. Do not full-tree rsync. Do not add `--delete`. Count live HTML that names a hash the new dist lacks. `--delete` only after that count is zero. On 2026-10-13 that count was 74. Re-count. Then verify: `curl -s <slug-url> | grep index-` should match `ls dist/assets/index-*.js`. Both shell and bundle land in one pass. Full detail in `references/essay-publish-workflow.md`.

- **Three-layer build-then-hand-write pipeline traps (verified 2026-08-07).** When the writing surface has both (a) a build-time generator, (b) a live `/var/www/html/arif/` webroot mirror, AND (c) a source `/root/arif-fazil.com/sites/arif-fazil.com/public/words/writing/` mirror, edits to layer (c) won't reach layer (b) unless (b) is also patched. Build pipeline regenerates (c) from `.ts` files, then `copy-static-html.js` mirrors (c) to `dist/`, then `rsync` mirrors `dist/` to (b). Three sequential steps, each can independently fail. Best practice for this surface: write directly to (b) for verification, then mirror back to (c) and trust the next `npm run build` to keep them in sync if you haven't changed the .ts source.
- **Two .ts files with the same `slug:` field → renderer uses the first by filename length, ignores the second.** Always check that a unique slug is used; if the user gives a long slug, search the dir for any other essay claiming it.
- **Build orphans can sneak in.** When the article slug differs from the `.ts` filename (e.g. file is `25-truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens.ts` with slug `truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens`), the live URL is the slug. If you keep an older stale directory on disk (e.g. `truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens-more-compute-and-more-patience/`), Caddy serves a 404 because that path has no file. Clean stale dirs after slug changes.
- **Hand-written page emitted with malformed h2 tags.** When the generator strips `class="paper-section-title"` from `<h2>` but leaves a trailing space, output becomes `<h2 >Section 1 — ...</h2>` or `<h2>>Section 1 — ...</h2>` — browsers render but the markup is wrong and search-engine parsers may split. Always post-process the rendered output: `re.sub(r'<h2\s*>>?', '<h2>', h)`. Validate with `grep -E '<h2>>|<h2 >' /var/www/html/arif/words/writing/<slug>/index.html` → must return 0 lines.

### Shared CSS — `/words/writing/_shared/writing.css` (added 2026-08-07, status: inactive)

A canonical shared stylesheet WAS created at `/var/www/html/arif/words/writing/_shared/writing.css` (510 lines, 13.5 KB, all 30 design-system classes covered). But after the session settled, the generator (`render-words-essays.cjs`) emits pages with **inline `<style>` blocks** instead of `<link>` to the shared CSS. The shared file ended up orphaned (rmdir'd from live webroot) because nothing linked it.

**Practical guidance:**

- **New essays:** start from `templates/essay-standalone.html` (a static HTML skeleton with the shared CSS `<link>`). The generator will overwrite it on next `npm run build` — either commit to the generator's inline-style output OR patch the generator to emit `<link>` to the shared CSS instead.
- **Existing essays:** all shipped with inline styles that duplicate the shared CSS. Migrating them is low-priority cleanup. Both approaches work in the browser.
- **Generator patch (one-time, T1):** in `scripts/render-words-essays.cjs`, replace the emitted `<style>...</style>` block with `<link rel="stylesheet" href="/words/writing/_shared/writing.css">`. Then the shared file earns its keep.

Full class inventory, token table, breakpoint map, and migration notes:
`references/writing-design-system.md`.

**Migration note:** existing essays (AGI Paradox, Truth Is Not Cheap, The Third Axis of Failure)
ship inline `<style>` blocks that duplicate the shared CSS. They look right; they pass verify-pages;
nothing links `_shared/writing.css`. Don't treat the orphan shared file as a defect — it documents the
intended design system even if the generator currently emits inline styles.

### [object Object] pitfall — SPA render failure on static shells

Symptom: `public/<route>/index.html` exists but every link renders as
`[object Object]` literally in the served HTML.

Cause: the static shell was hand-authored assuming the SPA would re-render
it at build time, but no generator ever overwrites the file. React JSX
inside a `template` tag or a `<div dangerouslySetInnerHTML>` with an object
gets stringified to "[object Object]" when no React runtime hydrates.

Fix: **rewrite the static shell by hand**. Group entries by series (S1–S9),
use real `<a href="...">` for every link (no template objects, no `{e.title}`
JSX leaking). For the writing index the pattern is:

```html
<p class="series-label">S4 · Governance Canon</p>
<ul>
  <li><a href="/words/writing/<slug>/">Title</a> <span class="meta">· YYYY-MM-DD</span></li>
</ul>
```

For Medium cross-links (separate language/territory) keep them grouped
under "Medium Pieces (cross-linked)" with `target="_blank" rel="noreferrer"`.

### Caddy `/writing/*` double-prefix bug (verified 2026-08-07)

`/etc/caddy/Caddyfile` has:

```caddy
redir /writing/* /words/writing{uri} 308
redir /essays/* /words/writing{uri} 308
```

`{uri}` includes the matched prefix, so `/writing/foo` → `/words/writing/writing/foo`
(double `/writing/`). Same for `/essays/foo` → `/words/writing/essays/foo`.
Both 404. **Affects every essay, not just new ones** — pre-existing.

Canonical URLs (`/words/writing/<slug>/`) work fine. The legacy redirects
are decorative for SEO/backlinks; if any inbound links exist they currently
break.

Fix recipe (T1, reversible):

```caddy
redir /writing/* /words{uri} 308
redir /essays/* /words{uri} 308
```

Strip the `/writing` or `/essays` prefix by replacing the destination
template, then verify:

```bash
curl -sIL "https://arif-fazil.com/writing/<any-slug>/" | grep -i location
# expect: location: /words/writing/<any-slug>/
```

Until this Caddy rule is patched, tell the user the canonical URL and note
the redirect chain is broken for inbound `/writing/` and `/essays/` traffic.
Do NOT silently patch Caddy during a routine essay-publish — that's a
separate day's work.

### Essay module slug convention — avoid prefix collisions (verified 2026-08-07)

The essay filename in `src/data/essays/` uses an ordinal prefix
(`01-...`, `02-...`, ..., `24-...`) but the **slug in the EssayContent**
must NOT include that prefix. Slug is the URL path component — `/words/writing/<slug>/`.

```ts
// filename: src/data/essays/24-the-agi-paradox-why-bigger-models-wont-save-us.ts
const content: EssayContent = {
  slug: 'the-agi-paradox-why-bigger-models-wont-save-us',  // ← no `24-` prefix
  // ...
};
```

If the filename prefix leaks into the slug, the canonical URL becomes
`/words/writing/24-the-agi-paradox-...` instead of the human-friendly form,
and `articles-annotated.json` entries won't match.
