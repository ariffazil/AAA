# Claude Code BYOK auth chain — 3-layer worked case 2026-08-09

Goal: route `claude -p` through the federation gateway (FED :4000 LiteLLM) with
model `apex-888`. Every attempt failed until three independent layers of stale
auth state were removed. Each layer produced a DIFFERENT error, which is the
diagnostic fingerprint to remember.

## Layer 1 — profile.d BYOK script pointed claude at a vendor endpoint

`/etc/profile.d/claude-code-byok.sh` exported:
```bash
export ANTHROPIC_BASE_URL="${ANTHROPIC_BASE_URL:-https://api.kimi.com/coding/}"
export ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-${KIMI_API_KEY}}"
```
→ claude hit Kimi's coding endpoint → `403 You've reached your usage limit for
this billing cycle ... kimi.com/code/#pricing`.

Fingerprint: error body references a VENDOR pricing URL = the request reached a
vendor endpoint, not your gateway. Check `env | grep ANTHROPIC` in the shell
that launches claude.

## Layer 2 — stored OAuth login overrode env routing

After fixing the shell env, claude still failed:
`Credit balance is too low` — with NO `/v1/messages` entry in the gateway access
log. The transcript at `~/.claude/projects/-root/<session>.jsonl` showed the
error as a SYNTHETIC assistant message (`"model": "<synthetic>"`, 0 tokens) —
proof the client decided locally without any network call.

Root cause: `~/.claude.json` still held `primaryApiKey` (an sk-ant key) +
`oauthAccount` from a past `/login`. Claude Code prefers the stored login over
env routing, and its stored account was out of credit.

Fingerprint: `model: "<synthetic>"` + 0 tokens in the transcript = local state
decision. `grep -o '"primaryApiKey"[^,]*' ~/.claude.json` to confirm.
Fix: `cp ~/.claude.json ~/.claude.json.bak-$(date +%Y%m%d-%H%M%S)` then delete
both keys.

## Layer 3 — inherited stale env defeated `:-` defaults

Even with profile.d rewritten to `${ANTHROPIC_BASE_URL:-http://127.0.0.1:4000}`,
a fresh login shell still showed `BASE=[https://api.kimi.com/coding/]`. The
Hermes/agent daemon was started in the kimi era and inherited the old value into
every child — profile.d's `:-` default only applies when the var is UNSET.

Fingerprint: `bash -lc 'echo $ANTHROPIC_BASE_URL'` differs from what profile.d
claims to export.

Fix: UNCONDITIONAL exports (no `:-`):
```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:4000"
export ANTHROPIC_API_KEY="${LITELLM_MASTER_KEY:-${KIMI_API_KEY}}"
```
Long-running daemons keep the stale value until restarted — note this in the
report; new login shells are fixed immediately.

## Bonus gotcha: pkill self-match

`pkill -f "claude.*daemon"` killed the shell running it (exit -15, "Orphan
recovery"): the pattern string is part of the shell's own argv, so pkill matched
itself. Use `pgrep -af claude` first, then `kill <pid>` by explicit PID.

## Working invocation (verified FED_OK)

```bash
env ANTHROPIC_BASE_URL=http://127.0.0.1:4000 \
    ANTHROPIC_API_KEY=<litellm master key> \
    ANTHROPIC_MODEL=apex-888 \
    claude -p --model apex-888 "Reply with exactly: FED_OK" --output-format text
```
