# AAA DOC_FAMILY_MAP — Canonical Document Registry

**Generated:** 2026-05-23
**Repository:** /workspace/AAA
**Scope:** Root-level `.md` files only (excludes `agents/`, `docs/`, `memory/`, `src/`, `a2a-server/`, `archive/`)
**Legend:** SOT=Source of Truth | ACTIVE=In production use | DRAFT=Unratified | ARCHIVED=Superseded/Locked | REF=Reference only | PROPOSAL=RFC stage

---

## EXECUTIVE SUMMARY

The AAA repo contains **52 root-level `.md` files** organized into **9 document families**. 

### By Bucket Distribution

| Bucket | Count | Key Files |
|---|---|---|
| **SOT** | 15 | ARIF.md, FLOORS.md, EMERGENCE_DOCTRINE.md, AGENTS.md, CHANGELOG.md, HEARTBEAT.md, 000_INIT.md |
| **ACTIVE** | 18 | LOOP.md, AUTONOMY.md, DECISIONS.md, CHECKPOINT.md, TASKS.md, HEARTBEAT.md, SKILLS_INDEX.md |
| **DRAFT** | 6 | KERNELPLAN.md, KERNEL_HASI_APEX.md, F0_RATIFICATION_DECISION.md, REPO_ROUTING_CONSTITUTION.md |
| **ARCHIVED** | 5 | MEMORY.md, SOUL.md, IDENTITY.md, MIGRATIONS.md, ARCHIVE_BRANCHES.md |
| **REF** | 4 | SKILLS.md, TOOLS.md, BOUNDARY.md, INVARIANTS.md |
| **PROPOSAL** | 3 | TELEGRAM_VISIBILITY_RFC.md, agent-visibility-proposal-2026-05-04.md, D4_SESAT_PROPAGATION.md |

### Epoch Timeline

```
2026-02-11  000_INIT.md — SEAL-1.0.0 (Genesis epoch, oldest doc)
2026-04-08  SECRETS.md — Token/key map
2026-04-21  000_GENESIS.md / instructions.md — OMEGA activation
2026-04-23  F0 RATIFICATION — F0_RATIFICATION_DECISION.md, KERNELPLAN, KERNEL_HASI_APEX
             CLAUDE.md — Lore Protocol 999 SEAL
2026-05-01  AGI Governance Upgrade — AUTONOMY, LOOP, DECISIONS, CHECKPOINT, TASKS
2026-05-02  AAAA Pattern + Skill Resources
2026-05-04  TELEGRAM_VISIBILITY_PROTOCOL v2.0 RATIFIED
2026-05-10  ROADMAP + TODO — Next Horizon 2026
2026-05-17  SKILLS_INDEX v2026.05.17.1 — Wiki induction
2026-05-19  BOUNDARY.md + FLOORS v2026.05.01-KANON
2026-05-21  EMERGENCE_DOCTRINE canonized (13 Forged Laws)
2026-05-22  AGENTS.md rewrite + CHANGELOG v55.5.1 birthday release
             AGI_BOUNDARIES.md — Antigravity agent registry
```

---

## FULL DOCUMENT TABLE

