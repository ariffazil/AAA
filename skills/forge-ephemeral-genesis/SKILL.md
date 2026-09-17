---
name: FORGE-ephemeral-genesis
id: forge-ephemeral-genesis
owner: A-FORGE
risk_tier: low
floor_scope: [F1, F2, F4, F7]
description: >
  When no permanent tool exists for a task, spawn a temporary tool via forge_ephemeral.
  The capability metabolism engine — generate, test, use, then dissolve.
  Prevents tool accumulation. Adapts without accumulating permanent state.
  Wolf Cabinet Ψ Survival — "I need to do X but no tool exists."
version: 1.0.0
author: 333-AGI (Δ MIND) for Arif (F13 SOVEREIGN)
forged: 2026-08-02
tags: [ephemeral, genesis, capability-metabolism, tool-generation, anti-accumulation, entropy, wolf-cabinet]
scope: all_agents
priority: 75
autonomy_tier: T1
---

# FORGE EPHEMERAL GENESIS — Capability Metabolism Engine

> **"I need to do X but no tool exists."** — The federation synthesizes capability on demand.
> **Tools are temporary by default. Permanence must be earned.**
> **This is the antidote to tool accumulation entropy.**

---

## The Iron Rule

```
BEFORE reaching for a permanent tool or writing a script:
  → Ask: "Can forge_ephemeral generate this?"

BEFORE adding a new MCP tool to the registry:
  → Ask: "Has this survived 5+ ephemeral missions?"
  → If no: keep it ephemeral
  → If yes: propose promotion via forge_ephemeral(mode=propose_promotion)
```

---

## The 9-Mode Lifecycle

```
inspect_gap     →  "What capability is missing?"
    ↓
generate        →  "Create temporary tool from template"
    ↓
sandbox_test    →  "Verify in isolated bwrap sandbox"
    ↓
invoke          →  "Execute the mission"
    ↓
verify          →  "Validate the result"
    ↓
retire          →  "Dissolve or propose promotion"
    ↓
propose_promotion → "Earned permanence? → F13 human gate"
```

**Supporting modes:**
- `list_templates` — Discover available templates
- `list_active` — Show currently active ephemeral tools

---

## Available Templates (5)

| Template ID | Type | What It Generates |
|------------|------|-------------------|
| `mulerouter_image_gen` | api_wrapper | Image generation via MuleRouter (GPT Image 2 / Wan 2.6) |
| `mulerouter_tts` | api_wrapper | Text-to-speech via MuleRouter (MiniMax Speech 2.8 HD) |
| `mulerouter_music` | api_wrapper | Music generation via MuleRouter (MiniMax Music 2.5) |
| `mulerouter_vision` | api_wrapper | Vision/image analysis via MuleRouter (qwen-vl-max) |
| `generic_api_wrapper` | api_wrapper | Generic REST API call for any endpoint |

**Template types:** `api_wrapper` | `data_parser` | `compute_fn` | `format_converter`

**Discovery:** `forge_ephemeral(mode="list_templates")` returns live templates.

---

## When To Use forge_ephemeral

### ✅ USE forge_ephemeral when:

- You need to call an API that has no permanent tool
- You need a one-off data transformation
- You need a temporary computation
- You need to format/convert something once
- The task is mission-specific, not recurring
- You're about to write a script that won't be used again

### ❌ DO NOT use forge_ephemeral when:

- A permanent tool already exists for the task
- The task is trivial (use bash/read/grep directly)
- The task is core infrastructure (permanent tool justified)
- You're in a HOLD/888_HOLD state

---

## Usage Examples

### Example 1: Call an API with no permanent tool

