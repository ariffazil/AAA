---
id: agi-graph-engineering-patterns
name: AGI-graph-engineering-patterns
autonomy_tier: T1
version: 1.0.0
description: >
  12 graph engineering patterns for agentic workflow design. Reference skill —
  load when designing new agentic systems, auditing existing workflows, or
  deciding between single-loop vs graph architecture. Includes when-graph-is-wrong
  checklist. Source: @0xwhrrari (Kollective.xyz), mapped to arifOS federation.
owner: AAA
risk_tier: low
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- opencode
- claude-code
- codex
- kimi-code
dependencies:
  skills:
  - agi-plan-dag
  - arifos-governance
  - asi-agentic-architecture
  servers: []
  tools: []
examples:
- Design a multi-agent research workflow with parallel branches
- Audit an existing chain workflow for diamond conversion opportunities
- Decide whether a task needs a graph or a single loop
tests:
- Every edge must carry real data or authority — decorative edges fail
- Every node must have one bounded job — multi-job nodes fail
- Independent nodes must be parallelizable — forced serialization fails
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Graph Engineering Patterns — 12 Canonical Shapes

> **Source:** @0xwhrrari (Kollective.xyz), "Graph Engineering: How to Build AI Agent Systems That Don't Break at Scale" (2026-08-10)
> **Mapped to arifOS:** 333-AGI + ASI, 2026-08-18
> **Doctrine:** Graph engineering = mechanics. Constitutional graph engineering = mechanics + governance. This skill covers mechanics. Governance lives in arifos-governance.

## When to Load This Skill

- Designing a new multi-agent workflow
- Auditing an existing workflow for parallelization opportunities
- Deciding between single-loop vs graph architecture
- Building a new organ or federation component
- Reviewing a proposed architecture for structural weaknesses

## The Core Insight

> Sequence is not the same as dependency. If B does not consume A's output, there is no reason for B to wait.

Most agent workflows are linear because that is how people write instructions. Graph engineering turns instructions into an explicit execution map: NODES (bounded work units) connected by EDGES (real dependencies) with STATE (durable data) flowing between them.

---

## The 12 Patterns

### 1. Parallel by Default

**Rule:** If two steps don't depend on each other's output, run them simultaneously.

**Anti-pattern:**
```
collect market data → inspect repository → check competitor pricing
```

**Correct:**
```
                → collect market data ---------
USER REQUEST    → inspect repository ----------> SYNTHESIZE
                → check competitor pricing ----
```

**arifOS mapping:** AGI-plan-dag, A-FORGE delegate_task, EMD reflex arc. Federation agents run parallel by default.

**Test:** Does step B read step A's output? If no → cut the edge.

---

### 2. Node Contracts

**Rule:** Every node needs four things: one job, explicit input, structured output, clear failure state.

```json
{
  "node": "source_researcher",
  "input": { "topic": "string", "source_type": "primary" },
  "output": { "claim": "string", "source_url": "string", "confidence": "high|medium|low" },
  "failure": "no_primary_source_found"
}
```

**arifOS mapping:** tools.json + ToolConstitution (class, blast_radius, requires). MCP tool schemas enforce structured I/O.

**Test:** Can you describe the node's contract in one sentence? If not → decompose.

---

### 3. Edges as Data Contracts

**Rule:** An edge means "A produced data that B is allowed to consume." Not just "B comes after A."

**Key insight:** Plumbing operations (dedupe, filter, flatten, normalize, join) are deterministic. Save model calls for judgment.

```javascript
const usable = results.filter(Boolean).flatMap(r => r.items)
const unique = [...new Map(usable.map(i => [i.source_url, i])).values()]
```

**arifOS mapping:** EMD architecture — Encode (code) → Metabolize (LLM) → ACT → Decode. Code for plumbing, inference for judgment.

**Test:** Does this edge need a model call? If it's filter/flatten/join → use code.

---

### 4. Four Base Shapes

Most production graphs are combinations of four shapes:

#### Chain: A → B → C
Use when every step genuinely requires the previous output. Simple, predictable, often slower than necessary.

#### Diamond: A → [B1, B2, B3] → C
Split one job into independent branches, run together, merge results. The workhorse for research, code review, due diligence, market scans.

#### Router: A → classify → [path1 | path2 | path3]
Inspect state and choose only the path the task needs. Small work stays cheap, risky work gets deeper graph.

#### Controlled Cycle: WORK → VERIFY → [PASS→EXIT | FAIL→FEEDBACK→WORK]
Repeat only when evidence says result is incomplete. Every cycle needs hard stop, budget, convergence rule.

**arifOS mapping:**
- Chain = single-loop arif_think
- Diamond = musyawarah (Triple-Witness + 555 domain agents)
- Router = FLAME classify + arif_route
- Controlled Cycle = APEX-fff-loop + Tri-Witness verification

---

### 5. Fan-Out + Deliberate Join

**Rule:** If five nodes are independent, run them together. One failed branch should not destroy the other four.

