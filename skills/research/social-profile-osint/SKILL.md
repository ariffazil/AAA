---
name: social-profile-osint
description: Use when researching a person's public social profile.
tags: [instagram, youtube, osint, scraping, research, vetting]
metadata:
  hermes:
    tags: [instagram, youtube, osint, research, vetting]
    related_skills: [person-dossier-from-public-sources, online-vendor-legitimacy-check]
---

# Social Profile OSINT (no login, datacenter host)

How to pull public social-profile data (bio, follower count, recent posts, tagged accounts) from a VPS without credentials, API keys, or a browser. Serves person dossiers, coach/vendor vetting, and athlete research.

## Instagram profile pull (works; use this, not the web page)

The rendered `instagram.com/<handle>` page and every mirror site (imginn/picnob/greatfon) sit behind a login wall or Cloudflare "Just a moment" — but the mobile app's private `web_profile_info` endpoint returns a public profile's JSON WITHOUT a session, given the Android app User-Agent:

```python
import json, urllib.request
url = "https://i.instagram.com/api/v1/users/web_profile_info/?username=<handle>"
req = urllib.request.Request(url, headers={"User-Agent": "Instagram 219.0.0.12.117 Android"})
d = json.loads(urllib.request.urlopen(req, timeout=30).read())
u = d["data"]["user"]
# u["biography"], u["full_name"], u["edge_followed_by"]["count"],
# u["edge_owner_to_timeline_media"]["count"], u["bio_links"]
```

- Recent captions live at `u["edge_owner_to_timeline_media"]["edges"][i]["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"]`. Regex `@([A-Za-z0-9_.]+)` over them surfaces who the person tags as coach/team/partner — the corroboration a profile bio never states.
- **Rate limit is real:** a handful of rapid calls returns HTTP 429. Space calls out or cache the JSON; a 429 means "slow down", not "the profile is unreachable".
- Handle existence alone is confirmable by an HTTP redirect on `instagram.com/<handle>` even when the body is login-walled.

## YouTube channel/video discovery (no API key)

`curl` the YouTube search or channel page with a desktop browser UA and regex-parse the embedded JSON — the search HTML carries `videoRenderer` blocks with id/title/owner, and channel pages carry `contentId` + title pairs:

```bash
curl -s "https://www.youtube.com/results?search_query=<query>" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" -o /tmp/yt.html
```

- Search results: `re.findall(r'"videoRenderer":\{"videoId":"([^"]+)".*?"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', html)`.
- Channel pages use the newer `contentId`/`lockupViewModel` shape — grep for `"contentId":"([^"]+)"` near `"title":\{"content":"..."`.
- The `oembed` endpoint (`youtube.com/oembed?url=...&format=json`) gives title/author/publish cleanly for a known video ID.
- The watch page itself may bot-check; the search snippet + oembed usually suffice.

## Pitfalls

- **Prefer the endpoint over the rendered page.** Instagram/TikTok/mirrors are login/Cloudflare-walled from a datacenter IP; the mobile private-API endpoint bypasses that. Do not conclude "can't scrape X" before trying the app-API endpoint with an app User-Agent.
- **Escape `$` and `@` when these snippets land in a Typst document** — Typst treats `$…$` as math mode and `@name` as a label reference, so unescaped dollar signs and @-handles raise "unclosed delimiter" / "label does not exist" at compile time. Write `\$` and `\@` in prose.
- **A 429/rate-limit is not a negative capability.** It means the endpoint works but you hit the throttle; retry spaced out or cache, don't record "Instagram blocked" as a permanent fact.
- **Tagged handles ≠ relationship proof.** A person standing next to a champion and being tagged by a client is not the same as the champion tagging them as "my coach". Require the person's OWN post (first-party tag) before treating a "they coach X" claim as verified.
