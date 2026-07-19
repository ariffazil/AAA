# ═══════════════════════════════════════════════════════════════════
# GitHub Organization Migration Guide
# ═══════════════════════════════════════════════════════════════════
# Phase 1: Move arifOS Federation from personal account to organization.
# This enables: org-wide rulesets, .github policy repo, team CODEOWNERS.
# ═══════════════════════════════════════════════════════════════════

## Prerequisites
- GitHub account: ariffazil (F13 SOVEREIGN)
- Org name: ArifFederation (or arif-os, arifos-federation)
- All 9 repos are currently under ariffazil/ personal account

## Step 1: Create Organization
1. Go to https://github.com/settings/organizations
2. Click "New organization"
3. Choose "Free" plan (sufficient for public repos)
4. Name: "ArifFederation"
5. Add billing email

## Step 2: Transfer Repositories
Transfer all 9 repos from ariffazil/ to ArifFederation/:
```
ariffazil/ariffazil    → ArifFederation/.github    (rename as policy repo)
ariffazil/arifos       → ArifFederation/arifos
ariffazil/AAA          → ArifFederation/AAA
ariffazil/A-FORGE      → ArifFederation/A-FORGE
ariffazil/GEOX         → ArifFederation/GEOX
ariffazil/geox         → ArifFederation/geox        (if separate)
ariffazil/WEALTH       → ArifFederation/WEALTH
ariffazil/WELL         → ArifFederation/WELL
ariffazil/arif-sites   → ArifFederation/arif-sites
ariffazil/HERMES       → ArifFederation/HERMES
```

After transfer, GitHub automatically redirects old URLs.

## Step 3: Create .github Policy Repository
The `.github` repo is the org-level control center:
- `workflow-templates/` — starter CI for new repos
- `profile/README.md` — org public profile
- `CODEOWNERS` — default ownership for org
- `FEDERATION.md` — org-level federation declaration

## Step 4: Setup Org-Wide Rulesets
Once repos are in the org:
1. Settings → Rules → Rulesets → New ruleset
2. Target: All repositories
3. Rules:
   - Require pull request before merging
   - Require approval of most recent review
   - Require conversation resolution
   - Require linear history
   - Block force pushes
   - Restrict deletions
   - Require workflows to pass before merging
   - Require deployment to succeed before merging

## Step 5: Update Remote URLs
After transfer, update all local clones:
```bash
for repo in arifos AAA A-FORGE GEOX WEALTH WELL arif-sites HERMES; do
  cd /root/$repo && git remote set-url origin git@github.com:ArifFederation/$repo.git
done
```

## Step 6: Update Workflow References
Update all reusable workflow references:
- `ariffazil/A-FORGE/.github/workflows/*` → `ArifFederation/A-FORGE/.github/workflows/*`
- Pin to full commit SHA after first merge

## Step 7: Setup arifOS GitHub App
1. Use manifest at arifOS/deploy/github-app-manifest.yml
2. Register app: https://github.com/settings/apps/new
3. Install on ArifFederation organization
4. Add as deployment protection rule in each environment

## Benefits After Migration
| Before (Personal) | After (Organization) |
|---|---|
| Rulesets per repo (8× config) | One org ruleset → all repos |
| No .github policy repo | Centralized workflow templates |
| No team CODEOWNERS | Org teams for review |
| No org-wide dependency review | Org-wide security policies |
| Limited attestation visibility | Org artifact attestation dashboard |

---
DITEMPA BUKAN DIBERI — 999 SEAL ALIVE
