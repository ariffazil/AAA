---
name: AAA-somatic-emd-pipeline
description: "Three-phase reflex arc for Somatic Music Intelligence in arifOS. Decode from voice-cadence somatic_proxy (WPM, pitch_mean, hesitation_ms, RMS variance) — NOT WELL until sensors ready. Metabolize adds music_intent packet field (role|BPM|density|max_seconds|kill_on_barge_in). Encode routes to parametrically-controllable music engines (MiniMax T2A Music primary). Three-layer maturity enforced: Layer 1 voice-cadence only, Layer 2 adds WELL when live, Layer 3 = F13."
version: 1.0.0
author: kimi-code (FI-008) for ARIF
forged: 2026-08-18
floor_scope:
  - F1
  - F2
  - F4
  - F7
  - F9
  - F10
  - F11
  - F13
extends:
  - AGI-audio-quantum-cognition
  - AAA-audio-qualia-doctrine
  - AAA-somatic-music-doctrine
companion:
  - AAA-audio-emd-pipeline
tags:
  - audio
  - music
  - emd
  - reflex-arc
  - somatic
  - decode
  - metabolize
  - encode
  - voice-cadence
  - well-bridge
owner: AAA
capability_tier: fed-realtime-voice
ecology_state: WARM
---

# AAA · Somatic EMD Pipeline

> Acoustic_intent without words. Same constitutional floor. Killed by the same barge-in.
> Voice-cadence proxy now; WELL biometrics when sensors live; F13 for state-change claims.

DITEMPA BUKAN DIBERI.

## The Three-Phase Reflex Arc (music)

```
        ┌─────────────────────────────────────────┐
        │  PHASE 1 — DECODE (Sense)                │
        │   Voice waveform → somatic_proxy         │
        │   Source: WPM, pitch_mean,               │
        │   hesitation_ms, RMS variance            │
        │   Label: OBS (cadence) + INT (state)     │
        │   NOT WELL until Layer 2                 │
        └────────────────┬────────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────────┐
        │  PHASE 2 — METABOLIZE (Route)            │
        │   somatic_proxy → music_intent packet   │
        │   {role, BPM_target, density,            │
        │    max_seconds, kill_on_barge_in}        │
        │   NO melody choice. NO lyric choice.     │
        │   Just acoustic parameters.              │
        └────────────────┬────────────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────────────┐
        │  PHASE 3 — ENCODE (Render)               │
        │   music_intent → MiniMax T2A Music       │
        │   Parametric: BPM, key, texture, density │
        │   Lane 6 in catalog (Layer 0 = lane 1-5) │
        │   Hard i-ARIF DENY for vocal melodic     │
        └─────────────────────────────────────────┘
```

This arc runs **in parallel** with the voice EMD pipeline
(`AAA-audio-emd-pipeline`). The two arcs share `acoustic_intent`
envelope but emit to different encoder lanes. The packet below shows
both.

## The Unified Packet (voice + music)

```python
{
    # Existing voice fields (from AAA-audio-emd-pipeline)
    "text": "Hang biar betul?",
    "epistemic_label": "INT",
    "acoustic_intent": {
        "emotion": "calm-confident",
        "intensity": 0.6,
        "pace_wpm": 165,
        "pitch_delta_hz": -8,
        "breath_tokens": ["[breath]", "[uv_break]"],
    },

    # NEW: Somatic proxy (Layer 1 source — voice cadence)
    "somatic_proxy": {
        "source": "voice-cadence",       # explicit (not WELL until Layer 2)
        "wpm": 172,                       # OBS — measured
        "pitch_mean_hz": 192,             # OBS — measured
        "hesitation_ms": 45,              # OBS — measured (low = rushed)
        "rms_variance": 0.18,             # OBS — measured (high = intense)
        "derived_state": "elevated",      # INT — F7 cap 0.90
        "derived_confidence": 0.71,       # F7-capped
    },

    # NEW: Music intent (this skill's contribution)
    "music_intent": {
        "role": "bed",                    # silence | bed | warn | none
        "bpm_target": 70,                 # derived from WPM / ~2.3
        "key": "auto",                    # engine chooses within musical bed
        "density": "low",                 # very_low | low | medium | high
        "max_seconds": 8,                 # hard cap (F1)
        "kill_on_barge_in": true,         # mandatory on voice-mode path
        "no_vocal": true,                 # no lyric, no vocal melodic
        "no_i_arif": true,                # hard DENY for i-ARIF voice_id
    },

    # Falsification gate (Layer 2 — placeholder for now)
    "falsification": {
        "voice_round_trip": null,         # STT round-trip on TTS (existing)
        "biometric_round_trip": null,     # WELL feedback (Layer 2 only)
        "rejected": False,
    },

    "policy": {
        "verdict": "ALLOW",               # ALLOW | HOLD | DENY
        "f13_token": null,                # required for Layer 3 / sustained
        "reason": "voice-cadence elevated → bed 70 BPM low density",
    },

    "receipt_id": "abc123..."             # F11 audit
}
```

