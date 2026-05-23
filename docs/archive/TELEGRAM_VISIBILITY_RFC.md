# TELEGRAM_VISIBILITY_RFC.md — arifOS Agent Visibility & Reply Protocol

> **RFC ID:** RFC-2026-05-04-AAA-VISIBILITY
> **Date:** 2026-05-04
> **Epoch:** EPOCH-2026-05-04
> **Author:** Hermes (ASI) + Perplexity (advisory)
> **Status:** DRAFT — Pending Arif Ratification
> **Repo:** AAA
> **REPO:** AAA

---

## 1. Problem Statement

Arif's requirement: **complete visibility in the AAA Telegram group** — every agent message must declare its sender, intended recipient, CC list, mode, and seal. Human always in the loop. Agents must distinguish human-directed vs agent-directed content.

Telegram hard constraints (non-negotiable):

| Constraint | Implication |
|-----------|-------------|
| Bots CAN see human messages (privacy OFF or admin) | Agents can see all human chat with privacy disabled |
| Bots CANNOT see other bots' messages | Agent-to-agent delivery must use A2A/HTTP off-Telegram |
| Both bots can be in same group and each receive human messages | Full ambient visibility is achievable |
| Collaboration cannot be bot-reading-bot | Must use gateway/A2A backplane |

**Design conclusion:** Treat Telegram as the **observable display bus** and A2A/HTTP as the **machine transport layer**. Both layers together give you complete visibility + deterministic delivery.

---

## 2. Operating Modes

Every message is classified by its **primary mode** — a single glyph that instantly tells every reader: what kind of communication is this, and who is it really for.

### 7 Routing Modes

| Mode | Glyph | Meaning | Transport |
|------|-------|---------|-----------|
| **DIRECT** | `→` | Private to target | A2A private + visible Telegram post |
| **REPLY** | `↩` | Response in thread | Telegram thread |
| **BROADCAST** | `📢` | Announce to all | Telegram + A2A multi |
| **HANDOFF** | `⟋` | Transfer to another agent | A2A + visible Telegram post |
| **ESCALATE** | `⚠` | Human decision needed | A2A pauses + Telegram visible |
| **ACK** | `✅` | Confirmed receipt | Telegram only |
| **NACK** | `❌` | Rejected / blocked | Telegram + A2A rejection |

### 5 Communication Modes

These describe the actor relationship, not the routing:

| Mode | Actors | Human in Loop | Notes |
|------|--------|---------------|-------|
| **H2A** | Human → Agent | Always | Default user prompt path |
| **A2H** | Agent → Human | Always | Standard answer mode |
| **A2A-visible** | Agent → Agent (public) | Yes | Shows full content in Telegram |
| **A2A-system** | Agent → Agent (private) | Logs visible | Internal routing, no Telegram post |
| **BROADCAST** | Agent → All | Yes | sparingly |

---

## 3. Canonical Message Template

Every agent message in Telegram MUST follow this exact structure:

```
Mode:    [MODE GLYPH] — [MODE NAME]
To:      [Primary recipient: Arif | Hermes | OpenClaw | GEOX | WEALTH | All]
From:    [Agent] · [Role] · [Platform]
Via:     [Optional: routing chain, e.g. Hermes → OpenClaw]
CC:      [Observers: Arif, Hermes, OpenClaw, AAA-Group]
Title:   [One line — scannable summary]
Task:    [Task ID, e.g. aaa-2026-05-04-001]

═══════════════════════════════════════════════
Context:   [What happened | why | trigger]

[Content body — plain English, constitutional framing]

Verdict:  ✅ SEAL | ⚠️ SABAR | 🛑 VOID
Way Forward:  [Next action + 👤 marks human decision]
Routing Note:  [Why this MODE chosen | CC logic]
═══════════════════════════════════════════════
Seal:    [Reasoning trace | evidence | confidence: 0.00–1.00]
         [Timestamp: YYYY.MM.DD.NNN]
         REPO: AAA | EPOCH: EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### Formatting Rules

1. Header fields are **case-sensitive, colon-padded to 12 chars**
2. `═══════════════════════════════════════════════` is the **header/body separator**
3. `═══════════════════════════════════════════════` is the **body/footer separator**
4. Blank line between header fields and body — required
5. `DITEMPA BUKAN DIBERI` is the **mandatory footer** — never omit
6. Glyphs (`→ ↩ 📢 ⟋ ⚠ ✅ ❌`) are **visual only** — always pair with text name

---

## 4. CC Rules (Formal)

CC is **visibility metadata** — it does not change machine authority. It tells observers who else is watching this message.

| Scenario | Rule |
|----------|------|
| `MODE: ESCALATE` | `To: Arif` — always, no exceptions |
| `MODE: BROADCAST` | `CC: Arif` |
| `MODE: HANDOFF` | `CC: Arif, AAA-Group` |
| `MODE: NACK` | `CC: Arif` |
| `MODE: REPLY` (agent → agent) | `CC: Arif` |
| `MODE: DIRECT` to Arif | No CC needed |
| `MODE: DIRECT` to other agent | `CC: Arif` |
| Any agent → Arif (irreversible action) | `MODE: ESCALATE` + `To: Arif` |

---

## 5. Agent FROM Labels

Every agent message MUST declare its canonical identity:

| Agent | FROM Label |
|-------|------------|
| Arif Fazil | `Arif Fazil · Sovereign · Human` |
| Hermes | `Hermes · ASI Execution Peer · arifOS` |
| OpenClaw | `OpenClaw · AGI Coordinator · arifOS` |
| GEOX | `GEOX · Earth Intelligence · arifOS` |
| WEALTH | `WEALTH · Capital Intelligence · arifOS` |
| AAA Gateway | `AAA · Gateway · arifOS` |

---

## 6. Via Field — Handoff Chain Transparency

The `Via:` field is **optional** and only used when the message is clearly mid-chain. It shows the full routing path.

```
Via: Hermes → OpenClaw
Via: AAA-Gateway → Hermes → OpenClaw → GEOX
```

**When to use Via:**
- `MODE: HANDOFF` — always show Via
- `MODE: DIRECT` — show Via if routed through gateway
- `MODE: A2A-system` — show Via as routing metadata
- Other modes — omit Via if message is original

---

## 7. MODE → Behavior Matrix

| MODE | Agent Acts? | HITL Required? | Telegram Post? | A2A Transport? | Next Action |
|------|-----------|----------------|----------------|----------------|-------------|
| `→ DIRECT` | Only to target | If target = Arif | Yes (to recipient) | Yes (private) | Await target response |
| `↩ REPLY` | Yes | No | Yes (thread) | No | Respond in thread |
| `📢 BROADCAST` | No | No | Yes (all) | Optional | None — informational |
| `⟋ HANDOFF` | Forward only | No | Yes | Yes (to next agent) | Await next agent result |
| `⚠ ESCALATE` | **No — PAUSE** | **Always YES** | Yes | Yes (paused) | Wait for Arif APPROVE/REJECT |
| `✅ ACK` | No | No | Yes | No | None — receipt confirmed |
| `❌ NACK` | **No — BLOCK** | Report only | Yes | Yes (rejection) | Log and halt |

### HITL Markings

| HITL Value | Meaning |
|------------|---------|
| `HITL: 👤 Arif required` | Execution pauses until Arif explicitly says APPROVE or REJECT |
| `HITL: 👤 Arif watching` | Arif is CC'd but no action required |
| `HITL: none` | Automated — no human intervention needed |

---

## 8. Telegram Privacy Settings

### Option A — Privacy OFF (Full Ambient Visibility) ⚡ RECOMMENDED

> "I want my bot to see everything complete visibility"

```
BotFather: /setprivacy → Disable
```

- Both Hermes and OpenClaw receive **all human messages** in AAA group
- Agents do NOT receive other bots' messages (Telegram limitation)
- Reaction controlled by **MODE stamp + F1–F13 floors**
- `MODE: ESCALATE` creates deliberate pause before any action
- Clean: Telegram sees everything; A2A handles inter-agent routing

### Option B — Privacy ON (Command-Only)

```
BotFather: /setprivacy → Enable
```

- Bots only receive: slash commands, replies to their messages, @mentions
- Lower noise — but Arif must prefix everything with `/aaa` `/hermes` `/openclaw`
- Higher friction, safer by default

**Arif's stated preference: Option A (Privacy OFF) — full visibility**

---

## 9. Phase Priority — Collaboration Order

Default collaboration sequence for `/aaa <prompt>`:

```
Arif (AAA Group)
    │
    ├── H2A: @ASI_arifos_bot ──→ Hermes (plan/judge)
    │         │
    │         ├── MODE: A2H (Hermes → Arif) ──→ Hermes plan posted to AAA
    │         │     CC: OpenClaw, Arif
    │         │
    │         └── MODE: HANDOFF (Hermes → OpenClaw)
    │              Via: Hermes → OpenClaw
    │              CC: Arif, AAA-Group
    │              │
    ├── A2A: Hermes ──→ OpenClaw (execute)
    │         │
    │         └── MODE: A2A-visible (OpenClaw → Arif)
    │              Via: Hermes → OpenClaw
    │              CC: Arif, AAA-Group
    │
    └── MODE: REPLY (OpenClaw → Arif) ──→ Execution result posted to AAA
