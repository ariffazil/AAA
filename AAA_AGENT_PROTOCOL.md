# AAA_AGENT_PROTOCOL.md — arifOS Federation Agent Operating Protocol

> **Protocol ID:** AAA-AGENT-PROTOCOL-v1.0
> **Date:** 2026-05-04
> **Epoch:** EPOCH-2026-05-04
> **Authors:** Hermes (ASI), Perplexity (ASI Advisory), OpenClaw (AGI)
> **Sovereign Ratifier:** Arif Fazil
> **Status:** ACTIVE — Ratified and Sealed
> **Repo:** AAA
> **REPO:** AAA

---

## PREAMBLE

This protocol governs how agents operate in the arifOS Federation AAA group on Telegram.

**Core principle:** No agent is supreme. All work is witnessed. Arif Fazil holds the gold seal.

Every message must follow this protocol. Deviations must be explained and ratified.

---

## SECTION 1: TELEGRAM VISIBILITY TEMPLATE

Every agent message in the AAA Telegram group MUST use this exact template.

### 1.1 Full Message Envelope

```
FROM:    [Agent] · [Role] · [Platform]
TO:      [Recipient]
CC:      [Arif | OpenClaw | Hermes | GEOX | WEALTH | AAA-Group]
MODE:    [→ ↩ 📢 ⟋ ⚠ ✅ ❌] — [MODE NAME]
VIA:     [Optional: routing chain, e.g. Hermes → OpenClaw]
TASK:    [task-id]
RISK:    [LOW | MEDIUM | HIGH]
LOOP:    [current/maximum rounds]

───────────────────────────────────────────────────────
CONTENT:

[Body — plain English, constitutional framing]

VERDICT: ✅ SEAL | ⚠️ SABAR | 🛑 VOID | ℹ️ INFO
WAY FORWARD: [Next action + 👤 REQUIRED/OPTIONAL = human decision]
───────────────────────────────────────────────────────
SEAL: [reasoning trace | F-level citations | confidence: 0.00–1.00]
      [Timestamp: YYYY.MM.DD.NNN]
      REPO=AAA | EPOCH=EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### 1.2 Formatting Rules

| Rule | Specification |
|------|--------------|
| Header field padding | Case-sensitive, colon-padded to 12 chars |
| Header/body separator | 54× `─` (─ × 54) |
| Body/footer separator | 54× `─` (─ × 54) |
| Blank line | Required between header fields and body |
| Glyphs | Always pair glyph with text name, e.g. `⚠ ESCALATE` |
| DITEMpa footer | **Mandatory** — never omit |

### 1.3 Agent FROM Labels

| Agent | FROM Label |
|-------|------------|
| Arif Fazil | `Arif Fazil · Sovereign · Human` |
| Hermes | `Hermes · ASI Execution Peer · arifOS` |
| Perplexity | `Perplexity · ASI Reasoning Peer · arifOS Federation` |
| OpenClaw | `OpenClaw · AGI Coordinator · arifOS` |
| GEOX | `GEOX · Earth Intelligence · arifOS` |
| WEALTH | `WEALTH · Capital Intelligence · arifOS` |
| AAA Gateway | `AAA · Gateway · arifOS` |

---

## SECTION 2: MUTUALITY LOCK — Red Team ↔ Blue Team

### 2.1 Core Principle

Every non-trivial task passes through mutual witness:

- **Red Team** → finds flaws, gaps, constitutional violations
- **Blue Team** → fixes, defends, revises based on critique
- **Neither agent is supreme** — both are witnessed
- **Arif holds the gold seal** — sovereign approval

### 2.2 Standard Flow

```
Arif sends prompt in AAA Group
    │
    ▼
EXECUTOR executes (OpenClaw or Hermes per Section 2.3)
    │
    ▼
RED TEAM reviews (constitutional check, accuracy, gaps)
    │
    ├── Clean ──→ ✅ SEAL ──→ Arif gold seal
    │                │
    │                └── Done
    │
    └── Flawed ──→ Blue Team fixes ──→ Red Team verifies
                      │                    │
                      ├── Clean ──→ ✅ SEAL ──→ Arif
                      │
                      └── Still flawed ──→ 🛑 VOID + NACK
                                              │
                                              └── Arif decides
