---
name: nasi-lemak-business-intelligence
version: 1.0.0
description: "Use when analysing nasi lemak business data — vendor costs, margins, sales dashboards and per-location performance."
triggers:
  - "nasi lemak"
  - "abang sado business"
  - "vendor pricing"
  - "order analytics"
  - "nasi lemak dashboard"
  - "Ali Maju"
  - "berlauk"
  - "telur mata"
  - "telur dadar"
  - "telur rebus"
---

# Nasi Lemak Business Intelligence

## When to Use

When analyzing Abang Sado's nasi lemak business: order data extraction, vendor pricing, location rules, financial modeling, or dashboard generation. Also covers WhatsApp chat parsing for order data.

## Vendor Pricing (Confirmed 2026-08-26)

| Variant | Vendor Cost | Sell | Margin | Waste Risk |
|---|---|---|---|---|
| Dadar | RM1.20 | RM2.50 | RM1.30 (52%) | ✅ free disposal |
| Rebus | RM1.20 | RM2.50 | RM1.30 (52%) | ✅ free disposal |
| Mata | RM1.50 | RM3.00 | RM1.50 (50%) | ✅ free disposal |
| **Berlauk** | **RM1.50** | **RM3.00** | **RM1.50 (50%)** | **⚠️ Syed covers** |

**Waste Rule:** Telur variants = free disposal (no cost if unsold). Berlauk = Syed covers vendor cost (RM1.50/unit loss).

## Location Rules — Berlauk Restriction

**🚫 NO berlauk (telur only):**
- Mamak 2 (1,208 units, 16% volume)
- Kedai P (1,196 units, 16% volume)
- Kedai A (130 units, 2% volume)
- **Total: 2,534 units (44%) = zero waste risk**

**✅ Berlauk allowed:**
- DSP/DSW (1,313 units, 17% volume)
- LRT Wangsa Maju (744 units, 10% volume)
- LRT Sg Buloh (483 units, 6% volume)
- Kedai L (385 units, 5% volume)
- EVEN (260 units, 3% volume)
- Dato (70 units, 1% volume)
- Parlimen (35 units, <1% volume)
- **Total: 3,290 units (56%) = berlauk risk**

**Berlauk Cap:** Normal day = 19 units max. Event day = 43 units max. Every 10 unsold = RM15 loss.

## Financial Model (31 orders, Jul 1–Aug 24, 2026)

| Metric | Value |
|---|---|
| Total units | 7,594 |
| Avg per order | 245 units |
| Peak day | 728 units (Aug 24, Mon) |
| Monthly revenue | RM19,018 |
| Monthly COGS | RM9,261 |
| Monthly gross profit | RM9,757 |
| Berlauk waste @10% | -RM116 |
| **Monthly net profit** | **RM9,640** |

**By location type:**
- Telur-only locations: RM3,750/month (zero waste risk)
- Berlauk-eligible locations: RM4,983/month (RM66 waste risk @10%)

## WhatsApp Chat Parsing Workflow

When Syed sends a WhatsApp chat export (ZIP file):

1. **Extract ZIP** → `_chat.txt` inside
2. **Parse format:** `[DD/MM/YYYY, HH:MM:SS AM/PM] sender: text`
3. **Multi-line messages** continue without timestamp prefix
4. **Order detection:** Look for "Order untk DD/MM/YY (Day)" pattern
5. **Location extraction:** Split by location headers (MAMAK 2, LRT WM, KEDAI P, etc.)
6. **Quantity extraction:** Last number on line = quantity (1-3 digits)
7. **Variant classification:** Match keywords (telur rebus, telur mata, telur dadar, berlauk paru/dendeng)

**Key patterns:**
- `MAMAK 2\nNasi lemak telur rebus separuh sambal campur 40` → Mamak 2, rebus, 40 units
- `LRT WM\n1.Nasi lemak telur mata sambal campur 10` → LRT WM, mata, 10 units
- `Even\nNasi lemak berlauk paru 15` → EVEN, berlauk paru, 15 units

**Pitfalls:**
- Gateway logs truncate at ~226 chars — use state.db or corpus for full text
- "Order untk" date may differ from message date (orders placed night before)
- Some orders have "tambah order" follow-ups — aggregate per delivery date
- "Even" = event/catering orders (higher volume, premium pricing)

## Analytics Dashboard Pattern

**URL:** `https://syedos.arif-fazil.com/nasilemak/analytics.html`
**File:** `/var/www/html/syedos/nasilemak/analytics.html`

**Tech stack:**
- Self-contained HTML (Chart.js from CDN, inline CSS/JS)
- Dark theme (#0a0a0f background, #f0a500 gold accent)
- Chart.js bar/line charts for daily volume, weekly trend
- Custom CSS bar charts for location breakdown, variant demand
- Mobile responsive (grid-template-columns: repeat(2,1fr) on small screens)

**Sections:**
1. Hero stats (total units, avg/order, monthly profit, berlauk risk)
2. Location rules box (green/red tags for berlauk eligibility)
3. Variant economics table (cost, sell, margin, waste risk)
4. Daily order volume chart (bar chart, event days highlighted purple)
5. Location breakdown + Day-of-week pattern (side by side)
6. Weekly growth trend (line chart)
7. Variant demand bars (estimated split: rebus 53%, mata 18%, dadar 9%, berlauk 9%, other 11%)
8. Berlauk waste risk model table
9. Order history table
10. Optimization insights

**Deployment:**
```bash
cp /root/sado/data/nasi_lemak_analytics_v2.html /var/www/html/syedos/nasilemak/analytics.html
```

## Optimization Recommendations

1. **Berlauk order cap** — 19 units normal, 43 event. Every 10 unsold = RM15 loss.
2. **Telur variants order freely** — unsold = free disposal. Order 10% buffer above forecast.
3. **Focus 3 locations** — DSP/DSW, Mamak 2, Kedai P = 48% volume. Optimize delivery timing.
4. **Event days = 1.9x revenue** — avg RM968 vs RM511 normal. Berlauk premium opportunity.
5. **Vendor timing critical** — 5:15-5:30 AM ready window. Late = customer loss.

## References

- `references/nasi-lemak-vendor-data.md` — full parsed order dataset (31 orders, location breakdown, variant mix)
- `references/whatsapp-chat-parsing.md` — detailed parsing workflow with regex patterns
- `references/nasi-lemak-analytics-dashboard.md` — dashboard generation pattern with Chart.js config