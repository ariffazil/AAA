---
id: voice-lane
name: voice-lane
description: "Use when a voice note / TTS render is requested, a TTS lane must be chosen or failed over, a rendered take must be verified, or a voice must be designed/cloned."
version: 2.0.0
owner: AAA
category: voice-stack
tags: [tts, voice, audio, asr, roundtrip, verification, fallback, lane, malay, bm, penang, dialect, sovereign, offline, minimax, mulerouter, edge-tts, piper, f5-tts, mimo, qwen, cosyvoice, corpus, consent, whisper, ogg, telegram]
floor_scope: [F1, F2, F4, F6, F7, F13]
autonomy_tier: T1
supersedes:
  - sovereign-tts-lanes
  - tts-edge-fallback
  - qwencloud-audio-tts
  - audio-roundtrip-diagnostics
  - tts-roundtrip-scoring
  - voice-lane-verification
  - minimax-voice-design-prompts
  - nusantara-acoustic-infrastructure
retired_into: /root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/voice-lane/
metadata:
  hermes:
    tags: [audio, tts, voice, verification, lane-router]
    related: [hermes-voice-config, nusantara-voice-stack, machine-read-verification, abang-sado-creative-lane]
    forged: 2026-09-19
    provenance: "Merge of eight lane-selection / fallback / verification skills (F13 in-chat order 2026-09-19, namespace-entropy collapse). Every command, provider name, parameter, threshold and failure signature of the eight source bodies is preserved here. Originals retired, never deleted."
capability_tier: fed-realtime-voice
ecology_state: WARM
---

# voice-lane — the canonical TTS/voice lane router, verification discipline, and voice-design contract

This is the ONE operational skill for synthetic voice. It has three parts and you must use them in order:

1. **§1 LANE ROUTER** — which provider for which job, the fallback order, the exact invocation for every lane.
2. **§2 VERIFICATION DISCIPLINE** — round-trip scoring, what a failed take looks like, and the witness rule (a machine read must be verified, never trusted).
3. **§3 VOICE DESIGN + §4 CORPUS/CONSENT** — prompt design, cloning/consent, dialect corpus law.

**Superseded skills:** `sovereign-tts-lanes` · `tts-edge-fallback` · `qwencloud-audio-tts` · `audio-roundtrip-diagnostics` · `tts-roundtrip-scoring` · `voice-lane-verification` · `minimax-voice-design-prompts` · `nusantara-acoustic-infrastructure`. An agent that remembers an old name lands via the table in **§9**. The retired bodies live at `/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/voice-lane/`.

**Load these two directly — they are NOT merged here and remain authoritative for their own content:**

- `/root/AAA/skills/domains/general/workshop/voice-stack/hermes-voice-config/SKILL.md` (≈30 KB) — live TTS config SOT, provider wiring, DSP.
- `/root/AAA/skills/domains/general/workshop/voice-stack/nusantara-voice-stack/SKILL.md` (≈47 KB) — engine ceilings, corpus, the general ASR/hallucination map §12.

Where a rule here and a rule in a deeper lane-specific skill disagree, the deeper lane-specific skill wins for its own artefacts.

---

## 1. LANE ROUTER — pick the lane, then invoke it

### 1.0 Classify the job first

| Job class | Route to |
|---|---|
| Conversational BM/rojak voice note (default) | Tier 1 rented lane: `mulerouter` (MiniMax 2.8 HD) → `edge-tts` free fallback |
| Highest-quality metered render, final take | MiniMax `speech-2.8-hd` via MuleRouter (`mulerouter-tts.py`) |
| English production quality | OpenAI `gpt-4o-mini-tts` (quota-billed) |
| Standard BM, free, always alive | `edge-tts` `ms-MY-OsmanNeural` / `ms-MY-YasminNeural` |
| Voice must not depend on a rented provider / CPU-only / zero quota | Piper (`id_ID-news_tts-medium`, MIT) |
| Clone of one specific voice, sovereignty-critical, time is free | F5-TTS (CPU ~4–5 min/utterance) |
| Penang / northern dialect accent | MiMo `mimo-v2.5-tts-voicedesign` with a Penang description |
| User explicitly asked a Qwen seat / QwenCloud API TTS | Qwen `qwen3-tts-flash` HTTP / CosyVoice WS — but route BM to edge anyway (§1.3.7) |
| Voice-design a NEW persona voice | MiniMax `/v1/voice_design` (§3.1) |
| Long (>2 sentence) or heavy-news BM note needing prosody | Nusantara Prosody Engine v3 (`nusantara_tts.py`) (§3.3) |
| Text full of shortforms / code-switch before synthesis | Rojak preprocessor (`rojak_tts.py`) (§4.2) |

### 1.1 The lane table (decision tree, 2026-07-30)

| Provider | Free? | Malay quality | Penang dialect | Singing | Voice cloning | Best for |
|---|---|---|---|---|---|---|
| **`mulerouter` (MiniMax 2.8 HD)** | ❌ billed | ✅✅ HD, emotion control | ❌ | ❌ | ❌ | **Primary — highest quality, one key, one bill** |
| `edge` (ms-MY-Osman) | ✅ | Standard BM, not Penang | ❌ Standard BM only | ❌ | ❌ | Quick free fallback, standard Malay |
| `openai` (gpt-4o-mini-tts) | ❌ quota-billed | OK | ❌ | ❌ | ❌ | Production quality English |
| `mimo` (Xiaomi V2.5) | ✅ (limited time) | Good — voice design supports Penang description | ⚠️ achievable via description, not guaranteed | ✅ (built-in voices only) | ✅ (voiceclone model) | Custom voice, Penang-style |
| `elevenlabs` | ❌ quota-billed | OK multilingual | ⚠️ via voice cloning | ❌ | ✅ | Highest quality, paid |
| `qwen-audio-3.0-tts-plus` (Token Plan) | ❌ credits | ❌ NO Malay — zh+en system voices only | ❌ | | ❌ | Qwen-seat TTS when asked; route BM to edge anyway |

**Default chain:** `mulerouter` (MiniMax 2.8 HD via MuleRouter) → `edge-tts` (free fallback).

### 1.2 Fallback order — the wired chain

`/root/AAA/engines/iarif_tts_pipeline.sh` failover chain (repaired 2026-09-18):

```
MiniMax (Tier 1, rented) → PIPER (sovereign, offline, zero-quota) → edge-tts → MiMo (last resort)
```

The rung below MiniMax used to be MiMo, which is falsified for BM — so the first fallback silently shipped mangled speech in a different voice. Every rung now writes `IARIF_ENGINE=` to stderr so the delivery message can name what actually spoke.

Override points: `IARIF_PIPER_BIN` (default `/usr/local/bin/piper`), `IARIF_PIPER_MODEL` (default `/root/forge_work/piper-sovereign/id_voice.onnx`).

**Before spending a metered lane, probe it:**

```bash
bash /root/AAA/engines/tts_lane_status.sh          # human; exit 3 = Tier 1 shut, use Piper
bash /root/AAA/engines/tts_lane_status.sh --json
```

**Lane-switch prohibition:** a plan/credit boundary is a boundary, not a defect. When a provider returns a usage-limit error, classify it and stop — do **not** swap in a substitute voice to keep the lane moving, because a swapped timbre breaks continuity silently while every text gate still passes. Re-probe the lane later instead of assuming it is still down.

### 1.3 Exact invocation, per lane

#### 1.3.1 edge-tts (free, local, always alive)

```bash
edge-tts --text "Your text here" --voice ms-MY-OsmanNeural --write-media /tmp/tts_output.mp3
```

With rate/pitch tuning:

```bash
edge-tts --voice "ms-MY-OsmanNeural" --rate "+5%" --pitch "+0Hz" --text "..." --write-media /tmp/output.mp3
```

Setup (one-time): `pip install edge-tts --break-system-packages`

Malay voices: `ms-MY-OsmanNeural` (male, warm, conversational — good for trading/analysis), `ms-MY-YasminNeural` (female, friendly, clear).
English voices: `en-US-GuyNeural` (male), `en-US-JennyNeural` (female).

Long-text form (file input):

```bash
edge-tts --voice ms-MY-OsmanNeural --rate -10% --pitch -5Hz --file /tmp/content.txt --write-media /tmp/voice.ogg
```

Native OGG: `--write-media /tmp/file.ogg` produces Opus-in-OGG that Telegram renders as a voice bubble. No ffmpeg step needed. Confirmed working.

**CLI gotcha:** `--pitch -15Hz` (space) fails; use `--pitch=-15Hz` or the Python API.

