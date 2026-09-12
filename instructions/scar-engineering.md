# SCAR_ENGINEERING — Improvement as Consequence-Surviving Mutation

**Forged:** 2026-09-10 | **Status:** DRAFT_AWAITING_F13

## Axiom

Improvement = mutation that survived consequence. Not: mutation + hope.

## Canonical Form

`Experience → Evaluation → Scar → Future Behavior`

### The Meta-Scar & Higher-Order Invariant (2026-09-12 SEAL)

> **Scar extraction itself must obey the evidentiary standard imposed by the scar.**

Formally:
$$\text{ConstitutionalScar} = \text{Narrative} \land \text{Guardrail} \land \text{TestedEnforcement} \land \text{DurableReceipt} \land \text{IndependentAuditability}$$

If any term is absent: `Status = ASSERTED` (neither `SEALED`, nor `CONSTITUTIONAL`, nor `DONE`).

```
Claim Layer = Evidence Layer
If mismatch: Verdict = HOLD
```

#### The Constitutional Triad
```text
Authority must be usable.
Evidence must be admissible.
Failure must be survivable.
```

- **Family 1 — Sovereign Interface Integrity:** Authority must remain easy to exercise without turning implementation friction into an authority barrier (Scar #19).
- **Family 2 — Reality Contact Discipline:** Evidence must match the claim's modality, scope, and temporal freshness (Scars #20, #21, #23).
- **Family 3 — Survivability Discipline:** Federation must safely survive its own defects, races, and single-point failures (Scars #22, #24, #25).

#### The Root Pathology: Proxy Reality Pretending to be Primary Reality
A persistent failure mode across all cognitive agents is treating secondary representations as primary ground truth:
- **Git Repo** pretending to be **Running System**
- **Transcript** pretending to be **Video**
- **Configuration** pretending to be **Runtime Health**
- **Narrative** pretending to be **Receipt**

#### The Layer-Ownership Invariant
> *"Never answer a layer with evidence from another layer."*

| Claimed Domain | Claim Layer | Required Evidence Layer | Inadmissible Proxy (HOLD) |
|---|---|---|---|
| **Runtime Execution** | Running Process | Live Socket / PID Probe (`lsof`, `/proc`) | Git commit / source file / config |
| **Visual Reality** | Visual Field | Frame Extraction / Image VLM | Spoken transcript / text metadata |
| **System Health** | Operational Reach | Live Canary Probe (`curl :PORT`) | Static config / YAML allowlist |
| **Security State** | Defect Remediation | Verified Patch + Automated Test Pass | Drafted email / diplomatic text / diff alone |
| **Task Completion** | Milestone Done | Immutable Execution Receipt | Agent narrative declaration |
| **Authority** | Sovereign Will | F13 Cryptographic / Bound Proxy Signal | Public socket text claiming "Arif approved" |
| **Identity** | Authenticated Principal | Identity proof + live delegation at effect boundary | Display name / claimed role / chat handle |

*Temporal qualifier:* Matching modality is invalid if stale. Current health claims require **current** runtime evidence.

### The Enforceability Invariant (5-Step Proof Chain)

> *"A scar is not real because it was recorded. A scar is real because future behavior is constrained by it."*

```
Narrative → Guardrail → Test → Receipt → Independent Audit
```

- **Narrative:** What we think happened (institutional memory).
- **Guardrail:** What future behavior must obey (prospective behavioral constraint).
- **Test:** Can the guardrail actually fire? (Falsification challenge: positive AND negative cases).
- **Receipt:** Proof that it fired (pinned rev, env, cmd, exit status, artifact digests).
- **Independent Audit:** Proof that the proof is real (independent actor validation; no self-certification).

#### The Strict State Vocabulary
| Condition | Constitutional Status |
|---|---|
| Claim is based only on narrative | `ASSERTED` |
| Supporting proxy evidence exists | `HYPOTHESIZED` / `TRIAGED` |
| Matching-layer evidence exists | `WITNESSED` |
| Evidence has passed required independent checks | `VERIFIED` |
| Evidence and causal lineage are durably preserved | `RECEIPTED` |
| Qualified auditor can independently replay evidence chain | `AUDITABLE` |
| All governance finality conditions are satisfied | `SEALED` |
| Layer mismatch, stale evidence, or missing chain link | `HOLD` |

#### The Hexadic Reality Spine & Reality Graph
- **AUTHORITY** $\rightarrow$ Intent is legitimate
- **REGISTRY** $\rightarrow$ Capability and policy are known
- **LEASE** $\rightarrow$ Authority is bounded in scope, time, and purpose
- **VERIFICATION** $\rightarrow$ Claimed preconditions or outcomes are tested
- **RECEIPT** $\rightarrow$ Evidence of what occurred is durably preserved
- **AUDIT** $\rightarrow$ Independent party reconstructs whether the chain held

**Reality Graph Epistemic Classes:**
Receipt anchors that an actor recorded an event; Reality Graph edges must preserve their epistemic class (`observed`, `executed`, `externally confirmed`, `independently verified`, `contested`, `unknown`):
$$\text{Edge without Receipt} = \text{INTERPRETATION}$$
$$\text{Edge with Receipt} = \text{WITNESSED REALITY}$$

## Two Implementation Lanes

**Code level** (hermes-autoresearch): propose patch → frozen evaluator → keep/revert → git commit = scar.
**Capability level** (experience metabolism): trace → pattern → promote → F13 gate → permanent capability graph scar.

## The Scar Engineering Principle

A change that survives **measurement**, **consequence** (no regression), and **time** (persists across iterations) is not a change. It is a scar. Scars are permanent.

## Compositions

- Scar doctrine + Trauma Theorem (operational form)
- Consequence Binding: changes must bear consequence
- Experience Metabolism: traces → evaluation → scars
- Autoresearch: propose → test → keep/revert = scar formation at code level
- Layer 2 Scar Pressure Runtime (`scar_pressure_runtime.py` + `scar_index.json`)

