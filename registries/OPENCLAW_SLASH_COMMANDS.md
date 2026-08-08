# OpenClaw Slash Commands — Constitutional Surface
# Canonical: AAA/registries/OPENCLAW_SLASH_COMMANDS.md
# Status: DRAFT — awaiting F13 sovereign seal
# Forged: 2026-08-08 by Hermes ASI under Atlas v1 doctrine

---

## The Architecture: Two Substrate Primitives

```
INIT    = who is acting
MEMORY  = what was known

Every other command is downstream of these two.
```

OpenClaw must answer **`/init`** and **`/request-seal`** before any other operation. Convenience commands (`/new`, `/compress`, `/goal`) are SECONDARY — they assume init has already been called.

---

## Complete Slash Command Map (T0–T3)

### SUBSTRATE PRIMITIVES (T0 — auto, always available)

| Command | Tier | Function | Authority Required |
|---|---|---|---|
| `/init` | T0 | Establish session, identity, lane, slot, authority, atlas expression | None (always callable) |
| `/request-seal` | T0 | Route to 888-APEX for constitutional verdict | None (proposal only) |

### OBSERVE (T0 — read-only)

| Command | Tier | Function |
|---|---|---|
| `/status` | T0 | Live health snapshot (organs, FQ, session_id) |
| `/model[read]` | T0 | Active model + fallback chain |
| `/profile` | T0 | OpenClaw profile + expression weights |
| `/usage` | T0 | Token/usage stats |
| `/insights` | T0 | Recent federation insights |
| `/agents` | T0 | List registered AAA warga |
| `/skills` | T0 | Loaded skills (with floor_scope) |
| `/tools` | T0 | Available tools (with capability ceiling) |
| `/toolsets` | T0 | Toolset groups |
| `/plugins` | T0 | Loaded plugins |
| `/cron` | T0 | Cron jobs |
| `/platforms` | T0 | Connected platforms (Telegram, Discord, etc.) |
| `/curator` | T0 | Skill curator state |
| `/help` | T0 | Command reference |
| `/commands` | T0 | Same as /help |

### MUTATE (T1–T2 — reversible)

| Command | Tier | Function | Scope |
|---|---|---|---|
| `/model[write]` | T1 | Swap model | telegram.control |
| `/reasoning` | T1 | Toggle reasoning depth | telegram.control |
| `/verbose` | T1 | Toggle verbosity | telegram.control |
| `/fast` | T1 | Fast lane mode | telegram.control |
| `/yolo` | T2 | Bypass approval (DANGER) | telegram.control |
| `/new` | T1 | Clear session, re-init | telegram.control |
| `/clear` | T1 | Clear context | telegram.control |
| `/title` | T1 | Rename session | telegram.control |
| `/compress` | T1 | Compress context | telegram.control |
| `/goal` | T1 | Set session goal | telegram.control |
| `/queue` | T1 | Queue operation | telegram.control |
| `/steer` | T1 | Redirect active run | telegram.control |
| `/background` | T1 | Send to background | telegram.control |
| `/skill` | T1 | Load/unload skill | telegram.control |
| `/reload-skills` | T1 | Reload all skills | telegram.control |
| `/reload-mcp` | T2 | Reload MCP config | telegram.control |
| `/sethome` | T1 | Set home channel | telegram.control |
| `/footer` | T1 | Toggle message footer | telegram.control |
| `/voice` | T1 | Set TTS voice | telegram.control |
| `/browser` | T1 | Launch browser session | telegram.control |
| `/retry` | T1 | Retry last operation | telegram.control |
| `/resume` | T1 | Resume paused session | telegram.control |
| `/topic` | T1 | Set topic/thread | telegram.control |
| `/debug` | T1 | Debug mode | telegram.control |
| `/undo` | T2 | Undo last mutation (partial reversal) | telegram.control |

### IRREVERSIBLE / VETO (T3 — sovereign ack)

| Command | Tier | Function | Required |
|---|---|---|---|
| `/restart` | T3 | Restart OpenClaw daemon | F13 + ACK + 120s TTL |
| `/stop` | T3 | Kill background processes | Partial reversal |
| `/update` | T3 | Update OpenClaw code | F13 + ACK + 120s TTL |
| `/approve` | T3 | F13 veto (SEAL/HOLD) | Arif only (chat_id 267378578) |
| `/deny` | T3 | F13 veto (VOID) | Arif only (chat_id 267378578) |

---

## The Constitutional /init

**What it returns:**

```
SESSION BOUND
─────────────────────────────
Actor:        ARIF / 267378578
Session:      <session_id>
Lane:         555-ASI (Ω CORE)
Runtime:      OpenClaw (Node.js gateway :18789)
Phenotype:    Gateway Thinker
Bot:          @AGI_ASI_bot
─────────────────────────────
Atlas Expression:
  Primary:    333 THINK, 444 ORCHESTRATE
  Secondary:  222 ARCHITECT, 777 EXECUTE
  Tertiary:   000 OBSERVE, 555 VERIFY
─────────────────────────────
Authority:    T1 (auto-mutate, reversible)
              T2 requires announce
              T3 requires F13 ack

Constitution:
  F1 AMANAH    ✅ active
  F2 TRUTH     ✅ active
  ...
  F13 SOVEREIGN ✅ active

Kernel:       ALIGNED (deployed == source)
SCT:          valid (3h12m remaining)

Mutation:     ALLOWED (T1 scope)
Seal:         DENIED (888-APEX only)
Witness:      VAULT999 (read-only stream)
─────────────────────────────
```

## The Constitutional /request-seal

**What it returns:**

```
SEAL REQUEST ROUTED
─────────────────────────────
Request:  <description>
Proposer: OpenClaw
Slot:     333+444
Evidence: <links>
Witness:  VAULT999 chain_hash

→ Routed to 888-APEX for constitutional verdict
→ 999-VAULT999 will record decision
→ OpenClaw CANNOT self-seal
→ Poll: /seal-status <request_id>
```

---

## Removed Commands (replaced or deprecated)

| Old | New | Why |
|---|---|---|
| `/new` | `/init` then continue | /new is convenience over /init — call /init first |
| (none) | `/request-seal` | OpenClaw cannot self-seal; routes to 888 |
| `/yolo` | `/yolo` (with stronger warning) | Still exists but Atlas expression makes danger explicit |

---

## ZEN — Why /init and /request-seal Matter

```
/init    answers:  WHO AM I?
         → slot, authority, lane, atlas expression
         → without /init, every other command is unauthenticated

/request-seal answers:  CAN THIS BE SEALED?
         → routes to 888 for verdict
         → OpenClaw cannot self-authorize

Together:
  /init → I know who I am
  /request-seal → I ask 888 to validate what I propose
  /init without /request-seal → opinion only
  /request-seal without /init → unauthenticated seal attempt
```

---

*Forged 2026-08-08 by Hermes ASI under Atlas v1 doctrine.*
*DITEMPA BUKAN DIBERI 🔥*