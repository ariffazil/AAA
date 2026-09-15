# AAA RSI Loop — capability evolution, not skill accumulation

> **Ratified by F13 SOVEREIGN (Arif Fazil), 2026-09-15 — verdict: PARTIAL-SEAL**
> A. recursive skill improvement ............... SEAL
> B. recursive capability improvement .......... SEAL (dengan verifier)
> C. recursive AAA intelligence improvement .... PARTIAL-SEAL
>    (333 proposal models · 555 verification · routing heuristics · capability ranking)
> D. recursive self-governance improvement ..... **HOLD**
>    (F1–F13 · kernel · canon · judge · verifier · promotion threshold)

```
Capability may mutate.
Governance must witness mutation.
Governance may not self-authorize mutation.
```

## Why this exists

Measured 2026-09-15 from `/root/.local/share/arifos/rsi-ledger.jsonl`:

| Field | Count | Meaning |
|---|---|---|
| `turn_rsi.pulse` | 776 (82%) | per-turn heartbeat — "I observed, nothing improved" |
| diagnosis rows (bottleneck + fix) | 5 (0.5%) | the only real DIAGNOSE records |
| `improvements` (fixes applied) | 259 rows, **all zero** | zero fixes recorded as applied |
| `improvements_proposed` | 26 over 5 days | inhale |

**26 inhales, 0 exhales.** The loop observed and proposed. It never applied. This
directory is the exhale.

## The defect this replaces

```
OLD (inhale-only)                       NEW (vNext, F13-ratified)
SESSION                                 SESSION
  ↓                                       ↓
LOG                                     EUREKA / SCAR EXTRACTOR   extract.py
  ↓                                       ↓
LEDGER                                  SCAR CLASSIFIER           extract.py
  ↓                                       ↓
NO_CHANGE                               CAPABILITY ATOM           atoms.py
                                          ↓
                                        CAPABILITY GRAPH          atoms.py
                                          ↓
                                        INDEPENDENT VERIFIER      verify.py
                                          ↓
                                        PROMOTION GATE            promote.py
                                          ↓
                                        LIVE CAPABILITY           loop.py (EXHALE)
                                          ↓
                                        AAA STATE IMPROVEMENT
```

## Why atoms are capabilities, not skills

`Capability → Organ → Tool → Skill`. Skill sits at the bottom. A loop that turns
every eureka into a new skill produces 372 → 800 → 1500 skills and no more
intelligence — *Skill Accumulation Without Capability Compression*, entropy
disguised as learning.

Selection pressure belongs at the capability layer. Skills are adapters.

## Files

| File | Role |
|---|---|
| `config.yaml` | F13-owned thresholds. **Read-only to the loop.** |
| `atoms.py` | Capability atom schema + capability graph + fitness ledger. |
| `extract.py` | Live `state.db` + scar candidates + eurekas → classified atoms. |
| `verify.py` | Independent verifier. 4 checks, all must pass. |
| `promote.py` | Promotion gate + Layer-5 boundary (`FORBIDDEN_PATHS`, hardcoded). |
| `loop.py` | Orchestrator. Writes the exhale record. |

## The four verification checks

| Check | Rule | Failure meaning |
|---|---|---|
| **C1 LAYER** | claim layer == evidence layer | PROXY_REALITY — a layer answered with another layer's evidence |
| **C2 FALSIFY** | the atom states what would prove it wrong | unfalsifiable claim |
| **C3 REDERIVE** | the verifier re-runs the check against the **live** surface | claim not reproducible |
| **C4 PROCESS** | what *rank* of independence did the verdict earn? | see below |

### Independence is a rank, not a boolean

A string comparison (`producer != verifier`) passed while both modules were
authored by the same hand. That is name-level independence, not independence.
So C4 returns a class, and the class decides what the verdict may be **used for**:

| Class | Meaning | Allowed |
|---|---|---|
| `SELF` | same actor graded itself | **rejected outright** |
| `NOMINAL` | different names, same author | graph entry only — **PROVISIONAL**: no survival recorded, no rule proposed |
| `STRUCTURAL` | distinct authors | may record survival |
| `EXTERNAL_ORGAN` | FRAME / arif_judge / external receipt | may record survival and back a judgment-layer claim |

C1–C3 still hold at `NOMINAL`: C3 re-derives against the live filesystem, which
does not care who wrote the extractor. So a same-author verdict may say *"this
pattern exists in reality"*. It may not say *"this pattern was beaten"*.

Currently **every node is PROVISIONAL with zero survivals** — that is the honest
state, not a defect.

## Promotion routing

| Layer | Policy | Applies automatically? |
|---|---|---|
| `skill` | `auto_verified` | yes — queue atom, drain via `skill-learn-ingest.py` |
| `capability` | `auto_verified` | yes — capability-graph node upsert + survival record |
| `policy` | `propose_only` | no — written to `/root/forge_work/rsi-proposals/`, F13 decides |
| `judgment` | `propose_only` | no — same queue, ranking function stays F13 |
| `governance` | `forbidden` | **never** — raises `GovernanceHold` |

`UNCLASSIFIED` patterns are quarantined, never promoted: promoting an unnamed
pattern is how a library grows without capability growing.

## Running

```bash
python3 /root/AAA/rsi/loop.py                    # full cycle
python3 /root/AAA/rsi/loop.py --dry-run          # verify only, writes nothing
python3 /root/AAA/rsi/loop.py --window 3         # 3-day window
python3 /root/AAA/rsi/promote.py                 # boundary self-test
```

Exit codes: `0` = exhaled or steady state · `3` = novel atoms existed, none applied.

## State

```
state/atoms.jsonl          append-only capability atoms (folded on read)
state/capability-graph.json nodes + edges + fitness
state/quarantine.jsonl     unnamed patterns, held for classification
state/proposals.jsonl      Layer-3/4 items awaiting F13
state/receipts/            per-atom verification receipts + loop receipts
state/loop-ledger.jsonl    local exhale ledger
```

Also appended to `/root/.local/share/arifos/rsi-ledger.jsonl` with
`"type": "diagnose"` and a non-empty `"applied"` list — the record the old loop
never wrote.

## Boundary

This loop may not write: `F1–F13`, kernel, canon, judge, verifier, promotion
threshold, or this directory's own `config.yaml` / `verify.py` / `promote.py`.
Enforced by `FORBIDDEN_PATHS` **hardcoded in `promote.py`**, deliberately not
readable from config — so the loop cannot relax its own boundary by editing a
file it is otherwise allowed to read. `promote.py` self-tests this on every run.

DITEMPA BUKAN DIBERI ⚒️
