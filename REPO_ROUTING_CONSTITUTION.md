# REPO_ROUTING_CONSTITUTION.md

> **DITEMPA BUKAN DIBERI** — Routing intelligence is earned, not assumed.
> **Amanah clause:** Never route faster than certainty. Refuse over misroute.

---

## MISSION

Put every piece of work into the **correct repository** on VPS and GitHub.
Prefer refusal over misrouting. Never trade correctness for speed.

---

## AUTHORITATIVE REPO MAP

| Repo | Domain Charter | VPS Workspace | GitHub |
|------|---------------|---------------|--------|
| **AAA** | Agent workspace, governance, ADRs, orchestration canon | `/root/AAA/` | `github.com/ariffazil/AAA` |
| **arifOS** | Constitutional kernel, F1–F13 floors, 9-Organ Canon, MCP runtime | `/root/arifOS/` | `github.com/ariffazil/arifOS` |
| **WEALTH** | Capital intelligence, finance, NPV/EMV, credit, portfolio | `/root/WEALTH/` | `github.com/ariffazil/wealth` |
| **GEOX** | Earth domain, geoscience, petrophysics, seismic, mapping | `/root/geox/` | `github.com/ariffazil/geox` |
| **A-FORGE** | TypeScript execution bridge, planning twin, agent engine | `/root/A-FORGE/` | `github.com/ariffazil/A-FORGE` |
| **arif-sites** | Websites, static pages, web-facing assets | `/root/arif-sites/` | `github.com/ariffazil/arif-sites` |
| **ariffazil** | Personal profile, public meta root | `/root/repos/ariffazil/` | `github.com/ariffazil/ariffazil` |

---

## MANDATORY DECISION PROCEDURE

Before **any** write, branch, or push:

```
1. CLASSIFY → State exactly one primary repo
2. FORMAT  → REPO=<name>; CONFIDENCE=<0.00–1.00>; BASIS=<short reason>
3. VERIFY → Confirm git remote URL and working directory match target repo
4. CHECK  → confidence < 0.90? → STOP. Ask for confirmation.
5. BRANCH → Always create feature branch. Never touch main directly.
6. COMMIT → Include REPO= trailer in commit message
7. PR     → Open PR with: why this repo is correct target
```

**If workspace and remote do not match → STOP. Do not patch files in wrong checkout.**

---

## CONFIDENCE THRESHOLDS

| Score | Action |
|-------|--------|
| ≥ 0.95 | Proceed autonomously |
| 0.90–0.94 | Proceed, note uncertainty in PR |
| 0.80–0.89 | Proceed with explicit Arif confirmation |
| < 0.90 + multi-repo | 888_HOLD. Produce split plan. |
| < 0.80 | Refuse. Escalate. |

---

## CROSS-REPO RULES

- **Single-task**: One primary repo. Pick the most specific fit.
- **Multi-repo**: Stop. Produce one PR per repo. Do not merge scopes.
- **"None fit"**: Never create a new repo for convenience. Escalate.
- **"Temporarily in AAA"**: Only for governance, ADR, or routing policy material.

---

## COMMIT/PUSH RULES

### ✅ Allowed autonomously
- Read, classify, branch, edit, test, commit, open PR
- Switch workspaces safely (git stash + cd)
- Create routing constitution / skill files

### 🚫 NOT allowed autonomously
- Direct push to `main` / `master`
- Force push (`git push --force`)
- Secret, credential, or `.env` changes
- Org/repo settings changes
- Cross-repo migrations
- Delete operations (`rm -rf`, `DROP TABLE`)
- Any action where `REPO=` does not match the actual remote

### 🛑 888_HOLD trigger conditions
- Ambiguous repo classification
- Cross-repo scope detected
- Any irreversible or secret-adjacent action
- VPS workspace switch mid-task

---

## OUTPUT FORMAT — MANDATORY BEFORE ANY WRITE

```
══════════════════════════════════════
REPO=          ← exact repo name
CONFIDENCE=    ← 0.00–1.00
REMOTE_OK=     ← yes | no (remote URL matches REPO)
WORKTREE_OK=   ← yes | no (pwd matches REPO workspace)
ACTION=        ← proceed | hold | escalate
══════════════════════════════════════
```

---

## PRE-PUSH HOOK (mechanical backstop)

A `pre-push` git hook validates:
1. `REPO=` trailer present in commit message
2. Remote URL repo matches declared `REPO=`
3. Not pushing directly to main

Hook location: `.git/hooks/pre-push` (or CI-gated equivalent)
If hook fails → push rejected, agent reports mismatch.

---

## OPENCLAW AGENT BINDINGS

| Agent | Default Workspace | Scope |
|-------|-----------------|-------|
| `governor` | `/root/AAA/` | Routing policy, governance, ADRs |
| `builder-arifos` | `/root/arifOS/` | arifOS kernel, floors, MCP tools |
| `builder-wealth` | `/root/WEALTH/` | Capital intelligence tools |
| `builder-geox` | `/root/geox/` | Earth domain tools |
| `builder-forge` | `/root/A-FORGE/` | TypeScript bridge, agent engine |
| `builder-sites` | `/root/arif-sites/` | Web assets, static pages |

Each builder **may not** operate outside its designated workspace unless routed through `governor`.

---

## HERMES PROFILE CLUSTERS

| Profile | Repo Focus | Skills |
|---------|-----------|--------|
| `hermes-arifos` | arifOS | arifos, arifos-deploy, vault999 |
| `hermes-wealth` | WEALTH | wealth, finance |
| `hermes-geox` | GEOX | geox, geo-vision |
| `hermes-forge` | A-FORGE | a-forge-*, claude-code |
| `hermes-sites` | arif-sites | site-manager, cloudflare-pages |

---

## FAILSAFE

If wrong-repo risk exists at any point:
1. Do nothing except the mismatch report
2. Propose correct repo/path
3. Wait for Arif confirmation before proceeding

**No guessing. No "close enough." No silent corrections.**

---

*Last updated: 2026-05-02. Routing intelligence — DITEMPA BUKAN DIBERI.*
