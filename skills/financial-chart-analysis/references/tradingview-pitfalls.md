# TradingView Browser Automation Pitfalls

## Indicators Dialog — Cannot Be Automated

TradingView's "Indicators, metrics, and strategies" dialog uses **custom canvas/shadow-DOM rendering**. There are ZERO standard HTML `<input>` or `<textarea>` elements in the DOM for the search field.

### What happens when you try:
1. `browser_click` on Indicators button → dialog opens (visual confirmation via screenshot)
2. `browser_snapshot` → shows dialog structure but NO input elements in accessibility tree
3. `browser_console` → `document.querySelectorAll('input')` returns empty array
4. `browser_type` → cannot find a target ref for the search field
5. `browser_press` a letter key → opens **Symbol Search** dialog instead (different dialog!)

### Root cause
TradingView renders the indicators search as a canvas-based or custom element UI. The browser's accessibility tree cannot see the input field. This is NOT a timing issue — the field never appears as a DOM input.

### Workaround
**Do not attempt TradingView indicator automation.** Go directly to Python chart generation:
```bash
python3 /path/to/scripts/psar_chart.py GC=F gold
```

## What DOES Work on TradingView via Browser

- ✅ Loading charts: `browser_navigate` to `https://www.tradingview.com/chart/?symbol=XAUUSD`
- ✅ Reading price data from the page header (StaticText elements)
- ✅ Taking screenshots for visual analysis
- ✅ Switching timeframes (if buttons are in the accessibility tree)
- ✅ Reading OHLCV data from the chart header

## Symbol Search — Partially Works
Pressing a letter key opens Symbol Search (separate from Indicators). The search field here IS accessible — you can type ticker symbols. But this only changes the chart symbol, not adds indicators.

## As of: 2026-08-09
Tested on TradingView web (non-logged-in, Browserbase standard plan without residential proxies). Logged-in or paid plans may have different rendering.
