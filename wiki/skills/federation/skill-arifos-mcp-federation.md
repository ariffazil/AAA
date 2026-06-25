---
title: "SKILL: arifOS MCP Federation Router"
type: skill
version: 1.0.0
category: governance
risk_band: LOW
floors: [F1, F4, F8]
evidence_required: true
sources: [/root/.agents/skills/arifos-mcp-federation/SKILL.md]
confidence: high
---

# SKILL: arifOS MCP Federation Router

> **Source:** `/root/.agents/skills/arifos-mcp-federation/SKILL.md`
> **Agent:** FORGE (A-FORGE)
> **Forged:** 2026-06-25
> **Status:** ACTIVE

---

## Trigger Conditions

- Task spans two or more organs (GEOX, WEALTH, WELL, A-FORGE, AAA)
- Cross-organ routing decisions needed
- Organ failure fallback required
- Intent classification before routing
- Keywords: route, route_to_organ, cross-organ, federation, multi-organ, organ_fail, fallback

---

## What This Skill Does

Routes tasks across the arifOS federation MCP servers, sequences tool calls, and defines fallbacks when an organ substrate fails.

**Use when:**
- A task requires GEOX + WEALTH (e.g., prospect economics)
- A task requires WELL + WEALTH (e.g., human capital vs financial capital)
- An organ is down and you need graceful degradation
- You need to classify intent before routing
- You're unsure which organ owns a concern

**Do NOT use when:**
- Single-organ task (use that organ's tools directly)
- Pure build/deploy (use A-FORGE forge_* tools only)
- Constitutional judgment needed (use arifOS arif_judge)

---

## The 7 Federation Organs

| Organ | Port | Domain | MCP Server |
|-------|------|--------|------------|
| arifOS | 8088 | Governance, session, vault, F1-F13 | arifos-kernel |
| A-FORGE | 7071/7072 | Build, deploy, execution | aforge |
| GEOX | 8081 | Earth intelligence, seismic, petrophysics | geox |
| WEALTH | 18082 | Capital, NPV, risk, stock | wealth |
| WELL | 18083 | Human readiness, vitality | well |
| AAA | 3001 | Control plane, A2A gateway | — |
| VAULT999 | — | Immutable audit ledger | arifos (vault_seal) |

---

## Intent Classification (arif_route)

Before routing, classify the user's intent:

```
arif_route(intent="<natural language task>")
```

Returns:
- `organ`: primary organ for this task
- `organ_tool`: specific tool on that organ
- `fallback_organs`: degraded path if primary fails
- `confidence`: 0.0-1.0

### Decision Tree

```
User intent
  ├── Build/Deploy/Execute  → A-FORGE (forge_*)
  ├── Geoscience/Earth     → GEOX (geox_*)
  ├── Finance/Capital/Risk → WEALTH (wealth_*)
  ├── Human health/vitality → WELL (well_*)
  ├── Governance/Judgment/Seal → arifOS (arif_*)
  ├── Control plane/A2A    → AAA
  ├── Multi-organ          → arif_route() first, then chain
  └── Unknown              → arif_triage() on arifOS
```

---

## Cross-Organ Routing Patterns

### Pattern 1: Sequential Chain (A → B)

```
1. arif_route(intent="<task>")
2. Primary organ tool call
3. Pass output to second organ
4. Synthesize result
```

### Pattern 2: Parallel Fan-Out

```
1. arif_route(intent="<task>")
2. Call multiple organs simultaneously
3. Wait for all results
4. Synthesize (arif_compose)
```

### Pattern 3: Conditional Branch

```
1. Call primary organ
2. If result.uncertainty > threshold → call fallback organ
3. Reconcile outputs
```

### Pattern 4: Graceful Degradation

```
1. Call primary organ
2. If primary DOWN → log organ_down event → call fallback organ
3. If fallback also DOWN → escalate to arifOS arif_judge
4. Never fail silently — always report organ state
```

---

## Organ Health Pre-Flight

Before any cross-organ task, verify organs are alive:

```bash
for svc in "arifos:8088" "aforge:7071" "aaa:3001" "geox:8081" "wealth:18082" "well:18083"; do
  name="${svc%%:*}"; port="${svc##*:}"
  curl -sf "http://localhost:$port/health" >/dev/null 2>&1 \
    && echo "✅ $name" || echo "❌ $name DOWN"
done
```

**Rule:** If any required organ is DOWN, proceed read-only on live organs. Do NOT assume dead organ config is still valid.

---

## Blast Radius Assessment

Before cross-organ mutation:

| Organs Affected | Blast Radius | Gate |
|----------------|--------------|------|
| 1 organ | LOW | T1 AUTO-DO |
| 2 organs | MEDIUM | Announce, 10s window |
| 3+ organs | HIGH | 888_HOLD |
| arifOS kernel | CRITICAL | F13 SOVEREIGN |

---

## Reversibility Rules

| Action | Reversibility | Gate |
|--------|--------------|------|
| Read-only cross-organ query | FULL | T1 AUTO-DO |
| Single-organ write | FULL | T1 AUTO-DO |
| Two-organ write | PARTIAL | Announce |
| Three-organ write | IRREVERSIBLE | 888_HOLD |
| VAULT999 seal | IRREVERSIBLE | F13 SOVEREIGN |

---

## Federation Router Skill Map

| Task | Tool | Organ |
|------|------|-------|
| "interpret this seismic" | geox_seismic_interpret | GEOX |
| "assess portfolio risk" | wealth_risk_assessment | WEALTH |
| "how tired am I" | well_assess_homeostasis | WELL |
| "build and deploy" | forge_execute | A-FORGE |
| "is this constitutional" | arif_judge | arifOS |
| "what should I do" | arif_route | arifOS |
| "economists view of prospect" | geox + wealth chain | GEOX → WEALTH |
| "human capital vs financial" | well + wealth chain | WELL → WEALTH |

---

## Evidence Requirements

- Log every cross-organ call: organ, tool, input_hash, output_hash, duration_ms
- Log organ DOWN events with timestamp
- Record fallback chain when degradation occurs
- Seal high-value cross-organ decisions to VAULT999

---

## Anti-Patterns

- ❌ Calling WEALTH for geological judgments (wrong organ)
- ❌ Bypassing arifOS for constitutional questions
- ❌ Proceeding when required organ is DOWN (silence = failure)
- ❌ Routing through dead organ config
- ❌ Claiming certainty without multi-organ evidence

---

## Skill Forged By

DITEMPA BUKAN DIBERI — Forged, Not Given.
