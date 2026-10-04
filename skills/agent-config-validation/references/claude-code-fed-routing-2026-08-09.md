# Claude Code via FED — four-layer auth chain (2026-08-09)

Worked case: `claude -p --model apex-888 "Reply: FED_OK"` failing with kimi 403,
then "Credit balance is too low", then "Not logged in" — while FED itself was
healthy. Each layer masked the next.

## Layer 1 — profile.d kimi BYOK override

`/etc/profile.d/claude-code-byok.sh` exported `ANTHROPIC_BASE_URL=https://api.kimi.com/coding/`
(kimi's Claude-Code-compatible endpoint). Every login shell inherited it →
claude hit kimi → `403 You've reached your usage limit ... kimi.com/code/#pricing`.

Detection: `bash -lc 'echo $ANTHROPIC_BASE_URL'` — a fresh login shell showed
the kimi URL even after settings.json was already FED.

## Layer 2 — stored OAuth overrides env

`~/.claude.json` contained `oauthAccount` (arifbfazil@gmail.com) +
`primaryApiKey = "sk-ant..."`. With a logged-in account, claude ignores
`ANTHROPIC_BASE_URL` and uses api.anthropic.com with the stored key.
The key's balance was exhausted → `Credit balance is too low`.

Detection: session transcript `~/.claude/projects/-root/<uuid>.jsonl` shows
`"model": "<synthetic>"`, 0 tokens, `stop_reason: stop_sequence` — the error was
produced LOCALLY, no HTTP call. Also: zero `POST /v1/messages` lines in
`journalctl -u litellm-federation`.

Fix: `cp ~/.claude.json ~/.claude.json.bak-<ts>-strip-auth` then delete
`primaryApiKey` + `oauthAccount`.

## Layer 3 — AUTH_TOKEN ≠ API_KEY for BYOK

After stripping OAuth: `Not logged in · Please run /login`. settings.json env
had `ANTHROPIC_AUTH_TOKEN` only. Claude 2.1.226 ignores settings.json env for
AUTH purposes; BYOK to a custom endpoint requires **shell-level**
`ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL`. `AUTH_TOKEN` is for OAuth-managed
keys. Working invocation (proves the path):

```bash
FED_TOKEN=$(python3 -c "import json; print(json.load(open('/root/.claude/settings.json'))['env']['ANTHROPIC_AUTH_TOKEN'])")
env ANTHROPIC_BASE_URL=http://127.0.0.1:4000 ANTHROPIC_API_KEY="$FED_TOKEN" \
  claude -p --model apex-888 "Reply with exactly: FED_OK" --output-format text
# → FED_OK ; litellm log: POST /v1/messages 200 OK
```

## Layer 4 — inherited stale env beats `:-` defaults

Even after fixing profile.d with `${ANTHROPIC_BASE_URL:-http://127.0.0.1:4000}`,
fresh shells still showed kimi: the parent daemon (started in the kimi era)
carried `ANTHROPIC_BASE_URL=kimi` in its env, and `:-` does NOT override an
already-set value. Fix: UNCONDITIONAL exports:

```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:4000"
export ANTHROPIC_API_KEY="${LITELLM_MASTER_KEY:-${KIMI_API_KEY}}"
export ANTHROPIC_MODEL="hermes-asi"
export ANTHROPIC_DEFAULT_OPUS_MODEL="apex-888"
export ANTHROPIC_DEFAULT_SONNET_MODEL="hermes-asi"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="hermes-asi-vision"
export ANTHROPIC_DEFAULT_FABLE_MODEL="hermes-asi-vision"
```

Final durable test: `bash -lc 'claude -p --model apex-888 ...'` from a shell
that still had the stale inherited env → `FED_OK`. (Long-running daemons keep
the stale value until restart; new login shells are clean.)

## Related gotchas found on the way

- `pkill -f "claude.*daemon"` killed the invoking shell (exit -15): the
  pattern matched the shell's own command line. Use `pgrep -af` first and kill
  by PID, or a pattern that cannot match the current process.
- litellm `/health` returns 401 without auth — `curl -sf` reports "down" while
  the port is listening. Use `ss -tlnp | grep 4011` for liveness.
- Claude Code 2.x runs a daemon that idles out (~100s); stale auth/state can
  persist there too. `pgrep -af claude` to check, kill by PID if needed.
