---
id: federation-release-attestation
name: federation-release-attestation
version: 1.0.0
description: 'Produces a seven-repository federation release manifest proving tag, commit, CI, artifact, and deployed-runtime parity'
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- claude-code
- codex
- opencode
- kimi
- kimi-code
- copilot-cli
dependencies:
  skills:
    - FORGE-repo-intelligence
    - FORGE-ci-diagnose
    - secret-safety-scan
  servers:
    - a-forge
    - github-official
  tools:
    - forge_worktree
    - forge_git_status
    - forge_git_log
    - forge_git_diff
    - forge_filesystem_read
    - forge_github_search
    - forge_github_get_file
examples:
- Generate v2026.07.17-AAA release manifest with all 7 repo SHAs
- Verify deployed commit matches source tag across federation
- Detect tag-vs-main drift and propose corrected tag
tests:
- Manifest includes all 7 repos with commit SHA
- Detects when a repo tag is behind main
- Detects missing CI evidence per repo
- Refuses to overwrite existing published tag
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Ω
  functional:
  - Audit
  - Ops
  layer: CODING/FI
  autonomy_tier: T1
floor_scope:
- F1
- F2
- F11
---

# federation-release-attestation

> **Prove parity. Never overwrite.**
> Tags are immutable receipts. If a tag is behind main, issue a new corrected tag.

## Manifest Schema

```json
{
  "release": "vYYYY.MM.DD-AAA",
  "generated_at": "ISO-8601",
  "generated_by": "agent-id",
  "repos": {
    "arifOS": {
      "commit": "full SHA",
      "tag": "vYYYY.MM.DD-AAA",
      "tag_matches_head": true,
      "ci_status": "pass|fail|unknown",
      "ci_run_url": "url or UNMEASURED",
      "artifact_hash": "sha256 or UNMEASURED",
      "deployed_commit": "full SHA or UNMEASURED",
      "runtime_health": "healthy|degraded|down|UNMEASURED",
      "tools_list_count": 0,
      "surface_consistent": false
    }
  },
  "federation_summary": {
    "total_repos": 7,
    "repos_at_tag": 0,
    "repos_with_ci_pass": 0,
    "repos_runtime_healthy": 0,
    "drift_detected": false,
    "drift_details": []
  },
  "corrected_from": null,
  "signature": "sha256 or UNMEASURED"
}
```

## Operating Procedure

### 1. Inventory

For each of the 7 federation repos:
```bash
cd /root/<repo>
git rev-parse HEAD                    # current commit
git rev-parse vYYYY.MM.DD-AAA^{}     # tag commit (if exists)
git status --porcelain               # working tree
git rev-list --count origin/main..HEAD  # ahead
git rev-list --count HEAD..origin/main  # behind
```

### 2. Tag-vs-Main Check

```yaml
for each repo:
  if tag_commit != head_commit:
    drift = true
    detail: "Tag {tag} at {tag_commit}, main at {head_commit}"
```

### 3. CI Evidence

For each repo, fetch the workflow run for the tag commit:
```yaml
if ci_status == "UNMEASURED":
  report as "missing evidence" — do not fabricate
```

### 4. Runtime Probe

```yaml
for each organ with a runtime:
  curl :port/health → parse status, deployed_commit, tools_loaded
  if timeout or error: report "UNMEASURED"
```

### 5. Generate Manifest

Combine all evidence into the manifest schema. If drift detected on any repo, set `corrected_from` to the previous release tag and propose a new tag.

### 6. Tag Discipline (Iron Rule)

- **Never** `git tag -f` an existing published tag.
- **Never** `git push --force` a tag.
- If correction needed: create new tag (e.g., `v2026.07.17-AAA-r2` or next date).
- Old tag remains as immutable receipt of what was known at that time.

---

## Federation Repo Map

| Repo | Path | Organs | Runtime Port |
|------|------|--------|-------------|
| arifOS | `/root/arifOS` | Governance kernel | :8088 |
| A-FORGE | `/root/A-FORGE` | Execution engine | :7071 |
| AAA | `/root/AAA` | Control plane | :3001 |
| GEOX | `/root/GEOX` | Earth intelligence | :8081 |
| WEALTH | `/root/WEALTH` | Capital intelligence | :18082 |
| WELL | `/root/WELL` | Human readiness | :18083 |
| arif-sites | `/root/arif-sites` | Web estate | — |

---

*DITEMPA BUKAN DIBERI — Forged, Not Given.*
