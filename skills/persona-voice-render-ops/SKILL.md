---
name: persona-voice-render-ops
description: "Use when rendering a persona voice note via sado."
version: 1.0.0
tags: [voice, tts, sado, telegram, minimax]
---

# Persona voice render — runner, registry, delivery

Supersedes the operational contract in `persona-voice-note-render` (which is read-only and still names revoked voice ids).

## Canonical runner

`/root/scripts/sado` collapses render → `verify_take` gate → deliver → receipt into one call:

```
python3 /root/scripts/sado say <script.txt> --voice <canonical-id> [--to telegram:<chat_id>] [--caption "..."]
```

Invoke with `python3`, never `bash` — it is a Python file and bash dies on `syntax error near unexpected token` before rendering. `verdict: PASS` with `gate_exit: 0` is the only pass; `REVIEW`/`FAIL` means do not deliver. Exit codes: 0 ok, 1 gate REVIEW, 2 gate FAIL, 3 render/transport, 4 usage.

Write the script to a scratch file first: prose only, no markdown, no internal vocabulary. Render at ~11–13 chars/s, so a 1,100-char script lands ~100s — say the length in the delivery line.

## Voice resolution

Read `/root/AAA/audio/voice-registry.json`. Only `voices{}` entries with `status: LIVE` are renderable; `REVOKED` aborts by design. Sado does NOT resolve the file's `aliases{}` block — `--voice pmx` fails with `voice 'pmx' not in registry` — so pass canonical ids: `pmx-live-v1`, `abang-sado-live-v1`, `siti`, `abang-sado-edge-deep`, `pegawai-rasmi-baku`. Take the provider voice id from the registry entry, never from memory: old ids go stale and some (including the principal's own former voice) are revoked outright and must be re-minted before use.

## Delivery

- Default target comes from `/root/.config/sado.json` (`deliver_to` = the principal's DM). A render requested inside a group WITHOUT `--to` lands silently in his private DM — pass the group id explicitly, or deliver by hand. Cross-room leakage is the failure, not the extra step.
- `--to` rides on `hermes send -t telegram:<id>`. A group id can fail to resolve (`Could not resolve 'telegram:-100…'`) while the render itself passed — the receipt then reads `PASS_UNDELIVERED`. Keep the rendered `take.mp3` and deliver it with a `MEDIA:/abs/path.mp3` line plus `[[audio_as_voice]]` on its own line; a transport miss is not a render failure, so do not re-render.

## Pitfalls

- The `verify_take` ASR gate renames acronyms and strips punctuation — a brand name can come back one letter off and still pass at ~95% match with no INSERTED/MISSING. Judge the verdict line, not a character diff.
- Laughter, onomatopoeia and numerals are the usual REVIEW triggers, because ASR cannot round-trip them. Keep spoken scripts free of them.
- REVIEW fix order: edit the SCRIPT, never re-render blind. ASR either INSERTS a phantom interjection (stutters like "bada..." become phantom words) or DROPS a real word — and the dropped word is almost always a reduplicated one (`dua-dua`, `bulan-bulan`) or a short function word the render swallowed. Replace reduplications with non-reduplicated forms (`berdua`, `kedua`, `serentak`) and delete written stutters entirely, then re-render once. Looping on the same script wastes takes.
- REVIEW verdicts report exactly one MISSING token at a time — fix the visible one AND scan the script for siblings of the same pattern before re-rendering, or you pay one take per occurrence.
- Register selection is content-driven: `abang-sado-mad-v1` keeps its high pitched edge even on calm text — never use it for calm/tender content; use the blend voice there. Match voice register to the CONTENT's emotion, not to the persona's reputation.
- Long multi-act scripts (3-act, ~10 min total) render as separate takes per act — deliver as numbered act files, not one concat; the gate runs per take and a single mega-script multiplies gate-failure risk.
- The voice carries the message; it does not license softening. If the ask needs analysis, the script is the finished analysis.
- Copy the take to a 644 scratch path before sending; the workdir is 0700 and the transport may not read it.
