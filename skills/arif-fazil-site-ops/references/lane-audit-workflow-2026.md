# Lane Audit Workflow (verified 2026-08-06)

This is the pattern for auditing a single federation lane (e.g. `/world`, `/earth`,
`/politics`) for SEO/GEO/CWV/WCAG and constitutional-machine-truth defects, then
producing a Tier 0–3 upgrade roadmap.

Proven on `/world` audit (06 Aug 2026, ~90 min from probe to verdict).

## When to use

- User asks "audit /world" / "audit the world site" / "what's wrong with X lane"
- A federation lane has grown without consistent maintenance and defects have
  accumulated (orphan 404s, fake machine files, missing OG, etc.)
- Constitutional integrity check on a SOUL/BODY/SPINE ring page before adding
  new features (avoid adding to a broken surface)

## Method (6 phases, ~90 min total)

### Phase 1 — Live probe (10 min)

Run these 5 probes in order. Each is curl-reproducible; the defect survives
in writing. Save output to `/tmp/lane-audit/<lane>-<date>/`.

```bash
LANE=$1  # e.g. "world"
DOMAIN=https://arif-fazil.com

# 1.1 — main page 200 + size
curl -sI $DOMAIN/$LANE/ | head -1
curl -s -o /dev/null -w "%{http_code} %{content_type} %{size_download}b ttfb=%{time_starttransfer}s\n" $DOMAIN/$LANE/

# 1.2 — machine-truth URLs (the F2/F12 wound)
for u in llms.txt page.json missions.json sitemap.xml; do
  curl -s -o /tmp/lane-audit/$LANE-$u -w "$u: %{http_code} %{content_type} %{size_download}b\n" $DOMAIN/$LANE/$u
  # Content-type must MATCH extension. HTML under .txt = LIE.
done

# 1.3 — security headers
curl -sI $DOMAIN/$LANE/ | grep -iE "content-security-policy|strict-transport|x-frame|x-content-type|permissions-policy"

# 1.4 — cache state
curl -sI $DOMAIN/$LANE/ | grep -iE "cf-cache|age|expires|cache-control"

# 1.5 — meta tags audit (live HTML body)
curl -s $DOMAIN/$LANE/ > /tmp/lane-audit/$LANE-body.html
echo "og:* count:    $(grep -c 'og:' /tmp/lane-audit/$LANE-body.html)"
echo "twitter:* count: $(grep -c 'twitter:' /tmp/lane-audit/$LANE-body.html)"
echo "theme-color:    $(grep -c 'theme-color' /tmp/lane-audit/$LANE-body.html)"
echo "JSON-LD count:  $(grep -c 'application/ld+json' /tmp/lane-audit/$LANE-body.html)"
echo "script srcs:    $(grep -c '<script' /tmp/lane-audit/$LANE-body.html)"
echo "map libs:       $(grep -ci 'leaflet\|d3\|maplibre\|mapbox' /tmp/lane-audit/$LANE-body.html)"
```

### Phase 2 — Defect catalog (15 min)

Every finding follows this shape:

| # | Severity | Finding | Evidence (curl-reproducible) |
|---|---|---|---|
| L1 | CRITICAL | /world/llms.txt returns 200 + HTML | `curl -I` shows content_type=text/html, body is `<!doctype html>...` |

Severity tiers:
- **CRITICAL** — machine-truth wound (F2/F12 violation). URL claims one thing, returns another. Must fix before deploy.
- **HIGH** — missing flagship feature (GEO leak, missing map, no OG meta). Hurts adoption/citation.
- **MED** — accessibility/compliance gap (no theme-color, no JSON-LD, no lang attr). Hurts machine reading.
- **LOW** — performance/style nit (DYNAMIC cache, unsafe-eval in CSP for no-script page).

Every defect gets a severity, the curl one-liner that reproduces it, and a fix
pattern (see Phase 5).

### Phase 3 — Capability map (10 min)

For the audited lane, list:
- **Sitemap entries** — `grep -E "<loc>" /tmp/lane-audit/$LANE-sitemap.xml`
- **Child pages / sub-lanes** — e.g. /world/makcikgpt/, /politics/, /world/articles/
- **Caddyfile route** — `grep -E "($LANE|@agent_shells)" /etc/caddy/Caddyfile`
- **Webroot** — `ls /var/www/html/arif/$LANE/` (verify actual served path)
- **Map capability** — does the lane use the federation's map stack? (CSP whitelist, Leaflet, d3-geo, world-atlas)

