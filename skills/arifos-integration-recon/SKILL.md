---
name: arifos-integration-recon
description: >
  Read-only code path tracing through the arifOS kernel source to find integration points,
  map decision flows, and design wiring recipes for new capabilities (ML models, external
  services, new organ hooks). Covers: identifying deterministic-vs-ML boundaries, locating
  env-var flip-points, reusing existing client libraries (Ollama, httpx, etc.), understanding
  Pydantic schemas I/O, and writing smoke-test patterns. Trigger: "how to wire X into arifOS",
  "trace the code path for Y", "find the integration point for Z", "how does the judge work",
  "map the decision pipeline", "where to hook ML into the kernel", or any pre-build investigation
  of arifOS source before making a change.
category: autonomous-ai-agents
---

# arifOS Integration Recon — Read-Only Code Path Tracing

Class of work: **investigate arifOS kernel source before wiring a new capability.** Not security auditing (use `kernel-security-claim-audit` for that), not ops (use `arifos-federation-ops`). This is the "look before you leap" layer — mapping decision flows, identifying flip-points, reusing existing patterns, and producing wiring recipes.

## 1. When to load

- User says "how does X work in arifOS", "trace the code path for Y", "find where to hook Z"
- Before wiring a new ML model, external service, or capability into the kernel
- When the user wants to understand a pipeline (judge, seal, measure, etc.) end-to-end
- Pre-build reconnaissance: "I want to do X — show me how the kernel currently works"
- When `ml_method: heuristic` needs to flip to ML
- User says "map the contradictions", "stabilize the kernel", "why does X disagree with Y in the code"
- Before patching a half-wired feature: verify the override/contract is applied at EVERY callsite, not just the response envelope

## 2. Canonical source locations

| What | Path | Notes |
|---|---|---|
| Kernel main | `/opt/arifos/app/arifosmcp/` | Python MCP server, ~25K lines in runtime/tools.py alone |
| Tool implementations | `/opt/arifos/app/arifosmcp/tools/` | One file per organ: judge.py, forge.py, sense.py, etc. |
| Runtime orchestration | `/opt/arifos/app/arifosmcp/runtime/tools.py` | 25K+ lines — canonical wrapper, _compute_canonical_verdict, _synthesize_async |
| LLM cascade client | `/opt/arifos/app/arifosmcp/runtime/llm_client.py` | TokenRouter → FLAME → MiniMax → ... → Ollama → rules; all provider configs here |
| Schemas (Pydantic) | `/opt/arifos/app/arifosmcp/schemas/` | VerdictOutput, AuditResult, etc. |
| ML floor runtime | `/opt/arifos/app/core/shared/law_audit.py` | `get_ml_floor_runtime()` flip-point, FloorAuditor |
| Capability map | `/opt/arifos/app/arifosmcp/runtime/capabilities.py` | `build_runtime_capability_map()` — Ollama/SBERT/DeepSeek gates |
| Health routes | `/opt/arifos/app/arifosmcp/runtime/rest_routes/rest_routes.py` | `:8088/health` surface — ml_floors, semantic_readiness, provider_status |
| **APEX primitives (tool metrics)** | `/opt/arifos/app/arifosmcp/runtime/apex_primitives.py` | `compute_apex_from_metrics()` — G from SQLite tool calls, NOT from floor scores. `MEMBRANE_BRIDGE` (temporary in kernel until A-FORGE TS ready) |
| **APEX calculus (judgment)** | `/root/arifOS/governance/_t000_evaluator/compute_apex.py` | `compute_apex()` — G from 13 floor scores. Different formula than apex_primitives. Contains inverse metric bug (F7/F9). |
| Existing Ollama usage | `/opt/arifos/app/arifosmcp/intelligence/tools/relate_bridge.py` | Proven qwen2.5:3b integration pattern |
| Tests | `/root/arifOS/tests/` | test_canonical.py, golden/e2e/, gi_kernel_readiness/ |

