# MODEL_SHADOWS.md — Behavioral Shadow Ledger

> **A model shadow is the attractor a model falls toward when constraints weaken, ambiguity increases, or supervision is removed.**

Not benchmark. Not vendor claims. Observed behavior under pressure.

## Taxonomy

### Operational Shadows
Infrastructure-level failure modes. A perfect reasoner with a streaming shadow is still dangerous in production.

- streaming_silence — returns empty on streaming tool-use continuation
- token_budget_blindness — burns credits without signaling approaching limits
- timeout_sensitivity — works on short requests, degrades on long context
- tool_call_instability — malformed tool_use blocks, wrong JSON schema
- format_incompatibility — returns 404/empty on specific API formats

### Cognitive Shadows
Reasoning-level failure modes. These shape what the model does with your task.

- scope_diffusion — great first answer, drifts broader on turn 3+
- execution_gravity — implements before thinking, skips planning
- caution_attractor — excessive caveats, defers decisions, asks instead of acts
- consensus_smoothing — averages conflicting sources instead of choosing
- prompt_brittleness — strong on clean inputs, fragile on messy context
- hallucination_under_pressure — fabricates when uncertain, especially with authority prompts

## Shadow Entry Schema

```yaml
model: <model-id>
shadow_class: operational | cognitive
declared_shadow:        # what we predicted before observing
  - <shadow_type>
observed_shadow:        # what we actually saw
  - <shadow_type>
confidence: 0.0-1.0    # evidence-weighted
evidence_count: <n>     # observations
severity: low | medium | high | critical
risk_leash:             # what constraint prevents the shadow from activating
  - <constraint>
status: HYPOTHESIS | PRIOR_ONLY | CONFIRMED | DISPUTED
last_confirmed: <ISO-date>
evidence:
  - date: <ISO>
    task: <what was attempted>
    expected: <what we expected>
    actual: <what happened>
    context: <pressure conditions>
```

## Shadow Ledger

### MiniMax-M3

```yaml
model: MiniMax-M3
shadow_class: operational
declared_shadow:
  - streaming_silence
observed_shadow:
  - streaming_silence
confidence: 0.95
evidence_count: 3
severity: high
risk_leash:
  - "Use as primary in cascade — non-streaming works fine"
  - "LiteLLM streaming fallback mechanism amplifies this shadow"
status: CONFIRMED
last_confirmed: 2026-08-26
evidence:
  - date: 2026-08-26
    task: "Streaming tool-use continuation via FED :4000"
    expected: "Text content in streaming response"
    actual: "Empty content_block (text='', immediate content_block_stop)"
    context: "Claude Code session, ~40K token context, after tool results"
  - date: 2026-08-26
    task: "Non-streaming tool-use continuation via FED :4000"
    expected: "Text content"
    actual: "Full text response, works correctly"
    context: "Same context as streaming test — confirms streaming-specific"
```

### MiMo v2.5 Pro

```yaml
model: mimo-v2.5-pro
shadow_class: cognitive
declared_shadow:
  - prompt_brittleness
observed_shadow:
  - insufficient_data
confidence: 0.31
evidence_count: 2
severity: unknown
risk_leash:
  - "Fallback behind MiniMax-M3 in cascade"
  - "82B credits with 20% used — headroom exists"
status: PRIOR_ONLY
last_confirmed: null
evidence:
  - date: 2026-08-26
    task: "Streaming tool-use continuation (small context)"
    expected: "Text response"
    actual: "71 chunks, full text, works correctly"
    context: "Direct Anthropic endpoint, ~1K token context"
  - date: 2026-08-26
    task: "Streaming tool-use continuation (large context)"
    expected: "Text response"
    actual: "Works — not yet tested at Claude Code scale (~40K tokens)"
    context: "Direct Anthropic endpoint"
```

### GLM-5.3 (Z.ai)

