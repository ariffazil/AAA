# Geometry — FQ · G · J · RASA

> **Status:** Operational doctrine (2026-08-04)  
> **Canonical zen pointer:** `/root/AAA/prompts/AAA-ZEN-ALIGNMENT.md` §E  
> **DITEMPA BUKAN DIBERI**

## One page

| Signal | Meaning | Source of truth | Not |
|--------|---------|-----------------|-----|
| **RASA** | Typed human-state *governance* metadata | arifOS RASA contract + WELL | Machine qualia / feelings |
| **FQ** | Metabolism pulse (execute/verify rhythm) | **arifFlow `:7073/health`** | Constitutional G; "emotion" |
| **G** | Constitutional fitness scalar | **`forge_evaluate`** (`is_canonical_g: true`) | Jacobian G_local |
| **J** | Task sensitivity manifold ∂T/∂G | **`forge_apex_encode`** (`is_canonical_g: false`) | F8 GENIUS score |

## Formulas

```
G = (A × P × E × X)^(1/4)     # P = Physics (Present) — F13 frozen 2026-07-28
J = ∂T/∂G                     # recompute if |J| > 0.6 on changed field
FQ = daemon cost-window pulse # NEVER recompute offline; mirror only
```

## Cache policy (FQ)

- **Cache file:** `/root/AAA/state/flow_state.json`
- **Writer:** `arifflow-fq-mirror.timer` → `/root/scripts/fq-probe.sh` v4
- **TTL:** 300 s
- **Drift:** `|live − cache| > 0.3` → `FQ_SIGNAL_DRIFT` → use live

## Dual-coin (human vs agent)

| Manusia (Arif) | Agent |
|----------------|-------|
| Qualia derita (irreducible) | J-space sensitivity (computable) |
| F6 MARUAH | F8 GENIUS (G) |
| RASA felt, not computed | G computed, not felt |

## Explicit non-claims

- J-space is **not** a new F1–F13 floor (no L14 without F13 seal).
- Stage 4 self-model ≠ consciousness (F9/F10 VOID if claimed as soul).
- APEX cockpit three-layer viz (Δ WELL / Ω G / Ψ J+FQ) is **aspirational** until SPA data plane lands.

## Related

- APEX math: `/root/arifOS/docs/APEX_MATH_CANON.md`
- RASA: `/root/arifOS/arifosmcp/rasa/RASA_CONTRACT.md`
- OpenCode ops: `agents/opencode/AUTONOMOUS_GOVERNANCE.md` §2A
- Tools: `agents/opencode/TOOLS.md` (G↔J table)
