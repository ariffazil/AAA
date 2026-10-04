---
name: fb-transaction-intelligence
description: Analyze payment gateway Excel exports (KPJD, TNG, DuitNow, GrabPay) for F&B businesses — parse transaction data, generate business intelligence (revenue breakdown, product performance, payment methods, peak hours), and provide actionable insights. Use when the user shares a payment gateway export, asks for sales analysis, wants to understand their business performance, or requests automation for recurring transaction analysis.
version: 1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [f&b, business-intelligence, payment-gateway, transaction-analysis, kpid, tng, duitnow, excel]
    related_skills: [ocr, financial-chart-analysis, local-business-deep-dive]
---

# F&B Transaction Intelligence

## Overview

Analyze payment gateway Excel exports for food & beverage businesses. The typical flow:
1. User shares Excel file (.xlsx) from payment gateway (KPJD, TNG, DuitNow, GrabPay, etc.)
2. Parse transaction data (date, product, amount, payment method, status)
3. Generate business intelligence report
4. Provide actionable insights

## When to Use

- User shares an Excel file with transaction/sales data
- User asks "boleh analyze sales saya?" or "summary transaksi"
- User wants to understand their F&B business performance
- User asks about automating invoice/sales tracking
- User shares payment gateway export from KPJD, TNG, DuitNow, GrabPay, etc.

## When NOT to Use

- Trading/stock screenshots (use `trading-screenshot-analysis`)
- PDF invoices or receipts (use `ocr` or `ocr-and-documents`)
- General business research (use `local-business-deep-dive`)

## Quick Start

### Step 1: Install openpyxl (if not already installed)

```bash
pip install openpyxl --break-system-packages -q
```

### Step 2: Parse the Excel file

```python
import openpyxl
from collections import defaultdict

wb = openpyxl.load_workbook('path/to/file.xlsx')
ws = wb[wb.sheetnames[0]]  # Usually first sheet

rows = []
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, values_only=True):
    if row[0] is None:
        continue
    # KPJD format: No, Date, Ref, MerchantCode, MerchantName, TransId, AuthCode, 
    #   ..., PaymentMethod, ..., Currency, Amount, Discount, ProductDesc, ..., Status
    rows.append({
        'date': str(row[1]),
        'payment_method': row[12],
        'amount': float(row[16]) if row[16] else 0,
        'discount': float(row[17]) if row[17] else 0,
        'product': str(row[18]).strip() if row[18] else '',
        'status': row[25],
    })
```

### Step 3: Generate analysis

```python
# Total revenue
total = sum(r['amount'] for r in rows)
success = [r for r in rows if r['status'] == 'Success']

# By date
date_counts = defaultdict(lambda: {'count': 0, 'total': 0.0})
for r in rows:
    d = r['date'].split(' ')[0]
    date_counts[d]['count'] += 1
    date_counts[d]['total'] += r['amount']

# By product
product_counts = defaultdict(lambda: {'count': 0, 'total': 0.0})
for r in rows:
    product_counts[r['product']]['count'] += 1
    product_counts[r['product']]['total'] += r['amount']

# By payment method
payment_counts = defaultdict(lambda: {'count': 0, 'total': 0.0})
for r in rows:
    payment_counts[r['payment_method']]['count'] += 1
    payment_counts[r['payment_method']]['total'] += r['amount']

# By hour (parse time from date string)
hour_counts = defaultdict(lambda: {'count': 0, 'total': 0.0})
for r in rows:
    try:
        parts = r['date'].split(' ')
        time_part = parts[1]  # e.g. "03:09:56"
        ampm = parts[2]       # AM/PM
        h = int(time_part.split(':')[0])
        if ampm == 'PM' and h != 12:
            h += 12
        elif ampm == 'AM' and h == 12:
            h = 0
        hour_counts[h]['count'] += 1
        hour_counts[h]['total'] += r['amount']
    except:
        pass
```

### Step 4: Categorize products (F&B specific)

```python
categories = defaultdict(lambda: {'count': 0, 'total': 0.0})
for r in rows:
    p = r['product'].upper()
    if 'BURGER' in p:
        cat = '🍔 Burger'
    elif 'SANDWICH' in p:
        cat = '🥪 Sandwich'
    elif any(x in p for x in ['MILO', 'CHOCOLATE', 'CHOCO', 'MILK', 'STRAWBERRY', 'LATTE', 'ZUS']):
        cat = '☕ Minuman'
    elif any(x in p for x in ['CASHEW', 'SPRITZER', 'DRINHO']):
        cat = '🥤 Other Drinks/Snacks'
    else:
        cat = '📦 Lain-lain'
    categories[cat]['count'] += 1
    categories[cat]['total'] += r['amount']
```

## Output Format

Produce a structured report with:

1. **Ringkasan** — total transactions, total revenue, average order value, success rate
2. **Breakdown by Date** — transactions and revenue per day
3. **By Category** — product categories with revenue share %
4. **Top Products** — ranked by revenue with quantity and average price
5. **Payment Methods** — which methods dominate, revenue share
6. **Peak Hours** — busiest times with visual bar
7. **Insights** — actionable business recommendations

## Common Payment Gateway Formats

### KPJD (Touch 'n Go / DuitNow)
- Sheet: `Trans_YYYYMMDD`
- Columns: No, Date, Ref, MerchantCode, MerchantName, TransId, AuthCode, ..., PaymentMethod, ..., Currency, Amount, Discount, ProductDesc, ..., Status
- Payment methods: `DuitNow QR`, `TNG QR (MYR)`, `GrabPay QR`

### TNG Direct Export
- Similar structure to KPJD
- May have additional columns for terminal ID, batch number

### DuitNow QR
- May come as CSV or Excel
- Columns: Transaction ID, Date, Amount, Merchant, Status

## Pitfalls

1. **openpyxl not installed** — `pip install openpyxl --break-system-packages -q`
2. **Date format varies** — KPJD uses "M/D/YYYY HH:MM:SS AM/PM", others may use "YYYY-MM-DD"
3. **Empty rows** — always check `if row[0] is None: continue`
4. **Status column** — not all rows are "Success"; filter for failed transactions
5. **Time parsing** — AM/PM conversion to 24-hour for peak hour analysis
6. **Currency** — assume MYR unless specified; check currency column if present

## Automation Pattern

For recurring analysis, the user can:
1. Export Excel from payment gateway
2. Drop file into a designated folder
3. Script auto-processes and generates summary

This skill provides the analysis logic; the automation (cron job, file watcher) is separate and depends on user's setup.

## References

- `references/kpjd-column-map.md` — KPJD Excel column mapping reference
- `references/fb-product-categories.md` — Standard F&B product category taxonomy
