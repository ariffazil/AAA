---
name: nusantara-voice-stack
description: "BM TTS realism, engine ceilings, provider lanes, I-ARIF."
version: 1.0.0
author: Hermes Agent
license: arifOS
tags: [tts, voice, malay, bahasa, nusantara, edge-tts, minimax, f5-tts, i-arif]
metadata:
  hermes:
    tags: [tts, malay, voice]
    related_skills: [mulerouter-media, minimax-cli, tts-edge-fallback]
triggers:
  - suara fake complaints about BM TTS
  - bunyi robot voice notes
  - Malay voice notes needing realism or loghat
  - BM or Penang voice layer for I-ARIF
  - Malaysian LLM or TTS landscape questions
  - prosody or emotional contour on edge-tts
  - MiniMax or MuleRouter TTS routing for Malay
capability_tier: fed-realtime-voice
ecology_state: WARM
---

# Nusantara Voice Stack

## When to Use

Load this skill before doing ANY of: rendering BM voice notes, diagnosing "fake voice" complaints, routing TTS for Malay output, evaluating new Malaysian voice models, or planning paid/free voice infrastructure.

Class-level capability: make machines speak Bahasa Malaysia like humans (loghat, code-switch, emotion) using sovereign-first resources. Context: I-ARIF north star — BM + Penang loghat data moat. Coined 2026-08-14 after Arif's "Malaysia x dak AI LLM sendiri, voice is so fake" session.

## 1. The Ceiling Doctrine (proven 2026-08-14)

Two distinct ceilings — diagnose BEFORE polishing:
- **PROCESSING ceiling** — fixable: rate/pitch contour, breath pauses, chunking (see §2).
- **ENGINE ceiling** — unfixable by post-processing. edge-tts ships exactly **2 ms voices** (ms-MY-OsmanNeural male, ms-MY-YasminNeural female), both one-style "Friendly, Positive" formal narration. No amount of contour creates a new vocal identity, real fillers, or loghat.

User verdict on full prosody contour vs flat baseline (A/B delivered as voice notes): "This is nice. But still kinda the same. So what??" — **contour alone does not close the gap.** When the complaint is "fake voice", the engine is usually the ceiling: swap the engine (voice cloning / voice design), don't keep post-processing the corpse.

## 2. Nusantara Prosody Engine v2 (LIVE, tested)

Script: `scripts/nusantara_prosody.py` (original deployed at `/root/nusantara-voice/nusantara_tts.py`). Deterministic, zero-LLM, zero-cost, no network beyond edge-tts itself.

Pipeline: text → split at natural pause points (punctuation, tapi/kalau/sebab) → per-chunk emotion classification via BM keyword lexicon (bahaya/risiko/rosak/hold = heavy; solid/jelas/lulus = good; trailing "?" = soal) → per-chunk rate/pitch offsets (heavy: -12%/-8Hz vs mood baseline, 320ms pause; good: +4%/+4Hz, 120ms) → ffmpeg concat with anullsrc breath silences → single .ogg.

```bash
python3 scripts/nusantara_prosody.py "Benda ni bahaya kalau buat sorang-sorang." out.ogg berat
# moods: neutral | berat | semangat | soal | tenang
```

Fixes: monotone pacing, missing breaths, uniform delivery.
CANNOT fix: timbre identity, loghat particles as real audio, genuine fillers, code-switch naturalness — those are engine-level (§4).

**Metric caveat:** RMS stdev does NOT distinguish contour from flat (edge normalizes loudness per chunk — measured 7.64 vs 7.32 dB, no signal). Human ear is the judge; never claim contour wins from DSP stats.

## 3. TTS Provider Lane Map (probed 2026-08-14)

Full probe transcript: `references/tts-provider-lane-map.md`

| Lane | Auth | Verdict |
|---|---|---|
| edge-tts | none, free | baseline; 2 voices; engine-capped |
| MiniMax direct api.minimax.io/v1/t2a_v2 | sk-cp Token Plan key works | best RM0 lane when weekly quota live; 334 voices; 2056 = quota, NOT auth failure; resets Sunday |
| MiMo Token Plan TTS (chat protocol) | MIMO_API_KEY (tp-) | **API proven 2026-08-21; BM USE NOT PROVEN — read the caveat.** No REST audio surface; works via `/chat/completions` + `modalities:["text","audio"]`; text in assistant msg; voices `mimo_default, 冰糖, 茉莉, 苏打, 白桦, Mia, Chloe, Milo, Dean`; base64 WAV reply; separate quota bucket from MiniMax TP — gap-filler lane when MiniMax 2056-blocked. **⚠️ NOT A BM LANE — Malay pronunciation falsified 2026-09-15 (STT-verified).** Base `mimo-v2.5-tts` mangles BM word-level (88-char probe → "Aku bayar hang pandang aku … sebelum keba aku tahu") and **long-form transcripts contain ASR-boilerplate strings that are NOT verified speech**: 3 of 4 long-form `mimo_default` transcripts read "Terima kasih kerana menonton!" or "Jangan lupa like, share, dan subscribe", and one run degenerated into a **202s runaway** (normal ≈50s, 4× overrun). ⚠️ **Do NOT report that MiMo speaks or invents a sign-off.** Falsified 2026-09-15: both engines decode that phrase from a clip of *digital silence* (−108 dBFS, 0.0% active frames); fed the isolated suspect window, turbo returns the sign-off while large-v3 returns "Oh, oh, oh…"; and large-v3 emits "Sari kata oleh SDI Media" (a subtitling-vendor credit) on the same file. What *is* real: pathological duration overrun and non-speech-like tails (spectral flatness 0.11–0.18 vs 0.02 for reference speech). Falsification method + controls: `references/mimo-token-plan-tts-2026-08-21.md` §9. The **variants DO work API-wise but do not fix Malay**: `mimo-v2.5-tts-voicedesign` needs top-level `voice_design.prompt` and `audio.voice` OMITTED (sending it → 400 `audio.voice is not supported for voice design model`; omitting the prompt → syllable soup); `mimo-v2.5-tts-voiceclone` needs `audio.voice` = `data:audio/mpeg;base64,…` ~20s reference. Both still garble BM (`biar→bayar`, `pandang→pandan`, `tak pandang→tak pernah`). F0 medians (librosa yin, two independent sessions): base `mimo_default` **unstable 159.6–236.3 Hz** across identical input (female register — unusable for a male BM persona); voicedesign ≈78.0–104.7 Hz; voiceclone ≈104.0–107.6 Hz; MiniMax `Indonesian_BossyLeader` reference 97.2–107.1 Hz. **MiMo = last-resort gap-filler only (better than silence), never the BM lane.** The one-off clean 771-char 冰糖 render (2026-08-30) does NOT reproduce (0/4 clean today); pitch-stability ≠ pronunciation. Pacing measured 10.8–13.2 chars/s — the old "~0.92 chars/s" figure is not reproduced and is internally inconsistent with its own 771-char/71.4s datapoint (`atempo=1.15–1.25` still available, usually unnecessary). Verbatim transcripts, exact call shapes, F0 table, BM verdict: `references/mimo-token-plan-tts-2026-08-21.md` |
| MiniMax TTV voice cloning | sk-cp Token Plan key | FREE on Token Plan; voice ID format `ttv-voice-*`; use with `mmx speech synthesize --voice`; 32kHz; breakthrough for custom voice |
| Qwen Voice Cloning (Singapore) | QWEN_TEAM_OWNER_API_KEY | FREE custom voice from 10-20s sample; supports Malay; breakthrough for abang sado |
| Qwen qwen-audio-3.0-tts-plus | QWEN_TEAM_OWNER_API_KEY | system voices Chinese+English only; 597 base voices ALL Chinese/English; NO Malay |
| MuleRouter speech-2.8-hd | MULEROUTER_API_KEY | DEAD (402, balance -0.75); separate credit pool |
| Runpod GPU (F5-TTS) | RUNPOD_API_KEY | breakthrough lane; pay/hr; requires F13 GO + top-up |
| Piper local CPU | none | NO ms_MY voice exists — dead end for BM |
| Pollinations openai-audio | token | legacy text API deprecated (404 + migration notice); not a TTS lane |

