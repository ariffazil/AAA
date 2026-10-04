# FED ↔ A2A Model-Metadata Drift (2026-08-07)

## The problem

Three layers — LiteLLM proxy (FED), AAA A2A registry, OpenCode config — disagree on what model powers what agent. Runtime works because OpenCode's inline `litellm-federation/*` references bypass the broken A2A declarations. The A2A control plane is blind.

## Live state (2026-08-07 11:36 MYT)

| FED Alias | Backend (primary) | A2A binding | AGENTS_UNIFIED | Drift |
|---|---|---|---|---|
| `hermes-asi` | MiMo V2.5 (Xiaomi) | `remote-agent` → hermes-agent | — | ✅ aligned |
| `openclaw` | MiniMax M3 | `openclaw-bridge` → openclaw-gateway | — | ✅ aligned |
| `opencode` | DeepSeek V4 Pro | `local-cli` → opencode | `FI-001` → deepseek/deepseek-v4-pro | ✅ aligned |
| `agi-333` | DeepSeek V4 Pro | `virtual-agent` → arifos-kernel | `333-AGI` no model field | ⚠️ runtime works, A2A blind |
| `asi-555` | DeepSeek V4 Flash | `virtual-agent` → hermes-agent | `555-ASI` no model field | ⚠️ runtime works, A2A blind |
| `apex-888` | MiniMax M3 | `virtual-agent` → arifos-kernel | `888-APEX` no model field | ⚠️ runtime works, A2A blind |
| `asi-555-audio` | MiMo V2.5 | ❌ not registered | — | ❌ phantom |
| `asi-555-video` | MiMo V2.5 | ❌ not registered | — | ❌ phantom |
| `dispatch` | MiMo V2.5 Pro | ❌ not registered | — | ❌ phantom (OpenCode routes direct kimi, bypasses FED) |

## Why runtime succeeded despite drift

OpenCode's `agent.333-AGI.model = "litellm-federation/agi-333"` sends the request through the proxy cascade. The proxy resolves `agi-333` → `openai/deepseek-v4-pro @ api.deepseek.com` and returns a response. OpenCode never queries the A2A registry for model info — it reads its own `opencode.json` directly.

A2A is only consulted by agents doing inter-agent discovery (who has what capability), not by agents making API calls. So the A2A blindness only matters when:
1. A new agent tries to discover `333-AGI`'s model capability via A2A
2. The AAA control-plane UI tries to display federation routing
3. A governance gate asks "what model powers this agent?" — A2A can't answer

## Root cause

OpenCode subagent models were defined in `litellm-config.yaml` (FED) and `opencode.json` (consumer), but never backfilled into `AAA/a2a/registry/agents.yaml` or `AAA/registries/AGENTS_UNIFIED.yaml`. The two AAA files predated the FED LiteLLM rewrite (2026-08-04 → 2026-08-05) and were not regenerated.

## Fix pattern

1. **Canonical binding map:** `AAA/federation/federation-model-bindings.yaml` — one file defines `agent_id → fed_alias → primary_model → provider → consumers`. All 5 consumer SOTs reference this file; no inline model strings.
2. **Backfill A2A registry:** add `fed_alias:`, `primary_model:`, `model_source:` fields to every agent entry in `AAA/a2a/registry/agents.yaml`.
3. **Drift gate:** `AAA/scripts/aaa_a2a_sync.py` — reads bindings, reads A2A, hits live `/model/info`, prints 3-row drift table, exit 1 on mismatch. Wire into `aaa-drift-check.py`.
4. **Plan:** `/root/HERMES/plans/2026-08-07_114400-fed-aaa-a2a-zen.md` — full 4-phase plan, T1 reversible, ~2h estimated.

## Key files

| File | Role |
|---|---|
| `AAA/federation/federation-model-bindings.yaml` | NEW canonical SOT (to be created) |
| `AAA/a2a/registry/agents.yaml` | A2A operational registry (to be backfilled) |
| `AAA/registries/AGENTS_UNIFIED.yaml` | Identity lanes + forge instruments (to be backfilled) |
| `A-FORGE/litellm-config.yaml` | LiteLLM proxy cascade definitions (reference, not edited in this fix) |
| `/root/.config/opencode/opencode.json` | OpenCode agent config (consumer, reads FED aliases) |
| `/root/.hermes/config.yaml` | Hermes config (consumer, reads FED aliases) |
| `AAA/scripts/aaa_a2a_sync.py` | NEW drift-gate script (to be created) |
| `/root/HERMES/plans/2026-08-07_114400-fed-aaa-a2a-zen.md` | Implementation plan |
