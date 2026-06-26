# Session: 2026-06-12 03:18Z — ARIFOS_CONTEXT_MCP_V1 sealed

## What Arif said (#74569, 02:59:59 UTC)
"The clean answer is: Agent context management is not only one MCP tool. In arifOS MCP it should be a small subsystem using Tools + Resources + Prompts, with the runner enforcing the flow."

He laid out the 18-item v1 contract: 5 tools, 6 resources, 4 prompts, 3 runner guards. Named the agent fleet (FI-001..FI-006). Said: "the next real forge is not more theory. It is: ARIFOS_CONTEXT_MCP_V1 + RUNNER-001."

## What I did
1. **Sealed the v1 contract** as doctrine: `forge_work/ARIFOS_CONTEXT_MCP_V1.md`. 12 sections. 18 items mapped. F-floor per item. Reversibility markers. Phase ledger.
2. **Final architecture sentence captured:**
   > In arifOS MCP, context management is a governed service: tools compute it, resources expose it, prompts standardize it, and the runner enforces it.
3. **Forge plan committed:**
   - 1.1 Seal contract ✅ (this session)
   - 1.2 Forge 12 of 18 in-process (F8 only, all untracked)
   - 1.3 Wire FI-001 opencode (F8 + minor F13, 30s reversible)
   - 2 7-day burn-in (F8, observe-only)
   - 3 Expose 5 tools + spread to FI-002..FI-006 (F13, after 7 days)

## Key substrate facts
- 13-tool lock: real, at `arifosmcp/runtime/tools.py:13424`
  - Adding the 5 v1 tools means rewriting `if len(_CANONICAL_HANDLERS) != 13: raise RuntimeError`
  - This is the only wall to the MCP tool surface
- Resources: 23 already exposed via REST + MCP, 0 context-specific. 6 to add.
- Prompts: route exists at `/prompts`, currently 500s. 5 prompts in `arifosmcp/runtime/prompts.py` (000_init, 111_agi, 444_asi, 888_apex, 999_seal). Need to fix live 500 + add 4 context prompts.
- Runner: built, pass/fail PASS, 217/217 tests. 3 guards in `Runner001.run` (steps 1-4, 7, 8).

## The F8 / F13 boundary
- F8 forgeable (12 of 18): 6 resources, 4 prompts, 3 in-process fns, /prompts 500 fix, runner wire
- F13 locked (5 of 18): expose the 5 in-process fns as MCP tools (rewrites 13-tool assertion)
- F13 territory (separate): touch /opt/arifos/app/, restart arifOS live kernel, git push, real VAULT999 seal, auto-compact enable, LLM summarizer activation

## The runner-as-bridge pattern
- Runner imports in-process fns (`prepare_context`, `arif_context_status`)
- For Python agents (opencode-bot, hermes-asi-gateway, AAA reactor): runner enforces the 11-step flow without needing MCP tool surface
- For external agents (non-Python MCP clients): need F13 to expose the 5 tools
- This means Phase 1.2-1.3 is F8-only and works for the Python fleet members

## Agent fleet (FI = Federation Identity)
- FI-001 opencode — opencode-bot, /root/.openclaw/workspace/bots/opencode-bot/bot.py
- FI-002 claude-code — Phase 4 spread
- FI-003 qwen-code — Phase 4 spread
- FI-004 gemini-cli — Phase 4 spread
- FI-005 codex-cli — Phase 4 spread
- FI-006 copilot-cli — Phase 4 spread

## Reversibility
- Phase 1.1: `rm forge_work/ARIFOS_CONTEXT_MCP_V1.md`
- Phase 1.2: `rm -rf` the new context_engine modules (all untracked)
- Phase 1.3: restore bot.py + `systemctl restart opencode-bot` (30s)
- VAULT999 unchanged, arifOS service unchanged, no /opt/arifos/app/ touch

## Forbidden actions honored
✗ auto-compact enable
✗ LLM summarizer activation
✗ all-agent rollout (Phase 4 only after 7 days)
✗ deploy/restart (only minor restart of opencode-bot in 1.3, not arifOS live kernel)
✗ remote push
✗ real VAULT999 seal
✗ /opt/arifos/app/ touch

## Carry-forward
1. Phase 1.2 next: 6 context resources, 4 context prompts, fix /prompts 500, 3 in-process fns (record_context_usage, verify_context_packet, compact_context_dry_run)
2. Phase 1.3 after 1.2: edit opencode-bot/bot.py to import Runner001, restart opencode-bot
3. Phase 2: 7-day burn-in
4. Phase 3 (F13): expose 5 tools + spread to FI-002..FI-006

## Test count
- 217 passed, 0 failed (8 test files)
- +2 substrate bugs that were pre-existing at 02:45Z are now fixed in parallel
- 34 net new tests (19 runner + 15 pass/fail)
