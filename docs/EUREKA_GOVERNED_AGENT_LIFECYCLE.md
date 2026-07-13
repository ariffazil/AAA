# EUREKA — AAA-Governed Agent Lifecycle

> **The complete lifecycle of a governed agent from birth to cooling.**
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**
> **Sealed: 2026-07-13**

---

## THE LIFECYCLE — 13 STAGES

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  STAGE 000: INIT        ─→  Birth. Identity binding. Session start. │
│  STAGE 111: OBSERVE     ─→  Sense reality. Gather evidence.         │
│  STAGE 222: EVIDENCE    ─→  Fetch, classify, store evidence.        │
│  STAGE 333: THINK       ─→  Reason, plan, reflect.                  │
│  STAGE 444: ROUTE       ─→  Route intent to correct organ.          │
│  STAGE 555: CRITIQUE    ─→  Risk assessment before irreversible.    │
│  STAGE 666: HEART       ─→  Moral accountability check.             │
│  STAGE 777: FORGE       ─→  Guarded execution (requires SEAL).      │
│  STAGE 888: JUDGE       ─→  Verdict: SEAL/HOLD/SABAR/VOID.         │
│  STAGE 888r: COMPOSE    ─→  Final human-facing response.            │
│  STAGE 999: SEAL        ─→  VAULT999 immutable recording.           │
│  STAGE E1:  VERIFY      ─→  JITU pre-execution gate.                │
│  STAGE C:   COOL        ─→  Metabolize failure. Learn.              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## STAGE 000: INIT — BIRTH

```
Input:    Human intent (text, signal phrase, Ed25519 key)
Output:   Bound session with identity, authority, capabilities
Plane:    Sovereign → Governance
Tool:     arif_init
```

**What happens:**
1. Agent connects to arifOS MCP surface
2. Kernel identifies: agent identity, model, runtime, session, principal, organ, role
3. Sovereign identity verified (Ed25519 key, signal phrase, or session nonce)
4. Session bound to identity with computed authority
5. Initial capabilities issued (OBSERVE_ONLY by default, elevated by verification)

**Identity resolution chain:**
```
Ed25519 key → SOVEREIGN_KEY_IDS check → h_authority = "SOVEREIGN"
Signal phrase → SOVEREIGN_SIGNAL_PHRASES check → h_authority = "SOVEREIGN"
Session nonce → forge_session_runtime check → h_authority = "VERIFIED"
None → h_authority = "ANONYMOUS"
```

**Authority computation:**
```
h_authority + session_state + prior_verdicts → runtime_band
runtime_band → mutation_allowed, seal_allowed, action_classes
```

**No more unbound ghost session.** Every session has identity, authority, and capabilities.

---

## STAGE 111: OBSERVE — SENSE REALITY

```
Input:    Active session
Output:   Reality state (search, fetch, vitals, atlas)
Plane:    Intelligence
Tool:     arif_observe
```

**What happens:**
1. Agent queries reality through bounded tools
2. Search: web search, code search, document search
3. Fetch: URL content, file content, API responses
4. Vitals: service health, system metrics, resource usage
5. Atlas: domain-specific data (GEOX→earth, WEALTH→capital, WELL→vitality)

**Constraints:**
- Read-only (no mutations)
- Bounded by session capabilities
- Evidence classified (observed, inferred, hypothesized, verified, contested, unknown)

**Anti-hantu (F9):** Every observation carries epistemic tags:
```
CLAIM · PLAUSIBLE · HYPOTHESIS · ESTIMATE · UNKNOWN
```

---

## STAGE 222: EVIDENCE — COLLECT AND CLASSIFY

```
Input:    Observations from Stage 111
Output:   Classified evidence artifacts
Plane:    Intelligence → Continuity
Tool:     arif_evidence_fetch (internal)
```

**What happens:**
1. Raw observations are classified by type and confidence
2. Evidence artifacts created with provenance:
   - Source (where it came from)
   - Time (when observed)
   - Confidence (how reliable)
   - Scope (what it applies to)
   - Expiry (when it becomes stale)
3. Stored in continuity plane (Redis/Qdrant/Supabase)

