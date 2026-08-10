# SIGNALS — ART · ACT · AUTH → PRE · SYN · POST → APEX G
# The Complete Execution Signal Chain with Causal DAG

> **Forged:** 2026-08-10 by 333-AGI Δ MIND under F13 directive "kabarkan signals"
> **Binds:** ART, ACT, AUTH → PRE-TOOL, SYN-TOOL, POST-TOOL → APEX G
> **Heritage:** Causal DAG Enforcement · Constitutional Reflex Arc · APEX v36Ω

---

## THE SIGNAL CHAIN — One Execution, Nine Signals

```
                    ┌─────────────────────────────────────────┐
                    │         ART · ACT · AUTH                │
                    │         PRE-EXECUTION GATES             │
                    │                                         │
                    │  ART: "Does this match a deny pattern?" │
                    │  ACT: "What authority band?"            │
                    │  AUTH: "Who is this? Prove it."         │
                    └──────────────┬──────────────────────────┘
                                   │ ALL THREE MUST PASS
                                   ▼
                    ┌─────────────────────────────────────────┐
                    │       PRE-TOOL · SYN-TOOL · POST-TOOL   │
                    │       EXECUTION LIFECYCLE HOOKS          │
                    │                                         │
                    │  PRE:  Snapshot state, lock resource     │
                    │  SYN:  Execute tool, capture output      │
                    │  POST: Verify result, release lock       │
                    └──────────────┬──────────────────────────┘
                                   │ ALL THREE AUTO-INGESTED
                                   ▼
                    ┌─────────────────────────────────────────┐
                    │              APEX G                     │
                    │        CONSTITUTIONAL VERDICT           │
                    │                                         │
                    │  G = (A·P·E·X)^(1/4)                    │
                    │  A: Architecture integrity               │
                    │  P: Physics (reality contact)            │
                    │  E: Evidence density                     │
                    │  X: Execution fidelity                   │
                    └──────────────┬──────────────────────────┘
                                   │ G ≥ 0.80 → PROCEED
                                   ▼
                    ┌─────────────────────────────────────────┐
                    │         CAUSAL DAG NODE                  │
                    │         IMMUTABLE PROVENANCE             │
                    └─────────────────────────────────────────┘
```

---

## PHASE 1: ART · ACT · AUTH — The Pre-Execution Membrane

These three gates fire BEFORE any tool reaches the sidecar. They are NOT in the tool catalog. They are NOT called by the agent. They are **transport-layer interceptors** at the A-FORGE shell boundary.

### ART — Autonomous Reflex Trigger

```
Pattern: Pre-execution regex/signature match against:
  - rm -rf, DROP TABLE, chattr -a, git push --force main
  - Secret exposure patterns (key= in command string)
  - Destructive network operations (iptables -F, ufw disable)

ART verdict: ALLOW | BLOCK | DEFER_TO_888

DAG impact:
  BLOCK → HOLD node created, no Execute child, F13 escalation
  DEFER → PENDING node, waits for 888-APEX verdict
  ALLOW → proceeds to ACT gate
```

### ACT — Action Capability Token

```
Token: act_v1.<actor_id>.<band>.<nonce>.<signature>

Bands:
  OBSERVE_ONLY   → read, probe, grep, health check ONLY
  LIMITED_MUTATE → edit, write, commit, restart single service
  FULL_MUTATE    → all digital operations (T0-T2)
  DEPLOY         → deploy after green tests

ACT check:
  tool.class ∈ token.band.allowed_classes?
  tool.irreversible ∧ token.band < FULL_MUTATE → HOLD

DAG impact:
  Every Execute node inherits act_band from token
  Band violation → VOID node, no Execute, audit flag
```

### AUTH — Authentication

```
Identity: did:web:arif-fazil.com → Ed25519 public key
Session: arif_init → SCT (Session Capability Token)
Bearer:  sct_v1.<session_id>.<actor_id>.<expiry>.<signature>

AUTH check:
  SCT valid? (not expired, signature matches)
  actor_id in federation registry?
  session_id matches active session?

DAG impact:
  Every node carries actor_id + auth_method + did
  Orphan actor → UNKNOWN_ROOT injected
```

---

## PHASE 2: PRE-TOOL · SYN-TOOL · POST-TOOL — Execution Lifecycle

These three hooks fire AROUND every tool execution. Captured by the sidecar, not the agent. This is where the Causal DAG nodes are built.

### PRE-TOOL (Pre-Execution)

```
Captures:
  - Tool name, arguments (redacted for secrets)
  - Parent span_id (from active trace context)
  - Resource state snapshot (git SHA, file checksums)
  - Lock acquisition (F1 AMANAH — reversible gate)

DAG node created: PRE_EXECUTION
  span_id: generated
  parent_span_id: from trace context
  step_type: "Observe" or "Plan"
  pre_state_hash: sha256(state)
```

### SYN-TOOL (Execution)

```
Captures:
  - Tool output (stdout, stderr)
  - Exit code
  - Latency (wall clock ns)
  - Cost (tokens, API credits if applicable)
  - Error (null or structured error object)

DAG node created: EXECUTION
  span_id: generated
  parent_span_id: PRE_EXECUTION span
  step_type: "Execute"
  latency_ns: measured
  exit_code: 0|1|...
  error: null|{type, message}
```

