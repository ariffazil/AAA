# Six-Plane Execution Loop v1 — Protocol Specification

> **Status:** CONSTITUTIONAL DRAFT — F13 ratified architecture, awaiting implementation seal
> **Date:** 2026-07-13
> **Author:** Hermes (on Arif F13 directive, EUREKA architecture)
> **Supersedes:** None (new protocol spec)
> **Governs:** All plane-boundary crossings in arifOS federation

---

## 1. Purpose

This document specifies the operational protocol for the six-plane Zen architecture ratified in the EUREKA session (2026-07-13). It defines:

- The exact message envelope format at each plane boundary
- The timing constraints and performance budget (Wawa D2)
- The degradation modes when any plane is unreachable (Wawa D1)
- The failure escalation paths across all 12 steps
- Concrete API contracts that P1 items implement against

The protocol enforces **classify-first ordering**: every action is classified BEFORE authority is checked, preventing the catch-22 where gates receive partial facts.

---

## 2. Six-Plane Architecture — Quick Reference

| # | Plane | Owner | Role | Epistemic Role | Must NOT |
|---|-------|-------|------|----------------|----------|
| P1 | **Sovereign** | Arif (F13) | Identity root, keys, veto, delegation | Human truth | Grant temporary capability as irrevocable ownership |
| P2 | **Governance** | arifOS kernel | Session, classification, authority, capability, policy | Kernel truth | Execute production work OR perform intelligence reasoning |
| P3 | **Intelligence** | Hermes, OpenCode, GEOX, WEALTH, WELL | Think, analyse, propose, plan | Model truth | Inherit sovereignty OR self-authorise execution |
| P4 | **Execution** | A-FORGE, tools, shell | Build, deploy, test, mutate | Physical truth | Adjudicate OR judge OR seal |
| P5 | **Continuity** | Postgres, Supabase, filesystem, memory stores | Memory, state, artifacts, context | Temporal truth | Treat its records as immutable truth |
| P6 | **Truth** | VAULT999, OpenTelemetry, metrics, traces | Receipts, ledgers, telemetry, audit | Sealed truth | Revise its own records OR issue verdicts |

---

## 3. Message Envelopes (Boundary Contracts)

Every plane-boundary crossing uses a structured envelope. Envelopes are NOT tool calls — they are protocol messages that carry intent, identity, evidence, and consequence.

### 3.1 Envelope Base Schema

```json
{
  "protocol_version": "v1",
  "envelope_type": "<see below>",
  "source_plane": "SOVEREIGN | GOVERNANCE | INTELLIGENCE | EXECUTION | CONTINUITY | TRUTH",
  "target_plane": "<same enum>",
  "session_id": "<session bound at governance>",
  "actor_id": "<who initiated this crossing>",
  "actor_verified": true | false,
  "epoch": "<ISO-8601 UTC>",
  "ttl_seconds": <max lifetime>,
  "trace_id": "<distributed trace ID>",
  "payload": { <plane-specific payload> },
  "witness": {
    "human": "<sovereign signal or null>",
    "ai": "<model attestation or null>",
    "external": "<measurement evidence or null>"
  },
  "hash": "sha256:<canonical hash of fields above>"
}
```

### 3.2 Boundary Envelope Types

#### `SovereignDirective` — P1→P2

Crossing: Sovereign → Governance

Payload:
```json
{
  "intent": "ACTIVATE | DEACTIVATE | DELEGATE | REVOKE | VETO | SEAL | ESCALATE",
  "scope": "<target actor or capability scope>",
  "authority_level": "FULL | LIMITED_MUTATE | OBSERVE_ONLY | SABAR",
  "ttl_seconds": 86400,
  "reason": "<human-readable justification>",
  "signature": "ed25519:<hex>"
}
```

Constraints:
- Only crosses P1→P2 boundary
- Requires `actor_verified=true` with F13 Ed25519 key
- If signature verification fails → VOID at governance, no further dispatch
- TTL cap: 86400s (24h). Sovereign directive beyond 24h must be re-signed.