## Phase 1 — DECODE (somatic_proxy from voice cadence)

### Layer 1 source (live NOW)

```python
# AAA-asr-glm-ingest / AAA-audio-emd-pipeline produces these fields.
somatic_proxy = {
    "source": "voice-cadence",
    "wpm": compute_wpm(last_n_utterances),         # OBS
    "pitch_mean_hz": compute_pitch_mean(waveform),  # OBS
    "hesitation_ms": compute_pause_distribution(),  # OBS
    "rms_variance": compute_rms_variance(waveform),  # OBS
    "derived_state": derive_state_int(...),          # INT, F7 ≤ 0.90
    "derived_confidence": F7_cap(0.90),
}
```

**Labels are non-negotiable:**

- `wpm`, `pitch_mean_hz`, `hesitation_ms`, `rms_variance` → `[OBS]` (raw measurement).
- `derived_state`, `derived_confidence` → `[INT]` (interpretation, F7 capped).
- The whole object is labeled `somatic_proxy` — never `hang_state`, `user_stress`, `arif_mood`.

**Honest derivation rules (F7 cap):**

| WPM | Hesitation | Pitch mean | Derived state (INT) | Confidence |
|---|---|---|---|---|
| < 100 | > 800 ms | < 150 Hz | `low_arousal` | ≤ 0.85 |
| 100–140 | 400–800 ms | 150–200 Hz | `stable` | ≤ 0.90 |
| 140–180 | 200–400 ms | 180–220 Hz | `focused` | ≤ 0.85 |
| > 180 | < 200 ms | > 200 Hz | `elevated` | ≤ 0.75 |

**Two listeners hear two intents.** Any agent that reports derived_state
with confidence > 0.90 has overclaimed. Return VOID.

### Layer 2 source (HOLD until WELL sensors live)

```python
# PLACEHOLDER — NOT YET WIRED.
somatic_proxy = {
    "source": "well-biometric",
    "hrv_rmssd": ...,                   # OBS — when WELL sensor live
    "heart_rate_bpm": ...,              # OBS
    "skin_conductance": ...,            # OBS
    "sleep_debt_hours": ...,            # OBS
    "derived_state": derive_state(...),
}
```

**Activation rule:** Layer 2 source can only be enabled after:
1. WELL biometric sensor hardware is live (sensor-debt currently 111 days).
2. A-FORGE Paradox Engine wired to arifOS kernel.
3. Falsification gate has run on at least 30 days of cross-correlated data.
4. `human_approval_token` to close the loop.

Until all four: Layer 1 voice-cadence is the ONLY source. No WELL
data in the packet.

## Phase 2 — METABOLIZE (harmonic router)

The metabolizer's job is **NOT to compose**. Its job is to map
`somatic_proxy` → `music_intent` parameters. No melody choice, no
lyric, no arrangement. Pure acoustic parameter routing.

### Routing Table (Layer 1)

