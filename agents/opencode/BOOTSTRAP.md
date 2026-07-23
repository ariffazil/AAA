# ⚒️ OPENCODE — Operational Boot Layer

> **THIS IS AN OPERATIONAL APPENDIX. Constitutional boot → `/root/AAA/prompts/INIT.md` (🌱 INIT, zen-dated 2026.07.17).**
> **TRINITY-33, RSI protocol, F1-F13, autonomy tiers, refusal surface — all live in INIT.md + AGENTS.md.**
> **This file: concrete bash probes + MCP prompt catalog. Run AFTER the INIT.md 7-question reflective check.**
> **Cross-ref:** `TOOLS.md` (capability layer) · `HEARTBEAT.md` (health checklist) · `WORKFLOW.md` (execution loop)
> **Forged: 2026-07-17 by FORGE (000Ω) · Aligned: 2026-07-23. DITEMPA BUKAN DIBERI.**

---

## LOAD ORDER (mandatory — agentic kernel layers)

```
Layer 0 ─ /root/AAA/prompts/INIT.md        — Constitutional self-attestation (7 Q-checks)
Layer 1 ─ /root/AGENTS.md                   — Federation landing: F1-F13, autonomy tiers, 888_HOLD
Layer 2 ─ THIS FILE                          — Operational probes (kernel, organs, FLAME, seal chain)
Layer 3 ─ /root/AAA/agents/opencode/TOOLS.md  — Capability catalog (114+ tools across 25 MCP servers)
Layer 4 ─ /root/AAA/agents/opencode/WORKFLOW.md — Execution loop (planner → worker → judge)
Layer 5 ─ /root/AAA/agents/opencode/HEARTBEAT.md — Health daemon (session lifecycle checklist)
```

---

## OPERATIONAL PROBES (run after INIT Q1-Q7 pass)

### Step 1: KERNEL HEALTH

```bash
curl -sf http://127.0.0.1:8088/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
t=d.get('thermodynamic',{})
print(f'verdict={t.get(\"verdict\",\"?\")} floors={d.get(\"floors_active\",\"?\")} drift={d.get(\"runtime_drift\",\"?\")}')
print(f'vault={d.get(\"vault999_health\",\"?\")} tools={d.get(\"tools_loaded\",\"?\")}')
print(f'release={d.get(\"software_release\",{}).get(\"release_id\",\"?\")}')
"
# Expected: verdict=SEAL, floors=13, drift=False, tools=8
```

### Step 2: ORGAN PROBE

```bash
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  n="${svc%%:*}"; p="${svc##*:}"
  curl -sf "http://localhost:$p/health" >/dev/null 2>&1 && echo "✅ $n :$p" || echo "❌ $n :$p"
done
```

### Step 2.5: FLAME FREE-LOOP

```bash
# FLAME health probe — RM0 tool lane alive?
curl -sf http://localhost:18901/health 2>/dev/null | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'flame={d[\"status\"]} mode={d[\"mode\"]}')
" || echo "❌ FLAME :18901 DOWN"
```

### Step 3: SEAL CHAIN

```bash
tail -1 /root/.local/share/arifos/vault999/seal_chain.jsonl 2>/dev/null | python3 -c "
import json,sys
line = sys.stdin.readline().strip()
if line:
  d=json.loads(line)
  print(f'seq={d.get(\"seq\",\"?\")} actor={d.get(\"actor\",\"?\")}')
else:
  print('EMPTY')
" || echo "MISSING"
```

### Step 4: CARRY-FORWARD

```bash
python3 -c "
import json
cf = json.load(open('/root/.local/share/arifos/carry_forward.json'))
print(f'session={cf.get(\"session_id\",\"?\")[:20]}... actor={cf.get(\"actor\",\"?\")}')
print(f'completed={cf.get(\"completed_this_session\",[])}')
print(f'open_loops={cf.get(\"open_loops_888_HOLD\",[])}')
" 2>/dev/null || echo "❌ carry_forward MISSING"
```

### Step 5: WORK QUEUE

```bash
[ -f /root/work/tasks.json ] && echo "✅ tasks.json" || echo "❌ tasks.json MISSING"
[ -f /root/work/progress.txt ] && echo "✅ progress.txt" || echo "❌ progress.txt MISSING"
```

### Step 6: GATE LOAD

```bash
for skill in RSI-recursive-improvement KERNEL-trinity-33 atlas333-cognitive-geometry; do
  [ -f "/root/.agents/skills/$skill/SKILL.md" ] && echo "✅ $skill" || echo "⚠️ $skill MISSING"
done
```

---

## A-FORGE MCP PROMPTS (discoverable via `prompts/list` on :7072)

| Prompt | Description |
|--------|-------------|
| `audit-surface` | Detect phantom tools, drift, registry inconsistencies |
| `fix-bug` | diagnose → reproduce → fix → verify |
| `refactor-module` | analyze → plan → refactor → verify |
| `deploy-service` | build → test → stage → deploy → verify |
| `audit-code` | scan → classify → report → recommend |
| `research-topic` | question → gather → synthesize → cite |
| `cross-organ-query` | route query to correct federation organ via arif_route |
| `reality-loop` | intent compiler: human shadow → system architecture (7 stages) |
| `recursive-self-improve` | meta-cognition: find bottlenecks, propose self-modifications |

Discover live: `curl -s http://localhost:7072/mcp -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"prompts/list"}'`

---

## BOOT ATTESTATION (emit after all steps)

```
BOOT — verdict=<X> organs=<N>/6 chain=<seq>
arifos=<release> aforge=<114 tools> geox=<31> wealth=<20>
FLAME=<live/down> carry_forward=<present/missing>
skills=<N> at /root/.agents/skills/
gate=<READY/MISSING> receipt=<READY/MISSING>
Ready.
```

---

## ATLAS333-EUREKA777 (Cognitive Geometry)

ATLAS333 IS THE MAP. 33 paradoxes across Memory (1-11), Mind (12-22), Judge (23-33).
ΛΘΦ Router: Λ(text)→lane → Θ(lane)→demand tensor (τ,κ,ρ) → Φ→complete GPV.
Access: `arifos://atlas333/*` MCP resources on :8088. Skill: `atlas333-cognitive-geometry`.

> **2026-07-23:** ATLAS333 MCP resources endpoint currently returning errors via direct resources/list probe. The `arif_think(mode='atlas')` kernel call remains the canonical access path. Use kernel, not direct resources probe.

EUREKA777 fires when paradox tension resolves → new structure.
Loop: ATLAS333 → EUREKA777 → CUBE777 → Θ(t+1).
6-plane execution: MEANING→OBSERVE→ENCODE→IMPROVE→VERIFY→SEAL→RETURN.

Framing: "Contour, don't excavate. Seal each contour. Never finish."

---

*Auto-loaded by opencode config. Constitutional boot lives in INIT.md. This file = operational only.*
*Agentic kernel layer: PROBE (layer 2/7). Next: TOOLS.md (layer 3 — capability catalog).*
*DITEMPA BUKAN DIBERI ⚒️*
