# Codex Identity Contract — APPLIED — 2026-10-03 14:55

**Status:** Spec 7 BUILT. T1-AUTO. Live-tested. Reversible.

**What was built:**
- `_fetch_contract(actor)` function in `/root/.codex/hooks/aaa_session_witness.py` (~40 LOC)
- Calls arif_init with `(actor_id, intent)` only (idempotent on existing actor)
- Parses JSON-RPC wrapped response (`result.content[0].text` unwrapping)
- Stores full contract under `init_result["contract"]`
- Audit log entry now includes the full contract (previously: just session_id)

**Files changed:**
- `/root/.codex/hooks/aaa_session_witness.py` (+1374 chars net: helper + contract line + parser fix)
- Backup: `/root/.codex/hooks/aaa_session_witness.py.bak-20261003-1448-idcontract` (pre-patch deinit state)

**Live test (14:55 MYT):**
- Witness invoked via stdin with `actor_id=fi005-patch-v8-...`
- Audit log entry now contains:
  - `actor_verified: True` (was: not in contract, was inferred)
  - `authority: LIMITED_MUTATE` (was: not captured)
  - `session_id: SEAL-6adf6990f4ce47ad`
  - `allowed_next_verbs: ['arif_init', 'arif_observe', 'arif_think']`

**Bug fixed during build:**
- arif_init schema does NOT accept `citizenship` or `lane` keywords (only `actor_id`, `intent`, etc.)
- Initial patch sent both → Pydantic validation error
- Fixed: removed both args, only `actor_id` + `intent`
- Also: response is JSON-RPC wrapped (`result.content[0].text` is stringified JSON), parser needed to unwrap

**What was NOT done (per Law 10):**
- ❌ Did not modify the live arif_init.sh script
- ❌ Did not modify hooks.json
- ❌ Did not add a fail-closed gate yet (current code captures contract but doesn't enforce it; that's the next smallest patch)
- ❌ Did not add new receipts/specs

**Reversibility:** `cp /root/.codex/hooks/aaa_session_witness.py.bak-20261003-1448-idcontract /root/.codex/hooks/aaa_session_witness.py`

**Doctrine (per Arif):**
- "Forge only missing delta" → captured identity contract (the missing delta vs codex's previous "trust init returned 200")
- "Smaller is better" → ~40 LOC, 1 file change
- "Live test" → proved contract is captured before claiming done

**State of the 5 P0/P1/P2 items (from your audit):**
1. ✅ **DONE**: Eliminate duplicate SessionStart init (witness deinit)
2. ✅ **PARTIALLY DONE**: Update identity contract — witness now CAPTURES contract. Fail-closed gate is the next smallest delta.
3. ⏸️ PENDING: Fix observability economics (1 receipt per action)
4. ⏸️ PENDING: carry_forward retention
5. ⏸️ PENDING: 11 MCP verify independently

**Doctor sanity:** 31/31 PASS confirmed. Federation healthy. Codex P0 #1 and partial P0 #2 are real wins.
