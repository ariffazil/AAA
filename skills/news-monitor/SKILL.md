---
name: news-monitor
description: RSS/Atom feed monitoring and news aggregation for automated tracking. Use when: (1) Monitoring blogs or news sites for updates, (2) Setting up automated news alerts, (3) Tracking specific topics via RSS, (4) Aggregating multiple news sources, (5) Creating cron-based news digests.
---

# News Monitor Skill

Monitor RSS/Atom feeds and aggregate news sources.

## Quick Start

### Using blogwatcher CLI

```bash
# List configured feeds
blogwatcher list

# Check for updates across all feeds
blogwatcher check

# Check specific feed
blogwatcher check --feed "feed-name"

# Add new feed
blogwatcher add "https://example.com/feed.xml" --name "example"

# Remove feed
blogwatcher remove "feed-name"
```

## Feed Configuration

Feeds stored in: `~/.config/blogwatcher/feeds.json`

### Sample Config Structure

```json
{
  "feeds": [
    {
      "name": "techcrunch",
      "url": "https://techcrunch.com/feed/",
      "checkInterval": "1h",
      "lastChecked": "2026-03-25T10:00:00Z"
    }
  ]
}
```

## Cron Integration

Set up automated news checks:

```json
{
  "tool": "cron",
  "action": "add",
  "job": {
    "name": "news-digest",
    "schedule": {"kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Kuala_Lumpur"},
    "payload": {"kind": "agentTurn", "message": "Run news check and send digest"},
    "sessionTarget": "isolated"
  }
}
```

## Common News Sources

| Category | Feed URL |
|----------|----------|
| Tech | `https://news.ycombinator.com/rss` |
| AI/ML | `https://arxiv.org/rss/cs.AI` |
| Malaysia | `https://www.thestar.com.my/rss/` |
| Geopolitics | `https://www.foreignaffairs.com/rss.xml` |
| Finance | `https://www.ft.com/?format=rss` |

## Output Format

News digest structure:

```markdown
# News Digest — YYYY-MM-DD

## [Category]
- **Headline** — Source, Time
  Summary snippet...

## [Category]
...
```

## Alert Patterns

### Keyword Alerts

```bash
blogwatcher check | grep -i "keyword" | tee alerts.log
```

### Priority Sources

Mark critical feeds with `--priority high` for separate alerting.

## F2 (Truth) Compliance

- Cross-verify breaking news with 2+ sources
- Flag unconfirmed reports with Ω₀
- Distinguish opinion from reporting
