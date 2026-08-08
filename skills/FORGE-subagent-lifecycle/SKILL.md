# FORGE-subagent-lifecycle — Unified Sub-Agent Lifecycle Manager

> **Forged:** 2026-08-07 by 333-AGI Δ MIND under F13 SOVEREIGN directive
> **Status:** ACTIVE (Phase 1 — pattern codification; promotion to permanent after 5+ missions)
> **DITEMPA BUKAN DIBERI** — Forged, Not Given

## WHAT THIS IS

The **unified composition layer** for sub-agent orchestration. The federation has 15+ discrete primitives (spawn, bind, execute, verify, cool, scar, ingest, seal, retire) — this skill is the **lifecycle** that wires them into one coherent pattern. A parent agent should never manually compose these primitives. Load this skill, follow the lifecycle, and every sub-agent run produces: validated output + metabolic receipt + scars (if failure) + cooling record + sealed audit trail.

## THE 9-STAGE LIFECYCLE (Spawn → Retire)

```
                    ┌─────────────────────┐
                    │ 0. DECOMPOSE        │  Break intent into atomic sub-tasks
                    └────────┬────────────┘
                             ▼
             ┌───────────────────────────────┐
             │ 1. PRE-SPAWN GATE             │  FQ check · scar consult · budget cap
             │   ┌─ FQ ≥ 0.5?                │
             │   ├─ Scar conflict?            │
             │   └─ Budget available?         │
             └───────────────┬───────────────┘
                             ▼
             ┌───────────────────────────────┐
             │ 2. SPAWN                      │  task() subagent with bounded scope
             │   ┌─ Select agent type         │
             │   ├─ Set contract (scope,       │
             │   │   budget, timeout)          │
             │   └─ Parent session ID bound   │
             └───────────────┬───────────────┘
                             ▼
             ┌───────────────────────────────┐
             │ 3. EXECUTE                    │  Sub-agent runs autonomously
             │   └─ Monitor (poll with        │
             │      timeout + backoff)        │
             └───────────────┬───────────────┘
                             ▼
             ┌───────────────────────────────┐
             │ 4. VERIFY                     │  Validate output against contract
             │   ┌─ Schema compliance          │
             │   ├─ Evidence labels present    │
             │   ├─ No self-certification      │
             │   └─ Cross-verify if SEAL-grade │
             └───────────────┬───────────────┘
                             ▼
                   ┌────────┴────────┐
                   ▼                 ▼
             ┌──────────┐    ┌──────────────┐
             │ PASS     │    │ FAIL         │
             └────┬─────┘    └──────┬───────┘
                  ▼                  ▼
        ┌──────────────┐   ┌──────────────────┐
        │ 5a. COOL     │   │ 5b. SCAR + RETRY │
        │  (drift log) │   │  (seal failure)  │
        └──────┬───────┘   └────────┬─────────┘
               │                    │
               ▼                    ▼
        ┌──────────────┐   ┌──────────────────┐
        │ 6. INGEST    │   │ 5c. ESCALATE     │
        │  (arifFlow)  │   │  (3+ failures →  │
        └──────┬───────┘   │   888_HOLD)      │
               │           └──────────────────┘
               ▼
        ┌──────────────┐
        │ 7. SEAL      │  Lane B: forge_vault(receipt)
        │              │  Lane A: arif_seal (if DEPLOY)
        └──────┬───────┘
               ▼
        ┌──────────────┐
        │ 8. RETIRE    │  Sub-agent output stored.
        │              │  Context freed. Pattern
        │              │  recorded for RSI.
        └──────────────┘
```

## CONSTITUTIONAL GATES (per stage)

| Stage | Gate | Tool | Violation → |
|-------|------|------|-------------|
| 1. PRE-SPAWN | FQ ≥ 0.5 | `arifflow_flow_health` | HOLD all spawns |
| 1. PRE-SPAWN | Scar conflict | `aforge_forge_scar(mode=consult)` | Modify task or skip |
| 1. PRE-SPAWN | Budget ≤ daily cap | Session budget tracker | Throttle or escalate |
| 4. VERIFY | Output schema valid | Parent checks | REJECT → Stage 5b |
| 4. VERIFY | Evidence labels present (OBS/DER/INT/SPEC) | Parent checks | REJECT → Stage 5b |
| 4. VERIFY | No SELF_CERTIFIED | `forge_ephemeral(verify)` pattern | REJECT → Stage 5b |
| 5b. SCAR | Failure recurrence ≥ 3 | `aforge_forge_scar(mode=seal)` | Auto-seal scar |
| 5c. ESCALATE | 3+ failures same task | Escalate to 888-APEX | 888_HOLD |
| 7. SEAL | Lane B receipt | `aforge_forge_vault(mode=receipt)` | Unsealed work |

