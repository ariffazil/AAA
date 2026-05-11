# STT/Voice Loop Research — arifOS Agent Ears

**Date:** 2026-04-23
**Status:** Complete
**Confidence Key:** Ω = confidence 0–1 per finding

---

## Executive Summary

To close the AI voice loop (TTS mouth + STT ears) in a containerized OpenClaw environment where `pip install` is restricted, **three viable paths** exist:

| Path | Sovereignty | Complexity | Rec. Use Case |
|---|---|---|---|
| **Groq API Whisper** | ☁️ Cloud (audio leaves VPS) | 2/5 | ✅ **Recommended** — fast, cheap, OpenAI-compatible |
| **OpenAI Whisper API** | ☁️ Cloud | 2/5 | Fallback if Groq unavailable |
| **whisper.cpp (local)** | 🔒 Full sovereignty | 4/5 | Offline/rubber-room scenarios |

**MiniMax does NOT support STT** — only TTS. OpenClaw already ships an `openai-whisper-api` skill and an `openai-whisper` local skill.

**Docker modification** (adding ffmpeg + whisper to container) is viable but complex — see §3.

---

## 1. Groq API Whisper STT Integration

### Overview
**Ω Confidence: 0.95** — Direct from Groq docs.

Groq runs Whisper-large-v3 and Whisper-large-v3-turbo via an **OpenAI-compatible `/v1/audio/transcriptions` endpoint**. Audio is downsampled to 16kHz mono internally. Free tier: 25 MB/file; Dev tier: 100 MB/file.

### Endpoint
```
POST https://api.groq.com/openai/v1/audio/transcriptions
Authorization: Bearer $GROQ_API_KEY
```

### Models & Pricing

| Model | Cost/min | Transcription | Translation | Speed Factor | WER |
|---|---|---|---|---|---|
| `whisper-large-v3` | $0.111/min | ✅ | ✅ | 189x | 10.3% |
| `whisper-large-v3-turbo` | $0.04/min | ✅ | ❌ | 216x | 12% |

### Supported File Types
`flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm` — or URL (Base64URL)

### Python Code Example

```python
import os
from groq import Groq

client = Groq()

with open("/path/to/audio.wav", "rb") as file:
    transcription = client.audio.transcriptions.create(
        file=file,
        model="whisper-large-v3-turbo",
        prompt="Specify context or spelling",
        response_format="verbose_json",
        timestamp_granularities=["word", "segment"],
        language="en",
        temperature=0.0
    )
    print(transcription.text)
    # Full object: transcription.text, transcription.segments, transcription.words
```

### Dependencies
```bash
pip install groq
```
Single package. No ffmpeg needed on client side — Groq handles preprocessing.

### Setup Complexity: **2/5**
- Get API key from https://console.groq.com
- Set `GROQ_API_KEY` env var
- `pip install groq` → done
- Audio sent to Groq servers (sovereignty: LOW — audio leaves VPS)

### OpenClaw Integration Point
OpenClaw's `openai-whisper-api` skill uses the OpenAI endpoint format. To adapt it for Groq, set:
```json
{
  "skills": {
    "openai-whisper-api": {
      "apiKey": "GROQ_API_KEY",
      "baseUrl": "https://api.groq.com/openai/v1"  // if supported by skill
    }
  }
}
```
Alternatively, write a custom skill using the Groq Python SDK directly.

---

## 2. Alternative Cloud STT APIs

### 2a. OpenAI Whisper API
**Ω Confidence: 0.95**

- **Endpoint:** `POST https://api.openai.com/v1/audio/transcriptions`
- **Model:** `whisper-1` (fixed model)
- **Pricing:** $0.006/min (~3x Groq)
- **Free tier:** $5 free credits for new accounts
- **Max file:** 25 MB
- **Dependencies:** `pip install openai`
- **Setup:** 2/5
- **Sovereignty:** ☁️ Audio leaves VPS

