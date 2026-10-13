# L5 (Graphiti) Layer Deprecation — Federation Memory Contract Amendment

> **Status:** F13_RATIFIED_CANON · Tier A · 2026-10-07 (TURN 123)
> **Authority:** F13 SOVEREIGN via TURN 123 (option 2 chosen: deprecate)
> **Amends:** /root/arifOS/docs/FEDERATION_MEMORY_CONTRACT.md §3 (Three-Leg Federation Write)
> **Decision trace:** /root/AAA/reports/memory-lifecycle-promotion-receipt-2026-10-07.md
> **Ratifikator:** Codex CLI (FI-005), session 01a1120c-e752-7422-9acc-ec0717ee5df8
> **Mutability:** Reversible (F13 may re-enable)

---

## 0 · Why now

L5 (Graphiti) was 4 months dormant after the 888 command neutralised the
worker (FEDERATION_MEMORY_CONTRACT.md §3.5, lines 73-78):

> 888 injects L5 entities manually via raw Cypher to FalkorDB
> The bridge stays in place as a forward-compatible substrate
> Do NOT auto-wake, debug, or fix the Graphiti worker. 888 owns this.

F13 has now resolved the ambiguity (TURN 123, option 2): **deprecate**.

The substrate (FalkorDB + graphiti-mcp container, 8 days up) stays running
as a *read-only historical graph* for any legacy entities 888 injected.
The *write path* through arif_memory_recall(mode=store) is now
**3-leg → 2-leg**: L3 (Qdrant) and L4 (Supabase Postgres) are canonical.
L5 is **advisory** and may be skipped without alarm.

## 1 · The amendment

| Before | After |
|---|---|
| 3-leg fan-out: L3 (Qdrant) + L4 (Supabase) + L5 (Graphiti) | 2-leg canonical fan-out: L3 (Qdrant) + L4 (Supabase) |
| L5 status field: queued / skipped / error | L5 status field deprecated; replaced by graph_tier=disabled |
| arif_memory_recall(mode=store) requires L5 | L5 absence no longer DEGRADED — only L3+L4 matter for stored=true |
| forge_canonize writes to L4 only (already true) | Unchanged |

## 2 · Migration of existing L5-queued rows

Any rows with l5_status=queued (pre-deprecation) **remain in L4 as
canonical** — the L4 row is the source of truth, not the L5 queue.

A one-shot cleanup task (l5_legacy_drain.py) is added in MOVE 3 to
flush any pre-deprecation queue to the L4-only state, and stamp a
l5_drain_at column on those rows.

## 3 · Re-enable path (if F13 ever reverses)

Reversibility is preserved. The re-enable path is:
1. F13 ratifies L5_RE_ENABLE_2026-XX-XX.md (single file).
2. The patch flips _l5_async_enabled() default back to true.
3. The bridge (arifosmcp.runtime.l5_sovereign_forge) wakes the worker.
4. A 3-leg fan-out is restored.

This single file IS the deprecation flag. Search this file in canon to
verify deprecation is in effect.

## 4 · What is NOT changed

- L5_EXECUTE_IRREVERSIBLE in tools.py (line 869 etc.) is an **agency
  level** label, not the Graphiti layer. Untouched. Renaming it is a
  separate decision (out of scope; L5 in agency levels is unrelated).
- FalkorDB + graphiti-mcp containers stay running for read-only queries
  (legacy entities, 888-injected Cypher).
- The 6-Layer Atlas (L1..L6) in the Federation Memory Contract remains —
  L5 is still in the atlas, but its *write path* is now optional.

## 5 · Falsifiability

1. New post-deprecation writes must NOT add l5_status=queued to memory_store.
   Allow 0 in production; test fixtures may carry it.
2. arif_memory_recall(mode=store, skip_l5=True) must succeed with
   stored=true based on L3+L4 only.
3. forge_vps_services may show graphiti up (read-only) but
   forge_vps_ports 18412 is no longer load-bearing for memory writes.

## 6 · Re-enable protocol (if F13 reverses)

A single ratification file (L5-RE-ENABLE-<date>.md) placed in
/root/AAA/instructions/ with status F13_RATIFIED_CANON supersedes this one.
The mechanism: a git pull on arifOS, then flip one env var
(L5_SOVEREIGN_ASYNC=true), then restart arifOS. No data migration needed —
L4 is already canonical.

---

DITEMPA BUKAN DIBERI

#L5-DEPRECATION-2026-10-07