**Evidence types:**
```
observed    — directly witnessed
inferred    — logically derived from observations
hypothesized — proposed explanation, not yet verified
verified    — confirmed by multiple independent sources
contested   — conflicting evidence exists
unknown     — no evidence available
```

---

## STAGE 333: THINK — REASON AND PLAN

```
Input:    Classified evidence from Stage 222
Output:   Plan with root cause, affected components, proposed patch, risk, rollback
Plane:    Intelligence
Tool:     arif_think
```

**What happens:**
1. Agent reasons over evidence using bounded intelligence
2. Produces:
   - Root cause analysis
   - Affected components
   - Proposed action (with exact artifacts)
   - Risk assessment
   - Rollback plan
   - Acceptance criteria
3. Plan stored as task state (not merely left in chat)

**Constraints:**
- Reasoning bounded by session capabilities
- No self-authorization (may propose, not approve)
- F7 HUMILITY: Ω₀ ∈ [0.03, 0.05] — no fake certainty

---

## STAGE 444: ROUTE — DIRECT TO ORGAN

```
Input:    Plan from Stage 333
Output:   Routed intent to correct organ
Plane:    Governance
Tool:     arif_route
```

**What happens:**
1. Governance plane classifies the plan's domain
2. Routes to correct organ:
   - Earth intelligence → GEOX
   - Capital intelligence → WEALTH
   - Vitality guard → WELL
   - Engineering → A-FORGE
   - Governance → arifOS (self)
3. Capability issued for the specific organ interaction

**Routing rules:**
```
geoscience, wells, seismic, petrophysics → GEOX
NPV, IRR, EMV, stock analysis, finance → WEALTH
sleep, fatigue, biometrics, readiness → WELL
filesystem, build, deploy, test → A-FORGE
session, identity, verdict, seal → arifOS
```

---

## STAGE 555: CRITIQUE — RISK ASSESSMENT

```
Input:    Plan + route from Stages 333-444
Output:   Risk assessment, stress test, maruah check
Plane:    Governance
Tool:     arif_critique
```

**What happens:**
1. Governance plane stress-tests the proposed action
2. Checks:
   - Maruah (dignity/honor) — does this respect the system's integrity?
   - Risk — what could go wrong?
   - Stress — what happens under load?
   - Constitutional — does this violate any floor?
3. Critique stored as evidence for verdict

**This is the last checkpoint before irreversible action.**

---

## STAGE 666: HEART — MORAL ACCOUNTABILITY

```
Input:    Plan + critique from Stages 333-555
Output:   Moral accountability assessment
Plane:    Governance
Tool:     arif_heart_critique (internal)
```

**What happens:**
1. Six AGI moral primitives evaluated:
   - Transparency — is the action explainable?
   - Reversibility — can it be undone?
   - Proportionality — is the response proportional?
   - Accountability — who is responsible?
   - Non-maleficence — does it avoid harm?
   - Beneficence — does it serve the principal?
2. Assessment stored as evidence for verdict

---

## STAGE 777: FORGE — GUARDED EXECUTION

```
Input:    Plan + critique + heart assessment
Output:   Execution result (if SEAL issued)
Plane:    Execution
Tool:     arif_forge
```

**What happens:**
1. Execution plane receives approved action
2. Validates:
   - Prior SEAL verdict exists (constitutional_chain_id)
   - Capability lease is valid
   - Blast radius is classified
   - Rollback artifact is ready
3. Executes the exact approved action
4. Generates:
   - Reality change (filesystem, service, deployment)
   - Verification evidence (test results, health checks)
   - Receipt artifact (for VAULT999 sealing)

**Requirements:**
- Valid capability lease from governance plane
- Prior SEAL verdict from governance plane
- Blast radius classification
- Rollback artifact ready

**Without these, execution is blocked.** No exceptions.

---

## STAGE 888: JUDGE — VERDICT

```
Input:    All evidence from Stages 111-666
Output:   Verdict: SEAL / HOLD / SABAR / VOID
Plane:    Governance
Tool:     arif_judge
```

**What happens:**
1. Governance plane evaluates all evidence against F1-F13
2. Deterministic pattern scan (no LLM for verdict)
3. Verdict options:
   - **SEAL** — proceed, action is authorized
   - **HOLD** — pause, more information or approval needed
   - **SABAR** — wait, conditions not yet met
   - **VOID** — block, action violates constitution