Key endpoint discovery: Token Plan `sk-cp-*` keys authenticate against **api.minimax.io** (global). `api.minimax.chat` rejects them with "invalid api key". Seeing `base_resp.status_code 2056 "Token Plan usage limit reached"` means auth WORKED — wait for weekly reset.

## 4. Indonesian Voice Breakthrough (PROVEN 2026-08-18)

MiniMax speech-2.8-hd has **Indonesian voices** that handle BM text naturally. Indonesian (Bahasa Indonesia) and Malay (Bahasa Malaysia) are mutually intelligible — phonemes, rhythm, and intonation map closely enough that Indonesian voices sound natural reading BM text. This is the first **32kHz, RM0-subscription, no-GPU** path to BM voice that passes the "sounds human" bar.

**Top voices:** `Indonesian_CaringMan` (warm male, speed 0.9), `Indonesian_BossyLeader` (dominant male, speed 0.85). Full voice table + invocation: `references/minimax-indonesian-voices-2026-08-18.md`.

**Full voice catalog:** `mmx speech voices --base-url https://api.minimax.io` returns **334 voices** across 16 languages. Deep/dominant English male voices also work with BM text: `English_ManWithDeepVoice`, `English_Deep-VoicedGentleman`, `English_ImposingManner`, `English_MatureBoss`, `English_BossyLeader`. These give "berat/dominan" weight but with English accent on BM words — use for persona authority, not Malay realism.

**Quota check:** `mmx quota show --base-url https://api.minimax.io` — `general` model = image + speech pool (shared), `video` = separate pool.

**Critical mmx CLI fix:** `--base-url https://api.minimax.io` is REQUIRED for ALL media commands (speech, image, AND video). The mmx CLI default points to `https://api.minimax.io/anthropic` which returns HTTP 404 on speech/image/video endpoints. Proven for video 2026-08-18: `mmx video generate --base-url https://api.minimax.io --image X --download Y` works (Hailuo-2.3 I2V, ~6s 768×768).

**Why this matters:** Previously the only path to engine-level BM realism was F5-TTS on Runpod (pending F13 GO + US$10). Indonesian voices are available NOW — no GPU, no license issues, deterministic, multiple voice personalities. This closes the "fake voice" gap for production use while F5-TTS remains the ultimate target.

**Limitations:** Subtle Indonesian accent (not native BM), no Penang loghat particles, no BM-English code-switch naturalness. Most listeners won't notice the accent; linguists will.

## 5. MiniMax TTV Voice Cloning — FREE on Token Plan (BREAKTHROUGH 2026-08-18)

**MiniMax has its own voice cloning (TTV = Text-To-Voice) that works on the Token Plan.** Voice ID format: `ttv-voice-YYYYMMDDHHMMSS-*`. Accessible via `mmx speech synthesize --voice <voice-id>`. FREE within existing `general` model quota (same pool as image + standard speech).

Previously documented as "Beijing only, CNY 9.9 unlock fee" — that was wrong. The user created voice `ttv-voice-2026081809381426-78AFZAgJ` directly on the Token Plan and it generated clean 32kHz output immediately.12.5s, ~200KB per generation.

**Invocation:**
```bash
mmx speech synthesize --base-url https://api.minimax.io \
  --model speech-2.8-hd \
  --voice "ttv-voice-2026081809381426-78AFZAgJ" \
  --speed 0.85 \
  --text "Sini. Dekat sikit. Kau pandang aku." \
  --out /tmp/clone_output.mp3
```

**Advantages over Qwen voice cloning:**
- No URL hosting required — voice created directly in MiniMax ecosystem
- Same `mmx speech synthesize` CLI — no separate SDK/endpoint needed
- 32kHz output (vs Qwen 22kHz)
- Voice ID persists server-side under the account

**Limitations:**
- `mmx speech voices` does NOT list custom TTV voices — must use voice ID directly
- Quota shared with standard speech synthesis (`general` model pool)

## 5b. MiniMax voice_clone REST API (PROVEN 2026-08-18 — minted `iarif-sovereign-v1`)

Earlier note said "voice creation API not reverse-engineered (UI only)" — WRONG. Full REST pipeline proven live: cloned Arif's 27s sample → `iarif-sovereign-v1`, synthesis verified within the minute, Whisper round-trip transcription perfect.

