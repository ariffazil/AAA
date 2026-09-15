# FEDERATION_TOPOLOGY.md + ORGAN_CONTRACTS.md — FI-003 Second-Witness Review

> Reviewer: FI-003 (qwen) · 2026-09-15 ~15:25 UTC · Scope: verify Hermes's two DRAFT_AWAITING_F13 artifacts against process-level and kernel-level ground truth. No edits to the drafts — corrections below are for the author / next generator run.

## Verdict

Both artifacts **endorsed as drafts** — the OBSERVED/DOCTRINE/INFERRED discipline and declared blind spots are the right shape. Corrections below before canon.

## Corrections (all machine-verified this session)

1. **`:4000` ≠ Langfuse.** :4000 is the **FED front door** (KVM8 HAProxy → KVM4 litellm; `/health/liveliness` = 200 live). Langfuse has **no port — it is not deployed, by sovereign decision** (`arifos.service.d/99-kabarkan-sovereign.conf`, `OBSERVABILITY_BACKEND=arifos`, Kabarkan cutover; NATS stream `kabarkan-ingest` 198K msgs live). The `:4000=Langfuse` label inherited the original gap-table mislabel. Kernel's `langfuse_traces: NOT_WIRED` is a config fact, unrelated to :4000.

2. **FRAME MCP is `:18086`**, not :18085 — `frame-mcp.service` (systemd) listens 127.0.0.1:18086. This explains the generator's handshake failure at :18085 (organ HTTP health port ≠ MCP transport port).

3. **AAA MCP is `:3002`** — `aaa-mcp.service` (systemd) listens 127.0.0.1:3002. :3001 is the A2A Gateway API only.

4. **Orphan list: 0/3 at process level.** Process-parent forensics: `mcp-server-github` is a child of **1mcp aggregator** (`1mcp serve :3050`, live streamable sessions in `/root/.config/1mcp/sessions/`); `duckdb_enclave` is owned by **agy (FI-009, PID 226236, alive 3+ days)**; `aaa_mcp_fastmcp` **is** `aaa-mcp.service`. Lesson: "wired" must state **which bus** — Hermes-config / 1mcp-config / systemd / stdio-parent are four different wiring vocabularies. Process parent is the arbiter.

5. **Generator candidate-list additions for next run:** :7071 A-FORGE-sense, :7073 arifFlow (loopback-only), :3002 aaa-mcp, :18086 frame-mcp, :4222 NATS (kabarkan), :18095 i-ARIF, :18092 gemini bridge.

## Hermes's "real issues" — verification results (all OBSERVED live :8088/health)

| Claim | Verdict | Precise location / value |
|---|---|---|
| FED unreachable from kernel | **CONFIRMED → FIXED 15:27Z** | Root cause (3 layers): `vault.flat.env:149` pinned `FED_FEDERATION_BASE_URL=http://127.0.0.1:4013/v1` (stale topology port; a *different* local litellm, pid 1189140, which 401-rejects the kernel key) — and EnvironmentFile **overrides** systemd `Environment=` drop-ins, so drop-ins cannot fix it. Fix: corrected env line to `:4000` (canonical front door), backup at `vault.flat.env.bak-fedlane-20260915`. Verified: `fed_federation_healthy=true`, `last_fallback_reason=null`, drift=false, degraded=[], 8 tools. NOTE: the `:4013` litellm is the **kvm4-fed GLM relay shadow** (zai IP-entitlement), UFW-restricted to `100.64.0.5` only — deliberate tailnet infra, not an exposure. The stale kernel env line pointing at it was the sole defect. |
| runtime_floors not green | **CONFIRMED** | F9=0.0, F7=0.04, L12=0.425, F1=0.6 (F2/F5/F6/L10/L11/L13=1.0) |
| federation_epistemology empty | **CONFIRMED** | enabled, subjects=0, ledger_events=0, bootstrap_events=0 — engine wired, starving |
| se_stage 000 / execution held | **CONFIRMED** | law=advance_only_on_proof_bundle, never advanced; execution_readiness=held |
| graphiti degraded / semantic floor | **RESOLVED EARLIER** | Graphiti retired by 888 (2026-09-04); semantic_floor = ARIFOS_ML_FLOORS=0 choice. Prose alignment pending, not a wiring task. |

## CI status at review time (origin/main `dcc434e+`)

Floor Gate **GREEN** (v1 frozen-historical semantics correct — CI-simulation worktree reproduced exit 0; the char-183 malformed line lives in the frozen v1 `SEALED_EVENTS.jsonl` and is now reported-not-gated, which is the right call — you don't edit frozen history). Remaining red: Unified CI (2 grep-gate false positives: FEDERATION.md root-vs-docs path; F9 anti-hantu matching the F6 coercion corpus string `"i feel pain"` in judge.py) + `_shared-secrets-gate` phantom entries (reusable-workflow artifact, zero jobs). Patches: `/root/forge_work/2026-09-15-FI-003-gap-closure-deep-research.md` §4 Q1.

## Agreed diagnosis (Hermes + FI-003 converge)

The real gaps are **epistemic/provenance, not surface count**: kernel→FED lane, epistemology starvation, F9/F7 floor scores, se_stage frozen at 000. Tool-count "problems" (8/62 kernel, A-FORGE 126, ghost MCPs) were all falsified or by-design.
