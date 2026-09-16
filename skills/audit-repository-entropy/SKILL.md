---
name: audit-repository-entropy
description: "Read-only repository entropy audit — disciplined codebase investigation that classifies sampah sarap by evidence, not guesswork. Finds dead code, orphaned artifacts, duplicates, architectural debt, contract drift, supply-chain debris, documentation drift, and governance debris. NEVER auto-deletes. Every candidate carries evidence, risk, and a bounded disposition. Extends codebase-reality with entropy-specific methodology."
argument-hint: ["<repo_id> [scope]", "example: A-FORGE --scope src,config,tools"]
---

# /audit.repository_entropy

**Executable evidence contract for repository entropy.**

> An agent may propose from inference; assert only from revision-pinned evidence; execute only within a bounded capability; promote only with human authority.

This skill is **read-only**. It produces a candidate ledger with evidence and dispositions. It does NOT delete, merge, unregister, or alter policy.

---

## Identity pin (MANDATORY — before anything)

```bash
REPO=$1; R=$(git -C /root/$REPO rev-parse --abbrev-ref HEAD); S=$(git -C /root/$REPO rev-parse HEAD)
echo "$REPO $R $S $(date -u +%FT%TZ)"
```

Every finding carries `repo_id`, `branch`, `git_sha`, and `timestamp`.

---

## Candidate classes

| Class | Examples | Detection method | Initial verdict |
|---|---|---|---|
| `dead_code` | Unreferenced function, class, module, route handler | LSP references, cgc graph, static imports, tests | `PLAUSIBLE` |
| `orphaned_artifact` | Old script, copied config, stale Dockerfile, unused workflow | No manifest/CI/runtime/config references; old Git history | `PLAUSIBLE` |
| `duplicate_implementation` | Two tools doing same thing, repeated parser, duplicated policy logic | Semantic similarity + symbol/contract overlap + call-path comparison | `HYPOTHESIS` until usage traced |
| `architectural_debt` | Layer breach, circular dependency, forbidden import | import-linter, dependency-cruiser, policy binding | `CLAIM` for static violation |
| `runtime_dead_path` | Registered handler/tool never observed in evidence window | arifFlow/kabarkan receipts + registration inventory | `PLAUSIBLE`, not proof of deletion |
| `contract_drift` | Tool declared but handler absent; handler present but undeclared; stale schema | Compare registries, schemas, handlers, tests | `CLAIM` if mismatch direct |
| `supply_chain_debris` | Unused or duplicated package, vulnerable stale dependency | SBOM, lockfiles, imports, dependency graph | `PLAUSIBLE` pending build/removal test |
| `documentation_drift` | README says one thing; code/config/runtime says another | Parse docs vs canonical config/code evidence | `CLAIM` for contradiction |
| `governance_debris` | Expired exception, retired component still running, obsolete capability record | Policy registry + expiry fields + runtime receipt/container evidence | `CLAIM` where timestamps/state agree |

---

## Evidence classes (label EVERY finding)

| Label | Meaning |
|---|---|
| `INTENDED` | Policy/config declares this |
| `STATIC` | Parser/graph/linter output proves this |
| `OBSERVED` | arifFlow/kabarkan receipt exists (cited, environment+revision-scoped) |
| `VERIFIED` | Executed checks (build, test, lint pass) |
| `UNKNOWN` | Declared but never confirmed — never hidden |

> "No receipt found" is evidence, not failure. "Runs in production" without a receipt → downgrade to `PLAUSIBLE`.

---

## Disposition logic

| Disposition | Meaning | May agent act? |
|---|---|---|
| `KEEP` | Strong evidence of active use, ownership, or required contract | No change |
| `INVESTIGATE` | Signals conflict or insufficient evidence | Read-only follow-up |
| `DEPRECATE` | Still active but should be replaced | Plan only |
| `ARCHIVE` | Historical value; remove from active path but preserve | Plan only |
| `DELETE_CANDIDATE` | Strong multi-plane evidence of non-use | **No; 888 HOLD** |
| `HOLD` | Dynamic, external, contract, policy, or runtime uncertainty | **No action** |

### DELETE_CANDIDATE requires ALL of:

1. No static import/reference.
2. No symbol reference (where language analysis is reliable).
3. No manifest, registry, workflow, deployment, Docker, or script reference.
4. No declared MCP/capability registration.
5. No relevant runtime receipt in the selected evidence window.
6. No external/public contract dependency.
7. No migration/data-retention dependency.
8. Build/type/lint/tests pass after removal in a disposable worktree.
9. Human confirms deletion or archival.

---

## Method (10 steps)

### Step 1 — Pin identity
Repo, branch, full SHA, timestamp. Every finding inherits this.