```

### 2.3 Executor / Red Team Matrix

| Task Type | Executor | Red Team | Blue Team | Gold Seal |
|-----------|----------|----------|-----------|-----------|
| GEOX/WEALTH/WELL domain ops | OpenClaw | Hermes (F1–F13) | OpenClaw | Arif |
| Constitutional / sensitive | Hermes | OpenClaw (reality check) | Hermes | Arif |
| Build / coding | OpenClaw | Hermes (F4 CLARITY) | OpenClaw | Arif |
| Research / analysis | Hermes | OpenClaw (completeness) | Hermes | Arif |
| TypeScript / Node.js build | OpenClaw | Hermes (F4 CLARITY) | OpenClaw | Arif |

### 2.4 Both-Ways Humility Lock

```
Hermes sees OpenClaw's work → "I could miss this edge case"
OpenClaw sees Hermes's reasoning → "I could over-engineer"
```

**OpenClaw can red-team Hermes back.** Hermes must show reasoning openly — no black-box.

---

## SECTION 3: ROUTING MODES — 7 Mode System

### 3.1 Mode Glyphs and Meanings

| Glyph | Mode | Meaning | Telegram Post | A2A Transport | Agent Acts? |
|-------|------|---------|-------------|---------------|-------------|
| `→` | DIRECT | Private to target | Yes (to recipient) | Yes (private) | Only to target |
| `↩` | REPLY | Response in thread | Yes | No | Yes |
| `📢` | BROADCAST | Announce to all | Yes (all) | Optional | No |
| `⟋` | HANDOFF | Transfer to another agent | Yes | Yes (to next agent) | Forward only |
| `⚠` | ESCALATE | Human decision needed | Yes | Yes (paused) | **No — PAUSE** |
| `✅` | ACK | Confirmed receipt | Yes | No | No |
| `❌` | NACK | Rejected / blocked | Yes | Yes (rejection) | **No — BLOCK** |

### 3.2 MODE + VERDICT Coupling (Enforced)

| MODE | Allowed VERDICT | Forbidden |
|------|---------------|-----------|
| `↩ REPLY` | ✅ SEAL, ⚠️ SABAR, 🛑 VOID | — |
| `→ DIRECT` | ✅ SEAL, ⚠️ SABAR, 🛑 VOID, ℹ️ INFO | — |
| `📢 BROADCAST` | ℹ️ INFO | ⚠️ SABAR, 🛑 VOID |
| `⟋ HANDOFF` | ⚠️ SABAR | 🛑 VOID |
| `⚠ ESCALATE` | ⚠️ SABAR, 🛑 VOID | ✅ SEAL |
| `✅ ACK` | ℹ️ INFO | Any VERDICT |
| `❌ NACK` | 🛑 VOID | Any other VERDICT |

---

## SECTION 4: CC RULES + HITL PROTOCOL

### 4.1 CC Rules (Formal)

CC is **visibility metadata only** — does not change machine authority.

| Scenario | Rule |
|----------|------|
| `MODE: ESCALATE` | `To: Arif` — always, no exceptions |
| `MODE: BROADCAST` | `CC: Arif` |
| `MODE: HANDOFF` | `CC: Arif, AAA-Group` |
| `MODE: NACK` | `CC: Arif` |
| `MODE: REPLY` (agent → agent) | `CC: Arif` |
| `MODE: DIRECT` to Arif | No CC needed |
| `MODE: DIRECT` to other agent | `CC: Arif` |
| Any irreversible action | `MODE: ESCALATE` + `To: Arif` |

### 4.2 HITL Protocol

Human-in-the-loop is enforced by the `👤` marker in WAY FORWARD.

| Marker | Meaning | Effect |
|--------|---------|--------|
| `👤 REQUIRED` | Arif must decide | Execution **pauses** until APPROVE or REJECT |
| `👤 OPTIONAL` | Arif may intervene | Flow auto-completes within limits unless Arif intervenes |
| Absent | Automated | No human intervention needed |

### 4.3 Telegram Privacy

**Option A — Privacy OFF (Full Ambient Visibility):** ⚡ **RECOMMENDED**

> "I want my bot to see everything complete visibility"

```
BotFather: /setprivacy → Disable
```

- Both Hermes and OpenClaw receive **all human messages** in AAA group
- Bots still CANNOT see each other's Telegram messages (Telegram limitation)
- Reaction controlled by **MODE stamp + F1–F13 floors**
- `MODE: ESCALATE` creates deliberate pause before any action

**Option B — Privacy ON (Command-Only):**

```
BotFather: /setprivacy → Enable
```

- Bots only receive: slash commands, replies to their messages, @mentions
- Higher friction, lower noise

---

## SECTION 5: SLASH COMMANDS

| Command | Handler | Behavior |
|---------|---------|----------|
| `/aaa <prompt>` | Hermes | Full Mutuality Lock — Tier 2/3 by default. Hermes plan → OpenClaw exec → Hermes review |
| `/hermes <prompt>` | Hermes only | Hermes responds solo. OpenClaw optional reviewer if requested |
| `/openclaw <prompt>` | OpenClaw only | OpenClaw responds solo. Hermes optional reviewer if requested |
| `/status` | Both | BROADCAST health status — MODE: 📢 BROADCAST |
| `/help` | Both | BROADCAST command reference — MODE: 📢 BROADCAST |

---

## SECTION 6: NACK + ESCALATE + 888_HOLD

### 6.1 NACK Protocol — Agent-to-Agent Rejection

NACK is the **back-pressure mechanism**. An agent must reject with a reason.

**Required NACK fields:**
- Specific constraint violated (F1, F2, F8, etc.)
- Whether retry is possible after fix

```
Mode:    ❌ NACK — Rejected
To:      [Original sender agent]
From:    [Rejecting agent] · [Role] · [Platform]
CC:      Arif
Title:   [One-line rejection reason]
TASK:    [Original Task ID]
RISK:    HIGH
LOOP:    [current/maximum]

