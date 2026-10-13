# GEOX README Alignment Audit — 2026-10-08 (FI-008)
**Scope:** README.md vs codebase + live runtime (:8081) + git/system state · repo `github.com/ariffazil/GEOX` (PUBLIC, HTTP 200)
**Action:** commit `3fcccb10` on local `main` (ahead of origin by 2 — **push HELD**, see binary below). Status generator fixed in same commit.

## Verified TRUE in the pasted README (kept, now live-probed)
- Canonical 27 = live 27, drift 0, gap 0, ok true · internal tools 39 · discovery profiles 15/21/22/22 · 5 unpacked tools confirmed · surfaces 6/6 in sync (`generate_all_surfaces.py --check` PASS).

## Found STALE / WRONG → FIXED
1. **Status block snapshot** predates three deploys: claimed runtime `geox-b0026426` on a feature branch; live runtime is `geox-3c2d4dc1` (on source lineage, BEHIND HEAD `d4cfd7c7` — redeploy pending). Regenerated via the sanctioned `generate_readme_status.py`.
2. **Generator itself lied while probing truth**: hardcoded suffixes "`public_count_target` held at 31 by sovereign decision" and "feature branch by design" were emitted regardless of probe result. Fixed: both clauses now computed. (`--check` mode has a pre-existing timestamp quirk — it reports STALE a minute after any regen; not fixed today, cosmetic.)
3. **`public_count_target: 31` defect row was resolved same day it was written** (commit `78604549`, 2026-10-03, target→27, attestation `ok=True`). Moved to the resolved list.
4. **capability_registry drift understated**: not just research→26 — ALL FOUR profile counts stale (13/19/26/26 vs true 15/21/22/22). Row corrected.

## Found MISSING (the "entire reality" gaps) → ADDED
5. **Data-provenance table omitted 6 of 9 basin packs**, including the one the repo's own scan marks **CRITICAL**: `kinabalu_basin/` carries **internal PETRONAS well-evaluation values in this public repo** (WCR Rotan-1 reference, TD 2141 MD/2114.7 TVDSS, MD formation picks, GWC 2072.1 MD, PDA biostrat ages — committed at `17802197`, live on GitHub main; scan 2026-10-03 report-only). Now the headline row of the table and the #1 open defect.
6. **Scan-coverage gap (new finding)**: `sabah_basin/` claims CLM-NWS-004..008 cite the internal "GEOX Kinabalu Basin Geologist Dossier (Fig. 8, p. 25)" but were NOT itemized in the 2026-10-03 scan. Flagged same-class until scanned.
7. East-Sabah relay family (`dangerous_grounds`, `layang_layang_basin`, `sabah_trough`, `northwest_borneo_trough`, `sabah_two_oceanics.yaml`) and the new **public-safe** `east_sabah_dg_models/` pack now listed with honest classes.
8. `/health` oracle tautology re-observed live today (`deployment_drift` probe ReadTimeout) — row annotated with fresh evidence.

## Working-tree state (not README's to carry; recorded here)
- Local `main` ahead 2 (`d4cfd7c7` governance sensor fix — other session; `3fcccb10` this audit). **Neither pushed.**
- Uncommitted: 13 modified + 3 untracked files from other sessions (apps manifests, kinabalu_xs, igrf adapters, pyproject) + this session's kinabalu claims kin_clm_12–16 (**PETRONAS INTERNAL — must not be pushed** before the confidentiality decision) + `east_sabah_dg_models/` (public-safe).

## F13 BINARY HELD FOR ARIF (one decision)
The Rotan-1 WCR-derived values are **already public on GitHub main** (pushed before today; scan flagged it, report-only). Options:
- **(a) Purge** — remove values from packs + history rewrite (force-push; breaks clones; scan rows then resolve).
- **(b) Retain documented** — accept the public exposure with provenance stated (current README posture after this commit).
Push of the alignment commit (and everything behind it) waits on this call. No other action blocked.

## Receipts
- Commit `3fcccb10` (README + generator; person-data/supply-chain/musyawarah pre-commit gates PASSED)
- Live probes 2026-10-08 ~07:2x–07:3x Z: `/health`, `/drift`, `surface_attestation()`, `tools_for_profile`, `generate_all_surfaces.py --check`
- Scan: `reports/readme_harden/2026-10-03_confidentiality_scan.md` (already public in-repo)
