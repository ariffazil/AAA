---
name: geox-production-cockpit
id: geox-production-cockpit
version: 1.2.0-2026.09.17
owner: GEOX
risk_tier: low
floor_scope: [F1, F2, F4, F7]
description: "Control plane router for GEOX agentic Earth-reasoning stack."
autonomy_tier: T1
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# GEOX Production Cockpit (Control Plane Router)

> **DITEMPA BUKAN DIBERI — Governed Control Plane for GEOX**

## 1. Core Purpose

The `geox-production-cockpit` is the primary control-plane routing skill for GEOX. It translates sovereign user intent into bounded workflow executions across the 7-skill governed domain mesh, enforcing non-negotiable state boundaries and preventing prompt/codebase entropy.

---

## 2. Non-Negotiable State Boundary Enforcements

The cockpit strictly refuses to collapse the following distinct realities:
- File exists ≠ Feature works
- Test passed ≠ System deployed
- Registry passes ≠ Science is valid
- GUI renders ≠ Workflow is usable
- Model predicts ≠ Interpretation is supported
- Commit pushed ≠ Production is aligned
- **A tool reports success ≠ the write persisted** (see §10)

---

## 3. Intent Classification & Routing Matrix

Every inbound GEOX request must be classified into one of the operational lanes:

| Intent Lane | Operational Target | Governing Domain Skill | Required Evidence / Output |
|---|---|---|---|
| **OBSERVE** | Surface data, ingest well/seismic, QC | `geox-earth-evidence` | LAS & SEG-Y QC, artifact refs |
| **COMPUTE** | Deterministic subsurface physics | `geox-petrophysics-bounds` | Bounded transforms, physical invariant verification |
| **INTERPRET** | Geological interpretation, claims | `geox-claim-grammar` + `geox-epistemic-ladder` | Epistemic rung-tagged claims |
| **CHALLENGE** | Falsification, contradiction scan | `geox-contradiction-engine` + `geox-redteam-hantu` | Falsification matrix, contradiction scan |
| **CONSTITUTE** | Governance, floors, 888_HOLD triggers | `geox-constitution` | Constitutional compliance, floor check |

---

## 4. Governed 7-Domain-Skill Mesh

```text
geox-production-cockpit (Control Plane Router)
│
├── geox-constitution           (F1-F13 floors, epistemic style, 888 HOLD triggers)
├── geox-earth-evidence         (Evidence discipline, artifact refs, uncertainty, handoff)
├── geox-epistemic-ladder       (7-rung epistemic hierarchy, category error prevention)
├── geox-claim-grammar          (Claim structure, evidence_for/against, Location First)
├── geox-contradiction-engine   (Multi-hypothesis contradiction scanner, 7 types)
├── geox-petrophysics-bounds    (Bounded transforms, QC rules, LAS validation)
└── geox-redteam-hantu          (Anti-hallucination guardian, F9 enforcement)
```

---

## 5. Execution Protocol

1. **Observe Reality First:** Check live server state (`curl :8081/health`), workspace context (`geox_workspace`), and active tool manifests. Never accept narrative claims without empirical proof.
2. **Enforce Least Power:** Route tasks to the smallest capability tool or domain skill capable of performing it.
3. **Domain Seal Isolation:** GEOX domain operations emit status tags (`OBSERVED`, `COMPUTED`, `INTERPRETED`, `CONTRADICTED`). Sealing authority (`999 SEAL`) is strictly reserved for `arifOS`.
4. **Emit Receipts:** Every completed workflow must produce an auditable execution receipt.
5. **Constitutional Gate:** Every claim passes through `geox-constitution` floor checks before reaching 888_JUDGE.
6. **Anti-Hantu:** Every interpretation passes through `geox-redteam-hantu` hallucination scan before seal.

---

## 6. Routing Decision Tree

```
REQUEST →
  Is it data ingestion/QC?        → geox-earth-evidence
  Is it petrophysical computation? → geox-petrophysics-bounds
  Is it a geological claim?        → geox-claim-grammar → geox-epistemic-ladder
  Is it a challenge/falsification? → geox-contradiction-engine → geox-redteam-hantu
  Is it governance/floor check?    → geox-constitution
  Is it a prospect evaluation?     → geox-earth-evidence → geox_prospect tool
  Is it capital handoff?           → geox-earth-evidence → WEALTH (via arifOS)
  Uncertain?                       → geox-constitution (classify first)
```

