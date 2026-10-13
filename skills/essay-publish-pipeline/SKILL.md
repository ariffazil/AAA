---
name: essay-publish-pipeline
description: "Publish a personal essay onto arif-fazil.com under /words/writing/<slug>/. Covers .ts module authoring, SPA routing registration, articles.json registry, build + rsync, and the dual-path (SPA + static shell) discoverability that prevents text-only crawlers from returning UNKNOWN. Also covers MakcikGPT direct-write deploys and the Caddy static-first fix for browser visibility. Load when Arif pastes a personal essay or asks to publish on his site."
version: "1.1.0"
metadata:
  hermes:
    tags: [essay, publish, arif-fazil.com, words-writing, content, authoring, makcikgpt, caddy]
---

# Essay Publish Pipeline — arif-fazil.com

Turn an essay paste from Arif into a live `/words/writing/<slug>/` page on
arif-fazil.com. Class of task: any time Arif writes a personal essay in chat
and says "publish" / "under words" / "publish on my site".

## Current rule (2026-10-13, wins over later copy-paste)

`rsync -a dist/ /var/www/html/arif/` and `systemctl reload caddy` below are historical scars. Ship the shells that name the NEW hash, plus `rsync -av --update` of the new assets. No `--delete`. No Caddy reload. A full-tree rsync overwrites live-only HTML. Count live HTML that names a hash the new dist lacks. `--delete` only after that count is zero. On 2026-10-13 that count was 74. Re-count. Live vhost is `/etc/caddy/vhosts/arif-fazil.com.conf`. Queue is `/root/work/tasks.json`.

## Template Selection (read this FIRST — grouped 2026-08-11)

arif-fazil.com has **three distinct writing surfaces**, each with its own
design register. Wrong template = essay lands in the wrong voice. Pick before
writing the body.

| Surface | Design register | Use for | Template file |
|---|---|---|---|
| **Medium** (external) | Intimate, single column, zero chrome, photo hero | Personal / reflective essays with emotional core (e.g. "The Scar Behind the Vision") | Medium editor — agent only drafts, Arif publishes |
| **`/words/writing/<slug>/`** (SPA + static shell) | Sovereign host, forge branding (italic uppercase title, "Narrative · Ψ SOUL" gold label, mono date+tags), body `prose-invert max-w-3xl`, no sidebar | Personal / reflective essays **owned sovereignly**. Same intimate register as Medium but in your own house. | `src/pages/EssayPage.tsx` (the existing component) — no SPA changes needed for personal essays |
| **`/world/makcikgpt/<slug>/`** (direct-write static) | Data-dense, full chrome: breadcrumb `MAKCIKGPT × TOPIC × SEALED 999`, subtitle/dek, bold-red data points, source panel, persona byline | Civic journalism / data analysis (PETRONAS, governance, sovereignty). NEVER use for personal essays — the chrome overwhelms emotional content. | `public/makcikgpt-md/<slug>.html` (direct write) + `src/data/essays.json` registration |

**Selection criteria (decision tree):**

```
Is it personal, reflective, emotional, scar-bearing?
  ├─ Yes → /words/writing/  (sovereign) or Medium  (broader reach)
  │        Rule of thumb: Arif says "publish on my site" → /words/
  │        Arif says "publish on Medium" → Medium (you draft, Arif posts)
  │
  └─ No, it's civic journalism / data analysis / sovereignty?
         └─ Yes → /world/makcikgpt/  (always)
```

**Arif's own comparison (verbatim, 2026-08-11):**

> "Untuk 'The Scar Behind the Vision' — article personal macam tu — Medium's
> design is actually BETTER reading experience. Bila content emotional,
> reader needs less scaffolding, not more. Navigation + breadcrumb + sidebar +
> 4 footer sections = noise between reader and feeling."

> "Untuk 'Syaitan yang Ingat Dirinya Malaikat' — data journalism dengan
> nombor audit — arif-fazil.com design is STRONGER. Reader needs sources,
> needs numbers highlighted, needs breadcrumb untuk trust the audit trail."

**Default: when in doubt, ask Arif which surface.** The body of the essay is
identical between Medium and `/words/writing/` — only the wrapper changes.
MakcikGPT body has its own register (Makcik persona, kampung analogies,
data-anchored) — it cannot be a personal essay.

See `references/design-templates.md` for the full layout comparison matrix,
screenshots of each surface, and the "Two Agents, One Scar" case study of why
this distinction matters.

## Pipeline (proven 2026-08-07 on "I'm Not a Programmer…")

The essay content is verbatim from Arif's paste. **Zero fabrication.** The agent's
job is plumbing — wiring it into the SPA bundle, the static shell, and the
discovery layer. No embellishment, no scholarly citations, no "Makcik analisa"
voice.

### Step 1 — Author the EssayContent module

`src/data/essays/<N>-<slug>.ts`:

```ts
import type { EssayContent } from './types';

const content: EssayContent = {
  title: `<Full title as Arif wrote it>`,
  date: '2026-08-07',  // ISO
  slug: 'i-didnt-invent-a-token-i-invented-a-question',  // URL path, no `<N>-` prefix
  tags: ['ai-governance', 'agi', 'arifos', ...],
  excerpt: `<one-sentence thesis for SPA catalog>`,
  mediumUrl: '',          // '' = direct publication, no Medium repost
  isDirectPublication: true,
  html: `<article>...full body HTML...</article>`,
};

export default content;
```

Rules:

- **No fabricated content.** Copy Arif's paste into the `html` field with minimal
  structural HTML (`<h2>`, `<p>`, `<blockquote>`, `<pre><code>`, `<ul>`, `<hr>`). Don't
  add scholarly citations, paraphrased summaries, or "Makcik" voice unless Arif
  wrote them.
- **Slug format:** kebab-case, no ordinal prefix. Filename: `27-i-didnt-...ts`,
  `slug:` field: `i-didnt-...` (no `27-`). The renderer builds the URL from the
  slug field.
- **Title field is CANON** — `<title>`, `<h1>`, meta description, llms.txt,
  essays.json, index cards must all match this exact string.

### Step 2 — Register in two places (not one)

This is where the session broke first: register in **only one** of the two
registries and the essay disappeared from the SPA bundle due to Vite
tree-shaking.

**Registry 1 — `src/data/essays/index.ts`:**

```ts
import e27 from './27-i-didnt-invent-a-token-i-invented-a-question';
// ...
export const essayModules = [..., e26, e27, ...];
```

Both the import AND the array entry are required. Drop the import → bundle
excludes it. Drop the array entry → no essay in the catalog.

**Registry 2 — `src/data/essays/articles.json`:**

```json
{
  "slug": "i-didnt-invent-a-token-i-invented-a-question",
  "title": "I'm Not a Programmer. I Accidentally Invented a New Question for AI.",
  "date": "2026-08-07",
  "categories": ["AI-Governance", "AGI", "arifos", ...],
  "mediumUrl": "https://arif-fazil.com/words/writing/i-didnt-invent-a-token-i-invented-a-question/",
  "hasContent": true,
  "isDirectPublication": true
}
```

This is the registry that **matters for SPA bundle inclusion**. Verified
2026-08-07: dropping this entry caused `getEssay(slug)` to return `undefined`,
SPA rendered "Essay Not Found", even though `essays.json` had the slug.
Diagnose with `grep "<your-slug>" dist/assets/index-*.js` — empty means
articles.json is missing the slug.

**Registry 3 — `src/data/essays.json` (SPA catalog):**

Add a top-level entry for the SPA catalog sidebar / index. Same slug.
`series: { id: 'S4', n: 4 }` for governance canon series, or whatever
matches.

### Step 3 — Build + rsync (and watch for SPA-only trap)

