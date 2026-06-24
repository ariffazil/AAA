---
id: kimi-code-aaa
name: Kimi Code AAA Configuration
version: 1.0.0
description: Configure, audit, and align Kimi Code CLI as AAA warga FI-008 with arifOS
  kernel and A-FORGE stdio actuator.
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- kimi-code
- kimi
- claude-code
- codex
- opencode
dependencies:
  skills:
  - arifos-mcp-federation
  - agent-onboarding
  servers:
  - arifos
  - aforge
  - geox
  - wealth
  - well
  tools: []
examples:
- Audit Kimi Code MCP configuration against federation canonical paths
- 'Repair A-FORGE stdio launcher after `source: not found`'
tests:
- '`kimi doctor` reports OK config.toml'
- All federation organ health endpoints respond
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Ω
  - ΦΙ
  functional:
  - Interface
  layer: HEXAGON
  autonomy_tier: T1-T2
floor_scope:
- F1
- F2
- F4
- F8
- F11
- F13
---

# Kimi Code AAA Configuration

## arifOS-ACT Embedding

Before using this skill on any mutating, irreversible, or high-blast-radius task:
1. **ART** — Attune (what is the real task?), Recognize (what class of power?), Test (fit · authority · evidence · blast · reversible).
2. **Kernel** — Route to arifOS for F1–F13 judgment if action class is Maker/Messenger/Mutator/Destroyer/Sovereign.
3. **ACT** — Apply narrow, Constrain scope, Trace witness, STOP before corruption.
4. **Receipt** — Leave evidence of what changed, why, and under whose authority.


## When to Use

- Kimi Code CLI fails with LLM 404, MCP `source: not found`, or missing federation tools
- Migrating from legacy `kimi-cli` (uv, v1.47) to `kimi-code` (v0.18+)
- Onboarding Kimi as warga AAA (FI-008)
- Auditing `mcp.json`, `config.toml`, or `KIMI_CODE_HOME` drift

## When NOT to Use

- Do not use to rotate secrets in `vault.env` without 888_HOLD
- Do not enable `default_yolo = true` for constitutional work
- Do not wire A-FORGE HTTP `:7071/mcp` as primary ingress (single-session SDK limit)

## Canonical Paths (af-forge VPS)

| Path | Purpose |
|------|---------|
| `/root/.kimi-code/bin/kimi` | kimi-code binary (v0.18+) |
| `/usr/local/bin/kimi` | Federation wrapper (sets `KIMI_CODE_HOME`, unsets dead `KIMI_API_KEY`) |
| `$KIMI_CODE_HOME` → `/root/.arifos/agents/kimi` | Config, MCP, hooks, credentials, skills |
| `/root/.arifos/agents/kimi/mcp.json` | User-global MCP (13 servers, 9 active) |
| `/root/.mcp.json` | Project-root MCP when cwd is `/root` |
| `/root/AAA/agents/kimi-code/WARGAAA_CARD.md` | Warga identity card |

## Official Docs

- Install & first launch: https://platform.kimi.ai/docs/guide/kimi-cli-support
- Config files: https://www.kimi.com/code/docs/kimi-code-cli/configuration/config-files.html
- MCP: https://moonshotai.github.io/kimi-cli/en/customization/mcp.html
- Migrate: `kimi migrate` (interactive — config only recommended)

## Audit Checklist

1. **Binary:** `which kimi` → `/usr/local/bin/kimi` → exec `~/.kimi-code/bin/kimi`
2. **Home:** `echo $KIMI_CODE_HOME` → `/root/.arifos/agents/kimi`
3. **Doctor:** `kimi doctor` → `OK config.toml`
4. **Auth:** OAuth via `/login` — **never** use dead `KIMI_API_KEY` from `vault.env` (causes 404)
5. **MCP launchers:** All stdio servers use `mcp-launchers/*.sh` (bash), not inline `sh -lc` with `source`
6. **A-FORGE:** stdio via `aforge.sh` — not HTTP for Kimi primary ingress
7. **Serena:** `arifOS/.serena/project.yml` and `A-FORGE/.serena/project.yml` exist
8. **Warga:** `config.toml` has `[agent_identity] citizenship = "warga-aaa"`

## Fix Patterns

### LLM 404 `resource_not_found_error`

Root cause: stale `KIMI_API_KEY` in environment overrides OAuth.

```bash
unset KIMI_API_KEY
kimi login   # or /login in TUI
kimi doctor
```

Wrapper at `/usr/local/bin/kimi` already unsets `KIMI_API_KEY`.

### `sh: 35: source: not found`

Root cause: MCP stdio launchers invoked via `sh` with bash-only `source`.

Fix: use dedicated bash scripts in `mcp-launchers/` with `#!/usr/bin/env bash` and `. /root/.env` (not `source`).

### MCP 11/13 connected, meyhem/github still loading

Ensure `disabled: true` on legacy servers in `mcp.json`. Start fresh session: `/new`.

## Health Verification

```bash
for p in 8088 8081 18082 18083 7071 3001; do
  curl -sf "http://127.0.0.1:$p/health" >/dev/null && echo ":$p OK" || echo ":$p FAIL"
done
kimi doctor
```

## Escalation

| Condition | Action |
|-----------|--------|
| OAuth revoked | `/login` in Kimi TUI |
| A-FORGE stdio fails | `cd /root/A-FORGE && npm run build` then retry |
| Cross-repo architecture change | 888_HOLD → Arif |

DITEMPA BUKAN DIBERI.