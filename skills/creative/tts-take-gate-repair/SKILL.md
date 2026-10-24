---
name: tts-take-gate-repair
description: "Use when a voice take fails its ASR gate. Fix one clause."
version: 1.0.0
author: Hermes
license: arifOS
tags: [voice, tts, qc, gate, repair]
metadata:
  hermes:
    category: creative
    tags: [voice, tts, qc, gate, repair]
triggers:
  - a voice take comes back REVIEW or FAIL from the ASR round-trip gate
  - a take needs re-rendering after one word was flagged missing or inserted
  - a clause-split render produced a suspiciously short or partly silent take
capability_tier: fed-agent-subagent
ecology_state: HOT
---

# TTS take gate repair — surgical re-render, never a blind re-read

Owns the mechanics of getting a **gated take back to PASS without re-synthesising the whole act**.
Script structure, register and wording live in the persona lane skills; this file starts at the
moment the gate hands back a verdict and ends when the file passes.

Applies to any clause-split renderer that keeps per-clause artifacts on disk (`sado say --clause`
is the reference implementation: `cNN.txt` + `cNN.mp3` + `cNN.wav` under one workdir, joined by an
ffmpeg concat list, then gated by `abang-sado-creative-lane/scripts/verify_take.py`).

## 1. Read the verdict properly before spending a render

- `heard` is the evidence; `MISSING`/`INSERTED` are only symptoms. The flag names a word, the
  `heard` line shows which clause the transcriber actually swallowed.
- `duration` plus the chars/s figure tells you whether the take is plausibly complete: a 2,000-char
  script rendering at 20 chars/s means clauses are absent, not fast speech.
- `match` below ~95 % on a long take means whole clauses, not single words.
- A check reported `SKIPPED` is not a pass. Say which check did not run when you report the take.

## 2. Recompute the clause list before touching any file

Load `clause_split()` from the renderer (`/root/scripts/sado`) and diff the fresh list against the
`cNN.txt` files on disk.

Editing a sentence so it merges with its neighbour changes the clause COUNT, and every later index
then points at a different sentence. Patching `c27` when the list has shifted rewrites a clause that
belongs to another part of the act, and the take comes back more broken than it started.

If the index moved, fix by TEXT: rewrite the master script, re-split, and render from a clean
workdir. Surgical repair is only for the case where the list is unchanged.

## 3. Re-render the single clause

The voice argument here is the registry's `provider_voice_id`, not the registry key. For a blended or
cloned voice these are different handles — only `/root/AAA/audio/voice-registry.json` maps one to the
other, and passing the key produces either a wrong identity or a hard failure.

```
mmx speech synthesize --base-url https://api.minimax.io --model speech-2.8-hd \
  --voice <provider_voice_id> --speed <same as the act> \
  --text-file cNN.txt --out cNN.mp3 --quiet
ffmpeg -y -loglevel error -i cNN.mp3 -ar 44100 -ac 1 cNN.wav
```

Speed must match the act's speed, or one clause sits at a different register from its neighbours.

## 4. Rebuild and re-gate

Regenerate the concat manifest with the current total clause count, insert the 0.38 s silence
between parts, re-apply `loudnorm=I=-18:TP=-2:LRA=11`, then page the gate against the **edited master
text** (not the clause file). Use the gate's `--alias heard=written` when a spelling differs from what
the transcriber will hear.

## Pitfalls

- **Never re-render into a workdir that already holds clause files.** A second run into the same
  `--out` directory mixes fresh clauses with stale ones from the previous text; the join is seamless
  and the duration is plausible, so the only symptom is a take missing whole paragraphs (observed at
  70 % word match with the final third absent). `rm -rf` the out dir before every render of the same
  text — cheaper than diagnosing the result.
- **`render_ok: true` does not mean every clause rendered.** A long clause run can finish having
  synthesised only a prefix (32 of 59 in one case) and still assemble a take. Compare
  `receipt.clause_split.clauses` against `len(clause_split(text))`; a mismatch means truncated, so
  delete the workdir and render again rather than repairing clause by clause.
- **A reduplicated or repeated construction swallows one copy.** `panjang-panjang`, `betul-betul`,
  and a word repeated across a full stop get elided at the seam and reported MISSING. Rewrite the
  clause (`minta maaf panjang`) instead of re-rolling identical text — same text reproduces the same
  swallow.
- **Transcriber tail artifacts are not contamination.** Extra words whose timestamps sit past the end
  of the audio (`last_word` beyond file duration) were invented over silence; the take is clean.
- **The workdir is the artifact.** Keep clause files until the take is delivered and the receipt is
  written; a repaired take cannot be re-cut or explained without them.

## Reporting the repair

One line: voice id, speed, duration, gate verdict. Do not narrate the rounds — the requester cares
that the take passed, not how many cycles it took.
