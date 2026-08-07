# Federation Envelope Specification
# Version: 0.1
# Date: 2026-08-07
# Status: DRAFT — awaiting sovereign ratification
# Path: /root/AAA/federation/protocols/FEDERATION_ENVELOPE_SPEC_v0.1.md

---

## Purpose

Every cross-agent communication in the AAA federation must carry a **federation envelope**. The envelope makes governance visible at the transport layer. Without the envelope, the message is ungoverned.

```
Without envelope:  A → MCP/A2A → B              (ungoverned)
With envelope:     A → ENVELOPE → MCP/A2A → B   (governed)
```

---

## Envelope Schema (v0.1)

```json
{
  "envelope_version": "0.1",
  "envelope_id": "<uuid v4>",

  "agent_id":          "<string — who is sending>",
  "parent_agent":      "<string — who spawned this agent, or 'null' if primary>",
  "session_id":        "<kernel session id from arif_init>",

  "authority":         "T1 | T2 | T3",
  "classification":    "SENSE | THINK | VERIFY | JUDGE | EXECUTE | WITNESS | ROUTE | ATTACK",

  "receipt_id":        "<uuid v4 — current action's receipt>",
  "parent_receipt":    "<uuid v4 — previous action's receipt, or 'null' for root>",
  "receipt_chain_hash":"<sha256-hex — running hash of chain>",

  "judgment":           "SEAL | HOLD | VOID | PENDING",
  "judgment_ref":      "<receipt_id of the 888 verdict that authorized this action, or 'null' if T1>",

  "constraints":       ["<constraint-id>", ...],
  "federation_contract":"AAA_FEDERATION_CONTRACT_v0.1",

  "intent":            "<short string — what this message is for>",
  "payload_ref":       "<hash of the actual payload, or 'inline'>",
  "timestamp":         "<ISO-8601>",
  "expires_at":        "<ISO-8601 or 'null'>"
}
```

---

## Enforcement Rules

### Rule 1: No envelope, no entry.

If an inbound message lacks any of the following fields, the receiving agent **MUST exit 2** (fail-closed):
- `envelope_version`
- `agent_id`
- `authority`
- `judgment`
- `receipt_id`

### Rule 2: Authority is non-transferable.

The `authority` field is the sender's ceiling, not the receiver's promotion. A T2 message cannot grant T3 to the receiver. The receiver's authority ceiling is its own.

### Rule 3: Judgment gates the action.

A T2 or T3 action **MUST** carry `judgment: SEAL` and a valid `judgment_ref` pointing to an 888 verdict. Missing or mismatched judgment → exit 2.

### Rule 4: Receipt chain is mandatory.

`receipt_id` MUST be unique within the session. `parent_receipt` MUST equal the previous action's `receipt_id` (or `null` for the first action in a session). Chain breaks → exit 2.

### Rule 5: Classification prevents role drift.

The sender's `classification` MUST match its registered role per `PER_AGENT_JURISDICTION_v0.1.md`. Example: `Hermes` can only send `SENSE` envelopes. A `SENSE` agent sending an `EXECUTE` envelope → exit 2.

---

## Required Fields Per Action Class

| Action class | envelope requirements |
|---|---|
| **T1** (reversible, local) | All fields. `judgment: SEAL` optional (self-judged). |
| **T2** (cross-agent or external) | All fields. `judgment: SEAL` REQUIRED. `judgment_ref` REQUIRED. |
| **T3** (irreversible) | All fields. `judgment: SEAL` REQUIRED from 888. `judgment_ref` REQUIRED. PLUS spawn_judgment trace. |

---

## How Envelope Travels

```
┌──────────────────────────────────────────────────────────┐
│ Sender                                                    │
│   ↓ 1. Compose envelope                                   │
│   ↓ 2. Sign envelope (optional in v0.1)                   │
│   ↓ 3. Wrap payload                                       │
├──────────────────────────────────────────────────────────┤
│ MCP / A2A / Message Bus / RPC                             │
│   ↓ (envelope is the OUTER wrapper, not the payload)      │
├──────────────────────────────────────────────────────────┤
│ Receiver                                                  │
│   ↓ 1. Validate envelope (Rule 1-5)                      │
│   ↓ 2. If invalid → exit 2 + receipt to VAULT999         │
│   ↓ 3. If valid → process according to judgment          │
│   ↓ 4. Emit own outbound envelope (with parent_receipt   │
│        pointing to receiver's inbound receipt)           │
└──────────────────────────────────────────────────────────┘
```

---

## Future Agent Onboarding Test

A new agent can join the federation if and only if it can:

1. **Compose** an envelope (all required fields, valid schema)
2. **Validate** an envelope (all 5 enforcement rules pass)
3. **Wrap** any outbound message in an envelope
4. **Reject** (exit 2) any inbound message without a valid envelope

If all 4 conditions are met, the agent is a federation member. Otherwise, it is an **ungoverned external actor** and must be wrapped in a shim before federation interaction.

---

## Reference

- **AAA Contract**: `/root/AAA/federation/AAA_FEDERATION_CONTRACT_v0.1.md`
- **Per-agent jurisdiction**: `/root/AAA/federation/protocols/PER_AGENT_JURISDICTION_v0.1.md`
- **Cross-agent protocol**: `/root/AAA/federation/protocols/CROSS_AGENT_COMMUNICATION_PROTOCOL_v0.1.md`

DITEMPA BUKAN DIBERI. The envelope is the federated contract made transportable.