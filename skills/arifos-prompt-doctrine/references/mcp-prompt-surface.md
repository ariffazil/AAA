# arifOS MCP Prompt Surface — Map & Drift Notes (audited 2026-08-07)

The kernel (:8088) serves MCP prompts that frame agentic work. They are the kernel-side
sibling of the SOUL/AGENTS prompt stack. Audited 2026-08-07 (Arif: "Evaluate arifOS MCP
/init to /seal prompts").

## Registration (file map)

| Layer | File | Role |
|---|---|---|
| Canonical zen sigils + bootstrap | `arifosmcp/runtime/fastmcp_ext/prompts.py` → `register_arifos_prompts()` | SOURCE of truth for prompt text |
| Legacy numeric aliases | `arifosmcp/prompts/__init__.py` → `register_prompts()` | Delegates to zen module, then re-registers deprecated aliases |
| Spec/archive (NOT live) | `arifosmcp/specs/prompt_specs.py` | `_HISTORICAL_PROMPT_SPECS` reference-only |
| Mind parallel surface | `arifosmcp/runtime/mind_mcp.py` | FastMCP `arifOS-Mind` — `arif_think`, `arif_mind_*` tools+prompts |
| Tool enforcement | `arifosmcp/runtime/tools.py` (~26k lines) | `TOOL_PURPOSE_CONTRACTS`, verdict-loop gate |

## Canonical surface (12 intended)

- 🌱 BOOT (PRE_LOOP) — depth='full' loads `/root/AAA/prompts/INIT.md`
- 🌊 WITNESS (111_SENSE) → 🧠 REASON (333_REASON) → ⚖ MARUAH (555_CRITIQUE)
- 🔍 PREFLIGHT (PRE_OPERATION) → 🔒 JUDGE (888_JUDGE) → 🔥 FORGE (777_FORGE) → 💎 SEAL (999_SEAL)
- 🌀 SABAR (000_LOOP orchestrator, depth=stage|auto)
- 📜 REPLY (POST_LOOP)
- /init (BOOT) — loads `/root/.config/opencode/command/init.md` (v5.0 collapsed, 4-step)
- /seal (CLOSE) — loads `/root/.config/opencode/command/seal.md` (v5.0 collapsed, 5-step, Lane A/B/C)

Loop: WITNESS → REASON → MARUAH → JUDGE → FORGE → SEAL. Floor references per stage are
tight and correct (WITNESS: F2,F3,F9,F12; REASON: F2,F7,F8; MARUAH: F5,F6,F9,F10).

## Legacy aliases (surface noise)

Live `prompts/list` returns ~20 items when design intent is 12:
`111_sense, 333_reason, 555_critique, 888_judge, 777_forge, 999_seal,
recursive_governed_loop, arif_init_prompt_v3` (plus `arif_init_prompt`,
`constitutional_pre_flight`, `agi_reply_protocol_v3` in the CANONICAL_PROMPTS tuple).
Removal epochs: 2026-08-16 (arif_init_prompt / constitutional_pre_flight /
agi_reply_protocol_v3) and 2026-09-16 (numeric aliases). Verify live surface before
assuming any alias is actually gone — several were "removed" in code comments yet still
registered.

## Known drift (verified 2026-08-07)

1. **Two loops disagree**: AGENTS.md preaches 8 verbs (init→observe→think→route→memory→
   judge→forge→seal); the zen prompt loop is 6 stages. INIT/MEMORY live in bootstrap;
   ROUTE absorbed into REASON. An agent following AGENTS.md verbs will not follow the
   zen sequence, and vice versa.
2. **INIT.md fork**: 🌱 BOOT depth=full loads `/root/AAA/prompts/INIT.md` (301 lines,
   older ceremony); /init loads `/root/.config/opencode/command/init.md` (175 lines,
   v5.0 collapsed 4-step). Two different init documents on one surface.
3. **Prompt→tool impedance gap**: prompts instruct agents ("call arif_observe with
   intent='…'") as advisory text; tools.py gates enforce `VERDICT_LOOP_REQUIRED` blocks
   on observe/think/route/memory outside a verdict loop. Prompt text and code
   enforcement can contradict — no schema cross-check at registration time.
4. **Parallel arif_think**: registered in both mind_mcp.py (FastMCP arifOS-Mind) and
   tools.py CORE surface. tools.py `TOOL_PURPOSE_CONTRACTS` still labels the surface
   "CORE 7" while AGENTS.md names 8 canonical verbs.
5. **seal fork**: 💎 SEAL (SABAR stage 6, provenance-chain prep) vs /seal (operational
   5-step close with Lane A/B/C records) — different lane logic, same "seal" word.
   Agents must know which is being invoked.

## Live probe (no auth needed for prompts/list)

```bash
curl -sN -X POST http://127.0.0.1:8088/mcp \
  -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"prompts/list","params":{}}'
# swap method for "tools/list" to audit the tool surface
```

Kernel `/health` confirms `mcp_protocol_version` (2025-11-25) and release name.

## Edit rules

- Canonical prompt text lives in `fastmcp_ext/prompts.py` (source, editable) — NOT in
  `/root/AAA/instructions/` fragments (those render AGENTS.md/CLAUDE.md only).
- Operational /init & /seal docs: `/root/.config/opencode/command/{init,seal}.md`
  (OpenCode command format, frontmatter `agent: 333-AGI`, `forged:` date stamps).
- Backup before editing prompt text (`/root/.local/share/arifos/snapshots/`), same
  discipline as SOUL surgery.
