"""
gold_casual_chart.py — Casual "Tengok sikit chart" mode (2026-08-18)
====================================================================

Use when Arif asks briefly: "Tengok sikit chart", "Tengok chart", "Boleh
tengok gold?", "Chart jap", "Snjo chart". NOT for full "PDF live gold today
+ week trend" requests — that's templates/gold_live_weekly_pdf.py.

Differences from gold_live_weekly_pdf.py:
- SIMPLER right-side panel: BACAAN CEPAT + RANGE only. Skip MINGGU HADAPAN
  and TINDAKAN panels (user wants the picture, not analysis).
- Chat-side ≤ 6 bullets (not 8).
- Period=7d H1 (138 candles) → last 72 visible. NOT 3d (only 46 candles).
- Bar `python3` (NOT `/root/trading/bin/python3` — that venv doesn't exist).

Inputs:
  - http://localhost:3456/api/gold/ticker (live price, RSI, EMA, S/R)
  - http://localhost:3456/api/gold/history?period=7d&timeframe=H1

Outputs:
  - /tmp/gold_live_chart.png (~250KB @ 150 DPI landscape)
  - /tmp/gold_live_intelligence.pdf (~50KB single page)
"""

import json
import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages
from pathlib import Path

# ---- LIVE DATA -----------------------------------------------------------
hist = json.loads(
    subprocess.run(['curl', '-s', '--max-time', '10',
                    'http://localhost:3456/api/gold/history?period=7d&timeframe=H1'],
                   capture_output=True, text=True).stdout
)
ticker = json.loads(
    subprocess.run(['curl', '-s', '--max-time', '10',
                    'http://localhost:3456/api/gold/ticker'],
                   capture_output=True, text=True).stdout
)

# Take last 72 H1 candles (~3 days of H1)
candles = hist['candles'][-72:]
ema20 = np.array([z['value'] for z in hist['ema20'][-72:]])
ema50 = np.array([z['value'] for z in hist['ema50'][-72:]])
ema200 = np.array([z['value'] for z in hist['ema200'][-72:]])
rsi_arr = np.array([z['value'] for z in hist['rsi'][-72:]])

x = np.arange(len(candles))
close = np.array([z['close'] for z in candles])
op = np.array([z['open'] for z in candles])
hi = np.array([z['high'] for z in candles])
lo = np.array([z['low'] for z in candles])

# ---- LEVELS (from ticker + recent swing) ---------------------------------
price = ticker['price']
supports = ticker['support']
resistances = ticker['resistance']

# Build buy/sell zones near current price
buy_low, buy_high = supports[0], supports[1] if len(supports) > 1 else supports[0]
sell_low, sell_high = resistances[0], resistances[1] if len(resistances) > 1 else resistances[0]

# SL below buy zone, T1/T2 above sell zone
sl = round(buy_low - 5)
t1 = round(sell_high + 8)
t2 = round(t1 + 18)

# Sentiment tag
ema20_now = ticker['ema20']
ema50_now = ticker['ema50']
ema200_now = ticker['ema200']
rsi_now = ticker['rsi']

if price < ema20_now < ema50_now:
    sentiment = 'BEARISH (H1)'
elif price > ema20_now > ema50_now:
    sentiment = 'BULLISH (H1)'
elif abs(price - ema50_now) < 3:
    sentiment = 'NEUTRAL @ EMA50'
else:
    sentiment = 'NEUTRAL'

# Recent swing high/low for context
recent_high = round(max(hi.tolist()), 1)
recent_low = round(min(lo.tolist()), 1)

# ---- RENDER --------------------------------------------------------------
plt.rcParams['font.family'] = 'DejaVu Sans'
fig = plt.figure(figsize=(11.69, 8.27), facecolor='#0d1117')

# Main chart axis
ax = fig.add_axes([.06, .22, .68, .62], facecolor='#0d1117')

# Candles
for i in x:
    is_bull = close[i] >= op[i]
    color = '#3fb950' if is_bull else '#f85149'
    ax.vlines(i, lo[i], hi[i], color=color, lw=1.1, zorder=2)
    body = max(abs(close[i] - op[i]), 0.3)
    y = min(op[i], close[i])
    ax.add_patch(Rectangle((i - .32, y), .64, body,
                           facecolor=color, edgecolor=color, lw=.8, zorder=3))

# EMAs
ax.plot(x, ema20, color='#58a6ff', lw=2.0, label='EMA 20')
ax.plot(x, ema50, color='#f0883e', lw=2.0, label='EMA 50')
ax.plot(x, ema200, color='#b48ead', lw=1.4, label='EMA 200')

# Zones
ax.axhspan(buy_low, buy_high, color='#3fb950', alpha=.16)
ax.axhspan(sell_low, sell_high, color='#f85149', alpha=.16)

# SL/TP lines
ax.axhline(sl, color='#f85149', ls='--', lw=1.4, alpha=.9)
ax.axhline(t1, color='#3fb950', ls=':', lw=1.4, alpha=.9)
ax.axhline(t2, color='#39d2c0', ls=':', lw=1.4, alpha=.9)

# Current price marker
ax.scatter([x[-1]], [price], s=90, color='#f0a500', zorder=6, edgecolor='#0d1117', linewidth=1.5)
ax.text(x[-1] + 1.2, price, f'LIVE  {price:,.2f}',
        color='#f0a500', fontsize=12, weight='bold', va='center')

