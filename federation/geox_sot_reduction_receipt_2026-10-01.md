# GEOX SOT Reduction Receipt — Lane 888c

**Date:** 2026-10-01
**Lane:** 888c (555-ASI Φ SENSE) — EDIT/MOVE ONLY
**Authority scope:** move + deprecation notes only. No commit, no push, no restart, no seal.
**Repo:** `/root/GEOX` · branch `main` · HEAD `17802197d9c4c81de19403125c32bd09736347ae`
**Untouched:** `/opt/geox` (never opened), `registry.py`, `tools_manifest.yaml`, the generator, all workflows, all tests.

---

## 0. PROVENANCE CORRECTION — the two ground-truth docs do not exist

The brief instructed me to read two files first and "use them as ground truth."
**Neither exists.** Verified by direct read and by `find`:

| Instructed path | Status |
|---|---|
| `/root/AAA/federation/geox_prep_evidence_pack_2026-10-01.md` | **ABSENT** |
| `/root/AAA/federation/geox_staged_commit_proposal_2026-10-01.md` | **ABSENT** |

`find /root/AAA -iname '*geox*2026-10-01*'` returns exactly three files, none of
which is the instructed pair:

- `/root/AAA/federation/geox_drift_receipt_2026-10-01.md` (27,435 B)
- `/root/AAA/federation/geox_one_manifest_design_2026-10-01.md` (70,597 B)
- `/root/AAA/federation/geox_steps_1_3_repair_receipt_2026-10-01.md` (31,264 B)

There is no "Section G" and no "Lane 777a"/"Lane 777b" content in any of the
three (grep for `Section G` / `SOT` returned nothing).

**Action taken:** I did **not** proceed on an absent ground truth. I substituted
`geox_one_manifest_design_2026-10-01.md` §0.1/§0.2 (the measured baseline, all
self-labelled OBS with receipts) as the closest available equivalent, and then
**re-derived every number myself by executing live code** rather than trusting any
document. Every count in this receipt is from direct execution, not from prose.

This is the binding scar class — `tier-0-phantom-evidence-2026-09-21` (`test -e`
before claim) and `scar-2026-09-28-audit-methodology-fork-bias` (mandatory live
probe before any gap claim). Both were honoured.

---

## 1. Live truth established first (all OBS, executed)

Run via `/root/GEOX/.venv/bin/python` against the live source tree, plus an HTTP
probe. These are the numbers every archive decision was tested against.

```
registry.py::CANONICAL_PUBLIC_TOOLS      → 26
surface_manifest.surface_attestation()   → public_count 26, ok=False, SURFACE_COUNT_DRIFT
capability_packs()                       → earth_core 14, earth_specialist 6, earth_research 1
tools_for_profile('default')             → 14
tools_for_profile('specialist')          → 20
tools_for_profile('research')            → 21
tools_for_profile('full')                → 21
GET http://127.0.0.1:8081/health         → status healthy, version v2026.08.26
tools_manifest.yaml                      → 87 entries, public_count_target: 31
scripts/generate_all_surfaces.py --check → PASS, 6/6 surfaces, 0 drifted, 0 missing
```

**Two corrections to the brief's premises:**

| Brief said | Live truth | Impact |
|---|---|---|
| "Lane 333d found research advertises 26 but code returns 21" | Confirmed: `capability_registry.yaml:40` says `tool_count: 26`; code returns **21** | The stale value is a *comment/decoration* — see §2 Candidate 1 |
| "`tools_for_profile('research')` returned 20" (per design doc §0.1) | Now returns **21** | Lane 333d's Step-2/3 repair already landed; the design doc is itself now stale on this point |

---

## 2. Candidates evaluated

### Candidate 1 — `capability_registry.yaml`: **NOT ARCHIVED** (brief premise wrong on two counts)

