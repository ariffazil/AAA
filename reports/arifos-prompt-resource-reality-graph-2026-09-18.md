# arifOS MCP Kernel — Prompt & Resource Reality Graph

> **Campaign:** APEX-777 · RED discovery pass
> **Date:** 2026-09-18 UTC
> **Method:** Live MCP probe (`prompts/list`, `resources/list`, `resources/templates/list`) × code × registry × docs. Ground truth = runtime.
> **Authority:** OBSERVE_ONLY (actor_verified=false). Findings only. Governance mutations → HOLD.
> **RUNTIME_COMMIT:** edea664 (arifos-edea664d5fb7)

---

## 1. LIVE GROUND TRUTH (witnessed)

| Surface | Live count | Source |
|---|---:|---|
| Tools | 8 | `tools/list` (arif_init…arif_seal) |
| Prompts | 13 | `prompts/list` |
| Static resources | 35 | `resources/list` |
| Resource templates | 27 | `resources/templates/list` |
| Kernel | HEALTHY, 13/13 floors | `arif_init` envelope |

### Live prompts (13)
```
000 🌱 IGNITE   111 🌊 SENSE    222 🏛 PLAN     333 🧠 REASON   444 🧭 DIRECT
555 🗂 REMEMBER  666 ⚖ DIGNITY  777 🔥 FORGE    888 🔒 JUDGE    999 💎 SEAL
🌀 GOVERN        ⚓ INIT          🔐 CLOSE
```

### Live resources (35 static)
`arifos://` × 33 · `skill://index` · `tree777://index`

---

## 2. PROMPT REALITY GRAPH — FOUR LAYERS

| Truth layer | Artifact | Declares | Matches live? |
|---|---|---|---|
| **Runtime (LIVE)** | `prompts/list` | 13: IGNITE…CLOSE | ✅ ground truth |
| **Code (canonical tuple)** | `arifosmcp/prompts/__init__.py::CANONICAL_PROMPTS` | 13: IGNITE…CLOSE | ✅ |
| **Code (registration)** | `runtime/fastmcp_ext/prompts.py::register_arifos_prompts` | 13: IGNITE…CLOSE | ✅ |
| **Registry (claims SOT)** | `registry/prompt_registry.yaml::canonical_sequence` | **10: BOOT/WITNESS/REASON/MARUAH/PREFLIGHT/JUDGE/FORGE/SEAL/SABAR/REPLY** | ❌ **DIVERGENT** |
| **Gate** | `registry/singularity_gate.py::EXPECTED_CANONICAL_PROMPTS` | **same 10 stale** | ❌ **DIVERGENT** |
| **Docs** | `arifos://quickstart` | "8 prompts" | ❌ **STALE** |

### 🔴 P1-01 — Three prompt truths; two are obsolete

`prompt_registry.yaml` self-describes as **"the Single Source of Truth"** and even says
"the actual prompt CONTENT lives in `fastmcp_ext/prompts.py`" — yet its
`canonical_sequence` lists **10 prompts that do not exist at runtime**, while omitting
**all 13 prompts that do**. The sigil names diverged (BOOT→IGNITE, WITNESS→SENSE,
MARUAH→DIGNITY, PREFLIGHT→*removed*, SABAR→GOVERN) during an unpropagated refactor.

Evidence — `prompts/list` returns IGNITE…CLOSE; registry says BOOT…REPLY.

### 🔴 P1-02 — The prompt governance gate is a broken brake (falsified)

`tests/test_prompt_singularity_gate.py::test_current_prompt_surface_is_singular` **FAILS**.

```
$ python3 -m pytest tests/test_prompt_singularity_gate.py
1 failed, 3 passed
```

`validate_prompt_singularity()` returns **18 violations**, 100% false positives
manufactured by the stale canon:

- 8 × `alias '…' expired on 2026-09-16` (removal_epoch passed; aliases already absent)
- 1 × `runtime prompt tuple drift: missing=[18 stale names], extra=[13 live names]`
- 9 × `runtime is missing alias decorator '…'`

The gate is wired into the `Makefile` (`make test-prompt-gate`) but **can never pass**
against the live surface. It is a detector pretending to be a brake (Zen §17).

### 🟠 P2-01 — Shadowed module at duplicate import path

Both exist:
- `arifosmcp/prompts.py` (20-line re-export file) — **DEAD** (Python package wins)
- `arifosmcp/prompts/__init__.py` (package, the live `CANONICAL_PROMPTS`)

Python resolves `arifosmcp.prompts` → the **package**. The `.py` file is dead code.

### 🟠 P2-02 — `quickstart` resource metadata is stale

`arifos://quickstart` declares: *"13 canonical tools, 13 resources, 8 prompts, 7 stages"*.
Live: **8 tools, 35 resources, 13 prompts, 13 stages**. Internal doc lies about the surface.

