---
name: replicate-prompting
description: >
version: 1.0.0
---
# Prompting image and video models on Replicate

Distilled from Replicate's blog posts (2024-2026). Techniques are model-agnostic. For model selection and execution, see [replicate-models](../replicate-models/SKILL.md).

---

## § Image

### Writing prompts

- **Natural language, not keywords**: "A woman standing in a Tokyo alleyway at dusk, neon signs reflecting off wet pavement" beats "woman, Tokyo, alleyway, dusk, neon, wet pavement."
- **Be specific**: name exact colors, materials, lighting, camera equipment, spatial relationships.
- **Name subjects directly**: "the woman with short black hair" — avoid pronouns.
- **Long prompts win**: most models accept thousands of tokens. 12+ specific requirements work if each is stated clearly.
- **Start simple, iterate**: test small edits first, then build.

### Photographic language

- **Film stocks**: Kodak Portra 800, Fuji Velvia 50, Ilford HP5
- **Lens**: 50mm Summilux wide open, 85mm f/1.4, 24mm wide-angle
- **Depth of field**: shallow vs deep
- **Techniques**: golden hour, blue hour, long exposure, double exposure
- **Lighting**: Rembrandt (triangle on cheek), soft diffused studio, rim/backlight, flat diffused, volumetric
- **Composition**: rule of thirds, symmetry, wide/medium/close-up/macro, high/low angle, tilt-shift

### Text rendering

- Wrap text in double quotes: `"Design a poster with the title \"BLUE NOTE SESSIONS\""`
- Stick to readable fonts
- Editing: `"Change 'old text' to 'new text'"`
- Match text length to avoid layout shifts
- Some models inpaint text: mask region, prompt with new text

### Style transfer

- Name exact style: "impressionist painting," "1960s pop art," "Sumi-e ink wash"
- Describe traits if label fails: "visible brushstrokes, thick paint texture, rich color depth"
- State what stays: "keep the original composition"
- Example-based editing: provide before/after pair, model infers transformation

### Character consistency

- Clear reference description: "the woman with short black hair and green eyes wearing a navy blazer"
- Say what changes (setting, activity) and what stays (face, clothing)
- Use reference images when supported
- Break complex changes into steps

### Image editing

- **General**: specify what to keep. "keeping the pose and expression unchanged"
- **Verbs**: "change the clothes to a blue jacket" not "transform"
- **Object removal**: describe what fills the space, not just what to remove
- **Background**: describe new background in detail; specify subject stays
- **Inpainting**: mask region, prompt fill. Describe whole scene if magic prompt is off; describe only masked region if on
- **Outpainting**: ControlNet-style conditioning (edge detection, depth maps) preserves structure

### Multi-image and storyboard

- Ask for "a series" or specify grid (e.g., "2x2 storyboard grid")
- Describe each panel with consistent character descriptions
- Repeat exact descriptions for style/character continuity

### Product photography

- Materials: "brushed steel," "matte aluminum," "kraft paper," "frosted glass"
- Lighting: "soft diffused studio lighting, crisp highlights and gentle shadows"
- For brand assets: look for models with native SVG output
- For layouts: look for models with strong typography and composition

### Fine-tuning and LoRAs

- Use trigger words from trained model in every prompt
- Balance multiple LoRAs with scale parameters (0.9-1.1)
- Generate synthetic training data: generate many images, pick best, retrain

### Common image pitfalls

1. Keyword-stuffed prompts — write sentences, not tags
2. "Transform" for small edits — use targeted language
3. Not specifying what to keep
4. Negative prompts on models not trained for them
5. Too-high guidance scale → burnt contrast
6. Short prompts for complex scenes
7. Ignoring aspect ratio — most models work best at ~1 megapixel
8. Wrong model for the task — if it struggles, try another
9. Not iterating — best results come from iterative refinement

---

## § Video

### Scene description

A good video prompt is a scene description, not a caption. Layer these elements:

1. **Subject**: who or what
2. **Context**: where
3. **Action**: what happens
4. **Style**: cinematic, animated, stop-motion, documentary
5. **Camera**: dolly, tracking, static, handheld
6. **Composition**: wide shot, close-up, over-the-shoulder
7. **Ambiance**: mood and lighting

**Be specific**: "A high-speed car chase on a rain-drenched highway at night. Two muscle cars weave through heavy traffic at 140mph..." beats "A car chase."

**Overdescribe**: "a desperate man in a weathered green trench coat picks up a rotary phone... bathed in the eerie glow of a green neon sign" beats "a man on the phone."