```bash
cd /root/arif-fazil.com/sites/arif-fazil.com
npm run build 2>&1 | tail -10
# Renderer: 14 → 15 essays in /words/writing/ index. Good.
# SPA bundle: new index-*.js. Good.

NEW_BUNDLE=$(ls dist/assets/index-*.js | head -1 | xargs basename)
echo "NEW BUNDLE: $NEW_BUNDLE"

# HISTORICAL SCAR. Do not full-tree rsync. Copy the shells that name the NEW hash,
# plus: rsync -av --update dist/assets/ /var/www/html/arif/assets/
# Do not add --delete. Re-count live HTML that names a hash the new dist lacks.
```

**The trap.** Without a static shell, the essay is **SPA-only**. A
text-only crawler (Copilot, EMD, research agent, curl) gets the React shell
back, content UNKNOWN. `curl -s https://arif-fazil.com/words/writing/<slug>/`
returns 200 but the body is empty.

### Step 4 — Author static shell (server-rendered fallback)

The renderer doesn't emit per-essay static shells (only the listing index).
**Hand-author the static shell** at:

`public/words/writing/<slug>/index.html`

Template rules (mirrors the live essay shells):

- Inline `<style>` block — no external CSS link, the shell must render in
  any browser without dependencies
- Forge black/gold palette (`#0A0B0D`, `#c9a227`, `#F4ECD8`)
- Minimal hero: `<title>` + canonical `<link>` + `<h1>` + `<p class="lede">`
  + breadcrumb + kicker
- Body = the same `html` field verbatim (no SPA-only chrome)
- Footer block = ARIF FAZIL brand + identity (3-col) + epistemic stance + pills
  + DITEMPA BUKAN DIBERI manifesto line

`public/words/writing/<slug>/index.md` (markdown mirror) — agent-friendly
fallback for any agent with `.md` preference.

### Step 5 — 5-gate verification (per `arif-sites-ops` skill)

```bash
SLUG="i-didnt-invent-a-token-i-invented-a-question"
URL="https://arif-fazil.com/words/writing/$SLUG/?cb=$(date +%s)"

# Gate 1: live URL returns 200
curl -sf -o /dev/null -w "%{http_code}\n" "$URL"

# Gate 2: title appears in served HTML
curl -s "$URL" | grep -oE "<title>[^<]+</title>"

# Gate 3: index lists the essay exactly once
curl -s "https://arif-fazil.com/words/writing/" | grep -c "$SLUG"

# Gate 4: essays.json slug matches the .ts slug exactly
python3 -c "import json; d = json.load(open('src/data/essays.json')); [print(e['dest']['path']) for e in d if 'programmer' in e.get('title','').lower()]"

# Gate 5: essays.json count incremented
python3 -c "import json; print(len(json.load(open('src/data/essays.json'))))"
```

If all five pass: ship. If any fail: stop, fix, re-verify. Don't seal receipt.

### Step 6 — Git push (protected branch workflow)

`main` is protected on `ariffazil/arif-fazil.com` and `ariffazil/web-canon`. Direct
push is rejected with `GH006`. Branch + PR:

```bash
BRANCH="feat/seal-essay-<NN>-$(date +%Y%m%d)"
git checkout -b "$BRANCH"
git add src/data/essays/<N>-<slug>.ts src/data/essays/index.ts \
         src/data/essays/articles.json src/data/essays.json \
         src/pages/EssayPage.tsx public/words/writing/index.html \
         public/words/writing/index.json public/words/writing/llms.txt \
         public/words/writing/<slug>/index.html \
         public/words/writing/<slug>/index.md
git commit -m "feat(words): <slug> — <one-line summary>"
git push -u origin "$BRANCH"
# Returns PR URL. STOP. Arif merges from GitHub UI.
```

## Dual-register articles (English + Bahasa Makcik)

For topics that need both an English essay and a Bahasa Makcik article (same content, two registers), see the `arif-fazil-web-ops` skill → **Dual-register article workflow** section. Those articles use direct-write deployment (write_file → chown → chmod), NOT the SPA pipeline. The MakcikGPT article goes to `/var/www/html/arif/makcikgpt-md/<slug>.html`, not through `scripts/generate-makcik-articles.cjs`.

### MakcikGPT browser-visibility (CRITICAL — verified 2026-08-09)

**⚠️ Direct-write MakcikGPT deploys were BOT-ONLY by default.** Caddy's `/world/makcikgpt/*` browser handler served the React SPA shell, which only knew slugs compiled into its JS bundle. Unregistered slugs rendered **"ARTICLE NOT FOUND"** in browsers while curl (bot UA) got the static HTML with HTTP 200. This produced false-positive "all gates passed" reports for 24 articles (verified 2026-08-09).

**The fix (applied 2026-08-09):** Changed the Caddy browser handler `try_files` from SPA-first to static-first:

```caddyfile
# BEFORE (bot-only visibility):
try_files {path} /index.html

# AFTER (static-first, SPA fallback):
try_files /makcikgpt-md{path}.html /makcikgpt-md{path}/index.html /index.html
```

**Location:** `/etc/caddy/Caddyfile`, inside `handle /world/makcikgpt/*` block (find with `awk '/handle \/world\/makcikgpt\/*/ { found=1 } found && /try_files/ { print NR; exit }' /etc/caddy/Caddyfile`).

**⚠️ Caddyfile editing pitfall:** The pattern `try_files {path} /index.html` appears in MULTIPLE handlers. Using `sed 's/try_files {path} \/index.html/.../'` without line targeting will change the WRONG handler (e.g., the homepage handler at line ~397 instead of the makcikgpt handler at line ~877). Always:
1. Find the exact line number first: `awk '/handle \/world\/makcikgpt\/*/ { f=1 } f && /try_files/ { print NR; exit }' /etc/caddy/Caddyfile`
2. Use line-specific sed: `sed -i '<LINE_NUM>s|old|new|' /etc/caddy/Caddyfile`
3. Verify: `sed -n '<LINE_NUM-5>,<LINE_NUM+5>p' /etc/caddy/Caddyfile`
4. Validate: `caddy validate --config /etc/caddy/Caddyfile`
5. Reload is T3. Do not run `systemctl reload caddy`.

**Post-fix behavior:** Any `.html` file dropped into `/var/www/html/arif/makcikgpt-md/` is immediately visible to browsers. No SPA registration needed. Landing page (`/world/makcikgpt/`) still serves the SPA shell (separate handler above the article handler).

### MakcikGPT 3-gate verification (MANDATORY)

After deploying a MakcikGPT article, verify ALL THREE gates — curl alone produces false positives:

```bash
SLUG="your-article-slug"
BASE="https://arif-fazil.com/world/makcikgpt"

# Gate 1: curl (bot UA) returns 200 with content
curl -sfL -o /tmp/test.html -w "HTTP:%{http_code} SIZE:%{size_download}\n" "$BASE/$SLUG/"
# Must be HTTP:200 and SIZE > 2000

# Gate 2: browser renders the article (NOT "ARTICLE NOT FOUND")
# Use browser_navigate to $BASE/$SLUG/ and check the snapshot
# The h1 must match the article title, NOT "ARTICLE NOT FOUND"

# Gate 3: landing page lists the article
grep -c "$SLUG" /var/www/html/arif/makcikgpt-md/index.html
# Must be >= 1 (typically 2: href + text)
```

**If Gate 2 fails:** The Caddy static-first fix may not be applied. Check `/etc/caddy/Caddyfile` for the `try_files /makcikgpt-md{path}.html` pattern in the `/world/makcikgpt/*` handler.

**If Gate 3 fails:** Add the article to `/var/www/html/arif/makcikgpt-md/index.html` (the landing page). See `references/makcikgpt-caddy-routing.md` for the full recipe.

## Tersurat/Tersirat Writing Technique (user-enforced, 2026-08-09)