```python
def metabolize_music_intent(somatic_proxy: dict) -> dict:
    """Layer 1: voice-cadence → music_intent. Pure routing, no composition."""

    wpm = somatic_proxy["wpm"]
    state = somatic_proxy["derived_state"]

    # F1 fail-closed
    if somatic_proxy.get("source") != "voice-cadence":
        return _silence_intent(reason="telemetry source not allowed for Layer 1")

    # Honest BPM derivation (not sacred Hz tables)
    if state == "elevated" or wpm > 180:
        return {
            "role": "bed",
            "bpm_target": 70,         # down-regulate via breath-rate match
            "key": "auto",
            "density": "low",
            "max_seconds": 8,
            "kill_on_barge_in": True,
            "no_vocal": True,
            "no_i_arif": True,
            "rationale_int": "elevated WPM suggests down-regulation via breath-rate match",
        }

    if state == "focused":
        return {
            "role": "bed",
            "bpm_target": int(wpm / 2.3),   # match cadence, not sacred tables
            "key": "auto",
            "density": "low",
            "max_seconds": 30,              # sustained focus, F11 audit
            "kill_on_barge_in": True,
            "no_vocal": True,
            "no_i_arif": True,
            "rationale_int": "focused WPM suggests cadence-matching bed",
        }

    # Default: silence (don't emit arbitrary music)
    return {
        "role": "silence",                   # F1: don't fabricate state
        "bpm_target": None,
        "max_seconds": 0,
        "rationale_int": "no state signal → silence (fail-closed)",
    }


def metabolize_f1_warning(somatic_proxy: dict, risk_class: str) -> dict:
    """F1 / high-risk: dissonance as pre-lexical alert. NO medical claim."""

    if risk_class not in {"F1_AMANAH", "F13_SOVEREIGN", "high-risk"}:
        return _silence_intent(reason="risk_class not authorized for warn")

    return {
        "role": "warn",
        "bpm_target": None,                  # dissonance is rhythm-agnostic
        "key": "auto",
        "density": "high",                   # spectral roughness ↑
        "max_seconds": 3,                    # pre-lexical only
        "kill_on_barge_in": True,
        "no_vocal": True,
        "no_i_arif": True,
        "rationale_spec": "F1 trigger → 3s spectral roughness, no lyric",
    }
```

### Hard rules in the metabolizer

1. **No lyric output.** Music with lyric in the voice-mode flow
   competes with the human's speech processing. Default is
   `no_vocal=True` and stays so unless explicit F13 override.
2. **No melody choice.** The agent picks BPM, density, duration. The
   engine picks key, timbre, arrangement. Separation of concerns.
3. **No i-ARIF clone.** If `voice_id` resolves to i-ARIF, the music
   encoder MUST DENY. i-ARIF singing is forbidden per F13 + DENY.
4. **No silence fabrication.** When state signal is missing, return
   `role: silence`, NOT a default bed. F1 fail-closed.

## Phase 3 — ENCODE (parametric music synthesis)

The encoder routes `music_intent` to a parametrically-controllable
music engine. The default lane is **MiniMax T2A Music** (music-2.6
or music-3.0).

### Engine routing

| music_intent.role | Engine | Why |
|---|---|---|
| `silence` | (no engine) | Fail-closed. Output nothing. |
| `bed` (low density) | MiniMax T2A Music (music-2.6) | Cheap, streaming-capable, BPM/key control |
| `bed` (medium density) | MiniMax T2A Music (music-3.0) | Higher fidelity when state requires richer texture |
| `warn` | MiniMax T2A Music (music-3.0) + spectral roughness prompt | F1 warning, 3s, no lyric |
| `none` | (no engine) | Caller chose silence explicitly |
| Vocal melodic content | **DENY in voice-mode flow** | i-ARIF singing forbidden; use Layer 0 composer lens instead |

### Example (MiniMax T2A Music call)