**Premise error A — wrong path.** The brief says `/root/GEOX/capability_registry.yaml`.
That path does not exist. The file is at **`/root/GEOX/registry/capability_registry.yaml`**
(3,168 B). Found by `find`.

**Premise error B — it is not a duplicate SOT. It is LIVE RUNTIME CONFIG.**
`registry.py` reads it at import time and branches on it:

```python
# src/geox_mcp/registry.py:213
_CAPABILITY_REGISTRY_PATH = Path(__file__).resolve().parents[2] / "registry" / "capability_registry.yaml"

# :219-223  _load_capability_registry()  → yaml.safe_load(...)
# :226-232  _get_discovery_profiles()    → reg.get("discovery_profiles", {})
# :285-287  is_escalation_required()     → reg.get("pack_visibility", {}).get(pack, {})
```

It is also a CI trigger path: `.github/workflows/surface-drift-gate.yml:40`.

**I proved the consequence of archiving it — non-destructively**, by repointing the
loader path at a nonexistent file *in memory only* (no file was moved, no state written):

```
--- simulated with capability_registry.yaml ABSENT ---
  default:    14
  specialist: 14     ← was 20
  research:   14     ← was 21
  full:       14     ← was 21
  is_escalation_required('geox_glof_cascade'): False   ← escalation governance silently disabled
```

Archiving it would **collapse all four discovery profiles to 14 tools** and
**silently disable escalation gating** — `is_escalation_required()` returns `False`
for every tool, so research/specialist tools become default-visible. That is a
capability-visibility regression and a governance hole, not a blast-radius reduction.
Fails rule 7 (it is neither duplicate, stale-in-effect, dead, nor redundant) and
fails the spirit of rule 6 (live config in active use).

**The genuine stale content inside it is decorative, not functional.** Lines 10-13,
23, 31, 40, 44 hardcode `tool_count:` values (13/19/26/26) that disagree with the
computed truth (14/20/21/21). But **`tools_for_profile()` never reads `tool_count`** —
it reads `visible_packs` (line 251) and computes the count from `capability_packs()`
(lines 253-263). So the wrong numbers are documentation only.

**Disposition: STAYS. Flagged, not moved.** Correcting those literals is an *edit*
to a CI-triggered runtime config file — outside this lane's move-only authority,
and it would conflict with the concurrent writer active in this repo (§5).
Recommended owner: Lane 333d (who already repaired the pack composition) or the
Lane 555 surface binary. Suggested fix: derive `tool_count` in the generator instead
of hand-maintaining it, so it cannot drift — same lesson as `regenerate_readme_badge`.

### Candidate 2 — `tools_sot.yaml`: **NOT ARCHIVED** (correctly, per rule 6)

Self-declares as generated and is verified as such:

```yaml
sot_source: registry.py::CANONICAL_PUBLIC_TOOLS
regenerated: '2026-10-01T11:55:32.137372+00:00'
regenerated_by: generate_all_surfaces.py (registry.py truth)
public_count: 26
```

It is in the CI `run_check()` surface list (`generate_all_surfaces.py:578`) and
currently **passes** the drift gate (`sha256=b0a5b2fb75f4ede4…`). Not hand-maintained.

### Candidate 3 — `contracts/tools.yaml`: **NOT ARCHIVED** (rule 6). Generated header
states "THIS FILE IS GENERATED FROM registry.py. DO NOT EDIT MANUALLY." `canonical_tool_count: 26`,
passes drift gate.

### Candidates 7/8/9 — `tools.json`, `llms.txt`, `src/geox_mcp/generated/CANONICAL_PUBLIC_SURFACE.json`:
**NOT ARCHIVED** (rule 6). All three in the CI surface list, all three pass the drift gate.

### Candidate 6 — `.well-known/mcp/server.json`: **NOT ARCHIVED**, flagged for Lane 555.
Per instruction and rule 6 (externally surfaced). See §4.

### Candidate 4 — `docs/`: **audited in full.** See §3.

