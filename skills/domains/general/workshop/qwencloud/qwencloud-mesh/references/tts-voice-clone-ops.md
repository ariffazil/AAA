---
label: TTS Voice Clone Ops — DashScope Singapore (CosyVoice / Qwen-Audio-TTS / Qwen-TTS)
applies_to: cosyvoice-v3-plus, cosyvoice-v3-flash, qwen-audio-3.0-tts-plus, qwen-audio-3.0-tts-flash, qwen3-tts-vc, qwen3-tts-vc-realtime, qwen-voice-enrollment, voice-enrollment
region: Singapore (dashscope-intl.aliyuncs.com)
author: hermes-curator patch (2026-09-24)
---

# TTS Voice Clone — Operational Reference

Companion to `AAA-voice-cloning-qwen-cloud` (bundled, read-only here). These are the *hard-won* constraints and quality levers that surface only when you actually try to enroll and synthesize a real clone.

## Enrollment Call Hard Constraints

The API rejects with `InvalidParameter` if any of these is wrong:

- `prefix` ≤ **10 characters**. Longer → `prefix should not be longer than 10 characters`. The API prepends `cosyvoice-v3-plus-` itself, so the prefix is the human-readable label, not the full handle.
- `language_hints` is a **single-string array**, not a multi-language list. `["ms","en"]` fails with `InvalidLanguageHints: the length of language_hints must be 1`. Use `["ms"]` and let the model handle code-switching at synthesis time.
- `action` differs by endpoint family: `voice-enrollment` uses `"create_voice"`, `qwen-voice-enrollment` uses `"create"`. Mismatch → empty `voice_id`.

```bash
# Correct payload (CosyVoice family)
curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "voice-enrollment",
    "input": {
      "action": "create_voice",
      "target_model": "cosyvoice-v3-plus",
      "prefix": "iarifcosy",        # ≤10 chars
      "url": "https://arif-fazil.com/_shared/sample.wav",
      "language_hints": ["ms"]      # single string
    }
  }'

# Response shape:
# {"output":{"preview_audio":{},"voice_id":"cosyvoice-v3-plus-iarifcosy-<hash32>"},
#  "usage":{"count":1},"request_id":"..."}
```

## Synthesis: SDK, not curl

`POST /services/audio/tts/SpeechSynthesizer` returns `{"code":"InvalidParameter","message":"current user api does not support http call"}` for the Singapore free-tier / Token Plan lanes. The synthesis path is **WSS-only** and only the `dashscope` Python SDK routes there. Don't waste time debugging curl here — switch to Python.

```python
import os, dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

dashscope.api_key = os.environ["DASHSCOPE_API_KEY"]
dashscope.base_websocket_api_url = "wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference"

# Patch cold-connect timeout — default 5s is too short on Singapore edge.
# Without this, the first .call() often raises TimeoutError before the WSS finishes handshake.
import dashscope.audio.tts_v2.speech_synthesizer as ss
_orig = ss.SpeechSynthesizer._SpeechSynthesizer__connect
def _patched(self, *args, **kwargs):
    if args:
        args = (30,) + args[1:]
    else:
        kwargs["timeout"] = 30
    return _orig(self, *args, **kwargs)
ss.SpeechSynthesizer._SpeechSynthesizer__connect = _patched

synth = SpeechSynthesizer(model="cosyvoice-v3-plus", voice="<voice_id>")
audio_bytes = synth.call("Salam. Hang nak checker Solar pukul 3 tadi?")
# First call first-packet latency: 1100–1200 ms (cold WSS handshake).
# Warm calls: 200–400 ms.
open("out.mp3", "wb").write(audio_bytes)
```

The returned `voice_id` is locked to the `target_model` from enrollment. Re-using it with a different model → silent synthesis failure or `InvalidParameter`. Switching models means re-enrolling.

## Speaker Identity Verification — Before You Enroll

**Volume alone does not identify the speaker.** Two people speaking in sequence at similar loudness produce indistinguishable `volumedetect` output. Before enrolling, run the candidate clip through a local ASR (e.g. `faster-whisper` with `language="ms"` for BM) and confirm the transcript matches the intended speaker.

Practical trap: in the PMX 2022-11-24 swearing-in source, the actual PMX oath sits at `t=1010-1080s` of the 28.7-minute broadcast, but the loudest continuous segment at `t=1280-1340s` is the *Mufti's doa after the oath* — same loudness profile, different speaker. Volume alone would have enrolled the wrong person.

For multi-speaker source material (ceremonies, interviews, talk shows):