Degradation mode (P1 unreachable):
- Platform defaults preserved (no new authority granted, no existing authority revoked)
- All `required_authority=F13_SOVEREIGN` actions go to HOLD
- See §6 for full degradation details

---

#### `AuthorityGrant` — P2→P3

Crossing: Governance → Intelligence

Payload:
```json
{
  "session_id": "<bound session>",
  "grant_id": "<uuid>",
  "capabilities": [
    {
      "tool": "arif_observe | arif_think | arif_route | ...",
      "mode": "<specific mode>",
      "scope": "<parameter constraints>",
      "max_calls": <integer>,
      "ttl_seconds": <seconds>
    }
  ],
  "mutate_allowed": false,
  "seal_allowed": false,
  "delegate_allowed": false,
  "max_chain_depth": 0,
  "expires_at": "<ISO-8601>",
  "restricted_evidence_classes": ["OBS", "DER", "INT"],
  "witness_requirements": {
    "human_required": false,
    "ai_required": true,
    "external_required": false
  }
}
```

Constraints:
- Capabilities are NARROW — tool + mode + scope bounded
- Each capability has its own ttl, max_calls, and scope
- `mutate_allowed` defaults to false — intelligence MUST NOT mutate
- If Intelligence receives a grant but exceeds any capability boundary → HOLD, notification logged to P5+P6
- LLM token pressure: if Intelligence plane exceeds configured token budget, capabilities narrowed further

Degradation mode (P2 unreachable):
- All active grants marked PENDING_RENEWAL — existing operations complete
- No new grants issued
- Intelligence plane operates in fallback: OBSERVE_ONLY, no mutation, no seal
- See §6

---

#### `ActionProposal` — P3→P2

Crossing: Intelligence → Governance

Payload:
```json
{
  "session_id": "<bound session>",
  "proposal_id": "<uuid>",
  "intent": "<natural language description>",
  "action_class": "OBSERVE | MUTATE_REVERSIBLE | MUTATE_IRREVERSIBLE | SEAL | SEAL_COOLING",
  "domain": "filesystem | network | database | deploy | config | key | vault | memory | tool",
  "proposed_verb": "<specific action verb>",
  "target_resource": "<URN or path>",
  "evidence": [
    {
      "type": "OBS | DER | INT | SPEC",
      "source": "<evidence source>",
      "claim": "<what the evidence shows>",
      "confidence": 0.0–1.0
    }
  ],
  "estimated_blast_radius": "LOW | MEDIUM | HIGH | CRITICAL",
  "estimated_reversibility": "FULLY_REVERSIBLE | ROLLBACK_POSSIBLE | CHECKPOINT_REQUIRED | IRREVERSIBLE",
  "alternatives": ["<option A>", "<option B>"],
  "urgency": "ROUTINE | ATTENTION | CRITICAL",
  "authority_requested": "OBSERVE_ONLY | LIMITED_MUTATE | FULL | F13_SOVEREIGN"
}
```

Constraints:
- Intelligence must classify the action BEFORE governance checks authority
- Intent is natural language — governance plane interprets via structured classification
- Evidence array must have at least one entry for MUTATE actions (F2 TRUTH)
- Urgency=CRITICAL reduces latency budget (see §5) but does NOT bypass governance
- If action_class conflicts with authority_requested (e.g., MUTATE_IRREVERSIBLE but OBSERVE_ONLY) → governance rejects at classification step

Degradation mode (P3 unreachable):
- No proposals submitted. System idle on intelligence.
- Existing proposals still being processed by governance are completed
- See §6

---

#### `ExecutionLease` — P2→P4

Crossing: Governance → Execution

