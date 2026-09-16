# MiMo Token Plan TTS — Lane Reference

**Baseline: 2026-08-21. Hardened with live Malay evidence: 2026-09-15.**
Endpoint: `https://token-plan-sgp.xiaomimimo.com/v1/chat/completions`
Auth: `Authorization: Bearer $MIMO_API_KEY` (key prefix `tp-`)

---

## 0. VERDICT FIRST — which lane for Bahasa Malaysia

**Do not use `mimo-v2.5-tts` (base model) to read BM text.** It destroys Malay at every
length tested, non-deterministically, and its default voice is a ~200 Hz female-register
voice (identity mismatch for any male BM persona). For BM, the order of preference is:

1. **MiniMax `speech-2.8-hd` + Indonesian voices** — the quality bar. 100% / 96.2%
   transcript fidelity on the probe text (§7). Primary lane.
2. **MiMo `mimo-v2.5-tts-voiceclone`** — best MiMo variant, and the only one that holds up
   at short length (96.5% on both engines, 88-char probe). **But it degrades long-form:
   49.8% (large-v3) / 57.9% (turbo) at 625 chars — below the §11 ship threshold.** So: use
   it for short lines, gap-filler when MiniMax is 2056-blocked, not for long-form. Do not
   quote the 96.5% without the length it applies to.
3. **MiMo `mimo-v2.5-tts-voicedesign`** — works, male register available, but ~78–82%
   at short length and ~25% long-form. Last resort, short lines only.
4. **`mimo-v2.5-tts` base** — short one-liners only (<~100 chars) and only if the
   female register is acceptable. Never long-form.

Any MiMo output shipped as BM **must pass the STT falsification gate** (§11).

---

## 1. Lane shape — chat protocol only (2026-08-21, still true 2026-09-15)

There is **no REST audio surface**. `/v1/audio/speech`, `/v1/tts`, and the OpenAI-compatible
audio routes do not exist for this lane. Audio is generated through the chat completions
endpoint with `modalities: ["audio"]`, and the text to be spoken is sent as the **`assistant`
message** — not the user message. The user message carries the delivery instruction.

```json
{
  "model": "mimo-v2.5-tts",
  "modalities": ["audio"],
  "audio": {"voice": "mimo_default", "format": "mp3"},
  "messages": [
    {"role": "user", "content": "Read the assistant text aloud in Malay, warm and composed."},
    {"role": "assistant", "content": "Aku tak pandang hang. Aku biar hang pandang aku."}
  ]
}
```

Separate quota bucket from MiniMax Token Plan — it is a gap-filler lane, not a duplicate.

## 2. Authenticated voice list (confirmed live 2026-09-15)

The list is self-documenting: send a bogus voice name and the 400 error enumerates it.

```json
{"code":"400","message":"Param Incorrect","param":"Unknown voice: definitely_not_a_voice.
 Available voices: [mimo_default, 冰糖, 茉莉, 苏打, 白桦, Mia, Chloe, Milo, Dean]","type":""}
```

All 9 voices generate successfully for the base model (verified individually 2026-09-15:
Mia, 茉莉, 苏打, 白桦, Dean, Milo, Chloe all HTTP 200). The list matches the 2026-08-21 record
— it has not drifted. These are Chinese-market voices; **none is a Malay voice.**

## 3. Response shape and decoding — base64, not hex

Audio arrives base64-encoded in `choices[0].message.audio.data`:

```
choices[0].message.audio.id          -> audio object id
choices[0].message.audio.data        -> base64 audio bytes
choices[0].message.audio.transcript  -> always null in every probe on 2026-09-15
choices[0].message.content           -> "" (empty; the spoken text is NOT echoed back)
choices[0].message.tool_calls        -> present, empty
```

```python
import json, base64
j = json.loads(raw_response)
blob = base64.b64decode(j["choices"][0]["message"]["audio"]["data"])
open("out.mp3", "wb").write(blob)
```

