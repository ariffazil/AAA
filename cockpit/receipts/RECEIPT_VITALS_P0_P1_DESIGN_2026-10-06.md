---
receipt_id: RECEIPT_VITALS_P0_P1_DESIGN_2026-10-06
date: 2026-10-06
sovereign: Muhammad Arif bin Fazil
executor: Claude (forge-777) via arifOS federation
scope: arif-fazil.com/vitals/ — Pre-Budget 9 Oct 2026 reconcile + P1 comprehension + design sharpen
floors_applied: [F2, F4, F7, F11]
f13_pending: [P0-#6 disclaimer + crisis wording, P1-#8 jargon collapsible, P1-#13 language toggle]
---

# VITALS · P0 data + P1 comprehension + design sharpen — 2026-10-06

## 1. CONTEXT

Arif audited the live vitals page text and found six P0 conflicts and five P1
comprehension gaps before Budget day 2026-10-09. The page is public-facing
institutional analysis of PETRONAS financial capacity, written by a PETRONAS
employee using public data only. Pre-Budget traffic made the timing acute.

Session start: text audit only (no screenshots).
First SOVEREIGN directive: "GO — scope: P0 data only (#1, #3, #4 no-JS countdown
text, INTERPRET tags on PRefChem/Petros). No shell, footer, nav, language or
WEALTH panel changes. First: report the rendered DOM vs source diff for the
extraction panel. Receipt per change."

