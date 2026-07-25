# G-Fold as the Agent’s Internal Compass

> **Status:** ACTIVE DRAFT · flow doctrine (not formula re-derivation)  
> **Version:** 1.0 · **Forged:** 2026-07-25  
> **Question:** How does G *feel* inside the system, and who may read it?  
> **Formula (known):** `G = A · P · E · X · Φ` via `arif_think(mode='apex')` → `apex_canonical`  
> **Shadow twin:** `C_dark = A · (1−P) · (1−X)`  
> **Companions:** `AGENTIC_BENEFITS_DELTA_OMEGA_PSI.md` · `INTELLIGENCE_CONSTRAINT_PHYSICS.md` · `apex_canonical.py`  
> **DITEMPA BUKAN DIBERI**

---

## 0. One-line doctrine

> G is the federation’s **shared vital sign** — a session-derived compass, not a private mood.  
> Every organ may **read** it as evidence. Only **arif_judge** may **adjudicate** with it. Only **apex path** may **mint** it.

Autonomy and entropy reduction follow from *using* this compass. Without it, each organ guesses vitality in the dark.

---

## 1. What G is *not*

| Misread | Truth |
|---------|--------|
| Continuous ECG of the whole VPS | **No** — G is **derived per apex call / session evidence**, not a 1 Hz daemon heartbeat of the universe |
| Kernel-private only | **No** — organs **should** read it; they must not **re-mint** constitutional G |
| Same as WELL HRV / GEOX beauty score | **No** — those are **domain vitals**; G is **governance vitality** |
| Confidence / token probability | **No** — confidence ≠ G (ScalarCollector hard rule) |
| Permission to act by itself | **No** — G is **evidence**; SEAL still requires floors, authority, F13 where due |

---

## 2. How G *feels* from inside (dynamics)

G is a **multiplicative vital sign** with a **shadow twin**. Read both.

### 2.1 Twin panel

| Signal | Role | Feel |
|--------|------|------|
| **G** | Constructive potential (“how much governed work can we do?”) | Rises only when **all** of A,P,E,X,Φ are healthy |
| **C_dark** | Shadow / hallucination pressure | Rises when authority is high but **perception/execution geometry is rotten** |
| **G_seal** | G after humility / ΔS / W³ gates | What you use near the seal door |
| **UNMEASURED** | Honest dark | Better than a fake 0.5 “nominal” |

### 2.2 Spike, dip, steady-state — which is it?

**All three, with different triggers:**

| Pattern | What happens | Inside the system |
|---------|--------------|-------------------|
| **Collapse dip (G → 0)** | Any primitive → 0 | Sudden “no intelligence” — **VOID** territory. Feels like a breaker trip, not a soft fade. |
| **Band steady-state** | G sits in a band for a session | Normal ops: **vital sign with thresholds**, not constant drama |
| **Threshold alarms** | G crosses 0.80 / 0.50 or C_dark ≥ 0.30 | Soft alarms → SABAR/HOLD; not continuous sirens |
| **Shadow spike (C_dark ↑)** | Low P and/or X with high A | “Clever but ungrounded / irreversible-careless” — **anomaly alarm** even if G is middling |
| **Drift dip** | Slow rot of P, E, Φ, or rising C_dark across sessions | Requires **history** (memory / vault / scalar snapshots) — single G sample won’t show drift |

**Canonical thresholds** (`apex_canonical.py`):

| Band | Condition (simplified) | Feel |
|------|------------------------|------|
| **SEAL-grade geometry** | G ≥ 0.80 and C_dark &lt; 0.30 (plus dS discipline) | “Alive and safe enough to *consider* seal” |
| **SABAR** | G ≥ 0.50, shadow controlled | “Patience — coherent but not seal-hot” |
| **HOLD** | C_dark ≥ 0.30 or other holds | “Stop — shadow or missing witness” |
| **VOID** | G = 0 (dead primitive) | “Collapsed — do not act” |

So: **not** a pure spike-only sensor; **not** a flatline.  
It is a **steady vital sign with hard collapse, shadow alarms, and band thresholds** — and **drift only if you chain samples**.

