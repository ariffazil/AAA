# Syed Khairuddin Morktarudin — Hermes Alignment Audit (2026-08-07)

> Snapshot of the 7-layer alignment audit for the persona "Abang Sado" (Syed).
> Re-run before any session where Syed is the active user.

## The 7-layer audit (current state)

| Layer | Status | What's done | What's missing |
|---|---|---|---|
| **1. Telegram access** | ❌ Unverified | — | Test: ask Syed to `/start` the bot; confirm DM reply |
| **2. USER.md profile** | ❌ None | — | Create `USER-syed.md` from `templates/USER-persona.md` |
| **3. Identity-test pattern** | ⚠️ Failed 3x in 2026-08-07 session | Codified first-message ask-not-assume protocol | Bake into session-start hook |
| **4. Cron jobs** | ❌ Zero | — | 4 jobs: `syed-gerd-log`, `syed-mak-dressing`, `syed-mak-cbd-followup`, `syed-sambal-preorder` |
| **5. Memory lane** | ⚠️ Mixed in operator's MEMORY.md | — | Migrate to `MEMORY-syed.md` per persona lane doctrine |
| **6. Skill whitelist** | ⚠️ Loads operator's full skill set | — | Per-session override for persona-safe skills only |
| **7. Response style** | ⚠️ Default to operator's BM standard | — | Override: BM Pasar, "hang" / "abang" / "beb" register, voice note default for >3 sentences |

## F13 consent checklist

- [ ] Syed confirmed Hermes is tracking caregiver/health context (recommended: ask on first DM)
- [x] No PII shared cross-persona
- [ ] Medical advice reminder: remind Syed to consult real doctor (log only, never diagnose)
- [ ] Money moves require explicit operator co-sign
- [ ] Cron delivery failures go to quarantine log, not operator's DM

## Action plan — order of execution

1. **Layer 1:** Test Syed can DM the bot. Fix `authorized_chats` if needed.
2. **Layer 2:** Copy `templates/USER-persona.md` → `USER-syed.md`, fill from identity fixture.
3. **Layer 3:** Bake ask-not-assume into persona-switched session-start.
4. **Layer 5:** Migrate Syed content from operator's `MEMORY.md` → `MEMORY-syed.md`.
5. **Layer 4:** Create 4 cron jobs, all `deliver: telegram:1042200555`.
6. **Layer 6:** Session-start hook filters skills to persona-safe set.
7. **Layer 7:** SOUL.md gains "Syed register" subsection.

## Verify-before-declare checklist

- [ ] Syed can DM bot → gets reply
- [ ] `USER-syed.md` exists, matches template
- [ ] Ask-not-assume protocol documented
- [ ] `cronjob(action='list')` shows 4 Syed jobs
- [ ] `MEMORY-syed.md` separate from operator's
- [ ] Session-start hook reads USER-syed.md
- [ ] SOUL.md has Syed register

**Status as of 2026-08-07: 0/7 verified.** This is the gap.

## Session lessons (2026-08-07)

1. **Voice-to-text medical terms:** "GERD" → "gerd" → "geram" → 3 misreads. Confirm specialist terms when STT involved.
2. **Identity-test is real:** Syed identity drifted 3x ("Abang Sado = dashboard?"). Don't auto-confirm from memory.
3. **Caregiver = voice-note default:** Logged 2026-08-07: "Dia malas nak Baca. Malas nak type."
4. **Sambal + GERD irony:** Don't draw the connection out loud. Track silently.
5. **F13 consent is per-persona, not per-session:** Lane isolation applies even if operator is the only consumer.
