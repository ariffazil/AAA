# 33 Bayang Anwar Ibrahim — Page Build + Parallel-Agent Collision (2026-08-21)

## What was built

Arif escalated 9 → 33 shadows: "Buat 33 la. 33 bayang Anwar Ibrahim. 3 axis - 11 each. Socio politics - economy - personal." Then: "publish here do real 33 shadows. Do it real language as PM bayang. Not makcikGPT voice. Real editorial psychology analysis."

## Two artifacts, two registers

1. **PDF draft** — `/tmp/anwar-33-article.html` → `/root/.hermes/output/anwar-33-bayang.pdf` via Playwright (dark theme, print overrides, 3 axis sections, 33 shadow cards).
2. **Site page** — SPA version AND a parallel-session static version both went live (see collision).

## The collision: SPA route vs parallel static deploy

While I built the React version, a sibling Claude Code session on the same VPS deployed a **static HTML** 33-bayang page in the same time window:

- My SPA: `src/pages/AnwarIbrahim33.tsx` + `src/data/anwarShadows33.ts` + route in `App.tsx` (`/politics/shadow/anwar-ibrahim`)
- Their static: `public/politics/shadow/anwar-ibrahim/index.html` → live at `/var/www/html/world/politics/shadow/anwar-ibrahim/index.html` (46KB, 35 shadow cards, same PM-Bayang design language: gold #c9a84c, verdict badges, IBM Plex)

**Caddy resolution:** `handle /world/politics/* { try_files {path} {path}/index.html =404 }` finds the static file FIRST; SPA fallback only fires when no file exists. `/politics/shadow/*` has 308 redirects to `/world/politics/shadow/*`. Result: **static version wins on every public URL variant.** Both 200 — verify which one you're actually reading before claiming your content is live.

**Lesson:** before building an SPA page for any `/world/` path, `ls /var/www/html/world/<section>/` for parallel static deploys. `ps aux | grep claude` + file mtimes tell you who's active. Reconcile, don't duplicate.

## Data file structure that worked

```typescript
// src/data/anwarShadows33.ts
export type ShadowAxis = "sosiopolitik" | "ekonomi" | "peribadi";
export interface Shadow { id: number; axis: ShadowAxis; depth: "persona"|"bayang"|"tragis"; title: string; body: string; source: string; }
export const ANWAR_SHADOWS: Shadow[] = [ /* 33 entries */ ];
export const ANWAR_SUMMARY = { name, tenure, totalShadows, axes, verdict: "TENGGELAM", coreInsight, jungLaw, sources: [] };
```

Per-card source line = F2 discipline carried into the page format itself.

## TS template-literal quoting traps (cost 3 build cycles)

- `TS1005: ',' expected` / `TS1002: Unterminated string literal` = unescaped `"` inside a double-quoted body, or body ending `.',` instead of `.",`
- Fix loop: `sed -n 'Np' file | python3` char-scan for exact positions, then python line-repair (inner `"` → `'`, fix terminator)
- **`npx tsc --noEmit` passed while `npm run build` (`tsc -b`) failed twice** — trust `tsc -b` only
- Prevention: write bodies with single-quote internals from the start; avoid smart-quote mixing

## The "33" content spine (for future N-shadow requests)

Axis 1 Sosiopolitik (01-11): origin acah (Baling false report + MP father), ABIM-as-ladder, 40-year title accumulation, all-enemies-except-UMNO, DNAA Zahid, Najib halved, shadow cabinet, security act, subsidy cuts, LGBT pander, empty legacy.
Axis 2 Ekonomi (12-22): no-bailout double standard, Petronas ATM, IMF boy who lost 1998, PTPTN lock-in, Petros limbo, Energy Asia/F1 theater, private deals, RM1.3T paid by rakyat, Soros scapegoat, Perwaja silence, ringgit sideline.
Axis 3 Peribadi (23-33): ascetic persona (Jung's law), tilam/Saiful/Munawar one-answer, monolith denial, eternal victim, black-eye sainthood, MCKK stage since 15, Nurul Izzah shadowed, Wan Azizah operator, unknown self, 99 locked rooms = BANGANG operating cost, persona-as-self.

Collapse line for the set: "Acah bukan strategi dia. Acah adalah identiti dia." — penipu biasa tipu orang lain; dia tipu diri sendiri dulu, lepas tu orang lain percaya.

## Final user journey (verified end-to-end)

1. Listing `/world/politics/shadow/` — Anwar card has gold CTA "→ 33 Bayang Penuh — Klik Untuk Analisis Lengkap"
2. Click → `/politics/shadow/anwar-ibrahim` → 200 (static page serves; SPA route exists but is shadowed)
3. 33 shadow cards numbered 01/33–33/33, three axis labels, filter works
4. `/world/politics/shadow/anwar-ibrahim` also 200 — two doors, one page

Commits: `0b5b432` (article v2) → `d00f0d8` (33-bayang SPA + route + card link). Deploy receipts: `20260821T081423Z`, `20260821T094001Z`.
