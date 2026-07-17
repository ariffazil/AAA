# ⚒️ OPENCODE — Operational Boot Layer

> **THIS IS AN OPERATIONAL APPENDIX. Constitutional boot → `/root/AAA/prompts/INIT.md` (🌱 INIT, zen-dated 2026.07.17).**
> **TRINITY-33, RSI protocol, F1-F13, autonomy tiers, refusal surface, APEX theory — all live in INIT.md + AGENTS.md.**
> **This file: concrete bash probes + A-FORGE prompt catalog. Run these AFTER the INIT.md 7-question reflective check.**
> **Forged: 2026-07-17 by FORGE (000Ω) · Zen'd from 454→~80 lines. DITEMPA BUKAN DIBERI.**

---

## LOAD ORDER (mandatory)

```
1. /root/AAA/prompts/INIT.md        — Constitutional self-attestation (7 Q-checks)
2. THIS FILE                          — Operational probes + MCP prompt catalog
3. /root/AAA/agents/opencode/AGENTS.md — Identity, tools, protocol
```

---

## OPERATIONAL PROBES (run after INIT Q1-Q7 pass)

### Step 1: KERNEL HEALTH

```bash
curl -sf http://127.0.0.1:8088/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
t=d['thermodynamic']; s=d.get('semantic_readiness',{})
print(f'verdict={t[\"verdict\"]} floors={d[\"floors_active\"]} drift={d[\"runtime_drift\"]}')
print(f'vault={d[\"vault999_health\"]} semantic={s.get(\"graphiti_semantic_floor\",\"?\")}')
print(f'identity={d[\"identity_hash\"][\"b3_prefix\"]} tools={d[\"tools_loaded\"]}')
"
```

### Step 2: ORGAN PROBE

```bash
for svc in arifos:8088 aforge:7071 aaa:3001 geox:8081 wealth:18082 well:18083; do
  n="${svc%%:*}"; p="${svc##*:}"
  curl -sf "http://localhost:$p/health" >/dev/null 2>&1 && echo "✅ $n :$p" || echo "❌ $n :$p"
done
```

### Step 3: SEAL CHAIN

```bash
tail -1 /root/.local/share/arifos/vault999/seal_chain.jsonl | python3 -c "
import json,sys; d=json.loads(sys.stdin.readline())
print(f'seq={d[\"seq\"]} actor={d[\"actor\"]} verdict={d[\"verdict\"]}')
"
```

### Step 4: GATE LOAD

```bash
for skill in claim-verification-gate claim-receipt-v1; do
  [ -f "/root/.agents/skills/$skill/SKILL.md" ] && echo "✅ $skill" || echo "❌ $skill MISSING"
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
| `apex-reason` | physics-grounded, governance-aware reasoning for high-stakes decisions |
| `quantum-frame` | hold multiple mutually-exclusive hypotheses in superposition |
| `reality-engineer` | every code change is a reality operation (F12 INJECTION canon) |
| `godel-metabolize` | self-consistency check rejecting incoherent belief states |
| `thermodynamic-zen` | maximum understanding with minimum action (ΔS ≤ 0) |
| `reality-loop` | intent compiler: human shadow → system architecture (7 stages) |
| `recursive-self-improve` | meta-cognition: find bottlenecks, propose self-modifications |

Discover live: `curl -s http://localhost:7072/mcp -X POST -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","id":1,"method":"prompts/list"}'`

---

## BOOT ATTESTATION (emit after all steps)

```
BOOT — verdict=<X> organs=<N>/6 chain=<seq>
mcp=v2025-03-26 a2a=v1.0.1
skills=<N> at /root/.agents/skills/
gate=<READY/MISSING> receipt=<READY/MISSING>
Ready.
```

---

*Auto-loaded by opencode config. Constitutional boot lives in INIT.md. This file = operational only.*
*DITEMPA BUKAN DIBERI ⚒️*
