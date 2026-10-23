---
name: makcikgpt-article-forging
description: "Use when forging or updating a MakcikGPT article on arif-fazil.com. Six-stage pipeline — observe, hypothesise, forge in MakcikGPT voice, audit on T×A×M×P×G×R, verify build, hand deploy to the canonical site owner — with the voice rules, zero-factor gate and pitfall set that keep the article human."
triggers:
  - "makcikgpt article"
  - "write makcikgpt"
  - "forge makcikgpt"
  - "publish makcikgpt"
  - "makcikgpt pasal"
  - "cerita makcik"
  - "pastikan manusia boleh relate"
  - "relate to my life"
  - "bukan untuk AI lab orang"
  - "kutuk essay"
  - "aku undi sado"
  - "menggatai"
  - "aku nak menggatai"
  - "BANGANG"
  - "dedah BANGANG"
  - "geng lanyard"
  - "buat pdf"
  - "nak baca dalam kereta"
  - "aku pun bias"
  - "jangan tipu diri sendiri"
version: "2.0"
capability_tier: fed-long-context
ecology_state: WARM
---

# MakcikGPT Article Forging — pipeline core

> Strip jargon. Tanya "niat siapa?". Sambung decay institusi ke hidup manusia.

**Current rule (2026-10-13, wins over any older copy).** Do not `rsync -av dist/` to the
webroot. Do not `sudo caddy reload`. Do not run `deploy-site.sh --apply`. Ship ONE article
path, additive, no `--delete`. A full-tree rsync overwrites live-only HTML. Queue is
`/root/work/tasks.json`. Deploy ownership: skill **`arif-sites-ops`**.

---

## PIPELINE — six stages, each gated

| Stage | What | Gate to pass before the next stage |
|---|---|---|
| **1 OBSERVE** | multi-source research on the topic | every load-bearing number has a primary source + year |
| **2 HYPOTHESISE** | find the hidden thread across the data | one sentence: what is really happening, who pays |
| **3 FORGE** | write in MakcikGPT voice, TS article format | voice rules pass, no epistemic labels in reader text |
| **4 AUDIT** | T×A×M×P×G×R pre-publish check | no factor scores zero; at least one G moment; rasa present |
| **5 VERIFY** | build (`npm install --legacy-peer-deps` → `npm run build`) | build green, bot-markdown + static HTML generated |
| **6 DEPLOY** | hand to `arif-sites-ops` | live URL returns the article, body not a 404 shell |

Stage detail (verbatim, moved 2026-10-23): `references/stage-1.md` · `stage-2.md` ·
`stage-3.md` · `stage-4.md` · `stage-5.md` · deploy record `references/deploy.md`.

---

## STAGE 4 GATE — T×A×M×P×G×R (mandatory before publish)

| Factor | Question | Fail = |
|---|---|---|
| **T** Truth fidelity | every number verified to primary source, year correct? | propaganda |
| **A** Cognitive access | a kampung makcik understands without asking anyone? | elite report |
| **M** Moral meaning | connected to human life — what does the number DO to people? | empty data |
| **P** Power legibility | who gains, who loses, who takes, who is exposed? | corporate comms |
| **G** Generational horizon | "anak cucu tinggal apa?" | short-termism |
| **R** Correction / memory | uncertainty acknowledged, correctable later? | frozen myth |

**Zero-factor rule:** any factor at 0 → do not publish. Fix first.
**G is the zero-test** — at least one moment that forces the reader to face the next
generation. It cannot be answered with data alone; it needs *niat*.
**Rasa audit after the six:** correct numbers with no human face still fails. Add one specific
grounded bearer of the consequence ("anak buah umur 24 kerja kilang", not "seorang pekerja").
The human face cannot be invented — archetypal, grounded.
**External verification:** at least one outside check (Gemini / web / peer) on the
highest-risk number. This is what caught RM55bn vs RM101.6bn when internal review missed it.
Full framework: `references/pre-publish-audit-framework.md`.

---

## STAGE 3 — VOICE (the rules that bite)

Seven rules: BM Penang casual ("hang", "depa", "kena") · strip jargon, translate it ·
ask the shadow question ("niat siapa?") · connect institution to the makcik at the pasar ·
no false balance (she has a view, shows evidence) · declare epistemic state **internally
only** · end with a question or a demand, not a summary.

Hard bans: corporate summary tone · academic bothsidesing when he said *kutuk* · AI-isms
("it's important to note") · English paragraphs in the body · bullet-point report formatting ·
moralising escalation on routine internal docs · defensive padding before a sharp claim ·
**epistemic labels / Greek headers / analyst jargon in reader-facing text** ("the moment aku
nampak epistemik, aku down") · big numbers without a human scale · AI-sounding makcik voice ·
academic opening that buries the punchline.

**Aloud test:** if it does not sound like your neighbour at the pasar, it is too AI. Short
sentences, "So / Tapi / Yang penting", punchline first, then context.

**Kutuk mode:** lead with the target, dual-target as two parallel attacks, mechanism before
specifics, floors used as alternative architecture (never lectured), closing line = a question
or a demand. Sweet spot ~6,000–7,000 characters for a full essay.

**Political analysis default:** present the "how they COULD lose" case before "how they WILL
win"; BN-PN gains are the default story, DAP/PH holds must be proven. Anti-pattern: a
framework built on "Loke will win" with a thin caveat.

All 14 named voice patterns with worked examples: `references/voice-patterns.md`.

---

## STAGE 6 — DEPLOY (pointer, not procedure)

Deploying any arif-fazil.com page belongs to **`arif-sites-ops`** (canonical owner). Load it.
The MakcikGPT-specific record — the five root causes, `curl -sI` lying about content-length on
HTTP/2, SPA "Tidak Dijumpai" despite a good bundle, Caddy having no `/images/*` handler,
Cloudflare caching 404s — is kept in `references/deploy.md`. It is history, not authority: if
it disagrees with `arif-sites-ops`, site-ops wins.

---

## OPERATIONS

File locations, TypeScript article template, the KEMASKINI / transparency-banner update
protocol, parallel-agent session ingestion, corpus digest, and the Wikipedia multi-pass
biography method: `references/operations.md`.

Editorial doctrine — the Anti-Calhoun "Beautiful Ones" frame, the Gödel lock for publishing
(external validation required), the dark-theme PDF delivery variant, and Stage 8 distribution:
`references/editorial-doctrine.md`.

---

## TOP PITFALLS

1. **Full-tree rsync overwrites live-only HTML.** One article path, additive, never `--delete`.
2. **`curl -sI` lies about content-length on HTTP/2** — verify with a full-body GET.
3. **Bundle good + page shows "Tidak Dijumpai"** = slug/index registration, not the bundle.
4. **Unregistered `.ts` file** silently missing from build — check `index.ts` / `essays.json`
   before blaming the build.
5. **Caddy has no `/images/*` handler by default** — image 404s look like build failures.
6. **Cloudflare caches 404s** — purge before declaring a deploy dead.
7. **Deploy "MISMATCH: live=no-live"** is often a regex false-negative, not a real mismatch.
8. **Numbers pass, rasa fails** — the zero-factor gate and the rasa audit are separate tests.

Full pitfall ledger with worked sessions: `references/pitfalls-ledger.md`.

## CHANGELOG

| Version | Date | Change |
|---|---|---|
| 2.0 | 2026-10-23 | Surgical compression 106KB → core. Stages 1–6, the 14 voice patterns (34KB), deploy record (29KB), operations and editorial doctrine moved verbatim to `references/`. Deploy redirected to canonical owner `arif-sites-ops`. Duplicate frontmatter triggers removed. |
