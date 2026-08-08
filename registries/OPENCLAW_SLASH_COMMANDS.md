# OpenClaw Slash Commands — Constitutional Surface
# Canonical: AAA/registries/OPENCLAW_SLASH_COMMANDS.md
# Status: DRAFT — awaiting F13 sovereign seal
# Forged: 2026-08-08 by Hermes ASI under Atlas v1 doctrine

---

## The Architecture: Two Substrate Primitives + One Execute Gate

```
INIT      = who is acting        (T0, always callable)
MEMORY    = what was known       (T0, substrate)
FORGE     = 777 EXECUTE gate     (T0 observe | T1+ mutate requires SEAL)
REQUEST-SEAL = propose → 888 judge → 999 seal  (T0, proposal only)

Every mutation command is downstream of /forge. Every seal command is
downstream of /request-seal. /init is required before either.
```

OpenClaw must answer **`/init`** and **`/request-seal`** before any other
operation. `/forge` is the execution surface — observe free, mutate gated.
Convenience commands (`/new`, `/compress`, `/goal`) are SECONDARY — they
assume init has already been called.

---

## Complete Slash Command Map (T0–T3)

### SUBSTRATE PRIMITIVES (T0 — auto, always available)

| Command | Tier | Function | Authority Required |
|---|---|---|---|
| `/init` | T0 | Establish session, identity, lane, slot, authority, atlas expression | None (always callable) |
| `/request-seal` | T0 | Route to 888-APEX for constitutional verdict | None (proposal only) |
| `/forge` | T0 (observe) / T1+ (mutate) | 777 EXECUTE gate — subcommands init/probe/status/judge/execute | Observe: none · Mutate: cc_id from SEAL |

### FORGE SUBCOMMANDS (gate per subcommand)

| Sub | Tier | Class | Auth | Routes to |
|---|---|---|---|---|
| `/forge init` | T0 | OBSERVE | None | `forge_session_init` → arifOS |
| `/forge probe` | T0 | OBSERVE | None | dry-run only |
| `/forge status` | T0 | OBSERVE | None | `forge_lease` status + health |
| `/forge judge` | T0 | OBSERVE | None | `forge_heart_critique` (pre-check) |
| `/forge execute` | T1–T2 | MUTATE | **cc_id from /request-seal SEAL** | `forge_execute` |
| `/forge sealed` | T2 | MUTATE | **stage_id + F13 human_seal_token** | `forge_execute_sealed` (FAILS HARD otherwise) |

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
Authority:
  T1 (auto-mutate, reversible)
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

---

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

## The Constitutional /forge

**What it returns (per subcommand):**

```
FORGE SURFACE
─────────────────────────────
Subcommand:   <init|probe|status|judge|execute>
Session:      <session_id>
Lease:        <lease_id | none>
Authority:    <T0|T1|T2> (from lease, never self-asserted)
─────────────────────────────
Plan:         <description of intended mutation>
cc_id:        <present | MISSING>
  MISSING → BLOCKED — route /request-seal → 888 first
  PRESENT → forge_execute (reversible first, dry-run probe available)
Stage:        <stage_id | none>
F13 token:    <present | absent>  (only for forge_execute_sealed)
─────────────────────────────
```

**Gate rule:** No SEAL → No Mutation. `/forge execute` without a cc_id
from a prior `/request-seal` is BLOCKED.

---

## Removed Commands (replaced or deprecated)

| Old | New | Why |
|---|---|---|
| `/new` | `/init` then continue | /new is convenience over /init — call /init first |
| (none) | `/request-seal` | OpenClaw cannot self-seal; routes to 888 |
| (none) | `/forge <subcommand>` | 777 EXECUTE gate — observe free, mutate requires SEAL |
| `/yolo` | `/yolo` (with stronger warning) | Still exists but Atlas expression makes danger explicit |

---

## ZEN — Why /init, /request-seal, and /forge Matter

```
/init          answers:  WHO AM I?
               → slot, authority, lane, atlas expression
               → without /init, every other command is unauthenticated

/request-seal  answers:  CAN THIS BE SEALED?
               → routes to 888 for verdict
               → OpenClaw cannot self-authorize

/forge         answers:  CAN THIS MUTATE?
               → observe free; mutate requires cc_id from SEAL
               → 777 EXECUTE — No SEAL → No Mutation

Together:
  /init          → I know who I am
  /request-seal  → I ask 888 to validate what I propose
  /forge         → I ask 777 to mutate, but only after 888 has sealed

  /init alone           → opinion only
  /init + /request-seal → sealed proposal
  /init + /forge probe  → safe dry-run
  /init + /forge execute (no cc_id)  → BLOCKED
  /init + /request-seal + /forge execute (with cc_id) → governed mutation
```

---

*Forged 2026-08-08 by Hermes ASI under Atlas v1 doctrine.*
*DITEMPA BUKAN DIBERI 🔥*