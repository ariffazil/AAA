---
name: nasilemak-engine
version: 4.0.0
description: "Nasi lemak vendor costs and 12-location order rules."
tags: [business, nasi-lemak, vendor, optimization, syedos]
triggers:
  - "nasi lemak"
  - "nasilemak"
  - "vendor Ali Maju"
  - "berlauk"
  - "order template"
---

# Nasi Lemak Business Engine v4

## Vendor: Ali Maju Sri Rampai

- Payment: Daily cash, next-day delivery
- Negotiation: NOT possible
- Manpower: Syed solo
- Overhead: RM100/month petrol

## Variant Economics

| Variant | Cost | Sell | Margin | Waste |
|---|---|---|---|---|
| Dadar | RM1.20 | RM2.50 | RM1.30 (52%) | free |
| Rebus | RM1.20 | RM2.50 | RM1.30 (52%) | free |
| Mata | RM1.50 | RM3.00 | RM1.50 (50%) | free |
| Berlauk | RM1.50 | RM3.00 | RM1.50 (50%) | covers |

## Location Rules (12 fixed)

NO BERLAUK: Mamak 2, Kedai P, Kedai A, Mamak 1
BERLAUK OK: DSP/DSW, LRT WM, LRT S, Kedai L, Even, Dato, Parlimen

## Berlauk Cap

- Normal day: 19 units max
- Event day: 43 units max

## Operational Rules

1. Order to Ali Maju by 9pm night before
2. Pickup ready 5:15-5:30 AM
3. Deliver before 7 AM
4. Telur orders: +10% buffer
5. DSP/DSW = first delivery stop

## Monthly Projection

Revenue: RM23,059 | Net: RM11,655/month

## Files

- Engine: /root/sado/data/engine_v4.json
- Dashboard: /var/www/html/syedos/nasilemak/analytics.html
- Orders CSV: /root/sado/data/nasi_lemak_orders.csv