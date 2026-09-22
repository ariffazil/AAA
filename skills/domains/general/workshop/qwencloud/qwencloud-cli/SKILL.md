---
name: qwencloud-cli
description: "Use when managing QwenCloud CLI ops — models list, auth, billing from terminal. QwenCloud CLI ops. Models, auth, billing from terminal."
version: 1.0.0
author: hermes-curator
license: MIT
metadata:
  hermes:
    category: devops
    tags: [qwencloud, cli, billing, auth, models, subscription]
    related_skills: [qwen-token-plan-team-edition, qwen-harness-tools, tokenrouter-guide]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

## When to Use

- User asks to check QwenCloud billing, usage, subscription, or quota from terminal
- User needs to authenticate the QwenCloud CLI (`qwencloud auth login`)
- User wants to browse or search available QwenCloud models
- User asks about QwenCloud account status, workspace info, or support tickets
- Installing or updating `@qwencloud/qwencloud-cli`

## When NOT to Use

- Making API calls to Qwen models (chat, image gen, TTS) → use `qwen-token-plan-team-edition` or `tokenrouter-guide`
- Token Plan Harness tools (web search, code interpreter) → use `qwen-harness-tools`
- Configuring Qwen models in Hermes/OpenCode/OpenClaw → use `tokenrouter-guide`

## Install

```bash
npm install -g @qwencloud/qwencloud-cli
```

Requires Node.js 18+. VPS has v22.23.2 as of 2026-08-26.

## Auth — OAuth Device Flow (NOT API Key)

**Critical:** This CLI uses OAuth PKCE/Device Flow. The existing `QWEN_API_KEY` / `QWEN_BAILIAN_KEY` from `kunci-root.env` are for the Token Plan REST API and do NOT work here.

### Headless/VPS auth pattern

```bash
# Step 1: Initiate device flow (outputs URL + auth_token, exits immediately)
qwencloud auth login --init-only

# Step 2: User opens the verification_url in any browser, authorizes

# Step 3: Complete the login
qwencloud auth login --complete
```

The `--init-only` flag is essential for headless servers — it prints the URL as JSON and exits without blocking. The auth token in the URL expires in ~300 seconds.

### Check auth status

```bash
qwencloud auth status
# Returns: {"authenticated": true/false, "server_verified": true/false}
```

### Logout

```bash
qwencloud auth logout
```

## Commands Reference

| Command | What it does | Auth required? |
|---|---|---|
| `qwencloud models list` | List available models | Yes |
| `qwencloud models search <query>` | Search models by keyword/modality | Yes |
| `qwencloud models info <id>` | Full details for a model | Yes |
| `qwencloud auth login` | OAuth device flow login | N/A |
| `qwencloud auth status` | Show auth state | No |
| `qwencloud usage` | View usage and billing | Yes |
| `qwencloud billing` | Billing limits, consumption breakdown, trends | Yes |
| `qwencloud subscription` | Subscription status and orders | Yes |
| `qwencloud workspace` | Inspect workspaces and quota limits (read-only) | Yes |
| `qwencloud config` | Manage CLI configuration | No |
| `qwencloud doctor` | Environment diagnostics | No |
| `qwencloud support list` | List support tickets | Yes |
| `qwencloud docs` | Browse official docs | No |
| `qwencloud update` | Update CLI to latest | No |

### Output format

All commands accept `--format <table|json|text>` (default: auto). Use `--format json` when piping to other tools.

## Pitfalls

- **Auth ≠ API Key**: Do NOT try to set `QWENCLOUD_API_KEY` env var — the CLI does not read it. OAuth device flow is the only auth method.
- **Token Plan REST API is separate**: The `QWEN_API_KEY` / `QWEN_BAILIAN_KEY` in `kunci-root.env` are for `token-plan.ap-southeast-1.maas.aliyuncs.com` endpoints. They do NOT authenticate `qwencloud` CLI commands.
- **Auth token expiry**: The device flow URL expires in ~300 seconds. If user takes too long, run `--init-only` again.
- **`--init-only` is required for headless**: Without it, `qwencloud auth login` tries to open a browser (PKCE) which fails on VPS.
- **`--complete` must run after user authorizes**: It polls the server. If user hasn't authorized yet, it will timeout (default 120s). Use `--timeout <seconds>` to extend.

## Relationship to Other Skills

- `qwen-token-plan-team-edition` — covers the 4 Token Plan seats, their IAM grants, OSS signed URLs, and REST API patterns. Different auth, different tool.
- `qwen-harness-tools` — covers built-in model tools (web search, code interpreter). Model capability, not account management.
- `tokenrouter-guide` — covers model routing in Hermes/OpenCode. Complementary.

DITEMPA BUKAN DIBERI.