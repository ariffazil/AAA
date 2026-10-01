# GEOX Repair Receipt — Steps 1-3 — DRAFT 2026-10-01
# Lane: 333d
# Status: OBSERVE_ONLY-authorized repair. Step 4 (build_info_handler) HELD.
# User binary: "go" — interpreted as steps 1–3 only.
# Mutation: minimal, source-tree only (/root/GEOX), not deployed runtime (/opt/geox).

---

## 0. Headline (read this first)

Steps 1–3 are **implemented, tested, and verified green in the source tree**. 6 files modified, 2 files added. Zero regressions against a measured baseline.

**One scope correction that matters** (OBS, proven): the capability packs the task told me to edit in `registry.py` **do not live in `registry.py`**. They live in `src/geox_mcp/tools_manifest.yaml` under `capability_packs:`. `registry.py` only *reads* them via `capability_packs()`. Step 2 was therefore implemented as a 1-line pack-membership addition in `tools_manifest.yaml` — the same class of change (metadata, not behaviour), in the file that actually owns the data. No behavioural code path changed. Details in §3.

**Three pre-existing defects surfaced** that are outside steps 1–3 and are reported in §7, not fixed:
1. `capability_registry.yaml` advertises `research → 26 tools`; code returns **21**. The docstring in `registry.py:tools_for_profile` repeats the same wrong numbers.
2. `tools_manifest.yaml` declares `public_count_target: 31`; the real public surface is **26**. `surface_attestation()` returns `ok=False, error=SURFACE_COUNT_DRIFT` — this has been failing silently.
3. `.github/workflows/09-boundary-ratchet.yml` contains **committed git merge-conflict markers** (`<<<<<<< HEAD` / `>>>>>>> feat/mcp-dual-era-2026-07-28` at lines 26 and 32). That workflow cannot parse. It landed in commit `79e372e5`.

---

## 1. Scope confirmation

Files touched. `old_sha256 → new_sha256`, with the line ranges actually changed.

### Modified (6)

| # | Path | old_sha256 | new_sha256 | Lines changed |
|---|---|---|---|---|
| 1 | `/root/GEOX/scripts/generate_all_surfaces.py` | `218089ae2cb3796c7a0af092a86be047c48090be168c74021e337943e0fe19ad` | `58430f8bc1698624a4e6036665f0cca6ddf0b74483b142ea3831f1e781b25547` | `@@ -9,0 +10` · `@@ -23,0 +25` · `@@ -476,0 +479,157` · `@@ -479,0 +639,5` · `@@ -481,0 +646,3` — **+167 / −0** |
| 2 | `/root/GEOX/src/geox_mcp/registry.py` | `412bf8de5255998a46bd0531288768984f85317c04e59e5aa8d91bfca46d0e69` | `5cff10ef503f05426afda7fb03c4a1a0c3949788a84e0c09a86f81b8cd8485ab` | `@@ -3,0 +4` (add `import re`) · `@@ -286,0 +288,86` (append derivation API) — **+87 / −1** |
| 3 | `/root/GEOX/src/geox_mcp/geox_middleware.py` | `a5570173049eeea8fe9954a2f352fdefbaee84b4fac6769dc5bbb2eb9e5d99e6` | `de2fde45e8f5ea3f7a54e626eebdca8f4193dda793a8ae117595d4a2147b04f6` | `@@ -725,0 +726,38` (RT1 derivation block) · `@@ -729 +767,2` — **+40 / −1** |
| 4 | `/root/GEOX/src/geox_mcp/tools_manifest.yaml` | `725a6574f6797f6ef3c4cb613de6554738137469b7379ec6b8e3b493a26e3379` | `f45a9d7d2cb492d8ec12db8f80c90bfbfef010b1bde8eebc2624cf63f797a402` | `@@ -1839,0 +1840,10` (pin `geox_surface_status` into `earth_core` + rationale comment) — **+10 / −0** |
| 5 | `/root/GEOX/contracts/tools.yaml` | `e3302ebeb8f148f84be28c2f94fec4ee4363e5495079fdcc4f8bf9899859a722` | `31832858d5ff12e582466b2369aeaf3ae561dd9b895a7d26fe530f141d76a994` | `@@ -3` · `@@ -11` · `@@ -21` — **+3 / −3** (GENERATED artifact — regenerated, not hand-edited) |
| 6 | `/root/GEOX/tools.json` | `e752e0f65def5b04f7e628eff6f078b5dc47283fd2aa69f7bb5f7af446cc2465` | `4b10fbba6a18ab0bace5c7ca7afc2297609c66e5f937cea94878c4926b9e738b` | `@@ -115,2` — **+2 / −2** (GENERATED) |
| 7 | `/root/GEOX/tools_sot.yaml` | `5d6d262da24485b3ed3a8bf514517a1d84564ca1a9749eb7436bce6f49496320` | `d5491d7fa0a8cfc5d39fe65cc54fde735018734fe489fec3b1d078ded6ead18b` | `@@ -2` · `@@ -6` — **+2 / −2** (GENERATED) |
| 8 | `/root/GEOX/src/geox_mcp/generated/CANONICAL_PUBLIC_SURFACE.json` | `dcf6454e408262c9a824a846d969aaed637b5ffaa6b35ff6f10166839ec62808` | `387e452a152e91c7bf81a8a796709b3fa1e3f8076689b3b0c1299bcce0773349` | 10 hunks `@@ -3 … @@ -638` — **+10 / −5** (GENERATED) |

