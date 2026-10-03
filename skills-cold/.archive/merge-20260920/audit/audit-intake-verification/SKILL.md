---
name: audit-intake-verification
description: "Use when an external audit or review of your system arrives."
version: 1.0.0
owner: Hermes
risk_tier: T1
floor_scope: [F1, F2, F4, F6, F13]
triggers:
  - "external audit arrived"
  - "an AI reviewed my system"
  - "is this audit right"
  - "readiness verdict from another agent"
  - "gap analysis from an external model"
  - "gate table with Unknown rows"
  - "audit says my artifact is missing X"
  - "vet this review before we act"
  - "another agent audited my work"
tags: [audit, verification, external-review, epistemic, intake]
capability_tier: fed-long-context
ecology_state: WARM
---

# Audit Intake Verification

When an external party — another AI, a vendor, a consultant, a peer agent — delivers an audit,
review, gap analysis, or readiness verdict about YOUR system, the deliverable is **not** to act
on it. It is to establish whether the audit measured the thing it claims to have measured.

Audits fail in a specific, repeatable way: they describe an artifact that does not exist.
They measure a plan, a proposal, a sibling's half-finished draft, or a conversation about the
work — and write it up in the present tense as the work itself. Every finding then inherits the
phantom premise, and acting on it damages a system that was never broken in that way.

**Core invariant: present tense is a claim, not a status. Specificity is not evidence of
existence.** A document that says "the pipeline handles X" has told you nothing about whether a
pipeline exists — only that someone wrote the sentence.

## Procedure

### 1. Locate the artifact the audit claims to be about

Before reading a single finding, answer: **what is this audit describing, and does it exist?**

```bash
# Does the named artifact exist at the named path?
ls -la <path-the-audit-names>
# If the audit names a document, does it exist in more than one version?
find <root> -iname '*<artifact>*' -not -path '*/node_modules/*'
```

A directory of the expected name containing **zero files** is the signature of a planned-but-never-built
version. If the audit describes a v2 and v2 is empty, the audit is describing the intent.

### 2. Grep the artifact for the audit's OWN vocabulary

This is the highest-value check and it takes one command. Take every distinctive term the audit
attributes to the artifact — section names it says it reviewed, frameworks it says are cited,
labels it says are used — and count occurrences **in the artifact itself**.

```bash
for term in "<distinctive term 1>" "<distinctive term 2>" "<cited author>" "<named section>"; do
  printf '%-28s %s\n' "$term" "$(grep -ric "$term" <artifact-path>)"
done
```

Zero hits on terms the audit treats as load-bearing means the audit measured something other than
the artifact in front of you. Report that as the primary finding, before evaluating any individual
gate. Do not "fix" a vocabulary mismatch by adding the missing words to the artifact — that
retrofits the audit's fiction onto real work.

### 3. Check the audit's premises against the artifact's actual stance

The sharpest failure mode: **an audit recommends reversing a decision the artifact already made
correctly**, because the audit did not read the stance — it read the topic.

Look for prose in the artifact that explicitly withholds, qualifies, or bounds something the audit
then demands. When the artifact is *stricter* than the audit, the audit is not a gap analysis; it
is a regression proposal. Surface this explicitly and let the owner decide — it is often a policy
choice the auditor had no way to know was deliberate.

### 4. Check the audit's own arithmetic and self-consistency

Run the audit's declared rules against the audit's own values (the general rule: a spec that
declares invariants must satisfy them itself — see also the internal-self-contradiction check in
the deployment-audit literature).

- Do the stated subtotals sum to the stated total?
- Are the "N of M" counts computed from the table, or asserted alongside it?
- **Rows marked Unknown / TBD / unverified cannot be counted as failing.** A score that includes
  unmeasured rows is arithmetic over nothing. A table with several `Unknown` rows and a confident
  "7 of 10 open" verdict is not a measurement.
- Does the audit cite paths it never opened? Probe each cited path.

### 5. Classify every finding before acting

| Class | Treatment |
|---|---|
| **Testable** — names a path, endpoint, count, file, or behaviour | Probe it yourself. Own the verdict. |
| **Editorial** — structure, tone, ordering, naming preference | Advisory only. Owner's call. |
| **Phantom premise** — describes artifact content that does not exist | Discard the finding; report the premise error. |
| **Already satisfied** — the audit lists as missing something that exists | Discard; report with the probe that proves it. |
| **Regression proposal** — asks to undo a deliberate, documented decision | Escalate as a binary; never apply. |

### 6. Report a verdict; do not apply fixes

Deliver, in this order: what the audit is describing (and whether it exists) · vocabulary and
premise check with raw counts · the classification table · the genuine gaps that survive · anything
the audit got right that you had missed. Then stop. Acting on an unvetted audit converts the
auditor's error into your damage.

## Pitfalls

- **Do not rebut the audit point-by-point in the owner's presence.** A long refutation reads as
defensiveness and buries the one finding that matters. Lead with the premise check, then the
  short verdict table.
- **An audit can be right about the goal and wrong about the artifact.** These are separate
  verdicts. Issue both ("premise: phantom / direction: valid") rather than collapsing them — the
  same split as separating a verifier's factual error from its structural concern.
- **Absence is a claim too, and needs the same warrant as presence.** "The system lacks X" and
  "the system has X" require equal evidence. Search every plausible root before accepting either;
  a probe aimed at the wrong path produces a false negative that masquerades as verification.
- **Vocabulary in the audit's sources is not vocabulary in the artifact.** An audit's own reference
  list (frameworks, authors, standards) does not transfer to the artifact merely because the audit
  cites them. Grep before accepting.
- **"Unknown" rows are not soft failures.** They are unmeasured. Exclude them from every count and
  say so.
- **When the audit and the artifact's owner disagree, the owner's documented policy wins** unless
  the audit brings new evidence. Deliberate decisions look like gaps to a reader who cannot see the
  decision.

## Related

For verifying claims about your OWN deployment (counts, routes, build freshness, served-vs-built),
use the deployment-claim-verification family. This skill is for the inbound direction: an external
party's claims ABOUT your system, where the failure mode is a phantom premise rather than an
inflated number.