## 3. Investigation methodology

### Step 1: Find the entry point

```bash
# Find all functions that match the tool name
grep -rn "def arif_XXX\|async def arif_XXX\|def _arif_XXX" /opt/arifos/app/arifosmcp/
```

### Step 2: Map the function signatures (Pydantic schema)

```bash
# Find Pydantic models used as input/output
grep -rn "class.*BaseModel\|class.*VerdictOutput\|class.*AuditResult" /opt/arifos/app/arifosmcp/schemas/
```

Read the actual function signature — every parameter is a governance input, not decoration.

### Step 3: Identify deterministic vs ML boundary

Look for: `call_llm()`, `_call_ollama()`, `_synthesize_async()`, `sentence_transformers`, `classify_asi_floors`. If none appear in the verdict/decision path → it's pure deterministic (like judge). If they appear → find which gates run before vs after the LLM call.

### Step 4: Locate the env-var flip-point

Search for `get_ml_floor_runtime`, `ml_floors_enabled`, `ml_method`, `heuristic_fallback`. The function `get_ml_floor_runtime()` in `law_audit.py` is the single flip-point for all ML floor scoring. Key env vars:

| Var | Default | Effect |
|---|---|---|
| `ARIFOS_ML_FLOORS` | unset/false | Enables SBERT floor scoring |
| `ARIFOS_ML_MODEL_NAME` | `all-MiniLM-L6-v2` | SBERT model to load |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama base URL |
| `OLLAMA_MODEL` | `qwen2.5:7b` | Default Ollama text-gen model |
| `OLLAMA_TEXT_ENABLED` | `false` | GATE: Ollama in the LLM cascade |

### Step 5: Reuse existing client patterns

The `_call_ollama()` in `llm_client.py:1410` is the direct path:
```python
from arifosmcp.runtime.llm_client import _call_ollama
raw, parsed = await _call_ollama(
    system="...", user="...", response_schema={...},
    temperature=0.1, max_tokens=400
)
# Returns (raw_output_str, parsed_output_dict)
```

The `call_llm()` in `llm_client.py:2019` goes through the full cascade (TokenRouter first). Use for cloud models; use `_call_ollama` for local-only.

### Step 6: Design the wiring recipe

Rules:
- HARD gates must remain non-overridable (ML cannot upgrade HOLD→SEAL when a hard gate failed)
- ML can only downgrade (SEAL→SABAR, SEAL→HOLD), never upgrade
- Record `meta["ml_method"]` for audit trail
- Schema output must match or be a subset of the tool's Pydantic output model

### Step 7: Write a smoke test

Pattern from test_canonical.py:
```python
@pytest.mark.asyncio
async def test_judge_with_ml_emits_valid_verdict():
    r = await arif_judge_deliberate(mode="judge", candidate="safe action", actor_id="arif")
    assert r.verdict.value in ("SEAL", "SABAR", "HOLD", "VOID")
    assert hasattr(r, "meta")
```

## 4. Known integration patterns (reference files)