- MP3 payloads begin `FF F3` (MPEG frame sync). WAV payloads begin `RIFF`.
- **Do not confuse this with MiniMax `t2a_v2`, which returns HEX.** MiMo is base64.
  Base64 char count ≈ 1.33 × byte count (observed 89,856 chars → 67,392 bytes).
- `audio.transcript` being null means you cannot trust the API to tell you what it said —
  that is exactly why §11 exists.

## 4. Format handling (measured 2026-09-15)

| `audio.format` | Result | Bytes for the 88-char probe |
|---|---|---|
| `"mp3"` | MP3, 24 kHz mono | 54,744 (Mia) … 67,392 (mimo_default) |
| `"wav"` | RIFF WAV, PCM16 24 kHz mono | 460,844 (≈7× the MP3) |
| omitted | **RIFF WAV** — default is WAV, not MP3 | 361,004 |

Always state `format` explicitly; omitting it silently returns WAV (large payloads,
large base64 strings, slower round-trip).

## 5. Call shape — `mimo-v2.5-tts-voicedesign` (PROVEN 2026-09-15)

Works **only** when the description is a **top-level `voice_design` object** and
`audio.voice` is **omitted entirely**:

```json
{
  "model": "mimo-v2.5-tts-voicedesign",
  "modalities": ["audio"],
  "audio": {"format": "mp3"},
  "voice_design": {"prompt": "Warm, composed Malaysian male voice. Deep chest register,
   slow deliberate pace, Penang northern cadence. No theatricality."},
  "messages": [
    {"role": "user", "content": "Read the assistant text aloud in Malay, warm and composed."},
    {"role": "assistant", "content": "<BM text>"}
  ]
}
```

Including `audio.voice` returns the documented hard error, verbatim:

```json
{"code":"400","message":"Param Incorrect",
 "param":"audio.voice is not supported for voice design model","type":""}
```

