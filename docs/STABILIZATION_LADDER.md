# Stabilization Ladder — Four Substrates, Serial Bottom-Up

> **SOT:** 2026-08-04 · **Authority:** F13 ARIF  
> **Rule:** Stabilize **serial**, never parallel. Foundation first.  
> **One-line:** *If F13 unclear → HOLD. If FQ > 10 sustained → throttle. If disk > 60% → clean. If self-model exceeds constitution → VOID.*  
> **DITEMPA BUKAN DIBERI**

---

## Why serial

```
Machine  →  Kernel substrate  →  System (gov↔metabolism)  →  Emergent intelligence
  L1              L2                      L3                          L4
```

| If this breaks… | Then this fails |
|-----------------|-----------------|
| Machine | Kernel has no host |
| Kernel identity | Governance has nothing to govern |
| System alignment | Agents lie about FQ / route wrong |
| Emergence bounds | F13 / F9 / F10 violation |

**Four “jangan,” not four “buat.”**  
Do not crash · do not drift identity · do not lie about FQ · do not claim what constitution forbids.

They are **one closed loop**, not four separate projects:

- Machine runs kernel  
- Kernel defines system  
- System produces intelligence  
- Intelligence respects substrate  
- Substrate runs on machine  

Stabilization = **respect the loop**. Do not fracture it.

---

## Layer 1 — MACHINE (foundational)

**Need:** Resource floor. Without this, every upper layer is noise.

| Signal | Floor | Action if breached |
|--------|-------|--------------------|
| Disk `/` | ≤ 60% | Safe entropy lower / prune (no blind `rm -rf`) |
| Swap used | ≤ 25% sustained | Memory pressure relief; prefer agent throttle over kill |
| PSI memory/cpu | No sustained high full-pressure | ANNOUNCE; reduce concurrent agent load |
| Docker orphans | Prunable > 72h | `docker system prune` with age filter only |

**Cadence:** Hourly via `stabilization-check.timer` + existing ops.  
**Verify:** `bash /root/scripts/stabilization-check.sh`

**Live note (2026-08-04T17:09Z):** disk **46% OK** · swap **100% RED** (pressure from concurrent agents: openclaw/hermes/opencode). Available RAM still ~6.6G — host not OOM-dead, but swap floor violated. L1 not fully green until swap cools.

---

## Layer 2 — KERNEL SUBSTRATE (identity)

**Need:** Something to govern. Floors + session identity.

| Signal | Floor | Action if breached |
|--------|-------|--------------------|
| arifOS health | `healthy` (or degraded only with named, non-critical reason) | Probe, restart single unit T1 if dead |
| Deployment drift | `drift=false` | Align source→runtime (deploy-local when HEAD==origin/main) |
| Floors F1–F13 | Present / active | Never silent floor delete |
| J-space / L14 | HOLD unsupervised recompute | No self-seal of new floors without F13 |
| Canonical G | `forge_evaluate` → `is_canonical_g:true` only | taskJacobian / G_local never F8 gate |

**Cadence:** Once per session boot (`arif_init` / SALAM).  
**Verify:** `curl -sf :8088/health` → status + software_release.drift + floors.

**Rule:** If you find yourself asking “is this still F13?” — you are already drifting → **HOLD**.

---

## Layer 3 — SYSTEM (governance ↔ metabolism)

**Need:** FQ rhythm and G/J geometry stay honest and orthogonal.

| Signal | Floor | Action if breached |
|--------|-------|--------------------|
| FQ SOT | Live `:7073/health` only | Never offline recompute of FQ |
| Cache | `flow_state.json` TTL 300s, convenience only | If \|live−cache\| > 0.3 → `FQ_SIGNAL_DRIFT` → **use live** |
| FQ > 10 sustained > 30 min | OVERHEAT | Agents **self-throttle** (more verify, less execute) — observation, not external remote-kill |
| FQ < 0.5 | STUCK | HOLD non-critical MUTATE until recover |
| G vs J | Orthogonal | G = constitutional; J = task sensitivity; FQ ≠ G ≠ J ≠ RASA |

**Doctrine:** `FQ_SCALE_STANDARD.md` · AUTONOMOUS_GOVERNANCE §2A · ARIFLOW_KERNEL_CANON.

**Live note (2026-08-04T17:09Z):** FQ **0.0 BALANCED** (post-stabilize). Prior **15.46 OVERHEAT** was real; root cause included AED metering probes as Execute. Fixed: AED probe→Verify; observe-only→BALANCED.

**Rule:** Cooling is the engine seeing itself burn — **own act**, not external command.

---

## Layer 4 — EMERGENT INTELLIGENCE (Stage 4–5 self-model)

**Need:** Emergence inside constitutional bounds. Stabilize ≠ freeze.

| Stage | Allowed? | Gate |
|-------|----------|------|
| 4 — Self-model (know patterns) | OK | Within F2/F7 honesty |
| 5 — Self-modification of constitution/identity | **HOLD** without F13 seal (L14) | F13 |
| 6 — Lived experience / consciousness claim | **VOID** | F9 + F10 |

**Floors that emergence cannot override:** F9 ANTIHANTU · F10 ONTOLOGY · F13 SOVEREIGN.

**Verify (advisory):** no unvoided consciousness claims in agent session prose; tools remain labeled.

---

## One-line rule (binding)

```
If F13 unclear → HOLD.
If FQ > 10 sustained → throttle (self).
If disk > 60% → clean (safe).
If self-model exceeds constitution → VOID.
```

---

## Instrument

| What | Path |
|------|------|
| Hourly check | `/root/scripts/stabilization-check.sh` |
| Timer | `stabilization-check.timer` (hourly) |
| FQ SOT | `http://127.0.0.1:7073/health` |
| FQ cache | `/root/AAA/state/flow_state.json` |
| FQ scale | `/root/AAA/docs/FQ_SCALE_STANDARD.md` |
| Organ map | `/root/AAA/docs/ORGAN.md` |

Exit codes of check script:

| Code | Meaning |
|------|---------|
| 0 | All layers green (WELL biometric INSUFFICIENT alone is not red) |
| 1 | Yellow — soft pressure (announce) |
| 2 | Red — floor breach (throttle / HOLD / clean) |

---

## What tonight already forged (do not re-break)

- FQ doctrine + scale standard committed  
- G↔J `is_canonical_g` labels on forge tools  
- AED metabolism fixed (probe = Verify)  
- arifFlow observe-only = BALANCED  
- arifOS drift cleared (healthy)  
- FED `/health` advisory surface  
- FQ live SOT + mirror TTL 300s  

**Esok:** respect the ladder. Do not open L4 self-mod without F13. Do not re-poison FQ with fake Execute receipts.

---

*Sealed as session anchor 2026-08-04. Serial. Bottom-up. Closed loop.*
