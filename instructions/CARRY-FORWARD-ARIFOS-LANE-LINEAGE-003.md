# CARRY-FORWARD-ARIFOS-LANE-LINEAGE-003

**MODE:** LEVEL 0 OBSERVE ONLY
**DATE:** 2026-09-12T14:50:00+08:00
**SCOPE:** arifOS-lane (`/root/.local/share/arifos/carry_forward.json`), declared schemas, writer/reader source code, local git history, and backup lineage.
**VERDICT:** HOLD_FOR_ARIF

---

## 1. Current-Object Forensic Record

| Field | Value |
|-------|-------|
| **Path** | `/root/.local/share/arifos/carry_forward.json` |
| **Inode** | 1564826 |
| **Permissions** | 0644 (rw-r--r--) |
| **Owner** | root:root |
| **Size** | 309 bytes |
| **Birth** | 2026-09-12T06:43:12.221Z UTC (14:43 MYT) |
| **Mtime** | 2026-09-12T06:43:12.221Z UTC |
| **Ctime** | 2026-09-12T06:43:12.221Z UTC |
| **SHA-256** | `4be7792343b5d7008c826b491d19c85a9eb94eafa3a0ab57ad88a3cff033b785` |
| **JSON type** | `list` (array) |
| **Array length** | 1 |
| **Entry keys** | `ts`, `action`, `session_id`, `actor_id`, `evidence_layer`, `receipt`, `doctrine` |

### Single entry content
```json
{
  "ts": 1789195392.221623,
  "action": "arif_vault_seal",
  "session_id": "SEAL-123362e528d347fb",
  "actor_id": "arif",
  "evidence_layer": "L1-L2",
  "receipt": {
    "entry_id": "ea7ec17618e7498b",
    "type": "constitutional_seal"
  },
  "doctrine": "CLARITY-CARRY-FORWARD"
}
```

**Observation:** This is a receipt-stream entry, NOT a generational object. The v2 schema expects a dict with `schema`, `generation`, `sessions`, `open_loops` keys. The v1 schema expects a dict with `session_id`, `open_loops`, `active_scars`, etc. This file has none of those — it is a receipt array.

---

## 2. Producer Contract

### Active writer: `clarity_carry.py`

**Path:** `/root/arifOS/arifosmcp/runtime/clarity_carry.py`
**Function:** `emit_carry_forward(action, session_id, actor_id, evidence_layer, receipt)`
**Called from:** `/root/arifOS/arifosmcp/runtime/tools.py` (line ~20591), during the kernel seal flow (`arif_seal` → `emit_carry_forward`).

**Serialization behavior:**
1. Reads existing file as `json.load(f)` → expects list
2. If not a list: `data = []` (RECOVERY MODE — **silently discards non-list contents**)
3. Appends one receipt entry
4. Trims to `data[-50:]` (last 50 entries)
5. Atomic write: tmp file → `os.replace()` (same filesystem)
6. Backup: copies trimmed array to `carry_forward_backups/carry_forward-{stamp}-{session_id[:8]}.json`

**Critical flaw:** On line 42–43:
```python
data = json.load(f)
if not isinstance(data, list):
    data = []  # corrupted — recover
```
This means when `clarity_carry.py` encounters a v1 object (dict), it **silently discards the entire v1 state** and starts fresh as an empty list. The v1 content is not preserved anywhere — the backup written AFTER the discard contains only the new receipt, not the original object.

**Last write event:** 2026-09-12T06:43:12Z UTC, triggered by `arif_seal` action with session `SEAL-123362e528d347fb`.

### Secondary writer: `carry_forward.py` (v2 writer)

**Path:** `/root/scripts/carry_forward.py`
**Schema:** `arifos.carry_forward.v2`
**Behavior:** Uses `CarryLock` (flock), atomic tmp→replace, backup-on-write. Writes a proper v2 object with `schema`, `generation`, `sessions`, `open_loops`.
**Status:** The v2 writer was NEVER applied to the current file. The current file has no `schema` key. Running `carry_forward.py migrate` would produce a valid v2 object but would also lose the current receipt data.

### Other writers to this path

| Writer | Path | Writes to SOT? | Backup pattern |
|--------|------|----------------|----------------|
| `mvm.py` | `/root/scripts/mvm.py` | Yes (dict mode) | `cf_{timestamp}.json` |
| `clarity_carry.py` | `/root/arifOS/arifosmcp/runtime/clarity_carry.py` | Yes (array mode) | `carry_forward-{stamp}-{sid[:8]}.json` |
| `carry_forward.py` | `/root/scripts/carry_forward.py` | Yes (dict mode, v2) | `carry_forward_{ts}_{tag}.json` |