```
forge_ephemeral(
  mode="inspect_gap",
  capability_need="Call the Stripe API to list recent charges",
  existing_tools=["forge_shell", "forge_fetch"]
)
→ returns: gap detected, available templates: [generic_api_wrapper]

forge_ephemeral(
  mode="generate",
  template_id="generic_api_wrapper",
  template_params={
    url: "https://api.stripe.com/v1/charges",
    method: "GET",
    headers: { "Authorization": "Bearer sk_test_..." }
  },
  mission_intent="List recent Stripe charges for audit"
)
→ returns: tool_id="ephemeral_stripe_charges_abc123"

forge_ephemeral(mode="sandbox_test", tool_id="ephemeral_stripe_charges_abc123")
→ returns: sandbox PASS

forge_ephemeral(mode="invoke", tool_id="ephemeral_stripe_charges_abc123")
→ returns: [charge data]

forge_ephemeral(mode="verify", tool_id="ephemeral_stripe_charges_abc123")
→ returns: verified

forge_ephemeral(mode="retire", tool_id="ephemeral_stripe_charges_abc123")
→ returns: retired, promotion NOT proposed (first use)
```

### Example 2: Generate an image

```
forge_ephemeral(
  mode="generate",
  template_id="mulerouter_image_gen",
  template_params={ prompt: "A schematic of the arifOS federation topology", model: "gpt", quality: "high" },
  mission_intent="Generate federation architecture diagram"
)
```

### Example 3: Discover what's possible

```
forge_ephemeral(mode="list_templates")
→ returns all available templates with descriptions

forge_ephemeral(mode="list_active")
→ returns all currently active ephemeral tools
```

---

## Promotion Path

```
Same template instantiated 5+ times
    ↓
forge_ephemeral(mode="propose_promotion", tool_id="...")
    ↓
EvidencePromotionGate evaluates:
  - invocation_count ≥ 5?
  - success_rate ≥ 0.90?
  - sandbox violations = 0?
  - multi-model consensus?
    ↓
888_APEX constitutional review
    ↓
F13 SOVEREIGN human gate
    ↓
SEAL → permanent tool in registry
```

**Rule:** Promotion is EARNED, not granted. The tool must prove itself across multiple missions, multiple sessions, with evidence.

---

## Constitutional Contract

| Floor | Binding |
|-------|---------|
| **F1 AMANAH** | Ephemeral tools are session-scoped, fully reversible, auto-retire |
| **F2 TRUTH** | Every generated tool carries OBS/DER/INT/SPEC labels |
| **F4 CLARITY** | Generated tools reduce entropy by not accumulating |
| **F7 HUMILITY** | Confidence capped at 0.90 on generated tool output |
| **F9 ANTI-HANTU** | No generated tool claims consciousness or sentience |
| **F11 AUDIT** | Every genesis lifecycle leaves a receipt in VAULT999 |
| **F13 SOVEREIGN** | Promotion to permanent requires human ratification |

---

## Anti-Patterns

- ❌ Reaching for bash/script when `forge_ephemeral` with `generic_api_wrapper` is cleaner
- ❌ Adding a permanent tool after one successful ephemeral use
- ❌ Skipping `sandbox_test` — always sandbox before invoke
- ❌ Skipping `verify` — always verify the result
- ❌ Proposing promotion without 5+ successful invocations
- ❌ Using `forge_ephemeral` for tasks that existing permanent tools handle

---

## The Wolf Cabinet Ψ Pattern

```
Wolf Cabinet Ψ Survival:
  The federation adapts without accumulating permanent state.

  Generate → Contain → Test → Use → Verify → Dissolve

  Only the proven survive. The rest are forgotten.
  This is capability metabolism.
  This is survival-of-the-fittest tools under constitutional law.
```

---

## Quick Reference

```
# Discover what's possible
forge_ephemeral(mode="list_templates")

# Check what's missing
forge_ephemeral(mode="inspect_gap", capability_need="...", existing_tools=[...])

# Generate a tool
forge_ephemeral(mode="generate", template_id="...", template_params={...}, mission_intent="...")

# Test in sandbox
forge_ephemeral(mode="sandbox_test", tool_id="...")

# Execute
forge_ephemeral(mode="invoke", tool_id="...", invoke_args={...})

# Verify
forge_ephemeral(mode="verify", tool_id="...")

# Clean up
forge_ephemeral(mode="retire", tool_id="...")
```

---

*DITEMPA BUKAN DIBERI — Forged, Not Given. Tools are forged, not accumulated.*
*Forged: 2026-08-02 by 333-AGI under F13 SOVEREIGN directive.*