# L5 (Graphiti) Layer Deprecation — Federation Memory Contract Amendment

> **Status:** F13_RATIFIED_CANON · Tier A · 2026-10-07 (TURN 123)
> **Authority:** F13 SOVEREIGN via TURN 123 (option 2 chosen: deprecate)
> **Amends:**  §3 (Three-Leg Federation Write)
> **Decision trace:** 
> **Ratifikator:** Codex CLI (FI-005)
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
The *write path* through  is now
**3-leg → 2-leg**: L3 (Qdrant) and L4 (Supabase Postgres) are canonical.
L5 is **advisory** and may be skipped without alarm.

## 1 · The amendment

| Before | After |
|---|---|
| 3-leg fan-out: L3 (Qdrant) + L4 (Supabase) + L5 (Graphiti) | **2-leg canonical fan-out: L3 (Qdrant) + L4 (Supabase)** |
| L5 status field: queued / skipped / error | L5 status field deprecated; replaced by graph_tier: disabled |
|  requires L5 | L5 absence no longer DEGRADED — only L3+L4 matter for stored=true |
|  writes to L4 only (already true) | Unchanged |

## 2 · Migration of existing L5-queued rows

Any rows with  (pre-deprecation) **remain in L4 as
canonical** — the L4 row is the source of truth, not the L5 queue.

A one-shot cleanup task () is added in MOVE 3 to
flush any pre-deprecation queue to the L4-only state, and stamp a
 column on those rows.

## 3 · Re-enable path (if F13 ever reverses)

Reversibility is preserved. The re-enable path is:
1. F13 ratifies  (single file).
2. The patch flips  default back to .
3. The bridge () wakes the worker.
4. A 3-leg fan-out is restored.

This single file IS the deprecation flag. Search this file in canon to
verify deprecation is in effect.

## 4 · What is NOT changed

-  in  (line 869 etc.) is an **agency
  level** label, not the Graphiti layer. Untouched. Renaming it is a
  separate decision (out of scope; L5 in agency levels is unrelated).
- FalkorDB + graphiti-mcp containers stay running for read-only queries
  (legacy entities, 888-injected Cypher).
- The 6-Layer Atlas (L1..L6) in the Federation Memory Contract remains —
  L5 is still in the atlas, but its *write path* is now optional.

## 5 · Falsifiability

1. 
   must NOT appear in *new* post-deprecation writes (allow 0 in test fixtures).
2.  must succeed with
    based on L3+L4 only.
3.  may stay up (read-only) but
    is no longer load-bearing for memory writes.

---

DITEMPA BUKAN DIBERI

#L5-DEPRECATION-2026-10-07