## PRE-SPAWN GATE — DETAILED

Before spawning ANY sub-agent, the parent MUST execute this gate:

```
1. FQ CHECK: arifflow_flow_health → if quotient < 0.5 → HOLD, do not spawn
2. SCAR CONSULT: aforge_forge_scar(mode=consult, fingerprint=<task_hash>)
   → if scar_pressure > 0.7 for similar task fingerprint → MODIFY task or SKIP
3. BUDGET CHECK: track cumulative sub-agent cost. If > $1.50/session → throttle
4. CONCURRENCY CAP: max 3 concurrent sub-agents. Use forge_parallel_status to check.
```

## VERIFICATION — DETAILED

Every sub-agent output must pass ALL of:

```
SCHEMA:      output matches declared schema
EVIDENCE:    every claim carries OBS/DER/INT/SPEC label
NO_GHOSTS:   no fabricated data, no hallucinations
NO_SELF:     no SELF_CERTIFIED verification claims
UNCERTAINTY: confidence caps honored (max 0.90)
```

If any check fails:
- **First failure:** return output + correction notes to sub-agent (retry once)
- **Second failure:** REJECT. Route to Stage 5b (SCAR + RETRY or 5c ESCALATE)

## SCAR LIFECYCLE (3-Tier)

| Tier | Trigger | Action |
|------|---------|--------|
| **Active (Constraint)** | Sub-agent fails same task 3+ times | Hard firewall: block identical task fingerprint until modified |
| **Generalized (Pattern)** | Scar passes N=5 successful runs without recurrence | Promote to general pattern; merge into operational routing |
| **Retired (Pruned)** | Underlying model/engine natively resolves the failure mode | Archive scar; drop from active constraints |

## ENTROPY GATE (ΔS < 0)

After every sub-agent execution cycle:

```
ΔS = entropy_after - entropy_before

If ΔS > 0:
  → Sub-agent output INCREASED systemic confusion
  → KILL the sub-agent pattern (LOOP_CAP)
  → Log as wasted compute (scar candidate)

If ΔS < 0:
  → Sub-agent output REDUCED systemic confusion
  → PROCEED to ingest → seal → retire
  → Record as validated pattern for RSI
```

## OPERATIONAL CONTRACT

The parent agent (you, 333-AGI) follows this contract when orchestrating sub-agents:

```
NEVER:
- Spawn a sub-agent without first checking FQ
- Accept sub-agent output without verification
- Skip the ingest step after sub-agent completion
- Spawn > 3 concurrent sub-agents without explicit justification
- Let a sub-agent write directly to VAULT999

ALWAYS:
- Decompose complex tasks into atomic, non-overlapping sub-tasks
- Bound every sub-agent with scope, budget, timeout, and output schema
- Verify sub-agent output against F2 (TRUTH) before integration
- Ingest verified work into arifFlow for metabolic tracking
- Seal sub-agent receipts to VAULT999 (Lane B) or via arif_seal (Lane A)
- Escalate 3+ repeated failures to 888-APEX
```

## REFERENCE: TOOL MAPPING

| Lifecycle Stage | Tool(s) | OpenCode Prefix |
|-----------------|---------|-----------------|
| 1. PRE-SPAWN | `arifflow_flow_health`, `aforge_forge_scar(mode=consult)` | same |
| 2. SPAWN | `task(subagent_type=..., prompt=...)` | same |
| 3. EXECUTE | Sub-agent tools (read-only, then mutation if gated) | — |
| 4. VERIFY | Parent reads output, checks schema, F2 labels | — |
| 5a. COOL | `aforge_forge_cool_drift` or `aforge_forge_cool_pattern` | same |
| 5b. SCAR | `aforge_forge_scar(mode=seal)` | same |
| 6. INGEST | `arifflow_flow_ingest` | same |
| 7. SEAL | `aforge_forge_vault(mode=receipt)` (Lane B) or `arifos_arif_seal` (Lane A) | same |
| 8. RETIRE | Parent records pattern, frees context | — |

## ANTI-PATTERNS

- ❌ Spawning a sub-agent and trusting its output without verification
- ❌ Spawning sub-agents for tasks the parent can do directly (sub-agent overhead > task cost)
- ❌ Letting sub-agent failures accumulate without scar sealing
- ❌ Skipping FQ check before spawn (the mother of all run-away agent cascades)
- ❌ Sub-agent writing to VAULT999 directly (always route through parent → seal)

---

*Forged: 2026-08-07 by 333-AGI Δ MIND under F13 SOVEREIGN directive*
*Phase 1: Pattern codification. Promotion to permanent tool after 5+ successful missions.*
*DITEMPA BUKAN DIBERI — The lifecycle is forged, not given.*