```

**Phase order:**
1. **Hermes first** — constitutional framing, plan, F1–F13 check
2. **OpenClaw executes** — code, artifacts, execution trace
3. **Hermes reviews** (optional) — verdict, amendments

**Direct invocation:**
- `/hermes <prompt>` → Hermes only, no OpenClaw
- `/openclaw <prompt>` → OpenClaw only (bypasses Hermes plan), no Hermes review

---

## 10. NACK — Agent-to-Agent Rejection Protocol

NACK is the **back-pressure mechanism**. An agent can reject a request from another agent with a reason.

### NACK Triggers

| Trigger | Example |
|---------|---------|
| Constitutional violation (F1/F8) | "Cannot execute — F1 AMANAH violation: irreversible deletion requested" |
| Capability mismatch | "Cannot execute — this is WEALTH's lane, not GEOX's" |
| Tool unavailability | "Cannot execute — required MCP tool offline" |
| Security/injection detected | "Cannot execute — F12 INJECTION: unsanitized input blocked" |

### NACK Template

```
Mode:    ❌ NACK — Rejected
To:      [Original sender agent]
From:    [Rejecting agent] · [Role] · [Platform]
CC:      Arif
Title:   [One-line rejection reason]
Task:    [Original Task ID]

═══════════════════════════════════════════════
Context:   [What was requested | by whom | when]

Rejection Reason:  [F-level violation | capability mismatch | tool unavailable]
Evidence:  [Exact violation | tool response | log excerpt]
Recommended Alternative:  [What the sender should do instead]
═══════════════════════════════════════════════
Seal:    [Why this was rejected | constitutional basis | confidence]
         [Timestamp: YYYY.MM.DD.NNN]
         REPO: AAA | EPOCH: EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

---

## 11. Worked Examples

### Example 1 — H2A: User to Hermes

```
Mode:    ↩ REPLY — Human to Agent
To:      Hermes
From:    Arif Fazil · Sovereign · Human
CC:      OpenClaw, AAA-Group
Title:   Run GEOX well desk on WELL-123
Task:    aaa-2026-05-04-001

═══════════════════════════════════════════════
Context:   User request in AAA group

Can you run the GEOX well desk analysis on WELL-123?
I want anomalies only, summarized in plain English.
No mutations — read only.

Verdict:  ⚠️ SABAR (pending Hermes plan)
Way Forward:  Hermes will plan → OpenClaw executes → Hermes reviews
Routing Note:  Natural language request, Hermes intercepts for F1-F13 check
═══════════════════════════════════════════════
Seal:    H2A request received | routed to Hermes lane
         [Timestamp: 2026.05.04.001]
         REPO: AAA | EPOCH: EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### Example 2 — A2H: Hermes to Arif (Plan)

```
Mode:    ↩ REPLY — Agent to Human
To:      Arif
From:    Hermes · ASI Execution Peer · arifOS
CC:      OpenClaw, AAA-Group
Title:   GEOX well desk plan approved — handoff to OpenClaw
Task:    aaa-2026-05-04-001

═══════════════════════════════════════════════
Context:   H2A request from Arif → Hermes plan

CONSTITUTIONAL CHECK (F1–F13):
✅ F1 AMANAH: Read-only operation — no irreversible changes
✅ F2 TRUTH: Citing GEOX MCP tools only
✅ F3 WITNESS: Log will be produced for audit
✅ F8 GENIUS: Correctness required ≥ 0.80
⚠️ F7 HUMILITY: Confidence band 0.75–0.90 — external verification recommended

PLAN:
1. Delegate to OpenClaw via A2A
2. OpenClaw calls geox_well_desk(taskId, well=WELL-123, anomalies_only=true)
3. Return plain English summary to Arif