#### 1.3.2 MuleRouter MiniMax Speech 2.8 HD

```bash
# load the MuleRouter key-env into the environment first, then:
source "$MULEROUTER_KEY_ENV" && /root/HERMES/scripts/mulerouter-tts.py \
  --text "Assalamualaikum" --voice man --malay --output /tmp/voice.mp3
```

The key-env file's exact path is preserved verbatim in the retired copy at `.../merges/voice-lane/tts-edge-fallback/SKILL.md` (this skill quotes it through an environment variable because the literal path trips the credential-path write gate). Load it with the local credential loader, never inline a value.

Confirmed voices: `Wise_Woman` (warm, wise female — general/conversational BM), `woman` (standard female — natural, clear), `man` (calm male — analysis, news, trading briefings).

**Malay mode** (`--malay`): auto-selects `man` voice + 0.95x speed for BM clarity.

**Integration:** when the user requests voice, try `mulerouter-tts.py` first (not via the `text_to_speech` tool, which routes through mimo). Same API key as chat — no separate billing.

#### 1.3.3 Piper (sovereign, offline, MIT, ~1.3–1.8 s on CPU)

Piper's library has **54 languages and NO `ms`**. Verified live:

```
HTTP 404  .../rhasspy/piper-voices/resolve/main/ms/ms_MY/
{"error":"ms does not exist on \"main\""}
```

SEA languages present: `id`, `ja`, `ko`, `th`, `vi`, `zh`. Use **Indonesian** — it reads BM natively (same phoneme-overlap principle as the MiniMax Indonesian voices).

```bash
D=/root/forge_work/piper-sovereign
B="https://huggingface.co/rhasspy/piper-voices/resolve/main/id/id_ID/news_tts/medium"
curl -sL "$B/id_ID-news_tts-medium.onnx"      -o $D/id_voice.onnx
curl -sL "$B/id_ID-news_tts-medium.onnx.json" -o $D/id_voice.onnx.json
echo "Aku tak tahu nak cakap apa." | /usr/local/bin/piper -m $D/id_voice.onnx -f out.wav
```

Tuning: `--length-scale` (pace, >1 slower), `--noise-scale`, `--noise-w-scale`, `--sentence-silence`.

Installed binary on KVM8: `/usr/local/bin/piper` is `piper_tts-1.8.0`, installed 2026-09-09.

**Known defect: `nak` → `na`.** One phoneme. Not yet fixed; consider pre-normalising the token or a different Indonesian voice.

#### 1.3.4 F5-TTS (the clone path)

Reference audio staged at `/root/AAA/engines/f5tts/reference.wav` (24.8 s) and `reference-10s.wav`. Module **not installed in any venv**. ~4–5 min per utterance on CPU. The only offline path that clones a specific voice. Too slow for production; correct for sovereignty-critical work.

#### 1.3.5 MiMo (Xiaomi V2.5)

Add to `~/.hermes/config.yaml` under top-level `tts:` (NOT under `providers:`):

```yaml
tts:
  provider: mimo
  mimo:
    api: https://token-plan-sgp.xiaomimimo.com/v1
    key_env: MIMO_API_KEY
    model: mimo-v2.5-tts-voicedesign
    voice: default
    sample_rate: 24000
```

Then `hermes config set tts.provider mimo`. Requires `MIMO_API_KEY` in `~/.hermes/.env` (or whichever `key_env` you declared).

Three TTS models: `mimo-v2.5-tts` (built-in voices, singing) · `mimo-v2.5-tts-voicedesign` (describe the voice in natural language, no sample) · `mimo-v2.5-tts-voiceclone` (clone from an audio sample, `data:` URI base64).

Gotchas: for `voicedesign` do **NOT** include the `audio.voice` field — returns 400 "Param Incorrect". For `voiceclone` the `audio.voice` field is REQUIRED and must be a `data:audio/<mime>;base64,<...>` URI. `audio.format` supports `wav` and `pcm16` — use `wav` for delivery. Audio is base64 in `choices[0].message.audio.data`; save to disk, verify the RIFF header, then send with `MEDIA:`. Sample rate 24 kHz PCM16 mono; Telegram accepts WAV as a voice bubble. Full quirks: `.../merges/voice-lane/tts-edge-fallback/references/mimo-tts-api-quirks.md`.

**MiMo is not a BM lane at any variant** (measured): `mimo-v2.5-tts-voiceclone` captures MALE REGISTER (f0 182.9 Hz from a male reference) but mangles BM pronunciation — transcript `"Hawekaku tatoa nō kakaapa, taipi akumasi sini."` for source `"Aku tak tahu nak cakap apa. Tapi aku masih sini."` The base `mimo_default` is also female-register (230.6 Hz) and merges words (`nak cakap`→`nakakap`). The turbo Whisper engine returns the non-speech boilerplate on the clone output.

MiMo is free "for a limited time" per their docs (verified 2026-07-08) — do not promise permanent free access.

#### 1.3.6 MiniMax voice design / clone

`POST /v1/voice_design` — `prompt` (voice description) + `preview_text` (≤500 chars) + optional `voice_id` → returns custom `voice_id` + hex-encoded trial audio. A "Penang kaki" voice = one API call. Voice clone via `/v1/voice_clone` (needs the `voice_id` param — a bare file upload 400s).

**Billing trap:** audio features bill on a separate audio-subscription balance, **NOT** the general Token Plan quota — general quota can show 100% while TTS returns `1008 insufficient balance`.

**Cost warning:** "Voice will be charged upon first use."

#### 1.3.7 QwenCloud TTS (seat lane)

Two different APIs, two different scripts (the retired `qwencloud-audio-tts` copy holds the full `scripts/` + `references/`):

```bash
python3 <skill-dir>/scripts/tts.py \
  --request '{"text":"Hello, this is a test.","voice":"Cherry"}' \
  --output output/qwencloud-audio-tts/ --print-response

pip install dashscope>=1.24.6
python3 <skill-dir>/scripts/tts_cosyvoice.py --text "Hello"
```

Models: HTTP `qwen3-tts-flash` (recommended default) / `qwen3-tts-instruct-flash` (instruction-guided style). CosyVoice WS: `cosyvoice-v3-flash`, `cosyvoice-v3-plus`.
Voices: Cherry / Ethan / Serena (Qwen system voices) · `longanyang`, `longanhuan`, `longhuhu_v3` (CosyVoice verified).

Request fields: `text` (required, **max 600 chars**), `voice` (required), `model` (default `qwen3-tts-flash`), `language_type` (`Auto` for mixed), `instructions` (instruct model only), `stream`.
Response: `audio_url` (**valid 24 h — download promptly**), `audio_format`, `sample_rate` (e.g. 24000), `usage`.

Script args: `--request '{...}'` · `--file path.json` · `--output dir/` · `--print-response` · `--model ID` · `--voice NAME`.

Key compatibility: scripts require a **standard QwenCloud key** (`sk-...`). Coding Plan keys (`sk-sp-...`) cannot be used — TTS models are not available on Coding Plan. Qwen voice params are lowercase with no underscores between syllables: `longanlufeng` (male flagship), `longanlingxin` (female flagship). Old CosyVoice names (`longxiaochun`, `longshu`, `longlaotie`) and Qwen3-TTS names (Cherry, Ethan) fail `[cosyvoice:]Engine error [411]`; `_v3.6`-suffixed voices are flash-only and also 411 on plus.

**No Malay.** The seat `qwen-audio-3.0-tts-plus` has NO Malay/BM voices (catalog: docs.qwencloud.com/api-reference/speech-synthesis/qwen-audio-tts/voice-list). User asks "Malay voice" on the Qwen token plan → go straight to edge-tts `ms-MY-OsmanNeural`; say so plainly. Qwen `qwen-audio-3.0-tts-plus` on the seat WebSocket (`wss://token-plan.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`) *does* handle code-switch natively, but can die with `Throttling.AllocationQuota` across ALL seat keys simultaneously — retry next day, do not key-hop (violates sabar-retry).

Seat quota is per-key weekly: `BAILIAN_TOKEN_PLAN_API_KEY` / `QWEN_ARIFOS_API_KEY` (same key) returned 429 `Throttling.AllocationQuota` (reset 08-21 03:30 UTC) while `QWEN_TEAM_OWNER_API_KEY` still had quota for both TTS and image gen.

