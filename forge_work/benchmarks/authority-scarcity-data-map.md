# AUTHORITY_SCARCITY_DATA_MAP

> **Status:** DRAFT — pre-probe declaration. No probe written yet.
> **Author:** HERMES (assisted), F13 SOVEREIGN pending.
> **Created:** 2026-10-07 (Asia/Kuala_Lumpur)
> **Scope:** declare the data sources for any future `authority_scarcity_probe.py`, before the probe is written. Honest about gaps, not aspirations.
> **Falsifier (this document):** any row whose "Candidate Source" is not on disk with the declared byte size, or whose "Confidence" is not justified by what the file actually contains.

---

## 0 · Why this exists first

The hypothesis "authority scarcity > capability density" needs a measurement before it becomes a doctrine. A probe that *finds* what its theory predicts is a tautology, not an instrument. This map lists what each proposed metric could plausibly read, and where the reading would come from, **before** any code is written.

The map has only four columns. No opinion, no fifth column for "remediation." Remediation is the next layer's job.

---

## 1 · The map

| # | Metric | Candidate Source | Confidence | Gap |
|---|--------|------------------|------------|-----|
| 1 | **Capability Count (C)** | `/root/AAA/state/aforge/warga-capabilities.json` (30,108 B, exists) | **Medium** | Snapshot only. Per FI-008 audit: 44/122 aforge tools mapped to 7 verbs (78 unmapped). Single point in time, no history. |
| 2 | **Authority Gates (A)** | `/root/.hermes/runtime/authority_registry.json` (6,599 B, exists) — `canonical_paths` + `scoped_per_organ` keys | **Medium** | The registry is a *path classifier*, not a gate-count. `enabled` boolean in arifOS schema (item 5) is the actual gate; the registry only declares which paths are canon. Two different meanings of "authority" in the same column. |
| 3 | **Authority State at runtime** | `/root/arifOS/schemas/authority-state.schema.json` (4,566 B, exists) — `seals.{kernel,domain,judge,vault999,public}`, `forge_gate.enabled`, `execution_authority` | **Low** | Schema ≠ runtime. The file is a JSON Schema declaration. No `.jsonl` of *populated* states was located in this probe pass. A populated-state series is what would actually feed a measurement. |
| 4 | **Authority Drift dA/dt** | `/root/.hermes/carry_forward.json` (28,104 B) and/or `/root/.local/share/arifos/carry_forward.json` (37,595 B) — extract `arif_judge` verdicts, `SEAL`/`HOLD`/`VOID` counts per session | **Unknown** | Time-series unverified. Need to confirm the carry-forward schema carries the verdicts in a stable shape, and that older sessions are still in the file (not rotated out). Will require a separate read. |
| 5 | **Single-Actor Paths** | (none located) | **None** | No graph artifact found that names the propose→verify→approve→execute chain per actor. Would need to be reconstructed from gate call sites (e.g. `arif_forge`, `arif_seal` consumers) in source code. That is a separate probe, not a data source. |
| 6 | **Ungated Capability Count** | join of (1) and (2) — capabilities whose actor/target is not covered by any entry in (2) | **Low** | Join rule missing. What does "covered by a gate" mean — same path? same actor? same authority class? Three different joins, three different counts. Must be defined *before* the join, or the result is unfalsifiable. |
| 7 | **Authority Reuse Ratio** | ratio of capabilities gated by one authority class vs total | **Low** | Depends on (6) join rule. Cannot compute before (6) is defined. |
| 8 | **A/C Ratio (geometry only)** | ratio of (2) entries to (1) entries | **Unknown** | Two definitions of "authority" (path-classifier vs gate-state) give two ratios. Ratio is undefined until definition is fixed. *Ratio = precision theater* if computed before the definition is pinned. |

---

## 2 · What the three sources I actually opened contain

This section is for verification — not a sales pitch. Reading order matches the audit done at 2026-10-07 ~22:40 MYT.

