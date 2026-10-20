---
name: persona-voice-act-arcs
description: "Use when a persona voice ask is N numbered acts."
version: 1.0.0
tags: [voice, tts, persona, qc, telegram]
---

# Persona Voice Act Arcs

Use when the ask is a numbered sequence of spoken persona pieces — "do 7 acts", "one voice per act", "expand each to 3 minutes", "act 2 harder" — rather than a single line. Lane craft (register, engines, floors, voice choice) lives in the subject's own lane skill; this skill is the production shape: how many takes, how long each one, and how to read the gate.

## Procedure

1. **Write every act script to disk FIRST, one file per act** (`act1.txt` … `actN.txt`), then render. Writing and rendering interleaved drifts voice and pacing mid-arc.
2. **Budget each act in characters before rendering.** At the persona clone's normal speed the band is ~11.5–12.5 chars/second of input (measured: 1875 → 150 s · 1960 → 163 s · 1786 → 145 s · 1714 → 176 s); a system voice with paragraph pauses runs ~13 chars/s. A 3-minute act needs ~1900–2100 chars. Print `round(len(text)/11.7)` and adjust the PROSE — never raise the speed to hit a duration.
3. **Render two long takes per terminal call.** A 150–180 s take renders slowly enough that four in one loop exceeds the 600 s foreground cap and is promoted to a background job you then have to poll. Short takes (~10–20 s audio) batch at four or more.
4. **One engine per act; the ARC may close on a different engine than it opened.** Engines are per-take, not per-arc: acts 1..N-1 may run the hard/alpha register and the final act land tender. Never blend two engines inside one act, and never move the tender beat off the close.
5. **Ship each act as its own voice bubble, in order, then a map in text.** One line per act, six words each — what the act does. No durations, no match scores, no retry counts, no pipeline narration.

## Gate triage — the score is a lead, not a verdict

Read the `heard` transcript on every take and decide from it:

- **`MISSING` on a word genuinely gone from `heard`, at a short clause junction → REWORD, do not re-roll.** Measured: `lama-lama penat` heard as `lama penat`; a brief `sebab abang` swallowed; `orang yang orang lupa` collapsed. The score still reads 97–99% with `INSERTED: none`, so the ratio hides it. Re-rendering identical text reproduces the drop; reshape the clause (`lama-lama penat` → `dia akan penat`) and render once.
- **`MISSING` on a word plainly present in `heard` is a phantom flag** from the aligner — ship the take unmodified.
- **`INSERTED` naming an outro nobody wrote ("terima kasih kerana menonton") on an otherwise clean take is a transcriber tail, not contamination.** The script is correct and must NOT be reworded; confirm with the word-timestamp check against file duration before touching prose.
- **Trap: a clean score is not a clean take.** A two-word fusion and a one-word semantic flip have each scored 99% PASS with `INSERTED: none`. Read the closing line of every take — that is where the arc lands and where seam defects sit.

## Delivery

- **Check whether the runner already delivered before adding a `MEDIA:` line.** A wrapper that posts to a declared target (e.g. `/root/scripts/sado`, target in `/root/.config/sado.json`) returns `"delivered": true` on a pass; that field is the authority on whether the artifact reached the human, so a `MEDIA:` line for the same take on top of it is a second send. Hand-rolled renderers that only write a file need the `MEDIA:` + `[[audio_as_voice]]` pair.
- **Compliance rides in one clause, not a paragraph.** On the first artifact name the engine and the voice id; on later artifacts in the same session compress to one clause. Never a disclaimer block over a request already answered.
- **A tender close inside a hard arc is deliberate.** When the requester asks for "all of them harder", change the hard acts, not the landing — say why in one line, and offer the all-hard version as a single closing clause.

## Pitfalls

- **Do not re-render to make the number look better.** A score below 100 with every lexical word in `heard` and an intact closing line is a finished take.
- **A blank-line paragraph break renders as a multi-second pause, and that pause is where a transcriber plants filler.** One paragraph per line, single newlines.
- **Do not re-render a whole arc because one act failed the gate.** Only the failing act is rewritten; the passing acts are final.
- **A file the human sends BACK may be your own earlier render.** Before advising what to do with it — send it, edit it, who it was for — check provenance (work dirs, `~/.hermes/cache/`, session log) instead of assuming they recorded it. Telling someone to send an artifact you made reads as not knowing your own work.
