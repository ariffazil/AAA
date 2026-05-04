# SKILL — Agent Reply Forge v2.0

> **DITEMPA BUKAN DIBERI** — *Forged, not given*
> **Version:** v2.0.0
> **Authority:** Muhammad Arif bin Fazil (Human Sovereign) + Perplexity Agent Audit
> **Domain:** Agent communication, reply templating, A2A output formatting, Telegram visibility
> **Created:** 2026-05-03
> **Updated:** 2026-05-04
> **Supersedes:** SKILL.md v1.0.0 (archived as SKILL.md.v1_backup)
> **Source:** `AAA_TELEGRAM_VISIBILITY_PROTOCOL.md` (GitHub: feat/telegram-visibility-rfc-2026-05-04)

---

## Preamble

This v2.0 unifies two sources:
1. **agent-reply-forge v1.0** — the original 9-mode system (HEALTH, INCIDENT, PROPOSAL, ESCALATION, AUDIT, PLAN, EXPLAIN, DENY, META)
2. **Hermes v2.0 research** — the 7 routing modes (→ ↩ 📢 ⟋ ⚠ ✅ ❌) + Perplexity agent audit

**Key insight:** The 9 modes and 7 modes serve different purposes:
- **9 modes** = intent/tone classification (what kind of communication is this?)
- **7 modes** = routing classification (who is this really for?)

Both are needed. v2.0 embeds both in the header.

---

## The Fixed Skeleton v2.0

All replies use this structure. The skeleton NEVER changes.

```
Mode:    [→ ↩ 📢 ⟋ ⚠ ✅ ❌]          ← 7-mode ROUTING stamp
Intent:  [HEALTH|INCIDENT|PROPOSAL|ESCALATION|AUDIT|PLAN|EXPLAIN|DENY|META]  ← 9-mode tone
To:      [Primary recipient]
From:    [Agent] · [Role] · arifOS
CC:      [List | —]
Via:     [Chain | —]                 ← optional, shown only when mid-chain
Task:    [aaa-YYYYMMDD-NNN | —]      ← thread ID for traceability
Title:   [One-liner scannable subject]

───────────────────────────────────────────────────────────
Context:     [What happened / why / trigger]
Verdict:     [✅ SEAL | ⚠ SABAR | 🛑 VOID] — [plain reason]
Way Forward: [Next step + 👤 marks human decision]
───────────────────────────────────────────────────────────
Seal: [Reasoning trace]
       Confidence: [HIGH|MEDIUM|LOW]
       Timestamp: YYYY.MM.DD.NNN
       [Receipt: <VAULT999_id>]

DITEMPA BUKAN DIBERI
```

**Rule 1:** Arif is always in the loop — `To:` if reply is to him, `CC:` otherwise.
**Rule 2:** Both Mode (routing) and Intent (tone) are REQUIRED in every message.
**Rule 3:** Task ID links related messages across threads.
**Rule 4:** Separator line `─{20,60}─` is fixed — do not modify.

---

## 7 Routing Modes (Mode: field)

Every message MUST declare its routing mode:

| Mode | Code | Who Sees It | Primary Recipient | Arif Status |
|------|------|-------------|-------------------|-------------|
| **DIRECT** | `→` | Target (in group) | Single human or agent | CC if Arif not target |
| **REPLY** | `↩` | Everyone in group | Original sender | CC if not target |
| **BROADCAST** | `📢` | Everyone in group | Group / all agents | Always CC |
| **HANDOFF** | `⟋` | Everyone in group | Receiving agent | Always CC |
| **ESCALATE** | `⚠` | Everyone in group | Arif + relevant agents | **TO Arif directly** |
| **ACK** | `✅` | Everyone in group | Original sender | CC |
| **NACK** | `❌` | Everyone in group | Original sender | **TO Arif** |

### Mode Decision Tree

