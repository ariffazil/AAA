---
name: minimax-voice-design-prompts
description: "Use when designing voice prompts for MiniMax speech synthesis. Voice design prompts that hit."
---

# minimax-voice-design-prompts

## Anatomy of a hit prompt

`voice_design` takes free-form description. Keywords alone underperform full prose. Layer 4 facets:

1. **Identity** — age range, gender, ethnicity/region
2. **Vocal quality** — pitch, resonance, breathiness, texture
3. **Accent/language** — regional flavor, native or second-language
4. **Pace + delivery** — rhythm, energy, what the voice DOES in conversation

## Template (proven hit)

```
A mature [ethnicity] [gender] in their [age range] with a [texture], [pitch] voice. [Resonance detail]. Speaks [language] with [accent/regional detail]. Pace is [pace description], never [contrast]. Tone is [vibe], [secondary vibe] — like [concrete reference]. [Pronunciation note]. Pitch is [pitch descriptor].
```

## Example that hit (sado mature Penang BM)

```
A mature Malay man in his mid-30s with a deep, calm, masculine voice. Slightly husky with rich bass resonance. Speaks Penang Malay with natural warmth and confident authority. Pace is relaxed and steady, never rushed. Tone is friendly but commanding — like an older brother who is respected. Slight smile in the voice. No exaggerated emotion, no theatrical delivery. Authentic Malaysian Malay accent with Penang regional flavor. Pronunciation is clear and grounded. Pitch is medium-low.
```

Generated voice ID: `ttv-voice-2026081808404926-BdoQh6ec`

## What NOT to do

- ❌ Keywords only ("male, deep, malay") — gives generic output
- ❌ Conflicting descriptors ("calm and energetic") — model picks one and ignores the other
- ❌ "Theatrical / dramatic / exaggerated" — produces over-acting voice
- ❌ Multiple accents ("American with Scottish undertones") — confuses model

## `preview_text` is critical

The preview_text is what the model uses to render the trial sample. Make it:
- Same accent/register as intended use
- 15-30s worth of content
- Showcases the emotional range you want

## Voice IDs are persistent

Once generated, voice_id stays in your account forever. Save them:

```python
with open("/tmp/voice-id", "w") as f:
    f.write(voice_id)
```

Reuse via `text_to_audio(voice_id="ttv-voice-...", ...)`.

## Voice cloning (separate path)

`voice_clone` takes audio file paths of target voice (≥30s clean sample). Use for:
- Cloning Arif's actual voice from voice notes
- Cloning Syed's voice
- Cloning a fictional character voice from movie clips

Cost warning: "Voice will be charged upon first use."
