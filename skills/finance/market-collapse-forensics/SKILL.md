---
name: market-collapse-forensics
description: "Use when charting how a listed company failed."
version: 1.0.0
author: Hermes Agent
tags: [finance, charting, forensic, delisted, equity, postmortem, matplotlib]
triggers:
  - "chart of a bankrupt company"
  - "how did <company> die"
  - "show me Enron / Serba Dinamik / Wirecard chart"
  - "could <company> fail without warning"
  - "why didn't the indicator warn me"
  - "is this company safe to hold"
---

# Market Collapse Forensics

Class of work: the user asks for the chart of a company that failed, asks how it failed, or asks
whether a company could fail while its chart still looks healthy. Also covers the adjacent question
about *why* a technical read cannot answer a company-viability question.

## 1. First, place the question in the right domain — state this, don't imply it

The user usually arrives with a technical-tool question and the real question is about the books.
Answer the domain question first; it reframes everything after it.

| | Commodity (gold, oil) | Listed company |
|---|---|---|
| Price reads | what people **pay** | what people **believe** |
| Hidden books to be wrong about | none | statements, auditor sign-off, insider knowledge |
| Is the chart the thing itself? | **yes** — no counterparty, no report to forge | **no** — it is the shadow of the books |
| What technical levels encode | the market's own structure | often the trail of insiders exiting |
| Fundamental layer | noise intraday, regime-relevant over weeks | decisive, and invisible in price |

Both sides of this can be true in one conversation: the trader who says "for gold I don't need
fundamentals" is correct, and the analyst who says "for a company I want the books first" is also
correct. They are not in conflict — they are different domains. Say so; the user is often being
pressed to pick a side by someone else and does not need to.

**Wholly private / wholly state-owned entities have no chart at all** — no ticker, no insider able
to press sell, therefore none of the mechanisms that turned a public collapse into a visible event.
The only comparable measure is distributions out to the owner versus capex back in, and only
insiders can see it. When the user is an insider of such an entity, that observation *is* the answer.

## 2. What a chart can and cannot evidence about a company

- **Cannot:** show fraud, or distinguish fraud from an ordinary decline.
- **Can:** show a **lower-high / lower-low staircase** — support breaks, price retests and fails at
  resistance, support breaks again. That is the record of who already left, and it is a *question
  generator*, not a verdict.
- The insiders exiting cannot say anything, but they can sell, and the selling prints. You cannot
  read "this company is lying" from a chart; you can read "the people who know are leaving," and
  then ask why.
- **The most attractive candles often print closest to death.** There is no warm-up: the failure is
  a cliff, not a slope. "It still looks technically healthy" is not evidence of soundness.
- Cost asymmetry makes the staircase actionable even without diagnosis: exiting a healthy company
  early costs a missed rally; staying in a dead one costs everything.
- **Do not answer a company-viability question with more indicators.** Widening a five-indicator
  read to nine buys less trading, not more information. Only three things raise signal quality —
  knowing something others don't, knowing where stops sit, strict sizing — and none come from a chart.
- **A signature is only worth what the signer's independence is worth.** The recurring anatomy is a
  *paid* auditor signing statements the company wrote. The useful question is not "are the numbers
  right" but "who checked, and were they free of the party that profited."

## 3. Procedure

1. **Classify the domain** (§1). Commodity → ordinary technical chart. Company → continue here.
2. **Identify the trigger and the terminal print.** The audit refusal / disclosure date and the last
   tradable price. These two anchors make the narrative legible; everything else is filler.
3. **Reconstruct the price series** — delisted tickers have no feed, so it must be rebuilt from
   documented closes. See `references/postmortem-candle-render.md` §1.
4. **Render** the annotated candle chart — `references/postmortem-candle-render.md` §2 for the
   matplotlib recipe and §3 for the layout that reads.
5. **State the reconstruction method on the artifact.** A footer line naming sources and saying
   "reconstructed for reading SHAPE, not a tick feed" is mandatory. Reconstructed candles presented
   as exchange OHLC is a fabrication.
6. **Verify before delivering** — `vision_analyze` the render with a layout question (overlapping
   annotations, clipped labels), fix, re-render. This catches real collisions and is cheaper than
   the user finding them.
7. **Deliver with the domain framing attached**, then the chart. The chart alone invites the wrong
   conclusion.
8. **Close with what would actually answer the question** — the document, the signer, the insider
   trail — not another indicator.

## 4. Anatomy of a collapse (the shape to expect)

Every reconstruction the user asks for tends to show the same five phases:

1. **Long flat base** — years of unremarkable, profitable, *boring* operation. Nobody writes about it.
2. **Parabola** — vertical advance over months. This is the phase everyone remembers and joins.
3. **Roll-over** — red/green/red/green chop with **lower highs**. The trap: it reads as a
   bull-market pullback.
4. **The audit candle** — one enormous red body on the disclosure date. This is the pivot, and by
   the time it prints price has typically already given back most of the parabola.
5. **Graveyard** — tiny candles near zero, then suspension, then delisting.

Phase 4 is where the lesson lands: the audit is not the cause, it is the moment everyone else found out.

Canonical peak/trough/trigger markers for the companies this gets asked about live in
`references/collapse-markers.md` — reuse them rather than re-researching.

## 5. Pitfalls

- **Do not loop on `yfinance` for a delisted symbol.** It returns zero rows and logs `possibly
  delisted; no timezone found`. That is not transient — the series is gone from the vendor. Go
  straight to source harvest.
- **Do not present a reconstructed series as market data.** Method note on the artifact, always.
- **`plt.Rectangle` is not exported** — import `Rectangle` from `matplotlib.patches`.
- **Datetime x-coordinates need `mdates.date2num()`** before building a rectangle; width is in
  fractional days. `ax.plot([dt, dt], [lo, hi])` accepts datetimes directly.
- **Give candle bodies a minimum visible height** or a near-zero close renders invisible and the
  collapse becomes unreadable.
- **Strip the pandas index timezone** (`tz_localize(None)`) before comparing against naive
  `datetime(...)` literals, or you get
  `Invalid comparison between dtype=datetime64[s, Asia/Kuala_Lumpur] and datetime`.
- **`fig.add_axes((l, b, w, h))` needs a tuple**; a list trips the type checker.
- **Escape `$`** out of every string passed to matplotlib (LaTeX). Write `USD` / `RM`.
- **The pyrolite `legend.bbox_to_anchor` warning is noise** — the figure still renders.
- **Convert to JPEG before `MEDIA:` delivery.** PNGs from these renders run 1–2 MB and the chat
  render is more reliable around 300 KB.

## References

- `references/postmortem-candle-render.md` — data harvest path + matplotlib candle recipe + layout
- `references/collapse-markers.md` — verifiable peak / terminal / trigger points per company
