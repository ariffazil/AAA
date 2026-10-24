---
name: governance-removal-review
description: "Use when an agent proposes removing a gate or field."
version: 1.0.0
owner: AAA
risk_tier: low
autonomy_tier: T0
floor_scope: [F1, F2, F7]
metadata:
  short-description: "Grade removal proposals - dead vs dormant vs load-bearing"
---

# Governance Removal Review

Someone — a peer agent, a pasted review, a frustrated human — hands you a list: "these eight
things are security theatre, remove them." The list usually mixes three kinds of item: name
furniture that should go, dormant-but-real machinery that should be switched on, and
load-bearing surface whose removal breaks a chain. Grade **each item**, then propose the
order. Never accept or reject the list wholesale.

Removal is easier to approve than to reverse. That asymmetry is why this skill exists.

## Procedure

1. **Split the list into discrete items.** One per line: a field, an enum member, a gate, a
   word, a branch of an `allowed_*` list.
2. **Grade each item** with the four tests below (dead / dormant / load-bearing /
   misdiagnosed). Do not skip one because it sounds obviously silly.
3. **Recompute every number they quote** from the store itself, not from the dashboard they
   are criticising. Publish the window, the denominator, the host, and the process start time.
   A counter-claim you did not measure is a second unreproducible figure.
4. **Check the hashed-body constraint** before approving any schema deletion (Test C).
5. **Check the authority constraint** before approving any capability widening (Test D).
6. **Propose an order**: small, reversible, chain-neutral items first; anything inside the
   constitution or the receipt schema last, with explicit human sign-off.
7. **Say what must NOT be removed**, one clause of why each. Not optional — a review that only
   lists deletions trains the next agent to keep deleting.

## The four tests

### Test A — dead, or only dormant?

Grep for **emitters and readers**, not for the definition. A symbol with a definition and zero
emitters is dead vocabulary and can go. A gate with zero recorded hits is usually **dormant**:
its refusal counter is `0` because nothing has ever tried the thing it refuses. Dormant
governance is the most common thing an auditor mislabels as theatre, because absence of
violations looks identical to absence of enforcement.

> Ask: did it never fire because it is broken, or because nobody attempted the failure?

### Test B — same word, or same decision?

Several refusal words that all read as "no" are often several decision classes: a
physical-irreversibility block, a capability/role resolution failure, an authority-band
ceiling, a witness wait, a governance verdict. Collapsing them into two deletes the
distinction between safety and permission — the one distinction a governed system exists to
keep.

The genuinely removable item in such a list is the *conflated* word (its own definition admits
two meanings) and the *unemitted* one. Fix a conflation by splitting it or renaming the
transport half; never by deleting the governance half.

### Test C — is the field inside a hashed body?

Before removing or nulling a field from an append-only, hash-chained record, read the hash
function. If the body hash covers the whole struct, deleting a field changes the digest of
every future record and breaks comparability with every sealed one.

Correct treatment: stop *emitting* or stop *returning* the field at the projection layer. Do
not delete it from the struct without a versioned migration. Say this in the review — it is
the constraint that turns "ten minutes of cleanup" into a migration, and the one an eager
reviewer always misses.

### Test D — does the shortcut reduce capability instead of guarding it?

A gate that withholds verbs at bind time, or a default that hides tools from a list, is not
safety — it is capability reduction at the surface. Check whether identity already restores it
(actor card, inherited-adat declaration, verified DID). If identity restores it, the list is
cosmetic and wrong. If only an irreversible verb is withheld, the list matches the stated
principle and stays.

Also separate the two fields that get confused here: a **transport status** and a
**governance verdict** may legitimately differ on the same successful call. Report both, and
name which one the human is reading.

## Rules

- **A field whose name says one thing and whose content is another is worse than a missing
  field.** Name-says-timestamp, content-is-uptime misleads every reader silently: fix or
  delete, never leave.
- **A deprecated label still preferred by a consumer is a two-body problem.** Find the
  consumer across the whole federation before deleting it. And before swapping it for the
  modern field, check both sit on the same axis — an aggregate band and a vector constellation
  are not interchangeable, and the swap becomes a second category error. When the axes differ,
  which axis the surface represents is the human's call.
- **An aggregate gated by a minimum measures who reported last**, not health: the evidence
  window is in memory, holds are persisted, so the scalar also measures time since the process
  started. Quote it with the start time and the per-actor table; never as a standing verdict.
- **Never bundle a hashed-schema change with cosmetic cleanup** in one proposal or commit.
- **Reversible first, constitutional last.** Renaming a transport state is not the same risk
  class as changing what the central governance verdict word means.

## Counting a field before calling it empty

Count `non-null / total` across the whole store, per field. Real stores are mixed: some fields
populate on every record, some on 4% (one producer only), some on 0%. A sampled null is not a
structural null. 0% rows are the only ones you may call empty — and then check whether the
producing path is dead code or merely not routed on the daemon route. A receipt-carried gate
reporting `{class: null, code: null, outcome: NOT_APPLICABLE}` on every response is honest
output for a gate that has never met a qualifying input.

## Output shape

Item, grade (`BUANG` / `DORMANT — switch on or remove deliberately` / `JANGAN — sebab` /
`FIX DAHULU`), one clause of evidence naming the file or probe. Then the order. Then the
don't-touch list. No ceremony.

## Pitfalls

- **Do not approve a removal because the report's arithmetic is right.** A correct ratio can
  support a wrong prescription; grade the prescription separately from the number.
- **Do not propose injecting receipts, seals or verification to make a gate look satisfied.**
  That is fabricating evidence into a sealed ledger, not cleanup. Genuine hold → real
  verification; misattributed reason → fix the reason, keep the hold.
- **Do not silently widen capability while removing a gate.** Check who can then call what.
- **Withdraw your own earlier prescription in the same turn** when a live read falsifies it.
  The reviewer who corrects himself is worth more than the one defending a prior line.