### Mystery writer: `carry_forward_YYYYMMDDTHHMMSSZ.json` backups

241 backup files with the pattern `carry_forward_YYYYMMDDTHHMMSSZ.json` (10339B each, v1 objects with 8 open_loops) continue to be written every 15 minutes, including AFTER the overwrite at 06:43. The cron `p0_metabolize_traces.py` (*/15) + `reexamine.py` run at the right intervals but write to `/root/AAA/docs/carry_forward.json` (AAA lane), not the arifOS lane. The exact script producing these backups could not be identified with certainty. Candidates:
- A hidden/systemd-triggered script not in the grep scope
- The `fq-probe.service` (loaded but inactive) or a process spawned by it
- A lingering background process from a prior session

**The 10339B v1 backups written after the overwrite are themselves evidence of an unexplained phenomenon** — the arifOS SOT file should be 309B (array) yet a writer is creating 10339B v1-object backups from the same path.

---

## 3. Consumer Contract

### Consumer inventory

| Consumer | Path | Expected shape | Required keys | Failure behavior | Current parse result |
|----------|------|----------------|---------------|------------------|---------------------|
| **A-FORGE aed.py** | `/root/A-FORGE/duties/aed.py` | dict | `open_loops` or `open_loops_888_HOLD` | Empty list fallback | `[]` (no loops) — FUNCTIONALLY DEGRADED |
| **session_context.py** | `/root/scripts/session_context.py` | dict | `active_scars`, `open_loops`, `metrics` | Empty dicts | Empty — NO SCARS, NO LOOPS, NO METRICS |
| **fastmcp_ext/resources.py** | `/root/arifOS/arifosmcp/runtime/fastmcp_ext/resources.py` | dict (decorated with `_served_from`) | Any | Falls back to raw | Serves raw array with metadata |
| **validate-carry-forward.py** | `/root/scripts/governance/validate-carry-forward.py` | dict with specific fields | `session_id`, `actor`, `open_loops_888_HOLD`, `carry_forward` | Exit 1 (INVALID) | **FAILS VALIDATION** |
| **validate_carry_forward.py** | `/root/arifOS/scripts/validate_carry_forward.py` | dict | `schema_version` | Exit 3 (schema not found) | **CANNOT VALIDATE** (schema file missing) |
| **flow_resume.sh** | `/root/arifOS/scripts/flow_resume.sh` | dict (json.loads) | N/A | Returns raw | Passes array to Python merge — may crash |
| **witness-heartbeat.sh** | `/root/scripts/witness-heartbeat.sh` | File existence + age | N/A | Reports age | Reports age of 8h (functional) |
| **generate-session-briefing.sh** | `/root/AAA/scripts/generate-session-briefing.sh` | dict | `session_id`, `open_loops` | UNKNOWN | `session_id` = null, loops empty |
| **graphiti_boot_context.py** | `/root/AAA/graphiti/graphiti_boot_context.py` | dict | N/A | Returns `{"_note": "no carry_forward.json found"}` | Would parse array, merge into boot context |
| **j-continuity.js** | `/root/AAA/a2a-server/j-continuity.js` | dict | `jacobian_state` | Console warn | Load failed — Jacobian state lost |
| **metabolize_cron.py** | `/root/scripts/metabolize_cron.py` | dict | `unmetabolized`, `pending_skills` | Returns empty | Empty pending — cron thinks nothing to metabolize |
| **scar_pressure_runtime.py** | `/root/scripts/scar_pressure_runtime.py` | dict | N/A | Hardcoded string | N/A (only references carry_forward as source) |
| **mvm_consume.py** | `/root/scripts/mvm_consume.py` | dict | `validated_capabilities` | N/A | Empty — consumes nothing |
| **metabolize.py** | `/root/scripts/metabolize.py` | dict | `carry_forward` key | N/A | Writes to AAA lane, reads from AAA lane |

### Damage assessment

**Active degradation (consumers reading arifOS-lane file and getting wrong shape):**
1. `session_context.py` → returns empty governance context (no scars, no loops, no metrics)
2. `aed.py` → no open loops to classify (309B array has no `open_loops` key)
3. `validate-carry-forward.py` → EXIT 1 (schema violation)
4. `generate-session-briefing.sh` → empty briefing
5. `j-continuity.js` → Jacobian state lost (fresh start every session)

