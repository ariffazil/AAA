# LEDGER MAP — one FROZEN RATIFIED REGISTRY, one LIVE FEED

*(marker file retained under its original name: `governance/federation-memory-writeback` tells agents to
look for `NON-CANONICAL.md` in this directory. Its original content was inverted — see "Correction carried"
below. Truth checked on disk 2026-09-19 with `lsattr`.)*

| ledger | status | attribute (`lsattr`) | rows · last written | entry shape |
|---|---|---|---|---|
| `/root/AAA/eurekas/eureka-entries.jsonl` | **LIVE FEED — the WRITE TARGET** | `--------------e-------` — writable, no immutable flag | 14 rows · 2026-09-18 | `{ts, agent, session, eureka, evidence, truth_class, actor, verdict}` |
| `/root/AAA/canon/eureka-entries.jsonl` | **FROZEN RATIFIED REGISTRY** — historical authority, **cite only** | `----i---------e-------` — **IMMUTABLE**; an append returns EPERM even as root unless the attribute is cleared, which is forbidden | 109 rows · 2026-09-16 | `{id, timestamp, type, title, source, summary, status}`, `id` = `EUREKA-<TOPIC>-<DATE>` |

**Append new eurekas to the live feed in this directory: `/root/AAA/eurekas/eureka-entries.jsonl`.** It is
read, not ignored — by `governance/durable-artifact-authoring/SKILL.md` (~line 87 instructs appending
there), by `skills/aaa-governance/aaa-doctrine-sealing/references/commit-gates.md`, and by
`governance/AMENDMENT-6-REGISTER-LAW-RATIFICATION-2026-09-15.md`.

**Never use `/root/AAA/canon/eureka-entries.jsonl` as a write target.** It is immutable by design and is
cited as historical authority by `canon/*.md` and `instructions/anti-calhoun.md`. Cite it; never unlock it.
The canon lock on `/root/AAA/canon`, `/root/AAA/governance`, `/root/arifOS/GENESIS` stays untouched —
promotion into that tree, where it ever happens, runs through the kernel seal lane, not an agent action.

## Correction carried — do not re-import

This file previously asserted that the SOT was `/root/AAA/canon/eureka-entries.jsonl` and described the
ledger beside it as *"a stray duplicate ledger (created 2026-09-12, no script reads it)"*, closing with the
rule *"Append nothing here. If you find new eurekas, write to `canon/eureka-entries.jsonl`."* Both halves
were wrong, and the label was factually inverted:

- the named write target **cannot be written at all** — immutable attribute → `EPERM`, so that instruction
  could never execute;
- the ledger in this directory is the **live feed**, with three readers, and it is the one written most
  recently (2026-09-18 vs 2026-09-16).

**Reason the two exist:** one was frozen as a ratified registry, one is the live feed. Do not port entries
between them and do not delete either — the frozen registry is the historical record of what was ratified
when. Both ledgers are unchanged by this correction: nothing was appended, unlocked, or moved.

## Historical record (2026-09-15 audit — kept as history, not as rule)

| entry | status at the time |
|---|---|
| 2026-09-12 ZZZ Sleep≠Death (333-AGI) | **PORTED** into the then-SOT as `EUREKA-2026-09-12-ZZZ-SLEEP-NOT-DEATH` |
| 2026-09-15 Register-as-Channel (HERMES) | already owned in canon by `EUREKA-REGISTER-AS-CHANNEL-2026-09-15` — no re-port |
| 2026-09-15 Register-as-Channel DELTA (HERMES) | fold-delta; doctrine lives in `instructions/register-as-channel.md` — no re-port |

DITEMPA BUKAN DIBERI