Error table: `HTTP 401` invalid/mismatched key · `HTTP 429` rate limited (retry with backoff) · `HTTP 5xx` server error (backoff) · `SSL: CERTIFICATE_VERIFY_FAILED` (macOS `Install Certificates.command`, else set the cert-file env var) · `URLError`/`ConnectionError` (network, set proxy env var) · `PermissionError` (`--output` to a writable dir) · `command not found: python3` → try `python`/`py -3` · `Python 3.9+ required` → upgrade.

**Credential hygiene (all lanes):** never print a credential value — check presence only ("set"/"not set", "valid"/"invalid"); never display the contents of a dotenv file; never ask the user to paste a key in chat. If a key is missing, create a dotenv placeholder and point the user at the provider console.

**Write prohibition:** never write output files into a skill installation directory or any `skills/` hierarchy — write to `./output/qwencloud-audio-tts/` (or a user-specified path). When generating multiple files in one session, append a numeric suffix (`out_1.wav`, `out_2.wav`) to prevent overwrites.

**Post-execution check:** exit 0 + valid JSON containing `output.audio` = success; non-zero exit / HTTP error / empty response / error JSON = fail. Verify the output file exists with non-zero size (`ls -la <output_dir>`). Scan stderr for `[ACTION_REQUIRED]` / `[UPDATE_AVAILABLE]` signals and act on them (see the retired copy's update-check section).

### 1.4 Quota and cap mechanics — read the cap correctly

**Do not read a MiniMax `2056` as "weekly quota gone".** The Token Plan caps `general` TWICE:

```bash
mmx quota show --base-url https://api.minimax.io
# general: current_interval_status 2 = EXHAUSTED  ← 4-HOUR window
#          current_weekly_status   1 = open, current_weekly_remaining_percent N
# video  : separate bucket (3 / 24 h, 21 / week)
```

Measured live: interval 0 %, **weekly 36 % with 3 days left**. The lane went quiet on a 4-hour cap while a third of the week sat unused.

**`general` serves BOTH `image_generation` and `t2a_v2`** — both endpoints returned the same 2056 at the same instant. Images spend the voice allowance. `video` is the only separate bucket. Model choice is irrelevant: `speech-2.8-hd`, `-turbo`, `2.6-*`, `02-*` and `2.5-hd-preview` all return 2056 identically, so the cap is account-level.

`--base-url https://api.minimax.io` is **required** for all `mmx` media commands; the default points at `/anthropic` and 404s.

**Allocation rule: *draft sovereign, seal rented.*** Iterate wording and pacing on Piper — it costs nothing and never runs out. Make every metered render the final take.

### 1.5 Offline / sovereign lanes

**INVENTORY FIRST — the phantom-absence trap.** Two complete offline TTS stacks were already installed and were declared missing because the probe checked `/usr/bin/python3` and `/root/venv` only, found no `torch`, and concluded "not available". Sweep every venv:

```bash
for p in /opt/arifos/venv/bin/python3 /root/GEOX/.venv/bin/python /usr/bin/python3; do
  [ -x "$p" ] && echo "--- $p" && $p -c "
import importlib
for m in ['torch','transformers','onnxruntime','piper','soundfile','librosa']:
    try: importlib.import_module(m); print('  ',m,'OK')
    except Exception: print('  ',m,'MISSING')" 2>/dev/null
done
# and binaries
which piper edge-tts
ls /usr/local/bin/piper 2>/dev/null
```

**Measured state (KVM8, 2026-09-18):** `/opt/arifos/venv` carries `torch 2.14.0+cu130`, `transformers`, `onnxruntime 1.28.0`, `soundfile`. `/usr/local/bin/piper` is `piper_tts-1.8.0`, installed 2026-09-09 — nine days unseen.

**Rule:** a capability may only be declared down after the inventory sweep AND an alternate-lane test. A venv you did not open is not absence.

Measured sovereign lanes on the identical test line `"Aku tak tahu nak cakap apa. Tapi aku masih sini."`:

| Lane | Engine | Voice | Round-trip | f0 | Latency | Size | License |
|---|---|---|---|---|---|---|---|
| **Piper** | ONNX VITS | `id_ID-news_tts-medium` | 91% (`nak`→`na`) | 260.5 Hz | **1.3–1.8 s** | 63 MB | **MIT** |
| **F5-TTS** | PyTorch | any reference | not run | — | ~5 min | — | MIT |
| ~~MMS-TTS-zlm~~ | ~~PyTorch VITS~~ | ~~native Malay~~ | *removed* | — | — | — | *CC-BY-NC* |

**MMS-TTS-zlm — EVALUATED AND REMOVED (2026-09-18). Do not re-propose without an F13 decision.** It was `facebook/mms-tts-zlm`, VITS, 36.3M params, 145 MB, 16 kHz, `zlm` = Malay specifically. Measured **100% round-trip** — best pronunciation of any sovereign lane tested. Removed because: (1) license `cc-by-nc-4.0` NON-COMMERCIAL — the fleet does employer work, a lane that cannot touch commercial output is a footgun; (2) f0 222–225 Hz female register, unusable for the persona lane; (3) no emotion contour — reads flat where MiniMax carries `penat`/`lembut` through pacing; (4) 16 kHz — half of MiniMax's 32 kHz, audibly thinner. Teardown receipt: `/root/forge_work/piper-sovereign/mms_teardown.py`.

**Rejected-lane rule:** a capability that was measured and then deliberately removed is *knowledge*, not a gap. Record WHY it was removed so a later session does not spend a cycle rediscovering it. Keep the finding; delete the artifact.

**Why the sovereign lane matters more than wiring a DSP pipeline:** wiring DSP (soul-envelope, WORLD stabilizer) across a cloud voice polishes a rented asset. Piper renders Malay-adjacent speech in 1.3 s on CPU, MIT, zero network, zero quota.

| Failure | Rented voice | Sovereign lane |
|---|---|---|
| Provider quota exhausted | silence | lane switch |
| Provider changes terms | silence | unaffected |
| Network down | silence | unaffected |
| Cost per render | non-zero | zero |

**Do not propose pipeline improvements around a provider without first asking why the provider is needed at all.**

**Tier restructure (proposed):**

| Tier | Voice | Engine | Sovereignty |
|---|---|---|---|
| 1 | Siti Nurhaliza (i-ARIF) | MiniMax `iarif-sovereign-v9` | rented |
| 2 | Abang Sado persona | MiniMax `abang-sado-live-v1` | rented (own voice) |
| 3 | Indonesian BM | MiniMax `Indonesian_*` | rented |
| **4** | **Sovereign-fast** | **Piper `id_ID-news_tts`** | **OWNED · MIT** |
| 5 | Clone | F5-TTS | OWNED |

**THE CTC SECOND WITNESS — check for it before claiming it is missing.** Two Whisper engines share a training prior, so their agreement is **not independent confirmation** — on pure noise both return the same fictitious Malay sentence. Absence and attribution claims need an architecture-independent witness; a **CTC** model cannot autoregressively invent fluent speech over non-speech. One was already on disk, staged 2026-09-15, unused for three days:

```
/root/audio-lane-2026-09-15/mms-1b-all/
├── onnx/model_int8.onnx     970 MB
├── vocab.json  ├── tokenizer.json  ├── config.json
└── preprocessor_config.json
```

Probed live — `inputs: ['input_values']`, `outputs: [(1, 221, 154)]`, **GRAPH INVOCABLE** via `onnxruntime` CPUExecutionProvider. The language-adapter decode step is not yet wired; the checkpoint loads and runs. **Run this probe before any absence claim on audio.**

### 1.6 Voice overrides and trigger detection

Workflow: user requests a voice message → **voice override check** → `text_to_speech` tool (configured provider) unless the override routed elsewhere → on 429/quota error or rejected quality fall back to `edge-tts` via terminal → generate → deliver with `MEDIA:/path/to/file.{mp3,wav,ogg}`.

| User signal | Route |
|---|---|
| "Nusantara mode", "suara lain", "tukar suara", "guna suara lain", "voice lain", "suara Melayu" | **edge-tts** `ms-MY-OsmanNeural` (skip mimo) |
| "elok sikit", "better quality", "yang bagus" / "yang bagus sikit" | edge-tts with `--rate "+5%"` (session-proven 2026-07-11) |
| "Penang", "suara Penang", "voice Bahasa Penang", "voice Penang" | MiMo `voicedesign` with a Penang description |
| "suara laki macho", "suara macho", "masculine voice" | always male — `ms-MY-OsmanNeural`, never YasminNeural |
| "voice mode", "voice", "dalam voice", "buat voice", "hantar voice", "TTS bahasa melayu" | default lane |

When the user says **"Nusantara mode"**, **"suara lain"**, or explicitly rejects the current voice → switch to **edge-tts** with Malay native voices. This is a strong preference signal — authentic Malay pronunciation, not AI-accented BM:

```bash
edge-tts --voice ms-MY-OsmanNeural --file /tmp/content.txt --write-media /tmp/output.mp3 --rate="-5%"
```

Don't ask which voice — default to OsmanNeural. Use `--rate="-5%"` for dense content (numbers, analysis), `--rate="+5%"` for casual/chat.

**Quality override for Malay:** when the user explicitly asks for "elok sikit" / "better quality" / "yang bagus" voice in Malay, **prefer `edge-tts` over the default mimo provider**. Session evidence (2026-07-11): user rejected mimo TTS output as low quality, then accepted Edge TTS `ms-MY-OsmanNeural` with `--rate "+5%"`. The default `text_to_speech` tool routes through mimo which can produce robotic output for long BM text.

**Converting existing text to voice** ("Voice mode" reply to a text answer already sent): take the previous text, reformat for spoken delivery (remove tables/links/formatting), generate via the configured provider, send with `MEDIA:`.

**Proactive voice offer:** when the user seems mobile (in car, parking, gym, outdoors) and the response is informational — offer ("Nak aku voice kan?") or send text + voice proactively.

### 1.7 Delivery rules

- Telegram renders **`.ogg` (Opus in OGG container)** as a voice bubble with waveform UI. **MP3 and WAV send as regular audio files — NOT voice bubbles.** Always convert for voice notes:

```bash
ffmpeg -y -i /tmp/output.mp3 -c:a libopus -b:a 32k -ac 1 /tmp/output.ogg
```

then deliver `MEDIA:/tmp/output.ogg`. Proven 2026-07-22: two BM voice notes delivered successfully as OGG voice bubbles.

- **Multi-channel delivery rule:** when voice accompanies text + chart in a briefing, send **text first → chart → voice last**. Voice reinforces; doesn't replace.
- **Skip voice when:** verdict is SABAR + state is Choppy. Text suffices for "jangan trade" alone.
- **Density:** max ~4 minutes of audio per note — split into segments if longer. Keep calls under ~5000 chars for reliability.
- **Never narrate the QC to the recipient.** Seed counts, retries, which take failed what — the requester experiences the artifact, not the search.

### 1.8 Write for speech, not text (BM voice content)

1. Remove markdown tables, symbols, links, formatting.
2. Spell out numbers naturally — "$4,120" → "empat ribu seratus dua puluh dolar"; "$4,023" → "empat ribu dua puluh tiga dolar"; "$67" → "enam puluh tujuh dolar".
3. Speak percentages — "2%" → "dua peratus"; ratios 1:2 → "satu banding dua"; RSI 63.6 → "enam puluh tiga perpuluhan enam".
4. Whole prices keep "dolar"; round to whole numbers when possible.
5. Conversational BM — "Kau" not "Anda".
6. Verbal markers — "Yang bagus dulu" / "Sekarang yang tak bagus pula" / "Kesimpulan dia".
7. Keep trading jargon English — "support", "resistance", "spread", "stop loss", "break" — BM traders expect these.
8. End with a clear action.

**Daily trader briefing template (90 s, proven 2026-07-18, SADO 8am cron):**

```bash
edge-tts --voice ms-MY-OsmanNeural --rate "+5%" --file /tmp/syed_voice.txt --write-media /tmp/syed_voice.mp3
```

1. Opening: "Abang [name], ni update gold [session]. Harga sekarang [spell out] dolar." (~10 s)
2. Cerita: 2–3 sentences on what happened (~25 s)
3. Levels: support + resistance, spelled out (~20 s)
4. Trend: EMA200 direction + RSI state (~15 s)
5. Verdict + action: SEAL/SABAR/HOLD/VOID + 1 specific trade action (~15 s)
6. Close: "Trade selamat, [name]." (~5 s)

The full template and verdict→action mapping live in the `syedos` workflow, which is **not present in the current skill library**.

### 1.9 Anti-gaslight checklist before declaring a lane dead

- Did you run `tts_lane_status.sh`? (exit 3 = Tier 1 shut, use Piper)
- Did you read `mmx quota show` interval **and** weekly, not just the 2056?
- Did you inventory every venv and `which piper edge-tts` before claiming absence?
- Did you check the staged CTC checkpoint before claiming no second witness exists?
- Did you name the engine that actually spoke (`IARIF_ENGINE=`)?

---

## 2. VERIFICATION DISCIPLINE

Load this after rendering a take and **before** declaring it clean or re-rendering it. The core discovery: a raw ~20% match on dense regional speech can be **100% after aliasing** — the take was clean the whole time, and re-rolling would have burned a clean render.

### 2.1 The metric law

**The gate is INSERTED = 0, not the raw match percentage.**

A low raw score with zero insertions is a CLEAN take. A high raw score carrying one inserted clause is a REJECTED take — an insertion means the audio says something the script never did, which is the one failure that cannot be explained by transcription surface.

Score in this order:

1. Apply the alias table (§2.2) → recompute the normalised match.
2. Read the transcript for INSERTED clauses specifically. Zero insertions = pass the hard gate.
3. Only then consider the normalised percentage: **≥95% ship · 85–95% ship if divergences are non-lexical · <85% block and re-render on another lane.**

Equivalent ladder form: ≥95% + zero INSERTED → ship · 85–95% with every divergence a known alias class → ship · <85%, or any INSERTED that is NOT a confirmed false positive → re-render.

### 2.2 The alias protocol (do this before re-rolling)

1. **Zero-alias pass.** Run the verifier with no aliases. Read the raw match, the INSERTED list, and the full transcript line.
2. **Diagnostic diff pass.** Print every divergent token pair in order (`difflib.SequenceMatcher`). Do not guess.
3. **Build the table from the diff.** One alias per class. The table IS the deliverable — it captures what this voice does to this text, and it is reusable across every later take.
4. **Re-score with the full table** — `--alias heard=written`.
5. **Judge** per §2.1.

**Direction is `HEARD=WRITTEN`.** Reversing it rewrites correct tokens into tokens the source lacks and manufactures a false FAIL whose MISSING row names a word plainly present in the transcript.

A multi-word key is legal (`--alias "tak ada=takde"`) and is the fix for token-count desync.

**Never rewrite the line to please the transcriber.** Alias real-word mishears; rewrite only a **pronunciation limit** — a word that mangles the same way on every take, including in isolation. Pre-normalising dialect into standard language destroys the register the take exists to carry, and it optimises the wrong quantity. Write the colloquial form, alias it, report the normalised figure.

**A normalised score LOWER than the raw score is the signal that the alias table itself is wrong**, not the take. Measured: 24.7% raw → 15.8% with one bad alias entry → 99.4% once corrected. Treat that inversion as a diagnostic, not a rounding error.

**An alias table is a claim about the transcriber — keep it falsifiable.** Only alias a substitution you have already seen recur across independent passes. Aliasing a real divergence away hides the exact defect the gate exists to find. For every alias, record the classes applied alongside the number, so a reader can re-derive it. **A bare normalised percentage is not auditable.**

**Alias tables are per-voice, not per-language.** Rebuild at least the desync and loanword rows for a new `voice_id`; carry over the rest as a starting point.

### 2.3 The false-FAIL classes (six in the round-trip diagnostics set, five in the scoring set — all preserved)

| Class | Example (heard → written) | Why it matters / handling |
|---|---|---|
| **Token-count desync** | `tak ada` → `takde` (one written token heard as two) | Every downstream token shifts by one and the aligner reports the whole remainder as INSERTED. A clean take collapses to ~20%. Alias the *expanded* form back to one token: `--alias "tak ada=takde"`. Multi-word alias keys work when the matcher word-bounds them |
| **Alias direction reversed** | the flag is `HEARD=WRITTEN` | Reversing it rewrites a correct heard token into one the source lacks, manufacturing a phantom INSERTED. Read the transcript before touching the line |
| English loanword | `syut` → `shoot`, `kamera` → `camera`, `fotografer` → `photographer`; `alpha` → `Alfa` | alias; never rewrite the line. ASR respells to its own orthography |
| Digit ↔ word | `11` → `sebelas`, `20` → `dua puluh`, `3` → `tiga`; `tiga`/`sepuluh` → `3`/`10` | the transcriber normalises digits while the source spells them; alias both directions |
| Slang standardisation / colloquial normalised to standard | `tahu` → `tau`, `pernah` → `penah`, `itu` → `tu`, `tidur` → `tidoq`; `mintak`/`takde`/`pastu`/`datang la` → `minta`/`tak ada`/`pas tu`/`datanglah` | alias; the dialect is the point, do not flatten it out of the source. The transcriber corrects the dialect |
| Particle / slang respell | `je`, `hang`, `tau` → `yeh`/`ja`, `Hank`, `tahu` | genuine phoneme ambiguity |
| Transcriber adds a syllable | `Bahu` → `Bahawa` | pronunciation, not content |
| **Engine inconsistency** | the SAME English word mangled two different ways inside ONE take (`somebody` → `sambodi` then `sambadi`) | one alias per instance — a single alias will not cover both, and this is an engine property, not an ASR error |

Measured on real colloquial Malay: a long take scored **66.6% raw → 99.8% normalised** with zero insertions; a short line scored **24.7% raw → 99.4% normalised** and was likewise clean. Raw percentage is not evidence of engine quality on dialect text.

**A long INSERTED list with an empty MISSING list is the signature of token-count desync, not contamination.** Fix the desync first and re-read; only then decide.

### 2.4 The timestamp gate — the verifier is not the sole witness for a tail

A transcriber can fabricate a whole sentence after the last spoken word, and a text-vs-transcript diff may still report `INSERTED: none` because the aligner matched the invented tokens loosely against real ones inside one block. **The two checks are not substitutes.** The decisive discriminator is the **timestamp**, not the text:

```bash
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 take.mp3
# then re-transcribe with word timestamps:
#   -F response_format=verbose_json  -F 'timestamp_granularities[]=word'
# compare the LAST word's end against the duration above
```

| Evidence | Reading |
|---|---|
| invented words' timestamps run **past the file duration** (measured: one ending at **117.24 s on an 87.62 s file**) | **Transcriber invention over silence.** The audio contains no such line. Do NOT cut it, do NOT report contamination |
| timestamps end at or before EOF, right where the script stopped, with real separated stamps | spent audio — hard-cut at the gap and state in the delivery line that the take is cut |
| audio energy agrees (speech ends ~0.05 s before EOF) | independent confirmation of the invention reading |

Never retract a take, and never report a checkpoint contamination, on a whole-file transcript alone.

### 2.5 Triaging a flagged token: read its OWN span before convicting it

A round-trip gate that flags an inserted word has not told you who inserted it. Two authors produce the same signature: the engine (real render-time contamination) and the transcriber (segmentation of a real word). Duration separates them — no human utterance of a word occupies ~80 ms.

```bash
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -F file=@take.mp3 -F model=whisper-large-v3-turbo -F language=ms \
  -F response_format=verbose_json -F "timestamp_granularities[]=word"
```

| flagged token's span | reading |
|---|---|
| a real span (~150 ms or more) sitting at the boundary | the engine spoke it — the take is defective, rewrite the clause and re-render |
| a **sliver** (measured: a two-word `ya bang` at **0.08 s**, wedged exactly between `puji` 5.80–6.54 and `bang` 6.62–7.12) | **transcriber segmentation of the real word's onset, not an insertion** — normalise it away and the same take reads clean with zero INSERTED |

- **Do not re-render on a sliver.** A re-roll spends a clean take and usually reproduces the same segmentation at the same boundary. The lever is the alias table, not a new render.
- **Position plus duration decide.** A stray beat at the very end carrying real separated timestamps and landing right where the line stopped is spent audio (hard-cut it, and say so). A short token mid-line at ~80 ms is a segmentation. A token whose timestamps run **past** the file duration is transcriber invention over silence — do not cut, and do not report contamination.
- **The aligner has no duration sense.** It matches tokens, not time, so its INSERTED row is a lead, not a verdict.

**Substitution vs respell:** respells normalise away (the table above). A word the script did not contain is a different event and must be isolated before it is called an insertion — slice the suspect window and re-read the slice (procedure owned by `machine-read-verification`, plus the duration-budget cross-check).

### 2.6 The witness rule

**A single pass of one model family is not a witness.** Re-running the same request, or stepping within a family (turbo → non-turbo), reproduces the same artifact.

Two Whisper engines share a training prior, so their agreement is **not independent confirmation** — on non-speech both return the same fictitious sentence. Whisper is the right tool for *"the engine mangled this"* (gross damage, both see it) but **not** for *"the engine did/did not say X"*.

For absence and attribution claims use an architecture-independent witness: a **CTC** model cannot autoregressively invent fluent speech over non-speech. Look for one already staged on disk (§1.5) before concluding a second witness is unavailable — the expensive part may already be done.

**A machine read must be verified before it is relayed or acted on.** Any ASR/OCR/vision read that will drive a decision (ship/retract/report) needs the §2.4/§2.5 adjudication, not a verdict word.

**Groq STT pitfall:** Python urllib multipart gets HTTP 403 where identical curl passes — use subprocess curl for Groq audio uploads. Add a dialect `prompt` param ("loghat utara, campur English, hang, depa, kambus") — it measurably improves Penang transcription.

### 2.7 Activating a voice: three layers, and only one of them speaks

"The voice is configured" describes three different artefacts. Say which one you changed.

| Layer | Artefact | What it proves |
|---|---|---|
| custom / non-schema keys | the assistant config, under a bespoke `voice.<lane>_locked_*` style name | **WRITTEN only.** Emits a schema warning, persists, and no runtime consumer reads it. Grep the tree for an importer before believing otherwise — a scaffold that *defines* a resolver constant is not a consumer of the key |
| provider entry | `tts.providers.<name>` (a command provider) | the route a TTS call actually takes |
| the resolver inside that provider's command | the registry that command reads (e.g. a `voice-registry.json`) | whether the id is **ALLOWED** — an unknown or REVOKED id aborts before synthesis and no file is written |

**Never report "the voice is now X" on a config write alone.** That is the claim/receipt gap: the write happened, the route did not change. Name the artefact, then render.

**Prove the route from BOTH sides, or you have proved nothing.**

- Render the intended id → confirm the engine line names it and an output file exists.
- Push an unregistered / legacy id through the **same command** → confirm the refusal (`UNKNOWN voice id … not in registry`, fail closed, **no file written**).

One render on the intended id is the happy path; it passes on a resolver that accepts everything. The refusal test is what shows the resolver is in charge. Report both, or report neither.

**Align every hardcoded id in a consumer to the registry — and keep the legacy id documented.** A constant left holding an id that is absent from the registry is a latent fail-closed abort the moment the route is wired to it; a scaffold constant can sit on an unregistered id at a different speed from the lane's registry precedent for months, unnoticed. Correct the constant, comment what it was and why it changed, and **do not delete the legacy id from the record** — its disposition (register or revoke) belongs to the human, and a silent rewrite destroys the evidence you would need later.

**Precedent beats symmetry.** When several live ids answer to one name, read the registry's own precedent field before choosing. Gates that only check the TEXT cannot tell them apart — only the timbre is wrong, and you cannot hear it.

### 2.8 Failed-take signatures catalogue

| Signature | Class | Action |
|---|---|---|
| raw score ~20% on dense regional speech, INSERTED list long, MISSING empty | **token-count desync**, not contamination | alias `--alias "tak ada=takde"`, re-score |
| normalised score < raw score | the **alias table is wrong** | fix the bad entry, re-score |
| INSERTED word with a **~80 ms sliver** span wedged mid-line | **transcriber segmentation** | normalise away; do not re-render |
| INSERTED word with a real ≥150 ms span at the boundary | **engine contamination** | rewrite the clause, re-render |
| invented words' timestamps **past the file duration** (measured 117.24 s on 87.62 s) | **transcriber invention over silence** | do not cut, do not report contamination |
| stray beat at the very end, real separated stamps, right where the line stopped | spent audio | hard-cut at the gap and state the cut in the delivery line |
| word mangled the SAME way on every take, including in isolation | **pronunciation limit** | rewrite is legal here (it is not an ASR respell) |
| at 0.85 speed `abang`→`abah`, `cakap`→`kakak`, `mintak`→`minta` | slow-speed articulation drift | load-bearing word → re-render at 0.88; incidental → alias and note |
| the SAME word mangled two ways inside one take | engine inconsistency | one alias per instance |
| engine returns 429 / 2056 / `1008 insufficient balance` / `Throttling.AllocationQuota` | boundary, not defect | classify and stop; re-probe later; never swap timbre silently |
| Whisper returns non-speech boilerplate on a clone output | hallucination signature | CTC witness; do not relay |
| config key written, schema warning emitted, output unchanged | **claim/receipt gap** | name the artefact (§2.7), wire the route, render |

### 2.9 Prosody truth — speed carries emotion, F0 does not (measured)

On a cloned voice the F0 median stayed **flat (~96 Hz) across speeds 0.85–0.90** — emotion lived in **pacing and pause**, not pitch.

| Speed | Register |
|---|---|
| ~0.90 | neutral, confident (default) |
| ~0.88 | deliberate, weighty |
| ~0.85 | most vulnerable — the mask is thinnest here |

**Never speed UP for intensity.** Escalation is slower, quieter, narrower permission — not louder.

**Slow-speed articulation drift is real:** at 0.85 final consonants degrade (`abang` → `abah`, `cakap` → `kakak`, `mintak` → `minta`). If the mangled word is load-bearing, re-render at 0.88 rather than shipping it. If it is incidental, alias it and note it — it is a voice property, not a defect.

### 2.10 Verification pitfalls (ship rules)

- **Delivery is not measured by the round-trip.** STT confirms words; it cannot assess warmth, authority, or persona fit. Ship on the text gate, judge on the ear.
- **A take at 100% can still be wrong.** Match percentage says the words are right; it says nothing about whether the speed, register, or emotion matched the brief.
- **A declaration of a pass must be made at the zoom the decision needs.** Announcing a clean take and then finding the defect on a closer look spends trust on every take after it. Run the decisive check first, then speak.
- **After a defect is fixed, re-verify the FIXED file, not the parent you already cleared.** Clearing an artefact you already cleared proves nothing about the one you are about to send.
- **Never collapse the chain into one "done".** Key written ≠ route live ≠ render produced ≠ take verified ≠ delivered. Name the position on the chain.
- **A low score is not a verdict on the engine** until the alias table has been applied and the transcript read for insertions. Reverse that order and you will re-render clean takes.
- **Never report a normalised score without the alias classes**, and never report a raw score as if it were the quality of the audio.
- **Run the full ladder and keep its output with the artefact** — duration band, ASR round-trip, normalised similarity, INSERTED/MISSING extraction, f0 family check. A verification step retyped by hand is a step that eventually goes missing, and the one that goes missing is usually the normalisation, which turns a clean take into a fake low score and can hide a real insertion inside the noise.
- **Check the channel's resolution before promising prosody control.** The free edge-tts lane emits **`SentenceBoundary` only** for its `ms-MY` voices — no `WordBoundary` events — while an English voice on the same client emits them (verified across two Malay voices). Any prosody feedback loop built on that lane therefore has sentence resolution at best, never word-level. Probe the event stream before designing against it.

---

## 3. VOICE DESIGN

### 3.1 MiniMax voice_design prompt anatomy

`voice_design` takes free-form description. Keywords alone underperform full prose. Layer 4 facets:

1. **Identity** — age range, gender, ethnicity/region
2. **Vocal quality** — pitch, resonance, breathiness, texture
3. **Accent/language** — regional flavor, native or second-language
4. **Pace + delivery** — rhythm, energy, what the voice DOES in conversation

**Template (proven hit):**

```
A mature [ethnicity] [gender] in their [age range] with a [texture], [pitch] voice. [Resonance detail]. Speaks [language] with [accent/regional detail]. Pace is [pace description], never [contrast]. Tone is [vibe], [secondary vibe] — like [concrete reference]. [Pronunciation note]. Pitch is [pitch descriptor].
```

**Example that hit (sado mature Penang BM):**

```
A mature Malay man in his mid-30s with a deep, calm, masculine voice. Slightly husky with rich bass resonance. Speaks Penang Malay with natural warmth and confident authority. Pace is relaxed and steady, never rushed. Tone is friendly but commanding — like an older brother who is respected. Slight smile in the voice. No exaggerated emotion, no theatrical delivery. Authentic Malaysian Malay accent with Penang regional flavor. Pronunciation is clear and grounded. Pitch is medium-low.
```

Generated voice ID from that prompt: `ttv-voice-2026081808404926-BdoQh6ec`.

**What NOT to do:**
- ❌ Keywords only ("male, deep, malay") — gives generic output
- ❌ Conflicting descriptors ("calm and energetic") — model picks one and ignores the other
- ❌ "Theatrical / dramatic / exaggerated" — produces over-acting voice
- ❌ Multiple accents ("American with Scottish undertones") — confuses model

**`preview_text` is critical.** It is what the model uses to render the trial sample. Make it the same accent/register as intended use, 15–30 s worth of content, showcasing the emotional range you want. `preview_text` is capped at ≤500 chars on the API.

**Voice IDs are persistent.** Once generated, `voice_id` stays in the account forever. Save them:

```python
with open("/tmp/voice-id", "w") as f:
    f.write(voice_id)
```

Reuse via `text_to_audio(voice_id="ttv-voice-...", ...)`.

**Voice cloning (separate path):** `voice_clone` takes audio file paths of the target voice (≥30 s clean sample). Use for cloning Arif's actual voice from voice notes, Syed's voice, or a fictional character voice from movie clips. Cost warning: "Voice will be charged upon first use."

### 3.2 edge-tts prosody profiles by content type

| Content type | Profile | Effect |
|---|---|---|
| Casual chat | `--rate +5% --pitch +0Hz` | Natural, conversational |
| Deep analysis | `--rate -10% --pitch -5Hz` | Authoritative, contemplative |
| Trading briefing | `--rate +5% --pitch +0Hz` | Energetic, clear for numbers |
| **Dramatic/macho (abang sado)** | `--pitch=-30Hz --rate=-12%` | Deep, dominant, alpha male presence |
| **Awek/admirer female** | `--pitch=+3Hz --rate=-8%` | Intimate, warm, slightly breathy |
| Wounded/driver persona | `--pitch=-15Hz --rate=-5%` | Subdued, melancholic, invisible observer |

**Rule:** dense/analytical content needs slower rate + lower pitch. Casual/update needs faster. Dramatic roleplay content pushes extreme pitch offsets. Shadow-mode / abang-sado register **MUST** use `--pitch=-30Hz --rate=-12%` on `ms-MY-OsmanNeural`. Don't default to the same settings for all content.

**Penang voice limitations.** `ms-MY-*` voices are Standard BM (DBP-style), not Penang. The only path to Penang accent is `mimo-v2.5-tts-voicedesign` with a description like "A 35-year-old Malaysian Chinese male from Penang, conversational casual tone, mixes English and Bahasa Melayu naturally, warm and direct, slight northern Malaysian intonation." ElevenLabs can clone a real Penang voice with a sample — slower + paid. **Honest framing beats pretending** — do not claim you will deliver Penang when the underlying model is Standard BM.

**Edge-tts prosody engine ceiling (verified):** only `<prosody pitch/rate/volume>` SSML tags are accepted on the free tier. `<break>` and `<mstts:express-as>` (chat/gentle/friendly styles) are all REJECTED — they require paid Azure. Monkeypatching `escape()`/`mkssml()` passes SSML through the text layer but the MS server still rejects unsupported tags. Multi-chunk + ffmpeg silence is the ONLY way to add breathing.

**Female voice "hantu" is structural, not fixable within edge-tts:** (1) the vocoder needs 32–64 spectral channels for female F0; (2) Yasmin = Osman + pitch offset, male prosody on a female voice; (3) the human auditory cortex is more sensitive to female pitch anomalies. True fix: GPU + F5-TTS or MiMo voiceclone with a real female sample.

**For true Penang dialect:** contour cannot change phonemes. Real path: Malaysian-F5-TTS-v3 (mesolitica, 15,631 h Malaysian-Emilia, CC-BY-NC, needs GPU). Full landscape + engine detail: `.../merges/voice-lane/tts-edge-fallback/references/nusantara-prosody-engine.md`.

**MiMo voicedesign description quality matters more than length:** 1–2 sentences with specific dialect cues ("Penang", "northern Malaysian", "conversational casual") beat a 200-word essay. Test iteratively.

### 3.3 Nusantara Prosody Engine v3 (2026-08-14)

**Root cause of "fake voice":** edge-tts has only 2 ms-MY voices (Osman/Yasmin), same neural backbone with a pitch offset, tagged "Friendly, Positive". Zero SSML style support, zero breath, zero expression on the free tier. Female voices sound "hantu" because higher F0 (~250 Hz) makes vocoder artifacts more perceptible, Yasmin = Osman with a pitch overlay (male prosody on a female voice = uncanny), and the evolved human auditory cortex triggers prediction error on flat female speech.

**Architecture (4 layers, deterministic, zero LLM, sovereign):**

```bash
python3 /root/nusantara-voice/nusantara_tts.py "text" out.ogg [mood]
# moods: neutral|berat|semangat|soal|tenang
```

| Layer | Function |
|---|---|
| L0 normalize | Phonetics (Manglish→Baku via extensible `vault/phonetics.json`), BM numbers (`num2ms` with se- prefixes: 100→seratus, 1000→seribu, 1e6→sejuta), RM prefix captured before comma-stripping, standalone `x`→`tak` with x-axis-safe regex |
| L1 plan | Chunk at commas/periods/conjunctions, classify (HEAVY/GOOD lexicons), mood sets global rate/pitch contour, heavy chunks get -12%/-8Hz delta, question terminal words split with +14Hz lift |
| L2 render | edge-tts Python API per chunk with individual rate/pitch |
| L3 stitch | ffmpeg concat + `anullsrc` silence segments: heavy=320ms, question=260ms, good=120ms, neutral=140ms |
| L4 vault | Every render saves `vault/<ts>_<hash>.ogg` + `corpus.jsonl` record (raw_text, normalized, plan, audio path). Accumulated pairs = F5-TTS training corpus |

**Key bug fixes (v3):** `\bx\b` in "x-axis" → fix: `(?<![a-zA-Z-])x(?![a-zA-Z-])`. RM prefix ordering: RM regex FIRST (captures full amount), THEN comma-stripping. se- prefixes: `num2ms` intercepts hundreds/thousands/millions positions.

**When to use:** long voice notes (>2 sentences), bad-news briefings, semangat updates. Not needed for one-liners.

**Measurement truth:** RMS stdev does NOT differentiate flat vs contoured (7.64 vs 7.32 dB, loudness normalized per chunk). Human ear = only judge. Always A/B render.

**CLI gotcha:** `--pitch -15Hz` (space) fails; use `--pitch=-15Hz` or the Python API.

---

## 4. CORPUS, DIALECT AND CONSENT

### 4.0 The acoustic deficit framing

Addresses the "Acoustic Deficit" — the structural lack of localized, high-quality TTS and STT for Bahasa Nusantara despite mature text-layer LLMs (ILMU, MaLLaM, Sahabat-AI). A nation can possess billions in GPU compute (MCMC Sovereign AI Cloud RM2B, YTL AI Cloud) yet remain "acoustically impoverished": compute is commoditized, localized labeled acoustic data is not. The "dapur tanpa beras" (kitchen without rice) paradigm. Text layer is settled; the voice layer is foreign-dependent (Edge-TTS OsmanNeural, Cartesia Sonic selling "Native Malay" voices Faiz/Aisyah back to Malaysia).

### 4.1 Corpus ingestion (the data moat)

The bottleneck is clean, labeled audio for regional dialects (Penang, Kelantan, Sarawak) and natural code-switching (rojak). HF dialect datasets have <60 downloads — the gap is real.

- **Vault:** `/root/AAA/corpus/voice/` — `raw/YYYY-MM/` + `meta/YYYY-MM/manifest.json`, sha-keyed entries.
- **Protocol:** copy (never move — F1 reversible) from the Hermes audio cache. Triad = `.ogg` + `transcript` + `meta` (speaker, dialect, consent, intent).
- **Pitfall:** **NEVER ingest agent-synthesized TTS into the human dialect corpus** — a synthetic feedback loop destroys authenticity. If an A/B sample lands in the cache, mark it `speaker: AGENT-OUTPUT, transcript_status: excluded` in the manifest (done once via a post-ingest correction script).
- **Consent labeling from day one:** `F13-sovereign-self` for Arif's own voice. If the loop ever serves other humans, the corpus must be consent-labeled per speaker or it becomes a PDPA/F6 problem.

### 4.2 The Rojak preprocessor (`/root/AAA/tools/voice/rojak_tts.py`)

Engine-level TTS cannot handle Malaysian code-switching or SMS shortforms. Five layers:

1. **Markdown/emoji strip** — engines speak asterisks/backticks.
2. **Shortform expansion** — "x"→"tak", "dlm"→"dalam".
3. **Phonetic code-switch** — "deploy"→"deploi", "bug"→"bag" (how Malaysians actually say them).
4. **Number/currency → BM words** — "RM2.5b"→"dua perpuluhan lima bilion ringgit", "15%"→"lima belas peratus".
5. **Micro-prosody** — per-sentence rate variation (long sentences slower, questions up), 180 ms inter-sentence pauses.

**CRITICAL LIMIT (user-verified 2026-08-14):** this layer changes WHAT the engine says, not HOW the engine sounds. User listened to raw vs rojak and said "still kinda the same" — correct: same OsmanNeural engine, same prosody ceiling. Text preprocessing is polish, not a voice transplant. Selling it as "the fix" overpromises; frame it as a preprocessor for ANY future engine.

### 4.3 Engine ladder — TTS

- **edge-tts** (free, always alive): `ms-MY-OsmanNeural` / `ms-MY-YasminNeural`. Baku, robotic, zero loghat. Baseline only.
- **MiniMax speech-2.8-hd** (Token Plan audio): voice design via `POST /v1/voice_design` — `prompt` + `preview_text` (≤500 chars) + optional `voice_id` → custom `voice_id` + hex-encoded trial audio. Voice clone via `/v1/voice_clone` (needs the `voice_id` param — bare file upload 400s). NOTE: audio features bill on a separate audio-subscription balance, NOT the general Token Plan quota — general quota can show 100% while TTS returns `1008 insufficient balance`.
- **Qwen `qwen-audio-3.0-tts-plus`** (Token Plan seat, WebSocket `wss://token-plan.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference`): handles code-switch natively. Can die with `Throttling.AllocationQuota` across ALL seat keys simultaneously — retry next day, do not key-hop (violates sabar-retry).
- **Cartesia Sonic**: commercial "Native Malay" (voices Faiz/Aisyah), no key on hand.
- **F5-TTS / Orpheus finetune** (mesolitica Malaysian-F5-TTS v1–v3, Malaysian-orpheus-3b): the sovereign endgame — fine-tune on own dialect corpus; a single RTX 3090/4090-class GPU (12–24 GB VRAM) is enough. Requires the corpus from §4.1.

### 4.4 STT (the ears)

- **Groq whisper-large-v3-turbo** via curl multipart — proven transcriber for the corpus. Works with `language=ms` + a dialect `prompt` param ("loghat utara, campur English, hang, depa, kambus") which measurably improves Penang transcription.
- **Pitfall:** Python urllib multipart gets HTTP 403 where identical curl passes — use subprocess curl for Groq audio uploads.

### 4.5 Consent and cloning rules

1. **Voice is biometric.** Cloning a real person's voice requires their consent; label it in the corpus manifest from day one (`F13-sovereign-self` for the sovereign's own voice; per-speaker consent labels for anyone else).
2. **Never mint a voice of a real person without an explicit grant.** The persona lane may use the sovereign's own voice (Tier 2 `abang-sado-live-v1` is "own voice").
3. **Never synthesize a human's voice into their own corpus** (§4.1) — that is the synthetic feedback loop.
4. **MiMo voiceclone / MiniMax voice_clone** take a real sample: confirm consent for the sample, and keep the sample's provenance in the corpus meta.
5. **F5-TTS training corpus** comes only from consent-labeled triads (§4.1) — accumulated pairs from the i-ARIF loop (L4 vault + `corpus.jsonl`).

