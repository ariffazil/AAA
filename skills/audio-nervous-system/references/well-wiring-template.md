# WELL Homeostasis Wiring Template — _gateway_voice_state → well_assess_homeostasis()

> Forged 2026-08-13 by Hermes Bridge. Template for connecting Layer 1 VoiceState sensor output to WELL organ diagnosis.

## The Gap

Layer 1 (`voice_state.py`) extracts prosody features and stores them on `event._gateway_voice_state`. This attribute is invisible to LLM context and transcript. BUT there is currently no consumer wired to read it and pass it through to WELL homeostasis assessment.

This file provides the wiring template for that connection.

## Implementation Pattern

### Step 1: Define the Wire Point

Location: After STT success in `gateway/run.py` (around line ~22340), immediately after `_gateway_voice_state` is set via `setattr(event, "_gateway_voice_state", _vs_features)`.

The wire fires as a fire-and-forget async task — parallel to transcription completion, not blocking any part of the response pipeline.

```python
async def wire_voice_to_well(event):
    """Fire-and-forget: read VoiceState and route to WELL homeostasis."""
    if not hasattr(event, "_gateway_voice_state"):
        return
    
    vs = event._gateway_voice_state  # dict from extract_voice_state()
    
    if not vs or not isinstance(vs, dict):
        logger.debug("voice-to-well: empty voice state")
        return
    
    try:
        # Map VoiceState features to WELL fields
        fatigue_proxy = compute_fatigue(vs)      # stress_load
        clarity_proxy = compute_clarity(vs)      # cognitive_clarity
        emotion_label = classify_emotion(vs)     # emotional_state
        
        await well_assess_homeostasis(
            mode="fatigue" | "stress" | "clarity",
            stress_load=fatigue_proxy,
            cognitive_clarity=clarity_proxy,
            emotional_state=emotion_label
        )
        
        logger.info(f"voice→well: stress={fatigue_proxy:.2f} clarity={clarity_proxy:.2f}")
    except Exception as e:
        logger.warning(f"voice-to-well wire failed: {e}")
        # Non-blocking — failure here does NOT affect conversation flow
```

### Step 2: Compute Proxy Functions

From VoiceState feature vector:

```python
def compute_fatigue(features: dict) -> float:
    """
    Fatigue score ∈ [0, 1]. Higher = more fatigued.
    
    Signal strength:
    - pitch_std↓ (less vocal variation = monotone fatigue)
    - pause_density↑ (more pauses between words = cognitive load/fatigue)
    - spectral_centroid_mean↓ (lower brightness = tired vocal quality)
    """
    pitch_std = features.get("pitch_std_hz", 50.0)
    pause_density = features.get("pause_density", 0.3)
    centroid = features.get("spectral_centroid_mean_hz", 2000.0)
    
    # Normalize signals (simplified normalization)
    norm_pitch = min(1.0, max(0.0, 1.0 - (pitch_std - 20.0) / 60.0))  # ↓ pitch_std → ↑ fatigue
    norm_pause = min(1.0, max(0.0, (pause_density - 0.2) / 0.4))       # ↑ pause → ↑ fatigue
    norm_centroid = min(1.0, max(0.0, 1.0 - (centroid - 1200.0) / 1500.0))  # ↓ centroid → ↑ fatigue
    
    # Weighted combination (pause density most reliable indicator)
    fatigue = 0.2 * norm_pitch + 0.5 * norm_pause + 0.3 * norm_centroid
    
    return min(1.0, max(0.0, fatigue))


def compute_clarity(features: dict) -> float:
    """
    Cognitive clarity ∈ [0, 1]. Higher = more clear-focused.
    
    Signal strength:
    - speech_activity_ratio↑ (clear speech has higher voiced fraction)
    - energy_avg_rms↑ (clear speech uses more vocal effort/energy)
    - voic_fraction close to speech_activity_ratio (consistent voicing)
    """
    speech_ratio = features.get("speech_activity_ratio", 0.7)
    energy_rms = features.get("energy_avg_rms_db", -20.0)
    
    # Simplified normalization (real implementation would use calibration data)
    norm_energy = min(1.0, max(0.0, -(energy_rms + 30.0) / 15.0))  # higher dB → more energy → more clear
    norm_speech = min(1.0, max(0.0, (speech_ratio - 0.4) / 0.4))   # ↑ speech ratio → ↑ clarity
    
    clarity = 0.6 * norm_energy + 0.4 * norm_speech
    return min(1.0, max(0.0, clarity))


def classify_emotion(features: dict) -> str:
    """Classify into low/neutral/high emotional arousal based on VoiceState."""
    pitch_mean = features.get("pitch_mean_hz", 150.0)
    pitch_range = features.get("pitch_max_hz", 0) - features.get("pitch_min_hz", 0)
    energy_rms = features.get("energy_avg_rms_db", -20.0)
    
    # High arousal indicators: wide pitch range, high energy
    arousal_signals = []
    
    if pitch_range > 150: arousal_signals.append(True)
    elif pitch_range < 80: arousal_signals.append(False)
    else: arousal_signals.append(None)  # inconclusive
    
    if energy_rms < -15: arousal_signals.append(True)  # loud → high arousal
    elif energy_rms > -25: arousal_signals.append(False)  # quiet → low arousal
    else: arousal_signals.append(None)
    
    true_count = sum(1 for x in arousal_signals if x)
    false_count = sum(1 for x in arousal_signals if x is False)
    
    if true_count >= 2: return "high"
    if false_count >= 2: return "low"
    return "neutral"
```

