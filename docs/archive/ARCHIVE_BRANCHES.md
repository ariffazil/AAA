# AAA Branch Unification Audit — Horizon 2026-05-07

> **DITEMPA BUKAN DIBERI** — Intelligence is forged, not given.
>
> This document is the canonical audit of all active AAA branches, their
> relationship topology, diff contrast analysis, and the unification plan that
> produced the `aaa-unified-horizon` integration branch.

---

## 1. Branch Topology Map

```
main (canonical) ─┬── canon/hermes-memory-v1 (2 commits) ─┬── h1-roadmap-1778019221 (+1 commit)
                  │                                       │
                  │                                       └── adr/013-federation-phase2 (+6 commits)
                  │
                  ├── master (orphaned — 15 commits, NO common ancestor)
                  │
                  └── openclaw-unified (orphaned — 968 commits, NO common ancestor)
```

### Shared-History Branches (fast-forward compatible)

| Branch | Base | Ahead of main | Behind main | Contains |
|--------|------|---------------|-------------|----------|
| `canon/hermes-memory-v1` | `main` | 2 | 0 | WAJIB secrets audit + daily backup |
| `h1-roadmap-1778019221` | `canon/hermes` | 3 | 0 | ↑ + H1–H4 roadmap |
| `adr/013-federation-phase2` | `h1-roadmap` | 9 | 0 | ↑ + ADR-012 + ADR-013 + A2A fix + Cockpit + SEARAH |

> **Key finding:** `adr/013-federation-phase2` is a **strict superset** of the other
> two feature branches. Merging it fast-forwards `main` cleanly — no conflicts.

### Orphaned Branches (no common ancestor with main)

| Branch | Root commits | Files | Delta vs main | Nature |
|--------|-------------|-------|---------------|--------|
| `master` | `fcd6a15` | ~800 | -98,891 / +4,276 | Legacy workspace snapshot (pre-AAA React app era) |
| `openclaw-unified` | `8888b06`, `485071c` | 3,669 | +854,218 / -110,683 | Full federation workspace snapshot (alternative directory layout) |

---

## 2. Diff Contrast Audit

### 2.1 adr/013-federation-phase2 vs main

**Merge type:** `fast-forward` — zero risk.

**Files changed (16 total):**

| Path | Change | AAA Relevance |
|------|--------|---------------|
| `.github/workflows/secrets-audit.yml` | +151 lines | CI gate — WAJIB secrets audit |
| `.pre-commit-config.yaml` | +19 lines | Pre-commit hooks alignment |
| `.secrets.baseline` | +239 lines | detect-seeds baseline |
| `ADR/ADR-012-A2A-MESH-GOVERNANCE.md` | **new** | Constitutional ADR — A2A mesh protocol |
| `ADR/ADR-013-FEDERATION-PHASE2-BLUEPRINT.md` | **new** | Constitutional ADR — Phase 2 federation architecture |
| `ROADMAP.md` | **new** | H1–H4 strategic roadmap |
| `a2a-server/server.js` | +173 / -15 | A2A server hardening (404 fix, route ordering) |
| `a2a-server/vault.js` | +51 / -? | Vault integration updates |
| `agi-stack/rotate-keys.sh` | ±6 lines | Key rotation script updates |
| `hooks/pre-commit-secret-scan` | **new** | Local pre-commit secret scanner |
| `memory/2026-05-06-searah-deep-dive.md` | **new** | SEARAH investigation log |
| `memory/investigations/SEARAH-TRUTH-DB.md` | **new** | SEARAH evidence database |
| `memory/investigations/SEARAH-TRUTH.md` | **new** | SEARAH truth findings |
| `skills/mmx/SKILL.md` | **new** | MMX skill definition |
| `src/Cockpit.tsx` | +396 / -98 | Cockpit UI enhancements |

**Verdict:** ✅ **Clean merge.** All changes are additive or surgical. No deletions of existing AAA surface.

---

### 2.2 master vs main (orphaned — DO NOT MERGE)

**Merge type:** `unrelated histories` — would require `--allow-unrelated-histories`.

**Risk assessment:** 🔴 **HIGH RISK / DESTRUCTIVE**

`master` is missing 586 files that exist in `main`, including the entire modern AAA React app
surface (`src/Cockpit.tsx`, `src/App.tsx`, `package.json`, `vite.config.ts`, `a2a-server/`,
`ADR/`, `AAA/`, etc.). A naive merge would **delete** these files.

**Unique files in master worth preserving (74 total):**

| Path | Value | Action taken |
|------|-------|--------------|
| `docs/WATCHDOG.md` | Observability spec | Extracted to `archive/legacy-master/docs/` |
| `arifOS-sentinel/HERMES_ASI_MEMORY.md` | ASI memory model | Extracted to `archive/legacy-master/arifOS-sentinel/` |
| `memory/2026-04-*.md` (40+ files) | Historical daily logs | Available in `master` branch; not extracted to avoid noise |
| `memory/2026-03-31-*.md` | Early migration logs | Available in `master` branch |