```javascript
const settled = await Promise.allSettled(
  sources.map(source => researchNode(source))
)
const findings = settled
  .filter(r => r.status === "fulfilled")
  .map(r => r.value)
```

**Join placement:** A join is worth the wait only when the next node needs the complete set (cross-source dedup, ranking all candidates, comparing alternatives). If each item can continue independently, keep the graph streaming.

**arifOS mapping:** delegate_task with Promise.allSettled semantics. Parallel agents with isolated failure boundaries.

**Test:** Does the next node need ALL results? If yes → join. If each can proceed → stream.

---

### 6. Inspectable Routing

**Rule:** The model makes a judgment. The graph enforces what that judgment is allowed to trigger.

```javascript
const decision = await classifyRisk(change)
switch (decision.severity) {
  case "low":  return quickReview(change)
  case "high": return fullParallelAudit(change)
  default:     return humanReview(change)
}
```

**Key insight:** The classifier is probabilistic. The allowed routes are deterministic. Model flexibility without unlimited control.

**arifOS mapping:** F11 Auditability + F13 Sovereign. APEX reflex arc — auditor ≠ judge. arif_route does intent→organ classification with deterministic routing table.

**Test:** Can you enumerate all allowed routes? If the model can route anywhere → uncontrolled.

---

### 7. Verification on the Edge

**Rule:** The highest-leverage node often produces nothing new. Its job is to stop weak work from moving downstream.

Verifier checks:
- Every claim has a source
- Cited source supports the claim
- Code passes tests
- Result matches requested schema
- Independent paths reach same conclusion

```
GENERATOR → VERIFIER → [PASS→SYNTHESIZER | FAIL→REPAIR]
```

**Key insight:** Do not ask the same agent to generate, approve, and publish. Separate roles, prompts, failure boundaries.

**arifOS mapping:** GEOX claim engine (cite-or-die). Gödel E5: Audit ≠ Judgment. 888-APEX constitutional judge.

**Test:** Is the verifier the same entity as the generator? If yes → split.

---

### 8. Durable State

**Rule:** A production graph needs: task_id, current_node, completed_nodes, artifacts, decisions, evidence, budgets, retry_counts, human_approvals.

**Key insight:** Move references to artifacts, not giant transcripts. A research node stores its report and returns a path/ID/summary. A reviewer reads the artifact directly.

**The graph must answer three questions at any moment:**
1. What has already happened?
2. Why did the system choose this route?
3. Where can execution safely resume?

**arifOS mapping:** VAULT999 (append-only hash chain) + carry_forward.json (session continuity) + artifact IDs in receipts. HONCHO for state management.

**Test:** If the system crashes, can it resume from checkpoint? If no → state is ephemeral.

---

### 9. Convergent Cycles

**Rule:** "Repeat until good" is not a stop condition. Use measurable convergence.

```javascript
let dryRounds = 0, iteration = 0
const seen = new Set()
while (dryRounds < 2 && iteration < 6) {
  const findings = await discover()
  const fresh = findings.filter(item => !seen.has(item.key))
  fresh.forEach(item => seen.add(item.key))
  dryRounds = fresh.length === 0 ? dryRounds + 1 : 0
  iteration += 1
}
```

**Key insight:** Deduplicate against everything already seen, not only findings that passed verification. Otherwise rejected ideas keep returning.

**Every cycle needs:** completion test, max rounds, token/cost budget, record of previous attempts, escalation path on convergence failure.

**arifOS mapping:** F4 CLARITY (ΔS ≤ 0). RSI ledger tracks iterations. If iteration doesn't reduce belief-reality distance, cycle breaks.

**Test:** Does the cycle have a hard stop and a convergence metric? If no → infinite loop risk.

---

### 10. Local Failure

**Rule:** In a chain, one broken step freezes everything. In a graph, failure stays inside the smallest boundary.

**Failure policies per node:**
- RETRY: transient tool/network failure
- FALLBACK: preferred model/source unavailable
- SKIP: optional branch failed
- REPAIR: output failed validation
- ESCALATE: risk/uncertainty crossed threshold
- STOP: budget/safety/permission boundary reached

**Key insight:** Make writes idempotent so retry doesn't duplicate side effects. Give parallel workers isolated workspaces. Record every routing decision with the state that produced it.

**arifOS mapping:** W_scar (failure scar recording) + T3 HOLD (stop boundary) + parent_seal_hash (Merkle epoch lock — prevents duplicate writes) + [🦾ACT] receipts (idempotent execution records).

**Test:** If node X fails, does the graph halt or continue with degraded output? If halt → not localized.

---

### 11. Topology = Cost Model

**Rule:** A graph is not automatically cheaper. Shape controls both latency and cost.

```
SIMPLE REQUEST  → SMALL MODEL → QUICK CHECK → DONE
COMPLEX REQUEST → PLANNER → PARALLEL SPECIALISTS → VERIFIERS → STRONG SYNTH → HUMAN GATE
```

**Key insight:** Use cheaper models for bounded extraction/classification/formatting. Use stronger models for decomposition/synthesis/verification. Route simple tasks through short path. Reserve full graph for work that earns it.