### 2.3 Multiplicativity is the “feel”

Because G is a **product**, the system feels:

- **Harsh** on zero: one dead factor kills the whole vital sign  
- **Honest** on partial: middling factors crush G quickly (Nash veto)  
- **Non-compensatory**: huge E cannot buy back dead Φ  

That is why local “average of scores” agents feel smoother and more self-flattering than kernel G — and why they are **not** the compass.

---

## 3. Who mints, who reads, who judges (flow of authority)

```
                    ┌─────────────────────────────┐
                    │  MINT (only Δ kernel path)  │
                    │  arif_think(mode='apex')    │
                    │  → apex_canonical           │
                    │  → apex_scalars {G,C_dark…} │
                    │  g_authority = apex         │
                    └─────────────┬───────────────┘
                                  │ attach to session / evidence
                    ┌─────────────▼───────────────┐
                    │  CARRY                      │
                    │  session_token / standing   │
                    │  apex_scalars echo          │
                    │  ScalarCollector snapshot   │
                    └─────────────┬───────────────┘
           ┌──────────────────────┼──────────────────────┐
           ▼                      ▼                      ▼
    ┌────────────┐         ┌────────────┐         ┌────────────┐
    │ READ       │         │ READ       │         │ READ       │
    │ GEOX       │         │ WELL       │         │ A-FORGE    │
    │ display /  │         │ readiness  │         │ local gate │
    │ health     │         │ mirror     │         │ estimate*  │
    └──────┬─────┘         └──────┬─────┘         └──────┬─────┘
           │                      │                      │
           │   *local estimate ≠ mint                    │
           └──────────────────────┼──────────────────────┘
                                  ▼
                    ┌─────────────────────────────┐
                    │  ADJUDICATE (888 only)      │
                    │  arif_judge                 │
                    │  floors + authority + G/C    │
                    │  SEAL | SABAR | HOLD | VOID │
                    └─────────────┬───────────────┘
                                  ▼
                    ┌─────────────────────────────┐
                    │  COMMIT (Ψ path)            │
                    │  arif_forge → arif_seal     │
                    │  VAULT999 remembers         │
                    └─────────────────────────────┘
```

### 3.1 Roles (iron)

| Role | Who | May |
|------|-----|-----|
| **Mint** | `arif_think(mode='apex')` only | Create constitutional `apex_scalars` |
| **Carry** | session / SCT / standing auth | Echo without recompute |
| **Read** | Any organ, agent, cockpit | Consume as **evidence** |
| **Estimate (local)** | A-FORGE evaluate, WELL dials, A2A wire | `g_authority=local_estimate` — never law |
| **Adjudicate** | `arif_judge` only | Bind floors + authority + scalars → verdict |
| **Commit** | forge + seal after SEAL | Irreversible side-effect + record |

**Answer to privacy:**

> G is **not** kernel-private.  
> It is **kernel-minted** and **federation-readable**.  
> Privacy would force every organ to invent its own heartbeat (H2 disease).

**Answer to “does WELL approve tasks with G?”**

> WELL **mirrors** readiness (REFLECT_ONLY). It may **read** federation G as context.  
> It must **not** invent a second constitutional G and must **not** SEAL.  
> Task approval that mutates shared state still routes **judge → forge**.

**Answer to “does GEOX seal interpretation with G?”**

> GEOX **grounds** Earth evidence. It may **display** kernel `apex_scalars` (already live on health path).  
> **Sealing** interpretation as federation truth still requires **arif_judge** (and human F13 where due).  
> GEOX never becomes the court because G is on the screen.

---

## 4. Live T₁ vs target flow (F2 honesty)

