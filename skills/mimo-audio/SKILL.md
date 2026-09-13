---
name: mimo-audio
description: "FEDERATED Xiaomi MiMo v2.5 audio intelligence — TTS (0-credit free window), ASR (en/zh), voice design, voice clone (F13-gated). Available to ALL AAA agents via this canonical skill. Use when generating speech/voice notes, designing voices, or transcribing wav/mp3 (en/zh). BM/dialect stays on GLM/dashscope lanes. TRANSPORT: direct lane (litellm cannot carry audio bodies)."
---

# MiMo Audio — federated organ (AAA canonical, 2026-09-07)

**Status:** LIVE — re-verified end-to-end 2026-09-13 (FI-008 embed audit). TTS = 0 credits while the free window lasts.
**Env (every FI home + Hermes):** `MIMO_TOKEN_PLAN_API_KEY` + `MIMO_BASE_URL` (https://token-plan-sgp.xiaomimimo.com/v1); alias `MIMO_API_KEY`.
**Anthropic wire:** `https://token-plan-sgp.xiaomimimo.com/anthropic` → `POST /v1/messages` (verified 2026-09-13: HTTP 200, real text + thinking block; auth accepted as either `x-api-key` or `Authorization: Bearer`).
**Clusters:** sgp / cn / ams. The tp- key is **cluster-scoped** — the SGP key returns **401** on `-cn` and `-ams` (verified 2026-09-13). Never repoint a lane at another cluster without a key for that cluster.
**Contracts SOT:** `/root/.config/federation-models.json` → `mimo/mimo-v2.5-*` (`api_contract`, `credit_model`, `cluster_endpoints`) + signatures `fed-realtime-voice` (WIRED_DIRECT_LANE) / `fed-audio-understanding`.

## Credit model (vendor page, retrieved 2026-09-13)
| leg | mimo-v2.5-pro | mimo-v2.5 |
|---|---|---|
| input, cache HIT | 2.5 credits/tok | 2 credits/tok |
| input, cache MISS | 300 credits/tok | 100 credits/tok |
| output | 600 credits/tok | 200 credits/tok |

- **pro/v2.5 ratio is NOT uniform:** cache-miss input **3×** (300/100), output **3×** (600/200), but cache-hit input only **1.25×** (2.5/2). Older federation notes claiming a flat "2×" were wrong; an intermediate "3× on every leg" note was also wrong — retracted 2026-09-13 after independent verification.
- **ASR:** 30,000,000 credits per audio-hour. **TTS series (tts / voiceclone / voicedesign): free, 0 credits** — limited promotional window.
- **One shared pool** across all 6 models, consumed in parallel at these ratios — not 6 independent buckets.
- **Off-peak:** Beijing 00:00–08:00 = **UTC 16:00–24:00** = 0.8× consumption coefficient.
- **Exhaustion = HARD STOP.** Service halts; it does NOT spill onto bonus/account balance. Recovery: pay-the-difference upgrade, or the separate PAYG lane (`sk-` key).
- **Counter ≠ enforcement.** 2026-09-13 the console read 82,016,728,360 / 82,000,000,000 (100.0%, over cap) while text, TTS, ASR and voicedesign all returned HTTP 200 in burst. Treat a live probe as truth, never the console number.

## ⚠️ TRANSPORT WARNING (corrected 2026-09-13; original E2E 2026-09-07)
- **FED front door `:4000` does NOT expose all 6 models** — the earlier "lists all 6 (discovery GREEN)" claim was wrong. Live 2026-09-13: `GET :4000/v1/models` returns **47 models total, of which only `mimo-v2.5-pro` and `mimo-v2.5` are MiMo**; calling `mimo-v2.5-asr` through FED returns **HTTP 400 "Invalid model name"**. (`:4000` = HAProxy → local litellm on **:4013**, docker container mounting `/root/A-FORGE/litellm-config.yaml`.)
- **Audio bodies MUST ride the DIRECT lane** (agent → `$MIMO_BASE_URL/chat/completions`). This is now mandatory for *availability*, not just for translator mangling. ToS-clean agent-tool usage, E2E-proven below; text-lane MiMo traffic may use :4000 for the 2 exposed ids.
- **Historical, not current:** the litellm translator crash (`convert_dict_to_response.py`, `message.audio` unknown; ASR `input_audio` mangled → "Param Incorrect") is recorded in litellm health-state with `fail_count: 10817, last_fail: 2026-09-03`. The affected routes were subsequently **removed** from the litellm config (generic `fed/audio-asr|tts` now point at Gemini), so that exact surface is no longer reachable at :4000. The one audio MiMo route still wired there is `fed/audio-voiceclone-restricted` (→ `openai/mimo-v2.5-tts-voiceclone`, locked under 888_HOLD).
- Open for FED owner (FI-008): expose the remaining 4 MiMo ids at :4000 + litellm audio-body support + classifier audio lexicon (v1 has no audio class).

## The three TTS models — ALL ride POST {BASE}/chat/completions (NOT /audio/speech)
| model | voice source | singing | clone | design |
|---|---|---|---|---|
| mimo-v2.5-tts | builtin | yes ((唱歌)/(sing) prefix, CN lyrics best) | no | no |
| mimo-v2.5-tts-voicedesign | text description (user msg) | no | no | yes |
| mimo-v2.5-tts-voiceclone | audio sample data-URI <=10MB mp3/wav | no | yes | no |

**Wire:** assistant message = text to speak; user message = style instructions (not spoken); `audio: {format: "wav"|"pcm16"(stream), voice: "<id>"}`; response `choices[0].message.audio.data` = base64 wav; stream = `delta.audio.data` 24kHz PCM16LE mono.
**Voices:** EN Mia / Chloe / Milo / Dean — CN 冰糖 / 茉莉 / 苏打 / 白桦 (+ mimo_default).
**Style control:** natural language (user msg) + inline audio tags `[pause] [sighs] [sternly] [trembling]` (bilingual, mixable) + screenplay layers Instruct/Text/Character/Scene/Direction.
**Gotchas:** `audio.voice` is model-specific — voicedesign MUST omit it (HTTP 400); clone needs data-URI; TTS output is random — regenerate a few times to pick the best take.

## ASR — mimo-v2.5-asr (chat/completions, NOT /audio/transcriptions)
Content part: `{"type":"input_audio","input_audio":{"data":"data:audio/wav;base64,..."}}`; wav/mp3 ONLY; b64 <= 10MB; `asr_options.language` in auto|zh|en — **no `ms`**; BM/dialect rides `auto` (Penang-Besi UNTESTED → prefer dashscope/GLM for BM fidelity). ~30M credits/audio-hour (~$0.074/h).

## Governance
- voiceclone/voicedesign new voice_id = **F13 SOVEREIGN gate**; reuse = F11 audit (see AAA-voice-cloning-mimo-minimax).
- i-ARIF **primary** voice_id stays MiniMax speech-2.8-hd (identity continuity) — do NOT move. **CORRECTION 2026-09-13 (F13 SOVEREIGN):** the MiMo ban on i-ARIF traffic is **LIFTED** — *"awat hang ban. bagi ada la"* (Arif). The 08-30 scar premise (Xiaomi content_filter kills family chat) **did not reproduce**: three family-chat probes returned HTTP 200 with normal warm Malay. MiMo is now a legitimate i-ARIF lane. The identity-voice constraint is separate and stands.
- ToS: token-plan key for agent/harness use only — never cron/backend.

## Fallback ladder
mimo-audio (0 credits, free window) → edge-tts (free floor, ms-MY voices) → QwenCloud token-plan TTS.

## E2E receipts (2026-09-07)
- Direct TTS (Hermes KVM4, Mia): 307,244B wav / 24kHz mono / 6.4s / 223 tokens / 0 credits
- Direct TTS (FI-003 KVM8): 133,180 b64 chars / 173 tokens / 0 credits
- Vision understanding: 128x128 red PNG → "Red." (img_tokens=16, cached=192)
- litellm :4000 TTS/ASR bodies: RED (translator) — warning above

## Quick recipe (direct lane)
    curl -sS "$MIMO_BASE_URL/chat/completions" \
      -H "Authorization: Bearer $MIMO_TOKEN_PLAN_API_KEY" \
      -H 'Content-Type: application/json' -d '{
      "model":"mimo-v2.5-tts",
      "messages":[{"role":"user","content":"Warm, friendly Malaysian English."},{"role":"assistant","content":"Good morning, the federation is healthy."}],
      "audio":{"format":"wav","voice":"Mia"}}' \
      | jq -r '.choices[0].message.audio.data' | base64 -d > out.wav

