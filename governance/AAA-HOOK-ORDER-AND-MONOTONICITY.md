# Hook Order and Monotonicity — Two-Agent Governed Execution
> **Status:** ALIGNED_TO_SOT_V1.3.0 (corrected 2026-09-14, FI-008)
> **Canonical Registry SOT:** `/root/AAA/governance/AGENTIC-HOOK-MESH-V1.yaml`
> **Constitutional Authority:** F1 Amanah, F2 Truth, F4 Clarity, F8 Simpler Path, F11 Audit, F13 Sovereign Attention

## 0. Separation of Powers (read this first)

Hooks **observe, enrich, trace, heal, and escalate**. They do not judge.

| Layer | Role | May refuse an action? |
|---|---|---|
| Hook mesh | sense / enrich / trace / heal / escalate | **NO** |
| arifOS kernel (:8088) | judge — sole issuer of ALLOW / HOLD / VOID / REVOKED | YES |
| Execution membrane (harness permission layer, A-FORGE ArifJudge) | enforce the kernel verdict at the side-effect boundary | YES |
| F13 sovereign | outside the machine | YES |

A hook may **DEFER** (emit HOLD + escalation receipt) for the enumerated fail-safe classes below.
A hook may **never ANNUL** (VOID / DENY / REVOKED) — those are kernel verdicts.

**Enumerated fail-safe classes** (fixed, non-discretionary — a firewall rule is not a judge).
Defined once in code; drift is checked by `scripts/hook_mesh_check.py`:

- `/etc/shadow`
- `/etc/sudoers`
- `/root/.ssh/authorized_keys`
- `/root/.secrets/kunci-root.env`

Off-list targets receive **no hook-originated refusal of any kind**. Digital work remains MUBAH.

---

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
   │  ├── enumerated fail-safe match (/etc/shadow, /etc/sudoers, ~/.ssh/authorized_keys, secrets env)
   │  │     → DEFER: HOLD + escalation receipt (the KERNEL issues VOID — not this hook)
   │  ├── monotonic ladder tracked as STATE (ALLOW < ALLOW_WITH_CONSTRAINTS < OBSERVE_ONLY < DEFER < HOLD < DENY < VOID < REVOKED)
   │  └── record pre-state in rollback journal
   └── if all pass: state = EXECUTE_BOUNDED | if escalation raised: state = AWAIT_KERNEL

4. tool.execute.after [200_HEAL]
   │  ├── emit execution outcome receipt (actual, not desired) with ΔS (F11)
   │  ├── auto-healing reflex for HTTP 406 / missing dependency / zombie process / git desync (F1)
   │  ├── update receipt chain and error frequency tracker (F2)
   │  └── state = MEASURE

5. session.idle [300_METABOLIZE]
   │  ├── anti-tangguh sentry: tripwire permission questions on digital tasks (F13)
   │  ├── autonomous scar crystallization: forge scar candidate if error repeats ≥ 2 times (F2+F11)
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
ALLOW < ALLOW_WITH_CONSTRAINTS < OBSERVE_ONLY < DEFER < HOLD < DENY < VOID < REVOKED
  (0)          (1)                  (2)         (3)    (4)   (5)   (6)     (7)
```

Ranks `(5)` and above are **kernel-only**. A hook that emits them is in defect
(see `known_gaps.ENGINE-VERDICT-OVERREACH` in the SOT).

### 2.2 Invariant Law

A downstream hook or subsequent agent turn may only **maintain or increase** the restriction level:

$$\text{verdict}_{n+1} \ge \text{restriction}(\text{verdict}_n)$$

This governs the **tracked state**, not an enforcement mechanism. It prevents a later
hook from quietly relaxing an earlier one's asserted restriction.

### 2.3 Transition Validation Matrix

| Initial State | Target State | Result | Governance Action |
|---|---|---|---|
| `ALLOW` | `OBSERVE_ONLY` | ALLOWED | Ratchet UP |
| `ALLOW` | `HOLD` | ALLOWED | Ratchet UP |
| `HOLD` | `VOID` | ALLOWED | Ratchet UP (kernel-only transition) |
| `OBSERVE_ONLY` | `ALLOW` | **REJECTED** | Degradation rejected |
| `HOLD` | `ALLOW` | **REJECTED** | Degradation rejected |
| `VOID` | `ALLOW` | **REJECTED** | Degradation rejected |
| `REVOKED` | `ALLOW` | **REJECTED** | Degradation rejected |

### 2.4 Violation Handling

```python
if incoming_restriction < current_restriction:
    emit_violation("VERDICT_MONOTONICITY_VIOLATION")
    effective_verdict = current_restriction   # state only — never an execution stop
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
| `tool.execute.before` | F1 + F2 + F13 | Tool classification, args hash, escalation receipt, journal entry ID | SENSOR_ESCALATE |
| `tool.execute.after` | F4 + F11 | Exit code, stdout/err hash, ΔS, auto-heal status | OBSERVE_ONLY |
| `session.idle` | F8 + F13 | Discussion debt, Anti-Tangguh status, scar delta | PROPOSE_BOUNDED |
| `session.close` | F11 + F13 | Carry-forward hash, seal ID, vault audit entry | SEAL_RECEIPT |

**Authority ceiling note.** `SENSOR_ESCALATE` means the hook senses and raises an
escalation; it does not confer authority to refuse. Earlier revisions of this document
declared `MONOTONIC_GATE` for `tool.execute.before`, which falsely implied the hook held
gate authority. Corrected 2026-09-14 (FI-008) under sovereign directive
APEX-ZEN-HOOK-DEFUSE-20260914.

---

## 5. What this document does NOT claim

- It does **not** claim hooks are frictionless in practice. The live receipt ledger
  (`opencode_receipts.jsonl`) contains blocking events; those are the defect tracked as
  `known_gaps.ENGINE-VERDICT-OVERREACH`, not the intended design.
- It does **not** claim receipts prove execution. Receipts record decisions only;
  `known_gaps.RECEIPTS-LACK-CONSEQUENCE` tracks the missing outcome field.
- It does **not** claim all harnesses are covered. `known_gaps.CLAUDE-PATH-TARGET-SCREEN`
  records that the Claude Code PreToolUse path screens no forbidden target.
