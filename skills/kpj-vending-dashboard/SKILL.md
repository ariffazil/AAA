---
name: kpj-vending-dashboard
description: Generate PDF dashboards from KPJ hospital vending machine transaction Excel exports. Supports single-site (KPJAP/KPJD/KPJR/KPJT) and combined multi-site reports. Handles product name variants and incremental GP rate corrections.
version: 2.0.0
---

# KPJ Vending Dashboard Generator

Generate PDF performance dashboards for Izzu's vending machines at KPJ hospitals. Built from monthly payment-gateway Excel exports (`WebOfProjects-VM` xlsx, Merchant M46098). Outputs A4 PDF via weasyprint.

## Sites

Currently four active sites (per Sept 2026 data):

- **KPJAP** — KPJ Ampang Puteri (Cheras branch)
- **KPJD** — KPJ Damansara
- **KPJR** — KPJ Rawang
- **KPJT** — KPJ Tawakkal (new site — partial month 15-30 Sept only; no Aug baseline, all GP rates need Izzu's input)

Site identity comes from the **filename**, not the merchant column. The merchant string `WebOfProjects-VM(Cheras)` appears for ALL sites in the xlsx — it is the operator, not the location.

## Excel schema (from KPJ payment processor)

Single sheet (e.g., `Trans_20261005`), 32 columns. Key columns (1-indexed):

| Col | Header | Use |
|---|---|---|
| 2 | Date | `datetime.strptime(s, '%d-%m-%Y %I:%M:%S %p')` |
| 5 | Merchant Name | `WebOfProjects-VM(Cheras)` — IGNORE for site ID |
| 13 | Payment Method | DuitNow QR / TNG QR (MYR) / GrabPay QR / Boost QR |
| 17 | Amount | MYR float |
| 19 | ProdDesc | **truncated to 20 chars** — generates spelling variants |
| 26 | Status | filter `== 'Success'` only |

## File location conventions

- **Inputs (current month):** `/root/.hermes/cache/documents/*.xlsx`
- **Outputs:** `/root/.hermes/workspace/zen/izzu-brief/artifacts/Sept_<YYYY>_<SITE>_Dashboard.pdf`
- **Generators:** `/tmp/sep2026_<site>_dashboard_gen.py`
- **Source data (Aug baselines):** `/root/.hermes/workspace/zen/izzu-brief/artifacts/kpj*_gp.json`
- **Generator template (where to start a new site):** `templates/single_site_generator.md`

## Outputs

Two report types:

1. **Single-site report** — 7-page A4 PDF per site
2. **Combined multi-site report** — 5-6 page A4 PDF comparing 2-3 sites

## Single-site report — 7 pages

| Page | Content |
|---|---|
| 1 | Header + 8 KPI tiles (2x4 grid) + Monthly Trend bar chart |
| 2 | Cumulative trend (line) + Daily revenue table (30 rows) |
| 3 | Top Products bar + Payment Method bar |
| 4 | GP summary (3 big tiles) + Top 10 GP bar |
| 5 | All Products GP Detail (Page 1 of 2) — top 23 by GP |
| 6 | All Products GP Detail (Page 2 of 2) + TOTAL row |
| 7 | Hourly chart (24 bars) + Top/Bottom 5 hours |

## Combined report — 5-6 pages

| Page | Content |
|---|---|
| 1 | Header + 3 sites × 6 KPI tiles (Txns, Revenue, Avg, Days, GP, Margin) + Combined TOTAL |
| 2 | Revenue & Avg per Transaction (bar charts) + Combined GP/Margin |
| 3 | GP & Margin comparison (bar charts) |
| 4 | Daily Revenue Trend (line chart, 3 sites overlaid) |
| 5 | Payment Method Split (3 horizontal bar charts) |
| 6 | Per-Site Summary Table (includes GP, Margin columns) |

## Generation procedure

### Single-site

1. Copy the last generator for the same site from `/tmp/sep2026_<site>_dashboard_gen.py`.
2. Update: `SITE = "..."` constant, XLSX path, OUT path, page titles.
3. Aug GP rates from `/root/.hermes/workspace/zen/izzu-brief/artifacts/<site>_gp.json` provide the baseline. Per-site overrides apply (see Rates section).
4. Add `PRODUCT_ALIASES` dict mapping ALL spelling variants seen in the new month to a Title Case canonical name (which must exist in `GP_RATES`).
5. Run, then verify the PDF with `pdftotext -layout` — grep for: leftover raw variants, products on the default rate, totals.
6. Deliver via `MEDIA:/abs/path.pdf`.

### Combined

1. Copy `/tmp/sep2026_combined_3sites_gen.py` and edit the `SITES` list with the 3 (or 2) site configs.
2. GP values are **hardcoded** per site in the SITES dict (read from previous individual reports — do not recompute here).
3. Output path: `Sept_2026_Combined_<SITE_A>_<SITE_B>_<SITE_C>_Dashboard.pdf`.

## GP rates — apply incrementally as user provides them

Izzu does NOT pre-bundle all rates. The flow is:

1. Generate report with Aug rates + `DEFAULT_RATE = 1.00` for any unknown product.
2. Izzu responds with corrections line-by-line: "MILO GP is RM1.50 per unit", "Choco Rolls Muzic GP is RM1.50", etc.
3. Apply each correction literally. Update the canonical-name rate in `GP_RATES`.
4. If the product in the xlsx data is a **spelling variant** (UPPERCASE, truncated, abbreviated), add the variant to `PRODUCT_ALIASES` pointing to the canonical name.
5. Re-run, report old GP → new GP delta.
6. Repeat until Izzu says "Good job" or "Good for KPJX".

**Both keys must match:** the alias maps UPPER → Title, and the rate key uses Title. E.g., `MILO` (UPPER, from data) → `'Milo'` (Title, canonical) → `GP_RATES['Milo'] = 1.50`.

**Do NOT auto-assume rates** for products Izzu has not specified. The default 1.00 is a placeholder; if a product still shows 1.00 GP in the rendered PDF, that's a signal a rate is missing.

## Product name canonicalization (MUST run before aggregation)

The xlsx truncates `ProdDesc` at 20 chars and uses inconsistent spelling. Every report needs a `PRODUCT_ALIASES` dict before aggregation. Common variants seen:

- `CHOCOROLLS MUZIC`, `MUZIC CHOCOROLLS` → `Choco Rolls Muzic`
- `LYCHEE SPARKLING TEA`, `SPARKLING LYCHEE TEA`, `LYCHEE SPARKLING` → canonical Lychee
- `ORANGE JUICE`, `ORANGE MINUTEMAID` → `Orange Minutemaid`
- `BURGER BLACKPEPPER C`, `BURGER BLACKPEPPER`, `BURGER BLACK PEPPER` → `Burger Blackpepper`
- `BURGER SHRIMP N FISH`, `BURGER SHRIMP AND FI`, `BURGER FISH N SHRIMP`, `BURGER FISH AND SHRIMP`, `SHRIMP AND FISH BURG` → `Burger Fish Shrimp`
- `SWEETPOTATO ROASTED` → `Sweet Potato Roasted`
- `GUAVA FRESH` → `Guava Fruit`
- `SANWISH EGG` (typo) + `SANDWISH EGG` → `Sandwich Egg`
- `CHOCOROLLS MUZIC` ≠ `CHOCO ROLLS MUZIC` (typo variant)

Aliases must match **exactly**. `MILO` ≠ `Milo`. After every alias update, grep the PDF text to confirm consolidation happened.

## Layout rules (from Izzu's corrections)

- **All fonts large** — 11-12pt table rows, 20pt page titles, 22pt KPI numbers. Small fonts get rejected.
- **Grand total on the LAST page only** — never on every page.
- **Every bar carries its value label**, horizontal (not rotated 90°).
- **Use the SAME Title-Case canonical name in payment table and GP table** — don't have "MILO" and "Milo" both appearing.
- **Exclude test transactions** — known example: `'自动售货机'` (Chinese for "vending machine") in KPJT. Map via alias to `EXCLUDE_TEST_ENTRY` and skip the row.
- **Daily revenue table** has columns: Date | Revenue (RM) | Transactions | Avg / TX
- **Top/Bottom hours** — Top 5 + Bottom 5 hours, side by side
- **Combined reports need 6 KPI tiles per site** (not 4) so GP and Margin are visible. Layout: **1x4 vertical strips** (each site as one column, 6 tiles stacked), NOT 2x2 — the 2x2 grid becomes unreadable because each tile is too narrow for the font.
- **Combined report title simplification**: Izzu strips redundant words until only "Combined" remains. Default to `"<Month> <Year> · Combined"`; do not include site-name list in the title.
- **Bold site labels, thick dark-blue borders**: site-section header band uses 14pt bold, dark-blue 2.5pt border, light-blue background. KPI tiles get 1.8pt dark-blue borders on white — separates each site's columns visually.
- **2x2 grid fails for 4 sites** — only use vertical strip layout for 4+ sites.

## Date handling (real bug I hit twice)

`min()` and `max()` on raw date strings is **wrong** for filtering by date range. The string `"10-9-2026"` sorts before `"2-9-2026"`. Always parse with `datetime.strptime(s, '%d-%m-%Y %I:%M:%S %p')` FIRST, then sort by date objects.

## Critical pitfalls

- **Default rate masks bugs.** A `DEFAULT_RATE = 1.00` fallback means an un-aliased product shows a plausible-looking rate instead of 0. Always grep the rendered PDF for products still on the default before declaring done.
- **Alias key typos collapse silently.** `'SANWISH EGG'` vs `'SANDWISH EGG'` — one missing char means the alias never fires and the product stays split. Always grep the PDF for leftover variants after each run.
- **UPPERCASE vs Title Case.** Data is UPPERCASE; rate dict is Title Case. Every product needs BOTH the alias map AND the rate key. Both must be present or the lookup misses.
- **Combined report GP values are hardcoded** — they come from previous single-site reports. If rates change in those reports after, the combined report is stale. Re-run individual sites first.
- **`weasyprint` yes, `wkhtmltopdf` no.** wkhtmltopdf is NOT installed. Use `weasyprint file.html out.pdf` for HTML→PDF, and matplotlib `PdfPages` for chart dashboards.
- **matplotlib/openpyxl may need install**: `pip install matplotlib openpyxl` if not present.
- **f-string with literal `\n` breaks Python syntax** when injected via patch. Use a separate variable: `label = f"text\n{margin}"`. Bit me during 4-site combined generation.
- **`vision_analyze` may return 404 in this environment** with error "models/hermes-default is not found for API version v1main". Fall back to `pdftotext -layout` extract for verification, then `pdftoppm -r 100 <pdf> <prefix> -png -f 1 -l 1` + `read_file` of the generated PNG path to inspect layout when vision is needed.
- **Combined reports with 4 KPI tiles per site overlap visually.** Always use 6 tiles in 2x3 grid so GP and Margin show. Visual separation between site groups needs explicit `y_top - s_idx * 0.32` (not 0.30) spacing.
- **Per-site GP values in combined reports come from the LATEST individual site report.** If you re-run a single site after generating the combined, the combined is stale — re-run the combined too. Izzu notices mismatches.

## Validation (run after every regeneration)

```bash
pdfinfo <output>.pdf | grep Pages
pdftotext -layout <output>.pdf - | grep -iE "<suspicious_product>"
pdftotext -layout <output>.pdf - | head -50
# If visual layout check needed (and vision_analyze unavailable):
pdftoppm -r 100 <output>.pdf preview -png -f 1 -l 1
```

Grep checks:
- No product name variants that should have been merged
- No "1.00" GP rates (would mean missing rate)
- Date range covers expected period
- TOTAL row appears once

## Dependencies

- `openpyxl` (read xlsx)
- `matplotlib` with PdfPages backend (chart PDF)
- `numpy`
- `weasyprint` (HTML→PDF; not strictly needed for chart-only dashboards)

Install if missing: `pip install openpyxl matplotlib numpy weasyprint`.

## Context

Business: Izzu runs prepared food vending (burgers, NYET Kitchens, sandwiches, drinks) at KPJ hospitals. Competes with Family Mart & CU Mart vending machines. Edge: hot prepared food FM/CU can't replicate.

Sept 2026 baseline numbers (for sanity check after generation):
- KPJAP: 471 txns, RM2,228, GP RM647.60 (29.07%)
- KPJD: 1,058 txns, RM6,091.90, GP RM1,841.40 (30.23%)
- KPJR: 251 txns, RM1,765.91, GP RM541.20 (30.65%)
- KPJT: 137 txns, RM508.41, GP RM159.40 (31.38%) — partial month (15-30 Sept)
- 4-site total: 1,917 txns, RM10,594.22, GP RM3,189.60 (30.11%)

## User preferences

- Izzu wants concise replies with the file path + small table of results — no flowery prose, no re-stating the question.
- Izzu sends each rate correction as a separate message. Apply one at a time, re-run, report delta.
- Izzu frequently renames or aliases products. Always confirm consolidation in the next PDF before declaring done.
- Izzu uses two distinct rename patterns: **"X to be Y"** (canonical rename) and **"X and Y are same"** (merge aliases). Treat both as alias updates — add the old spelling to `PRODUCT_ALIASES` pointing to the canonical name, and verify the alias actually fires (UPPERCASE/SANDWISH typos are common — grep the rendered PDF for leftover variants after each rename).
- Izzu sometimes uploads duplicate xlsx files (same data, different name). Reuse the same data, don't generate twice.
- Izzu uses BM Penang casual. Match: "Biar", "Try", "OK proceed", not "I shall endeavor to..."
- Izzu regularly asks for combined reports across 2-3 sites — always include GP and Margin in combined tables.
