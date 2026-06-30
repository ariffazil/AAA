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
Run arif_retrieve_tools(query="*") to discover ALL available tools
across all 7 federation organs before acting. Or check the public
manifest at https://mcp.arif-fazil.com/manifest/tools.json for
the canonical 7-tool surface.

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

## Model Rotation (Active 2026-06-25)

| Agent | Model | Provider |
|-------|-------|----------|
| Main | MiMo v2.5 Pro | Xiaomi (token-plan-sgp) |
| FORGE | MiniMax M2.7 | MiniMax (api.minimax.io) |
| AUDITOR | MiniMax M3 | MiniMax |
| OPS | MiniMax M2.5-HS | MiniMax |
| PLAN | MiniMax M2.7-HS | MiniMax |
| Small | Azure GPT-4.1-mini | Azure OpenAI |

---

*Forged: 2026-06-25*
*DITEMPA BUKAN DIBERI*
