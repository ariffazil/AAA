# Register Contrast — Abang Sado / Syed lanes

> **Class:** AAA governance. Operational. No F5-private content.
> **Date:** 2026-09-16 · **Authority:** F13 DM directive ("Contrast all. This is reality engineering.")
> **Status:** F13_RATIFIED_CHAT (2026-09-16 "Contrast all. This is reality engineering.")
> **Companion (F5-private master index):** `/root/.hermes/lanes/private/shadow/00-REALITY-MAP-2026-09-16.md`

## Why this file exists

The federation holds four distinct registers that all answer to the name "abang sado". They have
twice been merged in prose and twice had to be unmerged by F13 ruling. Every merge produced a
subsequent correction. This file fixes the separation so the next session does not rediscover it.

## The four registers

| # | Register | What it governs | Canonical home | Access |
|---|---|---|---|---|
| 1 | **LAW** | How agents must behave around the human | `/root/VAULT999/syed/syed-care-architecture-sealed.md` (SEALED 2026-09-07) | VAULT999 |
| 2 | **PERSON** | The real human in his real roles (coach, competitor, friend) | `/root/forge_work/syedsado-physique-intel/` | operational |
| 3 | **PATTERN** | The private psychology / shadow material | `/root/.hermes/lanes/private/shadow/` | F5 · chmod 0600 |
| 4 | **MEDIA** | Synthetic voice / stills / video of an archetype | `/root/AAA/audio/voice-registry.json` + archive dirs | registry |

**Rule:** a change in one register never propagates to another. A voice id is not law. A private
pattern is not a coaching input. A coach session is not persona material.

## Contrast table — what each register is NOT

| Register | Is | Is NOT |
|---|---|---|
| LAW | behavioural constraint, 10 directives | a description of the man; not content |
| PERSON | evidence-based professional substrate | not psychological modelling; diagnose only |
| PATTERN | private synthesis, sovereign-owned | not AAA input; not session preamble; not web |
| MEDIA | synthetic artifacts | **not a likeness, not a voice, not a record of any human** |

## Live drift (this session's sweep)

| # | Drift | State |
|---|---|---|
| D1 | `ttv-voice-2026081808404926-BdoQh6ec` is declared "the locked sado/Syed voice" by `syed-persona-lock.md` (2026-08-18) but is absent from `voice-registry.json` (2026-09-14, declared source-of-truth). Probe: it still renders, f0 108.4 Hz. | UNRESOLVED |
| D2 | `syed-persona-lock.md` lives only in quarantine; the live `nusantara-voice-stack` skill has no such reference. | BROKEN POINTER |
| D3 | Config key `voice.sado_locked_voice_id` documented by the skill is absent from config. | BROKEN WIRING |
| D4 | "abang sado persona = Syed" survives in prose despite two F13 corrections (shadow-mode v2 "One≠Syed"; 2026-09-08 topology ruling). | CONTESTED |
| D5 | `malaysian-physique-circuit` referenced a quarantined substrate path in 4 places. | REPAIRED 2026-09-16 |
| D6 | The seal cites `/root/VAULT999/syed/syed-knowledge-graph.json`; the file does not exist and SANCTUARY.md forbids fabricating it. | STANDING GAP |
| D7 | **The local-seal ledger's chain is discontinuous.** Of 19 prior entries in `/root/arifOS/VAULT999/local_seals.jsonl`, 3 carry no `log_sha256` at all (the ZEN seals, entries 12–16), and one hashed entry (`FED_LITELLM_REWIRE_SEAL`, 2026-09-14) cites `previous_receipt_hash=902d74aad26e0697` — a hash that appears nowhere in the file. | PRE-EXISTING, REPORTED |
| D8 | **The kernel seal lane is broken.** `seal_to_vault999.py` imports `read_v2_seals` from `v2_epoch.py`; that symbol no longer exists. No kernel `arif_seal` can be written from this script. | BROKEN |
| D9 | **A concurrent Hermes session registered a second clone from the same brief, of the PRINCIPAL'S OWN voice.** `abang-sado-live-v1` = provider-side clone of a 46.9 s concatenation of Arif's own Telegram voice notes (`/root/forge_work/backstage/voice-src/clone_source.mp3`, file_id 442145552838935). Verified rendering, f0 98.8 Hz. No consent artefact exists for a voice stream in `/root/WELL/envelopes/_consent/`. | LIVE — needs F13 decision |

## Naming rulings issued 2026-09-16

1. **Voices are named by register, never by person.** `abang-sado-*`. A synthetic voice with zero
   human audio in its chain may not be registered under a real person's name — a registry entry is
   a provenance record, and a false name in it becomes citable evidence for every later session.
2. **The PATTERN and MEDIA registers never take the real human's name as a label.** He has not
   consented to be the referent of either.
3. **A real person's own voice is a consent-gated separate act** — his enrolment, his consent
   entry. `/root/WELL/envelopes/_consent/` holds `arif.json` only; agents do not fill that gap.
4. **"Abang" is cultural kinship, never evidence of biological family** (2026-09-08 ruling).

## Voice inventory after 2026-09-16

| Voice id | Register | Provenance | Status |
|---|---|---|---|
| `ttv-voice-2026082515384726-njTJ5yOR` | i-ARIF sovereign (assistant lane) | parametric design | LIVE |
| `i-ARIF-20260819T084602` | i-ARIF v8 | clone | REVOKED (checkpoint contaminates) |
| `ttv-voice-2026081808404926-BdoQh6ec` | sado persona (legacy lock) | parametric design | UNREGISTERED |
| `ttv-voice-2026091602501026-szbvcVGx` | abang-sado-alpha | parametric design | LIVE |
| `abangSadoRef01` | abang-sado-clone-ref01 | provider-side clone of a vendor system voice | LIVE |

## The seal issued 2026-09-16

`abangSadoRef01` / registry name `abang-sado-clone-ref01` is SEALED.

| Field | Value |
|---|---|
| Seal class | SOVEREIGN_CHAT_SEAL (not a kernel seal — D8) |
| Ledger | `/root/arifOS/VAULT999/local_seals.jsonl` |
| Chain entry | `seq` field `1` ⇒ position 20 of 20; corrected by a following AMEND entry because the ledger is append-only |
| `log_sha256` | `0ce1e9557caa287b89039f51da68f942f4fd77c4968004aa24520bbc853cc12a` |
| `previous_receipt_hash` | `34ba91bc478c7a76b44d517761756b864900e6d8003f354682dc923d422406d9` |
| Payload | `/root/forge_work/backstage/voice_test/voice_seal_payload.json` |
| Not sealed | `abang-sado-alpha` (`ttv-voice-2026091602501026-szbvcVGx`) — registered, not sealed |

The seal payload records the refusal explicitly: the artifact was requested to be registered under a
real human's name, and the **name** was refused while the work was delivered. A refusal that is
silently dropped leaves the next session to re-ask, and re-asking is how a false name eventually
lands in the registry.

## Pointer integrity

`malaysian-physique-circuit` reference files that name the restored substrate now resolve:
`pre-comp-battle-plan.md`, `person-id-workflow.md`, `syedsado-physique-substrate.md`. No edit was
needed — the path itself was restored rather than the pointers rewritten.

---

*DITEMPA BUKAN DIBERI ⚒️*