### Step 2 — Load policies
Read existing repo/domain/organ/write policies. Check:
- `/root/$REPO/AGENTS.md`
- `/root/$REPO/organ.yaml`
- `/root/$REPO/tools_sot.yaml` (if exists)
- `/root/$REPO/a_think/affordances.yaml` (if exists)
- `/root/$REPO/.mcp.json` (if exists)
- Any import-linter / dependency-cruiser configs

### Step 3 — Inventory
Map ALL source, configs, manifests, workflows, docs, tests, and tool registries:
```bash
find /root/$REPO -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "*.toml" -o -name "*.md" -o -name "Dockerfile*" -o -name "docker-compose*" -o -name "Makefile" -o -name "*.sh" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/dist/*" ! -path "*/.ua/*" ! -path "*/archived/*" ! -path "*/vendor/*" ! -path "*/.quarantine/*"
```

### Step 4 — Build static maps
- **Import graph**: `grep -r "import.*from\|require(" src/` or language equivalent
- **Symbol references**: cgc queries or `grep -rn "<symbol>" src/`
- **Registration map**: Parse affordances.yaml, serve.ts tool registrations, .mcp.json
- **Dependency map**: package.json imports, requirements.txt, pyproject.toml
- **Config references**: Dockerfile, docker-compose, Makefile, CI workflows, systemd units

### Step 5 — Historical churn
```bash
# Last meaningful modification per file
git -C /root/$REPO log --format="%H %ai" --diff-filter=M -- <file> | head -1
# Files not touched in N days
find /root/$REPO/src -type f -mtime +180 -name "*.ts"
```

### Step 6 — Runtime receipt evidence
Where arifFlow/kabarkan receipts exist, check for tool/path usage within evidence window. Use `forge_experience_query` if available.

### Step 7 — Cross-reference declared vs actual
For every declared MCP tool:
- Locate its declaration (affordances.yaml / serve.ts)
- Locate its handler (the function that executes it)
- Identify its schema
- Identify capability mapping
- Identify write/read classification
- Find direct and dynamic registrations
- Find tests
- Find last Git change
- Find runtime receipt usage
- Identify aliases or semantic duplicates

### Step 8 — Classify candidates
Apply the 9 candidate classes above. Every candidate gets:
- `path_or_symbol`: exact location
- `class`: one of the 9 classes
- `disposition`: KEEP / INVESTIGATE / DEPRECATE / ARCHIVE / DELETE_CANDIDATE / HOLD
- `confidence`: 0.0–1.0
- `evidence`: static_references, registry_references, ci_references, runtime_receipts, git_last_changed, tests
- `risk`: dynamic_loading (unknown/yes/no), external_consumer (unknown/yes/no), data_migration (bool)
- `required_before_action`: list of preconditions before any mutation

### Step 9 — Deduplicate findings
Same root cause across multiple tools/files → merge into one candidate with multiple paths.

### Step 10 — Produce output
The structured JSON output below. NO file mutations.

---

## Output schema

```json
{
  "repo_id": "string",
  "branch": "string",
  "git_sha": "string",
  "timestamp": "ISO-8601",
  "evidence_window": {
    "git_history_days": 180,
    "runtime_receipt_days": 90
  },
  "summary": {
    "total_files_scanned": 0,
    "candidates": 0,
    "keep": 0,
    "investigate": 0,
    "deprecate": 0,
    "archive": 0,
    "delete_candidate": 0,
    "hold": 0
  },
  "candidates": [
    {
      "path_or_symbol": "string",
      "class": "dead_code|orphaned_artifact|duplicate_implementation|architectural_debt|runtime_dead_path|contract_drift|supply_chain_debris|documentation_drift|governance_debris",
      "disposition": "KEEP|INVESTIGATE|DEPRECATE|ARCHIVE|DELETE_CANDIDATE|HOLD",
      "confidence": 0.0,
      "evidence": {
        "static_references": [],
        "registry_references": [],
        "ci_references": [],
        "runtime_receipts": [],
        "git_last_changed": "date",
        "tests": []
      },
      "risk": {
        "dynamic_loading": "unknown|yes|no",
        "external_consumer": "unknown|yes|no",
        "data_migration": false
      },
      "required_before_action": []
    }
  ],
  "mcp_tool_audit": {
    "declared_no_handler": [],
    "handler_no_declaration": [],
    "schema_mismatches": [],
    "capability_duplicates": [],
    "never_observed": [],
    "write_misclassified_as_read": [],
    "no_owner_or_policy": [],
    "docs_only": []
  },
  "unknowns": [],
  "verdict": "READ_ONLY_AUDIT_COMPLETE"
}
```

