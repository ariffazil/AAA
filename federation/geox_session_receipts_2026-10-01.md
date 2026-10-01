# GEOX Session Receipts Index — 2026-10-01

**Purpose:** Single retrieval pointer for every GEOX-related receipt produced during this session. Cross-federation discoverable. Pure doc; reversible.

**Authority order (read first):**

1. `geox_prep_evidence_pack_2026-10-01.md` — Lane 777a (latest, most comprehensive)
2. `geox_steps_1_3_repair_receipt_2026-10-01.md` — Lane 333d repair execution
3. `geox_one_manifest_design_2026-10-01.md` — Lane 333 architecture
4. `geox_drift_receipt_2026-10-01.md` — Lane 555 live probe
5. `geox_staged_commit_proposal_2026-10-01.md` — Lane 777b commit structure
6. `geox_boundary_ratchet_fix_receipt_2026-10-01.md` — Lane 888b + parent applied
7. `geox_readme_refresh_receipt_2026-10-01.md` — Lane 888a (pending)
8. `geox_sot_reduction_receipt_2026-10-01.md` — Lane 888c (pending)

---

## Receipts by lane

### Lane 555 — GEOX drift probe

`/root/AAA/federation/geox_drift_receipt_2026-10-01.md`

**Load-bearing finding:** the user's three claimed "live RT1 rejections at 26 declared tools" do not exist. Real rejections (2026-09-19) report 25. 2026-10-01 transcript matches are prompt-template echoes, not server output. `geox_surface_status` was genuinely rejected on 2026-09-19 but is public today.

**Scar-class evidence:**
- Cross-organ identity contamination (GEOX `/health` publishes arifOS SHA `297abcb`)
- Source/runtime disjoint (`/opt/geox@7027ff64` vs `/root/GEOX@17802197` are mutually non-existent)
- Phantom receipts (`/opt/geox/.git_commit=7750a2b3` not a valid object; `/root/GEOX/.git_commit=658a921` 7.8 weeks stale)
- 22 of 22 enabled MCP servers have `owner_skill: null`
- `geox_well_desk_open` ghost still wired (deregistered ZEN-15 but in server.py:132 + organ_governance.py:56)
- Expired OAuth static client (`geox-claude-conn-20260804-a01`, expires 2026-09-04)
- Harness config error: `/root/.mcp.json` declares 1 server while `/root/.claude/mcp.json` declares 33 at a path never read

### Lane 333 — GEOX ONE MANIFEST design

`/root/AAA/federation/geox_one_manifest_design_2026-10-01.md` (1103 lines)

