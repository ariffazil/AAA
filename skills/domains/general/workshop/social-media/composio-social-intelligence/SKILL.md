---
id: composio-social-intelligence
name: composio-social-intelligence
autonomy_tier: T1
version: 1.0.0
description: "Composio social-mcp gateway for Gmail + Reddit + X/Twitter + public web search. 3-band policy."
owner: AAA
risk_tier: medium
knowledge_basis:
  language: true
  math: false
  physics: false
host_compatibility:
- hermes
- claude-code
- opencode
dependencies:
  skills:
  - FORGE-mcp-federation-ops
  servers: []
  tools: []
examples:
- Monitor Gmail inbox for specific senders or subjects
- Search Reddit for trending topics or competitor mentions
- Draft Reddit posts with approval-before-publish flow
- Send email drafts for review before sending
- Check social-mcp gateway health and Composio connectivity
tests:
- social_mcp_status returns composio_proxy=ok
- gmail_fetch_emails returns results for valid query
- reddit_draft_post creates draft without external API call
- reddit_post without approval_id returns pending approval
- Replay of used approval_id is rejected
version_lock:
  schema_version: '1'
  artifact_hash: pending
orthogonal_tags:
  trinitarian:
  - Δ
  functional:
  - Routing
  - OBSERVE
  layer:
  - RUNTIME
  autonomy_tier: T2
floor_scope:
- F2
- F3
- F4
- F8
- F13
---

# Composio Social Intelligence

## Overview

Social media intelligence operations via the **social-mcp gateway** (`/root/social-mcp/`) — a policy-enforced bridge between Hermes and Composio's 1000+ app integrations. Currently active: **Gmail** (full suite), **Reddit** (read + write with approval), **X/Twitter** (via xurl CLI, read + write with approval), and **public web social search** (Firecrawl, no OAuth needed). The gateway enforces a 3-band security model with F13-gated approvals for all mutating operations.

## Reference Files

- [references/composio-cli-dual-key.md](references/composio-cli-dual-key.md) — diagnostics for dual API key issue (ak_ vs uak_)
- [references/composio-skills-api.md](references/composio-skills-api.md) — how Composio skills arrive via runtime search
- [references/reddit-exploration-sweep.md](references/reddit-exploration-sweep.md) — multi-query parallel sweep pattern for open-ended Reddit signal discovery

## When to Use

- Monitor Gmail inbox — search, fetch messages, list labels, check profile
- Draft emails for review before sending
- Search Reddit — browse subreddits, search posts, get comments
- Draft Reddit posts/comments (local-only, no external API)
- Publish Reddit content (requires approval flow)
- Read X/Twitter — search, timeline, mentions, user profiles (via xurl CLI)
- Post/reply/DM on X — requires approval flow (xurl CLI wrapped)
- Public web social search — Reddit/X/IG/LinkedIn/TikTok/YouTube via Firecrawl, no OAuth needed (works even before account linking)
- Check social-mcp gateway health and Composio connectivity
- Audit social media operations via ledger

## When NOT to Use

- **Do not use for X/Twitter OAuth setup** — requires `xurl` CLI auth (`xurl auth apps add`), not Composio OAuth. User must complete manually.
- **Do not use for Instagram direct posting** — Meta OAuth pending, not yet wired. Public search works via `web_search_social(platform="instagram")`.
- **Do not bypass approval flow** — all PROTECTED operations require single-use approval
- **Do not hardcode API keys** — Composio key in `kunci-root.env`, xurl tokens in `~/.xurl` (NEVER read/send)
- **Do not call Composio tools directly** — always route through social-mcp gateway

## Architecture

```
Hermes Agent
    ↓ MCP tool calls
social-mcp gateway (FastMCP, /root/social-mcp/src/server.py)
    ├── ComposioClient (CLI subprocess) → `composio execute SLUG -d '{...}'` → Composio API → Gmail / Reddit
    ├── xurl_run() (subprocess) → xurl CLI → X/Twitter API
    └── firecrawl_search() (aiohttp) → Firecrawl API → public web results
```

