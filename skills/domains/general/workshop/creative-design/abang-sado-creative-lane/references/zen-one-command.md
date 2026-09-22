# Zen pass — the lane in ONE command (2026-09-21)

The lane had six manual steps per take (pick voice from registry, pick speed, render, gate,
deliver, write receipt). The steps are identical every time; hand-typing them adds nothing but
the chance to drop one. Collapsed into `sado`.

    sado say  <textfile|->     render + gate + deliver + receipt
    sado gate <take.mp3> --text F    gate only (front-end on verify_take.py)
    sado doctor                lane health: voices, key, gate, destination

Source: `/root/scripts/sado` → `/usr/local/bin/sado`.
Destination: declared once in `/root/.config/sado.json` (`deliver_to`), never inferred.
Work dir: `/root/forge_work/sado/<out>/` — `line.txt`, `take.mp3`, `receipt.json`, 0700/0600.

## Capability parity — what must NOT be lost (all verified)

| capability | where it lives now |
|---|---|
| voice by registry precedent | `resolve_voice()` reads `lane_precedence`; a REVOKED id is refused (exit 4) |
| speed from that voice's own settings | `preferred_settings.speed[0]` |
| full verify_take.py ladder | called as a subprocess — **not reimplemented**, one writer |
| alias table (`heard=written`) | `--alias`, repeatable, passed straight through |
| tail / EOF discriminator | `tail_check()` — word timestamps vs file duration |
| declared delivery destination | `--to` or `sado.json`; refuses with no declared target |
| never ship a failed take | gate non-zero ⇒ `delivered: false` |
| per-take receipt | `receipt.json` beside the take |

Parity evidence, run 2026-09-21 (`/root/forge_work/sado/parity-20260921.py`):

| artifact | gate | tail | reading |
|---|---|---|---|
| clean BM take | PASS 90.0% | `SPENT_AUDIO_OR_CLEAN` (−0.44 s) | ships |
| MiMo garbled BM | REVIEW 18.2% | — | refused — gate still catches it |
| penang06 (had an invented outro) | FAIL, INSERTED `terima kasih kerana menonton` | `TRANSCRIBER_INVENTION` (+29.58 s) | **clean** — see below |

## The combined verdict — and why two gates are needed

`verify_take.py` alone cannot separate render-time contamination from a transcriber appending
text over silence: both appear as INSERTED words. Without a second signal, a **clean** take is
refused — a capability loss in the other direction. The wrapper therefore disproves an
INSERTED flag only on positive evidence:

    gate == FAIL  AND  INSERTED != none  AND  tail == TRANSCRIBER_INVENTION  AND  overrun > 2 s
      ⇒ deliver anyway, with `gate_fail_disproven_by: tail/EOF overrun`
    otherwise ⇒ refuse

`--strict` disables the disproof for anyone who wants the literal gate verdict.

**Rule:** additions and deletions of whole words are caught by the diff; a **fusion** and a
one-word **semantic flip** are filed as *replace* and sail through at 99%. Run the gate, then
read the transcript — closing lines first.

## Timbre vs language — measure both, every time

Same run, same reference, two properties that trade off against each other:

| lane | MFCC-cos vs source | Δf0 | BM transcript |
|---|---|---|---|
| MiMo `clone` 01–04 | 0.9966 – 0.9979 | −11 → +9 Hz | mangled (0/4) |
| edge-tts `ms-MY` Osman | 0.8934 | +54 Hz | exact |
| edge-tts `ms-MY` Yasmin | 0.9050 | +111 Hz | exact |
| MiniMax `abang-sado-live-v1` | — | ≈ source | exact |

A cosine ≈0.997 **is** the same speaker. MiMo clone carries the voice and destroys the
phonology — right voice, wrong language. A timbre check alone passes a take whose words are
gone; a transcript check alone passes a take in the wrong person's voice. **Run both**, and do
not let the possessive reaction ("that's him") stand in for the transcript gate.

## Operational notes

- `hermes send` **needs `-t telegram:<chat_id>`**. Without it the TRANSPORT LOCK hook blocks the
  command — correctly: an inferred destination already sent a brief into the bot's own chat once.
- The same hook matches the literal string `hermes send` **anywhere** in a command, so read-only
  uses (`--help`, a `grep` whose echo mentions the phrase) are blocked too. Two false positives
  observed 2026-09-21. Narrow it to "the command's executable is `hermes send`" — do not settle for
  noticing it.
- **A delivery failure log is not proof the principal received nothing.** Two sessions answer one
  DM; one route (the bot-to-bot mirror) fails loudly on every media send while the other delivers.
  Count the `Delivering 1 non-image MEDIA attachment(s)` lines, not just the errors, before telling
  a human they heard nothing.
