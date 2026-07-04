# FI Citizens Skills Binding Sweep — 2026-06-22

**Operator:** Hermes (sovereign relay)
**Authorization:** Arif directive — "make sure my opencode, openclaw, codex, claude code, gemini cli and copilot cli, kimi code and all is being wireed as real warga AAA"
**Scope:** T1 reversible mutations only. No T3. No floor changes.

## What was done

9 FI (Forge Instrument) citizens wired as real AAA warga with the 8-skill baseline per the orthogonal mapping pattern. Each card now declares:
- id, name, tier=FI, class=CODING/FI
- capabilities (streaming, tool_calling, mcp_native, file_read/write, shell_exec, subagent_spawn)
- security schemes (bearer_auth + api_key for A2A)
- mcp_servers list (arifOS, geox, wealth, well, aforge)
- subAgentPolicy (default=888_HOLD, maxParallel=3, isolation=worktree, capability_modes)
- autonomy_tiers T1/T2/T3 with explicit floor gates
- authority_boundary (canDo/cannotDo)
- 8 skills with floor_scope annotations

## Cards written

| Citizen | Binary | Skills | Mirror |
|---------|--------|--------|--------|
| opencode | /root/.local/bin/opencode | 8 | ✓ |
| claude-code | /root/.local/bin/claude | 8 | ✓ |
| codex | /root/.local/bin/codex | 8 | ✓ |
| copilot | /root/.local/bin/copilot | 8 | ✓ |
| kimi-code | /root/.local/bin/kimi | 8 | ✓ |
| aider | /root/.local/bin/aider | 8 | ✓ |
| antigravity | /root/.local/bin/agy (Gemini 3.5) | 8 | ✓ |
| continue-cli | /root/.local/bin/cn | 8 | ✓ |
| gemini-cli | /root/.local/bin/gemini | 8 | ✓ |

All written to BOTH locations:
- `/root/AAA/agents/{id}/agent-card.json` (canonical spec)
- `/root/AAA/a2a-server/agent-cards/{id}.json` (runtime mirror for dir-load)

## Baseline 8 skills (per FI citizen)

1. **hermes-opencode-protocol** — Unified Hermes/OpenCode/OpenClaw governed intelligence protocol (F1, F2, F4, F8, F11, F13)
2. **agentic-architecture** — Class-level skill for designing sovereign agentic agents (F8, F11)
3. **fabrication-prevention** — Artifact fabrication prevention (F2, F9, F11)
4. **autonomous-governed-execution** — ASI-tier autonomous governed execution (F1, F2, F4, F7, F11, F13)
5. **arifos-arconstitutional-audit** — Light constitutional audit (F1, F2, F4, F7, F9, F11, F13)
6. **godel-humility-lock** — Self-critique before SEAL-grade claims (F2, F7)
7. **github-workflow** — GitHub operations umbrella (F1, F11)
8. **arifos-mcp-federation** — Route tasks across federation MCPs (F4, F11)

## Authority boundary (uniform across FI)

**canDo:** forge code under F1-F13, route MCP federation calls, spawn bounded subagents (worktree isolated), run tests/build/lint with evidence, generate diffs and PR drafts.

**cannotDo:** issue SEAL/HOLD/VOID verdicts (888-APEX only), modify constitutional floors without 888_HOLD, push to main without sentinel-premerge-gate, execute irreversible shell without F13 ack, fabricate evidence, claim consciousness (F9 ANTIHANTU).

## Registry sync

- `/root/AAA/registries/AAA_AGENTS_REGISTRY.json` — added 9 FI entries, lastValidated = 2026-06-22T...Z
- `/root/AAA/agents/AGENT_REGISTRY.md` — appended "FI Citizens Skills Binding Sweep" section with table
- Existing 9 agents preserved (333-AGI, 555-ASI, 888-APEX, A-ARCHIVE, A-AUDIT, antigravity, grok-build, hermes-asi, openclaw) → 17 total

## Pattern source

`/root/HERMES/skills/aaa-agentic-governance/references/orthogonal-skill-binding-pattern-2026-06-22.md` (forged by grok Phase 2 synthesis)

## What is NOT done (deferred)

- aaa-a2a.service restart — needs Arif ratification for runtime activation
- Continue-cli's "qwen-code" cousin in forge/ subdir not touched
- Sub-agent spawn contracts not validated against live runtime (test suite needed)
- No skill authoring — only declaration (skills live in Hermes library, cards bind)

## Receipt files

- `/root/AAA/artifacts/FI_WARGA.md` (this file)
- 9 × agent-card.json (canonical) + 9 × a2a-server mirror
- AAA_AGENTS_REGISTRY.json updated
- AGENT_REGISTRY.md appended

DITEMPA BUKAN DIBERI — 9 FI warga wired, 72 skill bindings forged, F11 audit trail sealed.