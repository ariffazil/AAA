# A-FORGE RSI — State Vector + Loop Diagram

```yaml
plan_id: AF-RSI-SV-2026-09-15-001
status: MEASURED — exhale empirically dead, state vector corrected
mutation: NONE
authority: ARIF / F13 SOVEREIGN
layer: A-FORGE (execution) + arifOS (judgment) — 333-AGI synthesis only
date: 2026-09-15
refs:
  - Oppenheim/Willsky/Young, Signals and Systems (1983/1997)
  - A-FORGE docs/ARCHITECTURE.md (dfd08fb0, 2026-07-19 — "zen: move root-level docs to docs/")
  - A-FORGE docs/CONSTITUTION.md
  - A-FORGE docs/RSI_BOOT_PROMPT.md (RSI 9-stage, BOOTSTRAP_ONLY)
  - Zen synthesis R ∉ S (2026-08-14)
  - Pipeline ≠ Loop (F13, 2026-09-10)
  - Capability Evolution Ecosystem (F13, 2026-09-10)
  - Temporal Intelligence Doctrine
  - A-FORGE repo HEAD: c7632cd9 (2026-09-15)
```

> Informational draft. Does not mutate kernel, constitution, evaluator, or production state.
> DITEMPA BUKAN DIBERI.

---

## 0. Stability precondition

**R ∉ S** — the reference (floors, intent, F13) is NOT a member of the state the loop
rewrites. If R ∈ S, the loop modifies its own target and stability is undefined. This
is not a design preference; it is the mathematical stability condition from the Zen
synthesis (2026-08-14). 888_HOLD enforces R ∉ S at the slow→meta boundary.

---

## 1. Bind order

**First organ: A-FORGE execution traces.**

| Rank | Organ | Why |
|---|---|---|
| 1 | **A-FORGE execution traces** | Only organ that mutates production state. Characterize `Imp` before attaching to any plant. Signal is discrete, timestamped, already instrumented (tool receipts, session traces, 888_HOLD queue, VAULT append). Failure here writes **wrong policy**, not wrong geology. |
| 2 | GEOX traces | Cleanest Nyquist story (physical bandwidth). COMPUTE_ONLY. Aliasing invents geology; does not rewrite governance. Second as the physical sampling-truth reference. |
| 3 | ARIF Cell civic pulses | Highest noise, slowest rate, no stable source yet, F13-heavy. Last. |

RSI in this federation = **governed system improvement** (docs, tests, architecture,
safety boundaries, observability) — not autonomous self-modification
(`RSI_BOOT_PROMPT.md`). This draft stays inside that definition.

---

## 2. State vector s_t

Minimal compression of history sufficient for the next lawful action.
If a field cannot be written, the run is a transcript, not an agent.

### A. Identity + authority (does not decay)

| Field | Source of truth | Notes |
|---|---|---|
| `session_id` | A-FORGE session / MCP session | Episode key |
| `actor_id` | declared actor | unverified → no meta-loop write |
| `lease_id` / SCT | arifOS lease | no lease → no execute |
| `plan_id` | planner / AREP | required before mutate |
| `verdict` | arifOS only | SEAL / PARTIAL / HOLD / SABAR / VOID |
| `floor_scope` | GovernanceBridge | F1–F13 hit-map for this run |
| `ratification_status` | F13 | `pending` / `HOLD` / `ratified` |

### B. Plant state (the work being done)

| Field | Source | Decay |
|---|---|---|
| `intent` | IntentRouter | per-task |
| `canonical_stage` | 111→222→333→555→666→777→888→010→999 | per-step |
| `evidence[]` | observe/fetch receipts | labeled OBS / DER / INT / SPEC |
| `hypotheses[]` | planner / critique | open / confirmed / abandoned |
| `tools_invoked[]` | ToolRegistry | per-call |
| `reversibility_score` | PlanValidator | gate input to ApprovalBoundary |

### C. Memory state (impulse response h)

| Store | Module | Persistence | Write loop |
|---|---|---|---|
| Working window | `ShortTermMemory.ts` | session; evicts to LTM | FAST |
| Long-term archive | `LongTermMemory.ts` | file-backed | MEDIUM |
| Tool-call receipts | Supabase `arifosmcp_tool_calls` | durable | FAST/MEDIUM |
| Session traces | Langfuse | durable | FAST |
| Escalation records | VAULT999 (888_HOLD only) | immutable append | MEDIUM |
| Federation telemetry | Prometheus / Grafana | time-series | FAST |
| Cooling receipt | RSI stage 9 | durable, non-authorizing | SLOW |

