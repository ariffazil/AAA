# CORRECTION LEDGER CONVENTION v1 (F13-ordered 2026-10-05)

> **Status:** PENDING_F13 (F13-ordered 2026-10-05; awaiting SAH)

> **Problem it solves (one sentence):** the "888 throughput bottleneck" debate is unsettleable
> because human correction turns are never recorded anywhere — this convention makes them countable
> at zero schema cost.

## 1 · Turn tag (Hermes / any warga session)

When the sovereign's turn corrects an agent failure, prefix the turn content:

```
[C:<cause>] <original message>
```

`cause_class` enum (closed):
| code | cause | example (2026-10-05) |
|---|---|---|
| `c` | confabulation | "check ur own facts wei!!" (Tengku Taufik tenure) |
| `p` | phantom work | adjudicating the "7 injections done" text |
| `a` | permission_ask | "Nak Kimi run?" ×3 (membrane violation) |
| `i` | intent_drift | 4 turns to hear "give expectations, not research" |
| `o` | other (requires note) | — |

Untagged human turns are NOT counted as corrections (honest measure — undercount preferred over
guessed count). Heuristic detection is HARAM for this metric; the sovereign's tag is the witness.

## 2 · Daily count (on-demand, NO cron — F13 event-driven law)

`/root/AAA/scripts/attention_debt_daily.py [--date YYYY-MM-DD]` → reads `state.db` messages,
counts `[C:*]`-tagged human turns by cause, prints JSON. Run at session seal or on demand.
Append result to `carry_forward.json` `open_loops` block at session close.

## 3 · CHRON events

Correction events are planted in CHRON as `kind: CORRECTION` (additive enum, falls back to
`OBSERVATION` with `CORRECTION:` title prefix if the store validates) with
`note: cause_class=<x>; turns=<n>; session=<id>`. These are the durable, queryable instances.

## 4 · Vault

Kind `CORRECTIVE_SEAL` (already exists in outcomes.jsonl, 1 prior use) is **reserved** for
correction closures only — a correction is closed when the causing agent demonstrably stops
repeating the failure class (fixture/audit evidence, not vibes).

## 5 · What is NOT debt

F13-class human turns (SAH binaries, money, irreversible, canonical records, external ports,
direction-of-record) are the constitution working — never counted as debt. Target of the metric
is not zero; it is **zero self-correctable failures**.