**CRITICAL (2026-08-25)**: Current architecture uses MCP stdio proxy (`/root/.config/mcp/composio-proxy.mjs`) with hardcoded `user_id=arif-federation`. This causes "No connected account" errors because OAuth connections exist under different user IDs (e.g., `arifbfazil@gmail.com`). 

**Root cause discovered**: Two separate API keys exist:
- `ak_` key (in `kunci-root.env`) — used by MCP proxy, v3 endpoint
- `uak_` key (in `/root/.composio/user_data.json`) — used by CLI binary at `/root/.composio/composio`

The CLI binary can see connections via `composio dev connected-accounts list`, but the MCP proxy cannot. **Fix options**: (1) update MCP proxy user_id mapping, or (2) switch ComposioClient to CLI subprocess. See `references/composio-cli-dual-key.md` for discovery commands.

> **STATE (verified 2026-09-19): the CLI half of this diagnosis cannot be reproduced today —
> the CLI is not installed.** `/root/.composio/` does not exist, so neither
> `/root/.composio/user_data.json` (the `uak_` key file) nor `/root/.composio/composio` (the
> binary) is on disk, and no `composio` binary is on PATH. What would have to exist: the
> binary from `curl -fsSL https://composio.dev/install | sh`, plus the `user_data.json` that
> `composio login` writes. Until then the only Composio transport on this host is the stdio
> proxy `/root/.config/mcp/composio-proxy.mjs`, and fix option (2) — CLI subprocess — is
> unavailable rather than merely disfavoured.

### 3-Band Policy

| Band | Operations | Approval | Example |
|------|-----------|----------|---------|
| **OBSERVE** | Read-only, autonomous | None | `gmail_fetch_emails`, `reddit_search_posts` |
| **MUTATE** | Local draft creation | Logged, no approval | `reddit_draft_post`, `gmail_create_draft` |
| **PROTECTED** | Send/post/delete | Requires single-use approval | `gmail_send_email`, `reddit_post`, `reddit_comment` |

Policy file: `/root/social-mcp/policy/social_policy.yaml`

## Tool Catalog (82 tools loaded)

### Gmail (full suite)
- **Read**: `fetch_emails`, `fetch_message`, `get_profile`, `list_drafts`, `search_people`, `get_attachment`, `list_labels`, `list_threads`
- **Draft**: `create_draft`, `edit_draft`
- **Protected**: `send_email`, `send_draft`, `forward_message`, `delete_message`, `delete_draft`, `add_label`, `batch_modify`, `move_to_trash`, `create_filter`, `update_settings`

### Reddit (read + write)
- **Read**: `browse_subreddit`, `search_posts`, `search_subreddits`, `get_post`, `get_comments`, `get_user_profile`, `get_subreddit_rules`, `list_flairs`, `get_random`
- **Draft**: `create_draft_post`, `create_draft_comment`
- **Protected**: `post`, `comment`, `delete_post`, `delete_comment`, `edit_comment`
- **Disabled**: `vote` (never auto-vote)

### Instagram (future)
- Pending Meta OAuth + App Review
- Planned: `lookup_profile_by_exact_handle`, `discover_media_by_hashtag`, `monitor_own_account_mentions`

### X/Twitter (via xurl CLI — wrapped in social-mcp, added 2026-08-25)
xurl v1.3.1 installed at `~/go/bin/xurl` (`go install github.com/xdevplatform/xurl@latest`). NOT via Composio — separate OAuth.
- **Read (OBSERVE)**: `x_status`, `x_whoami`, `x_search`, `x_read`, `x_user`, `x_timeline`, `x_mentions`
- **Draft (MUTATE)**: `x_draft_post` — local-only, zero external call
- **Protected**: `x_post`, `x_reply`, `x_dm` — same single-use payload-bound approval flow as Reddit
- **Not yet wired**: like/repost/follow/delete (future, each needs approval flow)
- Requires X developer app + OAuth2 (`xurl auth oauth2 --app NAME`, then `xurl auth default NAME`). Until done, read tools fail with auth error — `x_status` shows "no apps registered".