## Federation map
Canonical: `/root/AAA/skills/mimo-audio` (this file) · official vendor reference: `references/official/` (MIT, XiaomiMiMo/MiMo-Skills).

**Visible on af-forge: 9 homes at first pass → 11 as of 2026-09-13.** The authoritative current roster is the "Federation access — audio lane" section at the END of this file. The list below is retained as the original mapping, which corrected the first print (it had listed `qwen` and omitted the opencode identity home).
1. `/root/AAA/skills/mimo-audio` — canonical (physical)
2. `/root/.agents/skills/mimo-audio` — whole-dir link
3. `/root/.claude/skills/mimo-audio` — whole-dir link
4. `/root/.codex/skills/mimo-audio` — whole-dir link
5. `/root/.grok/skills/mimo-audio` — whole-dir link
6. `/root/.gemini/skills/mimo-audio`
7. `/root/.kimi-code/skills/mimo-audio` — per-skill symlink
8. `/root/.config/opencode/skills/mimo-audio` — per-skill symlink
9. `/root/.arifos/agents/opencode/skills/mimo-audio` — per-skill symlink

**Still absent (do not claim):** `/root/.copilot/skills/mimo-audio`. The "Hermes original on KVM4" is off-host and unverified from af-forge — neither `/root/HERMES/skills/` nor `/root/.hermes/skills/` contains it locally. (`/root/.qwen/skills/mimo-audio` and `/root/A-FORGE/skills/mimo-audio` were absent at first pass and were **added** on 2026-09-13 — see the appended section.)