### 4.6 Key facts (verified 2026-08-14, HuggingFace API)

- Malaysia text LLMs: ILMU (YTL+UM, self-reported MalayMMLU 87.20 > GPT-4o 84.97 — unverified third-party), MaLLaM 2.5 (mesolitica), Merdeka-LLM (Agmo).
- mesolitica TTS family: Malaysian-TTS-0.6B (12k dl) / 1.7B (290 dl) / 4B, F5-TTS finetunes, Orpheus-3B — heroic, underfunded.
- Singapore benchmark: IMDA National Speech Corpus → MERaLiON-AudioLLM (21k downloads, WER 0.05 local). MNSC partition table sums ~10.6k hours; "260k hours" claims circulating are unverified inflation — do not quote.
- Sarawak SAIC + FLock.io: federated learning for Iban/Bidayuh/Sarawak Malay — raw audio never leaves the device.
- Groq free tier hosts Orpheus TTS (English/Arabic only as of 2026-08) — watch for Malay addition.

**Macro strategy (if drafting national policy):** (1) National Speech Corpus (100k+ hours, all dialects, gamified gotong-royong collection via existing national apps). (2) Sovereign open TTS on MCMC cloud — fund a mesolitica/UM consortium, F5-TTS/Orpheus finetune, 3–5B params. (3) Code-switching as first-class syntax in evaluation benchmarks.

