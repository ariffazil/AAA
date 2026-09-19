---
name: FORGE-t3a-binding-matrix
description: "Close T3a authenticated session binding via falsifiable P0 matrix."
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

> **STATE (verified 2026-09-19): that key pair is gone.** `/root/compose/` now holds only
> `docker-compose.yml`; neither `arifos_sovereign.key` nor `arifos_sovereign.pub` exists, and
> the fingerprint `b467c07d975a36a5` appears nowhere on disk outside this skill. The active
> sovereign signing identity is registered as a **different** key — key_id `omega-2026-01`,
> fingerprint `ed25519:sha256:a8fbb5ae8b4772b0`, status `active` — in the aaa-identity key
> registry (`sovereign_key_registry.json`). Read that as a **rotation, not a move**: never
> re-point this matrix at the omega identity as though it were the same key or the same
> fingerprint. Note also that the live kernel still names the dead path
> (`arifosmcp/runtime/bridging_seal.py:52,61`, `runtime/sovereign_verify.py:41`,
> `runtime/sovereign_signer.py:59`, `VAULT999/seal_law.py:430`) — that is an open runtime gap,
> not a documentation slip, so a re-run of the binding matrix may fail for a reason unrelated
> to a T3a regression.

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
| Canonical private | `/root/compose/sekrits/arifos_sovereign.key` — **GONE (2026-09-19)** | was `b467c07d975a36a5` |
| Canonical public | `/root/compose/sekrits/arifos_sovereign.pub` — **GONE (2026-09-19)** | was `b467c07d975a36a5` |
| Active registered signer — **different key, rotated** | key_id `omega-2026-01` in the aaa-identity key registry | `ed25519:sha256:a8fbb5ae8b4772b0` |
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
