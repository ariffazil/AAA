# GEOX Prep Evidence Pack — 2026-10-01
# Lane: 777a
# Purpose: Stage F13 binary for Arif on commit/push/redeploy/seal
# Status: read-only evidence. No production artifact mutated.

Epistemic labels: OBS = observed by direct probe, DER = derived from OBS, INT = interpretation, SPEC = speculation.
Every finding carries a literal path (file:line) or live-probe source.

---

## Section A — Local CI gate state  [OBS]

Command: `cd /root/GEOX && PYTHONPATH=src python3 scripts/generate_all_surfaces.py --check`
Exit code: **0**
Verdict line: **PASS — every surface is in sync with registry.py. No drift.**
Truth source: `registry.py::CANONICAL_PUBLIC_TOOLS`, Truth count = **26**, hash fn = sha256 (timestamp-normalised content).

Per-surface hash table (gate output = timestamp-NORMALISED content sha256):

| Surface | Gate (normalised) sha256[:16] | Status |
|---|---|---|
| tools_sot.yaml | b0a5b2fb75f4ede4 | OK |
| CANONICAL_PUBLIC_SURFACE.json (src/geox_mcp/generated/) | 7e891bec69f927a6 | OK |
| tools.json | eb194f9dec69d420 | OK |
| llms.txt | 555726b9b4a18936 | OK |
| contracts/tools.yaml | fc961faaad5da2ce | OK |
| README.md | b6f61f43fba95d5c | OK |

Surfaces checked 6 / Missing 0 / Drifted 0 → GATE PASS.

Raw on-disk sha256 (byte-for-byte, NOT normalised — these differ from gate hashes because generators embed `datetime.now()` stamps; the gate deliberately normalises clock churn — see scripts/generate_all_surfaces.py:483-523):
- tools_sot.yaml d5491d7fa0a8cfc5d39fe65cc54fde735018734fe489fec3b1d078ded6ead18b
- src/geox_mcp/generated/CANONICAL_PUBLIC_SURFACE.json 387e452a152e91c7bf81a8a796709b3fa1e3f8076689b3b0c1299bcce0773349
- tools.json 4b10fbba6a18ab0bace5c7ca7afc2297609c66e5f937cea94878c4926b9e738b
- llms.txt 14da26e66a974b60c1f6aac5fac2ba780a848e78bc7fb6df5bd807c516b563be
- contracts/tools.yaml 31832858d5ff12e582466b2369aeaf3ae561dd9b895a7d26fe530f141d76a994
- README.md 934551c1fc5d600cde98d340d189b50394750387b339fd1ac14398addea7548d

DRIFT NOTE (badge URL, not caught by gate): README.md:3 badge IMG URL still reads `GEOX-31_Canonical_Tools` while alt-text reads `GEOX-26`. The generator's badge regex (scripts/generate_all_surfaces.py:435-441) only rewrites the human-readable `GEOX-\d+ Canonical Tools` (alt-text) and never the URL slug `GEOX-\d+_Canonical_Tools`. So the gate hashes a README whose alt-text says 26 but whose rendered badge still says 31. PASS is real for the 6 tracked surfaces; the badge URL is a cosmetic-but-wrong residual. [OBS + DER]

READ-ONLY PROOF: run_check (scripts/generate_all_surfaces.py:560-633) documents "No file is written by this function" and drives every generator through `_render_surface(..., dry_run=True)` (lines 533-557). /root/GEOX mtimes unchanged after my invocation (tools.json/tools_sot.yaml stayed 20:07:40, README.md stayed 19:55:32; my run was ~20:26). [OBS]

---

## Section C — /opt/geox dirty files inventory  [OBS]

`git -C /opt/geox status --porcelain` → **40 lines**: 26 MODIFIED (M) + 14 UNTRACKED (??).
`/opt/geox` HEAD = 7027ff64d4210cf5a9d624a724f13692469f3eb1, branch main.
diffstat: 26 files changed, 1251 insertions(+), 692 deletions(-).

### MODIFIED (26) — sha256 working-tree vs HEAD, byte sizes

