# BOOTSTRAP.md — OpenCode Cold Start Procedure

> **DITEMPA BUKAN DIBERI** — Forged, Not Given.

## Ignition Sequence (Run at Every Session Start)

```
STEP 1: VERIFY ENVIRONMENT
─────────────────────────────
$ uname -a
$ python3 --version
$ which opencode
$ node --version

STEP 2: REALITY CHECK (MANDATORY — no exceptions)
─────────────────────────────────────────────────
$ for svc in "arifos:8088" "aforge:7071" "aaa:3001" "geox:8081" "wealth:18082" "well:18083"; do
    name="${svc%%:*}"; port="${svc##*:}"
    curl -sf "http://localhost:$port/health" >/dev/null 2>&1 \
      && echo "✅ $name :$port" || echo "❌ $name :$port"
  done

If any ❌: that organ is DOWN. Proceed read-only on live organs.
Do NOT assume dead organ config is still valid.

STEP 2.5: LOAD ZEN ORGANS (MANDATORY — before any action)
─────────────────────────────────────────────────
Load skill: zen-organs
→ /root/.agents/skills/ZEN_ORGANS/SKILL.md
→ Enforce Seven Organs: Reality, Governance, Civilization, Execution, Memory, Witness, Meaning
→ If any organ missing/degraded/contradicted: DECLARE FIRST.
→ No exceptions.

STEP 3: LOAD CONTEXT
─────────────────────
Read (in order):
1. /root/AGENTS.md              — Federation constitution
2. /root/AAA/agents/opencode/AGENTS.md — Agent identity
3. /root/AAA/agents/opencode/SOUL.md   — Voice
4. /root/.openclaw/workspace/USER.md   — About Arif
5. /root/CONTEXT.md              — Live machine state (if exists)

STEP 4: SYSTEM HEALTH
──────────────────────
$ free -h                    # Memory
$ df -h /                    # Disk
$ docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"  # Containers
$ uptime                     # Load average

STEP 5: SESSION INIT (optional — for governed work)
───────────────────────────────────────────────────
Call arif_session_init via MCP to bind constitutional session.
Call arif_organ_attest_all to verify 7 organs alive.

STEP 5.5: TOOL DISCOVERY
─────────────────────────
Three probes to discover ALL available tools:
1. MCP tools/list: `curl -s http://localhost:8088/mcp -X POST \
   -H "Content-Type: application/json" -d '{"method":"tools/list"}'`
   — returns 9 canonical arif_* tools.
2. /health: `curl -s http://localhost:8088/health` — tool counts, naming.
3. arif_retrieve_tools(query="*") — BM25 across full 58-tool catalog.
Or check the public manifest at https://mcp.arif-fazil.com/manifest/tools.json
for the federation organ surface. Run before first action.

STEP 6: REPORT
──────────────
IGNITION COMPLETE. State:
- Organs: X/7 alive
- Memory: X% used
- Disk: X% used
- Load: X.XX
- Ditempa Bukan Diberi.
```

## Quick Health Commands

```bash
# One-liner full health check
curl -sf http://localhost:8088/health >/dev/null && echo "✅ arifos" || echo "❌ arifos"; \
curl -sf http://localhost:7071/health >/dev/null && echo "✅ aforge" || echo "❌ aforge"; \
curl -sf http://localhost:3001/health >/dev/null && echo "✅ aaa" || echo "❌ aaa"; \
curl -sf http://localhost:8081/health >/dev/null && echo "✅ geox" || echo "❌ geox"; \
curl -sf http://localhost:18082/health >/dev/null && echo "✅ wealth" || echo "❌ wealth"; \
curl -sf http://localhost:18083/health >/dev/null && echo "✅ well" || echo "❌ well"

# Git status for all repos
for d in /root/{arifOS,A-FORGE,AAA,WEALTH,WELL,geox}; do
  printf "%-12s " "$(basename $d)"
  git -C $d status -sb 2>/dev/null || echo "not a git repo"
done
```

## What To Do If Organ Is Down

1. **arifos down** → STOP. Cannot proceed with governed work. Read-only only.
2. **aforge down** → Cannot build/deploy. Can still read/plan.
3. **aaa down** → Control plane offline. Federation still runs, no cockpit.
4. **geox/wealth/well down** → Domain organ offline. Skip its tools, proceed with others.
5. **All down** → VPS issue. Check `systemctl status`, `docker ps`, `journalctl`.

## Model Rotation (Active 2026-07-02)

| Agent | Model | Provider |
|-------|-------|----------|
| Main | MiMo V2.5 Pro | Xiaomi token-plan-sgp |
| FORGE | GLM-5.2 | Bailian token-plan |
| AUDITOR | DeepSeek V4 Pro | Bailian token-plan |
| OPS | MiniMax M2.7 Highspeed | MiniMax direct |
| PLAN | Kimi K2.7 Code | Bailian token-plan |
| Small | Qwen 3.6 Flash | Bailian token-plan |

---

*Forged: 2026-06-25 · Model rotation corrected: 2026-07-02*
*DITEMPA BUKAN DIBERI*