---

## Federation access — audio lane (added 2026-09-13)

**One command for every AAA agent. No skill needed, no plumbing, no key handling:**

```bash
mimo-audio doctor                      # probe endpoint + env + audio-model presence
mimo-audio voices                      # built-in voice list + per-model constraints
mimo-audio tts    --text "..." [--style "..." ] [--voice Mia] [--format wav|pcm16] [--out NAME]
mimo-audio design --desc "young male, gravelly, slow" [--text "..."] [--optimize-preview]
mimo-audio clone  --sample voice.mp3 --text "..."        # F13 SOVEREIGN gate on new voice_id
mimo-audio asr    --file audio.wav [--lang auto|zh|en] [--out transcript.txt]
```

- **Path:** `/root/scripts/mimo-audio`, symlinked to **`/usr/local/bin/mimo-audio`** → on PATH for every process.
- **Stdlib only** (urllib/wave/base64) — no pip deps in any agent home.
- **Emits a JSON receipt** on stdout: `{ok, lane, endpoint, path, bytes, duration_sec, sample_rate, usage, …}`.
- **Auto-retries one `429`** — the lane intermittently returns `quota exhausted` even when healthy (~18% of audio calls observed 2026-09-13). A single 429 is NOT quota death.
- **Output dir:** `$MIMO_AUDIO_OUT` or `/root/forge_work/audio/`.
- **Env:** `MIMO_BASE_URL` + `MIMO_TOKEN_PLAN_API_KEY` (alias `MIMO_API_KEY`), both exported by `/etc/profile.d/mimo-tokenplan.sh` — verified inherited by login, non-login, and `env -i` shells.

