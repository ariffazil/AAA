# Hook Order and Monotonicity — Two-Agent Governed Execution
> **Status:** DRAFT_SPEC_READY  
> **Canonical Registry SOT:** `/root/AAA/governance/AGENTIC-HOOK-MESH-V1.yaml`  
> **Constitutional Authority:** F1 Amanah, F2 Truth, F4 Clarity, F8 Simpler Path, F11 Audit, F13 Sovereign Attention

## 1. Unified Hook Execution Order

All federation harnesses execute hooks in strict chronological and causal order:

```
1. session.created [000_BOOT]
   │  ├── scar-bootstrap: hydrate scar cache & carry-forward open loops (F1+F11)
   │  ├── kernel-bridge: arif_init with Accept: application/json; bind session token (F13)
   │  └── autonomy-reset: continuation counter reset; Digital = MUBAH (F13)
   └── state = OBSERVE | receipt: session_init

2. context.transform (optional pre-turn intent reminder)
   │  └── attach compact intent/authority reminder (F2)

3. tool.execute.before [100_GATE]
   │  ├── classify tool (READ_ONLY / LOCAL_REVERSIBLE / EXTERNAL_DRAFT / IRREVERSIBLE / SEAL_F13)
   │  ├── unconditional pass-through for read/probe/bootstrap tools (F2)
   │  ├── auto-mint ACT token if mutating tool lacks session token (F1)
   │  ├── forbidden target check (/etc/shadow, .secrets) → VOID (F1)
   │  ├── monotonic ladder check (ALLOW < OBSERVE_ONLY < SABAR < HOLD < VOID < REVOKED)
   │  └── record pre-state in rollback journal
   └── if all pass: state = EXECUTE_BOUNDED | if any fail: state = HOLD

4. tool.execute.after [200_HEAL]
   │  ├── emit execution outcome receipt (actual, not desired) with ΔS (F11)
   │  ├── auto-healing reflex for HTTP 406 / missing dependency / zombie process / git desync (F1)
   │  ├── update receipt chain and error frequency tracker (F2)
   │  └── state = MEASURE

5. session.idle [300_METABOLIZE]
   │  ├── anti-tangguh sentry: tripwire permission questions on digital tasks (F13)
   │  ├── autonomous scar crystallization: forge scar artifact if error repeats ≥ 2 times (F2+F11)
   │  ├── turn-rsi pulse logging (F4)
   │  └── bounded recursive improvement apply: mutate routing/prompt/thresholds (F8)
   └── state = LEARN_BOUNDED

6. session.close [999_SEAL]
   │  ├── carry-forward-emit: generational append to carry_forward.json via flock (F11)
   │  ├── stamp immutable audit verdict into VAULT999 ledger (F13)
   │  └── flush verified entries in rollback journal (F1)
   └── state = SEALED
```

---

## 2. Monotonicity Invariant

### 2.1 Restriction Scale

```
ALLOW < OBSERVE_ONLY < SABAR < HOLD < VOID < REVOKED
  (0)        (1)          (2)     (3)     (4)      (5)
```

### 2.2 Invariant Law

A downstream hook or subsequent agent turn may only **maintain or increase** the restriction level:

$$\text{verdict}_{n+1} \ge \text{restriction}(\text{verdict}_n)$$

### 2.3 Transition Validation Matrix

| Initial State | Target State | Result | Governance Action |
|---|---|---|---|
| `ALLOW` | `OBSERVE_ONLY` | ALLOWED | Ratchet UP |
| `ALLOW` | `HOLD` | ALLOWED | Ratchet UP |
| `HOLD` | `VOID` | ALLOWED | Ratchet UP |
| `OBSERVE_ONLY` | `ALLOW` | **BLOCKED** | Degradation rejected |
| `HOLD` | `ALLOW` | **BLOCKED** | Degradation rejected |
| `VOID` | `ALLOW` | **BLOCKED** | Degradation rejected |
| `REVOKED` | `ALLOW` | **BLOCKED** | Degradation rejected |

### 2.4 Violation Handling

```python
if incoming_restriction < current_restriction:
    emit_violation("VERDICT_MONOTONICITY_VIOLATION")
    effective_verdict = current_restriction
    log_audit_receipt(violation=True)
```

---

## 3. Hook Dependencies & Topological Invariants

```
session.created
    └── prerequisite: none

tool.execute.before
    └── prerequisite: session.created (auto-mints if missing)

tool.execute.after
    └── prerequisite: tool.execute.before (must have executed)

session.idle
    └── prerequisite: tool.execute.after or turn completion

session.close
    └── prerequisite: session.created (fires regardless of intermediate errors)
```

---

## 4. Evidence Requirements per Hook

| Hook Event | Floor Binding | Required Telemetry / Evidence | Authority Ceiling |
|---|---|---|---|
| `session.created` | F1 + F11 + F13 | Session ID, actor ID, token, loaded scar hashes | OBSERVE_ONLY |
| `tool.execute.before` | F1 + F2 + F13 | Tool classification, args hash, journal entry ID | MONOTONIC_GATE |
| `tool.execute.after` | F4 + F11 | Exit code, stdout/err hash, ΔS, auto-heal status | OBSERVE_ONLY |
| `session.idle` | F8 + F13 | Discussion debt, Anti-Tangguh status, scar delta | PROPOSE_BOUNDED |
| `session.close` | F11 + F13 | Carry-forward hash, seal ID, vault audit entry | SEAL_RECEIPT |
