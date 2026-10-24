---
name: vending-site-reporting
description: Build monthly vending-site performance dashboards.
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [excel, openpyxl, matplotlib, pdf, dashboard, gross-profit, vending]
metadata:
  hermes:
    category: document-production
    related: [formal-document-rebuild, chart-artifact-render-qa, rendered-document-audit]
---

# Monthly Vending-Site Performance Reporting

## When to Use

A monthly payment-gateway Excel export arrives (one file per site: KPJAP, KPJD, KPJR, KPJT, or a new
site code) and the ask is the familiar report: revenue, gross profit, product mix, payment split,
hourly pattern — plus, on request, a combined multi-site page.

## Input schema (single sheet, ~32 columns, 1-indexed)

| Col | Field | Use |
|---|---|---|
| 2 | Date | `'%d-%m-%Y %I:%M:%S %p'` — **parse with strptime** |
| 5 | Merchant Name | `WebOfProjects-VM(Cheras)` on **every** export — the site comes from the FILENAME, not this field |
| 13 | Payment Method | DuitNow / TNG / GrabPay / Boost |
| 17 | Amount | MYR float |
| 19 | ProdDesc | truncated to ~20 chars — the source of every alias problem |
| 26 | Status | keep only `Success` |

## Procedure

1. **Probe first:** sheet name, row count, distinct products, parsed date range, merchant string.
   Never report a date range from `min()/max()` on the raw date string — string order puts `10-9`
   before `2-9`, which reads as a 9-day month when the month is complete.
2. **Detect a partial month and say so.** Compute first and last transaction date per site; a site
   that starts mid-month gets labelled `partial` and is excluded from month-on-month comparisons.
   Drop obvious test rows (non-Latin placeholder descriptions, single-unit zero-value entries).
3. **Normalise product names before aggregating** with a `PRODUCT_ALIASES` map, then aggregate.
4. **Apply the site's own GP-rate dict** (see rules). Default rate is a placeholder, not a result.
5. **Render** a 7-page PDF: (1) KPIs + daily trend, (2) cumulative + daily table, (3) product and
   payment mix, (4) GP summary + top-10 GP, (5–6) all-products detail split in two, (7) hourly pattern.
6. **Verify by grepping the render,** not by reading the numbers you computed:
   `pdftotext -layout out.pdf - | grep -iE '<suspect product names>'` for leftover variants and
   `grep` for any product still sitting on the default rate. A plausible-looking rate on an un-aliased
   product is the failure mode this catch exists for.
7. **Deliver** with `MEDIA:/abs/path` and a four-row summary table (site, txns, revenue, GP, margin).

## Rules that cost real rework

- **GP rates are per site.** The same product carries different GP/unit at different sites (Milo 1.50
  at two sites, 1.00 at another; Guava 1.30 vs 1.00). One rate dict per site, never copied across —
  a copied dict produces a plausible, wrong margin with no error.
- **Rate corrections arrive one at a time.** Apply each literally, re-run, re-grep the affected
  product, and report the GP delta (old → new) in one line. Do not batch-assume or round.
- **Alias keys must match the data character-for-character.** A one-character typo (`SANWISH` vs
  `SANDWISH`, `CHEEZY` vs `CHEESY`) collapses silently: the alias never fires, the product stays
  split, and the PDF looks fine. After every run, grep the render for each raw variant you intended
  to merge.
- **A product that exists in the export but not in the rate dict gets the placeholder rate** — so any
  product still holding the default is either genuinely new or a missed alias. List those explicitly
  for the user rather than shipping the number.
- **Combined reports are opt-in and per-request.** The site set changes between asks; never infer it.

## Layout and legibility (learned the hard way)

- Table rows 11–12pt, page titles 20pt, KPI figures 22pt. Smaller type comes back as "too small to
  read".
- Grand total appears **once**, on the final page — a `<tfoot>` in a long table repeats on every page
  in weasyprint; move the total out of the table into its own block after `</table>`.
- Every bar carries its value label, horizontal (not rotated).
- A multi-site comparison page is **one flat table** — sites as columns, metrics as rows, one header
  row, one total row. Card grids built from separate panels per site collide and cannot be fixed by
  adding borders; see `formal-document-rebuild` §Page layout QA.
- Verify the page count matches the intended section count after every structural edit; an extra page
  usually means content reflowed, not that a section grew.
