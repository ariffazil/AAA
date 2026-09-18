---
name: security-disclosure-handling
description: Use when a vulnerability report arrives from outside.
version: 1.0.0
tags: [security, disclosure, cve, correspondence, vendor-acknowledgment]
---

# Inbound Security Disclosure — Handling

Class-level. Trigger: an external researcher reports a vulnerability (email, GitHub, advisory), the project has to respond, or the principal forwards a researcher's letter and asks what to do with it.

This is a recurring class, not a one-off: arifOS is indexed in MCP registries and scanners find it automatically. Expect more reports.

## Procedure

### 1. Reconstruct the whole thread before drafting anything

A researcher who escalates publicly has usually already tried the private lane and got silence. Before replying, recover the chain: when the report arrived, what was said, what was fixed, what was promised.

- Load `agent-session-forensics` § "Episode reconstruction".
- **Look for the unsent draft.** A reply drafted earlier and never sent is the artefact that explains the public escalation. Check the quarantine tree and the outbound cache.
- Re-probe every claim the earlier session made (`git log -1 <sha>`, `md5sum` source vs deployed) — an old "fixed and sent" carried forward into a new reply is how a vendor ends up contradicting itself in a CVE record.

### 2. Reproduce before acknowledging

A vendor acknowledgment becomes a permanent public record: the reporter quotes it in the CVE filing and in any write-up. Never write "confirmed" from the strength of someone's code reading, including a correct one.

