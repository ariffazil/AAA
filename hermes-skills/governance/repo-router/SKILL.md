---
name: repo-router
description: Routing validation skill — classifies work to correct repo, checks confidence, enforces REPO= trailer before commit. Activate on ANY task that involves git, file writes, or multi-repo context.
category: governance
---

# repo-router — Routing Validation Skill

## Trigger
**Every task involving:** git, file writes, PRs, cross-repo context, or ambiguous scope.

## Routing Constitution
Full text: `/root/AAA/REPO_ROUTING_CONSTITUTION.md`

## Repo Map (canonical)

| Repo | Domain | Local Path | Remote |
|------|--------|-----------|--------|
| **AAA** | Agent workspace, governance, ADRs | `/root/AAA/` | `github.com/ariffazil/AAA` |
| **arifOS** | Constitutional kernel, F1–F13, MCP runtime | `/root/arifOS/` | `github.com/ariffazil/arifOS` |
| **WEALTH** | Capital intelligence, finance | `/root/WEALTH/` | `github.com/ariffazil/wealth` |
| **GEOX** | Earth domain, geoscience | `/root/geox/` | `github.com/ariffazil/geox` |
| **A-FORGE** | TypeScript bridge, agent engine | `/root/A-FORGE/` | `github.com/ariffazil/A-FORGE` |
| **arif-sites** | Web assets, static pages | `/root/arif-sites/` | `github.com/ariffazil/arif-sites` |
| **ariffazil** | Personal profile, meta | `/root/repos/ariffazil/` | `github.com/ariffazil/ariffazil` |

## Mandatory Pre-Write Checklist

```
══════════════════════════════════════
REPO=          ← exact repo name
CONFIDENCE=    ← 0.00–1.00
REMOTE_OK=     ← yes | no
WORKTREE_OK=   ← yes | no
ACTION=        ← proceed | hold | escalate
══════════════════════════════════════
```

## Confidence Thresholds

| Score | Action |
|-------|--------|
| ≥ 0.95 | Proceed autonomously |
| 0.90–0.94 | Proceed, note in PR |
| 0.80–0.89 | Ask Arif |
| < 0.90 + multi-repo | 888_HOLD |
| < 0.80 | Refuse |

## Commit Message Format

```
<subject line>

REPO=<correct-repo>
CONFIDENCE=<0.00-1.00>
```

## Enforcement Layers

| Layer | Mechanism | Reliability |
|-------|-----------|-------------|
| 1 | GitHub branch protection (require PR + 1 review) | ✅ Strong — mechanical |
| 2 | CI workflow (`repo-routing-validation.yml`) validates REPO= on all PR commits | ✅ Strong |
| 3 | Local pre-push hook (branch name check) | ⚠️ Partial — see git 2.51.0 stdin bug |
| 4 | Pre-push hook REPO= validation | ⚠️ Broken over SSH — use CI instead |

### ⚠️ git 2.51.0 Pre-Push Hook Limitation

**Bug:** Git 2.51.0 passes stdin as `/dev/null` to pre-push hooks over SSH transports. The hook receives zero bytes on stdin — cannot read push data.

**Impact:** Local pre-push hook REPO= validation silently fails (blocks push even with valid REPO= because stdin is empty).

**Workaround:** Primary REPO= enforcement is CI + branch protection. Install hook for branch-name-only check (main/master block), not for REPO= validation.

**Full details:** skill `git-pre-push-hook-stdin-bug`

### Pre-Push: Only Safe Validation

```bash
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" == "main" || "$CURRENT_BRANCH" == "master" ]]; then
  echo "🛑 Direct push to main blocked"
  exit 1
fi
```

For REPO= validation → rely on CI workflow.

## Cross-Repo Detection
If task touches ≥ 2 repos: STOP. Produce one PR per repo. Do not merge scopes.

## Failure Response
Wrong repo risk → Do nothing except report mismatch + propose correct path.
