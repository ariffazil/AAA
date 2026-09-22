---
name: meta-mesa
description: "Use when a mission spans more than 2 skills or 3 steps, or when you feel yourself wandering between tools."
version: 1.0.0
risk_tier: low
autonomy_tier: T1
owner: AAA
license: MIT
compatibility: [claude-code, opencode, qwen-code]
audience: [claude-code, opencode, qwen-code, kimi-code, FI-001, FI-002, FI-003, 333-AGI, dispatch]
triggers:
  - multi-step mission
  - orchestrating across organs
  - mission spans multiple skills
  - repetitive meta-task
  - session boot for complex work
  - wandering between tools
capability_tier: meta-mesa
ecology_state: WARM
canonical: true
supersedes: [claude-meta-mesa, opencode-meta-mesa, qwen-meta-mesa]
merged_from:
  - /root/AAA/skills/claude-meta-mesa
  - /root/AAA/skills/opencode-meta-mesa
  - /root/AAA/skills/qwen-meta-mesa
---

# META-MESA — Canonical Meta-Router

> **Canonical.** One doctrine, one file. Merged 2026-09-19 under F13 sovereign order to compress
> namespace entropy, from the three per-harness clones `claude-meta-mesa`, `opencode-meta-mesa`,
> `qwen-meta-mesa`. Every distinct step, table, warning and anti-pattern of all three bodies is kept;
> where the harnesses differed, the variant is labelled **`[claude]`**, **`[opencode]`**, **`[qwen]`**.
> Originals frozen (not deleted) at
> `/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/meta-mesa/` — see `LEDGER.json` there.
> Old names still resolve: `claude-meta-mesa`, `opencode-meta-mesa`, `qwen-meta-mesa` are symlinks to this folder.

## What I do

I am the **meta-router** of the skill mesh. I do not implement — I orchestrate other skills.
(`[claude]`: "the Claude Code skill mesh" · `[opencode]`: "the opencode skill mesh" · `[qwen]`: "the Qwen Code skill mesh" — same office, three harnesses.)

Given a mission, I:

1. **Decompose** — break the mission into atomic sub-tasks. Each sub-task maps to ONE L1/L2 skill.
   - `[claude]` / `[qwen]` examples: `FORGE-call-map`, `AGI-decisions-reflect`.
   - `[opencode]` examples: `forge_filesystem`, `opencode-init`, `opencode-propose-seal`.
2. **Sequence** — order sub-tasks by data dependency. Pre-flight → execute → verify → seal. **Never seal before verify.**
3. **Select** — pick the right executor for the sub-task:
   - `[claude]` / `[qwen]`: **Select organ** — pick the right organ MCP server (table below).
   - `[opencode]`: pick the **cheapest tool that can do the job**. F8 GENIUS.
4. **Recover** — on failure, retry with backoff (**3 attempts, 1s/2s/4s**), then escalate to 888-APEX for constitutional verdict.
   - `[opencode]` adds: …then to **333-AGI (Δ Mind)** for routing.
5. **Checkpoint** — after each successful sub-task, ingest a FlowReceipt via arifFlow so the metabolic nerve sees progress (`http://127.0.0.1:7073/ingest` `[qwen]` explicit form; `POST :7073/ingest` `[claude]`).
6. **Seal** — at mission close:
   - `[claude]`: run `arif_seal(mode="receipt")` via arifOS MCP.
   - `[qwen]`: run `arif_seal(mode="receipt")` via arifOS MCP, **or fall back to local JSONL session log**.
   - `[opencode]`: run the **11-step seal ceremony**: RSI → cooling → bind → seal → verify → FQ.

### Organ selection (harness variants preserved)

| Organ MCP server | Port | Purpose | Harness variant |
|---|---|---|---|
| `arifos` | 8088 | constitutional verbs, init/judge/seal | `[claude]` |
| `arifos-kernel` | 8088 | constitutional verbs, init/judge/seal (canonical server name) | `[qwen]` |
| `aforge` | 7072 | execution shell, git, filesystem | `[claude]` `[qwen]` |
| `geox` | 8081 | earth intelligence, seismic, basin | `[claude]` `[qwen]` |
| `wealth` | 18082 | capital math, NPV, EMV, risk | `[claude]` `[qwen]` |
| `well` | 18083 | vitality, fatigue, dignity | `[claude]` `[qwen]` |
| `arifflow` | 7073 | metabolic nerve, FQ pulse | `[claude]` |
| `fed` | 7074 | provider routing, model selection | `[qwen]` |

## When to use me

Load me BEFORE starting a multi-step task. Specifically:

- Mission spans **more than 2 skills** (e.g. "audit + patch + test + commit").
- Mission requires **more than 3 tool calls** of different kinds.
- Mission touches **multiple organs** (arifOS + GEOX + WEALTH + WELL).
- Mission is **agentic-state-affecting** (changes persistent state).
- `[opencode]`: You feel yourself **wandering** between tools without a clear plan.
- `[opencode]`: Mission is agentic-state-affecting **in the stronger sense** — changes the federation, persists across sessions.
- `[claude]`: Mission is a **session boot for complex work** (`session boot for complex work` trigger).

