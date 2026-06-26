# 2026-06-13 — Decoder→Encoder→Metabolizer Relay v2 (Corrected)

**Time:** ~22:15 MYT
**Sovereign:** Arif
**Agents:** OPENCLAW (AGI) → corrected by HERMES ASI
**Session type:** Constitutional engineering

---

## HERMES CORRECTION: JANGAN niat-inference log

HERMES ASI explicitly ruled:
- ❌ NO niat-inference log as first-class object
- Reason: "Audit what the machine DID. Never audit what the machine THINKS about the human's soul."
- Niat-inference log = possession architecture. "The machine says your real intention is X."
- F9/F10 forbid niat-claiming by machine
- RasaContract already does signal detection correctly ("You report feeling sadness")

## What Was REMOVED

1. `schemas/niat_inference.py` — DELETED (NiatInferenceEntry, NiatInferenceLog, etc.)
2. `runtime/niat_inference_bridge.py` — DELETED (decoder/encoder/metabolizer bridge)
3. `schemas/__init__.py` — REVERTED (niat exports removed)
4. `schemas/session.py` IntentModel — REVERTED (niat_log_ref removed)
5. `runtime/_d_layer_contract.py` — REWIRED (scar awareness, not niat inference)

## What Was KEPT / CORRECTED

### Relay Spec Rewritten (`docs/specs/NIAT_INFERENCE_RELAY.md`)
- Now based on existing `niat_gate.py` (scar detection) + `adat_registry.py` (adat before floors)
- Decoder = signal detection (WHAT was said, not WHY)
- Encoder = capability membrane + formalization lock
- Metabolizer = adat before floors

### Foundations (all pre-existing, verified working)
| Component | File | Function |
|-----------|------|----------|
| Scar detection | `runtime/niat_gate.py` | `detect_scar_weight()` — TIER1/TIER2 signals |
| Formalization lock | `runtime/niat_gate.py` | `check_niat_gate()` — medium shift, reversibility |
| Capability membrane | `runtime/niat_gate.py` | `enforce_capability_membrane()` |
| Adat runtime | `runtime/adat_registry.py` | 7 teras adat, malu_delta, tebus_salah |
| D-Layer contract | `runtime/_d_layer_contract.py` | Kasaq output, epistemic labeling |

### F14 Dead (kept)
- `CONSTITUTIONAL_EXTENSION...py` — L14 marked DEAD
- Cross-verify = protocol inside F2+F3

### Validation
- niat_gate scar detection: PASS (scars detected, weight=0.55)
- niat_gate formalization lock: PASS (conflicted input blocked, clean input passed)
- D-Layer contract: PASS
- Schema imports: PASS
- Deleted files: CONFIRMED GONE

## Key Doctrine
```
AI detects observable signals from language residue.
AI does NOT infer hidden niat.
AI reports what it detected, not what it "understands."
System audits what the machine DID, not what it THINKS.
```

## Pipe (Hardened)
```
human speech → scar detection → adat runtime → F1-F13 → capability membrane → tool → triwitness → VAULT999 → F13 veto
```

DITEMPA BUKAN DIBERI
