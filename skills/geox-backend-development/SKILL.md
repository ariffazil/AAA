---
name: geox-backend-development
description: "Develop, test, and verify GEOX backend Python code (src/geox_mcp/). Covers the venv-only test runner, session enforcement architecture, tool tier classification, rate limiting, and the pre-existing test failure catalog. Use when editing any .py under src/geox_mcp/, adding new MCP tools, or modifying session_enforcement.py."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [geox, python, backend, session-enforcement, testing, mcp, rate-limiting]
related_skills: [geox-panel-authoring, geox-temporal-intelligence, forge-mcp-testing]
---

# GEOX Backend Development

Develop and verify GEOX backend Python code under `/root/GEOX/src/geox_mcp/`.

## When to use

- Editing any `.py` file under `src/geox_mcp/`
- Adding/modifying MCP tool implementations
- Changing session enforcement, rate limiting, or tool tier classification
- Running GEOX backend tests or linter
- Editing GEOX resource files under `resources/` (basin profiles, claims, analogs, ontology YAML)

## CRITICAL: Python interpreter

GEOX dependencies (fastmcp, httpx, pydantic, etc.) live in the venv ONLY.
System python3 will fail with `ModuleNotFoundError: No module named 'fastmcp'`.

```bash
# ALWAYS use venv python for tests and verification
cd /root/GEOX && PYTHONPATH=src .venv/bin/python3 -m pytest tests/ -q --tb=short

# Ruff lives outside the venv
/root/.local/bin/ruff check src/geox_mcp/
```

**make test** handles this automatically:
```bash
cd /root/GEOX && make test   # uses venv python via Makefile PYTHON variable
cd /root/GEOX && make lint   # ruff + mypy (both tolerate errors with || true)
```

## Session enforcement architecture

`src/geox_mcp/session_enforcement.py` is the central auth gate.
Every MCP tool call flows through `validate_session()`.

### Validation paths (in order)

| Path | Trigger | Authority | Rate limit |
|------|---------|-----------|------------|
| Auto-mint | `session_id` is None/empty/whitespace | OBSERVE_ONLY | 30/min anon |
| PATH 1: SCT | `act_v1.<base64>.<hmac>` | From SCT claims | Typed check |
| PATH 2: SEAL | `SEAL-*` (≥12 chars) | From kernel verify | Typed check |
| PATH 4: ANON | `ANON-*` or `__auto_mint__` | OBSERVE_ONLY | 30/min anon |
| PATH 3: Reject | Everything else | — | — |

**Rate limiting** is wired at every successful return path.
The check only fires for sessions with `type` in `("anon", "session")`.
SCT and SEAL sessions (no `type` field) pass through as no-ops.

### Key functions

- `validate_session(session_id, actor_id, required_authority)` → `ValidationResult`
- `enforce_session_or_400(session_id, actor_id, required_authority)` → `dict | None`
- `_error_code_to_http_status(error_code)` → `int` (400/401/403/429)

### Error code → HTTP status

| Code | Status | Meaning |
|------|--------|---------|
| SESSION_MISSING | 400 | No token (client error) |
| ACTOR_MISSING | 400 | No actor (client error) |
| RATE_LIMITED | 429 | Too many calls |
| SESSION_INVALID | 401 | Invalid/forged token |
| SCT_INVALID | 401 | Bad SCT signature |
| ACTOR_MISMATCH | 401 | Actor binding failed |
| TRANSPORT_DEGRADED | 401 | arifOS unreachable |
| INSUFFICIENT_AUTHORITY | 403 | Valid token, authority too low |

## Tool tier classification

`src/geox_mcp/tool_tiers.py` classifies MCP tools by what they TOUCH:

- **anon**: Pure functions, caller-supplied inputs (geox_temporal, geox_source, geox_map, etc.)
- **session**: Server-held artifacts, workspace state (geox_workspace, geox_well, geox_petrophysics)
- **verified**: Ingest, mutations, seal, vault writes (geox_well_ingest, geox_claim, geox_seismic_ingest)

Unknown tools default to `anon`. Use `get_tool_tier(tool_name)` to query.

## Rate limiter