**Verdict:** ❌ **Do not merge.** Treat as archive. Valuable artifacts extracted surgically.

---

### 2.3 openclaw-unified vs main (orphaned — DO NOT MERGE)

**Merge type:** `unrelated histories` + **structural incompatibility**.

**Risk assessment:** 🔴 **CRITICAL / STRUCTURAL MISMATCH**

`openclaw-unified` has **zero** common files with `main` at matching paths:
- No `src/Cockpit.tsx` — the AAA React app does not exist in this branch.
- No `AAA/` directory — AAA governance docs absent.
- No `ADR/` directory — ADRs absent.
- Root-level `AGENTS.md` is the **workspace** AGENTS.md (arifOS kernel), not the AAA project AGENTS.md.
- `package.json` exists under `arifosmcp/packages/npm/`, not at repo root.

**What openclaw-unified actually is:**
A snapshot of the **entire `/root` workspace** (arifOS, A-FORGE, GEOX, WEALTH, WELL, HERMES)
using the workspace root as the repo root. It is an **alternative repository topology**, not a
superset of AAA.

**Unique files worth preserving:**

| Path | Value | Action taken |
|------|-------|--------------|
| `.agents/rules/arifOS.md` | Agent rules for arifOS | Extracted to `archive/legacy-openclaw/.agents/rules/` |
| `.agents/workflows/*.md` (8 files) | Agent workflow definitions | Extracted to `archive/legacy-openclaw/.agents/workflows/` |
| `ADVERSARIAL_TESTS.md` | Test matrix | Extracted to `archive/legacy-openclaw/` |
| `ARCHITECTURE_TRUTH.md` | Architecture doctrine | Extracted to `archive/legacy-openclaw/` |
| `CHANGELOG.md` | Historical changelog | Extracted to `archive/legacy-openclaw/` |

**Verdict:** ❌ **Do not merge.** Treat as workspace snapshot archive. Key agent workflows
extracted for reference.

---

## 3. Unification Strategy

### What was unified

The `aaa-unified-horizon` branch was created from `adr/013-federation-phase2` and
contains:

1. ✅ **All feature branch work** (canon/hermes + h1-roadmap + adr/013)
2. ✅ **Key legacy documents** from `master` (docs/WATCHDOG.md, HERMES_ASI_MEMORY.md)
3. ✅ **Key agent workflows** from `openclaw-unified` (`.agents/` rules + workflows)
4. ✅ **Key architecture documents** from `openclaw-unified` (ADVERSARIAL_TESTS.md,
   ARCHITECTURE_TRUTH.md, CHANGELOG.md)

### What was NOT unified (and why)

| Excluded content | Reason |
|------------------|--------|
| `master` full merge | Would delete 586 modern AAA files (no common ancestor) |
| `openclaw-unified` full merge | 3,669 files with zero path overlap; would create parallel universe |
| Old `memory/` entries from `master` | Historical noise; kept accessible in `master` branch |
| `00_legacy_materials/` from `openclaw-unified` | Explicitly named legacy; superseded by `main` |

---

## 4. Recommended Next Steps

### Immediate (this PR)
1. Merge `aaa-unified-horizon` → `main` (fast-forward of feature work + additive archives)
2. Tag `master` as `archive/master-2026-04-25` before any future deletion
3. Tag `openclaw-unified` as `archive/openclaw-unified-2026-05-02` for preservation

### Post-merge governance
4. Delete stale remote branches after sovereign confirmation:
   ```bash
   git push origin --delete canon/hermes-memory-v1
   git push origin --delete h1-roadmap-1778019221
   # adr/013-federation-phase2 can be deleted after PR merge
   ```
5. Keep `master` and `openclaw-unified` as **read-only archives** until Horizon H2 review.

---

## 5. Branch Registry (Canonical)

| Branch | Type | State | Disposition |
|--------|------|-------|-------------|
| `main` | Canonical | Active | **Keep** — primary line |
| `aaa-unified-horizon` | Integration | Proposed | **Merge** via PR → main |
| `adr/013-federation-phase2` | Feature | Superseded | **Delete after merge** |
| `h1-roadmap-1778019221` | Feature | Superseded | **Delete** (subset of adr/013) |
| `canon/hermes-memory-v1` | Feature | Superseded | **Delete** (subset of h1-roadmap) |
| `master` | Orphan / Archive | Frozen | **Tag + preserve read-only** |
| `openclaw-unified` | Orphan / Snapshot | Frozen | **Tag + preserve read-only** |

---

*Audit generated: 2026-05-07 by workspace agent.*
*Methodology: `git merge-base`, `git diff --stat`, `git ls-tree`, path analysis,*
*conflict simulation, and surgical artifact extraction.*
