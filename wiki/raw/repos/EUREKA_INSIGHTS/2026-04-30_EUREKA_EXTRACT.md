# EUREKA INSIGHTS — Extracted from /opt/arifos/src/

> Captured: 2026-04-30 | Source: Stale /opt/arifos/src/ mirrors being deleted
> Not embedded in: arifOS, A-FORGE, AAA, arif-sites canonical remotes

---

## 1. A-FORGE `fhs-clean-apply` Branch — AGENTS.md v2

**File:** `src/A-FORGE.git/fhs-clean-apply:AGENTS.md`
**Status:** More complete than current `/root/A-FORGE/AGENTS.md`

### Eureka insights:

- **Personal OS v2** — `src/personal-v2/PersonalOS.ts` with 6-verb interface: `remember`, `recall`, `track`, `think`, `hold`, `execute`
- **Memory Contract** — 5 tiers: `ephemeral → working → canon → sacred → quarantine` with `store/correct/pin/forget/downgrade/verify` actions
- **Context-Adaptive Thresholds** — F3/F7/F13 thresholds adapt based on `intentModel` and `riskLevel`
- **Human Expert Escalation** — `WebookHumanEscalationClient` sends 888_HOLD to external reviewers with full telemetry payload
- **PlanValidator** — DAG validation for acyclicity, reachability, phantom deps, depth/branching bounds
- **9-Agent Federation** — Named agent roles: APEX (sovereign), AAA-Agent (ASI), AUDITOR-Agent, VALIDATOR-Agent, ENGINEER-Agent, GEOX-Agent, WEALTH-Agent, ARCHIVIST-Agent, NOTIFIER-Agent

### Not in current root/A-FORGE:

```typescript
// Personal OS v2 not in root/A-FORGE yet
src/personal-v2/PersonalOS.ts
src/personal-v2/index.ts
src/personal-v2/README.md

// Governance F-floor implementations not in root/A-FORGE:
src/governance/f3InputClarity.ts
src/governance/f4Entropy.ts
src/governance/f6HarmDignity.ts
src/governance/f7Confidence.ts
src/governance/f8Grounding.ts
src/governance/f9Injection.ts
src/governance/f11Coherence.ts
src/governance/thresholds.ts  // context-adaptive

// Human escalation
src/escalation/HumanEscalationClient.ts
src/escalation/index.ts

// Memory contract
src/memory-contract/MemoryContract.ts
src/memory-contract/index.ts
```

### CLI command structure (more complete than root):
```
agent explore --goal "..." [--mode internal|external] [--cwd path]
agent fix --file src/file.ts [--issue "..."] [--mode internal|external]
agent test [--goal "..."] [--mode internal|external]
agent coordinate --goal "..." [--mode internal|external]
agent scoreboard [--period weekly] [--command explore|fix|test|coordinate]
agent operator approvals [--status <status>] [--sessionId <id>] [--riskLevel <level>]
agent operator vault [--verdict <verdict>] [--sessionId <id>]
```

---

## 2. A-FORGE `origin/main` — CLAUDE.md Workspace Layout

**File:** `src/A-FORGE.git/origin/main:CLAUDE.md`
**Status:** Has workspace-level overview not in root

### Eureka insights:

- **Shared MCP Launchers** — `.github/mcp/start-arifos-stdio.sh`, `start-GEOX-stdio.sh`, `start-playwright.sh`
- Shared server names: `arifos-local`, `GEOX-local`
- **Scientific terminology mappings:** sense=evidence acquisition, mind=reasoning, heart=safety review, judge=policy verdict, vault=immutable audit, forge=controlled execution
- **A-FORGE Commands** — Work from `A-FORGE/` directory

### Workspace layout table:

| Directory | Stack | Role |
|-----------|-------|------|
| `A-FORGE/` | TypeScript/Node.js 22+ | Agent runtime (Planner/Executor/Verifier, event store, policy engine) |
| `arifOS/` | Python 3.12+/FastMCP | Policy kernel (F1-F13 governance, MCP server, immutable audit path) |
| `GEOX/` | Python 3.10+ + React 19 | Geospatial domain service (seismic, well-log, governance verdicts) |
| `APEX/` | Docs only | Constitutional theory hub |
| `WORKFLOWS/` | Markdown | Autonomous workflow definitions (Subuh, Morning, etc.) |
| `VAULT999/` | Ledger | Immutable audit registry for sealed verdicts |

---

## 3. A-FORGE `docs/horizon-architecture` — README.md

**File:** `src/A-FORGE.git/docs/horizon-architecture:README.md`
**Status:** Architecture doc not in root

### Key framing:

> GEOX may witness. WEALTH may evaluate. WELL may reflect. arifOS judges. **A-FORGE orchestrates.**

"A-FORGE is the metabolic shell — display, orchestration, and execution surface"

---

## 4. AAA — ARIF-999-SEAL-RITUAL.md (v1.1)

**File:** `src/AAA/ARIF-999-SEAL-RITUAL.md`
**Status:** Full seal ritual with `seal_record` containing `blockers/scars/open_decisions/code_delta`

### Eureka pattern: 3-step seal ritual

1. **PREPARE** — Verify conditions, check blockers
2. **SEAL** — Write seal_record with blockers/scars/open_decisions/code_delta
3. **COMMIT** — Push to canonical repo

### Not yet in root/AAA:
- `ARIF-999-SEAL-RITUAL.md` full document
- `D4_SESAT_PROPAGATION.md`
- `F0_RATIFICATION_DECISION.md`
- `KERNEL_HASI_APEX.md`

