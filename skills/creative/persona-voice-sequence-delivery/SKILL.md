---
name: persona-voice-sequence-delivery
description: "Use when a brief asks for N numbered persona voice notes."
version: 1.0.0
author: Hermes
license: arifOS
tags: [voice, tts, persona, delivery, telegram]
metadata:
  hermes:
    category: creative
    tags: [voice, tts, persona, delivery]
    related: [abang-sado-creative-lane, abang-sado-tenderness-arc, voice-lane, multi-voice-note-assembly]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Persona Voice Sequence Delivery

How to turn a brief that contains a COUNT ("do 7 acts", "N beats", "part one … part four") into the
right number of delivered voice artifacts, gated and in order. Craft rules for the persona's register
live in the lane skills this one points at; this skill owns the **shape of the delivery**.

## The rule that gets misread

**A numbered brief is a count of ARTIFACTS, not a count of paragraphs.** Seven acts = seven separate
voice bubbles, each rendered and gated on its own. Rendering the whole numbered arc as one long take
is the recurring error: it arrives as a monologue where N hits were asked for, and the correction
comes back as *"maksud aku 7 voices act"*. The count in the brief IS the file count.

- One text file per act: `act1.txt` … `actN.txt`, each written as its own complete little piece (it
does not depend on the previous bubble being audible).
- Deliver in the brief's own order. The sequence is the argument; a shuffled batch loses it.
- **Exception:** a line the requester frames as ONE piece — a single rangkap, a single narrative
  scene, a single letter — ships as one take. The count rule applies to enumerated acts, not to a
  subject with internal movements.

## Procedure

1. **Parse the count and the register(s).** Write down N and what each act is meant to do before
   rendering anything. If the brief names one register for the whole arc, note which act (if any)
   cannot honestly be written in it.
2. **Write one file per act** — short beats, spoken prose, no markdown, no digits, no blank-line
   paragraph breaks inside a file (a blank line renders as a multi-second pause and invites a filler).
3. **Render + gate in batches of 4–5 per call.** Each take is ~10–20 s of synthesis; ten in one call
   trips the foreground cap and gets promoted to a polled background job. Loop and print one line per
   take (`verdict / match% / take path`) so the whole batch is readable at a glance.
4. **Read the receipt from the wrapper**, not just the verdict field, then read the `heard` transcript
   for the classes a score cannot see (below).
5. **Deliver in order**, one voice bubble each, then a short text line naming what shipped. No
   pipeline narration, no seed counts, no "here are seven, pick one".

## Render path (fail-closed wrapper)

`/root/scripts/sado say <textfile|->` renders on the registry-resolved persona voice, runs the ASR/f0
gate, and delivers to the declared target, returning one JSON receipt (`take`, `gate_exit`, `match`,
`inserted`, `missing`, `delivered`, `verdict`). A take that does not PASS is never delivered — so
`verdict: PASS` + `delivered: true` is the shippable state. `/root/scripts/sado-edge say <file>` is
the wallet-free fallback lane (local edge-tts, same gate, same declared target).

Use the wrapper instead of hand-assembling synthesis + `verify_take.py` + a separate send.

- **The receipt's printed take path can come back mangled by output redaction** — a numeric
take-dir stamp pattern-matches a card number and prints as `/root/forge_work/sado/take-[REDACTED:CARD]`.
Do not try to repair the string. Resolve the real directory with
`ls -dt /root/forge_work/sado/take-* | head -1`, confirm its mtime is the take just rendered, and
deliver from that path.
- Delivery on Telegram: `[[audio_as_voice]]` on its own line before each `MEDIA:/abs/path` line so
each act lands as a native voice bubble rather than a file. Many bubbles in one reply is fine — the
brief asked for N.

## Score vs transcript — what the gate cannot see

`INSERTED: none` / `MISSING: none` catches additions and deletions of whole words. It does **not**
catch a two-word fusion or a one-word semantic flip (both file as a *replace* opcode and can score
99% PASS). Always read the `heard` line — closing beats first, because that is where an arc lands.

- **A score in the high 80s is usually a respelling, not a defect.** Word-initial `biar` transcribes
  as `Biya` and pulls the match to ~89% with nothing actually wrong; `hang` → `Hank`, `urat` → `purat`,
  `dada` → `dadah` are the same class. Read the words, then ship. Never re-roll to chase a ratio.
- **A short standalone word between two pauses gets eaten.** Fold it into the clause.
- **A word that mangles identically on every take is a pronunciation limit.** Change the word; do not
  re-roll the seed.

## Register split inside a numbered arc

When the brief names a hard register across the whole arc but one act — usually the close — lands
tender by the arc's own logic, deliver the mixed set and **name the split in one clause**, then offer
to re-cut that single act in the named register. Do not silently harden the tender act to match the
label, do not soften the rest to match it, and do not present a mixed set as uniform.

## Ownership pointers

Craft for the register itself is owned elsewhere and is read-only to curation:

- `abang-sado-creative-lane` — engines, line craft, escalation by withdrawal, voice registry rules,
  image/video lanes.
- `abang-sado-tenderness-arc` — the tender/reassurance engine, and why routing a tender ask through
denial phrasing fails.

This skill deliberately does not restate their craft. It carries the multi-artifact delivery shape,
the wrapper invocation, the redacted-path workaround, and the score-vs-transcript discipline.

DITEMPA BUKAN DIBERI ⚒️
