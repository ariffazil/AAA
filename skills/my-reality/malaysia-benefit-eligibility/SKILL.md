---
name: malaysia-benefit-eligibility
description: "Use when claiming who qualifies for Malaysian aid."
version: 1.0.0
author: Hermes Agent
license: arifOS
tags: [malaysia, budget, str, sara, eligibility]
triggers:
  - does my household qualify for STR or SARA
  - what does Budget 2027 give B40 / M40 / singles
  - claiming a person gets nothing from the budget
---

# Malaysia Benefit Eligibility

## When to use

Any time a Malaysian budget measure, cash aid or tax relief is mapped onto a specific person or household — including the negative claim "hang tak dapat apa". Load before answering.

## The rule

**Resolve the person's category first, then speak.** "Gets nothing" is a claim about a category you have not read. Getting this wrong is not a numbers error; it is telling a human their government gave them nothing when it gave them RM600.

Categories are person-level (age, marital status, income), not vibes. Ask only if the value is genuinely unknown; otherwise infer from what the lane already holds and state the assumption.

## Budget 2027 working figures (tabled 9 Oct 2026 · RM459.8b · STR+SARA RM16b)

Re-verify each cycle at `mof.gov.my` (Fiscal Outlook + speech) and `bantuantunai.hasil.gov.my` (STR/SARA). Figures below are 2027; thresholds shift yearly.

| Category | Income test | Entitlement |
|---|---|---|
| Household — 0 to 5+ children | ≤ RM5,000/month | STR RM200–1,600 + SARA RM1,200–1,800 → RM1,400–3,400/yr |
| Single (bujang 21–59, not full-time student) | ≤ RM2,500/month | SARA RM600/yr, no STR cash |
| Elderly without spouse (60+) | ≤ RM5,000/month | STR RM600 + SARA RM600 = RM1,200/yr |
| Anyone 18+, not an STR recipient | — | SARA MADANI RM100 × 2/yr (pre-Aidilfitri, Merdeka), ~13m people including M40 |

Common rejection reasons (LHDN): income over the limit · property transaction ≥ RM300k · more than five cars, or a car over 2,000cc under 10 years old · three or more homes on electricity records · eight-plus entries/exits in a month (living or working abroad).

Other 2027 measures a headline-deficit story misses:

- Minimum wage RM1,700 → RM2,000 from June 2027, 4m+ workers — **MSMEs under RM50m annual sales exempt**, which is most employers of the people this is meant to help.
- Personal income tax relief RM9,000 → RM12,000 (first revision since 2010); rates 70–100k → 18%, 100–150k → 24%; up to RM1,600/yr to ~5m taxpayers.
- Electricity bill exemption 600 → 800 kWh/month (8m households) — reaches M40 with no claim form.
- BUDI95 300 L/month; MoF says under 1% of users reach the cap, so it rations nothing and the RM40b bill stands.
- Foreign-worker tightening: non-MSME employers can only deduct wage expenses if wages are paid through a bank account under the Employment Act 1955 — relevant to maid and gig agencies.

## Answer discipline

1. Name the category you used, and the assumption behind it.
2. Separate the three goods: cash in hand (STR/SARA), tax relief (delayed, needs income), and cost that did not rise (exemption, subsidy, wage-floor exemption). They are not interchangeable, and calling all three "goodies" flatters the budget.
3. A budget is a claim about the future until parliament passes it and disbursement rules are published — say so once, then answer.
4. When corrected, retract in one line and state what changes. Do not re-argue with the person who has the fact.

## Pitfall (proven 2026-10-19)

Answering "tak ada satu pun untuk hang berdua" from a national aggregates read (RM459.8b, deficit, dividends) — before checking that a single adult under RM2,500 gets RM600/yr and an M40 taxpayer keeps more via relief plus SARA MADANI. The aggregates were right; the eligibility claim was invented. Aggregates never license a per-person verdict.