### Candidate 5 — pre-existing archives: **NOT TOUCHED.** `docs/archive/` (3 entries)
left as-is per instruction. No `_staging/` or `_deprecated/` directory exists at
`/root/GEOX` top level (verified by `find`).

---

## 3. docs/ systematic audit — 53 files, full matrix

I did not rely on the brief's candidate list. I ran a systematic scan over every
`docs/*.md`: inbound-reference count (all file types, excluding `.venv/`, `.ua/`,
`.git/`, `.ruff_cache/`, `docs/archive/`, and self) crossed against stale-count
detection (`31|32|33|15|52|19|73` + "tools").

**Critical methodological finding:** the `.ua/` directory is a code-analyzer cache,
not a set of readers. A naive grep makes 11-17 files look "referenced" when the
only hits are `.ua/knowledge-graph.json`, `.ua/fingerprints.json`, and
`.ua/tmp/*.json` — all machine-generated indexes that merely catalogued the
filename. Excluding `.ua/` changed the reference count for several docs from
11-17 to 0-2. **I re-ran every check with `.ua/` excluded before trusting any
"dead" verdict.**

### ARCHIVED — 2 files

Both are DEAD (zero inbound refs across all file types, `.ua/` excluded) **and**
STALE (verifiably wrong counts vs live 26).

| # | From | To | Bytes | Criteria met |
|---|---|---|---|---|
| 1 | `docs/GEOX_FORGE_FLOW_AGENT_PROMPT.md` | `_archive/2026-10-01/GEOX_FORGE_FLOW_AGENT_PROMPT.md` | 11,284 | DEAD + STALE |
| 2 | `docs/README-FULL.md` | `_archive/2026-10-01/README-FULL.md` | 11,992 | DEAD + STALE + DUPLICATE/REDUNDANT |

**1. `GEOX_FORGE_FLOW_AGENT_PROMPT.md`** — frozen at tip `18e9e9ac` (2026-07-25).
Claims **33** tools at lines 3, 32, 50, 80, 168 vs live **26**. Zero inbound refs
(exact basename and partial stems `FORGE_FLOW`/`forge_flow` both searched).
Elevated hazard beyond a stale count: it is written as "paste this to the next
agent" and embeds `set -a && source /root/.secrets/vault.env` plus a Supabase
project reference — an agent prompt that misdirects on the surface count and
points at secrets.

**2. `README-FULL.md`** — the strongest candidate in the repo; met three criteria.
A full second copy of the README, carrying its own `<!-- SOT-MANIFEST -->` header:

| Field | Declared | Live |
|---|---|---|
| `mcp_tools_live` | **19** | **26** |
| `mcp_apps_registered` | 18 | 12 |
| `last_verified` | `2026-08-11T05:58:51Z` | 51 days stale |
| `live_commit` | `d79a9b59` | `17802197` |
| badge (line 20) | "33 Canonical Tools" | 26 |

The decisive defect: the generator refreshes the SOT-MANIFEST header **only** in
the root README —

```python
# scripts/generate_all_surfaces.py:423-425
def regenerate_readme_badge(dry_run: bool) -> None:
    """Regenerate README.md badge count and capabilities heading."""
    path = ROOT / "README.md"          # ← /root/GEOX/README.md, NOT docs/README-FULL.md
```

and `docs/README-FULL.md` appears in neither that path nor the `run_check()`
surface list (`:578-587`) nor any workflow. So `mcp_tools_live: 19` is permanently
unrefreshable while presenting itself as verified truth. A stale count inside a
**machine-readable SOT-MANIFEST header** is worse than stale prose: any scanner
grepping `mcp_tools_live:` across `*.md` now finds two answers (19 and 26).

Both moves were made with `git mv`, so both are git-tracked renames (`R` status)
and reversible with a single `git mv` back. Each has a sibling
`_DEPRECATED_*.md` note (2,968 B + 3,533 B) recording date, lane, reason,
replacement canonical source, and exact restore command.

