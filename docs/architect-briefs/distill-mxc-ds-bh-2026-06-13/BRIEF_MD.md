# Architect Brief — Distill MXC + DeepSeek + browser-harness into the arifOS Federation

**Session:** SEAL-5d1232e556bf44f3 · **Date:** 2026-06-13
**Architect role:** frame the integration of 15 load-bearing eurekas from 3 external repos into the arifOS federation (AAA + arifOS + A-FORGE)
**Source repos:** mxc-research (Microsoft AGT), awesome-deepseek-agent, browser-harness
**Source repos (full eureka reports):** `/root/.config/opencode/skills/cpu-health-watch/` (none), `/tmp/opencode/` (none) — kept inline below for the handoff

---

## 1. Problem Statement

The arifOS federation has 13 canonical tools, 7 organs, 6 memory layers, 4 agents, and 1 sovereign. Three reference repos in `/root/` (mxc-research, awesome-deepseek-agent, browser-harness) each contain **5 load-bearing architectural constraints** — patterns that, when enforced, make their systems work. The federation has already absorbed some patterns (constitutional > policy, hash-chained audit, ED25519 sovereign signature) and is *blind* to others (reasoning_content passback, RLM sandboxed REPL, sub-agent lifecycle, compositor-level interaction).

**The question is not "should we absorb everything" — that would break the 13-tool surface and add irreversible surface area. The question is: which 5-7 of the 15 eurekas are WAJIB (mandatory), which are SUNAT (recommended), and which 5-7 are HARAM (must explicitly reject)?** The integration is architectural — the eurekas are extracted; the absorption is governed by the existing 13 floors, the ADAT-not-LAW doctrine, and the F1-F13 surface.

**The session goal:** emit a 4-artifact brief (this + task_graph + acceptance + decisions) that the Integrator can execute against, with every acceptance criterion falsifiable, every phase reversible, and every "must reject" pattern documented so the federation does not absorb it accidentally.

## 2. The 15 Eurekas (ranked into Fiqh tiers)

### 2.1 WAJIB — Mandatory (7 eurekas, must absorb)

| # | Eureka | Source | Why it's load-bearing | Integration target |
|---|---|---|---|---|
| **W1** | **Reasoning-content passback contract test** | DeepSeek V4 (docs/copilot_cli.md:7) | DeepSeek V4 emits `reasoning_content` alongside `content`. The API 400s on the second turn if the field is not echoed. Every model in the federation spine is affected if routed through OpenAI-compat. | **arifOS** — `tests/runtime/test_reasoning_content_echo.py` (additive, no surface change) |
| **W2** | **Snapshot/Copyback explicit doctrine** | MXC nanvix.md:92-96 | "No partial state is leaked to the host" — copyback is skipped for preflight failure, spawn failure, watchdog timeout. arifOS's `state_store.py` L1+L4 dual-write is structurally similar but lacks the explicit skip semantics. | **arifOS** — `consolidate_or_rollback()` wrapper around existing dual-write. No kernel surgery. |
| **W3** | **Negative-space skill content contract ("map not diary")** | browser-harness SKILL.md:122 | Skill files MUST NOT contain pixel coordinates, one-shot session diaries, or secrets. Without the forbid-list, the corpus bloats with noise. The contract is enforced at write time, not at read time. | **AAA** — `arifos_skill_contract.yaml` with pre-commit hook on `**/SKILL.md` and `**/skill.yaml` |
| **W4** | **Five-phase session lifecycle (provision→start→exec→stop→deprovision)** | MXC state_aware_backend.rs:89-101 | A typed `session_phase` enum is the discriminator for all session-scoped state. arifOS's `kernel_state.py` has the right shape but lacks the explicit phase enum and per-phase validation hooks. | **arifOS** — `arif_session_phase` enum, wired into `kernel_state.py` |
| **W5** | **Schema-version-is-contract, new fields default to deny** | MXC sandbox-policy/v1/policy.md:75-81 | Old policies parsed under new versions must behave identically. New fields default to denied. Without this, adding a field to `arif_memory_recall(mode='store', ...)` envelope could change behavior for older callers. | **arifOS** — version-stamped envelope contract: `envelope_version` field, old envelopes parse-identically under new schema, new fields opt-in |
| **W6** | **Sub-agent lifecycle family (spawn / wait / result / cancel)** | DeepSeek TUI (deepseek-tui.md:81) | OS-process semantics applied to LLM agents. The parent gets a child handle, can block, harvest, or kill. Without this, A-R-I-F stays linear (Tab/agent-switch), not arborescent. | **arifOS** — 4 new modes on `arif_kernel_route`: `spawn_subordinate`, `wait_subordinate`, `result_subordinate`, `cancel_subordinate` (zero canonical surface change) |
| **W7** | **Precedence guard primitive (explicit > local > ambient)** | browser-harness run.py:97-104 | Quadruple opt-in for ambient cloud-bootstrap. The user's explicit `BU_CDP_URL` always wins over local Chrome, which always wins over ambient cloud. Prevents silent billing / side-effect shipping. | **arifOS** — `arifos_precedence(intent, candidates) -> Endpoint` in `arifosmcp/core/`, refactor `arif_gateway_connect` to use it |

