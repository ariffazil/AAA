# Voice-clone audio in chat — receipt, conversion, and the F9 fail-closed gate

When a `.ogg` (Opus 24 kHz mono from MiniMax TTS) or any audio file lands in the
chat, the human may ask for it back: *"bagi file sound ni"*, *"MP4 or wave aku nak
download"*, *"hantar balik"*. That ask looks like a trivial file-handling request,
but the audio's identity is the load-bearing question — the format conversion is
not.

## Receipt — always, before any conversion

A voice-clone audio in the chat is one of three things:

1. **The human's own voice** (cloned from their notes) — the audio IS them
   speaking back. No F9 problem; this is their identity. Convert freely.
2. **A consented speaker** (kawan, keluarga) — the human has standing
   permission to receive, replay, and reformat. Convert freely.
3. **A voice clone of someone else** (public figure, third party, an
   unnamed source) — this is F9 territory. The audio is a borrowed voice print,
   and *"bagi balik"* is asking the agent to pass a borrowed voice print
   out of the chat boundary. Do NOT convert + ship on the strength of the
   ask alone.

The audio file itself does not tell you which case you are in. There is no
metadata tag, no `artist=` field, no header. A 4-minute Opus 24 kHz mono file
is the format for both an i-ARIF sovereign clone and a public-figure clone —
same wire shape, opposite provenance.

**The rule that survives the unknown:** ask the human before converting.
The ask is two questions, one cluster:

- **Whose voice?** — (a) yours, (b) consented other, (c) voice clone / TTS,
  (d) original audio from a source.
- **For what, after download?** — (x) dengar sendiri, (y) hantar ke
  seseorang tertentu, (z) publish / share awam.

(a)/(b) convert freely. (c)/(d) require the human to know — and the agent
to know — what is moving where, because (c)+(z) and (d)+(y or z) are
the F9 fail-closed zone.

## The "bagi balik" pattern

When the human says *"bagi file sound ni"* or *"Bagi ja la file"*, the reflex
is to re-attach the same file (`MEDIA:/path/to/...ogg`). That is correct for
(a) and (b). It is also correct for (c) when the receipt is the file as it
already exists in the cache — the human sent it in, the agent sends the
same file back, the boundary is not crossed.

The defect class is **auto-converting without asking**. Opus 24 kHz → MP4
audio or WAV is one ffmpeg call. Doing it without the receipt is the
agent manufacturing the action the human might not have asked for. The
human asked for the file. The format was a follow-up ask. The agent
collapsed two asks into one.

The shape that survives:

- *First ask is "bagi file"* — re-attach as-is, then ask about format if
  conversion is implied.
- *First ask is "convert to MP4/wav"* — that is conversion territory,
  ask the receipt first.
- *First ask is "hantar kat <person>"* — that is out-of-chat delivery,
  ask the receipt first.
- *First ask is "publish"* — F9 fail-closed; do not convert, do not pass.

## Reference — the audit table the agent must run

| Ask shape | Receipt status | Action |
|---|---|---|
| "bagi file" | unknown, file in chat | re-attach as-is |
| "bagi MP4/wav" | unknown, file in chat | ask (a/b/c/d) before convert |
| "hantar kat X" | unknown, file in chat | ask (a/b/c/d) + (x/y/z) before action |
| "publish kat site" | unknown | refuse until (a/b) confirmed |
| File in cache, no ask | any | do not auto-act |

## Why this rule is not in the lane craft

The lane craft skills (e.g. `abang-sado-creative-lane`, `nusantara-voice-stack`)
govern how to render a take. They do not govern the receipt of a take that
arrived without a request — the file-in-chat case. That is a human-interface
boundary, and it lives here. The persona-boundary-conduct skill governs the
moment a synthetic voice is given to a person; this reference governs the
moment a synthetic voice is asked to leave the chat with a person.

## Anchor in F9 / fail-closed

The voice-print-as-identity rule lives canonically in
`/root/AAA/instructions/anti-hantu-behavior-canonical.md` (F9) and is
operationalised for voice in `AAA-voice-cloning-mimo-minimax` §F9 ANTI-HANTU.
The three-tier ladder (creating / modifying / using) is for the engine
side. The receipt side — *"whose voice is in this file, and where is it
going"* — is the human-side of the same invariant.
