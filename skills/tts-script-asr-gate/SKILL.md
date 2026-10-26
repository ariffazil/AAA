---
name: tts-script-asr-gate
description: "Use when a TTS script must pass an ASR round-trip gate."
version: 1.0.0
tags: [tts, asr, verification, gate, voice, malay]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# TTS scripts that pass an ASR round-trip gate

Many voice lanes render speech, transcribe it back and diff against the script (`verify_take.py` and the `sado` runner are the reference implementation). The gate is a hallucination check — it proves the audio says what the script said. It is NOT a quality score, and most REVIEW verdicts are the gate's own limitation, not a bad render.

## Write the script for the gate, not for the eye

Before the first render, strip everything an ASR round-trip cannot reproduce:

| Trigger | Why it fails | Write instead |
|---|---|---|
| `100%`, `RM2,600`, `4 bulan` | ASR spells digits out; the token becomes `seratus peratus` / `dua ribu enam ratus` and diffs as MISSING | Spell it: `sepenuhnya`, `dua ribu enam ratus ringgit`, `empat bulan` |
| Laughter, `hahaha`, onomatopoeia | Not lexical — ASR drops it or invents a word | Cut it; convey tone through phrasing |
| Acronyms, brand names, `DBKL`, `SC4` | Renamed or expanded one letter off | Say it in full once if it must be in the audio, or keep it out |
| English loanwords inside BM | Transcribed phonetically (`ekon` for aircond, `teknisien` for technician) | Accept as an alias, or use the BM word |

Length sanity: most lanes run ~10–13 chars/s, so a 1,200-char script is ~100 s. State the duration when you deliver so the recipient knows what they are getting.

## When the gate says REVIEW — re-judge, do not re-render

The ASR error is *systematic*, not random. Re-rendering the same script reproduces the same MISSING list and burns a render cycle. Re-judge the artefact you already have with explicit heard→written aliases:

```
sado gate <path>/take.mp3 --text script.txt \
  --alias "ekon=aircond" --alias "teknisien=technician" --alias "hari bulan=haribulan"
```

- Read the `heard:` line the gate prints — it contains the exact transcription to alias against.
- Both directions of a digit/word swap may be needed: `--alias "peratus=100%"` and `--alias "100=100%"`.
- Every alias must be a genuine transcription artefact, never a way to paper over a real omission. If `heard:` shows a whole clause dropped, the take is genuinely bad — re-render.

**Rule:** numerals are the most common false REVIEW. If `MISSING` contains only digits or a spelled-out number, it is a gate artefact — rewrite that sentence to avoid the numeral, or alias it.

## Judge the verdict line, not a character diff

A ~87–95% match with `INSERTED: none` / `MISSING: none` is a passable take; the percentage is dragged down by normalisation, not by lost content. Conversely a high percentage with a non-empty MISSING list is a real problem. Read `verdict:` and the MISSING/INSERTED fields.

A `PASS` on the gate is the only licence to deliver. `REVIEW` means do not send — re-judge with aliases, then re-render if it still fails.

## Delivery after a passing gate

The take lives in a 0700 workdir; copy it to a readable path before attaching. Deliver with `[[audio_as_voice]]` on its own line plus a `MEDIA:/abs/path.mp3` line, and give the duration. If transport fails but the gate passed, keep the take and hand-deliver — do not re-render, a transport miss is not a render failure.

## Pitfalls

- A passing gate licenses nothing about the *content*. The gate checks fidelity, not judgement — the script still has to be the finished answer.
- Re-rendering to chase a higher match percentage is wasted work; the score is not the pass condition.
- If the user forwards a delivered voice note back to you, hash it before treating it as new speech from the human. It will match the take you just rendered (or near-match after transport re-encode) — transcribing it as the human's own words invents an input that does not exist.