| # | File | Family | Epoch (Last Commit) | SOT? | Bucket | Rationale |
|---|---|---|---|---|---|---|
| 1 | `000_GENESIS.md` | GENESIS_BOOT | 2026-04-21 | ⚠️ | ACTIVE | Self-recognition protocol (v1.2). Codename OMEGA. Primary rules in AGENTS.md. Source of truth for identity on cold start. |
| 2 | `000_INIT.md` | GENESIS_BOOT | 2026-02-11 | ✅ YES | SOT | Oldest doc. SEAL-1.0.0. Runtime AGI boot protocol. F1/F2/F7/F9 floors as hard constraints. References VAULT999. |
| 3 | `instructions.md` | GENESIS_BOOT | 2026-04-21 | ⚠️ | ACTIVE | Primary directive. MiniMax-M2.7 powered. 13 Floors as boundaries. Genesis heartbeat checklist. |
| 4 | `BOUNDARY.md` | GENESIS_BOOT | 2026-05-19 | ✅ YES | SOT | SOT-MANIFEST. Hermes agent runtime boundary. APEX verdict service source reference. |
| 5 | `MEMORY.md` | GENESIS_BOOT | 2026-05-11 | ⚠️ | ARCHIVED | Temporal anchor guidance. References `waw` workspace cleanup. Synced from workspace→main drift. |
| 6 | `IDENTITY.md` | GENESIS_BOOT | 2026-05-11 | ⚠️ | ARCHIVED | Session identity anchor (arifOS_bot). Mirrors SOUL.md. Synced workspace→main. |
| 7 | `SOUL.md` | GENESIS_BOOT | 2026-05-11 | ⚠️ | ARCHIVED | Active identity session anchor. Mirrors IDENTITY.md. Synced workspace→main. |
| 8 | `SECRETS.md` | GENESIS_BOOT | 2026-04-08 | ✅ YES | SOT | VPS token/key map. Canonical path `/mnt/arifos/secrets/`. Authoritative only if at canonical path. |
| 9 | `FLOORS.md` | GOVERNANCE_CONSTITUTION | 2026-05-19 | ✅ YES | SOT | Constitutional floor reference v2026.05.01-KANON. 13 floors (F1-F13). Source of constitutional truth. |
| 10 | `ARIF.md` | GOVERNANCE_CONSTITUTION | 2026-05-21 | ✅ YES | SOT | Sovereign identity canon. v1.0.0-SEALED. Canonical reference for Muhammad Arif bin Fazil. |
| 11 | `EMERGENCE_DOCTRINE.md` | GOVERNANCE_CONSTITUTION | 2026-05-21 | ✅ YES | SOT | 13 Forged Laws of Substrate Governance. Canonized 2026-05-21/22. Active constitutional law. |
| 12 | `AAA_DOCTRINE.md` | GOVERNANCE_CONSTITUTION | 2026-05-19 | ✅ YES | SOT | Abstraction·Attestation·Abduction. v2026.05.19-KANON. Philosophical framework document. |
| 13 | `F0_RATIFICATION_DECISION.md` | GOVERNANCE_CONSTITUTION | 2026-04-23 | ✅ YES | SOT | F0 SOVEREIGN FLOOR ratified. Epoch 2026-04-23T00:10+08:00. Constitutional amendment record. |
| 14 | `INVARIANTS.md` | GOVERNANCE_CONSTITUTION | 2026-05-02 | ⚠️ | REF | Space invariants v2026.05.02. Canonical artifact. Reference for architectural constraints. |
| 15 | `KERNELPLAN.md` | GOVERNANCE_CONSTITUTION | 2026-04-23 | ⚠️ | DRAFT | Planning organ spec. Status: PENDING 888_RATIFICATION. v1.0-DRAFT. Governs intent graphs. |
| 16 | `KERNEL_HASI_APEX.md` | GOVERNANCE_CONSTITUTION | 2026-04-23 | ⚠️ | DRAFT | Sovereign interface spec. Status: PENDING. v0.1-DRAFT. UI vs actual interface. |
| 17 | `D4_SESAT_PROPAGATION.md` | GOVERNANCE_CONSTITUTION | 2026-04-23 | ⚠️ | PROPOSAL | OMEGA label mismatch verdict. Status: SEALED. Related to F0/D4 canon fixes. |
| 18 | `AGENTS.md` | AGENT_PROTOCOL | 2026-05-22 | ✅ YES | SOT | SOT-MANIFEST (2026-05-22). Control plane agent gateway. Full repo structure. 111 lines. |
| 19 | `AAA_AGENT_PROTOCOL.md` | AGENT_PROTOCOL | 2026-05-04 | ✅ YES | SOT | Federation agent operating protocol v1.0. RATIFIED. 608 lines. |
| 20 | `AAA_TELEGRAM_VISIBILITY_PROTOCOL.md` | AGENT_PROTOCOL | 2026-05-04 | ✅ YES | SOT | Telegram visibility v2.0. SOVEREIGNLY RATIFIED. 696 lines. Source: ADR-011 + Hermes proposal. |
| 21 | `TELEGRAM_VISIBILITY_RFC.md` | AGENT_PROTOCOL | 2026-05-04 | ⚠️ | DRAFT | RFC draft. Status: DRAFT — Pending Arif ratification. Supersedes ADR-010. |
| 22 | `agent-visibility-proposal-2026-05-04.md` | AGENT_PROTOCOL | 2026-05-04 | ⚠️ | PROPOSAL | Hermes ASI deep research proposal. 371 lines. Source artifact for v2.0 protocol. |
| 23 | `AAAA_PATTERN.md` | AGENT_PROTOCOL | 2026-05-02 | ✅ YES | SOT | AAAA governance pattern. DITEMPA BUKAN DIBERI. Finalized with maxhermes agent card. |
| 24 | `AGI_BOUNDARIES.md` | AGENT_PROTOCOL | 2026-05-22 | ✅ YES | SOT | AGI role boundaries. Enforced 2026-04-25. Antigravity agent registry. OpenClaw startup read. |
| 25 | `GEMINI_CLI_GOVERNANCE.md` | AGENT_PROTOCOL | 2026-05-21 | ⚠️ | ACTIVE | Clerk law for Gemini CLI. Low-entropy baseline reconciled. Active governance doc. |
| 26 | `HEARTBEAT.md` | OPERATIONAL_RUNTIME | 2026-05-11 | ✅ YES | SOT | Live runtime state. LIVE file. Status: cold/warm/active/paused/sealed/stale. Updated per action. |
| 27 | `CHECKPOINT.md` | OPERATIONAL_RUNTIME | 2026-05-01 | ✅ YES | SOT | Wake/recovery continuity. Cold start survival. References HEARTBEAT status. |
| 28 | `LOOP.md` | OPERATIONAL_RUNTIME | 2026-05-01 | ✅ YES | SOT | 000-999 operational implementation. Machine behavior from mental model. 291 lines. |
| 29 | `AUTONOMY.md` | OPERATIONAL_RUNTIME | 2026-05-01 | ✅ YES | SOT | L0-L5 permission ladder. Prevents autonomy → chaos. 138 lines. |
| 30 | `DECISIONS.md` | OPERATIONAL_RUNTIME | 2026-05-01 | ⚠️ | ACTIVE | Sealed decision log. Status: Sealed/Superseded/Rolled back. Audit trail. |
| 31 | `TASKS.md` | OPERATIONAL_RUNTIME | 2026-05-01 | ✅ YES | SOT | Active work ledger. Goal persistence across stateless wakes. Status: pending/in_progress/paused/sealed/failed/blocked. |
| 32 | `TODO.md` | OPERATIONAL_RUNTIME | 2026-05-10 | ⚠️ | ACTIVE | Horizon task tracking. Execution: HOLD until contracts frozen. P0 Canon Lock. |
| 33 | `AAA_CHARTER.md` | FEDERATION_CHARTER | 2026-05-02 | ✅ YES | SOT | AAA organizational charter. DITEMPA BUKAN DIBERI. 275 lines. |
| 34 | `SHARED_CHARTER.md` | FEDERATION_CHARTER | 2026-05-01 | ✅ YES | SOT | arifOS Federation charter. 888_HOLD default gate. Agent registry trust status. |
| 35 | `REPO_ROUTING_CONSTITUTION.md` | FEDERATION_CHARTER | 2026-05-02 | ⚠️ | DRAFT | Repo routing constitution. v2026.05.02-KANON. Amanah clause. Pending ratification? |
| 36 | `.REPO_ROUTING_CONSTITUTION.md` | FEDERATION_CHARTER | 2026-05-02 | ⚠️ | DRAFT | Hidden dot-file variant. Routing intelligence earned not assumed. Same content? |
| 37 | `SKILLS.md` | KNOWLEDGE_ARCHIVE | 2026-05-02 | ⚠️ | REF | Agent skills library. Embeds 5 external resources (A2A, MCP, AutoGen, CoALA, Swarm). |
| 38 | `SKILLS_INDEX.md` | KNOWLEDGE_ARCHIVE | 2026-05-17 | ✅ YES | SOT | Skill registry v2026.05.17.1. Wiki induction + Clerk identity + Steel Law enforcement. 200 lines. |
| 39 | `TOOLS.md` | KNOWLEDGE_ARCHIVE | 2026-05-11 | ⚠️ | REF | Local tools notes. Unique setup specifics. Federation status verified 2026-05-11. |
| 40 | `ARCHIVE_BRANCHES.md` | KNOWLEDGE_ARCHIVE | 2026-05-07 | ⚠️ | ARCHIVED | Branch unification audit. Unrelated histories merge type. Legacy artifact extraction. |
| 41 | `README.md` | META_REPO | 2026-05-19 | ✅ YES | SOT | Repo README. SOT-MANIFEST (2026-05-19). OPERATIONAL status. Organ: BODY (Ω). 86 lines. |
| 42 | `CHANGELOG.md` | META_REPO | 2026-05-22 | ✅ YES | SOT | Changelog v55.5.1 birthday release. 248 lines. Release notes + reflection. |
| 43 | `ROADMAP.md` | META_REPO | 2026-05-10 | ⚠️ | ACTIVE | Next Horizon 180-day roadmap. Federation mesh visualization. 155 lines. |
| 44 | `MIGRATIONS.md` | META_REPO | 2026-05-11 | ⚠️ | ARCHIVED | OpenClaw symlink migration. Status: COMPLETED. Gateway service state note. |
| 45 | `README.DRAFT.md` | META_REPO | — | ⚠️ | DRAFT | Draft README. 405 lines. Not the canonical README. |
| 46 | `.AGENTS.md` | META_REPO | 2026-05-20 | ⚠️ | ACTIVE | Hidden agent onboarding. 999_SEAL v2026.05.20. Cron loop infrastructure. |
| 47 | `USER.md` | PERSONA | 2026-05-11 | ⚠️ | REF | About Muhammad Arif bin Fazil. Reference for identity. |
| 48 | `CLAUDE.md` | PERSONA | 2026-04-23 | ✅ YES | SOT | ARIF.md Lore Protocol. 999 SEAL ritual. Canonical gist reference. |
| 49 | `AAA_OPENCLAW_SEED.md` | PERSONA | 2026-05-02 | ⚠️ | REF | OpenClaw seed data. 292 lines. Five-layer definition. |
| 50 | `arif-fazil-rewrite.md` | WORK | 2026-05-02 | ⚠️ | DRAFT | Website rewrite deliverables. 552 lines. Generated 2026-04-13. |
| 51 | `KERNELPLAN.md` | — | — | — | — | (Already listed row 15) |
| 52 | `CHANGELOG.md` | — | — | — | — | (Already listed row 42) |