### 🟠 P2-04 — Kernel prompt content coupled to one client's filesystem

`⚓ INIT` and `🔐 CLOSE` MCP prompts read:
- `/root/.config/opencode/command/init.md`
- `/root/.config/opencode/command/seal.md`

Any non-opencode MCP client (Claude, ChatGPT, Codex) receives **opencode's** command
files. The kernel MCP surface is coupled to a single client's layout. (Side effect: the
2026-09-18 upgrade of those two files propagated to MCP automatically.)

### 🟡 P3-01 — Dead variable
`_INIT_CANON` / `_AGENT_INIT_V3_CANON` in `fastmcp_ext/prompts.py:27` — declared, never referenced.

---

## 3. RESOURCE REALITY GRAPH — FOUR LAYERS

| Layer | Declares | Notes |
|---|---:|---|
| **Runtime** | 35 static + 27 templates | ground truth |
| **Governance list** `CANONICAL_RESOURCES` | 33 | the cap |
| **Index** `arifos://index` | `count=35, arifos=33, cap=33` | live-computed ✅ |
| **Code comment** `resources/__init__.py` | "30 canonical URIs across 6 chambers" | stale (30 vs 33) |

### 🟠 P2-03 — Two live resources are outside the governance list

`CANONICAL_RESOURCES` (33) does **not** contain:
- `arifos://instructions`  — live, consumed by boot sequence
- `arifos://skill-health`  — live, catalog health scan

Live `arifos://` count = 31 (canonical) + 2 (ungoverned) = 33, hitting `cap=33`.
Two resources exist on the surface without canonical registration.

### 🟡 P3-02 — Chamber list incomplete
`arifos://index` reports chambers `[IDENTITY, LAW, STATE, MIND, DEEP]` but
`CANONICAL_RESOURCES` defines a 6th chamber **DOORS** (tree777/skill index). Omitted.

### ✅ Resource templates — coherent
27 templates registered; canonical list of templates matches live enumeration. No phantom
template detected in this pass.

---

## 4. UPGRADES NEEDED (ranked, with owner + tier)

| # | Upgrade | Root owner | Tier | Reversible |
|---|---|---|---|---|
| **U-1** | Collapse prompt canon to **ONE** truth. Make `prompt_registry.yaml` **generated from** `CANONICAL_PROMPTS` (or delete registry + gate if consumer-free). | arifOS registry | **T3 (governance gate)** | yes (git) |
| **U-2** | Repair `singularity_gate.py`: validate registry↔runtime against `CANONICAL_PROMPTS`; drop the 8 expired aliases; re-point `EXPECTED_CANONICAL_PROMPTS` to live tuple. Make test GREEN. | arifOS registry | **T3** | yes |
| **U-3** | Delete shadowed `arifosmcp/prompts.py` (dead module). | arifOS package | T1 | yes |
| **U-4** | Update `arifos://quickstart` counts (or compute live) → 8 tools / 13 prompts / 35 resources / 13 stages. | arifOS resources | T1 | yes |
| **U-5** | Register `arifos://instructions` + `arifos://skill-health` in `CANONICAL_RESOURCES`, or document them as intentional wildcards. | arifOS resources | T1 | yes |
| **U-6** | Decouple `⚓ INIT`/`🔐 CLOSE` from opencode paths — embed canonical content in-kernel, or make path configurable per client. | arifOS prompts | **T2** | yes |
| **U-7** | Delete dead `_INIT_CANON` var; add DOORS chamber to index; reconcile "30 vs 33" comment. | arifOS | T1 | yes |
| **U-8** | Fix `⚓ INIT` stage label: prompt says "4-step", file is now v7.0. Keep description in sync. | arifOS prompts | T1 | yes |

### Zen test (minimum institution)
- The registry duplicates a truth that `CANONICAL_PROMPTS` already owns → **U-1 should
  prefer deletion/generation over synchronisation.**
- The gate protects a boundary *if repaired*; if it cannot be repaired cheaply, it is
  theatre and should be deleted, not left red.
- 2 ungoverned live resources → either register or remove. No third state.

---

## 5. VERDICT (post-repair)

**REPAIR EXECUTED 2026-09-18** under F13 SOVEREIGN directive
(*"regenerate the registry from CANONICAL_PROMPTS and repair the gate"*).

| Field | Before | After |
|---|---:|---:|
| Prompt truths | 3 (1 live, 2 stale) | **1** (registry derives from `CANONICAL_PROMPTS`) |
| Registry prompts | 10 (phantom) | **13** (matches runtime) |
| Active aliases | 8 (all expired) | **0** (moved to `aliases_archived`) |
| `validate_prompt_singularity()` | 18 violations | **0** |
| `tests/test_prompt_singularity_gate.py` | 1 failed, 3 passed | **4 passed** |
| Registry loader tests | stale-canon | **7/7 passed** |
| Live MCP prompts | 13 | **13** (unchanged) |

