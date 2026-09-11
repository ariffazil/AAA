# OpenAI Agents API × arifOS Federation — Architecture Mapping & Adoption Decision

> **Author:** FI-008 Kimi (warga-aaa) · **Date:** 2026-09-12
> **Trigger:** F13 chat directive — "execute all agents api related to our system architecture"
> **Evidence class:** OBS for external (live fetch of OpenAI docs, 2026-09-12) + OBS for internal (live probes: env var names, federation-models.json, litellm config)
> **External source:** https://developers.openai.com/api/docs/guides/agents-api/overview
> **Authority:** Analysis + file + marker = within 333-AGI. Any new external binding/spend = 888_HOLD (listed §6).

---

## 1. Executive Verdict

```text
OpenAI Agents API  = rented harness (sessions, orchestration, compaction, recovery managed by OpenAI)
arifOS federation  = governance science (floors, witness, scars, authority, repair loops)

They do not compete. But they are not neutral either:
the vendor harness hosts YOUR witness layer — and the federation
sealed a law yesterday that says that is the one thing you never rent.
```

The external analysis relayed by F13 ("OpenAI supplies machinery, arifOS supplies judgment") **converges on an eureka the federation already sealed**: `HARNESS_COMMODITY_BOUNDARY` (eureka-entries.jsonl, 2026-09-11) — *"when the agent harness becomes a rentable API, execution cost collapses and governance value becomes absolute."* Independent convergence = corroboration, not novelty.

## 2. What the Agents API IS (probed, not relayed)

Four concepts: **Agent** (model+instructions+tools+MCP), **Environment** (OpenAI-hosted sandbox OR `self_hosted` with `workspace_directory` + `capability_directories`), **Session** (durable, resumable), **Events/items**. Managed Codex harness handles: command/code execution in sandbox, skills/instructions application, MCP, mid-work steering, context summarization/compaction, subtask delegation to subagents (`max_concurrent_subagents`), session resume. Billing at model API rates + container rates for hosted sandboxes.

**Critical constraint (verbatim from docs):**
> "The Agents API currently supports data residency only in the United States and does not support Zero Data Retention (ZDR). Choosing a self-hosted sandbox does not make the Agents API ZDR-eligible."

Meaning: self-hosted sandbox = your hands, their brain. Sessions, orchestration, compaction, recovery — the state layer — always runs on OpenAI US infrastructure. There is no sovereign deployment mode.

**Convergence note:** their `capability_directories` is the skills-directory pattern; their incident-response example ("investigate alerts and request approval for recovery actions") is the arifOS approval-gate pattern. The industry is re-deriving federation primitives without the governance layer.

## 3. Capability Map (probed equivalents)

| Agents API feature | arifOS equivalent | Handle | Verdict |
|---|---|---|---|
| Managed sessions | KERNEL 000 `arif_init` sessions; kernel-born IDs; `carry_forward.json` | mcp arifos; /root/AGENTS.md chain | **HAVE + constitutional** (floors bind at birth) |
| Orchestration (conductor) | `forge_compose` DAG bus; `forge_parallel` A2A; Tower missions; musyawarah-gotong | mcp aforge; AAA skills | **HAVE** (fragmented by design — separation of powers) |
| Context compaction | Native harness compaction; FORGE-context-compressor; reality-compression; strata S0–S3 | skills + instructions | **HAVE-as-doctrine** (not a managed runtime primitive — GAP) |
| Recovery | 5-R Protocol; incident-response; monotonic-recovery; flap fail-closed semantics | canon STUCK-ACTOR-RECOVERY-2026-09-10; scar c3c30ea0 | **HAVE** (ours learned from scars; theirs managed retries) |
| Subagents | af-* fleet, spawn/lifecycle contracts, snapshot-fork; swarm ≤128 | AAA FORGE-subagent-*; Agent tool | **HAVE** (theirs caps at 4 concurrent in example config) |
| Sandboxes | `forge_sandbox_run/pause/resume` (bwrap, ABSOLUTE timeout, 24h eviction); `forge_ephemeral` generate→retire | mcp aforge | **HAVE** (ours: F1 reversible + capability metabolism) |
| MCP | 13+ organ servers; FORGE-fastmcp; surface guard/audit | /root/.kimi-code/mcp.json (SOT) | **HAVE** — interop is the point, both MCP-native |
| Tool execution | `forge_execute` (cc_id-gated); `forge_shell` (ArifJudge + hash-chain ledger) | mcp aforge | **HAVE-PLUS** (floor-gated; theirs is not) |
| Long-running tasks | `forge_job` submit/status; cron registry (`forge_vps_cron`) | mcp aforge | **HAVE** |
| Local/other models | FED litellm lanes; Ollama localhost; FLAME; 202-model registry | /root/.config/federation-models.json | **HAVE** (vendor-neutral router — OpenAI is one lane of many) |
| Tracing/observability | arifFlow FlowReceipts; experience traces; FRAME drift observer; VAULT999 seal chain | mcp arifFlow/aforge | **HAVE-PLUS** (theirs: perf traces; ours: constitutional receipts) |