### Public Web Social Search (no OAuth — added 2026-08-25)
`web_search_social(query, platform, limit)` — Firecrawl search wrapper, OBSERVE band.
- Platforms: `reddit`, `x`, `instagram`, `tiktok`, `youtube`, `linkedin`, or `""` (any) — maps to `site:` operator
- **Use this for discovery/monitoring when OAuth is not yet connected** — it works immediately
- Returns compact `{title, url, description}` per result; markdown scraping enabled upstream

**Total gateway tools: 28** (5 Gmail + 9 Reddit + 11 X + 1 web search + 2 approval mgmt + status). Composio-side catalog remains 82 tools (61 Gmail + 21 Reddit).

### ACTUAL tool parameters (verified 2026-08-25 — NOT what docs say)

The Composio tool schemas differ from the social-mcp gateway's interface. **When wrapping or debugging, ALWAYS verify with `composio execute <SLUG> --get-schema` first.** Key mismatches discovered:

| Social-mcp function | WRONG param | CORRECT param |
|---|---|---|
| `reddit_browse(subreddit=...)` | `subreddit` | (drop — REDDIT_GET has no subreddit param; use `show`, `sort`, `limit`, `time_filter`) |
| `reddit_search_posts(query=...)` | `query` | `search_query` (required) |
| `reddit_get_post(...)` | `post_id` | `subreddit` (required) — fetches subreddit feed, not single post |
| `reddit_post(..., body=...)` | `body` | `text` (for self post) or `url + kind:"link"` (for link post) |
| `reddit_comment(..., post_id=..., body=...)` | flat args | `thing_id` + `text` (both required) |
| `reddit_get_comments(post_id=...)` | `post_id` | `article` = the post permalink URL (required); optional `sort`, `depth`, `limit` |
| `gmail_create_draft(to=...)` | `to` | `recipient_email` |
| `gmail_fetch_message(...)` | `message_id` | `message_id` + `user_id:"me"` |

**REDDIT_GET schema**: top-level keys = `[show, sort, after, count, limit, before, time_filter]` — no `subreddit` key at top level. Use `show` to filter (e.g., `"all"` for frontpage).
**REDDIT_RETRIEVE_POST_COMMENTS** (gateway tool `reddit_get_comments`): requires `article` = the post's full permalink URL (e.g. `https://www.reddit.com/r/x/comments/<id>/...`). There is NO `post_id` key. Optional keys: `sort`, `depth`, `limit`. Passing `post_id` → "Unknown key" schema rejection (verified live 2026-08-26, 3× failed loop).
**GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID**: requires `message_id` + `user_id` (use `"me"`).

Workflow when adding a new wrapper tool:
```bash
composio execute SLUG --get-schema  # read inputSchema carefully
```


## Composio Skills (Execution Playbooks)

Composio "Skills" are **not installable** — they are execution playbooks that arrive inside `COMPOSIO_SEARCH_TOOLS` responses. When the agent searches for tools by use case, the response includes:

```json
{
  "primary_tool_slugs": ["SLACK_FIND_CHANNELS", "SLACK_SEND_MESSAGE"],
  "related_tool_slugs": ["SLACK_FIND_USERS"],
  "difficulty": "easy",
  "recommended_plan_steps": ["Resolve channel ID first", "Send message with resolved ID"],
  "known_pitfalls": ["Passing channel name where ID expected returns not_found"]
}
```

**Key insight**: Use case phrasing matters. "Post message to Reddit subreddit" gets a skill. "Reddit tools" does not.

**No list API** — skills come via runtime search only. Our gateway currently calls tools by slug directly; future enhancement could add a search-first layer.

## Approval Flow

