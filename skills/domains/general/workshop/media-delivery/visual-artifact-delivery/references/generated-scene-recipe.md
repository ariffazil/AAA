# Generated Human Scenes — Prompt Skeleton & Verification Harness

Companion to SKILL.md §3 and §4b. For photographic-looking scenes built from an image or video model where real people appear.

## Prompt skeleton that survives the model's improvisation

Lead with medium and camera, then scene, then people, then light, then anti-artifact tail. Every clause is load-bearing.

```
Raw documentary photograph, cinematic, <location>.
Composition: <camera relationship to the scene>.
<Foreground element, if any — see 'keep the subject out of frame' in SKILL.md §4b>.
Inside/setting: <3-5 concrete environmental nouns only — no props that carry text>.
<N> <ethnicity/age descriptor> people, <build>, <clothing with no logos>, standing well apart and fully separate,
<what most of them are doing>.
<The one who carries the scene: posture, gaze direction, what the gaze does>.
Lighting: <warm source> against <cold source>, deep shadows, faint haze.
Photorealistic skin texture and pores, natural proportions, clean anatomy, well-formed hands,
film grain, no logos, no lettering, no numbers, 35mm lens wide open, shallow depth of field,
candid sports editorial photography.
```

Keep it to one coherent moment. Two competing actions in one prompt is where warping starts.

## Iterate one variable at a time

Regenerate rather than nudge the whole prompt. Vary in this order: phenotype wording → subject count → composition → lighting → gaze/attitude. `--seed` locks the rest, so a seed change with the *same* prompt is a cheap independent sample when one variable is unknown.

## The verification harness

The point is to catch fabrication, not to admire the output. Four steps:

1. **Author ground truth first.** For a benchmark, build your own test image where you know the exact content (a known string, an exact count of shapes, a known crop region). You cannot score a model against an image whose contents you are guessing at.
2. **Read the output back with a different vision lane** than the one that made it — generate with the image model, read with the vision tool. Ask for the specific falsifiable facts (count, text, arrangement), not "describe this".
3. **Score against your own ground truth:** CORRECT / WRONG / HALLUCINATED. A model that returns a number it could not have seen is a hallucination finding and belongs in the record.
4. **Write the verdict per lane** — WORKS / PARTIAL / BLIND / FABRICATES — with the raw output pasted, so the next session does not have to re-probe.

## Composition rules that prevent fused anatomy

- Cap the cast. Say the number, say "separate", and repeat the number if the model overshoots.
- Keep everyone standing and apart; seated/overlapping bodies are where limbs merge and ownership becomes ambiguous.
- One subject may make eye contact; the rest should be occupied with their own action, so no one is posed against each other.
- Hands are the highest-risk detail. Either place them in a trivially safe position (hanging at the sides) or crop them out of frame.
- Mirrors and reflections are unreliable — the reflected body drifts from the actual one. Avoid mirror framing unless the reflection is the whole point.