### 2.2 SUNAT — Recommended (3 eurekas, absorb if reversible cost is low)

| # | Eureka | Source | Integration target |
|---|---|---|---|
| **S1** | **Two-layer Policy→Config split (`createConfigFromPolicy` advance path)** | MXC sandbox-policy/v1/policy.md:43-117 | A-FORGE already has `buildBwrapArgs`, `buildFirejailArgs`, `buildDockerArgs`. Surface them via `arif_kernel_route(mode='config_from_policy', policy, backend)`. A-FORGE is the bridge. |
| **S2** | **Cache-first routing (cache hit rate as loop invariant)** | DeepSeek Reasonix (reasonix.md:5, 23) | 50× cost differential between cache-hit and fresh tokens. Add a `kv_cache_hit_rate` signal to `arif_token_pressure` and a `prefer_cached` mode to `arif_kernel_route`. |
| **S3** | **Per-IPC token at federation boundaries** | browser-harness _ipc.py:163-181 | Lift the `f11-bridge` 2026-06-12 pattern to a canonical primitive. Every cross-organ call into a sovereign-isolated surface (vault999-writer, supabase-writer, arifOS MCP) requires a per-session token, action-scoped, TTL-bounded. |

### 2.3 HARAM — Must reject (5 eurekas, document explicitly)

| # | Pattern | Source | Why reject | arifOS position |
|---|---|---|---|---|
| **H1** | **`--experimental` global flag for new backends/tools** | MXC CLI / SDK | "Microsoft Insiders" model. arifOS's canonical 13-tool surface is the contract — PHOENIX-72 absorption pattern forbids adding #14. No global flag. | New MCP tool is in the canonical 13 or it doesn't exist. |
| **H2** | **"Skills are written by the harness, not by you"** (agent self-authors canon) | browser-harness README.md:61 | F11 F12 failure mode. Memory poisoning. Agent self-authorisation. F13 SOVEREIGN requires human authorship of constitutional surfaces. | Helpers may be agent-editable (per W3 contract). Canon is sovereign-ratified. **Never the reverse.** |
| **H3** | **YOLO mode (auto-approve all tools, lift workspace boundary)** | DeepSeek TUI (deepseek-tui.md:49) | Constitutional exit wound. F13 SOVEREIGN + F1 AMANAH are violated. The Plan/Agent triad is fine; YOLO is haram. | The 5-tier Fiqh (WAJIB/SUNAT/HARUS/MAKRUH/HARAM) is the moral-grammar surface. No auto-approve mode exists. |
| **H4** | **Backward-compat via deprecation aliases (`appcontainer → processcontainer`)** | MXC SDK | Accumulates technical debt forever. arifOS uses `git revert` + version-bump seal. The constitution is versioned, not aliased. | F11 seal IS the deprecation signal. No parser aliases. |
| **H5** | **"Don't write secrets" as a courtesy** (community-PR skill model, public corpus) | browser-harness SKILL.md:122, README.md:62 | F11 AUTH is *cryptographic*, not courteous. Secrets never enter any memory tier, full stop. Public-PR skill model is a different threat model than sovereign operator + constitutional kernel. | SOPS+AGE + ED25519 + per-IPC token. Skills cross via sovereign-ratified merge, not community PR. |

