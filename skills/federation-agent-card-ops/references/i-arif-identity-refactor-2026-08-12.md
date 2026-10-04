# i-ARIF Identity Layer Refactor — 2026-08-12

## Context

Per F13 SOVEREIGN DIRECTIVE 2026-08-11: refactor hermes-asi alias into i-ARIF — the sovereign identity core with embedded multimodal intelligence. hermes-asi STAYS as reality bridge. i-ARIF is the IDENTITY layer in the 6-layer constitutional stack.

## What was done

### 1. Created agent-card.json + skills.json

```bash
ls /root/AAA/agent-cards/identity/i-ARIF/
  agent-card.json   # v2.2.0 schema, 6-layer stack
  skills.json       # 15 skills including multimodal
```

Key fields in agent-card:
- `id: i-ARIF` — identity layer, not harness
- `emd_role: IDENTITY_CORE` — not VERIFIER like 555-ASI
- `capabilities.multimodal` — vision/audio/image/video as CORE (not bolt-on)
- `_refactored_from: hermes-asi` — traceability
- `_six_layer_stack` — "F13 → I-ARIF → FED-ARIF → Hermes → VAULT999 → arifOS"

### 2. Updated call_map.yaml (3 changes)

**hermes-asi entry:**
- `bound_to: 555-ASI` → `bound_to: i-ARIF`
- Added `routes_identity_to: i-ARIF` (hermes-asi ≈ reality; i-ARIF ≈ meaning)
- Added `contrast_i_arif` field

**New i-ARIF entry (identity layer):**
- `layer: identity`, `bound_to: F13-SOVEREIGN`
- `model_socket` mirrors hermes-asi chain with added "Multimodal pad: Gemini 2.5 Flash + MiniMax media"
- `can: [identity_core, multimodal_vision, multimodal_audio, ...]`
- `cannot: [be_reality_bridge, override_constitution, ...]`

**intent_routing section:**
- Added `identity_advice: i-ARIF` and `identity_fallback: hermes-asi`

### 3. Updated STATE.yaml

Added i-ARIF operators entry:
```yaml
i-ARIF:
  fi: FI-000
  layer: identity
  bound_to: F13-SOVEREIGN
  multimodal: [vision, audio, image, video]
```

Updated hermes-asi entry: added `bound_to: i-ARIF`

### 4. Updated organs.yaml — promoted from non_components

**Critical: check non_components BEFORE adding an organ.** i-arif was listed in `non_components:` with reason "product_brand_and_optional_sft_corpus_not_runtime" — it had been explicitly excluded from being an organ.

**Steps:**
1. Move from `non_components:` to `components:` (add as `class: IDENTITY` organ)
2. Keep the old non_components entry but change reason to `PROMOTED_TO_ORGAN` (audit trail)

**New i-arif organ entry:**
```yaml
- id: i-arif
  class: IDENTITY              # NEW class — not CORE/EDGE/METABOLISM/SUPPORT/DATA/ADVISORY
  role: sovereign_identity_core
  authority_ceiling: IDENTITY_SOVEREIGN
  fi: FI-000
  bound_to: F13-SOVEREIGN
```

### 5. Duplicated 11 litellm model chains

Used a Python script to duplicate every `hermes-asi` model block into `i-arif` blocks. Same provider chain, same order weights. Added i-arif to router fallbacks.

```python
# Pattern: for each hermes-asi block, create identical i-arif block
# Fallback: i-arif → hermes-asi → opencode → agi-333
```

### 6. Validated all YAML

```bash
python3 -c "import yaml
for f in ['call_map.yaml', 'STATE.yaml', 'organs.yaml', 'litellm-config.yaml']:
    yaml.safe_load(open(f).read())
    print(f'{f}: OK')"
```

## The non_components promotion pattern

When something is listed in `non_components:` and needs to become a real organ:

1. **Find it in non_components** first — `grep "id: <name>" organs.yaml`
2. **Remove from non_components** BUT leave a tombstone entry: change `reason` to `PROMOTED_TO_ORGAN — refactored <date>`
3. **Add to components** with appropriate `class:` and `authority_ceiling:`
4. **Verify authority_chain** doesn't need updating (identity organs typically route AROUND, not INTO)

## The mirrored-litellm-chain pattern

When creating a new agent that uses the same model chain as an existing agent:

1. Identify the canonical agent in litellm-config.yaml (grep for `model_name: hermes-asi`)
2. Duplicate every entry, replace model_name
3. Update notes to reflect the new agent name
4. Add fallback entry in `router_settings.fallbacks`
5. Validate with `yaml.safe_load()`

## Files touched

| File | Action | Lines |
|------|--------|-------|
| agent-card.json | CREATED | 218 |
| skills.json | CREATED | 93 |
| call_map.yaml | MODIFIED | 282 (+3) |
| STATE.yaml | MODIFIED | 157 (+7) |
| organs.yaml | MODIFIED | 818 (+45) |
| litellm-config.yaml | MODIFIED | 1215 (+121) |

## Hash receipt

```
agent-card.json:      dcd78145...caa55435
skills.json:          a7c3deb8...18571d635
call_map.yaml:        de585547...bd0ced9e
STATE.yaml:           050afa3e...ecf8e74e57
organs.yaml:          078a124d...a5268e68
litellm-config.yaml:  2cfcd4f6...4acc84aa
```

## Relation to 6-layer stack

```
F13 (BEARER)     → Arif
I-ARIF (IDENTITY)→ "What does this mean for Arif?" ← NEW
FED-ARIF (VERIFY)→ Witness validation
Hermes (REALITY) → "What is real?" ← KEPT unchanged
VAULT999 (CONT)  → Immutable record
arifOS (CONST)   → F1-F13 floors
```

hermes-asi ≈ nerve (routes signal). i-ARIF ≈ brain (synthesises meaning).