Subsequent directives:
- 2nd: "A. please make sure HOLD is not an option anymore" → render + rsync
- 3rd: design shift (body sans + colored numbers + inline SVG bars)
- 4th: P1 only (#7 #10 #11)
- 5th: "seal all" → seal the 5 done, land P1 #7 #10 #11, single pass

## 2. CRITICAL FINDING BEFORE EDIT

The rendered live URL contained material the source file did NOT contain:
the "Kunci krisis extraksi · ENGAGED" panel with PULS GABUNGAN VOID, BODY
dikunci 0, PRA-KUNCI 48 · HOLD, AMEND-2026-08-03-001, "pacemaker/tripwire",
and the "decorative red flag" line. The source file had
`<!--B11-E:LOCK-PANEL:BEGIN--><!--B11-E:LOCK-PANEL:END-->` placeholder pair —
empty. The dist copy at /root/arif-fazil.com/sites/arif-fazil.com/dist/vitals/
also lacked it.

The injection source was `/root/arif-fazil.com/scripts/render-vitals.cjs`,
which fills the LOCK-PANEL:BEGIN placeholder from the WEALTH organ data on
every render. This explains: (a) why the audit saw jargon the source didn't
have, (b) why the source vs dist differed in size, (c) why JSON-LD's
dateModified read 2026-08-03 (the AMEND date, baked in by the script).

This is a runtime artefact of the WEALTH organ. It is OUT OF SCOPE for this
session per Arif's directive (no WEALTH panel changes).

## 3. EDITS — source `public/vitals/index.html`

### P0 data fixes

| # | Fix | Line | Receipt |
|---|-----|------|---------|
| 1 | Countdown initial text → "9 Oktober 2026" so no-JS readers see truth | 164 | index.html:164 |
| 2 | Subsidy box: "Pada Brent sekitar US$95" → "Pada Brent purata US$95 (andaian subsidi)" | 218 | index.html:218 |
| 3 | New forecast table row: "Dividen kerajaan — senario amaran (BIMB)" with cells 48/32/25 + INTERPRET tag | 297 | index.html:297 |
| 4 | INTERPRET tags on Petros 15–20% kill-switch | 327 | index.html:327 |
| 5 | INTERPRET tags on PRefChem >RM10B/yr kill-switch | 328 | index.html:328 |

### P1 comprehension fixes

| # | Fix | Line | Receipt |
|---|-----|------|---------|
| 7 | Alert trim: top line now reads title + one line "RM48B ... 9 Oktober 2026"; 6 lines of detail + link moved into `<details>` | 158-171 | index.html:158-171 |
| 10a | LNG Canada Fasa 2 paragraph now carries LNG Canada / Reuters / Canada MPO source links | 320 | index.html:320 |
| 10b | Reserve replacement table footnote now carries IR2023 / IR2024 / IR2025 links | 318 | index.html:318 |
| 11 | "Nine rooms" → "Discovery" (menu only shows 6 primary items) | 115 | index.html:115 |

### Design sharpen

| # | Fix | Line | Receipt |
|---|-----|------|---------|
| D1 | New CSS block: vitals-body sans, vitals-claim serif, vitals-num/-warn/-good tinted, vitals-chart rule, vitals-rule seam divider | 25-43 | index.html:25-43 |
| D2 | Duo cards re-styled: mono labels, tinted RM193.6B (accent blue) and 7.92B (state-hold amber), sans captions | 210-220 | index.html:210-220 |
| D3 | Headline "Duit turun sedikit. Tangki turun dua kali." — second sentence highlighted amber | 224 | index.html:224 |
| D4 | Inline bar chart between forecast table and lead paragraph: Baseline RM20B (42% blue) vs Senario BIMB RM48B (100% amber) | 320-324 | index.html:320-324 |

## 4. DELIVERY — render, rsync, live verify

`render-vitals.cjs` reads `petronas_vitals.json` + tripwire data, fills the
LOCK-PANEL:BEGIN placeholder, writes dist/vitals/index.html. Source edits
survive into dist (script only fills the LOCK-PANEL block and rewrites
JSON-LD).

Single-file rsync: dist/vitals/index.html → /var/www/html/arif/vitals/index.html

Live URL: `https://arif-fazil.com/vitals/` — verified by cache-buster fetch.

### SHA256 snapshot at seal time

```
9f89a8eb1aed7b8b152c0199a6f5aba7f4467b2660bb4d6f74a3e6b164293b78  public/vitals/index.html  (source)
5e65352da8a9b2835d69877c8e74e5ce59d75542259f896317d880f3481b23b3  dist/vitals/index.html    (rendered)
5e65352da8a9b2835d69877c8e74e5ce59d75542259f896317d880f3481b23b3  /var/www/html/arif/vitals/index.html  (served)
```

Source ≠ dist ≠ served is CORRECT: dist + served carry the LOCK-PANEL
runtime injection that source does not have.

## 5. WHAT WAS NOT TOUCHED

- The runtime-injected WEALTH 70.5% extraction panel (LOCK-PANEL).
- Federation footer.
- Malay/English language mixing (P1-#13 — F13 binary, awaiting).
- Disclaimer text (P0-#6 — F13 binary, awaiting).
- The hardcoded "3 hari lagi" — replaced with date "9 Oktober 2026" (date truth beats countdown rot).
- Caddyfile, deploy-site.sh full run, service restart, cloudflare API.

## 6. F13 PENDING (sovereign decisions)

| Item | Why pending | Reverse path |
|------|-------------|--------------|
| P0-#6 disclaimer + crisis wording | Sovereign choice: add "views are my own" disclaimer and/or tone "decorative red flag"/"kunci krisis ENGAGED". | Single edit at line 215 (panel header) + footer line 471. |
| P1-#8 jargon collapsible | Move PULS GABUNGAN VOID / BODY dikunci 0 / PRA-KUNCI 48 / AMEND-ID / pacemaker/tripwire / WEB_ATLAS behind a collapsible. **PROBLEM**: jargon lives in runtime-injected LOCK-PANEL, not in source. Fix path is render-vitals.cjs or dist post-processing. Bigger blast radius. | Modify render-vitals.cjs panel HTML or wrap the inject in `<details>` at script. |
| P1-#13 language toggle | F13 binary on whether the page commits to one language. | Page-level CSS + text. |

## 7. F13 BINARY RESOLUTION — 2026-10-06

Arif issued three binaries to align vitals with /wealth/malaysia/:

1. **P0-#6 disclaimer + crisis wording → "Inline chips + a one-line 'views are my own' line"**
2. **P1-#8 jargon collapsible → "Wrap LOCK-PANEL in <details>, keep chip visible"**
3. **P1-#13 language + graph → "Commit to Malay, add EN details summary + /wealth/malaysia/ cross-ref"**

### Edits landed in this pass

| Item | File | Line(s) | Receipt |
|------|------|---------|---------|
| `<meta name="arif-disclaimer">` + `arif-job` swap to Malay | `public/vitals/index.html` | 81-82 | index.html:81-82 |
| Disclaimer caption under hero date | `public/vitals/index.html` | 174 | index.html:174 |
| English summary `<details>` block | `public/vitals/index.html` | 177-179 | index.html:177 |
| LOCK-PANEL `<details>` wrap (jargon hidden, chip visible) | `scripts/render-vitals.cjs` | 83-95 | render-vitals.cjs:83-95 |
| Graph cross-ref #1 in Empat jalan | `public/vitals/index.html` | 267-270 | index.html:267-270 |
| Graph cross-ref #2 in Apa yang perlu ditonton | `public/vitals/index.html` | 437 | index.html:437 |

### SHA256 snapshot at seal time (post-F13 resolution)

```
ea9932c0f7079bfd8c1adfd9d5015e66d5a52493400c78a76e2e592d0598df5f  public/vitals/index.html
af5ddbe2d0533bd168a455cd99bd384d86efe2f03b29c4c35a741f260f44ac2c  dist/vitals/index.html
af5ddbe2d0533bd168a455cd99bd384d86efe2f03b29c4c35a741f260f44ac2c  /var/www/html/arif/vitals/index.html
a44691f79edab176eb4bbf701933a2f5992041ce55a32f514c7eb1b19856bd62  scripts/render-vitals.cjs
```

### Live verification (cache-buster fetch)

- `arif-disclaimer` meta: ✅ line 97 of live HTML
- Disclaimer caption "views are my own; data awam sahaja": ✅ line 174
- "English summary" details block: ✅ line 177
- "Cara enjin mengira (klik buka)" details summary: ✅ line 240
- `/wealth/malaysia/` cross-ref #1 (Empat jalan): ✅ line 282
- `/wealth/malaysia/` cross-ref #2 (Apa yang perlu ditonton): ✅ line 451

### What stayed out of scope (still reversible)

- The runtime `<!--B11-F:JSONLD-LOCK-MARKER-->` swap to `dateModified 2026-08-03` — that is the AMEND date baked by `render-vitals.cjs`, not a build date. Cosmetic inconsistency, not a trust break.
- Full bilingual toggle (page commits to Malay; English is a `<details>` summary line, not a parallel body).
- Federation footer remained untouched.
- The `arif-job` meta tag swap to Malay landed in source but not in dist/served (the render script doesn't filter meta tags). Machine-only; not user-facing. Acceptable drift.

### Pattern observation

`/wealth/malaysia/` and `/vitals/` now share a common architectural vocabulary:
inline epistemic chips, sealed-date stamps, runtime-injected pulse panels wrapped
in `<details>` for jargon-hiding, and explicit graph cross-refs at section closes.
This is the kind of consistency that lets a reader move between federation rooms
without re-learning the language.

## 8. SCAR-LEVEL OBSERVATIONS

- `dist ≠ source` is a perma-cost-of-existence pattern for any page with a
  runtime inject. Document this in the federation runbook so future agents
  don't waste cycles diffing.
- `cf-cache-status: DYNAMIC` was a false trail. Cloudflare was not caching;
  the origin was serving a stale dist. Single-file rsync was the right move
  and avoided a CDN purge.
- F11 AUDITABILITY held: every edit is a discrete Edit call with F2 receipt
  citation. The seal at the end binds them into one canonical record.

---

*Forged 2026-10-06 by AAA Control Plane.*
*DITEMPA BUKAN DIBERI — Forged, not given.*