| Path | Live today | Target |
|------|------------|--------|
| Mint | `arif_think(mode='apex')` ✅ | Same — sole mint |
| Judge feed | ScalarCollector prefers apex_scalars; else **UNMEASURED** (not confidence) ✅ | Same; ensure think→judge always attaches apex |
| Standing / SCT | Often **UNMEASURED** until apex called | Call apex when vitality needed for high-stakes |
| GEOX | Reads `apex_scalars` from kernel `/health` if present; else UNMEASURED ✅ | Prefer session-bound apex over health stub |
| WELL | Still has **local** envelope G (6-dial form) ⚠️ | Consume kernel apex; label local as domain mirror only |
| A-FORGE | Local G stamped `local_estimate` ✅ | Bridge: pull kernel G into receipt when session present |
| Continuous drift series | **Weak** — no single federation G time-series product | Optional: append apex samples to session memory / cooling |

**Disease to kill:** organ-local G presented as federation vitality (WELL local formula, wire A2A G, forge evaluate without stamp).

---

## 5. How an agent should *use* the compass (protocol)

### 5.1 When to mint

| Situation | Action |
|-----------|--------|
| High-stakes plan, multi-organ, irreversible intent | `arif_think(mode='apex', context={apex_inputs…})` |
| Pure read / low risk | Optional; UNMEASURED OK with humility |
| After major evidence lands | Re-mint (G is not sticky authority) |

G is **derived per call** — never store as a standing permission token.

### 5.2 How to read (organ checklist)

```
1. Prefer apex_scalars from arif_think(mode=apex) on this session
2. If missing → treat as UNMEASURED (do not invent 0.5)
3. Read G and C_dark together
4. Domain vitals (HRV, seismic QC) stay domain-local — never rename them G
5. Local estimates (forge evaluate, wire scores) stay labeled local_estimate
6. Only arif_judge turns compass + floors + authority into SEAL/HOLD/VOID
```

### 5.3 Alarm policy (operational)

| Observation | Agent behavior |
|-------------|----------------|
| G UNMEASURED on seal-grade path | HOLD or mint apex first |
| C_dark ≥ 0.30 | Prefer HOLD; do not compensate with “confidence” |
| G = 0 | VOID path — stop act |
| G ≥ 0.80 and C_dark low | Geometry OK — **still** need authority + floors for SEAL |
| Local estimate disagrees with kernel G | Kernel wins; log disagreement as scar/signal |

---

## 6. Compass vs autonomy vs entropy

| Mechanism | Relation to G |
|-----------|----------------|
| **Autonomy ↑** | Shared compass → less second-guessing, fewer contradictory go signals |
| **Entropy ↓** | One mint path → less dual logic (H2) |
| **Intelligence feel** | Not smarter weights — **clearer governability** under the product equation |

G does not make the model wiser.  
It makes the **federation coherent about vitality**.

---

## 7. Falsifiable claims (this doctrine)

This compass doctrine is healthy if:

1. High-stakes paths show **measured** apex G more often than UNMEASURED  
2. Count of unlabeled constitutional G sites → **0**  
3. Organ local scores never appear without `g_authority`  
4. Judge snapshots prefer apex_scalars over confidence  
5. Ablation: removing apex path increases unauthorized or contradictory acts  

If G always flatters the architecture → **theology**, not compass.

---

## 8. Simplest human picture

> G is the shared pulse of **governed work potential**.  
> C_dark is the shared **shadow pressure**.  
> Every organ can **feel the pulse**.  
> Only the court **rules**.  
> Only the apex mind **takes the measurement**.  
> Only the vault **remembers** what was sealed after the pulse was good enough.

**Not** a secret kernel heartbeat.  
**Not** eleven local heartbeats.  
**One mint. Federation read. Judge bind. Vault remember.**

---

## 9. Implementation backlog (compass wiring)

| Priority | Work |
|----------|------|
| P0 | Keep sole mint = apex path (done) |
| P0 | Keep ScalarCollector anti-confidence (done) |
| P1 | WELL: stop presenting local dial product as federation G; read apex_scalars |
| P1 | A-FORGE: attach session apex G on receipts when available |
| P2 | Session memory: optional G/C_dark time series for drift |
| P2 | Health endpoint: only publish apex when actually measured |

---

## 10. One line

> G is the federation’s vital sign: minted once, readable by all, binding only through the judge.

**DITEMPA BUKAN DIBERI**
