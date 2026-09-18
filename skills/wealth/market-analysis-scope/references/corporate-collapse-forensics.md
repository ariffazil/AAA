# Corporate Collapse Forensics

Covers: comparison charts of failed/delisted companies, candlestick reconstruction for dead tickers, and the printed distribution signature.

## When this applies

User asks to see "a company that went bankrupt", wants two collapses compared, or wants to see how a chart looked *before* the company died. This is a lesson-teaching request, not a trade request — the deliverable's job is to make a pattern legible, not to price a trade. Do not add entry/SL/TP grammar.

## Data: a delisted ticker has no OHLC

`yfinance` returns **zero rows** for delisted symbols, and exchange feeds stop paginating daily history. Treat this as "reconstruct it", never as "no data available" — and never as licence to invent a plausible series.

Reconstruct from documented closes at event dates:

- news-wire closing prices at named events (Reuters / The Edge / FT),
- exchange end-of-day or OTC archival price tables,
- year-end series from market-data aggregators,
- peer-reviewed case studies, court and regulator filings (e.g. SEC Form 8-K) for the terminal prints.

Body = open→close from reported closes. Wick = reported intraday range where documented, otherwise a modest modelled range — do not invent dramatic wicks.

**State the reconstruction method in the chart footer**, naming the sources and saying the chart is built for reading shape, not as a tick feed. A reconstructed candle chart that reads as live data is a fabrication.

## The universal silhouette (4 phases)

1. **Long base** — years of unremarkable, orderly candles. Nothing to see; nobody writes about it.
2. **Parabola** — vertical candles, index inclusion, analyst coverage, the name becomes well known.
3. **Roll-over with failed rallies** — lower highs against each broken support. This phase looks like "a correction" and is the informative one.
4. **Cliff** — one session, or one filing, converts years of apparent value into cents. Then flatline, suspension, delisting.

## Collapse chronology (verified cases)

| Company | Market | Peak | Terminal | Loss |
|---|---|---|---|---|
| Enron | NYSE: ENE | $90.75, Aug 2000 | $0.36 close 29 Nov 2001; Ch.11 2 Dec 2001 | −99.6% in 15 months |
| Wirecard | DAX | €226.39, Sep 2018 | insolvent Jun 2020; final trade €0.05 Jul 2024 | −99.98% |
| Serba Dinamik | Bursa 5279 | RM2.42, Jan 2020 | RM0.02; delisted 5 Jun 2024 | −99.2% |

Common structure across all three: the peak is the highest-quality phase on the chart (no reversal signal, neutral RSI, aligned EMAs, healthy volume), and the audit/flag event that is later described as the cause occurs **after** the price has already lost roughly two thirds from the peak.

## Rendering recipe

- **Two stacked panels, one per company, identical layout.** The comparison is the message — do not vary scales or annotation styles between panels.
- One accent colour per panel (e.g. red for the first, gold for the second); keep one shared visual grammar.
- Shade the collapse window as a translucent band; use a distinctly darker block for the suspended/delisted stretch where no trading occurred.
- One summary callout per panel, inside the plot area top-right: `PEAK → TERMINAL` plus the percentage. Place it where the price has already flatlined so it covers no data.
- Annotate 4–6 dated events per panel (audit flag, suspension, insider exit, terminal close). Fewer, well-placed, beats many.
- Give the panel headroom above the peak so the peak annotation clears the title.
- Dark theme: bg `#0d0d0d`, text `#f5f0e8`, gold `#d4a843`, red `#c0392b`, green `#27ae60`, grey `#888888`, callout fill `#161628`.

## Pitfalls

- **Summary box or peak annotation colliding with the panel title.** Add y-limit headroom above the peak and offset the peak label upward; verify by reading the render back (see SKILL.md pitfall).
- **Density is not authority.** Five label boxes inside a three-year collapse zone makes leader lines cross and destroys the shape. Space them; pull the outermost label back inside the plot boundary so it is not clipped.
- **Colour by candle direction only** — never tint candles by trend. Alternating bull/bear colours across a down-trend mislead.
- **Dated event labels are the payload.** The chart's job is to show that the informative events all arrived *after* the damage; pick annotations that make that ordering visible.
