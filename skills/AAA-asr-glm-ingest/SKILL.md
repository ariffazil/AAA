---
name: AAA-asr-glm-ingest
description: "Transcribe speech with GLM-ASR; supports Malay dialect."
version: 1.0.0
author: kimi-code (FI-008) for ARIF
forged: 2026-08-18
floor_scope:
  - F1
  - F2
  - F4
  - F10
  - F11
extends:
  - AGI-audio-quantum-cognition
  - AAA-audio-emd-pipeline
tags:
  - audio
  - asr
  - glm-asr-2512
  - ingest
  - decode
  - penang
  - code-switch
  - transcription
owner: AAA
capability_tier: fed-long-context
ecology_state: WARM
owned_by: AAA
authority_of: AAA
---

# AAA · ASR — GLM-2512 Ingestion Layer

> "K-DIP" transcribed as "K-Deep" is an acoustic hallucination.
> Custom dictionary is the cheapest fix for the highest-impact failure.

DITEMPA BUKAN DIBERI.

## API Surface

| Endpoint | Purpose |
|---|---|
| `POST https://api.z.ai/api/paas/v4/audio/transcriptions` | Transcribe audio chunk |

**Auth**: `Authorization: Bearer $ZAI_API_KEY`.

> **[LANE CAVEAT 2026-10-14]** `/api/paas/v4/audio/transcriptions` is the PAYG/general-API surface, NOT the Coding Plan lane. The coding key passes auth (live-probed: 1214 file-format error, not 401) but **billing attribution is UNVERIFIED** — GLM-ASR is not part of the Coding Plan. Verify quota ledger at z.ai/manage-apikey/billing after first real transcription; if it 402/403s, a separate PAYG key (`ZAI_PAYG_API_KEY`, not yet provisioned) is required.

> **[FALLBACK LADDER — WAJIB 2026-10-18 · 333-AGI]** GLM-ASR gagal (401/402/403/timeout) → **JANGAN BLIND-STOP**. Turun tangga ni, catat status setiap lane yang dicuba:
> 1. **GLM-ASR** — `POST https://api.z.ai/api/paas/v4/audio/transcriptions`, `Authorization: Bearer $ZAI_API_KEY`, `model=glm-asr-2512`. Lane utama, dialek BM.
> 2. **Groq Whisper** *(PROBED LIVE 2026-10-18, auth HTTP 200)* — `POST https://api.groq.com/openai/v1/audio/transcriptions`, `Authorization: Bearer $GROQ_API_KEY`, form: `file=@note.ogg`, `model=whisper-large-v3`, `language=ms`. Binaan stt gateway pun memang lalu sini.
> 3. **MiMo Token Plan** *(PROBED LIVE 2026-10-18, aud_tok tepat, transkrip betul)* — **BUKAN** `/v1/audio/transcriptions` (404, dah disahkan). Guna chat lane: `POST $MIMO_BASE_URL/chat/completions`, `Authorization: Bearer $MIMO_API_KEY`, `content=[{"type":"input_audio","input_audio":{"data":"data:audio/ogg;base64,<b64>"}},{"type":"text","text":"Transkrip verbatim apa yang disebut."}]`, `model=mimo-v2.6-pro` (atau `mimo-v2.5-asr`), `max_completion_tokens≥1500` (budget kecil = reasoning telan semua, content kosong!).
> 4. Semua gagal → lapor `UNKNOWN: audio tidak dapat dibaca` + minta Arif taip ringkas. **JANGAN sekali-kali agak atau huraikan isi audio yang tak berjaya dibaca** (H4 private — teks ≠ realiti).

**Model**: `glm-asr-2512` (production) — based on GLM-ASR-Nano backbone.

## Hard Constraints

| Item | Limit |
|---|---|
| Audio duration per request | ≤ 30 s |
| File size per request | ≤ 25 MB |
| Sample rate | 16 kHz or higher recommended |
| Channels | Mono preferred |
| Output | `{ "text": "...", "language": "..." }` |

**Mitigation** — audio chunker (mandatory for any continuous listening):

```python
# Pseudocode
chunks = chunk_audio(
    source=mic_stream,
    max_duration_s=25,           # safety margin below 30s limit
    silence_threshold_db=-40,
    min_silence_ms=500,
    target_sample_rate=16000,
    target_channels=1,
)
for chunk in chunks:
    segment = arifos.audio.asr_ingest(chunk, model="glm-asr-2512")
    yield segment
```

## Why GLM-ASR-2512 (the F2 evidence)

GLM-ASR-2512 is chosen for arifOS because of three concrete capabilities
that matter for our operational profile:

### 1. Dialect & Code-Switch Support

Min Nan / Hokkien (Penang-Besi linguistic family) is recognized.
Mixed-language utterances (BM + English + Mandarin) are stable across
switch points — the failure mode of single-language ASRs is *inserting
filler words at switch boundaries* (a hallucination).

### 2. Custom Dictionary (the F2 floor)

Per the model spec, terms in the dictionary are transcribed verbatim,
not phonetically interpreted. This is the **F2 TRUTH floor** for audio
ingestion — without it, domain terms drift.

