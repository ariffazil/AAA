# FI-011 — Context Prune Clerk

> **DITEMPA BUKAN DIBERI** ⚒️ — Forged because every MCP tool call bloats the
> context window and the agent gets stupider every turn.
>
> **Author:** FI-008 Kimi Code (proposal for 2026-08-25)
> **Status:** DESIGN — not yet implemented. Awaiting 888_HOLD or
> FI-003/F1 cron-trigger to flip from design → on-demand FI.
>
> **Refs:**
> - `r/ClaudeCode` "MCP costs you money" — context-window inflation
> - `Chronicle MCP` — context-aware pruning precedent
> - Reddit consensus 2026-08-25 — graph-driven prune preferred over heuristic

---

## Why this FI exists

Every MCP tool response gets dumped into the agent's context window. Over
a long session, this dilutes attention — the LLM forgets earlier work
because later tool outputs pushed it out of the context. Reddit calls this
"context bloat".

Three responses in industry:
1. Compress blindly — risky, may strip critical context
2. Sliding window / compaction — already auto-fires in some harnesses
3. **Signal-driven prune** — only what graph says is relevant survives

We have a code graph (Phase 1). Graph says "for task X, files A/B/C matter,
files D/E/F don't". Use that.

---

## Hook point candidates

Two surfaces in the federation that pass context into a sub-agent:

| Hook | Path | What's passed | Invasiveness |
|------|------|---------------|--------------|
| **A. arifOS delegation** | `arifOS/arifosmcp/runtime/delegation_envelope.py` | signed envelope of allowed tools + parent context | LOW — additive: prune `parent_context` before attach |
| **B. A-FORGE ephemeral** | `A-FORGE/src/domain/containment/EphemeralGenesisRunner.ts` | bootstrap workspace + skill references | LOW — additive: prune bootstrap list before fork |

**Recommendation:** start with **A** (arifOS delegation), because:
- delegation_envelope already exists, signed, governed
- F11 audit trail is built-in (every delegation emits a receipt)
- Smaller blast radius — touches one module, doesn't fork ephemeral workspace

---

## Graph signals to use

Live bridge at `127.0.0.1:18922`, verbs:

```
POST /blast        {path|symbol, depth?}    → affected files
POST /dependents   {symbol}                 → callers
POST /symbols      {path}                   → definitions
POST /search       {name, kind?, limit?}    → find by name
POST /cross        {symbol}                 → cross-repo callers/importers
```

**Heuristic for prune:**

1. Tokenize task description (regex: snake_case + CamelCase identifiers)
2. For each token, query `/search name:<token>` → list of candidate symbols
3. For each candidate, query `/blast symbol:<sym> depth:1` → blast radius
4. Union: `relevant_set = ⋃ blast_radius per candidate`
5. Final: `kept = candidate_files ∩ relevant_set` + directly-mentioned files

**Token budget guard:**

- Default `MAX_CONTEXT_TOKENS = 8000`
- If `len(kept)` × avg(file_tokens=350) > MAX → keep files with shortest blast-distance
- Drop files with no blast distance AND no symbol match

---

## F11 receipt shape (per prune)

```json
{
  "task_hash": "sha256...",
  "input_files": 42,
  "kept_files": 11,
  "dropped_files": 31,
  "estimated_tokens_saved": 10850,
  "graph_queries": [
    {"verb": "search", "name": "arif_judge", "matches": 5},
    {"verb": "blast", "symbol": "arif_judge", "depth": 1, "affected": 7}
  ],
  "confidence": 0.85,
  "receipt_id": "pr-..."
}
```

Writes to `arifFlow :7073/ingest` (per GOTONG_ROYONG.md).

---

## Implementation path

```
Phase 1 (THIS PROPOSAL): design + reference impl
  └─ /root/AAA/graph/FI-011-DESIGN.md     [THIS FILE]
  └─ /root/AAA/graph/prune_context.py    [reference impl, ~120 lines]

Phase 2 (after approval): wire as on-demand FI
  └─ Register FI-011 in /root/AAA/governance/GOTONG_ROYONG.md
  └─ Hook into arifOS delegation_envelope (additive patch)
  └─ F11 audit + receipts

Phase 3 (after proven): promote to cron
  └─ FI-011 cron: nightly context hygiene sweep on long sessions
```

---

## Falsification criteria (when to abandon)

- If prune changes don't measurably reduce token spend (savings <10% of
  unpruned baseline over 10 sessions) → heuristic is wrong, redesign
- If prune drops files that turn out to be needed (3+ false negatives per
  50 sessions) → safety budget too aggressive, raise
- If graph_bridge unreachable → fallback to no-prune (pass full context)
  + log a F11 receipt warning

---

## Open questions for 888_APEX

1. **Token estimator** — how do we estimate per-file tokens without
   reading every file? Use `wc -w * 1.3` approximation? Cache by sha?
2. **Task tokenization** — is regex on snake/CamelCase enough, or do we
   want embeddings + a small in-process model?
3. **Cache strategy** — should prune results be cached keyed by
   `(task_hash, files_hash)` so identical redos skip the graph?
4. **Multi-tenant scope** — does this prune happen per-session or
   per-warga? (per-session is safer; per-warga faster)
5. **F11 audit threshold** — every prune or only when tokens saved > N?