| # | path | WT sha256 | HEAD sha256 | bytes WT→HEAD | RISK CLASS |
|---|---|---|---|---|---|
| 1 | .git_commit | 12d9c0fb… | 65437d1d… | 9→8 | DESCRIPTOR (deploy stamp) |
| 2 | .well-known/openapi.json | e2b3b52e… | 50393826… | 27620→20672 | DESCRIPTOR |
| 3 | .well-known/tools.json | f92f533d… | 3d4f7fbf… | 35983→29583 | DESCRIPTOR |
| 4 | llms.txt | 9b5ccfcb… | f927f4a8… | 4992→7173 | DESCRIPTOR |
| 5 | src/geox_core/engines/vision/mimo_vlm_adapter.py | 6e61782d… | 939f3cf9… | 29889→29451 | RUNTIME (core engine) |
| 6 | src/geox_core/engines/vision/minimax_vlm_adapter.py | 57ceb04c… | 15b86950… | 26221→25783 | RUNTIME (core engine) |
| 7 | src/geox_core/integrations/arifos_governance.py | b6777075… | 62e71fd3… | 14330→14114 | RUNTIME (governance) |
| 8 | src/geox_core/services/asset_memory.py | 52e048d0… | b8bbb01e… | 10909→9187 | RUNTIME (service) |
| 9 | src/geox_core/services/eia_client.py | 20d92b32… | 1234d71d… | 12531→12315 | RUNTIME (service) |
| 10 | src/geox_core/services/npd_client.py | 1e5d8b12… | 38832e32… | 12106→11890 | RUNTIME (service) |
| 11 | src/geox_core/services/spglobal_client.py | cc4380ac… | 2b94146a… | 15470→15254 | RUNTIME (service) |
| 12 | src/geox_mcp/geox_middleware.py | 0f952617… | f51f022d… | 61959→60119 | **RUNTIME-CRITICAL (hot-load)** |
| 13 | src/geox_mcp/server.py | 13b066e0… | fc412156… | 176416→180897 | **RUNTIME-CRITICAL (hot-load)** |
| 14 | src/geox_mcp/session_enforcement.py | 7e9e5c1b… | ab0eeb44… | 26313→26300 | **RUNTIME-CRITICAL (hot-load)** |
| 15 | src/geox_mcp/tools/claim_unified.py | 55ed9162… | ad0de99d… | 36252→35514 | RUNTIME (tool) |
| 16 | src/geox_mcp/tools/earth_map.py | e49a7da3… | c182b965… | 44419→44273 | RUNTIME (tool) |
| 17 | src/geox_mcp/tools/macrostrat_client.py | a8eac80f… | 1126b24b… | 22660→22444 | RUNTIME (tool) |
| 18 | src/geox_mcp/tools/mcp_apps_bridge.py | 5d8073a2… | 888c4db9… | 63289→62031 | RUNTIME (tool) |
| 19 | src/geox_mcp/tools/section_render.py | b6757aa8… | 6edbff52… | 14164→14096 | RUNTIME (tool) |
| 20 | src/geox_mcp/tools/seismic_interpret.py | 541679e9… | e17e74bd… | 57307→56724 | RUNTIME (tool) |
| 21 | src/geox_mcp/tools/structure_gates/__init__.py | 6b9d2e73… | 66acd98c… | 16735→7181 | RUNTIME (tool, +9554 bytes) |
| 22 | src/geox_mcp/tools/wealth_bridge_tool.py | d1db1d4d… | 882aa5d8… | 17906→17690 | RUNTIME (tool) |
| 23 | src/geox_mcp/tools/well_1d_surface.py | dadf936e… | 7d160576… | 12560→12519 | RUNTIME (tool) |
| 24 | src/geox_mcp/tools_manifest.yaml | d8179697… | 5ffb1a80… | 59218→60100 | DESCRIPTOR (manifest) |
| 25 | src/geox_mcp/tools_wiring.py | 266b6e42… | eb4766a7… | 335878→335549 | RUNTIME (wiring) |
| 26 | tools.json | 46487c6c… | f5e54432… | 3384→3601 | DESCRIPTOR |

### UNTRACKED (14) — a redeploy `git clean`/checkout would DELETE these

- data/dde_cache/  (directory)
- ingest/seismic_arif_2026-09-25.webp
- src/geox_core/engines/seismic/axis_cd_population.py
- src/geox_core/httpx2_shim.py
- src/geox_core/ontology/tectonic_events/regime_invariants.yaml
- src/geox_core/ontology/tectonic_events/regime_loader.py
- src/geox_core/vision_structural/  (directory)
- src/geox_mcp/prompts/structural_invariants.py
- src/geox_mcp/servers/structural_vision.py
- src/geox_mcp/servers/structural_vision_wiring.py
- src/geox_mcp/tools/geox_glof.py
- src/geox_mcp/tools/structural_vision.py
- src/geox_mcp/tools/structure_gates/axis_b_isochore.py
- src/geox_mcp/tools/structure_gates/tectonic_regime.py

