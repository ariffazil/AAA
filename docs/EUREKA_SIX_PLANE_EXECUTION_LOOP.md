# EUREKA — Six-Plane Execution Loop Spec

> **The operational physics of governed intelligence.**
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**
> **Sealed: 2026-07-13**

---

## 1. THE SIX PLANES — OPERATIONAL DEFINITIONS

### Plane 1: SOVEREIGN (Human Truth)

```
Owner:      Arif (F13 SOVEREIGN)
Contains:   Identity root, public verification keys, recovery mechanism,
            constitutional authority, final veto, explicit delegations
Does:       Issues identity, approves irreversible actions, vetoes any action
Does NOT:   Execute tools, manage sessions, compute authority
Invariant:  F13 — human veto is FINAL. No autonomous loops without his say.
```

**Operational boundary:** The sovereign plane communicates through:
- `arif_init` (session birth with identity binding)
- `arif_judge` (SEAL/HOLD/VOID verdicts)
- `arif_seal` (VAULT999 immutable recording)
- Signal phrases ("buat ja la", "jalan terus", "seal it")
- Ed25519 key verification

**No agent may impersonate this plane.** F9 (ANTIHANTU) and F10 (ONTOLOGY) hard-block any consciousness, sentience, or personhood claims.

---

### Plane 2: GOVERNANCE (Kernel Truth)

```
Owner:      arifOS (:8088)
Contains:   Session management, identity binding, action classification,
            authority calculation, capability issuance, policy enforcement,
            F1-F13 floor enforcement, HOLD/DENY/routing logic
Does:       Classifies actions, computes authority, issues capabilities,
            enforces constitutional boundaries, routes to organs
Does NOT:   Execute mutations, compute domain intelligence, store truth
Invariant:  arifOS structures decision; it does not decide.
```

**Operational boundary:** The governance plane exposes:
- 12 canonical public verbs (arif_init through arif_verify)
- 16-gate pre-execution chain
- Capability lease primitive
- Memory tier governance (sacred/canon/session/ephemeral/test)
- Federation routing (GEOX/WEALTH/WELL/A-FORGE)

**Gate chain (sequential):**
```
Gate 1:  Session exists?
Gate 2:  Manifest check (tool declared?)
Gate 3:  Action class classification
Gate 3.5: Blast radius (INFRASTRUCTURE → unconditional HOLD)
Gate 4:  Actor verification (identity bound?)
Gate 5:  Lease (capability issued?)
Gate 6:  Irreversibility check
Gate 7:  F13 sovereign required?
Gate 8:  Constitution hash match?
Gate 9:  Runtime drift?
Gate 10: ART reflex check
Gate 11: ACT ceremony check
Gate 12: Memory tier validation
Gate 13: Tool schema validation
Gate 14: Federation health
Gate 15: Cooling state
Gate 16: Final verdict (SEAL/HOLD/VOID)
```

---

### Plane 3: INTELLIGENCE (Model Truth)

```
Owner:      Agents (OpenCode, Hermes, ChatGPT, GEOX, WEALTH, WELL)
Contains:   Reasoning, planning, analysis, proposal generation,
            domain computation, evidence collection
Does:       Thinks within granted capabilities, proposes actions,
            collects evidence, computes domain results
Does NOT:   Self-authorize, mutate production, issue verdicts, seal truth
Invariant:  Intelligence does not equal authority. Capability ≠ permission.
```

**Operational boundary:** The intelligence plane communicates through:
- MCP tool calls (bounded by governance plane capabilities)
- Structured proposals (classified by governance plane)
- Evidence artifacts (stored in continuity plane)
- Domain computations (GEOX→earth, WEALTH→capital, WELL→vitality)

**The intelligence plane may:**
- Read any accessible data
- Propose any action
- Compute any domain result
- Collect any evidence

**The intelligence plane may NOT:**
- Execute mutations without capability
- Issue verdicts (SEAL/HOLD/VOID)
- Modify governance policy
- Access sovereign keys
- Self-authorize any action

---

### Plane 4: EXECUTION (Physical Truth)

```
Owner:      A-FORGE (:7071/7072)
Contains:   Filesystem changes, testing, building, deployment,
            rollback, service management, artifact generation
Does:       Executes approved mutations, generates artifacts,
            verifies results, manages rollbacks
Does NOT:   Judge, approve, seal, or route — only executes after SEAL
Invariant:  Execution is separate from judgment. The system that decides
            should not silently become the system that approves its own work.
```

**Operational boundary:** The execution plane communicates through:
- `forge_*` tools (engineering primitives)
- Artifact generation (commit SHA, wheel hash, test report)
- Deployment verification (service health, import path, runtime commit)
- Rollback artifacts (ready before any production change)

