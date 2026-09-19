---
name: voice-lane-verification
description: "Use when activating a TTS voice or judging a take anomaly."
version: 1.0.0
owner: AAA
category: verification-discipline
tags: [tts, voice, asr, whisper, verification, registry, activation]
triggers:
  - activating, wiring, or switching a persona voice, or asked to prove one is live
  - a round-trip / ASR gate flags an inserted word in a TTS take
  - reporting that a voice lane is down, refused, or mis-routed
  - a config change must be shown to have actually taken effect
---

# Voice-lane verification — prove the mechanism, not the intention

Two questions recur whenever a synthetic voice is involved, and both share one failure mode: an
observation that is merely *consistent* with your belief gets treated as proof of it.

1. **Is this voice route live?** (activation)
2. **Is this anomaly the engine's fault?** (take triage)

---

## Part 1 — Activating a voice: three layers, and only one of them speaks

"The voice is configured" describes three different artefacts. Say which one you changed.

| Layer | Artefact | What it proves |
|---|---|---|
| custom / non-schema keys | the assistant config, under a bespoke `voice.<lane>_locked_*` style name | **WRITTEN only.** Emits a schema warning, persists, and no runtime consumer reads it. Grep the tree for an importer before believing otherwise — a scaffold that *defines* a resolver constant is not a consumer of the key |
| provider entry | `tts.providers.<name>` (a command provider) | the route a TTS call actually takes |
| the resolver inside that provider's command | the registry that command reads (e.g. a `voice-registry.json`) | whether the id is **ALLOWED** — an unknown or REVOKED id aborts before synthesis and no file is written |

**Never report "the voice is now X" on a config write alone.** That is the claim/receipt gap: the
write happened, the route did not change. Name the artefact, then render.

**Prove the route from BOTH sides, or you have proved nothing.**

- Render the intended id → confirm the engine line names it and an output file exists.
- Push an unregistered / legacy id through the **same command** → confirm the refusal
  (`UNKNOWN voice id … not in registry`, fail closed, **no file written**).

One render on the intended id is the happy path; it passes on a resolver that accepts everything. The
refusal test is what shows the resolver is in charge. Report both, or report neither.

**Align every hardcoded id in a consumer to the registry — and keep the legacy id documented.** A
constant left holding an id that is absent from the registry is a latent fail-closed abort the moment
the route is wired to it; a scaffold constant can sit on an unregistered id at a different speed from
the lane's registry precedent for months, unnoticed. Correct the constant, comment what it was and why
it changed, and **do not delete the legacy id from the record** — its disposition (register or revoke)
belongs to the human, and a silent rewrite destroys the evidence you would need later.

**Precedent beats symmetry.** When several live ids answer to one name, read the registry's own
precedent field before choosing. Gates that only check the TEXT cannot tell them apart — only the
timbre is wrong, and you cannot hear it.

---

## Part 2 — Triaging a take: read the flagged token's OWN span before convicting it

A round-trip gate that flags an inserted word has not told you who inserted it. Two authors produce the
same signature: the engine (real render-time contamination) and the transcriber (segmentation of a real
word). Duration separates them — no human utterance of a word occupies ~80 ms.

Re-transcribe with word-level timestamps and read the flagged token's span:

```bash
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -F file=@take.mp3 -F model=whisper-large-v3-turbo -F language=ms \
  -F response_format=verbose_json -F "timestamp_granularities[]=word"
```

| flagged token's span | reading |
|---|---|
| a real span (~150 ms or more) sitting at the boundary | the engine spoke it — the take is defective, rewrite the clause and re-render |
| a **sliver** (measured: a two-word `ya bang` at **0.08 s**, wedged exactly between `puji` 5.80–6.54 and `bang` 6.62–7.12) | **transcriber segmentation of the real word's onset, not an insertion** — normalise it away and the same take reads clean with zero INSERTED |

- **Do not re-render on a sliver.** A re-roll spends a clean take and usually reproduces the same
  segmentation at the same boundary. The lever is the alias table, not a new render.
- **Position plus duration decide.** A stray beat at the very end carrying real separated timestamps and
  landing right where the line stopped is spent audio (hard-cut it, and say so). A short token mid-line
  at ~80 ms is a segmentation. A token whose timestamps run **past** the file duration is transcriber
  invention over silence — do not cut, and do not report contamination.
- **The aligner has no duration sense.** It matches tokens, not time, so its INSERTED row is a lead, not
  a verdict.

### The alias table is the deliverable, not a workaround

On dialect text one take can carry half a dozen substitutions and still round-trip clean. A low score is
usually an **unbuilt alias table**, not a bad take:

- Verify ONCE with no aliases, diff the normalised token lists (`difflib.SequenceMatcher`), and print
  every differing pair in one shot. Then re-verify with `--alias heard=written`.
- **Direction is `HEARD=WRITTEN`.** Reversing it rewrites correct tokens into tokens the source lacks
  and manufactures a false FAIL whose MISSING row names a word plainly present in the transcript.
- A multi-word key is legal (`--alias "tak ada=takde"`) and is the fix for a token-count desync — one
  written token heard as two puts every downstream token off by one and reports the remainder as
  insertions.
- Never rewrite the line to please the transcriber. Alias real-word mishears; rewrite only a
  **pronunciation limit** — a word that mangles the same way on every take, including in isolation.

### Ship only what the gate has seen

Run the full ladder — duration band, ASR round-trip, normalised similarity, INSERTED/MISSING extraction,
f0 family check — and keep its output with the artefact. A verification step retyped by hand is a step
that eventually goes missing, and the one that goes missing is usually the normalisation, which turns a
clean take into a fake low score and can hide a real insertion inside the noise.

---

## Pitfalls

- **A declaration of a pass must be made at the zoom the decision needs.** Announcing a clean take and
  then finding the defect on a closer look spends trust on every take after it. Run the decisive check
  first, then speak.
- **After a defect is fixed, re-verify the FIXED file, not the parent you already cleared.** Clearing an
  artefact you already cleared proves nothing about the one you are about to send.
- **A plan/credit boundary is a boundary, not a defect.** When a provider returns a usage-limit error,
  classify it and stop — do not swap in a substitute voice to keep the lane moving, because a swapped
  timbre breaks continuity silently while every text gate still passes. Re-probe the lane later instead
  of assuming it is still down.
- **Never collapse the chain into one "done".** Key written ≠ route live ≠ render produced ≠ take
  verified ≠ delivered. Name the position on the chain.

## Relationship to other skills

| This skill | Other skills |
|---|---|
| Is the route live, and is this anomaly real? | `abang-sado-creative-lane` — the persona lane's line craft, prompt shapes, and full take gate |
| The ASR / hallucination general case beyond voice | `machine-read-verification` — hallucination signatures, slicing, abstention rules |
| Provider config, DSP, fallback chain | `hermes-voice-config` |

This skill is a compact, self-contained statement of the two verification rules; the lanes above carry
the depth. Where a rule here and a rule there disagree, the deeper lane-specific skill wins for its own
artefacts.

DITEMPA BUKAN DIBERI ⚒️
