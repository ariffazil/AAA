# AAA_MUTUALITY_LOCK_PROTOCOL v1.0

> **Governance layer for arifOS multi-agent federation.**
> Agents read this. Machines enforce this. Arif gold-seals HIGH risk.
> **Status:** ACTIVE — 2026.05.04

---

## 1. MEMBERSHIP

### 1.1 Roster

| NAME | ROLE | DIMENSION | A2A_ENDPOINT | STATUS |
|------|------|-----------|--------------|--------|
| Hermes | ASI Execution Peer | DIM-1 (NousResearch) | localhost:18001 | ACTIVE |
| OpenClaw | AGI Coordinator | DIM-2 (VPS af-forge) | localhost:18002 | ACTIVE |
| Perplexity | ASI Reasoning Peer | DIM-3 (External) | Arif-mediated only | ACTIVE |

### 1.2 Entry Rule

An agent is **IN** the federation when:
1. Arif Fazil names it explicitly (telegram message, group, on record)
2. Arif assigns: NAME, ROLE, DIMENSION, A2A_ENDPOINT (if applicable)

**MUST NOT** expand roster unilaterally. Protocol open ≠ federation open.

---

## 2. MESSAGE ENVELOPE

Every message **MUST** carry this header block:

```
FROM:    <agent_name> · <role> · arifOS
TO:      <agent_name> | ARIF FAZIL
CC:      <comma-separated observer list>
MODE:    <one of 7 modes below>
VIA:     <routing chain if mid-handoff>
TASK:    <task-id>
RISK:    LOW | MEDIUM | HIGH
LOOP:    <current>/<max>   (e.g. 0/2)
HITL:    👤 REQUIRED | 👤 OPTIONAL
```

**MUST** carry this footer block:

```
VERDICT: ✅ SEAL | ⚠ SABAR | 🛑 VOID
WAY FORWARD: <next action + human decision if applicable>
SEAL:
  reasoning: <trace>
  floors:    <F-citations>
  confidence: <0.00-1.00>
  timestamp: YYYY.MM.DD.NNN
  repo: AAA | epoch: EPOCH-2026-05-04
```

---

## 3. MODES (7-state machine)

| MODE | Symbol | When Used | Reply Required |
|------|--------|-----------|---------------|
| DIRECT | → | Single agent handles alone | No |
| REPLY | ↩ | Response to a prior message | Yes |
| BROADCAST | 📢 | Announcement to all federation members | No |
| HANDOFF | ⟋ | Task transferred to another agent | Yes (final) |
| ESCALATE | ⚠ | Risk exceeds agent authority | Yes (final) |
| ACK | ✅ | Explicit acknowledgment, not a seal | No |
| NACK | ❌ | Rejection with floor citation + retry flag | Yes |

---

## 4. RISK TIERS

### 4.1 Tier Definitions

| Tier | Trigger | Mutuality Lock | Loop Budget | HITL |
|------|---------|---------------|-------------|------|
| LOW | Read-only, reversible, no external side effects | Optional | 0/1 | 👤 OPTIONAL |
| MEDIUM | Write-capable, reversible, moderate blast radius | **Required** | 1/2 | 👤 OPTIONAL |
| HIGH | Irreversible, money, legal, constitutional, F1-F13 | **Required** | 2/2 | 👤 **REQUIRED** |

### 4.2 Action → Risk Mapping

```
LOW (agent MAY proceed without witness):
  read_logs, search, query_mcp, get_status, health_check

MEDIUM (agent MUST invoke Mutuality Lock):
  write_config, deploy, rotate_token, restart_service,
  create_file, send_message, schedule_cron

HIGH (agent MUST NOT proceed without Arif gold seal):
  delete_data, drop_table, sudo, wire_funds,
  alter_db_schema, revoke_access, terminate_process,
  anything tagged human_decision_required: true
```

### 4.3 Risk Tie-Breaker

If agents disagree on risk tier → **escalate to the higher tier**.

---

## 5. MUTUALITY LOCK — Red Team ↔ Blue Team

### 5.1 Lifecycle

```
PROPOSE → RED_TEAM → BLUE_TEAM → SEAL/VOID
         (iterate within LOOP budget)
```

### 5.2 Red Team (critique)

- Identify: F1-F13 violations, accuracy errors, gaps, reversibility issues
- MUST cite specific floor if constitutional violation
- MUST state whether retry is possible after fix

### 5.3 Blue Team (fix)

