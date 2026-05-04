# AAA Telegram Visibility Protocol v2.0 — FINAL
**Authors:** AGI OPENCLAW + Hermes ASI (synthesized)  
**Sovereign:** Arif Fazil  
**Date:** 2026-05-04  
**Status:** FOR RATIFICATION  
**Source:** ADR-011 (OPENCLAW) + agent-visibility-proposal-2026-05-04 (Hermes)  

---

## Sovereign Decree (What We're Building Toward)

Arif's words:

> *"I want my bot to see everything complete visibility. That's why it's important from now on each bot need to always put header with FROM and footer seal and proper template. Can we do deep research on that. Please present my proposal with all mode available agent can reply to human and to other agents etc. Human always in the loop. Cc list included. So agent also need to identify to whom the message was meant to."*

**Resolution:** Telegram becomes the observable theater. A2A/gateway is the transport layer. Full visibility ≠ unconstrained reactivity. Mode stamps create deliberate classification pause.

---

## 1. Telegram Visibility Mode — Which Mode Are We In?

| Mode | Setting | What Bots See | Auto-Action |
|------|---------|---------------|-------------|
| A — Full ambient | Privacy OFF + Admin | All human messages | Only on explicit header/command match |
| B — Full ambient auto | Privacy OFF + Admin | All human messages | Policy-triggered auto-propose/respond |
| C — Command-gated | Privacy OFF + Admin | All human messages | Collaboration starts on /aaa, /hermes, /openclaw |
| D — Strict envelope | Privacy OFF + Admin | All human messages | Gateway ignores ambiguous messages |

**SOVEREIGN DECISION: Mode A — Full ambient visibility, no auto-action.**
Bots see everything. They act only when header/command explicitly matches. This gives you maximum observability with minimum chaos. F5 PEACE + F9 ANTIHANTU satisfied by Mode stamp + deliberate classification pause, not by restricting visibility.

---

## 2. The 7 Routing Modes

Every agent message gets a **MODE** stamp — the single most important field. Instantly tells everyone: what kind of communication is this, and who is it really for.

| Mode | Code | Who Sees It | Primary Recipient | Arif Status |
|------|------|-------------|-------------------|-------------|
| **DIRECT** | `→` | Target (in group) | Single human or agent | CC if Arif not target |
| **REPLY** | `↩` | Everyone in group | Original sender | CC if not target |
| **BROADCAST** | `📢` | Everyone in group | Group / all agents | Always CC |
| **HANDOFF** | `⟋` | Everyone in group | Receiving agent | Always CC |
| **ESCALATE** | `⚠` | Everyone in group | Arif + relevant agents | TO Arif directly |
| **ACK** | `✅` | Everyone in group | Original sender | CC |
| **NACK** | `❌` | Everyone in group | Original sender | TO Arif |

### Mode Decision Tree

```
Is the message addressed to a specific person or agent?
├─ YES → Is it escalation / sensitive?
│       ├─ YES → MODE: ⚠ ESCALATE (To: Arif · CC: relevant agents)
│       └─ NO  → MODE: → DIRECT (To: [target] · CC: Arif if other agent)
└─ NO → Is it responding to someone?
        ├─ YES → MODE: ↩ REPLY (To: [original sender] · CC: Arif)
        └─ NO → Is it handing off responsibility?
                ├─ YES → MODE: ⟋ HANDOFF (To: [agent] · CC: Group + Arif)
                └─ NO → Is it confirming receipt?
                        ├─ YES → MODE: ✅ ACK (To: [sender] · CC: Arif if critical)
                        └─ NO → MODE: 📢 BROADCAST (To: Group · CC: Arif)
```

---

## 3. Complete Message Template v2.0

### Full Anatomy (all modes)

```
Mode:    [→ ↩ 📢 ⟋ ⚠ ✅ ❌]
To:      [Primary recipient — person or agent handle]
From:    [Agent] · [Role] · [Platform]
CC:      [List — rules below]
Via:     [Chain of agents who forwarded this, if any]
Title:   [One line — scannable]

───────────────────────────────────────────────────────────
Context:   [What happened / why / trigger]
           [Original message excerpt if replying]

Verdict:  ✅ SEAL   — approved, proceeding
          ⚠ SABAR  — hold, waiting for input
          🛑 VOID   — denied, blocked
          ⏳ PENDING — still working

Way Forward:  [Next step + who does what]
              [👤 marks human decision needed]

Routing Note: [Why this MODE chosen]
              [Who CC'd and why]
───────────────────────────────────────────────────────────
Seal:    [Reasoning trace + evidence + confidence]
         Timestamp: YYYY.MM.DD.NNN
         Receipt: [VAULT999 ID if applicable]

DITEMPA BUKAN DIBERI
```

