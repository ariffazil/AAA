# Single-Site Generator Template

Use one of the existing generators as a starting template:

- `/tmp/sep2026_kpjap_dashboard_gen.py` — KPJAP (most refined after many rate iterations)
- `/tmp/sep2026_kpjd_dashboard_gen.py` — KPJD (has many alias rules from product-name variants)
- `/tmp/sep2026_kpjr_dashboard_gen.py` — KPJR (smaller, simpler)
- `/tmp/sep2026_kpjt_dashboard_gen.py` — KPJT (has test-entry exclusion)

## To generate a new site

1. Copy the closest existing generator: `cp /tmp/sep2026_<existing>_dashboard_gen.py /tmp/<new>_gen.py`
2. Find/replace these constants near the top:
   - `SITE = "..."` — site code (KPJAP, KPJD, KPJR, KPJT, or new)
   - `XLSX = "/path/to/data.xlsx"` — input file
   - `OUT = "/path/to/output.pdf"` — output location
3. Update all page title strings (e.g., "KPJ Damansara" → "KPJ New Site")
4. Replace `GP_RATES` dict (use Aug baseline JSON if available, else start empty and ask Izzu)
5. Add `PRODUCT_ALIASES` for any spelling variants in the new data
6. Run: `python3 /tmp/<new>_gen.py`
7. Verify: `pdfinfo <out>.pdf | grep Pages` + `pdftotext -layout <out>.pdf - | head -50`

## Layout constants (do not change without Izzu's approval)

- Page size: `figsize=(11, 14)` — A4 portrait
- KPI tile text: 18pt value, 10pt label (single-site), 14pt for combined 4-site strips
- Bar chart label rotation: 0° (horizontal)
- Table row spacing: 0.030 figure-units between rows
- Daily table: 30 rows for full month