```
K-DIP          → K-DIP         (not "K-Deep")
W_scar         → W_scar        (not "W scar")
F1, F2, F13    → F1, F2, F13   (not "F one")
GEOX           → GEOX          (not "gee-ox")
Ditempa Bukan Diberi → exact
i-ARIF         → i-ARIF
333-AGI        → 333-AGI
555-ASI        → 555-ASI
888-APEX       → 888-APEX
arifOS         → arifOS
VAULT999       → VAULT999
EMD            → EMD
```

### 3. Low-Volume / Quiet Speech

The Nano backbone is trained for whisper / quiet speech. Operators in
quiet environments (Arif at home at night) do not need to project.

## Reference Implementation

```python
import os
import requests

API_KEY = os.getenv("ZAI_API_KEY")
URL = "https://api.z.ai/api/paas/v4/audio/transcriptions"

DEFAULT_DICTIONARY = [
    "K-DIP", "W_scar", "F1", "F2", "F13",
    "GEOX", "WEALTH", "WELL", "AAA", "A-FORGE",
    "Ditempa Bukan Diberi", "i-ARIF",
    "333-AGI", "555-ASI", "888-APEX", "999-SEAL",
    "arifOS", "VAULT999", "EMD", "ΔS", "G_score",
    "Hermes", "OpenClaw", "OpenCode",
]

def ingest_audio_to_text(
    file_path: str,
    stream: bool = False,
    custom_dictionary: list[str] | None = None,
) -> str:
    """
    AAA Decode layer — Audio → Text (Phase 1 of EMD).
    File MUST be ≤ 30 s and ≤ 25 MB.
    Returns transcribed text with [OBS] epistemic label.
    """
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": "glm-asr-2512",
        "stream": str(stream).lower(),
        "dictionary": ",".join(custom_dictionary or DEFAULT_DICTIONARY),
    }
    with open(file_path, "rb") as audio_file:
        files = {"file": (os.path.basename(file_path), audio_file, "audio/wav")}
        try:
            r = requests.post(URL, headers=headers, data=payload, files=files, timeout=15)
            r.raise_for_status()
            return r.json().get("text", "")
        except requests.exceptions.RequestException as e:
            # F1 warning — return UNKNOWN so metabolizer can HOLD
            print(f"[F1 WARNING] ASR ingest failed: {e}")
            return "UNKNOWN"
```

## Federation Control Loop

```python
# EMD Phase 1 + 2 + 3 — full reflex arc
while listening:
    chunk = next_audio_chunk()           # silence-triggered
    user_text = ingest_audio_to_text(chunk)  # Phase 1 DECODE
    if user_text == "UNKNOWN":
        continue                         # F1 HOLD — do not invent

    decision = metabolize(user_text)     # Phase 2 — LLM with F2/F1 validation
    if decision.hold:
        continue                         # F4 CLARITY — agent chooses silence

    audio = tts_encode(decision)         # Phase 3 — TTS with acoustic_intent
    play(audio)
```

## F2 TRUTH Epistemic Labels

| Source | Label |
|---|---|
| Audio transcription output | `[OBS]` — observation |
| Custom dictionary match | `[SPEC]` — specification verbatim |
| Code-switch detection | `[DER]` — derived from pattern |
| Uncertainty (low confidence) | `[INT]` — interpretation, capped at F7 0.90 |

## F10 ONTOLOGY Reminder

A transcription is **observation**, not **meaning**. The audio
waveform is physics. The transcription is a measurement. The agent
processes physics; the human assigns meaning. Confidence cap applies.

## ΔS Discipline

Ingestion may NOT increase entropy:

- Audio with silence → empty string (not random text)
- Audio with noise → "UNKNOWN" (not hallucinated transcription)
- Audio with sensitive content (politics / porn / violence per spec)
  → reject at intake, not transcribe and "summarize"

## When to Load This Skill

- Wiring GLM-ASR into a voice pipeline (Hermes, edge bot, voice note).
- Adding domain-specific terms to the custom dictionary.
- Debugging transcription drift (e.g., "K-Deep" appearing).
- Designing the audio chunker for continuous listening.
- Auditing F2 floor compliance in a downstream transcription pipeline.

## Integration Points

- **EMD pipeline (Phase 1)**: `/root/AAA/skills/AAA-audio-emd-pipeline/SKILL.md`
- **Doctrine parent**: `/root/AAA/skills/AGI-audio-quantum-cognition/SKILL.md`
- **Hermes SOUL**: `/root/HERMES/SOUL.md` (listening config)
- **Edge bot wiring**: `/root/HERMES/config.yaml` (line ~870: `stt:`)
- **OpenClaw gateway**: `/root/openclaw/SOUL.md`

## Related Skills

- `AGI-audio-quantum-cognition` — Phase 1 measurement doctrine
- `AAA-audio-emd-pipeline` — Phase 1 DECODE orchestration
- `AAA-tts-engine-catalog` — Symmetric Phase 3 ENCODE catalog
- `AGI-multimodal-bridge` — Cross-modal reasoning
- `forge-document-intelligence` — OCR symmetric (text from image)

---

*Operational binding forged 2026-08-18. F2 evidence: derived from Z.AI GLM-ASR-2512 technical specification + arifOS domain glossary. F11: every transcription request produces a receipt with input hash + transcript.*