**Graceful degradation (consumers that handle missing keys or catch errors):**
- `fastmcp_ext/resources.py` → serves raw content with metadata
- `witness-heartbeat.sh` → reports age (functional)
- `graphiti_boot_context.py` → graceful fallback

**Self-healing observation:** The `fastmcp_ext/resources.py` resource selector picks the FRESHEST file across 3 lanes (arifOS, Hermes, AAA). Since the Hermes lane (10339B) is newer than the arifOS lane (309B), agents booting via `arifos://carry-forward` MCP resource may actually get the Hermes-lane v1 object instead of the arifOS-lane receipt array. This partially masks the corruption for MCP-connected agents.

---

## 4. Schema Archaeology

### Schema versions

| Version | Identifier | Defined in | Status |
|---------|-----------|------------|--------|
| v0 | (pre-schema) | Original carry_forward.json | Superseded by v1 migration |
| v1 | `arifos.carry_forward.v1` | `/root/arifOS/scripts/validate_carry_forward.py` | ACTIVE in backup chain; schema file at `/root/arifOS/schema/carry_forward.schema.json` is MISSING |
| v2 | `arifos.carry_forward.v2` | `/root/scripts/carry_forward.py` line 45 | LIVE code, never applied to current file |

### Schema archaeology detail

**v1 schema:** The validation script at `/root/arifOS/scripts/validate_carry_forward.py` references `SCHEMA_PATH = Path(__file__).parent.parent / "schema" / "carry_forward.schema.json"`. This file does NOT exist on disk (`/root/arifOS/schema/` directory is empty or absent). The validator would exit code 3 (schema not found) even if the file were v1.

**v1 → v2 migration:** `/root/scripts/carry_forward.py migrate` was designed for this transition. It would:
1. Create a v2 wrapper around the v1 data (preserving under `carried_v1`)
2. Extract sessions and open_loops
3. Write with flock + backup

**Current file status:** Neither v1 nor v2. It is a receipt-stream array produced by `clarity_carry.py`, which was written without consulting either schema.

**The governance validator** at `/root/scripts/governance/validate-carry-forward.py` references `/root/scripts/governance/carry-forward-schema.json`. This file also does not exist on disk (ls showed empty). The validator falls back to basic structural checks, which the current file fails (requires `session_id`, `actor`, `open_loops_888_HOLD`, `carry_forward` as top-level keys).

---

## 5. Backup Lineage

### Backup streams identified

**Stream A: `carry_forward_backups/` directory (arifOS lane)**
Contains backups from at least 3 different writers:

| Pattern | Writer | Example | Shape |
|---------|--------|---------|-------|
| `carry_forward-{stamp}-{sid[:8]}.json` | clarity_carry.py | `carry_forward-20260912T064312Z-SEAL-123.json` | array(1), 309B |
| `carry_forward_{ts}_{tag}.json` | carry_forward.py (v2) | `cf-pre-seal-20260911T034716Z.json` | object(schema=v1), 18198B |
| `carry_forward_YYYYMMDDTHHMMSSZ.json` | UNKNOWN (mystery writer) | `carry_forward_20260912T064502Z.json` | object(MISSING schema), 10339B |

**Stream B: restic backups** (via `/root/scripts/direct-backup.sh`)
The live file is included in Tier-A restic backups. These are point-in-time snapshots; the most recent restic snapshot would contain the 309B receipt array.

**Stream C: `/root/.archive/aaa_carry_forward_archive/`**
Historical archive containing 19 files with epoch-based naming (`carry_forward_1787667527.json` etc.). These are all from the pre-v1 era (epoch ~178766xxxx = ~2026-08-25).

### Backup chain analysis (chronological, most recent)

| # | Timestamp (UTC) | Size | Shape | Filename | Source |
|---|-----------------|------|-------|----------|--------|
| 232 | 2026-09-12T06:30:02Z | 10339B | object(loops=8) | carry_forward_20260912T063002Z.json | Mystery writer |
| **233** | **2026-09-12T06:43:12Z** | **309B** | **array(1)** | **carry_forward-20260912T064312Z-SEAL-123.json** | **clarity_carry.py** |
| 234 | 2026-09-12T06:45:02Z | 10339B | object(loops=8) | carry_forward_20260912T064502Z.json | Mystery writer |
| ... | every 15 min | 10339B | object(loops=8) | ... | Mystery writer |
| 241 | 2026-09-12T08:15:01Z | 10339B | object(loops=8) | carry_forward_20260912T081501Z.json | Mystery writer |

