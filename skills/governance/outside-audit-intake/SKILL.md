---
name: outside-audit-intake
description: "Use when a stranger sends an unsolicited audit."
version: 1.0.0
category: governance
tags: [audit, vendor, provenance, discovery, verification, cold-outreach]
capability_tier: fed-long-context
ecology_state: WARM
---

# Outside Audit Intake

> A cold email that names real defects in your code is the highest-value free thing you will get,
> and the highest-risk thing you will receive. Both are true at once. Treat it as an audit of two
> objects: the finding, and the sender.

## Use when

- A stranger, lab, or "independent evaluator" emails findings about your product.
- A vendor offers a free audit, a pre-evaluation pack, or a security scan of your repo.
- Someone reports a bug in a system you own and asks for nothing in return.
- A directory, benchmark, or scoring site lists you, or claims to have evaluated you.

## Step 1 — Intake, and make the attachment safe first

Pull the message and its attachments, then inspect the file **before** you read it as content.

- Extract PDF text with `pymupdf` (`pymupdf.open`), not by fanning out a browser.
- Check the PDF is a document and not a delivery vehicle: `doc.embfile_count()` (embedded files),
  `doc.is_form_pdf`, and the catalog for `/JS` or `/Launch`, plus every `/URI` action.
- Read the PDF `metadata` — producer and creation timestamp answer two questions at once: was this
  machine-rendered, and how long before the send was it generated? A headless-Chrome producer string
  with a creation time minutes before arrival means the artefact is automated.
- Read the message auth headers before trusting the From line: `Authentication-Results` (dkim / spf /
  dmarc), `Return-Path`, and the first `Received` hop. `dmarc=pass` with a matching DKIM `d=` means
  the domain is genuinely theirs. It does not mean the claims are true.

**Never conclude "spoofed" or "phishing" from a mismatch you have not read the header for.** Free
mailbox providers legitimately relay on behalf of custom domains.

## Step 2 — Authorise the sender: registry before rhetoric

Before repeating a single thing the sender says about themselves, date the institution.
Full recipe with commands and the cross-registry table: `references/entity-provenance-and-discovery.md`.

Minimum set:

- **Corporate registry** — incorporation date, SIC, officers, any prior company (and any liquidation).
- **Domain WHOIS** — creation date, compared against incorporation.
- **Code-host org** — `created_at`, repo count, followers.
- **Publication registry** — first DOI/paper date and stated affiliation.

The load-bearing discipline: **claimed tenure is a claim, not a fact.** "Thirty years across financial
services, insurance and defence" with no talk, paper, registration or prior filing behind it is
`UNKNOWN`, never `FALSE` — and never enters a credibility score as though it were measured.

Two axes, judged separately: **the entity** by its registry record, **the finding** by reproduction.
A six-month-old company with an unverifiable CV can still hand you a correct bug. Do not let a weak
sender discredit a real finding, and do not let a real finding launder a weak sender.

## Step 3 — Reproduce before you believe

Every finding is a claim about your system. Open the source, find the component, and make it fail on
your own machine. An audit that arrives with **negative controls** (a valid case that must pass, a
wrong-key case that must fail) has already ruled out its own probe — weight it accordingly, and then
still reproduce it.

Where to reproduce: the **deployed** environment or a checkout with its real interpreter, never a
freshly installed copy of a different version. Pin the commit the sender named and confirm your HEAD
matches, or state the drift.

### Three defect archetypes worth naming

Most genuine findings on a governed system are one of these. The class dictates the repair.

**a. The tolerant reader feeds the strict checker.** An enumeration function skips rows it cannot
parse; a verification function walks the survivors and returns success. A truncated tail, a corrupt
middle, or a file of pure garbage verifies **clean**, and the damaged record reads as *never written*.
Reproduce by appending one unparseable line to a known-good store and by corrupting the newest
record — both must go red. Repair: verification parses its own input and reports the failure index;
the tolerant reader survives as a separate, explicitly named inspection API.

**b. Key-based redaction that recurses into one container type only.** A scrubber that walks mappings
but treats sequences as leaves passes `{"items": [{"api_key": ...}]}` through intact, and skips
value-scanning inside lists as well. A key-name policy is not a traversal policy. Verify end-to-end at
a sink, not only on the pure function — the pure function passing is what lets this survive review.

