# Federated Docs Consolidation — STATE.md Entropy Reduction

> Produced 2026-08-09. Triggered by Arif: "map all MD canon related files in AAA that should be federated and zen lower entropy"

## The Pattern

When `/root/AAA/docs/` has accumulated 300+ files and STATE.md exists as the working SOT, use this workflow to reduce entropy.

### Step 1: Inventory
```bash
find /root/AAA/docs -name '*.md' -type f | grep -v '/archive/' | wc -l
find /root/AAA/docs -name '*.md' -type f | grep -v '/archive/' | sort
```

### Step 2: Classify each file

| Category | Rule | Action |
|----------|------|--------|
| **FEDERATED** | Already points to STATE.md | Keep as-is |
| **CANONICAL** | Contains constitutional/governance truth (F1-F13, separation axiom, authority layers, protocol doctrine) | Merge key sections into STATE.md |
| **SATELLITE** | Operational/runbook (ops, recipes, config guides, session receipts) | Add header: `→ See STATE.md for constitutional context` |
| **ARCHIVE** | Superseded drafts, old audit receipts, historical design docs | Move to `/root/AAA/archive/` |

### Step 3: Tiered merge

**Tier 1 — FEDERATE INTO STATE.md** (constitutional truth):
- Files mentioning F1-F13 floors, separation axiom, ACT+DID, protocol subordination
- Example: `CONSTITUTIONAL_SEPARATION_AXIOM.md`, `ACT_AUTHORITY_LAYER.md`

**Tier 2 — SATELLITE** (operational pointer):
- Files about specific tools, procedures, runbooks, session receipts
- Keep as-is but add reference to STATE.md

**Tier 3 — ARCHIVE** (dead weight):
- `architecture/` design history
- `audit-*` old audit receipts
- `receipts/` old receipts
- Anything superseded by a newer version

### Step 4: Verify
```bash
# Count federated vs independent
grep -rl "STATE.md" /root/AAA/docs/*.md | wc -l
find /root/AAA/docs -name '*.md' -not -path '*/archive/*' | wc -l
```

## Key Insight (from the Constitutional Separation Axiom)

Protocol files (MCP, A2A) are replaceable. Governance files (F1-F13, ACT, VAULT999) are immutable. The consolidation priority order follows the axiom:
- L6/L5/L4 files → merge into STATE.md (constitutional layer)
- L3/L2 files → satellite pointers (replaceable layer)
- L1 files → archive or delete (disposable layer)

## Current State (as of 2026-08-09)

| Status | Count |
|--------|-------|
| Federated (→ STATE.md) | 11 |
| Independent | 329 |
| Total non-archive | 340 |

STATE.md: 300 lines, commit `b335949b`.
