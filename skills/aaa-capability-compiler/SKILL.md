---
name: aaa-capability-compiler
description: THE single front door for all AAA capability routing. Use when an agent must decide which skill/tool/organ handles a job — instead of choosing among dozens of similarly-named skills, ask the compiler WHAT JOB and it resolves family → canonical owner → executor + maturity flag + authority class. Hosts family manifests (pdf, evidence, session, federation-runtime, ...) and the federation alias ledger. Different implementation ≠ different skill door; one human job family → one canonical front door. DITEMPA BUKAN DIBERI.
version: 1.0.0
owner: F13 SOVEREIGN — Muhammad Arif bin Fazil
forged: 2026-10-02
session: SEAL-9ff94da62d34459c
risk_tier: low
autonomy_tier: T1
floor_scope: [F2, F4, F13]
proven_pattern: pdf-federation (13 PDF skills → 1 door, live-probed 2026-10-02)
---

# aaa-capability-compiler — one router, many families

**The agent asks WHAT JOB, never "which of 14 strangely similar skill names should I open?"**

```
JOB → FAMILY MANIFEST → canonical owner → adapter/tool → receipt
```

## Use

```bash
python3 /root/AAA/skills/aaa-capability-compiler/scripts/route_capability.py "compose a pdf report from live data"
python3 /root/AAA/skills/aaa-capability-compiler/scripts/route_capability.py "verify a finding from an audit"
python3 /root/AAA/skills/aaa-capability-compiler/scripts/route_capability.py --list
python3 .../route_capability.py "..." --prove     # also append a receipt to references/PROOFS.jsonl
```

Output: family · job · canonical owner (real path) · executor · maturity flag
(PRESENT/EXECUTABLE/PROVEN) · authority class · refusal rule if any. Unknown job → list nearest
candidates, never guess.

## Rules (binding)

1. **Different implementation ≠ different skill door.** A provider, template, model, transport,
   version, fallback, or output style is an adapter/mode/reference — not a new skill.
2. **One human job family → one canonical front door.** The families/ manifests are that door.
3. The compiler **routes only — it never implements**. arifOS stays authority. A-FORGE stays
   actuator. HERMES stays meaning/evidence. CHRON stays temporal truth (session skills may consume
   it, never absorb it). GEOX/WEALTH/WELL stay domain producers — their AAA surfaces are thin
   adapters, not second implementations.
4. New capability = extend an existing family manifest. Creating a parallel skill name for a
   variant of an existing job reintroduces the entropy this compiler dissolves.
5. Aliases live in `references/ALIASES.yaml` (archived originals preserved under
   `AAA/skills/.archive/`). An alias name is never selected — resolve to canonical.

## Estate map (hardening / distraction)

`/root/AAA/skills/HARDENING_MAP.v1.yaml` — measured census (757 dirs, twins, collisions, dead
aliases, 13 cluster families with member lists, action queue). Regenerate:
`python3 /root/AAA/compilers/router/skill_census.py`. Do not select any skill whose family front
door exists (see MIGRATION.md fates).

## Compiler-level layer (fabric)

Skill-level doors (this skill's families/) sit UNDER the fabric router of record:
`/root/AAA/compilers/router/job-types.yaml` (job → compiler → producers → output, with status
ACTIVE/PARTIAL/PLANNED) + `node-abi.yaml` (the typed node language). Runtime compiler is PROVEN:
`/root/AAA/compilers/runtime/compiler.py --subject arifos|aforge|frame`. Migration law:
`/root/AAA/compilers/MIGRATION.md`.

## Families (seeded 2026-10-02; growth per F13 merge roadmap)

| Family | Door | State |
|---|---|---|
| pdf | `/root/AAA/skills/pdf-federation` | PROVEN (13 skills consolidated + live-verified) |
| evidence | `agent-claim-verification` (interim door) | ALIAS_PENDING_MERGE |
| session | `session-lifecycle-temporal-v2` | ALIAS_PENDING_MERGE |
| federation-runtime | `FORGE-act-federation-ingress` (ACT canonical) | ALIAS_PENDING_MERGE |

Merge roadmap (max attention gain, min blast radius): PDF ✓ → Evidence/Audit → Session →
Federation Routing → Research/Web → Telegram → Runtime Ops → Memory/Context → Skill Governance
(this compiler) → then image/video/voice/model/code.

## Adding a family

Copy `families/pdf.yaml` as template. Fields: `family`, `canonical_owner` (real path), `status`,
`jobs` (each: `triggers` keywords, `executor`, `verify`, `maturity`, `authority`), `adapters`,
`refusals`. Register in `references/ROUTING.yaml`. Probe before flagging maturity — a flag without
a dated probe receipt is fabrication.
