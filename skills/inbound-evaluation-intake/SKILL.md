---
name: inbound-evaluation-intake
description: "Use when an outside party emails a report on your system."
version: 1.0.0
owner: HERMES (forged)
risk_tier: T1
floor_scope: [F1, F2, F4, F7, F11, F13]
triggers:
  - "someone emailed an evaluation of my product"
  - "vendor sent an audit report PDF"
  - "unsolicited security review arrived"
  - "paid evaluation offer with free findings"
  - "another company audited my code"
  - "ingest this email and tell me the reality"
  - "is this report about my system real"
  - "free audit from an external firm"
capability_tier: fed-long-context
ecology_state: WARM
---

# Inbound Evaluation Intake — an outside party reports on your own product

Use when an email arrives carrying findings about a system YOU own: a vendor offering paid
evaluation, a security researcher, a benchmark lab, a partner's due-diligence note. The report may
be attached as a PDF; it may name a commit; it may be entirely right.

**Governing posture:** a sales pitch can carry a valid defect report. Produce three separate
verdicts — *findings* graded by reproduction, *remedies* graded by your own architecture, *offer*
graded on its own merits. Commercial motive is not evidence against a finding, and a real company is
not a validation of one.

Related: `audit-ops` covers pasted text reviews. This skill covers the email+attachment path, where
the reviewer claims to have RUN your code and may therefore be checked against it.

## Procedure

### 1. Ingest and locate the thread

Search the mailbox by sender first (`from:<name>`, then a surname-only query — the display name and
the address rarely match). Pull `format=metadata` for the thread index (date, from, subject), then
`format=full` for bodies. Walk `payload.parts` recursively; `text/plain` first, `text/html` only as
fallback. Download attachments by `attachmentId` before reading anything.

### 2. Authenticate the sender before trusting the content

Read `Authentication-Results` (dkim / spf / dmarc), `Return-Path`, `Received-SPF`, `X-Mailer` from the
headers. Then check the company itself: registration number, registered address, whether the
benchmark or leaderboard it cites actually publishes results or is still "in verification". These are
two different questions — passing one says nothing about the other.

### 3. Triage the attachment before trusting it

With `pymupdf`: page count, `doc.metadata` (producer/creator reveals the generation tool),
`doc.embfile_count()` (expect 0), `doc.is_form_pdf` (expect False), every `pg.get_links()` URI, and
absence of a `JS` key in the catalog. Embedded files, form actions or JavaScript ⇒ hostile input, do
not open in a viewer. Then extract text per page and keep the page markers for citation.

### 4. Pin the claim to a version — their commit against your HEAD

`git cat-file -t <sha>` then `git rev-list --count <sha>..HEAD`. Zero means they tested the tree you
are standing on: take the findings seriously. Non-zero means part of the report describes code that
no longer exists — re-check each finding at HEAD before grading it in either direction. Confirm the
working tree is clean first; uncommitted edits make every probe ambiguous.

### 5. Reproduce every finding — do not grade by reading their description

Write a throwaway probe that imports the REAL modules and exercises the named boundary. See
`references/reproduction-probes.md` for the defect classes with the highest hit rate in
verification, redaction and response-assembly code, plus the probe shape for each.

Run probes with the project venv (`./.venv/bin/python`), never the system interpreter — a missing
dependency otherwise reads as a product defect.

Exactly three verdicts per finding: `CONFIRMED` (reproduced, quote what the probe printed) ·
`SCOPE-LIMITED` (real, but only inside the isolated component they tested — say what the deployed
path actually uses) · `REFUTED` (their probe was wrong, show the corrected run).

### 6. Read their scope-limits section before their findings

The "what we did not test" page is the most useful part: it names where your own unknown-unknowns
still live. A caveat like "not reached in the deployed service" is usually honest and does not shrink
the finding — it defines the blast radius.

### 7. Commercial posture — fix first, then reply with the commit

One short paragraph: fixed at `<sha>`, thanks, no purchase needed. That converts a lead-generation
email into free QA without creating an obligation. Do not buy before the free findings are
reproduced; do not ignore the report because it is an advertisement. Never send the reply without
the fix landed — a thank-you note for a defect you have not closed is a receipt of your own exposure.

## Pitfalls

- **Discount the plan, not the finding.** Remedies assume a greenfield; findings assume only that they
  opened the file.
- **Vendors inflate their pedigree** — a leaderboard still "in verification", unbounded years of
  experience, a free tier that is really a funnel. Verify the claim, ignore the tone.
- **Generalize their fix prompt, do not apply it verbatim.** "Make the walker traverse list elements"
  generalizes; "patch line 434" does not. Then grep for sibling call sites — the same boundary is
  usually guarded in more than one place.
- **A finding you can reproduce is a free QA receipt, not an embarrassment.** Say CONFIRMED plainly and
  move to the fix; hedging on a reproduced defect costs more credibility than the defect itself.
- **The reviewer's negative controls tell you how much to trust the positive ones.** A report that
  shows paired controls (absent/supplied, valid/altered, dict/list) has been built by someone who
  suspects their own probe. One that shows only passing checks has not.
- **Do not forward the report's verdict to F13 as fact.** Report what YOUR probe returned; the vendor's
  sentence is a claim about their run, not a state of your system.

## Deliverable shape for F13

Plain BM sentences with short bold labels: who they actually are (one verified line) · what they found,
per finding — confirmed or not, and what the probe printed · what they did not test · one
recommendation · then a decision request.

No markdown tables, no severity scores, no JSON, no restating the PDF's own prose. F13 reads for
"is this real and what do I do", not for a summary of a document he already received.

## Files

- `references/reproduction-probes.md` — high-yield verification-boundary defects and the exact probe
  shape for each (tolerant verifier, non-recursive redaction, refusal carrying success narrative).
