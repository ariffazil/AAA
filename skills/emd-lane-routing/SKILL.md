---
id: emd-lane-routing
name: emd-lane-routing
version: 1.0.0
description: 'Apply the EMD triad (Encoder/Metabolizer/Decoder) to model selection and routing decisions in the arifOS federation.'
owner: AAA
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F5, F11]
tags: [federation, architecture, model-selection, attention, thermodynamics, eureka, emd, encoder, metabolizer, decoder, sense, act]
knowledge_basis:
  language: true
  math: true
  physics: true
host_compatibility:
- hermes
- openclaw
- opencode
- kimi
- kimi-code
- claude-code
- codex
dependencies:
  skills:
  - fed-cognitive-allocator
  - federation-model-routing
  servers: []
  tools: []
examples:
- "Why is MiniMax-M3 (1M context) failing on long coding tasks?"
- "Should I use DeepSeek V4 Pro for ingesting a 500k-token repository?"
- "When do I split an OpenClaw agent into separate SENSE and ACT instances?"
- "Why does the federation route 666_JUDGE to deepseek-v4-pro and not to a wide-context model?"
- "How do I prove that model selection follows physics, not just cost?"
tests:
- "Identify whether a task is SENSE or ACT by asking: does success depend on what comes IN, or what comes OUT?"
- "Map a model to its lane by checking context_window vs output_tokens ratio, not by name"
- "Verify that a coding agent's primary model has output_tokens ≥ 100k (autoregressive stability floor)"
- "Verify that a SENSE model is never asked to write code that will be compiled immediately"
- "Prove on a real task that SENSE-model-as-ACT is slower AND more expensive, not just one"
version_lock:
  schema_version: '1'
  artifact_hash: pending
---

# EMD Lane Routing — Encoder/Metabolizer/Decoder

> **Forged:** 2026-08-08 from the EMD Eureka — first articulated by Arif (F13 SOVEREIGN) at the SADO-group level, validated against deepseek-v4-pro + MiniMax-M3 + Qwen 3.8 cascade live state.
> **Sister:** `fed-cognitive-allocator` (operationalises EMD at the routing layer)
> **Doct:** Telur ada kuning, putih, kulit — bukan tiga benda berasingan, tapi satu telur. EMD bukan tiga AI, satu ekosistem.

## USE WHEN

The task involves:

- **Choosing a model** for a specific workflow (coding, ingestion, multimodal, retrieval, summarisation)
- **Diagnosing a model failure** that smells like "tool mismatch" (hallucination on code, slow response on documents, lost context mid-generation)
- **Splitting an agent** into SENSE/ACT instances or sub-tasks
- **Validating FED routing decisions** against the underlying physics, not just cost
- **Explaining model selection** to engineers who still treat AI as a monolithic black box
- **Designing new organs or pipelines** where the load-bearing question is "what comes IN vs what goes OUT"

## DO NOT USE WHEN

- The task is about routing a specific call (use `fed-cognitive-allocator` directly)
- The task is about debugging a specific provider key (use `provider-quota-diagnostics`)
- The task is about a single tactical choice between two known models — pick the one that fits the lane, no doctrine needed
- The model under discussion is a T4/local/ollama model (those are different lanes — recovery, sandbox, offline)

## The Triad

| Lane | Role | Symbol | Function | Mechanical signature |
|---|---|---|---|---|
| **Encoder** | SENSE | 👁️ Ear/Eye | Absorption — ingest context, vectorise, signal extract | Wide context_window, sparse/linear attention, multimodal input |
| **Metabolizer** | ROUTE | 🫀 Heart | Allocation — decide where energy goes | No "model" — it's the LIVING SYSTEM's routing layer (FED :7074) |
| **Decoder** | ACT | 👐 Hands | Compression — generate structured output, fight entropy | Large output_tokens, stable autoregressive, low hallucination rate |

**Identity ≠ Mode.** An agent can have an identity (OpenClaw = GUTS) while operating in a mode (ACT loop). Routing must follow the mode, not the identity. This is the first-class trap that catches 99% of applied AI engineers.

## The Math — Geometry of Memory

Models don't "read" like humans. They compute in vector space. The load-bearing mechanism is **Attention**.