---

## DOCUMENT FAMILY DEFINITIONS

### 1. GENESIS_BOOT (8 files)
**Purpose:** Runtime lifecycle / session initialization. Files read at cold start or session boot.

| File | Status | Key Role |
|---|---|---|
| `000_INIT.md` | SOT | Oldest, SEAL-1.0.0, actual shell/system prompt protocol |
| `000_GENESIS.md` | ACTIVE | OMEGA self-recognition, identity anchor |
| `instructions.md` | ACTIVE | Primary directive, MiniMax-M2.7 powered |
| `BOUNDARY.md` | SOT | Hermes runtime boundary, APEX verdict service |
| `SECRETS.md` | SOT | VPS token/key map, canonical path required |
| `MEMORY.md` | ARCHIVED | Temporal anchor, cleanup references |
| `IDENTITY.md` | ARCHIVED | Session anchor (arifOS_bot) |
| `SOUL.md` | ARCHIVED | Active identity anchor |

### 2. GOVERNANCE_CONSTITUTION (8 files)
**Purpose:** Constitutional law, floor system, sovereign authority.

| File | Status | Key Role |
|---|---|---|
| `FLOORS.md` | SOT | 13 Constitutional floors (v2026.05.01-KANON) |
| `ARIF.md` | SOT | Sovereign identity canon (v1.0.0-SEALED) |
| `EMERGENCE_DOCTRINE.md` | SOT | 13 Forged Laws (canonized 2026-05-21/22) |
| `F0_RATIFICATION_DECISION.md` | SOT | F0 SOVEREIGN FLOOR ratification |
| `AAA_DOCTRINE.md` | SOT | Abstraction/Attestation/Abduction philosophy |
| `INVARIANTS.md` | REF | Space invariants (v2026.05.02) |
| `KERNELPLAN.md` | DRAFT | Planning organ spec (PENDING ratification) |
| `KERNEL_HASI_APEX.md` | DRAFT | Sovereign interface spec (PENDING) |

