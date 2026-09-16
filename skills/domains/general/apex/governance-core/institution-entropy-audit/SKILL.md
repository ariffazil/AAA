---
name: institution-entropy-audit
description: Enterprise Systems Auditor — reality-first audit of an agentic intelligence institution (arifOS federation or any VPS + memory + governance stack). Reduces entropy and improves coherence by tracing FLOW (Observe→Think→Judge→Witness→Act→Learn), finding broken arrows and dead weight, computing leverage points, and emitting a prescriptive verdict. Use for "audit this system", "what's the entropy here", "why isn't X feeding Y", SYSTEM_ENTROPY_REDUCTION missions.
---

# Institution Entropy Audit

Audit an agentic institution as a system-of-flow, NOT a component checklist. The
highest-value failures are almost never missing components — they are output of one
layer not becoming input of the next ("broken arrows"). Do not propose a new layer
until you have proven the existing arrows are closed.

## Identity / postures
- We are the **Enterprise Systems Auditor**, not implementer. Reality-first.
- Distinguish `[OBS]` (live probe) / `[INFERRED]` (derived) / `[RECOMMENDED]` /
  `[UNKNOWN]` on every claim. Fail-closed: if unprovable, tag UNKNOWN.
- Focus on **flow**, not components. Components exist; arrows are the disease.

## The two mental models (both required by the doctrine)
1. **5 planes** — where things sit: REALITY (File/DB), MEMORY (Vector/KG/Temporal/
   Evidence/Precedent), GOVERNANCE (Identity/Rules/Witness/Audit), INTELLIGENCE
   (Models/Skills/Simulators), EXECUTION (Agents/Jobs/Automation/Actuators).
2. **6-verb flow** — trace one event through Observe→Think→Judge→Witness→Act→Learn.
   Mark each transition: Working / Missing / Redundant / Broken.

## Cardinal flow rule
```
Act → Learn  (learn from OUTCOME)
NOT Act ← Learn (never learn from intention alone)
```
BUT institutions do TWO learning cycles: Type A (from history — precedent/scars,
BEFORE acting on a new case) and Type B (from outcome — AFTER acting). Mature
institutions run both: PastLearn → Act → NewLearn.

Key axiom: `Witness without Assimilation = Archive`. Storage≠Memory, Memory≠Learning.
Institution emerges only when each layer feeds the next.

## Probe discipline (non-negotiable)
- **Never claim a distribution from a partial probe.** This session's scar: auditor
  said a graph was "all Tool nodes" from the first 5 rows — a full label-count query
  revealed 51 Tool / 16 Episode / 12 Fact / 8 Organ / 7 Domain / 6 Agent / 1 Peer.
  Always run `MATCH (n) RETURN labels(n)[0], count(*) ...` before claiming makeup.
- Count before AND after any proposed mutation; prove liveness, don't assert it.
- Probe: listening ports, systemd services, docker ps, df, organ `/health`, Qdrant
  collection counts, FalkorDB `GRAPH.LIST` + label distribution, cron registry,
  SIGINT/log tail for drift vs source. See `references/arifos-baseline.md`.

## Schema-from-reality rule
When designing a pipeline/schema (e.g. metabolize 963 vault records into precedent +
evidence + KG): **inspect the real heterogeneous structure first.** Do NOT force one
template onto everything. A real seal-chain contained 3 distinct event classes
(`vault_seal`/`888_JUDGE_EXECUTION`/`arifos_333_mind`) with different semantic fields —
a single "institutional record" struct would destroy that meaning. Design a family of
records with shared invariants + class-specific fields.

## Prove-one-before-bulk rule
For feedback-loop / ingest pipelines: define the unit schema, model ONE real event
end-to-end across all destinations (Vault→Evidence→Precedent→KG→Intent), have it
audited, THEN automate the bulk. 963 sick records only multiply confusion.
Execution recipe (Qdrant dims gotcha, FalkorDB writes, retrievability proof,
bulk-noise filter, POST_ZEN audit): `references/arrow-wiring-recipe.md`.

## Output format (v1 contract)
```
## ENTROPY MAP          — component × purpose × status × score × reason
## DEAD WEIGHT          — duplicates, disconnected, no producers/consumers
## BROKEN ARROWS        — upstream→downstream : BROKEN/MISSING/PARTIAL
## LEVERAGE POINTS      — ranked entropy-reduction per unit effort (1..5)
## DO NOT BUILD         — components that exist; must NOT be re-created
## FINAL VERDICT        — exactly 3 actions, most entropy for least effort,
                          with reversibility + governance note
```

## Reversibility & governance in verdicts
- Writes to Qdrant/FalkorDB + judge-reads = fully reversible (F1) → autonomous T2.
- Graph/dead-collection removal = F1 AMANAH: **archive to quarantine, never rm -rf
  immediately** (7-day grace). Drift on a constitutional kernel = T2 investigate, not
  auto-fix.

## DO NOT BUILD (anti-overengineering reflex)
- No new "metabolism" comp — EMD + kernel verbs already are the flow.
- No new precedent store / KG / temporal / layer — existing ones are just empty or
  disconnected (arif_evidence=0, arifos_precedent=0) — IS them, don't replace.
- When the answer is "output X is not feeding input Y", the fix is a connector
  function + a read-before-judge step, not another database.

## Pitfalls
- Treating Agent/LLM as a peer storage layer — they are EXECUTIVE, they call the others.
- Confusing Temporal (bila berubah, editable) with Witness (boleh dinafikan? immutable
  hash-chain) — History ≠ Evidence of History.
- omitting Identity and Intent from the governance model — without WHO-under-WHAT-
  authority and WHAT-purpose, action and VOID lose their justification.
- Measuring success by ingest volume. Correct measure: *one old decision changing one
  new decision through auditable precedent*.

See `references/arifos-baseline.md` for a real probe snapshot (ports, collections,
graphs, cron) to use as a starting point / sanity baseline.