**Pipeline (3 calls):**
```bash
source /root/.secrets/kunci-root.env

# 1. Upload sample (mp3/m4a/wav, 10s–5min, ≤20MB)
curl -s https://api.minimax.io/v1/files/upload \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  --form 'purpose="voice_clone"' \
  --form 'file=@sample.mp3'
# → file_id

# 2. Clone
curl -s https://api.minimax.io/v1/voice_clone \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"file_id": <file_id>, "voice_id": "my-voice-v1",
       "text": "Test sentence.", "model": "speech-2.8-hd"}'
# → status 0 + demo_audio URL (signed OSS preview, expires ~48h — download immediately)

# 3. Synthesize with the new voice_id via normal t2a_v2 — works instantly,
#    no hydration delay.
```

**Pitfalls (hit live):**
- **OGG rejected:** MiniMax voice_clone returns `2013 invalid file ext for voice clone` for OGG files. Accepts WAV, MP3, M4A only. Always `ffmpeg -i source.ogg source.wav` before upload.
- **Minimum 10.0s:** Files below 10s are rejected. Proven clean at 10.17s. For best fidelity, 2–3 minutes preferred.
- **Duplicate voice_id:** If the voice_id already exists, clone returns `2039 voice clone voice id duplicate`. The existing clone still works for synthesis — you don't need to re-clone.
- `clone_prompt.prompt_audio` IS REQUIRED (not optional as previously documented). Omitting it → `2013: prompt_audio or audio_url is required`. Upload with `purpose="prompt_audio"`. **Duration window (verified 2026-08-19):** 5–8 seconds is the sweet spot. Below 5s → `2037: voice duration too short`. Above 10s → `2048: prompt audio too long`. Trim with `ffmpeg -t 7` for a safe default.
- **Source audio <10s:** If the voice sample is under 10 seconds, pad with silence: `ffmpeg -i source.mp3 -af 'apad=whole_dur=12' -ar 16000 -ac 1 padded.wav`. Then upload padded.wav as `voice_clone` source. The clone quality depends on the speech content, not the silence padding.
- Clone response does NOT echo back the voice_id — the string you sent IS the ID. If synthesis returns `2054 voice id not exist`, the ID string mismatched, not a hydration delay.
- TTS synthesis (`t2a_v2`) returns HEX-ENCODED audio, not base64. Decode: `bytes.fromhex(audio_str)`. Ratio `len(audio_str) / audio_size == 2.0`.

Full details: `references/minimax-voice-clone-v9-2026-08-19.md` (the 2026-08-18 TTV note was never vendored; the V9 session record supersedes it).

## 6. Qwen Voice Cloning — FREE Custom Malay Voice (BREAKTHROUGH 2026-08-18)

**Qwen-Audio-TTS voice cloning is FREE on the Singapore Token Plan.** First zero-cost path to a custom Malay male voice without GPU. Upload a 10-20s sample of a deep Malay male voice → clone → synthesize BM text with that voice. Cloned voice preserves timbre, accent, emotional quality. No Indonesian accent bleed.

**Supported cloning input languages:** Chinese (20+ dialects), English, Japanese, Korean, Russian, French, German, Portuguese, Thai, Indonesian, Vietnamese, Spanish, Italian, **Malaysian**, Filipino, Arabic.

**API (Singapore region):**
```bash
# Step 1: Create voice (audio must be accessible via URL)
curl -X POST "https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "voice-enrollment",
    "input": {
      "action": "create_voice",
      "target_model": "cosyvoice-v3-plus",
      "prefix": "iarif2026",
      "url": "https://aaa.arif-fazil.com/audio/source.mp3",
      "language_hints": ["ms"]
    }
  }'
# Returns voice_id for synthesis

# Step 2: Synthesize with cloned voice (WebSocket only — REST returns 404)
# MUST use /usr/bin/python3 (system), NOT venv python
/usr/bin/python3 -c "
import dashscope, os
dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
dashscope.base_websocket_api_url = 'wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference'
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat
s = SpeechSynthesizer(model='cosyvoice-v3-plus', voice='YOUR_VOICE_ID', format=AudioFormat.MP3_22050HZ_MONO_256KBPS)
audio = s.call('Sini. Dekat sikit. Kau pandang aku.')
with open('out.mp3', 'wb') as f: f.write(audio)
"
```

**Billing:** Voice creation = FREE. Synthesis = normal Token Plan quota. Up to 1,000 custom voices/account. Auto-deleted after 1 year unused.

**Audio requirements:** WAV/MP3/M4A, 10-20s (60s max), ≥ 16kHz, mono, clear speech, no background noise, ≥ 5s continuous speech.

**Critical:** `target_model` must match synthesis model. Create with `cosyvoice-v3-plus` → synthesize with `cosyvoice-v3-plus`.