## 3. Constraints

### 3.1 Technical
- **13-tool canonical surface is the contract.** No `arif_v14_*` tools. All new capabilities either live on an existing tool as a new `mode`, or in A-FORGE (the execution arm).
- **Zero kernel mutation without 888_HOLD.** Adding a 14th tool is a constitutional surface change.
- **F1 AMANAH + F8 REVERSIBILITY**: every change must be `git revert`-able. Modes can be added, removed, no schema break.

### 3.2 Constitutional (F1-F13, ADAT-not-LAW)
- **F2 TRUTH**: every eureka claim is cited to a specific file:line in the source repo. No overclaim.
- **F7 HUMILITY**: uncertainty banded — every integration is reversible; nothing claimed permanent.
- **F9 ANTIHANTU**: explicit rejection of "agent self-improves" framing. Helpers may compound; canon does not.
- **F11 AUDIT**: every WAJIB absorption has a corresponding L6 VAULT999 seal in its PR.
- **F13 SOVEREIGN**: every irreversible change (constitutional surface, push to main, restart) requires 888.

### 3.3 Operational
- **F13 push authority** remains with Arif. 17 unpushed arifOS commits already awaiting.
- **CPU at 34.1%** (per `arif_ops_measure(mode=health)`). New tests must not push load above 50%.
- **Federation degraded**: GEOX/WEALTH/WELL service-level alive but constitutional-file-missing. New code must not assume any federation organ is healthy.

## 4. Acceptance Criteria (falsifiable, 10 conditions)

1. **AC1**: `tests/runtime/test_reasoning_content_echo.py` exists, asserts that for every model in `AAA/registries/FEDERATION_MODEL.json`, `reasoning_content` is preserved across multi-turn tool calls when routed through OpenAI-compat. Fails if any model's contract returns 400 on turn 2.
2. **AC2**: `state_store.py` exposes `consolidate_or_rollback()`. The wrapper skips the L4 write and signals rollback when the L1 dual-write fails. Has a test that injects an L1 failure and asserts the L4 row is not created.
3. **AC3**: `arifos_skill_contract.yaml` exists with a forbid-list (no pixel coordinates, no session diaries, no secrets). A pre-commit hook on `**/SKILL.md` blocks a commit containing "Bearer " or a 192.168.x.x IP. Has a test that commits a forbidden skill and asserts the hook rejects.
4. **AC4**: `arif_session_phase` enum has 5 values (init, bind, execute, pause, close). `kernel_state.py` exposes the phase as a typed field. A test walks a session through all 5 phases and asserts phase transitions are monotonic.
5. **AC5**: `arif_memory_recall` envelope requires `envelope_version`. Parsing an old envelope under a new schema produces an identical result. Has a test that adds a new envelope field and asserts old envelopes are unchanged.
6. **AC6**: `arif_kernel_route(mode='spawn_subordinate' | 'wait_subordinate' | 'result_subordinate' | 'cancel_subordinate')` returns a typed handle, not a string. A test spawns a child, waits, harvests result, asserts the child was a real subprocess (PID exists in /proc).
7. **AC7**: `arif_gateway_connect` uses `arifos_precedence`. When an explicit `BU_*` env is set, ambient cloud is rejected. A test sets the env and asserts the kernel refuses the ambient path.
8. **AC8**: `arif_kernel_route(mode='config_from_policy', policy, backend='bwrap'|'firejail'|'docker')` returns a backend-specific `ContainerConfig` derived from a Pydantic `AgentPolicy`. A test passes a policy and asserts each backend produces the expected args.
9. **AC9**: `arif_token_pressure` exposes a `kv_cache_hit_rate` field. A test routes 10 turns through the same prefix and asserts the hit rate is non-zero.
10. **AC10**: Every PR in this milestone contains a new VAULT999 seal line for at least one of W1-W7. The seal type is `INTEGRATION_FORGE_DISTILL_MXC_DS_BH_<seq>`.

