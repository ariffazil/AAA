---
name: multisite-performance-dashboards
description: Use when building a combined multi-site performance PDF.
---

# Multi-Site Performance Dashboards

Build a combined comparison dashboard (revenue, GP, margin, mix, trend) across several branches/locations from their raw transaction exports, as one PDF.

Companion to the single-site dashboard work. This skill is for the **combined** deliverable only.

## When to load

- User names 2–4 locations and asks for one dashboard/report covering all of them
- User changes the combination ("now add X", "do the same for A+B+C") — expect this repeatedly
- User wants a year-on-year or month-on-month table across sites

## Step 1 — Intake, then assert the totals

Payment-gateway export, one sheet, 32 columns. 1-indexed openpyxl columns that matter:

| Col | Field | Notes |
|---|---|---|
| 2 | Date | string like `30-9-2026 08:20:54 PM` |
| 5 | Merchant Name | **identical for every site** |
| 13 | Payment Method | DuitNow QR / TNG QR (MYR) / GrabPay QR / Boost QR |
| 17 | Amount | MYR float |
| 19 | ProdDesc | **truncated at ~20 chars** |
| 26 | Status | filter `== 'Success'` |

**The site is the filename, not the merchant field.** Every export carries the same merchant string regardless of branch. Do not infer the site from column 5 — you will label three sites as one.

**Parse dates, never sort the string.** `'10-9-2026'` sorts before `'2-9-2026'`. `min()`/`max()` on the raw string yields a false date range and a false active-day count. Use `datetime.strptime(s, '%d-%m-%Y %I:%M:%S %p')` then compare dates.

Before building anything, print: row count after the status filter, parsed date range, distinct days, distinct products. If the user asserts full-month data and you compute 9 days, you have a parsing bug — not partial data.

## Step 2 — Normalise product names before aggregating

Excel truncates the product description, so one product arrives under many spellings across months and sites (`BURGER FISH N SHRIMP`, `BURGER SHRIMP AND FI`, `SHRIMP AND FISH BURG`, `BURGER FISH AND SHRI`). Build a `PRODUCT_ALIASES` dict and apply it **before** counting.

Rules that cost time when missed:

- **Alias keys must match the source string exactly.** One wrong character means the alias silently never fires and the product stays split. After each run, grep the rendered PDF for leftover raw variants.
- **Uppercase data vs Title Case rate keys.** The export is uppercase; a curated rate dictionary is usually Title Case. Each product needs both: an alias (UPPER → Title) *and* a rate entry under that Title key.
- **A default rate hides the bug.** A fallback of `1.00` makes an un-aliased product look plausible instead of obviously wrong. Grep the output for every product still sitting on the default before declaring done.
- **User-driven merges arrive one line at a time** ("X to be Y"). Apply literally, re-render, and report the merged unit count. Never batch-guess a merge.

## Step 3 — Gross profit is per-site

The same product carries different GP at different locations. Keep one rate dictionary per site and pass the right one in. Never reuse one site's dictionary because the product list looks similar.

Margin is `total_gp / total_revenue`. Derive it; never carry a margin number forward after changing a rate.

## Step 4 — Layout architecture (the part that goes wrong)

Build the whole comparison table inside **one axes**, drawing cells as `Rectangle` patches in `ax.transAxes`. Do not give each site its own nested axes with its own border.

**Why:** nested axes each draw their own spines, so adjacent cells render double borders; a site label placed as a separate small axes collides with the tile row beneath it; a `fig.text` footer at `y≈0.0` runs off the canvas and over the last row. All three failures look like "the layout is broken" and cannot be patched away one border at a time.

The shape that works:

```
fig = plt.figure(figsize=(13, 9))
fig.suptitle(title, fontsize=22, fontweight='bold', y=0.97)
ax = fig.add_axes([0.05, 0.05, 0.90, 0.85]); ax.axis('off')

# header band: one Rectangle across the full width, facecolor navy
#   then white bold text per column, centred at column midpoints
# data rows: one Rectangle per cell, edgecolor navy, linewidth 1.0
# total row: a Rectangle spanning all columns, warm facecolor + red text
```

Rules:

- `suptitle` at `y=0.97` with the axes starting at `0.85` — the title needs its own band above the header row, or it clips the column names.
- Column width `1.0 / n_cols`; row height `1.0 / n_rows`; place text at `(col + 0.5) * col_w` and `row_y + row_h / 2`. No hardcoded pixel offsets.
- The TOTAL row is a table row inside the axes, not a free-floating `fig.text`. A footer outside the axes has no container and gets cut at the page edge.
- Zebra-stripe data rows (`white` / near-white) so wide rows stay readable.
- Site grouping: with 4 sites use **4 vertical strips side by side** (one column of metrics per site), not a 2×2 grid. A 2×2 grid at A4 gives each tile too little room and the user will call it confusing.
- Duplicated row labels per column ("Total Transactions" repeated under each site) are correct in a strip layout — each strip must be readable alone.

## Step 5 — Verify visually before delivering

Raster page 1 and look at it:

```bash
pdftoppm -r 100 out.pdf chk -png -f 1 -l 1
```

Then check with vision: title clear of the table, every site label attached to its own block, no cut-off footer, no doubled borders. Text extraction (`pdftotext -layout`) proves the numbers are present but says nothing about overlap — a page can extract perfectly and still look broken.

When the user says "confusing" or "very stupid", do not ask which element. Raster the page, list the defects yourself, and fix them in one pass. Repeated one-property patches on a layout defect make it worse and read as not listening.

## Format the user expects

- **Large fonts.** Table rows 11–12pt, page titles 20–22pt, KPI numbers 14–22pt. Small fonts get rejected outright.
- **Grand total once, at the end** — never repeated on every page.
- **Every bar labelled** with its value, horizontal text (not rotated), on trend and hourly charts.
- Summary table columns: Site, Txns, Revenue, GP, Margin, Avg/Txn, Days, Best Day.
- Deliver one PDF via `MEDIA:/absolute/path`, plus a compact summary table in the message. No menus.

## Pitfalls

- **Partial-month sites must be labelled.** A site whose data starts mid-month has fewer active days; showing it beside full-month sites without a note produces a misleading average. Flag it in the message, not just the chart.
- **Test/system rows.** Non-product entries (e.g. a machine-name string, a one-cent transaction) inflate counts. Detect and exclude them, and tell the user you excluded them so they can object.
- **Hardcoded GP totals go stale.** If the combined dashboard takes GP as an input constant rather than recomputing from rates, any later rate correction silently desynchronises it. Recompute from the rate dictionaries, or state plainly that the GP column is pinned.
- **Never invent a site name or branch label** to fill a gap in the request; ask, or use the code exactly as the user wrote it.
