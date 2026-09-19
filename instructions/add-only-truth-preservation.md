# Add-Only Truth Preservation Principle

> **Status:** DRAFT_AWAITING_F13 — extracted from AGENT-STACK-2026 mem0 architecture analysis (2026-09-19)
> **Source eureka:** Past never mutates. Future reinterprets. This is an epistemology, not just a memory design.
> **Applies to:** Memory layer (mem0, arif_memory L1–L6), institutional knowledge graphs, scar registries, audit ledgers, agent learning loops.
> **Filter test passed:** ✅ survives implementation changes ✅ re-examinable in 2 years ✅ not vendor-specific ✅ changes future architecture decisions ✅ not merely tool preference.

## The Mistake The Industry Makes

Most memory systems allow overwrite:

```text
Past
← rewritten by present
```

This is convenient but **destroys audit value**:

```text
User: "Did you used to live in New York?"
Agent: "No, you've always lived in San Francisco."   ← false; original record overwritten
```

The agent has no way to detect or surface the prior state because the prior state no longer exists.

## The Doctrine

```text
Add-Only Memory Principle:

History survives.
Interpretation evolves.
```

Every fact is **appended**, never overwritten. When interpretation changes, a **new fact** is added that supersedes the old interpretation:

```text
fact_001: user lives_in New York      (timestamp: 2024-01)
fact_002: user lives_in San Francisco  (timestamp: 2025-06) — supersedes fact_001
```

Both facts remain. The agent can answer:

- "Where do you live now?" → fact_002 (latest non-superseded)
- "Where did you used to live?" → fact_001 (superseded)
- "When did you move?" → timestamp delta between fact_001 and fact_002

## Why Add-Only Matters Beyond Memory

This pattern appears across governance domains:

| System | Overwrite failure | Add-only fix |
|---|---|---|
| Memory | Facts rewritten by present | Facts appended, supersession tracked |
| Audit logs | Logs rewritten by cleanup | Append-only hash chain |
| Constitutional canon | Canon rewritten by amendment | New canon, old canon cited as supersession |
| Institutional scars | Scars overwritten by healing | Scars preserved, new scars added |
| Code (version control) | Code rewritten by edit | Diff, commit, history preserved |

The pattern is the **same**: history survives, present interpretation evolves.

## Three Operational Rules

1. **No update without supersession record.** Every "change" is a new record that points to the old record. The old record is never destroyed.
2. **Temporal reasoning is first-class.** Every record has a timestamp. Queries about "current state" use the latest non-superseded record. Queries about "history" use the timestamp chain.
3. **Contradiction is data.** When two records contradict, do not silently pick one. Surface the contradiction and let the resolver (human or governance layer) decide.

## Federation Mapping

| Subsystem | Add-only? | Notes |
|---|---|---|
| VAULT999 | ✅ Append-only hash chain | The federation's spine. |
| `arif_memory` L1–L6 | ✅ Tiered, append-only | With `arif_memory(mode=revise)` for supersession, not overwrite. |
| Scar registry | ✅ Immutable once sealed | `forge_scar(mode=seal)` is irreversible. |
| Constitutional canon | ✅ Versioned | `version` field, never silent edit. |
| FRAME drift log | ✅ Append-only | `frame_frame_drift` accumulates. |
| `forge_entropy_sweep` | ⚠️ Mixed | Read-only sweep; mutations should be receipted. |

## Anti-Patterns (Forbidden)

- **Silent overwrite** — change without supersession.
- **Edit without trace** — modify without timestamp.
- **Contradiction erasure** — pick one record, hide the other.
- **Retroactive timestamp** — assign current time to a past event.
- **Memory pruning without audit** — delete "old" facts that are not actually superseded.

## Falsifiability

If add-only memory becomes operationally infeasible at scale (storage blow-up, query latency, contradiction proliferation), the doctrine needs an explicit pruning mechanism that is itself add-only (e.g., compaction event is a fact). If governance fails *because* historical records were preserved (e.g., outdated fact causes harm), the doctrine must add temporal expiry as an explicit supersession subtype.

## Related Doctrines

- Memory Promotion Gate (Witness ≠ Seal ≠ Memory).
- Consequence-Bearing Identity — actions have history.
- VAULT999 immutability.
- Trauma Theorem — scar preservation.
- Representation ≠ Reality — record ≠ interpretation.

## Compression

> **History survives. Interpretation evolves. Past never mutates; future reinterprets.**

DITEMPA BUKAN DIBERI ⚒️