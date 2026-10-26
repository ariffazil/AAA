---
name: tts-render-failure-modes
description: "Use when a TTS render comes out short, wrong or silent."
version: 1.0.0
author: Hermes Agent
license: arifOS
tags: [voice, tts, render, diagnostics, fail-closed]
metadata:
  hermes:
    tags: [voice, tts, render, diagnostics, fail-closed]
    related_skills: [generated-audio-provenance, voice-clone-operations, voice-lane]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# TTS render failure modes

Companion to `generated-audio-provenance` (what the finished file declares). This skill is about the
render *lane*: the failures that produce a wrong artefact rather than no artefact.

## The one that matters most: a silently short take

Long scripts are rendered one clause per call — better breath and pitch range than a single flat
take, which rides one pitch contour and drops the pauses between sentences. That loop must be
**fail closed**:

```python
for i, cl in enumerate(clauses, 1):
    ok = False
    for attempt in range(1, 4):
        subprocess.run(one_render(cp, mp).args, capture_output=True, timeout=600, env=env)
        if os.path.exists(mp):
            ok = True; break
        time.sleep(2 * attempt)
    if not ok:
        manifest['error'] = f'clause {i}/{len(clauses)} failed after 3 attempts'
        manifest['partial_clauses'] = len(parts)
        write_receipt(manifest); sys.exit(3)   # never concatenate the remainder
    parts.append(convert_to_wav(mp))
```

`if not os.path.exists(mp): continue` is the defect. A wallet stall or quota stop then removes whole
sentences: the text file is complete, the audio is not, and the ASR gate only downgrades to REVIEW
because every word it *does* hear matches the script. Retry a clause, then abort. A truncated take
must never be built, let alone delivered.

**Completeness check independent of the ASR:** the gate prints
`duration : <T>s (<N> chars/s of <M> input chars)`. `M` must equal the character count of the script
file. If the implied input length is shorter than the file, clauses were dropped — the take is
truncated even when the verdict says REVIEW rather than FAIL.

## "insufficient credit" / a transport error is a config question first

Symptom: the lane reports empty credit (or a bare HTTP error) while a funded key sits in the
environment.

Mechanism: the CLI loads its own config file (one MiniMax CLI uses `~/.mmx/config.json`). An older,
spent key in that file shadows a working `*_API_KEY` in the environment. Nothing is broken — two
credentials are in play and the message names only one.

Diagnose by comparing hashes, never by printing values:

```python
import json, os, hashlib
cfg = json.load(open(os.path.expanduser('~/.mmx/config.json')))
h = lambda k: hashlib.sha256(k.encode()).hexdigest()[:12] if k else None
print(h(cfg.get('api_key','')), h(os.environ.get('MINIMAX_API_KEY','')))
```

Different hashes = the trap. Fix: back up the config with a timestamp, write the funded key in,
re-probe **one short line**, then resume the batch.

A wrong endpoint base is a *separate* cause that also presents as a transport error. Check base URL
and key as two probes — one failing probe cannot tell you which cause fired.

## Long renders are a background job

40+ clauses of sequential synthesis runs into many minutes. Run the render detached and poll the
work directory's `receipt.json` for `verdict`, rather than holding a foreground call open and risking
a timeout that leaves you unsure whether it finished. Every render should write a receipt with
voice id, settings, clause count, gate verdict and error field, so the poll has something to read.

## f0 cannot settle identity

A highpass filter — a common 70 Hz cleanup on a low male register — removes the fundamental. A naive
autocorrelation estimator then locks onto the 2nd harmonic and reports roughly double the true
pitch. The same voice reads as two different speakers depending on the chain.

- Use f0 to compare *register* between recordings processed the same way. Never to answer "whose
  voice is this".
- For identity use the dated mint receipt: provider `file_id`, source path and duration, processing
  chain, and the registry's `provenance`. Those are dated artefacts; f0 is a snapshot of one take.
- When a claim already made rests on a measurement that later proves unmeasurable, retract it in
  those words — "the registry says X" is not the same sentence as "I measured X".

## Register is not persuasion

A clone built from an angry sample renders neutral text high; a clone built from quiet material
renders angry text low. Match the register to the moment the text describes, not to the emotion the
listener wants to hear. A calm line read in a shout register reads as parody, and the failure gets
attributed to the voice rather than to the routing decision.

## Gate-fix loop (ASR misses one word, not the take)

A single-word `MISSING: ['x']` usually means the TTS slurred or dropped one token — often a
numeral word (`dua-dua`, `sepuluh`), a stutter construction, or a sentence split right before a
numeral. The fix is a text patch and one re-render, not a re-record of anything:

1. Read the `MISSING` list. Rewrite ONLY those tokens in the script: swap numerals for non-numeral
   phrasing (`dua-dua` -> `kedua`/`berdua`/`serentak`), remove stutters and ellipses, and join any
   sentence that ends right before a numeral into its next clause — a clause-final numeral renders
   weak and gets dropped.
2. Re-render the whole script. One patch + one re-render normally clears it; two failed rounds
   means the token itself is unpronounceable in this voice — rewrite the sentence, don't retry.
3. `INSERTED: ['x']` fires the same loop in reverse: the take invented a syllable, usually at a
   short-pause boundary. Join the sentences around it (comma instead of full stop) and re-render.

Never deliver on REVIEW. The gate refusing is the gate working; patching the text is cheaper than
arguing with the checker.

## Verdict discipline

- PASS with `gate_exit: 0` is the only pass; REVIEW and FAIL mean do not deliver.
- A gate that skips a check is not a pass — read the `note:` lines (an absent DSP family check is
  `not measured`, never `passed`).
- Say the duration in the delivery line. It is the one number the human can check without tools.
