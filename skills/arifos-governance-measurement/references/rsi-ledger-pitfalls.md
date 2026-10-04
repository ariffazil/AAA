The RSI ledger (`/root/.local/share/arifos/rsi-ledger.jsonl`) is the primary telemetry source for W1 (Objective Fidelity) and W5 (Feedback Integrity). This document captures known data-quality pitfalls discovered during FRAME implementation (2026-08-10).

## Field Type Inconsistency: `fix_installed`

The `fix_installed` field has 4 observed shapes:

| Value | Type | Meaning |
|-------|------|---------|
| `true` | bool | Fix was applied |
| `false` | bool | Fix was not applied |
| `"description text"` | string | Fix was applied, described inline |
| `"False"` | string | Fix was not applied (string, not boolean) |

### Correct Pattern

```python
fix_installed = d.get('fix_installed', False)
remediate = d.get('remediate', {})
if isinstance(remediate, dict):
    fix_installed = fix_installed or remediate.get('fix_installed', False)

# Count as remediated if truthy and not the string "False"
if fix_installed and fix_installed != "False":
    remediated += 1
```

### Wrong Pattern

```python
# WRONG — misses string descriptions and "False" string
if fix_installed == True:
    remediated += 1
```

## Schema Variability

RSI entries have inconsistent shapes across sessions. Three common patterns:

### Pattern A: Flat (early sessions)
```json
{
  "session_id": "SEAL-xxx",
  "timestamp": "...",
  "bottleneck": "description",
  "fix": "none_required",
  "delta_S": 0.0
}
```

### Pattern B: Nested (mid sessions)
```json
{
  "session_id": "SEAL-xxx",
  "timestamp": "...",
  "trace": { "task": "...", "tools_called": [...] },
  "diagnose": { "bottleneck": "...", "root_cause_found": true, "finding": "..." },
  "remediate": { "fix_installed": true, "fix_description": "...", "sovereign_action_required": false }
}
```

### Pattern C: Mixed (recent sessions)
```json
{
  "session_id": "SEAL-xxx",
  "timestamp": "...",
  "bottleneck": "description",
  "fix_installed": "description text or bool",
  "delta_entropy": -0.3
}
```

### Robust Access Pattern

Always use `.get()` with defaults. Never access nested fields directly:

```python
# Safe: handles all patterns
bottleneck = d.get('bottleneck', '')
if not bottleneck:
    diagnose = d.get('diagnose', {})
    if isinstance(diagnose, dict):
        bottleneck = diagnose.get('bottleneck', '')

fix_installed = d.get('fix_installed', False)
remediate = d.get('remediate', {})
if isinstance(remediate, dict) and not fix_installed:
    fix_installed = remediate.get('fix_installed', False)
```

## No Harness Attribution

RSI entries record `session_id` but NOT which harness (OpenCode/Kimi/Claude) was used. This makes harness-level error rate analysis (T3 demotion criterion) impossible without extending the schema.

**Recommendation:** Add `harness_id` field to RSI ledger entries. Auto-populate from session context.

## Baseline Statistics (2026-08-10)

- Total entries: 265
- With bottleneck (diagnosed): 75
- With fix_installed truthy (remediated): 33
- W5 ratio: 0.44 (CAUTION)
- Top bottleneck patterns: EVIDENCE_GAP (10x), TOOL_DRIFT (9x), ENTROPY_GAIN (2x)
