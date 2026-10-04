# MakcikGPT Landing Page Template

Canonical: `/var/www/html/arif/makcikgpt-md/index.html`

## Structure (2026-08-09)

```text
1. Breadcrumb nav (← arif-fazil.com /world/ MakcikGPT)
2. H1 + description + meta line (article count, updated date)
3. Zen Pulse aside (WHERE AM I? / WHY CARE? / WHAT NEXT?)
4. 📰 Terkini (Latest) — newest 8 articles, newest-first, date + title + series badges
5. 🏷 Topik chips — links to each series anchor (#series-M1 etc.)
6. Series sections (collapsible <details>):
   - ⚡ M1 — Energy & PETRONAS
   - 🏛 M2 — Governance & Sovereignty
   - 🛡 M3 — Tech & AI
   - 📈 M4 — Economy & Rakyat
   - 🗳 M5 — Politics
7. Flat list (hidden, aria-hidden=true) — full chronological dump for RSS/crawlers
8. Meta footer (source of truth note + DITEMPA BUKAN DIBERI)
```

## CSS classes

- `.latest-list li` — flex row: `.l-date` (mono, 72px min-width) + `.l-title` (flex:1) + `.l-series` (right, dim)
- `.zen-reveal summary` — series header with emoji + count
- `.tag` — small pill for topic keywords per article
- `.chips .chip` — topic filter buttons

## Update protocol

When adding a new article:
1. Add to **Terkini** list (newest first, max 8 shown)
2. Add to appropriate series section(s) — cross-list if multi-topic
3. Add to **flat-list** (aria-hidden ul) at the bottom
4. Bump the article counter in the meta line ("24 articles")
5. Update the `updated` date

## Series assignments (current, 2026-08-09)

| Series | Topic | Slug prefix pattern |
|--------|-------|-------------------|
| M1 | Energy & PETRONAS | petronas-*, iran-hormuz, suriname-*, 13-sebab-* |
| M2 | Governance & Sovereignty | syaitan-*, suara-*, anak-sarawak-*, searah-*, cerita-makcik, siasatan-* |
| M3 | Tech & AI | ytl-monopoli, ilmu-bbb |
| M4 | Economy & Rakyat | ai-johor-rakyat-2026, daily-2026-07-01 |
| M5 | Politics | chennah-bangang, dap-*, anwar-jung-shadow, sam-altman-elon-musk-anwar-akal |

## Key dates in current index

- 2026-08-09: 13-sebab-taufik-kena-berhenti, syaitan-ingat-dirinya-malaikat
- 2026-08-02: suara-terlalu-siap
- 2026-07-29: anak-sarawak-bayar-pda-anak-bangla-telefon, chennah-bangang
- 2026-07-28: dap-8-tahun-bangang, anwar-jung-shadow
- 2026-07-22: searah-senyum-media-suap, searah-kekal-milik-penuh
- 2026-07-18: searah-bernama-lewat
- 2026-07-14: petronas-visi-misi
- 2026-07-13: petronas-atm-kerajaan
- 2026-07-06: ai-johor-rakyat-2026
- 2026-07-05: petronas-hive-sale, suriname-exxon-cabut
- 2026-07-01: sam-altman-elon-musk-anwar-akal, daily-2026-07-01, ytl-monopoli, ilmu-bbb, searah-followup, petronas-dna
- 2026-06-30: iran-hormuz
- 2026-06-07: cerita-makcik, siasatan-harakah
