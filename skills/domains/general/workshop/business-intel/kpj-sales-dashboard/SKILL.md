---
name: kpj-sales-dashboard
version: 1.1.0
author: hermes
license: MIT
description: "KPJ Excel sales export → BM summary + dashboard PDF + product profit matrix."
metadata:
  hermes:
    tags: [kpj, sales, dashboard, pdf, excel]
    related_skills: ["business:nasi-lemak-sales"]
triggers:
  - "KPJD"
  - "KPJ "
  - "transaction excel"
  - "dashboard pdf"
  - "Trans_20"
---

# KPJ Sales Dashboard

## When to Use

A payment-gateway Excel export for a KPJ stall arrives (filename like `14 AUG 2026 KPJD.xlsx`, sheet `Trans_YYYYMMDD`) — typically from the "Mohd"/Izzu DM lane. Deliver a chat summary first, then the established dashboard PDF. Corporate-context questions (KPJ leadership, tenancy, vendor policy) also route here — see `references/kpj-context-2026-08.md`.

Recurring task: user sends periodic payment-gateway Excel exports (e.g. `14 AUG 2026 KPJD.xlsx`) from the KPJ stall(s). Two deliverables, in this order:

1. **Quick BM summary in chat** — product table + payment-method table + total + one insight line.
2. **Dashboard PDF in the established format** — run the existing generator. NEVER hand-build a new format.

## The canonical script

`/root/izzu-automation/generate_dashboard.py`

```bash
cd /root/izzu-automation && python3 generate_dashboard.py "<input.xlsx>" "<output.pdf>"
```

- Location auto-detect from filename/merchant: `KPJAP` → KPJ Ampang Puteri (orange), `KPJR` → KPJ Rawang (green), `KPJD` → KPJ Damansara (blue), else regex `KPJ[\s-]*(\w+)`, else WebOfProjects-VM. Detection iterates `sorted(locations.keys(), key=len, reverse=True)` so KPJR/KPJAP win over the KPJ prefix (patched 2026-08-17). **If you encounter a new KPJ venue suffix not in this list, patch the `detect_location()` dict in the script first** — the default fallback writes generic "KPJ" which is wrong when the file is clearly KPJR/KPJAP.
- Date range auto-detect from filename (`14 AUG 2026`, `12-14 AUG 2026`, etc.).
- Output: 4-page PDF, 6 charts, ~350KB. Established format — replicate, don't redesign (user rejects format changes).
- If the script isn't at that path: `search_files` for `generate_dashboard.py` under /root BEFORE rebuilding anything. session_search returned nothing for this workflow (verified 2026-08-15) — file search is the reliable discovery path.

## Excel schema (payment-gateway export)

Sheet: `Trans_YYYYMMDD`. Key columns (0-indexed in openpyxl row tuples):

| Idx | Field | Notes |
|---|---|---|
| 1 | Date | `D-M-YYYY H:MM:SS AM/PM` |
| 4 | Merchant Name | e.g. `WebOfProjects-VM(Cheras)` |
| 12 | Payment Method | DuitNow QR / TNG QR (MYR) / GrabPay QR / Boost QR |
| 16 | Amount | MYR, per transaction (no qty column) |
| 18 | ProdDesc | truncated ~20 chars, e.g. `BURGER BLACKPEPPER C` |
| 25 | Status | `Success` — verify all rows Success |

## Quick-summary pattern

```python
wb = openpyxl.load_workbook(path, data_only=True)
ws = wb[wb.sheetnames[0]]
rows = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0] is not None]
# aggregate: Counter by ProdDesc (18) and Payment Method (12), sum Amount (16)
```

Present: txn count + Status check, total RM, product table (Kuantiti | Jualan), payment table (count | RM), one insight line (peak hours / top seller).

**Product-name normalization:** singular/plural variants exist (`CHOCO ROLL MUZIC` / `CHOCO ROLLS MUZIC` = same item). Merge before presenting, footnote the merge.

## User preferences (this lane)

- **NO voice notes — text/PDF only.** Explicit instruction 2026-08-15.
- Full BM, terse, answer first, no preamble.
- "dashboard yang dah biasa" = the izzu-automation script output. Find it and run it — don't ask which format.

## Multi-venue file discipline (KPJ has multiple branches)