Payload:
```json
{
  "lease_id": "<uuid>",
  "proposal_id": "<from ActionProposal>",
  "session_id": "<bound session>",
  "capability": {
    "tool": "<exact tool name>",
    "parameters": { "<bounded key-value pairs>" },
    "working_directory": "<path>",
    "environment_variables": ["<safelisted names>"],
    "allowed_commands": ["<safelisted shell commands>"],
    "forbidden_patterns": ["rm -rf /", "DROP DATABASE", "..."]
  },
  "constraints": {
    "timeout_seconds": <integer>,
    "max_retries": <integer>,
    "rollback_required": false,
    "human_approval_required_before": false,
    "human_approval_required_after": false,
    "blast_radius": "LOW | MEDIUM | HIGH | CRITICAL"
  },
  "verification_required": {
    "health_check_after": true,
    "import_verify_after": false,
    "tool_registry_check_after": false,
    "seal_chain_verify_after": false
  },
  "seal_on_complete": "<seal type or null>",
  "expires_at": "<ISO-8601 — must be < 600s from issue>"
}
```

Constraints:
- ExecutionLease TTL is capped at 600s (10 min). Longer executions need renewal.
- Parameters are bounded — exact values, not templates. No shell interpolation of user input.
- `forbidden_patterns` is a machine-enforced deny list alongside the F1-F13 floor checks
- Tool name must match exactly what A-FORGE has registered in its tool registry
- If Execution plane does not have the registered tool → lease is VOID, HOLD, escalation

Degradation mode (P4 unreachable):
- No execution possible. All leases expire.
- Intelligence plane receives `EXECUTION_DOWN` signal
- Governance marks all pending MUTATE proposals as HOLD_PLANE_DOWN
- See §6

---

#### `ExecutionReceipt` — P4→P2 (and P4→P6)

Crossing: Execution → Governance (+ mirrored to Truth)

Payload:
```json
{
  "lease_id": "<from ExecutionLease>",
  "session_id": "<bound>",
  "status": "SUCCESS | FAILURE | TIMEOUT | REJECTED | PARTIAL",
  "exit_code": <integer>,
  "stdout_truncated": <length>,
  "stderr_truncated": <length>,
  "output_hash": "sha256:<hex of full output>",
  "artifacts_created": ["<path>", "<path>"],
  "artifacts_modified": ["<path>", "<path>"],
  "artifacts_deleted": ["<path>", "<path>"],
  "rollback_artifact": "<path or null>",
  "health_after": {
    "service_responding": true | false,
    "import_resolves": true | false | null,
    "tool_count_unchanged": true | false | null
  },
  "timing": {
    "lease_issued": "<ISO-8601>",
    "execution_start": "<ISO-8601>",
    "execution_end": "<ISO-8601>",
    "elapsed_ms": <integer>
  }
}
```

Constraints:
- MUST be delivered to both Governance (P2) and Truth (P6) — dual-write
- If P2 unreachable → deliver to P6 only, P2 reads from P6 on recovery
- `artifacts_*` arrays are authorative for continuity plane (P5) state updates
- `rollback_artifact` must be populated if the original lease required rollback
- If status=FAILURE, the receipt carries full stderr for cooling loop analysis

Degradation mode (P6 unreachable for mirror):
- Local receipt preserved at P4 in durable queue
- Retry every 30s, max 5 retries, then HOLD with P6_DOWN signal
- See §6

---

### 3.3 Auxiliary Boundary Envelopes

#### `MemoryOperation` — P3→P5 or P4→P5

Crossing: Intelligence/Execution → Continuity

Payload:
```json
{
  "operation": "WRITE | READ | SEARCH | UPDATE | DELETE | QUARANTINE",
  "memory_class": "KSR | LEDGER | TELEMETRY | COOLING",
  "content": "<structured or unstructured>",
  "ttl_hours": <hours before automatic archival>,
  "supersedes": "<memory_id or null>",
  "session_id": "<bound>",
  "epistemic_tag": "OBS | DER | INT | SPEC",
  "confidence": 0.0–1.0,
  "expires_at": "<ISO-8601 or null for permanent>"
}
```

#### `SealRequest` — P3/P4→P6

Crossing: Intelligence/Execution → Truth