Build a **map of what's there vs what should be there** per federation identity.
The audit asks: does this lane actually deliver on its name? `/world` named
after the planet should have a map. `/earth` named after the planet should
have live data. `/politics` named after power should have election timelines.

### Phase 4 — Defect ledger (10 min)

Group by fix priority, not by severity alone. Severity = urgency. Priority =
urgency × cost-of-fix × blast radius. A HIGH-severity defect in core content
takes priority over a CRITICAL-severity defect in a footer link.

Format (markdown table):

| Tier | Window | Defects | Effort |
|---|---|---|---|
| 0 — Constitutional | this week | machine-truth files (W1), OG meta (W3), JSON-LD (W4) | 1–2 hours |
| 1 — Ship flagship | this week | world atlas drop-in (W2), theme-color lane-wide (W5) | half-day |
| 2 — Make it the index | this month | wire atlas to surfaces.json/articles (W8), commodity chokepoints layer | 1 week |
| 3 — Agentic parity | this quarter | query_world MCP tool, llms-full.txt with article corpus | ongoing |

The Tier 0/1/2/3 numbering is what makes the deliverable scannable. Don't
write prose; write a numbered roadmap with the fix per tier.

### Phase 5 — Fix recipes

Common patterns:

| Defect | Fix | Time |
|---|---|---|
| `llms.txt` returns HTML | `tee sites/.../public/$LANE/llms.txt <<< "..."` OR add Caddyfile rewrite that 404s for known machine files when missing | 5 min |
| Missing og: meta | Add `<meta property="og:title" content="...">` etc to `<head>`. Required: title, description, image, type | 5 min / page |
| No JSON-LD | Add `<script type="application/ld+json">` block per page. Use Article/NewsArticle for journalism, Organization for hubs, BreadcrumbList for nav | 10 min / page |
| Map absent | Drop in `world-atlas/index.html` (or sibling pattern). Link from hub. Register in surfaces.json + sitemap | half-day |
| DYNAMIC cache | Add `Cache-Control: public, max-age=3600` to Caddyfile for static HTML pages | 2 min |
| unsafe-eval in CSP | Drop `'unsafe-eval'` if no scripts run `eval()`; document why if it does | 2 min |
| 200 with HTML on .json | Either write the real file OR add Caddyfile rule to 404 for known machine-file extensions when missing. **Never** serve HTML at a `.json` URL | 5 min |

**The canary rule:** add a check to `scripts/verify-surfaces.cjs` — any URL
declared as a machine file in surfaces.json must return its declared
content-type, must not contain `<!doctype html>`. Fail-closed. This catches the
class of bug (200-with-wrong-content) that the current gate misses.

### Phase 6 — Deliverable shape

The audit deliverable is a **single markdown file** (no PDF for an audit —
verdicts-first, scannable, in-repo). Sections:

1. **Executive Summary** — verdict (888_HOLD / 999_SEAL / VOID), 1-paragraph
   read on whether the lane is delivery-grade.
2. **Part 1 — Findings** — defect catalog table (Phase 2 output).
3. **Part 2 — Strengths** — what's SEAL-grade. Don't only criticise; the
   user needs to know what to keep.
4. **Part 3 — The deliverable** (if a feature artifact is included, e.g. the
   world atlas) — design decisions, deployment instructions, CSP changes needed.
5. **Part 4 — Upgrade Roadmap** — Tier 0/1/2/3 numbered list (Phase 4 output).
6. **Appendix A — Evidence & Method** — every defect curl-reproducible, Ω₀
   confidence, signing line.

Length: 4–8 pages. Audits are scannable, not exhaustive.

## Bias discipline

The audit must test the user's stated framing at equal rigour. If Arif asks
"is the world lane good?", don't just enumerate what's wrong — enumerate
what's SEAL-grade first. If the lane is mostly fine, say so. If the audit
becomes a complaint list, the audit has failed.

## Cross-link to other skills

- Site-edit flow after audit: `arif-fazil-site-ops` SKILL.md
- Constitutional floors: `/root/AGENTS.md` (F2 truth, F11 audit, F13 sovereign)
- Machine-truth files (sitemap, llms.txt, surfaces.json): see `arif-fazil-site-ops`
  references section
- verify-pages gate: `scripts/verify-pages.sh` — extend with the content-canary
  rule after this audit's defects are fixed

## Reference (proven)

`forge_work/proposals/333-agi/world-audit-2026-08-06/` — full audit output for
the /world lane. Use as a template for /earth, /politics, /gold, etc.