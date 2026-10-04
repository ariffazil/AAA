# Izzu Memory Persistence Debug — 2026-08-09

## Symptom

Izzu posts in AIA group. Hermes responds. Izzu posts again. Hermes has no memory of previous interaction — asks "Hang yang hantar hang buat lupa" (You sent it, you forgot?).

## Root Causes (3 found)

### 1. Wrong lane routing (critical)

Runtime state had `chat:-1003521544074 → "arif"` instead of detecting Izzu/Aliff per-user. The `pre_gateway_dispatch` hook saved the LAST person's lane for the entire chat.

**Fix:** Cleared stale chat-level mappings from `.runtime.json`, kept only user-level.

### 2. Memory never persisted

Lane plugin `pre_llm_call` READS memory files but nothing WRITES to them. After every LLM turn, the interaction was lost.

**Fix:** Added `post_llm_call` hook to lane_switch plugin that accumulates interactions into `MEMORY-{lane}.md`.

### 3. kunci-mas.env env var override (related)

Izzu (1024343313) and Aliff (1237635275) were MISSING from `TELEGRAM_ALLOWED_USERS` and `TELEGRAM_GROUP_ALLOWED_USERS` in `kunci-mas.env`. The adapter uses env vars as sole authority — config.yaml `allow_from` is ignored when env vars exist.

**Fix:** Added IDs to all three allow lists in kunci-mas.env.

## Verification

After gateway restart:
1. Runtime state: no chat-level mappings, only user-level
2. `post_llm_call` hook registered: `grep 'registered' gateway.log`
3. Memory file grows: `wc -l MEMORY-izzu-aia.md`
4. Izzu's messages arrive: `grep '1024343313' gateway.log`

## Lesson

Memory persistence requires BOTH read path (`pre_llm_call`) AND write path (`post_llm_call`). Without write, memory is read-once-then-forgotten.
