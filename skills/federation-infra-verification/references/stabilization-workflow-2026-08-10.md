# External Research → Federation Stabilization Workflow

## Session: 2026-08-10

**Trigger:** Arif sent external deep-research PDF ("arifOS Architecture and Horizon.pdf") and said "stabilize the kernel, map to current architecture, spawn opencode."

## Workflow

### Step 1: Extract + classify findings
- `pdftotext` for PDF extraction
- For each gap: classify RESOLVED / CONFIRMED / FALSE_POSITIVE / ARCHITECTURAL
- Don't trust snapshot date — probe fresh

### Step 2: Live probe
```bash
# Local organs
for p in 8088 7071 7072 3001 8081 18082 18083 7073; do
  curl -sf http://127.0.0.1:$p/health >/dev/null 2>&1 && echo "✅ $p" || echo "❌ $p"
done
# Manifest staleness
wc -l /root/arifOS/VAULT999/outcomes.jsonl  # actual
grep "records:" /root/AAA/federation/federation-manifest.yaml  # claimed
```

### Step 3: Plan file
`/root/forge_work/stabilization/STABILIZATION_PLAN.md` — GAP → STATE → ACTION table

### Step 4: Spawn opencode
```bash
opencode run 'Execute STABILIZATION TASKS...' -f /root/forge_work/stabilization/STABILIZATION_PLAN.md
```

### Step 5: Verify + report
Re-probe all endpoints. Table: Gap | Reality | Severity | Action

## Findings

| Finding | Evidence | Resolution |
|---------|----------|------------|
| VAULT999 manifest 30× stale | Manifest: 171 records. Actual: 45,712 | Updated federation-manifest.yaml |
| WELL degraded | state.json from Jul 4 (36 days stale), MOCK mode | Architectural gap — needs biometric pipeline |
| /doctrine/apex-theory SPA | Returns homepage HTML | React routing issue (low priority) |

## Key principle
External research = HYPOTHESIS. Live system = TRUTH. Map, don't copy.
