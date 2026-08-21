---
name: FORGE-t3a-binding-matrix
description: >
  Close T3a authenticated session binding via falsifiable P0 matrix.
  Use when: T3a, free_nonce, bridging_seal, Ed25519 arif binding, key fragmentation,
  forge_p0_binding_test, NEG.3, NEG.6b, authenticated_session_binding.
version: 2026.07.17
floors: [F1, F2, F7, F11, F13]
---

# FORGE — T3a Binding Matrix

> **SE stage stays 000 until this matrix is 13/13 PASS.**  
> Positive path alone ≠ CLOSED.

## Runnable proof

```bash
python3 /root/scripts/forge_p0_binding_test.py
# Receipt: A-FORGE/forge_work/2026-07-17/APEX-CONCORDANCE-17072026/t3a-p0-binding-matrix.md
```

## Known score (CLOSED 2026-07-17)

```text
13 PASS / 0 FAIL — T3a CLOSED
commit arifOS 196cb5ef2
canonical key: /root/compose/sekrits/arifos_sovereign.{key,pub}  fp b467c07d975a36a5
```

## Fix order — DONE (do not re-open unless regression)

| # | Gap | Status |
|---|-----|--------|
| **B** | Key fragmentation | **CLOSED** — bridging_seal prefers compose sekrits |
| **C** | free_nonce | **CLOSED** — `challenge_not_issued` |
| **D** | bridging_seal | **CLOSED** — fresh True + single_use replay False |

Re-run matrix only if regression suspected → expect **13/13**.

## Key path inventory (canonical)

| Role | Path | Fingerprint note |
|------|------|------------------|
| Canonical private | `/root/compose/sekrits/arifos_sovereign.key` | → `b467c07d975a36a5` |
| Canonical public | `/root/compose/sekrits/arifos_sovereign.pub` | `b467c07d975a36a5` |
| AAA alias | `/root/AAA/IDENTITY/keys/arif_public.pem` | same |
| Legacy fragment | `/opt/arifos/secrets/did_arifos_*` | `47ae539c…` — not preferred |

## Code entry points

- `arifosmcp/runtime/crypto_auth.py` — verify_init_identity, free_nonce label  
- Challenge store issue/consume  
- `bridging_seal` mint/verify  
- `sovereign_verify.py` pubkey candidates  

## CLOSED (do not re-prove as if broken)

- Identity component leak  
- Authority collapse on unverified  
- POSITIVE Ed25519 → SOVEREIGN path works  
- **T3a overall — matrix 13/13 (2026-07-17)**  
- free_nonce / key fragmentation / bridging_seal single_use  

## Do not

- Re-open T3a without regression evidence  
- Advance SE by hand-edit — use `se_stage_engine.try_advance` only  
- Rotate secrets without F13 / 888_HOLD documentation 
