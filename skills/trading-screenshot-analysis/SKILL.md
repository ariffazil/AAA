---
name: trading-screenshot-analysis
description: Read MT5/TradingView trading screenshots (XAUUSD/gold), compute P&L from order + price markers, and reply with quick win-validation verdicts in casual chat. Use when the user shares a chart screenshot, asks "berapa untung", or says "Boom" with a chart.
---

# Trading Screenshot Analysis

Casual-chat support for Arif's XAUUSD trades (MT5 mobile). He posts screenshots and expects instant numbers, not lessons. This is F2 evidence-based chat work: quantify from what the screenshot shows, never fabricate precision.

## Triggers
- MT5/MT4/TradingView screenshot (candles + `SELL 0.3` / `BUY 1` labels, SL/TP lines, cyan position boxes)
- "Boom" + chart = trade winning → celebrate with verified numbers
- "Ni da jalan" / "berapa untung" / "letak TP berapa" style questions

## XAUUSD contract math (MT5)
- 1.0 lot = 100 oz → a $1.00 move = $100 per lot
- P&L (USD) = |entry − current| × 100 × lots
- RM ≈ USD × 4.3–4.5 (use live rate when quoting RM)

| Price move | 0.1 lot | 0.3 lot | 0.5 lot | 1.0 lot |
|---|---|---|---|---|
| $1 | $10 | $30 | $50 | $100 |
| $5 | $50 | $150 | $250 | $500 |
| $25 | $250 | $750 | $1,250 | $2,500 |

## Reading the screenshot elements
- `SELL 0.3` / `BUY 0.5` label on a horizontal line = **entry price** of the filled order
- `SL` line = stop loss; separate `TP` line if present
- Cyan/teal rectangle zones with small corner circles = position box (entry/SL/TP markers)
- Purple/magenta dotted line with a timestamp = **current price marker**
- Red solid line = often TP or structural level; red dashed = SL line
- Header timeframe (M15/W1) sets context: W1 = structure/big picture, M15 = execution
- **Pending orders** (`SELL LIMIT` / `BUY LIMIT`) ≠ filled trades — never report them as P&L

## Reply pattern (Arif's style)
1. **Lead with the number**: current price → points/pips → USD profit → RM equivalent
2. One line validating setup (tight SL, good entry) — no lecture, no risk-management sermon, no "should I close?" theater
3. In profit → "biarkan dia jalan" (let it run); don't suggest premature close
4. No flattery openers; short, punchy Malay/slang is fine
5. If entry is not visible on the screenshot, say "dari entry ~X" (estimate) — never invent exact entry

## Worked example (2026-08-06 session)
- SELL 0.3 @ ~4282.34, SL 4282.34, current 4255.96 (M15) → ~26 pts in profit
- P&L ≈ 26.4 × $30 ≈ **$790 ≈ RM3.4k**
- Verdict delivered: reject from 4282 area, tight SL good, let it run, don't drag SL up prematurely

## Related Skills
- **`financial-chart-analysis`** — for *generating* charts with technical indicators (PSAR, RSI, MACD) when the user asks for live charts, "letak indicator", or future analysis. This skill reads screenshots; that skill creates them.

## Pitfalls
- Gold "pips" on MT5: 1.0 price unit = 1 point. Don't apply 10-pip forex conventions to gold.
- P&L is only valid as of the screenshot timestamp — the trade moves fast; if asked "now", offer to re-check live rather than extrapolating.
- Volume histogram at the bottom is context (spike = momentum), not a signal to over-explain.
