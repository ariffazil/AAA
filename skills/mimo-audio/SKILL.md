---
name: mimo-audio
description: "FEDERATED Xiaomi MiMo v2.5 audio intelligence — TTS, ASR, voice design, voice clone (F13-gated)."
---

# MiMo Audio — federated organ (AAA canonical, 2026-09-07)

## 🛑 READ THIS FIRST — LANGUAGE CAPABILITY (hard-verified 2026-09-15, KVM8 af-forge)

**Raw MiMo TTS does NOT speak Bahasa Malaysia. It produces fluent-sounding garbage.**
Do not route BM/MS text to `mimo-v2.5-tts` or `mimo-v2.5-tts-voicedesign`. There is no
style prompt, no voice choice, and no `--style` value that fixes it.

Test phrase (all five lanes generated live, then transcribed by the **independent** gate
`groq-stt --lang ms`, i.e. Groq whisper-large-v3-turbo — never by MiMo's own ASR):

> TARGET: `Sini. Dekat sikit. Jangan malu. Aku dah nampak kau dari tadi.`

| lane | independent Groq transcript | verdict |
|---|---|---|
| `mimo-audio tts --voice Milo` | `Sini, teka tsikit. Jangan malu. Akuda nam pak kaudari dadi.` | ❌ BROKEN |
| `mimo-audio tts --voice Dean` | `Sini, dekat sekit. Jangan malu. Aku dah nampak kot dari tadi.` | ❌ BROKEN |
| `mimo-audio tts --voice Mia` | `Sini, dekat sakit. Jangan malu. Aku ta nampak kodari tadi.` | ❌ BROKEN |
| `mimo-audio tts --voice 苏打` | `Semi, dekat cik, zangga malu, aku, da, na, pa, kau, day, teh.` | ❌ BROKEN |
| `mimo-audio tts --voice 白桦` | `Tehya da katsite dan gaung malu akuta nampa kaudiyati.` | ❌ BROKEN |
| `mimo-audio design` (the "Penang path") | `Jadi, saya akan menghubungi saya untuk menghubungi saya.` | ❌ HALLUCINATED |
| `mimo-audio clone --sample <Malay ref>` | `Sini dekat si kecil. Jangan malu. Aku dah nampak kau dari tadi.` | ✅ USABLE |
| `edge-tts --voice ms-MY-YasminNeural` | `Sini. Dekat sikit. Jangan malu. Aku dah nampak kau dari tadi.` | ✅ EXACT |
| `edge-tts --voice ms-MY-OsmanNeural` | `Sini. Dekat sikit. Jangan malu. Aku dah nampak kau dari tadi.` | ✅ EXACT |
| `mmx speech synthesize --voice Indonesian_BossyLeader` | `Sini. Dekat sikit. Jangan malu. Aku dah nampak kau dari tadi.` | ✅ EXACT |

**Rules that follow, and they are binding:**
1. **BM text → `clone` (with a Malay reference sample), or `edge-tts` ms-MY, or MiniMax
   `Indonesian_*` voices.** The MiMo **base TTS and voicedesign lanes are English/Mandarin
   instruments** — treat raising them at BM as a known-wrong action.
2. **`voicedesign` is the WORST BM lane**, not the best. It does not merely mispronounce —
   it invents unrelated Malay. Any doc that recommends voicedesign for Penang/Malay dialect
   is wrong; see the correction recorded in `references/` and in
   `media/tts-edge-fallback/references/mimo-tts-api-quirks.md`.
3. **`clone` is good but not guaranteed exact.** The 2026-09-15 run rendered "Dekat sikit"
   as "dekat si kecil" — one word off, while the sentence stayed intact. Re-generate and
   re-gate if a word matters. Do not advertise clone as verbatim.
4. **NEVER use `mimo-audio asr` to judge BM audio quality.** It supports `auto|zh|en` only —
   **no `ms`**. It garbled the edge-tts ms-MY control (`Sini, dekat sikit, jangan manu. Akhu
   dah nampak kau dari tadi.`) that Groq Whisper transcribed **exactly**. A vendor ASR cannot
   be the witness for the vendor's own TTS anyway: that is circular. Use `groq-stt --lang ms`.
5. `mimo-audio asr` now emits a `language_caveat_INT` field on every `auto` run saying this.

**The independent gate lives at `/root/scripts/groq-stt`** (also `/usr/local/bin/groq-stt`) —
stdlib-only, no `requests` dependency, `--lang ms`. Keep ASR test clips under ~15 s; Groq is
free but MiMo ASR bills 30 M credits/audio-hour.

## ⚠️ Content filter on the clone lane — status CORRECTED 2026-09-15

`mimo-v2.5-tts-voiceclone` has been observed returning, with **no audio**:

```json
{"finish_reason": "content_filter",
 "message": {"content": "The request was rejected because it was considered high risk"}}
```

**Honest status: UNRESOLVED — not a settled "no" and not a settled "yes."** An earlier note in
this skill claimed the filter "did not reproduce"; a later report held it live. On 2026-09-15 an
explicitly flirty Malay line was sent to **both** the clone lane and the base TTS lane: both
returned **HTTP 200 with full audio**, so the filter did **not** reproduce on that input. The
trigger condition is therefore **unknown**, and the honest label is *intermittent / input-dependent*.

What was actually fixed is the **failure mode**, which was worse than the filter: a refusal used
to surface as a generic `no audio in response` truncated to 300 characters and exit code 2 —
indistinguishable from a transport bug, so agents retried the same rejected text in a loop. The
CLI now emits a distinct, greppable, **non-retryable** condition:

```json
{"ok": false, "error": "CONTENT_FILTER", "finish_reason": "content_filter",
 "vendor_message": "The request was rejected because it was considered high risk",
 "guidance": "The vendor refused this text on the audio lane. Do NOT retry the same text ..."}
```
exit code **3**. Handle it: rewrite the text, or route to edge-tts / MiniMax. Do not retry.

Status: LIVE — re-verified end-to-end 2026-09-13 (FI-008 embed audit). TTS = 0 credits while the free window lasts.
**Hardened 2026-09-15** — see "CLI defects fixed 2026-09-15" at the end of this file.
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

---

## CLI defects fixed 2026-09-15 (KVM8 af-forge, `TELINGA` hardening)

Every defect below was **reproduced live, patched in `/root/scripts/mimo-audio`, and
re-verified by re-running the failing command**. `mimo-audio` is the single command every AAA
agent uses; each of these was silently costing receipts, credits, or trust.

| # | defect (reproduced) | fix | re-verify |
|---|---|---|---|
| 1 | **ASR cost meter blind.** `cost_DER_credits: null`, `audio_seconds_OBS: null` on *every* ASR call. The CLI read `usage.prompt_tokens_details.seconds`; the API returns `seconds` at the **top level** of `usage`. | read `usage["seconds"]`, keep the old path as fallback | 8 s clip → `cost_DER_credits: 66667`, `audio_seconds_OBS: 8` |
| 2 | **`--out` with a subdirectory crashed.** `--out probes/x` joined onto `$MIMO_AUDIO_OUT` without creating the dir → `FileNotFoundError`; `--out /abs/x` silently escaped `OUT_DIR`. | `out_path()` honours absolute and separator-bearing paths and creates the parent | `--out verify/sub/dir_test` → `.../verify/sub/dir_test.wav` (69 164 B) |
| 3 | **`--no-flow` was dead.** Every subparser did `set_defaults(no_flow=False)`, and argparse applies subparser defaults *last* — so the global flag was overwritten and never took effect. | subparsers no longer touch `no_flow` | `--no-flow` → no `arifflow` key; control → `ingested` |
| 4 | **arifFlow receipts silently lost under load.** Daemon returns `HTTP 400 {"error":"EOF while parsing a value at line 1 column 0"}`. Isolated live: **20/20 sequential → 200**, **27/30 concurrent (8 workers) → 400 EOF**. Daemon-side concurrency defect; a *body shape* bug is ruled out (sequential is perfect). | 3 attempts with 0.25/0.7/1.5 s backoff on the 400-EOF signature only | 40 concurrent → **40 `ingested`, 0 lost** (11 recovered by retry) |
| 5 | **`clone` had no `--text-file`** — long-form text had to be shell-quoted from a file (the classic silent-truncation pattern). `mmx` has the flag; this CLI did not. | `--text-file` added to `tts`/`design`/`clone`; `-` reads stdin | `clone --text-file /tmp/bm_short.txt` → 138 284 B WAV; `--text-file -` piped → works |
| 6 | **`content_filter` was indistinguishable from a transport bug.** Generic `no audio in response`, 300-char truncation, exit 2 → agents retried a deliberate refusal. | dedicated `error: "CONTENT_FILTER"` receipt + exit code **3** + do-not-retry guidance | handler executed against the exact captured vendor body → exit 3, `error=CONTENT_FILTER` |
| 7 | **`understand` returned `ok: true` with an EMPTY answer** while billing. With the default `--max-tokens 1024` the reasoning channel consumed the whole budget: `completion_tokens=1024`, `content_len=0`, `reasoning_len 3632–4038`, reproduced **3/3 runs**. | default `--max-tokens` → **4096**; empty `content` now recovers from `reasoning_content` labelled `content_INT_source: RECOVERED_FROM_REASONING_INT`; a truly empty answer sets `ok: false` | `understand` → `content_len 1578`, `finish_reason stop`, `content_INT_source message.content`, `completion_tokens 1960` |
| 8 | **`clone` accepted `flac/m4a/ogg` reference samples** (`TTS_MIME \| UND_MIME`), formats the vendor lane rejects. | reference sample restricted to `wav\|mp3` (`ASR_MIME`) | lane-level; no regression on the wav path |

### Not reproduced — do not repeat the claim

- **`mmx speech synthesize` does NOT require `--base-url`.** It succeeded **without** it, in a
  clean `env -i` shell with only `MINIMAX_API_KEY` set, and with `MINIMAX_API_HOST`/
  `MINIMAX_BASE_URL` present. `--base-url` is a **global** `mmx` flag (documented in `mmx --help`,
  *not* in `mmx speech synthesize --help`) and it parses fine both before and after the subcommand.
  If an `mmx` call 404s, the cause is elsewhere — check the key and the model id.
- **The voiceclone `content_filter`** — see the corrected section above. Intermittent; the
  failure *mode* is what got fixed.

### Repro harness

`/root/forge_work/harden-20260915/audio/selftest-audio-stack.sh` re-runs the whole `TELINGA`
sweep (all lanes, the BM pronunciation gate, the CLI defect regressions). Run it after any
change to `mimo-audio`, `groq-stt`, the TTS skills, or the arifFlow daemon.