**Key observation:** Entry #233 (the clarity_carry backup) is the ONLY array-shaped backup in the entire chain. Every other backup is a v1 object. The mystery writer continues to create v1-object backups at 15-minute intervals regardless of the live file state.

### Pre-overwrite predecessor

**File:** `cf-pre-seal-20260911T034716Z.json`
- **Size:** 18198 bytes
- **Shape:** v1 object (`schema: arifos.carry_forward.v1`)
- **Keys:** 22 top-level keys including `session_id`, `open_loops`, `active_scars`, `witness_chain`, `eurekas_sealed_tonight`, `scar_research_sealed`, `hermes_memory_audit_2026-09-10`, `four_layer_split_doctrine`, `seal_outcome_2026_09_11`
- **Session ID:** `session-2026-09-11-kimi-layer0-compile-execute-seal`
- **Open loops:** 8 items
- **Timestamps:** `compiled_at_utc: 2026-09-11T03:45:00Z`
- **Content density:** Extensive — contains 5-era model, HARAM canonical list, compression doctrine, 4-layer split doctrine, Jacobian state, and more

### The 10339B "post-overwrite" backups

The 9 backups from 06:45 to 08:15 UTC (after the overwrite) are ALL 10339B v1 objects with:
- 8 open_loops
- `last_session: session-20260912_084001_f2068a8c`
- `session_id: SEAL-54cee348f64a4fc0`
- Keys: `active_scars`, `closed_at`, `closing_agent`, `hold_register_status`, `judge_chain_id`, `lane`, `metrics`, `next_session`, `pending_skills`, `reality_pulse`, `verdict`, etc.
- No `schema` key (neither v1 nor v2)

These represent a DIFFERENT v1 variant from the predecessor (which had `schema: arifos.carry_forward.v1`). The post-overwrite backups lack the `schema` key and have different field names (e.g., `session_final_state_20260912` vs `completed_tonight`). This suggests a separate writer maintaining a separate v1-format state that is NOT the original pre-overwrite file.

---

## 6. Continuity Test

### Monotonic session IDs/timestamps
**FAIL.** The predecessor had `session_id: session-2026-09-11-kimi-layer0-compile-execute-seal`. The current file has `session_id: SEAL-123362e528d347fb`. The mystery v1 backups have `session_id: SEAL-54cee348f64a4fc0`. Three different session IDs, no continuity.

### Append continuity
**FAIL.** The predecessor was an 18KB v1 object. The current file is a 309B receipt array. The mystery v1 backups are 10KB objects. No monotonic append chain exists across these shapes.

### Expected retention/compaction behavior
**AMBIGUOUS.** `clarity_carry.py` trims to last 50 entries. If this writer were the only writer, the file would accumulate up to 50 receipts. But the file currently has only 1 entry — either this was the first call since the overwrite, or compaction occurred.

### Unexplained field-type changes
**PRESENT.** The file changed from:
- **dict** (v1 object, 18KB, 22 keys, 8+ open_loops) → **list** (receipt array, 309B, 1 entry)

This is a type-level discontinuity (dict → list), not a field-level change.

### Evidence of truncation or format switching
**PRESENT.** The 309B file is consistent with a fresh-start scenario: `clarity_carry.py` read the old v1 dict, silently discarded it (`data = []`), appended 1 receipt, and wrote. No truncation in the traditional sense — the old data was overwritten atomically.

### Continuity test result

```
PROBABLE_OVERWRITE
```