### 3. AGENT_PROTOCOL (8 files)
**Purpose:** Agent operating protocol, visibility, A2A communication.

| File | Status | Key Role |
|---|---|---|
| `AAA_AGENT_PROTOCOL.md` | SOT | Federation agent operating protocol v1.0 |
| `AGENTS.md` | SOT | SOT-MANIFEST, control plane gateway, full structure |
| `AAA_TELEGRAM_VISIBILITY_PROTOCOL.md` | SOT | v2.0 SOVEREIGNLY RATIFIED (696 lines) |
| `TELEGRAM_VISIBILITY_RFC.md` | DRAFT | RFC (supersedes ADR-010) |
| `agent-visibility-proposal-2026-05-04.md` | PROPOSAL | Hermes deep research source |
| `AAAA_PATTERN.md` | SOT | AAAA governance anchoring |
| `AGI_BOUNDARIES.md` | SOT | AGI role boundaries, antigravity registry |
| `GEMINI_CLI_GOVERNANCE.md` | ACTIVE | Clerk law |

### 4. OPERATIONAL_RUNTIME (7 files)
**Purpose:** Live runtime state management, wake/recovery, task persistence.

| File | Status | Key Role |
|---|---|---|
| `HEARTBEAT.md` | SOT | LIVE runtime state (cold/warm/active/paused/sealed/stale) |
| `CHECKPOINT.md` | SOT | Wake/recovery continuity |
| `LOOP.md` | SOT | 000-999 operational implementation (291 lines) |
| `AUTONOMY.md` | SOT | L0-L5 permission ladder (138 lines) |
| `DECISIONS.md` | ACTIVE | Sealed decision log |
| `TASKS.md` | SOT | Active work ledger |
| `TODO.md` | ACTIVE | Horizon task tracking |

