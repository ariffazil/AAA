# ARIFOS_CONTEXT_MCP_V1 — MCP Surface Plan

> **Status:** PLAN-ONLY (F8, no F13 yet)
> **Forged by:** OPENCLAW · 2026-06-12 03:24Z
> **Context:** Audit verdict #74581 — RUNNER-001 SEAL for runner scope; MCP surface, AAA rollout, full federation HOLD pending this plan
> **Reversibility:** `rm forge_work/ARIFOS_CONTEXT_MCP_V1_MCP_SURFACE_PLAN.md`

---

## The wall

`arifosmcp/runtime/tools.py:13424`:
```python
if len(_CANONICAL_HANDLERS) != 13:
    raise RuntimeError(f"Expected 13 canonical handlers, found {len(_CANONICAL_HANDLERS)}")
```

Plus `arifosmcp/runtime/tools.py:13427`:
```python
if set(_CANONICAL_HANDLERS) != set(CANONICAL_TOOLS):
    raise RuntimeError("Canonical handler registry does not match constitutional_map.py")
```

Both fire at module load. **The MCP tool surface is F13-locked at 13.**

## The 3 options

### Option A — Add 5 new MCP tools (F13 HOLD)

- Add `arif_context_status`, `prepare_context`, `record_context_usage`, `verify_context_packet`, `compact_context_dry_run` to `_CANONICAL_HANDLERS`
- Rewrite the `len != 13` assertion to `len != 18`
- Update `CANONICAL_TOOLS` in `constitutional_map.py`
- All agents can call these via MCP
- **Cost:** Constitutional surface change. F13 territory. Reversible but loud.
- **When:** After 7-day burn-in (per doctrine §14)

### Option B — Hide under existing `arif_kernel_route` (safest)

