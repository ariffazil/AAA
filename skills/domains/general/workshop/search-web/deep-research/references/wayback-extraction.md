# Wayback Extraction — Cloudflare-walled newsroom/PR pages (ladder rung 13)

> Companion to `research-tool-fallback-ladder.md` (appended there when that file becomes patchable — the read-before-write gate + view-dedup currently block reference-file patches on this skill).

Gartner/IDC/vendor press releases: r.jina.ai returns a 1x1 tracker-pixel stub ("cached snapshot" warning), and direct curl hits the JS challenge. The Wayback snapshot serves the full page:

```bash
curl -sL --max-time 40 "https://web.archive.org/web/2026/<full-original-url>" -o /tmp/page.html
python3 -c "
import re, html
x = open('/tmp/page.html', errors='ignore').read()
x = re.sub(r'<script.*?</script>|<style.*?</style>', '', x, flags=re.S)
x = re.sub(r'<[^>]+>', ' ', x); x = html.unescape(x); x = re.sub(r'\s+', ' ', x)
i = x.lower().find('<keyword>')
print(x[max(0,i-300):i+2200])"
```

- Locate body text by keyword search (`'By 2027'`, `'STAMFORD'`) — press-release bodies index well after tag stripping.
- Rate limit is real (429 on the availability API) — fetch the `web/2026/<url>` form directly, one URL per call.
- **Proven:** 2026-08-15 — Gartner May 2026 "uniform governance / AI agent autonomy levels" press release extracted complete (L1 Observe / L2 Advise / L3 Act with Approval / L4 Act Autonomously tables intact) after both Jina and curl failed. Same session: SearXNG all-engine outage (brave/DDG/google suspended) handled by jina-wrapped DDG + Bing News RSS per rungs 10/12.
