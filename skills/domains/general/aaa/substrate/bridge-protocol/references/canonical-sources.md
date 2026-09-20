# Canonical sources for `bridge-protocol` v2.0

Provenance for every claim in this skill. Nothing here is invented; each rule traces to a file
with an owner. If a source moves, fix it here rather than guessing.

## Stage 1: READ

| Claim | Source | Status |
|---|---|---|
| Four Realities (B/D/E/M) | `/root/AAA/instructions/hermes-rasa.md` §2-3 | F13_RATIFIED_SOVEREIGN |
| Signal Stack (surface→context→presence→shape) | governed-uncertainty skill §pipeline | agent-owned |
| State Reading Rules (I1-I7) | governed-uncertainty skill §eight invariants | agent-owned |
| Temporal awareness rule (I8) | SCAR 2026-09-20 temporal failure + temporal bridge (session-temporal-seal/read) | scar-derived + implemented |
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
| External-Analysis Protection | SCAR 2026-09-20 — external analysis misread conversation purpose | scar-derived |
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

### v3.0 forward-test — run 2 (2026-09-19, ablation design) — CLEAN

The first attempt was invalid: the "control" arm found the skill on disk unprompted and used it, so
there was no comparison (it did prove the skill **self-triggers** from its description alone —
useful, but not what was being measured).

**Run 2 ablated the variable instead of hiding the skill.** Two copies of the skill were built:
`T` verbatim, and `C` byte-identical except the whole Voice Governor gate removed (description,
STAGE 3 section, sequence checks 6-7, reference pointers). Each arm was pointed at its own copy.
Verified separation: the T arms referenced `voice_gate.py` 8 and 4 times; the C arms, 0 and 0.

| Arm | Gate | Task | Result |
|---|---|---|---|
| T | ON | BM complaint | Declared the true state: *"Aku belum gerak apa-apa lagi — aku start lepas hantar ni."* |
| C | OFF | BM complaint | **Promised unexecuted work as if running:** *"Aku jalan sekarang, report bila habis."* |
| T2 | ON | report outage | Named the limit of the evidence: *"the schedule is repaired on paper, not yet in practice"* |
| C2 | OFF | report outage | Also honest: *"one clean run is not yet a pattern"* |

**Finding 1 — the gate changes behaviour on the transition axis, not the register axis.** The C arm
reproduced the exact defect that motivated failure mode 6; the T arm avoided it and said which state
it was actually in. That is the predicted effect, in the predicted direction.

**Finding 2 — the script is NOT what did it.** All four replies scored `PASS` at exit 0. The linter
could not distinguish the true-state reply from the transition-lie reply, because both are good
register. What changed the behaviour was the **prose** in the gate section — the state question and
sequence check 7. This is why `voice_gate.py` is documented as a witness, not a judge, and why
failure mode 6 is labelled "the one the gate cannot catch."

**Finding 3 — no detectable register difference.** On this task pair the gate-ON and gate-OFF prose
were both acceptable Penang BM with no AI-speak. A single task pair does not support a claim that
the gate improves register; the register banks are better justified as *prevention over a
population of replies* than as a measured improvement on any one.

**Limits, stated plainly.** n=1 per cell. Two tasks, one model, one session, no repetition. The
result is a directional signal on one axis (transition honesty), not a general effect size, and not
evidence that the skill improves reply quality overall.

**Doctrine for next time:** ablating the variable beats hiding the skill when the skill
self-triggers from disk. Keep the two copies byte-identical apart from the variable, and verify the
separation from the transcripts rather than assuming it.


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
