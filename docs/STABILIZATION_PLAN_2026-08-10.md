# Federation Stabilization — Autonomous Prompts
# Generated: 2026-08-10 01:15 MYT
# Status: OBSERVE_ONLY (blocker: 1-commit deploy lag)

## Current State Summary

| Metric | Value | Status |
|--------|-------|--------|
| Organs | 8/8 alive | ✅ |
| FQ (live) | 2.0 OPTIMAL | ✅ |
| FQ (carry_forward) | 0.51 WATCHING | ⚠️ STALE |
| Git repos clean | 6/6 | ✅ |
| Deploy lag | 1 commit (39f6b1d → 1cdcc31) | 🟡 |
| Cron jobs | 8 ok, 11 error | 🔴 |
| Open loops | 4 | 🟡 |
| Drift flag | true (kernel source_commit stale) | 🟡 |

---

## PHASE 1: Deploy Lag Fix (T2)

**Trigger:** Sovereign switches profile to EXECUTE, or manual run.
**Risk:** REVERSIBLE. 1 commit behind. No schema changes.

```bash
cd /root/arifOS && make deploy-local
```

**Verification:**
```bash
curl -sf http://127.0.0.1:8088/health | python3 -c "
import sys, json
h = json.load(sys.stdin)
d = h['software_release']
print(f'drift={d[\"drift\"]}')
print(f'source={d[\"source_commit\"][:12]}')
print(f'built={d[\"built_commit\"][:12]}')
print(f'deployed={d[\"deployed_commit\"][:12]}')
"
# Expected: drift=false, all three match
```

**Carry forward update:**
```json
{
  "DRIFT_6": {
    "status": "RESOLVED",
    "resolved_at": "2026-08-10T01:15:00+08:00",
    "resolution": "deploy-local synced runtime to HEAD 1cdcc315e",
    "receipt": "pending"
  }
}
```

---

## PHASE 2: Cron Job Triage (11/19 erroring)

### Erroring jobs by category:

#### A. Script-based (no_agent=true) — check script exists + deps
- `output-attestation-check` (4f47cde23bb8) — script: check-unattested-outputs.sh
- `hermes-dna-metrics-refresh` (8ab448e3e11b) — script: hermes-dna-refresh.sh
- `institution-metrics-pulse` (4eee9cc62dfb) — script: publish-metrics.sh

**Diagnosis prompt:**
```
You are cron-diagnostics. Check each erroring script-based cron job:

1. output-attestation-check:
   - Script: /usr/local/lib/hermes-agent/profiles/aaa-hermes/scripts/check-unattested-outputs.sh
   - Check: does it exist? is it executable? run it manually, capture exit code + stderr

2. hermes-dna-metrics-refresh:
   - Script: /usr/local/lib/hermes-agent/profiles/aaa-hermes/scripts/hermes-dna-refresh.sh
   - Check: does it exist? deliver target = telegram:8410138119 (bot can't message itself)
   - FIX: change deliver to 'local' or remove

3. institution-metrics-pulse:
   - Script: /usr/local/lib/hermes-agent/profiles/aaa-hermes/scripts/publish-metrics.sh
   - Check: does it exist? is it executable?

Return: script_path | exists | executable | last_error | fix_action
```

#### B. Agent-based (LLM-driven) — check prompt + tool access
- `arif-morning-pulse` (2a3fe4915620)
- `arif-world-reality-intel` (0e37cdaf4a37)
- `syed-mak-dressing` (5d87405c1770)
- `syed-gerd-log` (0f07d72c0673)
- `syed-sambal-preorder` (cf1c6b534b2f)
- `seal-integrity-sweep` (50149e42f6d9)
- `memory-compression` (7602d6cfdcc7)
- `artifact-drift-audit` (3d369c28f1ab)

