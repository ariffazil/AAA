# Context Admission Map — P0 #1

**measured** 2026-10-23T03:47:53+00:00 · host forge · observer hermes-kvm8 · classification OBSERVED_SELF

## The claim under test

> "Fail panduan federation berukuran 43,433 aksara tetapi had kemasukan ialah 32,000,
> menyebabkan kandungan ditanda TRUNCATED setiap turn."

## What is actually true (measured, not narrated)

```
file            /root/AAA/AGENTS.md
source chars    43,434
admitted        28,800   (66.3%)   <- head 22,400 + tail 6,400
omitted         14,634   (33.7%)   <- the middle, 19 lines
config          context_file_max_chars: 70000
runtime marker  "[...truncated AGENTS.md: kept 22400+6400 of 43433 chars ...]"
sha256(source)   77951da9bb708ae2b814b1d8bcd7d8c9
sha256(admitted) c0dfd560df8131b6f35fc7c4f8e700e9
```

The 32,000 figure is **not** what the runtime reports. The marker names 43,433 total and
28,800 kept, i.e. a 66.3% admission rate against a 70,000-char configured cap. Recorded as a
contradiction between the brief and the live marker.

## Which ranges survive

| region | lines | chars | content |
|---|---|---|---|
| head kept | 1–100 | 22,400 | preamble, EMD gate, fragment table (first 16 rows), mid-doctrine |
| **gap** | **100–118** | **14,634** | **the rest of the doctrine-fragment table — 16 markdown rows** |
| tail kept | 118–133 | 6,400 | R-FILTER, Q-MAP, GOL, DeepSeek distill, question policy, MCP interceptor |

## Mandatory invariant coverage

| invariant | verdict |
|---|---|
| EXECUTION-FIRST / anti-collapse | **SURVIVES** |
| F1/F13/888 binding | **SURVIVES** |
| Fail-closed / HOLD | **ABSENT_IN_SOURCE** |
| Authority envelope / CanMutate | **SURVIVES** |
| State transition PRODUCED!=SENT | **ABSENT_IN_SOURCE** |
| Anti-bangang 10 laws | **ABSENT_IN_SOURCE** |
| Human attention membrane | **SURVIVES** |
| Sovereign = ARIF terminal | **SURVIVES** |
| No self-SEAL / Godel | **SURVIVES** |
| Data authority hierarchy | **ABSENT_IN_SOURCE** |

**Result: 0 of 10 mandatory invariants are lost to truncation.**
6 survive in the head, 1 survives in the tail, 1 in both.
4 are **absent from this file entirely** — anti-bangang laws, `PRODUCED≠SENT`,
`data-authority-hierarchy`, fail-closed/HOLD — because they live in `/root/AGENTS.md`
(the canonical constitution) and in `/root/.codex/AGENTS.md` / `/root/.kimi-code/AGENTS.md`
(rendered overlays), not in the AAA pointer file.

## So what IS lost — the sharper finding

The omitted 33.7% is **the doctrine index**: 16 table rows naming canon and instruction files.
**20 doctrine paths are named only inside the gap**, and therefore invisible to the runtime:

- `/root/AAA/canon/APEX-ZEN-CONSTITUTIONAL-MAINTENANCE-WITNESS-2026-09-20.md`
- `/root/AAA/canon/BIJAKSANA-SUBSTRATE-CANON-2026-09-21.md`
- `/root/AAA/canon/COMMERCIAL-SURVIVAL-CANON-2026-09-21.md`
- `/root/AAA/canon/CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md`
- `/root/AAA/canon/CONSTITUTIONAL-COMPLEXITY-BUDGET-2026-09-21.md`
- `/root/AAA/canon/KIMI-APEX-ZEN-BOOTSTRAP.md`
- `/root/AAA/canon/META-WISDOM-CANON-2026-09-21.md`
- `/root/AAA/instructions/anti-haram-behavior-canonical-human.md`
- `/root/AAA/instructions/federation-init-reality-first-2026-10-22.md`
- `/root/AAA/instructions/proxy-reality-paradox.md`
- `/root/AAA/instructions/rationality-filter-doctrine.md`
- `/root/AAA/instructions/safety-is-emergence.md`
- `/root/AAA/reports/TRILOGY-GAP-ANALYSIS-2026-09-21.md`
- `/root/AAA/reports/anti-haram-human-witness-2026-09-21.md`
- `/root/AAA/reports/bijaksana-substrate-witness-2026-09-21.md`
- `/root/AAA/reports/commercial-survival-witness-2026-09-21.md`
- `/root/AAA/reports/constitutional-architecture-witness-2026-09-21.md`
- `/root/AAA/reports/constitutional-complexity-budget-witness-2026-09-21.md`
- `/root/AAA/reports/kernel-actor-mismatch-falsehold-2026-10-02.md`
- `/root/AAA/research/CANON-LITERATURE-COROLLARY-MAP-2026-09-21.md`

This is **discoverability loss, not authority loss**. The agent still knows it must not
self-SEAL and must fail closed where those clauses appear; it no longer knows that
`/root/AAA/instructions/safety-is-emergence.md` or
`/root/AAA/canon/CONSTITUTIONAL-COMPLEXITY-BUDGET-2026-09-21.md` exist at all.

## Verdict

```
ADMISSION VERDICT: PARTIAL
```
Not `TRUNCATED_CRITICAL` — no authority clause is lost.
Not `COMPLETE` — a third of the index never arrives.

## Fix direction (not applied)

Do **not** shorten the file — shortening deletes doctrine. Two better moves:

1. **Split the index out.** The fragment table is machine-readable data wearing prose. Emit it
   as `/root/AAA/state/fragment-index.json` and have the runtime load the index separately from
   the doctrine prose. Then truncation of the prose cannot blind the index.
2. **Reorder for truncation safety.** Place the authority and fail-closed clauses in the first
   20% (they already are) and the index in the last 20% (it is currently in the middle 33.7%,
   exactly the range the 70/20/10 split discards). One move: index to the end.

## Falsifier

If the runtime marker changes to a different kept/total pair, or if a mandatory authority clause
is found inside the omitted char range `[22400, 37034]`, this map is wrong and must be re-derived.