# Right-side labels — OFFSET to avoid overlap with LIVE marker
ax.set_xlim(-1, len(x) + 18)
for yv, label, col, va in [
    (buy_high + 1.5, f'ZON BELI {buy_low:.0f}-{buy_high:.0f}', '#3fb950', 'bottom'),
    (sell_low + 1.5, f'ZON JUAL {sell_low:.0f}-{sell_high:.0f}', '#f85149', 'bottom'),
    (sl, f'SL {sl:.0f}', '#f85149', 'top'),
    (t1, f'TP1 {t1:.0f}', '#3fb950', 'top'),
    (t2, f'TP2 {t2:.0f}', '#39d2c0', 'top'),
]:
    ax.text(len(x) + 1.0, yv, label, color=col,
            fontsize=10, weight='bold', ha='left', va=va)

ax.grid(alpha=.15, color='white')
ax.tick_params(colors='#e6edf3')
for s in ax.spines.values():
    s.set_color('#30363d')
ax.set_ylabel('USD / oz', color='#e6edf3', fontsize=11)
ax.set_title('XAUUSD — LIVE H1 | 72 candles (~3 hari)',
             color='#f0a500', fontsize=16, weight='bold', loc='left', pad=10)
ax.legend(facecolor='#161b22', labelcolor='#e6edf3', loc='upper left', ncol=3, fontsize=10)

# RSI tiny panel below
ax_rsi = fig.add_axes([.06, .10, .68, .08], facecolor='#0d1117')
ax_rsi.plot(x, rsi_arr, color='#b48ead', lw=1.4)
ax_rsi.axhline(70, color='#f85149', ls=':', lw=.8, alpha=.5)
ax_rsi.axhline(30, color='#3fb950', ls=':', lw=.8, alpha=.5)
ax_rsi.axhline(50, color='#8b949e', ls=':', lw=.6, alpha=.4)
ax_rsi.fill_between(x, 30, 70, color='#161b22', alpha=.4)
ax_rsi.set_ylim(15, 85)
ax_rsi.set_xlim(-1, len(x) + 18)
ax_rsi.set_ylabel('RSI', color='#e6edf3', fontsize=9)
ax_rsi.tick_params(colors='#e6edf3', labelsize=8)
for s in ax_rsi.spines.values():
    s.set_color('#30363d')

# Right-side panel — CASUAL MODE: BACAAN CEPAT + RANGE ONLY
panel = fig.add_axes([.77, .10, .20, .74], facecolor='#161b22')
panel.axis('off')

panel.text(.06, .97, 'BACAAN CEPAT', color='#f0a500',
           fontsize=14, weight='bold', transform=panel.transAxes)

sent_color = '#f85149' if 'BEAR' in sentiment else '#3fb950' if 'BULL' in sentiment else '#e6edf3'
panel.text(.06, .92, sentiment, color=sent_color,
           fontsize=13, weight='bold', transform=panel.transAxes)

panel.text(.06, .86, f'Harga: {price:,.2f}', color='#e6edf3', fontsize=11,
           weight='bold', transform=panel.transAxes)
panel.text(.06, .815, f'Change: {ticker["change"]:+.2f}  ({ticker["changePct"]:+.2f}%)',
           color='#f85149' if ticker['change'] < 0 else '#3fb950',
           fontsize=10, transform=panel.transAxes)
panel.text(.06, .775, f'RSI: {rsi_now:.1f}  ({ticker["rsiState"]})',
           color='#e6edf3', fontsize=10, transform=panel.transAxes)
panel.text(.06, .735, f'EMA20: {ema20_now:.2f}',
           color='#58a6ff', fontsize=9, transform=panel.transAxes)
panel.text(.06, .700, f'EMA50: {ema50_now:.2f}',
           color='#f0883e', fontsize=9, transform=panel.transAxes)
panel.text(.06, .665, f'EMA200: {ema200_now:.2f}',
           color='#b48ead', fontsize=9, transform=panel.transAxes)

panel.text(.06, .585, 'RANGE 3 HARI', color='#39d2c0',
           fontsize=13, weight='bold', transform=panel.transAxes)
panel.text(.06, .545, f'Tinggi: {recent_high:.1f}\n'
                       f'Rendah: {recent_low:.1f}\n'
                       f'Span: {recent_high-recent_low:.1f} pts',
           color='#e6edf3', fontsize=10, va='top', linespacing=1.6,
           transform=panel.transAxes)

# Footer — epistemic + disclaimer (clear of side panel)
fig.text(.06, .035,
         f'[OBS] Live feed {ticker["timestamp"]} · 72 H1 candles · EMA/RSI server-side. '
         f'[DER] Level S/R dari ticker + swing 3 hari. '
         f'[INT] Plan = senario, bukan jaminan.',
         color='#8b949e', fontsize=8)
fig.text(.06, .012,
         'Bukan nasihat kewangan. Sahkan spread, broker & candle live sebelum sebarang tindakan.',
         color='#f85149', fontsize=8)

# Save outputs
fig.savefig('/tmp/gold_live_chart.png', dpi=150, facecolor=fig.get_facecolor())
with PdfPages('/tmp/gold_live_intelligence.pdf') as pdf:
    pdf.savefig(fig, facecolor=fig.get_facecolor(), bbox_inches='tight')
plt.close(fig)

print(f"Chart saved: /tmp/gold_live_chart.png")
print(f"PDF saved: /tmp/gold_live_intelligence.pdf")

import os
print(f"PNG size: {os.path.getsize('/tmp/gold_live_chart.png')} bytes")
print(f"PDF size: {os.path.getsize('/tmp/gold_live_intelligence.pdf')} bytes")