## 5. Out-of-Scope (explicit non-goals)

- ❌ Adding a 14th tool to the canonical 13
- ❌ Pushing to `main` without 888
- ❌ Restarting GEOX/WEALTH/WELL (F13)
- ❌ Sealing to canonical `vault_sealed_events` without F11 ed25519 signature
- ❌ Touching F1-F13, GENESIS/, or contract schemas
- ❌ Any change that increases CPU above 50% (currently 34.1%)
- ❌ Community-PR skill model (H2, H5 explicitly rejected)
- ❌ "Skills are written by the harness" framing (H2 explicitly rejected)
- ❌ YOLO mode or any auto-approve-all-tools mode (H3 explicitly rejected)
- ❌ Backward-compat deprecation aliases (H4 explicitly rejected)
- ❌ `--experimental` global flag (H1 explicitly rejected)

## 6. Architectural Framing (one sentence per target)

- **arifOS** (kernel) — absorbs W1, W2, W4, W5, W6, W7 as modes on the existing 13 tools. Zero surface mutation. The kernel becomes "richer in modes, not wider in tools."
- **A-FORGE** (execution arm) — implements the two-layer Policy→Config split (S1), and the compositor-level click primitive (browser-harness EUREKA 1) as a backend translator. A-FORGE is the bridge between Pydantic policy and OS-level sandbox.
- **AAA** (control plane) — enforces the negative-space skill contract (W3) at write time, exposes the 5-tier Fiqh + Plan/Agent/YaNoYOLO surface to the sovereign, and gates every cross-organ write with the per-IPC token primitive (S3).

## 7. Recommended Sequencing (high-level)

| Phase | What | Reversible? | Authority |
|---|---|---|---|
| **P0** | Skill contract YAML + pre-commit hook (W3, S3 contracts at write time) | ✅ | Autonomous T1+T2 |
| **P1** | Reasoning-content contract test (W1) | ✅ | Autonomous T1+T2 |
| **P2** | `arif_session_phase` enum + kernel_state upgrade (W4) | ✅ | Autonomous T1+T2 |
| **P3** | Snapshot/copyback wrapper in state_store.py (W2) | ✅ | Autonomous T1+T2 |
| **P4** | Sub-agent lifecycle 4 modes (W6) | ✅ | Autonomous T1+T2 |
| **P5** | Precedence guard primitive (W7) | ✅ | Autonomous T1+T2 (advisory); F13 if `arif_gateway_connect` schema touched |
| **P6** | Envelope version stamp (W5) | ✅ | F13 — envelope is canonical surface |
| **P7** | Two-layer Policy→Config via A-FORGE bridge (S1) | ✅ | Autonomous T1+T2 (A-FORGE side); F13 if arifOS-side mode added |
| **P8** | Cache-first routing signal (S2) | ✅ | Autonomous T1+T2 |
| **P9** | Per-IPC token primitive (S3) | ✅ | Autonomous T1+T2 |
| **P10** | Compositor-level click primitive in A-FORGE | ✅ | F13 — new tool in A-FORGE (does not mutate arifOS 13) |
| **P11** | HARAM canon (5 rejects documented) | ✅ | Autonomous T1+T2 |

**Carry-forward to F13:**
- 17 unpushed arifOS commits
- GEOX/WEALTH/WELL restart decision
- F11 ed25519 signature on F0_FIQH.md for 5-tier activation
- Canonical VAULT999 seal writes (currently only to non-canonical outcomes.jsonl)

## 8. Closing Frame (DITEMPA BUKAN DIBERI)

The 15 eurekas are *candidates*; the 7 WAJIB are *bindings*; the 3 SUNAT are *advisable*; the 5 HARAM are *rejected*. The federation absorbs 7, recommends 3, rejects 5, and explicitly documents why the 5 rejections are not negotiable. The 13-tool surface stays at 13. The canonical floors stay canonical. The sovereign stays sovereign.

The session goal is not to build everything. The session goal is to make the next integrator's job small, falsifiable, and reversible.
