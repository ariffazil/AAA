# Nusantara TTS Landscape & Engine Reference — Updated 2026-08-14

## Landscape: Who's Building What

### Malaysia (Local)
| Project | Org | Type | Status | Notes |
|---------|-----|------|--------|-------|
| **MaLLaM** | Mesolitica (Husein Zolkepli) | LLM 1.1B-5B | Open, HF | 760K downloads. Community-driven, no govt funding. |
| **Malaysian-TTS-0.6B/1.7B** | Mesolitica | TTS | Open, HF | DistilCodec, 7 speakers, code-switch MS/EN. |
| **Malaysian-F5-TTS v3** | Mesolitica | TTS (voice clone) | Open, HF, CC-BY-NC | 15,631h Malaysian-Emilia corpus. Can clone from reference sample. **Needs GPU**. |
| **ILMU** | YTL AI Labs + UM | Multimodal LLM | Closed, hosted | Launch PM Aug 2025. Ilmu-Nemo-30B with NVIDIA (Mar 2026). ILMU Claw agentic (Apr 2026). |
| **Sovereign AI Cloud** | Gov Malaysia | Infrastructure | RM2B Budget 2026 | GPU/data center only. Zero allocation to language/voice layer. |
| **Nusantara TTS Engine v4** | AAA/arifOS | Prosody engine | Open, local | This engine. 5-layer, deterministic, zero GPU, gender-aware. |

### Regional
| Project | Org | Type | Status |
|---------|-----|------|--------|
| **SEA-LION v4.5** | AISG (Singapore) | LLM, 11+ SEA langs | Open, free API, agentic-ready, 1T SEA tokens |
| **Sahabat-AI** | GoTo + Indosat (Indonesia) | LLM 70B | Open, BM-adjacent |
| **Sailor2** | SAIL (Alibaba) | LLM 1B-20B | Open, multilingual SEA |

### Corpora Available for Fine-Tuning
| Dataset | Size | Source | Notes |
|---------|------|--------|-------|
| Malaysian-Emilia | 15,631h | Mesolitica | 600h Mandarin included |
| Malaysian-Emilia-v2 | Updated | Mesolitica | Post-filtered |
| Malaysian-Voice-Conversion | Derived | Mesolitica | F5-TTS training pair |
| Malaysian-Emilia-annotated | Annotated | Mesolitica | With metadata |
| Malaysian-YouTube | 5,200 | malaysia-ai | YouTube-extracted |
| Malaysian-Dialects-YouTube | 5,079 | malaysia-ai | Dialect-specific |
| CommonVoice 17.0 (ms) | 1,924 | malaysia-ai | Mozilla crowdsourced |

## Engine v4 Architecture

### Gender-Aware Profiles
```python
{
  "man": {"voice": "ms-MY-OsmanNeural", "base_rate": "+4%", "base_pitch": "+0Hz"},
  "makcik": {"voice": "ms-MY-YasminNeural", "base_rate": "-18%", "base_pitch": "-16Hz"},
  "wanita": {"voice": "ms-MY-YasminNeural", "base_rate": "+2%", "base_pitch": "+0Hz"},
}
```

Each profile has `mood_mod` with full key set in `neutral` (inherits to other moods):
- `rate_adj`, `pitch_adj` — global mood modifier
- `heavy_rate/pitch/pause` — chunk classified as HEAVY
- `good_rate/pitch/pause` — chunk classified as GOOD
- `q_pitch/pause` — question chunks
- `default_pause` — neutral chunk pause

### Extend Without Code Edit
- `vault/phonetics.json` — add Manglish→Baku mappings
- `vault/profiles.json` — add custom voice profiles (merges with defaults)

### Penang Blacklist
Phonetics layer NEVER modifies: hang, depaa, hangpa, kawe, korang, weh, lah, kan, tah, ni, tu, ish, alah, eh, ha, hmm, huh, ishk. Discovered when "hang" was being converted to "hand" by the phonetics dictionary during makcik voice test.

### Corpus Vault
Every render saves:
- Audio: `vault/<timestamp>_<sha1_hash>.ogg`
- Index: `vault/corpus.jsonl` (one JSON record per render)
- Fields: id, ts, voice, profile, mood, raw_text, normalized, plan (chunk array), audio path
- Purpose: accumulated labeled audio+text pairs for future F5-TTS fine-tuning
- Human verification: user grades output → quality label can be added

## Key Technical Findings

### Why Female AI Voices Sound "Hantu"
1. **Vocoder resolution**: Female F0 ~250-300Hz requires 32-64 spectral channels; free engines don't provide this → metallic artifacts in F2/F3/F4 formants
2. **Male prosody on female voice**: Yasmin = Osman + pitch offset. Prosodic patterns originate from male training data
3. **Human auditory cortex**: evolved to detect pitch anomalies in female range (mother-infant communication) → prediction error → "uncanny" sensation
4. **Prosodic expectation gap**: female speech has wider pitch range; flat contour triggers stronger "robotic" perception

### Malay Number System (num2ms)
- 100 = "seratus" (NOT "satu ratus")
- 1000 = "seribu" (NOT "satu ribu")
- 1000000 = "sejuta" (NOT "satu juta")
- 11 = "sebelas", 15 = "lima belas"
- 110 = "seratus sepuluh", 2500000 = "dua juta lima ratus ribu"

### RM Regex Ordering Bug
`RM2,500,000` — RM regex MUST run before comma-stripping. If comma-stripping runs first, `\b` fails between "M" and "2" (both `\w`) → RM regex captures only "2" → "ringgit dua,lima ratus ribu". Fix: RM first → strip commas → num2ms.

### Edge-TTS SSML Ceiling
Only `<prosody pitch/rate/volume>` works. `<break>`, `<mstts:express-as>` (all styles), `<emphasis>`, `<say-as>` ALL REJECTED. Full test matrix: `references/edge-tts-ssml-ceiling.md`.

## Upgrade Ladder
| Level | Engine | Cost | Quality | Penang | Female | What Unlocks |
|-------|--------|------|---------|--------|--------|--------------|
| **L0** | edge-tts | Free | Standard BM, monotone | ❌ | ❌ "hantu" | Nothing — ceiling |
| **L1** | Nusantara TTS v4 | Free | Prosody contour, gender profiles | ⚠️ phonetics | ⚠️ pitched Yasmin | Breathing, emotion |
| **L2** | MiniMax Speech 2.8 HD | Billed | HD, emotion control | ❌ | ✅ natural | Expression styles |
| **L3** | MiMo voiceclone | Free (limited) | Custom voice from sample | ✅ achievable | ✅ clone real | Penang accent |
| **L4** | F5-TTS v3 (GPU) | ~$2-4/hr | Best — 15K hours training | ✅ from data | ✅ from data | Full qualia |

## Verified Operational Facts
- RMS stdev flat vs contoured: 7.64 vs 7.32 dB — no signal (edge normalizes per chunk). Human ear = only judge.
- `edge-tts --pitch -15Hz` (space) fails; use `--pitch=-15Hz` or Python API.
- Piper TTS: no Malay (ms_MY) voices in rhasspy repo.
- MuleRouter MiniMax 2.8 HD: credit -0.7476 (needs top-up).
- Runpod: balance zero (needs top-up for GPU experiments).
- MiniMax Token Plan: weekly limit hit on TTS endpoint, resets ~Sunday.
- mmx-cli v1.0.19: `speech synthesize` returns 404 (endpoint may have changed).