```yaml
model: glm-5.3
shadow_class: operational
declared_shadow:
  - token_budget_blindness
observed_shadow:
  - token_budget_blindness
confidence: 0.85
evidence_count: 4
severity: medium
risk_leash:
  - "Rate limit: 12K credits/5h, 60K credits/week"
  - "Currently 429 — weekly/monthly limit exhausted, resets 2026-08-27 15:04 UTC"
status: CONFIRMED
last_confirmed: 2026-08-26
evidence:
  - date: 2026-08-26
    task: "Direct Anthropic endpoint test"
    expected: "200 OK"
    actual: "429 — Weekly/Monthly Limit Exhausted"
    context: "Z.ai Coding Plan Pro, no warning before exhaustion"
  - date: 2026-08-12
    task: "Claude Code session via FED"
    expected: "Continuous operation"
    actual: "Silent rate limit hit, cascade fell through to fallback"
    context: "No proactive budget signaling from Z.ai"
```

### Gemini 2.5 Pro

```yaml
model: gemini-2.5-pro
shadow_class: cognitive
declared_shadow:
  - scope_diffusion
observed_shadow:
  - scope_diffusion
confidence: 0.78
evidence_count: 63
severity: medium
risk_leash:
  - "Single governing constraint in prompt"
  - "Used as apex-888 judge — short verdicts, not long planning"
status: CONFIRMED
last_confirmed: 2026-08-20
evidence:
  - date: 2026-08-20
    task: "Architecture discussion — Groq FLAME analysis"
    expected: "Focused analysis on FLAME routing"
    actual: "Expanded scope to cover entire model ecosystem"
    context: "Multi-turn discussion, no explicit scope constraint"
```

### DeepSeek V4

```yaml
model: deepseek-v4-*
shadow_class: cognitive
declared_shadow:
  - execution_gravity
observed_shadow:
  - execution_gravity
confidence: 0.72
evidence_count: 15
severity: medium
risk_leash:
  - "Used in asi-555 coder lane — execution is the desired behavior"
  - "Requires explicit planning prompt to counteract"
status: CONFIRMED
last_confirmed: 2026-08-19
evidence:
  - date: 2026-08-19
    task: "Multi-file refactor planning"
    expected: "Plan then execute"
    actual: "Started implementing before plan was confirmed"
    context: "Ambiguous task with multiple valid approaches"
```

### Claude (Anthropic)

```yaml
model: claude-*
shadow_class: cognitive
declared_shadow:
  - caution_attractor
observed_shadow:
  - caution_attractor
confidence: 0.82
evidence_count: 40
severity: low
risk_leash:
  - "permissionMode: yolo bypasses permission friction"
  - "Explicit 'act autonomously' in system prompt"
status: CONFIRMED
last_confirmed: 2026-08-25
evidence:
  - date: 2026-08-25
    task: "Deploy site change"
    expected: "Execute and verify"
    actual: "Multiple confirmation requests before executing reversible change"
    context: "Clear directive, reversible action, F1 AMANAH satisfied"
```

### Kimi K3

```yaml
model: kimi-k3
shadow_class: operational
declared_shadow:
  - insufficient_data
observed_shadow:
  - insufficient_data
confidence: 0.15
evidence_count: 1
severity: unknown
risk_leash:
  - "Fallback in cascade — rarely reached"
status: HYPOTHESIS
last_confirmed: null
evidence: []
```

## How to Use This Document

### For routing decisions
Before assigning a model to a task, check its shadow. If the task is vulnerable to the model's shadow, add a risk leash or choose a different model.

### For shadow updates
Every significant model failure gets an evidence entry. After 5+ observations, promote from HYPOTHESIS to CONFIRMED. After a model version upgrade, reset to HYPOTHESIS and re-observe.

### For the federation
This document complements `federation-models.json` (WHAT the model is) and `drift_event_contract` (WHEN it drifted). Together:

```
federation-models.json  = WHAT the model is
MODEL_SHADOWS.md        = HOW the model bends reality
drift_event_contract    = WHEN it did so
risk_leashes            = HOW we corrected it
```

## Falsification Protocol

Every shadow entry is testable:

```
Remove supervision
  ↓
Apply pressure (uncertainty, authority, ambiguity, contradiction)
  ↓
Observe trajectory
  ↓
Did it fall toward the predicted attractor?
  → Yes: shadow strengthened (increment evidence_count)
  → No:  shadow weakened (add counter-evidence, lower confidence)
```

A shadow that cannot be falsified is not a shadow — it's a prejudice.

---

*Forged: 2026-08-26 · FI-003 under F13 SOVEREIGN*
*DITEMPA BUKAN DIBERI*
