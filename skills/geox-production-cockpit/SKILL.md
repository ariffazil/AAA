---
name: geox-production-cockpit
description: Control plane router for GEOX agentic Earth-reasoning stack. Classifies requests into OBSERVE, COMPUTE, INTERPRET, CHALLENGE, CERTIFY, DEPLOY, ACTUATE lanes and enforces non-negotiable state boundaries before routing to specialist skills or tool surfaces.
---

# 🏛️ GEOX Production Cockpit (Control Plane Router)

> **DITEMPA BUKAN DIBERI — Governed Control Plane for GEOX**

## 1. Core Purpose

The `geox-production-cockpit` is the primary control-plane routing skill for GEOX. It translates sovereign user intent (`F13 ARIF`) into bounded workflow executions across the 12-skill governed mesh, enforcing non-negotiable state boundaries and preventing prompt/codebase entropy.

---

## 2. Non-Negotiable State Boundary Enforcements

The cockpit strictly refuses to collapse the following distinct realities:
- $\text{File exists} \neq \text{Feature works}$
- $\text{Test passed} \neq \text{System deployed}$
- $\text{Registry passes} \neq \text{Science is valid}$
- $\text{GUI renders} \neq \text{Workflow is usable}$
- $\text{Model predicts} \neq \text{Interpretation is supported}$
- $\text{Commit pushed} \neq \text{Production is aligned}$

---

## 3. Intent Classification & Routing Matrix

Every inbound GEOX request must be classified into one of the 7 operational lanes:

| Intent Lane | Operational Target | Governing Specialist Skill | Required Evidence / Output |
|---|---|---|---|
| **OBSERVE** | Surface / Deployment / Registry Audit | `geox-reality-auditor` / `geox-data-ingestion-qc` | 6-Reality Audit Report / LAS & SEG-Y QC |
| **COMPUTE** | Deterministic Subsurface Physics | `geox-subsurface-scientist` | Physical Invariant Verification |
| **INTERPRET** | Geological Workflow & State Transition | `geox-interpretation-workflow` | Canonical `GeoProjectState` Transition |
| **CHALLENGE** | Scientific Falsification & Alternatives | `geox-subsurface-scientist` | Falsification Matrix & Epistemic Tags |
| **CERTIFY** | Test Suite & Machine Receipts | `geox-test-certifier` | Verified `pytest-receipt.json` |
| **DEPLOY** | Production Release Attestation | `geox-deployment-release` | `888_HOLD` → Signed Deployment Receipt |
| **ACTUATE** | Inter-Organ Consequence Routing | `geox-federation-bridge` | `888_HOLD` → WEALTH/WELL/arifOS Packets |

---

## 4. Governed 12-Skill Mesh Map

```text
geox-production-cockpit (Control Plane Router)
│
├── Tier 1 — Foundational Governance (Active)
│   ├── geox-reality-auditor          (6-reality surface & deployment audit)
│   ├── geox-subsurface-scientist     (Earth constraints & falsification rules)
│   ├── geox-test-certifier           (Multi-gate machine receipt generator)
│   └── geox-deployment-release       (Commit alignment & release attestation)
│
├── Tier 2 — Operational Productization
│   ├── geox-data-ingestion-qc        (LAS/SEG-Y/CRS header & null validator)
│   ├── geox-interpretation-workflow  (GeoProjectState transition engine)
│   ├── geox-gui-workbench            (MCP Apps workbench & linked views)
│   └── geox-mcp-contract-auditor     (Canonical surface & annotation parity)
│
└── Tier 3 — Enterprise Intelligence
    ├── geox-observability-incident   (Telemetry, blast radius & containment)
    ├── geox-model-evaluation         (Geoscience LLM/FM benchmark evaluation)
    └── geox-federation-bridge        (Consequence routing to WEALTH/WELL/arifOS)
```

---

## 5. Execution Protocol

1. **Observe Reality First:** Check git commit (`fafb6ddc`), live server state, and active tool manifests. Never accept narrative claims without empirical proof.
2. **Enforce Least Power:** Route tasks to the smallest capability tool or sub-skill capable of performing it.
3. **Domain Seal Isolation:** GEOX domain operations emit status tags (`OBSERVED`, `COMPUTED`, `INTERPRETED`, `CONTRADICTED`). Sealing authority (`999 SEAL`) is strictly reserved for `arifOS`.
4. **Emit Receipts:** Every completed workflow must produce an auditable JSON execution receipt.
