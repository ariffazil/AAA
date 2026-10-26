---
name: voice-register-tuning
description: "Use when a TTS voice register sounds flat or wrong."
version: 1.0.0
author: Hermes
license: arifOS
tags: [voice, tts, cloning, measurement, registry, register, emotion]
metadata:
  hermes:
    category: audio
    related_skills: [voice-identity-provisioning, voice-clone-operations, voice-render-verification, voice-lane]
---

# Voice Register Tuning

Owning "make this voice better". A register is the mood the listener hears — calm, angry, tender,
performing — on top of an identity that must not change. This skill is the measured procedure for
changing the register without losing the person.

Triggers: "this voice sounds flat", "can we improve X's voice", "here's a sample of him angry",
"reply in this voice", an A/B between two clone candidates, or a claim that a clone is "better"
that has to be grounded before it goes into the registry or a live room.

Adjacent owners, do not restate them here: registry birth procedure → `voice-identity-provisioning`;
render gate and delivery → `voice-render-verification`; engine choice and failover →
`voice-engine-fallback-chain`.

## Procedure

1. **Fix the test line first.** One sentence with a question, a statement and an imperative — used
   verbatim for every voice and every setting in the comparison. Without a fixed line, no two
   numbers are comparable.
2. **Measure the incumbent and the target register.** Same axis set, both. Statistics recipe and
   the axis table: `references/measurement-recipe.md`. `parselmouth.Sound` refuses OGG — re-encode
   Telegram voice notes to mp3/wav before measuring.
3. **Read which axis is actually deficient before choosing a lever.** "Flat" is usually a
   pitch-excursion deficit, not an energy deficit; "synthetic" is usually too-high HNR and a
   dark centroid. Measure all axes — the intuitive lever is often the wrong one.
4. **Sweep settings on the existing voice first.** `speed` / `pitch` are usually the only knobs.
   Sweep a grid, measure every cell, and find the peak. The window is narrow: past roughly
   `speed 1.08` / `pitch +2` on MiniMax `t2a_v2` the f0 range COLLAPSES (observed 67 Hz → 28 Hz).
   Pushing harder is not more angry, it is flatter and faster.
5. **Only then consider re-cloning** — and follow the re-clone rules below. Expressive-only source
   material produces a different speaker.
6. **Verify intelligibility.** ASR round-trip on the winning take. A take that gains emotion and
   loses words is not an upgrade; compare against the incumbent's match %, not against a fixed
   threshold.
7. **Deliver the A/B to the principal, numbered, with the numbers beside each.** He decides with
   his ear; the measurements exist so that his ear is not the only record.

## Rules

- **Identity guard before ranking.** f0 median within 25% of baseline AND F2 within 10%. A candidate
  that fails either is a different person, not a mood of the same person. Report it as rejected with
  the drift figure instead of ranking it low.
- **Ship what was approved, not what scored best.** The principal's verdict attaches to one specific
  render. If a pushed variant measures better than the take he picked, keep it in the entry as a
  documented variant and default to the approved one.
- **Hash before minting and hash before believing a verdict.** The same audio forwarded twice has the
  same sha256 — that is not a request for a second clone. When he replies "this is better" to a
  voice message, hash the file he replied to before touching the registry; two candidates can be in
  flight at once.
- **Register split = separate keys + a tone map, never a settings argument.** A calm default and a
  mood register are two voice ids under `lane_precedence.<lane>.tone_precedent` (`calm`, `mad`, …)
  with a one-line routing rule. Verify a mood clone on calm text before promoting: a clone built
  from angry material renders neutral sentences near its source pitch (observed 171 Hz), so as a
  general default it makes the persona sound permanently angry. Put that in the entry as
  `do_not_use_for` so the next agent reads it at the resolver.
- **Route by tone, not by preference.** Verdicts are per-take and per-register: "this is normal" and
  "this is mad I like" may approve two different ids. Record both, with which register each one
  governs.
- **Promotion is allowed on an explicit sovereign verdict, with a rollback.** Move the persona's
  aliases onto the promoted key in the same write, leave the previous entry LIVE with a plain
  rollback alias (`<persona> old`), and prove the routing with
  `python3 /root/AAA/engines/resolve_voice_id.py "<trigger phrase>"` — reading the JSON is not proof.
- **A clone's provenance names every human in the audio chain.** Blending a third party's recorded
  voice into a persona clone makes the result partly that person's voice. Record each source
  component with duration and hash, and say it once, plainly, before that voice is used in a room
  the person is in. Provenance fact, not a consent ceremony.
- **Report what you gave up.** Every register choice trades something (identity drift, formant
  drift, intelligibility, brightness). Name the trade in the same message as the artifact.

## Pitfalls

- **The registry is a shared namespace across sessions.** A key you planned can appear with a
  DIFFERENT construction between your read and your write. Diff `updated_at`/`updated_by` against a
  snapshot taken at the start. If a colliding key now exists with another `provider_voice_id`, do not
  overwrite it and do not reuse the name — register under a non-colliding key and add a
  `cross_reference` block naming the other entry. A name pointing at the wrong provider id is worse
  than a new name.
- **Render-time contamination.** The engine can append an unrequested closing phrase
  (`... Terima kasih kerana menonton!`). The STT gate catches it as `INSERTED` — re-render the same
  text; never hand-edit the audio and never deliver a take with INSERTED words.
- **Two ids for one voice.** Cloning one source twice yields near-identical ids that drift apart
  later, and then nobody knows which one is the persona. Reuse the live entry instead.
- **Small ASR models mis-hear names and numerals.** Divergence on a proper noun from a `small` model
  is not evidence the take is bad; compare against the incumbent lane under the same model.
- **A single weighted score hides the decision.** Order by it if you like, but report headroom
  (candidate excursion ÷ target excursion) and the drifts beside it.

## Reporting

Short, in the principal's language, three parts: what the measurement says is wrong, what you tried
and what each attempt cost, and the one choice you recommend with its ceiling. Do not narrate the
pipeline; do not present a menu of equally-valid options when the data already orders them.

DITEMPA BUKAN DIBERI ⚒️