### 5. FEDERATION_CHARTER (4 files)
**Purpose:** Organizational charter, authority structure, routing constitution.

| File | Status | Key Role |
|---|---|---|
| `AAA_CHARTER.md` | SOT | Organizational charter (275 lines) |
| `SHARED_CHARTER.md` | SOT | Federation charter, 888_HOLD default |
| `REPO_ROUTING_CONSTITUTION.md` | DRAFT | Repo routing (v2026.05.02-KANON) |
| `.REPO_ROUTING_CONSTITUTION.md` | DRAFT | Hidden variant |

### 6. KNOWLEDGE_ARCHIVE (4 files)
**Purpose:** Skills library, tools reference, branch audit.

| File | Status | Key Role |
|---|---|---|
| `SKILLS_INDEX.md` | SOT | Skill registry (v2026.05.17.1, 200 lines) |
| `SKILLS.md` | REF | Skills library with 5 external resources |
| `TOOLS.md` | REF | Local tools notes |
| `ARCHIVE_BRANCHES.md` | ARCHIVED | Branch audit |

### 7. META_REPO (6 files)
**Purpose:** Repository metadata, changelog, roadmap, drafts.

| File | Status | Key Role |
|---|---|---|
| `CHANGELOG.md` | SOT | v55.5.1 (248 lines) |
| `README.md` | SOT | SOT-MANIFEST (86 lines) |
| `ROADMAP.md` | ACTIVE | Next Horizon 180-day |
| `.AGENTS.md` | ACTIVE | Hidden onboarding (999_SEAL) |
| `MIGRATIONS.md` | ARCHIVED | Migration (COMPLETED) |
| `README.DRAFT.md` | DRAFT | Draft README (405 lines) |