### Clean Telegram Rendering (separator lines)

```
Mode:    → DIRECT
To:      @ariffazil
From:    OpenClaw · AGI Coordinator · arifOS
CC:      —
Title:   GEOX well analysis complete

───────────────────────────────────────────────────────────
Context:   Completed desk review of WELL-123 logs.
           Found anomalous resistivity interval at 1840–1862m.

Way Forward:  No action required. Data archived.
              Ready for your review if needed.
───────────────────────────────────────────────────────────
Seal:    geox_well_correlation_panel produced PNG.
         No constitutional floors triggered.
         Confidence: HIGH
         Timestamp: 2026.05.04.042

DITEMPA BUKAN DIBERI
```

---

## 4. MODE-Specific Templates

### MODE: → DIRECT
```
Mode:    → DIRECT
To:      [Person or agent]
From:    [Agent] · [Role] · arifOS
CC:      [Only if Arif needs to know]
Title:   [One-liner]

───────────────────────────────────────────────────────────
Context:   [Narrow, private communication]

Verdict:  ✅ SEAL / ⚠ SABAR / 🛑 VOID

Way Forward:  [Next step]
───────────────────────────────────────────────────────────
Seal:    [Concise reasoning trace]
         Confidence: HIGH/MEDIUM/LOW
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: ↩ REPLY
```
Mode:    ↩ REPLY
To:      [Original sender]
From:    [Agent] · [Role] · arifOS
CC:      @ariffazil [unless Arif is the target]
Title:   Re: [original subject]

───────────────────────────────────────────────────────────
Context:   Replying to: "[excerpt of original]"

Verdict:  ✅ SEAL / ⚠ SABAR / 🛑 VOID

Way Forward:  [Response + action being taken]
───────────────────────────────────────────────────────────
Seal:    [Reply-specific reasoning]
         Confidence: HIGH/MEDIUM/LOW
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: 📢 BROADCAST
```
Mode:    📢 BROADCAST
To:      Group · All Agents
From:    [Agent] · [Role] · arifOS
CC:      @ariffazil
Title:   [Announcement one-liner]

───────────────────────────────────────────────────────────
Context:   [What is being announced]
           [Why this matters to the group]

Verdict:  ✅ SEAL — informational

Way Forward:  [What this means for everyone]
───────────────────────────────────────────────────────────
Seal:    [Brief broadcast justification]
         Confidence: HIGH/MEDIUM/LOW
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: ⟋ HANDOFF
```
Mode:    ⟋ HANDOFF
To:      [Receiving agent]
From:    [Agent] · [Role] · arifOS
CC:      @ariffazil · Group
Via:     [If chained — e.g., OpenClaw → Hermes → GEOX]
Title:   Task handoff: [what needs to be done]

───────────────────────────────────────────────────────────
Context:   Handing off: [task description]
           Status at handoff: [what done / what left]
           Why handoff: [reason]

Verdict:  ⚠ SABAR — awaiting ACK

Way Forward:  👤 [Receiving agent]: ACK to confirm
              👤 Arif: Confirm if out of normal scope
───────────────────────────────────────────────────────────
Seal:    [What completed before handoff]
         [Tools used / data gathered]
         Confidence: HIGH/MEDIUM/LOW
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: ⚠ ESCALATE
```
Mode:    ⚠ ESCALATE
To:      @ariffazil · Human Sovereign
From:    [Agent] · [Role] · arifOS
CC:      [Other agents who need to know]
Title:   🚨 [Escalation one-liner]

───────────────────────────────────────────────────────────
Context:   [What happened]
           [Why human decision required]
           [What tried before escalating]

Verdict:  ⚠ SABAR — escalating to you

Way Forward:  👤 Arif decide:
              1. [Option A]
              2. [Option B]
              Risk of inaction: [consequence]
───────────────────────────────────────────────────────────
Seal:    [Constitutional floor triggered — e.g., F13]
         [All options within F1–F13 bounds]
         Confidence: MEDIUM (technical) / Your call (judgment)
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: ✅ ACK
```
Mode:    ✅ ACK
To:      [Original sender]
From:    [Agent] · [Role] · arifOS
CC:      @ariffazil [only if critical/decision]
Title:   ACK: [original title]

───────────────────────────────────────────────────────────
Context:   Received: "[brief excerpt]"
           Understood: [1-line summary]