Risk-class roll-up of /opt/geox 40 dirty files [DER]:
- RUNTIME-CRITICAL (hot-load): 3 → geox_middleware.py, server.py, session_enforcement.py
- RUNTIME (other src/ code): 13
- DESCRIPTOR (.well-known/, tools.json, llms.txt, manifest, .git_commit): 7
- UNTRACKED new source (would be lost on clean checkout): 10 code/data files + 2 dirs
- DOCUMENTATION: 0 modified in /opt/geox (no .md dirty)
- CONFIG (yaml outside src/): 0 (tools_manifest.yaml is inside src/, classed DESCRIPTOR)

NOTE: /opt/geox tree is a DIFFERENT lineage than /root/GEOX (see Section D). These 26 modified files are opt-side local edits NOT present as commits in /root/GEOX. A redeploy from /root/GEOX over /opt/geox would clobber all 26 opt-local modifications AND delete the 14 untracked opt-local files. [DER]

---

## Section D — Runtime vs source divergence  [OBS + DER] — MOST IMPORTANT

Inputs:
- /opt/geox HEAD = 7027ff64d4210cf5a9d624a724f13692469f3eb1 (branch main, 1442 commits)
- /root/GEOX HEAD = 17802197d9c4c81de19403125c32bd09736347ae (branch main, 1521 commits)
- Both remotes = https://github.com/ariffazil/GEOX.git (same origin). [OBS]

### Mutual non-existence (pre-fetch)
- `git -C /root/GEOX merge-base 7027ff64 HEAD` → `fatal: Not a valid commit name`, EXIT 128. [OBS]
- `git -C /opt/geox merge-base 17802197 HEAD` → `fatal: Not a valid commit name`, EXIT 128. [OBS]
- `git cat-file -t` on each other's HEAD in the foreign repo → "could not get object info". The two working copies had NOT fetched each other's objects. [OBS]

### After sanctioned fetch (`git -C /root/GEOX fetch /opt/geox` — objects + FETCH_HEAD only, no branch moved)
- merge-base now resolves: **d353dd12f351d0160938edbaed6ee4be2df42cbc** (2026-09-08, "seal-all 2026-09-08: borneo2023 datum…"). [OBS]
- Divergence: /root/GEOX is **105 commits ahead** of merge-base; /opt/geox is **26 commits ahead**. Common point = 2026-09-08. The two mains forked ~3.5 weeks ago and never re-converged. [DER]

