# Reddit + Composio Monitoring Infrastructure

**Proven: 2026-08-26** — Reddit daily cron + volatility features build session.

## Composio CLI Syntax

Correct `composio execute` format (as of v0.4.0):

```bash
# CORRECT — --account flag + -d flag
composio execute REDDIT_SEARCH_ACROSS_SUBREDDITS \
  --account reddit_dace-proker \
  -d '{"search_query":"gold","limit":5,"sort":"hot","time_filter":"week"}'

# WRONG — positional args don't work
composio execute REDDIT_SEARCH_ACROSS_SUBREDDITS reddit_dace-proker '...'
```

Flag reference:
- `--account <selector>` — alias, word_id, or connected account ID
- `-d '<json>'` — JSON or JS-style object arguments (use single-quoted string)
- `--get-schema` — fetch input schema without executing
- `--dry-run` — validate without executing
- `-p` — parallel mode (repeated slug -d pairs)

## Composio Reddit Connection Status

```bash
# Check connections
composio connections list | grep -i reddit

# Verify Reddit OAuth is active
composio execute REDDIT_GET_ME_PREFS --account reddit_dace-proker
```

Active connection: `reddit_dace-proker` (arifbfazil@gmail.com). OAuth valid as of 2026-08-26.

## Reddit API Response Format

The `REDDIT_SEARCH_ACROSS_SUBREDDITS` tool returns:

```json
{
  "successful": true,
  "data": {
    "after": "t3_1vxsq34",
    "before": null,
    "posts": [
      {
        "author": "username",
        "created_datetime": "2026-08-25T19:54:52+00:00",
        "id": "1vyak4z",
        "permalink": "https://www.reddit.com/r/SubName/comments/...",
        "score": 7,
        "num_comments": 14,
        "selftext": "...",
        "subreddit": "SubName",
        "title": "Post title",
        "url": "https://..."
      }
    ]
  }
}
```

**Key: response has `data.posts[]` array, NOT `data.children[].data`.**

Pitfall: Social-mcp `reddit_search_posts` is a different tool with different params. Use `REDDIT_SEARCH_ACROSS_SUBREDDITS` for structured Reddit search with sort/time filter control.

## Reddit IP Blocking

Reddit blocks datacenter IPs (403 from VPS even with curl_cffi browser impersonation, firecrawl, and direct requests). Three workarounds that work:

1. **Composio Reddit tools** — routes through Composio's infra (not our IP). This is the primary path.
2. **social-mcp web_search_social** — uses Firecrawl public search with platform=reddit filter. Returns snippets, not full content.
3. **Old Reddit JSON** — `https://old.reddit.com/r/SUB/THREAD_ID.json` — also blocked from datacenter IPs. Not a workaround.

## yfinance MultiIndex Column Handling

yfinance 1.5.x returns DataFrames with MultiIndex columns even for single-ticker downloads. To flatten:

```python
import yfinance as yf, pandas as pd
df = yf.download('GC=F', period='6mo', interval='1d', progress=False)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)
```

Without this, `df['Open']` returns a Series wrapping another Series, causing `TypeError: unsupported operand type(s) for /: 'list' and 'list'` downstream.

## Cron Scripts

Daily Reddit scan: `/root/.hermes/scripts/reddit_daily_scan.py`
- Searches r/algotrading (XAUUSD/gold/volatility), r/AI_Agents (memory/MCP/architecture), r/malaysia (Penang/semiconductor/tech)
- Output: `/root/forge_work/reddit_daily/scan_YYYY-MM-DD.json`
- Cron: `reddit-daily-monitor` (job_id: 14e52a8cab81), daily at 09:00 MYT
- Uses `composio execute` with correct syntax

Weekly Malaysia intel: `malaysia-intel-weekly` (job_id: c37e116d61af), Monday 10:00 MYT
- 8 topics across r/malaysia, r/Tech_Malaysia, r/MalaysianPF, r/Penang, r/ExpatFIRE
- Uses mcp__social_mcp__web_search_social (Firecrawl public search, no Reddit OAuth needed)