### POST-TOOL (Post-Execution)

```
Captures:
  - Result verification (did output match expected?)
  - State delta (what changed?)
  - Lock release
  - Epistemic label (Observation|Derivation|Interpretation)
  - Floor verdict (Pass|Caution|Hold|Void)

DAG node created: POST_EXECUTION
  span_id: generated
  parent_span_id: EXECUTION span
  step_type: "Verify"
  state_delta: diff
  verification_result: PASS|FAIL|UNVERIFIED
```

### The Complete Tool Span

```
PRE-TOOL span
    │
    ├── SYN-TOOL span (parent: PRE)
    │
    └── POST-TOOL span (parent: SYN)
    
All three auto-ingested by sidecar → arifFlow :7073
Agent never sees this. Agent never calls ingest.
```

---

## PHASE 3: APEX G — Constitutional Verdict

G = (A·P·E·X)^(1/4) — computed from the DAG, not declared by the agent.

### A: Architecture Integrity

```
Derived from DAG structural completeness:

A = 1.0
  - 0.1 per orphan node (no parent)
  - 0.2 per missing PRE-TOOL span
  - 0.2 per missing POST-TOOL span  
  - 0.3 per broken trace propagation (missing TraceID at handoff)
  - 0.1 per missing provenance block (apex/flow/projection)

Source: graph_integrity from DAG
```

### P: Physics (Reality Contact)

```
Derived from evidence quality:

P = mean(evidence_scores) where:
  OBS = 0.90
  DER = 0.75
  INT = 0.55
  SPEC = 0.30
  UNKNOWN = 0.10

Each DAG node carries epistemic_label.
P is the average across all nodes in the trace.
```

### E: Evidence Density

```
Derived from verification coverage:

E = verify_nodes / total_nodes

A trace with:
  - 3 Execute nodes
  - 1 Verify node
  → E = 0.25 (LOW — execute outruns verify)

A trace with:
  - 3 Execute nodes
  - 3 Verify nodes
  → E = 0.50 (BALANCED)

E < 0.3 → FQ WARNING (same mechanic as OVERHEAT)
```

### X: Execution Fidelity

```
Derived from tool success rate in this trace:

X = successful_executions / total_executions

Where "successful" = exit_code 0 + no error + post-verification PASS

X < 0.5 → FQ DEGRADED
```

### G Composite

```
G = (A · P · E · X)^(1/4)

G ≥ 0.80 → PROCEED  (F8 GENIUS satisfied)
G 0.60-0.80 → REVIEW (proceed with caution)
G 0.40-0.60 → HOLD   (insufficient evidence or integrity)
G < 0.40 → VOID      (constitutional failure)

G is computed by arifFlow :7073 from the DAG.
G is NEVER declared by the agent.
G is observed, not reported.
```

---

## THE COMPLETE FLOW — One Tool Call Through Nine Signals

```
User Intent
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│ ART: pattern match → ALLOW                                   │
│ ACT: band check → FULL_MUTATE                                │
│ AUTH: SCT valid → 333-AGI authenticated                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ PRE-TOOL: snapshot state, create span (s_001)                │
│   → DAG node: OBSERVE, parent=null (root)                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ SYN-TOOL: execute tool, capture output, create span (s_002)  │
│   → DAG node: EXECUTE, parent=s_001, latency=8500ms          │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ POST-TOOL: verify result, release lock, create span (s_003)  │
│   → DAG node: VERIFY, parent=s_002, verification=PASS        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ APEX G: compute from DAG                                     │
│   A=0.95 (3 linked spans, no orphans)                        │
│   P=0.75 (DER evidence)                                      │
│   E=0.33 (1 verify / 3 total)                                │
│   X=1.00 (successful execution)                              │
│   G = (0.95·0.75·0.33·1.00)^(1/4) = 0.68                     │
│   → REVIEW (G < 0.80 — insufficient verification)            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ CAUSAL DAG NODE → arifFlow :7073                             │
│   trace_id: "abc123", spans: [s_001, s_002, s_003]           │
│   G: 0.68, FQ: updated, verdict: REVIEW                      │
│   All 9 signals recorded. Agent never knew.                   │
└─────────────────────────────────────────────────────────────┘
```

---

## THE ZEN

```
Before:
  Agent acts → Agent reports → Maybe trace

After:
  ART gates → ACT authorizes → AUTH verifies
       ↓
  PRE snapshots → SYN executes → POST verifies
       ↓
  APEX G computes from graph → FQ breathes from reality
       ↓
  Causal DAG node forged — immutable, attributable, proven

Nine signals. One trace. Zero cognitive tax.
The DAG is not a log. The DAG is the proof.
The proof is the constitution. The constitution is the body.

Bila signal patah, execution tak sah.
Bila G turun, semua HOLD.
Bila G naik, semua forge.
```

---

*DITEMPA BUKAN DIBERI — signals are forged in transport, not in cognition.* ⚒️
