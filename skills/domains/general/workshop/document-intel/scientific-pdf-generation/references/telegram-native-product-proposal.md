# Telegram-Native Product Proposal (3-in-1) — Mode B Pattern

Proven 2026-08-31: arifOS "Tiga Produk AI Telegram-Native" — 13 pages, 57KB, weasyprint, dark/gold Mode B. Requested as "business proposal and market study and potential valuation and business strategy. 3 in 1."

## When to use

Arif (or Syed via Arif) asks for a proposal / valuation / market study / business strategy for Telegram-native AI products. "3 in 1" = ONE PDF covering multiple products, each with its own proposal + market study + valuation + strategy section.

## User preferences (encoded, from 2026-08-31 session)

- **"Just give me pdf."** — Deliver the PDF artifact directly. Keep the chat message short (≤8 lines: file + one-line summary per product + recommendation). Do NOT pitch the product in chat first and offer the PDF after — he corrected this exact sequence.
- **"Manusia nak satu apps ja."** — Every product must be Telegram-native. No app sprawl, no "serabut apps". The AI agent IS the product; Telegram is the single channel.
- **User-based, not institution-based** — price RM79–199/bulan per user/coach/business, NOT enterprise contracts. Frame valuation that way (bottom-up ARR, not sales pipeline).
- **"Future is ai agent yang pakai apps tu."** — Lead with what the agent does autonomously, not feature lists.
- **BM document body** with English business terms; dark/gold Mode B aesthetic (same family as SADO pitch decks).

## Document spine (3-in-1)

1. **Cover** — kicker "Ditempa Bukan Diberi", title, badge listing kernel/MCPs, prepared-for + date + "dokumen sulit"
2. **TOC** — numbered sections
3. **Exec summary** — thesis box + product table (Produk / Pengguna / Harga / ARR Tahun 3 asas / Nilai asas) + "why 3 products one kernel" bullets
4. **Market** — "Kenapa Telegram + AI Agent?" — Malaysia numbers table with sources + thesis box
5. **Per product (repeat)** — Product tag → Proposal (with an "Yang sudah terbina" evidence box — proof, not promises) → Market study (sourced numbers + pesaing + kelebihan) → Valuation (bear/base/bull table) → Strategy (Fasa 1/2/3 + moat)
6. **Portfolio** — combined scenario table, unit economics (90%+ margin), "mengapa bukan institusi"
7. **Realiti eksekusi** — 90-day plan table (Minggu × Produk columns) + order-of-execution musyawarah box
8. **Risiko & mitigasi** — table with kebarangkalian/kesan/mitigasi + "Prinsip besi" box (F1/F2/F5/F9/F13)
9. **Sumber & metodologi** — external sources (web), internal federation sources, valuation method + F2 note

## Valuation methodology (bottom-up)

- **ARR = users × blended price × 12.** Blend tier prices for the base case (e.g. RM99 + RM199 → ~RM149 blended).
- **Multiples: 3x bear / 4x base / 5x bull ARR** — early bootstrap SaaS range.
- Always label: `[ANDAIAN]` on internal estimates, note "bukan tawaran sebenar", add F2 disclaimer (no fabricated numbers).
- Portfolio value = sum of per-product ARR × weighted multiple; show bear/base/bull rows.
- Include a **unit economics table** (VPS, API per-user, payment gateway, margin 90%+) to justify multiples.

## Malaysia market anchors (sourced Aug 2026 — re-verify before reuse)

- Telegram MY: ~8–10M users (24–30% internet population) — Hashmeta
- Fitness MY: USD 370M (2025) → USD 692M (2034), CAGR 7.2% — Report Cubes; SEA fitness USD 2.68B → 4.56B (2031), 9.24% — Mordor Intelligence
- Bursa retail CDS account openings 2024–25: Sabah +89.7%, Sarawak +61.9%, Terengganu +48.5% — The Star, 30 Aug 2026
- LHDN e-Invoice: Phase 4 1 Jan 2026 (RM1–5M), Phase 5 1 Jul 2026 (RM500k–1M); <RM1M exempt
- SMEs: ~1.17M, 97.4% of businesses — DOSM

## arifOS product-line context (for future proposals)

- **Product 1 — AI Coach** (RM99/bulan per coach): WELL MCP :18083 (31 tools) + arifOS kernel. Pilot = Syed / D'Popeye / SADO group. WELL is currently MOCK/test biometrics — state honestly, do not claim live readiness.
- **Product 2 — Wealth Trading** (RM99–199/bulan): WEALTH MCP :18082 (11 tools) + gold API :3456 + XAUUSD stack (OANDA, ccxt, backtrader). "Kalah semua IB trading group" via auditable track record, chart-first, paper-trade gate. Regulatory: education/analysis only, F13 sovereign gate.
- **Product 3 — Business Intel** (RM79–149/bulan): nasilemak engine v4 proof (26 days: RM16,482 revenue, RM8,456 profit, 51.3% margin). e-Invoice compliance as hook.

## Render & verify

- weasyprint HTML → PDF (13 pages renders in seconds). Inline CSS, dark theme, tables with alternating rows. No emoji (weasyprint drops them).
- Verify after render: `pdftotext file.pdf - | grep -cE 'PRODUK [123]|PENILAIAN|STRATEGI'` and grep valuation numbers — confirms sections and tables survived, catches silent layout failure without vision.
