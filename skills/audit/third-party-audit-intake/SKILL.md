---
name: third-party-audit-intake
description: "Use when an external AI audit or readiness report arrives."
version: 1.0.0
owner: Hermes
risk_tier: T1
floor_scope: [F1, F2, F4, F13]
triggers:
  - "external AI audit or review dropped in"
  - "readiness report says NOT READY"
  - "ChatGPT / Perplexity / Copilot review of my work"
  - "compliance or gate table with pass/fail rows"
  - "gap analysis from another model"
  - "someone says my artifact is not publishable"
tags: [audit, verification, external-review, governance, evidence]
---

# Third-Party Audit Intake

An external AI delivers a readiness report, compliance table, or gap analysis on work the user
owns. Posture: **ADVISORY, never authority.** Its value is in what it noticed. Its danger is in
what it assumed.

## Procedure

1. **Read once end to end without acting.** Sort every row into *testable* (state of a real
   system: a file, a route, a config value, a deployment, a published artifact) vs *editorial*
   (structure, tone, ordering, naming taste). Only the first category can be resolved by probing.

2. **Probe every testable row against live state before repeating it.** A row is a claim, not a
   finding, until you have looked. Curl the route, read the file, grep the artifact. Rows the
   audit labelled with a question mark were never tested by it either — they are hypotheses.

3. **Test every path, file and URL the audit cites.** Audits routinely demand links to routes that
   do not exist and quote files they never opened. `curl -so /dev/null -w '%{http_code}' -L` each
   one. An audit that did not check its own references has not checked much else.

4. **Recount its arithmetic from the rows it actually measured.** A verdict like "7 of 10 gates
   open" containing any Unknown row is a rhetorical device, not a measurement — Unknown means
   untested, which is not a tick in either direction. Recompute before you repeat any fraction or
   severity score. Do not carry a number you cannot rebuild.

5. **Before applying a prescription, grep the live artifact for an already-recorded decision on
   that exact point.** External reviewers cannot see what has already been decided, so they will
   propose reversing standing policy as if filling an empty gap — a licence term, an access
   posture, a naming convention, an architecture choice. Check the live source of truth first
   (`rsl.xml`, `robots.txt`, `llms.txt`, `canon/*.yaml`, the schema file, the config) and quote it.
   Silently importing such a prescription reverses the owner's own ruling on the machine's advice.

6. **Treat the rows it marked Unknown as the real findings.** It did not test them. Probe those
   first — that is where the actual defect is, and where its prescription is least trustworthy.

7. **Deliver a reality verdict, then stop.** Structured table: what is correct · what is partially
   correct · what is wrong. Then offer the fix in one line. Never apply a fix set wholesale, and
   never let the audit's severity score set your scope.

8. **Report in the audit's own words when stating what it claims.** Paraphrasing launders a wrong
   claim into a plausible one; a short verbatim quote lets the user see the error themselves.

## Pitfalls

- **Remedies are the least reliable section.** Findings are usually sound (the auditor looked at
  the artifact); remedies usually assume a greenfield that does not exist. Value the findings,
  discount the plan.
- **An audit prescribing a new file, page, route or schema has not checked whether one already
  covers it.** Grep for the existing surface before creating a parallel one; duplicate structures
  are the most expensive kind of accepted advice.
- **"Required" in an audit's table is the auditor's taste, not a standard.** Distinguish a
  genuinely broken thing from a thing the auditor would have built differently.
- **Never forward the audit's verdict to the user as fact.** It is a second opinion; the user
  decides. If the audit says HOLD and your own probes say the artifact is sound, say both.
- **A single audit is not a consensus.** Where two external reviewers agree, check whether they
  share a source or a model family before treating the agreement as independent evidence.
- **Watch for the audit flattering the work.** A report that opens with "the strongest piece in
  your corpus" and then lists gates is building permission for its own prescriptions. Praise is
  not evidence; test the gates.