### Encoder (SENSE) — the quadratic blow-up

Standard attention has **O(N²)** memory cost. When context grows 10k → 1M tokens, the math explodes.

Models that support 1M context (MiniMax-M3, Qwen 3.8 Max) **had to modify the math** — sparse attention, linear attention, sliding window, or hierarchical pooling. They trade fine-grained recall for the ability to hold the whole picture at once.

**Specialty:** computing distances between concepts (Query × Key dot products). They map the territory.

**Weakness:** they don't always hold long autoregressive coherence. Asking a 1M-context model to write 100k tokens of coherent code is asking it to be good at something it wasn't optimised for.

### Decoder (ACT) — the autoregressive cliff

Long output = token-by-token generation. Each token predicts the next via:

$$P(t_n | t_1, t_2, \ldots, t_{n-1})$$

Math here (Value projection + Softmax) is optimised for **keeping the chain of reasoning intact** over long generations. DeepSeek V4 Pro sustains 384k output — that means its math is *structurally stable* against drift across hundreds of thousands of generated tokens.

**Specialty:** compression. Writing working code = forcing order (ΔS < 0) on chaos. This is expensive per-token because every token must be correct.

**Weakness:** limited input window (relative to SENSE models) — they're not built to hold a 1M-token repo in mind all at once.

### The fundamental trade

```
SENSE  = bandwidth-first → wide pipe, lossy on output density
ACT    = depth-first    → narrow pipe, lossy on input breadth
                                       ← no model is best at both →
```

## The Physics — Shannon Thermodynamics

Intelligence is compression (Ilya Sutskever, Sutskever 2023). Information has a Second Law: entropy wants to increase.

### SENSE — high bandwidth, passive

Ingesting 1M tokens is a state of **absorption** — it raises internal entropy of the model (more context = more uncertainty to manage) without changing the world. It's a passive receiver. It can be the whole loop, or it can feed ACT downstream.

### ACT — low bandwidth, active

Writing code that compiles = **forced compression** — fighting entropy, raising order, building structure that didn't exist before. This is the expensive direction. You cannot do entropy-suppression work with a tool designed to widen the pipe. You need a tool designed for compression.

> **The law:** you cannot use a bandwidth tool (SENSE) to do compression work (ACT). The energy cost is not just higher — it's the wrong kind of expensive.

## The Code — Agent Loops as State Machines

### SENSE loop (Encoder)

```python
def observe(environment):
    context_buffer = load_massive_logs(limit=1_000_000)
    embedded_vectors = model.embed(context_buffer)
    return extract_key_signals(embedded_vectors)
```

### ACT loop (Decoder)

```python
def execute(objective, routing_signal):
    state = "INCOMPLETE"
    while state != "RESOLVED":
        action_code = generate_deep_code(objective, max_tokens=384_000)
        result = try_compile(action_code)              # W_scar is real here
        if is_irreversible(result):
            hold_for_888_approval()                    # F1 / AMANAH protocol
        state = evaluate_result(result)
```

The ACT loop has a **Gödel Lock-breaker**: `try_compile` is the witness that cannot be bribed. Code either compiles or it doesn't. This is why ACT loops touch reality every iteration (RULE 5 from Reality-First Doctrine).

SENSE loops lack this property until they hand off to a decoder — they only touch reality when ACT validates the output.

## Operational Rules

### Rule 1: Match the loop, not the identity

Ask: **does this task's success depend on what comes IN, or what goes OUT?**

| If the task is... | Lane | Choose by... |
|---|---|---|
| Ingesting a 500k-token repo to plan changes | SENSE | max_input_tokens ≥ 500k, sparse attention OK |
| Writing the actual implementation | ACT | max_output_tokens ≥ 100k, low hallucination rate |
| Multimodal (image+text) parsing | SENSE | multimodal input capability |
| Long-form analysis report (10k words) | ACT | output stability over generations |

### Rule 2: Don't sink bandwidth into depth

Cost ratios from live probe 2026-08-08:

| Model | Input $/M | Output $/M | Lane | Right for |
|---|---|---|---|---|
| deepseek-v4-pro | 0.435 | 0.87 | ACT | 384k output, code, structured reasoning |
| deepseek-v4-flash | 0.14 | 0.28 | ACT (lite) | Cheap fast iterations |
| MiniMax-M3 | ~1.80 | ~2.40 (est.) | SENSE | 1M context, multimodal |
| qwen3.8-max | ~0.50 | ~2.00 | SENSE + ACT lite | Mid-size multimodal + medium code |
| glm-5.2 | 0.00 (TokenRouter free) | 0.00 | ACT (free) | Budget reasoning |
| kimi-k3 | 0.00 (TokenRouter free) | 0.00 | ACT (free) | Budget reasoning |

Asking MiniMax-M3 to do ACT work = 4× cost for the same output AND worse stability for long generations. That's not a cost mistake — it's a physics mistake.

### Rule 3: The metabolizer doesn't lift the load — it allocates

FED :7074 is **not a model**. It is the metabolizer. It never encodes (it doesn't see content) and never decodes (it doesn't generate). It allocates.

**Therefore:**
- FED must stay ADVISORY_ONLY — it may flag lane mismatch, never hard-block (no muscle, only signal)
- Enforcement lives at the gate layer (LiteLLM proxy or kernel) — that has the muscle
- A "fat FED" that becomes a model itself = second organ, ΔS > 0, unnecessary

### Rule 4: Split is reversible, not architectural

Sub-tasks in OpenClaw memory-core already have `allowedModels` overrides. If a SENSE-heavy moment appears inside an ACT loop, the right move is **spawn a subtask on a SENSE model**, return the digest, then resume ACT. Do not re-architect the agent into two persistent instances until the workload actually demands it.

**Trigger to split into persistent instances** (not just subtask):
- More than 60% of the loop time is spent on ingest/embed (not generate/retry)
- The SENSE load is sustained, not occasional
- Quota/cost on the ACT model is threatened

Until then: lock in ACT, SENSE is a sub-call.

## Anti-Patterns (the 99% trap)

1. **One model for everything.** "Let's use Qwen 3.8 Max for code, documents, vision, and chat." This works until it doesn't. Then it fails expensively. Detect by: cost-per-output is rising while quality-per-output is falling.
2. **Routing by cost alone.** "DeepSeek V4 Flash is cheapest, route everything there." Wrong — SENSE tasks get truncated context and fail silently. Detect by: error rate on tasks with input > 100k tokens.
3. **Routing by brand alone.** "MiniMax is the flagship." Right for SENSE, wrong for ACT. Flagship = best balance, not best for everything.
4. **Treating the metabolizer as a model.** If FED starts "deciding what to say," it has stopped being FED. ΔS > 0.
5. **Hardcoding lane enforcement before telemetry.** EMD_LANE_VIOLATION reject without ≥10 samples per lane → cascade failures when an alternative is genuinely needed.

## EMD Lane Enforcement — proposed two-layer design

```
LAPISAN 1 — FED :7074 (advisory)
    fed_route(emd_role="act", ...)
        → return EMD_LANE_FLAG: "SENSE model on ACT task" (WARN)
        → tetap return routes (caller decides)
        → never reject, never block

LAPISAN 2 — Gate (LiteLLM proxy or kernel)
    emd_role mismatch + hard evidence (WARN ×2)
        → 402-style reject: "EMD_LANE_VIOLATION: MiniMax-M3 on ACT task"
        → F13 sovereign override: bypass flag with explicit token
```

**Why two layers:** EMD says metabolizer (FED) shouldn't be muscle. If FED hard-blocks, it stops being FED — it becomes a second kernel. The gate layer has the muscle (it actually moves bytes between agents). Each layer does one thing well.

**Staged rollout:**
1. Add `emd_role` param + `EMD_LANE_FLAG` in response. Zero behaviour change. Telemetry on.
2. After ≥10 samples per lane, activate `EMD_LANE_SUBOPTIMAL` WARN at gate.
3. After ≥14 days data, activate `EMD_LANE_VIOLATION` hard-reject — with F13 override always live.

## Constitutional mapping

