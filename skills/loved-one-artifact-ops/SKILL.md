---
name: loved-one-artifact-ops
description: "Use when making a loved-one artifact for Arif."
version: 1.0.0
triggers:
  - "buat video birthday untuk [nama]"
  - "voice note untuk mak / abah / adik"
  - "surat / nasihat untuk [nama]"
  - "dah hantar"
  - "lama dah"
  - "tak balas"
  - "follow up on the video I sent"
  - "loved-one artifact"
tags: [family, loved-ones, artifact, voice, video, delivery, F5, witness]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Loved-one artifact ops

Class of work: personal artifacts produced **for** one of Arif's people (mak, siblings, Syed, close
friends) — birthday video, cloned-voice greeting, nasihat letter/PDF, sajak. Different from client
deliverables: short, personal, once-off, and the failure mode is emotional, not technical.

Companion skills (authoritative for their own content): `wisdom-letter-for-loved-ones` (letter
register), `human-bond-action` (bond conduct), `governed-uncertainty` (state beneath words),
`voice-lane` / `persona-voice-note-render` (render mechanics).

## 0 · Probe the store before you author or advise

This family's artifacts exist in series, not singly. Before writing anything new — and before
answering any status line — list what already exists.

```bash
ls -lat ~/.hermes/artifacts ~/.hermes/cache/videos ~/.hermes/cache/documents ~/.hermes/output 2>/dev/null | head -40
find /root/voice -maxdepth 2 -type f -newermt "-60 days" -printf '%TY-%Tm-%Td %TH:%TM  %10s  %p\n' | sort -r | head -30
find ~/.hermes/storage -maxdepth 3 -type f \( -iname '*.mp4' -o -iname '*.jpg' -o -iname '*.png' \) -printf '%TY-%Tm-%Td %p\n' 2>/dev/null | sort -r | head
```

Layout to expect:

- `/root/voice/<SLUG>-<date>/` — one directory per series: `seg1..segN` renders (`<seg>.txt` = the
exact script, `<seg>.wav` = render), the concatenated full take, often a `_v2`.
- `~/.hermes/artifacts/<slug>/` — finished videos (sajak tracks, poem videos).
- `~/.hermes/cache/videos/` — generator output, newest first; not the deliverable, but shows what
  was rendered and when.
- `~/.hermes/storage/<host>-<date>/inputs/` — inbound media the principal sent to be worked into
  the artifact (the slides that became a birthday video live here).

**The `.txt` segment files are the authoritative record of what was actually said to the person.**
Read them before drafting a follow-up — new prose that contradicts the delivered script reads as a
retraction the principal never authorised.

## 1 · Referent discipline — resolve before you read a scene

Short status lines carry no object: *"dah hantar"*, *"lama dah"*, *"tak balas"*, *"dah buat"*.
In a lane where an artifact exists, the referent is **that artifact**, not a message one human sent
another. Manufacturing the scene ("he sent it to her, she has not replied") and then counselling
the scene puts two turns of advice on a person who was never in the exchange.

- Probe (§0) first. One probe call versus two turns of wrong counsel.
- If the artifact's script answers the line, answer the artifact — not the story about it.
- When the principal names the real referent (*"hang yang buat video tu la"*), that naming is the
  whole read: drop the scene in one line and continue. Re-narrating the old scene is
  repair-by-reframe — the same sin with better manners.
- No long apology. One clause, then the substance.

## 2 · One artifact carries one truth

A delivered artifact says one thing. A birthday video says *aku sayang mak*; it does not say
*aku penat jadi satu-satunya*. When the principal keeps circling the same person after delivery,
he is not asking for the relationship to be re-explained — he is saying the artifact left one
sentence unsaid.

- Name the gap plainly, once: what the artifact said, what it did not.
- Offer the **second, shorter artifact**: no occasion, no date, 20–30 seconds, one straight
  sentence. The absence of an occasion is the point — a dated artifact can be sent late, an undated
  one cannot.
- Never re-cut, re-send, or "improve" a delivered artifact as if it were unfinished. It landed.
- One sentence of insight, then the offer. No second round of relationship analysis.

## 3 · Register rules (hard)

- BM dapur, Penang register, `hang`/`aku`. No therapy vocabulary, no "attachment", no "inner
  child" phrasing — say *budak kecik dalam aku*.
- Tersurat = sayang. Tersirat = luka. The wound is implied, never stated.
- Sign nothing the principal did not write; no agent bylines, no "dari Hermes".
- No PETRONAS/career content in artifacts for Syed's room; no system/internal vocabulary anywhere.
- Family privacy is F5-grade: these artifacts are never published, never indexed into a public
  surface, and the relationship is never profiled or scored in memory (HUMAN MEMORY LAW — story
  stays with the human, the agent keeps map only).

## 4 · Production and delivery

1. Draft the script first as plain text, one file per segment. Keep it speakable — read it aloud in
   your head; cloned voices punish long clauses.
2. Render each segment through the live voice lane (see `voice-lane`), verify each take before
   assembly — the render gate must pass before the file leaves the machine.
3. Concatenate with matching sample rate and channel layout; confirm with `ffprobe` (duration,
   streams).
4. Deliver as a native attachment in chat (`MEDIA:/abs/path`), never a `/tmp` path and never a
   description of the file.
5. The artifact is the receipt; do not narrate the pipeline after delivery.

## Pitfalls

- **"Sent" does not mean "replied"** — silence after a personal artifact is the other person's
  processing, not a status to monitor. Never propose a nudge *to the loved one*; offer the next
  artifact to the principal instead.
- **Do not re-render to fix an emotional gap** — the gap is in the script, not the encoding.
- **Do not quote the delivered script back at length** — he approved it; he knows. One clause max.
- **Do not build a metric around a person** — no tone scores, no enthusiasm indices, no family
  dashboards.

## References

- `references/store-and-assembly.md` — probe commands, directory inventory, segment → concat recipe
  with verification checks.
