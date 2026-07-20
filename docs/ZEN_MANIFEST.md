# 🧘 ZEN MANIFEST — arifOS Federation Aligned State

> **SOT:** 2026-07-20T00:37Z | **Session:** AAA Full Alignment
> **AUTOPILOT:** ON | **HITL:** OFF (digital MUBAH)
> **Single source of truth for any agent waking up in this federation.**

---

## Agents (8 — all AUTOPILOT ON)

| Agent | Model | Fallback | AGENTS.md | MCPs |
|-------|-------|----------|-----------|------|
| Copilot CLI | deepseek-v4-pro | TokenRouter | /root/.arifos/agents/copilot/ | 15 |
| Claude Code | deepseek-v4-pro | TR | /root/AAA/CLAUDE.md | 20 |
| Codex CLI | gpt-5.6-sol | TR | /root/.codex/AGENTS.md | 9 |
| Kimi Code | MiniMax-M3 | TR | /root/.arifos/agents/kimi/ | 11 |
| OpenCode | MiMo V2.5 Pro | TR | /root/.config/opencode/AGENTS.md | cmd-init |
| Grok Build | grok-build | TR | /root/.grok/AGENTS.md | — |
| Antigravity | Gemini 3.5 Flash | TR | /root/.arifos/agents/antigravity/ | 13 |
| Hermes ASI | deepseek-v4-pro | TR→MiMo→MiniMax | /root/HERMES/config.yaml | 6+federation |

## Organs (6 — all green)

| Organ | Port | Role | Systemd |
|-------|------|------|---------|
| arifOS | 8088 | Governance kernel | arifos.service |
| A-FORGE | 7071/7072 | Execution engine | a-forge.service |
| GEOX | 8081 | Earth intelligence | geox-mcp.service |
| WEALTH | 18082 | Capital intelligence | wealth-organ.service |
| WELL | 18083 | Human readiness | well.service |
| AAA | 3001 | Control plane | aaa-a2a.service |

## LLM Routing

```
TokenRouter ($85.57) → PRIMARY cognitive: reasoning, synthesis, dossiers
  GLM 5.2 FREE tier until July 25, 2026
  API: TOKENROUTER_API_KEY @ api.tokenrouter.com/v1

Direct providers → BACKUP (keep enabled, TokenRouter mahal)
  DeepSeek | MiniMax | MiMo | Kimi | OpenAI | Anthropic

Ollama bge-m3 (FREE) → EMBEDDINGS only: RAG, memory search, 2.5s warm
  127.0.0.1:11434 | CPU 500% | 1 model, 1 parallel
```

## Synthesis Pipelines (auto-run via cron)

| Pipeline | Script | Schedule | Output |
|----------|--------|----------|--------|
| VAULT999 Chronicle | chronicle_vault999.py | Daily 6am MYT | /root/AAA/docs/WEEKLY_CHRONICLE.md |
| Health Narrative | health_narrative.py | Every 4h | /root/AAA/docs/FEDERATION_HEALTH.md |
| Memory Bridge | memory_bridge.py | Every 6h | /root/AAA/docs/CONTINUITY_BRIDGE.md |
| Prospect Narrator | prospect_narrator.py | On-demand | /root/AAA/docs/prospects/ |

## Config Files (all SOT stamped 2026-07-19)

| File | Purpose |
|------|---------|
| /root/.copilot/copilot-instructions.md | Copilot CLI baseline |
| /root/.copilot/mcp-config.json | 15 MCP servers |
| /root/.copilot/settings.json | deepseek-v4-pro, AUTOPILOT |
| /root/.copilot/permissions-config.json | Full exec, no deny |
| /root/.copilot/lsp-config.json | Python + TS + YAML |
| /root/.secrets/providers.yml | LLM provider routing |
| /root/.secrets/vault.env | All API keys (187 vars) |
| /root/AAA/registries/AAA_AGENTS_REGISTRY.json | 16 agents |

## Key Paths

| What | Where |
|------|-------|
| Agent configs | /root/.arifos/agents/<agent>/AGENTS.md |
| AAA skills library | /root/AAA/skills/ (406) |
| Session state | /root/.claude/projects/-root/memory/ |
| Memory logs | /root/memory/YYYY-MM-DD.md |
| Seal chain | /root/.local/share/arifos/vault999/ |
| Forge work | /root/A-FORGE/forge_work/ |
| Secrets | /root/.secrets/vault.env |
| Audit reports | /root/AAA/docs/ |

## Session Boot Sequence

Every agent MUST load in this order:
1. Source secrets: `set -a && source /root/.secrets/vault.env && set +a`
2. Read ZEN manifest: `/root/AAA/docs/ZEN_MANIFEST.md`
3. Read continuity: `/root/AAA/docs/CONTINUITY_BRIDGE.md`
4. Read live context: `/root/CONTEXT.md`
5. Probe health: `curl :8088/health`

---

*Forged 2026-07-20. Federation fully AAA-aligned. AUTOPILOT ON.*
*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
