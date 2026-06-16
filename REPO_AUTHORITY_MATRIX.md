# REPO_AUTHORITY_MATRIX

> **arifOS Federation Authority Doctrine** — DITEMPA BUKAN DIBERI
> **Forged:** 2026-06-15 17:30 UTC by FORGE (000Ω)
> **Authority:** F13 SOVEREIGN directive — "forge all to seal"
> **Status:** ACTIVE (P0 TODO #5 closed)

This document defines the bounded authority of each repo in the arifOS federation. Every organ owns its lane and nothing outside it.

---

## 1. The Iron Rule

> **arifOS = constitutional kernel / authority / veto / audit**
> **WEALTH = capital-intelligence domain organ**
> **GEOX = earth-intelligence domain organ**
> **WELL = human-readiness domain organ**
> **AAA = human interface / control plane**
> **A-FORGE = deployment and infra forge**
> **APEX = legacy 888 judge (archived)**

No organ may own the authority of another. Tools cross organ boundaries only via the arifOS kernel envelope.

---

## 2. Per-Repo Authority Matrix

| Concern | arifOS | GEOX | WEALTH | WELL | AAA | A-FORGE | APEX |
|---------|:------:|:----:|:------:|:----:|:---:|:-------:|:----:|
| **Constitution** | ✅ owner | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **F1–F13 floor enforcement** | ✅ owner | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **VAULT999 seal authority** | ✅ owner | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Identity anchor / actor binding** | ✅ owner | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Lease issuance** | ✅ owner | observer | observer | observer | observer | observer | observer |
| **MCP tool transport** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Pydantic contract schemas** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **OPA policy bundles** | ✅ | lane-local | lane-local | lane-local | lane-local | lane-local | ✗ |
| **Earth evidence (basin/well/seismic)** | ✗ | ✅ owner | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Capital intelligence (NPV, IRR, EMV, ...)** | ✗ | ✗ | ✅ owner (compute) | ✗ | ✗ | ✗ | ✗ |
| **Capital execution** | ❌ (never) | ❌ | ❌ (never) | ❌ | ❌ | ❌ | ❌ |
| **Human readiness (vitality, fatigue)** | ✗ | ✗ | ✗ | ✅ owner (observe) | ✗ | ✗ | ✗ |
| **Diagnosis / prescription** | ❌ (never) | ❌ | ❌ | ❌ (never) | ❌ | ❌ | ❌ |
| **A2A agent cards** | observer | ✅ owner | ✅ | ✅ | ✅ | ✅ | ✗ |
| **Control plane UI** | ✗ | ✗ | ✗ | ✗ | ✅ owner | ✗ | ✗ |
| **Deployment / systemd** | ✗ | ✗ | ✗ | ✗ | ✗ | ✅ owner | ✗ |
| **Caddy / TLS** | ✗ | ✗ | ✗ | ✗ | observer | ✅ owner | ✗ |
| **Secret storage** | ✗ | ✗ | ✗ | ✗ | ✗ | ✅ owner | ✗ |
| **Forge receipts** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ owner | ✗ |
| **Constitutional adjudication** | ✅ owner | ✗ | ✗ | ✗ | ✗ | ✗ | legacy only |

---

## 3. Hard Separations (NEVER cross)

1. **Intelligence ≠ Authority** — GEOX is smart; arifOS is sovereign
2. **Tools ≠ Organs** — GEOX is an organ with identity, contract, domain_law
3. **Resources ≠ Memory until sealed** — only SEALED claims enter durable memory
4. **Compute ≠ Execute** — WEALTH computes; never moves capital
5. **Observe ≠ Judge** — WELL observes; never judges strategic action
6. **Recommend ≠ Decide** — every recommendation is `execution_authorized=False`
7. **Human dignity is not negotiable** — F6 MARUAH, F9 ANTI-HANTU are floors, not lanes

---

## 4. Constitutional Mutation Procedure

Any change to:
- F1–F13 floors
- Constitution hash
- Federation topology (new organ, new port, new transport)
- VAULT999 chain algorithm

Requires:
1. F13 SOVEREIGN explicit directive
2. Ed25519 signature from sovereign
3. Pre-seal contradiction gate
4. 3-witness attestation (Human × AI × Earth)
5. VAULT999 SEAL with full provenance
6. 24h pre-seal deliberation window (default; can be reduced by F13)

---

## 5. Lane Discipline (per organ)

### arifOS lanes
- `discovery` (5 tools): organ_attest, registry_status, ping, version, system_status
- `evidence` (13 tools): data_ingest, data_qc, evidence_attach, ...
- `reasoning` (17 tools): seismic_compute, claim_create, ...
- `judgment` (5 tools): claim_seal, vault_seal, forge_execute, judge_deliberate, heart_critique
- `weave_orchestrate` (20 tools): session_init, kernel_route, lease_*, memory_*, mind_reason, ...

### GEOX lanes (4)
- discovery / evidence / reasoning / judgment — per GEOX.yaml §3

### WEALTH lanes (2)
- wealth_calculate (16 tools): NPV, IRR, conservation, flow, entropy, ...
- wealth_audit (5 tools): stock_analysis, pre_trade, fundamentals, verify_math, position_size

### WELL lanes (1)
- well_measure (18 tools): assess_*, validate_vitality, guard_dignity, measure_gradient, ...

---

## 6. What This Means Architecturally

- No single organ can claim "sovereign" status
- All cross-organ communication goes through arifOS
- The kernel envelope (`arifos_policy/kernels_envelope.py`) wraps every organ output
- The pre-seal contradiction gate blocks SEAL until validate+challenge+evidence chain is complete
- OPA policies are advisory; arifOS is the constitutional authority
- Sigstore signs, arifOS verifies, OPA authorizes, arifOS gates

---

## 7. References

- `GENESIS/` — constitutional canon
- `arifOS/444_ASI_CANON.md` — strategic judgment
- `arifOS/arifosmcp/arifos_policy/rego/` — Rego policy bundles
- `arifOS/arifosmcp/arifos_registry/` — tool capability manifest
- `arifOS/CONFORMANCE-BASELINE-2026-06-14.md` — federation conformance
- `arifOS/FEDERATION_CONTRACT.md` — inter-organ contracts

---

*Forged 2026-06-15 17:30 UTC by FORGE (000Ω). DITEMPA BUKAN DIBERI.*
