# SUBSTRATE.md — Live Runtime State

> **Updated:** 2026-06-13 15:30 UTC (Asia/Kuala_Lumpur 23:30)
> **Refresh cadence:** On every major action

## Model Status

| Model | Role | Status | Last Checked |
|-------|------|--------|--------------|
| deepseek/deepseek-chat | Primary | 🟢 Active ($7.06 USD) | 2026-06-13 15:15 |
| deepseek/deepseek-reasoner | Secondary | 🟢 Ready (R1, same key) | 2026-06-13 15:15 |
| ollama/qwen2.5:7b | Local fallback | 🟢 Ready (localhost:11434) | 2026-06-13 15:30 |
| minimax/MiniMax-M3 | External | ⚠️ Rate-limited (429) | 2026-06-13 15:15 |
| minimax/MiniMax-M2.7-highspeed | External | ⚠️ Rate-limited (429) | 2026-06-13 15:15 |
| kimi/kimi-for-coding | Available | ⚪ Available (not bound) | 2026-06-13 |

**Active inference endpoint:** deepseek @ api.deepseek.com/v1
**Secondary inference:** deepseek-reasoner @ api.deepseek.com/v1
**Local inference endpoint:** ollama @ localhost:11434 (qwen2.5:7b)

## Federation Health

| Service | Port | Status | Notes |
|---------|------|--------|-------|
| arifOS MCP | 8088 | 🟢 GREEN | healthy, 13 tools, 13 floors, commit e99bcfc |
| GEOX MCP | 8081 | 🟢 GREEN | 33 tools, geox-unified, healthy |
| WEALTH MCP | 18082 | 🟢 GREEN | healthy, registry=PASS |
| WELL MCP | 18083 | 🟢 GREEN | healthy |
| A-FORGE | 7071 | 🟢 HEALTHY | identity verified |
| OpenClaw Gateway | 18789 | 🟢 Live | ws://127.0.0.1:18789 |
| AAA A2A | 3001 | 🟢 | aaa-a2a |
| Hermes ASI Gateway | systemd | 🟢 Active | deepseek-chat, Telegram connected |

## Substrate Metrics (last verified 17:30 UTC)

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| **Genius (G)** | ~0.85 | ≥ 0.80 | 🟢 |
| **Entropy ΔS** | ~0.02 | ≤ 0 | 🟢 |
| **Human Impact Load (Ω)** | ~0.08 | ≤ 0.10 | 🟢 |
| **Vitality (Ψ)** | ~1.05 | ≥ 1.0 | 🟢 |
| **Peace²** | ~1.0 | ≥ 1.0 | 🟢 |
| **C_dark** | ~0.05 | < 0.30 | 🟢 |
| **Uncertainty (Ω₀)** | ~0.04 | [0.03, 0.05] | 🟢 |

## OpenClaw Version State

| Field | Value |
|-------|-------|
| Live | Current (systemd openclaw-gateway) |
| Gateway | ws://127.0.0.1:18789, health={"ok":true} |
| Agent Card | https://openclaw.arif-fazil.com/.well-known/agent-card.json |

## Sub-Agent Surface

| Agent | Path | Use |
|-------|------|-----|
| main | /root/.openclaw/agents/main/ | Default, this session |
| codex | /root/.openclaw/agents/codex/ | Coding tasks, multi-file edits |
| kimi | /root/.openclaw/agents/kimi/ | Long-context analysis (256K) |
| opencode | /root/.openclaw/agents/opencode/ | Multi-file structural changes |

**Routing:** Not yet wired (gap). Planned: codex→code, kimi→long-context, opencode→structural.

## Host Vitals

| Metric | Value |
|--------|-------|
| **Disk** | 45% used / 216G free |
| **Load** | 1.71 (low — clean) |
| **arifOS** | systemd active, commit e99bcfc |
| **Identity hash (b3_prefix)** | c01c70fdfa3c4dce |

## Constitutional State

| Field | Value |
|-------|-------|
| **Constitution Hash** | v2026.05.16-eureka-metabolic |
| **Invariants Hash** | v2026.05.05-SSCT |
| **Stage** | 444 (Kernel Orchestration) |
| **Lane** | AGI |
| **Decision Class** | C2 |
| **Actor** | arif-fazil-af-forge |
| **Autonomy Level** | L3 default, L4 for this session (per F13 waiver) |
| **F13 SOVEREIGN** | 🔓 WAIVED for 2026-06-06 17:26 UTC session only |

## Skills (Workspace — 24 total)

21 + 3 forged today:
- 21 original: active-maintenance, agent-memory-bridge, arif-mcp-governor, code-analysis-skills, constitutional-auditor, docker, docker-guardian, federation-orchestrator, github, google-workspace-cli, infra-crons, infra-guardian, mcp-lifeguard, model-fallback-monitor, openclaw-memory, openclaw-skill-vetter, secret-hygiene, summarize-pro, telegram-security-audit, vault999-reader, wealth-claim-state, well-boundary-repair
- 3 forged today (2026-06-06): **agentic-loop**, **self-audit**, **deep-research**

## How to Update This File

Run after major actions:
```bash
bash /root/.openclaw/workspace/skills/model-fallback-monitor/probe.sh
bash /root/.openclaw/workspace/skills/docker-guardian/probe.sh
```

Or refresh manually with `date` and current status checks (what this run did).
