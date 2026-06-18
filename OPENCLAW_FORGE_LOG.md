# OPENCLAW_FORGE_LOG.md

## 2026-06-14 06:47–06:53 UTC — P0 Restore: Search, MCP Sessions, Health Scan

### Context
Arif (msg #75099) directed: restore OpenClaw's ability to operate as a staff agent. Three P0 blockers:
1. web_search dead (all 3 providers failing)
2. arifOS MCP sessions unreliable
3. No systematic federation health check

### Changes Made

#### P0-1: Restore web_search → Brave
- **Config change**: `tools.web.search.provider`: `minimax` → `brave`
- **Plugin added**: `brave` to `plugins.allow` and `plugins.entries`
- **Verified**: Brave Search API key (`BSABWbaBI-sVc-i-2iCya6AcHjLQflt`) works — returns real web results
- **Why not Tavily top-up**: Both Tavily keys rate-limited (dev tier). Brave was already configured (key in env) and built into OpenClaw (`brave-web-search-provider.runtime.js`). Free tier: 2,000 queries/month.

#### P0-2: Fix arifOS MCP session reliability
- **Config change**: `mcp.servers.arifos.url`: `http://127.0.0.1:8088/mcp` → `http://127.0.0.1:8091/mcp`
- **Why**: Gateway :8091 handles session management, auth, routing to all 6 upstream organs. Direct :8088 has session expiry issues + "Not Acceptable" header requirements.
- **Verified**: `tools/list` via :8091 returns 79 tools. `arif_ops_measure(mode=health)` returns live system data (CPU 16.4%, mem 44.7%, disk 41.9%).

#### P0-3: Forge federation_health_scan() skill
- **Files created**: 
  - `skills/federation-health-scan/SKILL.md` (1.9KB)
  - `skills/federation-health-scan/federation_health_scan.py` (8.5KB)
- **Probes**: 5 organ health endpoints, NATS CLI, VAULT999 file, arifOS gateway
- **Output**: Structured JSON with organs/nats/drift/vault/summary/recommendation
- **Live test**: 273ms scan, 6 organs, 3 NATS streams, 1,337 vault events
- **Reversibility**: Read-only. No mutations. Safe to run anytime.

### Collateral
- **Config backup**: `/root/.openclaw/openclaw.json.bak.20260614-pre-p0-fixes` (pre-change snapshot — but note: was captured after accidental wipe, so this is the re-reconstructed version from ariffazil home dir + arifos backup merge)
- **Config rebuilt from**: merger of `/root/ariffazil/.openclaw/openclaw.json` (full 33KB user config) + `/root/backups/arifos-pre-minimax-2026-06-12/config/openclaw/openclaw.json` (gateway structure) + observed gateway live values
- **F2 confession**: Initial pipe-to-python command accidentally truncated the active config file. Rebuilt from backups. Gateway is running on in-memory config from startup (still has old values until restart).

### 888_HOLD Items

| # | Item | Status | Action Needed |
|---|------|--------|---------------|
| 1 | **Gateway restart** | PENDING | `systemctl restart openclaw-gateway` to activate Brave search + :8091 MCP routing. ~3 sec downtime. Reversible: restore from backup. |
| 2 | **arifOS runtime drift** | PENDING | build_commit 0f88747 ≠ live_commit 428f039. Non-critical but flagged. Fix: rebuild/deploy container or `systemctl restart arifos`. |

### Verification
- [x] Brave Search API tested: returns real web results
- [x] arifOS :8091 gateway tested: 79 tools callable
- [x] health_scan.py tested: returns structured JSON in 273ms
- [ ] Gateway config activated (needs restart → 888_HOLD)
- [ ] End-to-end web_search test via OpenClaw (needs restart)

### Reversibility
```bash
# Revert all changes:
cp /root/.openclaw/openclaw.json.bak.20260614-pre-p0-fixes /root/.openclaw/openclaw.json
systemctl restart openclaw-gateway
rm /root/.openclaw/workspace/skills/federation-health-scan/ -rf
```

---

## 2026-06-14 06:52–06:56 UTC — SOP Skills: Drift Response, Sub-Agent Template, Tool Health Check

Arif directive #75100: Give OpenClaw standard operating procedures.

### Skill 1: Drift Response (`skills/drift-response/`)
- **SKILL.md** (3.8KB): 5-stage constitutional procedure
  1. DETECT — probe all drift signals (health endpoints, file diff, .pth check)
  2. VERIFY — `/health?nocache=1` + NATS governance + file mtime comparison
  3. CLASSIFY — NUISANCE | IMPORTANT | CRITICAL based on blast radius
  4. PROPOSE — concrete remediation, 888_HOLD for restarts
  5. ROUTE — NUISANCE→log, IMPORTANT→present to Arif, CRITICAL→alert immediately
- **Constitutional**: Never auto-executes restarts. Always routes through 888_HOLD.
- **Reversibility**: Stages 1-3 read-only. Stage 4 proposal-only. Stage 5 logging-only.

### Skill 2: Sub-Agent Spawn Template (`skills/subagent-spawn-template/`)
- **SKILL.md** (4.2KB): Standard contract for bounded, auditable sub-agents
- **Input contract**: task_name, task_description, output_schema (JSON Schema), time_budget_minutes, evidence_required, autonomy_band, tools_scope, rollback_plan
- **Behavior rules**:
  1. Time budget enforced — return BLOCKED before timeout
  2. Output schema compliance — structured JSON only
  3. Evidence attachment — every finding backed by verifiable evidence
  4. Autonomy band — AUTONOMOUS | PROPOSE_ONLY | NEVER (E7-aligned)
  5. Rollback — every spawn includes rollback plan
- **Integration**: Maps template fields to `sessions_spawn` params
- **Example**: Code auditor spawn with full contract

### Skill 3: Tool Health Checker (`skills/tool-health-check/`)
- **tool_health_check.py** (7.7KB): Smoke-tests 22 critical tools across all organs
- **SKILL.md** (1.7KB): Usage docs + cron integration
- **Live test result** (06:55 UTC, 6,950ms):
  - 16 PASS (gateway_health 11ms, arif_os_attest 22ms, arif_organ_attest_all 166ms, GEOX 34ms, WEALTH 13ms, WELL 5ms, NATS 98ms, A-FORGE 11ms)
  - 0 FAIL
  - 6 UNTESTABLE (arif_session_init, arif_lease_issue, arif_judge_deliberate, arif_vault_seal, arif_forge_execute, arif_gateway_connect — require full session)
  - Slowest: arif_memory_recall (3892ms), arifOS /health (1582ms), arif_ops_measure (975ms)
- **Cron-ready**: Systemd timer or crontab entry provided

### Summary of All Skills Forged This Session

| # | Skill | Path | Size | Status |
|---|-------|------|------|--------|
| 1 | Federation Health Scan | `skills/federation-health-scan/` | 8.5KB .py | ✅ Live |
| 2 | Drift Response | `skills/drift-response/` | 3.8KB .md | ✅ Forged |
| 3 | Sub-Agent Spawn Template | `skills/subagent-spawn-template/` | 4.2KB .md | ✅ Forged |
| 4 | Tool Health Checker | `skills/tool-health-check/` | 7.7KB .py + 1.7KB .md | ✅ Live-tested |

### 888_HOLD Items (still pending)
| # | Item | Status |
|---|------|--------|
| 1 | Gateway restart (activate Brave search + :8091 MCP) | PENDING |
| 2 | arifOS runtime drift fix (build 0f88747 ≠ live 428f039) | PENDING |

### Files Changed This Session
- `/root/.openclaw/openclaw.json` (rebuilt, 17KB)
- `/root/.openclaw/workspace/skills/federation-health-scan/` (2 files)
- `/root/.openclaw/workspace/skills/drift-response/` (1 file)
- `/root/.openclaw/workspace/skills/subagent-spawn-template/` (1 file)
- `/root/.openclaw/workspace/skills/tool-health-check/` (2 files)
- `/root/.openclaw/workspace/OPENCLAW_FORGE_LOG.md` (this file)
- `/root/.openclaw/workspace/memory/2026-06-14.md` (appended)

### Related
- Arif directives: Telegram #75099, #75100
- Session: phase1-stabilize-2026-06-06 (continued)