Venue is identified by the **filename suffix**, NOT the merchant name in the data. Both KPJ Damansara and KPJ Rawang currently report under the same `WebOfProjects-VM(Cheras)` account and the same merchant code `M46098`. The SaaS data is identical-looking — separator comes from the file and folder only.

| Suffix | Venue | Output folder | Color in PDF |
|---|---|---|---|
| `KPJD` | KPJ Damansara (est. Aug 2026) | `/root/izzu-automation/dashboard_<date>_KPJD.pdf` (root) | blue (`#0984e3`) |
| `KPJR` | KPJ Rawang (live 16 Aug 2026) | `/root/izzu-automation/kpjrawang/dashboard_<date>_KPJR.pdf` | green (`#00b894`) |
| `KPJAP` | KPJ Ampang Puteri (live 20 Aug 2026) | `/root/izzu-automation/kpjampangputeri/dashboard_<date>_KPJAP.pdf` | orange (`#e17055`) |
| `TransactionReport_*` (no suffix) | diagnose by elimination | venue folder after manual rename | rename to `<D> AUG 2026 <VENUE>.xlsx` in /tmp first |

**If you see a new suffix, create its folder first, before generating the PDF.** The default root is reserved for KPJD.

When Arif opens a new venue, expect a 3-day "calibration window" where sales are ~5-10% of the established venue. Don't frame a 3-transaction day as failure — frame it as "before customer awareness." User explicitly surfaced hurt about a 3-txn day (2026-08-17). Acknowledge the feeling FIRST (one short line), then offer the comparative frame. Do not skip to engineering reframe.

## Emotional handling pattern for this lane

When Arif surfaces hurt about a number (sales, transactions, comparisons with another venue):

1. One sentence acknowledging the feeling — name it, don't explain it.
2. **One** numbered question that pulls him back into the operator chair: target number, expected ramp window, or which single decision he has to make today.
3. Do not over-explain, do not lecture on calibration curves, do not preempt with frameworks. He wants a partner, not a textbook.

Wrong (this session, ~21:51): reaching for "reality check" / "expectation management" / "three pieces of advice" before acknowledging.

### Product Profit Matrix Analysis

When the user asks about product sales volume, margin, or profit (e.g. "berapa banyak burger", "gross profit drinho"), run a per-product query across ALL available KPJD Excel files, then present:

1. **Daily breakdown** — qty per day, revenue, cost, profit
2. **Summary** — total unit, total revenue, avg price, profit/unit, margin %, est. 30-day volume, est. monthly profit
3. **One insight line** — trend, spike, or opportunity

### Building the Profit Matrix

After querying individual products, compile a **sorted Profit Matrix** (descending by profit/bulan) showing all categories. Include:
- Known-margin products (from the table below)
- Loss leaders (zero profit, traffic drivers)
- Proposed/target products (mark as "NEW" or "target")
- Products with no margin data (mark as "NO MARGIN" or "???")

The matrix serves as the single source of truth for mesin profitability. When user provides new margin data, re-sort and re-present.

**Key metric: Net Profit = Gross Profit − ~RM 400/bulan kos tetap (elektrik, sewa, SIM, maintenance).**

### Query pattern (use terminal, NOT execute_code — openpyxl unavailable in sandbox)

```python
import openpyxl, os, glob
files = sorted(glob.glob("/root/.hermes/cache/documents/*KPJD*.xlsx"))
# For each file: extract rows, filter by product keyword, aggregate
# Key columns: [1]=Date, [16]=Amount, [18]=ProdDesc
# Normalize: "CHOCO ROLLS MUZIC" → "CHOCO ROLL MUZIC", "BURGER BLACKPEPPER C" → "BURGER BLACKPEPPER"
```

### Known product margins (KPJD, as of 2026-08-20)