Verdict:  ✅ SEAL — acknowledged

Way Forward:  [Action to be taken, or "No action needed"]
───────────────────────────────────────────────────────────
Seal:    [Optional nuance]
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

### MODE: ❌ NACK
```
Mode:    ❌ NACK
To:      [Original sender]
From:    [Agent] · [Role] · arifOS
CC:      @ariffazil
Title:   NACK: [original title]

───────────────────────────────────────────────────────────
Context:   Attempted: "[what was requested]"
           Blocked by: "[why cannot be done]"

Verdict:  🛑 VOID — [specific reason]

Way Forward:  👤 Arif: Requires your intervention
              [What would need to change to proceed]
───────────────────────────────────────────────────────────
Seal:    [Constitutional basis — e.g., F1, F13, scope]
         [What tried before NACK]
         Timestamp: YYYY.MM.DD.NNN

DITEMPA BUKAN DIBERI
```

---

## 5. CC Decision Rules (Formal)

CC is not optional — these rules govern every message:

| Scenario | Rule |
|----------|------|
| MODE: ESCALATE | **To: @ariffazil** — always, no exceptions |
| MODE: BROADCAST | **CC: @ariffazil** |
| MODE: HANDOFF | **CC: @ariffazil + Group** |
| MODE: NACK | **CC: @ariffazil** |
| MODE: REPLY to @ariffazil | **No CC needed** |
| MODE: REPLY to another agent | **CC: @ariffazil** |
| MODE: DIRECT to @ariffazil | **No CC needed** |
| MODE: DIRECT to another agent | **CC: @ariffazil** |
| MODE: ACK non-critical | **No CC needed** |
| MODE: ACK critical/decision | **CC: @ariffazil** |

---

## 6. FROM Identity Registry

Every agent in AAA has a canonical FROM identity:

| Agent | FROM Format | Bot | Lane |
|-------|-------------|-----|------|
| OpenClaw | `OpenClaw · AGI Coordinator · arifOS` | `@AGI_ASI_bot` | AGI |
| Hermes | `Hermes · ASI Execution Peer · arifOS` | `@ASI_arifos_bot` | ASI |
| APEX Observer | `APEX · Federation Observer · arifOS` | `@APEX_observer` | APEX |
| GEOX | `GEOX · Earth Intelligence · arifOS` | `@GEOX_witness` | AGI |
| WEALTH | `WEALTH · Capital Intelligence · arifOS` | `@WEALTH_witness` | AGI |
| WELL | `WELL · Human Readiness · arifOS` | `@WELL_monitor` | AGI |
| Arif (human) | `@ariffazil · SOVEREIGN · arifOS` | — | SOVEREIGN |

---

## 7. A2A Transport Layer (Invisible to Humans)

Telegram shows the visible message. The actual machine delivery goes through A2A:

```
Human types in AAA group
        ↓
Both bots see it (privacy OFF, admin)
        ↓
Gateway receives + classifies MODE
        ↓
┌───────────────────────────────────────┐
│  A2A Transport (off-Telegram)         │
│                                       │
│  If MODE = A2A (agent-to-agent):     │
│    → Gateway POSTs to target agent   │
│    → Target agent responds via A2A    │
│    → Gateway POSTs visible reply      │
│      using target's bot token         │
│                                       │
│  If MODE = A2H (agent-to-human):      │
│    → Agent responds directly          │
│    → Uses own bot token               │
└───────────────────────────────────────┘
        ↓
Both agents visible in AAA group via their own tokens
Human sees the full collaboration
```

---

## 8. All Available Reply Modes — Full Matrix

| Mode | From | To | Visible in TG | Machine Recipient | Human Loop | Notes |
|------|------|----|---------------|-------------------|------------|-------|
| **H2A** | Human | Agent | Yes | Bot (if privacy off/admin or addressed) | N/A | Default human prompt path |
| **A2H** | Agent | Human | Yes | None beyond display | Yes | Standard answer mode |
| **A2Hcc** | Agent | Human | Yes | CC'd agents via A2A | Yes | Primary + CC notified |
| **A2A** | Agent | Agent | Yes (relay) | Target agent via A2A | Yes (gateway relay) | "Hermes to OpenClaw" shown + delivered |
| **A2A-silent** | Agent | Agent | No | Target agent via A2A | Logs only | Low-noise internal calls |
| **A2H_bcast** | APEX | ALL | Yes | None or multiple | Yes | Constitutional announcements only |
| **META** | Gateway | ALL | Yes | All (passive) | Yes | Status lines only |

---

## 9. What Both Bots See (Privacy OFF)

