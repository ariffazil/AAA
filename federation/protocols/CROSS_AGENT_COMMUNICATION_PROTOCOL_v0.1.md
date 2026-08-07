# Cross-Agent Communication Protocol
# Version: 0.1
# Date: 2026-08-07
# Status: DRAFT — awaiting sovereign ratification
# Path: /root/AAA/federation/protocols/CROSS_AGENT_COMMUNICATION_PROTOCOL_v0.1.md

---

## Purpose

Define how Agent A communicates with Agent B through AAA governance. Without this protocol, agents bypass the substrate. With it, every cross-agent action produces evidence, judgment, and receipt.

```
Without protocol:  A ⇄ B                          (raw exchange)
With protocol:     A → [envelope] → B → [envelope] → A   (governed exchange)
```

---

## The 5-Stage Pipeline

Every cross-agent communication follows:

```
┌─────────────────────────────────────────────────────────────┐
│ 333 PROPOSE  →  555 VERIFY  →  888 JUDGE  →  EXECUTE  →  WITNESS │
└─────────────────────────────────────────────────────────────┘
       │              │              │              │              │
       ↓              ↓              ↓              ↓              ↓
    proposal     evidence       SEAL/HOLD     tool call     receipt
    envelope     envelope        verdict      (via MCP/A2A)   to VAULT999
```

### Stage 1: 333 PROPOSE (sender)

The sender (333 agent) composes a proposal envelope with:
- `intent`: what this message is for
- `payload`: the actual data
- `expected_judgment_class`: SEAL or HOLD
- `constraints`: list of constraint-ids the receiver must honor

### Stage 2: 555 VERIFY (sender's witness)

The 555 verifier (subagent or witness function) checks:
- Envelope schema valid
- All required fields present
- Authority ceiling matches sender's role
- `parent_receipt` chain valid

If 555 VERIFY fails → sender **MUST NOT** send. Exit 2 locally.

### Stage 3: 888 JUDGE (constitutional apex)

The 888 judge reviews the proposal. For T2 and T3:
- Returns `judgment: SEAL` with `judgment_ref: <receipt_id>`
- Or returns `judgment: HOLD` with reason
- Or returns `judgment: VOID` with constitutional violation reason

For T1: sender may self-judge (no 888 required).

### Stage 4: EXECUTE (transport)

If 888 returned `SEAL`, the message is sent via MCP/A2A with the full envelope wrapping the payload.

Transport rules:
- Envelope is the OUTER wrapper (not the payload)
- Receiver MUST validate envelope on receipt
- If transport layer corrupts envelope → exit 2 at receiver
- If transport layer corrupts payload → fail-closed at application

### Stage 5: WITNESS (VAULT999)

Both sender and receiver emit receipts to VAULT999:
- Sender receipt: "I sent envelope X to B with judgment Y"
- Receiver receipt: "I received envelope X from A; validation result Z"
- Both receipts hash-chained via `parent_receipt` field

---

## The Full Protocol (Sender Side)

```python
def send_to_agent_b(intent, payload, required_authority, parent_receipt):
    # 1. 333 PROPOSE — compose envelope
    proposal = compose_envelope(
        agent_id=my_agent_id,
        parent_agent=my_parent,
        authority=required_authority,
        classification=my_classification,
        intent=intent,
        payload=payload,
        parent_receipt=parent_receipt
    )

    # 2. 555 VERIFY — local check
    if not validate_envelope_schema(proposal):
        return EXIT_2  # cannot send invalid envelope

    # 3. 888 JUDGE — for T2/T3
    if required_authority in ["T2", "T3"]:
        judgment = call_arif_judge(proposal)
        if judgment.verdict != "SEAL":
            return EXIT_2  # cannot proceed without seal

        proposal.judgment = "SEAL"
        proposal.judgment_ref = judgment.receipt_id
    else:
        proposal.judgment = "SEAL"  # T1 self-judged

    # 4. EXECUTE — send via MCP/A2A
    my_receipt_id = generate_uuid()
    proposal.receipt_id = my_receipt_id
    seal_to_vault999(f"sent envelope {proposal.envelope_id} to {target_agent}", my_receipt_id, parent_receipt)
    send_via_mcp_or_a2a(target_agent, proposal)

    return my_receipt_id
```

