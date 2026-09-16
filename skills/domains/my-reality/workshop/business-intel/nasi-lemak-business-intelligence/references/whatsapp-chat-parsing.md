# WhatsApp Chat Parsing — Order Extraction Workflow

> Session: 2026-08-26 · Extracted 31 orders from Ali Maju Sri Rampai vendor chat

## Source Format

WhatsApp chat export arrives as ZIP containing `_chat.txt`:
```
[21/04/2026, 8:01:25 PM] ‪+60 11‑2616 1483‬ Ali Maju Sri Rampai: Messages and calls are end-to-end encrypted...
[28/06/2026, 8:02:28 PM] .: Salam kak esk nak awal
 mamak 2( dalam tray)
Kedai p(dalam tray)
...
```

## Parsing Steps

### 1. Extract ZIP
```bash
cd /tmp && unzip -o "/root/.hermes/cache/documents/doc_XXXXX*.zip"
# Extracts _chat.txt
```

### 2. Parse WhatsApp Format
Regex: `^\[(\d{1,2}/\d{1,2}/\d{4}),\s*(\d{1,2}:\d{2}:\d{2})\s*([AP]M)?\]\s*`

Multi-line messages continue without timestamp prefix until next sender.

### 3. Identify Syed's Orders
Filter sender == "." (Syed's display name) AND text contains "Order untk"

Pattern: `Order untk DD/MM/YY (Day)`

### 4. Extract Location + Quantity Structure

**Location headers** (line < 35 chars):
- `MAMAK 2`, `MAMAK 1`
- `LRT WM`, `LRT S`, `LRT`
- `KEDAI P`, `KEDAI L`, `KEDAI A`
- `DSP/DSW`, `DSP`, `DSW`
- `PARLIMEN`, `PEGAWAI KERAJAAN`, `EVEN`, `DATO ORDER`, `DATO`

**Quantity extraction:** Last number on line = qty (1-3 digits, < 500)

### 5. Variant Classification

| Variant | Regex Pattern |
|---|---|
| telur_rebus_separuh_sambal_campur | `telur\s+rebus\s+separuh\s+sambal\s+campur` |
| telur_rebus_sambal_campur | `telur\s+rebus\s+sambal\s+campur` |
| telur_rebus_sambal_asing | `telur\s+rebus\s+sambal\s+asing` |
| telur_mata_sambal_campur | `telur\s+mata\s+sambal\s+campur` |
| telur_mata_sambal_asing | `telur\s+mata\s+sambal\s+asing` |
| telur_dadar_sambal_asing | `telur\s+dadar\s+sambal\s+asing` |
| berlauk_paru | `berlauk[\s\S]*?paru` |
| berlauk_dendeng | `berlauk[\s\S]*?dendeng` |
| daun_pisang | `daun\s+pisang` |

## Python Parser Pattern

```python
import re
from collections import defaultdict

with open('_chat.txt', 'r', encoding='utf-8') as f:
    raw = f.read()

lines = raw.split('\n')
messages = []
current = None
date_re = re.compile(r'^\[(\d{1,2}/\d{1,2}/\d{4}),\s*(\d{1,2}:\d{2}:\d{2})\s*([AP]M)?\]\s*')
sender_re = re.compile(r'^([^:]+?):\s*(.*)$')

for line in lines:
    m = date_re.match(line)
    if m:
        if current:
            messages.append(current)
        rest = line[m.end():]
        sm = sender_re.match(rest)
        sender = sm.group(1).strip() if sm else "?"
        text = sm.group(2).strip() if sm else rest.strip()
        current = {'date_raw': m.group(1), 'sender': sender, 'text': text}
    elif current and line.strip():
        sm = sender_re.match(line)
        if sm and sm.group(1).strip() == current['sender']:
            current['text'] += '\n' + sm.group(2).strip()
        else:
            current['text'] += '\n' + line.strip()
if current:
    messages.append(current)

# Extract orders
order_blocks = []
for m in messages:
    if m['sender'] == '.' and 'Order untk' in m['text']:
        order_date_match = re.search(r'Order untk (\d{1,2})/(\d{1,2})/(\d{2,4})', m['text'])
        if order_date_match:
            d, mo, y = order_date_match.groups()
            yr = y if len(y) == 4 else f"20{y}"
            order_date = f"{yr}-{mo.zfill(2)}-{d.zfill(2)}"
            order_blocks.append({'order_date': order_date, 'text': m['text']})
```

## Pitfalls

1. **Gateway logs truncate at ~226 chars** — use state.db or corpus for full text
2. **"Order untk" date ≠ message date** — orders placed night before delivery
3. **"tambah order" follow-ups** — aggregate per delivery date
4. **"Even" = event/catering** (not location name)
5. **"Dato order" = special premium order** (70 units single event)
6. **Variant mix percentages are inferred from keyword frequency, not exact**
7. **Some orders include "Even" section BEFORE location headers** — event orders come first

## Output Schema

```json
{
  "orders": [
    {
      "date": "2026-07-22",
      "total": 524,
      "items": [
        {"location": "MAMAK2", "variant": "telur_rebus_separuh_sambal_campur", "qty": 40},
        {"location": "LRT_WM", "variant": "telur_rebus_separuh_sambal_campur", "qty": 4}
      ]
    }
  ],
  "by_date": {"2026-07-22": {"total": 524, "dow": "Wed", "by_loc": {...}}},
  "loc_totals": {"DSP_DSW": 1313, "MAMAK2": 1208, ...},
  "meta": {"orders": 31, "total_units": 7594, "range": ["2026-07-01", "2026-08-24"]}
}
```