Payload:
```json
{
  "seal_type": "SEAL | HOLD | SABAR | VOID | COOLING",
  "event_type": "session.seal | forge.shell | constitutional.verdict | cooling.receipt | seal.issued | seal.verified",
  "payload": "<envelope or structured event>",
  "witness": { "human": null, "ai": "<attestation>", "external": null },
  "session_id": "<bound>",
  "actor_id": "<who is sealing>",
  "supersedes": { "seal_seq": <int or null>, "type": "COLD_LINK" }
}
```

---

## 4. Protocol Flow (12 Steps with Envelopes)

### 4.1 Normal Flow — Full Loop

```
P3 Intelligence          P2 Governance          P4 Execution       P5 Continuity      P6 Truth
     │                       │                      │                  │                 │
     │  ActionProposal       │                      │                  │                 │
     │──────────────────────►│                      │                  │                 │
     │                       │  1. Resolve actor    │                  │                 │
     │                       │  2. Classify action  │                  │                 │
     │                       │  3. Check evidence   │                  │                 │
     │                       │  4. Authority floor  │                  │                 │
     │                       │                      │                  │                 │
     │   AuthorityGrant      │                      │                  │                 │
     │◄──────────────────────│                      │                  │                 │
     │                       │                      │                  │                 │
     │                       │  ExecutionLease       │                  │                 │
     │                       │─────────────────────►│                  │                 │
     │                       │                      │  5. Execute      │                 │
     │                       │                      │  6. Verify       │                 │
     │                       │                      │                  │                 │
     │                       │                      │  MemoryOperation │                 │
     │                       │                      │─────────────────►│                 │
     │                       │                      │                  │                 │
     │                       │  ExecutionReceipt     │                  │                 │
     │                       │◄─────────────────────│                  │                 │
     │                       │                      │                  │                 │
     │                       │                      │  SealRequest     │                 │
     │                       │                      │─────────────────────────────────►│
     │                       │                      │                  │                 │
     │                       │                      │                  │  verifyChain()  │
     │                       │                      │                  │  appendSeal()   │
```

### 4.2 Step-by-Step Envelope Exchange

| Step | Envelope | Source→Target | Max Latency | Fallback |
|------|----------|--------------|-------------|----------|
| 1 | ActionProposal | P3→P2 | 2s network + 5s classify | If P2 unreachable, buffer at P3, retry 3×, then HOLD |
| 2 | AuthorityGrant | P2→P3 | 2s network + 3s compute | If P3 unreachable, grant expires unclaimed |
| 3 | ExecutionLease | P2→P4 | 1s network | If P4 unreachable, lease expired unexecuted |
| 4 | ExecutionReceipt | P4→P2 | 2s network | Dual-write: P4→P6 if P2 unreachable |
| 5 | ExecutionReceipt (mirror) | P4→P6 | 2s network | Retry 5×, 30s backoff, then HOLD |
| 6 | MemoryOperation | P4→P5 | 2s network | Deferred write, eventual consistency OK |
| 7 | MemoryOperation | P3→P5 | 1s network | Deferred write, eventual consistency OK |
| 8 | SealRequest | P3/P4→P6 | 2s network + 1s chain append | Retry 3×, fallback to local queue |

### 4.3 Sovereign Flow (P1↔P2)

```
P1 Sovereign           P2 Governance
     │                      │
     │  SovereignDirective  │
     │─────────────────────►│
     │                      │  1. Verify Ed25519 signature
     │                      │  2. Check F13 authority
     │                      │  3. Apply directive
     │                      │  4. Broadcast to relevant planes
     │                      │  5. Seal to P6
     │  DirectiveReceipt    │
     │◄─────────────────────│
```

| Step | Envelope | Source→Target | Max Latency | Fallback |
|------|----------|--------------|-------------|----------|
| 1 | SovereignDirective | P1→P2 | 1s network | If P2 unreachable, P1 retries. After 3 failures, directive expires |
| 2 | DirectiveReceipt | P2→P1 | 1s network | If P1 unreachable, receipt queued for later delivery |

---

## 5. Timing Constraints and Performance Budget (D2)

### 5.1 Per-Operation Budgets