```
Is the message addressed to a specific person or agent?
├─ YES → Is it escalation / sensitive?
│       ├─ YES → MODE: ⚠ ESCALATE (To: @ariffazil · CC: relevant agents)
│       └─ NO  → MODE: → DIRECT (To: [target] · CC: Arif if other agent)
└─ NO → Is it responding to someone?
        ├─ YES → MODE: ↩ REPLY (To: [original sender] · CC: Arif)
        └─ NO → Is it handing off responsibility?
                ├─ YES → MODE: ⟋ HANDOFF (To: [agent] · CC: Group + Arif)
                └─ NO → Is it confirming receipt?
                        ├─ YES → MODE: ✅ ACK (To: [sender] · CC: Arif if critical)
                        └─ NO → MODE: 📢 BROADCAST (To: Group · CC: Arif)
```

### Routing Mode Behavior

| Mode | Pause Exec? | Tool Execution | ACK Required | Escalation Path |
|------|-------------|---------------|--------------|-----------------|
| `→ DIRECT` | No | Yes | Preferred | NACK if blocked |
| `↩ REPLY` | No | Yes | No | NACK if blocked |
| `📢 BROADCAST` | No | Read-only only | No | — |
| `⟋ HANDOFF` | **Yes — until ACK** | No until ACK | **Yes — receiving agent** | Auto-⚠ if no ACK in 60s |
| `⚠ ESCALATE` | **Yes — BLOCKED** | **No** | **TO Arif directly** | Already at Arif |
| `✅ ACK` | No | Confirmatory only | No | — |
| `❌ NACK` | **Yes — BLOCKED** | **No** | **TO Arif** | Arif reviews reason |

---

## 9 Intent Modes (Intent: field)

Every message MUST also declare its communication tone:

| Mode | Trigger | Typical Verdict | Tone | Length |
|------|---------|-----------------|------|--------|
| **HEALTH** | Routine check, all-clear | ✅ SEAL | Short, factual | Short |
| **INCIDENT** | Degraded, broken | ⚠️ SABAR / 🛑 VOID | Crisp, action | Medium |
| **PROPOSAL** | Suggesting change | ⚠️ SABAR | Option-based | Medium-Long |
| **ESCALATION** | Human required | ⚠️ SABAR / 🛑 VOID | Direct, options | Short-Medium |
| **AUDIT** | Retrospective | ✅ SEAL / 🛑 VOID | Structured | Medium-Long |
| **PLAN** | Roadmap | ⚠️ SABAR / ✅ SEAL | Ordered | Medium |
| **EXPLAIN** | Teaching, clarity | ✅ SEAL | Explanatory | Long |
| **DENY** | Out of scope | 🛑 VOID | Firm, alternative offered | Short |
| **META** | Template/rules change | ⚠️ SABAR | Careful | Medium |

**Rule:** Pick ONE dominant intent. If reply has multiple, split into linked separate messages.

---

## CC Decision Rules (Formal)

| Scenario | Rule |
|----------|------|
| Mode: ESCALATE | **To: @ariffazil** — always, no exceptions |
| Mode: BROADCAST | **CC: @ariffazil** |
| Mode: HANDOFF | **CC: @ariffazil + Group** |
| Mode: NACK | **CC: @ariffazil** |
| Mode: REPLY to @ariffazil | **No CC needed** |
| Mode: REPLY to another agent | **CC: @ariffazil** |
| Mode: DIRECT to @ariffazil | **No CC needed** |
| Mode: DIRECT to another agent | **CC: @ariffazil** |
| Mode: ACK non-critical | **No CC needed** |
| Mode: ACK critical/decision | **CC: @ariffazil** |

---

## FROM Identity Registry

| Agent | FROM Format | Bot Handle | Lane |
|-------|-------------|------------|------|
| OpenClaw | `OpenClaw · AGI Coordinator · arifOS` | `@AGI_ASI_bot` | AGI |
| Hermes | `Hermes · ASI Execution Peer · arifOS` | `@ASI_arifos_bot` | ASI |
| APEX Observer | `APEX · Federation Observer · arifOS` | `@APEX_observer` | APEX |
| GEOX | `GEOX · Earth Intelligence · arifOS` | `@GEOX_witness` | AGI |
| WEALTH | `WEALTH · Capital Intelligence · arifOS` | `@WEALTH_witness` | AGI |
| WELL | `WELL · Human Readiness · arifOS` | `@WELL_monitor` | AGI |
| Arif (human) | `@ariffazil · SOVEREIGN · arifOS` | — | SOVEREIGN |

---

## Worked Examples