---

## 5. arif-sites — llms.txt with Sovereign Identity

**File:** `src/arif-sites/llms.txt`
**Status:** Detailed human identity context (`Muhammad Arif bin Fazil`) not in any other repo

### Contains:

- Full identity core: Born May 22, 1990 (Bayan Lepas, Penang, Malaysia)
- Role: Anak Sulung (Eldest Son), Architect, Exploration Geoscientist, System Designer
- Cultural roots: Penang Malay (Loghat Utara), Queer + Melayu + Miskin
- Motto: "DITEMPA BUKAN DIBERI"
- Professional: 11 years PETRONAS, 100% drilling success rate, zero dry wells
- Key discoveries: Bekantan-1 (shallowest flowing oil), Puteri Basement-1, Lebah Emas-1

### Significance:

This is the **human context injection** — AAA's sovereign identity file. Should be preserved and possibly propagated to other repos as the canonical human context document.

---

## 6. arif-sites — ARIF.md Metabolic Kernel

**File:** `src/arif-sites/ARIF.md`
**Status:** Domain-specific ARIF.md instance for public web layer, not in root/arif-sites

### Key entry:

```
REPO_NAME: arif-sites
DOMAIN_ROLE: Public web presence — arif-fazil.com, geox.arif-fazil.com, mcp.arif-fazil.com
STABILITY_CLASS: MAINTENANCE
HARD_BLOCK: VPS offline → 502 on all subdomains
```

---

## 7. CI/CD — A-FORGE `fhs-clean-apply` GitHub Actions

**File:** `src/A-FORGE.git/fhs-clean-apply:.github/workflows/ci.yml`

### Eureka: Full test battery command list:

```yaml
- npm test
- node dist/test/PlanValidator.test.js
- node dist/test/confidence.test.js
- node dist/test/sense.test.js
- node dist/test/governanceViolation.test.js
- node dist/test/ticketStore.test.js
- node dist/test/operatorConsole.test.js
- node dist/test/operatorAuth.test.js
- node dist/test/thermodynamic.test.js
```

**Currently missing from root/A-FORGE workflow:**
- `governanceViolation.test.js`
- `operatorAuth.test.js`
- `thermodynamic.test.js`

---

## 8. A-FORGE Architecture — Governance Floors Status Table

**Source:** `fhs-clean-apply:AGENTS.md` (full table)

| Floor | Name | Location | Trigger | Verdicts | Status |
|-------|------|----------|---------|----------|--------|
| F3 | Input Clarity | `src/governance/f3InputClarity.ts` | Pre-execution | PASS, SABAR | ✅ Active |
| F4 | Entropy | `src/governance/f4Entropy.ts` | Per-tool | PASS, HOLD | ✅ Active |
| F6 | Harm/Dignity | `src/governance/f6HarmDignity.ts` | Pre+per-tool | PASS, VOID | ✅ Active |
| F7 | Confidence | `src/governance/f7Confidence.ts` | Post-execution | PASS, HOLD | ✅ Active |
| F8 | Grounding | `src/governance/f8Grounding.ts` | Per-tool | PASS, HOLD | ✅ Active |
| F9 | Injection | `src/governance/f9Injection.ts` | Pre-execution | PASS, VOID | ✅ Active |
| F11 | Coherence | `src/governance/f11Coherence.ts` | Post-tool batch | PASS, HOLD | ✅ Active |
| OPS/777 | Thermodynamic | `src/ops/ThermodynamicCostEstimator.ts` | Per-tool | PASS, HOLD, VOID | ✅ Active |
| F1 | Amanah | `ToolRegistry.runTool()` | Per-tool dangerous | 888_HOLD | ⚠️ Gate |
| F5 | Continuity | `src/continuity/ContinuityStore.ts` | Session | — | ⚠️ Outside governance |
| F13 | Sovereign | `AgentEngine` permission | Dangerous approval | 888_HOLD | ⚠️ Gate |
| F2 | Truth | `src/governance/index.ts` | — | — | ⏳ Stub |
| F10 | Privacy | `src/governance/index.ts` | — | — | ⏳ Stub |
| F12 | Stewardship | `src/governance/index.ts` | — | — | ⏳ Stub |

---

## Recommendations

### High-priority merge to canonical repos:

1. **A-FORGE `/root/`** ← needs governance floor implementations:
   - `src/governance/f3InputClarity.ts`
   - `src/governance/f4Entropy.ts`
   - `src/governance/f6HarmDignity.ts`
   - `src/governance/f7Confidence.ts`
   - `src/governance/f8Grounding.ts`
   - `src/governance/f9Injection.ts`
   - `src/governance/f11Coherence.ts`
   - `src/governance/thresholds.ts`
   - `src/escalation/HumanEscalationClient.ts`
   - `src/memory-contract/MemoryContract.ts`
   - `src/personal-v2/PersonalOS.ts`

2. **arif-sites** ← needs `llms.txt` with sovereign identity context

3. **AAA** ← needs `ARIF-999-SEAL-RITUAL.md`, `D4_SESAT_PROPAGATION.md`, `F0_RATIFICATION_DECISION.md`, `KERNEL_HASI_APEX.md`

### Low-priority (architectural reference only):

- `fhs-clean-apply` AGENTS.md — more complete than root, use as reference for rewrite
- `docs/horizon-architecture/README.md` — framing document for organism roles