---
id: minimax-m-plan
name: MiniMax M Plan
version: 1.0.0-2026.10.21
description: "Use when routing work to MiniMax — deciding whether the M Plan seat or another provider serves the task, which credential to bind, and when the plan boundary (credits, not PAYG) changes the answer. Also use when a MiniMax call returns 402, 401, or an empty model catalogue."
owner: 333-AGI
risk_tier: low
floor_scope: F2, F4
autonomy_tier: T1
capability_tier: fed-multimodal-vision
ecology_state: WARM
owned_by: 333-AGI
authority_of: 333-AGI
---

# MiniMax M Plan — the federation's primary MiniMax seat

> **Governance:** this skill is *routing* doctrine, not credential doctrine. It never prints a key value.
> Any credential change goes through `/root/scripts/rotate-secret.sh` (the only sanctioned write path) and
> `/root/.secrets/KEY_REGISTRY.md` for discovery. (F1 AMANAH / F2 TRUTH)

## What this plan is

**MiniMax M Plan (Build tier)** — one subscription seat that covers text, video, image, speech,
web search, multimodal understanding, and an API key for agents and coding tools.

| Fact | Value |
|------|-------|
| Tier | Monthly M Plan Build |
| Renewal | **2026-11-19** (auto) |
| Order ID | `2112696757015031993` |
| Usage | 7.5x Go usage · 3 Hailuo video clips/day |
| Credential | `sk-cp-…` — **subscription/credits only** |
| Endpoint | `https://api.minimax.io` (global) |

**The credential boundary that bites:** the `sk-cp` key is subscription/credits. It **cannot** be
used for pay-as-you-go. The separate `sk-api` PAYG key is a different product and is currently
**dead** — live-probed 2026-10-21: `HTTP 402 insufficient_balance_error`.

So there is exactly **one** working MiniMax credential in the federation, and it is the plan seat.
Treat MiniMax as a single-seat provider, not as a two-lane one.

## Which key to bind

| Env var | Value | Use |
|---------|-------|-----|
| `MINIMAX_API_KEY` | sk-cp plan seat | **Default.** Use this. |
| `MINIMAX_MPLAN_KEY` | same sk-cp seat | Explicit alias. Both are correct; pick one and be consistent. |
| `MINIMAX_PLUGIN_API_KEY` | same sk-cp seat | Legacy alias. Works; do not treat as a separate lane. |
| `MINIMAX_PAYG_API_KEY` | sk-api PAYG | **Do not route production traffic here.** 402, no balance. |

All three working names are the *same* seat. Only `MINIMAX_PAYG_API_KEY` is different — and it is dead.

**How to tell them apart without printing them:** `sk-cp-` = plan, `sk-api-` = PAYG.

## When to use the plan vs another provider

The M Plan is the federation's **P1 constitutional lane** — not a fallback. In FED (`:4000`)
these aliases are headed by MiniMax-M3 on the plan key:

| FED alias | Use it for |
|----------|-----------|
| `apex-888` | **Constitutional judging** (888-APEX). The chain head. Multimodal evidence accepted. |
| `forge-judge` | Diff + receipt comparison during forge. |
| `forge-planner` | Task decomposition, scope/budget/architecture planning. 1M ctx. |
| `forge-777` | Engineering execution lane. |
| `hermes-default` | HERMES general lane. |
| `i-arif` | i-ARIF synthesis. Vision-capable. |
| `hermes-asi-vision` | Anthropic-compatible path (`/anthropic/v1/messages`). |
| `MiniMax-M3.1-Flash-Preview` | M Plan / MiniMax Code **exclusive**. Fast, effort-tunable thinking. |
| `fed/minimax-tts` | Speech synthesis via FED. |

**Reach for the plan when:** you need 1M context; you need to judge large evidence bundles; you need
image/video/speech generation; you need web search; or you need the Anthropic-compatible wire.

**Reach for another provider when:** the task is a deep-reasoning coding audit (`deepseek-v4-pro`),
or the plan seat is rate-limited — then use the lane's own fallback chain, never the dead PAYG key.

## Why it matters (the trap this skill exists for)

Until 2026-10-21 the vault SOT held `MINIMAX_API_KEY` = the **sk-api PAYG** key, while six other
surfaces (the `qwen.env` / `mimo.env` / `tokenrouter.env` / `a-forge.env` / `mimo-token-plan.env`
copies and `HERMES/.env`) plus the model SOT already declared `MINIMAX_API_KEY` = the **sk-cp
plan** key. The vault SOT was the outlier.

Consequence: the TTS lane and every organ reading `MINIMAX_API_KEY` resolved the dead key and
silently fell back to Edge-TTS / F5-TTS, and 11 live services held a stale env snapshot.

