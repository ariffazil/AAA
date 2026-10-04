# Deploy Lag vs Source/Runtime Divergence — Diagnosis Pattern

> **Canonical since:** 2026-08-10
> **Source:** arifOS kernel health_routes.py drift detection fields
> **Read this when:** kernel reports `drift=true`, or diagnosing drift claims

## The Three Commit Fields

The arifOS kernel health endpoint (`:8088/health`) exposes three commit fields in `software_release`:

| Field | Meaning | Source |
|-------|---------|--------|
| `source_commit` | What the runtime was **deployed from** | Baked into running code at deploy time |
| `built_commit` | What git HEAD **is now** | Live `git rev-parse HEAD` at health-check time |
| `deployed_commit` | Same as `source_commit` | Redundant field for cross-validation |

## Two Drift Types

### Type A: Deploy Lag (TRIVIAL)

```
source_commit = 39f6b1d   (deployed)
built_commit  = 1cdcc31   (git HEAD)
drift         = true
```

**Meaning:** Someone committed after the last deploy. Runtime is fine, just behind HEAD.

**Diagnosis:**
```bash
cd /root/arifOS
git log --oneline <source_commit>..<built_commit>
# 1-3 commits: trivial deploy lag
# 10+ commits: significant lag, check what changed
```

**Fix:** `make deploy-local` (T2 — reversible)

### Type B: Source/Runtime Divergence (SERIOUS)

```
source_commit = 39f6b1d   (claimed deployed)
built_commit  = 39f6b1d   (matches — no lag)
deployed      = 1cdcc31   (actual runtime DIFFERENT)
drift         = true
```

**Meaning:** Runtime was hot-fixed from `/opt/arifos/app` without going through git.

**Diagnosis:**
```bash
diff <(git show HEAD:arifosmcp/runtime/tools.py) /opt/arifos/app/arifosmcp/runtime/tools.py | head -50
```

**Fix:** Promote hot-fixes back to source, commit, deploy (T2 with review)

### Type C: False Positive (STALE TRACKER)

Service restarted AFTER deploy → tracker didn't update → drift is phantom.

**Diagnosis:**
```bash
systemctl show arifos.service --property=ActiveEnterTimestamp
# If restart > deploy time: tracker is stale
```

## Decision Tree

```
drift=true
  ├─ source ≠ built? → TYPE A (deploy lag) → deploy-local
  ├─ source ≠ deployed? → TYPE B (divergence) → promote hot-fixes
  └─ restart > deploy? → TYPE C (stale tracker) → self-corrects
```

## Carry Forward Convention

When resolving drift, always record the TYPE, not just "RESOLVED":
```json
{
  "DRIFT_6": {
    "status": "RESOLVED",
    "drift_type": "deploy_lag",
    "resolution": "TYPE_A deploy-local synced to HEAD 1cdcc315e"
  }
}
```

## Pitfall: Previous Session Claims ≠ Live State

carry_forward claims "DRIFT RESOLVED" are EVIDENCE, not TRUTH. Always re-probe live kernel health before trusting carry_forward drift status. Previous session resolved at commit X, but current HEAD is Y — the drift may have re-appeared or never actually resolved.