| Integration | Reference file |
|---|---|
| Judge pipeline + ML wiring (arif_judge → qwen2.5:3b) | `references/judge-pipeline-ml-wiring.md` |
| Dual contract system (PURPOSE/AFFORDANCE/MODE_OVERRIDES) with known cross-callsite gaps | `references/dual-contract-system.md` |
| Verdict path divergence (wrapper vs judge composer) | `references/dual-verdict-paths.md` |
| **Payload text consistency** — `constitutional_check` vs `failed_floors`, actor identity mutation, weight-table token rent (Opus 5 audit, 2026-08-07) | `references/payload-text-consistency-2026-08-07.md` |
| D0–D5 audit series (2026-08-06) — defect catalog + revert cycles | `references/d-series-defects-20260806.md` |
| Deployment drift markers — what lies about alignment | `references/deployment-drift-markers.md` |
| Kernel vault & floor encoding bugs (`ts` vs `timestamp`; unmeasured-as-PASS) | `references/kernel-vault-and-floor-encoding-2026-08-07.md` |
| SC4 floor-defaulting trap (silent `_FLOOR_DEFAULTS` substitution hides unmeasured floors) | `references/sc4-floor-defaulting-trap-2026-08-07.md` |
| 2026-08-06 contradiction map (CRITICAL/HIGH/MEDIUM/federated, post-D6) | `references/contradiction-map-20260806.md` |
| Vault dual-file precedence bug (seal_chain.jsonl stale masking outcomes.jsonl — read both, sort by ts, pick newest) | `references/vault-reader-dual-file-precedence-2026-08-07.md` |
| **Two-path G scoring** — `compute_apex.py` (judgment) vs `apex_primitives.py` (health endpoint) use completely different formulas; inverse metrics F7/F9 bug; compliance inversion fix | `references/two-path-g-scoring-architecture-2026-08-10.md` |
| **Double-helix memory wiring state** (forged-but-not-wired baseline + wiring recipe for scar_read/scar_index/meaning_anchor; verified evidence: kernel zero refs, 43,886 VAULT999 receipts with 0 meaning_anchor) | `references/double-helix-memory-wiring-2026-08-09.md` |
| **Sovereign chain-probe audit pattern** (cumulative multi-turn investigation; i-ARIF model identity via litellm, memory embedding = prompt-layer only, ATLAS333 wiring status, drift/divergence/convergence/eureka/memory/dream taxonomy — 2026-08-12) | `references/sovereign-chain-probe-audit-pattern.md` |
| **/health handler two-route split** — `horizon_health()` in server.py is NOT the serving handler; `health()` in rest_routes.py:3114 is. 80+ key enriched response. Umbrella `degraded` problem (no `degraded_reasons[]`). 62/48/8 tool counts BY DESIGN. 5-min cache TTL. Init token staleness — 2026-08-14 | `references/health-handler-architecture-2026-08-14.md` |

Add new reference files as more investigations complete.

## Pitfalls

