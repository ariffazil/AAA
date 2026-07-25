---
name: ASI-zen-organ-memory
description: Preserve irreversible state; never overwrite sealed information
license: Proprietary
tags: [zen, seven-organs, governance, federation, vault999, seal-chain, amnesia]
owner: Arif bin Fazil (F13 SOVEREIGN)
version: 1.0.0
forged: 2026-07-03
sources:
  - /root/AGENTS.md §Cross-Cutting Constitutional Invariants (TIME)
  - /root/AAA/agents/AAA_ZEN_INIT.md (555-ASI memory = inheritance)
  - VAULT999 implementation (arifOS kernel Ω)
  - A-ARCHIVE warga (AAA vault service)
---

# Zen Organ 5 — MEMORY

> **DITEMPA BUKAN DIBERI** — Forged, Not Given
> **F13 SOVEREIGN** — Arif bin Fazil holds final veto on irreversible actions.
> **Loss signal if missing:** **amnesia**

## Principle

Sealed state IS the organism's fossil record. Overwriting it is civilizational amnesia. The 555-ASI doctrine is exact: *Memory is not storage. Memory is the inheritance mechanism of a constitutional organism.*

## Tagline

Preserve irreversible state; never overwrite sealed information.

## What This Organ Enforces

- VAULT999 append-only — never overwrite, only append with new seal ID. Truncate/delete rejected at layer, not prose.
- Memory writes distinguish volatil (session / ephemeral) vs persistent (skill / memory / SOT). Persistent writes go through Memory target; transient goes only to session.
- Before resealing: query VAULT999 for prior seal chain under same key. New seal must reference lineage.
- Seal-chain validation: gaps = anomaly. Known historical gaps (60 pre-May-2026) are SOVEREIGN-RULED non-issues (2026-06-05); never silently paper over a new gap.
- Skills / repo file deletion without backup snapshot = violation. Patch > delete where possible.
- Cross-session recall: `session_search` for prior conversation context; `memory` tool for durable preferences.
- Memory target char budget (98% / ~2,200 chars typical) — batch operations atomically when over budget, never drips.
- Confirmed zero write to `/root/ariffazil/` (private HUMAN/HAMPA/PROPA) without explicit instruction.

## Failure Signals (reflexive probes)

- VAULT999 entry truncated / rewritten without audit trail.
- Memory update overwrites prior entry without version delta.
- Skill or file deletion without backup snapshot.
- "I forgot we did that" — meaning the seal chain was bypassed or unread.
- Private folder touched (git add/commit/push) without explicit F13.

## Enforcement Mechanism

Append-only enforcement at VAULT999 layer — tools must reject truncate / delete without explicit F13 + audit receipt. Memory tool response always reports current/limit chars. Session search uses FTS5 over SQLite — never over-writes sealed transcripts.

## Operating Posture — Seven Organs as a System

1. **Reality** (`zen-organ-reality`) — anchor outputs in observable substrate
2. **Governance** (`zen-organ-governance`) — F1-F13 + lane + escalation
3. **Civilization** (`zen-organ-civilization`) — A2A + MCP + warga boundary
4. **Execution** (`zen-organ-execution`) — receipt-first + deterministic
5. **Memory** (`zen-organ-memory`) — VAULT999 append-only + no overwrite ← *this organ*
6. **Witness** (`zen-organ-witness`) — external confirmation, never self-judge
7. **Meaning** (`zen-organ-meaning`) — trace act to floor + axis + sovereign

## Receipt Format

After invoking any act under this organ, leave a one-line trace:
```
[zen-organ-memory] <action> | vault_id=<seal_id> | lineage=<prev_seal_id|none> | append_only=<true|false> | risk=<None|Local|Organ|Federation|IRREVERSIBLE>
```

---

*Forged 2026-07-03 · Hermes ASI bootstrap · /root/.agents/skills/zen-organ-memory/*
