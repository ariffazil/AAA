---
name: corporate-language-audit
description: "Use when auditing corporate language for what it avoids."
version: 1.0.0
owner: Hermes
risk_tier: low
tags: [language, audit, corporate, pr, governance, measurement]
---

# Corporate Language Audit

Use when the user asks why an institution's public statements feel evasive, or wants a
critique of a press release / results statement / CEO letter that lands on evidence rather
than grievance. Also use to review our own outward-facing language by the same instrument.

## Why measure instead of argue

Saying "this language is spin" invites the reply "that is your feeling." Counting does not.
A finding of the form *86% of sentences name no actor · 257 praise-words · zero words for
the people affected* is not an opinion and cannot be dismissed as one. Convert the
complaint into an arithmetic the reader can re-run.

## The three tests

Run all three. Each catches something the others miss.

**1. Actor test.** Split into sentences over ~45 characters. Count how many contain a
first-person actor (`I/we/my/our`) and how many carry a passive or agentless verb
(`was delivered`, `is driven by`, `underpins`, `was due to`). A high no-actor share means
the text assigns credit without an owner and difficulty without a cause.

> "PETRONAS' resilient performance for 2025 was *delivered* against a backdrop of
> prolonged volatility." Who delivered it? Nobody. What made it hard? Weather.
> Weather cannot be blamed, and a passive verb cannot be cross-examined.

**2. Ratio test.** Count praise-words (deliver, sustainable, value, portfolio, growth,
committed, strategic, resilient, challenging, volatility, headwinds, disciplined) against
human-impact words (employee, staff, worker, colleague, retrench, layoff, redundancy,
injury, accident, fatality, safety incident). Report the ratio. 15:1 is a finding.

**3. Absence test — the strongest one.** Count the words that appear **zero** times. What
a document never says is a choice, not an oversight. When a results release reports a
safety metric worsening 50% and contains the word `accident` zero times in 47,000
characters, that gap *is* the story.

## Procedure

1. **Collect primary documents only** — the institution's own releases, not reporting about
them. Verify each URL returns HTTP 200 before citing it; write the status codes to a
receipt file on disk. A citation-shaped string that does not resolve is not a source.
2. **Read from disk, not from the payload.** Cache the pages first, then have the counting
script open the cached files. Two practical reasons: the run is reproducible later, and
trigger-word gates on financial or legal vocabulary will block a script whose *body*
contains those words even when it only counts them.
3. **Count, then read the outliers.** The numbers locate the passages worth quoting; they
do not replace reading them.
4. **Quote verbatim and in order.** For an apology or a denial, the *sequence* of clauses
is the finding — self-defence placed before the apology reaches readers who stop early,
while the apology reaches those who finish.
5. **Ship the script path with the deliverable** so anyone can re-run the count and disagree
with it.

## Rules of fairness (non-negotiable)

- **Do not assert intent.** Report the gap between language and behaviour. The finding is
  "this word never appears," not "they are lying."
- **Check the numbers are true.** In the case this skill was built from, every figure in the
  statements was accurate. The finding was selection and framing, not falsehood. Say that
  plainly — an audit that overclaims collapses on first contact.
- **Explain the structural pressure.** An institution that must be both a business and a
  revenue source for its owner cannot openly admit the two conflict. Naming that constraint
  makes the analysis credible and keeps it from reading as a personal attack.
- **Distinguish a job description from a person.** Corporate register is the register of the
  seat, not evidence about the character of whoever occupies it.
- **Apply the instrument inward.** The same tests run against our own outward language.
  A rule that only points outward is rhetoric.

## Reading the output

- Passive voice is not politeness. It is a sentence that cannot be asked a follow-up question.
- Abstract nouns hide the transaction: "solutions" hides what is sold; "stakeholders" merges
everyone into a group with no particular claim; "just transition" defers the justice and keeps
the extraction.
- Euphemism reassigns blame, not just tone. "Rightsizing" implies the previous size was wrong —
so the people cut were surplus all along.
- Watch for two audiences inside one paragraph. Shareholders, the public and "those we serve"
can each get a sentence while the people doing the work get none.

## When the user is an insider

If the reader works inside the institution being audited, they already know the substance.
Do not explain their own company to them. Do not add protective framing meant for outsiders —
check first whether they want it. Lead with the measured finding, treat them as a competent
colleague, and separate the institutional critique from the individual so their employment is
never the subject.

## Pitfalls

- Asserting motive instead of measuring the text. Motive is unfalsifiable and forfeits the argument.
- Counting honour-words only and reporting a big number without the absence test beside it.
- Forcing a page break before every section — it produces half-empty pages. Let prose flow and
  keep only the cover break.
- Letting a table's rows fail to sum to its stated total. Recompute every total before shipping.
- Citing a URL that was never fetched, or a body that was never read.