```
1. Agent calls PROTECTED tool (e.g., reddit_post) WITHOUT approval_id
   → Gateway returns: {approval_id: "ap-xxx", status: "pending"}
   
2. Agent (or human via Telegram) approves
   → State: pending → approved
   
3. Agent calls SAME tool WITH approval_id
   → Gateway: approved → executing → executed/failed
   → Approval is single-use, payload-bound (SHA-256 hash)
   
4. Replay attempt with same approval_id
   → Rejected: "Approval not valid for execution (status: executed)"
   
5. Tampered payload (different body, same approval_id)
   → Rejected: "Payload mismatch — approval was bound to different content"
```

Approval records: `/root/social-mcp/audit/approvals/ap-*.json`
Draft records: `/root/social-mcp/audit/drafts/dr-*.json`
Audit ledger: `/root/social-mcp/audit/ledger.jsonl` (metadata only, no raw payloads)

## Security Hardening (2026-08-25)

Five fixes implemented:

1. **Approval replay protection** — State machine: pending → approved → executing → executed/failed. `consume_approval()` atomically transitions before any Composio call.

2. **Payload binding** — Every approval stores `payload_hash` (SHA-256 of canonical JSON). Tampered payloads rejected.

3. **Draft semantics** — `reddit_draft_post` and `reddit_draft_comment` save to local audit dir only. Zero Composio calls for draft creation.

4. **Async/event loop** — All MCP tools are `async def`, direct `await composio.call_tool()`. FastMCP event loop stays responsive.

5. **Sensitive payload protection** — Ledger contains only metadata. Approval records store `encrypted_payload` (Fernet) + `payload_hash`. All sensitive dirs `chmod 700`, files `chmod 600`.

## OAuth Connection (BLOCKER)

**Current status**: API key present (`COMPOSIO_API_KEY` in `kunci-root.env`), gateway operational, but **OAuth connections not linked**.

**Last audit log**:
```json
{"result_status": "executed", "result_id": "No connected account found for user ID arif-federation for toolkit..."}
```

**Required action**: Connect Gmail + Reddit OAuth via Composio dashboard:
1. Go to `composio.dev` → login
2. "Connected Accounts" → connect Gmail + Reddit with Arif's accounts
3. Test read-only operations first (`gmail_fetch_emails`, `reddit_search_posts`)
4. Then test protected flows with real accounts

## Procedure

### Step 1: Check Gateway Health

```python
# Via MCP tool
mcp__social_mcp__social_mcp_status()
# Expected: {"composio_proxy": "ok", "api_key": "present", ...}

# X/Twitter CLI status (separate from Composio)
mcp__social_mcp__x_status()
# Shows xurl install status + auth state
```

### Step 2: Public Discovery (no OAuth needed — works immediately)

```python
# Web social search via Firecrawl
mcp__social_mcp__web_search_social(query="agentic AI", platform="reddit", limit=5)
# Returns compact {title, url, description} — no OAuth required

# Reddit search (Composio — needs account linking)
mcp__social_mcp__reddit_search_posts(query="AI agents", limit=5)
```

### Step 3: Gmail Operations (needs OAuth account linking)

```python
# Gmail search
mcp__social_mcp__gmail_fetch_emails(query="from:ariffazil@gmail.com is:unread", max_results=10)

# Draft email
mcp__social_mcp__gmail_create_draft(to="user@example.com", subject="Meeting", body="Hi there")
# Logged as MUTATE, no approval needed for draft

# Send email (PROTECTED — needs approval)
mcp__social_mcp__gmail_send_email(to="user@example.com", subject="Hello", body="Body")
# Returns {approval_id: "ap-xxx"} → approve → call again with approval_id
```

### Step 4: Reddit Operations (needs OAuth account linking)