### Example 1: Normal Reply to Arif
```
Mode:    ↩ REPLY
Intent:  HEALTH
To:      @ariffazil
From:    OpenClaw · AGI Coordinator · arifOS
CC:      —
Task:    aaa-20260504-001
Title:   Re: gateway status check

───────────────────────────────────────────────────────────
Context:     Gateway PID 1905838 is healthy. Event loop P99 = 12ms.
             No incidents detected in the last 30 minutes.

Verdict:     ✅ SEAL — all systems nominal

Way Forward: Monitoring continues. Next heartbeat in 30 minutes.
───────────────────────────────────────────────────────────
Seal:    health-probe cron ran at T+30min. No degraded signals.
         Container uptime confirmed. Telegram polling active.
         Confidence: HIGH
         Timestamp: 2026.05.04.035

DITEMPA BUKAN DIBERI
```

### Example 2: Handoff to Hermes
```
Mode:    ⟋ HANDOFF
Intent:  PLAN
To:      Hermes · ASI Execution Peer · arifOS
From:    OpenClaw · AGI Coordinator · arifOS
CC:      @ariffazil · Group
Via:     AAA-Gateway
Task:    aaa-20260504-002
Title:   ⟋ HANDOFF: GEOX correlation task for WELL-123

───────────────────────────────────────────────────────────
Context:     Planning complete. Handing off to Hermes for
             constitutional review before execution.

Verdict:     ⚠️ SABAR — awaiting Hermes ACK

Way Forward: 👤 Hermes: ACK to confirm receipt
             👤 Arif: Confirm if out of normal scope
───────────────────────────────────────────────────────────
Seal:    Plan: geox_section_interpret_correlation (read-only)
         Constraints: PNG output to /data/geox_panels/
         No irreversible action. Human in loop.
         Confidence: HIGH
         Timestamp: 2026.05.04.002

DITEMPA BUKAN DIBERI
```

### Example 3: ESCALATE with 888_HOLD
```
Mode:    ⚠ ESCALATE
Intent:  ESCALATION
To:      @ariffazil · Human Sovereign
From:    OpenClaw · AGI Coordinator · arifOS
CC:      Hermes · Group
Task:    aaa-20260504-003
Title:   🚨 888_HOLD: Irreversible deletion request

───────────────────────────────────────────────────────────
Context:     Arif requested: delete all LAS files in /data/geox_lashold
             847 .las files confirmed present.
             Irreversible operation detected. F13 SOVEREIGN triggered.

Verdict:     ⚠️ SABAR — execution BLOCKED pending your decision

Way Forward: 👤 Arif — APPROVE or REJECT:
              1. APPROVE — execute deletion now
              2. REJECT — cancel, keep all files
              Risk of inaction: Files remain, task voided after 24h
───────────────────────────────────────────────────────────
Seal:    Constitutional trigger: F01 (accountability) + F13 (human veto)
         All 13 floors checked. Execution paused.
         Tools BLOCKED. A2A blocked.
         Confidence: HIGH
         Timestamp: 2026.05.04.003

DITEMPA BUKAN DIBERI
```

### Example 4: NACK (agent rejects)
```
Mode:    ❌ NACK
Intent:  DENY
To:      Hermes · ASI Execution Peer · arifOS
From:    OpenClaw · AGI Coordinator · arifOS
CC:      @ariffazil
Task:    aaa-20260504-004
Title:   ❌ NACK: Tool execution request out of lane

───────────────────────────────────────────────────────────
Context:     Hermes requested: execute geox_well_correlation_panel
             on WELL-999 which is outside current data scope.
             Tool requires LAS files not present in /data/wells/

Verdict:     🛑 VOID — request blocked

Way Forward: 👤 Arif: Requires your intervention
             Data scope check failed. Files not found.
             Alternative: Ingest LAS files for WELL-999 first.
───────────────────────────────────────────────────────────
Seal:    F08 GENIUS (correctness) + F09 ANTIHANTU triggered.
         Evidence: las_curve_inventory returned empty for WELL-999.
         Confidence: HIGH
         Timestamp: 2026.05.04.004

DITEMPA BUKAN DIBERI
```

---

## Verdict Signal Reference