`src/geox_mcp/rate_limiter.py` — sliding-window per-session_id:

- Anon: 30 calls/60s
- Session: 100 calls/60s
- Verified: unlimited (999)

Import: `from geox_mcp.rate_limiter import rate_limiter`

## Test files affected by session_enforcement changes

Any change to `validate_session()` or `enforce_session_or_400()` may break:

| Test file | What it tests |
|-----------|---------------|
| `tests/test_c3_redteam_session_enforcement.py` | Fabricated sessions, SCT path, actor binding, authority, unknown format |
| `tests/test_session_error_taxonomy.py` | HTTP status code mapping (400/401/403/429) |
| `tests/test_session_id_roundtrip_invariant.py` | Session ID preserved across middleware hops |
| `tests/test_session_apex.py` | Apex authority flow |
| `tests/test_session_echo.py` | Surface status echo (requires fastmcp) |
| `tests/unit/test_session_propagation.py` | Session propagation through tool calls |

**Always run ALL session tests after modifying session_enforcement.py:**
```bash
cd /root/GEOX && PYTHONPATH=src .venv/bin/python3 -m pytest \
  tests/test_c3_redteam_session_enforcement.py \
  tests/test_session_id_roundtrip_invariant.py \
  tests/test_session_apex.py \
  tests/test_session_error_taxonomy.py \
  tests/test_session_echo.py \
  tests/unit/test_session_propagation.py \
  -q --tb=short
```

## Pre-existing test failures (known, not introduced by current work)

These tests have been failing before any session enforcement changes.
Do NOT treat them as regressions. See `references/pre-existing-test-failures.md`.

## Middleware layer ordering (FastMCP transport vs on_call_tool)

FastMCP's HTTP transport resolves the `Mcp-Session-Id` header **before**
the middleware chain runs. This has two consequences:

1. **Truly headerless `tools/call`** (no `Mcp-Session-Id` at all) → FastMCP
   returns HTTP 400 `"Missing session ID"` at the transport layer. Middleware
   `on_call_tool` **never fires**. An auto-mint inside `on_call_tool` cannot
   help. The client must always send a session header (any value).

2. **FastMCP-issued session IDs are raw hex** (e.g. `8f8a874b0cc74415...`)
   and are NOT in GEOX-recognized format (`act_v1.*`, `SEAL-*`, `ANON-*`).
   Passing them directly to `validate_session()` triggers PATH 3 →
   `SESSION_INVALID`. The middleware must detect this and mint a fresh
   `ANON-*` for GEOX validators (preserving the raw SID for FastMCP
   transport only).

See `references/fastmcp-session-id-mismatch.md` for the full analysis
and the injection pattern implemented in `geox_middleware.py`.

## Support files

- `references/pre-existing-test-failures.md` — catalog of known-failing tests (SCT prefix mismatch, session_echo kernel mock gap) with root causes and the git-stash proof technique.
- `references/fastmcp-session-id-mismatch.md` — FastMCP session ID format mismatch: why naive header passthrough fails, the middleware injection pattern, and the transport-layer ordering constraint.
- `references/coverage-propagation-doctrine.md` — full reference for hardening GEOX tools to carry coverage_score, epistemic_label, and coverage_model. Includes the 5-tier taxonomy, fail-closed rules, 3-step harden recipe, verification commands, and the remaining tools still pending hardening.
- `scripts/verify_session_enforcement.py` — runnable verification for auto-mint, tiers, rate limiter, and HTTP mapping.

## 2026-07-28 protocol contract + deploy gate (2026-10-15)

Every stateless-era reply carries `resultType:"complete"` — enforced ONCE inside
`stateless_era.py` (`augment_stateless_result` / `_augment_captured_response`) at the
era-bridge choke point: JSON bodies re-serialized, SSE `data:` frames rewritten
line-wise (split chunks safe), content-length recomputed from emitted bytes. Errors
and legacy 2025-11-25 traffic untouched. Existing discriminators (`input_required`)
never clobbered; tool errors (`isError:true`) still get `complete`.

- Contract test: `tests/test_stateless_resulttype_contract.py` (11 tests — run on any
  stateless_era.py / server.py middleware change).
