---
name: constitutional-commands
description: "Slash command architecture across federation bots — /init, /propose-seal, /forge. Telegram surface for constitutional primitives (arif_init, arif_judge, arif_seal). Also covers FORGE notification routing (forge-notify.sh → AAA group). Triggers: slash commands, /init, /seal, /forge, propose-seal, notification routing, FORGE bot posts, telegram group routing."
version: 1.0.0
author: Hermes ASI
license: MIT
metadata:
  hermes:
    tags: [federation, telegram, slash-commands, constitutional, forge-notify]
---

# Constitutional Commands — Federation Telegram Surface

The federation exposes constitutional primitives as Telegram slash commands across three bots. This skill governs the command architecture, the 888≠999 separation of powers, and the FORGE notification routing pattern.

## Trigger conditions
- Any question about `/init`, `/propose-seal`, `/forge`, or slash command routing
- "FORGE bot should post to the group" / notification routing changes
- Configuring or debugging Telegram bot commands across federation bots
- 888≠999 separation of powers in chat surface

---

## Three Bots, Three Roles, One Kernel

| Bot | Handle | Role | /init | /propose-seal | /forge |
|---|---|---|---|---|---|
| Hermes | @ASI_arifos_bot | COORDINATE — context/mandor | ✅ | ✅ | status only |
| OpenClaw | @AGI_ASI_bot | THINK — 333 thinker, 444 orchestrator | ✅ | ✅ | init/probe/status/judge/execute |
| FORGE | @arifOS_bot | EXECUTE — 777 executor | ❌ | ❌ | status/deploy/rollback |

- All bots share the same kernel at `:8088` (`arif_init`, `arif_judge`, `arif_seal`).
- Chat bots (Hermes, OpenClaw) propose. Kernel seals. Forge mutates.
- A-FORGE exposes `forge_*` MCP tools, not Telegram slash commands.

---

## The Slash Command Map (three layers)

### Layer 1 — Runtime (native, no work needed)

These come from OpenClaw/Hermes core. No skills or plugins required:

```
/new /reset /status /whoami /model /restart /config /mcp
```

### Layer 2 — Constitutional (skill-based, must be implemented)

| Command | Substrate | Kernel verb | Output |
|---|---|---|---|
| `/init` | INIT | `arif_init` | SESSION BOUND card (who is acting, authority, TTL) |
| `/propose-seal` | MEMORY | `arif_judge` (888) → `arif_seal` (999) | Verdict card (SEAL / HOLD / VOID) |

### Layer 3 — Forge Subcommands (OpenClaw only)

`/forge` is not one command — it's a gateway to pipeline subcommands:

```
/forge init      → arif_init (session ignition)
/forge probe     → forge_probe (organ liveness)
/forge status    → forge_registry_status (tool registry)
/forge judge     → arif_judge (888 verdict — READ ONLY for OpenClaw)
/forge execute   → arif_forge (777 — MUTATE, requires cc_id SEAL)
/forge seal      → BLOCKED for OpenClaw (999 = 888's witness)
```

---

## Critical Invariants

### Self-seal is HARAM (888 ≠ 999)

```
/seal (❌ BLOCKED everywhere — self-author is forbidden)
   ↓
/propose-seal (✅ — the only chat-layer command)
   ↓
candidate + evidence → arif_judge (888)
   ↓
SEAL → arif_seal (999, VAULT999 immutable append)
HOLD → feedback, revise
VOID → reject
```

**Every bot. Every surface. Nobody self-seals.** The slash command surface is the *proposer*, not the *sealer*. The sealmaker is arifOS kernel (`:8088` → `arif_seal` → VAULT999).

### /init SESSION BOUND card format

```
SESSION BOUND

Actor: OPENCLAW (bound to ARIF_FAZIL)
Runtime: OpenClaw 2026.7.1-2
Phenotype: Gateway Thinker

Atlas Expression:
333 THINK (primary)
444 ORCHESTRATE (secondary)

Authority: OBSERVE_ONLY → FULL (dynamic)
Mutation: DENIED (unless SEAL)
Seal: DENIED

Kernel: DEGRADED
Reason: source (2657104) != built (cb5afef)
Session: SEAL-
TTL: 28800s
```