1. Extract 30 s windows at 30–60 s strides across the source.
2. ASR each with `faster-whisper` (small model is enough for routing).
3. Pick the window whose transcript matches the target speaker.
4. Extract the final 15–25 s sample from inside that window.

## Source Normalization — Measurable Quality Lift

Raw extracted clips need cleanup before enrollment. Apply this chain and target **mean ≈ -18 dB, max ≈ -1 dB**:

```bash
ffmpeg -i source.wav \
  -af "highpass=f=80,lowpass=f=8000,dynaudnorm=f=150:g=15,loudnorm=I=-18:TP=-1.5:LRA=11" \
  -ac 1 -ar 24000 -codec:a pcm_s16le normalized.wav
```

- `highpass=80` removes HVAC rumble and mic handling noise.
- `lowpass=8000` keeps the speech band, drops codec hiss.
- `dynaudnorm` levels intra-clip volume swings (oath quiet, outro loud).
- `loudnorm=-18 LUFS` puts the file in the range DashScope expects.

Typical improvement on raw ceremony audio: mean -24 dB → -18.9 dB, perceived SNR ~+6 dB, clone fidelity noticeably better — synthetic output's mean goes from -19.4 dB to -17.4 dB after the source is normalized.

## Public Hosting for the Enrollment URL

CosyVoice + Qwen-Audio-TTS require the sample to be a **public URL** (DashScope server fetches it). `qwen-voice-enrollment` accepts Base64 inline. Two working patterns in arifOS:

- **`arif-fazil.com/_shared/<file>`** — drop the WAV into `/var/www/html/_shared/`; the `shared_assets` snippet imported in `arif-fazil.com.conf` already serves `/_shared/*` as `file_server` root. No Caddy reload needed.
- **`geox.arif-fazil.com/audio/<file>`** — used by the bundled `AAA-voice-cloning-qwen-cloud` examples; works but requires the geox vhost route.

Localhost URLs do **not** work — DashScope servers can't reach `127.0.0.1`. The file must be reachable from the public internet.

## Free Quota — Singapore Region

- **1000 voice creations** per account within **90 days** of QwenCloud activation.
- Each successful `create_voice` consumes 1; failed creations are not billed and do not consume quota.
- Deleting a voice does **not** restore quota.
- After exhaustion or expiry, voice creation costs **USD 0.01 per voice** (Beijing).
- TTS **synthesis** is pay-per-character and is **not** covered by the free quota — only voice creation is.
- The free quota is granted automatically once; new accounts do not get a second allotment.
- The quota is per-`voice_id`, not per-model — switching `target_model` requires a new enrollment call (and a new quota consumption).
- After expiry or depletion without pay-as-you-go enabled, calls return `AllocationQuota.FreeTierOnly`.

## Failure-Signature Map (synthesis)

| HTTP / error | Likely cause | Fix |
|---|---|---|
| `current user api does not support http call` on `SpeechSynthesizer` | Tried curl for synthesis | Switch to `dashscope.audio.tts_v2.SpeechSynthesizer` |
| `TimeoutError: websocket connection could not established within 5s` | Cold WSS handshake exceeded default | Monkey-patch `__connect` to 30s (see above) |
| `InvalidParameter: prefix should not be longer than 10 characters` | `prefix` > 10 chars | Shorten |
| `InvalidLanguageHints: the length of language_hints must be 1` | Multiple entries in `language_hints` | Pass one entry |
| `code: InvalidApiKey` | Key empty (env not loaded) | `set -a && source /root/.secrets/kunci-root.env && set +a` |
| Synthesis audio sounds like wrong speaker | Enrolled Mufti / Penyimpan Mohor instead of PMX | Re-run speaker-identity verification before re-enrolling |

## Procedure Summary

1. Extract a clean 15–25 s sample of the target speaker (no background music, no other speaker).
2. Normalize via the ffmpeg chain above.
3. ASR-verify the sample's transcript matches the target speaker.
4. Host at a public URL (`arif-fazil.com/_shared/`).
5. Enroll via `voice-enrollment` + `create_voice` with `prefix` ≤10 chars and `language_hints: ["ms"]`.
6. Save the returned `voice_id` and the chosen `target_model` together (lock-in).
7. Synthesize via `dashscope.audio.tts_v2.SpeechSynthesizer.call()` with the patched 30s connect timeout.
8. Write receipt to `/root/VAULT999/identity/<handle>/` with `voice_id`, `target_model`, `request_id`, source provenance.

DITEMPA BUKAN DIBERI.