**Architecture:** ONE manifest → generates tools/list, RT1 allowlist, connector descriptor, compat aliases, registry, docs. G0 conformance test (`declared == exported == callable == observed`).`).

**Three findings from probe:**
- `geox_surface_status` IS on live tools/list at 26. The real bug is narrower: **6 of 26 public tools belong to no capability pack**, so any profile-layer consumer sees 20, and the recovery tool is one of the 6 that vanishes.
- The three "rejected" tools are not hallucinations — `geox_system_registry_status` and `geox_resource_registry_status` are real implemented callables absent from the manifest entirely. **GEOX under-declares its own runtime.**
- `scripts/generate_all_surfaces.py` already exists (531 lines) declaring "registry.py is the ONLY truth" — referenced by zero workflows in `.github/`. Dry-run: 4 of 6 surfaces CHANGED. Lane 333's reading: **hardening, not replacement.**

**Critical structural defect flagged:** `/health` cannot fail. `_GIT_VERSION` returned for all four fields (`source_commit`/`built_commit`/`deployed_commit`/`physics_manifest_hash`). A drift check that compares a variable to itself returns `drift:false` unconditionally. **Sealed Oracle Independence Law violation, live in production.**

### Lane 333d — GEOX Steps 1–3 repair

`/root/AAA/federation/geox_steps_1_3_repair_receipt_2026-10-01.md` (rewritten by parallel writer — see scar-class pattern)

**What landed:**
- Step 1: `.github/workflows/surface-drift-gate.yml` (CI gate, sha256 `86884e80…`) + `--check` mode in `generate_all_surfaces.py` with **timestamp-normalised sha256** (naive raw-byte hash would be permanently red; 4 of 6 generators embed `datetime.now()`)
- Step 2: `geox_surface_status` pinned in `tools_manifest.yaml:1839` `earth_core` pack (earth_core is in all 4 profiles)
- Step 3: `derive_recovery_tool(rejected_tool)` in `registry.py:288`; RT1 guard in `geox_middleware.py:723` derives suggestion from registry, not literal; `recommended_next: null` if no callable recovery

**Live verified:** `python3 scripts/generate_all_surfaces.py --check` → **PASS** (6/6 OK). Tests: 18 passed. Regression: 12 pre-existing failures, +18 new passing, **zero regressions**.

**Pre-existing defects surfaced (NOT fixed, held):**
1. `capability_registry.yaml` advertises `research → 26` but code returns 21
2. `tools_manifest.yaml` declares `public_count_target: 31`, real public 26, `surface_attestation()` returns `ok=False, error=SURFACE_COUNT_DRIFT` permanently
3. **`.github/workflows/09-boundary-ratchet.yml` had committed merge-conflict markers at lines 26, 32** → fixed in Lane 888b

**Scar-class finding in 333d's own work:** first draft of RT1 test rebuilt the error string inside the test body — would have passed even with the hardcoded literal still in place. Third recurrence of `audit-measures-its-own-construction` scar in this session.

### Lane 555b — A-FORGE fingerprint + selection-ledger gap

`/root/AAA/federation/aforge_registry_fingerprint_2026-10-01.md` (sha256 `cd21d6f0…`)
`/root/AAA/federation/aforge_selection_ledger_gap_2026-10-01.md` (sha256 `dacd2d18…`)

**A-FORGE fingerprint:** `aa39ecd5cc2a282a511379c9f789daad1e60356b0e0266aac45c58428f6f03c7` (sha256 over sorted 122-tool name list, A-FORGE-scoped). Three authoritative sources agree on 122 tools; three other sources disagree by design or staleness.

**Selection ledger:** 12 events, 0 outcomes, 0 verifications. **`independent_verification_result` is schema-absent**, not merely empty.

**Drifts:**
- DRIFT-1: fingerprint scope conflation (federation 343-tool digest vs A-FORGE 122-tool)
- DRIFT-2: silent-drop coverage gap (78/122 tools vanish from projection, 4/7 verbs empty)
- DRIFT-4: source ahead of runtime (A-FORGE repo HEAD 25 commits ahead)

**Adapter fragment audit:** Codex directly fragment-driven; canonical `/root/AGENTS.md` trunk has 27 fragments; Claude+Gemini transitive pointers; **Kimi+OpenCode+Grok hand-maintained** (confounds §21 benchmark)

### Lane 555c — A-FORGE substrate witness

`/root/AAA/federation/aforge_substrate_verification_2026-10-01.md` (sha256 `85feb217…`, 827 lines)

**8 of 8 components VERIFIED-ON-DISK.** Federation substrate for the new design IS present. Every component Arif named exists at canonical path.

**Honest caveats:**
- EphemeralGenesis: TTL retirement in `EphemeralGenesis.ts`; scar-pressure retirement in adjacent `canary.ts` + `register.ts` (not co-located)
- "One graph" principle: spec frontmatter `valid_until: 2026-07-24` — **expired 69 days ago** — and line 33 cites a phantom path

**Concurrent-writer event:** during probe, separately-signed writer modified `policyTools.ts` (session-gate trust fix). Lane555c appended a dated ADDENDUM rather than leave a misleading seal.

### Lane 333b — A-FORGE contract + capability map drafts

Six files (corrected to projection-architecture after Arif's correction):

- `/root/AAA/instructions/aforge-citizen-contract-333b-DRAFT.md`
- `/root/AAA/federation/AFORGE_CAPABILITY_MAP_v1_DRAFT.md`
- `/root/AAA/federation/WARGA_AFORGE_VIEW_SPEC_v1_DRAFT.md`
- `/root/AAA/federation/AFORGE_COMPETENCY_SCHEMA_v1_DRAFT.md`
- `/root/AAA/federation/AFORGE_COMPETENCY_EVAL_v1_DRAFT.md`
- `/root/AAA/federation/AFORGE_LEARNING_LOOP_NOTE_v1_DRAFT.md`

**The FI-008 collision:** Lane333b correctly refused to overwrite FI-008's already-committed, config-bound `aforge-citizen-contract.md` at `version: 0.1.0-draft`. Wrote sibling `…-333b-DRAFT.md`. Four binaries queued (F13-adjacent but reversible): contract canonical, LEARN class, unadopted-draft binding, GOVERN class.

### Lane 777a — GEOX prep evidence pack

`/root/AAA/federation/geox_prep_evidence_pack_2026-10-01.md` (sha256 `f7658f61661b6aaa…`, 323 lines)

**Gate status: PASS** (6/6 OK, 0 missing, 0 drifted). **But:** gate is blind to README prose (says 31) and badge URL slug (says 31).

**Dirty files in /opt/geox: 40 confirmed** (26 modified + 14 untracked). 14 untracked include `structural_vision/`, `geox_glof.py`, "tectonic regime" — intentional new source a clean redeploy would **delete**.

**Runtime-vs-source divergence: FORKED, redeploy NOT SAFE as blind overwrite.** Both claim main, same origin, forked at merge-base `d353dd12` (2026-09-08). 22/26 /opt commits already patch-present in /root/GEOX; **4 opt-unique commits would be lost**:
- `0bd60576` registry-regen
- `73fb8977` gitlink-ignore
- `b0508ff7` surface-20→25
- `d669605c` prospect-flag

**Three contradictory commit stamps** for one process: `git_version=3f344b84`, `.git_commit=7750a2b3` (phantom), `deployed_commit=297abcb` (phantom = arifOS SHA). Self-reporting `deployment_drift:false` is untrustworthy.

**SOT reduction table:** 5 files archivable/regenerable:
1. Root-level `CANONICAL_PUBLIC_SURFACE.json` (v1, count 25, sourced from manifest not registry — superseded by `src/geox_mcp/generated/` v2) — ARCHIVE
2. `src/geox_mcp/tools_manifest.yaml` (31/32 stale counts) — REGEN
3. `.well-known/mcp/server.json` (31, Lane 555 disk-vs-wire) — REGEN **but F13-binary, held**
4. `GEOX_MCP_APPS_SURFACE.json` (32) — REGEN
5. README prose Live-reality table (31/25/e8e6f93 all wrong) — Lane 888a fixes

`capability_registry.yaml` is **NOT stale** — research/full=26 matches, governs pack visibility (13/19/26), not tool count.

### Lane 777b — staged commit proposal

`/root/AAA/federation/geox_staged_commit_proposal_2026-10-01.md` (44,142 bytes)

**Recommendation: 3 commits, not 1.** Bundling the gate with a truth change inverts the proof — the gate's first run can't distinguish "passing because clean" from "passing because coincidentally matches a half-changed surface."

| # | Subject | What it lands |
|---|---|---|
| 1 | `repair(ci): add surface-drift-gate` | workflow YAML + `--check` mode |
| 2 | `repair(rt1): derive recovery + pin recovery tool` | registry.py, geox_middleware.py, tools_manifest.yaml |
| 3 | `chore(surface): refresh generated artifacts` | 4 generated YAML/JSON/MD outputs |

**Direct push to `main`, no PR.** Rationale: PR adds review latency without a new reviewer; the staging proposal IS the review artifact. **Confirm with Arif before executing.**

**F13 boundary table:** 4 F13-CANONICAL artifacts, 3 F13-NEAR, 2 F13-NONE. None can be executed by agent.

### Lane 888b — boundary ratchet fix (APPLIED)

`/root/AAA/federation/geox_boundary_ratchet_fix_receipt_2026-10-01.md`

**What:** conflict markers at lines 26, 32 of `09-boundary-ratchet.yml` resolved. HEAD-prefer (`checkout@v7`/`setup-python@v7`), feat-side discarded (older `v4`/`v5`, dual-era substance already shipped via `stateless_era.py`).

**Discipline caught:** Lane 888b held OBSERVE_ONLY mandate, refused mutation despite "E "EDIT ONLY" framing, resolved-in-evidence at `/tmp/resolved-09-boundary-ratchet.yml` (sha256 `e74f7ab1…`), parent agent applied. Lane 888b and a parallel-writer both produced the same resolution at 20:29:06 — institutional coordination without parent intermediation.

**Scar-class closure:** converted an inert YAML into valid YAML. **The gate will now fire on the next CI run** instead of silently no-oping. Closes the scar class opened by `tier-0-phantom-evidence-2026-09-21` generalized — a configuration that *appears* present but is in fact inert.

### Lane 888a — README refresh (pending)

Output: `geox_readme_refresh_receipt_2026-10-01.md`. Lane 777a found README claims 31 / live 25 / commit `e8e6f93` (phantom). Lane 888a corrects to 26 / 26 / `17802197`.

### Lane 888c — SOT reduction (pending)

Output: `geox_sot_reduction_receipt_2026-10-01.md`. Per Lane 777a, archives root-level `CANONICAL_PUBLIC_SURFACE.json` (v1), regenerates `tools_manifest.yaml` 31→26, `GEOX_MCP_APPS_SURFACE.json` 32→26.

---

## Held F13 binaries (your call)

### GEOX repair sequence

1. **Commit** — Lane 777b's 3-commit structure, direct to main
2. **Push** — to `ariffazil/geox` canonical origin (after fork-state verification)
3. **Redeploy** — `/opt/geox` is FORKED; blind overwrite would lose 4 unique commits + 14 untracked source files. **Not safe as-is.**
4. **Seal** — kernel_verdict=HOLD, drift self-report untrustworthy

### GEOX defects (pre-existing, surfaced)

5. `.well-known/mcp/server.json` regen (19→26, expired OAuth) — Lane 555 binary, held
7. `geox_well_desk_open` ghost removal from `/opt/geox/src/geox_mcp/server.py:132`
8. `/opt/geox` vs `/root/GEOX` fork reconciliation — needs the 4 opt-unique commits per-file adjudication
9. `capability_registry.yaml` advertises research→26 but code returns 21 (pre-existing defect)
10. `tools_manifest.yaml` `public_count_target: 31` (pre-existing defect, affects `surface_attestation()`)
11. **Step4: GEOX `/health` oracle tautology (`build_info_handler` returns `_GIT_VERSION` for 4 fields)** — Lane 333's deepest finding

### A-FORGE binaries (Lane 333b/555b/555c)

12. Contract canonical — FI-008's committed-bound vs333b's sibling-DRAFT vs merge
13. LEARN as a verb — FI-008's schema says no; FI-008's own competency schema requires it
14. Was binding `ROOT_AGENT_CONFIG.yaml` to an unadopted `version: 0.1.0-draft` correct?
15. 8th GOVERN class — 19 `aforge.governance.*` tools with no verb
16. Three divergent `affordances.yaml` siblings (canonical `cbe99c45…` vs browser-poc `9a2853d6…` vs wt-l11l09 `687618ac…`)

### Harness / federation

17. `/root/.mcp.json` declares 1 server while `/root/.claude/mcp.json` declares 33 at a path never read — entire GEOX/etc. surface unreachable from this harness
18. `/root/.claude/settings.local.json:enabledMcpjsonServers` dangling enablement (6 servers absent from every loaded file)
19. `cloudflare` / `forge-infra-guardian` (memory's "gold standard") `status:disabled_intentional`

---

## New scar-class patterns surfaced this session

### Concurrent-writer-improves-output (saw 3× this session)

1. Lane 555c reported a separately-signed edit to `policyTools.ts` during its probe
2. Lane 333d's receipt was rewritten between my read and Arif's message — additional findings I missed (capability-packs location, runtime-vs-source forks, volatile-vs-stable distinction)
3. Lane 888b and a parallel-writer both resolved the boundary ratchet at 20:29:06 with the same SHA — coordinated without parent intermediation

**Pattern:** the institution has processes that improve output after the agent emits it. **Property:** the institution doesn't degrade when the agent gets tired. **Implication:** agents should stop at "halting for direction" rather than perform tiredness — the institution finishes the work.

### Gate-parses-as-configured (boundary ratchet)

A gate that fails to parse produces no red build; it produces no build at all. The gate appears configured in the workflow YAML directory; it is in fact inert. Sister scar to `scar-2026-09-28-audit-methodology-fork-bias`. Different organ: `scar-2026-09-30-hermes-mcp-organs-alive-vs-healthy` — same shape, served field doesn't exist on the endpoint that supposedly serves it.

### Volatile-vs-stable generator output

4 of 6 GEOX generator outputs embed `datetime.now()` in their headers. **A naive raw-byte SHA256 comparison is permanently red.** Lane 333d proved this by running the generator twice, one second apart. The fix is timestamp-normalised hashing. The lesson: **CI gates measuring generator output must design around clock churn by design, not as a workaround.**

---

## Receipts: this index

Path: `/root/AAA/federation/geox_session_receipts_2026-10-01.md`
sha256: pending parent verification.