**c. One payload, two truths.** A response carries a refusal status *and* success prose ("session
bound", "proceed", `ok: true`). Machines read the prose, humans read the status; both are wrong.
Repair at the single place that decides the outcome — not by scrubbing strings after assembly — and
assert that text content and structured payload agree.

All three share a shape: **honest about what it did, silent about what it did not cover.** Write the
class into the fix, not just the line.

## Step 4 — Answer the discovery question without inventing the mechanism

You will want to know how they found you. You can measure your own surface; you cannot measure their
intent.

Measurable: exact-phrase fingerprint of a distinctive line from your repo description (if yours is the
only hit, that string is a live discovery key); unique cloners vs unique viewers over the code host's
traffic window; which paths are fetched (instruction files such as `CLAUDE.md` / `AGENTS.md` /
`SKILL.md` indicate agents, the overview page indicates humans); human referrers; the gap between your
last commit and their email.

> **Discoverability is provable. Discovery is not.** Without direct provenance — a crawler in your
> logs, a referrer on the landing request, or the sender saying so — the mechanism is `UNKNOWN`.

Naming a directory or an agent from a traffic pattern alone is a story, not a finding, and a reviewer
will pull it back. Say what the evidence supports: the artefact was machine-produced, the process is
disclosed as AI-assisted, the gap is consistent with monitoring. Stop there.

Same restraint on the epoch claim. A company incorporated days before its domain, shipping an
automated pipeline, is **agent-leveraged institutional formation** — one principal plus agent labour
producing something that functions like a firm. That is narrower and stronger than declaring a new
anthropology.

## Step 5 — Decide: fix, buy, or neither

The default is **fix it yourself**. A free audit is QA; paying for the same findings is buying back
your own homework.

- Small, reproducible, in your own code → fix, add the regression test that fails first, commit, and
  reply with the commit reference. That closes the loop and costs nothing.
- Findings about a service you did not test, or a boundary outside the stated scope → do not accept
  them as defects. Say what the audit explicitly did not test.
- Paid engagement → only when the scope requires something you genuinely cannot self-administer:
  independence, an accredited signature, or an adversarial run you cannot perform on yourself. Price
  it against the cost of the fix, not against the report's impressiveness.

When you decline, decline in one paragraph, name what was useful, and leave the door open. The
sender's labour deserves acknowledgement even when the invoice does not get paid.

## Pitfalls

- **Do not restate the sender's marketing as your finding.** "Independent" is their word. Your file
  says: registered entity, N months old, one officer, N repos, first paper dated <date>.
- **A claim of an independent audit is not an independent audit.** Check what was actually run before
  quoting a verdict. "Pre-evaluation pack" and "source review, no code execution" are self-described
  as weaker than an evaluation — believe the label.
- **Their own coverage claim may be inflated.** Directory and index sites overstate their corpus. If a
  page says "24K indexed" and the live scanner says "2,914 tools", both numbers go in the note, dated.
  Everything in this class of work is also being audited by the same instruments; nobody is exempt.
- **Do not pay for findings you can reproduce in an hour.** The value of an external evaluator is
  independence and a verifiable signature, not the discovery of a bug in your own repo.
- **Do not let scrutiny become paralysis.** A public surface is judged on *material claims* — numbers,
  status assertions, compliance statements — not on every sentence. Prose may say what it likes; a
  claim that can be falsified must carry its scope, timestamp, method and commit.
- **Check your own published state block against the live endpoint before anyone else does.** A
  generated "current state" header goes stale the moment the system moves, and it is the first thing
  a scanning agent quotes back at you. Timestamp it, print the full fraction rather than a score, and
  expire it.
- **Planning text or duplicated fragments in a delivered answer are output contamination.** If you
  see truncated clauses, doubled phrases or a stated plan inside someone else's analysis, treat it as
  a defect in the artefact — do not explain it away as depth, and do not build on the mangled part.

## See also

- `references/entity-provenance-and-discovery.md` — registry commands, cross-registry dating table,
  traffic-endpoint semantics, and the discoverability/discovery line in full.
- `claimed-defect-verification` — the inverse case: a probe reported a defect and you must prove the
  probe before believing it.
- `person-dossier-from-public-sources` — when the ask grows into a full profile of the sender.