**Rationale:** The file is a receipt-stream array (dict→list type change), the overwrite moment is precisely timestamped (birth=mtime=06:43:12Z), the producing agent (`clarity_carry.py` via `arif_seal`) is identified, and the mechanism (`json.load` on non-list → discard) is confirmed in source code. The only uncertainty is whether the overwrite was intentional (arif_seal emitting a receipt) or accidental (clarity_carry.py being called when it shouldn't have been).

---

## 7. Repair Readiness (Not Repair)

### Diagnosis

**Root cause:** `clarity_carry.py`'s `emit_carry_forward()` treats the carry_forward file as a receipt list. When called after `arif_seal`, it reads the existing v1 dict, fails `isinstance(data, list)`, silently discards the v1 content, and writes a 1-element receipt array. This is a **format war** between two writers that assume incompatible shapes.

**Two competing contracts:**
1. **Receipt-stream contract** (clarity_carry.py): `carry_forward.json` = array of action receipts, last 50 retained
2. **Generational contract** (carry_forward.py, v1 schema, all consumers): `carry_forward.json` = object with session state, open loops, scars, metrics

These contracts are mutually exclusive. The current file satisfies only contract #1. All consumers expect contract #2.

### Candidate restoration source

| Source | File | Size | Shape | Confidence |
|--------|------|------|-------|------------|
| Mystery v1 backup (most recent) | `carry_forward_20260912T081501Z.json` | 10339B | v1 object (no schema key), 8 loops | MEDIUM — different v1 variant from predecessor |
| Pre-seal backup | `cf-pre-seal-20260911T034716Z.json` | 18198B | v1 object (schema=v1), 15 loops | HIGH — last known good state before any overwrite |
| Hermes lane | `/root/.hermes/carry_forward.json` | 10339B | v1 object (no schema key), 8 loops | LOW — separate lane, not the arifOS SOT |

### Proposed restore method (NOT executing)

**Option A — Restore from predecessor backup (recommended):**
1. Source: `cf-pre-seal-20260911T034716Z.json` (18198B, v1 with schema)
2. Target: `/root/.local/share/arifos/carry_forward.json`
3. Method: `cp` (preserves atomicity; no need for tmp+replace since file is small)
4. Rollback: Current 309B file saved to `carry_forward_rollback_309B_20260912.json`
5. Verification: `python3 /root/scripts/governance/validate-carry-forward.py` (will fail due to missing schema file, but basic structural check should pass)

**Option B — Let the mystery writer self-heal:**
The mystery writer appears to be maintaining a v1-format copy and writing backups every 15 minutes. If this writer also writes to the live file (not just backups), the file may self-heal. Risk: this relies on an unidentified process.

**Option C — Apply v2 migration:**
Run `carry_forward.py migrate` which would:
1. Read current array as v1 (it's not v1, so it would treat it as generic v1 and wrap it)
2. Produce a v2 object with the single receipt under `carried_v1`
3. Lose the receipt as a useful record

This is NOT recommended because the 309B receipt array is NOT a valid v1 object — the migration would produce a semantically empty v2.

### Affected services (if restored)

- `session_context.py` → would resume returning scars/loops/metrics
- `aed.py` → would resume classifying open loops
- `j-continuity.js` → Jacobian state would be restored
- `fastmcp_ext/resources.py` → would serve restored v1 object
- `metabolize_cron.py` → would resume detecting pending items

### Human approval text

> The arifOS-lane carry_forward.json (309B receipt array) was overwritten by clarity_carry.py during an arif_seal action at 2026-09-12T06:43:12 UTC. The previous state was a v1 generational object (18KB, 8+ open_loops, extensive session history). The overwrite mechanism is clarity_carry.py's `emit_carry_forward()` which silently discards non-list contents. All consumers of the file expect a v1/v2 object, not a receipt array.
>
> A pre-seal backup exists at `carry_forward_backups/cf-pre-seal-20260911T034716Z.json` (18KB, v1 with schema). This is the strongest restoration candidate.
>
> **Recommendation:** Restore the v1 object from the pre-seal backup, then apply `carry_forward.py migrate` to upgrade to v2 (which adds flock collision protection). This closes the two-writer race by making `carry_forward.py` the sole writer.
>
> **Does Arif approve restoration from the pre-seal backup?**

---

## Continuity Test Result

```
PROBABLE_OVERWRITE
```

Evidence:
1. Type-level discontinuity: dict (v1 object) → list (receipt array)
2. Overwrite timestamp precisely identified: 2026-09-12T06:43:12Z
3. Producing agent identified: clarity_carry.py via arif_seal kernel path
4. Mechanism confirmed: `isinstance(data, list)` check → silent discard → append receipt
5. All consumers broken: expecting dict, receiving array
6. Pre-seal backup exists with intact v1 state

## Verdict

```
HOLD_FOR_ARIF
```

**Reason:** This is a PROBABLE_OVERWRITE with a viable restoration path, but it touches the session-state continuity file for the entire federation. The overwrite was produced by a live kernel path (arif_seal → clarity_carry), meaning the root cause is a design conflict between receipt-stream and generational contracts. Restoration alone does not fix the design flaw — the two-writer race must be resolved (via carry_forward.py v2 migration + clarity_carry.py path redirect) to prevent recurrence.

**Next steps for sovereign decision:**
1. Approve restoration from pre-seal backup (Option A)
2. Approve migration to v2 (carry_forward.py migrate)
3. Approve clarity_carry.py patch to stop writing to the SOT path (redirect to a separate receipt log)
4. Identify and document the mystery v1 backup writer