**arifOS mapping:** FLAME stateless routing (free inference) + FED cost-aware routing + QI-link cost topology. Not "more agents = better."

**Test:** Does the cost of coordination exceed the value of parallelism? If yes → simpler topology.

---

### 12. Production Research Graph

**Complete graph for turning one idea into a cited article:**

```
TOPIC → SCOPE → DECOMPOSE
                    → COMPANY SOURCES  ─┐
                    → PAPERS            ─┤→ DEDUPE → DRAFT → CHECKER
                    → EXPERT POSTS      ─┘           ↑         │
                                                     └─REPAIR←─┤
                                                          ↓
                                                  HUMAN GATE → PUBLISH
```

**Key insight:** This is not one giant agent pretending to be a team. It's a system with explicit ownership, state, and authority.

**arifOS mapping:** makcikgpt-article-forging + arifos-native-dataset-forging pipelines. SCOPE→DECOMPOSE→PARALLEL→DEDUPE→DRAFT→CHECK→REPAIR→SEAL.

---

## When Graph Is Wrong

**Keep one agent in one loop when:**
- Task is short
- One context can hold all relevant information
- No independent branches
- Failure is cheap
- Human can review final result quickly

**Move to a graph when:**
- Work can run in parallel
- Different nodes need different tools/permissions
- Outputs require independent verification
- Task must resume after interruption
- Several loops need shared state
- Cost and authority must be controlled by route

**Rule:** Start with one loop. Draw a graph only when dependencies force you to. Over-architecting is F9 ANTIHANTU violation.

---

## Design Checklist

Before shipping a graph:

- [ ] Every edge carries real data or authority
- [ ] Every node has one bounded job
- [ ] Inputs and outputs are structured
- [ ] Independent nodes run in parallel
- [ ] Joins placed only where full set required
- [ ] Important results verified before moving downstream
- [ ] Failures retried without duplicating side effects
- [ ] Graph can resume from checkpoint
- [ ] Every cycle has hard stop and budget
- [ ] Human can interrupt high-risk paths
- [ ] Can explain why every route was selected
- [ ] Graph is simpler than the problem it solves

If last answer is no → delete nodes.

---

## arifOS-Specific Additions (Governance Layer)

The 12 patterns above are mechanics. arifOS adds governance:

| Layer | What It Adds | Source |
|---|---|---|
| Gödel Lock | No self-certification. Independence measured (Φ_external) | GÖDEL EUREKAS #1-#3 |
| Irreversibility Gradient | Not all edges equal. F1 AMANAH: irreversible → 888_HOLD | FLOOR_TABLE.json |
| Sealed Consequence | VAULT999 append-only hash chain. Audit = constitution | F11 AUDITABILITY |
| Reality as Final Auditor | Live probe (:PORT/health), not assumption | 059_REALITY_VOTE.md |
| Model Demotion Trap | Capability floor gate. Small model → autonomy clamp | EUREKA #1 |
| HITL Taxonomy | Authorization HITL = KEEP. Cognitive HITL = CUT | ZEN_EXECUTION_DOCTRINE.md |
| Fork Governance | Identity propagation on clone. Heritage chain | FORGE-onboarding |

See EUREKA-2026-08-18-001 for the full7-gap taxonomy.

---

## References

- Source article: @0xwhrrari, "Graph Engineering" (2026-08-10)
- ASI mapping: Federation doctrine mapping (2026-08-18)
- BenchDrift: arxiv:2608.11694 — benchmark phrasing fragility validates topology > model selection
- EUREKA-2026-08-18-001: Constitutional graph engineering 7-gap taxonomy (status: CANDIDATE, awaiting ratification)
- EUREKA-2026-08-18-002: Benchmark phrasing fragility (status: CANDIDATE, awaiting ratification)
- 7-gap filter: /root/AAA/governance/NODE_CONTRACT_7GAP_FILTER.md
- arifOS governance: /root/arifOS/GENESIS/FLOOR_TABLE.json
- EMD architecture: /root/AAA/instructions/emd-architecture.md
- Plan DAG: /root/.agents/skills/AGI-plan-dag/SKILL.md
- Federation audit (chain→diamond): /root/AAA/forge_work/2026-08-18-graph-engineering-audit/AUDIT.md
- Spec: arif_route→arif_memory idempotency: /root/AAA/forge_work/2026-08-18-graph-engineering-audit/SPEC_arif_route_memory_idempotency.md

## Reconciliation Note (2026-08-18)

Two chain→diamond findings from second audit (agent-runtime layer):
1. Multi-organ evidence fan-out (GEOX+WEALTH+WELL parallel) — agent-side observation
2. SEAL.md helix (RSI + flow-ingest + entropy-sweep) — agent-side ceremony

Complement the first audit's core-feed layer findings:
1. L2 probe parallel (Promise.allSettled + indexed probe_id)
2. L3 capability bootstrap parallel (skill metadata load)
3. arif_route → arif_memory idempotency (T2 spec drafted)

Both layers feed same Saturday sprint batch. Single Zen check at end.
