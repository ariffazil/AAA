# F1–F13 ↔ I-01–I-24 Mapping — With Institution Enforcement Per Plane

> **Status:** F13_RATIFIED_CHAT (2026-09-16) — convergence deliverable from Orthogonality Contract review
> **Companion to:** federation-orthogonality.md
> **Source:** Universal invariants I-01–I-24 from Orthogonality Contract v0.1-draft; Constitutional floors F1–F13 from arifOS constitution

## How to Read This Mapping

Each invariant (I-01 through I-24) maps to:
1. **Constitutional floor(s)** — which F-floor(s) encode the same principle
2. **Enforcement institution** — which institution bears primary enforcement responsibility
3. **Plane coverage** — which of the four planes each invariant applies to
4. **Current enforcement mechanism** — how it is actually enforced today (or PROPOSED if not yet)

**Legend:**
- H = Human plane, W = Workshop plane, P = Protocol plane, I = Implementation plane
- INST = institution (AAA / arifOS / VAULT999)
- LIVE = enforced in running code/config today
- CANON = enforceable via loaded doctrine fragments
- PROPOSED = defined in contract but not yet wired

---

## The Mapping

### I-01 — Human Sovereignty
**"No agent may override or impersonate a verified human final decision."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F13 (SOVEREIGN) | AAA (consent verification) + arifOS (verdict gate) | H, W, P, I | LIVE — F13HaltChannel.ts, consent protocol, SOUL.md bridge |

### I-02 — Authority Separation
**"The same actor may not independently approve, execute, validate, and witness the same high-impact action."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F1 (AMANAH) + F3 (TRI-WITNESS) | AAA (lease issuance) + arifOS (judgment separation) | W, P, I | LIVE — AutonomousForgeGate.ts, TriWitnessValidator.ts, change-contract separation |

### I-03 — No Self-Authorisation
**"No tool or agent may set its own execution authority."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F9 (ANTI-HANTU) + F13 (SOVEREIGN) | AAA (authority-envelope) + arifOS (seal gate) | W, P, I | CANON — authority-envelope doctrine; LIVE — arif_seal gate |

### I-04 — Explicit Action Class
**"Every request is classified before dispatch: OBSERVE, ANALYSE, PREPARE, ESCALATE, MUTATE, PUBLISH, EXECUTE."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F4 (CLARITY) | AAA (intent routing) | H, W, P, I | CANON — action-classification primitive; partially LIVE in FED router |

### I-05 — Bound Approval
**"Irreversible approval binds exact actor, target, operation, payload hash, policy version, expiry, nonce, and trace ID."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F1 (AMANAH) + F11 (AUDITABILITY) | AAA (approval binding) + arifOS (verification) + VAULT999 (recording) | P, I | CANON — authority-envelope tuple; PROPOSED in contract §5.5 |

### I-06 — Four-Truth Receipt
**"PASS requires transport AND execution AND semantic validation AND policy permission."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F3 (TRI-WITNESS) + F11 (AUDITABILITY) | VAULT999 (receipt chain) + arifOS (policy gate) | W, P, I | CANON — receipt-witness primitive; partially LIVE in VAULT999 writer |

### I-07 — No Silent Default
**"Missing material input must never become zero, false, empty, observed, recommendation, or PASS."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F7 (HUMILITY) | arifOS (admissibility) + AAA (input fidelity check) | H, W, P, I | CANON — evidence-contract primitive |

### I-08 — Input Fidelity
**"Every material input must have a consumed-field record and output reflection."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F11 (AUDITABILITY) | arifOS (admissibility gate) | W, P, I | CANON — evidence-contract primitive; PROPOSED input-fidelity blocking gate |

### I-09 — Evidence-Bound Named Claims
**"A public claim about a named person/institution requires evidence source, effective date, contradiction state, freshness, and public-eligibility review."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F3 (TRI-WITNESS) + F9 (ANTI-HANTU) | AAA (evidence disclosure) + HERMES (human edge filtering) | H, W | CANON — hermes-rasa doctrine, register-as-channel; LIVE in rasa_boundary.py |

### I-10 — Claim Typing
**"Observed, Derived, Interpreted, Assumed, Speculated, Unmeasured, Historical_Stale, Conflicted, Void are distinct states."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) | arifOS (epistemic tagging) | W, P, I | LIVE — epistemic tagging pipeline, aThinkGuard.ts |

### I-11 — Runtime Over Declaration
**"Source declaration is not runtime proof. Public state derives from live probes."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F7 (HUMILITY) | arifOS (probe verification) | W, P, I | CANON — probe-before-panic doctrine; LIVE in probe scripts |

### I-12 — Five-Manifest Truth
**"Source, build, runtime, public, and probe manifests are distinct."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F11 (AUDITABILITY) | arifOS (manifest verification) + AAA (visibility) | P, I | CANON — reality-alignment-kernel; PROPOSED manifest audit |

### I-13 — Tool Narrowness
**"A tool has one primary semantic contract. Multi-axis tools must declare active axis per invocation."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F8 (GENIUS) | arifOS (admissibility) + AAA (routing) | W, P, I | CANON — SYMBOL_TABLE.json + symbol-probe.py (C20) |