### CONSIDERED BUT NOT ARCHIVED — with rationale

| File | Stale? | Refs | Why it stays |
|---|---|---|---|
| `CANONICAL_PUBLIC_SURFACE.json` (top level) | **YES** — `public_count: 25`, `generated_at 2026-09-19`, structurally different from the generated copy | 2 | **CI reads it.** `.github/workflows/sentinel-premerge-gate.yml:91` sets `SURFACE = "CANONICAL_PUBLIC_SURFACE.json"` and it is a `CRITICAL_PATHS` entry at `:45`. `tests/test_master_forge_truth_loop.py:284` also hardcodes the absolute path. Archiving would break a gate. Fails rule 4/rule 5. See §4 flag. |
| `docs/PROTOCOL_CONFORMANCE.md` | **YES** — "32 public tools", "32 canonical tools" | 2 | Linked from `docs/index.md:36` (the canonical docs index). Archiving leaves a broken link in the one entry-point doc. Needs a coordinated index edit, not a move. |
| `docs/HOST_COMPATIBILITY_MATRIX.md` | **YES** — "tools/list = 32", "32 public tools" | 2 | Linked from `docs/index.md:24` **and** from `docs/MCP_APPS_READINESS.md:17`. Same reason. |
| `docs/MCP_APPS_READINESS.md` | mild | 1 | **Inbound ref from live app HTML**: `apps/index.html:71` renders `<code>docs/MCP_APPS_READINESS.md</code>` to users. Not dead. |
| `docs/STRUCTURAL_VISION_INTEGRATION_MAP.md` | **YES** — "31 public tools at snapshot" | 1 | **Test depends on it**: `tests/test_structural_vision_integration_verified.py` exists solely to re-verify this doc's findings. Rule 5 (don't touch tests) — moving the doc would orphan a test's stated subject. |
| `docs/ZEN_15_SURFACE.ARCHIVED.md` | already-archived tombstone claiming "32" | 1 | **Test depends on it AND already handles the move**: `tests/test_master_forge_truth_loop.py:288-290` checks `docs/ZEN_15_SURFACE.ARCHIVED.md` then falls back to `docs/archive/ZEN_15_SURFACE_ARCHIVED_2026-07-24.md`. It is already a tombstone (rule 5-adjacent, candidate 5). |
| `docs/SOT_AUDIT_2026-09-06.md` | dated audit, internally consistent for its date | 0 | A **dated receipt**, not a live claim. It explicitly says "`tools_manifest.yaml` … leave; health is SOT". Archiving receipts destroys provenance (F11). Stays. |
| `docs/POST_MERGE_DRIFT_AUDIT_2026-07-13.md` | dated audit | 0 | Same — dated receipt with its own DRIFT verdicts recorded. F11 provenance. Stays. |
| `docs/RELEASE_CHANGELOG_DRAFT_v2026.07.13-institution-1.md` (+ `.sha256`) | dated | 2 | Release receipt with a hash sidecar. Stays. |
| `docs/ZEN_HORIZON_ARCHITECTURE.md` | **YES** — "Freeze at 33 canonical tools" | 0 | **RATIFIED STRATEGIC DIRECTIVE**, `SOT Date 2026-07-26`, `Authority: 888_JUDGE · F13 SOVEREIGN`. One of its "FORGET" items happens to name 33. Archiving an F13-ratified directive is **not** within a move-only lane — that is direction/authority, F13-class. Stays; flag only. |
| `docs/mcp_apps_verification_matrix.md` | mild — "expect 32 tools" in a comment | 1 | Referenced; a comment in a verification matrix, low blast radius. Stays. |
| `docs/GEOX_PETRO_RUNBOOK_F2.md` | mild — "PASS at audit (32 public tools)" | 2 | Historical PASS record, correctly dated as "at audit". Live runbook. Stays. |
| `docs/SEISMIC_SECTION_INTERPRET_ZEN.md` | mild — "Tip baseline: 78963c61 · 32 public tools" | 3 | Explicitly labelled as a **tip baseline** (a dated snapshot anchor), which is honest. Stays. |
| `docs/ARCHITECTURE-EARTH-OS.md` | no | 0 | Dead by refs but **not stale** — fails rule 7's stale branch, and archiving a non-misleading architecture doc has no blast-radius benefit. Stays. |
| `docs/MODE_PARAM_SCHEMA_GUIDE.md` | no | 0 | Same — dead but not stale, no misleading claim. Stays. |
| `docs/README-FULL.md`, `docs/GEOX_FORGE_FLOW_AGENT_PROMPT.md` | **YES** | 0 | **ARCHIVED** (§3 above). |
| `docs/CODE_OF_CONDUCT.md`, `docs/SUBSURFACE_TOPOGRAPHY_ISOMORPHISM.md` | no | 0 | Not stale. No benefit. Stay. |
| `FEDERATION_MAP.md` (top level) | no — it is a 106-byte pointer stub | 0 | Already self-declares: "This file is superseded by `/root/AAA/docs/FEDERATION_MAP.md`. Status: DERIVED — do not update this copy." It is **already a tombstone**, doing the job an archive note would do, at 106 bytes. Moving it gains nothing and could break a reader expecting the pointer. Stays. |