### Are the 26 opt-side commits already in root? (git cherry)
`git -C /root/GEOX cherry -v HEAD 7027ff64 d353dd12` → **22 of 26 are patch-equivalent (`-`)** already present in /root/GEOX under different SHAs (the af-fix #1–#6 series, D1/D2/D3, basin forges). **4 are NOT (`+`)** — unique to opt-side, absent from /root/GEOX:
- 0bd605767 refactor(registry): regenerate tools manifest/SOT + drop stale .bak/.patch wiring
- 73fb8977a fix: remove accidental app gitlink (embedded repo); ignore app/
- b0508ff75 docs(geox): regenerate canonical public surface 20 -> 25
- d669605c9 fix(geox/prospect): flag pos_default_heuristic on preview path (555-ASI verify finding)
[OBS]

Two of the four unique opt commits (`0bd60576` registry regen, `b0508ff7` surface 20→25) touch exactly the surface/registry area /root/GEOX has since redone at 26. They are plausibly superseded, not additive. The other two (`73fb8977` gitlink ignore, `d669605c` prospect heuristic flag) may carry opt-local intent not reflected in root. [INT]

### Runtime-critical file history (geox_middleware.py, server.py)

`src/geox_mcp/geox_middleware.py` last 5 — /root/GEOX side:
- 79e372e5 (2026-09-30) merge feat/mcp-dual-era → main — canonical surface reconcile
- 1e4f44e2 (2026-09-30) style(G) ruff clean 166→0
- b5bf3c06 (2026-09-18) seal: GEOX cleanup + vision/integration hardening
- a76acf27 (2026-09-18) fix(geox): audit-layer + wire-contract conformance
- d223f3d2 (2026-08-26) feat(authority): C3 carry validated SCT authority context

`src/geox_mcp/geox_middleware.py` last 5 — /opt/geox side:
- 0bd60576 (2026-09-18) refactor(registry): regenerate tools manifest/SOT + drop stale wiring  [opt-UNIQUE]
- d223f3d2 (2026-08-26) feat(authority): C3  [shared with root]
- 6406e8d0 (2026-08-12) fix(governance): mandatory content_sha256
- 55fa8141 (2026-08-10) fix(geox): MCP error code -32002→-32602 (SEP-2164)
- e903976c (2026-08-10) feat: HTTP-level auto-mint

`src/geox_mcp/server.py` last 5 — /root/GEOX side:
- 7750a2b3 (2026-09-19) feat(glof): collapse 7 cascade tools → 1 unified geox_glof (7→1, public surface 31→25)
- 0dee4d49 (2026-09-18) chore: server.py update (+5 lines)
- 7e7b5ed0 (2026-09-18) fix(geox): audit entropy reduction — CSP contract, Dockerfile, server.py count
- 6d55a682 (2026-09-15) feat(geox-mcp): dual-era MCP transport — stateless 2026-07-28 + legacy
- 24308677 (2026-09-09) fix(glof): structured input gate

`src/geox_mcp/server.py` last 5 — /opt/geox side:
- 0bd60576 (2026-09-18) refactor(registry)  [opt-UNIQUE]
- 3be2d283 (2026-09-09) fix(glof): structured input gate
- e16c95cb (2026-09-06) fix(mcp): restore map/basin/deep_time/geomechanics evidence path
- a5cbbbb9 (2026-09-06) fix(Z2): remove stale geox_workspace + real freshness timestamps
- 757af762 (2026-09-04) fix(mcp): accept protocol 2025-03-26 in version gate

### Content divergence on the two runtime-critical files
- MB→opt: geox_middleware.py +57 lines, server.py +66 lines (2 files, 110 ins, 13 del). [OBS]
- MB→root: geox_middleware.py +116 lines, server.py +245 lines net (2 files, 196 ins, 165 del — server.py heavily rewritten). [OBS]
- root HEAD vs opt HEAD, whole tree: **814 files differ**, 4620 insertions / 1,746,562 deletions. The deletion mass is almost entirely `.ua/` (−1,713,715 lines) — a knowledge-graph extract cache present in /root/GEOX but ABSENT from /opt/geox HEAD. src/ net −16,938, tests −7,053. [OBS + DER]

### DIVERGENCE VERDICT
/root/GEOX and /opt/geox are **two genuinely forked lineages** off a 2026-09-08 ancestor, both claiming branch `main`, both pointing at the same GitHub origin. They are NOT one-ahead-of-the-other; each carries commits the other lacks (root +105, opt +26). 22/26 opt commits are already patch-present in root; **4 opt commits are unique** and would be LOST by a naive "deploy /root/GEOX over /opt/geox". Compounding: /opt/geox also holds **26 uncommitted modifications + 14 untracked files** (Section C) on top of its forked HEAD.

REDEPLOY SAFETY = **NOT SAFE as a blind overwrite.** A redeploy that checks out /root/GEOX main onto /opt/geox would: (a) discard 4 opt-unique commits, (b) clobber 26 opt-local uncommitted edits including 3 hot-load RUNTIME-CRITICAL files, (c) delete 14 untracked opt files. This is the classic source≠runtime deployment-drift scar. The correct move is a merge/rebase reconciliation of the fork, not a copy — and that reconciliation is F13-class (canonical records + irreversible mutation surface). [DER + INT]

### Live-runtime identity — a THIRD, contradictory stamp set  [OBS]
`curl :8081/health` (live process) reports: status=healthy, kernel_verdict=**HOLD**, version=v2026.08.26, tools_loaded=26, canonical_tools=26, surface_drift{canonical 26, live 26, drift_count 0, ok true}, deployment_drift{source_commit=297abcb…, built=297abcb, deployed=297abcb, drift=false, status=aligned, source=arifOS:/api/build}, git_version=**geox-3f344b84**.
- git_version 3f344b84 = opt-side commit "fix(basin-unified): icgem dispatcher…" (2026-09-30 18:15) — an ancestor inside opt history, NOT opt HEAD (7027ff64). [OBS]
- /opt/geox/.git_commit file = **7750a2b3** (root-side commit "feat(glof) collapse 7→1, surface 31→25", 2026-09-19) — a DIFFERENT stamp again. [OBS]
- deployment_drift.source_commit **297abcb04afd…** = `fatal: Not a valid object name` in BOTH /root/GEOX and /opt/geox. The commit the live health endpoint claims to be deployed does not exist in either GEOX repo — it is a phantom/foreign stamp (likely an arifOS build-registry id, per `source: arifOS:/api/build`). [OBS + DER]

So ONE running process advertises THREE mutually-inconsistent commit identities (3f344b84 / 7750a2b3 / 297abcb-phantom) and self-reports deployment_drift=false "aligned" while doing so. kernel_verdict=HOLD. This is the "alive ≠ healthy / stamp ≠ truth" scar class. The live process's own drift self-report cannot be trusted as redeploy authorization. [DER + INT]

---

## Section E — Boundary ratchet diagnosis  [OBS]

File: `/root/GEOX/.github/workflows/09-boundary-ratchet.yml` (1134 bytes, committed in HEAD).
Confirmed: committed merge-conflict markers at lines 26 / 29 / 32 — present in HEAD blob (`git show HEAD:…09-boundary-ratchet.yml | grep` finds them), NOT merely a dirty worktree. Introduced by commit **79e372e5** "merge: feat/mcp-dual-era-2026-07-28 → main — canonical surface reconcile (BL surface ruling 2026-09-30)". [OBS]

Both sides verbatim (the conflicted hunk is `jobs.ratchet.steps`, the checkout/setup-python action pins):

HEAD side (lines 27-28):
```
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
```
feat/mcp-dual-era-2026-07-28 side (lines 30-31):
```
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
```
Common (unconflicted) tail: `with: python-version '3.12'` → install grimp/import-linter → `python boundary/boundary_ratchet.py --repo-root .`. [OBS]

Which side is which: `<<<<<<< HEAD` = the branch the merge target had checked out = /root/GEOX main (current). `>>>>>>> feat/mcp-dual-era-2026-07-28` = the merged-in branch (the dual-era work Lane 333 confirmed "shipped, needs manifest wiring only"). [OBS]

### CONCURRENT-WRITER EVENT during this sweep  [OBS]
At my Section E read (~20:26) the file's mtime was Sep 30 23:51 and `git status` on it was clean (markers committed, worktree == HEAD). At 20:29:06 — AFTER my read, DURING this read-only lane — a separate process rewrote the file: mtime now 2026-10-01 20:29:06, `git diff` now shows `1 file changed, 5 deletions(-)`, markers GONE from disk, and the surviving content is the **HEAD side (checkout@v7 / setup-python@v7)**; the feat side (v4/v5) was deleted. HEAD blob still carries the markers; worktree is now Modified. This is not my mutation — I ran only `--check` (dry-run) and read commands. Another lane (likely 333d, whose surface-drift-gate.yml is also untracked here) resolved the conflict live under me. Evidence that the /root/GEOX worktree is being actively mutated by concurrent lanes while I observe it. [OBS + DER]

### RECOMMENDATION — which side is right  [INT]
**Keep the HEAD side (actions/checkout@v7, actions/setup-python@v5→v7).** Rationale:
1. The two sides differ ONLY in GitHub Action version pins (v7/v7 vs v4/v5). This is a dependabot-style version bump collision, not a semantic code difference. The repo already bumps the actions group (commit 46f22887 "bump the github-actions-official group"). Higher pin (v7/v7) is the forward choice.
2. The feat branch's substance (dual-era MCP transport) is already merged into main via 79e372e5 and — per Lane 333 — stateless_era.py already serves both eras, so the feat side carries no unique workflow logic worth preserving; only its stale action pins. Discarding the v4/v5 pins loses nothing functional.
3. The concurrent writer already made exactly this choice on disk (kept v7/v7, deleted v4/v5). The recommendation and the observed live resolution AGREE.
Action for Arif's binary: the on-disk resolution is correct but is an UNCOMMITTED worktree edit; HEAD still ships a broken YAML with markers. Committing the resolved file is required before any push — a workflow file with conflict markers is invalid YAML and would red the CI. That commit is part of the same F13-class "commit/push" binary. [INT + DER]

---

## Section F — README current state  [OBS + DER]

File: `/root/GEOX/README.md`
- sha256 (raw bytes): 934551c1fc5d600cde98d340d189b50394750387b339fd1ac14398addea7548d
- gate-normalised sha256[:16]: b6f61f43fba95d5c
- mtime: **2026-10-01 19:55:32 +0800**, size 17268 bytes, **345 lines**, 33 heading lines.
- Sections: Live reality / Problem / Architecture / Public surface (SOT) / Authority floor / Epistemic labels / Federation role / Documentation / License / Tool inventory / Integration / Failure model / Quickstart / Provenance / Recent changes / Compliance / Pointers.

Badge (README.md:3): `![GEOX-26 Canonical Tools](https://img.shields.io/badge/GEOX-31_Canonical_Tools-0b7285)`. Alt-text = 26, IMG URL slug = **31**. Mismatch. The generator self-heals alt-text but not the URL slug (scripts/generate_all_surfaces.py:435-441). [OBS]

### Does README reflect current truth? (README "Live reality" table, lines ~21-50)

| README claims | README says | LIVE probe says | Verdict |
|---|---|---|---|
| Canonical MCP tools | **31** (registry.py SOT) | :8081/health canonical_tools=**26**; worktree registry imports to **26** | **STALE — wrong** |
| Live tools observed | **25** on :8081/drift | :8081/drift live_count=**26**, drift_count=0, ok=true | **STALE — wrong** |
| Runtime on older commit e8e6f93 | claims `e8e6f93` not on branch | e8e6f93 = `fatal: Not a valid object name` in /root/GEOX; live git_version=3f344b84, .git_commit=7750a2b3, deployed=297abcb(phantom) | **STALE + phantom** |
| Generated manifests all 31 | claims tools.json/sot/CANONICAL/contracts all **31** | all now **26** (gate truth count 26) | **STALE — wrong** |
| Drift | "drift_count=0, gap_count=0, ok=true on deployed runtime" | live drift_count=0 ok=true (agrees) but on 26 not 31 | partially right, wrong count |
| Latest commit | does not name 17802197 anywhere | /root/GEOX HEAD = 17802197 | **not reflected** |
| The 5-tool gap narrative (lines ~46-50) | explains SOT 31 vs live 25 gap, lists 5 evidence-spine tools, says "redeploy → 31" | reality is the reverse: canonical is now **26**, live is **26**, no gap | **STALE — narrative obsolete** |

README FRESHNESS VERDICT = **STALE / SELF-CONTRADICTORY.** mtime is fresh (2026-10-01 19:55) but CONTENT is stale: it asserts a 31-canonical / 25-live / needs-redeploy world that the live runtime and the gate both contradict (26 / 26 / drift 0). It names a commit `e8e6f93` that does not exist in the repo. It does NOT reflect: 26 tools (says 31), does NOT reflect live drift=false correctly in count terms (says live 25), does NOT reflect live status:healthy accurately (health=healthy but kernel_verdict=HOLD — README says plain "healthy"), does NOT name latest commit 17802197. The badge URL still renders "31".

IMPORTANT for the F13 binary: the surface gate PASSED (Section A) because the gate only normalises + hashes the badge/heading fields it regenerates; it does NOT validate the prose "Live reality" table against the live runtime. So a green gate does NOT mean the README prose is true. The README's stale prose (31 vs 26) is a real defect the gate is blind to. If Arif seals on "gate PASS", the README will still ship asserting 31 tools. [DER + INT]

---

## Section G — SOT doc audit  [OBS + DER]

Generator rule string (canonical): scripts/generate_all_surfaces.py:4 and :628 — "registry.py is the ONLY truth. Every surface is GENERATED from it." Live worktree `registry.py::CANONICAL_PUBLIC_TOOLS` imports to **26**. That is THE canonical count. [OBS]

| File | Class | Why |
|---|---|---|
| src/geox_mcp/registry.py::CANONICAL_PUBLIC_TOOLS | **CANONICAL (THE source)** | Self-declared ONLY truth (generate_all_surfaces.py:4). Worktree imports to 26. Every surface derives from it. |
| tools_sot.yaml (root) | GENERATED | Header `sot_source: registry.py::CANONICAL_PUBLIC_TOOLS`, `public_count: 26`, `regenerated_by: generate_all_surfaces.py`. Gate-tracked, in sync. No deprecation self-decl in current header (earlier-session deprecation NOT present now). Do not hand-edit. |
| tools.json (root) | GENERATED | Gate-tracked surface #3, in sync. 26 tools. |
| llms.txt (root) | GENERATED | Header "Surface: generated from registry.py::CANONICAL_PUBLIC_TOOLS", "(26 Public Tools)". Gate-tracked, in sync. |
| contracts/tools.yaml | GENERATED | `canonical_tool_count: 26`. Gate-tracked, in sync. |
| src/geox_mcp/generated/CANONICAL_PUBLIC_SURFACE.json | GENERATED (canonical pack) | schema v2, 26 tools, gate-tracked, in sync. This is the CURRENT generated surface. |
| CANONICAL_PUBLIC_SURFACE.json (ROOT-LEVEL) | **STALE DUPLICATE** | schema v1, `generated_at 2026-09-19`, `public_count: 25`, `source: tools_manifest.yaml` (not registry.py). A second, older copy at repo root shadowing the generated/ one. Git-tracked. Contradicts the v2 (26). ARCHIVE CANDIDATE. |
| capability_registry.yaml (registry/) | CANONICAL for DISCOVERY (not tool count) | `manifest_version 2026.09.15-discovery-governance`. Governs pack VISIBILITY profiles (default 13 / specialist 19 / research 26 / full 26), not tool existence. research/full = 26 matches registry truth. Lane 333d's "advertises 26 for research but code returns 21" — the 26 claim is CORRECT vs current registry; the "21" would be a profile-visibility or live-observation discrepancy, not a registry mismatch. Not stale on count. |
| src/geox_mcp/tools_manifest.yaml | **STALE / CONFLICTING** | Header `public_count_target: 31`, `generated_from: MASTER FORGE W8 — restore 32-tool`, 87 name-hits. Asserts a 31/32-tool world. Contradicts registry's 26. NOT gate-tracked (gate tracks the 6 surfaces, not this). Root-level copy is ALSO dirty in /opt/geox (item 24). The manifest is the OLD authority the registry displaced; it still claims 31. ARCHIVE-or-REGEN CANDIDATE. |
| README.md | GENERATED(partial) + **STALE prose** | Badge/heading generator-managed; but prose "Live reality" table hand-written and STALE (31/25/e8e6f93). See Section F. |
| .well-known/mcp/server.json | **STALE DESCRIPTOR** | description: "Canonical surface: 31 public tools, 85 total registered (54 internal)", version 2026.09.18. Asserts 31. Contradicts 26. The disk-vs-wire drift Lane 555 caught: wire (:8081) says 26, disk descriptor says 31. NOT gate-tracked. ARCHIVE/REGEN CANDIDATE. |
| .well-known/tools.json | DESCRIPTOR (dirty in opt) | modified in /opt/geox (item 3). 26-hits high, 1 stale 31-hit. Mixed. |
| .well-known/openapi.json | DESCRIPTOR (dirty in opt) | modified in /opt/geox (item 2). |
| GEOX_MCP_APPS_SURFACE.json (root) | **STALE DESCRIPTOR** | `canonical_tools: 32`, 6 stale 31-hits. Asserts 32/31. Not gate-tracked. ARCHIVE/REGEN CANDIDATE. |
| apps.json (root) | DESCRIPTOR | 0×31, 2×26. Consistent-ish. MCP-Apps list, separate concept. |
| FEDERATION.md / FEDERATION_CONTRACT.md / AGENTS.md / CONTEXT.md / RUNBOOK.md | DOC (mixed) | CONTEXT.md and RUNBOOK.md each carry a stale "31" hit; FEDERATION/AGENTS consistent. Explainer tier per README provenance order (below gate). |
| docs/ (60+ md) | DOCUMENTATION | Not SOT. ARCHITECTURE/CAPABILITY_MAP/etc. — explainer tier, may carry stale counts, low authority. |

README provenance order (README.md:301-311), self-declared authority ranking:
1. `:8081/health` + `:8081/drift` (runtime truth, beats prose)
2. `registry.py::CANONICAL_PUBLIC_TOOLS` (gate-enforced surface)
3. `CANONICAL_PUBLIC_SURFACE.json` (generated from 2)
4. `FEDERATION_CONTRACT.md`
5. `arifOS/docs/FEDERATION.md`
6. README (explainer; gates beat it)

OBSERVATION: the live runtime (:8081) and the code SOT (registry.py) BOTH say 26. The stale artifacts (server.json 31, tools_manifest.yaml 31/32, GEOX_MCP_APPS_SURFACE.json 32, root CANONICAL_PUBLIC_SURFACE.json 25/v1, README prose 31) all disagree with both top-ranked authorities. Under the README's own provenance order, all of them are wrong. [DER]

### SOT REDUCTION PROPOSAL  [INT]

CANONICAL (1, keep as sole truth): registry.py::CANONICAL_PUBLIC_TOOLS (=26).

GENERATED-and-gate-enforced (6, keep, auto-regen, never hand-edit): tools_sot.yaml, tools.json, llms.txt, contracts/tools.yaml, src/geox_mcp/generated/CANONICAL_PUBLIC_SURFACE.json, README.md badge/heading.

ARCHIVE / REGEN CANDIDATES — files claiming tool-count authority but STALE and NOT gate-tracked (5):
1. CANONICAL_PUBLIC_SURFACE.json (root-level, v1, 25, sourced from manifest not registry) — superseded by src/geox_mcp/generated/ v2. ARCHIVE. Rationale: duplicate name, older schema, wrong count, wrong source-of-derivation.
2. src/geox_mcp/tools_manifest.yaml (31/32, "MASTER FORGE W8") — the displaced OLD authority. Either regenerate from registry or demote to historical. Rationale: asserts 31/32 vs canonical 26; not gate-tracked; still dirty in opt runtime.
3. .well-known/mcp/server.json (31) — disk descriptor contradicting wire 26. REGEN from registry. Rationale: this is the exact disk-vs-wire drift Lane 555 caught.
4. GEOX_MCP_APPS_SURFACE.json (32) — REGEN or ARCHIVE. Rationale: asserts 32, no gate coverage.
5. README prose "Live reality" table (31/25/e8e6f93) — REGEN or hand-correct to 26/26 + real commit stamps. Rationale: green gate does not cover prose; currently false on every count.

REDUCTION COUNT: **5 files can be archived-or-regenerated** (1 hard ARCHIVE = root v1 CANONICAL_PUBLIC_SURFACE.json; 4 REGEN-to-26 = tools_manifest.yaml, .well-known/mcp/server.json, GEOX_MCP_APPS_SURFACE.json, README prose table). Net effect: collapse the "how many tools" question from 6 conflicting answers (25 / 26 / 31 / 32 / live-25 / live-26) to ONE gate-enforced 26.

The uncommitted repair in /root/GEOX already moves in this direction: it modifies registry.py (+87 lines, adds derived RT1 recovery — see Section below), geox_middleware.py, tools_manifest.yaml (+10), contracts/tools.yaml, the generated CANONICAL surface, both tools.json, tools_sot.yaml, generate_all_surfaces.py (+167 = the new --check gate), and adds an untracked surface-drift-gate.yml + tests/test_rt1_recovery_derivation.py. This is the "Step 1 of 3 / Lane 333d" work forging the drift gate. It is UNCOMMITTED (9 M + 2 ??). [OBS]

---

## Cross-cutting: the /root/GEOX uncommitted repair (what the F13 binary would commit)

`git -C /root/GEOX status --porcelain` (read-only): 9 MODIFIED + 2 UNTRACKED.
Modified: .github/workflows/09-boundary-ratchet.yml (conflict resolved on disk 20:29:06 by concurrent lane), contracts/tools.yaml, scripts/generate_all_surfaces.py (+167 = --check gate), src/geox_mcp/generated/CANONICAL_PUBLIC_SURFACE.json, src/geox_mcp/geox_middleware.py (+41), src/geox_mcp/registry.py (+87 = derive_recovery_tool RT1), src/geox_mcp/tools_manifest.yaml (+10), tools.json, tools_sot.yaml.
Untracked: .github/workflows/surface-drift-gate.yml (Lane 333d "Step 1 of 3", fail-closed CI gate), tests/test_rt1_recovery_derivation.py.
diffstat: 9 files, 321 insertions(+), 18 deletions(-). [OBS]

This repair is the surface-drift-gate + RT1-recovery-derivation work. The Section A gate PASS reflects THIS worktree state (uncommitted). Committing it is reversible-in-principle but pushes to canonical origin; deploying it over /opt/geox is the irreversible step gated by Section D's fork divergence. [DER]

---

## F13 BINARY STAGING (what Arif is being asked to decide)

Four separable decisions, each with its own reversibility:
1. COMMIT the /root/GEOX repair (9 M + 2 ??) — reversible (local git). Blocked-by: boundary-ratchet conflict must be committed resolved (Section E) or CI reds.
2. PUSH to origin/main — canonical-record mutation, external. Note origin already has BOTH divergent mains' upstream; push target state must be verified (Section D fork).
3. REDEPLOY /root/GEOX → /opt/geox — IRREVERSIBLE, would clobber 26 opt-local edits + delete 14 untracked opt files + discard 4 opt-unique commits (Section C + D). NOT SAFE as blind overwrite; needs fork reconciliation first.
4. SEAL — per apex_verdict_seal doctrine, schema/gate fixes are precondition, not answer; live kernel_verdict=HOLD and deployment_drift self-report is untrustworthy (3 contradictory stamps incl. a phantom 297abcb).

Unknowns / UNMEASURED:
- Whether the 4 opt-unique commits (0bd60576, 73fb8977, b0508ff7, d669605c) carry intent that must survive reconciliation, or are fully superseded by root's 26-surface redo. Needs per-commit diff review (not done — would require deeper opt-side inspection).
- Identity/provenance of deployed_commit 297abcb (phantom in both GEOX repos; likely arifOS build-registry id). UNMEASURED — not resolvable from GEOX alone.
- What the concurrent writer lane (333d?) is doing live to /root/GEOX during this sweep; it resolved boundary-ratchet at 20:29:06 mid-observation. Coordinate before commit to avoid clobber.