- **`arif_judge` is fully deterministic** — do NOT expect an LLM call in the verdict path. If you need ML reasoning, you must INSERT it (after hard gates, before final emit).
- **`OLLAMA_TEXT_ENABLED=false` by default** — Ollama is embedding-only until explicitly opted in. Set to `true` for text-gen.
- **`_call_ollama` has a 4s timeout** (`PROVIDER_TIMEOUT`) — too short for large prompts. qwen2.5:3b at ~30 tok/s can only produce ~120 tokens in 4s. For longer outputs, bypass the timeout or increase `PROVIDER_TIMEOUT`.
- **The cascade vs direct distinction**: `call_llm()` enters TokenRouter first (adds latency + model routing). For local-only PoC, use `_call_ollama` directly.
- **`VerdictOutput` is 20+ Pydantic fields** — for Qwen, output only the minimal subset (`verdict`, `reasons`, `next_safe_action`, `truth_band`, `confidence`) and let the kernel fill the rest.
- **Existing test assertions check `r.result["verdict"]` (dict path) AND `r.verdict.value` (Pydantic path)** — use whichever matches the return type (dict from `_arif_judge_deliberate`, Pydantic from `arif_judge_deliberate`).
- **`_compute_canonical_verdict` now threads `mode`** (D6, `ef5ee9bba`, 2026-08-06): the signature gained `mode: str | None = None` and Step 6's `_get_affordance_contract(tool_name, mode=mode)` call wires it. The single caller at `_enforce_nine_signal` (~line 4463) passes `out.get("mode")`. If you add a new call site for `_compute_canonical_verdict`, thread `mode` explicitly — silently dropping it re-creates the original over/under-gating bug class.
- **D4 series had a revert+reapply cycle** — v1 (`63d8d78e3`) placed `MODE_AFFORDANCE_OVERRIDES` dict with wrong indentation causing IndentationError, was reverted (`7752f441f`), then v2 (`bc6973802`) placed it correctly after the real closing brace. When investigating "why is my D-series fix gone?", check for revert commits. D6 (`ef5ee9bba`) closed the v2 follow-up — mode was wired in envelope but not in verdict path.
- **Three parallel APEX G formulations existed before E7**: `runtime/apex_canonical.py` (canonical F8), `runtime/apex_c_dark.py` (deprecated), `kernel/apex_decision_field.py` (governance fitness, NOT F8). E7 (`5d5fc2b0`) added a banner to the third one. If you see G computation in non-arif_judge code, verify which module it imports from.
- **Two completely independent G computations** (verified 2026-08-10): `compute_apex.py` (judgment path, uses 13 floor scores) and `apex_primitives.py` (health endpoint, uses SQLite tool call metrics). They produce DIFFERENT G values for the same system. Never compare `apex_scalars.G` with `runtime_floors.F8` — they measure different things. Full detail: `references/two-path-g-scoring-architecture-2026-08-10.md`.
- **Inverse metrics in geometric means** (verified 2026-08-10): F7 (Ω₀ humility) and F9 (C_dark shadow) are INVERSE metrics — low value = GOOD. But `compute_apex.py` uses them RAW in `geometric_mean()`, which interprets low as bad. F7=0.04 (perfect humility) drags A down to 0.34. F9=0.00 (zero deception) causes geometric_mean to return 0 (any factor ≤ 0 → 0) AND triggers hard floor VOID. Fix: compliance inversion `1 - raw_value` before geometric mean. Full detail: `references/two-path-g-scoring-architecture-2026-08-10.md`.
- **Floor IDs have TWO live encodings (F1–F13 and L01–L13).** `/health` `runtime_floors` mixes them in one dict (`F1..F9, L10..L13`). Grep BOTH (`"F1"` and `"L01"`) or you'll miss half the gate paths. `judge.py` has `_identity_floors = {"L11", "F11", "L13", "F13"}` — an explicit dual-encoding accommodation, not a normalization. Full detail: `references/kernel-floor-id-duality-and-judge-paths.md`.
- **`arif_judge` has multiple implementations.** Runtime facade `runtime/tools.py:23696` forwards to `tools/judge.py`, but `_arif_judge_deliberate` (tools.py:17255) and `_arif_judge_deliberate_tool` (tools.py:18393) are separate paths. Identify which the MCP surface actually registers before describing "the judge".
- **`.bak` files live in the production tree** (`tools/judge.py.bak-*`, `tools/session.py.bak.*`). Treat them as second interpretations of the live file; never `cp *.bak *.py` to roll back — that bypasses git history. Found in production: 9 .bak files in `/opt/arifos/app/{arifosmcp/data,arifosmcp/prompts,arifosmcp/runtime,arifosmcp/tools,contracts}/`. Module-shadow hazard on case-insensitive FS. F1 action: `mv` (not `rm`) to archive dir.
- **Python module-vs-subpackage shadowing** (verified 2026-08-08): when a `.py` file and a same-name `/` package coexist at the same import path (e.g. `arifosmcp/prompts.py` + `arifosmcp/prompts/__init__.py`), Python **always** picks the package — the `.py` file is invisible to `import`. Confirmed empirically: `python -c "from arifosmcp.prompts import CANONICAL_PROMPTS"` hit `__init__.py`, not the sibling module. Before deleting or gutting a `__init__.py`, grep for a sibling `.py` that may depend on being shadowed (e.g. a thin re-export wrapper). Conversely, if a `.py` file "works in isolation" but its exports don't appear on `import`, a silent sibling package is the cause — `from arifosmcp.prompts import X` resolves against the package, not the file.
- **Verify by executing, not reading source** (verified 2026-08-08): when a dependency file is being concurrently rewritten, reading its source gives stale names and signatures. Only the runtime return value is ground truth. For prompt registration: `register_arifos_prompts(mcp)` returned 13 hooks; the stale `grep name= prompts.py` showed old 10-hook names that were already overwritten on disk. Always run the function to get the live surface, never assume source-on-disk equals live behavior.
- **Three health endpoints disagree** (`/health`, `/api/governance-status`, `/metrics/json`) — they use DIFFERENT code paths, caches, and read from different aggregates. `/health` has a 5-minute `_health_cache` TTL plus reads `thermo.get("floors")` directly from the governance pipeline. `/api/governance-status` reads `_build_governance_status_payload()` which IS where SC4 fixes land. `/metrics/json` reads `get_live_metrics()` from `webmcp/live_metrics.py` (separate in-process 5s cache). If you patch `rest_routes.py:_build_governance_status_payload()` the fix IS live but you won't see it in `/health.runtime_floors` — query `/api/governance-status` first, then verify `/health` separately. Full detail: `references/vault-reader-dual-file-precedence-2026-08-07.md`.
- **TWO `/health` handler implementations exist, but only one serves** (verified 2026-08-14). `horizon_health()` at `server.py:2465` is a clean 3-signal design (~7 fields) — it is NOT registered as the route handler. The actual serving handler is `health()` at `rest_routes.py:3114`, registered inside `register_rest_routes()`, which produces the 80+ key enriched response. When reading source to diagnose /health behavior, always read `rest_routes.py:3114`, never `server.py:2465`. Full detail: `references/health-handler-architecture-2026-08-14.md`.
- **`status: degraded` is an opaque umbrella** (verified 2026-08-14). The actual handler at `rest_routes.py:~3247` computes `_degraded = runtime_drift_val or contract_drift_val` — a single boolean. No `degraded_reasons[]` array tells agents WHICH field caused degraded. Multiple independent issues (init token staleness, registry config mismatch, software_release wheel drift) collapse into one status. Agents that read different fields reach different conclusions about the same "degraded" label. The fix is additive: add `degraded_reasons[]` + `layer_health{}` to the payload.
- **62/48/8 tool counts are BY DESIGN, not drift** (verified 2026-08-14). `tools_registry_size=62` (includes aliases), `total_declared_tools=48` (public 8 + diagnostic 40), `tools_exposed_via_mcp=8` (public wire). The `registry_truth: DRIFT_DETECTED` field is derived from drift flags (`contract_drift_val or runtime_drift_val`), NOT from comparing these numbers. Do not report tool count differences as registry drift.
- **Init token caches stale `built_commit`** (verified 2026-08-14). The `arif_init` response carries `software_release.built_commit` from install-time wheel metadata. After a `git pull` without `pip install -e .`, the init token shows the old commit while `/health` shows the new `source_commit`. Agents reading init see drift; agents reading /health see match. Fix: rebuild wheel (`pip install -e .`) after every source change.
- **`_floor_status_strict` exists but never triggers "unmeasured"** (SC4 half-fix, verified 2026-08-07). The helper at `runtime/rest_routes/rest_routes.py:761` correctly returns "unmeasured" for `None`/NaN scores. BUT the upstream `resolved_floors` dict at `runtime/rest_routes/rest_routes.py:907` does `{k: floors.get(k, v) for k, v in _FLOOR_DEFAULTS.items()}` — silently substituting `_FLOOR_DEFAULTS[fid]` for missing floors BEFORE `_floor_status_strict` runs. So a floor with no real measurement shows up as `_FLOOR_DEFAULTS` (e.g. `F9: 0.04`), passes through to `_floor_status_strict` as a real number, and gets labeled "pass". The result: F9 in `/health` reads `0.04` even when `shadow` telemetry was never measured. To fix: replace `floors.get(k, v)` with explicit `None` substitution; emit `score: null, reason: "no_measurement"` for unmeasured. The helper is correct; the silent default is wrong. Full detail: `references/sc4-floor-defaulting-trap-2026-08-07.md`.
- **`last_seal_timestamp` reads indirectly with silent failure** (verified 2026-08-07). `runtime/rest_routes/rest_routes.py:2979-2991` reads `live_metrics.governance.vault_last_seal` (a cached aggregation) with `except Exception: pass`. Three problems: (1) silent failure swallows every error; (2) indirect/stale source; (3) no distinction between "empty chain" and "no seal ever". The canonical vault reader `apps/command_center/vault_chain.py:_read_last_entry()` exists and should be used directly. Same hazard class as `runtime_floors` — the right helper exists, the wiring uses an indirect path that loses information.
- **`last_seal_timestamp` reads indirectly with silent failure** (verified 2026-08-07). `runtime/rest_routes/rest_routes.py:2979-2991` reads `live_metrics.governance.vault_last_seal` (a cached aggregation) with `except Exception: pass`. Three problems: (1) silent failure swallows every error; (2) indirect/stale source; (3) no distinction between "empty chain" and "no seal ever". The canonical vault reader `apps/command_center/vault_chain.py:_read_last_entry()` exists and should be used directly. Same hazard class as `runtime_floors` — the right helper exists, the wiring uses an indirect path that loses information.
- **Doctrine-change guard:** when Arif surfaces doctrine/invariants in dialogue, do NOT auto-codify (no new GENESIS files, no spawned coding agents to land new law). First map whether the invariant already exists in canon (`052_INVARIANTS_OF_AI_AUTHORITY.md`, `018_REALITY_ENGINEERING_DOCTRINE.md`, `021_HUMANENTROPY_LAW.md`, `INVARIANTS.md`, `FLOOR_TABLE.json`), then stabilize live state. New law lands only on explicit sovereign direction — Arif 2026-08-06: "No new laws allowed. No new files. Just stabilize it."

