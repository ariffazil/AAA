# POV / Peek Composition & Crowd Scenes

Prompt patterns that reliably land for backstage, crowd and observer-framed imagery, plus the
synthetic-subject boundaries that apply whenever the frame implies a real person.

## The peek frame

Highest charge is usually an observer in the dark, the world in the light beyond — not a portrait.

- Foreground figure: ``the back of a broad-shouldered man in a black tank top, only his silhouette and
  the back of his head, out of focus, no face visible, in the left third of the frame``. State it
  positively; do not lean on a negative prompt to remove a face — verify instead.
- Frame it with architecture: `seen through a doorway`, `dark jambs at the left and right edges`,
  `the camera just behind him`. This reads as witnessing rather than watching, which is the point.
- The observer is the viewer's avatar. Keep them anonymous so the user can occupy the position.

## Crowd scenes need one payoff beat

Prompts that demand many simultaneous elements land only some of them. Write the scan first and the
payoff last, as a single focal action:

```
... the camera moves along the crowded room, searching across the many athletes preparing,
 then settles as one of them turns away from the glass and looks directly into the lens,
 calm, unsmiling, the faintest nod ...
```

Verify with `vision_analyze` that the payoff actually landed; if the model dropped it, regenerate.

## Phenotype and place

- Name the phenotype explicitly — regional descriptors plus skin/hair detail
  (`Malay Southeast Asian male bodybuilders, tan brown skin, short black hair, deep spray tan`).
  Left unsaid, the model drifts to East Asian or generic-tropical.
- Anchor props to the real subculture rather than generic nouns: posing trunks, a coach dabbing oil on
  a competitor's back, resistance bands, folding chairs, duffel bags, cables on concrete, mirrors.
- Match the aspect ratio of any still you intend to use as a video's first or last frame.

## Boundaries

- Do not place a real named person, or the user's own likeness, into a generated frame without a
  user-supplied reference image. Offer the reference path instead of improvising a face.
- A collective noun for a type of person (`abang sado`, `the fans`, `the regulars`) is not one person:
  ask which referent is meant rather than defaulting to one.
- Close the delivery by naming what is synthetic: the bodies, faces and observer in the frame are
  AI-generated and no one in it is real. That line is part of the deliverable.

## Quality checks specific to these frames

- Mirror-heavy rooms produce spatially impossible reflections — check a background/reflection region,
  not just the subject.
- Hand-held/coaching touches (a palm on a shoulder, a hand on a chest) are where fingers fuse into
  muscle; check those contact points at the frame where they appear.
- Heavy crowd prompts tend to warp faces in the deep background: acceptable if the foreground reads,
  but say so rather than claiming the whole frame is clean.