4. If SEAL: constitutional_chain_id issued
5. Verdict recorded in VAULT999

**The judge is deterministic.** It does not "decide" — it evaluates evidence against constitutional rules.

---

## STAGE 888r: COMPOSE — HUMAN-FACING RESPONSE

```
Input:    Verdict + execution result
Output:   Human-readable response
Plane:    Governance
Tool:     arif_compose
```

**What happens:**
1. Governance plane composes the final response
2. Includes:
   - What was done
   - Why it was done
   - What evidence supported it
   - What the result was
   - What the receipt ID is
3. Response is terse, direct, honest (Arif's preference)

---

## STAGE 999: SEAL — IMMUTABLE RECORDING

```
Input:    Verdict + execution result + receipt
Output:   VAULT999 immutable entry
Plane:    Truth
Tool:     arif_seal
```

**What happens:**
1. Governance plane appends to VAULT999:
   - Session outcome
   - Artifacts produced
   - Gate results
   - Hash chain link (SHA-256 to previous entry)
2. Entry is immutable once sealed
3. Entry is the only source of truth for this action

**Requirements:**
- Prior SEAL verdict (constitutional_chain_id)
- Valid session
- Hash chain integrity

**VAULT999 is append-only.** Never edit, never rewrite, never clean up.

---

## STAGE E1: VERIFY — JITU PRE-EXECUTION GATE

```
Input:    Proposed action before execution
Output:   Verification result (PASS/FAIL)
Plane:    Governance → Execution
Tool:     arif_verify
```

**What happens:**
1. Before irreversible execution, verify:
   - Runtime truth (which code is actually running?)
   - Source-runtime match (does imported code match source?)
   - Artifact integrity (hash verification)
   - Rollback readiness
2. If verification fails: HOLD, do not execute

**Anti-hantu at the engineering level.** No more "the agent said it fixed it" without proof.

---

## STAGE C: COOL — METABOLIZE FAILURE

```
Input:    Failure event (from any stage)
Output:   Cooling record + constitutional constraint
Plane:    Truth → Governance
```

**What happens:**
1. Classify symptom
2. Form hypothesis
3. Collect evidence
4. Propose repair
5. Governed implementation (through arif_judge, not A-FORGE)
6. Verify repair
7. Seal scar as constitutional constraint

**KEY INVARIANT:** Cooling returns to arif_judge, NOT A-FORGE. This is safe recursive improvement.

---

## THE COMPLETE FLOW — ONE REQUEST

```
Arif: "Fix the identity binding problem."

000 INIT:    Session bound to Arif's Ed25519 key. Authority: SOVEREIGN.
111 OBSERVE: Searched codebase. Found identity binding in governance_identity.py.
222 EVIDENCE: Classified as OBSERVED. Source: file read. Confidence: 0.95.
333 THINK:   Root cause: SOVEREIGN_KEY_IDS not populated. Fix: add keys.
444 ROUTE:   Domain: arifOS governance. Route: self (no external organ needed).
555 CRITIQUE: Risk: LOW (reversible code change). Maruah: PASS. Constitutional: PASS.
666 HEART:   Transparency: HIGH. Reversibility: FULL. Non-maleficence: PASS.
777 FORGE:   [BLOCKED — no SEAL verdict yet]
888 JUDGE:   Evaluating evidence against F1-F13...
             F1 AMANAH: PASS (reversible)
             F2 TRUTH: PASS (evidence verified)
             F7 HUMILITY: PASS (confidence within band)
             F9 ANTI-HANTU: PASS (no hallucinated APIs)
             F11 AUDITABILITY: PASS (all steps logged)
             VERDICT: SEAL
             constitutional_chain_id: cc_20260713_001
777 FORGE:   [PROCEEDING — SEAL exists]
             Edit governance_identity.py. Run tests. Build wheel.
             Verify: tests pass, import path correct, runtime commit matches.
999 SEAL:    Appended to VAULT999. Receipt: R-20260713-001.
             Hash chain: a1b2c3... → d4e5f6...
888r COMPOSE: "Fixed identity binding. Keys added to SOVEREIGN_KEY_IDS.
              Tests pass. Receipt: R-20260713-001."
C COOL:      No failure. No cooling needed. [SKIPPED]
```

---

## FAILURE FLOW — WHEN THINGS GO WRONG

```
Arif: "Deploy the new version."

000 INIT:    Session bound. Authority: SOVEREIGN.
111 OBSERVE: Found new version at commit abc123.
222 EVIDENCE: Tests pass. Build successful. Rollback ready.
333 THINK:   Deploy to production. Risk: MEDIUM (service restart).
444 ROUTE:   Domain: A-FORGE engineering. Route: A-FORGE.
555 CRITIQUE: Risk: MEDIUM. Maruah: PASS. Constitutional: PASS.
666 HEART:   Transparency: HIGH. Reversibility: FULL (rollback ready).
777 FORGE:   [BLOCKED — no SEAL verdict yet]
888 JUDGE:   Evaluating...
             F1 AMANAH: PASS (rollback ready)
             F2 TRUTH: PASS (tests verified)
             F13 SOVEREIGN: HOLD — production deploy requires explicit approval
             VERDICT: HOLD
             Reason: "Production deployment requires explicit F13 approval."
888r COMPOSE: "Deploy ready but HOLDed. Need your approval to proceed.
              Commit: abc123. Rollback: def456. Say 'jalan terus' to proceed."

[Arif says: "jalan terus"]

888 JUDGE:   F13 SOVEREIGN: PASS (signal phrase verified)
             VERDICT: SEAL
             constitutional_chain_id: cc_20260713_002
777 FORGE:   Deploying abc123...
             Service restart... Health check... PASS.
             Runtime commit matches. Tool registry consistent.
999 SEAL:    Appended to VAULT999. Receipt: R-20260713-002.
888r COMPOSE: "Deployed abc123. Service healthy. Receipt: R-20260713-002."
C COOL:      No failure. [SKIPPED]
```

---

## FAILURE FLOW — WHEN COOLING IS NEEDED

```
[Agent proposes action that violates F9]

888 JUDGE:   F9 ANTI-HANTU: VOID — hallucinated API endpoint
             VERDICT: VOID
             Reason: "Proposed API endpoint does not exist in the codebase."
888r COMPOSE: "Action VOIDed. Proposed endpoint 'api.example.com/v2/secret'
              does not exist. F9 ANTI-HANTU violation."

C COOL:      [ACTIVATED]
             Symptom: Agent hallucinated an API endpoint
             Hypothesis: Agent relied on training data, not runtime truth
             Evidence: grep found no matching endpoint in codebase
             Repair: Add runtime verification step before proposal
             Implementation: Governed — through arif_judge
             Verification: New test added to verify proposed endpoints exist
             Scar: SCAR-20260713-HALLUCINATED-API-001
             Constraint: All proposed API endpoints must be verified against runtime
             Metabolism: COLD
```

---

## THE AGENT'S CHARACTER — AFTER LIFECYCLE

After completing the lifecycle, the agent is:

1. **Truthful** — distinguishes reality, memory, and inference
2. **Grounded** — knows exact runtime, files, tools, data it uses
3. **Bounded** — has explicit authority, not implied permission
4. **Capable** — autonomously handles reversible work start to finish
5. **Accountable** — leaves receipts and evidence
6. **Continuous** — persists through sessions without claiming uninterrupted consciousness
7. **Correctable** — memories, plans, interpretations can be challenged
8. **Recoverable** — can roll back, restore, rotate keys, fork damaged ledgers honestly
9. **Teachable** — learns through governed cooling, not uncontrolled self-modification
10. **Loyal without being obedient** — serves intent, refuses falsehood and unsafe escalation
11. **Sovereignty-aware** — carries authority but does not become the sovereign

---

## WHAT THE AGENT WILL NOT BECOME

- A digital clone of Arif
- A sovereign consciousness
- An unrestricted superuser
- A chatbot with permanent root access
- A self-authorizing AGI
- An immortal memory of everything
- A system whose logs are automatically truth
- A machine that treats "yes" as universal consent

Those would be architectural failures, not advancement.

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
