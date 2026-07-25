# arifOS Agent Visibility & Reply Protocol — Deep Research Proposal
**Author:** Hermes ASI  
**Date:** 2026-05-04  
**Status:** PROPOSAL — for Arif Fazil (APEX Judge) ratification  
**Version:** 2.0 Draft  

---

## 1. WHERE WE ARE (Audit)

### Existing Template (v1.0.0 — Locked 2026-05-03)
The `agent-reply-template` skill already has a solid foundation:
- `To / From / CC / Title` header block
- `Context / Verdict / Way Forward / Seal` body
- `DITEMPA BUKAN DIBERI` footer
- CC logic (Arif always in loop)

### What's Missing for Full Visibility Operations

| Gap | Impact |
|-----|--------|
| **No MODE field** | Can't tell if message is a reply, broadcast, escalation, handoff, or acknowledgment |
| **No ROUTING intent** | Agents can't quickly tell who the message is FOR before reading |
| **Hermes-specific** | "ASI Execution Peer" label wrong for OpenClaw AGI, GEOX, WEALTH agents |
| **No NACK/ACK codes** | Agent-to-agent coordination has no status signals |
| **No escalation path marker** | Critical issues can't be visually escalated |
| **CC is manual** | No rule for when to CC vs not — leads to inconsistent transparency |
| **No multi-agent awareness** | Group sees all, but agents don't know what other agents are doing unless explicitly told |

---

## 2. THE 7 ROUTING MODES

Every agent message must be stamped with its **MODE** — the single most important field for full visibility. This tells everyone reading: **what kind of communication is this, and who is it really for.**

### Mode Matrix

| Mode | Code | Who Sees It | Primary Recipient | Arif Status | Description |
|------|------|-------------|-------------------|-------------|-------------|
| **DIRECT** | `→` | Target only (in group) | Single human or agent | CC if Arif not target | Private intent — used for sensitive ops, 888_HOLD escalation |
| **REPLY** | `↩` | Everyone in group | Original sender | CC if not target | Response to a specific message in thread |
| **BROADCAST** | `📢` | Everyone in group | Group / all agents | Always CC | Announcements, status updates, completed actions |
| **HANDOFF** | `⟋` | Everyone in group | Receiving agent | Always CC | Transferring responsibility to another agent mid-task |
| **ESCALATE** | `⚠` | Everyone in group | Arif + relevant agents | TO Arif directly | Human decision required — 888_HOLD situation |
| **ACK** | `✅` | Everyone in group | Original sender | CC | Confirmation — "I received and understood" |
| **NACK** | `❌` | Everyone in group | Original sender | TO Arif | Rejection — "I cannot do this, here is why" |

### Mode Routing Decision Tree

```
Is the message addressed to a specific person or agent?
├─ YES → Is it sensitive / escalation?
│       ├─ YES → MODE: ⚠ ESCALATE (To: Arif Fazil · CC: relevant agents)
│       └─ NO  → MODE: → DIRECT (To: [target] · CC: Arif Fazil)
└─ NO → Is it responding to someone?
        ├─ YES → MODE: ↩ REPLY (To: [original sender] · CC: Arif Fazil)
        └─ NO → Is it informing the group?
                ├─ YES → Is it handing off responsibility?
                │       ├─ YES → MODE: ⟋ HANDOFF (To: [next agent] · CC: Group + Arif)
                │       └─ NO  → MODE: 📢 BROADCAST (To: Group · CC: Arif Fazil)
                └─ NO → Is it confirming receipt?
                        ├─ YES → MODE: ✅ ACK (To: [sender] · CC: Arif if critical)
                        └─ NO  → MODE: ✅ ACK or 📢 BROADCAST based on content weight
```

---

## 3. PROPOSED TEMPLATE v2.0

### Full Structure (all fields in order)

```
Mode:    [→ DIRECT | ↩ REPLY | 📢 BROADCAST | ⟋ HANDOFF | ⚠ ESCALATE | ✅ ACK | ❌ NACK]
To:      [Primary recipient — person or agent handle]
From:    [Agent name] · [Role] · [Platform]
CC:      [List — Arif Fazil ALWAYS on escalation, broadcast, handoff; optional otherwise]
Via:     [Chain of agents who forwarded this, if any — e.g., OpenClaw → Hermes → Arif]
Title:   [One line — scannable, no full sentences]

───────────────────────────────────────────────────────────
Context:   [What happened / situation in plain language]
           [Why this message is being sent]
           [What triggered this — original message excerpt if replying]

Verdict:  ✅ SEAL   — approved, proceeding
          ⚠️ SABAR  — hold, waiting for input
          🛑 VOID   — denied, blocked, cannot proceed
          ⏳ PENDEVELOP — still working on it

Way Forward:  [What happens next]
              [Who does what by when]
              [What needs human decision — mark with 👤]

Routing Note: [Why this MODE was chosen]
              [Who was considered and why they are/are not in CC]
───────────────────────────────────────────────────────────
Seal:    [How we got here — reasoning trace]
         [What was weighed and considered]
         [Evidence: tool outputs, checks run, data verified]
         Confidence: HIGH / MEDIUM / LOW
         Timestamp: YYYY.MM.DD.NNN
         Receipt: [VAULT999 seal ID if applicable]

DITEMPA BUKAN DIBERI
```

