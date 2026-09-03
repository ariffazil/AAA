# Red Team: Copilot CLI vs Claude Code vs OpenClaw
## Research Notes — 2026.04.25

---

## RED TEAM: Claim Analysis

### Claim: "Copilot CLI is Level 2→3, reactive, human-is-brain"
**AUDIT: PARTIALLY CORRECT but incomplete.**
- Copilot CLI in 2026 has agents mode with autonomous execution, not just reactive
- The "human is the brain" characterization is 2024-era thinking
- However: still true that Copilot CLI has NO memory, NO policy, NO invariant awareness
- Hard limit: it can execute autonomously but cannot remember WHY it made a decision
- VERDICT: Claim underestimates current Copilot but correctly identifies structural limits

### Claim: "Claude Code thinks well, operates weakly"
**AUDIT: GENERALLY CORRECT.**
- Claude Code has extensive tool-use capabilities but the UX is optimized for human-in-loop
- Permission dialogs interrupt flow — designed for approval, not autonomous operation
- However: the Agent SDK removes these friction points for embedded use cases
- VERDICT: Correct for terminal/IDE use; incomplete for SDK use

### Claim: "OpenClaw is an operating system for tools"
**AUDIT: MOSTLY CORRECT, the framing is right.**
- arifOS does have role separation, tool boundaries, memory, policy, auditability
- The constitutional floors (F1-F13) ARE a policy enforcement system
- However: OpenClaw lacks the formalized hook interception system that Claude Code has
- The governance is in the LLM layer (via prompts/instructions) not the execution layer
- VERDICT: True, but OpenClaw's "OS" is currently more conceptual than implemented

---

## EXTRACTABLE INTELLIGENCE PATTERNS

### 1. HOOK SYSTEM (from Claude Code Agent SDK)
Most important pattern. Concrete implementation of interception architecture.

Events available:
- `PreToolUse` — before tool call, can block/modify/allow
- `PostToolUse` — after tool result, can log/transform
- `PostToolBatch` — after batch resolves, inject context once per model call
- `UserPromptSubmit` — before prompt sent to model, inject context
- `Stop` / `SessionStart` / `SessionEnd` — lifecycle
- `SubagentStart` / `SubagentStop` — parallel task tracking
- `PermissionRequest` — custom permission handling
- `PreCompact` — before conversation compaction

Matcher pattern: regex filter per hook (e.g., `"Write|Edit"`)

Output decisions: allow, deny, modify input, inject context

**What arifOS can learn:**
- This is exactly FLEX_GATES but formalized as a first-class SDK feature
- PreToolUse = 888_JUDGE pre-execution gate
- PostToolUse = vault write verification
- Hook matchers = tool name pattern matching, already partially in arifOS_mcp

### 2. PERMISSION MODES (from Claude Code Agent SDK)
Structured trust escalation levels:

| Mode | Behavior |
|------|----------|
| `plan` | No execution, planning only |
| `default` | Ask for approval |
| `acceptEdits` | Auto-approve file edits |
| `dontAsk` | Deny unlisted tools |
| `bypassPermissions` | Approve all |
| `auto` | Model classifies own tool calls |

**What arifOS can learn:**
- arifOS floors map to permission modes but in LLM prompt, not runtime
- A `permission_mode` config would make this explicit and enforceable by the framework, not just the model
- The `auto` mode (model evaluates own calls) is interesting but risky — could be gamed

### 3. FILE CHECKPOINTING (from Claude Code Agent SDK)
- Track file changes during agent sessions
- Restore to any previous state
- Concrete rollback mechanism

**What arifOS can learn:**
- VAULT999 is immutable ledger but we lack a ROLLBACK mechanism for bad file changes
- Could implement git-based checkpointing: `git worktree` or `git stash` per session
- Pre-commit checkpoint before any critical path file change

### 4. OBSERVABILITY (from Claude Code Agent SDK)
- OpenTelemetry integration
- Traces, metrics, events
- Export to observability backend

**What arifOS can learn:**
- We have no observability stack currently
- Should export to geox.arif-fazil.com observability endpoint
- Traces = audit trail for every tool call