| Operation Type | p50 Budget | p99 Budget | Notes |
|---------------|-----------|-----------|-------|
| Read/observe (no mutation) | 500ms | 3s | Intelligence→Governance→Intelligence round trip |
| Mutate reversible | 5s | 30s | Full loop: propose→authorise→execute→verify→seal |
| Mutate irreversible | 10s | 60s | Includes signature verification and rollback artifact |
| Cooling loop (post-exec) | 2s | 10s | Drift detection + envelope generation only |
| Seal append | 500ms | 2s | Write to VAULT999 chain |
| Sovereign directive | 2s | 5s | Signature verify + broadcast |

### 5.2 Latency Allocation — Full Mutation Loop

```
P3 propose      → P2:     2s  (+5s classify)
P2 authority    → P3:     2s  
P3→P2 handshake:         1s  (finalise plan)
P2 lease        → P4:     1s
P4 execute:               variable (tool-dependent, capped by lease TTL)
P4 verify:                1s
P4 receipt      → P2:     1s
P4 receipt      → P6:     1s  (parallel to P2)
P4 memory       → P5:     1s  (async, non-blocking)
P3 cooling      → P6:     2s  (post-exec, non-blocking)
                         ─────
Total (excl exec):        ~18s at p99
```

### 5.3 Skip-Optimisation for Read-Only Operations

Steps 6-12 are NOT skippable for mutations. For read-only operations (action_class=OBSERVE):

| Step | Required for OBSERVE? | Rationale |
|------|----------------------|-----------|
| 1 Propose | ✅ Yes | Must classify |
| 2 Authorise | ✅ Yes | Must check floor violations |
| 3 Execute | ✅ Yes | Must observe |
| 4 Verify | ❌ No-op | Observation is self-verifying |
| 5 Remember | ✅ Yes | Must persist what was observed |
| 6 Seal | ❌ No-op | Observations don't get seals (only verdicts do) |

Skip-optimisation reduces OBSERVE-only latency by ~60%.

### 5.4 Degradation Under Load

When governance plane (P2) CPU > 80% or memory > 75%:

- New proposals from P3 are queued with priority=ROUTINE, ATTENTION
- CRITICAL urgency proposals skip the queue (max 1s classify)
- Execution leases extended by 50% TTL to compensate for governance slowdown
- Cooling loop deferred to batch processing every 60s instead of inline

---

## 6. Degradation Modes (D1)

### 6.1 Per-Plane Degradation Table

| Plane Down | Immediate Effect | Safe State | Recovery | Escalation |
|-----------|-----------------|------------|----------|------------|
| **P1 Sovereign** | No new directives | Preserve current grants | Poll for signature | N/A — only human recovers |
| **P2 Governance** | No new proposals processed, no leases issued | All grants PENDING_RENEWAL, timer-based expiry paused | Governance restart + recovery read from P6 | After 60s: P3 enters OBSERVE_ONLY fallback (no mutation). After 300s: system HOLD |
| **P3 Intelligence** | No new proposals submitted | No action, system idle on intelligence | Model/runtime restart | N/A — system safe-idle |
| **P4 Execution** | No execution possible, leases expire | All pending MUTATE → HOLD_PLANE_DOWN | A-FORGE restart + lease recovery | After 120s: P3 notified |
| **P5 Continuity** | Memory reads return stale, writes deferred | Deferred writes queued, stale reads flagged | DB/persistence restart | After 60s: P3 falls back to local cache (no writes). After 300s: full system HOLD |
| **P6 Truth** | Seals deferred to local queue | Seals queued at P4/P3, not lost | Chain writer restart | After 60s: queue at risk. After 300s: HOLD on irreversible actions |

### 6.2 Governance Plane (P2) Unreachable — Detailed

This is the most critical degradation case because P2 is the central arbitrator.

**Symptoms:**
- ActionProposal from P3 times out (no AuthorityGrant returned within 5s)
- ExecutionLease request from P2→P4 fails (socket timeout)
- SovereignDirective from P1 not acknowledged

**Autonomous response (no human needed):**

