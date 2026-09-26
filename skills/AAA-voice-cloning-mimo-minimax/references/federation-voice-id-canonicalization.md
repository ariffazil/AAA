---
name: federation-voice-id-canonicalization
description: "Pattern for one voice_id serving multiple hosts without drift. KVM4 owns canonical, other hosts reference (not mint)."
---

# Federation Voice ID Canonicalization

## The Pattern

When a TTS voice_id serves the federation (multiple KVMs answering "voice X" to one human), one host owns the canonical card + sample, and the others reference it.

**Anti-pattern:** each host mints its own voice_id for the same trigger alias. Result: drift, double sample storage, divergent tuning.

## State Files (one per voice_id)

| Path | Owner | Role |
|---|---|---|
| `/root/.openclaw/workspace/voice/<ALIAS>/<ALIAS>-VOICE-CARD.json` | KVM4 | Canonical card (source provenance, F0 measurements, STT scores) |
| `/root/.openclaw/workspace/voice/<ALIAS>/source_*.mp3` | KVM4 | Source audio (immutable, sha256 verified) |
| `/root/.openclaw/workspace/scripts/voice_alias.sh` | KVM4 | Canonical resolver |
| `/root/.hermes/voice/<ALIAS>-VOICE-CANONICAL.json` | KVM8 | Mirror state (read-only, references canonical owner) |
| `/root/VAULT999/identity/<SEAL>.json` | KVM8 | F1 immutable seal record |
| `/root/.openclaw/workspace/voice/<ALIAS>/<ALIAS>-VOICE-CANONICAL-FEDERATION.json` | KVM4 | Mirror copy of the KVM8 federation record |

## Naming Convention

`SS<Subject><YYYYMMDD>v<N>` — capital letters identify it as a sealed alias, not a casual ID.

Example: `SSSiti20260926v1` = SS-alias for Siti Nurhaliza, sealed 2026-09-26, version 1.

Never reuse a name. `voice_clone` will happily overwrite — never reuse a name across hosts.

## Adding a New Voice Alias (Recipe)

1. Pick the alias (e.g. "AR", "AM") and define trigger phrases.
2. Mint the voice_id on KVM4 with the correct prefix and date stamp.
3. Write the canonical card at `/root/.openclaw/workspace/voice/<ALIAS>/<ALIAS>-VOICE-CARD.json`.
4. Update `/root/.openclaw/workspace/scripts/voice_alias.sh` to handle the new alias (add to the case statement).
5. Mirror state: copy `<ALIAS>-VOICE-CARD.json` content into `<ALIAS>-VOICE-CANONICAL.json` at KVM8.
6. Write VAULT999 seal record at `/root/VAULT999/identity/<ALIAS>-VOICE-CANONICAL-FEDERATION.json`.
7. Patch SOUL.md §Voice Signal Routing with the new trigger.
8. Test render from KVM8 (idempotency check — same voice_id, same API key, same audio).
9. Don't broadcast to other KVMs unless they have an explicit TTS use case; orphan registrations are anti-pattern.

## Pitfall — Orphan Registration

A voice_id registered on KVM4 but never rendered by any host = waste. Don't mint speculative IDs "in case we need them later."

## Pitfall — Skill Duplication

When voice_id setup got bootstrapped across multiple agents, we created `voice-ss` skill on KVM8 alongside the canonical `hermes-voice-config` on KVM4 — same job, two homes, drift risk. Resolution: removed the KVM8 skill, pointed SOUL.md routing direct to the canonical resolver + voice_id. One alias, one resolver, two call sites.

## Sealed Examples (verified)

- `SSSiti20260926v1` — Siti Nurhaliza, source *Apa Cerita?* Ep.26 window 8499.7s-8529.7s (30 s), sha256 `8a3aa4f8…`, F0 source 197.1 Hz → clone 216.3 Hz, STT 99.0%.