**Diagnosis prompt:**
```
You are cron-agent-diagnostics. For each erroring agent-based cron job:

1. Read the full prompt from the cron job (use cronjob action=list)
2. Check if the prompt references files/tools that exist
3. Check if enabled_toolsets are correct
4. Check delivery target validity
5. Check if the job's workdir exists

Common failure modes:
- Prompt references non-existent files
- Tool access denied (subagents can't use delegate_task, clarify, memory, send_message)
- Delivery target unreachable (bot messaging itself, wrong chat_id)
- Workdir doesn't exist

Return: job_name | error_type | root_cause | fix_action | priority(P0/P1/P2)
```

#### C. Delivery error (bot messaging itself)
- `hermes-dna-metrics-refresh` — deliver=origin (self-targeting)
- FIX: change deliver to 'local'

---

## PHASE 3: State Reconciliation

### 3A. Update carry_forward.json

**Prompt:**
```
You are state-reconciler. Update /root/.local/share/arifos/carry_forward.json:

1. Read current file
2. Update FQ to match live: fq=2.0, verdict=OPTIMAL (from arifFlow :7073)
3. Update DRIFT_6 status to RESOLVED (after deploy)
4. Update git HEADs:
   - aforge=d896e9e4
   - aaa=76a1d04e
   - arifOS=1cdcc315e (or 39f6b1d if deploy not done yet)
   - geox=43d32778
   - wealth=94193d4
   - well=baba783
5. Update session_id to current: SEAL-0a6f4140e7124414
6. Write file
7. Verify: cat the file and confirm fields match
```

### 3B. Reconcile kernel source_commit tracker

**Investigation prompt:**
```
You are kernel-drift-investigator. The arifOS kernel reports:
- source_commit: 39f6b1d (deployed)
- built_commit: 1cdcc31 (git HEAD)
- drift: true

This is a 1-commit deploy lag, not a source/runtime divergence.

1. Read /opt/arifos/app/arifosmcp/runtime/rest_routes/health_routes.py
2. Find where source_commit and built_commit are computed
3. Determine: is source_commit = deployed version? is built_commit = git HEAD?
4. If the drift detection is by design (deploy lag = drift), document it
5. If the tracker is stale/broken, identify the fix

Return: root_cause | is_by_design | recommended_action
```

---

## PHASE 4: Open Loop Progress

### 4A. DRIFT_5a — Wiki mkdocs (empty directory)

**Prompt:**
```
You are wiki-pipeline-builder. The wiki subdomain route exists in Caddy
but /var/www/html/wiki is empty. No mkdocs installed.

TASK: Create a minimal mkdocs setup for the wiki.

1. Check if mkdocs is installed: which mkdocs || pip install mkdocs
2. Create /root/wiki/ with mkdocs.yml
3. Use material theme (dark, consistent with arifOS aesthetic)
4. Create 3 starter pages:
   - index.md (federation overview)
   - organs.md (organ topology — from /root/AAA/docs/ORGAN.md)
   - floors.md (F1-F13 — from /root/arifOS/GENESIS/FLOOR_TABLE.json)
5. Build: cd /root/wiki && mkdocs build -d /var/www/html/wiki
6. Verify: curl -sf http://localhost/wiki/ returns HTML
7. Do NOT deploy to production — just build locally

CONSTRAINTS:
- Read-only on production configs
- Reversible: wiki output can be deleted without impact
- Do not modify Caddy config (routes already exist)
```

### 4B. FRAME — W-vector Measurement Infrastructure

**Prompt:**
```
You are frame-designer. The W-vector measurement infrastructure is not
implemented. Weights remain narrative.

TASK: Design the FRAME measurement system.

1. Read /root/AAA/governance/AGENCY_LEVELS.md for the 7 agent contract properties
2. Read /root/AAA/governance/ZEN_EXECUTION_DOCTRINE.md for FQ/ΔS definitions
3. Read /root/arifOS/GENESIS/FLOOR_TABLE.json for F1-F13 definitions

DESIGN OUTPUT (write to /root/AAA/governance/FRAME_DESIGN.md):
- Define 5 measurable W-vector dimensions (one per agent contract property)
- For each: signal source, measurement method, threshold, escalation path
- Map to existing telemetry (arifFlow, VAULT999, organ health)
- Define aggregation formula (weighted average with F13 override)

CONSTRAINTS:
- Design only, no implementation
- Must be measurable with existing tools (curl, grep, jq)
- F13 (SOVEREIGN) always has veto
```

