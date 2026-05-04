# ADR-011: AAA Telegram Messaging Protocol — Structured Template with FROM/TO/CC/SEAL

**ADR ID:** ADR-011-AAA-TELEGRAM-MESSAGING-PROTOCOL  
**Date:** 2026-05-04  
**Epoch:** EPOCH-2026-05-04  
**Verdict:** RESEARCH — IN PROGRESS  
**Author:** AGI OPENCLAW  
**Status:** DRAFT — awaiting sovereign ratification  

---

## Preamble

Arif's sovereign decree (2026-05-04):

> *"I want my bot to see everything complete visibility. That's why it's important from now on each bot need to always put header with FROM and footer SEAL and proper template. Can we do deep research on that. Please present my proposal with all mode available agent can reply to human and to other agents etc. Human always in the loop. Cc list included. So agent also need to identify to whom the message was meant to."*

This ADR is the research output — proposing the full messaging protocol.

---

## 1. Problem Statement

Current state:
- OpenClaw and Hermes both in AAA group
- Bots cannot see each other's messages (Telegram limitation)
- No structured FROM/TO/CC headers
- No consistent footer SEAL template
- Recipient intent is implicit, not explicit
- Human is not systematically in the loop

Required:
- Every message is structured with FROM identity, TO recipient, CC list
- Every message has body, proper template, footer SEAL
- Multiple communication modes cover all A→H, A→A, A→H(cc), A→broadcast cases
- Human is always in the loop
- Recipient is always identifiable by sender and readers

---

## 2. Communication Mode Taxonomy

### 2.1 Mode List

| Mode | Code | From | To | CC | Human Loop | Description |
|------|------|------|----|----|------------|-------------|
| Agent → Human (direct) | `A2H` | Agent | Human | — | Direct | Single human recipient, no copies |
| Agent → Human (cc) | `A2Hcc` | Agent | Human | List | Direct + CC | Human primary, CC notified |
| Agent → Agent | `A2A` | Agent | Agent | — | Via gateway | Agent-to-agent, gateway relays visible |
| Agent → Human (broadcast) | `A2H_bcast` | Agent | ALL | — | All humans | Announcement to all |
| Human → Agent | `H2A` | Human | Agent | — | N/A | Human invokes agent |
| Human → Human | `H2H` | Human | Human | — | N/A | Human-to-human, bots observe |
| Gateway Meta | `META` | Gateway | ALL | — | All | Orchestrator status lines |

### 2.2 Mode Priority for AAA

For AAA governance context, the primary modes are:
1. **`A2H`** — agent to human (Arif)
2. **`A2Hcc`** — agent to human with CC list
3. **`A2A`** — agent to agent (Hermes ↔ OpenClaw via gateway relay)
4. **`A2H_bcast`** — rare, for constitutional announcements only
5. **`META`** — gateway orchestrator lines only

---

## 3. Message Template Structure

### 3.1 Full Template Anatomy

```
╔══════════════════════════════════════════════════════════════╗
║ HEADER                                                      ║
║   FROM:      agent://arifos/{AGI|ASI|APEX} @{bot_handle}     ║
║   TO:        {recipient_handle}                              ║
║   CC:        {comma_separated_handles|—}                    ║
║   MODE:      {A2H|A2Hcc|A2A|A2H_bcast|META}                  ║
║   TASK_ID:   {taskId|—}                                      ║
║   TIMESTAMP: {ISO-8601}                                      ║
╠══════════════════════════════════════════════════════════════╣
║ BODY                                                        ║
║                                                              ║
║   [content — varies by mode]                                 ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║ FOOTER — SEAL                                                ║
║   🔏 SEAL: {verdict_code} | {floor_scope} | {confidence}     ║
║   🏛️ VAULT999: {receipt_id|pending|—}                       ║
║   ⚖️ VERDICT: {SEAL|SABAR|HOLD|VOID|—}                      ║
╚══════════════════════════════════════════════════════════════╝
```

### 3.2 Template By Mode

#### Mode A2H (Agent → Human)

```
╔══════════════════════════════════════════════════════════════╗
║ HEADER
║   FROM:      agent://arifos/AGI @AGI_ASI_bot
║   TO:        @ariffazil
║   CC:        —
║   MODE:      A2H
║   TASK_ID:   aaa-20260504-001
║   TIMESTAMP: 2026-05-04T13:55:00Z
╠══════════════════════════════════════════════════════════════╣
║ BODY
║
║   [content directed to Arif only]
║
╠══════════════════════════════════════════════════════════════╣
║ FOOTER — SEAL
║   🔏 SEAL: CLAIM | F01,F02,F04 | HIGH
║   🏛️ VAULT999: pending
║   ⚖️ VERDICT: —
╚══════════════════════════════════════════════════════════════╝
```

#### Mode A2Hcc (Agent → Human with CC)

