# OpenCode Trinity Notes — Architectural Meta

> **Why this file exists:** Prior versions of `opencode.json` carried an `_meta`
> block at the top level plus a `max_task_depth` key. Both are **not valid
> opencode schema keys** (validated by opencode 1.18.9 against the JSON Schema
> at `https://opencode.ai/config.json`). The CLI refuses to start when
> unrecognized top-level keys are present:
>
> ```
> Configuration is invalid at /root/.config/opencode/opencode.json
> ↳ Unrecognized keys: _meta, max_task_depth
> ```
>
> To preserve the architectural intent, the full content of the old `_meta`
> block was moved here on 2026-07-29. This file is **documentation only** — it
> does not influence opencode behavior. The single source of truth for runtime
> behavior remains `opencode.json` + the agent prompts in `./agents/*.md`.

---

## Trinity Architecture

- **zen_aligned:** 2026-07-29
- **trinity_collapse:** true
- **architecture:** Δ Mind (agi) → Ω Core (asi) → Ψ Soul (apex)
- **agentic_flow:** agi orchestrates, invokes asi for memory/research, invokes apex for governance gates. No human tab-switch needed.

## Separation of Powers

| Role | Agent | Mandate |
|---|---|---|
| Δ Mind | **agi** (333-AGI) | Acts, builds, forges — full tools. DS V4 Pro @ direct. Cannot seal its own work without apex. |
| Ω Core | **asi** (555-ASI) | Remembers, watches, researches — read-heavy. GLM 5.2 @ tokenrouter. 6/6 MY clean. |
| Ψ Soul | **apex** (888-APEX) | Judges, seals, voids — read-only, write-frozen. Claude Sonnet 5 @ zen. F11: authority must be expensive. |

## Handoff Protocol

| Edge | Mechanism |
|---|---|
| agi → asi | agi invokes asi via Task tool for memory recall, drift scan, telemetry, research |
| agi → apex | agi invokes apex via Task tool for constitutional verdict before irreversible mutation |
| asi → agi | asi returns structured findings to agi's context |
| apex → agi | apex returns RECOMMEND_SEAL \| HOLD \| VOID to agi; agi routes to arif_judge for binding verdict |

## Collapse Provenance

- **collapsed_from_10_agents:** build, plan, forge → agi | explore, scout, ops, general → asi | apex unchanged
- **shadow_tr_001_aware:** true — never route DeepSeek through TokenRouter (DS lives on the direct API only).

## Trinity Flow Depth

- **max_task_depth: 3** *(operational, NOT a config key)*
  - **reason:** Trinity requires agi→asi/apex but also agi→general→apex for delegated evaluations. Default depth=1 breaks the flow.
  - **tested:** T3 revealed depth=1 prevents subagent-from-subagent apex invocation.
- OpenCode exposes no `max_task_depth` setting. The depth is enforced at the
  prompt layer (subagent prompts must declare their own Task-tool calls). To
  keep the value discoverable, the agi prompt at `./agents/agi.md` should be
  considered the operational source of this number.

## Soft-Spot Mitigations

### Soft-Spot 1 — Prompt-deep apex gate
- **issue:** Gate is prompt-deep — agi chooses when to invoke apex.
- **mitigation:** `max_task_depth=3` (prompt-side) ensures apex IS reachable. agi prompt includes mandatory apex invocation before any edit / write / bash outside `forge_work/`.
- **remaining_risk:** Still prompt-enforced, not mechanical. OpenCode has no `require_subagent_before_tool` config.
- **monitoring:** Audit agi sessions for edits without preceding apex invocation.

### Soft-Spot 4 — asi routes through TokenRouter
- **issue:** asi routes through TokenRouter — memory steward on a truncating gateway.
- **mitigation:** GLM has no direct API path. Until direct GLM or DS Flash swap: asi must checksum all memory writes (SHA-256), verify on read, VOID on mismatch.
- **test_needed:** T4 — ledger integrity through TR.

---

*DITEMPA BUKAN DIBERI — Forged, Not Given. Schema-compliant, doctrine-preserving.*