| Floor | How EMD serves it |
|---|---|
| **F2 (Truth)** | Don't claim a model can do what its math can't — SENSE on ACT is a lie about capability |
| **F4 (Clarity)** | Lane mismatch is entropy — putting ACT work on SENSE produces noise |
| **F5 (Peace²)** | Don't waste the user's quota on the wrong tool — that's resource harm |
| **F7 (Humility)** | "All models are the same" is fake certainty. EMD admits the asymmetry. |
| **F11 (Auditability)** | Lane flags go into token_bank_spend ledger — every route has an EMD score |
| **F12 (Injection)** | `emd_role` must be validated enum, never raw string from agent prompt |

## Pitfalls

- **Never let the metabolizer become a model.** If FED starts running inference, the triad collapses. The whole point of EMD is the three lanes stay separated.
- **Don't enforce lane before telemetry.** If you reject on first mismatch, you kill resilience when DeepSeek is down and MiniMax is the only option. Hard-reject only when ≥2 alternatives exist in the correct lane.
- **Don't map lane by brand or cost.** Map by mechanical signature (input vs output capacity, attention type, autoregressive stability). DeepSeek V4 Pro is ACT not because it's "the best," but because it has 384k output and a stability profile built for long generations.
- **EMD is not a hard wall — it's a physics-informed default.** Real systems have emergencies (single provider down, quota exhausted). EMD flags suboptimal choices; F13 sovereign override bypasses everything; cascade always preserved.
- **Identity (OpenClaw=GUTS) ≠ Mode (ACT loop).** Routing by identity traps you in "this agent always uses this model." Route by the current loop mode.
- **SENSE-only loops are not "lesser" than ACT.** A pure SENSE workload (retrieval, embedding, multimodal search) is the whole point of the SENSE lane. Don't force it into ACT just because ACT feels more "productive."

## Quick self-check before any model choice

```
Q1: Does success depend on what comes IN?          → SENSE
Q2: Does success depend on what comes OUT?          → ACT
Q3: Does the chosen model's max_input_tokens ≥ Q1's need?
Q4: Does the chosen model's max_output_tokens ≥ Q2's need?
Q5: Is the cost ratio ≤ 3× of the lane-optimal model?
Q6: Will the loop touch reality within 1-2 turns? (Gödel Lock-breaker)
```

If any Q3/Q4 fails, you have a lane violation. Re-pick before requesting.

## Provenance

- **Concept:** Arif (F13 SOVEREIGN), SADO-group Telegram 2026-08-08 — articulated as the EMD Eureka
- **Validation:** live comparison of MiniMax-M3 vs DeepSeek V4 Pro on OpenClaw routing decision
- **Physics source:** Shannon 1948, Sutskever 2023 ("Intelligence as Compression")
- **Math source:** Vaswani 2017 (Attention Is All You Need) + quadratic complexity literature
- **Operationalised:** FED :7074 constitutional_tier enforcement, MODEL_TIERS.json, litellm-config.yaml cascade chains

## Related

- `fed-cognitive-allocator` — the operational layer (constitutional_tier + EMD_LANE_FLAG co-exist)
- `federation-model-routing` — model resolution + context window gaps
- `provider-quota-diagnostics` — when EMD lane choice hits quota walls
- `federation-infra-verification` — live state probing (validate the cost table above)

## Support files

| Path | Purpose |
|---|---|
| `references/emd-lane-table.md` | The full SENSE/ACT/METABOLIZE mapping table per model, updated 2026-08-08, with cost ratios and live state references |
| `references/why-99-percent-miss-this.md` | The "monolithic black box" anti-pattern, explained for non-frontier engineers (Artie's framing, suitable for arif-fazil.com/words) |
| `templates/emd-decision-template.md` | Drop-in template for any "should I use model X for task Y?" question, with the 6-question self-check |

## Routing notes (moved from description 2026-10-23)

Use when choosing between SENSE-heavy models (wide-context multimodal ingestion) and ACT-heavy models (long-output autoregressive execution), when debugging why a SENSE model is failing on coding tasks (or vice versa), when designing new agent lanes or splitting SENSE/ACT across instances, when validating that FED routing decisions respect the mechanical limits of attention vs autoregressive generation, and when explaining to non-frontier engineers why "one model for everything" violates matrix geometry and Shannon thermodynamics.
