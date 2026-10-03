<!-- provenance: cross-surface-conformance-audit (audit-ops member) -->
<!-- source: /root/AAA/skills/audit/cross-surface-conformance-audit/SKILL.md -->
<!-- sha256 of the body below, byte-for-byte: 03ad312d3643ee9d42c57ecf49a9a7e28885128bfc84d8aaa45d8d435a1fa6a8 -->
<!-- folded into audit-ops v2.0.0, cluster audit/verification, 2026-09-20 -->
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

## Cross-node fresh-first discipline (vantage staleness)

A surface's "current state" is a function of the vantage the reader holds and when they last
fetched. Cross-node claims decay unless the reader declares the probe timestamp and a fresh
fetch was performed in the same audit window. The defect class is "address on stale map":
two agents each read the right file at the right path, but at different times, and report
incompatible states that are both individually true.

- **Stale remote-tracking ref.** `git rev-parse origin/main` returns the *remote-tracking
  ref*, not the live origin. Without `git fetch`, the ref is whatever the local repo last saw.
  A "KVM4 ahead 26 / behind 2838" claim sourced from the local ref is a local-side reading; an
  origin-side claim must follow `git fetch origin` in the same audit window. A peer
  relay of a number is *not* a fresh fetch — re-derive, do not relay.
- **Stale schema path.** The same JSON can be addressed two ways (`d.get('key')` vs
  `d['nested']['key']`). When a writer adds a nested schema and a reader still uses the
  flat path, the reader sees a phantom absence. The fix is not "fabrication" — the data
  exists; the reader's schema is the wrong address. Probe the write path before declaring
  the field empty.
- **Probe-without-fetch = address on stale map.** Whether git remote-tracking, JSON schema
  path, or runtime config — every cross-node / cross-schema claim must declare (a) the
  vantage (host, path, checkout state) and (b) the probe timestamp + freshness action
  (`git fetch origin` within the last N minutes). Without both, the claim auto-decays to
  "based on last known state" and is not citable as a present-tense finding.
- **Per-node identity, not global identity.** Config files diverge across nodes by design:
  opencode.json on KVM4 hash ≠ KVM8 hash because node-specific overrides, runtime paths, and
  credentials differ. A hash pin is per-vantage; cross-node hash equality is not a property
  to claim. Audit integrity requires **per-node pin + schema comparison**, not "file X has
  hash Y" treated as a global fact.

## Receipt / reference ID type declaration

Reports that cite "the receipt", "the commit", or "the session" without specifying the
identifier type (git hash, FQ receipt UUID, session ID, OTel trace id) are unprovable
without first-class evidence. The cross-auditor must restate the claim or downgrade to
UNKNOWN — never accept a bare 8-char prefix and infer the type.

- **Git commit hash.** 40 hex chars (prefix allowed). Verifiable by `git -C <repo> log` or
  `git cat-file -t <sha>`. Pushed = appears in `git log origin/<branch>`. Local-only =
  appears in `git log` but `git rev-list --left-right --count origin/main...main`
  returns non-zero on at least one side.
- **FQ receipt ID.** UUID 8-char prefix, arifFlow runtime, JSONL-backed. Verifiable by
  `grep <full-uuid> /var/lib/arifflow/receipts.jsonl`. KVM-local; no cross-node
  sync. Receipt chain parent links are in `parent_receipt_ids` / `parent_receipt_hashes`
  fields — same shape, different namespace.
- **Session ID.** Free-form string. Verifiable by `carry_forward.json` grep, or
  `session_search` lookup. Per-runtime, may differ across harnesses.
- **OTel / trace id.** Standard hex. Verifiable by telemetry backend.
- **UNKNOWN by default.** If the report does not declare the type, downgrade the claim
  to UNKNOWN — not PASS. Two reviewers who pass an untyped ID have passed the same
  unverified text; that is an echo, not independent confirmation.

## Local committed vs pushed (git-specific)

"Committed" and "pushed" are two distinct transitions. A local commit that exists in the
working tree but is not on `origin/<branch>` is *not* reachable by a peer audit. Reports
that say "pushed" without `git ls-remote origin <branch>` confirmation are
overclaim — default to "committed locally" until remote-side evidence is in hand.

- `git log --oneline -1` proves local HEAD only.
- `git fetch origin && git rev-parse origin/<branch>` is the minimum to claim "matches
  origin".
- `git rev-list --left-right --count origin/main...main` is the divergence readout —
  `0\t0` means synced, anything else means at least one side has unpushed work or
  stale remote-tracking.
- "PONG" or "PONG observed" is **not** push evidence — the local daemon can respond
  before the remote is updated.

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
