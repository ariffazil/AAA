---
name: financial-distress-forensics
description: "Use when assessing if a listed company can fail."
version: 1.0.0
license: MIT
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# financial-distress-forensics

> Assess solvency from filed statements — not from price charts, and not from prediction.
> Covers: reading balance sheets for barrier distance, sourcing filings for companies that
> already died, separating erosion from fabrication, and delivering it as a figure.

## The routing decision that governs everything

Two questions look identical and are not:

| Question | Answerable? | What to do |
|---|---|---|
| "Will the price go up or down?" | **No** | Say so plainly, then pivot. Do not produce a direction call. |
| "How far is this company from its debt barrier, and how fast is it closing?" | **Yes — arithmetic** | Answer this. |

Direction prediction has been tested and fails: a signal *sensitive* to collapse produces far
too many false alarms to act on, and a blind-control baseline matches an "analysis" that never
looked at the data. Report that result when asked for a forecast — it is the honest answer and
it redirects to the work that can be done.

## Procedure

1. **Name the failure mode you are testing for.** Erosion (a firm shrinking toward its barrier)
   and fabrication (books that look fine while cash never arrives) need *different* detectors.
   Deciding first prevents building the wrong model. See `references/barrier-distance-model.md`.
2. **Source the filings, not the chart.** Registries carry the dead; free price APIs drop
   delisted tickers, so a price-based panel is survivors-only. Route to the filings API first.
   Recipe and tag list: `references/sec-edgar-xbrl-lanes.md`.
3. **Verify the entity before using its data.** Registrant identifiers get reused after a filer
   dies — a dead company's ID still returns data belonging to somebody else. Match the entity
   name against the expected filer, and reject on mismatch. Same rule in reverse for
   hand-collected figures: confirm which legal entity and which fiscal period a number
   actually describes.
4. **Compute the barrier series.** Distance = ln(assets / liabilities) per fiscal year;
   closing rate = the year-over-year change in that distance; time-to-barrier = distance ÷
   closing rate. A *negative* closing rate (distance widening) means unbounded time — report it
   as such, not as a large number.
5. **Compute the cash pair alongside it, always.** Operating cash flow ÷ reported profit, and
   cash ÷ total borrowings. Never publish the barrier number without these two: the barrier
   term has the reported asset figure in its numerator, so it cannot see an asset-side
   fabrication.
6. **Validate against known deaths before presenting.** Take companies that actually failed and
   measure them in the years *before* the event. A model only backtested on survivors has not
   been tested. Report which cases it caught and which it missed, by name.
7. **Deliver as a figure.** See *Delivery* below.

## Hard rules

- **Never interpolate a missing period.** If a source does not carry a fiscal year, leave a
  visible gap and say a source is missing. A smoothed line through a hole in a filed balance
  sheet is fabrication.
- **Every number carries its source and its period.** Annual reports change fiscal year-ends; a
  column labelled with a year may be an 18-month stub. State the period convention before the
  first number.
- **Separate "eroded" from "stole".** Buying assets at a cycle peak on debt is a bet that lost.
  Falsifying records is a different act. Both end in failure and only one is fraud — say which
  you are describing, and never imply the other.
- **Investigations are not findings.** If a regulator has opened a file, report the file's
  existence and that no one has been found liable. Do not let proximity imply guilt.
- **When the principal names a person + role + period, verify all three against a source before
  analysing on it.** A mis-stated attribution published back to them damages *them*, not the
  person named. Correct it once, plainly, then continue with the analysis underneath — the
  underlying instinct is usually right even when the attribution is not.
- **Attribute a failure to whoever signed when the liability was created, and check whether they
  were still in post when it matured.** Long lags are the norm (see Pitfalls).

## Delivery (this principal's format)

Mathematical exposition is not the deliverable. He has said so directly. Therefore:

- **Lead with the rendered figure.** Numbers live *inside* the chart; chat prose carries the
  meaning, not the arithmetic.
- **Dark background, gold accents** — the standing visual house style.
- **Short prose around the figure, in his register.** One idea per line. Name the consequence,
  not the method.
- **Render, then LOOK at the render before sending.** Load the saved image through the vision
  tool and check every label, footer and axis. Clipping and overlap are the default failure:
  text laid over a shaded band, a two-line footer colliding with the panel beneath it,
  annotations stacking on a shared axis. Fix and re-render; do not send an unchecked figure.
- **Show the gap you cannot fill.** Annotate missing years as missing.

## Pitfalls

- **A model whose numerator is the falsified line item cannot see the falsification.** Inflating
  assets widens the computed distance, so the barrier score improves exactly when the company is
  lying. Always pair it with the cash detectors.
- **Cash ÷ total borrowings is the hardest signal to fake** because it needs money that actually
  arrived. A monotone year-on-year decline with no restatement is a stronger warning than any
  single ratio being low.
- **A reported loss is not automatically fatal.** Depreciation and impairment are non-cash; a
  firm can report a loss and still generate operating cash. Read the cash pair, not the earnings
  headline.
- **A price chart is a measurement, never a mechanism.** It shows what participants believe now;
  it does not show cause. Reading it for "why" is how a chart gets mistaken for a diagnosis.
- **Long lags are the norm — five to eight years.** Debt taken at a peak becomes unavoidable loss
  much later, by which time the signatories have moved on. This is why the incumbent executive is
  often an inheritor, not an author.
- **Do not let a single validated case become a general claim.** If the model catches one
  well-documented collapse and misses another, both belong in the write-up.
- **Erosion-based models miss shocks.** A balanced firm hit by an exogenous price collapse shows
  *improving* leverage as it approaches failure. State this limit in every write-up.

## References

- `references/barrier-distance-model.md` — the derivation, the two failure modes, and measured
  separation.
- `references/sec-edgar-xbrl-lanes.md` — filing-data API recipe, tag fallbacks, the
  identifier-reuse trap, and non-US issuer routing.
