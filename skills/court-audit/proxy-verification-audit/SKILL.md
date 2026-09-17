---
name: proxy-verification-audit
id: proxy-verification-audit
version: 1.0.0
risk_tier: low
floor_scope: [F2, F9, F11, F13]
autonomy_tier: T0
description: "Use when auditing an auth/gate control for verification."
when_to_use: "Auditing a session gate, an authority band, a human-approval field, an allow/deny regex, or any control whose name promises verification. Also when a fix must be proven to close a bypass rather than to merely look closed."
tags: [authority, gates, verification, audit, falsification, arifos]
---

# Proxy-Verification Audit

> **DITEMPA BUKAN DIBERI** — A control that never says no is a label, not a boundary.

## The one question

For any control, ask: **what input would make it refuse?** If you cannot name a failing input from
reading the code, the control is not checking content — it is checking the shape of a request.

Six shapes recur, and all six are the same defect wearing different clothes:

| # | Proxy trusted | Reality it stands in for | How to falsify |
|---|---|---|---|
| 1 | a service answers a handshake | the session/credential is valid | pass a fabricated id; if it returns PASS the check was availability |
| 2 | a command string does not match a deny-regex | the action is authorized | same verb via a Makefile target, a wrapper script, or `subprocess` |
| 3 | a caller-supplied boolean | cryptographic proof of identity | set the flag `true` yourself and watch the hold clear |
| 4 | a non-empty string in an approval field | a human approved | pass a self-labelled fabricated sentence; compare field-for-field with a genuine receipt |
| 5 | a name present in an allow-table | identity proven | A/B an unknown name against a table name, same lane, same call shape, no signature |
| 6 | text does not match a threat pattern | the text is not a threat | write documentation *about* the control — the detector fires on the description |

Defect 5 usually supplies the precondition for defect 4, which supplies the label that makes 3 look
sanctioned, while 2 blocks the fix from being loaded. Map the chain before ranking severity.

## Procedure

1. **Find the granting branch**, not the function name. `grep -n` the boolean/flag, then read the
   expression that consumes it (`auth = bool(caller_flag or payload.get(...))`). Check BOTH routes —
   a top-level parameter and the same key inside a free-form payload dict. Removing the schema
   parameter alone leaves the payload path open.
2. **Read the comment above it.** Controls often carry a note admitting they are not a boundary
   while the branch below uses them as one. Comment contradicting code is itself a finding, and it
   tells you the fix is unwelcome to nobody.
3. **Inject the fabricated value.** Measure the output. Then run the identical call WITHOUT it and
   diff. One PASS proves nothing; the pair is the evidence.
4. **Prove the ordering.** A gate can be "cleared" while another validator is erroring in the same
   response, because the two are computed at different points and land in different lists
   (`warnings` vs `errors`) that never meet. Read the line numbers, not just the verdict.
5. **Witness on a durable artifact.** Trace ids returned in a response are frequently not persisted
   anywhere. Cite the ledger row, session-store entry, or DB record — and confirm the store actually
   contains it before citing it.
6. **Patch, test fail-closed, then prove load.** A committed fix in an already-imported module is
   disk truth, not runtime truth. Re-run the attack after the restart and show the new verdict.

## Rules that cost the least to follow

- **Fail-closed must be tested as a branch, not assumed.** Unreachable, rejected, and raising are
  three separate paths; assert all three, plus that a legitimate verified session still passes and
  that non-critical paths are unchanged. Otherwise the fix breaks the users who were never the
  problem.
- **Keep the rejected parameter.** Removing it turns a soft warning into a hard schema rejection for
  every legacy caller. Retain it, strip its authority, and emit an explicit
  `SELF_ATTESTED_..._IGNORED` warning so the caller learns instead of silently breaking.
- **A scan will over-report by orders of magnitude.** `verify(signature_hex)` *must* accept a
  signature from the caller — that is the thing being checked, not authority being claimed — and
  unrelated `*_override` names (a gamma-ray column, a depth parameter) collide by shape. Filter with
  one question: *does the code USE this value to grant something without an external check?* Report
  the surviving sites, never the hit count.
- **Pre-existing test failures: prove them by stash.** `git stash push <your files>`, re-run, show
  the identical failure, restore. Without that, every red test becomes your regression.
- **Never route around a gate with a string it happens not to match.** If the deny-regex misses a
  Makefile target or a wrapper, using it is circumvention by proxy and voids the audit's own
  standard. Escalate the deny-all, or stop.
- **If you must alter wording to get a document past a detector, disclose it inside the document.**
  An audit that self-censors to fit a shape detector is worthless unless the censorship is named.
- **Corrected claims stay in the record.** Keep a retraction table: claim, correction, evidence.
  A corrected claim is still a claim, and the next agent needs to see both halves.

## Metrics and witnesses: derive before hypothesising

Three wrong explanations for one scalar is the normal outcome when you reason from observed values
instead of from the formula. Full procedure in `references/metric-derivation-discipline.md`.
Short form:

1. Read the function that computes it — the formula, the window, the zero-data branch.
2. Recompute it from the underlying table for every observation you hold. Report "6/6 instants
   match", not "consistent with".
3. Check whether the value is a **floor constant** in disguise. A geometric mean over clamped factors
   (`max(0.01, x)`) returns the fourth root of the floor whenever one factor is zero — a single
   number that looks like a measurement and is really a constant.
4. Separate the regimes. A cold start (zero rows for that actor) returns an UNMEASURED sentinel by
   design, and the first call writes the row that makes the second call measurable — a
   self-referential threshold easily mistaken for transport, actor state, or runtime entropy.
5. Then ask what the formula really reports. If a factor is an evidence-compliance ratio and it is
   ~0 across the fleet, the scalar is a near-constant readout of that one fact, and its narrow range
   is why it hides the anomaly.

The same applies to any "witness" or "consensus" count: **find the literals.** A tri-witness score
built from hardcoded constants is a restatement of the verified/unverified branch, not
corroboration, and must never be cited as independent confirmation of an identity.

## Related

- `deploy-drift-verification` — disk truth vs process truth, node forks, which tree the service
  imports. Load it alongside this skill whenever the fix must be proven *loaded*, not just written.
- `claim-receipt-discipline` — tagged claims, receipts, denominators, retraction discipline.
- `references/metric-derivation-discipline.md` — the derive-before-hypothesise procedure in full,
  with the floor-constant, cold-start-regime, and literal-witness traps.