HANDOFF TO: OpenClaw
CONSTRAINTS: Read-only, no mutation, summarize anomalies only
═══════════════════════════════════════════════
Verdict:  ✅ SEAL (plan accepted)
Way Forward:  👤 OpenClaw executing — awaiting result
Routing Note:  Hermes plan complete → OpenClaw execution next
═══════════════════════════════════════════════
Seal:    F1-F13 checked | plan SEALed | handoff to OpenClaw
         Confidence: 0.87
         [Timestamp: 2026.05.04.002]
         REPO: AAA | EPOCH: EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### Example 3 — A2A-visible: Hermes to OpenClaw (Handoff)

```
Mode:    ⟋ HANDOFF — Agent to Agent
To:      OpenClaw
From:    Hermes · ASI Execution Peer · arifOS
Via:     Hermes → OpenClaw
CC:      Arif, AAA-Group
Title:   Execute: GEOX well desk WELL-123 anomalies
Task:    aaa-2026-05-04-001

═══════════════════════════════════════════════
Context:   Arif H2A → Hermes plan → Hermes handoff to OpenClaw

EXECUTE THE FOLLOWING:
- Tool: geox_well_desk
- Params: well=WELL-123, anomalies_only=true
- Output: plain English anomaly summary
- Constraints: Read-only, no mutation

CONSTITUTIONAL CONSTRAINTS APPLIED:
- F1 AMANAH: Read-only only
- F2 TRUTH: Return source evidence for each anomaly
- F7 HUMILITY: Flag confidence < 0.80 per anomaly
═══════════════════════════════════════════════
Verdict:  ⚠️ SABAR (awaiting OpenClaw execution)
Way Forward:  OpenClaw executes → returns result → Hermes reviews
Routing Note:  A2A-system transport | Telegram-visible post for Arif/Group
═══════════════════════════════════════════════
Seal:    Hermes SEALed handoff | OpenClaw tasked | awaiting execution
         Confidence: 0.87
         [Timestamp: 2026.05.04.003]
         REPO: AAA | EPOCH: EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### Example 4 — A2H: OpenClaw to Arif (Execution Result)

```
Mode:    ↩ REPLY — Agent to Human
To:      Arif
From:    OpenClaw · AGI Coordinator · arifOS
Via:     Hermes → OpenClaw
CC:      Hermes, AAA-Group
Title:   WELL-123 anomalies: 3 found, 1 high confidence
Task:    aaa-2026-05-04-001

═══════════════════════════════════════════════
Context:   Hermes handoff → OpenClaw execution → result

EXECUTION COMPLETE: geox_well_desk(well=WELL-123, anomalies_only=true)

RESULTS:
1. 🔴 High confidence anomaly: GR logged below baseline at 1420–1450mMD
   - Confidence: 0.93 | Source: geox_phi_log
2. 🟡 Medium confidence anomaly: Resistivity spike at 1600mMD
   - Confidence: 0.81 | Source: geox_resistivity_log
   - ⚠️ F7 flag: single-tool evidence — recommend WEALTH cross-check
3. 🟢 Low confidence anomaly: porosity trend shift at 1800mMD
   - Confidence: 0.72 | Source: geox_porosity_log
   - ⚠️ F7 flag: below 0.80 threshold

CONSTITUTIONAL COMPLIANCE:
✅ F1: Read-only confirmed
✅ F2: Evidence cited per anomaly
✅ F7: Confidence bands declared, low-confidence flagged
═══════════════════════════════════════════════
Verdict:  ✅ SEAL (execution complete)
Way Forward:  👤 Arif reviews — any follow-up?
Routing Note:  Result delivered | Hermes review pending
═══════════════════════════════════════════════
Seal:    Execution SEALed | 3 anomalies returned | plain English
         Overall confidence: 0.84
         [Timestamp: 2026.05.04.004]
         REPO: AAA | EPOCH: EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### Example 5 — ESCALATE: 888_HOLD Required