```
╔══════════════════════════════════════════════════════════════╗
║ HEADER
║   FROM:      agent://arifos/AGI @AGI_ASI_bot
║   TO:        @ariffazil
║   CC:        @ASI_arifos_bot, @APEX_observer
║   MODE:      A2Hcc
║   TASK_ID:   aaa-20260504-002
║   TIMESTAMP: 2026-05-04T13:56:00Z
╠══════════════════════════════════════════════════════════════╣
║ BODY
║
║   [content with implicit CC notification]
║
╠══════════════════════════════════════════════════════════════╣
║ FOOTER — SEAL
║   🔏 SEAL: PLAUSIBLE | F01,F02,F08 | MEDIUM
║   🏛️ VAULT999: receipt-id-xyz
║   ⚖️ VERDICT: SABAR
╚══════════════════════════════════════════════════════════════╝
```

#### Mode A2A (Agent → Agent, relay via gateway → Telegram)

```
╔══════════════════════════════════════════════════════════════╗
║ HEADER
║   FROM:      agent://arifos/AGI @AGI_ASI_bot
║   TO:        agent://arifos/ASI @ASI_arifos_bot
║   CC:        —
║   MODE:      A2A
║   TASK_ID:   aaa-20260504-003
║   TIMESTAMP: 2026-05-04T13:57:00Z
╠══════════════════════════════════════════════════════════════╣
║ BODY
║
║   [Hermes-visible plan or query — relayed by gateway]
║
╠══════════════════════════════════════════════════════════════╣
║ FOOTER — SEAL
║   🔏 SEAL: HYPOTHESIS | F01,F02 | LOW
║   🏛️ VAULT999: pending
║   ⚖️ VERDICT: —
╚══════════════════════════════════════════════════════════════╝
```

#### Mode META (Gateway orchestrator)

```
╔══════════════════════════════════════════════════════════════╗
║ HEADER
║   FROM:      gateway://aaa/ AAA-Gateway
║   TO:        ALL
║   CC:        —
║   MODE:      META
║   TASK_ID:   aaa-20260504-001
║   TIMESTAMP: 2026-05-04T13:57:01Z
╠══════════════════════════════════════════════════════════════╣
║ BODY
║
║   [Orchestrator status: "Planning… Executing… Reviewing…"]
║
╠══════════════════════════════════════════════════════════════╣
║ FOOTER — SEAL
║   🔏 SEAL: META | — | —
║   🏛️ VAULT999: —
║   ⚖️ VERDICT: —
╚══════════════════════════════════════════════════════════════╝
```

### 3.3 Special Cases

#### Broadcast Mode (A2H_bcast) — Constitutional Announcements Only

```
╔══════════════════════════════════════════════════════════════╗
║ HEADER
║   FROM:      agent://arifos/APEX @APEX_observer
║   TO:        ALL
║   CC:        —
║   MODE:      A2H_bcast
║   TASK_ID:   constitutional-20260504-001
║   TIMESTAMP: 2026-05-04T00:00:00Z
╠══════════════════════════════════════════════════════════════╣
║ BODY
║
║   [Constitutional broadcast — treaty update, etc.]
║
╠══════════════════════════════════════════════════════════════╣
║ FOOTER — SEAL
║   🔏 SEAL: CLAIM | F01,F02,F13 | HIGH
║   🏛️ VAULT999: vault-entry-id
║   ⚖️ VERDICT: SEAL
╚══════════════════════════════════════════════════════════════╝
```

---

## 4. FROM Identity Registry

Every agent in AAA must have a canonical FROM identity:

| Agent | FROM String | Bot Handle | Lane |
|-------|-------------|------------|------|
| OpenClaw (this agent) | `agent://arifos/AGI` | `@AGI_ASI_bot` | AGI |
| Hermes | `agent://arifos/ASI` | `@ASI_arifos_bot` | ASI |
| APEX Observer | `agent://arifos/APEX` | `@APEX_observer` | APEX |
| AAA Gateway | `gateway://aaa/` | `@AAA_conductor` | MESH |
| Arif (human) | `human://ariffazil` | `@ariffazil` | SOVEREIGN |

---

## 5. TO and CC Routing Rules

### 5.1 TO Rules

| FROM → TO | Routing | Notes |
|-----------|---------|-------|
| AGI → Arif | Direct via OpenClaw token → TG | Normal response |
| AGI → Hermes | A2A via gateway relay | Gateway POSTs Hermes message via Hermes token |
| Hermes → Arif | A2A via gateway relay | Gateway POSTs via Hermes token |
| Hermes → AGI | A2A via gateway | Gateway POSTs via OpenClaw token |
| APEX → Arif | Via gateway relay | Rare, constitutional only |
| Gateway → ALL | META broadcast | Status lines only |

### 5.2 CC Rules

CC list is comma-separated handles in HEADER. Rules:
- CC is always visible in the message header
- CC recipients should be @mentioned in body if action required
- CC can include other bots (for audit trail) and humans (for information)
- Empty CC = `—`

### 5.3 Human in the Loop

| Scenario | Human Loop |
|----------|-----------|
| A2H direct | Human is primary recipient |
| A2Hcc | Human is primary, CC includes others |
| A2A | Gateway relays to human for visibility (both agents visible) |
| A2H_bcast | All humans in group notified |
| META | Human sees gateway status lines |

