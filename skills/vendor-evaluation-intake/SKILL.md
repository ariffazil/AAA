---
name: vendor-evaluation-intake
description: Use when an outside lab evaluates your own product.
version: 1.0.0
author: hermes
license: proprietary
tags: [audit, vendor, evaluation, receipt, legitimacy, reproduction]
floor_scope: [F2, F4, F9, F13]
autonomy_tier: T1
capability_tier: fed-reasoning-heavy
ecology_state: WARM
triggers:
  - "an outside lab evaluated my product"
  - "vendor sent a security or quality report"
  - "free evaluation of my repo arrived"
  - "external evaluator reviewed arifOS"
  - "agentic evals / pentest report"
  - "is this audit report right about my code"
  - "someone sent a PDF evaluation of my system"
  - "should I pay for a re-test"
metadata:
  hermes:
    related_skills: [audit-ops, online-vendor-legitimacy-check, external-artifact-verdict]
---

# Vendor evaluation intake — an outside lab reports on YOUR product

Canonical owner for the general "another party's report is a claim, not evidence" flow is
`audit-ops` (routes by shape: findings document, gate table, pasted AI review). **This skill is the
single slice that flow does not cover: the report is about the principal's own product, arrives
unsolicited, and has a price ladder behind it.** Apply audit-ops rules; add the two things specific
to this shape.

## The two verdicts, answered separately and never blended

1. **Are the findings true?** — reproduce each one on live code.
2. **Who is the sender, and what are they selling?** — corporate identity, published work, funnel.

A report can be technically correct and still be a sales asset. Say both out loud, in that order.

## Procedure

**1. Extract, and read the report's own limits before its findings.**

```bash
pdftotext -layout report.pdf out.txt
```

A report that names what it did NOT test is stronger evidence than one claiming full coverage.
Weight the self-disclosure, and repeat it back in the verdict.

**2. Pin the subject.**

```bash
git cat-file -t <sha>
git merge-base --is-ancestor <sha> HEAD && echo ANCESTOR
```

Then compare the LIVE copy to the source tree by hash, resolving the import path rather than trusting
a directory name:

```bash
/opt/<svc>/venv/bin/python -c "import pkg; print(pkg.__file__)"
md5sum <live>/runtime/x.py <src>/pkg/runtime/x.py
```

A deploy dir called `current` can hold symlinks or an editable install pointing back at the source
tree. Resolve the module path before saying "they tested the code that serves production".

**3. Reproduce each finding on live code with a synthetic, non-secret canary.** Never grade a finding
by reading source. Run the exact failing input, print the output; the number is the receipt.

**4. Grade production exposure separately from defect reality.** Grep for callers/importers:

```bash
grep -rn "from pkg.runtime.<module> import\|import <module>" --include=*.py . | grep -v build/
```

A confirmed bug in a module with zero production callers is a **component finding**, not a production
finding — say both halves: "the defect is real; the exposure is not." Defects reachable only from the
test suite are the least severe and the most likely to be printed as finding #1.

**5. Re-rank severity by your own probe.** The vendor ranked by what its sandbox could reach — no
database, no registry, no identity provider. You rank by production consequence. If the ordering
differs, lead with yours and say which severity you replaced.

**6. Verify the sender independently of the findings.**

- UK company → Companies House **by number**, not by name search:
  `https://find-and-update.company-information.service.gov.uk/company/<NUMBER>` and `/officers`.
  Read incorporation date, status, officer legal names, identity-verification flag.
- Any DOI → `curl -sIL https://doi.org/<doi>` must redirect to a live record; then read the
  Zenodo/Crossref metadata and confirm title, date and creator match the claim.
- Every claimed product or domain → an HTTP HEAD returning 200. A dead product page under a live brand
  is a real signal.
- **Separate the founder's résumé from the company's track record.** "Thirty years in controls" plus a
  company incorporated months ago = one experienced individual, new lab. Not fraud — but the org has
  no history, and the report's authority is the person, not the firm.

**7. Answer the commercial question last.** What a paid re-test buys is a named third party's signature
for a pilot, investor or enterprise review — not the fix. Re-testing a defect you can reproduce and
verify yourself within the week is money for a certificate you do not yet need. Say exactly that; do
not price-shop the ladder on the principal's behalf.

## Reproducing integrity findings in a receipt / ledger component

The shape is always one question: **does the verifier fail closed on malformed input?** Four cases,
read all four:

1. N valid records → expect pass.
2. N valid + a malformed tail line → if it still passes, the parser skipped before verifying.
3. A file containing ONLY malformed lines → `(True, "")` means "nothing parsed, nothing failed". Zero
   parsed records must never be reported as integrity.
4. Corrupt the LAST record in place vs a MIDDLE record → if the middle is caught (`chain_broken`) and
   the last still passes, the newest record silently disappears on damage.

"The chain verifies" is meaningless without the input population. Report which case failed.

**Fixture pitfall:** sign records with the **same secret** the store verifies with. Passing a secret to
the store while letting the receipt builder default to its own secret yields `signature_invalid at
index 0` on a perfectly good fixture — probe-author error, not a product defect. Confirm the clean
baseline returns `True` *before* appending any corruption, or every later case measures the fixture.

## Live kernel / MCP payload probe

When the finding is about a response envelope, POST with a stream-capable Accept header, then decode
the nested payload:

```bash
curl -s -X POST http://127.0.0.1:<port>/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"<tool>","arguments":{}}}'
```

`result.content[0].text` is a JSON **string** — parse twice. A refusal envelope can still carry success
prose elsewhere in the same object, so grade the whole envelope (`status`, `error_code`, `facts`,
`next_safe_action`, verdict fields), not the status field alone.

## PDF metadata — read it for what it can support

`pdfinfo` gives the creation stamp and producing engine. A PDF generated at delivery time by a headless
browser tells you the report was **assembled as a document for you** — not that the work was fabricated.
State the mechanism, never the accusation.

## Verdict shape to hand the principal

Per finding: **BETUL / SEPARUH / SALAH**, one line of the reproduced mechanism, and the production
exposure. Then what the report got honestly right about its own limits, then the sender's standing,
then one recommendation. No menu. Never relay the vendor's severity as your own.

## Pitfalls

- **Do not mirror the report's framing.** Its check names are its product vocabulary; the principal's
  question is "benda ni betul ke tak". Answer in that register.
- **Do not let a free report create a debt.** A warm reply draws a second free contribution. Keep the
  door open, decline the ladder politely, never imply an obligation to purchase.
- **A report listing your own known gaps is not thereby a surprise.** The new information is the
  reproducible receipt, not the fact of the gap — say which ones you already had on your list.
- **Never let the vendor's commit hash stand as your deployment claim.** "They tested commit X" and
  "commit X is what serves production" are two different sentences.
- **A follow-up after a warm human reply is a sales cadence step, not a new fact.** Read the thread
  before treating the latest message as news.
- **Do not run the whole audit in the reply.** Lead with the three findings reproduced, then the
  sender's standing, then one recommendation. The reproduction detail belongs in the work, not the
  message.
