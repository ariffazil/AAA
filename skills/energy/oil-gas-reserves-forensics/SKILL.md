---
name: oil-gas-reserves-forensics
description: "Use when auditing oil and gas reserves numbers (RRR, 2P)."
version: 1.0.0
risk_tier: low
floor_scope: [F2]
tags: [oil-gas, reserves, PRMS, RRR, audit, national-oil-company]
---

# Oil & Gas Reserves Forensics

> A reserves disclosure rarely prints enough to be checked. The work is to derive what is missing from
> what is printed, then ask for the lines that would close it.

## When this applies

- Any number from a reserves statement: RRR / reserves replacement, reserve life index, 1P / 2P / 2C,
  net entitlement volumes, "portfolio rationalisation", deconsolidation of a JV or farm-out.
- A peer agent, a broker note, a minister or the company itself argues a thesis *from* reserve numbers
  and someone will open the statement beside it.
- A career, budget or sovereign-risk question is being answered with a reserves statistic.

Not for production forecasting, price decks, or reserve *estimation* methodology. This is the audit of
what is disclosed.

## Always-on rules

1. **Label every number twice** — classification (1P / 2P / 2C) and basis (net entitlement vs gross /
   working interest; boe vs liquid-only). Two numbers on different bases are not comparable, and the
   sentence that compares them is false even when both figures are exactly right.
2. **A ratio question gets a ratio answer.** Additions ÷ production is invariant to the basis of both.
   Correcting the production basis cannot rebut an RRR — it lands beside the load-bearing step. Check
   where your correction lands before delivering it.
3. **The deliverable is usually a demand, not a verdict.** Statements print opening, closing and ratios;
   the four reconciliation lines that would settle the argument are the ones missing. Ask for them.
4. **Assume the company is honest and still cannot be checked.** The finding is the absent table, not a
   lie. That framing survives contact with insiders and cannot be rebutted.
5. **Never quote a reserve-life year as a forecast.** The invariant is barrels lost per year; the year
   the index lands on depends on a production assumption the company controls.

## Procedure

1. **Pull the primary** — the reserves section of the integrated/annual report, or the 10-K / 20-F
   reserves note, never a news summary. Note the measurement date: usually 1 January, so the movement
   belongs to the *prior* year.
2. **Pin the denominator** by backing it out of every published ratio and keeping the one figure that
   makes all of them cohere (see algebra below). A ratio is only usable once its denominator is known.
3. **Compute net additions:** `closing − opening + production`. One line answers "did they replace what
   they produced" without needing the company's reconciliation at all.
4. **Run the impossibility test.** Rescuing the 2P decline entirely through disposals implies a 2P RRR
   near 1.0 while 1P RRR sits at 0.3 and 2C is shrinking. Three published numbers that cannot all hold
   is the strongest finding available, because it needs no external source.
5. **Date-check every claimed cause.** A transaction effective after the measurement date cannot cause
   the movement measured at that date. Farm-outs, divestments and JV formations are the usual alibi and
   the usual error.
6. **Size the cause's capacity.** With the right denominator, compute the share of the decline that
   production explains, then what is left. If the leftover is small, no portfolio story can fill it —
   report the ceiling, not the floor.
7. **Write the ask:** opening, discoveries/extensions, technical revisions, economic revisions,
   production, disposals/transfers, closing. Peers publish all six.

## The algebra, with worked numbers

Given 2P 7.92 bn boe, 2C 13.16 bn boe, RRR 0.3 (1P), RLI 9.9 yrs (1P), ORLI 38.6 yrs (2P+2C), group
production ~2,334 kboe/d gross (0.852 bn/yr):

```
production (entitlement) = (2P + 2C) / ORLI = 21.08 / 38.6 = 0.546 bn boe/yr   (~64% of gross)
1P                       = RLI × production  = 9.9 × 0.546 = 5.41 bn boe     (68% of 2P)
check                    = 2P / production = 7.92 / 0.546 = 14.5 yrs          (not the 9.9 — that is 1P)
2P opening               = 7.92 / 0.92 = 8.609
net additions (2P)       = closing − opening + production = 7.92 − 8.609 + 0.546 = −0.143 bn boe
annual loss (1P)         = (1 − 0.3) × 0.546 = 0.382 bn boe/yr
```

