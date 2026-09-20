---
name: cross-surface-conformance-audit
description: "Use when surfaces disagree about one entity's truth."
version: 1.0.0
owner: Hermes (arifOS federation)
risk_tier: low
floor_scope: [F2, F7, F11]
autonomy_tier: T1
tags: [audit, conformance, multi-surface, divergence, contradiction, witness-reconciliation, verification]
triggers:
  - "surfaces disagree"
  - "which number is right"
  - "registry drift"
  - "advertised vs callable"
  - "stage mismatch"
  - "two witnesses disagree"
  - "phantom tool"
  - "schema mismatch"
  - "conformance audit"
  - "capability truth"
  - "split brain"
  - "docs say X but the API says Y"
---

# Cross-Surface Conformance Audit

> Existence scanning asks *"is X there?"*. This asks a different question:
> *"do all surfaces of this live service say the SAME THING about X?"*

## When to use

- A service exposes more than one read surface (MCP method lists, HTTP endpoints, health
  output, generated manifests, repo canon, prompt/doc registries).
- Two auditors, witnesses, or agents report accurate but contradictory findings.
- A capability is advertised but fails when called, or a number in docs differs from the number
  the API returns.
- Before declaring any registry/manifest "drifted" — establish which surface is stale first.

## Core law

**A healthy service can serve mutually contradictory semantics from its own endpoints, with
nothing cached and every surface live.** Each surface is then individually correct and the
system is still lying to half its readers.

The second law: **when two competent witnesses disagree and both are accurate, suspect an
unqualified term, not a wrong value.** One word serving two meanings produces two correct,
mutually contradictory reports.

## Step 1 — Enumerate every surface before comparing anything

```python
# JSON-RPC surfaces — reach layers a convenience endpoint may not expose
#   1. initialize  ->  2. tools/list  ->  3. prompts/list  ->  4. resources/list
# then the projection surfaces:
#   curl :PORT/tools   |   curl :PORT/health   |   the repo's declared canon/manifest file
```

Bump the protocol version and reuse the session id across these calls so you are comparing one
server, not four handshakes. Record which surfaces you could NOT reach — an unenumerated
surface is an open caveat, not a clean result.

## Step 2 — Build the comparison grid, then diff columns

One row per `entity | surface | field | value`. Then diff the columns.

| entity | surface A | surface B | surface C | canon file | verdict |
|---|---|---|---|---|---|
| `entity_1` | 666 | 888 | 888 | 666 | **DIVERGENT** |

Any entity whose value differs across surfaces is a divergence — even when each surface is
individually correct. Include the repo's declared canon column: it anchors which surfaces are
following the source and which have drifted.

## Step 3 — Classify the cause before proposing a fix

The fix class depends entirely on which of these it is:

1. **Different axes** — the surfaces are not measuring the same thing.
2. **Different readers** — each surface resolves the term to a different object.
3. **Different ladders** — two coexisting vocabularies share one set of bare labels.
4. **Different sources of truth** — two hardcoded tables in one artifact, no import between
   them, no cross-check gate. **Diverges permanently.**

Cause 4 is the most common and the only one where a one-sided correction is actively wrong.

## Step 4 — Check for the coupling gate, not just the values

After finding a divergence, ask whether **any check compares the surfaces.** If none exists, the
divergence regresses the moment either side is edited, and the real finding is the missing gate.

Report the fix as a *class*: reconcile to one source, regenerate the derived surfaces, add a
per-entity cross-surface gate. Never "change the number in file B".

## The veto

**Never resolve a contradiction by overwriting one side's namespace with the other's.** That is
a category error, not a fix — it trades a visible divergence for an invisible one and loses the
evidence that the divergence existed.

When both sides are defensible, the deliverable is a **decision request to the owner**, with the
evidence weight of each reading stated plainly, not a silent pick.

## Negative claims and witness vantage

Absence, "missing", and "fabricated" are claims, not defaults, and the observing vantage
silently supplies them.

- Every absence claim states its **vantage** — host, path, checkout state. A path absent on one
  node says nothing about another node's tree.
- Before accepting a peer's absence/fabrication verdict, require all three: their seat identity
  (host + network address, executed on their node), whether their view is a **stale mirror**, and
  one **positive control** they can see from the same tree.
- A fabrication verdict founded on a stale vantage is the same defect as a phantom-capability
  claim with the sign flipped: both assert a state of the world from a position that cannot
  observe it.
- Separate **UNKNOWN** (not measured) from **absent** (measured, not found) from **UNCREATED**
  (cannot exist yet). Only the middle one is an evidence claim.
- On retraction, record the retraction *and* the vantage discipline that would have prevented it.
  Do not let a retraction be read as the original claim having been "half right".

## Pitfalls

- **Probe-author error is not tool defect.** Before scoring a call as `schema_mismatch`, re-read
  the entity's declared `inputSchema`. A mismatch caused by arguments you invented is your bug.
  Re-probe with the documented property names before recording a CALLABLE failure.
- **Two numbers on different axes are not a contradiction.** Artifact-chain health versus
  governance-question results, or point-in-time quality versus dynamics, answer different
  questions. Do not force-reconcile them into one verdict.
- **A large GENESIS/None fraction in a chain is parallel lineages, not breakage** — but keep
  going: find what wrote them. Test fixtures resolving a production store constant (instead of a
  tmp path) write real records on every test run, so the fixture count measures *test executions*,
  not production activity.
- **Do not delegate the cross-check to a subagent.** The second reading must be a genuinely
  independent surface or seat, or it is an echo, not a witness.
- **Count of surfaces reached is part of the result.** N surfaces probed, M divergent, and the
  list of surfaces you did not reach.

## Reporting contract

- Grid of `entity | surface | value | verdict` — no prose substitute for the table.
- For each divergence: the cause class (axes / readers / ladders / sources), and whether a
  coupling gate exists.
- Every value labelled with the surface it came from; every absence claim labelled with its
  vantage.
- Findings that need a decision go to the owner as a binary with evidence weight per side — not
  as a self-selected fix.
- Unreachable surfaces listed explicitly. "All consistent" is only claimable over the surfaces
  you actually reached.

## Related

- `live-probe-audit-pattern` (user-owned) — existence scanning, multi-writer awareness,
  hash-chain lineage. This skill is the *semantic divergence* companion to its *existence* scan.
- `federation-machine-verification` (user-owned) — node/seat identity, node-local path resolution.
- `arifos-evidence-policy` (user-owned) — claim states, recency contract, uncertainty labels.

DITEMPA BUKAN DIBERI.