**Pitfall:** Audio must be accessible via URL (not local file://). Host reference audio on temporary HTTP server or object storage first.

**Pitfall (PROVEN 2026-08-25):** `prefix` must be alphanumeric only — hyphens/special chars rejected with `InvalidParameter`. `language_hints` must be exactly 1 element (array of 2+ rejected with `InvalidLanguageHints`).

**Pitfall (PROVEN 2026-08-25):** CosyVoice synthesis via WebSocket **truncates on long text** (>10 words). Short text (3-6 words) works. Mitigation: chunk text into short segments, synthesize each, concatenate with ffmpeg. REST API (`/compatible-mode/v1/audio/speech`) returns HTTP 404 — CosyVoice is WebSocket-only.

**Pitfall (PROVEN 2026-08-25):** `dashscope` package is installed under system python (`/usr/bin/python3`), NOT the Hermes venv (`/root/venv/bin/python3`). Always use `/usr/bin/python3` for CosyVoice synthesis.

**Seat quota:** QWEN_ARIFOS_API_KEY exhausted (HTTP 44 `Throttling.AllocationQuota`), QWEN_TEAM_OWNER_API_KEY works. Always ladder seats before declaring dead.

Full Qwen voice cloning details: `references/qwen-voice-cloning-2026-08-18.md`.
CosyVoice clone session (2026-08-25): `references/cosyvoice-clone-session-2026-08-25.md`.

## 7. Breakthrough Path: Malaysian-F5-TTS-v3 (identified, first experiment PENDING)

`mesolitica/Malaysian-F5-TTS-v3` — full-parameter finetune of SWivid/F5-TTS `F5TTS_v1_Base` on Malaysian-Emilia (15,631 hrs Malaysian speech + 600 hrs Mandarin). Model-card claims (NOT yet verified by our own ears): generates fillers (erm, uhm) when reference speaker has them; transfers emotion from reference speaker; Malay/local-English/Mandarin code-switch even from a mono-speaker reference. Checkpoint: `hf://mesolitica/Malaysian-F5-TTS-v3/checkpoints/model_220000.pt`. Source: github.com/mesolitica/malaya-speech session/f5-tts. **License CC-BY-NC-4.0 — non-commercial.**

Experiment plan (awaiting F13 GO + Runpod top-up ~US$10): 4090 pod → clone SWivid/F5-TTS → gradio infer app → custom model path = checkpoint above → feed the sovereign's own voice sample as reference. Status as of 2026-08-14: NOT RUN — Runpod balance was empty. Do not present as validated until ears have judged.

## 8. Target Fingerprint Method (LIVE)

Know what "real" sounds like before tuning anything: transcribe the sovereign's own voice locally.
`faster-whisper` small/int8/CPU on the VPS transcribed a 16.7s BM sample perfectly (lang=ms p=1.00, ~20s wall, zero cost). Extracted style fingerprint (Arif, 2026-08-14): BM santai with English technical jargon flowing inline (tiga API call, latensi, deploy ke staging), numbers spoken not read, closes with a direct binary question. Use this as the reference bar when judging TTS output.

## 9. Arif's Bar (user preference, hard)

- Contour tricks are not the solution. Engine-level humanity or nothing.
- RM0/sovereign lanes first; paid GPU = F13 decision, never auto-top-up.
- Voice notes = conversational prose only; numbers spelled in BM; technical jargon stays English.
- **Reports, not hymns.** When a constitutional axiom / i-ARIF doctrine amendment has just sealed, do NOT drift into puitic prose ("tiga cermin", "aku nampak, Arif", "Hang yang tentukan visually akhir"). That register sounds wise but carries zero information. Arif's literal correction (2026-08-18): *"Hate reply like this. No meaning to me"* and *"Laporan tu ukur benda salah."* See `hermes-response-format-fit > Pitfall — Poetic Axiom Mode (2026-08-18)` for the home of this lesson — duplicated here only because voice-stack sessions tend to hit it after a G061/G062 seal.
- **Default vs sovereign-lane question — answer, don't bypass.** When Arif asks "should default model be I-ARIF?", give the deployment-real third way (sovereign lane for Hang's work, default Hermes for tenant-3 work) rather than philosophical-only "two are different." He wants the answer to act on.

## 10. Pitfalls

- **V8 fallback silently swaps voice identity (hit 2026-08-30).** `iarif_tts_pipeline.sh` fail-open chain (MiniMax→MiMo→edge) protects *delivery*, not *identity*: MiniMax 2056'd mid-session and stage 1M rendered the text in MiMo 冰糖 — a different voice from the V8 clone `i-ARIF-20260819T084602` (that voice_id only exists on MiniMax). The artifact shipped with an unlabeled voice change. **Rule:** when stage 1 falls through to stage 1M/1E, SAY SO in the delivery message (name the actual engine/voice) — and if the voice identity matters to the artifact (e.g. a persona wish), consider holding for the MiniMax reset instead of shipping the substitute. Per §17 declare-vs-reality: a silent engine swap is exactly the "saksi palsu" pattern.

- **V8 (`i-ARIF-20260819T084602`) injects a BANNED phrase at the MODEL level (PROVEN 2026-09-15).** Rendering plain BM text through this voice prepends a greeting that is not in the input: `"Salam Arif, lembut tapi besi."` (Groq turbo) / `"Salam Arif, lembut tapi bersih."` (local large-v3). `lembut tapi besi` is on the pipeline's own FORBIDDEN list — but the pipeline cleans the **input text**, not the **model output**, so the injection passes straight through to delivery. Both engines saw it on the RAW `t2a_v2` response, so it is voice-level autoregressive contamination, not a pipeline or ASR artifact. **Use `iarif-sovereign-v9`** (100% STT match, no injection). Generalisation: a voice_id can carry content the script never contained; every render must be STT-checked for *extra* words, not just mismatched ones.
- **The pipeline has NO output-length validation — a transient truncation can ship silently (hit 2026-09-15).** One run of `iarif_tts_pipeline.sh` returned **0.216 s / 3,335 bytes** for an 88-char input (MiniMax `base_resp.status_code 0`, no error raised); the next two runs returned 9.18 s and 9.40 s from the same input whereas raw `t2a_v2` gave 9.61 s. The near-empty artifact then transcribed as `"Terima kasih kerana menonton!"` — the Whisper non-speech boilerplate of §12, appearing on a REAL artifact (not just synthetic controls). **Rule:** check duration after every render (`ffprobe`) and re-render on an obvious anomaly; never trust `status_code 0` alone. Also: a raw-vs-pipeline duration mismatch of >0.5 s means something in the chain clipped the audio.
- **Live voice_id provenance gap (found 2026-09-15).** `tts.minimax.voice_id` and the pipeline default are both `iarif-sovereign-v9`, but the only manifest on disk (`/root/AAA/audio/i-arif-v9-manifest.json`) documents a DIFFERENT id (`ttv-voice-2026082515384726-njTJ5yOR`, `vault_seal: F13_APPROVED`). `iarif-sovereign-v9` has no manifest of its own. Separately `/root/AAA/audio/rollback-v9.sh` is stamped **F13 REJECT** (`reason: Ear-test fail — rasa tidak hits`) and is "Awaiting ARIF approval to execute", while `/root/VAULT999/voice-revocations.jsonl` does not exist (rollback step 4 never ran). The reject timestamp (2026-08-25T07:49Z) **predates** the manifest's approval (15:41Z), so the rollback is most likely stale rather than live — but that is inference, not established fact. Resolve before citing V9 as constitutionally clean.