**Impulse-response question (open):** how many sessions does one HOLD, one failed gate,
or one sealed fix remain causally active in routing / tool choice / budget? Unknown →
h is unmeasured. Until measured, the system is ungoverned per the book's own definition.

**Operationally:** h[n] is the retrieval curve — for a decision at step n, which prior
events at n-k causally influenced the output. Currently shaped by embedding similarity
and recency bias (retrieval heuristics), not by deliberate design. The binding must
measure h empirically by tracing which scars, transitions, and claims from how far
back were retrieved and weighted.

### D. Controller state (Imp) — SLOW/META only

| Field | Meaning | Who may write |
|---|---|---|
| `bottleneck` | exactly one diagnosed constraint | propose: 333; seal: arifOS |
| `fix` | installed change + reversible? | A-FORGE after SEAL |
| `entropy_delta` / cooling | what changed, what did not | RSI stage 9 |
| `Imp_version` | improvement policy pointer | META + F13 only |
| `evaluator_id` | what scores "better" | META + F13 only |

A-FORGE **does not own** `Imp_version` or `evaluator_id`. These are META-layer
fields. Writing them without F13 is a constitutional violation, not a bug.

---

## 3. Four loops — timescales (do not mix)

```
FAST    AgentEngine tool loop          per tool call / turn     writes: receipts, STM
MEDIUM  session persist                per task / session       writes: LTM, traces, HOLD records
SLOW    RSI VERIFY → WITNESS → COOL    per session boundary     writes: cooling receipt after SEAL
META    Imp / evaluator / floors       F13 ONLY                 writes: Imp, evaluator, constitution
```

Mixing timescales is how recursive systems eat themselves.

---

## 4. Loop diagram

```
  R ∉ S:  R (floors, intent, F13) is NOT a member of S (state the loop rewrites).
  If R ∈ S → loop modifies its own target → stability undefined.

                          R  (reference: floors, intent, F13)
                          │
                          ▼
  ┌────────────────────────────────────────────────────────────┐
  │   C — controller (Imp)                                     │
  │   diagnose → remediate → zen-margin gain                   │
  │   slow loop: writes skills/ledger @ /seal                  │
  │   meta loop: edits Imp — F13-GATED, 888_HOLD               │
  └────────────────────────────┬───────────────────────────────┘
                               │ u_t  (action / fix)
                               ▼
          ┌──────── INHALE ─────────────────────────────────────┐
          │                                                     │
          ▼                                                     │
  ┌────────────────────────────────────────────────────────────┐│
  │   P — plant (agent doing work)                             ││
  │   AgentEngine: observe → encode → improve → verify         ││
  │   y_t = T(x_t ; θ, M, H)                                   ││
  └────────────────────────────┬───────────────────────────────┘│
                               │ y_t  (output)                  │
                               ▼                                │
  ┌────────────────────────────────────────────────────────────┐│
  │   Eval — e_t = Eval(y_t, r_t)                              ││
  │   causality: only info ≤ t  (no lookahead)                 ││
  │   INDEPENDENT observer required (FRAME :18085)             ││
  │   Self-eval degenerates into recursive hallucination       ││
  └────────────────────────────┬───────────────────────────────┘│
                               │ e_t  (error / bottleneck)      │
                               └────────────► C  (feedback) ────┘
                                              │
          ┌──────── EXHALE ───────────────────┘
          │  Pipeline ≠ Loop (F13, 2026-09-10):
          │  exhale closes the cycle.
          ▼
  ┌────────────────────────────────────────────────────────────┐
  │   CORRECTION APPLIED → reality RE-TESTED → new WITNESS     │
  │   emitted → receipt written → h updated                    │
  │                                                            │
  │   NOTE: "Tak flow lagi" (F13, 2026-09-10) applies to the  │
  │   SKILL-LEVEL rsi-ledger (5-phase, 82% heartbeat, 0 applied)│
  │   NOT to the 9-stage RSI_BOOT_PROMPT, which has exhale in │
  │   stages 6-9. Measurement (2026-09-15):                    │
  │     seal_chain: 264 entries, 167 SEAL, 57 HOLD             │
  │     WITNESS event type: 0 entries (never fired)            │
  │     COOL receipts: 1 test receipt (2026-07-13)             │
  │     EXECUTE (stage 6): active (167 seals)                  │
  │     VERIFY (stage 7): implicit in SEAL verdicts            │
  │     WITNESS (stage 8): does not fire                       │
  │     COOL (stage 9): pipeline wired, exhale never landed    │
  └────────────────────────────────────────────────────────────┘

   State s_t feeds both P and C (memory, scars, deltas, h).
   R is read by C but NEVER written by any loop.
```