> Why a CLI and not just the curl in "Quick recipe" below: FED cannot carry audio (the audio ids are not exposed there at all — `mimo-v2.5-asr` via FED → HTTP 400), so audio *must* ride the direct lane, and hand-rolled base64 plumbing in every agent is exactly how silent drift starts.

### Skill visibility — now 11 homes (was 9)

Supersedes the roster printed earlier in this file. Added 2026-09-13: `/root/.qwen/skills/mimo-audio`, `/root/A-FORGE/skills/mimo-audio`.

1. `/root/AAA/skills/mimo-audio` (canonical, physical)
2. `/root/.agents/skills/mimo-audio`
3. `/root/.claude/skills/mimo-audio`
4. `/root/.codex/skills/mimo-audio`
5. `/root/.grok/skills/mimo-audio`
6. `/root/.gemini/skills/mimo-audio`
7. `/root/.kimi-code/skills/mimo-audio`
8. `/root/.config/opencode/skills/mimo-audio`
9. `/root/.arifos/agents/opencode/skills/mimo-audio`
10. `/root/.qwen/skills/mimo-audio`
11. `/root/A-FORGE/skills/mimo-audio`

### Contract deltas from the vendor docs (2026-09-13)

Sources: [Speech Synthesis v2.5](https://mimo.mi.com/docs/en-US/quick-start/usage-guide/audio/speech-synthesis-v2.5) · [Speech Recognition](https://mimo.mi.com/docs/en-US/quick-start/usage-guide/audio/Speech-Recognition)

- **`mimo_default` is cluster-dependent** — China cluster resolves it to 冰糖, all other clusters to Mia. Pin an explicit voice id for reproducible output.
- **`optimize_text_preview` (voicedesign only)** — when `true` the assistant message may be **omitted**; the model polishes the broadcast text itself. Now exposed as `--optimize-preview`.
- **Streaming availability is per-model:** `mimo-v2.5-tts` has **real low-latency streaming** (vendor: "restored"); `voicedesign` and `voiceclone` are **compatibility-mode only** — they buffer and flush once after inference completes. For streaming you MUST use `format: "pcm16"` (24 kHz PCM16LE mono) to splice chunks.
- **Placement rules restated by the vendor:** spoken text goes in the **assistant** message; style instructions go in the **user** message (optional for tts/clone, **required** for voicedesign); user content never appears in the synthesized speech.
- **Style control is two-channel:** natural language in the user message, **and** inline tags in the assistant message. Style prefix accepts half-width `()`, full-width `（）`, or `[]`. Singing requires `(唱歌)` / `(sing)` / `(singing)` at the very start; CN lyrics synthesize best.
- **ASR** — wav/mp3 only (mime `audio/wav`, `audio/mpeg`|`audio/mp3`), base64 ≤ 10 MB, `asr_options.language` ∈ {auto, zh, en}. Vendor claims native **Cantonese / Wu / Minnan / Sichuan** and lyrics-with-background-music. That is *Chinese* dialect coverage — it does **not** extend to Malay; BM fidelity guidance (prefer dashscope/GLM) is unchanged.
- **Billing:** TTS series free for a limited time; ASR billed per audio-hour (30M credits/h on the Token Plan).

### Reference scripts fixed

`references/official/scripts/mimo_tts{,_voicedesign,_voiceclone}.py` hardcoded the **PAYG** host (`api.xiaomimimo.com`) while reading `MIMO_API_KEY` — which on af-forge is the `tp-` token-plan alias, i.e. a guaranteed cross-lane 401. All three now honour `MIMO_BASE_URL` (vendor's PAYG URL retained as the fallback default) and accept either key name.

---

## APEX-ZEN + arifFlow + Reality Graph wiring — v2 CLI (2026-09-13)

Directed by F13: *"apex-zen all audio with somatic intelligence and make sure its arifFlow and
reality graph to all"*. Full record: `/root/AAA/knowledge-graph/audio-intelligence-map.md`.

### Verbs (all on PATH as `mimo-audio`)

| Verb | Model | Lane character | Bills |
|---|---|---|---|
| `tts` | mimo-v2.5-tts | built-in voice synthesis | **free** (limited window) |
| `design` | mimo-v2.5-tts-voicedesign | voice from text description | **free** |
| `clone` | mimo-v2.5-tts-voiceclone | voice from wav/mp3 sample — **F13 SOVEREIGN gate** | **free** |
| `asr` | mimo-v2.5-asr | **transcribe** (wav/mp3, ≤10 MB b64) | 30M credits/audio-hour |
| `understand` | **mimo-v2.5** | **reason ABOUT audio** — mp3/wav/flac/m4a/ogg, URL ≤100 MB or b64 ≤50 MB | billed as tokens |
| `voices` / `doctor` | — | introspection | free |

`asr` and `understand` are **different capabilities**, not two names for one thing: `asr` returns a
transcript; `understand` answers a *question about* the audio (content, speakers, tone, emotion,
events). Vendor page: [audio-understanding](https://mimo.mi.com/docs/en-US/quick-start/usage-guide/multimodal-understanding/audio-understanding).

Token estimate for `understand` = **duration_seconds × 6.25**. Cross-checked live: 1.92 s → est 12.0,
actual `audio_tokens` 13; 3.36 s → est 21.0, actual 22.

### Every step emits an arifFlow receipt (L1 metabolism)

Schema-conformant to `/root/arifFlow/spec/FLOW_RECEIPT_v1.md` — `receipt_id` (UUIDv4), `created_at`,
`step_type`, `risk_class`, `step_number`, `cost_ns`, `epistemic_label`, `floor_verdict`,
`cooling_decision`, `payload`.

- `tts` / `design` / `clone` → `Execute` / **`T1Mutate`**
- `asr` / `understand` → `Verify` / **`T0Observe`**

Verified persisted to `/var/lib/arifflow/receipts.jsonl`. If the daemon is down the verb still runs
and reports `rejected`/`unavailable` **inside the artifact** — never silently dropped.
`gate()` exists against `/check` but runs **advisory** (non-blocking); flipping it to blocking is a
deliberate one-line decision left to the FED owner.

### Reality Graph — L1 only, and why

Reality Graph = L0 ledger + **L1 arifFlow** + L2 Witness Graph (FalkorDB) + L3 Qdrant. This tool
writes **L1**. It does **not** write L2, because `REALITY_GRAPH.md` §6 guardrail 4 is binding:
*"every edge cites `vault_seq` or it does not exist"* — and the belief→seq linkage patch is STAGED,
not deployed. Projecting today would fabricate unanchored edges. **Claimed ≠ running.**

### Somatic seam — `understand --somatic`

Emits a `somatic_proxy` block that is **deliberately incomplete**: `derived_state` is `null` and
`NOT_MEASURED` lists `wpm · pitch_mean_hz · hesitation_ms · rms_variance`, because those require
**DSP** which this tool does not do. What it can honestly supply: `duration_sec_OBS`,
`sample_rate_OBS`, and the model's reading as `model_reading_INT` (F7 cap 0.75).

The constraint this creates: **no DSP pass ⇒ no `music_intent` emission.** A guessed somatic state
would route straight into audio the sovereign hears; F1 fail-closed beats a confident guess.

### Epistemic labels on every field

- **OBS** — bytes, duration, sample_rate, channels, API usage counters, `audio_tokens`, source bytes
- **DER** — `token_estimate_DER` (s × 6.25), `cost_DER_credits`
- **INT** — `transcript_INT`, `content_INT`, `model_reading_INT` (F7 ≤ 0.75)

### To every agent

Env inherited by login / non-login / `env -i` shells; binary on `PATH`; skill resolvable in
**11 homes**. An agent in any cwd can call `mimo-audio understand --file X --somatic` and receive
an APEX-ZEN-labelled, arifFlow-metabolised result with no prior knowledge of the MiMo contract.

---

## FED federation state — MiMo (2026-09-13)

### What is federated, and where

| Layer | MiMo surface | Status |
|---|---|---|
| **litellm `model_list`** (`:4013`) | `mimo-v2.5`, `mimo-v2.5-pro` (text/omni) | **LIVE** — HTTP 200, "PONG" |
| **litellm pass-through** (`:4013/mimo/*`) | **all 6 models**, audio included | **LIVE** — verified below |
| Front door `:4000` (HAProxy) | answers from **KVM4**, not this litellm | ⚠️ does NOT reach the pass-through — see caveat |
| Direct lane (`$MIMO_BASE_URL`) | all 6 models | LIVE (primary documented path for audio) |

### How to call MiMo through FED

```bash
# text/omni — normal model-name routing
POST http://127.0.0.1:4013/v1/chat/completions   {"model":"mimo-v2.5", ...}

# ANY of the 6 models incl. audio — pass-through (bodies carried verbatim)
GET  http://127.0.0.1:4013/mimo/models
POST http://127.0.0.1:4013/mimo/chat/completions  {"model":"mimo-v2.5-tts", "audio":{...}}
```

### Why a pass-through exists at all

litellm's translator **cannot** carry MiMo audio responses — `message.audio` is not part of its
`Message` schema. **Reproduced live 2026-09-13 on litellm 1.102.0** via the pre-existing
`fed/audio-voiceclone-restricted` route:

```
litellm.InternalServerError ... convert_dict_to_response.py:681 Message(...) → HTTP 500 (15.7 s)
```

`model_list` therefore federates **text/omni only**. The four audio ids ride
`general_settings.pass_through_endpoints` → `/mimo/*`, which bypasses the parser entirely.

**Verified through the pass-through:** TTS → 200, **215,084-byte 24 kHz WAV**, 199 tokens (the exact
body that used to 500). ASR → 200 with transcript. `GET /mimo/models` → 200, all 6 ids.

**Explicit trade-off:** a pass-through is a raw authenticated proxy — it bypasses litellm routing,
spend logs and cost tracking. Credit accounting for those calls comes from MiMo's own console, not
from FED spend logs.

### ⚠️ Front-door caveat (owner decision, not taken)

`:4000` requests **never reach this litellm**. Proven: a marked request to `:4000/mimo/models`
produced **0 hits** in the local litellm access log while the same request to `:4013` produced a
200. HAProxy's front door is answering from KVM4 (`fed_primary`).

Two pre-existing defects surfaced while establishing that:

1. **Truncated key in the front-door config.** `haproxy.cfg:26` injects
   `Authorization: "Bearer sk-lit...c8ac"` — a *partial/placeholder* literal in the LIVE file. Any
   request arriving without its own Authorization header gets a broken key; the same string is used
   for the `zen_local` health check.
2. **No stats socket**, so backend health cannot be read; `zen_local` may be marked DOWN by that
   failing health check, which would explain the fallback to `fed_primary`.

Fixing these means writing a real secret into the front-door config and/or re-pointing routing —
a front-door architectural change. **Not done unilaterally.** To expose the pass-through at `:4000`,
either repair the HAProxy↔`:4013` path, or replicate `pass_through_endpoints` on KVM4's config.

### The other direction — the i-ARIF ban is lifted

F13 lifted the MiMo↔i-arif ban 2026-09-13 (*"awat hang ban. bagi ada la"*). **Root cause corrected by
the sovereign:** the 08-30 failure was **not the model** — it was the federation's own **MD files /
system prompts (shadow)**. See `FED_GENESIS_MAP.md` → "UNBAN era".
