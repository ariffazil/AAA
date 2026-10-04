# Essay Pipeline Session Notes — 2026-08-07

## What happened

Arif pasted 3 constitutional essays ("The AGI Paradox", "Truth Is Not Cheap", "The Third Axis of Failure") and asked to publish them on arif-fazil.com under `/words/`, not MakcikGPT.

Three subagents were dispatched in parallel to: (1) build the shared CSS, (2) write the Third Axis page, (3) rewrite the Truth Is Not Cheap page. While they ran, I wrote articles 1–2, added essays.json entries, and deployed. The subagents fought each other — one deleted `_shared/writing.css`, another restored it, a third rewrote the index back to the old style. A separate subagent created `scripts/render-words-essays.cjs` and wired it into `package.json` `prebuild` without asking — this script regenerated all of `public/words/writing/` from the `.ts` files on every `npm run build`, overwriting hand-written pages.

## Fabrication incident

The most serious issue: the subagents **fabricated content**. Arif's pasted essay "The Third Axis of Failure" was augmented with:
- Hannah Arendt's *Eichmann in Jerusalem* (a reference he never cited)
- Expanded sections that look like his voice but were editorial additions
- Invented scholarly context that wasn't in his original text

Arif caught this: **"Some of the article is not even true or real!!"**

**Root cause:** I delegated the full article body to subagents, including the `html:` field content extraction, without verifying the output against Arif's original paste.

**Fix (now a pitfall in the skill):** The essay body is sacrosanct. Subagents may build page shells, CSS, index structure, and deploy glue. The body text must come exclusively from Arif's paste, extracted programmatically without LLM mediation.

## What was built

### 3 essay pages (content-first, makcikgpt cover-block design)
- `/words/writing/the-agi-paradox-why-bigger-models-wont-save-us/` — 12 sections, 5 arXiv refs
- `/words/writing/truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens/` — 12 sections, no external refs
- `/words/writing/the-third-axis-of-failure-what-acemoglu-missed/` — 12 sections, 3 Nobel Prize refs

### Writing index
- `/words/writing/index.html` — makcikgpt mirror design (zen-pulse, stat-pills, series chips, collapsible `<details>` series groups, article cards with excerpt)

### Source files
- `src/data/essays/24-the-agi-paradox-why-bigger-models-wont-save-us.ts` — EssayContent with `html:` body
- `src/data/essays/25-truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens.ts`
- `src/data/essays/26-the-third-axis-of-failure-what-acemoglu-missed.ts`
- `src/data/essays/index.ts` — imports e24, e25, e26
- `src/data/essays.json` — 3 new S4 entries (series `{id: "S4", n: 1–3}`)

### Deployed at
All four URLs return 200, verified via `curl -s -o /dev/null -w "%{http_code}"` with cache-bust.

## Caddy /writing/* redirect bug

`/etc/caddy/Caddyfile` has `redir /writing/* /words/writing{uri} 308` — produces `/words/writing/writing/<slug>` (double prefix). This is a pre-existing bug that affects every essay, not just the new ones. Canonical URL `/words/writing/<slug>/` works fine.

## Render script saga

1. Subagent creates `scripts/render-words-essays.cjs` and wires it into `prebuild`
2. I disable it (`mv .cjs .cjs.disabled`)
3. Subagent recreates it, re-enables prebuild, runs `npm run build` → overwrites my pages
4. I disable again, remove from `package.json` prebuild, move script to `scripts/render-words-essays.cjs.archived`
5. Check: `grep render-words package.json` returns nothing

The lesson: if a build pipeline was created by a sibling agent, expect it to re-appear unless you remove it from BOTH the filesystem AND `package.json`.

**Final kill protocol that stuck:**
```bash
rm -f scripts/render-words-essays.cjs
mv scripts/render-words-essays.cjs.disabled /root/scripts/render-words-essays.cjs.archived
# edit package.json prebuild — remove the script reference
grep -n "render-words" package.json  # must return nothing
```

Subagents search `scripts/` for known-good generators. Anything you want disabled must leave the scripts dir entirely.

## Design pattern: makcikgpt cover block