```python
# Browse subreddit
mcp__social_mcp__reddit_browse(subreddit="r/artificial", sort="hot", limit=10)

# Search posts
mcp__social_mcp__reddit_search_posts(query="AI agents", limit=5)

# Draft (local only, zero external API)
mcp__social_mcp__reddit_draft_post(subreddit="r/artificial", title="Test post", body="Draft content")
# Returns draft_id for later publishing

# Publish (PROTECTED — needs approval)
mcp__social_mcp__reddit_post(subreddit="r/artificial", title="Test", body="Content")
# Returns {approval_id: "ap-xxx"} → approve → call again with approval_id
```

### Step 5: X/Twitter Operations (requires separate xurl OAuth)

```python
# Check X auth status
mcp__social_mcp__x_status()

# Read-only searches
mcp__social_mcp__x_search(query="agentic AI", limit=10)
mcp__social_mcp__x_whoami()
mcp__social_mcp__x_mentions(limit=20)

# Post (PROTECTED — needs approval)
mcp__social_mcp__x_post(text="Hello world!")
# Returns {approval_id: "ap-xxx"} → approve → call again with approval_id
```

## Allowed Tools

| Tool / Capability | Purpose |
|-------------------|---------|
| `mcp__social_mcp__*` | All social-mcp gateway tools (Gmail, Reddit, X, web search, status) |
| `mcp__composio__*` | Direct Composio tools (82 total: Gmail + Reddit) |
| `curl` | Health probes for social-mcp gateway |
| `cat` / `read_file` | Inspect audit ledger, approval records, policy file |

## Pitfalls

1. **Python path for testing**: social-mcp runs under `/usr/bin/python3` (system python with fastmcp 3.4.6 installed). The default `python3` may resolve to a venv that lacks `fastmcp`. Always use `/usr/bin/python3` for direct testing: `/usr/bin/python3 -c "import fastmcp"`.

2. **xurl ≠ xurls**: The X/Twitter CLI is `xurl` (from `github.com/xdevplatform/xurl`). The system `xurl` at `/usr/local/bin/xurls` is a URL extractor. The real xurl is at `~/go/bin/xurl` (installed via `go install`). Verify: `xurl auth status`.

3. **MCP server restart**: Killing social-mcp (`pkill -f "social-mcp/src/server.py"`) lets Hermes respawn it automatically. Do NOT use `&` backgrounding in terminal — use `background=true` if needed. For manual test: `background=true` with `notify_on_complete=true`.

4. **Composio OAuth ≠ xurl OAuth**: Gmail/Reddit use Composio OAuth (dashboard.composio.dev → Connected Accounts). X/Twitter uses xurl's own OAuth2 (`xurl auth apps add` + `xurl auth oauth2`). They are independent auth flows.

5. **web_search_social as discovery bridge**: Before OAuth is connected, `web_search_social` is the only tool that returns real data. Use it for Reddit/X/IG discovery while waiting for account linking.

6. **Snippet ≠ evidence (critical)**: `web_search_social` returns TIER-2 evidence (title + ~200-char description). This is sufficient for "a post titled X exists" but NEVER sufficient for body-level claims, sentiment analysis, or fact extraction. When full-content retrieval is unavailable (Reddit 403, no OAuth), the honest output is "snippets only — cannot synthesize beyond this." Do NOT build confident narratives from snippets. See `claim-receipt-discipline` FM13 for the full T1–T4 evidence-tier ladder. For CVE verification, use NVD API (`services.nvd.nist.gov/rest/json/cves/2.0?cveId=...`). For MCP spec versions, use `modelcontextprotocol.io/specification`. For GitHub repo receipts, use `api.github.com/repos/OWNER/REPO`.

6. **aiohttp required for Firecrawl**: The `firecrawl_search()` helper uses `aiohttp`. Available in system python (`/usr/bin/python3`) but may not be in all venvs.

7. **Composio dual-key issue**: Two API keys exist — `ak_` key (MCP proxy) and `uak_` key (CLI). They operate under different user contexts, causing OAuth connections to be invisible to one or the other. See `references/composio-cli-dual-key.md` for diagnostics and fix options.