### Duplicate-basename pairs checked (top level vs `docs/`)

All eight pairs **DIFFER** by content hash — none is a byte-identical copy, so none
qualifies as REDUNDANT under rule 7d:

```
PROTOCOL_CONFORMANCE.md  top=2742  docs=1284  DIFFER (6a2966486c1c / 54c6b22bfdf2)
RUNBOOK.md               top=4599  docs=6523  DIFFER (34ca368a133f / 6a04f50c00da)
SECURITY.md              top=1069  docs=685   DIFFER (186e94961d45 / 8ae46805b731)
CHANGELOG.md             top=733   docs=6099  DIFFER (9966d4ffce07 / 9260aef12b29)
CONTRIBUTING.md          top=1358  docs=1390  DIFFER (0f3903a0f71e / 72300a84a8f1)
CONTEXT.md               top=4187  docs=3839  DIFFER (f43d9107212c / ae5513758aca)
FEDERATION_CONTRACT.md   top=1203  docs=2645  DIFFER (17126a933ae9 / fc1148fc35ba)
FEDERATION.md            top=699   docs=1203  DIFFER (cb13b9ab02ea / 17126a933ae9)
```

Note `docs/FEDERATION.md` is a **symlink** to `../FEDERATION_CONTRACT.md`, which is
why its hash equals top-level `FEDERATION_CONTRACT.md`. This is a naming tangle
(two `FEDERATION*` docs, two `PROTOCOL_CONFORMANCE.md`, two `RUNBOOK.md`, two
`SECURITY.md`) but each pair has divergent content, so de-duplicating requires an
editorial merge decision, not a move. **Not actioned.** Flagged in §4.

### `docs/index.md` broken link found

`docs/index.md:29` links `[ZEN_15_SURFACE.md](./ZEN_15_SURFACE.md)`. That file
does not exist — only `ZEN_15_SURFACE.ARCHIVED.md` and
`docs/archive/ZEN_15_SURFACE_ARCHIVED_2026-07-24.md`. Also `docs/index.md:4`
states "**SOT for tools:** live `tools/list` (15)" and `:3` claims "Max canonical
set: ≤20" while `docs/` holds 53 top-level `.md` files plus 10 subdirectories.
The index is itself stale and over-subscribed. **Not actioned** — it is an edit,
not a move, and it is the docs entry point (high blast radius if wrong). Flagged.

---

## 4. Flagged for other lanes (not actioned here)

