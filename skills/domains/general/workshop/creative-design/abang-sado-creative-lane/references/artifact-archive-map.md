# Abang-sado artifact archive map

Where the persona artifacts live, and how to answer "mana set lama tu / ada apa dalam dia" without a
fresh full-disk sweep. Read this instead of `find /` when he asks about an existing set.

## Live surfaces

| Path | Holds |
|---|---|
| `/root/forge_work/backstage/` | Current working dir: rendered stills, voice takes, `line_*.txt`, `VOICE-MINT-RECEIPT.md`, `alpha10.json` batch manifests |
| `/root/forge_work/<concept>-<date>/` | One dir per accepted concept (private, `chmod 700`) |
| `/root/AAA/corpus/abang-sado/` | Reference corpus for the register |
| `/root/AAA/artifacts/sado-logo/` | Logo / brand marks for the SADO miniapp lane |
| `/root/AAA/telegram-miniapp/bots/sado/` | Miniapp deploy surface |
| `/var/www/html/syedos/sado-reference/` | Served reference surface |

## Archived persona packs (quarantine)

Seven packs, moved (not deleted) under
`/root/.quarantine/zen-20260912/_quarantine/2026-08-25-sado-*/`. Each is readable in place.

Shape of every pack: 3–4 stills, 2–3 clips each shipped as a `-raw` and a `-bass` variant, one persona
line as `voice-*.mp3` plus an `.ogg`, and a shared `bass-chest-cavity.mp3` bed reused across packs.

| Pack | Carries |
|---|---|
| `sado-syed-persona` | 4 stills (hero, chest close, 3/4 portrait), 6 clips, `voice-syed-sado.mp3` |
| `sado-syed-cocky` | 3 flex / biceps / low-lens stills, 6 clips, `voice-cocky.mp3` |
| `sado-not-mine` | 3 crowd / walk-out / one-fan stills, 4 clips, `voice-not-mine.mp3` |
| `sado-dream-fictional` | 3 stills, 4 clips, `voice-dream.mp3` |
| `sado-behind-stage` | 3 wings / stage / curtain stills, 4 clips, `voice-wings.mp3` |
| `sado-chest-pack` | 3 chest stills, 6 clips, `voice-sado-dada.mp3` + `voice-osman-dada.mp3` |
| `sado-final` | `MALAM-NI-DIA-BUKAN-KAU.mp4` (8.8 MB), 3 segments + `concat.txt`, `voice-final.mp3`, **and the two receipt files** |

Re-locate a set that is not in the live dir with:

```bash
find /root/.quarantine -maxdepth 4 -type d -name "*sado*"
```

## Reading why a set was held — read the RECEIPT, not the imagery

A pack that was judged carries its own receipts beside the media. Read them before characterising
anything:

- `apex-judge.json` — `effective_verdict` (`HOLD` / `SEAL`), `independence_class` (doer ≠ judge actor),
  `reasons`, `forbidden[]`, `call_hash`, `receipt_path`. This is the kernel's own record.
- `session-close-evidence.json` — a `holds: []` array stating the reason in one sentence, plus
  artifact `sha256` values and the Telegram delivery id.

Two consequences for how you answer:

1. **The hold reason is about the FRAMING or the NAMING, not necessarily the faces.** The `sado-final`
   receipt records a hold on a named-person worship framing while a face-match run in the same session
   reported the rendered face did **not** match the reference. State what the receipt says; do not infer
   a likeness from the pack title, and do not infer that the pack is "clean" either — the faces and the
   naming are different findings and the receipt is the one that was judged.
2. **Quarantine is move-not-delete.** Nothing in it is lost or broken, and nothing in it is live. Say
   which of the two it is, and offer to open any specific file rather than summarising the whole set
   from its filenames.

## Persona lines inside archived packs

The `voice-*.mp3` files are short persona lines (5–20 s). Transcribe on read with the same Groq
round-trip used by the QC gate (`-F model=whisper-large-v3-turbo -F language=ms`) rather than quoting
from memory or from the filename — these are rendered lines, and the transcript is the only evidence of
what was actually said.