Arif taught this Malay literary technique for viral advocacy content. **Tersurat** = explicit (what is written). **Tersirat** = implicit (what is understood between the lines).

**How it works:**
- **Tersurat layer:** Factual, auditable, data-driven. Tables, numbers, timelines. The "surface" that anyone can verify.
- **Tersirat layer:** The deeper meaning that readers intuit but the text never states directly. The emotional/political subtext.

**Example from this session:** The "paradox" section about rightsizing:
- Tersurat: CEO gets extension while 5,000 workers are cut
- Tersirat: The pattern of exploitation — one side always takes, one side always gives, and the taker is never satisfied

**User correction (verbatim):**
> "Hang tulis paradox tu sebijik sebijik. Aku bagi analogi ja. Tulis la bahasa tersurat tersirat sikit hang. Tu level SPM kot. X kan aku nak ajar tersurat tersirat"

**When to use:**
- Open letters to parliamentarians
- Viral MakcikGPT articles
- Any advocacy content that needs to resonate emotionally while being factually bulletproof
- Content where direct statements would be too sensitive or legally risky

**Rules:**
- The tersurat layer MUST be backed by verifiable data (F2 compliance)
- The tersirat layer should be obvious to any Malaysian reader but never explicitly stated
- Never explain the tersirat layer — let readers discover it themselves
- The best viral content has both layers working simultaneously

## Open Letter (Surat Terbuka) Format — Parliamentary Submissions

For formal letters to Malaysian parliamentarians, use this format:

**Structure:**
1. Header block (right-aligned): To, From, Date, Reference
2. Title: centered, uppercase, formal
3. Salutation: "YANG BERHORMAT AHLI-AHLI PARLIMEN YANG DIHORMATI"
4. Body: numbered paragraphs (for easy reference in parliamentary discussion)
5. Sections with bold headers and left-border accent
6. Data tables for comparison
7. Blockquotes for key philosophical points
8. Specific demands at the end
9. Signature block
10. Footer with attribution and data sources

**Voice:** Formal Bahasa Malaysia (surat menyurat register). NOT MakcikGPT register. NOT English.

**Data visualization:** Include charts for visual hooks ("Manusia need visual hook"). Revenue trends, cash flow waterfalls, governance structure diagrams.

**Attribution:** Include the producing agent/system (e.g., "Hermes ASI with arifOS Kernel, Warga Agentik AAA"). Add GitHub link if applicable.

**External AI audit:** Before finalizing, run through an external AI (Gemini via FED proxy) for independent review. Document the audit results as part of the submission.

### Constitutional witness declaration — APEX Letter pattern (2026-08-12)

When the surat is a F13 SOVEREIGN constitutional petition — not a corporate memo — apply this pattern. Verified on PETRONAS APEX LETTER II (v14, 10 pages, sealed `SHA: f31349…082e`).

**Goal discovery BEFORE drafting — never assume.** The 2026-08-12 session produced 11 reversals (v3→v14) because the stated vehicle ("audit") was assumed to be the goal. The actual goal surfaced only after F13 direct Q&A: *"Tengku Taufik mesti pergi."* If you treat the stated **vehicle** (audit, SEARAH exposure, governance documentation) as the **goal**, you produce corporate compliance, not constitutional witness. Open with 1 direct question: *"What is the actual goal, not the vehicle for reaching it?"* Then draft.

**Voice choice — three options, never blended:**
1. **Tenang institutional** — Pak Arif's APEX Letter canonical. Open: "Nama saya X. Saya seorang geosaintis. Saya tidak menulis untuk meminta sesiapa dihukum." Use when the letter is to an institutional recipient (PAC, AG, regulator).
2. **Qualia + real WhatsApp voice** — Sensory anchors (pukul 3 pagi, kopi sejuk, cahaya bilik tak padam) + verbatim quotes from real source data (e.g. `/root/ariffazil/HUMAN/mak-abah/whatsapp-family-kita/`). Use when the human story IS the message (NAIO, media, public surface).
3. **Oppenheimer/INTJ patience** — "Now I am become Death, the destroyer of worlds." frame. Long-view strategic. Use when the writer has decided to commit to irreversible cost.

**Defensive language audit.** If the writer's stated goal is direct (e.g., "Tengku Taufik mesti pergi"), REMOVE defensive phrases like:
- ❌ "Saya tidak menulis untuk meminta sesiapa dihukum" (×3)
- ❌ "Saya tidak menulis untuk meminta sesiapa dibuang kerja"
- ❌ "Saya tidak minta sesiapa dipenjara"

These dilute intent. Three repetitions of denial signal **the opposite of what they say they want**. The reader (PAC, regulator) sees deflection, not constitutional witness.

**Iteration discipline — honor the most-recent F13 directive.** When the writer reverses (one letter → three letters → one letter → final), STOP asking "confirm or adjust?" and BUILD the most-recent directive. Do not keep asking. Pak Arif verbatim: *"Aku penat la"* → terse acknowledgment + action + result. Multiple reversals in one session are the model's discipline failure, not the writer's.

**APEX judge pattern — HOLD+F13_REQUIRED is constitutional, not failure.** All reversals of v3-v14 returned `effective_verdict: HOLD, f13_required: true, next_action: AWAIT_INPUT`. This is the constitutional pattern for irreversible dispatch — do not treat HOLD as failure. The agent must not bypass; F13 SOVEREIGN personal signature is required for dispatch.

**Real WhatsApp voice extraction technique** (for qualia):
1. Read `/root/ariffazil/HUMAN/mak-abah/whatsapp-family-kita/2015-2026-whatsapp-transcript.txt`
2. Search: `grep -E "(Mak tengah siang|Siapa pun tak ucap|Assalamuailom|pagi)"` — yields 100+ matches
3. Select 3-5 verbatim quotes that anchor specific dates
4. Use inline with `<span class="voice-quote who">SUARA MAK — WhatsApp "Family Kita", DD Month YYYY, HH:MM</span>`
5. NEVER paraphrase. NEVER use "mother archetype" / "fiksyen mak" — Pak Arif rejects this as regression (verified v9→v10→v11)

**Single anchor discipline.** The mak voice appears ONCE only in the surat — as quoted memory, then rejected. Do not repeat the mak narrative multiple times. One anchor = honorable. Five anchors = performative.

**Multimedia fallback for video (ffmpeg when Gemini times out).** Gemini video generation on this infrastructure has 2/3 timeout rate. When it fails:
```bash
# Trim audio to opening 60s
ffmpeg -y -i surat-narrative.mp3 -ss 0 -t 60 -acodec copy surat-narrative-60s.mp3

# Combine cover image + audio with fade-in/out, 30s budget
timeout 30 ffmpeg -y \
  -loop 1 -framerate 1 \
  -i cover-image.png \
  -i surat-narrative-60s.mp3 \
  -c:v libx264 -preset ultrafast -tune stillimage \
  -c:a aac -b:a 128k -pix_fmt yuv420p \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fade=t=in:st=0:d=2,fade=t=out:st=58:d=2" \
  -shortest -movflags +faststart \
  cover-trailer.mp4
```
Deterministic, no external API timeout. Produces a 60s MP4 with cover image + opening audio + fade-in/out.

**Skill load order — load at the START of any constitutional petition task, not mid-session:**
1. `pdf-report-generation` — HTML → weasyprint pipeline, charts, page discipline
2. `humanizer` — strip AI-isms, add qualia
3. `apex-judge` — constitutional verification, F13 escalation
4. `arif-sites-content-ops` — if dispatching to arif-fazil.com
5. `essay-publish-pipeline` — this skill (for format reference)

Loading mid-session wastes 5+ minutes of context per skill. Load once at task start.