**The `voice_design` prompt is effectively REQUIRED.** Omitting the field still returns
HTTP 200, but the output is non-speech: the same file decoded twice by the same ASR gave
two different fictional boilerplate sentences ("Saya akan berhubungan untuk mencari
kembali" / "Saya akan berkata kepadang ke utubaya…"), and its spectral flatness measured
0.1029 versus 0.0104 for a reference speech signal. Treat a return without `voice_design`
as a generation failure, not a default voice.

## 6. Call shape — `mimo-v2.5-tts-voiceclone` (PROVEN 2026-09-15)

Works when `audio.voice` is a **data URL** carrying the reference audio. Nothing else:

```json
{
  "model": "mimo-v2.5-tts-voiceclone",
  "modalities": ["audio"],
  "audio": {"voice": "data:audio/mp3;base64,<BASE64_MARKER_OF_REFERENCE>", "format": "mp3"},
  "messages": [
    {"role": "user", "content": "Read the assistant text aloud in Malay, warm and composed."},
    {"role": "assistant", "content": "<BM text>"}
  ]
}
```

Sending a plain voice name returns the other documented hard error, verbatim:

```json
{"code":"400","message":"Param Incorrect",
 "param":"audio.voice must be a DataURL for voice clone model","type":""}
```

Reference used here: a **20.05 s / 322,547-byte MP3** (MiniMax BossyLeader reading BM),
which becomes a **430,064-char** data URL. The whole reference is re-uploaded inline on
every call — there is no server-side voice registration and no voice id to reuse. Cost of
the reference rides on every request.

## 7. The defect — `mimo-v2.5-tts` mangles Malay (RECORDED 2026-09-15)

Probe text (88 chars), spoken verbatim as the assistant message:

> `Aku tak pandang hang. Aku biar hang pandang aku. Badan aku tahu sebelum kepala aku tahu.`

Transcribed by **two independent engines** — Groq `whisper-large-v3-turbo` (cloud) and
local `faster-whisper large-v3` (CTranslate2 weights, `condition_on_previous_text=False`) —
so the mangling is in the audio, not in one ASR's quirks:

| Lane / voice | Chars | Dur (s) | Turbo transcript | Large-v3 transcript | Match |
|---|---|---|---|---|---|
| base / `mimo_default` | 88 | 12.32 | Aku tak pandang hang. Aku **bayar** hang pandang aku. Badan aku tahu sebelum **keba** aku tahu. | …Aku **bayar** Heng… sebelum **kabar** aku tahu. | 95.9 / 92.9% |
| base / `冰糖` | 88 | 8.48 | Atutab panggung, aku, Biharhan, Pantang aku, Pantang aku, Tahu, Sipilong, Kepalel aku, Tahu. | atutah pangjanghan aku birhan pandang aku padang aku tahu sebalong kepalaku tahu | 76.2 / 84.8% |
| base / `mimo_default` | 625 | 51.36 | Sini. **Dugul gerha** sikit… Bukan pasal **di**. Pasal **kar** kita jalan dalam **hitumi**… aku tak **bandong hing**… **dukan pensi**… **Peng an** aku **sego** masa hang **sepot nabadi**… **Aaring ong ahak kutaka** hati yang **tenel** tak pun **lubuki**… **du dayam** denga **banyi kepaz** **Dengan ujana ta zink** **tenggu bagam** aku **Kakab** dulu… **Kakaku masaka** | …**duku gerah** sikit… bukan pasal **di pasakar** kita jalan dalam **hitumi**… tak **bandang hing**… **dukan pensi**… **Peng'an** aku **segel** masa hangse**p putna badi**… **isi alat**… **Aring, unggah aku terka**… **tenang tak perluluh buki**… **gabungi kepaz**… **tunggu bagaimana** aku **kakap** dulu… **Oh kak, aku mesak.** | 28.2 / 12.6% |
| base / `mimo_default` | 517 | 56.16 | Bila **huyantar in** petang petang… **daidup tepi tingkap**… **mena nakan** kepala aku yang **penakberkir**… **Hidum ni bukan pelumbun**… **Tasalah simpang Tanya arang**… | Bila hujan **tering** petang-petang, aku selalu **terhidup** tepi **tingkat**… **termena nakkan** kepala… **penat berker**… **hidup mit berumbun**… **Insepas-insepas bima ni?**… **pelombong**… **Pemilu tujuh perjalanan similuh**… | 4.1 / 27.4% |

**The MiniMax control is the proof this is not an ASR limitation.** Identical probe text,
`speech-2.8-hd` / `Indonesian_BossyLeader` / speed 0.85, transcribed by the same two engines:
**100.0% and 100.0%** (short form), **96.2% and 99.8%** (long form). The ASR is capable of
perfect BM on the same text; MiMo is the variable.

Characteristic MiMo damage patterns: `biar`→`bayar`, `kepala`→`keba`/`kabar`,
`duduk`→`duku`/`dugul`, `kita`→`kar`, `hidup ni`→`hitumi`, `tak pandang hang`→`tak bandong hing`,
`bukan benci`→`dukan pensi`, `Tangan`→`Peng an`, `sejuk`→`sego`/`segel`, `isyarat`→`isialat`/`isi alat`,
`bunyi kipas`→`banyi kepaz`/`gabungi kepaz`, `otak`→`Kakab`/`Oh kak`, `masuk kerja`→`masaka`/`mesak`.
Fidelity degrades monotonically with length: ~93–96% at 88 chars → ~12–28% at 517–625 chars.

## 8. Long-form collapse and the 3.3× duration non-determinism (RECORDED 2026-09-15)

Two identical requests (same model, same voice, same 625-char text) produced:

| Run | Duration | Throughput | Turbo match | Large-v3 match |
|---|---|---|---|---|
| 1 | 51.36 s | 12.2 chars/s | 28.2% | 12.6% |
| 2 | **168.96 s** | 3.7 chars/s | 15.7% | 16.8% |

A **3.3× duration swing on byte-identical input**. The same text through
`mimo-v2.5-tts-voicedesign` gave 51.36 s and through `mimo-v2.5-tts-voiceclone` 64.48 s, so
run 2 did not merely hit a slow path — the base model is non-deterministic in output length.
For anything with a duration budget this alone disqualifies the base model.

Additionally the tail regions of run 2 are not speech-like. Frame analysis (50 ms frames):

| Window | RMS (dBFS) | Active frames | Spectral flatness | Voiced |
|---|---|---|---|---|
| MiniMax reference 0–10 s | −24.3 | 60.2% | **0.0243** | 42.8% |
| C2 base run2 0–10 s | −23.4 | 53.1% | 0.0216 | 68.1% |
| C2 base run2 57–110 s | −22.6 | 31.0% | **0.1076** | 52.2% |
| C2 base run2 110–139 s | −18.6 | 47.8% | **0.1767** | 52.1% |
| C2 base run2 139–169 s | −18.6 | 58.7% | **0.1596** | 64.1% |

Flatness 4–8× the reference signal in the tail = broadband/noise-like content, not speech.

## 9. The "Terima kasih kerana menonton!" sign-off — **NOT REPRODUCED as MiMo behaviour**

This was the specific hypothesis to test on a 400+ char BM paragraph. It **did** appear in
the first transcript pass, but falsification killed it: **the phrase is a Whisper hallucination,
not something MiMo spoke.** Recording the falsification because the false positive is the
more dangerous artifact.

**Step 1 — it appeared.** Groq turbo, on the 625-char base-model run 2:

```
… But then, Terima kasih kerana menonton Jangan lupa like, share dan subscribe,
share dan subscribe. Terima kasih kerana menonton!
```
Segment timestamps placed it at **57.86–109.46 s** (a 51.6 s segment) and **139.48–169.46 s**.

**Step 2 — the controls hallucinate too.** The same phrase was returned for a control clip
carved from a stretch `ffmpeg silencedetect` classes as **silence** (102.83–110.19 s of run 2,
measured −108.2 dBFS, 0.0% active frames — true digital silence):

```
Groq turbo  → "Terima kasih kerana menonton!"
faster-whisper large-v3 → "Terima kasih kerana menonton"
```

Both engines emit it on Malay silence. A separate clean MiniMax control clip returned
"Al-Fatihah" for a stretch of perfectly transcribed BM. The phrase is Whisper boilerplate.

**Step 3 — engine disagreement inside the suspect window.** Feeding only 57.0–110.0 s to
both engines: they disagree on the phrase itself (58.8% agreement) while agreeing on the
gibberish tail:

```
turbo          → "Terima kasih kerana menonton! Masa, pasal, han si mama, di ni mama, bah ma, bah ma, bah bah ka."
large-v3       → "Oh, oh, oh, oh, oh, oh, oh, oh, oh. Masa pasal hansi mama. Tini mama. Bahama berboka."
```

large-v3 also volunteered **"Sari kata oleh SDI Media"** ("subtitles by SDI Media") on the
same file — a subtitling-vendor credit that cannot possibly be MiMo output. That is the
signature of ASR training-data boilerplate.

**Step 4 — the phrase generalises to ALL non-speech, which is why one Whisper is not a witness.**
Six synthetic controls at matched levels, both engines:

| Control | Level | turbo | large-v3 |
|---|---|---|---|
| white noise | −22.6 dBFS (matches the suspect window) | "Terima kasih kerana menonton!" | "Terima kasih kerana menonton!" |
| speech-band noise 300–3400 Hz | −22.6 dBFS | "Terima kasih kerana menonton!" | "Terima kasih kerana menonton!" |
| gated speech-band noise | −27.4 dBFS, 62% active | "Terima kasih kerana menonton!" | "Terima kasih kerana menonton!" |
| near-silence | −55 dBFS | "Terima kasih kerana menonton!" | "Terima kasih kerana menonton" |
| digital silence | −240 dBFS | "Terima kasih kerana menonton!" | "Terima kasih kerana menonton!" |
| **clean speech** | −23.7 dBFS | *correct BM, no hit* | *correct BM, no hit* |

**5 of 6 non-speech clips produce the identical phrase, and it fires at LOUD noise (−22.6 dBFS),
not just silence.** The original single-clip control was one instance of a general property: Whisper
emits fluent Malay boilerplate for *any* non-speech input. This is the strongest form of the
falsification — it no longer rests on a level-dependent edge case.

**Corollary that matters more than the sign-off itself:** both engines agree on that phrase because
they are the SAME family with the same training-data prior — agreement between them is **not**
independent confirmation. Whenever the input is non-speech, dual-Whisper returns a unanimous and
entirely fictitious Malay sentence. Two Whisper engines are one witness wearing two hats.

**Conclusion:** `NOT REPRODUCED` as MiMo behaviour. Do **not** write "MiMo invents a
YouTube sign-off" into any report. What *is* established about long-form base output:
fidelity collapse (§7), 3.3× duration non-determinism, and noise-like non-speech regions
(§8). Any future "the model hallucinated speech" claim must survive this same control test
before it is written down.

## 10. Measured F0 medians (librosa, 2026-09-15)

`librosa.yin(fmin=60, fmax=400, frame_length=2048)` per the lane order, with
`librosa.pyin` (voiced frames, hop 512) as the cross-estimator. Both agree within ~8% on
these files, so no octave-error correction is needed at this fmax.

| Lane / voice | Model | `yin` median | `pyin` median (voiced) | Register |
|---|---|---|---|---|
| base `mimo_default` | `mimo-v2.5-tts` | **183.6 Hz** | 198.3 Hz | female-ish |
| base `冰糖` | `mimo-v2.5-tts` | **269.9 Hz** | 283.8 Hz | female, high |
| base `mimo_default` 625c run1 | `mimo-v2.5-tts` | **219.9 Hz** | 237.2 Hz | female-ish |
| base `mimo_default` 625c run2 | `mimo-v2.5-tts` | **195.8 Hz** | 223.9 Hz | female-ish |
| base `mimo_default` 517c | `mimo-v2.5-tts` | **214.8 Hz** | 229.2 Hz | female-ish |
| voicedesign (male prompt) 88c | `…-voicedesign` | **78.3 Hz** | 71.4 Hz | male |
| voicedesign (male prompt) 625c | `…-voicedesign` | **98.9 Hz** | 99.7 Hz | male |
| voicedesign, no prompt | `…-voicedesign` | 90.7 Hz | 86.3 Hz | (non-speech output) |
| voiceclone (20 s ref) 88c | `…-voiceclone` | **104.1 Hz** | 99.7 Hz | male |
| voiceclone (20 s ref) 88c retest | `…-voiceclone` | 104.0 Hz | 99.7 Hz | male |
| voiceclone (20 s ref) 625c | `…-voiceclone` | **107.5 Hz** | 104.8 Hz | male |
| **MiniMax reference 88c** | `speech-2.8-hd` | **107.1 Hz** | 104.2 Hz | male |
| **MiniMax reference 625c** | `speech-2.8-hd` | **97.2 Hz** | 94.2 Hz | male |

Two consequences:

- **The base model cannot serve a male BM persona.** Its `mimo_default` median sits at
  184–236 Hz and `冰糖` at ~270 Hz. Every 2026-09-15 base-model call landed in a female
  register. Voice identity is part of the artifact — shipping it under a male persona is the
  §17 declare-vs-reality defect.

  **Cross-session range:** a concurrent session measuring the same base model on
  `mimo_default` long-form reported 159.6–224.4 Hz. The honest combined figure for the base
  model is therefore **~160–240 Hz**, i.e. female register — the *spread* is the finding:
  the base model does not hold a stable pitch across identical input, which is why a single
  measurement must never be quoted as "the" F0 of this voice. Variant measurements agree
  tightly between sessions (voicedesign 78–105 Hz, voiceclone 104–108 Hz).
- `voicedesign` honours a male register (~78–99 Hz) from a plain-text prompt, and
  `voiceclone` tracks its reference (104–108 Hz against the reference's 105.9 Hz yin median).
  Those two are the only MiMo variants with usable BM identity control.

## 11. STT falsification gate — **REQUIRED before any BM audio ships**

Every BM TTS artifact — any engine — passes through this gate before delivery. Two engines,
not one: a single Whisper pass cannot distinguish model mangling from ASR mangling (§9 is
exactly the trap).

```bash
# Engine 1 — Groq turbo (cloud, free)
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F file=@out.mp3 -F model=whisper-large-v3-turbo -F language=ms \
  -F response_format=verbose_json | python3 -c "import json,sys; print(json.load(sys.stdin)['text'])"
```

```python
# Engine 2 — local large-v3, different weights; disable cross-segment drift
from faster_whisper import WhisperModel
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
segs, info = m.transcribe("out.mp3", language="ms",
                          condition_on_previous_text=False, temperature=0.0, beam_size=5)
print(" ".join(s.text.strip() for s in segs))
```

Compare both transcripts against the input and score with
`difflib.SequenceMatcher(None, normalized_input, normalized_transcript).ratio()`.

**Pass criteria for BM:**

| Score | Action |
|---|---|
| ≥ 95% both engines | ship |
| 85–95% | ship only if the divergences are non-lexical (particles, punctuation) |
| < 85% | **do not ship** — re-render on another lane |

**Mandatory controls (this is the part that stops false verdicts):**

1. Run the **same text** through the reference lane (MiniMax) and transcribe it too. If the
   reference does not score ≥95%, your ASR or text is the problem — not the engine under test.
2. Include **non-speech controls at MATCHED LEVEL**, not just silence: synthesise white noise,
speech-band noise, and gated noise at the RMS of the suspect window (recipe: `/root/audio-lane-2026-09-15/noise_controls.py`).
   If any non-speech clip returns words — it will — that ASR hallucinates boilerplate, and you
   must check whether your suspect phrase appears in the non-speech output *before* attributing
   it to the engine. Silence alone is insufficient: Whisper also emits the phrase on loud noise,
   which is the regime real failure windows actually sit in.
   **Also required:** a clip of known-clean speech that transcribes correctly. Without it you
   cannot tell a quiet recording from a broken ASR. One clip cannot serve both roles.

2b. **Know the limit of your witness.** Two Whisper engines share a training-data prior, so their
   agreement is not independent confirmation (see §9 Step 4 — both return the same fictitious
   sentence for pure noise). Dual-Whisper is sufficient to prove *"the engine mangled this"*
   (gross damage, both engines see it) but is **not** sufficient to prove *"the engine did/did not
   say X"* in a noisy or unintelligible region. For absence/attribution claims, use an
   architecture-independent engine — a **CTC** model cannot autoregressively invent a fluent
   sentence on non-speech, so it is the correct second witness. Candidate at zero recurring cost:
   `onnx-community/mms-1b-all-ONNX` (Meta MMS, Wav2Vec2/CTC, `ms` adapter) on the VPS's existing
   `onnxruntime`. Z.AI `glm-asr-2512` is the paid alternative — confirmed dead 2026-09-15 with
   HTTP 1113 "Insufficient balance or no resource package" (needs recharge).
3. Use `response_format=verbose_json` and inspect segment timestamps. Segments tens of
   seconds long, or spanning silence, are drift artifacts.
4. Beyond transcripts, measure **duration, sample rate, and spectral flatness**. Flatness
   a multiple of a reference speech signal means non-speech content even when a transcript
   looks plausible.

## 12. Pacing — the "~0.92 chars/s" figure is a **unit error**

Still carried in the lane table. Measured 2026-09-15 on the 88-char probe (625-char
paragraph in brackets) → chars/s:

| Lane | chars/s |
|---|---|
| MiMo base `mimo_default` | 7.1 (12.2) |
| MiMo base `冰糖` | 10.4 |
| MiMo base run 2, same text as run 1 | (3.7) |
| MiMo voicedesign | 14.5 (12.2) |
| MiMo voiceclone | 9.3 (9.7) |
| **MiniMax reference** | 14.4 (12.4) |

MiMo base is **not** slow — it is in the same band as MiniMax. The historical session's own
numbers contradict the note: 771 chars in 71.4 s is 10.8 chars/s, not 0.92. The 0.92 almost
certainly records *seconds per character* (71.4/771 = 0.0926 s/char) mislabelled as chars/s.
Correct the figure wherever it propagates.

The old mitigation is harmless and still valid as a duration tool — if a render is over
budget, time-compress rather than re-rolling a non-deterministic render:

```bash
ffmpeg -y -i in.mp3 -filter:a "atempo=1.15" out.mp3   # 1.15–1.25 keeps intelligibility
```

Note this does **not** apply to the base model's failure mode: run 2 was 3.3× *too long*
but its problem was corrupted content, which atempo does not fix.

## 13. Reproduce it

```bash
source /root/.secrets/kunci-root.env   # MIMO_API_KEY, GROQ_API_KEY, MINIMAX_API_KEY

# MiMo base, BM probe
python3 - <<'PY'
import base64, json, os, urllib.request
BODY={"model":"mimo-v2.5-tts","modalities":["audio"],
      "audio":{"voice":"mimo_default","format":"mp3"},
      "messages":[{"role":"user","content":"Read the assistant text aloud in Malay, warm and composed."},
                   {"role":"assistant","content":"Aku tak pandang hang. Aku biar hang pandang aku. Badan aku tahu sebelum kepala aku tahu."}]}
r=urllib.request.Request("https://token-plan-sgp.xiaomimimo.com/v1/chat/completions",
    data=json.dumps(BODY).encode(),
    headers={"Authorization":"Bearer "+os.environ["MIMO_API_KEY"],"Content-Type":"application/json"})
open("out.mp3","wb").write(base64.b64decode(
    json.loads(urllib.request.urlopen(r).read())["choices"][0]["message"]["audio"]["data"]))
PY

# reference lane for the control
mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice Indonesian_BossyLeader --speed 0.85 --text-file probe.txt --out ref.mp3
```

## 14. Evidence index (2026-09-15 run)

All raw responses, artifacts, and measurement scripts:
`/root/audio-lane-2026-09-15/`

| Path | Contents |
|---|---|
| `mimo_probe1.py` … `mimo_probe4.py`, `voice_matrix.py` | live probes; raw JSON saved per tag |
| `mimo/*.raw.json` | unmodified HTTP responses |
| `mimo/*.mp3` | generated audio (24 kHz mono) |
| `stt_gate.py`, `f0_mangling.py`, `f0_stt_matrix.py` | Groq + F0 instrumentation |
| `cross_engine.py`, `cross_engine_largev3.json` | local large-v3 re-transcription of every artifact |
| `falsify_clause.py`, `falsify/*` | sign-off hallucination falsification (§9) |
| `window_char.py`, `window_characterisation.json` | speech/silence/noise frame analysis |
| `EVIDENCE_TABLE.json` | consolidated per-batch table |
| `refs/clone_ref_20s.mp3` | 20.05 s clone reference used for the voiceclone call |

Environment note: `MIMO_API_KEY` = `tp-` prefix. GLM-ASR (`api.z.ai`, `glm-asr-2512`) was
unavailable as a third engine — HTTP 1113 "Insufficient balance or no resource package" —
so the independent cross-check was local `faster-whisper large-v3` (CTranslate2), which
shares the Whisper family with the Groq endpoint. A non-Whisper second opinion is still
outstanding; until one is available, treat any *phrase-level* claim about MiMo speech as
unverified unless it is corroborated acoustically.