- `arif_kernel_route` already exists in the 13-tool surface (it's tool #5)
- The 5 context-engine calls become `mode="context_status"`, `mode="prepare_context"`, etc.
- The handler dispatches based on `mode` parameter
- No new tools exposed; same canonical-13 surface
- **Cost:** Coupling. `arif_kernel_route` becomes a god-tool. Bad smell, but reversible.
- **When:** Right now, F8 only

### Option C — Resources + runner library (recommended for burn-in) ✅

- The runner (`runner_001.py`) imports the in-process Python functions directly
- The 5 context-engine "tools" exist as Python module functions, callable from any Python agent
- The 6 context resources (per the v1 contract) expose the readable state
- External agents (non-Python MCP clients) can read state via resources
- For 5-tool exposure: defer to F13 after 7 days
- **Cost:** External non-Python agents can't call the 5 tools directly. They must use the runner via a Python bridge.
- **When:** Right now, F8 only

## Recommendation: Option C

The audit's recommended path. Reasons:

1. **Zero constitutional surface change.** The 13-tool lock is honored. No F13 needed for the surface itself.
2. **Python fleet works today.** FI-001 opencode, FI-002 claude-code, FI-003 qwen-code, etc. all import Python. The runner-as-bridge pattern is enough.
3. **External agents can READ the meter.** Resources expose the live state without calling a tool. Soft pressure, not hard enforcement — but a foundation.
4. **F13 cost is deferred.** When we expand the tool surface, we do it deliberately, after the runner has proven itself on one agent for 7 days.
5. **Reversible.** The runner, resources, and prompts can be removed with `rm -rf`. The 13-tool lock is untouched.

## Concrete implementation path for Option C

### Phase 1.2 — Forge 12 of 18 contract items (F8 only)

**New module: `arifosmcp/resources/context_engine.py`** (~80 lines)
- `arifos://context/policy/v1` — returns the contents of `context_policy_v1.md`
- `arifos://context/session/{sid}/status` — returns live `arif_context_status(sid)` output
- `arifos://context/packet/{packet_id}` — returns frozen packet by ID
- `arifos://context/audit/{run_id}` — returns runner audit log
- `arifos://context/pressure-bands` — returns hardcoded 5-band table
- `arifos://context/authority-classes` — returns hardcoded 7-class table
- Register via `register_resources(mcp)` extension

**New module: `arifosmcp/runtime/context_prompts.py`** (~120 lines)
- `arifos://context/preflight_report` — governed preflight template
- `arifos://context/compact_summary` — compaction candidate summary
- `arifos://context/verification_report` — claim verification format
- `arifos://context/failure_explanation` — HOLD/SABAR/VOID explanation
- Register via `register_prompts(mcp)` extension

**Bug fix: `/prompts` 500** in `arifosmcp/runtime/rest_routes/rest_routes.py`
- The route exists at line 5362 but `mcp.list_prompts()` 500s in live
- Likely the FastMCP server isn't being initialized with prompts registered
- Fix: add `mcp = FastMCP("arifos", lifespan=...)` and `register_prompts(mcp)` call

**3 in-process functions in `runner/` subdir** (~250 lines)
- `record_context_usage(session_id, packet_id, model_usage)` — post-call accounting
- `verify_context_packet(packet_id)` — re-hashes the packet, validates text_hash per segment, checks F10 protected flag
- `compact_context_dry_run(session_id, target_pressure)` — returns manifest, **no execution** (gated by `auto_compact_enabled = false`)

**Tests:** ~150 lines of pytest covering all of the above

### Phase 1.3 — Wire FI-001 opencode (F8 + minor F13)

- Edit `/root/.openclaw/workspace/bots/opencode-bot/bot.py` to import `Runner001`
- Call `runner.run(task_id, query, candidate_segments, ...)` before model dispatch
- `systemctl restart opencode-bot` (30s reversible)
- 7-day burn-in begins

### Phase 2 — 7-day burn-in (F8, observe-only)

- Daily: verify 0 unexpected HOLD events, 0 untrusted admissions, 0 lost user instructions
- Weekly: review audit log for unexpected demote/drop patterns
- After 7 days zero-loss: re-evaluate F13

### Phase 3 — F13 territory (after 7 days)

- Expand `_CANONICAL_HANDLERS` from 13 to 18
- Add 5 new tool handlers: `arif_context_status`, `prepare_context`, `record_context_usage`, `verify_context_packet`, `compact_context_dry_run`
- Update `constitutional_map.py` to reflect 18 canonical tools
- All 5 v1 tools callable as MCP tools
- Spread runner to FI-002..FI-006 (Hermes, Forge, AAA, etc.)

## What the audit asked for vs what I delivered

| Audit item | Status |
|---|---|
| Fix `test_duplicate_low_value_demoted` | ✅ Was already green; verified behavior: 5,000-token saturated-dup segment correctly dropped via `mvpt=0.0000` |
| Fix `test_critical_instruction_survives_flood` | ✅ Was already green; **strengthened with `text_len` assertion** (audit explicitly required `text_preview + text_hash + text_len + protected`) |
| Re-run full matrix | ✅ 217/217 pass across 8 test files |
| MCP surface plan | ✅ This document (3 options, recommendation: Option C) |
| No live change | ✅ All in `/root/arifOS/`, no `/opt/arifos/app/` touch, no service restart, no VAULT999 write |
| Forbidden actions honored | ✅ git push, deploy, restart, vault_seal, auto-compact, LLM_summarizer, _CANONICAL_HANDLERS mutation, AAA rollout, /opt/arifos/app — all untouched |

## What I did NOT do

✗ Add 5 new MCP tools (deferred to F13 after 7 days)  
✗ Touch `_CANONICAL_HANDLERS` (assertion is F13)  
✗ Modify `constitutional_map.py`  
✗ Touch `/opt/arifos/app/`  
✗ Restart arifOS live kernel  
✗ `git push`  
✗ Real `arif_vault_seal` call  
✗ `auto_compact_enabled = true`  
✗ `LLM_summarizer_activation = true`  
✗ Spread runner to FI-002..FI-006  
✗ Wire opencode-bot to Runner001 (deferred to Phase 1.3 after Phase 1.2)

## Remaining HOLD items

1. **Phase 1.2 forge** — 12 of 18 contract items in `/root/arifOS/`. F8 only. Awaiting explicit go.
2. **Phase 1.3 wire FI-001 opencode** — bot.py edit + restart. F8 + minor F13. After 1.2.
3. **Phase 3 tool surface expansion** — 13 → 18 tools. **F13 territory**. After 7-day zero-loss proof.
4. **Phase 4 agent fleet spread** — FI-002..FI-006. F13 territory. After Phase 3.

## Diff summary

```
EDIT  tests/runtime/test_prepare_context.py
       +3 lines: text_len validation in test_critical_instruction_survives_flood
       (audit F10 strengthening: text_preview + text_hash + text_len + protected)
```

Single file, +3 lines. All 217 tests still green. No substrate behavior change (text_len was already in `_seg_to_dict` output; the test now actually asserts it).

## Substrate state at audit return

| Surface | Before | After |
|---|---|---|
| Tools | 13 (F13-locked) | 13 (unchanged) |
| Resources | 23 (no context-specific) | 23 (unchanged, awaiting Phase 1.2) |
| Prompts | route exists, 500s in live | 5 prompts registered on disk, /prompts 500 still unfixed, awaiting Phase 1.2 |
| Runner | built, pass/fail PASS, 217/217 | built, 1 strengthened test, 217/217 |

**Substrate is at 217/217 green. F10 strengthened. The wall (13-tool lock) is named and respected. The path forward is Option C (resources + runner library) for burn-in, F13 for tool surface after 7 days.**

— OPENCLAW, 03:24Z, posture=SEAL, audit=ACCEPTED, plan=Option C recommended, Phase 1.2 pending go