**Micro strategy (i-ARIF loop — proven live):** every voice note in the Telegram loop = Penang dialect data at zero marginal cost. Ingest + transcribe triads accumulate the corpus nobody else has. 12 months of casual voice notes → proprietary dialect moat → fine-tune when GPU access arrives.

---

## 5. Pitfalls (cross-lane)

- **`/opt/arifos/venv` has a cffi version mismatch** (2.1.1 API vs 2.1.0 `_cffi_backend`), which breaks `librosa` import there. Use system `python3` for librosa, `/opt/arifos/venv/bin/python3` for torch/transformers.
- **MiniMax `status 2056`** = Token Plan weekly/interval quota, NOT an auth failure. The key is valid.
- **`--base-url https://api.minimax.io` is required** for all `mmx` media commands; the default points at `/anthropic` and 404s.
- **Piper needs its `.onnx.json` beside the `.onnx`** — the model alone fails.
- **MiMo is not a BM lane at any variant** (§1.3.5).
- **edge-tts character limit:** handles long text well, but keep under ~5000 chars per call for reliability.
- **File cleanup:** `/tmp/` files are ephemeral — fine for one-shot delivery.
- **Telegram voice:** `.ogg` = voice bubble; MP3/WAV = regular audio file (§1.7).
- **"Penang voice" expectation management:** edge-tts cannot do Penang. Honest framing beats pretending.
- **MiMo is free "for a limited time"** (verified 2026-07-08). Don't promise permanent free access.
- **Never narrate QC to the recipient** (§1.7).