0.382 is the invariant to argue over. Life falls ~0.7 yr/yr only if production is held flat at 0.546;
if the company defends the life index instead, production falls and the barrels lost stay 0.382. Argue
the barrels — "life drops to 6.4 years by 2031" is one branch, and it is the branch an insider waves
away with "production decline is natural".

**The mixed-basis test:** back out the implied denominator from *each* derived figure and check they
match. 7.92 / 0.546 = 14.5 kills a 20.7-year figure borrowed from a 0.383 denominator; 0.383 also
inflates 2P+2C life to 55 yrs, contradicting the printed 38.6. Keep the denominator that makes the whole
set cohere, and say which one you kept and why — the rejected one is not wrong, it measures something
else.

**Sensitivity of the residual:** on the entitlement basis (0.546) production explains ~79% of a 0.689 bn
2P decline, leaving ~0.14 bn for revisions plus disposals. On the gross basis (0.852) it explains ~56%,
leaving ~0.30 bn. Pick one basis and stay in it; the conclusion (no sale can fill the gap) holds either
way, and mixing the two is what invites the correction.

**What RRR can and cannot absorb.** RRR is additions ÷ production, so it is invariant to the basis of
both. Disposal volumes sit outside the numerator by definition (a separate PRMS reconciliation line from
technical and economic revisions), so rationalisation cannot *explain* a low RRR. It does move the
printed number one way: selling mature, high-production assets shrinks the denominator faster than the
numerator, so the printed RRR **rises** — which makes a low printed RRR a *floor* on the organic number,
not a ceiling. That framing is sharper than the raw figure and cannot be waved away.

**Deconsolidation (any 50:50 farm-out).** 100% leaves the consolidated line, 50% returns as an
equity-accounted interest, so the net removal is **half the gross booked volume**. Pin the asset's booked
size before quoting a delta: 3 bn gross → 1.5 bn removed ≈ 19% of a 7.92 bn base; a 0.75 bn delta implies
only 1.5 bn gross, so size and delta cannot both be quoted.

**Two readings of a falling 2C.** Maturation lag (discovered volumes not yet proved — time, benign) or
commercial failure (projects below threshold on cost or contract terms — price, worse, and not a
geologist's problem to fix). A 2C decline running ~2.9× the 2P decline points at the second. State the
caveat: 2C sits on the same entitlement basis and carries the same price sensitivity, so the divergence
is not pure volume — "unexplained by price" is the honest claim.

## Pitfalls

- **Basis stitching** — one derived figure on an entitlement denominator, the next on gross, in the same
  breath. Two denominators cannot both be true; the wrong one typically inflates a life index ~40%.
- **Date pairing** — a farm-out completing in the following year or a JV effective mid-year cannot
  explain a movement measured at 1 January. Check transaction date against portrait date.
- **A 50:50 farm-out removes half, not all.** Quoting the full gross volume as the loss double-counts
  the retained equity interest.
- **boe vs liquid** — gas is inside the RRR. Mixing a boe stock with a liquid-only flow yields a
  plausible, wrong answer.
- **Definition drift between reporting years** — a change in what the metric measures is part of the
  delta. Quote the footnote.
- **Do not argue motive from arithmetic.** The arithmetic establishes a gap; the gap does not establish
  intent. Concede facts to an insider immediately and hold the algebra, which is the part they cannot
  answer from memory. End on the ask, not on the thesis.

## Downstream: what a reserves squeeze actually does

A reserves shortfall does not arrive as a collapse; it arrives as a narrowing sanction window and a capex
mix that quietly stops funding the discretionary end.

- **Different decisions run on different clocks.** A finished reorganisation, a new org design or an
  operating-day date settles the *staffing* question and says nothing about the exploration budget —
  that line moves with the dividend and the capex cycle. Using the first to reassure about the second is
  the same error as using one ratio's basis to settle another ratio's value.
- **Separation packages are formula-priced** (a multiple of months per completed year, capped). A strong
  balance sheet does not enlarge the formula; it changes whether the door is open and how many slots
  exist. The time-critical thing is access, not quantum.
