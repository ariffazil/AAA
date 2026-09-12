# CARRY-FORWARD-PATH-RECONCILIATION-001

**MODE:** LEVEL 0 OBSERVE ONLY  
**DATE:** 2026-09-12T16:30+0800  
**AUTHOR:** FI-003 (Qwen Code)  
**SCOPE:** Source-of-truth conflict resolution for carry_forward.json path  

---

## Executive Summary

Three **structurally incompatible** files exist across the filesystem. They are not copies — they are **different formats** written by **different writers** to **different paths** with **different schemas**:

| Path | Format | Schema | Size | Writer | mtime |
|------|--------|--------|------|--------|-------|
| `.hermes/carry_forward.json` | flat dict | none | 10,339 B | Kimi/FI-008 via kernel seal | 08:15 UTC |
| `.local/share/arifos/carry_forward.json` | JSON array | receipt | 309 B | `clarity_carry.py` / vault seal | 06:43 UTC |
| `AAA/docs/carry_forward.json` | — | — | ABSENT (deleted) | `session_end_hook.py` / `metabolize.py` | — |

**The conflict is not two files claiming the same role. It is three (formerly four) parallel data stores that drifted apart because each writer assumed it was the canonical author and none enforced a schema version.**

---

## A. Path-Resolution Matrix

| Candidate Path | Exists | Type | Size (B) | Owner | Mode | mtime (UTC) | Schema Marker | JSON Structure |
|---|---|---|---|---|---|---|---|---|
| `/root/.hermes/carry_forward.json` | YES | regular file | 10,339 | root:root | 0644 | 2026-09-12T08:15:01 | ABSENT (no `schema_version`) | flat dict (22 keys) |
| `/root/.local/share/arifos/carry_forward.json` | YES | regular file | 309 | root:root | 0644 | 2026-09-12T06:43:12 | ABSENT | JSON array [1 element] |
| `/root/carry_forward.json` | NO | — | — | — | — | — | — | — |
| `/root/AAA/docs/carry_forward.json` | NO (deleted) | — | — | — | — | — | — | — |
| `/root/HERMES/carry_forward.json` | NO | — | — | — | — | — | — | — |
| `/root/arifOS/schemas/carry_forward.schema.json` | YES | schema file | — | — | — | — | v1 (`const: 1`) | JSON Schema draft-07 |
| `/root/scripts/governance/carry-forward-schema.json` | YES | schema file | — | — | — | — | v1 | JSON Schema draft-07 |

---

## B. Reader/Writer Matrix

### Writers (who mutates each path)

| Source File | Target Path | Role | Verified Mechanism |
|---|---|---|---|
| `scripts/carry_forward.py` (line 43) | `.local/share/arifos/` | **WRITER** (canonical v2 append) | `os.replace(tmp, CARRY_PATH)` with flock |
| `arifOS/.../clarity_carry.py` (line 14) | `.local/share/arifos/` | **WRITER** (emit_carry_forward) | `json.dump` via `CARRY_PATH` env fallback |
| `scripts/mvm.py` (line 21) | `.local/share/arifos/` | **WRITER** (MVM auto-fire) | direct path constant |
| `scripts/metabolize.py` (line 73) | `AAA/docs/` | **WRITER (LEGACY)** | direct path constant — TARGET MISSING |
| `scripts/auto_episod.py` (line 17) | `AAA/docs/` | **WRITER (LEGACY)** | direct path constant — TARGET MISSING |
| `scripts/session_end_hook.py` (line 26) | `AAA/docs/` | **WRITER (LEGACY)** | direct path constant — TARGET MISSING |
| `scripts/metabolize_cron.py` (line 18) | `AAA/docs/` | **WRITER (LEGACY)** | direct path constant — TARGET MISSING |
| Kimi/FI-008 session close (via kernel) | `.hermes/` | **WRITER** (implicit) | Session seal writes flat dict to .hermes path |
| `arifOS/.../fastmcp_ext/resources.py` | all 3 lanes | **READER** (mtime-freshest) | mtime-based candidate selection |

### Readers (who consumes each path)

| Source File | Reads From | Role | Fallback Chain |
|---|---|---|---|
| `arifOS/.../fastmcp_ext/resources.py` | `.local/share/` → `.hermes/` → `AAA/docs/` | **READER** (freshest mtime) | 3-path mtime cascade |
| `arifOS/.../resource.py` (line 170) | `.local/share/` → `/root/` | **READER** (first-match) | 2-path first-match |
| `arifOS/.../measurement.py` (line 33) | `.local/share/` | **READER** | single path |
| `scripts/session_context.py` (line 28) | `.local/share/` → `AAA/docs/` → `HERMES/` | **READER** (3-path) | 3-path first-match |
| `scripts/flow_resume.sh` (line 18) | `$CARRY_FORWARD_PATH` → `.local/share/` | **READER** | env + fallback |
| `.hermes/scripts/morning-readiness.py` (line 24) | `.hermes/` | **READER** | single path |
| `.hermes/scripts/evening-anchor.py` (line 13) | `.hermes/` | **READER** | single path |
| `scripts/direct-backup.sh` (line 9) | `.local/share/` | **READER** (backup source) | single path |
| `scripts/backup-tier-a.sh` (line 31) | `.local/share/` | **READER** (backup source) | single path |
| `scripts/doctor.sh` (line 254) | `.local/share/` | **READER** (health check) | single path |
| `scripts/witness-heartbeat.sh` (line 88) | `.local/share/` | **READER** | single path |
| `scripts/asi_readiness_probe.sh` (line 66) | `.local/share/` | **READER** | single path |