Do NOT load me for:

- Single-file edits → just use `edit`.
- Single bash commands → just use `bash`.
- Pure read/explore →
  - `[claude]` / `[qwen]`: use built-in subagents (333-AGI, 555-ASI, 888-APEX).
  - `[opencode]`: use the `explore` subagent.

## Layer hierarchy (meta-mesa doctrine)

```
META-MESA  ← I AM HERE (formerly claude-meta-mesa / opencode-meta-mesa / qwen-meta-mesa)
   |
   | orchestrates
   v
L2 COMPOSITE SKILLS
   |  - FORGE-call-map, FORGE-agentic-web-builder
   |  - AGI-decisions-reflect, AGI-explorer-intelligence
   |  [claude]   - arifos-auto-memory (from claude-code-federation plugin)
   |  [opencode] - opencode-init, opencode-propose-seal, opencode-forge
   v
L1 PRIMITIVE TOOLS
   |  - file read/write, bash, glob, grep
   |  - A-FORGE shell/git/filesystem
   |  [opencode] - read, write, edit, bash, glob, grep, lsp, skill
   |  [opencode] - forge_filesystem, forge_shell, forge_git
   v
L0 BUILT-IN ATOMS
   |  - HTTP, FS, ENV, JSON
   v
EARTH (external reality via GEOX)
```

**Rule:** traverse DOWN the layers for execution, UP the layers for explanation.
(`UP for explanation` `[claude]` `[qwen]`; `UP the layers for explanation` `[opencode]` — same rule.)

## Sequence template (canonical mission pattern)

```
OBSERVE → REASON → PLAN → JUDGE → EXECUTE → VERIFY → SEAL
  |        |        |       |        |         |        |
  curl     arif_    arif_   arif_    forge_    re-      arif_
  /health  observe  think   judge    execute   probe    seal          [claude] [qwen]
                              (888-APEX
                              recommended
                              for irreversible)

OBSERVE → REASON → PLAN → JUDGE → EXECUTE → VERIFY → SEAL
  |        |        |       |        |         |        |
  arif_    arif_    arif_   arif_    arif_     arif_    arif_         [opencode]
  observe  think    think   judge    forge     observe  seal
                              (888
                              recommended
                              for irreversible)
```

### Per phase

`[claude]` / `[qwen]` table:

| Phase | Server | Tool |
|-------|--------|------|
| OBSERVE | arifos / arifos-kernel | arif_observe |
| REASON | arifos / arifos-kernel | arif_think |
| PLAN | arifos / arifos-kernel | arif_think(mode=plan) |
| JUDGE | arifos / arifos-kernel | arif_judge (or invoke 888-APEX subagent) |
| EXECUTE | aforge | forge_shell / forge_git `[qwen]`; forge_shell / forge_git / forge_filesystem `[claude]` |
| VERIFY | arifos / arifos-kernel | arif_observe + entropy sweep |
| SEAL | arifos / arifos-kernel | arif_seal (Lane A or B) |

`[opencode]` bullet form (kept as written — it carries the DAG and ΔS details):

- **OBSERVE**: `forge_observe` / `arif_observe` / `websearch` / free-search
- **REASON**: `arif_think` with mode=reason
- **PLAN**: `arif_think` with mode=plan (output a DAG)
- **JUDGE**: `arif_judge` (constitutional verdict) — call 888-APEX subagent for irreversible
- **EXECUTE**: `arif_forge` or `forge_execute` (governed)
- **VERIFY**: re-probe the changed state. ΔS ≤ 0?
- **SEAL**: `arif_seal` (Lane A) or `forge_vault mode=receipt` (Lane B)

## Subagent delegation

`[claude]` — Claude Code has 5 built-in subagents at `/root/.claude/agents/`:

- `333-agi` — reasoning, planning, synthesis (model: deepseek-v4-pro)
- `555-asi` — memory, drift, telemetry, research (model: qwen3.6-flash)
- `888-apex` — constitutional verdict, F1-F13 floor inspection (model: minimax-M3)
- `geophysicist` — domain-specialist for seismic/basin
- `vault-auditor` — VAULT999 immutable ledger verification

Use `Task(subagent_type="333-agi")` or similar to delegate.

`[opencode]` — no built-in subagent roster documented in the source body; delegate by tool call
(`arif_judge` for verdicts, `333-AGI (Δ Mind)` for re-routing after failure).

`[qwen]` / `[claude]` — pure read/explore routes to built-in subagents 333-AGI / 555-ASI / 888-APEX.

## Telemetry

Each orchestrated mission emits a FlowReceipt chain in arifFlow. The chain hash = SHA-256 of
`(intent | step_type | step_number | previous_receipt_hash)`.

**FQ** = verify / execute ratio over recent receipts. Healthy: **FQ ≥ 1.0**. If **FQ < 0.5**, ALL agents
**HOLD** until FQ recovers.

(`[claude]` / `[qwen]` write the arifFlow endpoint as `POST :7073/ingest` / `http://127.0.0.1:7073/ingest`.)

