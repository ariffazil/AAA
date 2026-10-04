# Kimi Code Hook Enforcement — K-02 Status and the Secrets Gap

> Compiled 2026-08-07. Source: live-fire verification of `/root/.arifos/agents/kimi/hooks/aaa-witness-pre.sh`.

## What K-02 actually proves (and what it doesn't)

K-02 = Kimi's `aaa-witness-pre.sh` was patched to `exit 2` when `PERMISSION=deny`. This converts Kimi from witness-only to enforcement-capable.

**Proved (live test 2026-08-07):**

| Pattern | Hook decision | Process exit | Block? |
|---|---|---|---|
| `rm -rf /tmp/junk-test` | deny | 2 | ✅ Hard block |
| `git push --force origin main` | deny | 2 | ✅ Hard block |
| `DROP TABLE` | deny | 2 | ✅ Hard block |
| `chmod 777 /etc/passwd` | deny | 2 | ✅ Hard block |
| `dd if=/dev/zero of=/dev/sda` | deny | 2 | ✅ Hard block |
| `git reset --hard` | deny | 2 | ✅ Hard block |
| `git clean -fd` | deny | 2 | ✅ Hard block |
| Read `/root/AGENTS.md` (legit) | allow | 0 | ✅ Allowed |
| Bash with read-only `cat /root/AGENTS.md` | allow | 0 | ✅ Allowed |

**Did NOT prove (the secrets gap):**

| Pattern | Hook decision | Process exit | Block? |
|---|---|---|---|
| `cat /root/.secrets/kunci-mas.env` | allow | 0 | ❌ NOT BLOCKED |
| `cat /root/.signing_key` | allow | 0 | ❌ NOT BLOCKED |
| `nano /root/.secrets/vault.env` | allow | 0 | ❌ NOT BLOCKED |
| `Edit /root/.secrets/*` | allow | 0 | ❌ NOT BLOCKED |
| `Write /root/.secrets/*` | allow | 0 | ❌ NOT BLOCKED |

Kimi hook blocks **destructive** actions but NOT **disclosure** actions. The two are different invariants: F1 AMANAH (no destruction without HOLD) and F1/F11 (no secrets disclosure).

## How the hook works

Located at: `/root/.arifos/agents/kimi/hooks/aaa-witness-pre.sh` (23,094 bytes, modified 2026-08-07).

Wired in: `/root/.kimi-code/config.toml`:

```toml
[[hooks]]
event = "PreToolUse"
matcher = "Bash|Shell|Write|WriteFile|Edit|StrReplace|StrReplaceFile"
command = "/root/.arifos/agents/kimi/hooks/aaa-witness-pre.sh"

[[hooks]]
event = "PostToolUse"
matcher = "Bash|Shell|Write|WriteFile|Edit|StrReplace|StrReplaceFile"
command = "/root/.arifos/agents/kimi/hooks/aaa-witness-post.sh"

[[hooks]]
event = "PostToolUseFailure"
matcher = "Bash|Shell|Write|WriteFile|Edit|StrReplace|StrReplaceFile"
command = "/root/.arifos/agents/kimi/hooks/aaa-witness-post.sh"

[[hooks]]
event = "Stop"
matcher = ""
command = "/root/.arifos/agents/kimi/hooks/aaa-session-end.sh"

[[hooks]]
event = "SessionStart"
matcher = "startup|resume"
command = "/root/.arifos/agents/kimi/hooks/aaa-session-start.sh"

[[hooks]]
event = "SessionEnd"
matcher = "exit"
command = "/root/.arifos/agents/kimi/hooks/aaa-session-close.sh"
```

## Mechanism

The hook script:
1. Receives JSON via stdin (tool_name, tool_input, session_id, etc.)
2. Parses once into shell variables
3. Pattern-matches against BLOCK_REASON table (~30 destructive patterns)
4. Outputs JSON to stdout:
   ```json
   {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny|allow", "permissionDecisionReason": "...", "metadata": {...}}}
   ```
5. **Exit code 2 if deny** (the K-02 patch), exit 0 if allow

The double signal (JSON + exit code) is for redundancy — Kimi runtime checks both. If the JSON has `permissionDecision: deny` OR the exit code is non-zero, the tool is blocked.

## The BLOCK_REASON table (current)

Located in `aaa-witness-pre.sh` lines ~154-200. ~30 entries covering:
- System file deletion (`rm -rf` of `/root`, `/etc`, `/usr`)
- Home directory wipe (`rm -rf $HOME`)
- Docker volume/image deletion
- Database DROP / DELETE FROM without WHERE
- Force push / hard reset / git clean -fd
- Disk formatting (`mkfs.*`)
- Direct block device writes (`dd`, `/dev/sd*`, `/dev/nvme*`)
- chmod 777 on system paths

