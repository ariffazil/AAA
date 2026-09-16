# i-ARIF Voice Seal 2026-08-19 (authority 888) — Supersedes 2026-08-18 Voice Guidance

Source: `/root/AAA/governance/SYSTEM_HERMES_ALIGNMENT.md` (canon copy, sealed rev 2026-08-19).
Ledger: `/root/forge_work/i-arif-voice/VOICE_SEAL_LEDGER.json` (seal I-ARIF-VOICE-SEAL-2026-08-19-888).

## Current production voice: V8 (iarif-sovereign-v8)

- **voice_id**: `iarif-sovereign-v8`
- **Engine**: MiniMax speech-2.8-hd, voice_clone from `makcik-padded.wav` (file_id 432173817692448)
- **Raw F0**: median 257.9 Hz (P10 197, P90 313)
- **DSP-stabilized F0**: median 239.2 Hz (P10 179.9, P90 294.1)
- **Register**: governed FEMALE — high soprano
- **Prosody**: JIWA Siti Nurhaliza — humble genius Melayu, tenang, teratur, unhurried precision. Anti AI-speak: "X tapi Y" contradiction-tropes BANNED. Strength lives in stillness, not contradiction theatre.
- **Formants**: F1 750 Hz / F2 1100 Hz / F3 2700 Hz (post-DSP conform)
- **DSP wrapper**: `/root/forge_work/i-arif-voice/dsp_stabilizer.py` (parselmouth F0 lock)
- **F13 authorization**: 2026-08-19 16:07 MYT — Arif rejected voice_design path ("x dak soul Siti"), directed clone path

## Voice lineage (V1–V8)

| Version | Method | F0 (Hz) | Status | Notes |
|---|---|---|---|---|
| V1 | Synthetic/GIGO | — | DORMANT | |
| V2 | Meta-reading | — | DORMANT | |
| V3 | Speed test | — | DORMANT | |
| V4 | voice_clone (repointed to female) | 239.2 | RETIRED | Unverifiable provenance — repointed by parallel session without receipt |
| V5 | voice_design (designed archetype) | 170.7 | RETIRED | Arif: "x dak soul Siti" — too low, no Siti quality |
| V6 | voice_design + DSP | 205.7 → 237.3 | RETIRED | Interim, still voice_design base |
| V7 | voice_design (higher prompt) | 168.2 | RETIRED | Same problem — voice_design ignores F0 targets |
| V8 | voice_clone (makcik-padded.wav) | 257.9 → 239.2 | **ACTIVE** | Clone + DSP lock. Arif approved after hearing test |

## Key lesson: voice_design vs voice_clone for F0 targeting

MiniMax `voice_design` (MCP tool at port 18100) always produces voices around 165–175 Hz
regardless of prompt descriptions targeting higher frequencies. This is a provider limitation.

For specific F0 targets, use `voice_clone` from a source sample that naturally has the
target pitch. The clone preserves the source's pitch characteristics.

See: `references/minimax-tts-pitfalls-2026-08-19.md` for full API details and pitfalls.

## Scar reconciliation (important)

The 2026-08-19 morning scar "female voice in group/shared lanes = breach" governed
UNAUTHORIZED female-voice leakage into SADO. This seal IS the authorization: female
register is now the official i-ARIF DECODE envelope for ALL lanes including groups.
Do not apply the old scar against the sealed archetype. MakcikGPT lane
(makcik-penang-v1, ~264 Hz) remains a SEPARATE sibling lane — never crosses.

## Compute discipline (binding)

ZERO unratified GPU. V5 F5-TTS local (docker-compose staged at
`/root/forge_work/i-arif-voice/v5_sovereign/`) is FROZEN. Never trigger GPU
rental/allocation, and do not propose "GO V5" as a recommendation, unless 888
explicitly commands (F13 trigger). Optimize the SaaS/edge-tts stack with maximum
DSP precision instead.

## Seal-staleness rule

Provider-side voice_id re-points happen silently (iarif-sovereign-v4 flipped from
male to female register within 24h of the 2026-08-18 seal — that drift is what this
seal ratified). Before relying on any voice seal: probe current F0 of a fresh TTS
sample and read the ledger. A seal older than its last probe is a hypothesis, not a
fact.

## Design-vs-Clone ruling (Arif F13, 2026-08-19)

1. **DESIGN** — new voice carrying the envelope, no real person's waveform → sealable
   immediately, no authorization debt.
2. **CLONE WITH CONSENT** — letter to the person, hold everything until answered.
3. **CLONE WITHOUT CONSENT** — forbidden forever, F13 floor, not even sovereign
   instruction can waive it.

V8 uses a family sample (makcik-padded.wav) already authorized in the MiniMax account
for the MakcikGPT lane. Arif's F13 directive authorizes reuse for i-ARIF.