- Deploy gate: `make deploy-gate` — fails a deploy unless health SHA == deployed commit,
  surface_drift ok (registry truth), and tools/list + tools/call + resources/list +
  prompts/list all reply resultType live over the wire (strict httpx, never curl).
  Inherited arifOS kernel HOLD state = WARN, not BLOCK (repo_guard Gate-3 doctrine).
- Live deployment: FHS systemd `geox-mcp.service` from `/opt/geox` (separate clone;
  same SHA as /root/GEOX). Deploy = push → `cd /opt/geox && git pull && systemctl
  restart geox-mcp` → `make deploy-gate`. `/opt/geox` legitimately carries untracked
  runtime dirs (`app/`, `data/dde_cache/`, `ingest/`) — do not "clean" them.
- `geox_surface_status` reports `deployed_git_sha` + `live_counts` — tools count is
  NAME-SET filtered to CANONICAL_PUBLIC_TOOLS (one duplicate registration exists on
  the live instance: tools_total=28 vs 27 public); `tools_public_names`/
  `tools_nonpublic_names` are the OBS instruments that settle count disputes.
- Known open defects (2026-10-15): `/health` cold-start bootstrap uses dead
  `_tool_manager` path (FastMCP 3.4.6 has async `list_tools()` on the instance —
  no `_tool_manager` attr); G0.7 missing-Mcp-Method 400 body never reaches strict
  clients (BaseHTTPMiddleware abort, documented server.py ~2847); simpeg declared
  in pyproject but never imported (retire or wire); pre-existing suite failures:
  test_mcp_apps_readiness::test_11_phase_01_truth_floor_and_csp_parity,
  test_truth_loop_hardening::test_w10_deployment_drift_invariant (both fail identically
  on clean main); transport_manifest + gateway_authority tests flake on generated-
  artifact set-ordering (tools.json app_export order is hash-randomized per process).

## Pitfalls

### 1. `make test` vs bare pytest
`make test` auto-selects venv python. Bare `python3 -m pytest` uses system python
which lacks fastmcp → collection errors. Always use `make test` or `.venv/bin/python3`.

### 2. Behavioral changes cascade to 4+ test files
session_enforcement.py is the most-tested file in GEOX. Changing validation behavior
(auto-mint, new error codes, HTTP status mapping) requires updating tests that assert
on the OLD behavior. Check: error taxonomy, C3 redteam, session echo, propagation.

### 3. Ruff location
Ruff is at `/root/.local/bin/ruff`, not in the venv. `make lint` uses `ruff check src/ || true`.
Project ruff config is in `pyproject.toml` under `[tool.ruff]` — selects rules E/F/I/UP/N/B only.
Running `--select ALL` will flag docstring/annotation rules NOT in the project config.

### 4. SCT prefix mismatch in tests
The test helper `_make_sct()` generates `sct_v1.*` tokens, but `validate_session()`
checks for `act_v1.*`. This is a pre-existing mismatch — not a regression.
Do not "fix" one side without updating the other.

### 5. FastMCP session IDs are not GEOX session IDs
FastMCP returns raw hex session IDs (`8f8a874b0cc7441584b61ef2e03a2332`)
that are NOT in any GEOX-recognized format. If you pass these directly as
`arguments.session_id` to a tool, `validate_session()` hits PATH 3 →
`SESSION_INVALID`. Fix: in the `on_call_tool` middleware injection, check
whether the header SID has a GEOX prefix (`act_v1.`, `SEAL-`, `ANON-`).
If not, mint a fresh `ANON-{uuid.uuid4().hex[:16]}` for arguments instead.
The header SID must stay untouched for FastMCP transport.

### 6. on_call_tool fires AFTER FastMCP transport validation
Auto-mint in `on_call_tool()` only helps when a `Mcp-Session-Id` header IS
present. A truly headerless request gets HTTP 400 from FastMCP's transport
before middleware runs. The standard MCP flow (initialize → get SID → use it)
is the only supported client path.

### 7. Editing resource files (basin_profile.yaml, claims.json, analogs/) — raw `yaml.safe_load` is not enough
A passing `yaml.safe_load` proves valid YAML syntax but does NOT exercise the production code path.
After any resource-file edit under `resources/`, run the integration tests:

```bash
cd /root/GEOX && PYTHONPATH=src .venv/bin/python3 -m pytest \
  tests/benchmarks/test_basin_questions.py \
  tests/test_analog_atlas.py \
  tests/test_tool_contracts.py \
  -q --tb=short
```

This catches schema drift that raw YAML parsing misses (missing required key, wrong value type
that parses as YAML but fails downstream Pydantic validation). Resource files and their loaders:
- `basin_profile.yaml` → `geox_basin_profile()` (overview/play_fairway/risk/contradiction_scan)
- `claims.json` → loaded as evidence_refs; claim count grows on edit (never delete existing)
- `analogs/seed_*.yaml` → auto-discovered by test_analog_atlas.py directory glob
- `ontology/formation_water.yaml` → no direct test loader; YAML parse + spot-check notes list

### 8. YAML list + sibling key parsing pitfall
A YAML mapping key (e.g., `source:`) at the same indentation as list items (`- "..."`) inside
a parent mapping produces: `expected <block end>, but found '?'`. Fix: nest the list under a
sub-key (e.g., `drivers:` containing the list, with `source:` as a sibling of `drivers:`),
or move `source:` to higher indentation outside the list block.

### 9. Pore pressure prediction — literature grounding is MANDATORY (Forged 2026-08-13)

**Never generate stratigraphy, formation depths, or pressure parameters from LLM priors.** All geological context for pore pressure analysis must come from published literature loaded via `basin_context_loader.py` from `resources/registry/stratigraphy/{basin}.yaml`.

**Canonical failure (2026-08-13):** Hermes fabricated "Group G" as a seal interval in Malay Basin stratigraphy during a Bekantan-1 pore pressure analysis. Arif (F13, project geologist) caught it with one sentence: *"Madon did some work here actually."* There is no Group G in the central Malay Basin. Group F is the regional overpressure seal (Madon 2006, GSM Bull 49:135-144).

**The scar:** This is not just a code bug. It's a F2 TRUTH violation. An agent that fabricates stratigraphy will fabricate pressure predictions. An agent that fabricates pressure predictions will produce artifacts that look authoritative but are built on invented geology. That is the exact pattern that Bekok Deep-1 represents at the institutional level — compressed assurance is not safety.

