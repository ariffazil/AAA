# Edge-TTS Free Tier SSML Ceiling — Verified 2026-08-14

## What Works
- `<prosody pitch="X" rate="Y" volume="Z">text</prosody>` — the ONLY supported tags
- Python API: `edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)`

## What Does NOT Work (all REJECTED with "No audio received")

| Tag | Status | Error |
|-----|--------|-------|
| `<break time="250ms"/>` | ❌ REJECTED | No audio received |
| `<mstts:express-as style="chat">` | ❌ REJECTED | No audio received |
| `<mstts:express-as style="gentle">` | ❌ REJECTED | No audio received |
| `<mstts:express-as style="friendly">` | ❌ REJECTED | No audio received |
| `<mstts:express-as style="affectionate">` | ❌ REJECTED | No audio received |
| `<mstts:express-as style="cheerful">` | ❌ REJECTED | No audio received |
| `<mstts:express-as style="sad">` | ❌ REJECTED | No audio received |
| `<emphasis level="strong">` | ❌ REJECTED | No audio received |
| `<say-as interpret-as="cardinal">` | ❌ REJECTED | No audio received |

## Why It Fails

1. **Monkeypatching `escape()` + `mkssml()`** — allows SSML tags through the Python text layer (bypasses `xml.sax.saxutils.escape`), but Microsoft's backend WebSocket endpoint still validates the SSML and rejects unrecognized tags.
2. **The `<speak>` template** in `communicate.py:263-281` only injects `<voice>`, `<prosody>` — no namespace declarations for `mstts:` or `<break>`.
3. **Free tier vs Azure Speech Service** — `mstts:express-as` styles require the paid Azure Speech Service with custom neural voice, not the free Edge endpoint.

## Workaround

Multi-chunk rendering + ffmpeg silence concatenation = the ONLY way to add breathing pauses on edge-tts free tier:

```python
# Split text at natural pause points, render each chunk separately,
# insert anullsrc silence segments between chunks via ffmpeg concat
```

This is exactly what `nusantara_tts.py` L2/L3 layers implement.

## Implications

- Female voice "hantu" effect is STRUCTURAL — cannot be fixed by SSML alone
- Vocal fry, breath, expression styles all require either paid Azure or a different engine (F5-TTS, MiMo voiceclone)
- The only knob available is rate + pitch per chunk — which is what the Nusantara TTS engine maximizes
