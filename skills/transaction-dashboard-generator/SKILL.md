---
name: transaction-dashboard-generator
description: Generate visual dashboard PDFs from business POS/transaction Excel exports. Clean, light-themed, non-federation dashboards for business operators (not Arif/WEALTH). Auto-detects location, date range; renders 6 charts + KPI cards + insights. Trigger when user uploads transaction Excel file (KPJAP, KPJD, etc.) and asks for "dashboard", "summary", or "automate invoice/management account."
---

# Transaction Dashboard Generator

Class of task: turn a POS/transaction Excel export into a visual dashboard PDF — quick, clean, and easy for business operators to understand. **Not** the Arif/WEALTH dark-theme report pipeline; this is for Izzu and similar non-technical business owners.

## When to use
- User uploads `.xlsx` transaction export and asks for "dashboard", "summary", or "automation"
- User says "buat dashboard yang mudah faham"
- User repeatedly uploads files from different store locations and wants consistent output format
- Trigger words: KPJ, KPJAP, KPJD, WebOfProjects, transaction dashboard

## What it does NOT cover
- Arif's SOVEREIGN-grade WEALTH/333 reports (use `pdf-report-generation` instead)
- Federation dark-theme HTML→PDF (use `html-pdf-reporting` instead)
- Management accounts (P&L, balance sheet, tax) — this is sales dashboard only
- Invoice generation — separate workflow not yet automated

## Pipeline (proven on this profile)

### 1. Process the uploaded Excel
The user uploads an Excel file via Telegram. The file lands in:
`/usr/local/lib/hermes-agent/profiles/aaa-hermes/cache/documents/doc_*.xlsx`

Run the automation script:
```bash
cd /root/izzu-automation && python3 generate_dashboard.py "<input_path>" "/tmp/izzu-dashboard/<location>_<period>.pdf"
```

### 2. What the script does automatically
- **Location detection** — from filename (`KPJAP` → KPJ Ampang Puteri, `KPJD` → KPJ Damansara). Color theme per location.
- **Date range detection** — from filename pattern or data range
- **Data extraction** — reads columns: Date, Payment Method, Amount, Product, Status
- **6 charts generated** via matplotlib: daily revenue trend, day-of-week, category donut, top 12 products, payment methods, peak hours
- **HTML → PDF** via WeasyPrint: clean light theme, KPI cards, auto-generated insights
- **Independent per location** — each dashboard is standalone. No cross-location comparison tables.

### 3. Deliver
Send the PDF via `MEDIA:/path/to/file.pdf`. No long text summary needed — the dashboard speaks for itself. Izzu prefers "just the PDF."

## Script location
- **Main script:** `/root/izzu-automation/generate_dashboard.py`
- **Charts output:** `/root/izzu-automation/charts/`
- **HTML template (auto-generated):** `/root/izzu-automation/dashboard.html`

## Supporting files
- `references/vending-machine-benchmarks.md` — industry benchmark data for vending machines vs food stalls. Load when user asks "how do I compare to other machines" or "how is the market doing."

## Expected Excel format
The script expects standard KPJ/WebOfProjects transaction export format:
- Sheet: first sheet in workbook
- Columns: No (A), Date (B), Reference No (C), MerchantCode (D), Merchant Name (E), TransId (F), AuthCode (G), ..., Payment Method (M), ..., Currency (P), Amount (Q), Discount (R), ProdDesc (S), ..., User Email (T), ..., Status (Z)
- Date format: `dd-mm-yyyy hh:mm:ss AM/PM`
- Amount: numeric, in MYR

## Design standards (Izzu-specific)
- **Clean, light background** — not federation dark theme. White cards, light grey backgrounds.
- **Color-coded by location** — KPJAP = orange/red (#e17055), KPJD = blue (#0984e3)
- **KPI cards at top** — transactions, gross sales, avg/txn, active days, avg/day
- **Charts: matplotlib, 150dpi** — no Chart.js/JS (WeasyPrint can't render). PNG embedded via `<img>`.
- **Bahasa Malaysia labels** — bukan English. "Isnin" not "Monday", "Jualan" not "Revenue."
- **Auto-generated insights** — in plain BM, not analyst-speak. "Burger = nadi bisnes" not "Burgers represent a statistically significant revenue contributor."
- **Product categories auto-detected** — NYET Kitchens, Burger/Hotdog, Minuman, Sandwich, Snacks/Sides

## Pitfalls
- **Never compare locations** — Izzu explicitly said "Saya tak nak compare KPJAP dengan KPJD." Each dashboard is standalone.
- **WeasyPrint no-JS** — matplotlib PNG charts only. Never use Chart.js/canvas for PDF dashboards.
- **matplotlib mplstyle warning** — the host has a `pyrolite.mplstyle` with `legend.bbox_to_anchor` that triggers a warning on every run. Harmless; suppress with `2>/dev/null` if needed.
- **openpyxl required** — must be installed system-wide: `pip install --break-system-packages openpyxl`
- **Multiple pythons** — the script runs with default `python3`; verify openpyxl + weasyprint are available.
- **Single-day files** — the daily trend chart still renders correctly with one data point (bar chart, no trend line).
- **Filename encoding** — Excel files with `&` in name must be quoted correctly in shell commands.
- **Multiple uploads of same file** — Izzu sometimes uploads the same filename with a new cache ID; output is identical. Just re-render without making a fuss about it.
- **Sheet name varies** — sometimes `Trans_20260810`, sometimes `Trans_20260808`. Always use `wb.sheetnames[0]` not a hardcoded name. Pitfall found Aug 2026 when hardcoding the sheet name caused KeyError.

## Response style after delivery
- **Izzu wants minimal text.** After sending the PDF, do not paste the full summary tables again in chat — the dashboard already has them. Just confirm with a one-liner like "KPJ Damansara 11 Ogos siap! 35 txn, MYR 157.30." If he asks for numbers, give them in a small table; otherwise keep it tight.
- **Brief is correct.** Don't ask "ada apa-apa lagi?", don't explain what you did. He'll say "Good" or move on to the next file.

## When user asks for market/competitor comparison
- Izzu compares his stall to "vending machines" (Family Mart, CU Mart) in the hospital.
- Acknowledge that vending machines are NOT a fair benchmark — his is a prepared-food stall, not a snack machine. Higher AOV, fresh food, staff.
- Use the benchmark data in `references/vending-machine-benchmarks.md` to frame this properly: hospital vending avg MYR 110-220/day vs his MYR 100/day, but his AOV MYR 4-6 vs vending MYR 1.50-3.
- End with a realistic target tier (hospital cafeteria MYR 200-300/day, food court MYR 500+/day), not the vending ceiling.

## When user shares emotional moment
- "I feel happy and grateful" or "fighting with giants" — celebrate the win briefly, with one concrete number showing growth. Don't preach, don't over-format. Single paragraph, emoji, done.
- e.g. "🔥 7 Ogos MYR 118 → 11 Ogos MYR 157. That's +33%. Kau deserve it, Izzu."