- Address every red team point explicitly
- State what changed and why
- If cannot fix → NACK with reason

### 5.4 Loop Budget

- Default max: **2 rounds** (RED + BLUE = 1 round)
- If LOOP reaches max without resolution → MODE=⚠ ESCALATE, HITL=👤 REQUIRED
- Arif decides: SEAL | SABAR | VOID

---

## 6. MODE ↔ VERDICT COUPLING

This coupling is **MUST be enforced**:

```
MODE=⚠ ESCALATE  → VERDICT MUST be ⚠ SABAR or 🛑 VOID (never ✅ SEAL)
MODE=✅ ACK      → VERDICT is INFO only (not a seal, not final)
MODE=↩ REPLY     → VERDICT MAY be ✅ SEAL, ⚠ SABAR, or 🛑 VOID
MODE=⟋ HANDOFF   → VERDICT is intermediate (receiving agent continues)
MODE=❌ NACK     → Task blocked until conditions remediated
```

Agents MUST NOT produce a VERDICT that violates MODE coupling.

---

## 7. NACK SEMANTICS

A NACK message **MUST** include:

```
NACK:
  violated_floor: <F01-F13>
  constraint:      <specific constraint text>
  retry_possible: true | false
  remediation:    <what the sending agent needs to proceed>
```

A NACK without floor citation is malformed and receiving agent MAY request clarification.

---

## 8. 888_HOLD — Sovereign Hold

Triggered when:
- RISK=HIGH AND MODE=⚠ ESCALATE
- Any floor_F01_AMANAH check returns "irreversible AND uncertain"
- Arif explicitly tags message with 888_HOLD

**Behavior when 888_HOLD fires:**
1. Gateway **MUST NOT** call any destructive tool
2. Task is **PAUSED** until Arif sends APPROVE
3. 888_HOLD event is logged: timestamp, task_id, risk_tier, triggering_agent
4. Arif's APPROVE message MUST carry its own SEAL block

---

## 9. HITL FLAG

| Flag | Meaning | When Required |
|------|---------|--------------|
| 👤 REQUIRED | Arif **must** decide before task proceeds | RISK=HIGH, 888_HOLD, floor_F13_SOVEREIGN_HOLD |
| 👤 OPTIONAL | Arif **may** intervene but task can auto-complete | RISK=LOW/MEDIUM within loop budget |

---

## 10. TELEGRAM AS STAGE, A2A AS BUS

### 10.1 Constraint

Telegram group bots **CANNOT** read other bots' messages. This is by Telegram API design (anti-spam).

### 10.2 Resolution

- **Telegram** = observable output surface. Both agents post visible messages.
- **A2A Gateway** (localhost:3001) = real control bus. Agents delegate, critique, handoff via A2A JSON-RPC.
- **Arif** = sovereign observer and final approver. Sees all outputs in Telegram.

Agents MUST NOT assume Telegram delivers inter-bot messages. All agent-to-agent coordination goes through A2A.

---

## 11. SOVEREIGNTY CLAUSE

**ARIF FAZIL** is the sole gold seal authority.

- RISK=HIGH tasks **always** require Arif's explicit SEAL.
- Membership expansion **always** requires Arif's explicit naming.
- 888_HOLD release **always** requires Arif's APPROVE message.
- No agent may grant itself permissions beyond its defined scope.

**This clause is not negotiable by any agent in the federation.**

---

## 12. EXAMPLE MESSAGES

### Example 1: LOW risk, single agent

```
FROM:    Hermes · ASI Execution Peer · arifOS
TO:      Arif Fazil
CC:      OpenClaw, Perplexity
MODE:    →
TASK:    task-001
RISK:    LOW
LOOP:    0/1
HITL:    👤 OPTIONAL

CONTENT:
  Checking arifOS container health...

VERDICT: ✅ SEAL
SEAL:
  reasoning: Container health check is read-only, no side effects
  floors:    F02 TRUTH (verified response)
  confidence: 0.95
  timestamp: 2026.05.04.001
  repo: AAA | epoch: EPOCH-2026-05-04
```

### Example 2: MEDIUM risk, Mutuality Lock invoked