### Step 3: Integration Point in run.py

Current code at ~line 22340 in gateway/run.py:

```python
# CURRENT (Layer 1 extraction only):
if successful_transcripts and not hasattr(event, "_gateway_voice_state"):
    try:
        _vs_features = asyncio.to_thread(_extract_vs, audio_path)
        setattr(event, "_gateway_voice_state", _vs_features)
    except Exception as _vs_exc:
        logger.debug(...)
```

**Add this block directly below:**

```python
# ADD: Wire VoiceState → WELL homeostasis (fire-and-forget consumer)
try:
    asyncio.create_task(wire_voice_to_well(event))
except Exception as _wire_exc:
    logger.debug(f"voice-to-well wire setup failed: {_wire_exc}")
```

### Step 4: F9 ANTIHANTU Guard

Ensure WELL consumer NEVER surfaces VoiceState analysis in LLM-facing text:

```python
async def well_assess_homeostasis(mode: str, **kwargs):
    """F9 guard: WELL receives sensor input but output stays internal."""
    # Accepts: stress_load, cognitive_clarity, emotional_state
    # Never returns values that enter LLM context
    # Only modifies WELL internal state (reflected metrics, not sent to human)
    ...
```

## Calibration Notes

Baseline VoiceState ranges from E2E test results:

| Sample | pitch_mean Hz | pause_density | energy_rms dB |
|---|---|---|---|
| Normal greeting ("Assalamualaikum") | ~215 | ~0.39 | -21.6 |
| Fatigue sample ("Aku penat...") | ~151 | ~0.39 | varies |

Use these as preliminary calibration anchors. Refine thresholds with more real-world samples.

## Reversibility

Remove wire entirely: delete the `asyncio.create_task(...)` call in run.py, restart gateway. Zero state mutation. No config change.

## References
- Source skill: `/root/hermes-agent-dev/tools/voice_state.py`
- Wiring location: `/root/hermes-agent-dev/gateway/run.py` ~line 22340
- WELL interface: `arifOS/arifosmcp/runtime/l5_seed_graph.py` well_assess_homeostasis definition
- A-FORGE bridge: `/root/A-FORGE/audio/state_aware_tts.py` TTS hint contract
