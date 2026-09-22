---
id: civic-shadow-editorial
name: civic-shadow-editorial
version: 1.0.0
description: Use when publishing MakcikGPT articles and PM shadow pages to the site.
owner: FORGE (000Ω)
risk_tier: T2
floor_scope: [F2, F6, F11]
autonomy_tier: ANNOUNCE
forged_from: SESSION-2026-08-21 (MyKad RM7.5b + Taufik KLCC + 33 Bayang Anwar)
capability_tier: fed-long-context
ecology_state: WARM
---

# Civic & Shadow Editorial — arif-fazil.com

## When to Use

- Arif asks to write/publish a MakcikGPT article (any BM civic tabloid piece)
- Arif asks for shadow/political-psychology pages (PM Bayang, 33 bayang, Jung analysis)
- Deep research on a Malaysian political figure for publication
- Publishing civic content to /world/makcikgpt/ or /politics/shadow/ surfaces

## Voice registers — NEVER MIX

| Surface | Register | Key features |
|---|---|---|
| `/world/makcikgpt/*` | MakcikGPT BM tabloid | "Hai Makcik", ▲ fact-boxes, pull-quotes, "Soalan untuk ahli Parlimen" numbered list, closing "Buat Ini Sekarang" callout |
| `/politics/shadow/*` | Formal editorial psychology | Jungian analysis, brutalist cards, verdict badges (TERSEDAR/SAMAR/TENGGELAM), source chips |

Arif 2026-08-21 (explicit): "Do it real language as PM bayang. Not makcikGPT
voice. Real editorial psychology analysis." Default: article request w/o
register named = makcik voice; shadow/politics pages = editorial.

## Research protocol for political figures

1. **Wikipedia full pull** via curl + strip tags — then MULTI-PASS term search
   (15-20 terms per pass: early life, career, scandals, finance numbers).
   web_search returns PR noise for politician names — useless for bio depth.
2. **Primary sources when offered**: Arif sends screenshots (LinkedIn, The
   Edge). Read image FIRST, extract facts, label observation vs interpretation.
3. **Arif hands THESES to validate, not questions**: "anak orang senang acah
   jadi orang susah" → research must CONFIRM or REFUTE with sources, never
   write unverified. His facts: directionally right, temporally loose —
   verify dates/numbers, keep the insight.
4. **Label discipline**: court allegations = "tuduhan, rekod mahkamah";
   interpretation = "sintesis"; unverifiable = "aku tak pasti". Sexual/
   personal material: state the REKOD (trials, DNA, verdicts, pardon) then
   analyze the JUNGIAN STRUCTURE (split, persona vs shadow) — never assert
   guilt or orientation as fact.
5. **Sensitive-figure guard (F6)**: article builds on public record + named
   sources. Every claim carries inline source. No new allegations, no
   embellishment of court records.

## Article publish path (MakcikGPT) — 5 files, ALL required

1. `src/data/makcikgpt/<slug>.ts` — `ArticleContent {slug, html}`
2. `src/data/makcikgpt/index.ts` — import + module array + meta entry
3. `src/data/essays.json` — `mX-Y` registry (series M1-M6). **Duplicate
   dest.path = MakcikSourceError build fail** — grep before insert
4. `public/makcikgpt-md/<slug>.html` + `.md` (frontmatter: article_id,
   canonical_url, seal 999, epistemic_summary)
5. Build + deploy:
   ```
   cd /root/arif-sites/sites/arif-fazil.com && npm run build
   cd /root/arif-fazil.com && scripts/deploy-site.sh arif-fazil.com --apply
   ```

## New SPA detail page pattern (e.g. /politics/shadow/anwar-ibrahim)

data file `src/data/<name>.ts` (export array + SUMMARY const) → page
`src/pages/<Name>.tsx` (framer-motion, axis filter buttons, cards) → route in
`App.tsx` → link from listing card conditional on `pm.id`.

**TS pitfall**: double-quoted body strings with inner `"` = TS1005 cascade.
Write bodies double-quoted with ONLY single quotes inside; run `npx tsc -b`
(the build's checker — plain `tsc --noEmit` misses project refs) until clean.

## Review workflow (Arif-mandated)

draft → **PDF first** (Playwright: `pg.goto('file://...')` → `pg.pdf(format='A4', print_background=True)` → deliver via MEDIA:) → he critiques vs source screenshot → v2 → deploy. Never deploy before PDF review when he asked "bagi aku baca".

His emotional spikes ("Now I fucking hate him. Serious x layak") = commission
for a full sourced corpus build — channel rage into evidence, don't match it.

## Verification checklist (post-deploy)

- SPA route: browser UA → 200, title matches
- Bot lane: `GPTBot/1.0` UA on article path → full content, not shell
- Hub index: `grep <slug>` in `/makcikgpt-md/index.html`
- feed.xml contains slug
- `/makcikgpt-md/` dir path 301s to `/world/makcikgpt/` for browsers —
  test `index.html` direct for bot lane
- Known: `make deploy` fails on 13 pre-existing catalog/Caddy mismatches
  (308s) — use `deploy-site.sh --apply` (passes its own f₂ gates)

## Anti-patterns

- ❌ "DITEMPA BUKAN DIBERI" as chat closer — Arif called it filler; tagline
  belongs to artifacts, not conversation
- ❌ Mixing makcik voice into shadow pages (or vice versa)
- ❌ Publishing before PDF review
- ❌ Asserting court allegations as fact; asserting orientation/innocence
- ❌ web_search for politician bios (PR noise) — Wikipedia pull + term passes
- ❌ Forgetting essays.json entry (hub/feed miss) or dup dest.path (build fail)

## Companion skills

- FORGE-agentic-web-builder — deploy gates, dual-lane doctrine (profile aaa-hermes)
- petronas-petros-shell-dispute — O&G dispute corpus
- MY-REALITY-STACK — Malaysia primary-source routing

DITEMPA BUKAN DIBERI — artifacts only, never chat closers.