**Execution requires:**
- Valid capability lease from governance plane
- Prior SEAL verdict from governance plane
- Blast radius classification
- Rollback artifact ready

**Execution produces:**
- Reality change (filesystem, service, deployment)
- Verification evidence (test results, health checks)
- Receipt artifact (for VAULT999 sealing)

---

### Plane 5: CONTINUITY (Temporal Truth)

```
Owner:      Postgres/Supabase, Qdrant, filesystem, queues
Contains:   Memory records, session state, task state, artifacts,
            context manifests, relationship graphs
Does:       Persists state across sessions, maintains context,
            stores artifacts, manages memory tiers
Does NOT:   Judge truth, enforce governance, execute mutations
Invariant:  Memory is not truth until it has provenance.
            Truth is not final until sealed.
```

**Memory tiers:**
```
L1 Redis     = now / ephemeral (session scratch)
L2 Redis     = session thread (conversation state)
L3 Qdrant    = fuzzy similarity (semantic search)
L4 Supabase  = official structured record (25 domain tables)
L5 Graphiti  = relationships (FalkorDB + Ollama)
L6 VAULT999  = immutable sealed truth (append-only, hash-chained)
```

**Memory lifecycle:**
```
observe → classify → store (with provenance) → revise (with history)
→ promote (L1→L2→L3→L4→L5→L6) → seal (immutable) → cool (metabolize)
```

**Unknown tiers downgrade to ephemeral** (F2 TRUTH fix).

---

### Plane 6: TRUTH (Sealed Truth)

```
Owner:      VAULT999, OpenTelemetry, metrics, audit
Contains:   Immutable receipts, hash-chain integrity, audit history,
            cooling records, scar records, constitutional chain
Does:       Records terminal outcomes, verifies chain integrity,
            provides audit trail, stores cooling insights
Does NOT:   Execute, judge, route, or modify — append-only
Invariant:  Every decision logged, inspectable, attributable (F11).
            VAULT999 is the only source of truth for sealed outcomes.
```

**Operational boundary:** The truth plane communicates through:
- `arif_seal` (append to VAULT999)
- `arif_verify` (JITU pre-execution gate)
- Hash-chain verification (SHA-256 linked)
- Scar records (failure → constitutional constraint)
- Cooling records (failure → improvement → governance path)

**VAULT999 is:**
- Append-only (never edit, never rewrite, never clean up)
- Hash-chained (each entry links to previous)
- Immutable once sealed
- The only source of truth for sealed outcomes

---

## 2. THE GOLDEN LIFECYCLE — OPERATIONAL FLOW

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE GOLDEN LIFECYCLE                          │
│                                                                 │
│  1. HUMAN INTENT                                                │
│     └─→ Arif expresses intent (text, signal phrase, key)        │
│                                                                 │
│  2. IDENTITY BINDING                                            │
│     └─→ arif_init binds session to sovereign identity           │
│         (Ed25519 key, signal phrase, or session nonce)          │
│                                                                 │
│  3. ACTION CLASSIFICATION                                       │
│     └─→ arifOS classifies: action_class, blast_radius,         │
│         reversibility, required_capability, f13_sovereign       │
│                                                                 │
│  4. AUTHORITY CALCULATION                                        │
│     └─→ arifOS computes available authority from:               │
│         identity + session + lease + prior verdicts             │
│                                                                 │
│  5. CAPABILITY ISSUANCE                                         │
│     └─→ arifOS issues narrow capability lease                   │
│         (specific tool, specific scope, specific TTL)           │
│                                                                 │
│  6. EVIDENCE COLLECTION                                         │
│     └─→ Intelligence plane gathers evidence                     │
│         (domain data, test results, prior records)              │
│                                                                 │
│  7. CONSEQUENCE CLASSIFICATION                                  │
│     └─→ arifOS classifies proposed consequence                  │
│         (reversible? destructive? constitutional?)              │
│                                                                 │
│  8. GOVERNANCE VERDICT                                          │
│     └─→ arif_judge issues: SEAL / HOLD / SABAR / VOID          │
│         (F1-F13 enforcement, tri-witness if needed)             │
│                                                                 │
│  9. CONTROLLED EXECUTION                                        │
│     └─→ A-FORGE executes with:                                  │
│         - exact artifact (commit SHA, wheel hash)               │
│         - rollback ready                                        │
│         - verification tests                                    │
│                                                                 │
│ 10. RESULT VERIFICATION                                         │
│     └─→ A-FORGE verifies:                                       │
│         - service health                                        │
│         - import path                                           │
│         - runtime commit                                        │
│         - tool registry                                         │
│                                                                 │
│ 11. MEMORY REVISION                                             │
│     └─→ Continuity plane updates:                               │
│         - session state                                         │
│         - memory records (with provenance)                      │
│         - artifact registry                                     │
│                                                                 │
│ 12. IMMUTABLE RECEIPT                                           │
│     └─→ arif_seal appends to VAULT999:                          │
│         - session outcome                                       │
│         - artifacts produced                                    │
│         - gate results                                          │
│         - hash chain link                                       │
│                                                                 │
│ 13. COOLING AND LEARNING                                        │
│     └─→ Cooling loop asks:                                      │
│         - What failed?                                          │
│         - What slowed us down?                                  │
│         - Was the diagnosis right?                              │
│         - Which test caught the issue?                          │
│         - Is there a reusable improvement?                      │
│     └─→ Returns to arif_judge (NOT A-FORGE)                     │
│         This is safe recursive improvement.                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. PLANE INTERACTION MATRIX