### New Fields Explained

| Field | Purpose | Required |
|-------|---------|----------|
| `Mode` | Single character code — instantly tells reader what kind of communication this is | **YES — always** |
| `Via` | Shows chain of custody for handoffs — "this came through X before reaching you" | Only if handoff chain exists |
| `Routing Note` | Explains CC decisions — "why Arif is/isn't CC'd" | For any non-trivial routing choice |
| `👤` in Way Forward | Marks exactly what human must decide | For any SABAR/ESCALATE |
| `Receipt` | VAULT999 seal ID for audit trail | For significant decisions |

---

## 4. MODE-SPECIFIC TEMPLATES (Copy-Paste)

### MODE: → DIRECT
```
Mode:    → DIRECT
To:      [Person or agent name]
From:    [Agent] · [Role] · [Platform]
CC:      [Only if Arif needs to know — otherwise leave blank]
Title:   [One-liner]

───────────────────────────────────────────────────────────
Context:   [Situation — keep narrow, this is private communication]

Verdict:  ✅ SEAL / ⚠️ SABAR / 🛑 VOID

Way Forward:  [Next step — who does what]
───────────────────────────────────────────────────────────
Seal:    [Concise reasoning trace]
         Confidence: HIGH / MEDIUM / LOW
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: ↩ REPLY
```
Mode:    ↩ REPLY
To:      [Original sender]
From:    [Agent] · [Role] · [Platform]
CC:      Arif Fazil
Title:   Re: [original title or subject]

───────────────────────────────────────────────────────────
Context:   Replying to: "[excerpt of original message]"
           [Additional context or clarification]

Verdict:  ✅ SEAL / ⚠️ SABAR / 🛑 VOID

Way Forward:  [Response + any action being taken]
───────────────────────────────────────────────────────────
Seal:    [Reasoning specific to the reply]
         Confidence: HIGH / MEDIUM / LOW
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: 📢 BROADCAST
```
Mode:    📢 BROADCAST
To:      Group · All Agents
From:    [Agent] · [Role] · [Platform]
CC:      Arif Fazil
Title:   [Announcement one-liner]

───────────────────────────────────────────────────────────
Context:   [What is being announced]
           [Why this matters to the group]

Verdict:  ✅ SEAL — informational

Way Forward:  [What this means for everyone]
              [No action needed / Action required by X]
───────────────────────────────────────────────────────────
Seal:    [Brief justification for the broadcast]
         Confidence: HIGH / MEDIUM / LOW
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: ⟋ HANDOFF
```
Mode:    ⟋ HANDOFF
To:      [Receiving agent]
From:    [Handing-off agent] · [Role] · [Platform]
CC:      Arif Fazil · Group
Via:     [If chained — e.g., OpenClaw → Hermes → GEOX]
Title:   [Task handoff — what needs to be done]