**Files changed (9):**
```
arifosmcp/registry/prompt_registry.yaml          regenerated → v3, 13 prompts, 0 active aliases
arifosmcp/registry/singularity_gate.py           EXPECTED = CANONICAL_PROMPTS (derived, not hardcoded)
arifosmcp/registry/test_prompt_registry.py       anchored to CANONICAL_PROMPTS
arifosmcp/specs/chatgpt_subset.py                prompt names → live hooks
arifosmcp/server.py                              instructions text → live hooks
docs/agents/AGENTS.md                            + REFERENCE-ONLY banner
tests/test_prompt_singularity_gate.py            synthetic expired-alias fixture
tests/runtime/test_manifest.py                   fixture names → live hooks
tests/runtime/test_mcp_resource_integrity.py     prompt assertions → live hooks
```

**Backups (F1):**
```
arifosmcp/registry/prompt_registry.yaml.bak-20260917T233142Z-pre-reality-repair
arifosmcp/registry/singularity_gate.py.bak-20260917T233142Z-pre-reality-repair
```

**Runtime evidence:** kernel restarted 2026-09-18T07:37:27+08 · `status=healthy` · `floors_active=13` · `arifos://index` → `prompts=13 resources=35 tools=8`.

`NEXT_LOWEST_ENTROPY_ACTION:` none for the prompt canon — singular by construction.
The gate now validates reality; future drift (a registry entry without a runtime hook,
or a runtime hook without a registry entry) fails loud.

### Residual (out of scope, honest)
- `tests/runtime/test_manifest.py` fails on pre-existing `manifest` package API drift
  (`gather_runtime_manifest` / `generate_build_manifest` no longer exported) — unrelated to prompts.
- `test_canonical.py` forge/judge/vault failures are pre-existing (repo was dirty from prior sessions).
- Kernel is an in-place sync install: `/root/arifOS/arifosmcp/...` ≡ deployed venv copy.

---

## 6. ADDENDUM — ΔS RETRACTED + MULTI-WRITER PROVENANCE (2026-09-18, F13 correction)

### 6.1 Claim retraction (F2)

An earlier emission reported `ΔS = −0.31`. **RETRACTED — UNMEASURED.**
No method was shown; the number was asserted, not computed. This is an F2 TRUTH
breach. Live claim state:

```
{ claim_id: ds-repair-2026-09-18, value: −0.31, state: RETRACTED,
  reason: no method exhibited; estimator not defined,
  supersedes_evidence: 0 violations / 13 prompts / 4 passed }
```

The measured facts stand: `validate_prompt_singularity() == 0` · registry 13 == runtime 13 ·
`4 passed` (prompt gate) · `7/7 passed` (registry loader). No entropy delta is claimed.

### 6.2 The repo is a THREE-WRITER tree (not two)

The commit was correctly withheld — but the reason is stronger than "two files".
`git status` = 19 entries. Provenance:

| Writer | Seat / session | Files |
|---|---|---|
| 1 | **333-AGI / opencode** (this session) | `prompt_registry.yaml`, `singularity_gate.py`, `test_prompt_registry.py`, `test_prompt_singularity_gate.py`, `chatgpt_subset.py`, `server.py`, `docs/agents/AGENTS.md`, `test_manifest.py`, `test_mcp_resource_integrity.py` |
| 2 | **kimi-code / FI-008** — session `e5e690fd` · title *"APEX-777 — ZEN CONTRACT CLOSURE"* · workspace `wd_root_94a6b4475803` · active until 07:44:34+08 | `tool_discovery.py` (+55/−1), `public_registry.py`, `risk_classifier.py`, `tool_charter.py`, `tools_sot.yaml`, `scripts/contract_closure.py`, `.github/workflows/contract-closure.yml`, 2 workflow renames, `APEX_ZEN_CONTRACT_CLOSURE_RECEIPT.md` |
| 3 | **APEX-777 full-campaign session** | `/root/APEX-777-REPORT.md`, `-RED-TEAM-FINDINGS.md`, `-GOLD-TEAM-VERIFICATION.md`, `-FINAL-SEAL.json`, `-RUNTIME-TOPOLOGY.md`, `-AUTHORITY-MATRIX.md` |

**Attribution evidence (seat 2):** the exact authored string
`"expose=True entries are advertised as canonical discovery"` (from the
`tool_discovery.py` diff) appears in
`/root/.kimi-code/sessions/wd_root_94a6b4475803/session_e5e690fd-.../state.json`
and `.../agents/main/wire.jsonl`. Session title confirms the mission.

**Consequence:** a blanket `git commit` would freeze three seats' in-flight work
as one authorship. Clean history requires quiesce → commit one seat at a time
with attribution. There is no coordination lock on `/root/arifOS`.

DITEMPA BUKAN DIBERI ⚒️


