---
name: entropy-metabolizer
description: "Bridge audit findings to action — classifies entropy candidates into safe-cleanup, tracked-cleanup, investigate, and hold buckets, then executes safe-cleanup automatically. USE WHEN: after audit-repository-entropy produces a JSON ledger, or when Arif says 'clean up', 'lower entropy', 'metabolize findings', 'act on audit'. "
argument-hint: ["<audit-json-path> [--dry-run] [--auto-local] [--commit]"]
capability_tier: fed-agent-subagent
floor_scope: [F1, F2, F7, F11]
autonomy_tier: T1
risk_tier: low
---# /entropy-metabolizer

**Audit → Action bridge. Takes entropy audit JSON, classifies candidates, executes safe actions, reports results.**

> The audit finds. The metabolizer acts. Neither judges — the constitution judges.

---

## Input

Accepts either:
1. **JSON path** — output of `audit-repository-entropy` skill (`entropy-audit-*.json`)
2. **Repo name** — runs a fresh audit inline, then metabolizes (loads `audit-repository-entropy` as prerequisite)

---

## Classification buckets

| Bucket | Criteria | Action | Requires |
|--------|----------|--------|----------|
| **SAFE_LOCAL** | Gitignored `.bak*`, `.stale`, `build/`, `__pycache__/`, `.orig`, `*~` | Auto-delete | `--auto-local` flag |
| **TRACKED_DEBRIS** | Git-tracked stale files (`.stale`, old reports, superseded configs) | Present + confirm → `git rm` | Human confirmation or `--commit` flag |
| **INVESTIGATE** | Zero-reference files, purpose unknown, may be dynamic | Report only | None |
| **HOLD** | Superseded configs, competing canonical docs, runtime-uncertain | Report only | None |
| **KEEP** | Active, referenced, required | Skip | None |

---

## Method

### Step 1 — Load audit
```bash
# If JSON path provided:
cat $AUDIT_JSON | python3 -c "import sys,json; audit=json.load(sys.stdin)"

# If repo name provided: run audit-repository-entropy inline first
```

### Step 2 — Classify each candidate
For each candidate in `audit.candidates[]`:
- `disposition == KEEP` → skip
- `disposition == HOLD` → HOLD bucket, report
- `disposition == INVESTIGATE` → INVESTIGATE bucket, report
- `disposition == DEPRECATE` or `ARCHIVE`:
  - If `git ls-files` shows tracked → TRACKED_DEBRIS
  - If not tracked but exists on disk → SAFE_LOCAL
  - If not on disk → skip (already gone)
- `disposition == DELETE_CANDIDATE` → HOLD bucket (888 required, never auto)

### Step 3 — Process local_debris from summary
```bash
# Count and measure gitignored debris
find /root/$REPO -name "*.bak" -o -name "*.bak-*" -o -name "*.stale" -o -name "*.orig" -o -name "*~" 2>/dev/null | grep -v .git | grep -v node_modules
du -sh /root/$REPO/build/ 2>/dev/null
du -sh /root/$REPO/__pycache__/ 2>/dev/null
```

### Step 4 — Execute SAFE_LOCAL (if --auto-local)
```bash
# Delete gitignored backup/temp files
find /root/$REPO -name "*.bak" -o -name "*.bak-*" -o -name "*.bak.*" -o -name "*.stale" -o -name "*.orig" -o -name "*~" 2>/dev/null | grep -v .git | grep -v node_modules | xargs rm -v
# Remove gitignored build artifacts
rm -rf /root/$REPO/build/ 2>/dev/null
# Remove __pycache__
find /root/$REPO -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
```

### Step 5 — Present TRACKED_DEBRIS
List tracked debris items. If `--commit` flag:
```bash
git -C /root/$REPO rm <files>
git -C /root/$REPO commit -m "chore(entropy): remove tracked debris from audit findings"
```
Otherwise: present list, wait for human decision.

### Step 6 — Verify
```bash
# Confirm git status is clean (or shows only expected changes)
git -C /root/$REPO status -s
# Confirm no tracked files were harmed
git -C /root/$REPO diff --stat HEAD
```

### Step 7 — Report
Output structured result:
```json
{
  "audit_source": "path or inline",
  "repo_id": "string",
  "git_sha_after": "string",
  "actions": {
    "safe_local_deleted": 0,
    "safe_local_bytes_freed": 0,
    "tracked_removed": [],
    "tracked_committed": false,
    "investigate_reported": [],
    "hold_reported": []
  },
  "remaining_entropy": 0,
  "verdict": "METABOLIZED|PARTIAL|HELD"
}
```

---

## Hard stops

- **NEVER** auto-delete tracked files without `--commit` flag or human confirmation.
- **NEVER** delete files with `disposition == DELETE_CANDIDATE` (888 HOLD).
- **NEVER** delete files with `risk.dynamic_loading == "yes"`.
- **NEVER** delete files with `risk.external_consumer == "yes"`.
- **NEVER** mutate `.gitignore` as part of cleanup (separate action).
- **NEVER** commit without verifying `git status` shows only expected changes.

---

## ArifOS deploy integration

After cleanup + commit on arifOS repo:
1. Run deploy guard: `cd /root/arifOS && git push` (triggers 3-gate check)
2. If deploy guard passes → push + tag if version bumped
3. If deploy guard fails → HOLD, report failure
4. Reconciler (`scripts/arifos-deploy-reconciler.sh`) will auto-deploy within ~3 min

---

## Invocation

```
/entropy-metabolizer /root/arifOS/entropy-audit-2026-09-17.json --auto-local --commit
```

Or inline (audit + metabolize in one shot):
```
/entropy-metabolizer arifOS --auto-local
```

---

*APEX-zen aligned. ΔS < 0. Safe-local auto, tracked requires confirmation. 888 HOLD on DELETE_CANDIDATE. DITEMPA BUKAN DIBERI.*