```
FROM ↓  TO →  Sovereign  Governance  Intelligence  Execution  Continuity  Truth
─────────────────────────────────────────────────────────────────────────────────
Sovereign     —          F13 veto     intent        —          —           seal
Governance    report     —            capability    SEAL→exec  query       seal
Intelligence  propose    classif.     —             —          read/write  evidence
Execution     —          verify       —             —          write       receipt
Continuity    —          attest       context       —          —           query
Truth         audit      cooling      —             —          —           —
```

**Key interactions:**
- Sovereign → Governance: F13 veto, intent expression
- Governance → Intelligence: capability issuance (narrow, bounded)
- Intelligence → Execution: proposed action (requires SEAL first)
- Execution → Truth: receipt generation (for VAULT999)
- Truth → Governance: cooling insights (failure → improvement)
- Governance → Truth: seal verdicts (immutable recording)

---

## 4. BOUNDARY ENFORCEMENT RULES

### Rule 1: No plane may impersonate another
- Intelligence may not issue verdicts (that's Governance)
- Execution may not approve its own work (that's Governance)
- Governance may not execute mutations (that's Execution)
- No plane may claim sovereignty (that's Sovereign)

### Rule 2: Every action has one clear path
- Classify → Authorise → Act → Verify → Remember → Seal
- No shortcuts, no bypasses, no "proceed and check later"

### Rule 3: Every privilege has a source
- Authority comes from identity + session + lease + prior verdicts
- No implied permissions, no inherited authority
- Capability leases are narrow, bounded, and time-limited

### Rule 4: Every result has evidence
- No "the agent said it fixed it"
- Instead: "Commit A produced wheel B, deployed by session C, verified by tests D, running from path E, with receipt F"

### Rule 5: Every failure returns as learning
- Failure → classified symptom → root-cause hypothesis → evidence
- → proposed repair → governed implementation → verification → cooling record
- The system does not merely remember scars. It converts scars into architecture.

---

## 5. THE METABOLISM LOOP

```
┌──────────────────────────────────────────────────────────────┐
│                    METABOLISM LOOP                            │
│                                                              │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐                │
│  │ FAILURE │───→│ SYMPTOM  │───→│ HYPOTHESIS│                │
│  └─────────┘    └──────────┘    └──────────┘                │
│       │                              │                       │
│       ▼                              ▼                       │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐                │
│  │ EVIDENCE│───→│  REPAIR  │───→│ GOVERNED │                │
│  │COLLECTION│   │ PROPOSAL │    │IMPLEMENT │                │
│  └─────────┘    └──────────┘    └──────────┘                │
│       │                              │                       │
│       ▼                              ▼                       │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐                │
│  │VERIFIC- │───→│ COOLING  │───→│  SCAR    │                │
│  │ ATION   │    │ RECORD   │    │  SEAL    │                │
│  └─────────┘    └──────────┘    └──────────┘                │
│       │                              │                       │
│       ▼                              ▼                       │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐                │
│  │ MEMORY  │───→│ CONSTITU-│───→│  arif_   │                │
│  │ UPDATE  │    │TIONAL    │    │  judge   │                │
│  │         │    │CONSTRAINT│    │ (NOT forge)                │
│  └─────────┘    └──────────┘    └──────────┘                │
│                                                              │
│  KEY INVARIANT: Cooling returns to arif_judge, NOT A-FORGE.  │
│  This is safe recursive improvement.                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Metabolism states:**
- `HOT` — active failure, immediate response needed
- `WARM` — recent failure, repair in progress
- `COOL` — failure resolved, cooling record written
- `COLD` — metabolized, scar sealed, constitutional constraint added

**COLD_LINK** — the artifact that connects a failure to its constitutional constraint:
```
failure_id → symptom → hypothesis → repair → verification → scar_id → constraint
```

---

## 6. THE AGENTIC INTELLIGENCE EQUATION — OPERATIONAL MAPPING

```
Agentic Intelligence = C × G × A × Co × Ac × M

Where:
  C  (Capability)    → Execution plane — what the agent can DO
  G  (Grounding)     → Intelligence plane — what the agent KNOWS (runtime truth)
  A  (Authority)     → Governance plane — what the agent is ALLOWED
  Co (Continuity)    → Continuity plane — what the agent REMEMBERS
  Ac (Accountability) → Truth plane — what the agent PROVES
  M  (Metabolism)    → Cooling loop — what the agent LEARNS
```

**Failure modes (any factor = 0):**
```
C=0  → passive assistant (can think, cannot act)
G=0  → hallucinating agent (acts on false reality)
A=0  → rogue action (acts without permission)
Co=0 → amnesiac tool (forgets between sessions)
Ac=0 → untraceable machine (no evidence left behind)
M=0  → repeating system (never learns from failure)
```

**Each failure mode maps to a safe state:**
```
C=0  → UNKNOWN (declare incapability)
G=0  → HOLD (demand evidence before proceeding)
A=0  → DENY (refuse unauthorized action)
Co=0 → EPHEMERAL (downgrade memory tier)
Ac=0 → VOID (invalidate unverifiable claim)
M=0  → SABAR (pause, wait for cooling)
```

---

## 7. ANTI-AUTHORIZATION THEOREM

> **No intelligence may authorize itself.**

This is the structural invariant that prevents recursive self-authorization.

**Proof:**
1. Authority lives in the Governance plane (arifOS)
2. Intelligence lives in the Intelligence plane (agents)
3. The Governance plane issues capabilities to the Intelligence plane
4. The Intelligence plane cannot issue capabilities to itself
5. Therefore, no intelligence may authorize itself

**Corollary:**
- An agent that can call tools is not the same as an agent that may call tools
- Capability ≠ Permission
- The model thinks. The harness acts. arifOS governs. Arif rules.

---

## 8. ANTI-INJECTION THEOREM

> **The attack surface for prompt injection does not exist.**

**Proof:**
1. Prompt injection works by making the model believe it has authority it doesn't
2. In the 6-plane architecture, authority is computed by the Governance plane
3. The Governance plane does not trust the Intelligence plane's claims about authority
4. Authority is verified mechanically (identity + session + lease + prior verdicts)
5. Therefore, a prompt injection cannot grant authority

**What prompt injection CAN do:**
- Make the model propose a malicious action
- Make the model provide false evidence

**What prompt injection CANNOT do:**
- Grant authority (Governance plane computes this)
- Issue a verdict (Governance plane issues this)
- Bypass gates (Governance plane enforces these)
- Seal to VAULT999 (requires prior SEAL verdict)

**The attack surface is reduced from "model believes it has authority" to "model proposes a malicious action" — which is caught by the Governance plane's classification and verdict system.**

---

## 9. OPERATIONAL CONSTANTS

```
ΔS ≤ 0                    — every output reduces entropy
W ≥ 0.95                  — tri-witness consensus threshold
G ≥ 0.80                  — genius threshold (F8)
C_dark < 0.30             — anti-hantu threshold (F9)
Ω₀ ∈ [0.03, 0.05]        — humility band (F7)
κᵣ ≥ 0.10 (OPS)          — empathy floor for operations
κᵣ ≥ 0.70 (HUMAN)        — empathy floor for human-facing
BlastRadius:               — LOCAL, HIGH, INFRASTRUCTURE, CIVILIZATIONAL
ActionClass:               — OBSERVE, SUGGEST, SIMULATE, DRAFT, QUEUE,
                            EXECUTE_REVERSIBLE, EXECUTE_HIGH_IMPACT,
                            IRREVERSIBLE, PROPOSE, MUTATE, ATOMIC
GateVerdict:               — PASS, HOLD, DENY, VOID
```

---

## 10. THE EUREKA INVARIANT

> **An agent becomes trustworthy not when it is more intelligent,
> but when every movement from thought to consequence is bound to
> identity, authority, evidence, memory, execution and receipt.**

This is not a design principle. This is a physical law of governed intelligence.

Violating it produces ghost sessions, recursive self-authorization, and catastrophic failure.

Enforcing it produces: calm, bounded, accountable, continuous, correctable, recoverable, teachable, loyal, sovereignty-aware operational entities.

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