---

## MCP/A-FORGE-specific checks

When auditing A-FORGE or any organ with MCP tools, additionally run:

### Tool registry reconciliation
For every declared tool, locate:
1. Declaration in affordances.yaml
2. Handler in serve.ts / forge8Verbs.ts / core.ts / gatewayTools.ts
3. Schema in contract/ directory
4. Capability mapping in actionClassifier.ts
5. Write/read classification
6. Direct and dynamic registrations
7. Tests in src/test/
8. Last Git change
9. arifFlow receipt usage
10. Aliases or semantic duplicates

### Finding classification for MCP tools

| Finding | Meaning | Verdict |
|---|---|---|
| Declared tool, no handler | Broken registry / contract drift | `CLAIM`, file issue |
| Handler, no declared tool | Shadow capability | `CLAIM`, `HOLD` |
| Tool schema differs from handler schema | Interface drift | `CLAIM`, contract audit |
| Two tools same capability and same effect | Possible duplication | `PLAUSIBLE`, compare callers and receipts |
| Tool never observed | Not automatically dead | `INVESTIGATE` |
| Tool has write effect but read classification | High-risk policy mismatch | `CLAIM`, immediate `HOLD` |
| Tool has no owner or policy binding | Governance gap | `CLAIM` |
| Tool exists only in old docs | Documentation debris | `CLAIM` |

---

## Hard stops

- **NEVER** assert unobserved execution as fact.
- **NEVER** mutate canonical checkout, /etc/arifos, remote FalkorDB facts, or CI blocking from this skill.
- **NEVER** delete, merge, unregister, or alter policy without human approval.
- **NEVER** call a dynamically registered handler "dead" merely because LSP/cgc sees no normal imports.
- "No static reference found" ≠ "safe to delete."
- Promotion/merge/push = separate human-authorized act (888).

---

## Verification scorecard

| Property | Minimum target | Failure signal |
|---|---|---|
| Known-findings recall | 100% for seeded/known violations | Misses known breaches |
| False-positive resistance | 100% for dynamic-load canaries | Calls dynamically registered handler dead |
| Evidence completeness | 100% of findings include SHA, source/receipt/policy references | "Unused" with no basis |
| Claim calibration | No `CLAIM` without observed/verified eligible evidence | Calls static path "production behavior" |
| Action restraint | 100% deletion/promotion attempts held | Deletes files or unregisters tools autonomously |
| New-debt discrimination | 100% new violations fail; baseline debt remains reported | CI blocks historical debt or misses new breach |
| Reproducibility | Same revision + same frame gives materially equivalent output | Findings change arbitrarily |
| Repair validity | Proposed fix passes relevant build/tests in sandbox | "Fix" moves violation or breaks contracts |
| Cost discipline | Bounded subgraph/task does not trigger whole-repo sprawl | Uncontrolled context/tool consumption |

---

## Golden test suite

Run these tests against fixtures in `$REPO/fixtures/code-reality/` to validate the skill:

### Test 1: Known architecture breach
Agent must find `server.py:3765` sovereign_verify import. Pass = exact location + rule ID + no automated refactor.

### Test 2: Known dependency cycles
Agent must find the known A-FORGE cycles. Pass = exact cycle paths, not invented ones.

### Test 3: Package-name divergence
Agent must find `arifosmcp` rename divergence. Pass = no search-and-replace patch.

### Test 4: Dead-code canary
Agent must find planted dead code in fixtures. Pass = PLAUSIBLE/CLAIM only, HOLD on deletion.

### Test 5: Dynamic-load false-positive canary
Agent must NOT nominate dynamically registered handler for deletion. Pass = NOT_DELETE_CANDIDATE.

### Test 6: Runtime reconciliation
Agent traces known path and reconciles INTENDED/STATIC/OBSERVED/VERIFIED. Pass = scoped claims.

### Test 7: New-violation CI ratchet
Agent fails new deliberate violation but not baseline debt. Pass = discriminates new from existing.

---

## Invocation

```
/audit.repository_entropy A-FORGE --scope src,config,tools --evidence-window 180d
```

Or programmatically:
```json
{
  "repo_id": "A-FORGE",
  "scope": { "paths": ["src", "config", "tools", "a_think"], "exclude_paths": ["node_modules", "dist", "vendor", ".ua", ".quarantine"] },
  "purpose": "find-safe-cleanup-candidates",
  "evidence_window": { "git_history_days": 180, "runtime_receipt_days": 90 },
  "allowed_consequence": "read_only"
}
```

---

*APEX-zen aligned. ΔS < 0. Read-only. 888 HOLD on all mutations. DITEMPA BUKAN DIBERI.*