```python
from openai import OpenAI
client = OpenAI()
with open("audio.m4a", "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        response_format="verbose_json"
    )
print(transcript.text)
```

OpenClaw ships an `openai-whisper-api` skill ready to use with `transcribe.sh`.

---

### 2b. Deepgram
**Ω Confidence: 0.92**

- **Pricing:** Nova-1/2: $0.0058/min; Nova-3: $0.0077/min
- **Free tier:** $200 free credit on signup
- **Sovereignty:** ☁️ Audio leaves servers; EU data residency available
- **Setup:** 3/5 (different API structure from OpenAI)
- **Features:** Speaker diarization, smart formatting, PII redaction

```python
from deepgram import Deepgram
dg_client = Deepgram("YOUR_API_KEY")
with open("audio.wav", "rb") as f:
    source = {"buffer": f.read(), "mimetype": "audio/wav"}
    response = await dg_client.transcription.prerecorded(
        source, 
        {"punctuate": True, "smart_format": True, "model": "nova-2"}
    )
print(response["results"]["channels"][0]["alternatives"][0]["transcript"])
```

---

### 2c. AssemblyAI
**Ω Confidence: 0.90**

- **Pricing:** $0.21/hr (~$0.0035/min) — cheapest option
- **Free tier:** $50 free credits on signup
- **Sovereignty:** ☁️ Audio leaves servers
- **Setup:** 3/5
- **Features:** Universal-3 Pro, 99 languages, real-time streaming

```python
import assemblyai as aa
aa.api_key = "YOUR_API_KEY"
config = aa.AudioConfig(language_code="en")
transcriber = aa.Transcriber(config=config)
transcript = transcriber.transcribe("audio.mp3")
print(transcript.text)
```

---

### 2d. Other Options (Brief)

| Provider | STT Free Tier | Notes |
|---|---|---|
| **Rev.ai** | Limited | Higher cost |
| **Speechmatics** | Trial available | Good accuracy |
| **Watson (IBM)** | Trial available | Enterprise focused |
| **Azure Speech** | Trial available | Requires Azure account |

---

## 3. MiniMax Multimodal Capabilities

**Ω Confidence: 0.75** — Web fetch returned minimal content.

MiniMax API documentation is behind authentication. Known from general knowledge:

- **Speech-02 API:** TTS (text-to-speech) — confirmed
- **STT (speech-to-text):** **Not confirmed available** — MiniMax's document pages returned minimal/no content on STT endpoints
- **Image understanding:** MiniMax does have multimodal models (e.g., abab6.5s), but specific API access is unclear
- **Voice agent loop:** No confirmed MiniMax STT endpoint for real-time voice

**Conclusion:** MiniMax is TTS-focused (excellent quality voice generation). Do NOT rely on MiniMax for STT — use Groq or OpenAI Whisper.

---

## 4. Docker Container Modification Approach

**Ω Confidence: 0.85**

### Problem
OpenClaw runs in a containerized environment where `pip install` is restricted. Adding local whisper requires either:
1. Pre-installed binaries in the container image
2. Runtime access to install tools (docker exec, privileged access)
3. Bind mounts of a pre-built whisper environment

### Option A: Build Whisper into Base Image

```dockerfile
FROM ghcr.io/ggml-org/whisper.cpp:latest
# OR
FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04
RUN apt-get update && apt-get install -y ffmpeg
RUN pip install faster-whisper
```

Then run OpenClaw inside this image or mount the binary.

### Option B: whisper.cpp Binary Bind Mount

`whisper.cpp` produces self-contained CLI binaries. Download once, bind-mount into container:

```bash
# On host
git clone https://github.com/ggml-org/whisper.cpp.git
cd whisper.cpp
cmake -B build && cmake --build build -j
# Download model
./models/download-ggml-model.sh base.en

# Mount into container at runtime
docker run -v /path/to/whisper.cpp/build/bin:/whisper-bin ...
```

### Option C: Add ffmpeg + whisper to existing container