### Camera and cinematography

- **Shot types**: wide/establishing, medium, close-up, extreme close-up
- **Motion**: static, pan, tilt, dolly, tracking, crane, handheld, drone, dolly zoom
- **Position**: eye level, low angle (powerful), high angle (vulnerable), over-the-shoulder, POV
- **Lens**: shallow depth of field, deep focus, macro, wide-angle, tilt-shift
- **Escalation pattern**: wide → medium → close-up → extreme close-up (maps well to 8-15s clips)

### Audio and dialogue

Prompt all four layers:
1. **Dialogue**: exact words or described intent
2. **Ambient sound**: rain on metal, city traffic, forest birds
3. **Sound effects**: door slamming, glass breaking, sword drawn
4. **Music**: genre, mood, instrumentation

**Dialogue tips**:
- Explicit: "The man says: My name is Ben."
- Implicit: "The man introduces himself."
- Match dialogue length to clip duration — 8s fits ~2-3 short sentences
- Use colons (not quotes) to avoid subtitle contamination: "She says: Hello there"
- Add "(no subtitles)" and repeat if needed
- Phonetic spelling for mispronounced names: "foh-fur" not "fofr"
- Tie dialogue to visual descriptions in multi-character scenes

### Multi-shot and time-coded prompting

Write timestamps directly:
```
[0-4s]: Wide establishing shot, static camera, misty bamboo forest at dawn
[4-9s]: Medium shot, slow push-in, the fighter steps forward
[9-15s]: Close-up, orbit shot, the fighter strikes, slow motion
```

**Transitions**: "Hard cut to...", "Seamless morph into...", "Whip pan to...", "Snap cut to..."

### Reference inputs

- **Image-to-video**: feed starting image; describe motion and changes
- **First/last frame interpolation**: provide both images; model generates transition
- **Subject references**: bracket syntax like `[Image1]` or `[Image2]`
- **Audio-driven**: sync video to audio — transcribe audio in prompt, match duration
- **Multi-reference**: image for appearance + video for motion + audio for rhythm + text for direction

### Style control

- Name style explicitly: "claymation," "Pixar animation," "anime," "stop-motion," "8-bit retro," "LEGO"
- Quality anchors: "hyper-realistic, 8k," "cinematic"
- Genre language: "Michael Mann cinematography" (neon, night), "Wes Anderson" (symmetrical, pastel), "Blade Runner 2049" (atmospheric, orange/teal)
- Use input images for pixel-level style control
- Grain/texture: "slightly grainy, film-like" or "VHS aesthetic" avoids too-clean AI look

### Character consistency

- Repeat descriptions verbatim across prompts
- Character sheet: "John, a man in his 40s with short brown hair, wearing a blue jacket and glasses, looking thoughtful"
- Vary scene, not character
- Reference images more reliable than text alone for facial features

### Common video pitfalls

1. Not describing audio → hallucinates inappropriate sounds (e.g., studio audience laughter)
2. Too much dialogue for clip length → unnaturally fast speech
3. Too little dialogue → gibberish or awkward pauses
4. Not specifying what to keep unchanged
5. Expecting variation from identical prompts — change the prompt, don't just rerun
6. Not prompting camera motion → static or unpredictable movement
7. Subtitle contamination — use colons, add "(no subtitles)"
8. Vague prompts for complex scenes
9. Ignoring aspect ratio and resolution (480p, 720p, 1080p)
10. Expecting real-time knowledge — models work from training data

---

## Sources

**Image**:
- [How to prompt Seedream 5.0](https://replicate.com/blog/how-to-prompt-seedream-5) (Feb 2026)
- [Recraft V4](https://replicate.com/blog/recraft-v4) (Feb 2026)
- [Run FLUX.2 on Replicate](https://replicate.com/blog/run-flux-2-on-replicate) (Nov 2025)
- [FLUX.1 Tools](https://replicate.com/blog/flux-tools) (Nov 2024)
- [Ideogram 3.0 on Replicate](https://replicate.com/blog/ideogram-v3) (May 2025)

**Video**:
- [How to make remarkable videos with Seedance 2.0](https://replicate.com/blog/seedance-2) (Apr 2026)
- [How to prompt Veo 3.1](https://replicate.com/blog/veo-3-1) (Oct 2025)
- [Wan 2.2](https://replicate.com/blog/wan-22) (Jul 2025)
- [Compare AI video models](https://replicate.com/blog/compare-ai-video-models) (Jul 2025)
