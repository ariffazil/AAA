# Casual Chart Mode — "Tengok sikit chart"

Two-tier chart delivery model. Match the request to the template.

## Tier 1 — Casual (Tengok sikit / Snjo chart / Chart jap)

**Trigger phrases** (Penang BM):
- "Tengok sikit chart"
- "Tengok chart"
- "Boleh tengok gold?"
- "Snjo chart"
- "Chart jap"
- "Buat chart"

**Template:** `templates/gold_casual_chart.py`

**Mode:**
- PNG + PDF in one shot
- Right-side panel: BACAAN CEPAT + RANGE only
- NO MINGGU HADAPAN panel
- NO TINDAKAN panel
- Chat-side ≤ 6 bullets

**Default chat-side bullets:**
1. Price + change
2. Bias (BULL/BEAR/NEUTRAL)
3. Key levels (one line)
4. Story (1-sentence)
5. Confirmation rule (wait for close > X / < X)
6. Disclaimer

## Tier 2 — Visual-First (full analysis)

**Trigger phrases:**
- "PDF live gold today + week trend"
- "Buat prediction untuk gold"
- "Boleh full analysis?"
- "Bagi signal lengkap"

**Template:** `templates/gold_live_weekly_pdf.py`

**Mode:**
- PNG + PDF
- Full right-side panel: BACAAN CEPAT + RANGE + MINGGU HADAPAN + TINDAKAN
- Chat-side ≤ 8 bullets

## Detection rule

When in doubt, default to Tier 1 (casual). User will say "explain" or "full" if they want Tier 2. Casual chart is the safer default because user can always ask for more — but Tier 2 over-delivers when the user just wanted to look.

## Data pipeline (both tiers)

```
1. GET http://localhost:3456/api/gold/ticker  → price, RSI, EMA, S/R
2. GET http://localhost:3456/api/gold/history?period=7d&timeframe=H1
   → 138 H1 candles + ema20/50/200 + rsi arrays
3. Take last 72 candles (axis array)
4. Render matplotlib figure with PdfPages wrap
5. Save PNG + PDF
```

## Known data quirks (2026-08-18)

- `period=3d` returns only 46 candles (insufficient for 72 visible)
- `period=4d` returns 0 (API bug)
- `period=5d` returns 92 candles
- `period=7d` returns 138 candles (recommended for casual mode)
- Live ticker fields: `price`, `change`, `changePct`, `rsi`, `rsiState`,
  `ema20`, `ema50`, `ema200`, `emaTrend`, `support[]`, `resistance[]`,
  `pivot`, `timestamp`
- History fields: `candles[]` (with time/open/high/low/close/volume),
  `ema20[]`, `ema50[]`, `ema200[]`, `rsi[]` (each is `[{time, value}, ...]`)

## Render pitfalls

- **Path:** `python3` (NOT `/root/trading/bin/python3`). System has matplotlib 3.11+ pre-installed.
- **Labels:** `xlim(-1, len(x) + 18)`, labels at `len(x) + 1.0`, `va='top'` for SL/TP1/TP2, `va='bottom'` for ZON BELI/JUAL. Otherwise LIVE marker overlaps.
- **Pyrolite warning** (`legend.bbox_to_anchor` from `~/.config/matplotlib/stylelib/pyrolite.mplstyle`) — ignore, non-fatal.
- **Confirm output:** `ls -lh /tmp/gold_live_chart.png /tmp/gold_live_intelligence.pdf` and check size > 0 before declaring "delivered." Telegram gateway sometimes drops MEDIA: links.