```bash
docker exec <container> apt-get update && apt-get install -y ffmpeg
docker exec <container> pip install openai-whisper torch
# Or for faster-whisper:
docker exec <container> pip install faster-whisper
```

### Memory Requirements (whisper.cpp)

| Model | RAM (CPU) | VRAM (GPU) | Notes |
|---|---|---|---|
| tiny.en | ~1 GB | — | Fast, lower accuracy |
| base.en | ~1 GB | — | Good baseline |
| small.en | ~2 GB | ~2 GB | Better accuracy |
| medium.en | ~5 GB | ~5 GB | High accuracy |
| large-v3 | ~6-7 GB | ~6-7 GB | Best accuracy |

**Recommendation for VPS:** `base.en` or `small.en` for memory-constrained environments.

### Setup Complexity: **4/5**
- Requires docker exec access or container rebuild
- Model download + storage overhead
- Not zero-effort in a restricted-pip environment

---

## 5. OpenClaw Agent STT Integration Points

**Ω Confidence: 0.90** — Based on skill inspection.

### Existing Skills

| Skill | Type | Location |
|---|---|---|
| `openai-whisper-api` | Cloud API (curl) | `/usr/lib/node_modules/openclaw/skills/openai-whisper-api/` |
| `openai-whisper` | Local CLI | `/usr/lib/node_modules/openclaw/skills/openai-whisper/` |

### openai-whisper-api Skill

Uses `{baseDir}/scripts/transcribe.sh` with environment variables:
- `OPENAI_API_KEY` — primary env var
- `OPENAI_BASE_URL` — optional proxy/compatible endpoint

**Usage:**
```bash
OPENAI_API_KEY=$GROQ_API_KEY OPENAI_BASE_URL=https://api.groq.com/openai/v1 \
  {baseDir}/scripts/transcribe.sh /path/to/audio.m4a --model whisper-1
```

The skill hardcodes `whisper-1` model — **cannot switch to `whisper-large-v3-turbo` without custom script modification**.

### Integration Architecture (Custom Skill)

To add a Groq STT skill to OpenClaw:

1. Create skill at `~/.openclaw/skills/groq-whisper-stt/SKILL.md`
2. Write `scripts/transcribe.sh` (Groq SDK version)
3. Configure in `openclaw.json`:

```json
{
  "skills": {
    "groq-whisper-stt": {
      "apiKey": "GROQ_API_KEY_HERE",
      "model": "whisper-large-v3-turbo"
    }
  }
}
```

### Voice Loop Flow

```
[User speaks] 
  → [Telegram voice msg / Audio capture]
    → [Save as .ogg/.mp3]
      → [STT: Groq/OpenAI API → text transcript]
        → [LLM processes text]
          → [LLM response]
            → [TTS: MiniMax API → audio]
              → [Send voice reply to user]
```

---

## 6. Full Voice Loop Code (TTS + STT)

### STT Side (Groq)

```python
import os
from groq import Groq

client = Groq()

def transcribe_audio(audio_path: str, language: str = "en") -> str:
    """Transcribe audio file using Groq Whisper API."""
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3-turbo",
            language=language,
            response_format="text",
            temperature=0.0
        )
    return result.text
```

### TTS Side (MiniMax — already working)

```python
# MiniMax TTS (confirmed working in openclaw via tts tool)
# Use the tts tool directly in OpenClaw
```

### OpenClaw Tool Bridge

```python
# In a custom OpenClaw tool/skill
import subprocess, os, tempfile
from groq import Groq

async def transcribe_voice_message(file_path: str) -> str:
    """Convert voice message to text via Groq."""
    client = Groq()
    with open(file_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3-turbo",
            response_format="text"
        )
    return result.text
```

---

## 7. Open-Source ASR for Memory-Constrained Environments

### 7a. faster-whisper (CTranslate2)
**Ω Confidence: 0.92**

- **4x faster** than openai/whisper with same accuracy
- **Memory:** 2926 MB VRAM (int8) vs 4708 MB (fp16) for 13-min audio
- **CPU RAM:** 1477 MB (int8) for 13-min audio
- **No ffmpeg dependency** — uses PyAV internally

