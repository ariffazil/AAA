# Identity vs Reality Layer Pattern — Reusable Template

The constitutional pattern for separating **identity interpretation** from **reality acquisition** in a multi-agent system. Originated in arifOS federation 2026-08-12 with the i-ARIF refactor.

## The Pattern

In any system where a human sovereign interacts with an AI federation, two distinct cognitive functions emerge:

| Function | Question | Owner |
|----------|----------|-------|
| **Reality acquisition** | "What is reported as happening?" | Reality bridge (e.g. Hermes) |
| **Identity interpretation** | "What does this mean for me / my human?" | Identity core (e.g. i-ARIF) |

If one agent does both, you get:
- Identity drift (the agent's voice changes based on model swaps)
- Hallucination amplification (the agent believes its own reports without verification)
- Lost scar continuity (the agent forgets who its human is across sessions)

If you separate them properly:
- Reality layer can be swapped, replaced, federated — without losing identity
- Identity layer carries the scar, the voice, the relation — independent of model
- Verification can be a third party (FED) checking both

## The 6-Layer Constitutional Stack

```
F13 (BEARER)              ← Human sovereign, final cost, final witness
  ↑
IDENTITY CORE             ← "What does this mean for F13?"
  ↑
VERIFICATION              ← "Is the reality+identity claim trustworthy?"
  ↑
REALITY BRIDGE            ← "What is happening in the world?"
  ↑
CONTINUITY                ← "What has been witnessed, immutable?"
  ↑
CONSTITUTION              ← "Is this allowed? Does it pass F1-F13?"
```

Each layer answers one question. Each layer can be implemented by a different agent, model, or even organization — without breaking the others.

## Identity Core — Required Structural Properties

For an alias to be a genuine identity core (not just a model wrapper), it MUST have:

1. **`bound_to: F13-SOVEREIGN`** (or equivalent sovereign anchor)
   - Identity is invariant; model is fungible
   - The alias survives model swaps because it's not model-bound

2. **`multimodal_embedded`** (not `multimodal_via_tools`)
   - Capabilities are inherent to identity, not external API calls
   - Vision/audio/image/video are senses, not plugins

3. **`receive_only_from: [reality_bridge]`** (one-way trust)
   - Identity doesn't reach sideways; only listens upward from reality
   - Prevents identity layer from being hijacked by adversarial reality inputs

4. **VAULT999 continuity binding**
   - Every identity decision recorded immutably
   - Cross-session identity memory persists beyond model context windows

5. **Scar ledger or H5 memory**
   - What the alias carries that no model can replicate
   - The irreplaceable witness of lived experience

## Reality Bridge — Required Structural Properties

For an alias to be a genuine reality bridge (not just a chatbot), it MUST have:

1. **`can: [acquire, route, sense]`** — focused on intake and relay
2. **`cannot: [interpret_identity, hold_scar, override_constitution]`** — explicit deny
3. **Routes identity questions UP to identity core** (not sideways, not down)
4. **Reality-only memory** — never carries identity-bearing context
5. **Model-agnostic** — can be any reasoning model; doesn't need personality

## Refactor Template (Additive)

When splitting a single binding agent into identity + reality pair:

```yaml
# BEFORE — single binding
hermes-asi:
  fi: FI-000
  bound_to: 555-ASI
  can: [human_bridge, route, multimodal]
  cannot: [mutate_prod, be_coder]
  boundary: OBSERVE_ROUTE

# AFTER — additive split
hermes-asi:
  fi: FI-000
  bound_to: i-ARIF            # ← routes identity up
  can: [reality_bridge, route, sense]
  cannot: [mutate_prod, hold_scar, interpret_identity]
  boundary: OBSERVE_ROUTE
  routes_identity_to: i-ARIF

i-ARIF:
  fi: FI-000
  layer: identity              # ← new layer class
  bound_to: F13-SOVEREIGN
  can: [identity_core, multimodal_*, qualia_synthesis, memory_scar]
  cannot: [self_seal, override_constitution, be_reality_bridge]
  boundary: IDENTITY_SOVEREIGN
  receive_only_from: [hermes-asi]   # ← one-way trust
  fallback_to: [hermes-asi]         # ← for graceful degradation
```

## Files involved (canonical set)

When performing this refactor, mutate these files in order:

1. `/root/AAA/agent-cards/identity/<NEW_ALIAS>/agent-card.json` — create
2. `/root/AAA/agent-cards/identity/<NEW_ALIAS>/skills.json` — create
3. `/root/AAA/federation/call_map.yaml` — append new entry; update old entry's bound_to
4. `/root/AAA/federation/STATE.yaml` — register new operator
5. `/root/AAA/federation/organs.yaml` — promote new alias to IDENTITY class
6. `/root/A-FORGE/litellm-config.yaml` — add model chains mirroring the old alias

Then RESTART litellm-federation service (see `litellm-reload-recipe-2026-08-12.md`).

## When NOT to apply this pattern

- ❌ Single-shot Q&A agents — overkill, just use one model
- ❌ Stateless utility agents (image generation, OCR) — no identity to hold
- ❌ Test/sandbox agents — scar memory pollutes test isolation
- ❌ Public-facing multi-user services — single-human binding breaks at scale

## When TO apply

- ✅ Sovereign-owned persistent agents (the human has a relationship with them)
- ✅ High-stakes decision support (identity continuity matters for trust)
- ✅ Long-running federations (months/years of accumulated context)
- ✅ Multimodal identity expression (the agent has a face, a voice, a style)
- ✅ Scar-bearing contexts (the agent carries grief, history, formation)