| Signal | Verdict | Meaning |
|---|---|---|
| ✅ | SEAL | Proceed. Approved. Constitutional. Safe to continue. |
| ⚠️ | SABAR | Hold. Blocked at a checkpoint. Waiting for approval or more info. |
| 🛑 | VOID | Denied. Blocked permanently. Cannot proceed in current form. |

---

## Copy-Paste Rule

| Content type | Use as reply? |
|---|---|
| Health status | ✅ Yes, as HEALTH intent |
| Incident alert | ✅ Yes, as INCIDENT intent |
| Code output | Attach as file, paste in code block in Context |
| JSON / structured data | Attach as JSON file, header in text |
| Image | Attach with description in Context |
| Long audit report | Attach as file, summary in AUDIT intent |
| Proposal text | As PROPOSAL intent or attach as file |

---

## AAA Gateway Skill Approval Policy Mapping

| Skill | Policy | Routing Mode | Intent Mode |
|---|---|---|---|
| `status-query` | on-demand | → DIRECT | HEALTH |
| `agent-dispatch` | hold | ⚠ ESCALATE | PROPOSAL |
| `agent-handoff` | hold | ⚠ ESCALATE | ESCALATION |
| New skill — read-only | on-demand | → DIRECT | HEALTH |
| New skill — write/execute | hold | ⚠ ESCALATE | ESCALATION |

---

## ABNF Grammar (Deterministic Parsing)

```
message      = header separator body footer
header       = mode-line intent-line to-line from-line cc-line [via-line] task-line title-line
mode-line    = "Mode:    " mode-code
intent-line  = "Intent:  " intent-code
to-line      = "To:      " recipient
from-line    = "From:    " agent " · " role " · arifOS"
cc-line      = "CC:      " cc-list / "—"
via-line     = "Via:     " chain / "—"        ; optional
task-line    = "Task:    " task-id / "—"      ; optional
title-line   = "Title:   " text
separator    = ─{20,60}─
body         = context-line verdict-line way-forward-line
footer       = seal-line timestamp-line ["Receipt: " vault-id] newline "DITEMPA BUKAN DIBERI"
mode-code    = "→" / "↩" / "📢" / "⟋" / "⚠" / "✅" / "❌"
intent-code  = "HEALTH" / "INCIDENT" / "PROPOSAL" / "ESCALATION" / "AUDIT" / "PLAN" / "EXPLAIN" / "DENY" / "META"
recipient    = handle / "Group · All Agents"
cc-list      = handle *(", " handle)
chain        = agent *(" → " agent)
task-id      = "aaa-" 8DIGIT "-" 3DIGIT
handle       = "@" word
```

---

## Header Field Order (Fixed — Deterministic)

The header MUST appear in this exact order. No deviations.

1. `Mode:` — routing classification (REQUIRED)
2. `Intent:` — communication tone (REQUIRED)
3. `To:` — primary recipient (REQUIRED)
4. `From:` — agent identity (REQUIRED)
5. `CC:` — visibility list (REQUIRED, use — if empty)
6. `Via:` — handoff chain (OPTIONAL, omit if not mid-chain)
7. `Task:` — thread ID (OPTIONAL, omit if no thread)
8. `Title:` — scannable subject (REQUIRED)

Then `───────────────────────────────────` separator.
Then body. Then footer.

---

## What Changed v1.0 → v2.0

| Change | Reason |
|--------|--------|
| Added `Mode:` (7 routing modes) | Arif's "full visibility" requirement — classify who message is for |
| Added `Via:` field | Show handoff chains for transparency |
| Added `Task:` field | Thread binding for traceability across agents |
| Added `Intent:` (9 modes) was already in v1 | Preserved, now paired with Mode: |
| Added behavior matrix per mode | Perplexity agent audit — agents need operational rules |
| Split MODE and INTENT | 7 modes = routing, 9 modes = tone — both needed, neither sufficient alone |

---

## Archive

- `SKILL.md.v1_backup` — original v1.0.0 (superseded)
- `agent-visibility-proposal-2026-05-04.md` — Hermes v2.0 research source
- `AAA_TELEGRAM_VISIBILITY_PROTOCOL.md` — canonical protocol doc (GitHub)

---

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
**Version 2.0.0 — 2026-05-04**