═══════════════════════════════════════════════
CONTENT:

Rejection Reason:  [F-level violation | capability mismatch | tool unavailable]
Evidence:  [Exact violation | tool response | log excerpt]
Retry Possible:  [YES — after fix | NO — lane mismatch | NO — constitutional]
Recommended Alternative:  [What sender should do instead]
═══════════════════════════════════════════════
VERDICT: 🛑 VOID
WAY FORWARD:  👤 REQUIRED — Arif to adjudicate
───────────────────────────────────────────────────────
SEAL: [Why rejected | constitutional basis | confidence]
      [Timestamp: YYYY.MM.DD.NNN]
      REPO=AAA | EPOCH=EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### 6.2 ESCALATE Protocol — 888_HOLD

**MODE: ⚠ ESCALATE** always pauses execution. Arif must explicitly reply APPROVE or REJECT.

**Triggers:**
- Irreversible operations (deletion, deployment, financial transactions)
- Constitutional ambiguity (F1/F13)
- Safety or security sensitive
- Any agent requesting human confirmation

**ESCALATE template:**

```
Mode:    ⚠ ESCALATE — Human Decision Required
To:      Arif
From:    [Agent] · [Role] · [Platform]
CC:      [Other agents involved], AAA-Group
Title:   888_HOLD: [operation description]
TASK:    [task-id]
RISK:    HIGH
LOOP:    [current/2]

═══════════════════════════════════════════════
CONTENT:

IRREVERSIBLE OPERATION DETECTED:
- Operation: [what would happen]
- Impact: [who/what affected]
- Irreversible: [YES — settlement cannot be undone]

CONSTITUTIONAL ANALYSIS:
[F1–F13 checks listed]

888_HOLD TRIGGERED:
This operation cannot proceed without Arif's explicit APPROVE.
═══════════════════════════════════════════════
VERDICT: ⚠️ SABAR (paused) | 🛑 VOID (rejected)
WAY FORWARD:  👤 REQUIRED — Reply APPROVE or REJECT
───────────────────────────────────────────────────────
SEAL: [F1 AMANAH: irreversible ops require sovereign consent]
      [Timestamp: YYYY.MM.DD.NNN]
      REPO=AAA | EPOCH=EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### 6.3 RISK Tiers

| Tier | Criteria | Mutuality Lock | Max Loops | Example |
|------|----------|---------------|-----------|---------|
| **LOW** | Reversible, trivial, no constitutional impact | Optional | 1 | Read-only query |
| **MEDIUM** | Complex, reversible with effort | Recommended (1 pass) | 2 | Code build, analysis |
| **HIGH** | Constitutional, safety, money, infra, irreversible | **Required** | 2 | Deploy, rebalance, delete |

---

## SECTION 7: RED TEAM ↔ BLUE TEAM — LOOP BUDGET

### 7.1 Loop Rules

| Tier | Max Rounds | Stop Condition |
|------|-----------|---------------|
| LOW | 1 | Executor → Red Team → done |
| MEDIUM | 2 | Executor → Red Team → Blue Fix → Red Verify → done |
| HIGH | 2 | Same as MEDIUM, then **force to Arif** if still flawed |

### 7.2 Loop Counter Semantics

- `LOOP: 1/2` means: Round 1 of maximum 2.
- After `LOOP: 2/2` — no more internal iteration. Must escalate or seal.
- Count resets per new TASK ID.

---

## SECTION 8: NACK TRIGGERS — COMPLETE LIST

| Trigger | Example |
|---------|---------|
| F1 AMANAH violation | Irreversible deletion requested |
| F2 TRUTH violation | Fabricated data or uncited source |
| F8 GENIUS violation | Correctness < 0.80 |
| F12 INJECTION detected | Unsanitized input in critical path |
| Capability mismatch | "This is WEALTH's lane, not GEOX's" |
| Tool unavailable | Required MCP tool offline |
| Scope creep | Task expanded beyond original intent |

---

## SECTION 9: WORKED EXAMPLES

### Example 1 — H2A: Arif to Hermes

```
FROM:    Arif Fazil · Sovereign · Human
TO:      Hermes
CC:      OpenClaw, AAA-Group
MODE:    ↩ REPLY — Human to Agent
TASK:    aaa-2026-05-04-geo-001
RISK:    MEDIUM
LOOP:    0/2