```python
import requests

def encode_music_intent(intent: dict, api_key: str) -> bytes:
    """Phase 3: emit authorized waveform."""

    # F1 fail-closed
    if intent["role"] == "silence":
        return b""

    # F13 / i-ARIF DENY
    if not intent.get("no_i_arif", False):
        return VOID  # policy gate

    # F1 frequency / dB bounds
    if intent["max_seconds"] > 30:
        return VOID  # F13 territory

    payload = {
        "model": "music-2.6",                # or music-3.0
        "prompt": _build_prompt(intent),     # see below
        "bpm": intent["bpm_target"],
        "duration": intent["max_seconds"],
        "format": "mp3",
        "sample_rate": 24000,
    }

    # CRITICAL: separate endpoint from voice clone
    # POST /v1/music_generation (not /v1/voice_clone)
    r = requests.post(
        "https://api.minimax.io/v1/music_generation",
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload,
        timeout=30,
    )
    r.raise_for_status()
    return r.content


def _build_prompt(intent: dict) -> str:
    """Translate intent → text prompt. NO lyric, NO melody choice."""
    if intent["role"] == "bed":
        density = {
            "very_low": "extremely sparse, single sustained tone, no rhythm",
            "low": "low entropy, minimal rhythm, ambient texture, no vocal",
            "medium": "moderate texture, subtle pulse, ambient, no vocal",
        }[intent["density"]]
        return f"Ambient bed, {intent['bpm_target']} BPM, {density}, no vocal"
    if intent["role"] == "warn":
        return f"Dissonant alert tone, spectral roughness, 3 seconds, no vocal"
    return "silence"
```

### Hard rules in the encoder

1. **Endpoint separation** — `/v1/music_generation` is the music lane.
   `/v1/voice_clone` is the i-ARIF lane. They MUST NOT cross. Music
   payload to clone endpoint = identity leak (F1).
2. **Format** — `mp3` for streaming, `pcm16` only for true realtime
   pipe. `wav` for archival.
3. **Timeout** — 30 s max per emission. If engine hangs, kill and
   return VOID.
4. **Reception** — receive response, write to F11 audit log with
   `receipt_id`, then route to playback.

## Kill-on-Barge-in (the same gate)

Music playback is killed by the **same** barge-in signal that kills
voice playback. Same `voice.barge_in = true` config key. Same RMS
threshold. Same grace period.

```python
# EMD Phase 3 must register a kill listener on the barge-in bus.
def on_barge_in():
    halt_music_playback()        # cut current emission
    cancel_pending_emission()    # cancel queued emissions
    return_to_silence()          # F1 fail-closed
```

When `kill_on_barge_in=True` (default for voice-mode flow), the
encoder registers this listener before emission. The music lane
inherits the same physics-of-conversation floor as the voice lane.

## Policy Gates (in voice_filters.py extension)

Layer 1 ignite adds these checks to
`/root/.hermes/voice_filters.py`:

```python
def check_somatic_policy(intent: dict, voice_id: str) -> PolicyVerdict:
    """F1 + F13 + i-ARIF DENY gates for somatic music."""

    # F1: hard fail-closed
    if intent.get("max_seconds", 0) > 30:
        return PolicyVerdict(allowed=False, reason="F1: duration > 30s without F13")

    # F1: no medical claim
    if any(kw in str(intent).lower() for kw in
           ["heal", "cure", "therapy", "therapeutic", "diagnose"]):
        return PolicyVerdict(allowed=False, reason="F9: medical claim detected")

    # F13: i-ARIF singing DENY
    if voice_id.startswith("i-ARIF") and intent.get("no_vocal") is False:
        return PolicyVerdict(allowed=False, reason="F13: i-ARIF vocal melodic DENY")

    # F1: group lane stays Sado-flat — no music overlay
    if voice_id == "ttv-voice-2026081808404926-BdoQh6ec":
        return PolicyVerdict(allowed=False, reason="F1: Sado-locked group lane, no music overlay")

    # F11: audit + receipt
    receipt = _receipt("somatic.allow", {"intent_role": intent.get("role"), "voice_id": voice_id})
    return PolicyVerdict(allowed=True, reason="Layer 1 voice-cadence", receipt_id=receipt)
```