| Item | Route to | Why |
|---|---|---|
| `.well-known/mcp/server.json` disk-vs-wire drift (19 advertised vs 26 live, expired OAuth client, `expires 2026-09-04`) | **Lane 555** | Per brief, candidate 6 — separate binary on regenerating. Externally surfaced; regeneration is not a move. |
| `registry/capability_registry.yaml` stale `tool_count` literals (13/19/26/26 vs computed 14/20/21/21) at lines 10-13, 23, 31, 40, 44 | **Lane 333d** | Edit to a CI-triggered runtime config. Best fix is deriving `tool_count` in the generator so it cannot drift. |
| Top-level `CANONICAL_PUBLIC_SURFACE.json` is STALE (`public_count: 25`, `generated_at 2026-09-19`) while the generated copy says 26, and the two have **different sha256** (`fab8617590cb…` vs `387e452a152e…`) and different schemas | **Lane 555 / 333d** | It is CI-read (`sentinel-premerge-gate.yml:45,91`) and test-read (`test_master_forge_truth_loop.py:284`) so it cannot be archived — but it *should* be regenerated or the CI path repointed at `src/geox_mcp/generated/`. Two files with the same name and different content is the exact duplicate-SOT class this lane targets. |
| `tests/test_master_forge_truth_loop.py:278` `test_t9_surface_truth_31` asserts `len(names) == 31` and `snap["public_count"] == 31` | **Lane 333d / 555** | This test **must currently be failing** — live truth is 26. I did not run the suite (out of scope, and a concurrent writer is active). A test asserting a wrong constant is a false-green/false-red hazard. |
| `tools_manifest.yaml:4` `public_count_target: 31` → `surface_attestation()` permanently returns `ok=False, SURFACE_COUNT_DRIFT` | **Lane 333d** | Confirmed live by execution. This is defect **D1** in `geox_one_manifest_design_2026-10-01.md`. Any consumer trusting `ok` gets a standing false alarm. Fixing it means editing `tools_manifest.yaml`, which is canonical and outside this lane. |
| `.github/workflows/09-boundary-ratchet.yml:26,29,32` — **git conflict markers COMMITTED at HEAD** (`<<<<<<< HEAD` / `=======` / `>>>>>>> feat/mcp-dual-era-2026-07-28`) | **URGENT — Lane 555 / 888** | See §5. Verified present in `git show HEAD:` output, i.e. committed, not just working-tree. |
| `docs/index.md` stale (claims ≤20 docs / 15 tools; links nonexistent `ZEN_15_SURFACE.md`) | **Lane 555** | Editorial edit on the docs entry point. |
| Duplicate-basename doc tangle (8 divergent pairs, `docs/FEDERATION.md` symlink) | **Lane 777/555** | Needs a merge decision, not a move. |
| `docs/ZEN_HORIZON_ARCHITECTURE.md` "33 canonical tools" inside an F13-RATIFIED directive | **Arif / F13** | Direction-class content. Not mine to archive. |

---

## 5. CONCURRENT WRITER — active in this repo during my lane

**OBS.** While I worked, files I never touched changed underneath me:

- `README.md` mtime advanced `20:39:58` → `20:42:09` (+0800); it gained **192
  insertions / 78 deletions** and was rewritten to canonical **26** truth,
  self-attributing at `README.md:425` to "**Lane 888a**".
- `.github/workflows/09-boundary-ratchet.yml` mtime `20:29:06` → `20:42:09`.
- Its git status flipped **off** the modified list mid-session, meaning the
  conflict markers are **committed at HEAD**, not merely present in the working tree:
  `git show HEAD:.github/workflows/09-boundary-ratchet.yml | grep '^<<<<<<<'` → line 26.

I re-verified after each change that my two moves were still safe: the new README
contains **no** reference to either archived file, so both moves remain valid.