### I-14 — Protocol Role Separation
**"MCP invokes. A2A exchanges. HERMES interfaces. Coding agents change code. A-FORGE executes."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F1 (AMANAH) + F5 (PEACE²) | AAA (role enforcement) + arifOS (boundary check) | ALL | THIS FRAGMENT — the orthogonality principle itself |

### I-15 — Least Attention
**"An agent loads the smallest skill set sufficient for the task."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F4 (CLARITY) + F7 (HUMILITY) | AAA (routing intelligence) | H, W, P, I | CANON — attention-budget primitive; LIVE in skill trigger system |

### I-16 — No Duplicate Doctrine
**"One canonical governance skill, one evidence contract, one action-class model, one receipt model, one federation envelope."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F4 (CLARITY) + F11 (AUDITABILITY) | AAA (skill portfolio audit) | ALL | CANON — skill-portfolio-audit, naming-doctrine; LIVE in symbol-probe |

### I-17 — Safe Delegation
**"Delegation may reduce work, never transfer final accountability."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F1 (AMANAH) + F13 (SOVEREIGN) | AAA (lease issuance) + arifOS (verdict remains with kernel) | W, P | CANON — capability-lease model (contract §8); partially LIVE in handoff-contract |

### I-18 — Reversible Forging
**"Coding-agent change is branch/PR/test artifact by default. Merge, deploy, restart are separate actions."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F1 (AMANAH) | A-FORGE (execution boundary) + arifOS (merge verdict) | I | LIVE — A-FORGE change-contract, no-deploy-default in forge repos |

### I-19 — Receipt Is Evidence, Not Truth
**"A receipt proves what was recorded, not that the claim is true."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F3 (TRI-WITNESS) + F11 (AUDITABILITY) | VAULT999 (recording) + arifOS (validation) | W, P, I | LIVE — vault999-writer, MerkleReceiptAnchor.ts |

### I-20 — Calibration Before Promotion
**"A capability remains SPECULATED until it has metrics, calibration cases, negative controls, and abstention rules."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F7 (HUMILITY) | arifOS (promotion gate) + AAA (capability registry) | W, P, I | CANON — calibration-register-witness in GEOX; PROPOSED in capability-telemetry-audit |

### I-21 — No Personality Inference
**"Analysis models structures and evidence, not hidden motives or personality diagnoses."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F9 (ANTI-HANTU) + F10 (ONTOLOGY) | HERMES (human edge filter) + AAA (evidence disclosure) | H | LIVE — SOUL.md prohibitions, hermes-rasa doctrine, anti-hantu gate |

### I-22 — Time Is Part of Truth
**"A current-state claim without observation time, source, and freshness policy is not decision-grade."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F7 (HUMILITY) | arifOS (freshness check) + VAULT999 (timestamp chain) | ALL | CANON — evidence-contract freshness policy; LIVE in VAULT999 timestamps |

### I-23 — Error Containment
**"Public errors are sanitized. No file paths, secrets, hostnames, tokens, or stack traces become external."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F5 (PEACE²) + F12 (INJECTION) | A-FORGE (output sanitization) + AAA (surface guard) | H, I | LIVE — surface-guard.service, F12 injection defense |

### I-24 — Honest Abstention
**"UNMEASURED, CONFLICTED, INSUFFICIENT_DATA, UNAVAILABLE, HOLD, and VOID are successful outcomes."**

| Floor | Institution | Planes | Enforcement |
|---|---|---|---|
| F2 (TRUTH) + F7 (HUMILITY) + F13 (SOVEREIGN) | arifOS (admissibility) + AAA (routing) | ALL | CANON — evidence-contract, honest-abstention primitive; LIVE in arif_judge SABAR/VOID verdicts |

---

## Coverage Summary

| Plane | Invariants touching it | Primary enforcer |
|---|---|---|
| **Human** | I-01, I-04, I-07, I-09, I-15, I-21, I-23 | HERMES + AAA |
| **Workshop** | I-02, I-04, I-06, I-07, I-08, I-10, I-11, I-12, I-13, I-14, I-15, I-16, I-17, I-19, I-20, I-22, I-24 | AAA + arifOS |
| **Protocol** | I-02, I-04, I-05, I-06, I-07, I-08, I-10, I-11, I-12, I-13, I-14, I-15, I-16, I-17, I-19, I-20, I-22, I-24 | AAA + arifOS |
| **Implementation** | I-02, I-04, I-05, I-06, I-07, I-08, I-10, I-11, I-12, I-13, I-14, I-15, I-16, I-17, I-18, I-19, I-20, I-22, I-23, I-24 | A-FORGE + arifOS |

**Observation:** The Workshop and Protocol planes share the heaviest invariant load because they handle the most inter-agent data flow. The Human plane has fewer invariants touching it but the highest-consequence ones (I-01, I-21). The Implementation plane has the broadest coverage because it carries irreversible physical effects.

## Enforcement Status Gap

| Count | Status |
|---|---|
| 8 | LIVE (enforced in running code) |
| 13 | CANON (enforceable via loaded doctrine, not all wired to runtime gates) |
| 3 | PROPOSED (defined in contract, not yet implemented) |

**The gap:** 13 invariants are canon-enforced but not runtime-gated. This means an agent that doesn't load the relevant doctrine fragment can violate the invariant without mechanical prevention. The contract's Phase 1 (establish common primitives) should close this gap by wiring canonical primitives into runtime checks.

DITEMPA BUKAN DIBERI ⚒️
