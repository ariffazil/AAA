# ADR-010: AAA Telegram Visibility — Dual-Bot Collaboration Pattern

**ADR ID:** ADR-010-AAA-TELEGRAM-VISIBILITY  
**Date:** 2026-05-04  
**Epoch:** EPOCH-2026-05-04  
**Verdict:** SOVEREIGN DECREE — Arif  
**Status:** ACTIVE  

---

## Context

Arif's requirement: **visibility in the same AAA group** for both Hermes (ASI lane) and OpenClaw (AGI lane). Arif rejects Option 2 (single bot multi-lane prefix) because he wants two real distinct agents visible in AAA.

Telegram constraints we must respect:
- Bots CAN see messages from **humans** (with privacy off or as admin)
- Bots CANNOT see messages from **other bots** — Telegram explicitly blocks bot-to-bot to prevent infinite loops
- Bots CAN be in the same group and each receive human messages
- "Collaboration" cannot happen by one bot reading the other's group messages

Solution: A2A orchestration off-Telegram, visible collaboration on-Telegram.

---

## Decision

### Two Real Bots in AAA Group

- **Bot A (Hermes):** `@ASI_arifos_bot` — ASI lane, Nous OAuth, planner/judge
- **Bot B (OpenClaw):** `@AGI_ASI_bot` — AGI lane, OpenClaw surface, executor

### Trigger Mode: Command-Only (Privacy ON)

- `/aaa <prompt>` → full collaboration (Hermes + OpenClaw)
- `/hermes <prompt>` → Hermes only
- `/openclaw <prompt>` → OpenClaw only
- Reply to any bot message → continues same taskId thread

Rationale: Privacy ON + command-only prevents ambient surveillance in group. Matches F05 PEACE and F09 ANTIHANTU. Execution is clean and intentional.

### Telegram Settings Per Bot

- `/setjoingroup` → enable groups
- Privacy ON (command-only) — no need to remove/re-add bot
- Make both admins is optional but not required for command-only mode

### Collaboration Architecture

```
AAA Group (Telegram)
    │
    ├── @ASI_arifos_bot receives /aaa → forwards to AAA gateway
    └── @AGI_ASI_bot receives /openclaw → forwards to AAA gateway
            │
            ▼
    ┌─────────────────────┐
    │   AAA Gateway       │
    │  (OpenClaw process) │
    │                     │
    │  handle_collab():   │
    │  1. call_a2a(       │
    │    hermes, "plan")  │
    │  2. send via Hermes │
    │    token → TG       │
    │  3. call_a2a(       │
    │    openclaw,"exec") │
    │  4. send via OC     │
    │    token → TG       │
    │  5. (optional)      │
    │    hermes review    │
    │  6. send via Hermes │
    │    token → TG       │
    └─────────────────────┘
            │
            ├──→ Hermes Token ──→ Telegram ──→ AAA group: ASI💃 Hermes: [plan/review]
            └──→ OpenClaw Token ──→ Telegram ──→ AAA group: AGI🦞 OpenClaw: [exec]
```

### Gateway handle_collab() Logic

```pseudocode
async function handle_collab(taskId, prompt, chat_id, source) {
  // Step 1: Hermes plans
  const hermes_plan = await call_a2a(hermes, {
    taskId,
    role: "planner/judge",
    prompt,
    epoch: current_epoch()
  });
  await send_via_telegram(HERMES_TOKEN, chat_id,
    format_hermes_plan(hermes_plan, taskId));

  // Step 2: OpenClaw executes
  const oc_exec = await call_a2a(openclaw, {
    taskId,
    role: "executor",
    hermes_plan,
    epoch: current_epoch()
  });
  await send_via_telegram(OPENCLAW_TOKEN, chat_id,
    format_openclaw_exec(oc_exec, taskId));

  // Step 3: Hermes reviews (optional)
  const hermes_review = await call_a2a(hermes, {
    taskId,
    role: "reviewer",
    openclaw_output: oc_exec
  });
  await send_via_telegram(HERMES_TOKEN, chat_id,
    format_hermes_review(hermes_review, taskId));
}
```

### Message Format Conventions

- **Hermes:** `ASI💃 Hermes (plan):` or `ASI💃 Hermes (review):`
- **OpenClaw:** `AGI🦞 OpenClaw (execution):`
- **AAA Conductor meta:** `AAA:` prefix for orchestrator context lines

---

## What Is Needed

### Already Have
- [x] `@AGI_ASI_bot` token — OpenClaw bot token in gateway config
- [x] OpenClaw gateway — handles routing and A2A
- [x] AAA group `-1003753855708` — active group

### Need to Create/Configure
- [ ] `@ASI_arifos_bot` — create via @BotFather, give token
- [ ] Hermes Nous OAuth credentials — depends on Hermes hosting
- [ ] A2A adapter for Hermes — depends on Hermes integration method
- [ ] `handle_collab()` stub in OpenClaw gateway
- [ ] Telegram sendMessage wrappers for both tokens

---

## Security Notes (F09 ANTIHANTU, F12 INJECTION)

- Gateway must sanitize all user input before forwarding
- taskId in metadata prevents thread confusion
- No bot reads another bot's messages — A2A is pure HTTP
- Command-only mode prevents indirect prompt injection via ambient listening

---

## Status History

- 2026-05-04: SOVEREIGN DECREE — active as Arif's canonical AAA visibility requirement

---

*Ditempa Bukan Diberi — forged, not given.*
