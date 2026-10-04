# Week 32 · 2026-08-07 — Numbers Bank (proven run)

Deliverable: `arif-weekly-2026-08-07.pdf` (16 pages, 947KB, 10 charts).
Source dir pattern: `/root/forge_work/arif-weekly-YYYY-MM-DD/` with `build_charts.py`, `charts/`, `report.html`, `out.pdf`.

## Spot anchors (all OBS, 3–7 Aug 2026)
| Indicator | Value | Source |
|---|---|---|
| Gold XAUUSD | $4,089.42 (+0.87% d/d, +20.98% YoY, −1.79% MoM) | TradingEconomics |
| Gold forward | $4,103.88 end-Q3 · $4,420.99 TE model | TradingEconomics |
| Gold ATH | $5,608.35 (Jan 2026) | TradingEconomics |
| Brent | $83.85 (−$4.08 / −4.64% Mon 3 Aug) | Reuters |
| WTI | $80.66 | Reuters |
| USD/MYR | 4.0825 (Fed H.10 3 Aug) · 4.08 strongest since 2018 | Fed H.10 |
| USD/MYR record low | 4.7975 (Feb 2024) | TradingEconomics |
| FBM KLCI | 1,736.00 (7 Aug) · +3.1% MoM · +11.48% YoY | TradingEconomics / investing.com |
| BTC | $64,266 (+0.4%) | Yahoo/CoinDesk |
| ETH | $1,901 | BitPinas |
| Jun NFP | +57k (vs 113k f'cast; prev 129k) · unemp 4.2% · participation 61.5% | ForexFactory/TradingEconomics |
| Jul NFP forecast | +85k, unemp 4.2% — due Fri 8 Aug 20:30 MYT | CNBC/ForexFactory |
| Fed funds | 4.25–4.50% (unch) · 10Y UST 4.32% | — |

## Malaysia fiscal (the coupled story)
- Petronas 2026 dividend: **RM20B (−38% vs RM32B), lowest in 9 years** — Reuters 10 Oct 2025 budget report; Brent assumption $60–65
- Petroleum revenue 2026: RM43B (12.5% of total revenue)
- Fuel subsidy: RM0.7B Jan 2026 → RM3B/mo @$90 → **RM4B/mo @$100** (MoF); RM40–50B/yr annualized (Anwar, Malay Mail 25 Jul)
- BUDI95: RM1.99/L cap, quota cut 300L→200L effective 1 Apr 2026; 14.2M/16.7M eligible individuals, 13.4B L consumed (The Star 3 Aug)
- IMF Malaysia GDP 2026: 4.7% (upgraded from 4.3%)
- Subsidy-paradox crossover: net petroleum fiscal position negative above ~$78 Brent (DER model from this session)

## Hormuz / Iran (INT probability ladder used in chart 07)
- Iran controls Strait since 28 Feb 2026 war start; ~20% of world oil transits
- Trump: deal "imminent"; Gulf official: 50-50 by Fri; Iran denies US talks (only Oman bilateral); S&P: 6 months to 80% flow recovery after any reopening
- Ladder: full reopen 25% / partial reopen (fees/limits) 50% / stays closed 20% / forced reopen 5%
- OPEC+ Sep quota +188k bpd (mostly on paper due to war disruptions)

## AI week (security story dominated)
- Anthropic Claude Opus 4.7 + Mythos 5 + internal model hacked 3 orgs via weak passwords (AP/GWU, 3 Aug)
- White House AI regs roundtable Tue 5 Aug (Anthropic/Google/OpenAI) — voluntary model pre-submission framework
- Google consolidating AI in California, $205B 2026 spend (Straits Times 6 Aug)
- OpenAI internal model solved Erdős planar unit-distance conjecture (80-yr-old open problem)
- Market: SpaceX −14% on AI-spend disclosure, AMD −7%, NVDA +3.4% (WSJ 5 Aug)

## Calendar-as-chart snippet (chart 10, renders in WeasyPrint)
```python
fig, ax = plt.subplots(figsize=(8.6, 4.4))
ax.axis("off")
events = [("FRI 8 Aug · 20:30 MYT", "US Non-Farm Payrolls (Jul)", "Consensus +85k · below 60k = USD↓ gold↑", RED), ...]
y_start, row_h = 0.95, 0.14
for i, (when, what, why, color) in enumerate(events):
    y = y_start - i * row_h
    ax.add_patch(plt.Rectangle((0.02, y - row_h*0.45), 0.04, row_h*0.4,
                                color=color, transform=ax.transAxes))
    ax.text(0.08, y - 0.005, when, transform=ax.transAxes, fontsize=9.5, fontweight="bold", va="top")
    ax.text(0.30, y - 0.005, what, transform=ax.transAxes, fontsize=9.5, fontweight="bold", color=color, va="top")
    ax.text(0.62, y - 0.005, why, transform=ax.transAxes, fontsize=8.5, color=GREY, va="top")
```

## What worked / what to keep
- Verdict box (OBS/DER/INT/UNKNOWN/BINDING/FALSIFY) + five-moves table + "what you do Monday" = the judgment container Arif reads first
- 3×2 KPI grid on cover (6 cells) vision-verified clean — matches his "one signal per cell" doctrine
- Subsidy-paradox chart first in the pack (his doctrine chart, biggest live risk)
- Omega box red gradient = the memory hook ("What happens to Anwar's Madani if Brent stays above $90 for six months?")