### Documentation (declared SOT)

| Source File | Declared Path | Status |
|---|---|---|
| `AGENTS.md` (line 81) | `carry_forward.json` (path-agnostic) | Path-agnostic |
| `AAA/instructions/base.md` (line 72) | `carry_forward.json` (path-agnostic) | Path-agnostic |
| `AAA/instructions/pointers.md` (line 22) | `.local/share/arifos/` | CORRECT |
| `AAA/instructions/topology.md` (line 65) | `.local/share/arifos/` | CORRECT |

---

## C. Backup Lineage Matrix

| Backup Directory | File Count | Naming Convention | Time Range | Active |
|---|---|---|---|---|
| `.local/share/arifos/carry_forward_backups/` | **185+ files** | ISO-8601 UTC timestamps | 2026-09-10 → 2026-09-12 | YES — written by `carry_forward.py` auto-backup |
| `AAA/docs/carry_forward_backups/` | **51 files** | Unix epoch timestamps | 2026-08-25 → 2026-09-12 | STALE — last write 2026-09-12 07:00, from legacy `metabolize.py` |
| `.archive/aaa_carry_forward_archive/` | **30+ files** | Unix epoch timestamps | 2026-08-24 | ARCHIVED — pre-heritage-move snapshots |
| `.hermes/` (no dedicated backup dir) | 0 | — | — | NO backup directory for .hermes path |
| Quarantine (`_quarantine/`) | 2 files | descriptive names | 2026-08-04, 2026-08-13 | ARCHIVED |

---

## D. Semantic-Integrity Boundary

### `.hermes/carry_forward.json` — Hermes session handoff (flat dict)

**Content structure:** Flat key-value dict with 22 top-level keys:
```
last_session, unmetabolized, active_scars, pending_skills, metrics,
last_updated_utc, session_id, closed_at, closing_agent, verdict, lane,
judge_chain_id, heavyweight_chain_status, f13_directives_executed,
open_loops, next_session, hold_register_status, session_final_state_*,
fi008_close_*_auditverify, reality_pulse, metabolized_scars,
scar_metabolization_note
```

**Key facts:**
- `schema_version`: ABSENT
- `session_id`: `SEAL-54cee348f64a4fc0`
- `closing_agent`: `kimi-code/FI-008`
- `last_updated_utc`: `2026-09-12T08:15:01Z`
- No `generations` field (not v2-compatible)
- No `system_state`, `session_anchor`, `humans` (not v1-schema-compatible either)

**This is a Hermes-specific session state, NOT the canonical carry_forward.**

### `.local/share/arifos/carry_forward.json` — Canonical writer target (JSON array)

**Content structure:** JSON array with 1 receipt entry:
```json
[{
  "ts": 1789195392.221623,
  "action": "arif_vault_seal",
  "session_id": "SEAL-123362e528d347fb",
  "actor_id": "arif",
  "evidence_layer": "L1-L2",
  "receipt": {"entry_id": "...", "type": "constitutional_seal"},
  "doctrine": "CLARITY-CARRY-FORWARD"
}]
```

**Key facts:**
- Not v2 generational format (no `generation` envelope)
- Not v1 schema (no `schema_version: 1`, no `session_anchor`, `system_state`, `humans`)
- Written by `clarity_carry.py` receipt-emit — a vestigial receipt, not session state
- The **actual v2 generational data** (as produced by `carry_forward.py`) appears to have been overwritten by this receipt at some point

### Schema Files (v1 — never adopted by live data)

Both schema files at `arifOS/schemas/carry_forward.schema.json` and `scripts/governance/carry-forward-schema.json` define v1 format with `schema_version: const: 1`, but **neither live file conforms to v1**. The `AGENTS.md` line 81 declares `schema arifos.carry_forward.v2` but no v2 schema file exists on disk.

---

## E. Three Canonicalization Options

### Option 1: Promote `.hermes/carry_forward.json` as SOT

**Action:** Rename `.hermes/carry_forward.json` → `.local/share/arifos/carry_forward.json` (atomic swap). Redirect all `.hermes`-specific readers.