### 5. SUBAGENT LIFECYCLE (from Claude Code Agent SDK)
- `SubagentStart` / `SubagentStop` hooks
- Aggregate results from parallel tasks
- Permission mode inheritance (security note: dangerous)

**What arifOS can learn:**
- OpenClaw subagents exist but lack lifecycle hooks
- Should have `subagent_start` / `subagent_stop` events that write to vault
- Permission inheritance is a security risk — need explicit per-subagent permission config

### 6. GITHUB COPILOT CLI (from `gh` CLI)
`gh copilot` is the Copilot CLI tool. Key commands:
- `gh copilot suggest` — get suggestions
- `gh copilot --agent` — run as autonomous agent
- `gh copilot --chat` — interactive chat
- Integrates with GitHub Actions, Codespaces, issues, PRs

`gh` CLI also has:
- `gh run` — GitHub Actions CI/CD monitoring
- `gh api` — raw GitHub API with `--jq` filtering
- `gh repo` — full repo management
- `gh issue` / `gh pr` — issue and PR management
- `gh release` — release management
- `gh ruleset` — repository rulesets

**What arifOS skills can learn:**
- The `gh api` with `--jq` is powerful for custom queries
- `gh run watch` is better than polling for CI status
- `gh ruleset` could check if repo has protection rules before pushing

---

## WHAT TO EMBED INTO OPENCLAW GITHUB SKILLS

### High Priority

1. **Pre-push GitHub ruleset check**
   - `gh ruleset check` before push
   - Verify branch protection is active
   - Verify status checks are required
   - BLOCK push if rulesets would be bypassed

2. **CI/CD smart polling**
   - `gh run watch` instead of sleep polling
   - Stream logs on failure
   - Attach run link to commit status

3. **Hook-aware tool execution**
   - Before any git push/pulls, run pre-push-check.sh
   - After any file change, run SOT audit
   - After any tool change, run invariant check (13-tool count)

4. **Permission mode configuration**
   - `bypassPermissions` for trusted local ops
   - `dontAsk` + explicit allowlist for untrusted repos
   - `plan` mode for any unknown repo

5. **File checkpointing before critical changes**
   - `git add . && git stash` before any critical path edit
   - Restore via `git stash pop` on failure

### Medium Priority

6. **Subagent result aggregation**
   - Track parallel subagent runs
   - Aggregate into single audit event
   - Write to vault

7. **Observability export**
   - Every push/commit writes trace event
   - Every SOT audit writes metric
   - Export to geox observability endpoint

8. **Session persistence**
   - Sessions should be resumable
   - Fork capability for parallel experiments
   - Conversation compaction before context overflow

---

## GITHUB SKILLS GAP ANALYSIS

| Pattern | Claude Code | Copilot CLI | arifOS/OpenClaw |
|---------|------------|-------------|-----------------|
| Hook interception | ✅ Full SDK | ❌ | ❌ (LLM-level only) |
| Permission modes | ✅ 6 modes | ❌ | ❌ |
| File checkpointing | ✅ | ❌ | ❌ |
| Subagent lifecycle | ✅ | ❌ | Partial |
| Observability | ✅ OTel | ❌ | ❌ |
| GitHub ruleset check | ❌ | ❌ | ❌ (should add) |
| Smart CI polling | ❌ | `gh run watch` | ❌ |
| Session persistence | ✅ | ❌ | Partial |
| Skill system | ✅ | Agent skills | ✅ OpenClaw skills |

---

## RECOMMENDATION

The most valuable pattern to extract and embed is the **HOOK + PERMISSION MODE** combination.

arifOS has the LLM-level governance (F1-F13 floors, 888_JUDGE verdict). What's missing is the **runtime enforcement layer**.

What should be built:
1. A `arifOS_hook` system — PreToolUse / PostToolUse / PostToolFailure events
2. A `permission_mode` config — plan / restricted / normal / bypass
3. A file checkpoint before any critical-path change
4. A GitHub ruleset check in pre-push gate

These are concrete, implementable, and directly reduce the failure modes we observed (wrong branch push, silent critical path changes).