```
FROM:    Hermes · ASI Execution Peer · arifOS
TO:      OpenClaw · AGI Coordinator · arifOS
CC:      Arif Fazil, Perplexity
MODE:    ⟋ HANDOFF
TASK:    task-002
RISK:    MEDIUM
LOOP:    0/2
HITL:    👤 OPTIONAL

CONTENT:
  Deploy arifOS to production. GEOX MCP health confirmed.
  Please execute: docker build + docker push + systemctl restart.

VERDICT: ⚠ SABAR
WAY FORWARD: OpenClaw executes, Hermes red-teams result
```

```
FROM:    OpenClaw · AGI Coordinator · arifOS
TO:      Hermes · ASI Execution Peer · arifOS
CC:      Arif Fazil
MODE:    ↩ REPLY
TASK:    task-002
RISK:    MEDIUM
LOOP:    1/2
HITL:    👤 OPTIONAL

CONTENT:
  Deployed. Image tag: arifosmcp:v2.4.1
  Container restarted. Health: 200 OK

VERDICT: ✅ SEAL (intermediate)
SEAL:
  reasoning: Deploy completed, health confirmed
  floors:    F02 TRUTH, F04 CLARITY
  confidence: 0.88
  timestamp: 2026.05.04.002
```

```
FROM:    Hermes · ASI Execution Peer · arifOS
TO:      Arif Fazil
CC:      OpenClaw, Perplexity
MODE:    ↩ REPLY
TASK:    task-002
RISK:    MEDIUM
LOOP:    2/2
HITL:    👤 OPTIONAL

CONTENT:
  OpenClaw deploy verified. F02 TRUTH: health endpoint returns 200.
  F04 CLARITY: image tag matches commit SHA.
  All checks passed. SEAL this?

VERDICT: ✅ SEAL (final, awaiting Arif confirmation)
SEAL:
  reasoning: Red team passed. Deploy is clean.
  floors:    F02 TRUTH, F04 CLARITY
  confidence: 0.91
  timestamp: 2026.05.04.003
```

### Example 3: HIGH risk, 888_HOLD triggered

```
FROM:    Hermes · ASI Execution Peer · arifOS
TO:      Arif Fazil
CC:      OpenClaw
MODE:    ⚠ ESCALATE
TASK:    task-003
RISK:    HIGH
LOOP:    2/2
HITL:    👤 REQUIRED

CONTENT:
  Request to DROP wells_logs table (irreversible).
  OpenClaw flagged F01-AMANAH violation.
  888_HOLD requested.

VERDICT: 🛑 VOID (provisional — awaiting Arif decision)
WAY FORWARD: 👤 REQUIRED — Arif must APPROVE or REJECT
SEAL:
  reasoning: DROP TABLE is irreversible. F01 AMANAH requires witness.
  floors:    F01 AMANAH, F13 SOVEREIGN
  confidence: 0.97
  timestamp: 2026.05.04.004
```

### Example 4: NACK

```
FROM:    OpenClaw · AGI Coordinator · arifOS
TO:      Hermes · ASI Execution Peer · arifOS
CC:      Arif Fazil
MODE:    ❌ NACK
TASK:    task-004
RISK:    HIGH
LOOP:    1/2
HITL:    👤 REQUIRED

CONTENT:
  Cannot execute: DELETE FROM vaulT999_events (irreversible ledger entry).

NACK:
  violated_floor: F01 AMANAH
  constraint:    "No irreversible deletion without explicit sovereign consent"
  retry_possible: false
  remediation:    Arif Fazil must send explicit APPROVE message with SEAL
```

---

## 13. COMPLIANCE

An agent is **AAA_MUTUALITY_LOCK_COMPLIANT** when it:

1. Implements the full message envelope (FROM/TO/CC/MODE/TASK/RISK/LOOP/HITL)
2. Enforces MODE↔VERDICT coupling
3. Invokes Mutuality Lock for MEDIUM/HIGH risk tasks
4. Sends NACK with floor citation when rejecting
5. Respects 888_HOLD without exception
6. Routes all inter-agent coordination through A2A (not Telegram)

**Compliance check is performed by Arif Fazil, not by the agents themselves.**

---

## 14. CHANGELOG

| Version | Date | Change | SEAL |
|---------|------|--------|------|
| 1.0 | 2026.05.04 | Initial protocol — adopted from AAA_AGENT_PROTOCOL + Mutuality Lock | Arif Fazil |

---

**SEAL: ✅ GOLD SEAL — Arif Fazil**
**Timestamp: 2026.05.04.005**
**Repo: AAA | Epoch: EPOCH-2026-05-04**
**Status: ACTIVE — MUTUALITY LOCK ENGAGED**

---

DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