> Rows 5–8 are **generator output**, not manual edits. I ran `generate_all_surfaces.py` because Step 2 legitimately changed the truth, and shipping Step 1's gate against a stale surface would have made my own CI red on arrival. Their diffs contain **only** the `geox_surface_status` pack/profile additions and regenerated timestamps — verified hunk-by-hunk.

### Added (2)

| Path | sha256 | Lines |
|---|---|---|
| `/root/GEOX/.github/workflows/surface-drift-gate.yml` | `86884e80c2f7cac3afafdca65d102d2337fa260aaef34dd16b5ddfa47c9ee285` | 92 |
| `/root/GEOX/tests/test_rt1_recovery_derivation.py` | `3b0a7293cb09951f40278bd94c9db1861036427ddeae4d1c547cacdb1c6cb181` | 287 |

### Byte-identical (regenerator touched, output unchanged)

`/root/GEOX/llms.txt` = `14da26e66a974b60c1f6aac5fac2ba780a848e78bc7fb6df5bd807c516b563be` and `/root/GEOX/README.md` = `934551c1fc5d600cde98d340d189b50394750387b339fd1ac14398addea7548d` — **unchanged old→new**. The generator rewrote them with identical bytes; `git diff` reports nothing.

**Rollback (F1 AMANAH):** every change is git-tracked and uncommitted. `cd /root/GEOX && git checkout -- <path>` restores rows 1–8; `rm` the two added files. A pre-regeneration snapshot also exists at `/tmp/geox_snap/`.

---

## 2. Step 1 — CI gate

- **Workflow YAML path:** `/root/GEOX/.github/workflows/surface-drift-gate.yml` (name: `🔒 Surface Drift Gate (registry.py truth)`)
- **Hash function:** `sha256` — the house function already used by `surface_manifest.py:272`. No new hash introduced.

### `--check` mode did NOT exist — added

The generator had only default-write and `--dry-run`. I added `--check` **additively**: one new `argparse` flag, one early return in `main()`, and new functions (`normalize_timestamps`, `content_sha256`, `_render_surface`, `run_check`) inserted before `main()`. **No existing mode was altered** — `--dry-run` and default-write byte-for-byte behaviour is unchanged.

