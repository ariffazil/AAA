---
name: kpj-vending-dashboard
description: Generate PDF dashboards from KPJ hospital vending machine transaction Excel exports. Auto-detects location (KPJ Damansara/KPJ Ampang Puteri), generates charts (daily trend, day-of-week, category, top products, payment, peak hours), and renders A4 PDF via weasyprint.
version: 1.0.0
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# KPJ Vending Dashboard Generator

Auto-generate PDF dashboards from KPJ hospital vending machine Excel exports (WebOfProjects-VM, Merchant M46098).

## Usage

```bash
python3 /root/izzu-automation/generate_dashboard.py <input.xlsx> [output.pdf]
```

If output path omitted, generates auto-named PDF in script directory.

## File naming convention (auto-detection)

- `*KPJD*` → KPJ Damansara (blue theme)
- `*KPJAP*` → KPJ Ampang Puteri (orange theme)
- Default: purple theme

## Excel schema (from KPJ payment processor)

- Col B (idx 1): DateTime string
- Col M (idx 12): Payment method
- Col Q (idx 16): Amount (float)
- Col R (idx 17): Discount
- Col S (idx 18): Product description
- Col Z (idx 25): Status

## Output

A4 PDF with: cover, KPI cards, daily revenue trend, day-of-week, category donut, top 12 products, payment methods, peak hours, auto insights, full product appendix.

## Critical Rules

- **NEVER compare KPJD vs KPJAP** — user explicit correction. Each location independent.
- **NYET Kitchens** = premium differentiator. Always highlight if present.
- Script: `/root/izzu-automation/generate_dashboard.py`
- Output: `/tmp/izzu-dashboard/`
- Dependencies: `openpyxl matplotlib weasyprint numpy`

## Context

Business: Izzu runs prepared food vending (burgers, NYET Kitchens, sandwiches, drinks) at KPJ hospitals. Competes with Family Mart & CU Mart vending machines. Edge: hot prepared food FM/CU can't replicate. Daily revenue growing MYR 100-157/day (Aug 2026).