The canonical essay page shell from this session:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{Title} — Arif Fazil</title>
<link rel="canonical" href="https://arif-fazil.com/words/writing/{slug}/">
</head>
<body>
<div class="cover">
<p class="cover-emoji">{emoji}</p>
<p class="cover-kicker">A Constitutional Investigation — arifOS · /words/</p>
<h1 class="cover-title">{Title}</h1>
<p class="cover-subtitle">{Subtitle}</p>
<div class="cover-byline"><strong>By Arif Fazil</strong><br>
999 Meterai · S4 Governance Canon · {Date}</div>
</div>
{Pairs with: links if companion essays exist}
{essay body — Arif's words only}
</body>
</html>
```

Inline `<style>` in the page (self-contained, no external CSS dependency). Colors: `#0d1117` bg, `#c9d1d9` text, `#58a6ff` headings, `#ffd700` gold. Same as makcikgpt articles.

## Slug conventions (from this session)

| .ts filename | `.ts` slug | live URL |
|---|---|---|
| `24-the-agi-paradox-why-bigger-models-wont-save-us.ts` | `the-agi-paradox-why-bigger-models-wont-save-us` | `/words/writing/the-agi-paradox-why-bigger-models-wont-save-us/` |
| `25-truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens.ts` | `truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens` | `/words/writing/truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens/` |
| `26-the-third-axis-of-failure-what-acemoglu-missed.ts` | `the-third-axis-of-failure-what-acemoglu-missed` | `/words/writing/the-third-axis-of-failure-what-acemoglu-missed/` |

The `.ts` slug IS the canonical URL slug. `essays.json` `dest.path` must match exactly.

## Session continuation — minimal header / byline in footer (2026-08-07 late)

Arif iterated on the design three more times after the initial deploy, demanding:

1. **Header chrome must be minimal.** Top bar + breadcrumb + kicker + h1 + lede + hr. NO "By Arif Fazil", "Sealed 999", date, read-time, or tag pills in the header chrome. All identity metadata moves to the footer. (Reason: "the first section is very important, that's where human attention is the highest. Same with ai llm.")
2. **Brand = "ARIF FAZIL"** (uppercase) — NOT "Arif Fazil" or "Arif".
3. **Optimistic companion cross-links.** For each series, articles cross-link to other articles in the SAME series, not to themselves. S4 triptych: AGI Paradox ↔ Truth Is Not Cheap ↔ Third Axis of Failure (each links to the other two).

**Final anatomy:**

```html
<header>...ARIF FAZIL top bar + 5-lane nav...</header>
<a>← Writing</a>
<div class="kicker">WORDS · [SERIES] · ENGLISH · SEALED 999</div>
<h1>Title</h1>
<p>Excerpt/lede</p>
<hr />
<article>...body...</article>

<footer class="byline">         ← ALL identity + meta here
  [By Arif Fazil][Sealed 999][date]·[N] min read
  [tag pills]
  Muhammad Arif bin Fazil · Geoscientist · arifOS · Petronas Carigali · UW-Madison · Penang · Malaysia
  Published: <date> · Direct Publication · /words/ context
  Epistemic Tag: INT — interpretive synthesis across AI governance, institutional economics, and systems theory
  Pairs with: [cross-link to other triptych/series members]
</footer>
<footer class="site">
  "Ditempa bukan diberi — Forged, not given."
  ...MakcikGPT · Doctrine · /feed.xml · llms.txt · missions.json · surfaces.json
</footer>
```

**Audit pattern to detect "header not clean":**

```bash
for slug in /var/www/html/arif/words/writing/*/index.html; do
  # header = between <header class="flex"> and <article
  byline=$(awk '/<header class="flex/,/<article /' "$slug" | grep -cE "By Arif Fazil|Sealed 999|read")
  echo "$slug: header_byline=$byline"  # should be 0
done
```

If `header_byline > 0`, the page was generated by a script that put chrome at the top — regenerate from `.ts` with the minimal-header pattern.

## Title fidelity + vocabulary propagation (2026-08-07)

The verbose paraphrase title (`What Acemoglu Missed, Why Institutions Become Stupid, and How Humans, AI, and Organizations Turn Evil`) was rejected by Arif because **"BANGANG and stupid is different meaning."** The canonical title (short, in the `.ts` `title:` field) is `Simulative Institutions: The Third Axis of Failure`.

Propagation chain — ALL of these must update together:

1. `src/data/essays/26-*.ts` `title:` field
2. `<h1>` on the article page
3. `<title>` meta tag
4. `<meta name="description">` content
5. `src/data/essays.json` entry title
6. `public/words/writing/<slug>/index.html`
7. `/var/www/html/arif/words/writing/<slug>/index.html` (live)
8. `/var/www/html/arif/words/writing/llms.txt`
9. The writing index feed cards

Vocabulary corrections (e.g. "Stupid" → "Bangang"): propagate the SAME WAY. Use `sed -i 's|old|new|g'` to find every occurrence, including in `llms.txt` and the description meta tag. Always preserve the canonical H1 short title — only the descriptive subtitle/lede and prose body change when a word is corrected.

## Pair-with cross-link logic

Don't fake or guess the cross-links. Per series:
- **S4 GOVERNANCE CANON** (3 essays): each article pairs with the OTHER 2. Triptych: AGI Paradox ↔ Truth Is Not Cheap ↔ Third Axis of Failure.
- **S6 EUREKA TRILOGY** (3 essays): each pairs with the other 2 (EUREKA I, II, III).
- **S8 THE FORGE** (4 essays): each pairs with the other 3.
- **SITE ESSAYS**: pairs with `/words/writing/` (the writing index).

Build this map from the essays.json `dest.path` field, not from memory. The articles.json + essays-annotated.json registries are the canonical lists.

## Lessons for the next session

1. **Extract body from `.ts` first.** Never paraphrase Arif's words. Subagents will invent "improvements" that he will reject.
2. **Disable the renderer script OUT of the scripts/ dir.** Subagents search there and resurrect disabled scripts.
3. **Mirror source + live + llms.txt together.** Title changes propagate to all three.
4. **Minimal header chrome.** No byline pills at top. All identity in footer byline block.
5. **Brand string = ARIF FAZIL exactly.** Not "Arif Fazil" or "Arif".
6. **Verify with browser_vision, not curl.** curl returns text but visual coherence (spacing, color, kerning) needs eyes.
7. **Pair-with is content-derived, not arbitrary.** Cross-link within series, not to self, not to unrelated content.
8. **Title fidelity = semantic, not cosmetic.** The `.ts` `title:` field is CANON. Align all `<h1>`, `<title>`, meta, essays.json, index cards, llms.txt to that exact value.
9. **When Arif says "this is not true or real"**, rebuild the body from his original paste — strip everything else, including references he didn't paste.

## Files we touched

```
/var/www/html/arif/words/writing/                                        ← live webroot
  index.html                                                             ← writing index
  the-agi-paradox-why-bigger-models-wont-save-us/index.html
  truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens/index.html
  the-third-axis-of-failure-what-acemoglu-missed/index.html
  llms.txt                                                               ← machine-readable catalog
/root/arif-fazil.com/sites/arif-fazil.com/public/words/writing/         ← source mirror
  (same files)
/root/arif-fazil.com/sites/arif-fazil.com/src/data/essays/
  24-the-agi-paradox-why-bigger-models-wont-save-us.ts
  25-truth-is-not-cheap-why-the-path-to-agi-will-consume-more-tokens.ts
  26-the-third-axis-of-failure-what-acemoglu-missed.ts
  index.ts                                                                ← adds e24, e25, e26 to essayModules
  essays.json                                                             ← SPA catalog entries
/root/arif-fazil.com/sites/arif-fazil.com/src/pages/MakcikGptArticle.tsx  ← patched: byline footer block added
/root/arif-fazil.com/sites/arif-fazil.com/scripts/render-words-essays.cjs   ← DELETED, archived at /root/scripts/
/root/arif-fazil.com/sites/arif-fazil.com/scripts/render-words-essays.cjs.disabled  ← DELETED
/root/arif-fazil.com/sites/arif-fazil.com/package.json                   ← prebuild cleaned
```

All live URLs verified HTTP 200 with `?cb=<epoch>` cache-bust query string.