This is a **substrate primitive**, not a convenience init. "Who is acting?" is answered before "What should we do?".

### Split-bind protection

If both Hermes and OpenClaw can `/init`, they may mint competing session bindings.

**Rule:** `/init` returns existing session id if already bound; only one bot binds per session thread. When implementing, pin this in the skill spec.

---

## Implementation Routes (verified 2026-08-08)

| Route | Method | Speed | Notes |
|---|---|---|---|
| **A. Skills ⭐** | Create skill files; `nativeSkills: auto` | Fastest | Telegram auto-registers as native commands with button menu. Skill names sanitized to `a-z0-9_` — all three names valid. |
| B. Plugin | `registerCommand()` via plugin SDK | Deterministic | Heavier, requires plugin development |
| C. Text fallthrough | `commands.text: true` | Fragile | Unknown /cmd reaches model. No picker UI. |

**Recommended: Route A** — skill files, governed via skill_workshop.

---

## FORGE Notification Routing (2026-08-08)

### The problem

`forge-notify.sh` (used by all A-FORGE duty scripts) was hardcoded to DM Arif:
```bash
CHAT_ID="267378578"   # Arif's user ID — DM to FORGE bot
```

Arif wants FORGE to post directly to the AAA group. He was copy-pasting from DM.

### The fix

```bash
CHAT_ID="-1003753855708"   # AAA group (prefix -100 = supergroup)
```

**Two bugs fixed:**
1. Wrong CHAT_ID (DM instead of group)
2. `parse_mode` parameter was declared in function signature but NOT passed to curl → Markdown not rendered, all text one wall

### The corrected curl

```bash
RESPONSE=$(curl -sf -X POST "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  -d text="${MESSAGE}" \
  -d parse_mode="${PARSE_MODE}" \
  --max-time 10 2>/dev/null || echo '{"ok":false}')
```

### Key routing facts

- **Bot identity:** FORGE posts AS `@arifOS_bot` INTO the group — it's the same bot account, different destination.
- **AAA group ID:** `-1003753855708` (Telegram supergroup prefix is `-100`).
- **Token file:** `/root/.secrets/tokens/telegram-opencode-bot` (FORGE bot token, NOT the OpenClaw GUTS token).
- **All three duty scripts call `forge-notify.sh`:**
  - `forge-constitutional-sync.sh` (07:00 UTC / 15:00 MYT)
  - `forge-vitality-pulse.sh` (15:00 UTC / 23:00 MYT)
  - `forge-drift-scanner.sh` (02:00 UTC / 10:00 MYT, silent if clean)

### Pitfall: group ID format

Telegram group IDs for supergroups MUST have the `-100` prefix. Using just the numeric ID (`1003753855708`) without the negative sign sends to the wrong destination or fails silently. The canonical format is `-1003753855708`.

---

## Federation Bot Token Map

| Bot | Handle | Token file | Token env var |
|---|---|---|---|
| Hermes | @ASI_arifos_bot | managed by Hermes gateway | via `.env` |
| OpenClaw | @AGI_ASI_bot | `/root/.secrets/tokens/telegram-agi-asi-bot` | `TELEGRAM_BOT_TOKEN` (systemd drop-in) |
| FORGE | @arifOS_bot | `/root/.secrets/tokens/telegram-opencode-bot` | `TELEGRAM_BOT_TOKEN` (systemd drop-in) |

Never paste token values into chat. Tokens live in mode-600 files.

---

## Verification checklist

- [ ] `/init` from each bot → SESSION BOUND card shows correct actor/atlas/authority
- [ ] `/propose-seal` from OpenClaw → routes to `arif_judge` (888), NOT to direct seal
- [ ] `/seal` → BLOCKED on every bot (no self-author)
- [ ] `/forge execute` → requires `cc_id` SEAL pre-existing (rejected without one)
- [ ] `forge-notify.sh` → posts to AAA group (`-1003753855708`), not DM
- [ ] Markdown formatting renders (parse_mode passed to curl)
- [ ] Both Hermes and OpenClaw `/init` return the same session id if bound to same thread

---

*Forged: 2026-08-08. Source: OpenClaw slash command architecture spec + FORGE notification routing fix. DITEMPA BUKAN DIBERI.*
