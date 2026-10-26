# ACD Component Inventory — Phase 111/222

**Date:** 2026-09-12 | **Probe:** FI-003 (Qwen Code) | **Repo:** /root/AAA (main, cb86b729)

## Repository Identity

| Field | Value |
|-------|-------|
| Path | /root/AAA |
| Branch | main |
| HEAD | cb86b729 — docs(dream): G3a reconciliation |
| Remote | github.com/ariffazil/AAA.git |
| Dirty files | 8 |
| ACD/ target | DOES NOT EXIST (to be created) |

## Component Inventory

### TIER 1 — RUNTIME PRESENT + EVIDENCE

| ID | Component | Path | Type | Status | Evidence |
|----|-----------|------|------|--------|----------|
| C01 | dream_engine.py (consolidate) | /root/AAA/engines/dream_engine.py | RUNTIME | 9 runs in last_dream.json (2026-08-21 → 2026-09-09) | last_dream.json |
| C02 | consolidate.py symlink | /root/AAA/dreams/consolidate.py → C01 | ADAPTER | Points to C01 | symlink verified |
| C03 | arif-dream.timer | systemd | SCHEDULE | ENABLED + ACTIVE | systemctl |
| C04 | golden_dreams.py | /root/AAA/dream_engine/tests/ | TEST | Syntax-checked, imports C01 | file exists |
| C05 | last_dream.json | /root/AAA/dream_engine/state/ | STATE | 9 consolidated runs, latest 2026-09-09 | file content |

### TIER 2 — DOCTRINE PRESENT, RUNTIME UNCERTAIN

| ID | Component | Path | Type | Status | Evidence |
|----|-----------|------|------|--------|----------|
| C06 | AGI-dream-engine SKILL.md | /root/AAA/skills/AGI-dream-engine/ | DOCTRINE | 325 lines, 4-phase plan | file exists |
| C07 | DESIGN.md | /root/AAA/dream_engine/DESIGN.md | DOCTRINE | Engineering spec | file exists |
| C08 | dream-555-ASI agent card | /root/AAA/agent-cards/agents/dream-555-ASI.json | SCHEMA | REVIEW + AUDIT role deeds | file exists |
| C09 | AIO-DOCTRINE.md | /root/AAA/governance/aio/ | DOCTRINE | AIO as separate organ | file exists |
| C10 | adaptation-receipt.schema.json | /root/AAA/governance/aio/ | SCHEMA | JSON Schema for adaptation receipts | file exists |
| C11 | G0-A packets (v1+v2) | /root/AAA/governance/aio/ | DOCTRINE | APEX normalization | files exist |
| C12 | distill.py | /root/AAA/dream-engine/ | RUNTIME | 6659 bytes, different from C01 | needs probe |
| C13 | wisdom.md | /root/AAA/knowledge-graph/dream-engine/ | STATE | Output artifact | file exists |
| C14 | dream-federation reports | /root/AAA/reports/dream-federation-2026-09-12/ | DOCTRINE | 4 reports from today's session | files exist |

### TIER 3 — STUB / ORPHANED / DANGLING

| ID | Component | Path | Type | Status | Evidence |
|----|-----------|------|------|--------|----------|
| C15 | auto-dream-spool.ts | /root/A-FORGE/scripts/ | STUB | Hollow — always writes proposals: [] | code inspection |
| C16 | dreamer-crucible.py | /root/A-FORGE/forge_work/2026-07-25/ | ARCHIVE | v2.0-crucible, forge work | file exists |
| C17 | dreamer.py (honcho) | /root/A-FORGE/forge_work/2026-07-25-honcho-pilot/ | ARCHIVE | v1.0.0 honcho pilot | file exists |
| C18 | /var/spool/arifos/dream-proposals/ | filesystem | STUB | Empty since 2026-07-25 | ls verified |
| C19 | dream-engine-monthly.timer | systemd | DANGLING | DISABLED, not-found | systemctl |
| C20 | dream-engine-weekly.timer | systemd | DANGLING | DISABLED, not-found | systemctl |
| C21 | arif-dream.service | systemd | DANGLING | DISABLED, not-found | systemctl |
| C22 | DREAMMODE_BLUEPRINT.md | /root/AAA/archive/2026-07-25/ | ARCHIVE | Historical | file exists |
| C23 | 2026-06-07-dream-engine-forged.md | /root/AAA/memory/ | STATE | Historical memory | file exists |