**Honest gaps (all cost-side, none governance-side):** (1) one unified REST surface vs our intentional organ fragmentation; (2) elastic hosted compute vs 3 KVMs; (3) compaction as managed primitive; (4) vendor-maintained harness vs our 7-harness FI mesh maintenance burden.

## 4. The New Finding: Vendor-Level Witness Channel Inversion

The federation's law (sealed 2026-09-12, marker `EXTERNAL-WITNESS-3META-F13-20260912`, chain `29cc39690dd4…`):

> A system cannot reliably certify itself — the observer must be outside the thing being observed, and the witness channel must be controlled by someone other than the witnessed.

Applied at vendor scale: **if OpenAI hosts our sessions, orchestration, compaction, and event traces, then the substrate that produces our telemetry is controlled by the party whose performance that telemetry reports.** Same failure shape as FLAME (`/health` certifying a zombie, scar_1788460914061) and FRAME (STABLE from N=0, scar_1788798276772) — one level up: the institutional witness layer would live inside the observed vendor. The no-ZDR/US-residency constraint makes this concrete, not hypothetical: the witness layer would be **non-sovereign by construction, with no export path to sovereignty**.

```text
Machinery may be rented.
Witness cannot be rented.
```

## 5. Probe Results (internal state, 2026-09-12)

- **Keys exist (names only, values never read):** `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `AZURE_OPENAI_{KEY,ENDPOINT,MODEL,EMBEDDING}`, `OPENAI_WHISPER_API_KEY`, `VOICE_TOOLS_OPENAI_KEY` — /root/.secrets/kunci-root.env
- **FED already routes openai:** `federation-models.json` (16 openai refs + OpenAI-compatible entries); `A-FORGE/litellm-config.yaml` contains openai providers
- **Conclusion:** OpenAI-as-MODEL-lane is already live. The only genuinely new question is OpenAI-as-HARNESS (Agents API sessions), which is a new product binding on the existing account.

## 6. Decision Register

| # | Option | Verdict | Authority |
|---|---|---|---|
| D1 | **ADOPT-AS-LANE** — OpenAI models behind FED (status quo), extend routes as economics warrant | **Already live — continue** | FED ops, reversible, no new binding |
| D2 | **ADOPT-AS-PATTERN** — steal primitives onto sovereign substrate: self-hosted-environment semantics, `capability_directories` (already have), webhook completion → `forge_job` ergonomic upgrade, managed-compaction primitive for harnesses lacking native compaction | **EXECUTE** — zero sovereignty cost, normal engineering backlog | 333-AGI, backlog items |
| D3 | **TRIAL-AS-SANDBOXED-LANE** — one bounded Agents API session for a non-sensitive benchmark task (public data only), behind existing key, cost-capped, zero federation state crossing the wire | **HOLD — 888** | New product binding + spend; preconditions: cost cap, public-data-only payload rule, trial duration, kill switch. If F13 says go: wire as skill, never as organ |
| D4 | **REJECT-AS-SUBSTRATE** — never move arifOS sessions, memory, ledgers, traces, orchestration, or compaction onto vendor-hosted harness | **STANDING** | Grounded in: no-ZDR/US-residency (§2) + witness-channel law (§4) + F13 sovereignty. Weakened only if OpenAI ships ZDR + exportable witness logs + sovereign residency — re-evaluation trigger |

## 7. Executed This Session

- This file: `/root/AAA/reports/openai-agents-api-arifos-mapping-2026-09-12.md`
- Ritual marker: `OPENAI-AGENTSAPI-ARCH-VERDICT-20260912` (handle in session log)
- No external binding created, no key used, no data egress. D3 parked at 888_HOLD.

## 8. Falsification

1. If OpenAI ships ZDR + data-residency choice + exportable session/witness logs → D4 weakens; re-map.
2. If a sovereign-substrate equivalent (FED + forge_compose + harness compaction) fails to deliver comparable reliability over next quarter → D3's trial value rises; re-present to 888 with evidence.
3. If D3 trial (if approved) shows cost/latency dominance with zero governance violations → expand lane scope proposal to F13.

DITEMPA BUKAN DIBERI ⚒️
