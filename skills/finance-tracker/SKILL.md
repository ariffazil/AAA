---
name: finance-tracker
description: Finance tracking including banking, crypto, and expense management. Use when: (1) Tracking expenses and budgets, (2) Crypto price monitoring, (3) Portfolio tracking, (4) Bank transaction analysis, (5) Financial reporting and categorization.
---

# Finance Tracker Skill

Track expenses, monitor crypto, and manage financial data.

## Quick Start

### Crypto Price Check

```bash
# Check Bitcoin price
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=myr" | jq

# Check multiple coins
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=myr,usd" | jq
```

### Expense Tracking

Store expenses in: `~/.openclaw/workspace/data/expenses.jsonl`

```json
{"ts":"2026-03-25T10:00:00Z","amount":25.50,"currency":"MYR","category":"food","merchant":"Kopitiam","tags":["lunch","workday"]}
```

### Add Expense

```bash
# Quick add
finance add --amount 25.50 --category food --note "Lunch with team"

# With tags
finance add --amount 150.00 --category transport --tags["petrol","claimable"]
```

## Categories

Standard expense categories:

| Category | Description |
|----------|-------------|
| food | Meals, groceries |
| transport | Petrol, toll, parking, public transport |
| utilities | Electric, water, internet |
| entertainment | Movies, games, subscriptions |
| health | Medical, pharmacy, insurance |
| shopping | Clothing, electronics, household |
| investment | Stocks, crypto, savings |
| income | Salary, freelance, dividends |

## Reporting

### Monthly Summary

```bash
finance report --month 2026-03 --format table
```

Output:
```
Category      | Amount (MYR) | % of Total
--------------|--------------|----------
Food          | 850.00       | 28%
Transport     | 620.00       | 20%
Utilities     | 450.00       | 15%
...
```

### Crypto Portfolio

```bash
# Track holdings
crypto portfolio --show-prices

# Alert on price changes
crypto alert --coin bitcoin --above 500000 --currency MYR
```

## Bank Integration (Manual)

Import bank statements:

```bash
# Parse bank CSV
finance import --file statement.csv --bank maybank --format csv

# Auto-categorize based on merchant
finance categorize --file imported.jsonl
```

### Bank Statement Formats

| Bank | Format |
|------|--------|
| Maybank | CSV |
| CIMB | CSV |
| Public Bank | PDF (OCR) |
| HSBC | CSV |

## Cron Alerts

```json
{
  "tool": "cron",
  "action": "add",
  "job": {
    "name": "crypto-alert",
    "schedule": {"kind": "every", "everyMs": 3600000},
    "payload": {"kind": "agentTurn", "message": "Check crypto prices and alert if BTC > 500k MYR"},
    "sessionTarget": "isolated"
  }
}
```

## F1 (Reversibility) Notes

- Financial data is sensitive — encrypt at rest
- Bank credentials: use 1Password integration
- Crypto transactions on-chain = irreversible
- 888_HOLD for actual trades/spend
