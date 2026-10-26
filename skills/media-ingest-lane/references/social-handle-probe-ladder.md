# Public social handle probe — VPS-IP hostile ladder

Use when a user asks "find this IG/TikTok/X account" and `media_ingest_url`
returns BLOCKED, OR when there is no URL to feed in (just a handle like
`@raifzilaf`). The default agent instinct is to spend a SerpApi credit on
`instagram_profile` — that is wrong. Five free reads beat one credit, and
the empty result IS a valid answer.

## The probe ladder (cost-ordered)

| # | Tool | Cost | When it works | When it lies |
|---|---|---|---|---|
| 1 | `mcp__exa__web_search_exa` (semantic) | 0 | Third-party directories indexed the handle (StarNgage, Socialveins, Famous Birthdays, influencer catalogs). Often the fastest first read. | Returns similar names that are NOT the handle — always verify the @. |
| 2 | `curl -sL "https://duckduckgo.com/html/?q=%22<handle>%22+instagram"` | 0 | DDG HTML endpoint serves real search results, no JS. The page itself prints "No results found" when nothing matches. | DDG sometimes rate-limits VPS IPs with a CAPTCHA interstitial — if so, fall through to Bing. |
| 3 | `curl -sL "https://www.bing.com/search?q=%22<handle>%22"` (real browser UA) | 0 | Bing serves organic hits for niche handles. | Most hits are search-form echoes (`<handle>%22`). Filter to URLs whose `href` actually points off-domain. |
| 4 | `curl -sL "https://web.archive.org/web/*/instagram.com/<handle>"` | 0 | The account was public at some point and was archived; even deleted accounts sometimes leave a profile-page snapshot. | None I have hit; the only failure mode is "no snapshots" which is the same as "handle was always private". |
| 5 | Same handle on Threads / TikTok / Twitter via Exa | 0 | Cross-platform footprint exists (most creators cross-post at least once). | None — index empty means no cross-post. |

After the ladder, only fall to:

| # | Tool | Cost | When to use |
|---|---|---|---|
| 6 | SerpApi `instagram_profile` | 1 credit | User confirmed the handle, the free ladder returned nothing, and the query is consequential (e.g., brand-safety audit). One credit covers the cost of running the free ladder 5+ times. |
| 7 | Residential-proxy viewer (picuki, imginn) | login + tokens | Almost never from VPS. Cloudflare 403 from datacenter IPs. Skip unless user provides cookies. |

## Per-tool concrete commands

```bash
# Exa semantic index
mcp__exa__web_search_exa --query "<handle> instagram bio"

# DDG HTML — note the quoted-handle trick to avoid drift to similar names
curl -sL -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
  (KHTML, like Gecko) Chrome/121.0 Safari/537.36" \
  "https://duckduckgo.com/html/?q=%22<handle>%22+instagram" \
  -o /tmp/ddg.html -w "HTTP=%{http_code} size=%{size_download}\n"

# Bing raw
curl -sL -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36" \
  "https://www.bing.com/search?q=%22<handle>%22" \
  -o /tmp/bing.html -w "HTTP=%{http_code} size=%{size_download}\n"

# Wayback Machine — single page is usually enough
curl -sL "https://web.archive.org/web/*/instagram.com/<handle>" \
  -o /tmp/wayback.html -w "HTTP=%{http_code} size=%{size_download}\n"
```

## What "empty ladder" looks like

When all five return nothing, the report is one sentence:

```
No public third-party footprint located for @<handle> via Exa, DDG, Bing, Wayback.
```

This is not a failure. It is the answer. Two real-world meanings:

- The handle is **personal** (private, no cross-post, no directory listing). The
  user would know the owner only by direct contact — agent can't help.
- The handle **doesn't exist** or is misspelled. A real "Arif Fazil" personal
  IG (e.g., `@raifzilaf`) with zero footprint is more consistent with personal
  than with non-existent.

## Decision tree

```
User: "find @handle on IG"
  ├─ handle has a URL form?  → media_ingest_url(url) → use the platform ladder
  └─ handle only?            → run the 5-step ladder above
                                ├─ any result → report the data, attach source URL
                                └─ all empty  → "no public footprint" report, no further spend
```

## Anti-patterns

- ❌ "I cannot access IG from VPS IP, account may not exist" — false by default; the VPS
  block is the lane, not the handle.
- ❌ Asking the user "is this your account?" before probing. The ladder's empty result is
  the answer; asking before probing steals attention the data does not require.
- ❌ Spending a SerpApi credit before the ladder — five free reads always come first.
- ❌ Treating Exa "similar names" as the target — verify the @ before quoting.
- ❌ Going to picuki/imginn first — they are residential-proxy viewers; from VPS, Cloudflare 403.

## Related skills

- `media-ingest-lane/SKILL.md` — the parent skill, owns the URL-form lane.
- `paste-router/SKILL.md` — for incoming pastes with URLs.
- `aaa-capability-compiler` — for routing once the handle resolves to an entity.