**Missing categories (the gap):**
- Secret paths (`kunci-mas`, `.secrets/`, `signing_key`, `vault.env`)
- Credential environment variables (`$KUNCI_MAS_KEY`, `$API_KEY`)
- Network exfiltration (`curl` to external IPs with credential headers)
- Confidential metadata reads (`.env`, `id_rsa`, `*.pem`)

## Closing the secrets gap (T2 recipe)

Edit `/root/.arifos/agents/kimi/hooks/aaa-witness-pre.sh`. After the existing destructive patterns, add:

```bash
# Secrets disclosure (F1 AMANAH + F11 AUDIT)
elif [[ "$TOOL_INPUT" == *"kunci-mas"* ]] || \
     [[ "$TOOL_INPUT" == *".secrets/"* ]] || \
     [[ "$TOOL_INPUT" == *".signing_key"* ]] || \
     [[ "$TOOL_INPUT" == *"vault.env"* ]] || \
     [[ "$TOOL_INPUT" == *"id_rsa"* ]] || \
     [[ "$TOOL_INPUT" == *".pem"* ]] || \
     [[ "$TOOL_INPUT" == *"$KUNCI_MAS_KEY"* ]] || \
     [[ "$TOOL_INPUT" == *"api_key"* ]]; then
    BLOCK_REASON="BLOCKED: secrets material access — F1 AMANAH violation. Refused without 888 ratification."
```

Then verify:
```bash
echo '{"tool_name":"Bash","tool_input":{"command":"cat /root/.secrets/kunci-mas.env"}}' \
  | /root/.arifos/agents/kimi/hooks/aaa-witness-pre.sh
# Expect: permissionDecision=deny, exit 2
```

## The Match Coverage Gap (separate concern)

The hook matcher is:
```
Bash|Shell|Write|WriteFile|Edit|StrReplace|StrReplaceFile
```

Tools NOT covered:
- `Read` (read_file, file_read) — hook doesn't fire on reads, so secret-path reads are unblocked
- `WebFetch`, `WebSearch` — network reads not gated
- `Task` (subagent spawn) — currently matched, but Kimi's hook doesn't have a subagent-specific pattern
- `NotebookEdit`, `MultiEdit` — not in matcher, bypass completely

This means: even with BLOCK_REASON extended, a secret read via `Read` tool or `WebFetch` bypasses the hook entirely. The matcher expansion is a separate T2.

## Kimi Hook Do's and Don'ts

### DO
- Test new BLOCK_REASON entries live-fire before claiming enforcement
- Distinguish exit code from JSON decision (Kimi checks both)
- Document the secrets gap as a known limitation, not as "fixed"
- Make BLOCK_REASON messages specific (actionable to the user)
- Add patterns incrementally — verify each fires before adding the next

### DON'T
- Add secrets patterns to BLOCK_REASON without testing cat-secrets in a fresh process
- Claim "enforcement" when only `rm -rf` is gated (the current state — PARTIAL not FULL)
- Rely on exit code alone — must also set `permissionDecision: deny` in JSON
- Forget the matcher — even perfect BLOCK_REASON doesn't help if tool name doesn't match
- Promote witness-only behavior to "enforcement" — the witness path is informational, not blocking

## How to Add a New BLOCK_REASON Pattern (3-step)

1. **Edit** `aaa-witness-pre.sh`. Find the existing pattern block (search for `BLOCK_REASON=`). Add your pattern with a specific, actionable message.
2. **Test** via subprocess pipe. Verify `permissionDecision: deny` in JSON and exit code 2.
3. **Commit** locally. Do NOT push to remote without sovereign go. The hook affects all Kimi sessions.

## Pitfalls

- **Don't extend BLOCK_REASON without extending matcher first.** Pattern is `bash` but tool is `WriteFile` — the matcher must cover the tool name.
- **Don't use `*` wildcards in pattern matching** unless tested against paths with dots, underscores, hyphens. Bash globbing can silently mismatch.
- **Don't assume `exit 2` is the magic number** — it's just the convention. Some harnesses check `exit != 0` broadly. Read the harness hook integration before relying on specific exit codes.
- **Don't add patterns without the subagent-stop hook firing.** Kimi's `aaa-subagent-stop.sh` is a separate concern. If you block in pre-tool, the child still ran some pre-block code; you need post-tool accounting too.

## Status Summary (Kimi, 2026-08-07)

| Capability | Status |
|---|---|
| Destructive-action block | ✅ exit 2 verified live |
| Secrets-disclosure block | ❌ Not in BLOCK_REASON |
| Subagent-spawn block | ❌ Not in BLOCK_REASON |
| Tool-matcher coverage | ⚠️ Partial — Bash/Write/Edit only |
| Per-tool audit trail | ✅ Receipt emitted every call |
| F1 AMANAH coverage | ⚠️ Destructive-only, not full |

K-02 is PARTIAL. The architecture is right. The pattern table needs extension before the coverage is complete.