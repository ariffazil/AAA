---
name: geox-production-cockpit
id: geox-production-cockpit
version: 1.1.0-2026.08.17
owner: GEOX
risk_tier: low
floor_scope: [F1, F2, F4, F7]
description: Control plane router for GEOX agentic Earth-reasoning stack. Classifies requests into OBSERVE, COMPUTE, INTERPRET, CHALLENGE, CERTIFY lanes and enforces non-negotiable state boundaries before routing to domain skills or tool surfaces.
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

*Updated 2026-08-17: Replaced 11 dead specialist skill refs with 7 canonical domain skills.*
*DITEMPA BUKAN DIBERI — Governed Control Plane for GEOX*