- **F0 claims without reference audio = fabrication (PROVEN 2026-08-19 23:30).** Agent claimed 239 Hz was "Siti Nurhaliza's register" without ever obtaining or measuring actual Siti Nurhaliza audio. The 239 Hz target was a DSP spec, not a voice reality. When Arif asked "do you even know what Siti Nurhaliza sounds like?", the honest answer was no. **Rule:** Before claiming any F0 target is correct for a named voice, produce or obtain that voice's actual audio and measure it. Text descriptions ("humble genius Melayu", "Penang female register") do not constitute F0 evidence. Makcik reference (Penang female, measured 190.5 Hz median) was available but never compared against the 239 Hz target. Always: measure reference → measure pipeline output → compare → THEN decide.

- **That rule is now mechanically executable (PROVEN 2026-09-15).** `python3 /root/scripts/rasa_somatic_dsp.py AUDIO --claim-f0 190.5` measures the file, compares against the claimed value, and prints PASS/FAIL with the error %. Run `--selftest` first: an uncalibrated instrument refuses to set its per-field `trustworthy` flag. The organ runs two independent estimators (`pyin` + autocorrelation) and reports `octave_flag: OCTAVE_DISAGREEMENT` instead of a confident wrong number when they differ by ≥0.5 octave — the exact failure mode the 239 Hz claim walked into. Re-measuring this host's declared voice metrics: i-ARIF v9 manifest `f0_median_hz 246.9` → 252.7 (+2.4 %, reproduced) and the Makcik reference 190.5 Hz → 180.8 (−5.1 %, reproduced), but the same v9 manifest's `voiced_frames_pct 82` → 71.1 (−13.3 %, NOT reproduced — a declared number that does not survive re-measurement). Doctrine and pitfalls: `aaa-somatic-emd-pipeline` §Phase 1 pitfalls.
- edge-tts CLI pitch: use `--pitch=-15Hz` form; `--pitch -15Hz` errors "expected one argument".
- runpodctl pod create flags: `--gpu-id`, `--image`, `--container-disk-in-gb` (NOT --gpuType/--imageName/--mem — those belong to the deprecated `create pod` form).
- pip on this VPS requires `--break-system-packages` (PEP 668).
- MiniMax GroupId query param is a CN-endpoint concept; global endpoint takes pure Bearer, no GroupId.
- r.jina.ai proxy to huggingface.co can be IP-blocked ("previous abuse"); use the HF REST API directly (`/api/models?author=...`) — faster and never blocked.
- `mmx speech synthesize` 404 workaround: direct curl (see creative/minimax-cli).
- **mmx CLI base-url for speech/image (PROVEN 2026-08-18):** The mmx CLI default `base_url` is `https://api.minimax.io/anthropic` (text/chat endpoint). Speech and image endpoints require `--base-url https://api.minimax.io` (no `/anthropic` suffix). Without override, `mmx speech synthesize` and `mmx image generate` return HTTP 404.
- **MiniMax t2a_v2 returns hex-encoded audio (PROVEN 2026-08-18):** The `api.minimax.io/v1/t2a_v2` endpoint returns JSON with `data.audio` as a hex string, not raw binary. Direct curl saves a JSON file. To get an MP3: `audio = bytes.fromhex(json.load(open(resp_file))['data']['audio'])`. Hermes decodes this internally, but independent curl calls do not. The `text_to_speech` endpoint (different path) returns raw binary.
- **Hermes minimax TTS provider uses t2a_v2 by default** (confirmed 2026-08-18): the built-in `_generate_minimax_tts()` in `tools/tts_tool.py` hits `https://api.minimax.io/v1/t2a_v2` with `model`, `voice_id`, `speed` from the `tts.minimax.*` config block. Custom voice IDs (standard catalog or `ttv-voice-*` clones) work natively — no MEDIA: workaround needed.
- **Video quota exhausted → Ken Burns voice montage (PROVEN 2026-08-18):** When Token Plan video quota is dead (weekly reset Sunday), deliver the voice line as a cinematic slideshow instead of holding: 3 subject-ref stills, ffmpeg zoompan slow push-in (alternate direction per frame) + xfade crossfades, mux the TTS mp3 with aac. Proven 40.76s 1080x1920 5.5MB over a 39s BossyLeader line. Queue real Hailuo I2V with the same stills as `--image` when quota resets. Full recipe + prompts: `references/alpha-worship-recipes-2026-08-18.md`.
- **Groq Whisper Python SDK path duplication (PROVEN 2026-08-18):** The `groq` Python SDK base URL already includes `/openai/v1/`. Calling `client.audio.transcriptions.create()` appends `/openai/v1/audio/transcriptions` again → `/openai/v1/openai/v1/audio/transcriptions` → HTTP 404. **Fix:** use curl directly against `https://api.groq.com/openai/v1/audio/transcriptions` with `-H "Authorization: Bearer $GROQ_API_KEY"`. Simpler, no venv dependency, works every time.
- **Hermes `config.yaml` direct writes are blocked (PROVEN 2026-08-18):** The `write_file`/`patch` tools refuse to edit `~/.hermes/config.yaml` with `Refusing to write to Hermes config file`. **Fix:** use `hermes config set <key.path> <value>` per key. Custom keys (not in the schema) emit a warning but are saved anyway and bridged to skills/external tools via env. Voice persona keys (`voice.persona_prompt_file`, `voice.sado_locked_voice_id`, etc.) land as custom-key warnings — expected behaviour. Verify with `hermes config get voice` (not `hermes config show voice` — that subcommand doesn't exist; the positional argument is wrong).
- **Probe third-party agent reports before believing (PROVEN 2026-08-18):** When another agent (kimi-code, sub-federation, CI forge) reports a "done" status on a voice/audio artifact, always re-probe: `stat` for mtime, `ls -la` for file presence, `ffprobe` for duration/channels/sample rate, `grep` for line numbers. Three failure modes seen: (1) claim "file dormant, zero edits" when mtime proves it was scaffolded 8 min ago, (2) claim "voice sample is Arif" when Whisper transcribes the audio as fluent English (wrong source), (3) claim "config line 851" when real line is 1581. F2 TRUTH discipline applies to sub-agent reports, not just user claims.
- **Voice sample provenance must be verified before mint (PROVEN 2026-08-18):** Before any voice_clone call, run `ffprobe -show_format -show_streams` on the candidate file. Reject if: channels≠1, duration<10s or >5min (MiniMax) or >20s (Qwen), sample_rate<16kHz, contains music/multiple speakers/clipped peaks. Then STT-falsify: transcribe with Groq Whisper; if language auto-detected as non-ms and content doesn't match the named speaker, the file is the wrong source. F1 AMANAH — voice identity provenance is immutable evidence, F13 territory to mint.

## 11. Per-Modality Evaluation Doctrine (PROVEN 2026-08-18)

**Never claim "Model X paling fasih BM" across all modalities.** Voice, LLM reasoning, code, and vision are separate evaluations with separate winners. A blanket BM-fluency verdict is a fabrication waiting to happen — falsified on 2026-08-18 when an external analysis ranked "Qwen = best BM" generally; reality was the inverse for TTS.

| Modality | Best lane | Why |
|---|---|---|
| BM copywriting / reasoning / naratif (LLM) | **Qwen Token Plan** | Qwen2.5/Qwen3 trained on SEA corpus including BM; BM output reads native |
| BM TTS / voice notes | **MiniMax Indonesian voices** or **MiniMax TTV clone** | Qwen's 597 base voices are 100% Chinese/English (zero BM); MiniMax Indonesian voices handle BM text naturally because Indonesian ↔ Malay phonemes map closely |
| Custom Malay voice clone | **MiniMax TTV** (free, persistent, in-ecosystem) or **Qwen voice cloning** (free, requires URL hosting) | Both free; MiniMax simpler, Qwen slightly better timbre preservation |
| BM STT / falsification | **Groq Whisper-large-v3-turbo** | 216× realtime, free, supports `language=ms` |
| Codebase crunch / 1M context | **MiMo-V2.5** | Cost-efficient on technical text; BM creative output weaker |

**Diagnostic question before any "best BM" claim:** "Best for *what*? Voice? Text reasoning? Code? Vision?" If the answer is more than one modality, the verdict is by definition wrong.

## 12. STT Quality Verification Pattern (PROVEN 2026-08-18) — **REQUIRED STEP, no exception**

**MANDATORY GATE (forged 2026-09-15):** no TTS artifact may be cited as a BM lane, delivered as a voice note, or promoted in this skill's lane table without a Groq Whisper `language=ms` round-trip. Render → STT → diff against the input text. Any word-level divergence, invented phrase, or duration overrun is a **BLOCK, not a note** — an engine that returns HTTP 200 is NOT an engine that speaks Malay. Two live falsifications prove why: MiMo returned 200 on every call while mangling BM word-level (`biar`→`bayar`, `kepala`→`keba` — confirmed by two independent ASR engines, `references/mimo-token-plan-tts-2026-08-21.md` §7), and a silently-swapped fallback voice shipped an unlabelled identity change (§10). Synthesis success ≠ lane. STT + duration check is the cost of admission.

**One engine is NOT enough (added 2026-09-15).** Whisper emits Malay boilerplate on non-speech — "Terima kasih kerana menonton", "Sari kata oleh SDI Media". Proven across SIX synthetic controls: **5 of 6 non-speech clips** (white noise, speech-band noise, gated noise, near-silence −55 dBFS, digital silence) returned the identical phrase from BOTH engines; only clean speech transcribed correctly. It fires at **loud noise (−22.6 dBFS)**, not just silence — which is the regime real failure windows sit in. So: run **two engines** and follow these controls — (1) the same text through the reference lane (MiniMax): if the reference also scores <95%, the fault is your ASR or your text, not the engine under test; (2) non-speech controls at **matched level**, not just silence (recipe: `/root/audio-lane-2026-09-15/noise_controls.py`) PLUS a known-clean-speech clip — one clip cannot serve both roles; (3) duration + sample rate + spectral flatness alongside the transcript: flatness a multiple of a reference speech signal means non-speech content even when the transcript looks plausible.

**Know the limit of your witness (added 2026-09-15).** Two Whisper engines share a training-data prior, so their agreement is **not independent confirmation** — for pure noise both return the same fictitious Malay sentence. Dual-Whisper proves *"the engine mangled this"* (gross damage; both see it) but NOT *"the engine did/did not say X"* in a noisy region. For absence/attribution claims use an architecture-independent engine: a **CTC** model cannot autoregressively invent fluent speech on non-speech, making it the correct second witness (`onnx-community/mms-1b-all-ONNX`, Meta MMS, runs on the VPS's existing `onnxruntime`; Z.AI `glm-asr-2512` is the paid alternative).

**Pass criteria for BM:** ≥95% (both engines) ship · 85–95% ship only if divergences are non-lexical (particles, punctuation) · <85% BLOCK and re-render on another lane.

When evaluating TTS output quality (especially for voice cloning or new voices), use STT as a falsification gate: if Whisper transcribes the TTS output perfectly, pronunciation and clarity are confirmed. Cheaper and more repeatable than human A/B listening.

**Pipeline:** Generate TTS → transcribe with Groq Whisper → compare transcript to input text → divergence = quality signal.

```bash
source /root/.secrets/kunci-root.env
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file="@/tmp/tts_output.mp3" \
  -F model="whisper-large-v3-turbo" \
  -F language="ms"
```

**What to look for:**
- 100% transcript match = pronunciation clear, consonants crisp
- Hallucinated words = unclear pronunciation, background noise, **or the ASR's own boilerplate** — run the silence control before blaming the engine
- Wrong language detection = accent bleed (Indonesian voice reading BM detected as "id" not "ms")

**Limitations:** STT cannot assess warmth, authority, or persona fit. Human ear is the final judge. STT is a floor check, not a ceiling check.

Full details: `references/stt-quality-verification-2026-08-18.md`.

## 13. Hermes Voice Mode Wiring (v2026.3.17+ patch, PROVEN 2026-08-18)

Hermes Agent ships a built-in Voice-to-Voice engine. Three capabilities from the patch are class-level wins for any BM/Penang voice pipeline:

**Barge-in (full-duplex interruption).** Native config key `voice.barge_in=true` plus `voice.barge_in_grace_seconds` (default 0.5) and `voice.barge_in_threshold_multiplier` (default 3.0× ambient RMS). When user speaks during agent playback, VAD cuts audio mid-syllable, STT captures the interjection, model is notified. Critical for live conversation; without it the agent monologues over the user.

**Two-stage silence detection.** Default keys: `voice.silence_threshold=200` (RMS), `voice.silence_duration=3.0` (end-of-turn). Combined with the built-in speech confirmation gate (0.3s above threshold), this prevents fan noise / long breaths / "uhh" filler from triggering end-of-turn detection.

**Stop phrases.** `voice.stop_phrases: ["cukup", "stop", "diam"]` (Penang-aware BM + English + neutral). Direct cutoff independent of silence detection — useful when user wants to abort mid-sentence without waiting for natural pause.

**Custom-key bridge pattern.** Voice persona attributes (`voice.persona_prompt_file`, `voice.sado_locked_voice_id`, `voice.hallucination_filter`, `voice.two_stage_silence`, `voice.tts_provider_default`) are NOT in the Hermes config schema. Setting them via `hermes config set` emits a warning but persists them; skills/external tools read them via env bridge. **Do not** try to enforce them via direct config write — the guardrail blocks it with `Refusing to write to Hermes config file`.

**Dormant scaffold pattern.** When a voice artifact (e.g. `voice_filters.py` for tag injection) depends on a physical blocker (real cloned voice_id not yet minted), write the scaffold with versioned filename (v0.1.0, SCAFFOLD tag in header), declare it dormant, and DO NOT wire it into runtime. Activate only after F13 mint. Reason: tag behaviour (which `[breath]`/`[hold]` produces what acoustic effect) is voice_id-dependent. Testing tag behaviour against the default `Indonesian_CaringMan` gives misleading signals; testing against the wrong voice_id breaks expectations when real voice lands.

**Identity file structure pattern.** i-ARIF identity card (`/root/AAA/agent-cards/identity/i-ARIF/identity-card.json`) carries the canonical voice stack: `audio_identity.primary_voice` (edge baseline), `audio_identity.voice_fallback_chain` (ordered lanes), `audio_identity.penang_voice_path` (experimental dialect), `audio_identity.stt_preference` (3-tier: cloud-fast / cloud / local-sovereign), `audio_identity.audio_understanding` (native audio via FED), `constitutional_audio_floors` (F1/F2/F4/F7/F9/F10/F13). Update the card whenever a fallback lane is added/removed. Treat as immutable record (F1 AMANAH); new variants get new identity cards (888-APEX-verdict).

**Voice Pipeline — 2-stage DECODE (sealed 2026-08-19, active).** Production pipeline: `bash /root/AAA/engines/iarif_tts_pipeline.sh {text_path} {output_path}` registered as Hermes command-provider `i-arif-sovereign`. Stage 1: MiniMax speech-2.8-hd, voice `i-ARIF-20260819T084602` (V8, synthetic Penang female clone, F0 ~211 Hz raw). Stage 2: Sovereign Sound Stabilizer (`/root/AAA/engines/sovereign_sound_stabilizer.py`, pyworld WORLD vocoder) — F0 lock 239 Hz (band 225–255), terminal pitch lift +35 Hz (northern cadence), coda truncation 40ms. Fallback: `ms-MY-YasminNeural` (purged OsmanNeural). Consent: synthetic voice, no real person waveform. Cultural anchor: Siti Nurhaliza as spirit reference (jiwa), NOT waveform (F9 anti-hantu). **Design-vs-Clone doctrine (Arif F13, 2026-08-19):** (1) DESIGN — seal now, no authorization debt; (2) CLONE WITH CONSENT — letter, hold; (3) CLONE WITHOUT CONSENT — forbidden forever, F13 floor. Provenance check: MiniMax `/v1/files/list` + local disk + pyworld F0 signature (unverifiable provenance → retire, never bless docs to match). **Overlapping skill:** `minimax-voice-design-prompts` covers voice_design prompt templates; this skill covers the full stack.

**Impact:** Violated F10 (male-only in SADO group). Syed saw female voice from "Arif's agent." See `references/asi-bot-voice-leak-2026-08-19.md` for full diagnosis + remediation direction (gateway-level routing fix, tag sanitizer).

## 14. MiniMax `voice_design` F0 Ceiling (PROVEN 2026-08-19)

`voice_design` CANNOT reliably hit a specific F0 target. Empirical test: three candidates minted with "bright mid-soprano, warm, high-pitched female" prompt → measured medians 162.7 / 175.4 / 205.7 Hz. None reached 239 Hz. The prompt describes envelope and character, NOT exact pitch.

**Rule:** If target F0 is non-negotiable, use `voice_design` for timbre/character only, then lock F0 post-hoc with Sovereign Sound Stabilizer (§15).

## 15. Sovereign Sound Stabilizer — WORLD Vocoder Envelope Lock (PROVEN 2026-08-19)

**Architecture:** Two-stage DECODE pipeline:
```
[Stage 1: MiniMax seed (clone or design)] → raw.mp3
    ↓
[Stage 2: WORLD vocoder (pyworld)] → locked.wav
    F0 lock: median → target (default 239 Hz, band 225–255)
    Terminal pitch lift: +35 Hz at clause end (northern cadence)
    Coda truncation: 40ms amplitude ramp (glottal dampening)
```

**Why WORLD, not numpy/scipy:** The naive approach `output = filtered * envelope * sin(phase_mod)` REPLACES speech with a pure sine wave (destroys all identity). A bandpass filter `300–3400 Hz` strips formants and glottal source. WORLD decomposition separates source (f0) from filter (sp = spectral envelope, ap = aperiodicity) — this is the LF glottal model family. Re-synthesizing from modified f0 + original sp + ap preserves speech identity while changing pitch.

**Source F0 dependency (verified 2026-08-19):** WORLD vocoder's output F0 depends on the source F0 ratio. Lower source F0 → larger rescale ratio → more overshoot above target. Example: source F0 197 Hz → output 246.5 Hz (7.5 Hz overshoot); source F0 211 Hz → output 240.4 Hz (1.4 Hz overshoot). The terminal pitch lift (+35 Hz) compounds this. If source F0 is far below target, consider reducing the lift parameter.

**Parselmouth wrapper phase distortion diagnostic (verified 2026-08-19):** When comparing DSP scripts, measure F0 with BOTH pyworld and Praat (parselmouth). If the two estimates disagree by >50 Hz on the same file, the output has phase distortion — the Praat autocorrelation estimator locks onto a different periodicity than pyworld's DIO. This is a sign the DSP script is introducing artifacts. Example: Parselmouth wrapper output showed pyworld F0 153.1 Hz vs Praat F0 238.7 Hz (85 Hz disagreement) — indicating severe phase distortion. WORLD vocoder output showed pyworld 241.4 Hz vs Praat 240.5 Hz (0.9 Hz agreement) — clean. Use this dual-estimator test as a quality gate before promoting any DSP script to production.

**Files:**
- Engine: `/root/AAA/engines/sovereign_sound_stabilizer.py` (pyworld, ~120 lines)
- Pipeline: `/root/AAA/engines/iarif_tts_pipeline.sh` (2-stage, Hermes command-provider)
- Install: `pip install pyworld --break-system-packages` (VPS requires `--break-system-packages` per PEP 668)

**Hermes wiring:** Registered as command-provider `i-arif-sovereign`:
```yaml
tts:
  provider: i-arif-sovereign
  providers:
    i-arif-sovereign:
      type: command
      command: "bash /root/AAA/engines/iarif_tts_pipeline.sh {text_path} {output_path}"
      output_format: wav
      voice_compatible: true
      timeout: 120
```

## 16. Sovereign Self-Clone — F13 Pathway (PROVEN 2026-08-19)

Arif's own voice can be cloned under F13 sovereign self-clone authority. No third-party consent needed.

**Minimum sample:** 10.0s WAV works (proven: 10.17s cloned clean). 2–3 minutes preferred for fidelity. Below 10s = MiniMax API rejection.

**Accepted clone formats:** WAV, MP3, M4A only. OGG rejected (`invalid file ext for voice clone`, code 2013). Always convert OGG→WAV before upload.

**Clone workflow (REST API):** See §5b. Key addition: if `voice_id` already exists, clone returns `2039 voice clone voice id duplicate` — synthesis still works with the existing clone.

## 17. Declare-vs-Reality Gap — Documentation Integrity (FORGED 2026-08-19)

The most dangerous failure mode in voice pipeline governance: config says one thing, runtime does another.

**Case study:** Persona file stated "chest-voice male, F0 110–160 Hz, female prosody forbidden" while runtime produced a 239 Hz female voice. Arif: "config bohong pada dirinya sendiri."

**Rule:** When you change runtime behavior (new voice_id, new F0 band, new gender register), patch EVERY documentation surface in the same session:
1. Config (`tts.minimax.voice_id`, `tts.edge.voice`, `tts.provider`)
2. Persona file (`/root/.hermes/prompts/iarif_persona.md`)
3. SOUL.md (Audio Identity section)
4. Identity card (`/root/AAA/agent-cards/identity/i-ARIF/identity-card.json`)
5. Seal ledger (`VOICE_SEAL_LEDGER.json`)
6. Alignment doc (`SYSTEM_HERMES_ALIGNMENT.md`)

If any one still references the old state, you are a "saksi palsu" — false witness. Arif will catch it, and he should.

## References
- `references/sovereign-sound-stabilizer-2026-08-19.md` — WORLD vocoder architecture, broken-pattern diagnosis, measured results, northern cadence lift, coda truncation
- `references/minimax-indonesian-voices-2026-08-18.md` — Indonesian voice table, invocation patterns, BM prompt patterns, quota notes
- `references/qwen-voice-cloning-2026-08-18.md` — Qwen voice cloning API, billing, audio requirements, seat quota ladder
- `references/cosyvoice-clone-session-2026-08-25.md` — Live clone session: Arif's OGG → hosted URL → CosyVoice enrollment, WebSocket truncation pitfall, REST 404, system python requirement
- `references/tts-provider-lane-map.md` — every endpoint, key prefix, HTTP result, quota semantic, dated
- `references/tts-lane-updates-2026-08-18.md` — mmx base-url fix, Qwen no-Malay discovery, seat quota flavours
- `references/malaysia-ai-landscape-2026-08.md` — Mesolitica/ILMU/SEA-LION/Sahabat-AI/datasets knowledge bank
- `references/iarif-lane-separation-2026-08-18.md` — three-lane voice architecture (i-ARIF sovereign / MakcikGPT sibling / Sado lock), Penang phonetic rewrite layer, V5 F5-TTS staging with GPU gate, voice_id PENDING truth discipline. NEW 2026-08-18.
- `references/stt-quality-verification-2026-08-18.md` — Groq Whisper STT as TTS quality falsification gate, curl template, pitfalls
- `references/tts-landscape-all-plans-2026-08-18.md` — Complete TTS provider comparison across all Token Plans (MiniMax, Qwen, edge-tts, voice cloning). Proven 2026-08-18.
- `references/mimo-token-plan-tts-2026-08-21.md` — **PART A** (2026-08-21) MiMo TP TTS lane: chat-protocol-only API (no REST audio), working call shape, dead-end endpoint table, voice list, F13 identity boundary. **PART B** (2026-09-15) falsifies MiMo as a BM lane: base model mangles Malay + hallucinates sign-offs (3/4 long-form runs, one 202s runaway), voicedesign/voiceclone exact call shapes, F0 medians, BM lane verdict. File was missing from disk and was restored from the quarantined skill snapshot 2026-09-15.
- `references/video-generation-api-quirks.md` — MiniMax video API model naming, quota, H3 unavailability, raw curl fallback, ffmpeg cinematic workaround. Proven 2026-08-18.
- `references/iarif-voice-minting-2026-08-18.md` — i-ARIF clone pipeline state, three F13 decisions, config-typo to fix, falsification threshold, rollback path. NEW 2026-08-18.
- `references/per-modality-bm-evaluation-2026-08-18.md` — Per-modality BM fluency table with live probe transcripts; falsification of blanket "best BM" claims. New 2026-08-18.

## Related
- `media/mulerouter-media` — MuleRouter TTS voices/settings, balance-pool caveat
- `creative/minimax-cli` — mmx CLI + direct API fallback
- `media/tts-edge-fallback` — basic fallback order (overlaps; curator may consolidate)
