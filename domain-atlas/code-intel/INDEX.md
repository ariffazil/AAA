# Code Intelligence — Layered Maps (Phase 1, 2026-09-16)

**RATIFIED 2026-09-16 (F13: "go and make it work") — see `RATIFICATION-2026-09-16.md` for the binding decision inventory + both-witness landed state.**

Forged by 333-AGI per sovereign directive. Layered system: static maps (Emerge) +
boundary contracts (import-linter). SCIP + code-intel MCP + OTel merge = Phase 2/3.

## Artifacts (this dir)
- `emerge-configs/*.yml` — 5 full-repo + 2 live-view configs
- `importlinter/{arifOS,GEOX,WEALTH}/pyproject.toml` — boundary contracts
- Generated graphs live at `/root/work/code-intel/emerge/{view}/` (GraphML+JSON;
  NOT committed — regenerable in ~20s total)

## Toolchain (verified 2026-09-16)
- venv: `/root/.tools/emerge-venv` (emerge-viz 2.0.7 + import-linter 2.15)
- ⚠️ PIN: `setuptools<81` required (emerge uses pkg_resources; py3.13 default
  setuptools 84.0.0 dropped it)
- Regen: `/root/.tools/emerge-venv/bin/emerge -c emerge-configs/{repo}.yml`
  (export dirs must pre-exist); lint:
  `PYTHONPATH={repo|src} /root/.tools/emerge-venv/bin/lint-imports --config importlinter/{repo}/pyproject.toml`

## Map sight — structure metrics (live views)
| Repo | SLOC | Communities | Modularity | Dangerous hub (fan-out) | Chokepoint (fan-in) |
|---|---|---|---|---|---|
| arifOS (arifosmcp) | 362,522 | 54 | 0.33 | runtime/tools.py **179**, server.py 124 | runtime/tools 63 |
| GEOX (src) | 149,437 | 77 | 0.32 | tools_wiring.py 112, server.py 73 | geox_core/enums/statuses.py 34 |
| WEALTH | 79,724 | 50 | 0.41 | internal/monolith.py 73 | wealth_contracts/epistemic.py 34 |
| WELL | 40,683 | 28 | 0.40 | server.py 64 | (fastmcp/urllib externals only) |
| A-FORGE | 38,622 | 16 | 0.31 | rag/ocr_document.py 19 | — (best factored) |

NOTE: `__future__`/pydantic/fastmcp "hubs" in raw emerge output = external
pseudo-nodes, filtered here. arifOS/GEOX full-repo numbers are archive-contaminated
(flatten-archive commits); live views above are the honest architecture.

## Semantic sight — boundary contracts (machine-verified baseline)
| Contract | Verdict | Violations (KNOWN DEBT — fail CI on NEW only) |
|---|---|---|
| ARIFOS-BOUNDARY-001 constitution ↛ runtime | KEPT | — |
| ARIFOS-BOUNDARY-002 transport ↛ runtime | BROKEN | conformance_spine.py:1026 → runtime.ingress_middleware._ARIFOS_INGRESS_INSTANCE (private singleton, lazy import) |
| GEOX-DATA-003 core ↛ mcp | BROKEN | 4 paths: benchmarks.geox_001_orthogonal_route→tools.{well_ingest,well_qc}; core.welltie→tools._helpers (l.43,580); well.tools.sensing→tools.kernel._petrophysics (l.49) |
| WEALTH-CONTRACT-001 contracts ↛ {mcp,core,internal} | BROKEN | 1 path: contracts.envelope→wealth_core.math (l.524) |

Doctrine: contracts are enforced as ratchet — existing violations are baseline
debt; CI HOLD on NEW violations only. Exceptions ledger needs expiry dates
(Phase 2) else exemptions become permanent ghosts.

## Supply-chain sight — enabled 2026-09-16
- GitHub vulnerability alerts + dependency graph + SBOM endpoint: enabled on
  arifOS, A-FORGE, GEOX, WELL, WEALTH (verified: /dependency-graph/sbom returns
  cyclonedx). Dependabot.yml deliberately NOT added (PR noise; sovereign quiet-
  ops preference — alerts surface in security tab).
- CODEOWNERS: present in all 5 repos (verified).

## Ownership truth
`/etc/arifos/repo-atlas.yaml` declares repo-ownership rules (one change = one
repo; arifOS must not become organ monorepo). Boundary contracts above are the
intra-repo complement, not a replacement.

## Staged (Phase 2 — LANDED 2026-09-16 same day)
- **Git change-coupling** (direct git-log co-change, 500 commits): arifOS hidden
  hub `core/physics/economic_invariants.py` co-changes with boot/constitution/
  core/kernel modules — **classification correction: core/physics is LIVE shared
  code, not archive**. GEOX coupling = healthy test↔source only. WEALTH
  `contracts/envelope ⇄ mcp/server` 15× — WEALTH layering is aspirational (INT).
- **Cycles** (networkx on emerge graphml): arifOS 1 mutual (bridge⇄tools_internal);
  GEOX 6 mutual + 3 longer (wiring⇄server⇄registry trinity — worst); WEALTH 2;
  WELL 1; A-FORGE **0 (cleanest)**. Cycle-breaking = refactor = 888_HOLD.
- **CI ratchet LIVE** (arifOS pilot, commit ac94be1ef): `boundary/` dir with
  `.importlinter` (INI) + `EXCEPTIONS-LEDGER.json` (expiry 2026-12-15) +
  `boundary_ratchet.py` (grimp-direct, exit 0/1/2) + workflow
  `09-boundary-ratchet.yml`. Verified locally BOTH paths before push.
  GEOX/WEALTH rollout = copy pattern after arifOS pilot proves in CI.
- emerge `git_directory` pass: computed but exports git metrics to HTML/d3 only
  (not JSON) — superseded by direct git-log coupling script (transparent).

## Staged (NOT done — requires separate build sessions + 888_HOLD where marked)
- Phase 2: git change-coupling pass (emerge git_directory param); cycles via
  grimp; CI wiring (fail-on-new).
  — PARTIALLY LANDED (FI-003, 2026-09-16): exceptions ledger v1 with expiry schema
  (forge_work/2026-09-16-code-intel-phase0/ledger/); A-FORGE TS gate (depcruise,
  domain-purity CLEAN baseline) + madge cycle census (3 cycles); semantic layer
  via CodeGraphContext 0.6.13 embedded FalkorDB Lite (arifOS indexed, 108K CALLS
  edges, CLI-queryable); envelope + reconciliation schemas v1 (drafts, unwired);
  Journey-1 reconciliation bundle (arif_seal→vault_receipt, PLAUSIBLE).
- Phase 3: code-intel MCP (**CORRECTED at ratification: CGC 0.6.13 + embedded
  FalkorDB Lite per-worktree — Kuzu REJECTED**, see RATIFICATION). Read-only.
- Phase 4: pre-PR constitutional gate (changed-subgraph + rule eval).
- Skill surface: `skills/codebase-reality/` (CLI-first evidence contract, 7 modes).
- 888_HOLD: any structural mutation derived from these maps (moving shared
  modules, boundary rule removal) — static evidence ≠ institutional intent.

Evidence labels: all table values OBS (emerge/lint-imports/gc api output in
session 2026-09-16). Confidence 0.9 (tool output directly witnessed).
