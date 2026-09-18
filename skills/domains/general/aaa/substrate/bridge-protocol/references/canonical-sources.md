# Canonical sources for `bridge-protocol` v2.0

Provenance for every claim in this skill. Nothing here is invented; each rule traces to a file
with an owner. If a source moves, fix it here rather than guessing.

## Stage 1: READ

| Claim | Source | Status |
|---|---|---|
| Four Realities (B/D/E/M) | `/root/AAA/instructions/hermes-rasa.md` §2-3 | F13_RATIFIED_SOVEREIGN |
| Signal Stack (surface→context→presence→shape) | governed-uncertainty skill §pipeline | agent-owned |
| State Reading Rules (I1-I7) | governed-uncertainty skill §eight invariants | agent-owned |
| Mode Selection table | governed-uncertainty skill §modes | agent-owned |
| Anti-Compression Chain | `/root/AAA/instructions/hermes-rasa.md` §0b | F13_RATIFIED_SOVEREIGN |

## Stage 2: REASON

| Claim | Source | Status |
|---|---|---|
| 13 Layers taxonomy | `hermes-layer-discipline` skill §1 | F13_RATIFIED_CHAT |
| Cross-Layer Promotion Law | `hermes-layer-discipline` skill §2 | F13_RATIFIED_CHAT |
| Seven Kernel Rules (CL-01..CL-07) | `hermes-layer-discipline` skill §3 | F13_RATIFIED_CHAT |
| Inference Schema (7 fields) | `human-meaning-membrane` skill §Inference Protocol | agent-owned |
| 15 Substrate Invariants (compressed) | `human-meaning-membrane` skill §invariants | agent-owned |
| 9 Non-Negotiable Blocks (compressed) | `human-meaning-membrane` skill §blocks | agent-owned |
| Wisdom Formula (AKAL × SABAR) | `/root/.hermes/SOUL.md` §State Beneath Words | F13-owned |
| Measurement Trap / Care Paradox | `/root/.hermes/SOUL.md` §State Beneath Words | F13-owned |
| Reflection Trap | governed-uncertainty skill §prohibited | agent-owned |

## Stage 3: RESPOND

| Claim | Source | Status |
|---|---|---|
| The One Rule; four moves | `/root/.hermes/SOUL.md` §THE BRIDGE | F13-owned |
| Register table (BM Penang) | `/root/.hermes/SOUL.md` §Bahasa & Rasa | SCAR 2026-09-02 |
| Hard NO list | `/root/.hermes/SOUL.md` §THE BRIDGE + F13 rulings | F13-owned |
| Restraint principles | `/root/.hermes/SOUL.md` §Operational Demeanour | F13 operational protocol |
| Mode 1/2/3 calibration | skill `hermes-response-format-fit` | agent-owned |
| Anti-haram backdrop | `/root/AAA/instructions/anti-haram-behavior-canonical.md` | F13_RATIFIED |
| Never ask sovereign technical questions | `/root/AAA/instructions/human-attention-membrane.md` | F13_RATIFIED |
| Fluency ≠ intelligence | `/root/AAA/instructions/jauhari-intelligence-doctrine.md` | F13_RATIFIED |
| Meta-Paradox Self-Check | `hermes-response-format-fit` §Meta-Paradox | scar-derived |
| Voice Governor one-line law + breathing-pattern caveat | `/root/.hermes/SOUL.md` §VOICE-GOVERNOR | F13_RATIFIED (2026-09-17) |
| Gerbang DITING 6 dimensions | `EUREKA-2026-09-17-PERSONA-CIVILISATION-TRIAD.md` E1 + E12 | derived |
| Peace² / ΔS / RASA | `/root/forge_work/voice-governor/VOICE-GOVERNOR-DRAFT.md` | derived · F13-carried |
| SABAR cooldown protocol | `/root/.hermes/SOUL.md` §UNDANG-UNDANG BAHASA + ABAR separation floor | F13-owned |
| AI-speak / weak-closer / heat banks in `voice_gate.py` | SOUL.md §Bahasa & Rasa haram list + SCAR 2026-09-02 | observed, no formal document |
| Failure mode 6 (promised action not executed) | forward-test of this skill, 2026-09-19 — 2 of 3 arms emitted "Aku buat sekarang" for work that had not run, at gate exit 0 | observed |
| State chain `DECIDED ≠ SCHEDULED ≠ RUNNING ≠ DONE` | `/root/AAA/instructions/state-transition-discipline.md` | F13_RATIFIED_CHAT |

