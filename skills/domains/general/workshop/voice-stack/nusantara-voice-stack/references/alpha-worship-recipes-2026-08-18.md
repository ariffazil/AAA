# Alpha-Down / Worshipper-POV Persona Recipes (proven 2026-08-18)

Session: "cocky abang sado alpha level, macho looking down to his worshipper".
Cross-modal persona package: one locked face (subject-ref) + BossyLeader voice +
Ken Burns montage when video quota is dead. Image mechanics live in
creative/minimax-cli (user-owned; pending `hermes curator adopt`).

## Identity lock (subject-ref)

```bash
source /root/.secrets/kunci-root.env
REF=/root/.hermes/cache/images/img_055d5db13fbf.jpg   # abang sado face ref
mmx image generate --base-url https://api.minimax.io \
  --subject-ref "type=character,image=$REF" \
  --prompt "<prompt below>" --aspect-ratio 9:16 --non-interactive
mv image_001.jpg /tmp/<target>.png   # --download/--output IGNORED for images
```

Local path inside `type=character,image=` WORKS (CLI uploads it). Bare/URL-shaped
path triggers `disallowed image url: localhost or private address not allowed`.
Proven: 7+ generations, one coherent identity.

## Proven prompts (vision-rated)

**D — worm's-eye worshipper POV (BEST, 9-10/10):**
"Camera at floor level, extreme worm's-eye view looking straight UP. A towering
muscular Malay man stands directly over the camera, chin tilted down, eyes locked
DOWN onto the lens with a cocky arrogant smirk. Massive chest and shoulders fill
the frame above. Black tank top. Harsh top lighting casting shadows under his
brow, dark smoky background. The viewer is kneeling at his feet. Intimidating
alpha dominance. Cinematic, 9:16 vertical."

**C — throne king (strong):**
"Extreme low angle from floor looking UP. Muscular Malay man sits on a dark
throne-like chair, one ankle on other knee, looking DOWN at camera with absolute
contempt and amusement. Hands resting on armrests. Wearing open black robe showing
sculpted abs and chest. Dramatic side lighting, smoke, cinematic color grading.
King looking at his subject. Worshipper POV. 9:16 vertical."

**A — arms crossed hoodie (good):**
"Worm's-eye view shot looking UP at a muscular Malay man standing tall. He looks
DOWN at the camera with a cocky smirk, arms crossed over massive chest. Black
sleeveless hoodie, exposed arms and shoulders. Dark dramatic studio lighting from
above, rim light on muscles. Smoke haze. Extremely dominant alpha energy. 9:16."

**B — chain grip (good, gaze slightly off-lens):**
"Low angle dramatic shot looking UP. Muscular Malay man standing with legs apart,
one hand gripping a chain around his neck. He stares DOWN at camera with intense
dominant eyes, slight smirk. Black tank top stretched over huge shoulders.
Backlit golden rim light, dark moody background. Worshipper POV. 9:16."

## What carries the dominance

- Camera position = worshipper position ("camera at floor level", "the viewer is
  kneeling at his feet"). Low angle does the power; smirk does the cocky.
- "chin tilted down, eyes locked DOWN onto the lens" — explicit gaze direction
  beats generic "dominant stare".
- Keep context gym/studio/dark-studio for safety (minimax-cli §Safety).

## Voice pairing

Cocky alpha monologue: speech-2.8-hd, `Indonesian_BossyLeader`, speed 0.82-0.85
(SKILL.md §4 + references/abang-sado-package-2026-08-18.md).

## Video quota exhausted → Ken Burns montage (proven 40.76s, 1080x1920, 5.5MB)

3 stills x 14s, ffmpeg zoompan slow push-in (alternate direction per frame) +
xfade crossfades ~1s, mux TTS mp3 `-c:v libx264 -c:a aac -shortest`. Queue real
Hailuo I2V with the same stills as `--image` input when quota resets (Sunday).