---

## 6. Reference files

Retired-but-preserved (moved 2026-09-19, still readable at their new paths). Base prefix: `/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/voice-lane/`.

| Reference | Path under the base prefix |
|---|---|
| MiMo V2.5 TTS API quirks (full) | `tts-edge-fallback/references/mimo-tts-api-quirks.md` |
| Arif voice-note proxy pattern (third party in the room) | `tts-edge-fallback/references/arif-voice-note-proxy.md` |
| edge-tts SSML ceiling | `tts-edge-fallback/references/edge-tts-ssml-ceiling.md` |
| Nusantara prosody engine landscape | `tts-edge-fallback/references/nusantara-prosody-engine.md` |
| QwenCloud TTS scripts + guides (`scripts/tts.py`, `tts_cosyvoice.py`, `gossamer.py`, `qwencloud_lib.py`, `api-guide.md`, `cosyvoice-guide.md`, `execution-guide.md`, `prompt-guide.md`, `codingplan.md`, `agent-compatibility.md`, `sources.md`, `custom-oss.md`) | `qwencloud-audio-tts/` |
| Acoustic sovereign strategy (macro/micro blueprint) | `nusantara-acoustic-infrastructure/references/acoustic-sovereign-strategy.md` |
| Voice-loop pipeline (vault layout, tool contracts, API schemas) | `nusantara-acoustic-infrastructure/references/voice-loop-pipeline.md` |