### 2.1 `/root/.hermes/runtime/authority_registry.json` (6,599 B)

- 11 `canonical_paths` entries: SOUL, AGENTS_runtime, AGENTS_organ, AGENTS_top_level, CANON, INSTRUCTIONS, STAGED, RECEIPTS, GOVERNANCE, SHEBTOC_P0, SHEBTOC_P2
- 7 `scoped_per_organ` entries: GEOX, WEALTH, WELL, arifOS, A-FORGE, arifFlow, arif-fazil.com
- 4 `scoped_profiles`: hermes_apex, hermes_asi, hermes_forge, aaa_hermes
- 10 `zombies_tagged_NOT_CANONICAL` (files that LOOK authoritative but are not)
- `forged_at: 2026-10-04T03:40:32Z` — single snapshot, not a stream

### 2.2 `/root/.hermes/hermes_mcp/authority_lookup.json` (2,393 B)

- 31 path → authority_class entries
- `forged_at: 2026-10-04T03:41:06Z` — 41 seconds after the registry above
- A `reverse_lookup` for `witness_capture.py` — i.e. consulted by an existing runtime consumer
- **Overlap with 2.1:** 11/31 paths appear in 2.1's `canonical_paths`. The other 20 are profile-scoped or per-organ SOUL/AGENTS files.

### 2.3 `/root/arifOS/schemas/authority-state.schema.json` (4,566 B)

- Defines a *runtime* state object: `state_id`, `actor`, `seals.{kernel,domain,judge,vault999,public}`, `forge_gate.{enabled,reversibility_threshold,blockers}`, `execution_authority ∈ {HOLD,SEAL_AUTHORIZED,VOID}`
- 10 required properties; instance file conforming to this schema is what would carry the live state
- `forged_at: 2026-06-02 18:41 UTC` (per `description` field) — three months older than 2.1/2.2

**Implication:** the schema exists, the registry exists, but **a populated `authority_state` instance file was not located in this probe pass.** The schema is the *shape of a measurement*, not a measurement itself.

---

## 3 · What I did not find

Honesty is the point of this document. The following were searched and not found in this pass:

- A `*.jsonl` or time-series of populated `authority_state` instances.
- A graph artifact enumerating propose→verify→approve→execute chains per actor.
- A canonical join rule between `warga-capabilities.json` and the authority registry.
- A history of `arif_judge` verdicts in the carry-forward files (not yet opened; only existence + size confirmed).
- Any prior `authority_scarcity_*` artifact (searched `/root`, `find ... -name 'authority*'`, `grep scarcity /root/AAA` — all empty).

These are not necessarily absent in the federation; they are **absent from the three files I actually opened** and from the surface search I ran. The next layer's job is to widen the search before declaring a measurement impossible.

---

## 4 · The order of operations this map commits to

```text
D. This document.                              (DONE)
B1. Geometry probe.                            (BLOCKED on row 8 definition)
B2. Historical drift probe.                    (BLOCKED on row 4 schema check)
C.  Longitudinal falsification.                (BLOCKED on B1 + B2 producing comparable data)
A.  Doctrine patch, if data survive.           (BLOCKED on C)
```

Each step requires the previous step's data to exist, *witnessed*, not assumed. This is the order. Reversing it is a known anti-pattern (observe → doctrine → falsification).

---

## 5 · Falsifier for this map

If any of the following is true, this map is wrong and should be re-issued:

- A populated `authority_state` instance file exists and was missed.
- A proposal/verification/approval/execution graph already exists in some organ's source tree.
- `warga-capabilities.json` is updated in real time (the snapshot assumption in row 1 is wrong).
- `arif_judge` verdicts are not in `carry_forward.json` (the time-series assumption in row 4 is wrong).
- The carry-forward files have been rotated/truncated and historical data is gone.

Any of these should be reported before B1 begins, so the probe does not run on a false map.

---

DITEMPA BUKAN DIBERI ⚒️
