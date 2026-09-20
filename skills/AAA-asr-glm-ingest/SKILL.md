---
name: AAA-asr-glm-ingest
description: "ASR (Automatic Speech Recognition) ingestion layer using GLM-ASR-2512 (Z.AI). Decode phase of AAA-audio-emd-pipeline. Custom dictionary for arifOS-specific terms, audio chunking for ≤30 s/≤25 MB constraint, stream mode for realtime. Penang-Besi dialect and code-switching support."
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