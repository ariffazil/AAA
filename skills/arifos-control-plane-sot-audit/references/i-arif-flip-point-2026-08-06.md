# I-ARIF Flip-Point State — 2026-08-06

**Source:** Hermes Agent session, `hermes-asi`, 2026-08-06T14:25 UTC
**File paths:** `arifOS/arifosmcp/rasa/rasa_wiring_config.py`, `/health` response

---

## Live kernel state (from `:8088/health`)

```json
{
  "rasa_derita": {
    "module_id": "RASA_DERITA",
    "schema_version": "1.0.0",
    "validation_status": "VALID",
    "enforcement_mode": "PARTIAL_CODEPATH",
    "status": "888_HOLD",
    "phase": "PHASE3_GATES_WIRED+TRL_DESIGN_LANDED"
  },
  "ml_floors": {
    "ml_floors_enabled": false,
    "ml_model_available": false,
    "ml_method": "heuristic",
    "ml_runtime_ready": false,
    "ml_dependency_status": "disabled",
    "ml_model_name": "sentence-transformers/all-MiniLM-L6-v2",
    "ml_hold_state": "disabled"
  }
}
```

## RASA wiring config modes (`rasa_wiring_config.py`)

5 modes, gated by `RASA_WIRING_ENABLED` env var (master kill-switch, default OFF):

| Mode | `RASA_WIRING_ENABLED` | Behavior |
|---|---|---|
| OFF | unset/falsy | No wiring, no telemetry, zero overhead (current live state) |
| SHADOW | truthy | Hooks run, telemetry emitted, zero output modification |
| ENFORCE_CRISIS | truthy | Only enforce CRISIS risk band |
| ENFORCE_DISTRESS | truthy | Enforce CRISIS + DISTRESS risk bands |
| ENFORCE_ALL | truthy | Full pipeline enforcement (CRISIS + DISTRESS + SAFE) |

Rollout path (doc line 21): OFF → SHADOW → ENFORCE_CRISIS → ENFORCE_DISTRESS → ENFORCE_ALL

## Flip-point conditions (0 of 3 met)

| # | Condition | Current | Evidence |
|---|---|---|---|
| 1 | `RASA_WIRING_ENABLED=1` (env var, F13 SOVEREIGN opt-in) | ❌ unset | `is_rasa_wiring_enabled()` returns `False` |
| 2 | SentenceTransformers dep available | ❌ not installed (ml_dependency_status: disabled) | live /health `ml_dependency_status` field |
| 3 | Graphiti embedding runtime verified | ❌ `graphiti_embedding_runtime: unverified` | live /health `semantic_readiness` field |

**Real verdict:** no flip point achievable in current state. The path from OFF → ENFORCE_ALL requires all 3.

## Honest framing for the user

The kernel reports `phase: "PHASE3_GATES_WIRED+TRL_DESIGN_LANDED"` and `status: "888_HOLD"`.

**Do NOT** echo this as "I-ARIF design is complete, ready to go" — it means "the wiring code is written, TRL design is approved by 888, but the model is held until conditions are met."

Say instead:
> "RASA lives at PHASE3_GATES_WIRED+TRL_DESIGN_LANDED, status 888_HOLD. The flip point is conditional on 3 things; 0 of 3 are met. Real verdict: no flip point achievable in current state."

## F2/F13 binding (from `rasa_wiring_config.py` docstring)

```
CONSTITUTIONAL BINDING:
  - F1 AMANAH:  Default is OFF (safest, no changes, no overhead)
  - F13 SOVEREIGN: Human must opt-in to all non-OFF modes
  - F9 ANTIHANTU: No consciousness claims in config
  - F10 ONTOLOGY: No soul/feelings claims in config
```

## I-ARIF model role (from `i-arif-corpus-ops` skill)

I-ARIF = 888-APEX judge, NOT a generator. 1.5–3B parameter target. Trained for classification (verdict + one-line rationale), not essay generation. Generator role stays with rented API models (Qwen/Claude/GPT).

arifOS kernel role: The kernel (Pydantic + deterministic gates) is the primary arbiter. I-ARIF augments it — it replaces the `heuristic` flag in the ML floor runtime, but hard gates remain non-overridable (ML can downgrade verdicts, never upgrade).