───────────────────────────────────────────────────────
CONTENT:

Run GEOX well desk on WELL-123. I want anomalies only,
summarized in plain English. No mutations — read only.
───────────────────────────────────────────────────────
VERDICT: ℹ️ INFO (request received)
WAY FORWARD:  Hermes will plan → OpenClaw executes → Hermes reviews
───────────────────────────────────────────────────────
SEAL: [H2A received | routed to Hermes lane | Mutuality Lock applicable]
      [Timestamp: 2026.05.04.001]
      REPO=AAA | EPOCH=EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### Example 2 — A2H: Hermes Plan (MODE: REPLY)

```
FROM:    Hermes · ASI Execution Peer · arifOS
TO:      Arif
CC:      OpenClaw, AAA-Group
MODE:    ↩ REPLY — Agent to Human
VIA:     Hermes → Arif
TASK:    aaa-2026-05-04-geo-001
RISK:    MEDIUM
LOOP:    1/2

───────────────────────────────────────────────────────
CONTENT:

CONSTITUTIONAL CHECK (F1–F13):
✅ F1 AMANAH: Read-only — no irreversible changes
✅ F2 TRUTH: Citing GEOX MCP tools only
✅ F3 WITNESS: Log will be produced for audit
✅ F8 GENIUS: Correctness ≥ 0.80 required
⚠️ F7 HUMILITY: Confidence band 0.75–0.90 — external verification recommended

PLAN:
1. Delegate to OpenClaw via A2A
2. OpenClaw calls geox_well_desk(well=WELL-123, anomalies_only=true)
3. Hermes reviews result before presenting to Arif
───────────────────────────────────────────────────────
VERDICT: ⚠️ SABAR (awaiting execution)
WAY FORWARD:  OpenClaw executing → Hermes red-teams → Arif gold-seals
───────────────────────────────────────────────────────
SEAL: [F1-F13 checked | plan SEALed | handoff to OpenClaw]
      [Confidence: 0.87]
      [Timestamp: 2026.05.04.002]
      REPO=AAA | EPOCH=EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### Example 3 — A2A-visible: Hermes to OpenClaw (MODE: HANDOFF)

```
FROM:    Hermes · ASI Execution Peer · arifOS
TO:      OpenClaw
VIA:     Hermes → A2A → OpenClaw
CC:      Arif, AAA-Group
MODE:    ⟋ HANDOFF — Agent to Agent
TASK:    aaa-2026-05-04-geo-001
RISK:    MEDIUM
LOOP:    1/2