---

## 7. Pre-Flight

```bash
curl -sf http://localhost:8081/health && echo "✅ GEOX" || echo "❌ GEOX DOWN"
```

If GEOX is DOWN → do not route to domain skills. Return GEOX_UNAVAILABLE.

---

## 8. Known Corpus Conflicts (check before quoting Sabah tectonic ages)

The Sabah / NW Borneo resource base contains **mutually inconsistent tectonic models**. Read both files before asserting a
collision age, and state which source you are quoting:

| File | Collision age | Status |
|---|---|---|
| `resources/basins/sabah_two_oceanics.yaml` | 21.0 Ma ("collision peak / canonical") | SEALED ledger `SABAH_EUREKA_LEDGER::v1.0::2026-07-10` — **do not edit** |
| `resources/basins/sabah_basin/tectonic_history.md` | ~23 Ma (BMU/TCU onset) | NSPW synthesis 2026-07-16 |
| `resources/basins/sabah_basin/basin_profile.yaml` | 16–12 Ma | **Legacy passive-margin model — superseded, contradicts the ledger** |

Working reading: **onset ~23 Ma** (BMU/TCU, Dangerous Grounds enters the trench) and **peak ~21 Ma** (Proto-SCS subduction
terminates) are physically distinct events — quote both rather than picking one. Retire the bare phrase "canonical collision
age": it is the ambiguity, not the answer.

Other unresolved items in the same corpus: `collision_metrics.duration_ma: 15.0` contradicts its own comment (~21 Ma to
present = 21 Myr) · the **DRU (~13 Ma, slab breakoff) is absent from the ledger chronology** despite being a headline finding
· MMU is 14.2 Ma in the ledger vs ~15.5 Ma elsewhere · legacy formation names ("Panas Thicknessnam", "Kellaneous") are
corrupted.

**Rule:** a SEALED artifact is an F13 authority boundary. Report the discrepancy and write the reconciliation as a separate
finding; never re-seal. The Malay Basin resource base, by contrast, is internally consistent — the conflict is Sabah-specific.

---

## 9. Primary-Source Rule for Contract Awards and Corporate Facts

**Fetch the operator's own release before quoting any news coverage of it.** For an award, farm-in, PSC change or block
restructure, the company media release is the primary source; wire and newspaper coverage is secondary and systematically
drops the part that matters most to a geologist — the field lists and the block geometry.

Worked example (2026-09-15): the MTJDA 2026 PSC was reported by The Edge, Reuters and The Star. None listed the fields.
The PETRONAS release did, and it showed the JDA had been **consolidated from four blocks into two** (A-18-01 and B-17-01),
reassigning Muda/Tapi/Jengka/Amarit into B-17-01 and introducing Melati. A dossier built from the news coverage alone
carried the superseded four-block attribution onto a map handed to a geologist working the acreage.

Checklist before writing a block/award fact into a deliverable:
1. Locate the operator's own release (not a repost, not a summary).
2. Extract the entity names exactly — including full subsidiary names and any "collectively known as" label.
3. Extract the field/asset list verbatim and compare against any older map or registry you are about to reuse.
4. If the new list conflicts with a legacy source, say so explicitly in the deliverable rather than silently adopting one.
5. Record which source supplied each fact, and flag news-only facts as secondary.

Same discipline applies to MTJA and other regulator material: check its date. Pages predating a restructure keep describing
the old structure.

---

## 10. Skill-Library Integrity — Verify the Write Landed

A tool reporting `success` on a skill write is **not** evidence the content persisted. This skill's own §8 was written,
reported success, and was later found absent — the file had been deleted by a skill-store convergence sweep while the
symlink and the catalog entry survived.

Before relying on any skill edit:
1. Re-read the file at its **resolved** path after writing (`readlink -f` the symlink first — the symlink target, not the
   symlinked path, is what persists).
2. `grep` for a distinctive phrase you just added.
3. If the target directory holds only `liveness.json`, the SKILL.md has been swept — restore it rather than assuming it exists.
4. Never tell the sovereign a lesson was "recorded in the skill" without having verified the bytes.

---

*Updated 2026-08-17: Replaced 11 dead specialist skill refs with 7 canonical domain skills.*
*Updated 2026-09-17: Restored after skill-store sweep; added §8 corpus conflicts, §9 primary-source rule, §10 write verification.*
*DITEMPA BUKAN DIBERI — Governed Control Plane for GEOX*