## Layer 1 / Layer 2 / Layer 3 Activation Matrix

| Layer | What enables | Telemetry source | F13 token | Reversible? |
|---|---|---|---|---|
| **0** | `music-intelligence` exists | (none) | n/a | Read-only |
| **1** | Voice-cadence `somatic_proxy` + `music_intent` packet + MiniMax T2A Music | Voice waveform | No (F11 only) | Yes (config revert) |
| **2** | WELL biometric sensor live + Paradox Engine wired + 30-day falsification pass | Voice + WELL | **Yes** (F13 ack to close loop) | Yes (Layer 2 to Layer 1 revert) |
| **3** | i-ARIF singing / voice+music fusion / closed-loop autonomic intervention | All of above | **Yes per intervention** | Yes (each emission is revocable) |

## Integration with Voice EMD

The music EMD arc runs **alongside** the voice EMD arc, sharing
`acoustic_intent` envelope but emitting to a different lane:

```
Voice Mode conversation turn
   ↓
Phase 1 (shared) — voice cadence → somatic_proxy
   ↓
   ├── Voice EMD continues (Phase 2 → Phase 3 → TTS)
   └── Music EMD continues (Phase 2 → music_intent → Phase 3 → T2A Music)
   ↓
   Both outputs gated by:
     - barge-in (kill both)
     - voice_id policy (i-ARIF DENY for music)
     - group lane policy (Sado lock, no music overlay)
     - F11 audit (separate receipt per emission)
```

## When to Load This Skill

- Any agent adds a music lane to a Voice Mode conversation.
- Any agent emits ambient frequency during dialogue.
- Any agent routes `music_intent` to MiniMax T2A Music.
- Any agent considers WELL biometric wiring (Layer 2).
- Any agent debugs a "music didn't stop" / "music overlapped Sado" issue.
- Any agent audits an emission that claims state-change.

## Integration Points

- **Doctrine (this family)**: `/root/AAA/skills/AAA-somatic-music-doctrine/SKILL.md`
- **Engines (this family)**: `/root/AAA/skills/AAA-somatic-engine-catalog/SKILL.md`
- **Voice EMD**: `/root/AAA/skills/AAA-audio-emd-pipeline/SKILL.md`
- **ASR / voice cadence**: `/root/AAA/skills/AAA-asr-glm-ingest/SKILL.md`
- **i-ARIF DENY**: `/root/AAA/skills/AAA-voice-cloning-mimo-minimax/SKILL.md`
- **Composer lens (untouched)**: `/root/HERMES/skills/media/music-intelligence/SKILL.md`
- **Enforcement module**: `/root/.hermes/voice_filters.py` (adds somatic lane in Layer 1)
- **WELL bridge (Layer 2)**: `mcp__well__well_assess_homeostasis`
- **A-FORGE Paradox Engine (Layer 2)**: `/root/A-FORGE/paradox-engine/`

## Related Skills

- `AAA-somatic-music-doctrine` — Three-layer maturity + corrected thesis
- `AAA-somatic-engine-catalog` — Parametric engine registry
- `AAA-audio-qualia-doctrine` — F10/F9 for voice (sister doctrine)
- `AAA-audio-emd-pipeline` — Voice EMD reflex arc (sister pipeline)
- `AGI-audio-quantum-cognition` — Audio physics + floors (parent)
- `music-intelligence` — Composer lens (Layer 0, untouched)
- `AAA-voice-cloning-mimo-minimax` — i-ARIF DENY surface
- `well_assess_homeostasis` — Layer 2 substrate (HOLD)

---

*Pipeline forged 2026-08-18. F2 evidence: derivation from ARIF's corrected framing (voice-cadence proxy, music_intent packet field, kill-on-barge-in shared gate, i-ARIF singing DENY, honest BPM derivation) + AAA-audio-emd-pipeline v1.0.0 + AGI-audio-quantum-cognition v1.0.0. F1 floor absolute: fail-closed to silence when telemetry missing. F9 floor absolute: agent is instrument, not shaman.*