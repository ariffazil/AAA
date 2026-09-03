# PETRONAS Site Updates — Master Patch Index

**Session:** SEAL-d7d3fde881a74721
**Date:** 2026-08-26 (Wednesday, MYT)
**Author:** 333-AGI Δ Mind (arifOS Federation)

---

## 4 patches ready-to-deploy

| # | File | Target surface | Priority | Effort | Status |
|---|------|----------------|----------|--------|--------|
| 1 | `01-vitals-re-seal-patch.md` | /vitals | 🔴 P0 | 4-6 hr | READY |
| 2 | `02-petronas-dna-v1.2-update.md` | /world/makcikgpt/petronas-dna | � P1 | 1 hr | READY |
| 3 | `03-world-signal-sync.md` | /world | 🔴 P0 | 1-2 hr | READY |
| 4 | `04-propa-decision-memo.md` | /propa | � P1 | 1 hr | READY |

---

## Patch 1 — /vitals Re-seal (P0, 4-6 hr) — HIGHEST IMPACT

**Why:** /vitals is the canonical institutional intelligence surface. Sealed 2026-08-03 — overdue by 23 days. This session generated new analysis (BOD chronology, 12 hidden risks, SOE corpus, JV walk-away, Monte Carlo, runway) that should be on this surface.

**8 sub-patches in the file:**
1. Update seal date banner (2026-08-03 → 2026-08-26)
2. Refresh LIVE MARKET PROXIES block (Brent $85.48, MYR 4.047)
3. Add BOD Chronology section (after Pacemaker Panel)
4. Add 12 Hidden Risks section (after plain language)
5. Add SOE Comparison Corpus section
6. Add JV Partner Walk-Away Map
7. Add Monte Carlo + Cash Runway section
8. Add Sabah MA63 footnote on Tripwire #8

**Source files for cross-linking:**
- `/root/AAA/forge_work/2026-08-26-petronas-bod-dossier/petronas-bod-chronology-2023-2026.pdf`
- `/root/AAA/forge_work/2026-08-26-petronas-rakyat-dossier/petronas-full-reality-rakyat-dossier.pdf`

---

## Patch 2 — petronas-dna v1.2 Update (P1, 1 hr)

**Why:** The civic PETRONAS piece is 8 weeks old (1 Jul 2026). Needs cross-link to /vitals + post-Aug 2026 evidence + dossier link.

**4 sub-patches:**
1. Update frontmatter (v1.1 → v1.2)
2. Insert cross-link banner at top
3. Add "Post-Aug 2026 Update" section at end (BM)
4. Update final seal line

---

## Patch 3 — /world Signal Sync (P0, 1-2 hr)

**Why:** Brent, MYR, KLCI values on /world are 4-10% stale vs /vitals. The 10% USD/MYR gap is severe. Also: add PETRONAS Sovereign Extraction as 6th radar signal (most important Malaysian macro indicator, currently absent).

**3 sub-patches:**
1. Sync 5 existing signal values to match /vitals
2. Add 6th signal: PETRONAS Sovereign Extraction
3. Fix "4/5 SEAL" label to honest count

**Underlying issue:** /world and /vitals may use different data pipelines. Audit `scripts/` for the radar update script and unify sources.

---

## Patch 4 — /propa Decision (P1, 1 hr)

**Finding:** /propa renders byte-identical to /vitals (verified via Firecrawl). Misconfiguration.

**Recommendation:** Option A — Canonical 301 redirect to /vitals. Lowest risk, highest clarity.

**If Option A is too aggressive:** Add `<link rel="canonical" href="https://arif-fazil.com/vitals/" />` to /propa HTML head instead.

**If Option B is preferred** (rebuild as procurement surface): content sketch in patch file.

---

## Deployment Sequence

```
1. Apply Patch 1 (vitals re-seal)         ← Highest impact, start here
2. Apply Patch 3 (world signal sync)     ← Quick win, 1-2 hr
3. Apply Patch 4 (propa decision)        ← 5-30 min depending on option
4. Apply Patch 2 (petronas-dna v1.2)     ← Civic piece, lower technical priority
5. Run: cd /var/www/html && make deploy
6. Verify: curl -I each surface, run verify-surfaces.cjs
```

---

## What I Cannot Execute Autonomously

- `make deploy` from /var/www/html (T3 territory — VPS-level deployment)
- Edits to `/etc/caddy/Caddyfile` (T3 — Caddy reload requires F13 nod per doctrine)
- Git push to remote (no remote configured; site is local-deploy)

## What You Can Hand to Me Next Session

If you want me to draft additional surface updates (e.g., /malaysia, /politics, /words essays), the pattern is the same:
1. Firecrawl fetch current content
2. Identify gaps vs this session's analysis
3. Draft patch in `/root/AAA/forge_work/2026-08-26-petronas-site-updates/`
4. Include exact FIND/REPLACE markers for surgical edits

---

## Files Produced This Session

```
/root/AAA/forge_work/2026-08-26-petronas-site-updates/
├── 00-MASTER-INDEX.md                  (this file)
├── 01-vitals-re-seal-patch.md
├── 02-petronas-dna-v1.2-update.md
├── 03-world-signal-sync.md
└── 04-propa-decision-memo.md

(plus from earlier turns in this session:)
/root/AAA/forge_work/2026-08-26-petronas-bod-dossier/
└── petronas-bod-chronology-2023-2026.pdf  (52 KB, verified PDF 1.7)

/root/AAA/forge_work/2026-08-26-petronas-rakyat-dossier/
└── petronas-full-reality-rakyat-dossier.pdf  (132 KB, 31 pages, verified PDF 1.7)
```

---

**DITEMPA BUKAN DIBERI ⚒️**

Session SEAL-d7d3fde881a74721 · 26 August 2026
All patches ready for your deployment. Apply in sequence. Ping me after to verify.