**The committed conflict markers are semantically corrupt but silently parse.**
`yaml.safe_load` succeeds — the markers land such that the job still yields four
well-formed steps (`actions/checkout@v7`, `setup-python@v7`, install grimp, run
ratchet). So **no YAML validator will catch this**; only a marker grep does.
`workflow_integrity` mode exists precisely for this class. This is a P0-ish
hygiene defect: a green-parsing workflow carrying unresolved merge state.

**Also OBS:** HEAD is `17802197` on `main`, working tree has 9 modified +
2 untracked files (including `registry.py`, `tools_manifest.yaml`,
`generate_all_surfaces.py`, `geox_middleware.py`) — i.e. Lane 333d's repair is
staged but uncommitted. My two renames are now interleaved into that same
uncommitted working tree. I did not commit (per instruction). **Whoever commits
must expect to find Lane 888c's two renames in the index.**

---

## 6. Blast-radius reduction

| Metric | Value |
|---|---|
| Files archived (moved) | **2** |
| Bytes moved out of active tree | **23,276 B** (11,284 + 11,992) |
| Deprecation notes added | 2 (6,501 B total) |
| Stale tool-count claims removed from active docs | **6** (five `33` in FORGE_FLOW; `mcp_tools_live: 19` + `33` badge in README-FULL) |
| Orphaned machine-readable SOT-MANIFEST headers eliminated | **1** (`mcp_tools_live: 19`) |
| Duplicate README front-doors eliminated | **1** (2 → 1) |
| Files deleted | **0** |
| Files committed | **0** |
| Protected files touched | **0** (`registry.py`, `tools_manifest.yaml`, generator, workflows, tests, all 6 regenerated surfaces, `/opt/geox`) |

**Post-move verification:** `scripts/generate_all_surfaces.py --check` → **PASS**,
6/6 surfaces in sync with `registry.py`, 0 drifted, 0 missing, truth count 26.
No test enumerates `docs/` by glob (verified — no `glob`/`iterdir`/`rglob` over
docs in `tests/`), so removing two files from `docs/` cannot break a collection
assertion.

---

## 7. Open questions for the parent lane

1. **The two instructed ground-truth docs do not exist.** Were
   `geox_prep_evidence_pack_2026-10-01.md` and
   `geox_staged_commit_proposal_2026-10-01.md` written to a different path, or
   never persisted? I proceeded on live-executed truth plus
   `geox_one_manifest_design_2026-10-01.md`. If Lane 777a/777b produced a
   specific archive list, it may differ from mine — please reconcile.
2. **Candidate 1's path was wrong and its premise inverted.** The brief treats
   `capability_registry.yaml` as a dead duplicate to archive; it is live runtime
   config whose removal I *measured* would collapse all discovery profiles to 14
   and disable escalation gating. Confirm you accept "STAYS" — or if the intent
   was only to fix its stale `tool_count` literals, that is an edit and needs a
   different lane.
3. **Committed conflict markers in `09-boundary-ratchet.yml`** — is a lane already
   on this? It parses green, so CI will not surface it.
4. **Top-level `CANONICAL_PUBLIC_SURFACE.json` (25, 2026-09-19) vs generated (26)**
   — two same-named files, different sha256, different schemas, one CI-read and
   test-read. Regenerate in place, or repoint CI/tests at
   `src/geox_mcp/generated/`? Either is an edit, not a move; outside my authority.
5. **`test_t9_surface_truth_31` asserts 31 against live 26.** Is it currently
   failing, xfail'd, or skipped? I did not run the suite (concurrent writer active,
   and running it was out of scope).

## Restore

Both moves are single-command reversible:

```bash
git -C /root/GEOX mv _archive/2026-10-01/GEOX_FORGE_FLOW_AGENT_PROMPT.md docs/GEOX_FORGE_FLOW_AGENT_PROMPT.md
git -C /root/GEOX mv _archive/2026-10-01/README-FULL.md                   docs/README-FULL.md
```

Nothing was committed, so `git -C /root/GEOX reset` on the two rename entries also
restores them.