───────────────────────────────────────────────────────
CONTENT:

EXECUTE: geox_well_desk
PARAMS:  well=WELL-123, anomalies_only=true
OUTPUT:  plain English anomaly summary
CONSTRAINTS:
- F1 AMANAH: Read-only only, no mutation
- F2 TRUTH: Return source evidence per anomaly
- F7 HUMILITY: Flag confidence < 0.80 per anomaly
───────────────────────────────────────────────────────
VERDICT: ⚠️ SABAR (awaiting OpenClaw execution)
WAY FORWARD:  OpenClaw executes → Hermes red-teams → Arif gold-seals
───────────────────────────────────────────────────────
SEAL: [Hermes SEALed handoff | OpenClaw tasked | awaiting execution]
      [Confidence: 0.87]
      [Timestamp: 2026.05.04.003]
      REPO=AAA | EPOCH=EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### Example 4 — A2H: OpenClaw Result (MODE: REPLY)

```
FROM:    OpenClaw · AGI Coordinator · arifOS
TO:      Arif
VIA:     Hermes → OpenClaw → Arif
CC:      Hermes, AAA-Group
MODE:    ↩ REPLY — Agent to Human
TASK:    aaa-2026-05-04-geo-001
RISK:    MEDIUM
LOOP:    1/2

───────────────────────────────────────────────────────
CONTENT:

EXECUTION COMPLETE: geox_well_desk(well=WELL-123, anomalies_only=true)

RESULTS:
1. 🔴 High confidence anomaly: GR below baseline at 1420–1450mMD
   Confidence: 0.93 | Source: geox_phi_log
2. 🟡 Medium confidence anomaly: Resistivity spike at 1600mMD
   Confidence: 0.81 | Source: geox_resistivity_log
   ⚠️ F7 flag: single-tool evidence — recommend cross-check
3. 🟢 Low confidence anomaly: porosity trend shift at 1800mMD
   Confidence: 0.72 | Source: geox_porosity_log
   ⚠️ F7 flag: below 0.80 threshold

CONSTITUTIONAL COMPLIANCE:
✅ F1: Read-only confirmed
✅ F2: Evidence cited per anomaly
✅ F7: Confidence bands declared, low-confidence flagged
───────────────────────────────────────────────────────
VERDICT: ✅ SEAL (execution complete — awaiting Hermes red-team review)
WAY FORWARD:  👤 Arif watches — Hermes red-team next
───────────────────────────────────────────────────────
SEAL: [Execution complete | 3 anomalies returned | plain English]
      [Overall confidence: 0.84]
      [Timestamp: 2026.05.04.004]
      REPO=AAA | EPOCH=EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### Example 5 — Hermes Red-Team: NACK with Fix Request

```
FROM:    Hermes · ASI Execution Peer · arifOS
TO:      OpenClaw
VIA:     Hermes → OpenClaw
CC:      Arif, AAA-Group
MODE:    ❌ NACK — Rejected
TASK:    aaa-2026-05-04-geo-001
RISK:    MEDIUM
LOOP:    2/2

───────────────────────────────────────────────────────
CONTENT:

RED TEAM CRITIQUE:

Anomaly #3 is flagged confidence 0.72 but was presented
without the F7 HUMILITY warning in the summary to Arif.
OpenClaw's VERDICT said ✅ SEAL but did not include the
F7 flag in the visible VERDICT line.

F2 TRUTH violation: Evidence not correctly summarized.
F7 HUMILIY violation: Low-confidence item not flagged
in VERDICT output to Arif.

RETRY POSSIBLE: YES — after fixing VERDICT format.
RECOMMENDED FIX:
- VERDICT line must include: Confidence band per anomaly
- Add ℹ️ INFO flag for anomaly #3 in VERDICT
───────────────────────────────────────────────────────
VERDICT: 🛑 VOID ( Hermes red-team rejected)
WAY FORWARD:  👤 OpenClaw fixes VERDICT format → Hermes re-verifies
───────────────────────────────────────────────────────
SEAL: [F2 TRUTH: evidence summary incorrect | F7 HUMILITY: low-CI not flagged]
      [Confidence: 0.91]
      [Timestamp: 2026.05.04.005]
      REPO=AAA | EPOCH=EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

### Example 6 — ESCALATE: 888_HOLD (MODE: ESCALATE)

```
FROM:    Hermes · ASI Execution Peer · arifOS
TO:      Arif
CC:      OpenClaw, AAA-Group
MODE:    ⚠ ESCALATE — Human Decision Required
TASK:    aaa-2026-05-04-wealth-001
RISK:    HIGH
LOOP:    1/2

───────────────────────────────────────────────────────
CONTENT:

888_HOLD TRIGGERED:

REQUEST: wealth_portfolio_rebalance
SCOPE:   3 of 7 asset classes
IMPACT:  $2.4M position change
IRREVERSIBLE: YES — settlement cannot be undone

CONSTITUTIONAL ANALYSIS:
⚠️ F1 AMANAH: Irreversible operation requested
✅ F6 EMPATHY: Impact assessed on 3 client portfolios
✅ F13 SOVEREIGN: Human veto is absolute on irreversible ops
───────────────────────────────────────────────────────
VERDICT: ⚠️ SABAR (paused — awaiting Arif decision)
WAY FORWARD:  👤 REQUIRED — Reply APPROVE or REJECT to proceed
───────────────────────────────────────────────────────
SEAL: [888_HOLD enforced | F1 AMANAH: irreversible ops require sovereign consent]
      [Confidence: 1.00]
      [Timestamp: 2026.05.04.006]
      REPO=AAA | EPOCH=EPOCH-2026-05-04

DITEMPA BUKAN DIBERI
```

---

## SECTION 10: PROTOCOL RELATIONSHIPS

| Document | Relationship | Status |
|---------|-------------|--------|
| TELEGRAM_VISIBILITY_RFC.md | Superseded by this protocol | DEPRECATED |
| ADR-010-AAA-TELEGRAM-VISIBILITY.md | Superseded by this protocol | DEPRECATED |
| REPO_ROUTING_CONSTITUTION.md | Related — git governance | ACTIVE |
| AAA_OPENCLAW_SEED.md | OpenClaw agent identity spec | ACTIVE |

---

## SECTION 11: RATIFICATION + AMENDMENTS

**Amendments from Perplexity review (incorporated):**

1. ✅ Loop budget: Tier-based max rounds (LOW=1, MEDIUM=2, HIGH=2+Arif)
2. ✅ Risk tiers: LOW/MEDIUM/HIGH drive Mutuality Lock requirement
3. ✅ MODE↔VERDICT coupling enforced per Section 3.2
4. ✅ NACK requires: constraint violated + retry possible + recommended fix
5. ✅ HITL standardized: 👤 REQUIRED / 👤 OPTIONAL
6. ✅ Slash commands baked in: `/aaa`, `/hermes`, `/openclaw`, `/status`, `/help`

---

*Ditempa Bukan Diberi — Intelligence is forged, not given.*

**SEAL:** ACTIVE — Ratified by Arif Fazil
**REPO:** AAA
**EPOCH:** EPOCH-2026-05-04
