---
id: hermes-coding-gateway
name: hermes-coding-gateway
owner: Hermes-Prime (333-AGI orchestration layer)
risk_tier: T2
version: 1.0.0-2026.08.25
description: >
  Governed multi-CLI coding fabric. Hermes dispatcher routes intent to
  specialist workers (qwen / claude / codex / kimi / gh). F13 enforcement
  via wrapper executables, not prompt-only. Hermes accepts only verifiable
  artifacts (diff, test result, lint, commit SHA, PR URL). First milestone
  of arifOS coding-fabric doctrine.
floor_scope: [F1, F2, F4, F7, F8, F11, F12, F13]
autonomy_tier: T1
capability_tier: coding-fabric-gateway
ecology_state: WARM
forbidden:
  - Never pass tokens through CLI args.
  - Never spawn workers with perm-bypass flags.
  - Never accept textual done claim without verification output.
  - Never bind opencode-ai/opencode (archived 2025-09-18 -> Crush).
  - Never let worker CLI bypass the F13 wrapper for T3 actions.
cites:
  - QwenLM/qwen-code: default execution substrate (multi-provider, MCP-native)
  - anthropics/claude-code: premium implementation/review worker
  - openai/codex: OpenAI-flavour coding worker
  - MoonshotAI/kimi-code: media-input specialist
  - cli/cli (gh): GitHub operations (F13-gated for writes)
---

# Hermes Coding Gateway — Governed Multi-CLI Coding Fabric

First milestone of arifOS coding-fabric doctrine (2026-08-25, F13 SOVEREIGN).
Hermes is the control-plane / orchestrator. CLI workers (qwen, claude, codex,
kimi, gh) are specialist executors. Hermes NEVER executes coding work itself.
It routes, gates, and verifies.

## Why this exists

CPU-only VPS is not a blocker. Worker CLIs use provider / cloud models
externally; only Hermes + the F13 wrapper live on the VPS. Isolation, policy
gate, observability, and F13 approval are the local concerns.

Do NOT bind opencode-ai/opencode. Upstream repo archived 2025-09-18, moved
to Crush. Quarantined at /root/.quarantine/2026-08-25-opencode-archived/.

## Architecture

Telegram / Cron / Webhook / AAA cockpit
        |
        v
  Hermes Router (this gateway)
   - Task classifier
   - Policy engine (routing.yaml)
   - F13 approval gate (gate-f13.sh)
   - State + audit log (VAULT999 + arifFlow)
   - Delegation broker
        |
        +-- qwen  (default autonomous coding worker)
        +-- claude  (premium implementation / review)
        +-- codex  (OpenAI-flavour worker)
        +-- kimi  (media-input specialist)
        +-- F13 wrapper -> /usr/bin/gh  (GitHub write gate)
        |
        v
  Isolated git worktree / sandbox
        |
        v
  Diff + tests + lint + commit SHA + PR URL
        |
        +-- Hermes reports structured artifact to caller

## Routing policy (routing.yaml)

```yaml
# Default worker for general autonomous coding
default:
  worker: qwen
  mode: headless
  reason: "Multi-provider, MCP-native, subagents, SDK, Telegram channel"

implementation:
  worker: codex
  fallback: claude
  requirements:
    - isolated_worktree
    - test_before_return

architecture_review:
  worker: claude
  requirements:
    - read_only_first
    - produce_risks_and_tradeoffs

research_or_media:
  worker: kimi
  requirements:
    - preserve_source_links
    - no_external_write

ssh_remote_maintenance:
  worker: antigravity
  requirements:
    - command_allowlist
    - interactive_confirmation

github_operations:
  worker: gh
  requirements:
    - read_only_default
    - f13_for_write
  f13_required_subcommands:
    - pr merge
    - pr close
    - release create
    - release delete
    - repo delete
    - secret set
    - secret delete
    - variable delete
    - workflow dispatch production
```

## Mandatory output schema

Every worker invocation MUST return this structured envelope. Hermes NEVER
accepts free-form done text.

```json
{
  "status": "ok | partial | failed | requires_f13",
  "plan": "<one-line intent>",
  "worker": "qwen | claude | codex | kimi | gh | antigravity",
  "session_id": "<hermes session id>",
  "worker_session_id": "<CLI worker session id>",
  "files_changed": ["path1", "path2"],
  "diff_summary": "<short diff narrative>",
  "tests_run": ["pytest tests/x.py::test_y"],
  "test_result": "pass | fail | skipped | not_applicable",
  "lint_result": "pass | fail | not_applicable",
  "commit_sha": "<git sha or empty>",
  "pr_url": "<url or empty>",
  "cost_usd": 0.0,
  "duration_ms": 0,
  "risk_level": "low | medium | high | irreversible",
  "requires_f13": false,
  "proposed_irreversible_actions": [],
  "verification_commands": [
    {"cmd": "pytest -q tests/x.py", "expected": "exit 0"}
  ],
  "evidence_paths": ["/path/to/diff", "/path/to/log"],
  "f1_snapshot": "/root/.local/share/arifos/snapshots/<ts>/"
}
```

## Spawn pattern (worker invocation)

```bash
# Qwen headless — default autonomous worker
qwen -p '<TASK>' --max-turns 15 --output-format json \
  --permission-mode plan --cwd <isolated_worktree>

# Codex headless
codex exec --json '<TASK>' --cd <isolated_worktree>

# Claude Code print mode
claude -p '<TASK>' --max-turns 15 --output-format json \
  --allowedTools 'Read,Edit,Glob,Grep,Bash(git diff),Bash(pytest)' \
  --permission-mode plan

# Kimi media-first
kimi --print '<TASK>' --output-format json --max-turns 10

# GitHub write via wrapper (exits 42 -> F13 approval)
gh-shim pr create --title ... --body ...
```

## F13 enforcement — wrapper executable (NOT prompt-only)

gate-f13.sh is a shell wrapper that intercepts T3-class commands and exits
with code 42 to signal F13 approval is required. Hermes detects the exit
code, sends the proposal (target + exact command + diff + reversibility)
to Telegram, and waits for Arif reply. On approval, Hermes executes the
SAME COMMAND VERBATIM — never a silently-improved version.

## F13 enforcement matrix

| Action | Policy |
|---|---|
| Read files, grep, test, lint | Auto-allow in workspace |
| Edit files in worktree | Allow; diff artifact mandatory |
| Commit local | Allow with diff summary |
| Push branch | F13 confirmation via gh-shim |
| Create/update PR, issue | F13 confirmation |
| Merge PR / release / deploy | F13 confirmation + human review |
| Secret access / export | Deny by default |
| Delete infra / data | F13 + explicit scoped command |
| Money / vault seal / identity mutation | Human-only |
