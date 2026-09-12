# OpenClaw Orchestrator — Threat Model & Contract Review

> **Version:** v0.1.0 | **Date:** 2026-09-12 | **Status:** PENDING F13 SEAL
> **Author:** 333-AGI | **Reviewer:** Arif (F13 Sovereign)

## Contract Summary

| Aspect | Value |
|--------|-------|
| **Capability** | `openclaw.orchestrator.*` (7 IDs) |
| **Transport** | Subprocess: `python3 orchestrator_cli.py` |
| **Wire format** | JSON stdin → JSON stdout |
| **Authority** | OBSERVE_ONLY (classify, DAG define/dry-run, state read) |
| **Network** | FORBIDDEN (no network calls in Python CLI) |
| **Timeout** | 30s per subprocess call |
| **Output cap** | 2MB stdout, 50KB stderr |
| **No shell** | Argument arrays only, no `shell: true` |

## Allowlisted Capabilities

| ID | What it does | Authority |
|----|-------------|-----------|
| `openclaw.orchestrator.classify` | Single-intent classification via FED flash lane | OBSERVE |
| `openclaw.orchestrator.classify_multi` | Multi-intent detection + decomposition | OBSERVE |
| `openclaw.orchestrator.dag_define` | Define a DAG workflow (persisted to disk) | OBSERVE |
| `openclaw.orchestrator.dag_execute` | Execute a DAG workflow (dry-run or live) | OBSERVE (dry) / MUTATE (live) |
| `openclaw.orchestrator.dag_template` | Create workflow from pre-built template | OBSERVE |
| `openclaw.orchestrator.state_get` | Read person state (conversation history) | OBSERVE |
| `openclaw.orchestrator.health` | Health check | OBSERVE |

## Input Guards

| Guard | What it blocks |
|-------|---------------|
| **Capability allowlist** | Any capability ID not in the 7 above |
| **URL rejection** | `http://` or `https://` anywhere in query |
| **Shell char rejection** | `;`, `|`, `&`, `$`, backtick, newline, carriage return |
| **Path traversal rejection** | `..` or `/` in flow_id |
| **Query length cap** | >10,000 characters |
| **Task count cap** | >20 tasks in a DAG |
| **Required fields** | Missing query/flow/flow_id/template |

## Threat Analysis

### T1: Arbitrary Command Execution
**Risk:** Node spawns arbitrary Python with user input.
**Mitigation:** Fixed command path (`python3 orchestrator_cli.py`), argument arrays, no `shell: true`, capability allowlist in Python CLI rejects unknown IDs.
**Residual:** Low. Python CLI is the trust boundary.

### T2: Network Exfiltration
**Risk:** Python CLI makes network calls.
**Mitigation:** Python CLI has zero `urllib`/`requests`/`httpx` imports for outbound calls. FED flash lane call is done by the semantic router (localhost only). No external URLs accepted.
**Residual:** Low. Semantic router calls FED :4000 (localhost) — this is the only network call, and it's to the federation's own free inference lane.

### T3: Path Traversal
**Risk:** Attacker reads/writes files outside approved paths.
**Mitigation:** Flow IDs reject `..` and `/`. State files use SHA256-hashed filenames under `/tmp/openclaw-runtime/state/`. DAG checkpoints under `/tmp/openclaw-dag-checkpoints/`.
**Residual:** Low. No file paths accepted from user input.

### T4: Denial of Service
**Risk:** Large query or infinite DAG loop.
**Mitigation:** Query cap (10K chars), task cap (20), subprocess timeout (30s), output cap (2MB).
**Residual:** Low. All bounded.

### T5: State Pollution
**Risk:** Malicious person_id overwrites state.
**Mitigation:** Person IDs are hashed (SHA256) for file paths. No cross-person state access. L1 cache has TTL + max size.
**Residual:** Low.

### T6: DAG Live Execution
**Risk:** Live DAG execution calls A2A bridge (external side effect).
**Mitigation:** Currently dry-run only in subprocess contract. Live execution requires888 confirmation. DAG nodes are OBSERVE_ONLY by default.
**Residual:** Medium. Live execution is the expansion point — requires separate F13 approval.

## Explicit Prohibitions

- No Telegram delivery
- No external network (except localhost FED :4000)
- No generic subprocess execution
- No URL acquisition (yt-dlp, cookies, etc.)
- No persistent skill creation
- No external write
- No shell interpolation
- No arbitrary file paths

## Files

| File | Purpose | Lines |
|------|---------|-------|
| `runtime/orchestrator_cli.py` | Python CLI entry (subprocess target) | 213 |
| `runtime/node_adapter.ts` | Node.js adapter (strict allowlist) | 280 |
| `runtime/semantic_router.py` | LLM intent classifier | 411 |
| `runtime/dag_engine.py` | DAG workflow engine | 816 |
| `runtime/state_manager.py` | Cross-session state | 363 |
| `runtime/observability.py` | Traces + token budget | 426 |
| `runtime/channel_manager.py` | Channel abstraction | 354 |
| `runtime/orchestrator.py` | The brain | 556 |
| `runtime/test_orchestrator.py` | Integration tests | 274 |

## Test Results

| Test | Result |
|------|--------|
| T1 health | ✅ 7 capabilities |
| T2 classify | ✅ rule=R10, conf=0.30 |
| T3 classify_multi | ✅ 3 intents |
| T4 dag_define | ✅ 2-task chain |
| T5 dag_execute dry | ✅ execution plan |
| T6 template | ✅ 3-task research_and_report |
| T7 reject bad cap | ✅ CAPABILITY_DENIED |
| T8 reject URL | ✅ URL_NOT_ALLOWED |
| T9 persistence | ✅ define→execute across subprocess |
| T10 integration | ✅ 6/6 component tests |

## Expansion Path (Future, Separate F13 Approval)

1. **Live DAG execution** — currently dry-run only; live requires 888
2. **Telegram delivery** — requires888 confirmation with exact target
3. **Network calls** — if FED :4000 becomes unavailable, fallback chain needed
4. **Multi-channel** — Discord/WhatsApp adapters (stubs exist)
5. **Voice pipeline** — TTS/ASR integration (not yet wired)

---

*DITEMPA BUKAN DIBERI — seal the reviewed contract, not the aspiration.*
