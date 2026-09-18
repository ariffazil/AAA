---
name: persona-voice-binding
description: "Use when binding a persona agent to its voice."
version: 1.0.0
author: Hermes
license: arifOS
metadata:
  hermes:
    category: persona
    tags: [persona, tts, voice, agent-identity, binding, federation]
    related_skills: [abang-sado-creative-lane, hermes-voice-config, nusantara-voice-stack]
triggers:
  - Arif asks to init a persona agent, give it a voice, or activate that voice
  - binding an existing registry voice to a federated persona agent
  - writing or updating a persona INIT.md or its agent-card voice block
  - deciding whether a persona voice is actually live in the runtime
---

# Persona Voice Binding

Turning "make persona X speak in voice Y" into a wired, discoverable, revocable binding.

Register craft for a *specific* persona (line-writing, image/video prompts, that register's consent
rules, its line-craft pitfalls) lives in that persona's own lane skill. This skill is the **wiring**:
identity artifacts, voice resolution, route truth, and the first-take gate. Load both when the ask is
"init persona X **with voice**".

## 1. Probe the persona's home before writing anything

Personas live as directories under `/root/AAA/agents/<persona>/`. Each file has ONE job:

| File | Job |
|---|---|
| `IDENTITY.md` | function + authority boundary + appeal path |
| `SOUL.md` | conduct, register, what it never does |
| `agent-card.json` | federation registration (tier, class, capabilities, boundaries) |
| `INIT.md` | the **live boot binding** — load order, voice, route state, boot line, delivery contract |

A persona can be running with SOUL + IDENTITY + card and **no INIT at all**. So an "init persona X"
ask is usually a request to *write the binding that is missing*, not to summarise the files already
there — `ls` the directory first, then produce the artifact that is actually absent.

- **The triad lens is not a persona runtime.** `/root/AAA/prompts/INIT_PERSONA_CIVILISATION.md` is a
  federation-wide cognitive lens; loading it does not load a persona, and loading a persona does not
  grant it authority. Never ship the lens as the missing INIT.
- Read `SOUL.md` + `IDENTITY.md` in full before writing `INIT.md`: the init **restates** the
  persona's real authority boundary (who issues, what it may never do, where appeal goes), it does
  not invent one. Copying a boundary from another persona is the failure this step prevents.

## 2. Resolve the voice from the registry — never by name, never by recency

```bash
python3 - <<'PY'
import json
r = json.load(open("/root/AAA/audio/voice-registry.json"))
for lane, v in r.get("lane_precedence", {}).items():
    print(lane, "->", v["precedent_voice"], "| alternates:", v.get("alternates"))
PY
```

- The registry's `lane_precedence.<register>.precedent_voice` is the arbiter. Several ids can be LIVE
  at once and they are different timbres, not versions — choosing by name symmetry, file mtime, or
  "whichever renders first" ships the wrong identity, and the render HIDES it: every quality gate
  passes because the text is right and only the timbre is wrong, which an agent cannot hear.
- Refuse a non-`LIVE` id **before** synthesis. A `REVOKED` id must never be selectable as a default,
  an explicit id, or a fallback rung.
- **Binding an existing voice is not minting.** Leave `voice-registry.json` untouched and say so.
  Minting a new provider-side clone is a different procedure with its own consent law (a human voice
  source is identity, not material).
- **Name the voice by REGISTER, never by a person.** A registry entry is a provenance record; a real
  human's name written into one becomes citable evidence for every later session.

## 3. Write the binding down TWICE

1. **`INIT.md`** — register → `precedent_voice`, model, endpoint, speed band, provenance of that
   voice, the pre-delivery gate, and the lane scope (`persona register only, never an assistant
   default`).
2. **`agent-card.json`** — a `voice{}` block carrying the same id, model, endpoint, default speed
   + band, alternates, provenance and gate. Other federation surfaces read the card; a binding that
   lives only in prose is invisible to them.

Then state the route truth (§4) in both, so a later session reads the state instead of guessing it.

## 4. Two layers decide whether a voice is live — probe BOTH

| Layer | Where | Live? |
|---|---|---|
| Provider registry | `tts.providers.<name>` (a command provider that calls the TTS pipeline, plus that provider's own `voice:`) | **YES** — addressable by name, e.g. `text_to_speech(provider="<name>")` |
| Declared-intent keys | `voice.<persona>_locked_voice_id` / `_speed` / `_emotion` / `_model` | **NO** — persisted (with a schema warning) and read by nothing |

Never report "the default voice is now X" off the intent keys alone — that is the claim/receipt gap.
State which layer you actually changed, and probe the other one before asserting anything about the
runtime.

- **Do not touch the assistant default while binding a persona.** `tts.provider` and
  `voice.tts_provider_default` stay where they are; the persona lives on its own provider entry. A
  persona binding must never become the assistant's voice.
- **A registered route is not the CALIBRATED route.** Render the same line through both paths and
  compare `ffprobe` duration and the f0 family — not just the QC verdict. A shared pipeline can
  hardcode one speed while the lane's verified band is another: in the measured case the registered
  route came out ~8% faster while BOTH passed every gate (no insertions, f0 medians within a few Hz),
  so the drift was visible only as pace. If the band matters, pinning it means editing an engine
  shared with the default lane → **F13-class**: flag it in the init and the receipt, do not silently
  patch it, and always say which route the delivered take came from.
- When a constant inside a script contradicts the registry, write **both facts** into the artifacts
  rather than "fixing" one silently — a recorded contradiction is recoverable, a silent edit is not.

## 5. Give the persona a boot line — and gate it like any take

The init line is spoken **in the bound voice** and is the persona's own statement of what it is and
what it may never do. Not a boast, not a feature list, not a summary of its own files.

- Spoken prose only: one paragraph per line, single newlines (a blank line renders as a multi-second
  pause, which is exactly where a transcriber plants filler). No digits, no English loanwords inside
  BM text, no markdown.
- Render it through the lane's own script so the voice resolves identically every time — then run the
  ASR gate **before** shipping: match % against the input line, `INSERTED: none`, and an f0 median
  inside the clone source's family. A cloned checkpoint carries a contamination risk class (it can
  speak a clause that was never in the input) and only a transcript-vs-line diff catches that, so the
  gate is mandatory on system lines too — a boot line gets no shortcut.
- Normalise the known dialect mishears before judging the take; they are ASR behaviour on real words,
  not defects. A flagged **phrase** with no close match is an insertion and rejects the take.
- Archive the accepted take beside its input line and a receipt: request verbatim, resolved voice id
  and its provenance, what was written where, what was deliberately left untouched, and the gate
  numbers.

## 6. What "done" means here

```
PRODUCED  ≠  BOUND  ≠  LIVE
```

Write into the receipt which one you reached: the artifacts exist (**produced**), the binding is
recorded in the agent's own files (**bound**), the route answers by name (**live**). Anything you did
not probe is `UNKNOWN` — never assume it, and never let a delivery line imply a layer you did not
verify.

---

DITEMPA BUKAN DIBERI ⚒️