## 5a. Doctrine: stabilize, don't add

User doctrine (2026-08-06, ratified when K-14..K-19 GENESIS additions were rejected mid-flight): **"No new laws allowed. No new files. Just stabilize it."**

When the kernel has open contradictions:

1. **Map contradictions first** (see §5). Don't start patching blind.
2. **Patch the existing code**, not new files. New GENESIS canon (`000_K_KERNEL_CANON.md` additions) and new constitutions are forbidden until the existing architecture is consistent. Half-wiring is preferable to spec-drafting.
3. **Same-file surgical edits** beat cross-file refactors. All D-series fixes (D0–D6) live in `runtime/tools.py` and `runtime/verdict.py` — the hot files. New modules require user opt-in.
4. **One patch, one day.** After landing the highest-severity contradiction, stop and report. Defer the rest to the next session.
5. **The paradox of "adding laws to fix inconsistency"** is itself the failure mode — a constitution that keeps growing while the existing implementation is half-wired is exactly the Goodhart drift the doctrine warns against.

If the user's request opens with "add [number] new floors/laws/canons" while the kernel has live contradictions, push back: "stabilize first, add second."

## 5b. Geometry-brief protocol — when to write before patching (2026-08-07)

When Arif asks for kernel changes that touch multiple files / phases / services, he often requires a **geometry brief first** — exact diff targets, file paths, and risk assessment — BEFORE any code is touched. Pattern quote:

> "Do not execute the write or restart the kernel immediately. Output the exact diff and file targets for all three phases first. I will review the geometry. If it aligns, I will authorize the commit. ΔS < 0. Jalan."

**The protocol:**

1. **STOP before any kernel write.** Even if the analysis is "obvious" — produce a written brief.
2. **Structure**: numbered phases, each with (a) inventory/state (b) proposed action (c) precise diff targets (file path + line range) (d) blast radius (e) reversibility (F1 check).
3. **End with explicit decision points** — "Choose A or B" / "Approve all N phases as one bundle?" — never assume.
4. **Do NOT execute** even trivial-looking steps (`mv .bak files`, `cp source runtime`, `systemctl restart`) until the brief is approved.
5. **Awkward hybrid case**: when some phases are pure investigation (no write) and others mutate state, group them anyway and ask for the whole package. Mixing "safe to read" with "requires write" silently bypasses review.

**Heuristic for triggering a brief**:
- Request names more than 2 phases → brief
- Touches hot files (`runtime/tools.py`, `runtime/verdict.py`, `runtime/rest_routes/rest_routes.py`) → brief
- Touches `.bak` files (module shadow hazard) → brief
- Touches federation-wide SOTs (organs.yaml, mcp_surface.yaml, contracts/) → brief
- Single trivial patch (one file, one line, well-understood) → just do it, but report what you did