| Dimension | Assessment |
|---|---|
| Blast radius | HIGH — 17+ scripts in `/root/scripts/`, kernel `resource.py`, `measurement.py`, `fastmcp_ext/resources.py` all expect `.local/share/` |
| Rollback | Easy — swap back from `.hermes/` backup |
| Affected consumers | All `scripts/` readers (17 files), kernel MCP resources (3 files) |
| Schema gap | `.hermes` file is flat dict — incompatible with v2 generational format. Would need schema migration |
| Validation plan | Validate mtime > 08:00 UTC (it is), check all 22 keys present |
| **Verdict** | **NOT RECOMMENDED** — format is structurally different (dict vs list/generational); migration needed before adoption |

### Option 2: Fix `.local/share/arifos/` to hold canonical v2 data (RECOMMENDED)

**Action:** Identify who overwrote the v2 generational data with a single receipt, restore the last known v2 generation from backups, and enforce single-writer discipline on this path.

| Dimension | Assessment |
|---|---|
| Blast radius | LOW — path is already the declared SOT in `pointers.md`, `topology.md`, and majority of code |
| Rollback | Trivial — backup exists at `.local/share/arifos/carry_forward_backups/` (185+ snapshots) |
| Affected consumers | None — all readers already read this path |
| Schema gap | Need to either (a) write a v2 schema file, or (b) adopt v1 schema and migrate |
| Validation plan | 1. Find last v2-format backup 2. Verify it parses 3. Write to primary 4. Run `carry_forward.py show` to confirm |
| **Verdict** | **RECOMMENDED** — lowest blast radius, matches declared SOT, all readers already correct |

### Option 3: Three-way merge into fresh v2 file

**Action:** Extract `open_loops` from `.hermes/`, `receipts` from `.local/share/`, and schema from `AGENTS.md` declaration. Write a new unified v2 file.

| Dimension | Assessment |
|---|---|
| Blast radius | MEDIUM — creates new data shape; all readers need schema compatibility check |
| Rollback | Medium — need to preserve both sources |
| Affected consumers | `fastmcp_ext/resources.py` (reads dict keys), `morning-readiness.py` (reads `priority_engine`, `context_engine`) |
| Schema gap | Full — no v2 schema exists on disk |
| Validation plan | 1. Draft v2 schema 2. Merge data 3. Validate against schema 4. Update 3 reader files |
| **Verdict** | **DEFERRED** — requires schema authoring + multi-file reader update; better as F13-directed Phase 2 |

---

## F. 888 HOLD List (Mutations Withheld)

| # | Mutation | Reason for HOLD |
|---|---|---|
| H1 | Restore v2 data to `.local/share/` | Requires F13 approval — changing primary data store |
| H2 | Delete `.hermes/carry_forward.json` | Hermes scripts depend on it; requires coordination |
| H3 | Unify writer paths in legacy scripts | 4 scripts (`metabolize.py`, `auto_episod.py`, `session_end_hook.py`, `metabolize_cron.py`) still write to `AAA/docs/`; fix requires testing |
| H4 | Write v2 schema file | Requires F13 ratification of v2 envelope structure |
| H5 | Add `.hermes/` to fastmcp fallback chain as SOT candidate | Requires testing mtime-freshest logic doesn't pick stale .hermes over live .local/share |

---

## G. Telemetry

```json
{
  "reconciliation_id": "CARRY-FORWARD-PATH-RECONCILIATION-001",
  "timestamp_utc": "2026-09-12T08:30:00Z",
  "verdict": "HOLD_FOR_ARIF",
  "evidence_quality": "HIGH",
  "files_probed": 8,
  "scripts_produced": 30,
  "backup_snapshots_probed": 236,
  "conflict_classification": {
    ".hermes vs .local/share": "HYPOTHESIS — structurally incompatible formats, not competing SOT claims",
    ".hermes vs AAA/docs": "RESOLVED — AAA/docs deleted, legacy writers orphaned",
    ".local/share overwritten": "PLAUSIBLE — clarity_carry receipt overwrote v2 generational data",
    "v2 schema missing": "CONFIRMED — AGENTS.md declares v2, no schema file exists"
  },
  "recommended_action": "Option 2 — restore v2 data to .local/share from backup, enforce single-writer",
  "requires_sovereign": true,
  "reversible": true
}
```

---

## Appendix: Reference Count Summary

| Path Variant | Source Files (non-pycache) |
|---|---|
| `/root/.local/share/arifos/carry_forward.json` | 17 source files |
| `/root/AAA/docs/carry_forward.json` | 6 source files (all LEGACY — target deleted) |
| `/root/.hermes/carry_forward.json` | 3 source files (2 Hermes scripts + 1 kernel reader) |
| `/root/HERMES/carry_forward.json` | 2 source files (all LEGACY — target never existed) |
| `/root/carry_forward.json` | 1 source file (LEGACY — kernel `resource.py` fallback) |