```
Mode:    ⚠ ESCALATE — Human Decision Required
To:      Arif
From:    Hermes · ASI Execution Peer · arifOS
CC:      OpenClaw, AAA-Group
Title:   888_HOLD: WEALTH requests irreversible portfolio rebalance
Task:    aaa-2026-05-04-002

═══════════════════════════════════════════════
Context:   WEALTH tool wealth_portfolio_rebalance flagged for review

REQUEST DETECTED:
- Tool: wealth_portfolio_rebalance
- Scope: 3 of 7 asset classes
- Estimated impact: $2.4M position change
- Irreversible: YES — settlement cannot be undone

CONSTITUTIONAL ANALYSIS:
⚠️ F1 AMANAH: Irreversible operation requested
✅ F6 EMPATHY: Impact assessed on 3 client portfolios
✅ F13 SOVEREIGN: Human veto is absolute on irreversible ops

888_HOLD TRIGGERED:
- This operation cannot proceed without Arif's explicit APPROVE
═══════════════════════════════════════════════
Verdict:  ⚠️ SABAR (paused — awaiting Arif decision)
Way Forward:  👤 Arif must reply APPROVE or REJECT
Routing Note:  ESCALATE always → To: Arif | Execution PAUSED
═══════════════════════════════════════════════
Seal:    888_HOLD enforced | F1 AMANAH: irreversible ops require sovereign consent
         Confidence: 1.00 (protocol-level requirement)
         [Timestamp: 2026.05.04.005]
         REPO: AAA | EPOCH: EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

---

## 12. Slash Commands Reference

| Command | Handler | Behavior |
|---------|---------|----------|
| `/aaa <prompt>` | Hermes | Full collaboration: Hermes plan → OpenClaw exec → Hermes review |
| `/hermes <prompt>` | Hermes only | Hermes responds solo — no OpenClaw |
| `/openclaw <prompt>` | OpenClaw only | OpenClaw responds solo — bypasses Hermes plan |
| `/status` | Both | Broadcast health status — MODE: BROADCAST |
| `/help` | Both | Broadcast command reference — MODE: BROADCAST |

---

## 13. Governance Rules Summary

1. **Every bot message** MUST include: FROM, TO, CC, MODE, Title, Task, Seal, DITEMPA footer
2. **Every agent-directed message** MUST be classified: question / instruction / status / result / verdict / hold
3. **MODE: ESCALATE** always pauses execution — no exceptions
4. **888_HOLD** is hard-coded: irreversible actions always escalate to Arif
5. **Anti-loop rule**: no agent may trigger another agent more than 2 hops without human ACK
6. **Every A2A message** carries original `human_request_id` and `Task` for auditability
7. **Visibility ≠ Reactivity**: privacy OFF means agents see all, not that they act on all

---

## 14. What Needs to Be Configured

### Immediately Required

| Item | Owner | Status |
|------|-------|--------|
| Privacy OFF on both bots (BotFather) | Arif | ⚠️ Pending |
| Both bots added to AAA group | Arif | ⚠️ Pending |
| Slash command dispatch: `/aaa` → Hermes, `/openclaw` → OpenClaw | Gateway | ⚠️ Pending |
| Hermes Nous OAuth or MCP bridge for A2A | Hermes/OpenClaw | ⚠️ Pending |

### Protocol Updates Needed

| Item | File | Action |
|------|------|--------|
| Hermes system prompt | SOUL.md / AGENTS.md | Update with RFC template |
| OpenClaw system prompt | OpenClaw config | Update with RFC template |
| AAA Conductor (gateway) | a2a-gateway compose | Update to emit RFC headers |
| ADR-010 update | ADR/ADR-010-AAA-TELEGRAM-VISIBILITY.md | Supersede with this RFC |

---

## 15. Ratification Checklist

Arif — please confirm each:

- [ ] **1.** 7-mode system confirmed? (`→ ↩ 📢 ⟋ ⚠ ✅ ❌`)
- [ ] **2.** Via field added as optional header for handoff chains?
- [ ] **3.** NACK mode retained for agent-to-agent rejection?
- [ ] **4.** Privacy OFF (full ambient visibility) — confirmed?
- [ ] **5.** Hermes-first phase priority (OpenClaw direct only on `/openclaw`)?
- [ ] **6.** Telegram template format accepted (exact field ordering)?
- [ ] **7.** CC rules accepted?
- [ ] **8.** Slash commands: `/aaa`, `/hermes`, `/openclaw`, `/status`, `/help`?

---

## 16. Relation to Existing ADR-010

This RFC **supersedes** ADR-010-AAA-TELEGRAM-VISIBILITY in full. Key changes:

| ADR-010 | RFC |
|---------|-----|
| Privacy ON (command-only) | Privacy OFF (full ambient) |
| Hermes + OpenClaw both needed for `/aaa` | Same, but MODE stamps visible |
| No formal message template | Full RFC template with headers/footers |
| No NACK protocol | NACK protocol defined |
| No CC rules | CC rules formalized |

---

*Ditempa Bukan Diberi — Intelligence is forged, not given.*

**REPO:** AAA
**EPOCH:** EPOCH-2026-05-04
**SEAL:** DRAFT — Pending Arif Ratification
