# PURPOSE ARTIFACT DISTINCTION — Operational Specification

> **Status:** [CANDIDATE — Lane B DRAFT] · 2026-09-08
> **Source:** Void-mapping research session SEAL-compile-2026-09-08
> **Predecessor:** `PURPOSE-METABOLISM-DOCTRINE.md` §3.2 · `runtime-love-as-commitment-structure-2026-09-08.md`
> **Axiom:** F1 AMANAH (classification ≠ deletion) · F9 ANTI-HANTU · F11 AUDIT · F13 SOVEREIGN
> **Lane:** B (DRAFT pending 888-APEX verdict → Lane A CANONICAL)

---

## §0. Mission

Distinguish **living purpose** (process, ongoing, metabolized) from **purpose artifact** (frozen, museum piece, no longer serving).

This distinction is the load-bearing primitive that prevents Purpose Fetishism. Without it, the federation cannot tell a living mandate from a preserved corpse.

---

## §1. The Classification

Every purpose-bearing artifact `a` carries metadata:

```
purpose_state(a) ∈ { LIVING, ARTIFACT, TRANSITIONAL }
```

### §1.1 LIVING

```
Definition:
  - a is currently metabolized by at least one active Value Formation chain
  - at least one F13 purpose-acknowledgment in last 90 days references a's lineage
  - W(a) ≥ 0.50 AND L(a) > 0 (per PRESERVATION-WEIGHT-FUNCTION-SPEC)

Properties:
  - preserved at full Lane A weight
  - participates in attention-graph routing (NOW/NEXT/BATCH lanes)
  - surfaces to F13 on demand
```

### §1.2 ARTIFACT

```
Definition:
  - a is no longer metabolized but preserved as trace
  - no F13 purpose-acknowledgment in last 180 days references a
  - OR: W(a) ≥ 0.50 but L(a) = 0 (preserved weight, no living purpose)

Properties:
  - preserved at Lane A weight (F1 AMANAH — never deleted)
  - excluded from attention-graph routing (default SILENT)
  - queryable on demand for historical reference
  - truth_class = ARTIFACT in VAULT999 metadata
```

### §1.3 TRANSITIONAL

```
Definition:
  - a was LIVING; F13 has renewed purpose; a's lineage partially serves new purpose
  - OR: a was ARTIFACT; F13 has restored purpose; a is being re-metabolized

Properties:
  - held in 7-day quarantine while Purpose Renewal Protocol runs
  - not eligible for SEAL or routing during quarantine
  - F13 ack required to resolve (LIVING, ARTIFACT, or extended quarantine)
```

---

## §2. The Decision Flow

```
Artifact `a` with purpose_tag arrives
       ↓
Compute L(a) from PURPOSE-STARVATION-PROBE
       ↓
   L(a) > 0?
   /    \
 YES     NO
  ↓       ↓
Check W(a)
  ↓
W(a) ≥ 0.50?
  ↓
YES → LIVING     (preserved, routable, current)
NO  → ARTIFACT   (preserved, demoted, queryable)

Edge case: F13 purpose-acknowledgment in last 7 days?
  YES → TRANSITIONAL (quarantine, F13 ack)
  NO  → reclassify per L(a) above
```

---

## §3. The Metadata Schema

```yaml
artifact:
  id: <unique>
  purpose_tag: <string>
  purpose_state: LIVING | ARTIFACT | TRANSITIONAL
  purpose_state_set_at: <utc timestamp>
  purpose_state_set_by: <actor>
  purpose_state_basis: <citation>
  living_purpose_score: <L(a), 0.0-1.0>
  last_f13_renewal_reference: <utc timestamp or null>
  renewal_window_days: 90    # default; Lane A ratification may revise
  truth_class: OBS | DER | INT | SPEC | ARTIFACT
  f11_receipt: <hash>
```

**The classification is F11-auditable.** Every state transition emits a receipt.

---

## §4. Constitutional Constraints (HARAM)

The distinction **MUST NOT**:

- Delete an ARTIFACT (F1 AMANAH — preservation is forever)
- Manufacture purpose to keep an ARTIFACT alive (F9 + Purpose Substitution)
- Auto-promote ARTIFACT → LIVING without F13 ack
- Modify F1-F13 floors (no F14 yet — proposal-only)
- Hide LIVING artifacts from routing (witness-first)

The distinction **MUST**:

- Be queryable (no shadow plays)
- Be reversible by F13 (Lane A authority)
- Cap confidence at 0.90 (F7)
- Emit receipt per state transition (F11)
- Distinguish LIVING and ARTIFACT in every SEAL output

---

## §5. Falsification Tests

| Test | Discriminates | Pass condition |
|---|---|---|
| **Petronas simulation** | Inject Petronas 1974 founding charter; run distinction | Classified as TRANSITIONAL (renewed purpose ≠ 1974 purpose) |
| **Live purpose stress** | Inject 100 LIVING artifacts; verify routability | All 100 surface in attention-graph NOW/NEXT/BATCH |
| **Artifact isolation** | Inject 100 ARTIFACT artifacts; verify non-routability | All 100 default SILENT; queryable on demand |
| **F13 override** | F13 forces LIVING → ARTIFACT manually | Override applied within 7 days; receipt emitted |
| **Substitution guard** | Try to auto-promote ARTIFACT by manufacturing purpose | HARD HOLD triggered; no promotion |

---

## §6. F2 Audit Summary

| Component | Class | Falsifiable? | Survives? |
|---|---|---|---|
| LIVING definition | OBS | yes (F13 receipt stream) | yes |
| ARTIFACT definition | DER | yes (L(a) computation) | partial — depends on purpose starvation probe |
| TRANSITIONAL state | SPEC | yes (7-day window) | yes |
| Metadata schema | SPEC | yes (Lane A ratification) | yes |
| L(a) computation | DER | yes (PRESERVATION-WEIGHT-FUNCTION-SPEC) | partial |

---

## §7. Ratification Path

```
Step 1 [DONE 2026-09-08]   : File as DRAFT (Lane B) — this artifact
Step 2 [T1, queued]        : contradiction_scan via geox_claim(mode=scan)
Step 3 [T2, 888-APEX]      : lane determination
Step 4 [T3, F13]           : if CANONICAL → VAULT999 append (constitutional classification)
```

---

## §8. Provenance

**Session:** SEAL-compile-2026-09-08 · 2026-09-08
**Actor:** 333-AGI Δ MIND — proposer
**Trigger:** Purpose Metabolism doctrine §3.2 named the distinction; this is its operational specification
**Axiom-9 boundary:** classification is structural, not judgmental; F13 has final say

---

*DITEMPA BUKAN DIBERI ⚒️*