8. **Composio tool schemas ≠ natural param names**: Always `composio execute SLUG --get-schema` before writing wrappers. For example: `search_query` not `query`, `recipient_email` not `to`, `thing_id` not `post_id`, `text` not `body`. The schema is canonical; the skill catalog may be misleading.

9. **Composio CLI install path**: `curl -fsSL https://composio.dev/install | sh` installs binary to `~/.composio/composio` and symlinks to `~/.local/bin/composio`. Ensure `~/.local/bin` is on PATH in social-mcp subprocess env. **UNBUILT on this host (verified 2026-09-19): neither path exists and `~/.composio/` is absent — the installer must be run before any `composio …` command or the CLI-subprocess ComposioClient can work.**

10. **reddit_get_comments requires `article` (permalink URL), not `post_id`**: The gateway tool `reddit_get_comments` maps to Composio's `REDDIT_RETRIEVE_POST_COMMENTS`. Its only required key is `article` — a full Reddit permalink URL like `https://www.reddit.com/r/x/comments/<id>/<slug>/`. There is no `post_id` key. Passing `post_id` triggers an opaque "Unknown key" schema error with no guidance on the correct param. Verified 2026-08-26 in a 3× retry loop. Always pass the full permalink URL as `article`.

11. **Composio CLI execute is SLOW — do NOT misdiagnose timeout as auth loss**: Each `composio execute REDDIT_*` call takes **~34-35s** wall-clock (verified 2026-08-31). A cron script with `timeout=30` will spuriously catch `subprocess.TimeoutExpired` and mislabel it as "No connected account / auth lost". Before assuming auth broke, (a) confirm the connection is ACTIVE via `composio connections list` (look for the `reddit` key), (b) run the exact query manually and TIME it, (c) only then diagnose auth. Connection `reddit_dace-proker` is valid and returns 5 legit posts — the chronic reddit-daily-monitor failure was purely a too-low `timeout=30` racing the ~35s real latency. **Fix:** set `timeout=75`+ in scan scripts (2026-08-31). Dual-key MCP-proxy "no connected account" (`ak_` vs `uak_`) is a SEPARATE, documented issue — the cron uses the CLI (`uak_`) path, not the MCP proxy, so it is unaffected by the proxy user_id mismatch.

## Forbidden Actions

- **NEVER** bypass approval flow for PROTECTED operations
- **NEVER** hardcode `COMPOSIO_API_KEY` — it's in `kunci-root.env`
- **NEVER** call Composio API directly — always route through social-mcp gateway
- **NEVER** expose raw payloads in audit ledger — metadata only
- **NEVER** auto-vote on Reddit — `vote` tool is DISABLED
- **NEVER** skip payload hash verification on approval consumption
- Escalate to **F13** if OAuth connection fails or approval flow breaks

## Output Format

```
## Skill Result: composio-social-intelligence

### Summary
One-paragraph summary of social media operation performed.

### Evidence
- Gateway health: <OK / DEGRADED / DOWN>
- Operation band: <OBSERVE / MUTATE / PROTECTED>
- Tool called: <tool_name>
- Approval ID: <ap-xxx or null>
- Result status: <success / pending / failed>
- Audit entry: <ledger line or "logged">

### Recommendations
- Next step (e.g., approve pending operation, check OAuth connection)
- Any security or policy concerns

### Escalations
- None / <list>
```

## Escalation Path

| Condition | Escalate To | Method |
|-----------|-------------|--------|
| OAuth connection missing | Human (F13) | Telegram: "Connect Composio OAuth" |
| Approval flow broken | arifOS 888_JUDGE | A2A / MCP verdict_request |
| Gateway health DEGRADED | A-FORGE + service-health-triage | Health probe + incident channel |
| Payload hash mismatch | Security audit | Investigate tampering attempt |
| Composio API quota exceeded | Human (F13) | Upgrade plan or throttle operations |

---

*Skill forged from: 2026-08-25 session — Composio social intelligence deep research + social-mcp gateway security hardening*
*AAA Skill Library — version 1.0.0*