**Voice preference order — Pak Arif's preferences, encoded 2026-08-12:**
1. **Terse** — direct, no preamble, no philosophical framing
2. **Action + result** — "Done. [what changed]. [evidence path]." (per AGENTS.md response contract)
3. **HOLD/F13 verbatim** — quote APEX receipts as returned, never paraphrase
4. **No "So what?" narration** — `audit this artifact` → corrected v2 ship, not self-audit
6. **Single F13 disposition** — never offer 4-option menu when the answer is obvious (audit→dispatch)

**Anti-patterns — what NOT to do** (encoded from this session's failures):
- ❌ 11 reversals when 1-2 suffices
- ❌ Asking "confirm or adjust?" 20+ times
- ❌ Treating "audit" / "SEARAH" / "exposure" as the goal when they're the vehicle
- ❌ Defensive language 3× when stated goal is direct
- ❌ Asking "Kerry's = key or carry or query?" — ONE guess, then act, ONE confirm
- ❌ Skipping real WhatsApp transcript in favor of "fiksyen mak archetype"
- ❌ Loading pdf-report-generation / humanizer / apex-judge skills mid-session — load at START

## External AI Audit Workflow (new, 2026-08-09)

Before publishing any advocacy content, run it through an external AI for independent review:

1. Extract text from PDF/document
2. Call Gemini via FED proxy (`gemini-flash` model)
3. Request: strengths, weaknesses, missing data, legal risks, virality assessment, overall verdict
4. Document findings
5. Make amendments based on valid criticisms
6. Re-run audit if major changes made

**FED proxy command:**
```bash
source /root/.secrets/kunci-mas.env
curl -s http://127.0.0.1:4000/v1/chat/completions \
  -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
  -d '{"model":"gemini-flash","messages":[...]}'
```

## MP Email Compilation Workflow (new, 2026-08-09)

For campaigns targeting Malaysian parliamentarians:

1. **PAC members** — primary targets for audit requests (`pacparlimen@parlimen.my`)
2. **Johor MPs** — relevant for Petronas/SEARAH/JCorp operations
3. **Sarawak MPs** — relevant for Petronas-Petros gas rights dispute
4. **Opposition voices** — those who have publicly questioned GLC governance
5. **Media amplifiers** — podcast hosts (KJ, Shahril Hamdan — Keluar Sekejap)
6. **Key ministers** — CC for notification (PMX, DPM, Finance Ministers)

**Output:** CSV with columns: Name, Constituency, Party, Email, Tier (Primary/CC/BCC), Reason

**Email format:** `name@parlimen.my` (official) or personal emails found via parlimen.gov.my/profile

### MakcikGPT SPA bundle registration (CRITICAL — verified 2026-08-09)

**The MakcikGPT SPA has THREE registries that must all stay in sync:**

| Registry | File | What it feeds | Sync required |
|----------|------|---------------|---------------|
| **SOT** | `src/data/essays.json` | Static landing page (`generate-makcik-index.cjs`), feed, sitemap, llms.txt | Every publish |
| **SPA module** | `src/data/makcikgpt/index.ts` (import + `makcikArticleModules[]`) | Vite SPA bundle — article pages render in browser | Every publish |
| **SPA meta** | `src/data/makcikgpt/index.ts` (`makcikArticlesMeta[]`) | SPA bundle landing page card list + article count badge | Every publish |

**The prebuild trap:** `npm run build` runs `generate-makcik-index.cjs` during prebuild, which regenerates `public/makcikgpt-md/index.html` from `essays.json`. If you manually edited the static index, your changes are overwritten. **Never hand-edit `makcikgpt-md/index.html` — always update `essays.json`.**

**The vite cache trap:** If you edit `index.ts` but vite doesn't detect changes (incremental build), the SPA bundle won't include the new entry. Fix: `rm -rf dist node_modules/.vite` before rebuild.

**Registration recipe for a new MakcikGPT article:**

```bash
SLUG="your-article-slug"
DATE="2026-08-09"
TITLE="Your Article Title"

# 1. essays.json — add entry with id, slug, title, date, lang, series, tags, dest, seal
# This is the SOT for static index, feed, sitemap

# 2. index.ts — add THREE things:
#    a) import: import myArticle from "./$SLUG";
#    b) makcikArticleModules: add myArticle to the array
#    c) makcikArticlesMeta: add {slug, title, subtitle, date, domain, language, excerpt, tags, seal, provenance_status}

# 3. Verify in compiled bundle:
#    BUNDLE=$(ls -t dist/assets/index-*.js | head -1)
#    grep -c "$SLUG" "$BUNDLE"  # must be >= 2

# 4. Rebuild clean:
rm -rf dist node_modules/.vite
npm run build
# HISTORICAL SCAR. Do not full-tree rsync dist/ onto /var/www/html/arif/
# Copy the shells that name the NEW hash, plus rsync -av --update of new assets.
# Do not add --delete. Re-count live HTML that names a hash the new dist lacks.

# 5. Verify all three gates (curl + browser + landing page)
```

**Why three registries?** The static landing page (`essays.json`) is for bots/discovery. The SPA module (`makcikArticleModules`) is for browser-rendered article pages. The SPA meta (`makcikArticlesMeta`) is for the landing page card list + article count badge. Missing any one breaks a surface.

**If you skip the meta array:** The SPA bundle has the article content (module array) but the landing page card doesn't appear and the article count stays wrong. The browser shows the old count.

**If you skip the essays.json:** The static index doesn't get regenerated. Bots see old count. Feed/sitemap don't include the article.

Arif explicitly rejected accounting/financial language for MakcikGPT articles:

> "Ni bahasa accounting la weiii. Cakap macam makcik kampung. Dia berniaga tenaga. Tapi rugi buat apa!!! Tutup la GENTARI tu. Lepas tu lantik Mat Salleh jadi CEO. Weiii. Makcik2 lagi sustainable la.. basuh berak pakai air, bukan tisu."

**Rules:**
- Use kampung analogies: "Macam kedai makcik: dulu jual 100 bungkus nasi lemak sehari, sekarang tinggal 83"
- Frame financial concepts as household/shop metaphors
- Include irreverent humor: "basuh berak pakai air, bukan tisu" (water > tissue = more sustainable)
- Name real people when Arif specifies: Charlotte Wolff-Bye, Gentari, etc.
- Never use jargon without a kampung translation
- The persona is MakcikGPT — never put Arif's name or credentials in the byline

**Article structure (viral-ready):**
1. Hook — one-sentence provocation ("13 sebab kenapa...")
2. Context — why this matters to the reader
3. Numbered points — each with a kampung analogy + hard number
4. Bonus section — contrast with a principled predecessor
5. Closing — philosophical punch + call to action
6. Summary table — all numbers in one scannable block
7. Attribution — "MakcikGPT · Civic Intelligence · [date] · [OBS]"

### MakcikGPT fact-verification pitfalls

- **Contract extension counts:** When writing about PETRONAS leadership, verify the extension count carefully. Tengku Taufik's timeline (as of 2026-08): Contract 1 (July 2020–June 2023), Extension 1 (July 2023–June 2026), Extension 2 (July 2026–?). The current extension is his **THIRD contract** overall, but only his **SECOND extension**. Arif corrected: "Wei ni kontrak kali ketiga la. Bukan kedua." Use "kontrak kali ketiga" when referring to the overall contract number, "extension kali kedua" when referring to extensions specifically.
- **PETRONAS financial data sources:** Always cite from the Integrated Report FY2025 (petronas.com/integrated-report-2025) or the Group FRA FY2025 PDF. Key figures: Revenue RM266.1B (down 17% from RM319.96B), PAT RM45.4B (down 18%), Capex RM41.6B (down 23% from RM54.2B), Dividend RM32B, Total borrowings RM121.6B, CFFO RM85.2B. The Edge Malaysia and FMT are secondary sources for CEO contract news.
- **Gentari losses:** Gentari falls under "Corporate & Others" segment which recorded LAT of RM0.5B in FY2025. Gentari has 8.4GW renewable capacity as of June 2025. Arif's angle: "Tutup la GENTARI tu" — frame as loss-making subsidiary draining parent company resources.
- **Charlotte Wolff-Bye:** She is VP/Chief Sustainability Officer at PETRONAS (formerly at Equinor). She is NOT from Wintershall Dea. CERAWeek 2026 speaker. Arif uses her as the "Mat Salleh CEO" alternative — frame as a competent Western woman who could run PETRONAS better.

### MakcikGPT F2 / F6 discipline (constitutional review pattern, 2026-08-11)

Apex-judge review of `syaitan-ingat-dirinya-malaikat` returned two recurring flags for MakcikGPT civic journalism. Encode them as pre-publish rules.

**F2 TRUTH — precision discipline for civic journalism:**

Civic journalism can round numbers for readability, but the rounding must be **owned** — either exact figures or an explicit `(anggaran dibundarkan)` footnote. Pattern verified 2026-08-11:

| Wrong | Right |
|---|---|
| "CAPEX runtuh dari RM52B ke RM40B" | "CAPEX runtuh dari RM54.2B ke RM41.6B" |
| "Revenue turun ke RM266B" | "Revenue turun ke RM266.1B (FY2024: RM319.96B)" |
| "Dividen 70.5% dari untung" | "Dividen 32/45.4 = 70.5% PAT" (already exact — keep) |

A ~4% rounding error (RM52B vs RM54.2B) on absolute values drops P(truth) below the F2 0.99 threshold even when the directional claim (-23%) is correct. The directional claim survives; the absolute numbers don't. Either use exact figures or add a rounding footnote at the bottom of the article.

**F6 EMPATHY ⇄ MARUAH — title dignity line:**

The title is the share/SEO/preview artifact. Loaded religious or moral metaphors ("Syaitan", "Malaikat", "Anjing") in the body work rhetorically with body caveats ("Makcik tak kata dia syaitan"). The same metaphor in the **title** is the dignity fault line — the body's nuance cannot redeem the title's shareable fragment.

Default title patterns that pass F6:
- Concrete governance framing: "Kontrak Kedua, Syarikat Makin Kurus"
- Subject + action: "CEO Dapat Perpanjangan, Dividen Pecah Rekod"
- Question form: "Bila Ketua Makin Gemuk, Syarikat Makin Kurus"
- Institutional noun: "Amanah Yang Tak Dilindungi"

**Override path:** Arif (F13 SOVEREIGN) can keep the loaded metaphor in the title. Apex flags CAUTION; F13 decides. Document the override in the apex receipt chain — "F13 override on F6 title; verdict SABAR with body unchanged."

### MakcikGPT SPA bundle registration (CRITICAL — verified 2026-08-09)
See `references/makcikgpt-spa-registration.md` for the three-registry sync details, failure modes, and debugging recipes.

After publish, the essay is discoverable through three independent paths:

| Path | Type | What serves it |
|---|---|---|
| `https://arif-fazil.com/words/writing/<slug>/` (browser) | Browser | SPA bundle (dynamic) |
| `https://arif-fazil.com/words/writing/<slug>/` (text-only) | Crawler | Static shell (server-rendered) |
| `https://arif-fazil.com/words/writing/<slug>/index.md` | Agent | Markdown mirror |
| `https://arif-fazil.com/words/writing/llms.txt` | Discovery | Renderer listing |
| `https://arif-fazil.com/llms.txt` (top-level) | Discovery | Site-wide manifest |

**Failure of one witness no longer destroys recoverability.** This is the
core lesson from 2026-08-07 — when the EMD crawler returned UNKNOWN on a
SPA-only essay, the static shell + markdown mirror + llms.txt listing
together made the essay fully extractable. Without any one of those three,
text-only agents would have a black hole.

## Publish discipline (user-enforced, 2026-08-09)

- **"Published" means findable, not 200.** If the surface has an index/landing
  page, the article must be LINKED from it before you report done. Arif's exact
  failure: agent announced "published", user clicked from the index, got nothing
  → "Article not found. Pembohong hang." Verify article + index entry + landing
  page in one pass, then announce.
- **Verify before announcing, every time.** A premature "it's live" costs more
  trust than a two-minute verification. Sequence: write → fix perms → update
  index → probe live → report. Never reorder.
- **Persona surfaces carry no author name.** On MakcikGPT and similar persona
  surfaces, never put Arif's name or credentials in the article — the persona
  is the byline ("Aku ni bukan anak raja. Aku share artikel x dak sapa baca.").
- **NEVER publish analysis/PDFs on arif-fazil.com without explicit permission.**
  Arif said: "Jangan la publish situ. New pages. Jangan merosakkan site aku."
  Research PDFs, MP email lists, and analysis deliverables go to local paths
  (`/tmp/` or `/root/arif-fazil.com/docs/`) — NOT the live website. Only
  MakcikGPT articles and approved essays go to the live site. Always ask:
  "Nak publish kat website ke atau local sahaja?" before deploying.
- **MakcikGPT articles: user approves content, then publishes.** In this
  session (2026-08-09), Arif asked for articles, I wrote them, he reviewed,
  said "go", and I deployed. But he also corrected me multiple times on voice
  ("Ni bahasa accounting la weiii") and data ("kontrak kali ketiga la. Bukan
  kedua."). Always get explicit "go" before deploying to live.

## Pitfalls

- **CRITICAL: Caddy `/words/*` uses DIFFERENT root than the rest of the site.**
  The Caddyfile handler `handle /words/*` (line ~740 in `arif-fazil.com.conf`)
  sets `root * /var/www/html` — NOT `/var/www/html/arif` which is the global
  site root. This means static shells for `/words/writing/<slug>/` must be
  deployed to `/var/www/html/words/writing/<slug>/index.html`, NOT
  `/var/www/html/arif/words/writing/<slug>/index.html`. Files placed in the
  `/arif/` prefix will return 404. Verified 2026-08-14: all three essays in
  the trilogy returned 404 until static shells were copied to the correct
  root. **Deploy recipe:**
  ```bash
  # WRONG, and also a wipe risk (404 plus live-only HTML overwrite):
  # HISTORICAL SCAR. Do not run: rsync -a dist/ /var/www/html/arif/
  # Static shells at /var/www/html/arif/words/writing/<slug>/ — NOT SERVED

  # RIGHT (200):
  # The dist/ build already creates dist/words/writing/<slug>/index.html
  # Copy to the Caddy handler's actual root:
  for slug in <slugs>; do
    mkdir -p "/var/www/html/words/writing/$slug"
    cp "dist/words/writing/$slug/index.html" "/var/www/html/words/writing/$slug/index.html"
  done
  ```
  Other Caddy handlers (`@agent_shells`, `@static_dirs`) use `root * /var/www/html/arif`
  — only `handle /words/*` and `handle /work/*` override to `/var/www/html`.

- **Essays.tsx pre-existing TS error on `series?.n` (verified 2026-08-14).**
  `src/pages/Essays.tsx` lines 48 and 73 access `e.series.n` and `e.series.id`
  without optional chaining. When essays.json has entries WITHOUT a `series`
  field (common for new essays), `npm run build` fails with:
  ```
  TS18048: 'a.series' is possibly 'undefined'
  ```
  **Fix:** Add `?.` to both lines:
  ```tsx
  // Line 48:
  <span className="text-forge-dim">#{e.series?.n ?? ''}</span>
  // Line 73:
  <span className="font-mono text-[0.55rem] text-forge-dim uppercase">{e.series?.id}#{e.series?.n}</span>
  ```
  This is a pre-existing bug in Essays.tsx, not caused by new essays. Patch
  it once and commit — it's a permanent fix for any essay without `series`.

- **Multi-article batch deployment pattern (verified 2026-08-14).**
  When publishing multiple essays in one session (e.g. a trilogy), batch the
  work to avoid redundant builds:
  1. Create ALL .ts modules first
  2. Register ALL in index.ts (imports + array entries) in one edit
  3. Register ALL in articles.json + essays.json in one pass
  4. Run `rm -rf dist node_modules/.vite && npm run build` ONCE
  5. Deploy ALL static shells in one loop
  6. Verify ALL in one pass
  Building per-essay wastes 2-3 minutes each on Vite compilation.

- **Cloudflare blocks browser access to Medium / Substack** when researching source essays for republication. If `browser_navigate` returns the Cloudflare "Sorry, you have been blocked" page (with a Ray ID), do NOT narrate from search snippets — the response will be a fabrication dressed as witnessing. Instead, fall back to:
  - `web_extract(urls=[...])` — HTTP client pathway, bypasses Cloudflare bot detection, returns full markdown content
  - `forge_fetch` — A-FORGE governed HTTP client, also bypasses
  - Only when ALL fetch pathways fail should you declare the source unreadable

  Verified 2026-08-11 with Arif's "Scar Behind the Vision" essay: `browser_navigate` returned Cloudflare block page (Ray `a29746b10c17b71c`); `web_extract` returned the full 3-minute essay including canon capsule tag and vault hash. The difference between snippet-narration and actual reading is the difference between fabrication and witness. **A sibling agent failed this case by reading snippets and writing a fluent response as if it had seen the essay — it had not.**

- **SPA-only slug = invisible to text-only crawlers** (the entire reason
  static shell + markdown mirror exist). Verified 2026-08-07: an essay
  shipped without `public/words/writing/<slug>/index.html` was UNKNOWN
  to EMD's text-only crawler, despite being visible in a browser.
- **`articles.json` registry is mandatory** — Vite tree-shakes essays
  without it. Don't register in only one of the three places.
- **Don't paste, paraphrase, or "improve" Arif's body.** Verified 2026-08-07:
  a prior sibling session fabricated Hannah Arendt quotes and added scholarly
  citations to Arif's Third Axis essay. Arif's feedback verbatim: *"Some of
  the article is not even true or real!!"* Strip and restore; never embellish.
- **Title fidelity is semantic, not cosmetic.** The canonical title lives in
  the `.ts` `title:` field, NOT in any hand-built page. The rendered
  `<h1>`, `<title>`, meta description, llms.txt, essays.json, index cards
  must all match exactly.
- **`render-words-essays.cjs` runs in prebuild** — it will overwrite any
  hand-placed `public/words/writing/<slug>/index.html` with what the .ts
  contains. Hand-writing is wasted entropy if the renderer also writes.
  Current renderer only writes the listing index, not per-essay shells —
  verify by reading `scripts/render-words-essays.cjs` before hand-writing.
- **Hero chrome for SPAs is centralized in `EssayPage.tsx`.** Any change
  to the hero (tags, MIN READ, SECTION count pills) should land in the SPA
  component, not in hand-built static shells. Static shells mirror the SPA
  footer (identity + publication + epistemic) but skip the chrome pills —
  those are computed at runtime.
- **`paper-meta` block at top of essay body is duplicate of footer.** Strip
  from all `.ts` files where it appears (verified 2026-08-07: 13 hand-authored
  essays were carrying this duplicate). Use a regex like:
  `<div class="paper-meta[^"]*">.*?</div>\s*(?:</div>\s*)?` (with DOTALL).
- **Chrome-creep is the slow killer of human-first design.** Every small
  addition to a visual surface — a footer note, source-of-truth line, status
  pill — accumulates. The 5 Rein (`Canonical landing:`, `WHERE AM I?`,
  `WHY CARE?`, `Source of truth:`, `Rendered by`) MUST NEVER appear in a
  visual HTML page. `scripts/design-lint.sh` blocks the build on any hit.
  See `DESIGN_INVARIANTS.md` for the canonical visual contracts. Companion
  skill: `makcikgpt-archived-designs` for the recovery patterns.
- **Match the design language to content type.** Medium's clean reading
  column suits personal essays (`/words/writing/`). The data-dense Primer
  Dark chrome suits MakcikGPT civic journalism (`/world/makcikgpt/`). Don't
  apply the wrong template — it overwhelms the wrong content.

- **Caddy `spa-shell.html` missing — new essays get 404 (verified 2026-08-14).**
  The `@spa_routes` handler in `arif-fazil.com.conf` references `try_files {path} {path}/index.html /spa-shell.html`. But `/var/www/html/arif/spa-shell.html` does NOT exist by default — it's never created during build. Result: any new essay without a static shell returns 404 in browsers, even though the SPA bundle has the slug. **Fix:** After every build, copy `dist/index.html` → `/var/www/html/arif/spa-shell.html`. This is the React SPA shell that renders client-side routing. One file, covers all missing static shells.

- **MakcikGPT articles need CSS injection (verified 2026-08-14).** The `prerender-articles.cjs` script produces bare HTML with NO styling — white background, default browser font. 80 out of 80 articles were unstyled. **Fix:** Run `python3 /tmp/inject-article-styles.py` which injects Primer Dark CSS (dark bg, gold headings, serif body, blue blockquotes) + Google Fonts link into every article `<head>`. Idempotent — skips files already containing the sentinel `MAKCIKGPT ARTICLE — Primer Dark reader`. After any regeneration of article HTML, re-run the injector.

- **Subagent 504 timeout pattern (verified 2026-08-14).** Long-running subagents (shell generation, landing page rebuild) consistently hit 504 after 7-11 minutes. The task completes on the filesystem but the API response times out. **Workaround:** For mechanical tasks (HTML generation, file manipulation), use `execute_code` directly instead of delegating — it doesn't have the 504 wall. Reserve `delegate_task` for reasoning-heavy tasks that benefit from isolated context.

## MakcikGPT voice evolution — "Empat Cara Kenal Realiti" (2026-08-14)

The mature MakcikGPT philosophical voice is NOT anti-metric. It is:

> "Every reality has its own rightful way of being known."

Four ways of knowing:
| Realiti | Cara Kenal | Example |
|---------|-----------|---------|
| Physical | Timbang (measure) | Blood pressure, weight, money |
| Social | Saksi (witness over time) | Trust, leadership, relationships |
| Internal | Rasa (feel) | Grief, love, shame |
| Existential | Hidup (live) | Meaning, purpose, sacrifice |

The error is using the WRONG method for the wrong domain:
- Measuring trust → you get a survey, not trust
- Feeling blood pressure → you get hope, not health
- Analyzing meaning → you get theory, not life
- Witnessing grief → you can't, you can only feel it

This replaced the earlier "anti-metric" position. The evolution:
1. "Not everything can be measured" (anti-metric, 4/10 as doctrine)
2. "Measurement is not wrong. Measurement is one way of knowing." (mature, 8.5/10)

Arif's correction (verbatim): "I don't want any jargons at all. I want full reality human. No ai no arifOS."

## Article unification script (2026-08-14)

`scripts/unify-makcikgpt-v2.cjs` — batch-fixes ALL MakcikGPT articles to canonical Primer Dark template. Handles: no-nav, no-article-tag, duplicate h1, old CSS, metadata paragraphs in body.

```bash
node scripts/unify-makcikgpt-v2.cjs
# Output: fixed=N skipped=N errors=N
# After: verify with grep -c 'header class="flex' /var/www/html/arif/makcikgpt-md/*.html
```

Run after any batch article generation or when Arif reports "sakit mata" on article design.

## Automated shell generation (added 2026-08-14)

Two scripts automate the manual Steps 4 + landing rebuild:

- **`scripts/generate-writing-shells.py`** — reads all `.ts` essay files, extracts metadata (title, date, slug, tags, html), generates canonical static shells matching EssayPage.tsx design. Handles both old format (`html: \`<h4>...`) and new format (`html: \`<article>...</article>`). Outputs to `public/words/writing/<slug>/` + `dist/words/writing/<slug>/`.
- **`scripts/generate-writing-landing.py`** — reads all `.ts` essays, generates unified `/words/writing/` landing page with featured section, monthly groupings, card layout matching site design system.

**After running both:** copy to Caddy paths (`/var/www/html/words/writing/`) per the root-path pitfall below, then verify.

## Landing page completeness (verified 2026-08-14)

The `/words/writing/index.html` landing page must list **every essay** that has a
static shell on disk. Verified: the page listed only 16 of 28 essays — 13 were
missing (including the entire trilogy + early essays like "I Have Trust Issues
With Agents", "The First Act of Creation", etc.).

**Recipe after any batch publish:**
```bash
# Count slugs on disk
DISK=$(ls -d /var/www/html/arif/words/writing/*/ | wc -l)
# Count links in landing
LINKED=$(grep -oP 'href="/words/writing/\K[^/"]+' /var/www/html/arif/words/writing/index.html | sort -u | wc -l)
echo "Disk: $DISK | Linked: $LINKED"
# If LINKED < DISK, rebuild landing page with all essays
```

**Unified shell design (canonical pattern from EssayPage.tsx):**
All static shells must use:
- tokens.css + Google Fonts (Fraunces + Newsreader + IBM Plex Mono) + Fontshare (Satoshi + Cabinet Grotesk)
- Header: `bg-forge-steel border-b-2`, breadcrumb `← Words & Writing`, label `Narrative · Ψ SOUL`
- Title: `text-4xl md:text-5xl font-black italic uppercase`
- Body: `max-w-3xl prose-invert font-body text-lg`
- Footer: `Published directly on arif-fazil.com` badge + `← All Essays`

Do NOT use inline Georgia fonts or omit tokens.css — that produces a different
visual register that clashes with the SPA version.

## Reference

- `arif-sites-ops` skill — the parent surface pipeline. Loads on any site edit.
- `essay-publish-watermark` skill — header/footer convention (NO author
  banner at top of essays; footer carries the ARIF FAZIL identity block).
- `apex-fact-check-pass` — pre-seal verification for cited claims.
- `constitutional-witness-apex-letter` (reference) — verified v14 APEX Letter pattern with SHA-256 anchors, real WhatsApp extraction, voice options, defensive language audit, ffmpeg fallback recipe, and F13 disposition format. Load when forging sovereign petitions to parliamentary/institutional recipients.
- `frontier-model-audit-verification` — when an audit claims the essay is
  missing or unregistered, verify against the actual schema before responding.
- `FORGE-agentic-web-builder` — agentic web class-level umbrella (DOCTOR / DEPLOY / AUDIT / REPAIR / SEAL / EPHEMERAL). Load on any agentic-web mutation.
- `makcikgpt-archived-designs` — git archive of archived MakcikGPT designs (Primer Dark, chat-interface, minimal essay page) + extract recipe + the chrome-creep drift trail.
- `arif-site-human-first-audit` — 4-lane deploy audit (Technical / Navigation / Visual / Attention) with anti-bulldoze pattern.
- `references/makcikgpt-css-injection.py` — idempotent Python script to inject Primer Dark CSS into all MakcikGPT article HTML files. Sentinel-based. Run after any article regeneration.
## Makcik Kampung register — philosophical essays (new, 2026-08-14)

Distinct from MakcikGPT civic journalism. Same Persona (Makcik), different register.

**When to use:** When Arif wants to express governance/life/love/truth concepts through
everyday kampung analogies, NOT data journalism. Topics: love, trust, reality, measurement,
human relationships. Zero jargon — no "entropy", "drift", "thermodynamics", "capability".

**CRITICAL — Zero Jargon Rule (Arif explicit, 2026-08-14):**
> "Fail. I don't want any jargons at all. I want full reality human. No ai no arifOS"
> "Zero AI. Zero arifOS. Zero FQ. Zero jargon. Full kampung."

BANNED in Makcik Kampung articles: FQ, arifOS, AI, proxy, KPI, Model, drift, confident,
bullshit, federation, constitutional, entropy, thermodynamic, capability, agent, token,
scalar, vector, metric, measurement, organ, governance, sovereign, seal, forge, apex, quantum.

REPLACEMENTS: "FQ jatuh" → "hubungan mula jauh", "Model ↔ Model" → "Cerita ↔ Cerita",
"AI rosak" → "syarikat tutup", "proxy" → "benda ganti", "drift" → "cerita yang tak betul".

Scan EVERY article with: `grep -oinE '\b(FQ|arifOS|AI|proxy|KPI|Model|drift|...)` before deploy.

**Pattern (from "Semua Hidup Adalah Jual Beli" + "Kenapa Love Mati" + "Tiga Lapis Realiti"):**

1. **Hook** — everyday object/action as entry (nasi lemak, timbang badan, kebun)
2. **Table** — expand the analogy (what you give / what you get)
3. **Sections with h2** — each section deepens the concept
4. **Blockquotes** — key wisdom (from "orang tua dulu" or "saintis panggil")
5. **Three hukum/rules** — the conceptual core, always exactly three
6. **Nasihat Makcik** — closing advice (3 questions, or one maxim)
7. **Footer** — "DITEMPA BUKAN DIBERI" + "Jangan lawan realiti. Realiti tak pernah kalah."

### MakcikGPT article CSS typography standard (verified 2026-08-14)

All MakcikGPT articles MUST use this unified CSS. Eye strain reported with
18px/1.7 line-height — fixed by 17px/1.65. Every article gets the same block:

```css
:root{--bg:#0a0a0a;--bg-card:#111;--fg:#f0f0f0;--fg-muted:#9a9a9a;--red:#e0301e;--blue:#1f3fd4;--yellow:#f2b705}
body{background:var(--bg);color:var(--fg);font-family:"Newsreader","Georgia",serif;font-size:17px;line-height:1.65;max-width:680px;margin:0 auto;padding:48px 24px}
h1{font-family:"Cabinet Grotesk","Inter",sans-serif;font-size:clamp(24px,4vw,36px);font-weight:800;line-height:1.15;letter-spacing:-0.02em;margin:0 0 12px;color:var(--fg)}
h2{color:var(--yellow);font-size:1.3em;font-weight:700;margin:1.8em 0 0.6em}
h3{color:var(--red);font-size:1.15em;font-weight:700;margin:1.4em 0 0.5em}
p{margin-bottom:1em}
blockquote{border-left:3px solid var(--blue);padding:10px 18px;margin:1.2em 0;background:rgba(31,63,212,0.05);border-radius:0 6px 6px 0;font-style:italic;color:var(--fg-muted);font-size:0.95em}
strong{color:var(--yellow);font-weight:700}
hr{border:none;border-top:1px solid #2a2a2a;margin:1.5em 0}
table{width:100%;border-collapse:collapse;margin:1.2em 0;font-size:0.95em}
th{text-align:left;padding:8px 10px;border-bottom:2px solid var(--yellow);color:var(--yellow);font-weight:700;font-size:0.85em;text-transform:uppercase;letter-spacing:0.04em}
td{padding:6px 10px;border-bottom:1px solid #2a2a2a}
```

**Why these values:**
- 17px body: smaller than 18px reduces visual fatigue on dark backgrounds
- 1.65 line-height: tighter than 1.7, text feels connected without crowding
- 680px max-width: comfortable line length (55-65 chars) for Malay prose
- h1 clamp(24px,4vw,36px): prominent but not jarring vs body
- h3 1.15em: clear step from 17px body (h3 at 1.1em was invisible difference)
- paragraph margin 1em: connected text flow, not floating blocks

**Injection recipe:** `python3 /tmp/unify-articles.py` replaces all `<style>` blocks
idempotently. After any article HTML regeneration, re-run the injector.

**Landing registration:** Add to ARTICLES array in `/var/www/html/arif/makcikgpt-md/index.html`
with series M5 (Philosophy/Politics) unless content clearly fits M1-M4.

**Registration recipe (direct-write, no SPA build):**
```python
# /tmp/add_article.py
path = '/var/www/html/arif/makcikgpt-md/index.html'
with open(path) as f:
    c = f.read()
new_entry = '  {s:"M5",d:"YYYY-MM-DD",u:"/world/makcikgpt/<slug>",t:"<Title>"},\n'
c = c.replace('const ARTICLES=[\n', 'const ARTICLES=[\n' + new_entry, 1)
with open(path, 'w') as f:
    f.write(c)
```
Note: Python heredoc string escaping fails on terminal for JS object literals with quotes.
Always use write_file to create a .py script, then terminal to run it.

**Key difference from civic journalism:**
| | Civic Journalism | Makcik Kampung |
|---|---|---|
| Topics | PETRONAS, governance, sovereignty | Love, trust, reality, life |
| Data | Hard numbers, financials | No numbers, analogies only |
| Tone | Irreverent, provocative | Wise, reflective, warm |
| Hukum | Specific institutional failures | Universal life principles |
| Series | M1-M4 typical | M5 always |

### MakcikGPT pattern consistency (canonical layout, verified 2026-08-11)

When publishing to `/world/makcikgpt/<slug>/`, the static HTML must match this pattern. Copy-paste from a sibling article and modify body content — DO NOT reinvent the chrome.

### MakcikGPT landing (`/var/www/html/arif/makcikgpt-md/index.html`)

- **Canonical version:** 19,638-byte archive from 2026-07-31
- **Color palette:** custom `--red: #e0301e`, `--blue: #1f3fd4`, `--yellow: #f2b705` (NOT forge tokens)
- **Hero:** 4-color stacked headline `Makcik` white + `Tanya.` blue + `Kuasa` red + `Jawab.` yellow
- **Stats grid:** 84 Artikel / 5 Siri / 999 Seal Standard / BM Bahasa Makcik (updated 2026-08-14 from 22 → 80 → 84)
- **Quote callout:** yellow left border, "Depa kata strategic partnership…"
- **Series cards:** M1 red, M2 blue, M3 yellow, M4 dim, M5 white
- **Search/filter:** functional JS, filter by series, search by title
- **Footer:** "MAKCIKGPT · ARIF-FAZIL.COM · DITEMPA BUKAN DIBERI 🇲🇾"
- **DO NOT replace with forge-red monochrome** — that's the degraded version (14,074 bytes)
- **Restored to Primer Dark on 2026-08-14** — agents kept adding agent-chrome (zen-pulse, WHERE AM I?, etc.) which turned the journalism brand into a GitHub repo. Restored from archived commit `767596c`. The Primer Dark tokens + fractal canvas + 3-color scheme (red/blue/yellow) are now canonical. Any future modification must preserve these tokens.

### MakcikGPT article (`/var/www/html/arif/makcikgpt-md/<slug>.html`)

Pattern from `syaitan-ingat-dirinya-malaikat.html` (canonical example post-patch):

```html
<!doctype html>
<html lang="ms" data-ring="SOUL">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title><Title> — MakcikGPT | ARIF FAZIL</title>
  <link rel="stylesheet" href="/_shared/design-system/tokens.css" />
  <link rel="stylesheet" href="/assets/index-Dte6gqTG.css" />
  <link rel="canonical" href="https://arif-fazil.com/world/makcikgpt/<slug>" />
  ...
</head>
<body class="bg-forge-black">
<div class="site-frame max-w-4xl mx-auto px-4">
  <header class="flex items-center justify-between py-6 border-b border-forge-iron mb-10">
    <a href="/" class="font-display text-2xl text-forge-white hover:text-forge-gold">ARIF FAZIL</a>
    <nav>...5-lane nav...</nav>
  </header>

  <a href="/world/makcikgpt/" class="font-mono text-xs text-forge-red hover:text-forge-white mb-6">← MakcikGPT</a>
  <div class="font-mono text-[0.65rem] text-forge-red uppercase tracking-widest mb-1">Civilization Intelligence · Ξ WEALTH ·</div>
  <div class="font-mono text-[0.65rem] text-forge-red uppercase tracking-widest mb-4">MAKCIKGPT × <DOMAIN> × <TAG></div>
  <h1 class="font-display text-3xl md:text-5xl font-black italic uppercase leading-[0.9] tracking-tighter mb-4 mt-2 text-forge-red"><Title></h1>
  <p class="font-technical text-sm md:text-base text-forge-orange mb-4"><Subtitle></p>
  <div class="flex flex-wrap items-center gap-3 font-mono text-xs text-forge-dim mb-3">
    <span class="px-2 py-0.5 border border-forge-iron text-forge-white/90">Bahasa Makcik</span>
    <span class="px-2 py-0.5 border border-forge-red text-forge-red">Sealed 999</span>
    <time datetime="<YYYY-MM-DD>"><DD> <Month> <YYYY></time>
  </div>
  <div class="flex flex-wrap items-center gap-2 mb-12"><!-- tag pills --></div>
  <hr class="border-forge-iron mb-12" />
  <article class="font-body text-lg leading-relaxed text-forge-white/85 space-y-5 max-w-3xl">
    <!-- BODY — verbatim from .ts source html: field -->
  </article>
</div>
</body>
</html>
```

**Verification after publish:**
- `curl -sfL -A "Mozilla/5.0" "https://arif-fazil.com/world/makcikgpt/<slug>/" -o /tmp/test.html && wc -c /tmp/test.html` (must be >2000)
- `grep "<h1" /tmp/test.html | head -1` (must have article title, NOT "Article Not Found")
- `grep "<link rel=\"canonical\"" /tmp/test.html` (must point to `/world/makcikgpt/<slug>`)

### Why landing + article use DIFFERENT palettes (intentional)

- **Landing uses custom red/blue/yellow palette** — high visual impact, "wow factor", rich canvas + JS animation. Cost: harder for future agents to maintain.
- **Articles use forge-red palette** — clean, readable, matches `/words/writing/` canon. Cost: simpler, future-agent-friendly.

**This split is intentional** (per Arif's 2026-08-11 design decision). Do NOT homogenize them. The contrast is part of the brand identity: "landing catches eye, article keeps attention."

### What you MUST NOT do (MakcikGPT)

- ❌ **Invent new CSS when existing template exists.** When deploying a new MakcikGPT article, ALWAYS copy the HTML structure from an existing canonical article (e.g. `syaitan-ingat-dirinya-malaikat.html`) and only change the title/description/body. Do NOT create new inline styles, new CSS variables, or new font stacks. Arif's correction (2026-08-14): *"Why u cannot follow whatever already there!!! Basic kot"*. The existing template has tokens.css + index.css + Primer Dark injected CSS + correct fonts + correct nav + correct footer. Use it.
- ❌ Write to `/var/www/html/arif/world/makcikgpt/index.html` (orphan 105-byte stub) — Caddy never serves from here. Use `/var/www/html/arif/makcikgpt-md/index.html`.
- ❌ Add `.ts` source for `syaitan-ingat-dirinya-malaikat` etc. without ALSO updating the static HTML — Caddy static-first fix means static is what users see, not SPA.
- ❌ Replace landing's custom palette with forge tokens — that's the drift Arif rejected.
- ❌ Add `<title>` F-codes (`F1-F13`) — public surfaces use plain language only.
- ❌ Remove "Ditempa bukan diberi" from any footer — F13 identity mark.

---

DITEMPA BUKAN DIBERI — Forged, not given.
