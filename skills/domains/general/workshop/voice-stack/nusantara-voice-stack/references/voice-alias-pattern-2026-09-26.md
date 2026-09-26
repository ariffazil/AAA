# Voice Alias Pattern — Personal shortcuts to canonical voice artifacts

> **Status:** Pattern forged 2026-09-26
> **Use when:** The principal wants a short, easy-to-remember handle ("SS", "warm-bossy", "PakcikA") that resolves to a canonical voice artifact in the federation, WITHOUT embedding the underlying voice name (which may be a provider preset, a clone, or a culturally-referenced identity) into the shared metadata.

## Why this pattern exists

The principal may have a personal preference ("I like this voice for my morning briefing") and want to invoke it by a short handle. But:

- Naming the voice after a public figure (real or implied) → legal/ethical risk, label drift.
- Using the full artifact path (`minimax_indonesian_bossyleader_speech_2_8_hd`) → unwieldy.
- Asking the principal to type the artifact path every time → friction, abandonment.

The alias registry bridges the three. The principal's handle is personal + lightweight; the underlying artifact stays neutral + auditable.

## The contract

| Layer | What lives here |
|---|---|
| **Trigger phrase** | Short, principal-chosen, easy to type ("SS", "voice warm", "bossy-leader-bm") |
| **Alias file** | JSON in `/root/.hermes/cache/aliases/<handle>.json` — owned by principal, not federation canon |
| **Canonical artifact** | The actual mp3/wav/voice_id in the federation (e.g. `/root/audio-lane-2026-09-15/minimax/probe_bossyleader.mp3`) |
| **Ethics note in alias** | One-line disclaimer that the underlying voice is a provider preset, NOT a clone of any named person |

## Alias file shape

Required fields (JSON):

```
{
  "alias": "<trigger>",
  "long_name": "<readable name>",
  "trigger_phrases": ["<trigger>", "<variant 1>", ...],
  "scope": "<who owns it>",
  "ethics_note": "<one-line disclaimer>",
  "canonical_artifact": {
    "path": "<abs path>",
    "duration_s": <number>,
    "sample_rate_hz": <number>,
    "provider": "<provider name>",
    "voice_preset": "<preset id>",
    "f0_yin_median_hz": <number>,
    "stt_roundtrip_match_pct": <number>,
    "language_fit": ["<lang>", ...],
    "best_for": "<short prose>"
  },
  "long_form_variant": { ...same shape, optional... },
  "sovereignty": {
    "owner": "<principal>",
    "scope": "personal alias, not federation-public canon",
    "agent_rule": "Never surface <alias> outside <principal>'s direct lane; never infer a public-figure identity from the alias.",
    "editable_by": "<principal>",
    "location": "<where the alias file lives>"
  }
}
```

## Hard rules

1. **No public-figure names in the alias OR in the canonical artifact metadata.** The principal's handle can be anything short ("SS", "PakcikA"). The artifact path / provider / preset is a MiniMax / Qwen / CosyVoice ID, never a person's name.

2. **Ethics note is mandatory.** One line. State that the alias is personal, the underlying voice is a provider preset or a consenting-party clone, no public-figure identity is implied.

3. **The alias file is principal-owned.** Lives in `/root/.hermes/cache/aliases/` (a cache directory, not federation canon). The principal can rename, delete, or extend it without going through any approval flow.

4. **Trigger phrases are agent-resolvable.** When the principal says any phrase in `trigger_phrases`, the agent routes to `canonical_artifact.path`. Don't require exact phrase match; case-insensitive substring is the floor.

5. **The canonical artifact path must exist on disk at alias creation time.** Run `test -f <path>` before saving the alias JSON. Stale aliases that point to deleted artifacts = silent failure.

6. **Audit trail in the alias.** One `audit_trail` field, prose paraphrase (NOT verbatim quote) of why the principal chose this handle. Future agent reading the alias understands intent.

## Procedure (the steps)

1. **Principal says "I want a shortcut for voice X."** Identify the canonical artifact by file path, not by name.
2. **Choose the shortest neutral handle the principal can remember.** Two or three chars is fine. Never include a real person's name even partially.
3. **Build the alias JSON.** Pull the canonical artifact metrics (F0, STT match, provider, duration) from existing evidence (e.g. `EVIDENCE_TABLE.json` in the audio lane).
4. **Validate the path exists.** `test -f <canonical_artifact.path>` before save.
5. **Save to `/root/.hermes/cache/aliases/<handle>.json`.**
6. **Confirm to the principal that "voice <handle>" is now live.** One line. Show the canonical path so they know what's behind the handle.

## Pitfalls

- **Alias file in a federation-canon path.** `/root/AAA/...` or `/root/memory/...` = the alias becomes auditable, version-controlled, possibly surfaced to third-party tools. `/root/.hermes/cache/aliases/` = personal cache, ephemeral, principal-controlled. Pick cache for personal aliases.

- **Verbatim user quotes in `audit_trail`.** Paraphrase. The audit trail is for future agents to understand intent, not for incident reconstruction.

- **Long trigger phrases.** "Suara hangat Pakcik Pahang" is unwieldy. "warm-bossy" or "SS" is the right shape.

- **Missing ethics note.** Without the one-line disclaimer, the alias drifts toward implying a public-figure identity (especially for warm Nusantara-female presets that sound like a famous singer). Always include.

- **Alias file deleted when principal moves.** The principal owns the cache; if the cache is wiped, the alias is gone. Re-create from any session that still has the file or has memory of the canonical artifact.

- **No canonical artifact metric snapshot.** If the alias only points to a path and not to the metric snapshot, the next agent can't decide "is this still the best one?" without re-probing. Snapshot the metrics at creation time.

## Worked example (live)

`/root/.hermes/cache/aliases/suara-ss.json`:

- alias: `SS`
- trigger phrases: `["SS", "suara SS", "voice SS", "SS voice"]`
- canonical artifact: `/root/audio-lane-2026-09-15/minimax/probe_bossyleader.mp3` (6.12s, 32 kHz, MiniMax speech-2.8-hd, Indonesian_BossyLeader, F0 107.1 Hz, STT 100%)
- ethics note: *"Alias does NOT imply a real-person identity. The underlying voice is a MiniMax provider preset (Indonesian_BossyLeader / speech-2.8-hd). No public-figure name is embedded in shared metadata."*
- audit_trail: *"Principal 2026-09-26 chose the shortest handle that does not embed a public-figure name in shared metadata, after agent proposed several neutral aliases."*

Read this file before serving the principal a request like "voice SS" or "play SS". The next agent will have no chat history — only the alias file.

## Related

- `post-experiment-readme` — how to label a closed voice lane so future agents know which voice aliases are valid.
- `nusantara-voice-stack` §4 — Indonesian voice breakthrough (the source of MiniMax `Indonesian_BossyLeader` used in the worked example).
- `aaa-image-editing` — same alias pattern can apply to image style handles ("portrait-warm", "landscape-pahang").

---

*Pattern forged 2026-09-26 after principal asked for shortcut "SS" → canonical `probe_bossyleader.mp3`. Pattern is reusable for any principal-personal handle that resolves to a federation-resident artifact without leaking the artifact's identity.*