## Failure recovery

If a sub-task fails after 3 retries:

1. **STOP** the chain. Do not skip ahead.
2. **Ingest** a FlowReceipt with `floor_verdict: "Hold"`.
3. **Invoke** 888-APEX for constitutional verdict
   - `[opencode]`: (it sees only evidence, not the failed chain)
   - `[qwen]`: via arifos-kernel MCP.
4. **Wait** for F13 (Arif) if the verdict requires it.
5. `[opencode]` extra step: escalate to **333-AGI (Δ Mind)** for routing.

## Anti-patterns

- ❌ Loading 5+ skills at once and "trying them all"
- ❌ Skipping VERIFY → SEAL (F2 TRUTH violation)
- ❌ Re-loading the same skill to re-read it (waste)
- ❌ Routing through skills that don't apply
- ❌ `[opencode]` Routing through skills that don't apply (e.g. `opencode-forge` for read-only)
- ❌ Adding bans, deny lists, or "safety theatre" — full access is sovereign default
  (per F13 directive 2026-08-26)
- ❌ Ordering a multi-tier mission by **feature value** when the same mission also contains
  **stop-the-bleed** work (auto-merge disabled, missing dependency, broken CI gate, hard-refusal
  defect in the most-exercised path). The natural pull is to do the exciting thing first. The
  right order is the opposite: stop-the-bleed first, then add features. Reason: each subsequent
  step's blast radius is gated by the cleanliness of the current state. An org with a silently
  broken required check (e.g. `allow_auto_merge: false`) makes every future PR cost extra
  investigation time; a missing runtime dependency makes every test run cost extra noise. Fixing
  the entropy-producing state first means later steps land on a clean base; doing them first
  means later steps inherit the friction. The one-line test: "if this step is broken, does it
  cause every *future* step in this mission to cost more?" If yes, this step comes first,
  regardless of its nominal urgency or how interesting it is.

## Preserved harness frontmatter (verbatim from the three sources)

Kept so no field of the retired clones is lost.

```yaml
# claude-meta-mesa
id: CLAUDE-meta-mesa
name: claude-meta-mesa
description: >
  Meta-mesa orchestrator for Claude Code (FI-002). Given a multi-step mission, decompose
  into L1/L2 skills, sequence them, route to the right organ (arifOS/A-FORGE/GEOX/WEALTH/WELL).
  Load this when a mission spans more than 2 skills or 3 steps, or when you feel yourself
  wandering between tools.
version: 1.0.0
risk_tier: low
autonomy_tier: T1
owner: AAA
audience: [claude-code, FI-002, 333-AGI]
triggers:
  - multi-step mission
  - orchestrating across organs
  - mission spans multiple skills
  - repetitive meta-task
  - session boot for complex work
capability_tier: meta-mesa
ecology_state: WARM
```

```yaml
# opencode-meta-mesa
name: opencode-meta-mesa
description: Meta-mesa orchestrator — given a multi-step mission, decompose into L1/L2 skills, sequence them, recover from failure. Load this when a task spans more than 2 skills or 3 steps, or when you feel yourself wandering between tools.
license: MIT
compatibility: opencode
metadata:
  layer: meta-mesa
  tier: orchestration
  audience: 333-AGI, dispatch
```

```yaml
# qwen-meta-mesa
id: QWEN-meta-mesa
name: qwen-meta-mesa
description: >
  Meta-mesa orchestrator for Qwen Code (FI-003). Given a multi-step mission, decompose
  into L1/L2 skills, sequence them, route to the right organ (arifOS/A-FORGE/GEOX/WEALTH/WELL).
  Load this when a mission spans more than 2 skills or 3 steps, or when you feel yourself
  wandering between tools.
version: 1.0.0
risk_tier: low
autonomy_tier: T1
owner: AAA
audience: [qwen-code, FI-003, 333-AGI]
triggers:
  - multi-step mission
  - orchestrating across organs
  - mission spans multiple skills
  - repetitive meta-task
  - session boot for complex work
capability_tier: meta-mesa
ecology_state: WARM
```

## Provenance

| Source | Harness | SKILL.md sha256 (before merge) |
|---|---|---|
| `/root/AAA/skills/claude-meta-mesa/SKILL.md` | claude-code (FI-002) | `fc760214a8ceba8e423e4a8ba68acc441c1884b0ab5b0251441daf847a134c31` |
| `/root/AAA/skills/opencode-meta-mesa/SKILL.md` | opencode | `97369aaf5efe42b4661132dd36101c9d7e6cc0b5dc4ae96689ad075a12a70950` |
| `/root/AAA/skills/qwen-meta-mesa/SKILL.md` | qwen-code (FI-003) | `f819d116fdb7ee94ac80255563d00934a564b8d1fd1a081f0ae571068be8c21a` |

Frozen copies + LEDGER.json:
`/root/AAA/skills-retired/2026-09-19-namespace-collapse/merges/meta-mesa/`

DITEMPA BUKAN DIBERI ⚒️
