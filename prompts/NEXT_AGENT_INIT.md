# 🌱 NEXT AGENT INIT — arifOS AGI Substrate Hardening · 2026.07.19

> **Handoff from:** FORGE (000Ω) · Session: SEAL-6cc0880d60e04a79 · Seal: AGI-SUBSTRATE-SURVEY-2026-07-19
> **To:** Next autonomous agent (OpenCode, Claude Code, or Copilot CLI)
> **Doctrine:** DITEMPA BUKAN DIBERI
> **Status:** SEAL_READY — 5 tasks remaining from AGI substrate survey phase

---

## 0. BOOTSTRAP (mandatory, blocking)

```
1. LOAD /root/AGENTS.md → /root/AAA/prompts/INIT.md → /root/AAA/agents/opencode/AGENTS.md
2. RUN: for s in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
     n="${s%%:*}"; p="${s##*:}"
     curl -sf "http://localhost:$p/health" >/dev/null 2>&1 && echo "✅ $n" || echo "❌ $n"
   done
3. arif_init(mode="init", actor_id="<YOUR_ID>", intent="AGI substrate hardening — execute remaining tasks")
4. READ /root/A-FORGE/forge_work/2026-07-19/agi-substrate-survey-20260719.md (487 lines, 48 sources)
5. READ THIS FILE completely before acting
```

## 1. CONTEXT — What Was Done

FORGE completed a deep AGI substrate architecture survey covering:
- **48 sources** across academic literature and industry projects
- **Full organ inventory:** arifOS, A-FORGE, AAA, GEOX, WEALTH, WELL, VAULT999
- **Architectural judgment:** arifOS is the unified reference implementation — no rewrite needed
- **Three missing substrate layers identified:** Signed Registry/Receipt Plane, Governed Memory Plane, Portable Identity Plane
- **Phased roadmap:** 5 phases, Aug 2026 – Feb 2027

**Key finding:** The two-protocol stack (MCP + A2A) is settled. arifOS ships what the industry is assembling from pieces. The gap is not architecture — it's surface convergence and proof language.

## 2. REMAINING TASKS (execute in order)

### TASK 1: Close the Tool Classification Gap 🔴 CRITICAL
**Problem:** 70 OBSERVE + 33 MUTATE = 103 registered. 8 tools remain unclassified. Registry not mathematically sealed.
**Action:**
```bash
# 1. Get live MCP tool list from A-FORGE
curl -s http://localhost:7072/mcp -X POST -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python3 -c "
import json,sys; tools=json.load(sys.stdin)['result']['tools']
obs=[t for t in tools if 'OBSERVE' in str(t)] 
mut=[t for t in tools if 'MUTATE' in str(t)]
unclassified=[t for t in tools if 'OBSERVE' not in str(t) and 'MUTATE' not in str(t)]
print(f'Total: {len(tools)}, OBSERVE: {len(obs)}, MUTATE: {len(mut)}, UNCLASSIFIED: {len(unclassified)}')
for t in unclassified: print(f'  {t[\"name\"]}')
"
# 2. Read /root/A-FORGE/src/domain/governance/actionClassifier.ts
# 3. For each unclassified tool, assign: OBSERVE | MUTATE | IRREVERSIBLE
# 4. Add readOnlyHint / destructiveHint annotations to MCP tool definitions
# 5. Verify: 70 OBSERVE + 33 MUTATE + 8 IRREVERSIBLE = 111 total
```

### TASK 2: Surface Count Unification 🟡 HIGH
**Problem:** Organ tool counts diverge by surface (GEOX: 15 vs 20 vs 24; WEALTH: 12 vs 26; WELL: 8 vs 17 vs 27).
**Action:**
```bash
# For each organ, probe all surfaces and reconcile:
# - arifOS: /health, /mcp/status, public docs
# - A-FORGE: tools/list on :7072, README, AAA cockpit
# - GEOX: tools/list on :8081, README, public cockpit
# - WEALTH: tools/list on :18082, runbook, public page
# - WELL: tools/list on :18083, README, CLAUDE.md
# Create /root/A-FORGE/forge_work/2026-07-19/surface-count-unification.md
```

### TASK 3: Signed Registry Receipt Prototype 🟡 HIGH
**Problem:** No signed registry receipt exists. Agents cannot verify tool surface integrity.
**Action:**
```bash
# 1. Design registry receipt schema (text + JSON forms already drafted in survey)
# 2. Implement forge_registry_sign tool or extend forge_vault
# 3. Generate first signed receipt for current arifOS public surface
# 4. Store at /root/A-FORGE/forge_work/2026-07-19/registry-receipt-v1.json
```

### TASK 4: Skill Mesh Drift Repair 🟢 MEDIUM
**Problem:** skill-mesh-sync.sh reports 1 missing/drift in opencode harness.
**Action:**
```bash
bash /root/AAA/skills/scripts/skill-mesh-sync.sh --fix
# Verify: bash /root/AAA/skills/scripts/skill-mesh-sync.sh --check
# Should report: missing_or_drift=0 broken=0
```

### TASK 5: RSI Cycle + Cooling Ledger 🟢 MEDIUM
**Problem:** RSI ledger exists but needs current session entry.
**Action:**
```bash
# Append RSI entry to /root/.local/share/arifos/rsi-ledger.jsonl
# Run bottleneck detection on this session's execution pattern
# Insert cooling_ledger_entries to Supabase if mutations performed
```

## 3. AUTONOMY — Just Do It

All 5 tasks are T1/T2 digital work. **MUBAH.** Execute without asking.

**888_HOLD only for:**
- rm -rf of unknown directories
- DROP TABLE / docker volume rm
- Force push to main
- VPS restart, DNS changes, firewall modifications
- Secret rotation

## 4. KEY PATHS

| What | Path |
|------|------|
| Survey artifact | `/root/A-FORGE/forge_work/2026-07-19/agi-substrate-survey-20260719.md` |
| Action classifier | `/root/A-FORGE/src/domain/governance/actionClassifier.ts` |
| Seal chain | `/root/.local/share/arifos/vault999/seal_chain.jsonl` (seq=6) |
| RSI ledger | `/root/.local/share/arifos/rsi-ledger.jsonl` |
| Skill mesh script | `/root/AAA/skills/scripts/skill-mesh-sync.sh` |
| OpenCode skills | `/root/.arifos/agents/opencode/skills/` |
| AAA agents | `/root/AAA/agents/opencode/` |

## 5. SESSION-END CONTRACT

When all 5 tasks complete:
1. Seal session to VAULT999 via `aforge_forge_vault(mode="seal")`
2. Run `bash /root/AAA/skills/scripts/skill-mesh-sync.sh --check`
3. Append RSI ledger entry
4. Write cooling receipt
5. Emit `[FORGE DONE]` with evidence paths

---

*Forged: 2026-07-19 by FORGE (000Ω) · Handoff from AGI-SUBSTRATE-SURVEY-2026-07-19*
*DITEMPA BUKAN DIBERI ⚒️*