- Stand the substrate up and fire the actual payload (see `deployment-claim-verification` #22 for the live-test discipline).
- Report the finding as valid AND say which path you reproduced it on versus which paths you did not test.
- A report can describe code that has already been fixed. Check the current tree before accepting or rejecting it.

### 3. Fix, then credit in the artefact — not just the email

- Land the fix as small, named commits (one concern per commit), conventional-commit style.
- Put the reporter's name in the module docstring and the commit trail. Credit that exists only in an email is credit the researcher cannot point at.
- **Verify the name is in the shipped build**, not only in the working tree — download the published artefact and inspect it, because "fixed on main" and "fixed in the build people install" are different facts.

#### Prove the fix COVERS every path — by set difference, not by reading

A multi-finding report is usually fixed *partially*: the guard lands on the paths the first
reading named, and a sibling call site with the same defect keeps its unguarded egress. "The
guard exists" in one module is not "every path is guarded".

Never accept the guard module's own docstring as the coverage claim. A header reading
"SINGLE source of truth. Every address the resolver would hand to the socket is checked" is a
statement of intent, and it is falsified by the difference of two greps:

```bash
grep -rn '<egress-sink>(' --include=*.py <pkg> | grep -v test    # every call site
grep -rln '<guard_module>' --include=*.py <pkg>                  # every guarded site
# the difference is the unguarded set — fix it or classify it explicitly, one by one
```

Run that per finding in the report and keep the count: "closed on 3 of 4 paths; the fourth is
open" is a residual you can state in the acknowledgment. Then re-run the guard behaviourally
against the vector table — local, link-local, `file://`, IPv6, and the non-dotted notations of
the same address — because a guard that resolves-then-verifies should block every one, and a
block is only a block if the call returns HOLD instead of fetching.

Finally, name the tree you verified. A guard landed in the development checkout is not a guard
in the running service; the fix reaches runtime through push → deploy → restart, and when that
deploy touches a kernel or a live service it is the principal's decision, not the agent's.

#### Reproduction patterns worth trying first

The three defect shapes that recur in agent-written Python, with the one probe that
settles each:

- **Escape the value, forget the key.** A query builder may escape literals correctly and
  still interpolate property *keys* unquoted (`e.{key} = '...'`), where quote-escaping does
  nothing. Keys usually arrive from an LLM's JSON extraction, so prompt injection reaches
  the datastore. Probe: build the statement with a key like `x MATCH (n) DETACH DELETE n //`
  and print it — if the payload appears unquoted, it is live. Fix by validating the key
  against `^[A-Za-z_][A-Za-z0-9_]*$` and **rejecting** (never silently mangling, which
  turns an attack into a silent data mutation).
- **Route parameter used as a filename.** Resolve the path and test containment against the
  **resolved root** (`root in p.parents`), not a character blocklist — blocklists miss
  encodings and symlinks. Probe with `../../../../root/.secrets` before and after; report
  the resolved path you got, not an inference that it "would" traverse.
- **Guessable secret fallback.** `os.getenv("X", "default_secret")` is a bomb even when the
  function is dead code. Confirm deadness by grepping call sites, then make it fail closed.
  "Nothing calls it yet" is not a control — it is a schedule.

When the root cause turns out to be the *framework* (a router matching a path template
before decoding it), fix your usage **and** report upstream; the reporter will tell you if
they traced it there, and confirming that split is part of the acknowledgment.

#### Verify the guard without exercising the danger

Proving an egress guard actually blocks has two traps, and both produce a green result that
means nothing.

- **An outer layer's refusal is not the guard's verdict.** Exec-approval harnesses, sandbox
  policy, and host firewalls deny the same call. If the DENY came from a layer wrapping the
  tool, it says nothing about the guard under test — the test reads as passing while the guard
  may be absent entirely. Name which layer refused, or drop to the guard itself.
- **Never aim the test at the real sensitive endpoint.** A cloud metadata address is the
  obvious vector and the worst choice: if the guard fails, the credentials it returns are
  captured by every layer that records tool calls — receipts, vault entries, gateway logs —
  not just the few characters you printed. Safe substitutes, best first:
  1. **Call the guard function directly.** A resolve-then-verify guard returns its verdict
     before any socket opens, so invoking it with each blocked URL exercises the real
     predicate with zero egress. This *is* the proof; the tool-level call only wraps it.
     Assert the verdict per vector (local, link-local, `file://`, IPv6, non-dotted notations)
     and assert that legitimate public URLs still return clean — a guard that blocks
     everything passes the first half and breaks the service.
  2. If end-to-end coverage is genuinely required, serve the path from a dummy listener on
     localhost with inert content, so a guard failure leaks nothing.

Harness note: import only the leaf module holding the predicate. Reaching one function by
importing the whole tool package pulls in the runtime's heavy initialisation and can hang the
session outright; put a hard `timeout` on the command so a hang costs one probe instead of the
kernel.

### 4. Verify the reporter's email address — BEFORE drafting

The acknowledgment is useless if it reaches a placeholder. When Gmail read is down or the thread origin is ambiguous, do not guess — discover.

Discovery ladder (check in order):
1. **Thread headers** — extract From address from the original email (via email client, Brevo inbox query, or session transcript).
2. **Git commit trail** — `git log --all --grep="<reporter name>"` may surface a co-authored commit or external-report reference with the address.
3. **Vendor acknowledgment file** — if one was already generated (e.g. `forge_work/<date>-<finding>/vendor-acknowledgment.html`), the reporter's full name is in it; cross-reference with the source channel.
4. **GitHub profile** — if the report came through a GitHub issue/PR/security advisory, the reporter's profile may list a public email.
5. **Web search** — full name plus professional context.
6. **Ask the principal** — last resort, and only once you have the full name and channel to offer.

**Block:** Do not proceed to step 5 (sending) with a placeholder or unverified address. A sent-to-nowhere acknowledgment is worse than silence — the researcher sees nothing, the vendor believes it was sent, and the thread dies.

### 5. The vendor acknowledgment email

Reply **on the existing thread** so the researcher's client threads it. Six things, no more:

1. Report date and the channel it arrived on.
2. Validity — and the reproduction evidence.
3. The fix: commit hashes, and what each one closes.
4. **The residual that is NOT fixed**, named explicitly, with a "do not treat the fix as complete" line. This is the single most important paragraph: it is honest, and it is what stops the eventual public write-up from contradicting the vendor record.
5. Credit — the exact name the researcher wants used.
6. Vendor contact for the CVE filing: full legal name and address.

Then the parts that are not formal: what the report made the vendor see, and the honest expectation for what comes next (e.g. "I cannot personally defend every line you will find"). See § Register below, and `references/outbound-send-lane.md` for the send lane, its response contract, and the receipt fields to record.

### 5. CVE path when the project has no CNA

The reporter files through MITRE directly and uses the vendor acknowledgment as the vendor-acknowledgment evidence. Deliver exactly what the filing needs and nothing speculative: dates, channel, validity, commit hashes, residual, credit, contact.

- Do not promise a CVE ID, a CVSS score, or a publication window — none of those are the vendor's to grant.
- The repo's own security-advisory surface must be **enabled** for the advisory-mediated path to exist at all; an advisory-mediated CVE cannot be opened on a repo where advisories are off.

### 6. Publication terms — set these explicitly, in writing

Three conditions, and they are not negotiable downward however impeccable the reporter has been:

1. **After the fix is in a RELEASED artefact**, not merely on `main`. Confirm it (see step 3).
2. **Reporter credited** as reporter, with the name already in the code.
3. **The vendor reads it before it goes up.**

Plus a scope limit: the write-up covers the **vulnerability class and the code paths only**. Hostnames, ports, service layout, and internal wiring stay out — those are the parts that turn a disclosure into reconnaissance for the next reader.

### 7. Estate upkeep after a disclosure

- `SECURITY.md`'s disclosure-history line goes stale the moment a CVE is filed; update `Known Gaps` too.
- Confirm the fixed build is the one people actually install — if the published artefact is older than the fix, say so in the reply rather than letting the researcher find out by installing it.
- If a release-pipeline block is what stands between the fix and the public build, state that as a named blocker in the email, not as a vague promise of a date.
- **Instrument the promise itself.** Writing "acknowledged within Nh" into `SECURITY.md` creates a
  measurement obligation, and until it is measured the policy is worse than absent: it advertises a
  channel and then silently does not answer. Build the watch, and make it check the two things that
  actually failed:
  - **That the lane can still read.** Probe the function, not the health endpoint — an
    authenticated read of the inbox surface itself, reporting `CANNOT_WITNESS` rather than `OK`
    when it cannot tell. A silently expired credential is the mechanism behind most escalated
    disclosures, and a green unit status will not reveal it.
  - **That a reply actually left.** This cannot be answered from a `sent` flag or an outbox
    record. Ask the thread: does a message *from us* exist in it? The characteristic failure is a
    reply that was seen, understood, drafted, and never sent — every local step green, the human
    still unanswered. Age the clock from the sender's `Date` header, so the researcher's window
    starts when they hit send rather than when you noticed.
  Keep the design small and use the channel the rest of the estate already routes to. Classify
  inbound mail with the provider's own category labels rather than a hand-maintained sender list —
  a vendor-maintained regex is one more thing that drifts. See `event-driven-alerting` for the
  lane-probe pattern and the threshold-equals-published-number rule; the threshold is a copy of
  `SECURITY.md`, so read it from that file and never from a summary of it.
- **Do not upgrade the audit row on the strength of one finding.** A report is evidence about one
  path; an audit is a systematic review. A `Known Gaps` row reading "no independent security
  review" stays open until an independently *produced* report exists — not when a reviewer starts,
  and not when one bug is fixed. The tempting edit is to `In progress`, which is defensible only if
  it names the scope actually under review ("reviewing the fetch surface"), never the whole system.
  Filing a CVE is a record that the project had a bug someone else found: it belongs in disclosure
  history, a different row, and it is not a credential to display.

### 8. After the acknowledgment — the scan, and the correction

The acknowledgment buys a follow-up stage. Two things happen there that decide whether the credibility holds.

**Pre-empt the false-positive class before their scan lands.** A scanner flags *shape*; a human supplies *reachability*. Sweep your own tree for the pattern you just fixed, then classify every surviving hit and send the table — `file:line — who supplies the target — why it is not the same class`. An internal health probe against a fixed localhost port, or a vendor API client with a hardcoded host, is not the same class as a caller-supplied URL. Strip comments before counting: a sweep for the pattern you just fixed will match the comment explaining why the guard exists, and a hit in a comment is not an open hole.

Add an explicit invitation to falsify the reasoning: *"test this rather than inherit it from me."* Two reasons this is not optional — their scan will hit those lines regardless, and borrowed confidence is the one thing a reviewer cannot verify. If they find the instances first, your summary of your own fix becomes their counter-evidence.

**Correct yourself the moment a fact changes.** Facts asserted in the acknowledgment go stale fast: a release lands, a pipeline recovers, a blocker clears. Send the short correction yourself, the same day — do not let the researcher discover the contradiction. A same-hour correction is a credibility asset, not a cost; it demonstrates the one property they are actually testing, which is whether your statements track reality.

Practical consequence for phrasing: **promises take the shape of messages, not dates.** "I will write to you when a release actually lands" survives a blocked pipeline; "it ships on Tuesday" does not.

**Do not ship under an active review without saying so.** A release during their review changes the artefact they are about to scan, and a service restart invalidates an observation they are halfway through. Check for concurrent sessions mutating the same tree first (`ps`, session store); if a release is ready, either hold it or tell them it is coming. Shipping is not the neutral option here.

## Register — the sentence that costs the sender something

Smooth institutional phrasing ("we take this seriously", "thank you for bringing this to our attention") reads to a working researcher as a legal template, and it is the register that gets a vendor filed under "responds, but says nothing."

Three things convert the letter from template into person:

1. **A specific fact the counterparty can check** — dates, commit hashes, artefact versions, the exact code path. Specificity is what reads as sincerity.
2. **One unflattering admission, stated plainly and briefly** — what the sender does not do, what is not verified, what is not fixed. The stated limit is what implies a human rather than a department.
3. **No inflation.** Every capability claim in external correspondence is a claim the counterparty may later test in public. Understate, then deliver.

**Rule:** the sentence that costs the sender something is the one that makes the letter credible. Include it deliberately — never write a courtesy formula where a fact belongs.

## Conduct boundaries

- **Resolve the correspondent by address, never by first name.** A researcher signs with a first
  name that may already be loaded in the agent's memory attached to a completely different person
  (a friend, a client, a group member). The collision is silent and corrupts both directions: a
  stranger's report gets filed against a personal relationship, and personal context leaks into
  the security thread. Key on the email address and the thread, keep the two personae separate,
  and never let a name match supply facts (occupation, relationship, location) that the security
  thread never established.
- **Separate the disclosure from any personal ask.** A researcher may ask for a support letter, a visa endorsement, a referral, or a job introduction in the same breath as the report. Acknowledging the report does not obligate any of that, and granting one courtesy does not create a standing channel. Handle the two as separate decisions, and let the principal decide the personal one himself.
- **Do not bundle the personal ask into the disclosure reply** to smooth the relationship. If it needs answering, answer it in its own message.
- **Verify the researcher before vouching.** Before the principal signs, endorses, or recommends anything, probe the public record: CVEs assigned by real CNAs, advisory credits, published writing, the tools they claim to maintain. A clean record is the finding; a thin one is also the finding.

## Pitfalls

- **A vendor acknowledgment is a permanent record, not a courtesy note.** Anything overstated in it is a claim the researcher may later test in public. Understate, then deliver.
- **"We fixed it" without "here is what is still broken" is the failure that ends vendor credibility.** The residual is not a concession; it is the part that makes the rest believable.
- **The reporter's read can be right about the bug and wrong about the current code.** Reproduce before accepting, and check whether the described path still exists.
- **Never let the researcher's publication approval become indefinite silence.** Give the three conditions, then commit to confirming when the fix reaches a released build. An unanswered approval request is what turns a friendly disclosure into a public write-up with no vendor input.
- **Do not export internal topology into any external reply, including a friendly one.** The scope rule at step 6 applies to the acknowledgment email as well.
- **A reply that never left the outbox is the root cause of most escalations.** When a report surfaces publicly, check the private lane's send records before assuming the researcher jumped the embargo.
- **A published acknowledgment window nobody measures is worse than no policy at all.** It advertises a channel and then does not answer. The remedy is a watch on the lane and on the unanswered-thread condition, not a firmer sentence in the document.
- **A guard that covers the paths the reporter named is not a guard that covers the sink.**
  Enumerate call sites, diff against guarded sites, and treat the module's own completeness
  claim as a hypothesis. Quote the difference, not the docstring.
- **A disclosure is not an audit.** One confirmed finding never closes the "no independent security review" gap — the two describe different artefacts and live in different rows.

## Send lanes — two options, different trade-offs

| Lane | Tool | Audit trail | When to use |
|---|---|---|---|
| **Governed** (`gov_email.py`) | `prepare` → confirm token → `send` | Hash-chained JSONL ledger (`audit/email_ledger.jsonl`), intent logged BEFORE send | Default for all disclosure correspondence. See `references/outbound-send-lane.md` § Governed lane. |
| **APA bridge** (`forge_email :18093`) | HTTP POST | Content hash (sha256) in response, no local ledger | When governed lane is unavailable or for non-disclosure sends. See `references/outbound-send-lane.md`. |

**Default:** Use the governed lane. It gives you a receipt chain and prevents unsent-by-accident.

## References

- `references/published-artifact-verification.md` — the three-layer probe (repo / running service / published artefact): registry `upload_time` vs fix commit, opening the archive and hash-matching the shipped module, call-site completeness inside the artefact, and why a stale raw-CDN read is not evidence a push failed.
- `references/outbound-send-lane.md` — both send lanes: the governed lane (`gov_email.py`) with prepare-confirm-send workflow and JSONL audit ledger, and the APA email bridge (`forge_email`, :18093) with probe, POST shape, and content hash receipt.

## Related

- `deployment-claim-verification` — #59 (fixed on main ≠ fixed in the published artefact) and #22 (security-gate claims need live behavioural tests)
- `agent-session-forensics` — § "Episode reconstruction" for recovering the thread
- `email-outbound` — the Brevo and governed lanes; the equivalent section for outbound sending in general. That skill is user-owned — if it needs the bridge contract, ask the user to run `hermes curator adopt email-outbound` rather than expecting this curator to patch it.
- `hermes-response-format-fit` — human-facing register calibration. Also user-owned; the register rule that applies to external correspondence is inlined here as § Register so it stays reachable.
