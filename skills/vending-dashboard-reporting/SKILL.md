---
name: vending-dashboard-reporting
description: Build vending sales dashboard PDFs per site or combined.
version: 1.0.0
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Vending Sales Dashboard Reporting

Monthly performance dashboards from payment-gateway Excel exports for the Web Of Projects vending fleet at KPJ hospitals (KPJAP Ampang, KPJD Damansara, KPJR Rawang, KPJT Tawakkal). One site per report, or 2-4 sites combined.

## Inputs and schema

Single sheet named like `Trans_20261005`, 32 columns, header in row 1. Index by 1-based column number:

- col 2 - Date, string `'%d-%m-%Y %I:%M:%S %p'` (e.g. `1-9-2026 03:48:42 PM`)
- col 5 - Merchant Name, **always** `WebOfProjects-VM(Cheras)` for every site
- col 13 - Payment Method (DuitNow QR / TNG QR (MYR) / GrabPay QR / Boost QR)
- col 17 - Amount, MYR float
- col 19 - ProdDesc, **truncated at 20 characters** (source of most spelling variants)
- col 26 - Status, filter `== 'Success'`

Site identity comes from the FILENAME (`*KPJAP*`, `*KPJD*`, `*KPJR*`, `*KPJT*`), never from the merchant field.

Dependencies: `openpyxl matplotlib numpy`. Install if absent: `pip install openpyxl matplotlib`.

## Data traps (each produced a wrong report once)

1. **Never `min()`/`max()` the raw date strings.** `1-9-2026` vs `10-9-2026`: string sort ranks day 10 below day 2, so a full-month export reads as a 9-day partial. Parse with `datetime.strptime` first, then compare dates, then state coverage (e.g. "13 of 30 days").
2. **ProdDesc variants.** Normalise through a `PRODUCT_ALIASES` dict BEFORE aggregating. Data is uppercase (`MILO`, `COCONUT WATER`) while rate keys are Title Case (`Milo`, `Coconut Water`); each product needs both an alias entry and a rate key.
3. **Alias keys must match byte-for-byte.** `SANDWISH EGG` != `SANWISH EGG`; one wrong letter and the merge silently never fires. Re-run and grep the PDF after every alias change.
4. **A `DEFAULT_RATE = 1.00` fallback hides a missing rate** - the product looks plausible instead of obviously broken. Grep the rendered PDF for anything still on the default before declaring done.
5. **Rates are per-site, never copy a dict across sites.** MILO is RM1.50 at KPJAP/KPJD but RM1.00 at KPJR; nut snacks are RM0.50 at KPJT vs RM0.90 elsewhere.
6. **Non-product rows exist.** A Chinese label (e.g. 自动售货机) marks a test entry - exclude it and say that you did.
7. **Rates arrive one message at a time.** Apply each correction, re-run, re-check the affected product in the PDF, report the exact GP delta (old -> new). Never batch-assume.
8. **Partial months happen.** KPJT started mid-September. Never compare a partial month to a full month without saying so.

## Report shape

Single-site, 7 pages: (1) KPIs + monthly trend, (2) cumulative + daily table, (3) product + payment mix, (4) GP summary + top-10 GP, (5-6) all-products GP detail split in two, (7) hourly pattern.

- Every bar carries its value label, **horizontal** orientation. Rotated labels rejected; labels on peak bars only rejected.
- Grand total appears **once, at the end**. A matplotlib `<tfoot>` row repeats on every page - put the total in a separate table block after the main table instead.
- Fonts must be large: table rows >=11pt, page titles 20pt, KPI numbers 22pt. 6-8pt tables get rejected as unreadable.
- Product aliases are expected to be corrected repeatedly; each merge should report the new combined unit count.

## Combined multi-site layout: one table, never nested axes

1. One axes: `ax = fig.add_axes([0.05, 0.05, 0.90, 0.85]); ax.axis("off")`.
2. Header band = one filled `Rectangle` in navy, white bold site names.
3. Each cell = its own `Rectangle` with `edgecolor` and `linewidth=1.0`, plus `ax.text(..., ha="center", va="center")` at its centre.
4. Metric rows below; final TOTAL row on `#fff3e0` with an `#a02020` border.

Do NOT build the grid from many small `add_axes` calls with their own spines, and do NOT wrap a column of axes in a figure-level `Rectangle`. That combination produced double borders, a title colliding with the header row, and a footer running off the page over the last tile row.

For a 4-site block, a 2x2 grid of per-site tiles with 6 KPIs each is unreadable - go straight to the single table.

## Verify before delivering (mandatory)

```bash
pdftoppm -r 100 out.pdf /tmp/chk -png -f 1 -l 1
pdftotext -layout out.pdf | head -60
```

Then `vision_analyze` the PNG asking explicitly about: title overlap, footer cut-off, double borders, truncated or missing labels. Ship only after that check passes.

Two visual defects on the same page means the page generator is wrong - rewrite that page from scratch. Repeated coordinate patches made the layout progressively worse.

## Output

`/root/.hermes/workspace/zen/izzu-brief/artifacts/<Mon>_<YYYY>_<SITE>_Dashboard.pdf`, plus `..._Combined_<n>Sites_Dashboard.pdf`. Deliver with `MEDIA:/abs/path.pdf` and a short txns / revenue / GP / margin table - not a wall of prose.