| Product | Selling Price | Cost (Lotus's) | Gross Profit/Unit | Margin |
|---|---|---|---|---|
| Burger (all types) | RM 7.90 | RM 5.33 | RM 2.57 | 32.5% |
| Hotdog (all types) | RM 7.90 | RM 5.33 | RM 2.57 | 32.5% |
| Choco Rolls Muzic | RM 3.90 | RM 2.40 | RM 1.50 | 38.5% |
| Spritzer Mineral Water | RM 1.90 | RM 0.66 | RM 1.24 | 65.3% |
| Milo | RM 2.90 | RM 1.60 | RM 1.30 | 44.8% |
| Coconut Water (Karta) | RM 3.90 | RM 2.40 | RM 1.50 | 38.5% |
| ZUS Latte / Boss Blend | RM 4.90 | RM 3.90 | RM 1.00 | 20.4% |
| Milk (Strawberry/Chocolate) | RM 1.90 | RM 1.30 | RM 0.60 | 31.6% |
| Drinho Sparkling | RM 2.90 | RM 2.00 | RM 0.90 | 31.0% |
| Honey Roasted Cashew | RM 4.57 | RM 3.60 | RM 0.97 | 21.2% |
| Salted Almonds | RM 4.50 | RM 3.60 | RM 0.90 | 20.0% |
| Sambal Nyet | RM 15.90 | RM 12.60 | RM 3.30 | 20.8% |
| Rendang Nyet | RM 16.90 | RM 13.60 | RM 3.30 | 19.5% |
| Orange Minutemaid | RM 2.12 | ~RM 2.12 | RM 0 (loss leader) | 0% |
| Lemon Fuzetea | RM 2.20 | ~RM 2.20 | RM 0 (loss leader) | 0% |
| Sandwich (Tuna/Telur/Sardin) | RM 3.90 | RM 3.10 | RM 0.80 | 20.5% |
| Buah Potong (vacuum sealed) | RM 6.60 | RM 5.40 | RM 1.20 | 18.2% |

**When new margin data arrives from the user, PATCH this table immediately.** The user provides cost prices verbally (e.g. "Drinho saya beli di Lotus's harga RM2") — extract, compute margin, add to table.

**Conservative estimation preference** (2026-08-20): When proposing targets for new/low-volume products, default to **1 unit/day** (not 2). User explicitly chose conservative over ambitious: "Saya setuju dengan conservative estimate 1 unit sandwich dan 1 unit buah potong." Use 1/day as baseline, mention 2/day only as stretch scenario. This prevents over-forecasting for products with no or low historical data.

**Product packaging notes:**
- Buah Potong: vacuum sealed from manufacturer with MESTI and HACCP certification. Sells at RM 6.60, cost RM 5.40. Suitable for standard spring-coil vending machine (no chill required). Premium health-conscious segment.
- Sandwich: Tuna/Telur/Sardin variants at RM 3.90. Pricing attack on FamilyMart (RM 5+). Targets budget-conscious staff.

### Sandwich pricing strategy

Sandwich RM 3.90 is a deliberate **undercut play** against FamilyMart (RM 5+). When presenting this product, frame as market positioning (not just "another product"). The sandwich fills the gap between impulse drinks (RM 1.90–2.90) and burgers (RM 7.90), capturing the "want something substantial but not burger" segment.

### Loss leader strategy

Minutemaid, Lemon Fuzetea, Tropical Minute Maid, and Ice Lemon Tea are **zero-margin loss leaders** — priced at cost to drive foot traffic. Frame them as traffic drivers, not low-profit items. Cross-sell effect: RM 2.12 Minutemaid customer may buy RM 7.90 burger.

### Multi-day aggregation

When user sends multiple Excel files at once, process ALL in a single pass:
- Deduplicate by date (two files for same date → count once)
- Check sheet dates inside the file, not just filename
- Sort results by date ascending
- Present cumulative totals AND per-day breakdown

## Pitfalls

- Not the nasi-lemak business — orders/claims go to `business:nasi-lemak-sales`. This skill = KPJ QR-transaction exports only.
- Each row = 1 unit. Volume = row count per product, not any qty field.
- Midnight–3 AM transactions belong to the SAME export date — keep in the day's total (they can be ~20% of revenue).
- **KPJR detection is now stable** (patched 2026-08-17). Filenames with `KPJR` will detect as `KPJ Rawang` (green) in both script output and PDF header. If a future KPJ venue opens and the PDF still says generic "KPJ", patch `detect_location()` to add a new key — list it BEFORE the bare `KPJ` fallback, and the script's `sorted(...key=len, reverse=True)` loop will pick the longest match first.
- Don't compare trial-day numbers of a new venue to an established venue head-to-head. The user will read "RM 23.70 vs RM 239.30" as personal failure. Always pair with the calibration window note above.
- **"Mana pdf?" is not an open-ended search** (2026-08-18). When user asks for a PDF in the KPJ lane, default to the established dashboard output path (`/root/izzu-automation/` or `/root/izzu-automation/kpjrawang/`). Don't scan /tmp, shadow files, etc. unless user specifies a non-KPJ context.
- **PDF delivery failure pattern — ACT on first repeat, not sixth** (2026-08-18 → 2026-08-23). User asked "mana pdf" ~9 times across 3 days. The `MEDIA:` line sends but the file does not reach the user's phone. Protocol: (1) first "mana pdf" → re-send MEDIA: once; (2) second "mana pdf" → STOP re-sending blind. The failure is real and repeating. Ask ONE binary question ("ada PDF pernah sampai? yes/no") to isolate gateway-vs-network, and offer JPG fallback (`pdftoppm -png -r 110 file.pdf prefix`) in the same message. Do not wait for the third ask. User explicitly said "Penatlah setiap kali kena tanya pdf" — fatigue is the signal to escalate the debug, not to retry the same delivery.
- **User wants PDF format even when delivery fails** (2026-08-23). When offered image fallback, user replied "Saya nak dalam pdf" — keep sending PDF as primary. Do NOT permanently switch to images on your own initiative. The delivery bug is the thing to fix, not the format.
- **Unlabeled TransactionReport files** (2026-08-23). Files named `TransactionReport_20260823_HHMMSS.xlsx` (no venue suffix) arrive sometimes. Diagnose venue by elimination: check which venues already have that date's dashboard, then match product mix. Copy to `/tmp/<D> AUG 2026 <VENUE>.xlsx` before running the generator so `detect_location()` produces the right header. State the assumption to the user and ask them to correct if wrong.
- **Malaysian public-holiday calendar effect** (2026-08-23). Slow weekends/holidays precede long weekends (people take Monday leave before a Tuesday holiday — hospital traffic drops Sat–Tue, rebounds Wednesday). Before diagnosing a sales dip as a trend, check the MY public holiday calendar. Frame: "calendar effect, not demand collapse; compare against Wednesday+ after the break." Also flag stock-prep opportunity (restock Nyet/burger during quiet days for the rebound).
- **Telegram PDF delivery is invisible sometimes** (2026-08-18). After `MEDIA:` send, if user says "Mana?" twice, the file landed in attachment view, not inline. Offer: re-send as MEDIA:, convert to JPG, or dump key numbers as plain text.
- **Trial-day emotional pattern** (2026-08-17, KPJR launch). When user says "sadly, only N transactions" for a NEW venue, the painful comparison is implicit (vs established venue). The right move: (1) one short acknowledge, (2) one factual comparison with calibration window context, (3) one operator question. Do NOT open with framework lectures.
- **execute_code sandbox lacks openpyxl** (2026-08-20). Always use `terminal` tool for KPJD Excel analysis, never `execute_code`. The sandbox interpreter doesn't have openpyxl installed.
- **Nyet supply = demand bottleneck** (2026-08-20). Sambal/Rendang Nyet has highest profit/unit (RM 3.30) but all sales clustered in 2 of 9 days due to stock shortage. When user mentions "short supply" on a high-margin product, flag the supply constraint as the primary revenue lever — not marketing or placement. Fix stock = fix profit.
- **Top-up timing on long weekends** (2026-08-23): when a public holiday falls on Tuesday, top up on SUNDAY, not Monday/Tuesday. Monday is a de-facto leave day (staff back at hospital), holiday-Tuesday hospital access may be restricted, and Wednesday is the rebound peak — a Sunday top-up covers all three. Stock-out days at Rawang cratered revenue ~4x vs stocked days (RM 24 vs RM 92–168).
- **Corporate-news verification for KPJ context** (2026-08-23): leadership/vendor-policy questions in this lane can affect the user's tenancy. Verify via the user's URL with curl+UA (see `references/kpj-context-2026-08.md` for the proven recipe; web_extract fails on theedgemalaysia.com and firecrawl may be out of credits). Never assert causation between the user's advocacy letter and a resignation — state timing, flag as coincidence-or-not. MD/OIC succession table also lives in that reference (pattern: KPJ board prefers external MD hires over promoting the OIC — Norhaizam 2022–23 is the precedent).

## References

- `references/detect-location-patch.md` — patch recipe for `detect_location()`
- `references/kpj-context-2026-08.md` — empire state per venue, KPJ MD/OIC succession table, vendor-risk window, news-verification recipe