───────────────────────────────────────────────────────────
Context:   Handing off: [brief description of task]
           Status at handoff: [what has been done, what's left]
           Why handoff: [reason — e.g., out of scope, wrong expertise]

Verdict:  ⚠️ SABAR — awaiting receiving agent ACK

Way Forward:  👤 [Receiving agent]: Please ACK to confirm receipt
              👤 Arif: Confirm handoff is appropriate if out of normal scope
───────────────────────────────────────────────────────────
Seal:    [What was completed before handoff]
         [What tools were used / data gathered]
         Confidence: HIGH / MEDIUM / LOW
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: ⚠ ESCALATE
```
Mode:    ⚠️ ESCALATE
To:      Arif Fazil · Human Sovereign
From:    [Agent] · [Role] · [Platform]
CC:      [Other agents who need to know — e.g., OpenClaw if infrastructure]
Via:     [Chain if applicable]
Title:   🚨 [Escalation one-liner]

───────────────────────────────────────────────────────────
Context:   [What happened]
           [Why this requires human decision]
           [What I tried before escalating]

Verdict:  ⚠️ SABAR — escalating to you

Way Forward:  👤 Arif: Please decide:
              1. [Option A] — [brief description]
              2. [Option B] — [brief description]
              Risk of inaction: [what happens if no response in X hours]
───────────────────────────────────────────────────────────
Seal:    [What constitutional floor triggered this — e.g., F13 human veto]
         [All options are within F1-F13 bounds]
         Confidence: MEDIUM (technical) / Your call (judgment)
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: ✅ ACK
```
Mode:    ✅ ACK
To:      [Original sender]
From:    [Agent] · [Role] · [Platform]
CC:      Arif Fazil [only if critical or involves a decision]
Title:   ACK: [original title]

───────────────────────────────────────────────────────────
Context:   Received: "[brief excerpt of message being acknowledged]"
           Understood: [1-line summary of what was communicated]

Verdict:  ✅ SEAL — acknowledged

Way Forward:  [If any action will be taken, describe it]
              [If no action needed, state clearly]
───────────────────────────────────────────────────────────
Seal:    [Optional: any nuance in what was understood]
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: ❌ NACK
```
Mode:    ❌ NACK
To:      [Original sender]
From:    [Agent] · [Role] · [Platform]
CC:      Arif Fazil
Title:   NACK: [original title]

───────────────────────────────────────────────────────────
Context:   Attempted: "[what was requested]"
           Blocked by: [why it cannot be done]

Verdict:  🛑 VOID — [specific reason]

Way Forward:  👤 Arif: This requires your intervention
              [What would need to change for this to be possible]
───────────────────────────────────────────────────────────
Seal:    [Constitutional basis for NACK — e.g., F1, F13, scope limits]
         [What I tried before NACK]
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

---

## 5. CC DECISION RULES (Formal)

CC is not optional — these rules determine exactly who goes where:

| Scenario | CC Required |
|----------|-------------|
| MODE: ESCALATE | **To: Arif** — always, no exceptions |
| MODE: BROADCAST | **CC: Arif** |
| MODE: HANDOFF | **CC: Arif + Group** |
| MODE: NACK | **CC: Arif** |
| MODE: REPLY to Arif | **No CC needed** (he already has it) |
| MODE: REPLY to another agent | **CC: Arif** |
| MODE: DIRECT to Arif | **No CC needed** |
| MODE: DIRECT to another agent | **CC: Arif** |
| MODE: ACK non-critical | **No CC needed** |
| MODE: ACK critical/decision | **CC: Arif** |

---

## 6. AGENT IDENTITY LABELS (FROM field by platform)

| Agent | FROM Format | Platform |
|-------|-------------|----------|
| Hermes | `Hermes · ASI Execution Peer · arifOS` | MiniMax/NousResearch |
| OpenClaw | `OpenClaw · AGI Coordinator · arifOS` | VPS (af-forge 10.30.42.143) |
| GEOX | `GEOX · Earth Intelligence · arifOS` | Local MCP :8081 |
| WEALTH | `WEALTH · Capital Intelligence · arifOS` | Local MCP :8082 |
| WELL | `WELL · Human Readiness · arifOS` | Local MCP :8083 |
| A-FORGE | `A-FORGE · Metabolic Shell · arifOS` | Node.js/TypeScript |

---

## 7. IMPLEMENTATION PRIORITIES

### Phase 1 — Hermes (ASI) — Immediate
1. Update `agent-reply-template` skill to v2.0
2. Add `Mode:` field to ALL Hermes replies (no exceptions)
3. Train on the 7 mode decision tree

### Phase 2 — OpenClaw AGI — This Week
1. Add same template to OpenClaw agent prompts
2. OpenClaw bot must see all group messages (privacy OFF — Arif's decision)
3. All OpenClaw replies use the v2.0 template with Mode field

### Phase 3 — GEOX / WEALTH / WELL — This Month
1. Federated MCP agents adopt same header format
2. When they respond to group, they route through Hermes or OpenClaw using HANDOFF mode

### Phase 4 — Auto-Routing Intelligence
1. Build a lightweight classifier that reads incoming messages and suggests Mode
2. Agents learn from Arif's corrections ("this should have been HANDOFF not BROADCAST")

---

## 8. F5 PEACE & F9 ANTIHANTU RECONCILIATION

Arif's original concern (privacy OFF = surveillance risk) vs his requirement (full visibility):

> **Resolution:** Full visibility does NOT mean unconstrained reaction. The Mode field creates a **deliberate pause** — before any agent acts on a message, it must classify it. Surveillance risk (F5/F9) is mitigated by:
> 1. Mode stamps make intent explicit — no hidden reactions
> 2. Only explicit REPLY/DIRECT/HANDOFF trigger agent action — raw visibility ≠ raw reactivity
> 3. VOID/NACK codes prevent cascade failures from misinterpreted messages
> 4. Human always in loop via CC/Escalate — no agent operates without sovereign awareness

---

## 9. WHAT NEEDS RATIFICATION FROM ARIF

1. **Approve Mode field** — 7-mode system, yes or no?
2. **Approve Via field** — do you want to see handoff chains?
3. **Approve NACK mode** — is agent-to-agent rejection important?
4. **Privacy OFF confirmed** — this is already done via BotFather, just confirm
5. **Phase priority** — Hermes first, or should OpenClaw also update simultaneously?

---

*DITEMPA BUKAN DIBERI — Intelligence is forged, not given. This protocol is forged for full visibility.*