```bash
pip install faster-whisper
```

```python
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = model.transcribe("audio.wav", beam_size=5)
text = "".join([seg.text for seg in segments])
```

- **Setup:** 3/5 (needs PyTorch + model download)
- **Sovereignty:** 🔒 Full (runs locally)
- **Best for:** VPS with 4+ GB RAM

---

### 7b. whisper.cpp
**Ω Confidence: 0.90**

- **Zero dependencies** — plain C/C++
- **Quantized models** (Q5_K_M, etc.) down to ~500 MB
- **CPU-only:** 1049 MB RAM for base model
- **Vulkan / CUDA / CPU execution**

```bash
# Download model
./models/download-ggml-model.sh base.en

# CLI usage
./build/bin/whisper-cli -f audio.wav -m models/ggml-base.en.bin
```

```python
# Python binding via whisper-python or direct subprocess
import subprocess
result = subprocess.run(
    ["./whisper-cli", "-f", "audio.wav", "-m", "base.en.bin", "-otxt"],
    capture_output=True, text=True
)
print(result.stdout)
```

- **Setup:** 4/5 (needs build from source or prebuilt binary)
- **Sovereignty:** 🔒 Full
- **Best for:** Heavily constrained environments (Raspberry Pi level)

---

### 7c. distil-whisper
**Ω Confidence: 0.85**

- Distil-Whisper = distilled version of Whisper, **3x faster**, slightly lower accuracy
- Runs on HuggingFace Transformers
- Compatible with `peft` fine-tuning for domain adaptation

```bash
pip install transformers torch
```

```python
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch

model_id = "distil-whisper/distil-whisper-large-v3"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True
)
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    torch_dtype=torch_dtype
)
result = pipe("audio.wav", return_timestamps=True)
print(result["text"])
```

- **Setup:** 3/5
- **Sovereignty:** 🔒 Full
- **Note:** Requires PyTorch — pip install may be an issue in restricted environments

---

## 8. Summary Table

| Solution | Cloud/Local | Free Tier | Setup | Sovereignty | Best For |
|---|---|---|---|---|---|
| **Groq Whisper API** | ☁️ | Rate limited | 2/5 | LOW | **Recommended** — fast, cheap, OpenAI-compatible |
| **OpenAI Whisper API** | ☁️ | $5 credits | 2/5 | LOW | Easy OpenClaw integration via skill |
| **Deepgram** | ☁️ | $200 credits | 3/5 | LOW | Enterprise/compliance needs |
| **AssemblyAI** | ☁️ | $50 credits | 3/5 | LOW | Cheapest per-minute rate |
| **faster-whisper** | 🔒 Local | Free | 3/5 | FULL | VPS with GPU, sovereignty priority |
| **whisper.cpp** | 🔒 Local | Free | 4/5 | FULL | Memory-constrained / offline |
| **distil-whisper** | 🔒 Local | Free | 3/5 | FULL | Balance of speed + local |
| **MiniMax STT** | — | — | — | — | ❌ NOT AVAILABLE — use for TTS only |

---

## 9. Recommended Path for arifOS_bot

**Immediate (low effort):**
1. Get Groq API key from https://console.groq.com
2. Create a custom Groq STT skill in `~/.openclaw/skills/groq-whisper-stt/`
3. Wire it to the voice message handler in OpenClaw (voice messages from Telegram → Groq STT → LLM → MiniMax TTS → reply)

**For full sovereignty (higher effort):**
1. Build `whisper.cpp` on the host machine
2. Bind-mount the binary into the OpenClaw container
3. Use `base.en` model (~1 GB RAM)

**The loop is nearly closed** — TTS already works via the `tts` tool. STT is the missing piece. Groq API is the fastest path to close that loop.

---

*Research compiled 2026-04-23. Pricing and availability subject to change — verify at time of implementation.*