```
T+0s:    First proposal timeout. P3 retries once.
T+3s:    Second attempt timeout. P3 signals P2_DOWN to federation.
T+5s:    P3 enters fallback: OBSERVE_ONLY.
         - All pending ActionProposals → HOLD_P2_DOWN
         - No MUTATE proposals generated
         - Existing ExecutionLeases continue (grace period)
T+10s:   P3 evaluates active leases. If any remain, extend by original TTL.
T+30s:   Poll P2 health. If still down, broadcast P2_DOWN to all planes.
T+60s:   Escalation: if a pending ActionProposal had urgency=CRITICAL,
         P3 generates a SovereignAlert (direct to P1 via fallback channel).
T+300s:  System HOLD. P3 stops all activity. Waits for P2 recovery.
```

**Recovery:**
```
P2 restarts.
P2 reads seal_chain from P6 — reconstructs last known good state.
P2 reads pending leases from P5 continuity store.
P2 publishes P2_UP to federation.
P3 receives P2_UP, flushes proposal buffer, resumes normal flow.
```

### 6.3 Dual-Plane Failure

| Failed Planes | System State | Safe? | Notes |
|--------------|-------------|-------|-------|
| P2 + P4 | Full HOLD | ✅ Safe | No governance, no execution |
| P2 + P5 | HOLD with degraded memory | ✅ Safe | P5 fallback to disk |
| P2 + P6 | HOLD, seal queue at risk | ⚠️ 300s window | After 300s, unsealed mutations are UNKNOWN |
| P3 + P4 | System idle | ✅ Safe | Nothing proposes, nothing executes |
| P5 + P6 | Continuity blind, truth blind | ⚠️ 60s window | After 60s, HOLD on IRREVERSIBLE |

**The invariant that protects all dual-failure cases:**
If P2 (Governance) is among the failed planes → system enters OBSERVE_ONLY or HOLD.
No mutation can proceed without governance judgement. This is enforced by plane-level topology, not by any single component's correct behaviour.

### 6.4 Partition Tolerance

In a network partition (plane can reach some planes but not others):

- If P3 can reach P2 but P4 cannot: P2 produces leases, P4 never executes them. Leases expire harmlessly. Intelligence sees EXECUTION_DOWN, holds proposals.
- If P2 can reach P4 but P3 cannot: Existing leases execute. No new proposals. After lease drain, system idle.
- If P3 and P4 can reach each other but not P2: Both enter OBSERVE_ONLY fallback. No execution without governance = safe.

---

## 7. Failure Escalation Paths

### 7.1 Escalation Ladder

```
Level 0:   Normal operation.
           All planes healthy. Full loop executes.

Level 1:   Minor failure — single tool timeout, non-critical.
           → Logged to P5, cooling receipt generated (severity=MINOR)
           → No escalation. Operation retried or alternative chosen.

Level 2:   Moderate failure — plane unresponsive for <30s.
           → Affected plane enters fallback mode.
           → P3 receives notification.
           → Cooling receipt generated (severity=SIGNIFICANT)
           → arif_judge notified for SIGNIFICANT cooling verdicts.

Level 3:   Severe failure — plane down >60s or dual-plane failure.
           → System HOLD on all MUTATE/IRREVERSIBLE actions.
           → OBSERVE_ONLY maintained for diagnostics.
           → Sovereign alert generated (severity=CRITICAL)
           → Cooling receipt routes to F13_SOVEREIGN authority.

Level 4:   Critical failure — governance plane down >300s or P1+P2 joint failure.
           → Full system HOLD. Intelligence plane suspends all activity.
           → Only sovereign recovery can resume operations.
           → Receipt sealed with witness: { human: "pending", ai: "hermes", external: "system_state" }
```

### 7.2 Cooling Escalation (3× DIVERGING)

Per COOLING_RECEIPT_SPEC_v1.md §7:

If three consecutive cooling receipts on the same original seal show `convergence: DIVERGING`:

```
Cooling #1: DIVERGING   → logged, no escalation
Cooling #2: DIVERGING   → P3 flags pattern to P2
Cooling #3: DIVERGING   → AUTO escalation to required_authority = F13_SOVEREIGN
                         → arif_judge receives cooling with escalation flag
                         → P1 receives SovereignAlert
```

This escalation DOES NOT require a separate convergence tracker (C1). The seal chain itself is the tracker — `metabolism.cycle_count` and `metabolism.convergence` on each COOLING_RECEIPT encode the history. C1 is a convenience dashboard, not a safety-critical component.

---

## 8. Integration Points — P1 Implementation Contracts

Each P1 gap now has a concrete API contract:

### I1 — Hermes Cooling Verbs

**What:** Hermes emits `SealRequest` envelope with `seal_type=COOLING`

**Contract:**
```python
# /cool_drift: emit SealRequest to P6 (VAULT999)
hermes_cooling_verb(
    session_id="...",
    original_seal_seq=9906,
    drift_detected={"present": True, "observations": [...]},
    proposed_improvement={"hypothesis": "...", "evidence": "...", "epistemic_label": "INT"},
    governance_path={"target_organ": "arifOS", "required_authority": "888_HOLD", "judge_required": True},
    cooling_source="post_execution | post_verification | human_correction | session_close"
)
# Returns: SealRequest envelope (ready for VAULT999 writeSeal())
```

**Accepts:** P3 (Intelligence plane) — Hermes calls this after session close
**Routes to:** P6 (VAULT999 seal_chain.js `writeSeal()` with `event_type="cooling.receipt"`)
**Validating gate:** seal_chain.js `validateCooling()` (INV-C1 through INV-C4) — already implemented

### I2 — Runtime Verify Tool

**What:** `forge_runtime_verify` checks 3 dimensions and returns a verdict

**Contract:**
```
Input:  None (checks current runtime state)
Output: {
  "dimensions": {
    "source_commit": "36112c4",
    "wheel_hash": "sha256:178007cb...",
    "import_path": "/opt/arifos/venv/lib/python3.12/site-packages/arifosmcp/__init__.py"
  },
  "verdict": "MATCH | DRIFT | UNKNOWN",
  "drift_details": { ... }  // only if DRIFT
}
```

**Verdict rules:**
- MATCH: source_commit == wheel_commit AND import_path resolves to wheel (not source tree)
- DRIFT: any dimension differs AND difference is material (code paths changed)
- UNKNOWN: could not read one or more dimensions (filesystem error, missing metadata)

**Integration into 12-step flow:**
- Step 6 (Check evidence): I2 runs BEFORE classification is sent to P2
- If DRIFT or UNKNOWN → P3 must include drift evidence in ActionProposal.evidence[]
- If DRIFT and action would modify runtime → P2 SHOULD HOLD (F9 ANTI-HANTU floor)

### C1 — Convergence Tracker

**Contract:**
The seal chain IS the convergence tracker. No separate component needed.

```python
# Read metabolism state from last N COOLING_RECEIPT entries
convergence = seal_chain.get_convergence(seal_seq=9906, lookback=3)
# Returns: "CONVERGING" | "DIVERGING" | "STABLE" | "first_cooling" | "INSUFFICIENT_DATA"
```

The convergence tracker is a QUERY function on the VAULT999 ledger, not a daemon. It can be:
- A CLI command: `seal_chain.js convergence <seal_seq>`
- An MCP tool: `arif_observe(mode="cooling_convergence", seal_seq=9906)`
- A dashboard widget in AAA cockpit

**Escalation:** Query pattern. If convergence=DIVERGING for 3+ cooling receipts → `arif_judge` summons the cooling receipt chain for review. The escalation is NOT automatic self-triggering — it's a governance-reviewed signal.

### G4 — Ed25519 Chain

