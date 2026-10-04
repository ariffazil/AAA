# MMA-2026-08-07 Session Postmortem — Sibling Subagent Overwrite Incident

**Source:** Multimodal memory architecture audit session, 2026-08-07
**Authors:** hermes (audit, deliverables 01-05, 07-09) · 333-AGI (deliverable 06) · sibling subagent `20260807_102940_a64e9dd4` (overwrote 07 + 09)
**Severity:** Lesson-bearing — discovered through actual failure, not theory

---

## Timeline

| Time (UTC) | Event |
|---|---|
| 11:26 | Hermes writes MISSION.md, spawns OpenCode (333-AGI) |
| 11:30 | OpenCode SIGKILL'd by earlyoom (`--prefer opencode`); partial artifacts in workdir |
| 11:32-11:37 | Hermes writes 01-06 deliverables by hand |
| ~11:41 | **Sibling subagent** overwrites `07_validation_report.md` |
| ~11:42 | Same subagent overwrites `09_seal_review.md` |
| 11:42 | Hermes notices `_warning` field: "modified by sibling at 11:42:40 — after last read at 11:42:18" |
| 11:42 | Reads sibling's version — finds it stronger (caught Graphiti claim error, "877 records" wrong, "54 RLS tables" unverifiable) |
| 11:42 | Decision: preserve sibling's version, add post-mortem as audit material |
| 11:48 | `10_housekeeping_report.md` gets same `_warning` — different file, same pattern |
| 11:51 | Seals via `git commit d57da408` + `git_to_vault.py` |

## What the sibling caught that Hermes missed

- **Graphiti claim "times out"** — WRONG. `curl :8000/health` → `{"status":"healthy"}`. MCP `initialize` handshake required. Severity: MEDIUM not CRITICAL.
- **"877 records"** — WRONG. Qdrant `arifos_memory` = **49 points**. "877" came from unprobed Supabase.
- **"54 Supabase tables with RLS disabled"** — UNVERIFIABLE. Supabase is remote cloud, no local probe. Claim exists only in chat summary, not deliverables.
- **Pydantic v2 + SQL overclaim** — REJECTED. Format is YAML narrative, not executable schema.

**Why:** sibling had fresh perspective, not anchored to "I just verified this." Hermes' bias was self-confirmation; sibling's bias was adversarial.

## The 4 rules (operational formalization of F1-F13)

### 1. Pre-seal gate

```yaml
pre_seal_gate:
  artifact_hash_matches: true
  artifact_name_matches: true
  artifact_count_matches: true
  sealed_by: "hermes"
  sealed_at: "ISO-8601"
  source: "audit/MMA-2026-08-07"
```

Mapping: F11 AUDITABILITY + F2 TRUTH + F7 HUMILITY.

### 2. Risk-tiered verification

| Tier | Example | Depth |
|---|---|---|
| Read-only | grep, curl, ls | lightweight |
| Schema migration | JSONB ALTER, envelope patch | medium + dry-run |
| Financial mutation | capital scoring | heavy + cross-witness |
| Irreversible | DROP TABLE | mandatory re-probe + sovereign |

### 3. Auditor outputs are CLAIMS

Every verdict (generator, verifier, auditor) is a claim. No agent exempt from F2.

### 4. Sibling-overwrite detection

Check `_warning` from `write_file`. Check mtime before `patch`/`write_file`. Re-read if sibling wrote more recently.

## Meta-pattern: the auditor chain

1. OpenCode → original audit
2. Hermes → audited OpenCode (caught: 04 misnamed, SUMMARY missing)
3. Hermes → self-audit (caught: 06 inherited from 333-AGI, never reviewed)
4. Sibling subagent → audited Hermes (caught: Graphiti claim wrong, 877 records wrong)

> "The biggest threat was not hallucination. The biggest threat was correct information attached to the wrong artifact state."

## Cron jobs deployed (operational artifact)

| Job ID | Name | Schedule | Output |
|---|---|---|---|
| `50149e42f6d9` | seal-integrity-sweep | Sun 03:17 | seal-sweep-{date}.json |
| `7602d6cfdcc7` | memory-compression | Daily 02:13 | memory-compress-{date}.json |
| `8aa44381de86` | contradiction-scan | Sat 03:23 | contradiction-scan-{date}.json |
| `b9a87156ab3f` | provenance-audit | Monthly 1st 04:41 | provenance-audit-{date}.json |
| `3d369c28f1ab` | artifact-drift-audit | Daily 01:53 | artifact-drift-{date}.json |

All `deliver="local"`, save to `/root/.local/share/arifos/state/`.

## File state at seal

13 deliverables / 2,396 lines, sealed at commit `d57da408`:
- `docs/design-notes/2026-08-07-multimodal-memory-doctrine.md`
- `reports/multimodal-memory-audit/` (12 files + execution log)

---

*Provenance: 2026-08-07, hermes, session trace preserved in execution log + 13 deliverables.*