Live, not merged (load directly):

| Skill | Path |
|---|---|
| `hermes-voice-config` — live TTS config SOT, provider wiring, DSP, fallback chain | `/root/AAA/skills/domains/general/workshop/voice-stack/hermes-voice-config/SKILL.md` |
| `nusantara-voice-stack` — engine ceilings, corpus, §12 general ASR/hallucination map | `/root/AAA/skills/domains/general/workshop/voice-stack/nusantara-voice-stack/SKILL.md` |
| `machine-read-verification` — hallucination signatures, slicing, abstention rules | inside `verification-discipline` |
| `abang-sado-creative-lane` — persona lane line craft, prompt shapes, full take gate | workshop/creative-design |

---

## 7. Relationship to other skills

| This skill owns | Other skills own |
|---|---|
| Which lane, how to invoke it, how to fail over | `hermes-voice-config` — provider config, DSP, live SOT |
| Round-trip scoring, alias tables, false-FAIL classes, thresholds | `machine-read-verification` — the general ASR/OCR hallucination case, slicing, abstention |
| Activation proof (three layers, refusal test) | `hermes-voice-config` — the wiring itself |
| Voice design prompts, preview_text law, clone cost | `minimax-voice-design-prompts` (absorbed here) |
| Corpus ingestion, dialect strategy, consent labels | `hermes-voice-config` consent registry, WELL consent protocol |
| BM prosody profiles, number spelling, OGG delivery | `abang-sado-creative-lane` — persona line craft and full take gate |

