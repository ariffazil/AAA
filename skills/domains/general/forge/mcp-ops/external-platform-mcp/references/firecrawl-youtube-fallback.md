# Firecrawl YouTube Scrape Fallback

When `yt-dlp` + `youtube-transcript-api` + browser all fail (cloud IP block, no cookies, expired auth), use Firecrawl MCP `firecrawl_scrape` on the YouTube watch page directly.

## When to use

Symptoms:
- `yt-dlp` returns `"Sign in to confirm you're not a bot"`
- `youtube-transcript-api` returns `IPBlocked` or `RequestBlocked`
- Cookies file at `/root/.secrets/yt-cookies.txt` only has consent cookies (no auth session)
- Browser tools hang or hit consent walls
- User needs transcript + metadata quickly, doesn't need keyframes or vision analysis

## Pattern

```python
result = mcp__firecrawl__firecrawl_scrape(
    url="https://www.youtube.com/watch?v=VIDEO_ID",
    formats=["markdown"],
    onlyMainContent=True,
    waitFor=5000,  # let page hydrate
)
# result.markdown contains:
# - Title, channel, upload date, duration, views
# - Description with timestamps
# - Full transcript (auto-extracted by Firecrawl)
# - Chapter list
# 
# Save large output:
with open('/tmp/yt_digest_<id>.md', 'w') as f:
    f.write(result.markdown)
```

## Why this works

Firecrawl routes through its proxy network — the request appears from Firecrawl's egress IPs, not your VPS IP. YouTube's anti-bot heuristics are bypassed. The watch page itself contains the transcript in `<script>` tags, which Firecrawl's renderer extracts server-side.

## Limitations

- Output can be 200KB+ for long videos (Huberman Lab 2h48m → 218KB). Save to file, don't keep in context.
- No keyframe extraction (use real pipeline if frames needed)
- No vision analysis
- Transcript may be cleaner than auto-generated (since YT embeds it in metadata)
- Sections appear with `>>` markers in markdown — strip before summarization

## Transcript extraction post-scrape

```python
import re
with open('/tmp/yt_digest_<id>.md') as f:
    md = f.read()
lines = md.split('\n')
# Transcript section starts after `## Transcript`
try:
    start = lines.index('## Transcript') + 1
    transcript = '\n'.join(lines[start:])
except ValueError:
    transcript = md

# Strip >> speaker markers
clean = re.sub(r'^>>\s*', '', transcript, flags=re.MULTILINE)
```

## Verified 2026-08-26

Used to extract Huberman Lab "Peptides: The Science, Uses & Safety | Dr. Abud Bakri" (2h48m, 218KB markdown). Got full transcript + 29 chapter markers + metadata in one call. All YouTube anti-bot paths had failed.

## When NOT to use

- User wants keyframes or vision analysis (use full yt-dlp pipeline with cookies)
- Video has captions disabled AND Firecrawl can't extract them (rare, but possible)
- User wants VAULT999 sealed hash (use `yt_digest.py --vault-hash-only` instead)