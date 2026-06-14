# Drift Response — OpenClaw Operational Skill

**Skill ID:** `drift-response`  
**Agent:** OpenClaw (AGI — Operational Gateway)  
**Priority:** P0  
**Forged:** 2026-06-14  
**DITEMPA BUKAN DIBERI**

## Purpose

Standard 5-step procedure for detecting and responding to runtime drift in the arifOS federation. Replaces ad-hoc "something feels wrong" with a structured, auditable protocol.

## Trigger

- `federation_health_scan` returns `drift: DRIFTING`
- AGI🦞 or any agent flags `drift = true`
- Filesystem/config divergence detected between `/root/arifOS` and `/opt/arifos/app`
- Service version mismatch detected

## The 5-Step Protocol

### Step 1: DETECT

```bash
# Run health scan to confirm drift signal
bash /root/AAA/skills/federation-health-scan/federation_health_scan.sh --json

# Check specific files for divergence
diff -q /root/arifOS/arifosmcp/server.py /opt/arifos/app/arifosmcp/server.py
diff -q /root/arifOS/arifosmcp/runtime/governance_pipeline.py /opt/arifos/app/arifosmcp/runtime/governance_pipeline.py

# Also check service versions
curl -s http://127.0.0.1:8088/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Live: {d.get(\"git_commit\",\"?\")}')"
cd /root/arifOS && git rev-parse --short HEAD
```

### Step 2: VERIFY

```bash
# Verify with nocache health check (bypasses any cached state)
curl -s "http://127.0.0.1:8088/health?nocache=1" | python3 -c "
import sys,json
d = json.load(sys.stdin)
print(f'Status: {d.get(\"status\")}')
print(f'Commit: {d.get(\"git_commit\")}')
print(f'Tools: {d.get(\"tools_loaded\")}')
print(f'Drift: {d.get(\"contract_drift\", \"unknown\")}')
"

# Check governance events for recent anomalies
# (via nat CLI or stream view)
```

### Step 3: CLASSIFY

| Severity | Criteria | Response |
|----------|----------|----------|
| **NUISANCE** | Minor file difference (whitespace, comments), no functional impact. All services healthy. | Log. No action needed. |
| **IMPORTANT** | Code logic divergence, different git commits between live and repo. Services still healthy. | Propose sync. 888_HOLD if restart needed. |
| **CRITICAL** | Service running different code path. Governance pipeline affected. Floors may not be enforced correctly. | IMMEDIATE 888_HOLD. Do not proceed with any MUTATE/ATOMIC actions. |

### Step 4: PROPOSE

Based on classification, output structured proposal:

```json
{
  "drift_id": "drift-20260614-001",
  "classification": "IMPORTANT",
  "affected_files": ["server.py", "governance_pipeline.py"],
  "impact": "Governance pipeline has NATS wiring in /root but not deployed to /opt",
  "proposed_action": "rsync updated files from /root/arifOS to /opt/arifos/app and restart arifos.service",
  "reversibility": "REVERSIBLE — keep backups of /opt files before sync",
  "requires_888": true,
  "888_reason": "arifos.service restart required"
}
```

### Step 5: ROUTE

- **NUISANCE:** Log to `/root/AAA/wiki/scars/` for record. No escalation.
- **IMPORTANT:** Present proposal to Arif. Wait for "Approve" or "888_HOLD override."
- **CRITICAL:** Immediate halt. Present to Arif with red flag. All MUTATE/ATOMIC tools blocked until resolved.

## Full Procedure (Single Command)

```bash
# Complete drift response in one invocation
bash /root/AAA/skills/drift-response/respond.sh
```

## Constraints

- Never auto-restart services. Any restart → 888_HOLD.
- Never auto-sync files that would change running code.
- Always keep backup of files before overwriting.
- Document every drift incident in `/root/AAA/wiki/scars/scar-drift-YYYY-MM-DD.md`.
