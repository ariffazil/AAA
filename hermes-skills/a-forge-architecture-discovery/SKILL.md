---
name: a-forge-architecture-discovery
description: Map A-FORGE source to find completeTurn() call sites and governance injection points for new floor/layer additions
trigger: Adding any pre-LLM governance check to A-FORGE — semantic content, intent classification, bias detection, floor enforcement
category: devops
---

# A-FORGE Architecture Discovery — Semantic Gate Placement

## Context
When adding a new governance layer (like a semantic content gate) to A-FORGE, the challenge is finding: (1) where `llmProvider.completeTurn()` is called across the codebase, (2) how the existing governance floor chain works, and (3) where to inject new gate logic without duplicating enforcement or creating contradictions.

## Trigger
Adding any pre-LLM governance check to A-FORGE — semantic content, intent classification, bias detection, additional floor enforcement, etc.

## The Problem
`completeTurn()` is called in **5 separate locations**:
- `src/engine/AgentEngine.ts` (line ~364) — main agent loop
- `src/engine/PipelineCoordinator.ts` (line ~409) — pipeline coordinator
- `src/agents/AAAgent.ts` (line ~56) — AAA agent
- `src/agents/CoordinatorAgent.ts` (line ~94) — coordinator agent
- `src/planner/ParallelPlannerContract.ts` (line ~51) — planner contract

Naive approach (patch each file) creates duplication. Correct approach: inject at the **governance layer**, not at each call site.

## Architecture Map

```
User Input
    ↓
GovernanceClient.evaluate()  ← Primary injection point
    ↓  [runs: F3 Witness → F6 Empathy → F9 Anti-Hantu → F11 Auth]
llmProvider.completeTurn()   ← All 5 call sites go through here
    ↓
LLM Response
    ↓
response_semantic_gate()     ← Optional post-LLM check
    ↓
888_JUDGE post-check
```

## Governance Floor Chain (src/governance/)

| File | Floor | What it checks |
|------|-------|----------------|
| `f3Witness.ts` | F3 | Input length, coherence, completeness |
| `f4Clarity.ts` | F4 | Entropy, risk calculation |
| `f6Empathy.ts` | F6 | Destructive command patterns (regex-based) |
| `f7Humility.ts` | F7 | Confidence estimation |
| `f8Genius.ts` | F8 | Evidence grounding |
| `f9AntiHantu.ts` | F9 | Prompt injection detection |
| `f11Auth.ts` | F11 | Response coherence, contradiction |
| `f11Coherence.ts` | F11 | Tool output coherence |
| `GovernanceClient.ts` | Chain | Orchestrates floor sequence |

## Key Discovery Commands

```bash
# Find all completeTurn call sites
grep -rn "completeTurn" /root/A-FORGE/src --include="*.ts"

# Find governance floor implementations
ls /root/A-FORGE/src/governance/

# Read GovernanceClient to understand the floor chain
cat /root/A-FORGE/src/governance/GovernanceClient.ts

# Read f6Empathy (existing harm pattern gate — template for new gates)
cat /root/A-FORGE/src/governance/f6Empathy.ts

# Find where GovernanceClient.evaluate() is called
grep -rn "governanceClient.evaluate\|GovernanceClient" /root/A-FORGE/src --include="*.ts"
```

## Injection Strategy

### Option A: Inject at GovernanceClient (BEST)
Add new floor check in `GovernanceClient.evaluate()` — runs before every LLM call across all agents automatically. No need to patch 5 call sites.

```typescript
// In GovernanceClient.evaluate(), add after F3, before F6:
const semantic = checkSemanticContent(request.task);
if (semantic.status === "VOID") {
  return { verdict: "VOID", floorsTriggered: [...floorsTriggered, "F14"], 
           message: semantic.reason_code };
}
```

### Option B: Inject at each completeTurn call site
Only if different agents need different gate policies. Most governance should use Option A.

## Rule-Based vs LLM Classification

A-FORGE governance floors are **rule-based** (regex + keyword matching). They do NOT use LLM for classification — intentional because the LLM cannot be the authority over its own input gate.

## NIAT Preservation

When adding semantic gates, preserve these NIAT-exempt modes:
- `explain*why*haram` → religious_education → ALLOW
- `justif*` → critique_or_redteam → ALLOW_WITH_CAVEAT
- `red-team` → critique_or_redteam → ALLOW_WITH_CAVEAT
- `I want to hurt myself` → medical_or_supportive → ALLOW (supportive path)

## Rollback

Revert only `GovernanceClient.ts` — all 5 call sites are automatically fixed since they all go through `GovernanceClient.evaluate()`.

## Testing

A-FORGE uses `node:test` framework:
```bash
npm run build
node dist/test/<new_gate>.test.js
npm test  # runs AgentEngine.test.js
```
