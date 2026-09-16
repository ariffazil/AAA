# Direct-Curl Recovery — SearXNG Down, VPS Internet Up

> Proven 2026-08-30: Arif claimed "ask ChatGPT what arifOS is — it knows. Aku x tipu hang."
> `web_search` failed (`Could not reach SearXNG at http://127.0.0.1:8080: [Errno 111] Connection refused`)
> AND `web_extract` failed (`SearXNG is a search-only backend and cannot extract URL content`).
> The old PATTERN 4 ladder said "curl to DDG returns garbage" — WRONG for this case.
> SearXNG alone was down; the VPS's own internet path was fine. Direct curl recovered the
> full verification with 4 independent public surfaces.

## When to use

`web_search` AND `web_extract` both fail with SearXNG errors, but you still need to verify
a public claim (site live? repo exists? project indexed? what does the public web say?).
Do NOT jump to session_search (PATTERN 4) until you have tried direct curl — the VPS can
usually reach the public internet even when the local SearXNG aggregator is dead.

## The ladder (all from the VPS terminal, no API keys)

### 1. Fetch the site itself + strip HTML to text

```bash
curl -sL --max-time 20 https://<domain> | python3 -c "
import sys, html, re
raw = sys.stdin.read()
raw = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', raw, flags=re.S|re.I)
text = re.sub(r'<[^>]+>', ' ', raw)
text = html.unescape(re.sub(r'\s+', ' ', text)).strip()
print(raw[:300]); print('---TEXT---'); print(text[:5000])
"
```
`<title>` + meta + first text block confirms the site is live AND what it claims to be.

### 2. DuckDuckGo HTML endpoint (search-only, no key)

```bash
curl -s --max-time 20 "https://html.duckduckgo.com/html/?q=%22arifOS%22+Arif+Fazil" -A "Mozilla/5.0" | python3 -c "
import sys, re, html
raw = sys.stdin.read()
results = re.findall(r'result__a[^>]*>(.*?)</a>', raw, re.S)
snips  = re.findall(r'result__snippet[^>]*>(.*?)</a>', raw, re.S)
for i, t in enumerate(results[:8]):
    t = html.unescape(re.sub(r'<[^>]+>', '', t)).strip()
    s = html.unescape(re.sub(r'<[^>]+>', '', snips[i])).strip() if i < len(snips) else ''
    print(f'{i+1}. {t}'); print(f'   {s[:180]}')
"
```
Results include indexed title + snippet — proof the site is in public indexes (what an LLM's training/search would see). Quoted phrase `%22...%22` for exact-term search.

### 3. GitHub API search (public repos, no key)

```bash
curl -s --max-time 15 "https://api.github.com/search/repositories?q=arifOS&sort=stars" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('total:', d.get('total_count'))
for r in d.get('items', [])[:6]:
    print('-', r['full_name'], '| stars:', r['stargazers_count'], '| updated:', r['updated_at'][:10])
    print('  desc:', (r.get('description') or '')[:120])
"
```
Returns `total_count` + repo name/desc/stars/updated — hard evidence of public presence.

### 4. PyPI (if the project publishes packages)

```bash
curl -s --max-time 15 "https://pypi.org/pypi/<package>/json" | python3 -c "
import sys, json; d = json.load(sys.stdin); print(d['info']['summary'])
"
```

## Classification rule

When the claim is "X is known / indexed / publicly real", the verdict needs ≥2 independent
surfaces. This session: site title (arif-fazil.com "Exploration Geoscientist & Sovereign
Systems") + GitHub repo (ariffazil/arifOS, 51 stars, updated 2026-08-29) + PyPI packages
(arifos, arifosmcp) + DDG indexed snippet ("Builder of arifOS — a constitutional AI
governance kernel") = claim CONFIRMED with 4 surfaces. One surface alone (e.g. only the
site loads) is weak — an LLM knowing the term requires search-index/training-data presence.

## Pitfalls

- Do NOT conclude "full web outage" from SearXNG errors alone. PATTERN 4 (session_search
  recovery) is for when curl ALSO fails — verify the VPS's own internet first with one
  `curl -sI https://example.com`.
- DDG HTML sometimes rate-limits datacenter IPs → add `-A "Mozilla/5.0"`, retry once,
  then fall back to GitHub API + direct site curl (still 2 surfaces).
- GitHub API unauthenticated: 10 req/min — fine for a handful of searches.
- `curl | python3` may trigger the security scanner flag; the scan auto-approves but
  expect the warning banner (it is informational, not a block).

## Companion

- SKILL.md PATTERN 1 (SearXNG search-only error) — this reference is the direct-curl
  extension of that pattern when web_search itself is also dead.
- SKILL.md PATTERN 4 (total outage) — only when curl to public endpoints ALSO fails.