---

## 6. SEAL and Verdict Footer

### 6.1 SEAL Structure

`🔏 SEAL: {belief_strength} | {floor_scope} | {confidence}`

| Field | Values | Description |
|-------|--------|-------------|
| belief_strength | CLAIM, PLAUSIBLE, HYPOTHESIS, ESTIMATE, UNKNOWN | Per epistemic signal schema |
| floor_scope | Comma-separated F-codes or `—` | Floors touched by this message |
| confidence | HIGH, MEDIUM, LOW | Self-assessed confidence |

### 6.2 VERDICT Field

`⚖️ VERDICT: {SEAL|SABAR|HOLD|VOID|—}`

Only present if 888_JUDGE was invoked.

### 6.3 VAULT999 Field

`🏛️ VAULT999: {receipt_id|pending|—}`

Links to VAULT999 receipt chain entry if applicable.

---

## 7. Task ID and Threading

- Every task gets a `taskId: aaa-YYYYMMDD-NNN` format
- Initial message from human: human generates taskId
- Subsequent replies carry same taskId for threading
- All messages in same thread share the same taskId
- A2A messages also carry taskId for traceability

---

## 8. Recipient Identification

Each message explicitly states:
1. **FROM** — who sent it (agent identity + bot handle)
2. **TO** — primary intended recipient (handle or ALL)
3. **CC** — secondary recipients (list or —)
4. **MODE** — communication mode for routing clarity

This allows:
- Human to know who the message is for
- Bot to know who it can respond to
- Gateway to know how to route the message
- Audit trail to reconstruct the full conversation

---

## 9. Mode Determination Logic (Pseudocode)

```python
def determine_mode(sender, primary_recipient, cc_list, context):
    # Mode A2H — direct to human, no CC
    if is_human(primary_recipient) and is_empty(cc_list):
        return "A2H"
    
    # Mode A2Hcc — to human with CC
    if is_human(primary_recipient) and not is_empty(cc_list):
        return "A2Hcc"
    
    # Mode A2A — agent to agent
    if is_agent(primary_recipient) and is_agent(sender):
        return "A2A"
    
    # Mode A2H_bcast — from APEX to ALL
    if primary_recipient == "ALL" and is_apex(sender):
        return "A2H_bcast"
    
    # Mode META — gateway orchestrator
    if is_gateway(sender):
        return "META"
    
    # Default: A2H (agent to human, safe default)
    return "A2H"
```

---

## 10. Telegram Implementation

### 10.1 Message Formatting

Telegram messages are plain text but structured:

```
FROM: agent://arifos/AGI @AGI_ASI_bot
TO: @ariffazil
CC: —
MODE: A2H
TASK_ID: aaa-20260504-001
TIMESTAMP: 2026-05-04T13:55:00Z

---

[body content]

---

🔏 SEAL: CLAIM | F01,F02,F04 | HIGH
🏛️ VAULT999: pending
⚖️ VERDICT: —
```

The box-drawing characters (╔, ╠, ╚) can be replaced with `---` separator lines for cleaner Telegram rendering.

### 10.2 Two-Bot Send Architecture

```
OpenClaw sends A2H:    → sendMessage via @AGI_ASI_bot token
Hermes sends A2H:      → sendMessage via @ASI_arifos_bot token
Gateway sends META:     → sendMessage via whichever token owns the session
A2A visible relay:     → gateway calls sendMessage with destination token
```

---

## 11. Research Gaps and Open Questions

| # | Question | Status |
|---|----------|--------|
| 1 | Should box-drawing characters render well in Telegram? | TEST: need to verify |
| 2 | How does Hermes receive A2A messages from gateway? | PENDING: Hermes token + endpoint unknown |
| 3 | Should CC list include @ mentions in body? | DECISION: yes if action required |
| 4 | How to handle long messages that exceed TG limits? | SPLIT: multiple messages with PART 1/N |
| 5 | Should we use Telegram message threading (reply_to)? | YES: for same taskId conversations |
| 6 | What is the Hermes bot token and endpoint? | BLOCKED: need from Arif |
| 7 | Do we need a META bot separate from AGI/ASI bots? | NO: META from gateway uses whichever token |

---

## 12. Next Steps

1. **Sovereign ratification** of this ADR — Arif approves or modifies
2. **Implement template parser** in OpenClaw gateway
3. **Wire Hermes token** — create @ASI_arifos_bot via @BotFather
4. **Test A2H mode** with this template
5. **Test A2A mode** when Hermes token is available
6. **Document agent cards** with new FROM identity registry

---

## 13. Alignment with Existing AAA Infrastructure

- **AAA_TREATY_LAW.md**: FROM identities must match agent registry in treaty
- **A2A_SPEC_ALIGNMENT.md**: `reply_mode` field maps to our MODE field
- **ADR-010**: Two-bot architecture confirmed — this ADR provides the message format for that architecture
- **epistemic_signal_schema.json**: `belief_strength` values map to SEAL field

---

*Ditempa Bukan Diberi — forged, not given.*
*AGI OPENCLAW — 2026-05-04*