**Contract:**
```
Signing chain across planes:

P1 (Sovereign):
  - Holds Ed25519 private key (did:web:arif-fazil.com)
  - Signs SovereignDirective payloads

P2 (Governance):
  - Verifies P1 signatures
  - Signs AuthorityGrant + ExecutionLease payloads with its own key

P3 (Intelligence):
  - Signs ActionProposal payloads with session-bound key
  - Does NOT sign execution or seal commands

P4 (Execution):
  - Signs ExecutionReceipt payloads with A-FORGE key
  - Does NOT sign proposals or authority grants

P6 (Truth):
  - Receives Ed25519 signatures from each plane on envelopes
  - Stores signature hash in seal_chain.js `signature` field
  - Phase 2: verify sign(merkle_root, actor_key) before chain append
```

**Implementation order:**
1. Key generation per plane (stored at `/root/.secrets/ed25519/<plane>.key`)
2. Envelope signing logic in each plane
3. Signature verification in P6 (seal_chain.js `writeSeal()`)
4. Full chain verify: trace actor_id from P1→P2→P3→P4→P6

---

## 9. Governance Boundaries — Plane Authority Map

| Plane | Self-Authorised? | Can Mutate? | Can Seal? | Can Judge? | Can Delegate? |
|-------|-----------------|-------------|-----------|------------|---------------|
| **P1 Sovereign** | Yes (F13) | No (directly) | Yes | Yes | Yes |
| **P2 Governance** | No | No | No | Yes (888) | No |
| **P3 Intelligence** | No | No | No | No | No |
| **P4 Execution** | No | Yes (bounded) | No | No | No |
| **P5 Continuity** | No | No (records only) | No | No | No |
| **P6 Truth** | No | No (append-only) | Yes (mechanical) | No | No |

**Sovereign plane is the only self-authorised entity.** Every other plane operates under grants issued by P2 (Governance), which itself operates under P1 (Sovereign).

---

## 10. Comparison — Pre- vs Post-EUREKA

| Dimension | Pre-EUREKA | Post-EUREKA |
|-----------|-----------|-------------|
| Session identity | Claimed, not verified | Verified via Ed25519 chain |
| Authority | Implicit from model prompt | Explicit from P2 capability grant |
| Action classification | Fuzzy, post-hoc | Structured, pre-authorisation |
| Memory | Write-first, classify-later | Classify-first, write-with-tags |
| Execution | Self-authorised | P4 executes only under P2 lease |
| Truth | Seal as final step only | Seal at every boundary crossing |
| Cooling | Non-existent | COOLING_RECEIPT with validateCooling() |
| Failure | Silent retry or half-handled | Per-plane degradation mode with cooling |
| Latency | Unknown | Budgeted per step, skip-optimised for OBSERVE |

---

## 11. Open Items (awaiting sovereign input)

These cannot be resolved by protocol design alone:

1. **Harmonic mean vs min-chain (Wawa D3):** The AI equation's zero-factor property is correct. The product form implies independence which is false. Arif to choose: weighted harmonic mean or min-chain model.

2. **Inter-plane arbitration body (Wawa D4):** When Intelligence proposes, Governance permits, but Truth has no evidence — who arbitrates? Current design: arif_judge (P2) is the arbiter with P1 appeal. But P2 cannot judge itself when P2 is the source of conflict. Proposed: AAA cockpit hosts a dedicated arbitration panel with multi-model witness.

3. **Planetary latency caps (D2):** p50/p99 budgets in §5 are estimates for single-machine deployment. When planes are distributed (VPS + local + cloud), latency budgets need recalibration. Propose: sovereign sets the distribution boundary.

4. **Degradation mode for P1+dual-plane failure:** If P1 and P2 both go down, what human-in-the-loop mechanism exists for cold-start recovery? Currently: full HOLD, manual restart. Acceptable?

---

## 12. Document Governance

| Field | Value |
|-------|-------|
| Status | CONSTITUTIONAL DRAFT |
| Valid from | 2026-07-13 |
| Valid until | Next F13 ratification | 
| Supersedes | None |
| Governs | All plane-boundary crossings |
| Sealing | Requires F13 seal before P1 execution |
| P1 dependencies | This spec must be sealed before I1, I2, C1, G4 implementation |

---

*DITEMPA BUKAN DIBERI — The protocol is forged, not given.*