**The lesson, generalised:** *a credential's name is a promise about its meaning.* When two
surfaces disagree about what a variable name means, the majority plus the working credential wins
and the minority is the bug — but verify that by probing, not by counting.

## How to call it

### Text / chat (OpenAI-compatible)
```bash
curl -s https://api.minimax.io/v1/chat/completions \
  -H "Authorization: Bearer $MINIMAX_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M3","max_tokens":32,"messages":[{"role":"user","content":"..."}]}'
```

### Text (Anthropic-compatible)
```bash
curl -s https://api.minimax.io/anthropic/v1/messages \
  -H "x-api-key: $MINIMAX_API_KEY" -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model":"MiniMax-M3","max_tokens":32,"messages":[{"role":"user","content":"..."}]}'
```

### TTS — resolve the voice through the registry, never by guessing
Use `provider_voice_id` from `/root/AAA/audio/voice-registry.json` (e.g. `siti` →
`SSSiti20260926v1`). Passing the *alias* (`siti`) to the API returns
`status_code 2054 voice id not exist` — the alias is federation-local.
```bash
curl -s -X POST https://api.minimax.io/v1/t2a_v2 \
  -H "Authorization: Bearer $MINIMAX_API_KEY" -H "Content-Type: application/json" \
  -d '{"model":"speech-2.8-hd","text":"...","stream":false,"voice_setting":{"voice_id":"SSSiti20260926v1"}}'
```

### Image
`POST /v1/image_generation` with `model: image-01`.

### Video — the model id the tier sheet advertises is NOT the id the API accepts
The Build tier sheet says "Video models, e.g. **H3**", but `POST /v1/video_generation` **rejects H3**
(`status_code 2013 invalid model param`). Callable ids verified 2026-10-21:
**`MiniMax-Hailuo-02`** and **`T2V-01`**. `Hailuo-02` without the `MiniMax-` prefix is also rejected.
Video is async: POST to create a `task_id`, then poll `/v1/query/video_generation`.

### Web search + MiniMax Code
`mmx` (MiniMax Code CLI, `/root/.npm-global/bin/mmx`) exposes `auth`, `text`, `speech`, `image`,
`video`, `search`, `vision`, `quota`, `config`. Config at `/root/.mmx/config.json`, `region: global`.
Use `mmx quota show` to read live credit consumption.

## Failure modes — what each error means

| Symptom | Meaning | Action |
|---------|---------|--------|
| `402 insufficient_balance_error` | You sent the **PAYG** key, or the plan credits are exhausted. | Check the key prefix: `sk-cp-` = plan, `sk-api-` = PAYG. If it is `sk-cp-` and still 402, the plan credit pool is spent — that is a renewal/quota matter, escalate. |
| `401` | Key revoked or rotated. | Rotate via `rotate-secret.sh`; do not hand-edit the vault. |
| `2054 voice id not exist` | You passed a federation voice *alias* to the API. | Resolve through `voice-registry.json` → `provider_voice_id`. |
| `2013 incorrect model param` (video) | Wrong video model id. | Use `MiniMax-Hailuo-02` or `T2V-01`, not `H3`. |
| Empty `/v1/models` list | Wrong host or key. | Global endpoint is `api.minimax.io`. Re-probe `/v1/models`. |
| TTS silently degrades to Edge/F5 | The lane resolved a dead key. | The TTS pipeline reads `MINIMAX_API_KEY` from env, then falls back to the vault file. Confirm the vault now carries the plan key. |

## Probing the seat (do this, do not assume)

```bash
curl -s --max-time 15 https://api.minimax.io/v1/models -H "Authorization: Bearer $MINIMAX_API_KEY"
```
Expect 200 with `MiniMax-M3.1-Flash`, `MiniMax-M3`, `MiniMax-M2.7`, `MiniMax-M2.5`, `MiniMax-M2.1`
and their `-highspeed` variants. Anything else means the key or host is wrong.

## Renewal

**2026-11-19.** CHRON carries the stake as `EV-MPLAN-RENEW-20261119`. There is no second
credential to fall back on: the PAYG lane is already 402. A silent non-renewal breaks the P1
judge lane for every agent that does not fall back — treat it as a P1 dependency, not a utility.

## Related skills

- `mmx-cli` — the MiniMax Code CLI (`mmx`).
- `minimax-image-gen` — image/video/TTS/voice-clone via the media MCP on `:18100`.
- `provider-integration` — cross-provider wiring, fallback chains, thinking-model quirks.
- `federation-seat-wiring` — adding/removing a provider seat and its credentials.