### 8. PERSONA (3 files)
**Purpose:** Sovereign persona, identity references.

| File | Status | Key Role |
|---|---|---|
| `CLAUDE.md` | SOT | ARIF.md Lore Protocol (999 SEAL) |
| `USER.md` | REF | About Arif |
| `AAA_OPENCLAW_SEED.md` | REF | OpenClaw seed |

### 9. WORK (1 file)
**Purpose:** Work artifacts, deliverables.

| File | Status | Key Role |
|---|---|---|
| `arif-fazil-rewrite.md` | DRAFT | Website rewrite deliverables (552 lines) |

### 10. UNCLASSIFIED / GHOST ENTRIES

| File | Note |
|---|---|
| `D4_SESAT_PROPAGATION.md` | Listed in GOVERNANCE_CONSTITUTION above as PROPOSAL |
| Duplicate KERNELPLAN/CHANGELOG entries | Table artifacts — already classified |

---

## SPECIAL CASES

### Visibility Protocol Lineage (2026-05-04)
```
agent-visibility-proposal-2026-05-04.md (PROPOSAL, Hermes ASI)
    ↓
TELEGRAM_VISIBILITY_RFC.md (DRAFT, pending ratification)
    ↓
AAA_TELEGRAM_VISIBILITY_PROTOCOL.md (SOT, SOVEREIGNLY RATIFIED, 696 lines)
    + AAA_AGENT_PROTOCOL.md (SOT, 608 lines) — different doc, also ratified same day
```

### Twin Files (likely duplicates)
- `REPO_ROUTING_CONSTITUTION.md` vs `.REPO_ROUTING_CONSTITUTION.md` — same date, same concept
- `IDENTITY.md` vs `SOUL.md` — both describe arifOS_bot session identity, same sync date

### Archived Triplets (synced workspace→main, 2026-05-11)
- `MEMORY.md`, `IDENTITY.md`, `SOUL.md` — all synced same session, all ARCHIVED

---

## STATISTICS

| Metric | Value |
|---|---|
| Total root .md files | 52 |
| SOT documents | 15 (29%) |
| ACTIVE documents | 14 (27%) |
| DRAFT documents | 7 (13%) |
| REF documents | 5 (10%) |
| ARCHIVED documents | 5 (10%) |
| PROPOSAL documents | 3 (6%) |
| Unclassified | 3 (6%) |
| Earliest doc | 000_INIT.md (2026-02-11) |
| Latest doc | AGENTS.md (2026-05-22) + CHANGELOG.md (2026-05-22) |
| Largest doc | AAA_TELEGRAM_VISIBILITY_PROTOCOL.md (696 lines) |
| Smallest doc | .REPO_ROUTING_CONSTITUTION.md (no content shown) |

---

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE** 🔥💜