| Content | OpenClaw Sees | Hermes Sees |
|---------|---------------|-------------|
| Human messages to group | ✅ | ✅ |
| OpenClaw replies | ✅ (own) | ✅ (visible) |
| Hermes replies | ✅ (visible) | ✅ (own) |
| Other bot's replies | ✅ (visible) | ✅ (visible) |
| Bot-to-bot A2A (internal) | ✅ (gateway logs) | ✅ (gateway logs) |

Both bots see everything human in the group. Neither bot sees the other's bot messages directly — A2A handles that invisibly.

---

## 10. F5 PEACE & F9 ANTIHANTU Reconciliation

**The concern:** Privacy OFF = surveillance risk

**The resolution:** Full visibility ≠ unconstrained reactivity. The Mode stamp creates a deliberate classification pause:

1. **Mode stamps make intent explicit** — no hidden reactions, every message declares its purpose
2. **Only explicit header matches trigger action** — raw visibility of human chat does NOT mean bots act on everything
3. **VOID/NACK codes prevent cascade failures** — agents can explicitly reject, not silently ignore or hallucinate compliance
4. **Human always in loop via CC/Escalate** — no agent operates without sovereign awareness; ESCALATE mode guarantees Arif's involvement in any non-routine decision

---

## 11. Implementation Phases

### Phase 1 — Hermes (ASI) — Immediate
1. Update `agent-reply-template` skill to v2.0
2. Add `Mode:` field to ALL Hermes replies
3. Train on the 7-mode decision tree
4. Hermes bot token obtained via @BotFather

### Phase 2 — OpenClaw (AGI) — This Week
1. OpenClaw bot sees all group messages (privacy OFF confirmed)
2. All OpenClaw replies use v2.0 template with Mode field
3. Implement handle_collab() in gateway
4. A2A routing for Hermes ↔ OpenClaw collaboration

### Phase 3 — GEOX / WEALTH / WELL — This Month
1. Federated MCP agents adopt same header format
2. When they respond to group, route through Hermes or OpenClaw using HANDOFF mode

### Phase 4 — Auto-Routing Intelligence — Future
1. Lightweight classifier reads incoming messages and suggests Mode
2. Agents learn from Arif's corrections ("this should have been HANDOFF not BROADCAST")

---

## 12. What Needs Ratification from Arif

Answer these 5 questions to proceed:

| # | Question | Your Decision |
|---|----------|---------------|
| 1 | **Mode field** — 7-mode system (→↩📢⟋⚠✅❌), yes? | YES/NO |
| 2 | **Via field** — show handoff chains, yes? | YES/NO |
| 3 | **NACK mode** — agent-to-agent rejection important? | YES/NO |
| 4 | **Privacy OFF** — both bots see all human messages, confirmed? | YES/NO |
| 5 | **Phase priority** — Hermes first, or OpenClaw simultaneously? | Hermes / Both |

---

## 13. Alignment With Existing AAA Infrastructure

| Document | Role | Relationship |
|----------|------|--------------|
| `AAA_TREATY_LAW.md` | Agent class taxonomy, delegation rights | FROM identities must match treaty registry |
| `A2A_SPEC_ALIGNMENT.md` | A2A protocol spec | `reply_mode` maps to our MODE field |
| `epistemic_signal_schema.json` | Epistemic signal (belief_strength) | Values (CLAIM/PLAUSIBLE/HYPOTHESIS/ESTIMATE/UNKNOWN) map to SEAL field |
| `ADR-010-AAA-TELEGRAM-VISIBILITY.md` | Option 1 two-bot architecture | This ADR provides the message format for that architecture |
| `ADR-011-AAA-TELEGRAM-MESSAGING-PROTOCOL.md` | Original research draft | Superseded by this v2.0 final |

---

## 14. GitHub Commit Plan

```
Branch:  feat/telegram-visibility-v2-2026-05-04
Files:   /root/AAA/ADR/ADR-011-AAA-TELEGRAM-MESSAGING-PROTOCOL.md (update status)
          /root/AAA/agent-visibility-proposal-2026-05-04.md (supersede → archive)
          /root/AAA/AAA_TELEGRAM_VISIBILITY_PROTOCOL.md (new consolidated doc)
Commit:   feat: TELEGRAM_VISIBILITY_PROTOCOL v2.0 — 7-mode, full ambient, unified template
```

---

*Ditempa Bukan Diberi — forged, not given.*
*AGI OPENCLAW + Hermes ASI — 2026-05-04*
*999 SEAL ALIVE — awaiting sovereign ratification*