**Required pipeline:**
1. Load basin context from `resources/registry/stratigraphy/{basin}.yaml` via `basin_context_loader.py`
2. Check `calibration_manifest` via `@requires_calibration` decorator
3. Check `coverage_manifest` via `@requires_coverage` decorator (Component #36)
4. Only then compute. Output MUST carry `epistemic_label`, `calibration_status`, `coverage_score`.

**Iron rule:** If a geological claim cannot cite at least one published source, it is fabrication. Default-deny claims not grounded in registry. Override only at F13 explicit ratification.

### 10. Coverage gate — Component #36: UNKNOWN_SPACE_MAPPING (Forged 2026-08-13)

`coverage_gate.py` implements the 4-layer coverage check. Coverage ≠ uncertainty:
- **Coverage** = where does the map end? How much of reality have we observed?
- **Uncertainty** = how wide is the range of the value?

A model can have confidence=0.81 in an interpolation where coverage=0.12. That gap is where disasters live. The canonical example is Bekok Deep-1 (SCAR-6): sensing PASS (3D seismic, historical well, mud logging), recognition/interpretation/memory FAIL (bright spot = DHI not hazard; pressure increase = "formation"; report compressed).

**Files:**
- `/root/GEOX/src/geox_core/gates/coverage_gate.py` — 4-layer check, `@requires_coverage` decorator
- `/root/GEOX/tests/test_coverage_gate.py` — 10 tests including Bekok Deep-1 scenario
- `/root/GEOX/resources/registry/pressure_components.yaml` — 36-component SOT

**Override rules (binding):**
- `coverage < 0.30` → epistemic_label = HYPOTHESIS (regardless of confidence)
- `coverage < 0.10` → 888_HOLD (void)
- `confidence > coverage + 0.30` → downgrade (confidence outruns evidence)
- Sensing PASS + any other layer FAIL → HOLD

### 11. V4A patch indentation trap — dict/list blocks (Forged 2026-08-13)

When the `patch` tool replaces a multi-line Python dict or list block via V4A format,
the diff can silently corrupt indentation — producing 7-space or mixed-indent lines
in a 4-space file. The diff *looks* correct but the actual file has wrong indentation
on the replaced lines.

**Detection:** After every V4A patch that replaces a block of 5+ lines containing dicts
or lists, read the patched region with `read_file` and visually confirm indentation
matches surrounding context. `py_compile` catches IndentationError but only after
the patch is already written, so ALWAYS check the file post-patch.

**Pattern:**
```bash
# 1. Apply patch (may corrupt indentation silently)
# 2. ALWAYS verify:
read_file(path, offset=PATCHED_LINE_START, limit=PATCHED_LINE_COUNT)
# 3. Check indentation consistency — must match surrounding lines
# 4. THEN run py_compile as a safety net
```

**Fix if corrupted:** Use the `patch` tool (replace mode, not V4A) with `old_string`
matching the corrupted block and `new_string` with correct indentation. Do NOT rely on
a second V4A patch to fix the first — the same trap can recur.

### 12. Coverage propagation pattern for existing GEOX tools (Forged 2026-08-13)

When hardening existing GEOX tools to include `coverage_score` alongside `confidence`
(per Component #36 — UNKNOWN_SPACE_MAPPING), the fields go in **two places**:

1. **Tool return dict** — add `coverage_score` (float 0.0–1.0) and `epistemic_label`
   (str: OBS/DER/INT/HYPOTHESIS/UNKNOWN) as new top-level keys. Default for
   uncalibrated tools: `coverage_score=0.0`, `epistemic_label="HYPOTHESIS"`.
2. **`evidence_refs`** — append `"ontology/pressure_states.yaml"` so the output
   envelope cites the coverage engine ontology.

**Example (prospect_unified.py falsify mode):**
```python
coverage_score = 0.0  # default: UNKNOWN
epistemic_label = "HYPOTHESIS"
return {
    "coverage_score": coverage_score,
    "epistemic_label": epistemic_label,
    # ... existing fields unchanged ...
}
```

**Example (basin.py evidence_refs):**
```python
evidence_refs=[f"basins/{normalized}/{f}" for f in evidence_loaded] +
    ["ontology/pressure_states.yaml"],
```

**Coverage score taxonomy (from `pressure_states.yaml`):**
- 1.0 OBSERVED | 0.8 CALIBRATED | 0.4 EXTRAPOLATED | 0.25 ANALOG | 0.0 UNKNOWN

**Files to check for remaining hardening:**
`prospect_unified.py`, `basin.py` (DONE 2026-08-13), `geox_geological_cognition.py`,
`vision.py`, `collision_zone.py`, `dde_reason.py`, `geomechanics_unified.py`,
`seismic_onnx_adapter.py` — all emit `confidence` but some still lack `coverage_score`.

**Verification recipe after hardening any tool:**
```bash
cd /root/GEOX && .venv/bin/python3 -c "
import sys, asyncio; sys.path.insert(0, 'src')
from geox_mcp.tools.<tool_module> import <tool_fn>
r = asyncio.run(<tool_fn>(<test_args>))
assert 'coverage_score' in r and 'epistemic_label' in r, 'MISSING coverage fields'
print('PASS')
"
# Plus the targeted unit suite:
cd /root/GEOX && .venv/bin/python3 -m pytest \
  tests/test_prospect_falsify.py tests/test_prospect_falsify_mode.py \
  tests/test_prospect_stratum.py tests/test_tool_contracts.py \
  tests/test_basin_synthesis_pipeline.py -q --tb=short
```

### 13. PptxGenJS usage — gemini-image.py positional argument trap

When generating cover images for GEOX artifacts via `gemini-image.py`, the prompt is a **positional argument**, NOT `--prompt`. Using `--prompt` will fail silently with argparse error.

```bash
# CORRECT — positional
python3 /root/HERMES/scripts/gemini-image.py "description here" --output image.png

# WRONG — will fail
python3 /root/HERMES/scripts/gemini-image.py --prompt "description" --output image.png
```