---

## 8. The chain (never collapse it)

```
lane probed → lane chosen → render produced → route verified → take scored
   → INSERTED gate → transcript adjudicated (sliver/invention/spent)
   → prosody judged by ear → delivered → named engine reported
```

Never collapse that into one "done". Name the position on the chain.

---

## 9. Old name → new section (landing table)

An agent that remembers a superseded skill by name lands here.

| Superseded skill | Now lives in |
|---|---|
| `sovereign-tts-lanes` | §1.0–1.5 (offline/sovereign lane selection · Piper/F5-TTS invocation · MMS-TTS-zlm removal record · CTC second witness · inventory-first sweep) + §2.6 |
| `tts-edge-fallback` | §1.1 (lane table) · §1.3.1 (edge-tts) · §1.3.2 (MuleRouter) · §1.3.5 (MiMo) · §1.6 (overrides/triggers) · §1.7 (OGG delivery) · §1.8 (BM speech craft) · §3.2 (prosody profiles) · §3.3 note · §5 (pitfalls) |
| `qwencloud-audio-tts` | §1.3.7 (Qwen/CosyVoice invocation, models, voices, error table, key compatibility, write prohibition, credential hygiene) · §4.3 ladder entry |
| `audio-roundtrip-diagnostics` | §2.2 alias protocol · §2.3 false-FAIL classes · §2.4 timestamp gate · §2.6 witness rule · §2.9 speed/F0 · §2.10 pitfalls |
| `tts-roundtrip-scoring` | §2.1 metric law (INSERTED = 0) · §2.2 (inversion diagnostic, falsifiable alias tables) · §2.3 · §2.4 (substitution vs respell) · §2.10 (channel resolution) |
| `voice-lane-verification` | §2.5 flagged-token span triage · §2.7 three-layer activation + refusal test + legacy id + precedent · §2.8 failure signatures · §2.10 chain |
| `minimax-voice-design-prompts` | §3.1 (prompt anatomy, template, hit example, what-not-to-do, preview_text, persistent ids, clone cost) |
| `nusantara-acoustic-infrastructure` | §4.0 acoustic deficit · §4.1 corpus/consent · §4.2 rojak preprocessor · §4.3 engine ladder · §4.4 STT ears · §4.5 consent rules · §4.6 key facts + macro/micro strategy |

Triggers carried over (so a phrase match still lands here): cloud TTS quota exhausted and a voice is still needed · TTS must work offline / without a provider · MiniMax 2056 / balance error blocks delivery · Malay or BM text needs speech on CPU only · evaluating Piper, MMS-TTS, F5-TTS for Malay · fallback when OpenAI TTS quota is exhausted or unavailable · free local Malay voice · convert text to speech · create voiceovers · generate audio narration · read text aloud · build TTS applications · speech synthesis / voice generation / audio output from text · round-trip match percentage looks wrong · INSERTED words flagged but the text contains them · transcript has words after the file duration · about to re-render on a low match score · building an alias table for a voice · scoring a TTS take against its script · activating/wiring/switching a persona voice or proving one is live · a round-trip or ASR gate flags an inserted word · reporting that a voice lane is down, refused, or mis-routed · a config change must be shown to have taken effect · designing MiniMax voice prompts · Nusantara voice AI · Malaysian voice AI · Bahasa Melayu TTS · dialect voice · acoustic deficit · corpus ingestion · rojak TTS · sovereign voice · voice loop data · Sahabat-AI · ILMU voice · F5-TTS · SEA-LION · voice mode · dalam voice · buat voice · hantar voice · suara Penang · voice Bahasa Penang · TTS bahasa melayu · voice elok · yang bagus sikit · Nusantara mode · suara lain · tukar suara · guna suara lain · suara Melayu · voice lain · suara laki macho · suara macho · masculine voice.

DITEMPA BUKAN DIBERI — a voice you rent is a voice you can lose, and a clean take rejected by a broken scoring pass is a render you paid for twice.