Closed loop: Y = (C·P / (1 + C·P)) · R. Unstable iff loop gain C·P encircles −1.

---

## 5. Where 888_HOLD sits

888_HOLD is anti-windup AND R ∉ S enforcement at three sites:

1. **ApprovalBoundary** — irreversibility gate (already in the 4-layer forge gate; do not reorder)
2. **VERIFY → SEAL** — no witness without tests/invariants
3. **SLOW → META** — no write to Imp, evaluator, or floors without F13

Removing any = unbounded integrator + R ∈ S = predicted divergence, not emergence.

---

## 6. Sampling discipline (Nyquist)

Each loop must sample ≥2× the bandwidth of the phenomenon it governs.
Actual bandwidths are unknown — must be measured during binding:

| Loop | Current rate | Unknown bandwidth | Risk if wrong |
|------|-------------|-------------------|---------------|
| Fast | per tool call | execution-state change rate | Low — discrete events |
| Medium | per session | sub-task failure oscillation | Medium — intra-session thrash aliases |
| Slow | per seal | governance pattern drift rate | High — slow drift invisible at seal cadence |

Measurement protocol: log transitions with wall-clock timestamps, compute the dominant
frequency of state changes, verify sample rate > 2× that frequency. If not, increase
sample rate or accept the alias and mark the metric UNVERIFIED.

---

## 7. Empirical holes (poles not yet measured)

These are the measurement backlog — not blockers, but conditions that must be resolved
before `Imp_version` can be raised:

| # | Hole | Why it matters | How to measure |
|---|------|---------------|----------------|
| 1 | Impulse response h of a HOLD | How long one HOLD biases routing | Trace retrieval of HOLD records across N sessions |
| 2 | Gate passes vs gate failures visibility | Success-mode aliasing — if passes aren't logged, h is biased toward failure memory | Audit ApprovalBoundary log completeness |
| 3 | Prometheus scrape vs act-loop rate vs WELL 5-min host sample | Three different clocks — which is Nyquist for what? | Timestamp comparison across all three |
| 4 | STM eviction vs task horizon | Context windup — eviction before task completion loses state | Measure eviction timing vs task duration |
| 5 | MEMORY:51002 status | Part of s_t may be undefined | Probe liveness |
| 6 | Cooling receipt (RSI stage 9) | Is it wired or inhale-only? | Trace one full RSI cycle end-to-end |
| 7 | forge_experience_trace actual call rate | Declared but dead is a known failure mode (metabolism cron) | grep call sites + check Langfuse for recent entries |
| 8 | ShortTermMemory.ts / LongTermMemory.ts existence | Are these files or architectural names? | file probe |
| 9 | Independent Eval availability for A-FORGE | FRAME exists at :18085 but does it observe A-FORGE executions? | Probe FRAME /frame/probe for A-FORGE data |
| 10 | carry_forward read-side retrieval curve | h shaped by heuristics, not design | Trace which carry_forward entries influence a decision |
| 11 | FQ aliasing at arifFlow cron rate | May alias a weekly governance cycle into a daily signal | Compare FQ time-series at daily vs weekly resolution |
| 12 | Decay Watcher half_life enforcement | Claims carry half_life but is it enforced? | Audit claim expiry logic |

---

## 8. What "next" means concretely

1. **F13 ratifies bind order + measurement schema** — accept or reject A-FORGE first.
2. **If ratified: read-path inventory** — verify that the stores in Section 2C actually
   produce the fields the state vector names. Do NOT claim the state vector is live
   until every field has a verified source.
3. **Measure one h** — pick a recent A-FORGE execution decision, trace which prior
   events were retrieved and weighted. One empirical sample. Until you have it, h is
   a parameter you're optimizing blind.
4. **Audit hole #2 (gate pass visibility)** — if passes aren't logged as visibly as
   failures, h is biased and the loop is optimizing toward failure memory.
5. **Then** — and only then — wire the first empirical sample into the loop diagram
   and re-evaluate stability.

Test then seal. Never canonize before the falsification gate passes.

---

## 9. Boundary

Draft only. No kernel mutation, no deploy, no purchase. Ratification (F13) is required
before any live RSI loop writes persistent policy, evaluator, or constitution.

**Layer ownership:** arifOS judges; A-FORGE executes and logs; AAA displays; GEOX later;
333-AGI drafted, does not seal.

**Confidence:** High on bind order and HOLD topology (constitution/architecture). Medium
on live sample rates and module existence claims. Low on numerical loop-gain of the
LLM plant.
