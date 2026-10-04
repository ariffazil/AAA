# SHEBTOC::P0::WITNESS_CAPTURE_LAYER::v1

> **Status:** F13_RATIFIED_SOVEREIGN (2026-10-04)
> **Ratified by:** Muhammad Arif bin Fazil (F13 SOVEREIGN) · Order: "sah"
> **Forged:** 2026-10-04 (session HERMES_MD_WITNESS_RESEARCH)
> **Author:** HERMES ASI under F13 directive
> **For:** closure of the historical-reconstruction gap in mutation governance

---

## Origin

During execution of the 6 SHEBTOC priorities (P1-P6) on 2026-10-04, F13 SOVEREIGN
identified that arifOS possesses **observation remnants** (scar ledger, receipt chain,
VAULT999, carry_forward, ratification records, session seals, arifFLOW receipts, state
transition discipline) but lacks a **unified Witness Capture Layer** that turns every
mutation into a structured witness object **at the moment of mutation**, not on
post-hoc audit.

This is the frontier SHEBTOC must close: **without P0, P1-P4 are historical reconstructions;
with P0, the substrate invoices reality continuously.**

---

## Problem Statement

Current state of mutation observation in arifOS:

| Substrate component | Captures | Misses |
|---|---|---|
| `scars.jsonl` (runtime) | W_scar events | non-scar mutations |
| `SEAL_RECEIPTS/` | ratifications | ordinary edits |
| `carry_forward.json` | session continuity | inter-session file changes |
| `arifFLOW receipts` | flow events | direct file writes |
| git log | all changes | non-git-tracked files, semantic meaning |
| `cron/jobs.json` | scheduled work | ad-hoc edits |
| `violations.jsonl` (runtime) | F-floor violations | non-violation mutations |
| `deploy-receipts.jsonl` | deployments | in-place mutations |

**Gap:** no single capture plumbing that records `who, when, what, why, authority,
consequence, downstream_impact` for every md file mutation in real time.

---

## Definition: Witness Capture Layer

A Witness Capture Layer is the substrate-level instrumentation that **records every
mutation as a witness object at the moment it occurs**, with five mandatory fields:

```
1. WHO       — actor (F13, sovereign_chat_override, 333-AGI, FI-NNN, cron, anonymous)
2. WHEN      — UTC ISO-8601 timestamp, microsecond precision
3. WHAT      — file path, byte delta, AST delta (heading add/remove/modify)
4. WHY       — provenance (PR link, commit msg, ratification chain, F13 binary)
5. CONSEQUENCE — downstream consumers affected, capability graph delta, embedding staleness flag
```

**Plus three optional fields** (when available):

```
6. AUTHORITY — canonical class (F13_RATIFIED, DRAFT, OPERATIONAL, SKILL, RECEIPT)
7. RELATION  — capability graph edge changes (added/removed/modified)
8. RECEIPT   — write-ahead log entry for the mutation itself
```

---

## Implementation Surface

### Capture Points

Three classes of capture point:

**1. Editor-level (preferred).** Hook into the canonical edit tools:
- `patch` (fuzzy search-replace, used by HERMES runtime)
- `write_file` (full overwrite)
- `edit` (Aider-style)
- `git commit` (with file paths)
- `find` + shell `mv/cp/rm` (when sanctioned)

Every editor invocation MUST emit a witness object before returning success.

**2. Watcher-level (passive).** `inotifywait` or `fswatch` on the protected paths
(`/root/.hermes/SOUL.md`, `/root/AAA/canon/`, `/root/AAA/instructions/`). Catches
edits by other tools (vim, VS Code, MCP server, A-FORGE).

**3. Cron-level (backstop).** 5-minute cron that diffs mtimes against last witness
log. If gap, emit retroactive witness. Catches missed captures.

### Storage

**Primary:** append-only JSONL at `/root/.hermes/runtime/witness_capture.jsonl`
(replaces or augments `scars.jsonl`).

**Schema per line:**

```json
{
  "ts": "2026-10-04T11:23:45.678901Z",
  "actor": "F13",
  "channel": "sovereign_chat_override",
  "file": "/root/AAA/canon/SHEBTOC_P0_WITNESS_CAPTURE_LAYER_v1.md",
  "before_sha256": "abc123...",
  "after_sha256": "def456...",
  "byte_delta": +1234,
  "ast_delta": {
    "headings_added": ["## P0.3 Capture Plumbing"],
    "headings_removed": [],
    "headings_modified": ["## Problem Statement"]
  },
  "authority_before": "STAGED",
  "authority_after": "F13_RATIFIED",
  "ratification_chain": ["ARIF 'sah' via 333-AGI channel"],
  "downstream_impact": {
    "embedding_stale": false,
    "capability_graph_affected": true,
    "consumers_to_notify": ["mcp__arifos__arif_route", "carry_forward.py"]
  },
  "trace_id": "wc-20261004T112345-001"
}
```

### Promotion Rule

Captures that involve a `DRAFT_* → F13_RATIFIED_*` transition **automatically**
emit a second witness object (the ratification event itself). This is the
**mutation-capture close-the-loop** semantic.

### Retention

- Hot: 30 days in JSONL
- Cold: rotate to `/root/.hermes/runtime/archive/witness_capture-YYYY-MM.jsonl.gz`
- Per-file chain: keep forever (rebuild = file history reconstruction)
- Aggregate: 7 years (matches ZKPC retention)

---

## Constitutional Anchoring

The Witness Capture Layer is **NOT a new canon**. It is **infrastructure for canon**.

Reference:

- `/root/AAA/canon/WITNESS_OBJECT_SPEC_v1.md` — defines what a witness object is
- `/root/AAA/canon/HERMES_DATA_CLASSIFICATION_ROUTING_v1.md` — class definitions
- `/root/AAA/canon/SCAR_AUTHORITY.md` — scar semantics that P0 captures
- `/root/AAA/canon/AUTHORITY_ENVELOPE` (in instructions/) — CanMutate predicate
- `/root/AAA/canon/STATE_TRANSITION_DISCIPLINE` (in instructions/) — PRODUCED≠SENT≠DELIVERED...

---

## Acceptance Criteria

P0 is operational when:

1. ✅ Every mutation to `/root/.hermes/SOUL.md`, `/root/AAA/canon/*`, `/root/AAA/instructions/*` produces a witness object within 1 second of the mutation.
2. ✅ Witness objects are queryable: `wc_query --file <path> --since <ts> --actor <id>`
3. ✅ Embedding staleness flag is set automatically when content_hash changes.
4. ✅ Capability graph delta is emitted for files referenced in `/root/.hermes/lanes/people.yaml`, `/root/AAA/canon/CANONICAL_GLOSSARY.md`, or `/root/AAA/names/`.
5. ✅ Daily cron produces `witness_capture_summary-YYYY-MM-DD.md` for the day's mutations.
6. ✅ Witness objects are hash-chained (each `prev_hash` = prior object's hash) for tamper-evidence.
7. ✅ F13 ratification of a staged file emits 2 witness objects: (a) the move itself, (b) the ratification event.

---

## Phased Rollout

**Phase 0 (staged proposal):** spec forged and ratified by F13.

**Phase 1 (post-ratification):** instrument HERMES own tools (`patch`, `write_file`,
`terminal mv/cp/rm`) to emit witnesses. **Pilot scope: SOUL.md only.**

**Phase 2:** extend to all `/root/AAA/canon/*.md`. Add `inotifywait` watcher as
passive backstop.

**Phase 3:** extend to `/root/AAA/instructions/*.md` and `/root/.hermes/*.md`.

**Phase 4:** extend to all SKILL.md (756 in AAA + 22 in hermes).

**Phase 5:** add `fswatch` watcher to catch external edits. Add daily cron summarizer.

**Phase 6:** add ZKPC anchor — every Nth witness object committed to a chain
that has external witness capability.

---

## Open Questions for F13

1. **Actor attribution for F13 SOVEREIGN edits** — when Arif edits via `/root/AAA/.staged/` →
   `/root/AAA/canon/` via F13 binary, who is the actor? "F13" or "ARIF"?
2. **Hash-chain or Merkle tree?** Hash-chain is simpler; Merkle allows O(log n) proofs.
3. **Should witness objects be themselves md files** (in `/root/AAA/canon/WITNESS_CAPTURE/`)?
   Or stay JSONL? md makes them human-readable; JSONL makes them queryable. Both?
4. **Retention of failed mutations** — should the layer capture *attempted* mutations
   that were ACL-blocked? Useful for security forensics, but adds noise.
5. **Cross-host propagation** — KVM4 (IRFANclaw) and KVM8 (HERMES) both mutate canon/.
   Should witness capture sync, or remain host-local with eventual consistency?

---

## Relationship to Existing Infrastructure

| Existing | P0 relationship |
|---|---|
| `scars.jsonl` (runtime) | P0 SUBSUMES — scars become a witness_class subtype |
| `violations.jsonl` | P0 INHERITS — violation events are witness with class=VIOLATION |
| `deploy-receipts.jsonl` | P0 REFERENCES — deploy events are witness with class=DEPLOY |
| `carry_forward.json` | P0 COMPLEMENTS — session continuity, not file mutation |
| `arifFLOW receipts` | P0 INCLUDES — flow events are witness with class=FLOW |
| git log | P0 AUGMENTS — git gives file-level, P0 gives semantic-level (heading delta) |
| VAULT999 | P0 EVENTUALLY ANCHORS — long-term storage of witness hash-chain |

---

## Anti-Bangang Compliance Check

Per `anti-bangang-engineering.md` LAWS:

- **LAW 1 (no extra work for human):** P0 runs on infrastructure, zero human action.
- **LAW 3 (no new canon/ledger/JSON without failure class):** ✅ failure class = post-hoc audit cost; P0 closes it.
- **LAW 4 (one-sentence problem statement):** "Every md mutation today is a post-hoc witness; P0 makes every mutation a real-time witness."
- **LAW 5 (Syed Test):** P0 output is hidden in runtime/, not visible to humans unless queried.
- **LAW 6 (Arif Test):** F13 reads ≤3 sentences to understand P0.
- **LAW 8 (one problem, one owner):** P0 owner = HERMES runtime; not duplicated.
- **LAW 9 (action > documentation):** P0 spec here is ratified; deployment is the action.
- **LAW 10 (simpler):** P0 = one append-only JSONL + three capture points. No new abstraction layers.

---

## SEAL-WORTHY (Analysis-Level)

```
Reality
↓
Attention
↓
Capture
↓
Witness
↓
Governance
↓
Mutation
↓
Continuity
```

This document closes the gap between `Attention → Capture` and `Mutation → Continuity`.
Without P0, the chain has a void at the capture point.
With P0, every mutation becomes a witness, every witness becomes a candidate for governance.

**Status:** F13_RATIFIED_SOVEREIGN (2026-10-04)

---

*Forged 2026-10-04 in session with HERMES ASI under F13 directive "execute all agentically until seal all P". Ratified by Arif with "sah".*