### TIER 4 — DUPLICATES / COPIES

| ID | Component | Path | Type | Status |
|----|-----------|------|------|--------|
| C24 | AGI-dream-engine (Hermes profile) | /root/.hermes/profiles/aaa-hermes/skills/ | COPY | 3 systemd unit copies |
| C25 | AGI-dream-engine (router-test) | /root/.hermes/profiles/router-test/skills/ | COPY | 3 systemd unit copies |
| C26 | AGI-dream-engine (global) | /root/.hermes/skills/ | COPY | 3 systemd unit copies |
| C27 | auto-dream-spool.js (compiled) | /root/A-FORGE/dist/scripts/ | COMPILED | JS output of C15 |
| C28 | rollback copies | /root/A-FORGE/deploy/rollback/ | ARCHIVE | 2 rollback snapshots of C15 |

## Critical Correction (vs earlier G3a probe)

**Earlier claim:** "Dream engine runtime ABSENT — scripts don't exist, systemd units dangling"

**Actual finding:** The **consolidation runtime IS present and HAS run successfully 9 times** (C01+C03+C05). What was absent was the **possibility generation** path (the "dream" = counterfactual exploration that ACD defines). The two functions are:

| Function | Component | Status |
|----------|-----------|--------|
| Memory consolidation (L1-L5 metabolism) | C01 dream_engine.py + C03 timer | PRESENT, 9 runs |
| Possibility generation (counterfactual search) | Not built | ABSENT |

**ACD targets the possibility generation gap.** The consolidation runtime is complementary — it handles memory metabolism; ACD handles future simulation.

## Map–Territory Contradictions

| # | Map (what docs say) | Territory (what exists) | Severity |
|---|---------------------|------------------------|----------|
| 1 | "Dream engine absent" (G3a probe) | Consolidation runtime HAS run 9 times | HIGH — earlier probe was wrong |
| 2 | auto-dream-spool.ts "reads Supabase" | Always writes proposals: [] | HIGH — stub |
| 3 | arif-dream.service "runs the engine" | DISABLED, not-found | MEDIUM — dangling |
| 4 | AIO "adaptation organ" | 3 files, 0 execution cycles | HIGH — doctrine only |
| 5 | SKILL.md "4-phase plan" | Phase 0-2 have no runtime | MEDIUM — plan not code |
| 6 | dream-555-ASI "intelligence principal" | Agent card only, no runtime | LOW — registration |

## Proposed Disposition

| ID | Disposition | Reason |
|----|-------------|--------|
| C01-C05 | ADOPT | Working consolidation runtime — integrate as ACD.memory_metabolism |
| C06 | ADOPT | Doctrine is canonical — rename to ACD/CONSTITUTION.md |
| C07 | ADAPT | Engineering spec — merge into ACD/ARCHITECTURE.md |
| C08 | ADOPT | Agent card — update to ACD identity |
| C09-C11 | REFERENCE | AIO is separate organ — keep as-is, document boundary |
| C12 | UNKNOWN | Needs runtime probe — different from C01 |
| C13 | ADOPT | Output artifact — move to ACD/receipts/ |
| C14 | ADOPT | Today's reports — move to ACD/forensics/ |
| C15 | DEPRECATE_WITH_SHIM | Hollow stub — replace with ACD adapter |
| C16-C17 | ARCHIVE_CANDIDATE | Historical forge work |
| C18 | ADOPT | Spool dir — becomes ACD inbox |
| C19-C21 | DEPRECATE | Dangling units — record and remove |
| C22-C23 | ARCHIVE_CANDIDATE | Historical |
| C24-C28 | DEPRECATE | Duplicates — canonical is C06 |
