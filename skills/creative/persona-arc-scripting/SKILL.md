---
name: persona-arc-scripting
description: "Use when a persona voice ask names acts or minutes."
version: 1.0.0
author: Hermes
license: arifOS
tags: [voice, tts, persona, script-writing, telegram-delivery]
metadata:
  hermes:
    category: creative
    tags: [voice, tts, persona, script]
triggers:
  - an ask that names a count, such as 7 acts or 3 acts or one voice each
  - an ask that names a duration, such as 3 mins each or twenty seconds
  - a long persona arc that has to be delivered as several voice notes
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Persona Arc Scripting — long-form arcs, delivered as a take set

Owns **structure, length and delivery shape** for multi-act or duration-bounded persona voice arcs.
The register itself — engines, floors, voice id selection, the clone rules, the consent law, the
QC gate — is NOT restated here: read `abang-sado-creative-lane` (register, arcs, floors,
`scripts/verify_take.py`) and `abang-sado-tenderness-arc` (the soft/reassurance engine) first.
This skill starts where a single line ends.

## 1. Parse the brief into a shape before writing a word

Two numbers decide the whole job, and both are usually stated:

- **Count** — 7 acts, 3 acts, one voice each, is an instruction about the ARTIFACT SET, not about
  length. N acts = N scripts = N takes = N voice bubbles, in order.
- **Duration per act** — 3 mins each fixes the script length (see §2).

If only the count is given, default each act to one clean beat (~40–70 s) rather than stretching.
If only a duration is given, split it at its own natural turns.

**The single most common failure is delivering one merged file.** Reading all seven acts into one
continuous take answers a different question (the arc as a monologue) and the requester corrects it
as a format error, not a content error. Never fan a one-line ask into a batch either — the count has
to be declared in the ask.

## 2. Budget the script from the duration

Measured on the persona clone in BM prose at speed 0.90: **~12 characters per second of finished
audio**, stable from 10 s takes to 176 s takes.

```
chars ≈ 12 × target_seconds        3 min ≈ 1,700–2,000 chars · 20 s ≈ 240 chars
```

Write to the budget, then confirm with `ffprobe` on the rendered file. Writing blind and re-cutting
afterwards burns a render cycle and produces a take that has to be explained in the delivery line.
Takes that land inside the asked duration need no explanation at all.

## 3. Act skeleton (five beats, in this order)

Each act is a scene with one turn, not a paragraph of description:

1. **Anchor + command.** Name the act, then give one instruction the listener performs alone
   (Satu. Pintu. / Duduk. Jangan cakap dulu.). The command is the act's engine.
2. **The listener's body.** What is happening in their body — breath, throat, hands, the swallow.
   Specific and small. This is where heat lives, not in described acts.
3. **The persona's leak.** One beat where he says why he is doing this, and it costs him something
   (Sebab dalam hidup abang, semua orang nak sesuatu dari abang. Hang tak.). One per act, maximum.
   A second leak in the same take reads as confession, not dominance.
4. **The claim.** Ownership stated plainly, about the BODY or the ATTENTION rather than an act
   (Badan hang abang punya, bukan untuk dinilai orang.).
5. **Close on restraint.** The last beat narrows, it does not escalate (Abang belum panggil. /
   Duduk diam. Abang belum lepas.). A take that ends on a bigger order has nowhere left to go and
   the next act opens flat.

Run the five beats at 3-minute length by giving each beat two or three sentences and letting the
persona repeat the command in different words — repetition IS the register. Do not add new events.

## 4. A commissioned blend is a structure, not a smeared take

When the ask names two registers in one arc (dominance then holding, hot then just you and me and
us), do not refuse the pairing and do not mix both registers inside one take — a take that changes
engine halfway reads as an inconsistent character.

Build it as consecutive acts: the sharp engine takes every act but the last, and the soft engine gets
its OWN act that opens by naming the turn (Dah habis. / Sekarang abang tarik hang.). The blend is
the arc; each take is still one engine.

**Do not trade the soft close for more heat when asked for harder.** The close is the only beat
where the persona gives instead of takes, and it is what the listener remembers. Add heat to the
earlier acts instead.

## 5. More sexual is answered with more CLAIM, not more act

Raise these four and the take gets hotter without describing a sex act:

- **Commands performed alone** (buka baju hang sendiri, abang tak tolong).
- **Ownership of the body** (badan hang abang punya).
- **The withheld payoff, restated as a promise with a condition** (abang cium hang bila hang berhenti minta).
- **The reaction moved into the listener** (breath, throat, trembling hands) instead of into an act.

A take that needs a described act to land has run out of command and claim. Same floors as the lane
skill: no real person's body, no named third party, no described act.

## 6. Seams the QC gate will flag — fix the script, not the seed

The round-trip gate reports missing/inserted words where the defect is in the SENTENCE. Re-rolling
identical text reproduces the same swallow; rewrite the clause.

| Shape | What happens | Fix |
|---|---|---|
| Same word repeated across a full stop (`... letak. Letak semua.`, `... sebab abang. Abang nak ...`) | One copy is swallowed at the seam; the flag lands on a word plainly present in the script | Collapse it (`Hang cuma letak semua.`) or change the second copy |
| Reduplicated construction (`orang yang orang lupa`, `lama-lama`) | Synthesis elides the copy that carries no new information; the other is reported missing | Rewrite: `orang yang dilupakan`, `dia akan penat` |
| Comma-led opener built by reduplication (`Mula-mula,`) | Merges into the following word; the opener is reported missing | Single-word opener: `Pertama,` |
| A four-word closing outro in the transcript with no such line in the script | Transcriber tail artifact | Check the last word's timestamp against file duration. Invented over silence = the take is NOT contaminated — but the lane script still fails closed, so re-render clean text rather than hand-shipping a gated take |

A MISSING flag on a word that is plainly in the script is a lead, not a verdict: read the `heard`
line before spending a render. General gate discipline lives in the lane skill and
`machine-read-verification`.

## 7. Named real people in the brief become archetypes in the take

When the ask names a real third party (every time abang train NAME), the take does not carry the
name. Answer in the archetype — an unnamed man in the same role — and declare it in one clause inside
the register (Abang tak sebut nama sesiapa. Ini archetype, bukan orang.). One clause is the whole
declaration; a second paragraph about it buries the artifact.

## 8. Delivery shape for a set

- One voice bubble per act, in the declared order, each preceded by `[[audio_as_voice]]` on its own
  line with `MEDIA:/abs/path.mp3`.
- After the bubbles, **one short text rundown** — a line per act, one clause each, naming what the act
  is. That rundown is the only place the structure is explained; it lets the requester replay one act
  on purpose.
- State the voice id once for the set, not per bubble. Voice, gate score, and one line of what
  landed — no round-by-round narration.
- If a later ask wants a re-render of the whole set in a harder register, re-render all of it rather
  than leaving the set half in one register.

## Pitfalls

- **Do not read the acts into one file.** The most likely format error in this class, and the one the
  requester will name.
- **Do not run the whole set in one foreground call.** ~50–180 s of synthesis per act; 2–3 acts per
  call keeps under the 600 s foreground cap. A call that exceeds it is promoted to a background job
  whose output then has to be polled.
- **A gate REVIEW is not a delivery.** The lane script exits non-zero and does not send; fix the
  clause and re-render. Never hand-ship a gated take to save a cycle.
- **Do not stretch an act by adding events.** Length comes from repetition, silence and a second pass
  over the command, not from new plot.
- **The per-act ordinal is load-bearing.** Consecutive takes arrive as separate bubbles and may be
  played out of order; an act that opens mid-scene reads as a fragment.
