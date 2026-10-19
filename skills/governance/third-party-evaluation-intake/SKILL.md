---
name: third-party-evaluation-intake
description: "Use when an outside lab audits your own product."
version: 1.0.0
tags: [audit, vendor, evaluation, due-diligence, evidence, inbound]
---

# Third-Party Evaluation Intake

Someone outside your project has read your public code, run tests against it, and sent you a report.
It may be a gift, a sales funnel, a genuine audit, or all three at once.

This skill governs the intake. It is **not** `online-vendor-legitimacy-check` (which asks whether a
shop is a lawful seller) and not `apex-fact-check-pass` (which checks your own artifact before seal).
Here the question is: **is this evaluation evidence, and what should I do with it?**

Load when a stranger, lab, or firm sends findings about your repo, product, or system — especially
unsolicited, and especially when the findings are correct enough to sting.

---

## THE ONE RULE

> **The report is a claim until you reproduce it. Reproduce it first, then argue about it.**

Replication is usually the cheapest step in the whole exchange and it converts a sales document into
evidence. Do it before forming any opinion about the sender, because a correct finding from a
suspicious firm is still a correct finding.

---

## PROCEDURE

### 1. Verify the evaluator as an institution — but keep it in proportion

Cheap, independent records, in this order:

| Check | Where | What it tells you |
|---|---|---|
| Legal entity | Company registry of the claimed country | Whether the firm exists, when it was incorporated, whether accounts are filed |
| Director history | Registry officer list | Whether there is a track record behind the name |
| Domain age | WHOIS creation date | Whether the brand predates the pitch |
| Code/org age | GitHub org `created_at`, first repo push | Whether the engineering claim has a paper trail |
| Publications | Zenodo / DOI / conference listings | Whether the "research lab" has research |
| Professional claim | LinkedIn, ORCID, filings | Whether "30 years in the field" is checkable anywhere but their own site |

**A young institution is not a fraudulent one, and a missing credential is not a lie.** Report the
shape: "company registered this year, domain two days later, organisation three days after that, one
prior company in liquidation, and the decades-of-experience claim is not independently checkable."
That is a fact pattern a reader can weigh. Do not upgrade it to fraud — you have not shown fraud.

Equally: **do not dismiss findings because the sender is new.** The findings stand or fall on
replication, not on the sender's pedigree.

### 2. Establish the boundary of what was actually tested

Answer these before reading a single finding:

- **Which commit?** Is it pinned and identical to yours? A report on an old commit is a report about
a different product.
- **Local copy or deployed system?** A local clone with dependencies installed tests the code, not
the service, the configuration, the credentials, or the deployment.
- **What was NOT tested?** Good evaluations state this themselves. If the report has no such section,
that absence is the single most important thing in it.
- **Who selected the tests?** Independently chosen checks are worth more than the author's own test
suite re-run.

### 3. Reproduce every finding, in order of severity

Run the smallest possible probe for each. Record pass/fail against the *claim*, not against your
feelings about the claim.

Reproduction turns three things into one:

- a real defect → fix it, and say thank you
- a misreading of your design → a documentation bug you now know about
- a false positive → you have the counter-evidence and can say so once, calmly

**A correct finding arrives with no obligation attached.** The obligation comes from the defect
existing, not from who found it.

### 4. Check the evaluator's own claims at the same standard

The most useful move available in this class, and almost nobody does it: hold the auditor to the
standard they applied to you.

- Their public metrics: does the headline number match their own live surface?
- Their coverage claim: does the directory/index they cite actually contain you?
- Their methodology: does the sample size support the generalisation?

This is not point-scoring. It tells you how much weight to put on the parts of the report you could
not independently check. A lab whose own numbers do not reconcile is a lab whose untested assertions
should carry a discount — and you should say so at the same time as you thank them for the parts
that were right.

### 5. Read the commercial structure

| Signal | What it means |
|---|---|
| Free, unsolicited, with real findings and a stated boundary | Either genuine goodwill or the best possible lead generation. Treat as evidence; ignore the intent. |
| Fee fixed, agreed before work, paid up front, result-independent | The normal shape of an honest paid evaluation |
| Paid by the party being evaluated | Structural conflict — but disclosure plus a fixed fee plus no endorsement is a workable mitigation |
| "Pass certificate" or badge as the product | You are buying a credential, not an audit. Price it as marketing. |
| No stated limits on what was tested | The report's confidence exceeds its evidence |

Ask one question and answer it in writing: **what does this evaluator gain if the result is clean, and
what do they gain if it is dirty?** Fee-only work is neutral. Lead-generation work is not hostile —
it is just not neutral, and you should price it that way.

### 6. Decide, and reply once

Three outcomes, and they are not interchangeable:

| Outcome | Condition | Action |
|---|---|---|
| **Fix and thank** | Findings reproduce | Fix, add regression tests, reply with the commit. No purchase. |
| **Fix partly, correct partly** | Some reproduce, some are misreadings | Fix the real ones, correct the others with evidence, once. |
| **Decline** | Findings do not reproduce | Say so with the counter-probe, once. Do not argue twice. |

Then stop. One reply. The correspondence is not the deliverable; the fix is.

---

## PITFALLS

- **Treating a free audit as free.** It is free of charge, not free of framing. The findings are real;
the omission is that nobody audited the auditor. Both facts belong in the same sentence.
- **Dismissing a finding because you dislike the sender.** Pedigree is not evidence in either
direction. Reproduce first; then judge.
- **Accepting a finding because it is well formatted.** A beautifully typeset PDF with a methodology
section and a named reviewer can still be wrong. Replication is the only vote that counts.
- **Skipping the "what was not tested" section.** That section is where the honest limits live, and
its absence is a finding about the report's confidence, not about your product.
- **Letting the intake become a relationship.** A free pack followed by a pre-eval pack followed by a
  proposal is a sales sequence executed with competence. You can be grateful and still decline. The
  correct close is: fix what is real, one reply, no dependency.
- **Replying before reproducing.** Once you have written "that is not a bug", you own that position.
  Two minutes of probing before hitting send prevents a paragraph of retreat.
- **Fixing only the ones they found.** Their three findings are a sample, not a census. Treat a
true finding as a class and sweep for its siblings before you call the fix done.

---

## OUTPUT SHAPE

```
## <sender> — Evaluation Intake

**Entity:** <name, registry number, incorporated date> | **Domain:** <created> | **Org:** <created>
**Credential claim:** <what they assert> — <independently checkable / not checkable>
**Tested:** commit <sha> | local/deployed | <what was explicitly out of scope>

| # | Finding | Reproduced? | Evidence | Action |
|---|---|---|---|---|

**Their own claims:** <headline vs live surface, if checkable>
**Commercial structure:** <who pays, what is sold, neutrality assessment>
**Verdict:** findings valid / partly valid / not reproduced
**Next action:** <fix list + commit> · reply once · no purchase
```