`--check` regenerates each of the 6 surfaces **in memory** (via each generator's `dry_run=True` path, capturing the string it would write), hashes it, and compares against the committed artifact on disk. **It writes nothing.**

### The trap I had to design around (OBS, proven by experiment)

A naive "regenerate → sha256 → compare" gate is **permanently red**. 4 of the 6 generators embed a wall-clock stamp (`regenerated`, `generated_at`, `policy`, `version`, `schema_version`, `contract_epoch`) from `datetime.now()`. I proved this by running the generator twice, one second apart:

```
ARTIFACT                                 RUN1==RUN2 (raw sha256)
  tools_sot.yaml                         VOLATILE
  CANONICAL_PUBLIC_SURFACE.json          VOLATILE
  tools.json                             VOLATILE
  llms.txt                               STABLE
  contracts/tools.yaml                   VOLATILE
  README.md                              STABLE
```

So `--check` hashes **timestamp-normalised** content: clock churn is stripped to a fixed token before hashing, identically on both the generated side and the committed side. Genuine drift — a tool added/removed, a domain changed, a pack changed, a count changed — still alters the hash and still fails the build. This is why the requirement "hash-stable" needed interpretation rather than literal implementation; a literal reading would have produced a gate that cries wolf on every commit and trains agents to ignore red.

**Corollary finding (OBS):** the incident brief's premise that "4 of 6 surfaces CHANGED" indicated real drift is **wrong**. I diffed committed-vs-generated line by line and the entire difference was timestamps. Real content drift at session start was **zero**:

```
tools_sot.yaml                 6 differing lines  → all version/regenerated stamps
CANONICAL_PUBLIC_SURFACE.json  3 differing lines  → all generated_at
tools.json                     5 differing lines  → all version/policy stamps
llms.txt                       0 differing lines
contracts/tools.yaml           9 differing lines  → all Regenerated/schema_version/contract_epoch
README.md                      0 differing lines
```

`diff_label()` compares raw strings, so it reports `CHANGED` on clock churn alone. That is a **reporting defect in the existing generator**, not surface drift.

### Failure mode — what makes the build red

Fail-closed on all four paths. `set -o errexit` + `set -o pipefail`, no `|| true`, no tee masking, no advisory echo:

| Condition | Result |
|---|---|
| Generator raises / crashes | caught per-surface → counted as drift → **exit 1** |
| Committed artifact drifted | hash mismatch → **exit 1** |
| Committed artifact missing | → **exit 1** |
| `registry.py` unimportable | import fails → **non-zero** |
| Full match across all 6 | **exit 0** |

### Local dry-run of the gate (no push, no deploy)

**Baseline — clean tree:**
```
═══ GATE RESULT ═══
  Surfaces checked: 6
  Missing:          0
  Drifted:          0
  PASS — every surface is in sync with registry.py. No drift.
EXIT: 0
```

**Positive control 1 — injected stale count into `tools_sot.yaml` (`public_count: 26 → 25`):**
```
DRIFT   tools_sot.yaml  committed=c8df89f18a9ff292…  generated=b0a5b2fb75f4ede4…
Drifted:          1 ['tools_sot.yaml']
FAIL — committed surfaces do not match registry.py truth.
EXIT CODE: 1        (restored afterwards)
```

**Positive control 2 — injected phantom tool into committed `tools.json` (`geox_phantom_tool`):**
```
DRIFT   tools.json  committed=4d9bfa0425566055…  generated=eb194f9dec69d420…
Drifted:          1 ['tools.json']
FAIL — committed surfaces do not match registry.py truth.
EXIT CODE: 1        (restored afterwards)
```

The gate fires in **both** directions. Per the paired-canary scar discipline, I ran the negative canary alongside the positive one — a gate that only ever passes proves nothing, and a gate that only ever fails is noise. Both controls were reverted; `git status` confirmed the tree returned to exactly the intended change set.

**Post-Step-2, the gate caught my own legitimate drift before I regenerated** (`DRIFT CANONICAL_PUBLIC_SURFACE.json`, exit 1) — the gate detecting a real truth change is exactly its job. After regeneration: exit 0.

---

## 3. Step 2 — Recovery tool pinning

### The 6 unpacked tools (verbatim)

Public tools in `tools_manifest.yaml` belonging to **no** `capability_packs` entry (20 packed of 26 public):

```
geox_surface_status
geox_calibration_register_witness
geox_extract_display_proxy
geox_register_native_source
geox_extract_native_trace
geox_list_registered_sources
```

Only `geox_surface_status` was pinned — the other 5 are **not** recovery tools and pinning them would have exceeded scope. They remain unpacked and are listed as an open question in §7.

### Scope correction — where packs actually live

The task said to find pack assignment in `registry.py`. Measured reality: `registry.py` contains **no** pack data. It calls `capability_packs()` from `surface_manifest.py:175`, which reads `capability_packs:` out of **`tools_manifest.yaml:1833`**. Consumers confirmed by grep — `capability_packs()` is called from exactly three places: `registry.py:252` (`tools_for_profile`), `registry.py:272` (`pack_for_tool`), and `generate_all_surfaces.py:170`. None of them owns pack membership.

So the minimal correct edit is 1 data line in `tools_manifest.yaml`, not a `registry.py` change.

### Which pack(s) `geox_surface_status` was added to

**`earth_core` only** — deliberately.

Evidence driving that choice, from the manifest entry itself: `tier: A`, `governance.action_class: OBSERVE`, `mutation: false`, `annotations.read_only: true`, `family: view`. And from `capability_registry.yaml`: `earth_core` has `default_visible: true`, `escalation_required: false`, and is the **only pack listed in all four profiles** (`default`, `specialist`, `research`, `full`).

The task's hypothesis was "at minimum the same packs that contain mutating tools, because mutation is what triggers RT1 rejection." That does not hold here: RT1 rejects on **name-not-on-surface**, which is independent of mutation class — a caller can be rejected for a ghost name while holding only OBSERVE authority. The binding requirement is that the recovery tool be visible under **every** profile, and a single `earth_core` pin achieves that for all four. Adding it to `earth_specialist`/`earth_research` too would have been redundant — `tools_for_profile` de-duplicates via its `seen` set, so the extra lines would add maintenance surface with zero behavioural gain.

### Before → After (`tools_for_profile`, measured live)

| Profile | Before | After | `geox_surface_status` visible |
|---|---|---|---|
| `default` | 13 | **14** | False → **True** |
| `specialist` | 19 | **20** | False → **True** |
| `research` | 20 | **21** | False → **True** |
| `full` | 20 | **21** | False → **True** |

`pack_for_tool('geox_surface_status')`: `None` → **`earth_core`**.

Note the `research` profile was **20, not 26** as the task stated — the brief's 20 is correct; `capability_registry.yaml`'s advertised 26 is the wrong number (§7 item 1).

**Verification re-executed:** `set(tools_for_profile('research')) <= set(public_tool_names())` → `True`. Every profile is a subset of the callable surface; no profile advertises an uncallable tool (asserted permanently in `test_every_profile_is_a_subset_of_the_callable_surface`).

I also checked for tests asserting pack/profile counts before editing, so this would not land blind: `grep` across `tests/` found **no** test asserting `tools_for_profile` lengths, `earth_core` membership, or the `tool_count` fields in `capability_registry.yaml` (which no Python code reads at all). The 12 failures in §4 are unrelated and pre-existing.

---

## 4. Step 3 — RT1 recovery derivation

### Old code — the f-string literal (`geox_middleware.py:721-730` at git HEAD)

```python
        # ── RT1: tool name must be in executable surface (canonical + compat) ──
        if tool_name not in self._EXECUTABLE_SURFACE:
            # Special-case: arifos_route_query gets a pass-through when feature-flagged
            if not (self._arifos_route_query_enabled and tool_name == "arifos_route_query"):
                logger.warning(f"RT1_BLOCK: tool '{tool_name}' is not on canonical public surface")
                raise ToolError(
                    f"RT1_GUARD: Tool '{tool_name}' is not on the canonical or compat surface. "
                    f"Canonical surface has {len(self._PUBLIC_SURFACE)} declared tools. "
                    f"Use geox_surface_status(mode='registry') to enumerate available tools."
                )
```

The literal was unfalsifiable: it named `geox_surface_status` while that tool was in **no** pack, hence invisible to every discovery profile. RT1 recommended a recovery path the caller could not resolve. Nothing enforced `recommended_next ⊆ callable_surface` — there was no `recommended_next` at all.

### New code — derivation (`geox_middleware.py:726-769`)

```python
                _recovery_tool: str | None = None
                try:
                    from geox_mcp.registry import derive_recovery_tool, recovery_is_callable

                    _candidate = derive_recovery_tool(tool_name)
                    if recovery_is_callable(_candidate):
                        _recovery_tool = _candidate
                except Exception as _rec_exc:
                    logger.error(f"RT1_RECOVERY_DERIVE_ERROR: {type(_rec_exc).__name__}: {_rec_exc}")

                if _recovery_tool:
                    _hint = f"Use {_recovery_tool}(mode='registry') to enumerate available tools."
                    _rec_line = f"recommended_next: {_recovery_tool}"
                else:
                    _hint = ("No callable recovery tool is registered — ... This is a registry "
                             "defect, not a caller error. Escalate to the organ owner.")
                    _rec_line = "recommended_next: null"

                raise ToolError(
                    f"RT1_GUARD: Tool '{tool_name}' is not on the canonical or compat surface. "
                    f"Canonical surface has {len(self._PUBLIC_SURFACE)} declared tools. "
                    f"{_hint} "
                    f"[{_rec_line} · derived-from-registry, verified-callable={bool(_recovery_tool)}]"
```

The derivation itself lives in `registry.py:291-373` (`derive_recovery_tool`, `recovery_is_callable`, `_is_non_mutating`) per the task's requirement that it "call into registry.py". Selection order, first match wins: (1) non-mutating + recovery-name-pattern tools sharing a pack with the rejected tool; (2) same criteria across all packs — necessary because the commonest RT1 rejection is a ghost/unknown name in no pack; (3) same criteria over the whole callable surface. Every candidate must satisfy `name in public_tool_names()` **and** `mutation != true` **and** `action_class ∈ {OBSERVE, OBSERVE_ONLY}` **and** name matching `surface|status|registry|discover`. Returns `None` when nothing qualifies — never a fabricated name. The lazy import matches the existing house pattern (`authority_gate`, `organ_governance` are imported the same way) to avoid the circular-import chain.

Two hardening details beyond the brief: if derivation returns a name that is *not* callable, it is logged as `RT1_RECOVERY_UNCALLABLE` and **suppressed** rather than surfaced; and if derivation raises, RT1 **still blocks** — the suggestion fails closed, never the rejection. A missing hint must not open the gate.

### Live output through the REAL middleware (not a reimplementation)

```
--- RT1 for 'geox_well_desk_open' ---
RT1_GUARD: Tool 'geox_well_desk_open' is not on the canonical or compat surface.
Canonical surface has 1 declared tools. Use geox_surface_status(mode='registry') to
enumerate available tools. [recommended_next: geox_surface_status ·
derived-from-registry, verified-callable=True]
```
Identical derivation for `geox_discover_stuff` and `totally_unknown`.

### Test results

`/root/GEOX/tests/test_rt1_recovery_derivation.py` — **18 passed** (`PYTHONPATH=src pytest -q`). All three required cases plus hardening:

1. **Ghost rejection** — RT1 rejects `geox_well_desk_open` → `recommended_next` is `geox_surface_status`, asserted callable and `in public_tool_names()`. Precondition asserted too: the name really is off the surface, so the test cannot pass vacuously if it is ever re-published.
2. **Discovery-name rejection** — `geox_discover_stuff` → `geox_surface_status`, callable.
3. **Negative case** — with `public_tool_names()` monkeypatched to `[]`, derivation returns `None`, and driven end-to-end through the real middleware the message carries `recommended_next: null`, `verified-callable=False`, no tool name, and the words "registry defect". A second negative patches the surface to `["geox_basin","geox_claim"]` (callable but no recovery-shaped name) → also `None`.
4. **Anti-fabrication invariant** — across 7 rejected names, any non-`None` return is asserted `in public_tool_names()`.
5. **No-literal regression guard** — isolates the RT1 block by source slicing and asserts `geox_surface_status` does **not** appear in it, so the literal cannot be reintroduced silently.
6. **Step 2 invariants** — the pinned tool has a pack, is present in every profile, and every profile is a subset of the callable surface.
7. **End-to-end cross-check** — `test_derived_recovery_is_visible_through_discovery`: the tool RT1 derives is also discoverable via `tools_for_profile('research')` and `('default')`. Before the fix these two disagreed; that disagreement *was* the incident, and it is now a permanent assertion.

**Methodology correction I applied mid-task:** my first draft of the middleware test rebuilt the message string inside the test body, then asserted on it. That measures the test's own construction, not the substrate — exactly the scar class logged twice on 2026-09-28. I replaced it with a driver that calls the real `GeoxGovernanceMiddleware.on_call_tool` through a minimal context object and captures the actual `ToolError`. The current tests exercise shipped code paths only.

### Regression status — baseline compared, not assumed

Same 13-file surface/registry suite, stashed tree vs changed tree:

| | Failures | Passed |
|---|---|---|
| **Baseline** (`git stash`, pristine) | 12 | 111 |
| **After steps 1–3** | 12 | **129** (+18 new) |

**Same 12 failures, same names, zero new failures.** The 12 are pre-existing and unrelated to this repair (stale `public_count_target: 31` vs real 26, a ZEN-24 frozen-count assertion, and a `test_gateway_authority` seal-session case). They are surfaced in §7 rather than fixed — fixing them means changing `public_count_target`, which is canonical-record territory and not in steps 1–3.

`ruff check` and `ruff format --check` (the `geox-ci` lint gate, `--line-length 130`) pass clean on all 4 files I authored or edited. Baseline `ruff format` on `registry.py` was clean before my edit and is clean after.

---

## 5. No-touch attestation

| Item | Status | Evidence |
|---|---|---|
| `/opt/geox/` | **NOT TOUCHED** | `find /opt/geox -newermt "2026-10-01 11:40:00" -type f` → **empty**. No file under `/opt/geox` has an mtime within this session. |
| `build_info_handler` / anything returning `_GIT_VERSION` | **NOT TOUCHED** | Step 4 HELD. Not in `git diff --name-only`; no edit performed. |
| `geox_well_desk_open` ghost entries (`server.py:132` timeout map, `organ_governance.py:56`) | **NOT TOUCHED** | `git diff --name-only \| grep -E "server.py\|build_info"` → **CLEAN**. `server.py` and `organ_governance.py` absent from the diff. The name appears in my work only as a *test input string* and as an RT1 rejection subject. |
| `/root/AAA/mcp.json` | **NOT TOUCHED** | Not in scope; no read, no write. |
| `/opt/geox/.well-known/mcp/server.json` | **NOT TOUCHED** | Under `/opt/geox` — covered by the empty `find` above. Lane 555's binary. |
| Network fetch | **Not made** | No `curl`/`wget`/WebFetch/firecrawl invocation. No `/opt/geox` ↔ `/root/GEOX` reconciliation attempted. All evidence is local-file or in-process. |
| `ROOT_AGENT_CONFIG.yaml` | **NOT TOUCHED** | Not read, not written. |
| Any `AGENTS.md` / adapter file | **NOT TOUCHED** | Absent from `git diff --name-only`. |
| Deploy / restart / service-affecting command | **None run** | No `systemctl`, no service restart, no deploy. The generator ran against the source tree only; the live `:8081` organ was never invoked. |

**Full change set (complete, nothing else):**
```
 M contracts/tools.yaml                                  (generated)
 M scripts/generate_all_surfaces.py                      (Step 1)
 M src/geox_mcp/generated/CANONICAL_PUBLIC_SURFACE.json   (generated)
 M src/geox_mcp/geox_middleware.py                       (Step 3)
 M src/geox_mcp/registry.py                              (Step 3)
 M src/geox_mcp/tools_manifest.yaml                      (Step 2)
 M tools.json                                            (generated)
 M tools_sot.yaml                                        (generated)
?? .github/workflows/surface-drift-gate.yml              (Step 1)
?? tests/test_rt1_recovery_derivation.py                 (Step 3)
```

**Nothing is committed.** All changes sit in the working tree so Lane 555 / Arif can review or `git checkout --` them wholesale.

---

## 6. Verification commands run (read-only)

**`git status --porcelain` on `/root/GEOX`** → the 10-entry block reproduced verbatim in §5.

**`git diff --stat` on `/root/GEOX`** →
```
 contracts/tools.yaml                                |   6 +-
 scripts/generate_all_surfaces.py                    | 167 +++++++++++++++++++++
 .../generated/CANONICAL_PUBLIC_SURFACE.json         |  15 +-
 src/geox_mcp/geox_middleware.py                     |  40 ++++-
 src/geox_mcp/registry.py                            |  87 +++++++++++
 src/geox_mcp/tools_manifest.yaml                    |  10 ++
 tools.json                                          |   4 +-
 tools_sot.yaml                                      |   4 +-
 8 files changed, 321 insertions(+), 12 deletions(-)
```

**`find /opt/geox -newermt "2026-10-01 11:40:00" -type f`** → **EMPTY** (exit 0). Deployed runtime untouched.

Additional read-only checks:
- `python3 scripts/generate_all_surfaces.py --check` → **exit 0, PASS, 6/6 surfaces OK**
- `python3 scripts/generate_all_surfaces.py --dry-run` → ran, wrote nothing
- `pytest tests/test_rt1_recovery_derivation.py -q` → **18 passed**
- `pytest` on 13-file surface/registry suite, changed tree → **12 failed, 129 passed**
- same suite on `git stash`ed pristine tree → **12 failed, 111 passed** (identical failure set)
- `ruff check` + `ruff format --check --line-length 130` on my 4 files → **All checks passed / 4 files already formatted**
- `python3 -m py_compile` on all 4 files → **OK**
- `yaml.safe_load` on `surface-drift-gate.yml` → parses; triggers `push`/`pull_request`/`workflow_dispatch`; gate step contains `--check`, `errexit`, `pipefail`
- `git grep -n "^<<<<<<<\|^>>>>>>>" -- .github/workflows/` → **found the pre-existing conflict in `09-boundary-ratchet.yml`** (§7 item 3)
- `git stash push`/`pop` used twice for baseline comparison — tree fully restored both times, confirmed by `git status`

---

## 7. Open questions for Lane 555 / Arif

**Q1 — `capability_registry.yaml` advertises counts the code cannot produce. Fix the YAML or the packs? (F13-class: canonical record)**
It claims `research → 26` / `full → 26`; live code returns **21**. `registry.py:239`'s docstring repeats `research → all packs (26 tools)`. The `tool_count` fields are read by **no** Python code (grep-verified) — pure prose that has drifted from behaviour. Two of the six unpacked tools are needed to reach 26. Closing the gap means deciding what `earth_research` should contain, which is a discovery-surface policy call, not a repair. **I did not touch it.**

**Q2 — the other 5 unpacked public tools. In scope for a follow-up lane?**
`geox_calibration_register_witness`, `geox_extract_display_proxy`, `geox_register_native_source`, `geox_extract_native_trace`, `geox_list_registered_sources`. All invisible under every profile, same mechanism as the `geox_surface_status` bug. `geox_list_registered_sources` in particular looks like it *should* be discoverable. I pinned only the recovery tool per scope. **These are the same defect class and are still open.**

**Q3 — `public_count_target: 31` vs real 26. This is why 12 tests fail. (F13-class)**
`tools_manifest.yaml:4` sets 31; the public surface is 26; `surface_attestation()` returns `ok=False, error=SURFACE_COUNT_DRIFT` — a live, continuously-failing invariant that nothing gates on. Several of the 12 pre-existing failures trace to this and to a `test_app_export_parity` assertion frozen at "ZEN-24". Correcting the target to 26 (or resurrecting 5 tools) changes canonical records. **Held.**

**Q4 — `.github/workflows/09-boundary-ratchet.yml` has committed merge-conflict markers. (needs an owner)**
`<<<<<<< HEAD` at line 26, `>>>>>>> feat/mcp-dual-era-2026-07-28` at line 32 — a `actions/checkout@v7`/`setup-python@v7` vs `@v4`/`@v5` conflict. This is **invalid YAML**; the workflow cannot run. It was committed in `79e372e5` ("merge: feat/mcp-dual-era-2026-07-28 → main — canonical surface reconcile"). The boundary ratchet has therefore been **silently not executing** since that merge. Two-line fix, but it is a merge-conflict resolution requiring a judgement on which action versions to keep, and it is outside steps 1–3. **Flagging for Lane 555 / Arif.** This is scar-class: a broken gate looks identical to a passing gate from the outside.

**Q5 — should `diff_label()` stop reporting timestamp churn as `CHANGED`?**
The existing summary counts clock-only differences as changes, which is what produced the "4 of 6 surfaces CHANGED" reading that framed this incident as surface drift when real drift was zero. `normalize_timestamps` from my `--check` work would fix it, but changing the default-mode report is out of scope. **Advisory.**

**Q6 — does the gate want a broader path filter?**
`surface-drift-gate.yml` currently triggers on `paths:` limited to the truth files and the surfaces. A change to a *generator helper* outside that list would not re-trigger the gate. `workflow_dispatch` and all-PR triggering cover the gap, but a wider filter may be preferred. **Advisory, one-line change.**

---

## 8. Scar-class evidence found

1. **A committed broken CI gate masquerading as a live one** (Q4). `09-boundary-ratchet.yml` has contained merge-conflict markers since commit `79e372e5`. YAML-invalid → workflow never runs → the boundary ratchet has been unenforced while appearing configured. Same class as *"Scar HERMES MCP organs_alive misleading"* (alive ≠ healthy) and *"Scar FORGE INIT SEAL refused at DEPLOYMENT_DRIFT"*: **declared ≠ enforced**. Nothing in the federation noticed, because a workflow that fails to parse produces no red build — it produces no build.

2. **A live invariant failing continuously with no consumer.** `surface_attestation()` returns `ok=False / SURFACE_COUNT_DRIFT` on every call because `public_count_target: 31` ≠ actual 26. The check exists, runs, fails, and nothing gates on it. Measurement without consequence — the "silent failure class" already named in the sealed entropy-metabolism EUREKAs.

3. **A generator whose drift report is mostly clock noise** (Q5). `diff_label()` compares raw strings including timestamps, so `CHANGED: 4/6` reads as "four surfaces drifted" when zero had. That single misreading shaped the incident brief's premise. **Description ≠ enforcement**, again — the report described churn as drift.

4. **A self-measuring test caught and removed mid-task.** My first draft of the RT1 middleware test reconstructed the error string inside the test body and asserted on that reconstruction — it would have passed even if the middleware were still hardcoded. This is precisely *"Scar audit methodology fork-bias"* / *"claimed-before-checking twice"*: an audit script measuring its own construction. I replaced it with a driver invoking real `on_call_tool`. **Recorded because the scar nearly recurred a third time, in my own work, in the same session that cited it.**

5. **A literal recommendation pointing at an unreachable tool** — the incident itself. RT1 said "use `geox_surface_status`" while that tool was in no pack and invisible under all four profiles. The recovery instruction was syntactically valid and semantically void. Now closed by derivation plus `test_derived_recovery_is_visible_through_discovery`, which makes the two facts agree permanently rather than by convention.

---

*Forged 2026-10-01 by claude-code/FI-002 (Lane 333d) under F13 SOVEREIGN.*
*Step 4 (`build_info_handler`) HELD — not touched. Nothing committed. Nothing deployed.*
*DITEMPA BUKAN DIBERI — Forged, not given.*
