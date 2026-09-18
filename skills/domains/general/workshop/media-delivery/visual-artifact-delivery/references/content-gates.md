# Content gates for a recurring artifact

Page geometry gates (page count, text layer, ink, leaked internals) prove the artifact RENDERED.
They say nothing about whether its CONTENT is still true. A recurring card — a daily brief, a weekly
digest, a standing dashboard — needs a second gate class that runs on the claims themselves.

## The gate ladder

| # | Rule | Refuses when |
|---|---|---|
| components | Exact count and numbering | A slot is missing, extra, or mis-numbered |
| tier balance | Each epistemic tier has its declared count | Sourced and unsourced content have drifted together |
| sourcing | Grounded tiers carry a source | A news/market/deadline line has none |
| **freshness** | Price/rate claims carry a DATE in the source, within a staleness limit | A real citation with a stale number |
| **no frozen counts** | Prose cites a date, never a computed day-count | A countdown was written into text |
| duplication | No two slots share a subject | The same item appears twice under two labels |
| privacy | No private marker, no first-person causal clause | The card explains why an item was chosen |
| attribution | Every quote has a real, checkable author | A quote is unattributed or attributed to "unknown" |
| anchors | Each subject's permanent interests are represented | A recurring section lost the thing it exists for |
| relevance | Every reader receives something | One subject's lane is empty |

Order matters in one place: run the **privacy** gate before the artifact exists, because once bytes
exist the cheapest path is to send them anyway.

## Freshness — presence is not currency

A citation proves the citation exists. It says nothing about whether the figure is current.

- Require a **date inside the source string**, not merely a source name, on any price/rate/market line.
- Set an explicit staleness limit. Four days is generous for market data; tighter for intraday.
- **Scope the rule to price-bearing lines.** Applying "must be dated within N days" to every numeral
  false-fails legitimate low-frequency series — monthly unemployment, annual fiscal figures — and a
  gate that fires on healthy input gets weakened within a week.
- A stale but properly-sourced number is *more* dangerous than an unsourced one, because it reads as
  verified. Budget a re-verify step rather than trusting yesterday's pull.

## Never store a countdown — compute it at render

A day-count written into prose or a field is frozen at authoring time. It does not error; it keeps
saying the old number, silently, forever.

```
WRONG   "Budget 2027 in 21 days"        # true once, wrong forever after
RIGHT   "Budget 2027 tabled 9 October"  # the date is the durable fact
        renderer: days = target - now   # the countdown is a VIEW of the date
```

So: store `target_date`, compute `delta = target_date - render_time`, and let prose cite dates while
the renderer owns every countdown. Expire passed events out of the pool automatically — a stale
countdown is worse than a missing one.

**Guard the false positive.** A deep-time or historical figure is a fact, not a clock. `"11,000
tahun"` (an archaeological age) and `"300 juta tahun dulu"` are not countdowns. Exclude year-scale
units entirely, and exclude numbers carrying a thousands separator, before flagging a day/week/month
value under a near-term threshold.

## Rank by consequence, not by proximity

For a clock surface, nearest-first is the wrong sort and it looks plausible enough to survive review.
Score on `urgency x consequence x actionability x confidence`, with a non-linear urgency curve that
saturates near the date and flattens far out. A high-consequence item three weeks away must outrank a
housekeeping deadline three days away, or the surface is answering the wrong question.

## Prove the gate can REFUSE

A gate that only ever says PASS is indistinguishable from no gate. Every rule needs a companion suite
of deliberately-broken inputs that MUST be rejected, plus at least one legitimate input that must
still pass.

```python
CASES = [
    ("good artifact passes",              lambda c: None,                       "PASS"),
    ("one slot missing",                  lambda c: c["rows"].pop(),            "HOLD"),
    ("grounded row with no source",       drop_source,                          "HOLD"),
    ("stale price in a real source",      age_the_source,                       "HOLD"),
    ("frozen day-count in prose",         freeze_a_count,                       "HOLD"),
    ("private marker leaks",              leak_a_causal_clause,                 "HOLD"),
    ("quote with no author",              drop_attribution,                     "HOLD"),
    ("deep-time figure is not a clock",   set_an_archaeological_age,            "PASS"),
]
```

The final line is as important as the refusals: it is the false-positive guard. A suite made only of
"must reject" cases will happily pass a gate that rejects everything.

## On a HOLD: fix the content, never the threshold

State it in the gate's own output, because that is where it is read:

> Fix the content. Do not lower a threshold to pass.

The pressure to relax a gate peaks exactly when it is doing its job — one slot short, one figure
unchecked, one deadline looming. A gate that can be widened to pass is a suggestion, not a wall.

Report the refusal as a finding, not a failure: which rule fired, on which slot, and what would clear
it. The refusal IS the output when it prevents a wrong artifact reaching a human.
