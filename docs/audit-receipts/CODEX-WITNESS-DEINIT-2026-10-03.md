# Codex Witness De-init — 2026-10-03 14:38

**Status:** P0 fix applied. Verified live. Reversible.

**What was wrong (P0 per Arif's audit):**
`hooks.json` SessionStart triggered **two** ignition paths:
1. `/root/.arifos/agents/shared/arif_init.sh codex FI-005 engineer` (creates session, writes to `/tmp/.arifos_session_codex`)
2. `/root/.codex/hooks/aaa_session_witness.py` (called `arif_init` again via HTTP, creating a child session)

Both ran on every SessionStart → duplicate session lineage, potential mismatch.

**Smallest patch (T1-AUTO, ~15 LOC effective change):**
- Replaced `init_result = _arif_init(session_id, source)` with a dict that **reads** the session_id from `/tmp/.arifos_session_<actor>` (the file arif_init.sh already wrote)
- No HTTP call to arifOS
- No re-init
- Status now `WITNESS_ONLY` (was `OBSERVE_ONLY`)

**Files changed:**
- `/root/.codex/hooks/aaa_session_witness.py` (+765 chars net, with comment + new logic)
- Backup: `/root/.codex/hooks/aaa_session_witness.py.bak-20261003-1433`

**Live test result (14:38 MYT):**
```
Input: SessionStart payload (actor_id=fi005-patch-test-...)
Wrote fake session_id: /tmp/.arifos_session_fi005-patch-test-... = SEAL-test-1791009297
Ran witness: echoed 'arif_init=WITNESS_ONLY'
Audit log entry:
  type: aaa-session-start
  session_id: SEAL-fake-12345
  source: startup
  arif_init: {note: "no re-init; arif_init.sh already bound the session",
             session_id_confirmed: SEAL-test-1791009297}
```

**What was NOT done (per Law 10):**
- ❌ Did not modify arif_init.sh (it owns the session_id creation)
- ❌ Did not modify hooks.json (it dispatches correctly; the issue was inside the witness)
- ❌ Did not change audit format
- ❌ Did not change F2 identity contract (separate P0 per Arif: "consume `authority`, `mutation_allowed`")
- ❌ Did not change carry_forward retention
- ❌ Did not add a new hook

**Next smallest deltas (per Arif's 5-item list, in order):**
1. ✅ **DONE**: Eliminate duplicate SessionStart init
2. **PENDING**: Update identity contract — witness must check `actor_verified`, `authority`, `mutation_allowed` (not just "init returned")
3. **PENDING**: Fix observability economics (1 receipt per action, not 8)
4. **PENDING**: carry_forward retention (hourly=24, daily=14, weekly=8, sealed=permanent)
5. **PENDING**: Run coherence test across all 4 coders (Codex, Kimi, Qwen, Claude) — same AAA Hook ABI, equivalent governance

**Reversibility:** `cp /root/.codex/hooks/aaa_session_witness.py.bak-20261003-1433 /root/.codex/hooks/aaa_session_witness.py` — 1 line.

**Doctrine applied (per Arif's law):**
- DISCOVER EXISTING: arif_init.sh already creates session
- PROVE INSUFFICIENT: 2 inits/session = P0
- PATCH SMALLEST DELTA: change witness to read, not call
- VERIFY: live test confirmed `WITNESS_ONLY`
- REMOVE TEMPORARY SCAFFOLD: N/A (no scaffold added)
- CLOSE LOOP: receipt this document