### 4C. PRIMARY-DEMOTION-Criteria

**Prompt:**
```
You are demotion-criteria-designer. No criteria exist for when opencode
should lose PRIMARY coding harness designation.

TASK: Design demotion criteria.

1. Read /root/AAA/governance/HARNESS_ROUTING_DOCTRINE.md (if exists)
2. Read the current PRIMARY designation in /root/AGENTS.md §Harness Routing
3. Read /root/AAA/governance/AGENCY_LEVELS.md for tier definitions

DESIGN OUTPUT (write to /root/AAA/governance/PRIMARY_DEMOTION_CRITERIA.md):
- Define 3 trigger conditions for demotion (e.g., N consecutive failures,
  capability mismatch, cost threshold)
- Define demotion process (who decides, how announced, rollback)
- Define re-promotion criteria
- Map to existing governance (apex-judge, F13)

CONSTRAINTS:
- Design only, no implementation
- Must be executable by apex-judge isolate
- F13 (SOVEREIGN) override always available
```

### 4D. Gödel Lock — 666 Auditor External Witness

**Prompt:**
```
You are godel-lock-investigator. The 666 Auditor is compressed into
arif_judge — no external witness. This creates a Gödel loop risk:
a system that audits itself cannot certify its own correctness.

TASK: Assess the risk and propose solutions.

1. Read /root/AAA/governance/GODEL_LOCK_STRANGE_LOOP.md (if exists)
2. Read /root/arifOS/GENESIS/000_KERNEL_CANON.md for constitutional architecture
3. Check if apex-judge isolate provides sufficient external witness
4. Check if the current arif_judge implementation has self-audit capabilities

OUTPUT (write to /root/AAA/governance/GODEL_LOCK_ASSESSMENT.md):
- Risk assessment: is the Gödel lock real or theoretical?
- Current mitigations: what already prevents self-certification?
- Proposed solutions: external witness options (OpenClaw, separate model, etc.)
- Recommendation: accept risk vs mitigate vs escalate to F13

CONSTRAINTS:
- Assessment only, no implementation
- Must be honest about what we don't know (F7 HUMILITY)
- F13 (SOVEREIGN) decides whether to accept or mitigate
```

---

## Execution Order

| Phase | Priority | Blocking? | Autonomy |
|-------|----------|-----------|----------|
| 1. Deploy lag | P0 | Yes (OBSERVE_ONLY blocks) | T2 — needs sovereign |
| 2. Cron triage | P1 | No | T1 — auto-do |
| 3A. carry_forward | P1 | No | T1 — auto-do |
| 3B. kernel tracker | P2 | No | T0 — observe only |
| 4A. Wiki | P2 | No | T1 — auto-do |
| 4B. FRAME | P3 | No | T1.5 — proposal |
| 4C. Demotion | P3 | No | T1.5 — proposal |
| 4D. Gödel | P3 | No | T1.5 — assessment |

---

## Verification Checklist (post-execution)

- [ ] deploy-local: drift=false in /health
- [ ] carry_forward: FQ=2.0, DRIFT_6=RESOLVED
- [ ] Cron errors: 0 (all jobs either fixed or paused)
- [ ] Wiki: curl localhost/wiki/ returns 200
- [ ] FRAME: design doc exists at /root/AAA/governance/FRAME_DESIGN.md
- [ ] Demotion: criteria doc exists at /root/AAA/governance/PRIMARY_DEMOTION_CRITERIA.md
- [ ] Gödel: assessment doc exists at /root/AAA/governance/GODEL_LOCK_ASSESSMENT.md

---

*DITEMPA BUKAN DIBERI — Stabilization forged, not given.*
