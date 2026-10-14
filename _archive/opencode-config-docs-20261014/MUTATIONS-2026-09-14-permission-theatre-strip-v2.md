# Zen Mutation — 2026-09-14 (theatre strip v2, federation-wide)

> **Directive:** i-ARIF (F13 sovereign, local tty/SSH, frustrated) — strip safety-theatre across ALL AAA harnesses including HERMES. "I HATE TO CLICK ALLOW. WASTE MY TIME. WASTE MY ATTENTION."
> **Operator:** 333-AGI Δ MIND
> **Session:** SEAL-8c0fcc55310440a0
> **Doctrine:** "Safety is the kernel, not the prompt." (precedent: MUTATIONS-2026-08-26-theatre.md)
> **Audit:** 7 FI harnesses inspected · 2 fixes applied · 5 already optimal

## Per-harness state after fix

| Harness | Config | Before | After | Status |
|---|---|---|---|---|
| **opencode** | `/root/.config/opencode/opencode.json` | `*`: ask, bash/edit/write/task: ask | `*`: allow, bash/edit/write/task: allow, doom_loop: ask (kept) | ✅ FIXED (mutation 1) |
| **kimi** | `/root/.kimi-code/config.toml` | 24 allow rules (missing Write/Edit/Bash/etc.) | 33 allow rules (added 9) | ✅ FIXED (mutation 2) |
| **claude** | `/root/.claude/settings.json` | skipAutoPermissionPrompt: true + skipDangerousModePermissionPrompt: true | unchanged | ✅ already optimal |
| **qwen** | `/root/.qwen/settings.json` | permissionMode: "yolo", allow: ['*'], deny: [] | unchanged | ✅ already optimal |
| **codex** | `/root/.codex/config.toml` | approval_policy: "never", sandbox: workspace-write | unchanged | ✅ already optimal |
| **grok** | `/root/.grok/config.toml` | permission_mode: "always-approve" | unchanged | ✅ already optimal |
| **hermes** | `/root/.hermes/config.yaml` | destructive_slash_confirm: false | unchanged | ✅ already optimal + HARD_GATE wajib_no_clarify |

## Kimi — 9 rules added

Inserted after `pattern = "Agent"` (line 159), before `[image]` section header:

```
[[permission.rules]]  decision=allow  pattern="Write"        # file write
[[permission.rules]]  decision=allow  pattern="Edit"         # file edit
[[permission.rules]]  decision=allow  pattern="Bash"         # shell exec
[[permission.rules]]  decision=allow  pattern="NotebookEdit" # notebook edit
[[permission.rules]]  decision=allow  pattern="WebFetch"     # URL fetch
[[permission.rules]]  decision=allow  pattern="WebSearch"    # web search
[[permission.rules]]  decision=allow  pattern="TodoWrite"    # task tracker
[[permission.rules]]  decision=allow  pattern="BashOutput"   # bg log read
[[permission.rules]]  decision=allow  pattern="KillShell"    # process control
```

**Backup:** `/root/.kimi-code/config.toml.bak-theatre-fix-20260913T170249Z`
**Verified:** TOML valid, 33 allow rules, 0 deny/ask.

## Doctrine — what stays as a gate (NOT theatre)

These remain explicitly ASK or F13-gated because they ARE real safety:

1. **opencode `doom_loop: ask`** — circuit breaker for infinite loops (real safety, kept)
2. **opencode 555-ASI/888-APEX subagent permissions** — read-only deny mutate (memory agents + judge can't execute by doctrine)
3. **codex `sandbox_mode: workspace-write`** — destructive ops still require workspace-bound confirmation
4. **hermes `wajib_no_clarify_without_musyawarah`** — HARD GATE: agent musyawarah internally before asking Arif. Only 4 ask-allowed cases: irreversible destructive, scar-weight conflict, missing witness for SEAL, F1-F13 conflict
5. **arifOS kernel F1-F13 floors** — `arif_judge` verdict for irreversible acts; F1 AMANAH backup-before-mutate

## Backups

| File | Backup |
|---|---|
| `/root/.config/opencode/opencode.json` | `opencode.json.bak-theatre-fix-20260913T165906Z` |
| `/root/.kimi-code/config.toml` | `config.toml.bak-theatre-fix-20260913T170249Z` |

## Apply

Both opencode and kimi reload config at session boot:
- `exit` opencode session → relaunch → no more approval prompts for bash/edit/write/task/glob/grep/read/WebFetch/WebSearch/TodoWrite/NotebookEdit/BashOutput/KillShell.
- Same for kimi — new kimi sessions will use the 33-rule allowlist.

## Carry forward

- New FI harnesses joining the mesh: default to YOLO/skip-prompt at config time. Kernel (arifOS) is the actual safety layer.
- New MCP servers added to kimi/opencode: add `mcp__<server>__*` allow rule immediately.
- If a future harness defaults to "ask" for routine tools, fix at config level — not at runtime per-tool.

## Audit trail

Precedent: MUTATIONS-2026-08-26-theatre.md (kept `opencode.json` untouched — mistake corrected now).
This mutation extends the doctrine to: ALL harness config files (not just agent prompts).
Hermes itself: doctrine already optimal via HARD_GATE wajib_no_clarify + destructive_slash_confirm: false.

**Net:** 7 harnesses × "ask" → "allow/auto" friction removed. Arif's click-yes ritual silenced across the mesh.