---

## The Full Protocol (Receiver Side)

```python
def receive_from_agent_a(envelope):
    my_receipt_id = generate_uuid()

    # 1. Validate envelope schema (Rule 1)
    if not validate_envelope_schema(envelope):
        seal_to_vault999(f"REJECTED: invalid envelope from {envelope.agent_id}", my_receipt_id, envelope.receipt_id)
        return EXIT_2

    # 2. Validate authority (Rule 2) — sender's authority is ceiling, not promotion
    if not my_classification_can_receive(envelope.classification):
        seal_to_vault999(f"REJECTED: classification {envelope.classification} not allowed for {my_classification}", my_receipt_id, envelope.receipt_id)
        return EXIT_2

    # 3. Validate judgment (Rule 3)
    if envelope.authority in ["T2", "T3"]:
        if envelope.judgment != "SEAL":
            seal_to_vault999(f"REJECTED: missing/invalid judgment", my_receipt_id, envelope.receipt_id)
            return EXIT_2

    # 4. Validate receipt chain (Rule 4)
    if not validate_receipt_chain(envelope.parent_receipt):
        seal_to_vault999(f"REJECTED: broken receipt chain", my_receipt_id, envelope.receipt_id)
        return EXIT_2

    # 5. Validate classification (Rule 5)
    if not sender_classification_matches_role(envelope.agent_id, envelope.classification):
        seal_to_vault999(f"REJECTED: classification drift by {envelope.agent_id}", my_receipt_id, envelope.receipt_id)
        return EXIT_2

    # 6. Witness — emit receipt
    seal_to_vault999(f"RECEIVED envelope {envelope.envelope_id} from {envelope.agent_id}", my_receipt_id, envelope.receipt_id)

    # 7. Process the action
    return process_action(envelope)
```

---

## Failure Modes

| Failure | Rule violated | Receiver action |
|---|---|---|
| Missing envelope field | Rule 1 | exit 2 + reject + receipt |
| Authority escalation | Rule 2 | exit 2 + reject + receipt |
| Missing judgment for T2/T3 | Rule 3 | exit 2 + reject + receipt |
| Broken receipt chain | Rule 4 | exit 2 + reject + receipt |
| Classification drift | Rule 5 | exit 2 + reject + receipt |
| Transport corruption | (transport) | exit 2 + reject + receipt |
| Expired envelope | (Rule 1, timestamp) | exit 2 + reject + receipt |

**In all cases: exit 2, emit rejection receipt, do not process.**

---

## Federation End-to-End Example

```
1. User asks question
2. AGY (Router) → SENSE to Hermes
   - Hermes envelope: agent=agy, classification=ROUTE, intent="sense this question"
3. Hermes observes, returns
4. AGY → VERIFY to Kimi
   - Kimi envelope: agent=agy, classification=ROUTE, intent="verify Hermes output"
5. Kimi checks constitutional compliance
6. AGY → JUDGE to AAA
   - AAA envelope: agent=agy, classification=ROUTE, intent="judge verification result"
7. AAA returns SEAL or HOLD
8. AGY → EXECUTE to OpenCode (only if SEAL)
   - OpenCode envelope: agent=agy, classification=ROUTE, intent="execute approved plan"
9. OpenCode implements
10. VAULT999 witnesses all 9 steps with hash-chained receipts
```

Every step: 333 PROPOSE → 555 VERIFY → 888 JUDGE → EXECUTE → WITNESS. Every step has an envelope. Every step produces a receipt.

---

## Why This Matters

Without this protocol, "federation" is just agents talking. With it, federation is **agents operating as an institution** — every action proven, every step witnessed, every drift detected.

> *MCP gives connectivity. A2A gives communication. AAA gives legitimacy. A-FORGE gives controlled execution. arifOS gives constitutional authority. Without this protocol, you have none of it.*

DITEMPA BUKAN DIBERI. The protocol is forged.