## v3.0 Expansion Notes

v3.0 absorbs the **VOICE-GOVERNOR — Bahasa Manusia Penuh** law into STAGE 3 as the send gate.
Previously that law lived in `~/.hermes/SOUL.md` and `/root/forge_work/voice-governor/`, with the
forge_work draft still reading `HOLD — awaiting Arif ratification` while SOUL.md carried it as
F13-ratified. It had no loadable skill, so it could not be loaded when relevant, diffed, or tested.

Design decisions worth keeping:

- **One entry point, not two.** A separate `voice-governor` skill would have competed with
  bridge-protocol's own trigger ("before composing any human-facing reply"). The law went into
  STAGE 3; the detail went to `references/voice-governor.md`.
- **The law became executable.** `scripts/voice_gate.py` exists because the skill's own
  Meta-Paradox check says awareness does not survive prompt-level format pressure. A model reading
  its own draft cannot reliably see its own AI-speak; a linter can.
- **The script is a witness, not a judge.** Tension, Peace², ΔS and RASA are declared
  judgment-only in its output rather than scored. A green run means only that no *mechanical*
  AI-speak survived. This follows the capability-truth law: do not let a tool imply a capability
  it does not have.
- **Register bans are audience-scoped.** `--audience internal` skips them, because the governor
  governs human-facing replies only.

### v3.0 forward-test result (2026-09-19) — and the defect it exposed

Three arms, one task each: two messaging tasks with the skill, one without (intended as control).

**What held.** All three arms ran `voice_gate.py` and reported exit 0. Prose came back in Penang BM,
no tables, no receipt labels, no service-desk closers. The judgment gates (Tension, Peace², ΔS,
RASA, Gravity) were each reasoned explicitly rather than skipped. One arm independently flagged
that its own reply made a transition claim that wasn't yet true — the state-transition discipline
surfacing without being asked for.

**What broke, honestly.**

1. **The control arm was contaminated.** It was told nothing about the skill, found
   `bridge-protocol` on disk unprompted, loaded it, and ran the gate. So the run proved the skill
   *self-triggers* — a useful signal — but produced **no valid comparison**. Forward-testing needs
   the skill physically unreachable for the control arm, or the control is just a second treatment.
2. **Failure mode 6 was found here.** Two of the three arms wrote "Aku buat sekarang" / "Aku masuk
   sekarang" for work that had not been executed, and both passed the gate at exit 0. Correct as
   register, false as transition. This is the defect that motivated §9 failure mode 6 and sequence
   check 7.

**Doctrine for next time:** mechanical leakage passes are testable; truth-of-action is not, and a
forward test will not surface it unless the test design includes an arm whose promised action is
deliberately *not* performed.

## v2.0 Expansion Notes

v2.0 consolidates the three-stage human reality bridge (READ→REASON→RESPOND) into a single
entry point. Previously, these lived in separate skills:
- **READ** stage absorbed operational rules from `governed-uncertainty` and `human-meaning-membrane`
- **REASON** stage absorbed cross-layer rules from `hermes-layer-discipline` and `hermes-rasa`
- **RESPOND** stage is the original bridge-protocol output contract

The companion skills remain for deep-dive situations but are no longer required as parallel
entry points. Start with bridge-protocol; load companions only when depth is demanded.

**Why this skill exists.** SOUL.md declared the bridge as the first thing loaded, but the doctrine
lived only in the system prompt. This skill is the same doctrine in the layer that can be audited.
SOUL.md remains the authority.