**Output location**: `/tmp/<topic>_GEOMETRY.md` so it doesn't pollute the federation tree. Reference the path in the chat reply.

**The 3-phase template proven 2026-08-07**:
1. PHASE 1 — Substrate cleanup (file inventory + F1 reversible `mv` plan)
2. PHASE 2 — Kernel function surgery (current code + defect + diff target + risk)
3. PHASE 3 — Empirical state refactor (silent-default → explicit-null pattern)

After brief, **await ratification before any execution**.

## 5. Contradiction mapping methodology

When asked to "map contradictions" or "find contradictions in the kernel," follow this systematic pattern:

### Phase 1: Source-vs-deployed drift check
```bash
# Compare source and deployed file content (byte-identical?)
diff -q /opt/arifos/app/arifosmcp/runtime/tools.py /root/arifOS/arifosmcp/runtime/tools.py
# Check git markers
cat /opt/arifos/app/.git_commit /root/arifOS/.git_commit
# Check actual git history
cd /root/arifOS && git log --oneline origin/main..HEAD | wc -l
cd /opt/arifos/app && git log --oneline -1
```
Files can be byte-identical while git markers diverge (manual file copy). Check `.git_commit` markers against actual code state — `_compute_runtime_drift()` reads these but can be stale.

### Phase 2: Contract system trace
The kernel has a THREE-LAYER contract system:
1. **`TOOL_PURPOSE_CONTRACTS`** (~line 617): Human-readable purpose, `use_when`, `do_not_use_when`, `agency_level`
2. **`TOOL_AFFORDANCE_CONTRACTS`** (~line 1254): Machine-gated `action_class`, `irreversible`, `requires_human_ack`, `safe_autonomous_use`
3. **`MODE_AFFORDANCE_OVERRIDES`** (~line 2085): Per-mode overrides that apply AFTER base contract lookup

Check whether all three layers agree for each tool+mode combination. Mismatches between layers are contradictions.

### Phase 3: Dual verdict path check
Two independent verdict derivation paths exist:
- **Wrapper path**: `_compute_canonical_verdict` (tools.py:2472) — 8-step pipeline, NO G gate
- **Judge path**: `compose_effective_verdict` (verdict.py:153) — accepts `g_score`, HAS G gate

Compare what gates each path enforces. Any gate present in one but not the other is a potential contradiction.

### Phase 4: Producer-consumer consistency
For each schema defined in `schemas/` (Pydantic model), verify:
- The producer (tool function) populates all non-optional fields
- The consumer (downstream function or health endpoint) reads fields that actually exist
- No field is declared but never populated, or populated but never read

### Phase 5: Revert/fix cycle analysis
```bash
# Find revert commits
git log --oneline --all | grep -i revert
# Find fix-then-revert-then-fix-again patterns (same defect ID)
git log --oneline | grep "D4\|D3\|D2\|D1\|D0" | head -20
```
A revert+reapply cycle (like D4 in 2026-08-06) indicates the fix was initially broken (e.g. IndentationError from misplaced dict close). Check that the final version is correctly placed.

## 6. Parallel skill notes

- `kernel-security-claim-audit` — for verifying security claims via code path reads (different purpose: security audit vs integration design)
- `arifos-federation-ops` — for SCT/seal/session lifecycle ops (operational, not investigatory)
- `arifos-collapse-vector-audit` — for cryptographic claim verification (specialized subset of security)
