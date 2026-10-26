# Transmission Engine visualization (ExxonMobil IR style)
> Moved verbatim from `arif-fazil-web-ops` on 2026-10-23 (F13 consolidation).

## Transmission Engine visualization (ExxonMobil IR style)

Arif directive (2026-08-08): *"For the transmission engine trail slider, where is graph visualization to model that slider. Use ExxonMobil modeling toolkit if needed. Use all data visualization intelligence skills u have."*

The Layer 5 Transmission Engine (`#engine` section) in `/world/vitals/` now has a **2×2 grid of pure SVG sensitivity visualizations** above the sliders, redrawn live on every slider move. Zero dependencies (no D3/Chart.js — CSP-safe, no CDN). See `references/vitals-transmission-engine-viz-2026-08-08.md` for the full pattern.

| Panel | What it shows | Key fact |
|---|---|---|
| TORNADO | Per-slider ±1σ PAT impact bars | BRENT ±10 → ±RM6.0B (green), JKM ±4 → ±RM2.4B (teal), FX/Gold = 0 |
| WATERFALL | PAT → CFFO → −CAPEX → FCF → −DIV → RETAIN | Dashed connectors between stages |
| SURFACE | PAT isolines on (Brent, JKM) plane | ✕ = current position, 6 isolines |
| SCENARIOS | Bull $110 / Base $85 / Bear $55 PAT paths | 4-quarter trajectories, 3 polylines |

**Full reference:** see `references/vitals-transmission-engine-viz-2026-08-08.md` for the complete pattern (panel-by-panel layout, drawGrid return-value contract, the rename-scope pitfall, validation checklist).

Model: `PAT = 45.4 + (Brent−85)×0.6 + (JKM−14)×0.6` · `CFFO = PAT×1.88` · capex RM46B · div capped 60% PAT floor RM20B.

### Caddyfile reversion hazard — sibling agent/process overwrites your patch (verified 2026-08-10)

**Symptom:** You patch a Caddyfile handler (e.g., `/999/vault` to serve local JSON instead of `reverse_proxy 127.0.0.1:8088`). `caddy validate` passes, `systemctl reload caddy` succeeds, your live probe confirms the fix works. Then minutes later the handler is BACK to the old config and serving 22-second 112KB payloads.

**Root cause:** A sibling agent or build process re-applies the Caddyfile from a different source. Your patch hit the file at `/etc/caddy/Caddyfile`, but the rebuild process regenerates from somewhere else.

**Mitigation steps:**

1. **Always snapshot before patch:** `cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak-$(date +%s)` BEFORE any edit.
2. **Probe AFTER every reload:** `curl -s -o /dev/null -w "%{http_code}|%{size_download}|%{time_total}" https://arif-fazil.com/<path>` — check size and time, not just status. A 22s response with 112KB payload is the smoking gun for a reverted proxy hitting a slow upstream.
3. **Re-verify after 5 minutes:** If you're done with the session, probe again before declaring done. Sibling reverts can happen mid-session.
4. **Check `git -C /root/arif-fazil.com log --oneline -5`:** if a sibling committed Caddyfile changes recently, that's the revert source.
5. **Fix the SOURCE if it's git-tracked:** Check `ls -la /etc/caddy/Caddyfile` and `readlink -f /etc/caddy/Caddyfile`. The real SOT might be in `/root/arif-fazil.com/infra/` or `/root/AAA/infra/`. Edit THAT instead.

**Specific incident (2026-08-10 T2):** `/999/vault` was patched to serve local `vault-data.json` via `file_server`. Worked at first probe (1791 bytes, 82ms). Then sibling re-applied Caddyfile with `rewrite * /api/observatory/v1/snapshot; reverse_proxy 127.0.0.1:8088` — proxied to observatory snapshot which returns 112KB payload and takes 22s. Fix: re-applied the patch, verified with size+time probe.

### /999/ live surfaces — the observability stack (forged 2026-08-10)

The `/999/` constellation is the live-proof surface of the federation. Static HTML shells fetch JSON from Caddy-routed endpoints every 30s:

| Surface | Data source | Caddy wiring |
|---|---|---|
| `/999/health` | arifOS kernel `:8088/health` | `reverse_proxy 127.0.0.1:8088` with `rewrite * /health` |
| `/999/flow` | arifFlow `:7073/health` | `reverse_proxy 127.0.0.1:7073` with `rewrite * /health` (root returns error JSON — MUST rewrite) |
| `/999/vault` | local `vault-data.json` (cron-refreshed) | `file_server` + `root * /var/www/html/arif/999` + `rewrite * /vault-data.json` |
| `/999/verify` | arifOS kernel attestation | `reverse_proxy 127.0.0.1:8088` with `rewrite * /999/verify` |

**F1 rule:** every `/999/*` handler carries `import cors_public` + `header Cache-Control "no-store"` + 405 on POST/PUT/DELETE (read-only by construction — the kernel and vault are never mutated through the public surface).

**Vault freshness cron:** `vault-data-refresh` (cron id `2123bfc0a3bc`) runs `/root/HERMES/scripts/refresh-vault-data.sh` every 5 min — tails `outcomes.jsonl`, extracts `ts/event/actor/tool/session`, writes `vault-data.json` as www-data:www-data 644.

**Progressive enhancement pattern:** the `/999/` index.html and `/words/doctrine/` live-enforcement section both use `fetch('/999/...')` inside `setInterval(..., 30000)`. If the fetch fails, the cell shows `OFFLINE`/`—` — the static content never breaks. This is the "static-first, enhancement-after" pattern that /999/ extends.

### META-rewrite proposal workflow (verified 2026-08-11)

When the user signals a tone/audience change for a canonical page (e.g., "/constitution/ META is cult dialect — rewrite for outsiders"), the workflow is:

1. **Locate the LIVE file first.** Three things matter:
   - The canonical source under git (`public/<route>/index.html` or `src/data/<topic>/<slug>.ts`)
   - The dist/ copy under `sites/<site>/dist/<route>/index.html` (DERIVED, hand_edit=false)
   - The LIVE webroot path — this is where the broken `/words/*` webroot trap catches you (see `/words/* and /work/* are served from /var/www/html` pitfall above)

2. **Patch the source**, not the live webroot. Source goes through git, gets committed, and survives sibling rebuilds.

3. **Copy to live webroot** — both the obvious path AND the redirected-from path. Example for `/constitution/`:
   - `/var/www/html/arif/constitution/index.html` (the old path)
   - `/var/www/html/words/constitution/index.html` (the actual live webroot after 308 redirect)
   - Fix perms: `chown www-data:www-data ... && chmod 644 ...`

4. **Copy to dist/** if you want the change to survive the next build: `cp <source> sites/<site>/dist/<route>/index.html`

5. **Verify live** with both `curl -sL "https://arif-fazil.com/<path>/" | grep <new-marker>` AND `curl -sL -o /dev/null -w "%{url_effective}\n" "https://arif-fazil.com/<path>/"` to follow ALL redirects.

6. **Commit source change** — `git -C /root/arif-fazil.com add ... && git commit -m "fix(<route>): <description>"`. The commit message is the receipt that the change was deliberate, not a sibling accident.

7. **Mention the proposal artifact location** if it was created in `forge_work/proposals/hermes/.../`. Future audits will look there for the rationale — not just "what changed" but "why this change over the alternatives considered."

**Specific incident (2026-08-11):** Constitution META rewrite — caught cult-dialect F1-F13 jargon in title/description/keywords. Proposal at `forge_work/proposals/hermes/constitution-meta-rewrite/v1/META_PROPOSAL.md` with before/after table. Source patch in `public/constitution/index.html`. Dist copy in `dist/constitution/index.html`. Deployed to BOTH `/var/www/html/arif/constitution/index.html` (the obvious path) AND `/var/www/html/words/constitution/index.html` (the actual live webroot). Committed as `d427ef2`. Verified live: `https://arif-fazil.com/constitution/` → 308 → `/words/constitution/` → 200 with new META.

**Common pitfall:** Patching only the source (`public/`) without copying to dist/ AND live webroot. The source change survives in git but the LIVE site still serves the old META until the next `make deploy` (which copies public → dist → live via rsync). For a fast META fix, copy directly to both dist/ and live to avoid waiting for the next build.

- **DEEP ARCHIVE EXTRACTION — when user says "deep archive" / "previous design" / "aku x mau ni" / "what was deployed before" / "restore the old one" / "I hate it / ugly for human", extract the archived design from git AND filesystem backups and serve it locally for visual comparison (verified 2026-08-11 on `/world/makcikgpt/`).** DESIGN DRIFT INVESTIGATION above lists the archives; this pitfall completes the workflow — once you find the old commit, you need to SEE the old design to decide what to restore.

  **Why this matters:** A git log line tells you a file existed in commit X. It does NOT tell you what that file looked like, whether it had a hero, whether the chrome matched. To make a restoration decision you need visual proof of the old design, side-by-side with the current one. The only way to get that is to extract the file and render it.

  **Step 1 — Search ALL archive paths, not just git.** The richest archived designs often live OUTSIDE git history. Search these paths in order, biggest first (size is a signal — 105B = stub, >10KB = real content):

  ```bash
  # Path 1: Recent deploy snapshots (last 7 days)
  find /root/forge_work/deployments/arif-fazil.com/2026*/previous/ \
    -name "index.html" -size +2k | xargs -I {} sh -c \
    'echo "{}: $(stat -c%s {})B"' | sort -t: -k2 -nr

  # Path 2: Older backup archives (FORGOT — found rich 19,638B Primer Dark here on 2026-08-11!)
  find /root/backups/forge_work-archive-2026-07/deployments/ -name "index.html" \
    -size +2k | xargs -I {} sh -c 'echo "{}: $(stat -c%s {})B"' | sort -t: -k2 -nr

  # Path 3: Site-archival backups (e.g. /root/_archive/2026-08-04/backups/)
  find /root/_archive/ -name "index.html" -size +2k -path "*makcikgpt*" | \
    xargs -I {} sh -c 'echo "{}: $(stat -c%s {})B"' | sort -t: -k2 -nr

  # Path 4: Quarantined versions
  find /var/arifos/quarantine/ -name "index.html" -size +2k | \
    xargs -I {} sh -c 'echo "{}: $(stat -c%s {})B"' | sort -t: -k2 -nr

  # Path 5: Git history (last resort — only if filesystem archives fail)
  cd /root/arif-fazil.com && \
    git log --all --oneline -- "**/<path-or-glob>" | head -20
  ```

  **Size tells the story:** 105B = stub (the placeholder HTML that Caddy falls back to). 14KB = flat agent-friendly listing. 19KB+ = rich human-designed chrome. The `+2k` filter excludes 105-byte stubs so you only see real designs.

  **Step 2 — Extract candidate files verbatim.**
  ```bash
  mkdir -p /tmp/<archive-name>
  for c in <commit1> <commit2> <commit3>; do
      git show "$c:public/makcikgpt-md/index.html"   > /tmp/<archive-name>/$c-md.html     2>/dev/null || true
      git show "$c:sites/arif-fazil.com/makcikgpt/index.html" > /tmp/<archive-name>/$c-old.html 2>/dev/null || true
      git show "$c:sites/arif-fazil.com/public/makcikgpt-md/index.html" > /tmp/<archive-name>/$c-public.html 2>/dev/null || true
  done
  ls -la /tmp/<archive-name>/      # confirm which paths existed per commit
  ```

  **Step 3 — Serve locally on a temp port.**
  ```bash
  cd /tmp/<archive-name> && python3 -m http.server 8765 &
  sleep 2
  curl -sf -o /dev/null -w "HTTP:%{http_code} SIZE:%{size_download}\n" http://127.0.0.1:8765/<file>.html
  ```

  **Step 4 — Screenshot each version with `browser_navigate` + `browser_vision`.** Save to `/tmp/<archive-name>/screenshot-<commit>.png` so they survive eviction (see SCREENSHOT PROOF PROTOCOL above).

  **Step 5 — Build the side-by-side comparison table for the user.** Format: commit · path · hero · chrome · stats · footer · vibe. Show the actual screenshots via `MEDIA:/tmp/<archive-name>/screenshot-<commit>.png`. Let the user pick which version to restore.

  **Step 6 — Don't auto-restore.** Show all candidates + current. Wait for the user's choice. Restoration is `cp <chosen> /var/www/html/arif/<live-path>/` + chown www-data + chmod 644 + curl verify + browser_navigate. The `git show` extraction is READ-ONLY until the user picks.

  **Real example (this session, `/world/makcikgpt/`):** Found 3-stage regression — `696f734` (chat-interface persona, warm gold/brown) → `767596c` (Primer Dark marketing hero, RED/BLUE/YELLOW, hero+stats+series cards) → HEAD (flat agentic list, "Source of truth: src/data/essays.json. Rendered by scripts/..."). Extracted all three via `git show`, served each from a temp HTTP server, screenshotted each, sent side-by-side. User picked the Primer Dark version (post-audit `767596c`) as the restoration target. Full timeline in `references/makcikgpt-design-regression-2026-08-11.md`.

  **Pattern class — "agentic web optimization" regression.** Each stage of this regression replaced human-friendly chrome (hero, persona, pull-quotes, colored cards) with agent-friendly metadata (canonical landing path, source-of-truth file paths, generator script names, "WHERE AM I? / WHY CARE? / WHAT NEXT?" info boxes). The user's pain is the institutional chrome leaking to human readers. If a regeneration step removes human voice, that is a regression regardless of "improvements" to AI discoverability.

### Caddy wildcard redirect pitfall — `@static_dirs` and `handle_path` shadow custom regex handlers (verified 2026-08-11)

**Symptom:** You add a custom `path_regexp` handler with a wildcard like `@em_redir path_regexp ^/economics/makcikgpt/(.+)$` and `handle @em_redir { redir /world/makcikgpt/{http.regexp.em_redir.1} 301 }`. `caddy validate` passes, `systemctl reload caddy` succeeds. But probes still return 404. You try:
- `path` matcher with `*` wildcard
- `handle_path` with `rewrite` + `redir`
- `handle` with `uri strip_prefix` + `{uri}` placeholder
- Named captures `{re.slug}`, `{http.regexp.*.1}`
- Header `Location` + `respond "" 301`

All return 404 or empty body. None fire.

**Root cause:** `handle` directives in Caddy are tried in **source order**, BUT once a `@static_dirs path /economics/*` handler exists later in the file, AND a `handle_path /economics/*` exists between your handle and the static_dirs handler, the request gets caught by `handle_path` first — which has `@not_makcikgpt not path /makcikgpt /makcikgpt/*` BUT `not` on a path matcher doesn't exclude sub-paths of `/makcikgpt/*` reliably in all Caddy versions. The result: your wildcard handler is shadowed.

**The actual fix (the one that works):** Put the wildcard logic INSIDE the existing `handle @static_dirs { ... }` block OR use a top-level `redir` directive with the `path` matcher that runs BEFORE all `handle` blocks. The Caddy processing order is:

```
1. `redir` directives at top level of the site block (run FIRST, before any handle)
2. `handle` directives in source order
3. `handle_path` directives
4. `handle @static_dirs` (or any other named matcher handler)
```

So `redir` at top level is the only thing that ALWAYS beats `handle @static_dirs`. For dynamic captures (article slug), you need:

```caddyfile
# 2026-08-11: Wildcard legacy MakcikGPT redirects — TOP-LEVEL bare redir.
# Bare redir runs BEFORE all handle blocks including @static_dirs.
# For simple fixed targets, this is the ONLY reliable pattern:
redir /economics/makcikgpt/* /world/makcikgpt{uri} 301
```

BUT `{uri}` includes the matched prefix, so for `/economics/makcikgpt/cerita-makcik` the redirect becomes `/world/makcikgpt/economics/makcikgpt/cerita-makcik` (wrong).

**The actual working pattern:** put the regex redirect INSIDE `handle @static_dirs { ... }` block:

```caddyfile
# Inside handle @static_dirs { try_files ... =404; file_server }
# Add at the TOP of the block, BEFORE try_files:
@legacy_makcikgpt path_regexp ^/(economics|wealth)/makcikgpt/(.+)$
rewrite @legacy_makcikgpt /world/makcikgpt/{http.regexp.*.2} 301
```

Or simpler: use Cloudflare page rules for legacy URL redirects if the Caddy regex handlers consistently misfire. Cloudflare rules run at the edge BEFORE Caddy, so they're immune to handler ordering issues.

**Lesson learned the hard way (2026-08-11):** spent 6 iterations on this. The pattern is: **when `path_regexp` handlers in a site block don't fire, it's because another handler (likely `handle_path` or `@static_dirs`) with a broader path matcher is catching the request first.** The reliable fix is one of:

1. Move the redirect logic INSIDE the catching handler (at the top, before try_files).
2. Use Cloudflare edge rules (immune to Caddy handler ordering).
3. Restructure the Caddyfile so the wildcard handler is in a separate vhost (rare, heavy).

NEVER assume a `handle` block will fire just because it's defined earlier in the Caddyfile. Always verify with a live probe and check the actual response body — `caddy validate` passing does NOT mean the handler fires.

### Bare landing path pitfall — `handle /path/*` does NOT match bare `/path/` (verified 2026-08-11)

**Symptom:** You land on `/world/makcikgpt/` (no slug, bare landing). The page renders but is essentially blank — a 1043-byte stub with `<h1>MakcikGPT Landing</h1>` and no CSS. The 24 articles on the corpus work fine; only the bare landing is broken. External probe finds it and reports "empty white".

**Root cause — five patterns that ALL require content after the prefix:**

```caddyfile
# 1. Bot handler — pattern requires at least one char after *
@ai-bot_world {
    path /world/makcikgpt/*  ← * requires content; bare path = NO MATCH
}
# 2. No-JS handler — regex requires at least 1 char
@makcikgpt_nojs path_regexp ^/world/makcikgpt/(.+)$  ← (.+) requires content
# 3. Trailing-slash handler — requires slug + trailing slash
@mk_trail path_regexp ^/world/makcikgpt/([^/]+)/$  ← [^/]+ requires content
# 4. Wildcard handle — * does not match empty path
handle /world/makcikgpt/* {  ← * requires content
# 5. Even the @static_dirs handler with /world/makcikgpt/* has the same constraint
```

For `/world/makcikgpt/` (bare, no slug after), all five handlers MISS. The request falls through to the SPA fallback stub.

**Fix — explicit bare-path handlers placed BEFORE the wildcard:**

```caddyfile
# Bare landing paths need their OWN handle block — * doesn't match empty.
# Place BEFORE handle /world/makcikgpt/* so first-match-wins applies.
handle /world/makcikgpt {
    uri strip_prefix /world/makcikgpt
    root * /var/www/html/arif/makcikgpt-md
    header Cache-Control "public, max-age=300"
    try_files /index.html =404
    file_server
}
handle /world/makcikgpt/ {
    uri strip_prefix /world/makcikgpt
    root * /var/www/html/arif/makcikgpt-md
    header Cache-Control "public, max-age=300"
    try_files /index.html =404
    file_server
}
# THEN the wildcard for slugs
handle /world/makcikgpt/* { ... }
```

**Detection recipe — sweep for the same pattern on other hubs:**

```bash
# For each hub landing, check if bare /world/<hub>/ returns real content or shell
for hub in vitals economics makcikgpt politics; do
  size=$(curl -s -o /dev/null -w "%{size_download}" "https://arif-fazil.com/world/$hub/")
  echo "/world/$hub/ → ${size}B $([ $size -lt 5000 ] && echo '⚠️ SUSPECT shell' || echo '✓ real content')"
done
# Repeat for /words/<hub>/, /propa/, /malaysia/, etc.
```

**Lesson:** When adding a new hub to the constellation, you need THREE handler blocks, not one:
1. `handle /hub` — bare landing
2. `handle /hub/` — bare landing with trailing slash
3. `handle /hub/*` — slugs (does NOT match the bare landing)

### Caddy insertion location trap — Python patch can target wrong handle block (verified 2026-08-11)

**Symptom:** Your `python3 << PY` script replaces a snippet in the Caddyfile correctly (e.g., `@api_organs_arifos` block). Then you do `c.replace(target, insert)` to add a new handle block right after the matched snippet. **But if your `target` anchor string is inside another `handle` block, your insertion goes INSIDE that block too** — and everything breaks (all routes start returning 404 or 500).

**Concrete incident (2026-08-11):** Replaced `import cors_public` (the @api_organs_arifos handler marker) with the @wm_legacy/@em_legacy handle blocks + `import cors_public`. But `import cors_public` appears 56 times in the Caddyfile — the FIRST occurrence was inside `@api_organs_arifos`, so my new handle blocks landed INSIDE that block. Result: `/api/organs/arifos/health` returned 404 AND `/wealth/makcikgpt/<slug>` returned 404 because the whole handler chain got poisoned.

**Mitigation:**

1. **Always use UNIQUE multi-line anchors.** Single-line targets like `import cors_public` will match the first occurrence — usually not where you want to insert.
2. **Verify the insertion point with `sed -n 'N,N+10p'` BEFORE the patch** — read the surrounding lines to confirm you're inside the right scope.
3. **Reload Caddy IMMEDIATELY after the patch and probe ALL known routes** — if any previously-working route breaks, the insertion went into the wrong block. Revert and re-target.
4. **Keep Caddy backups BEFORE every patch:** `cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak-$(date +%s)`.

**Recovery if it breaks:** `cp /etc/caddy/Caddyfile.bak-<timestamp> /etc/caddy/Caddyfile && caddy validate && systemctl reload caddy && verify with curl`.

### Dark subdomain + SPA catch-all pattern (verified 2026-08-11)

**Two related DRIFTs from external probe:**

**DRIFT #1 — Empty webroot + missing root handler:**
```caddyfile
wealth.arif-fazil.com {
    root * /var/www/html/wealth
    # ... other handlers for /mcp, /api, etc.
}
```
If `/var/www/html/wealth/` has no `index.html`, the subdomain returns 404 on `/` even though `/api/...` works. Fix: either add `index.html` (minimal landing), or `redir / https://arif-fazil.com/wealth/<reason> 308` to redirect to the canonical surface.

**DRIFT #4 — SPA catch-all serving shell on garbage routes:**
```caddyfile
geox.arif-fazil.com {
    root * /var/www/html/geox
    handle /mcp { reverse_proxy ... }
    # ... other handlers
    # NO final handle that fail-closes
}
```
Result: any path not caught by the named handlers falls through to `file_server` on the root dir, which serves `index.html` (the SPA shell) on every garbage route. External probe found `geox.arif-fazil.com/garbage-route-8f3k2` → HTTP 200 with shell content.

**Fix:** Add explicit fail-closed at the END of the vhost block:
```caddyfile
handle {
    respond "404 Not Found" 404
}
```

This catches all unhandled routes and returns honest 404 instead of serving the SPA shell. Same fix applies to any subdomain with mixed static + reverse_proxy routing.

### External witness probe pattern (verified 2026-08-11)

When auditing the live site, run an **external probe suite** with raw status codes + deviation math, NOT just "does curl return 200". The 10-probe matrix that caught the 4 DRIFTs:

| # | Probe | Pass criterion |
|---|---|---|
| 1 | All hub surfaces (`/`, `/words/`, `/earth/`, `/world/`, `/work/`, `/999/`, `/000/`) return 200 with sane sizes | HTTP 200 + 1KB < size < 100KB |
| 2 | `/000/` and `/999/` return real static docs (not SPA shells) | `size > 10KB` AND distinct `<title>` |
| 3 | `/oil/`, `/gas/`, `/gold/` JSON-LD prices within ±2% of live market | `\|sealed - live\| / live < 0.02` |
| 4 | Legacy redirects (`/economics/makcikgpt/*`, `/wealth/makcikgpt/*`) → 301 to canonical | `curl -sI <path> \| grep -i location` shows canonical URL |
| 5 | Unknown routes → real 404 (not SPA shell) | `curl -s <random-path> \| head` does NOT show SPA content |
| 6 | `feed.xml` article count matches sitemap | `grep -c '<item>' feed.xml == grep -c '<loc>' sitemap.xml` |
| 7 | `llms.txt` organs list matches `soul.json` | both enumerate same 5 organs |
| 8 | `/api/public-state` signed + fresh (timestamp < 5 min old) | `signature_state: SIGNED` AND `ts_utc` recent |
| 9 | MCP `POST /mcp initialize` returns valid JSON-RPC result | HTTP 200 + `result.protocolVersion` populated |
| 10 | Canonical redirects work (`/federation` → `/doctrine`) | 301 with correct Location header |

Verdict format per probe: `🟢 PASS` or `🔴 DRIFT` with specific failure detail. Aggregate verdict at the top: "6 PASS · 4 DRIFT — seal is NOT clean".

This pattern catches things internal agent audits miss because:
- It measures response **size** (112KB instead of expected 1.8KB = proxy regression)
- It measures response **time** (22s instead of 100ms = shadow handler firing)
- It probes from outside (catches Cloudflare edge cache, DNS routing)
- It includes deviation math for stale data (`/oil/` sealed 84.53 vs live 87.18 = 3.04%)

### UA-differential debugging — same path, different responses per UA (verified 2026-08-11)

**Symptom:** You curl `/world/makcikgpt/` → 200 / 15KB with the real landing page. Arif's browser hits the same URL → 404 (empty body). Both responses show `cf-cache-status: DYNAMIC` so Cloudflare isn't caching differently. Live page works for some clients, broken for others.

**This is the worst kind of bug** — your probes say "fine", user's reality says "broken", and there's no obvious explanation. Run the differential matrix BEFORE guessing.

**The 7-UA differential probe:**

```bash
URL="https://arif-fazil.com/<suspect-path>"
for ua_label in "CURL_DEFAULT" "MOZILLA_MAC" "MOZILLA_WIN" "MOZILLA_LINUX" "IPHONE_SAFARI" "EMPTY_UA" "PYTHON_URLLIB"; do
  case $ua_label in
    CURL_DEFAULT)     ua="curl/8.14.1" ;;
    MOZILLA_MAC)      ua="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" ;;
    MOZILLA_WIN)      ua="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" ;;
    MOZILLA_LINUX)    ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36" ;;
    IPHONE_SAFARI)    ua="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" ;;
    EMPTY_UA)         ua="" ;;
    PYTHON_URLLIB)    ua="Python-urllib/3.10" ;;
  esac
  result=$(curl -sI "$URL" -H "User-Agent: $ua" -H "Accept: text/html" 2>/dev/null | grep -iE "^HTTP|content-length" | head -2 | tr '\n' ' ')
  printf "  %-15s %s\n" "$ua_label" "$result"
done
```

**Pattern recognition from this matrix:**

| UA pattern | Likely cause |
|---|---|
| All UAs → 200 | Genuine edge cache miss; user problem is browser-side |
| Only `curl/<ver>` → 200, all others → 404 | **Caddy handler order** — `@ai-bot-world` matcher shadows other handlers; handler chain terminates at the 404-producing block for non-bot UAs |
| Only `Mozilla/Chrome/Safari` → 200, `curl` → 404 | Cloudflare Super Bot Fight Mode blocking perceived bots |
| Only `Mozilla` with `Accept: text/html` → 404 | **`@makcikgpt_nojs` matcher** with `not header_regexp Accept text/html` — request WITHOUT that Accept is treated as a no-JS client and routed to a static path that doesn't exist for bare landings |
| All UAs → 404 | Genuine missing file or broken handler for everyone |

**The 2026-08-11 incident:** `curl/8.14.1` → 200 / 15KB; all other UAs → 404 / 0 bytes. `cf-cache-status: DYNAMIC` on both. Cause: a `handle /world/makcikgpt/` block at line 936 rewrote to `/spa-shell.html` (file doesn't exist on disk) → Caddy returns 404 for everyone. But curl UA matched `@ai-bot-world` (the matcher includes `curl` in its UA regex) AND fell through to a different handler that served real content. The two UAs took completely different paths through the handler chain.

**Diagnostic next steps after the matrix:**

1. **Identify which handler is producing the 404.** `caddy adapt --config /etc/caddy/Caddyfile --pretty > /tmp/caddy.json` then `grep -B2 -A20 '/suspect/path' /tmp/caddy.json` to see the actual handler chain. Walk the JSON to find which `try_files` or `file_server` is the terminal handler.
2. **Check Cloudflare trace** — `curl -s "https://arif-fazil.com/cdn-cgi/trace"` to see colo, IP, and confirm the request reaches origin. If `cf-cache-status: DYNAMIC` and `cf-ray` is present, Cloudflare passed through to origin — the divergence IS in Caddy.
3. **Check browser cache on the user's side** — if all probes return 200 from server but user sees 404, the user has stale browser cache. Tell them to hard-refresh (`Cmd+Shift+R` / `Ctrl+Shift+R`) and clear site data for the domain.
4. **Test direct-to-origin** — `curl -sk "https://127.0.0.1/<path>" -H "Host: arif-fazil.com" -H "User-Agent: Mozilla..."` to bypass Cloudflare entirely. If this returns 200, Cloudflare is the divergence source; if 404, Caddy is.
5. **Check sibling agent activity** — `git -C /root/arif-fazil.com log --oneline -10 -- sites/arif-fazil.com/public/` and `journalctl -u caddy --no-pager -n 30` for recent changes that might have reverted your work.

**Lesson:** Never declare "fixed" after a single curl probe. The matrix above is 30 seconds of work and catches UA-specific routing bugs that single-probe testing misses entirely. Add it to your standard post-deploy verification for any landing-page change.

### Critical JS scoping pitfall (verified 2026-08-08)

`drawGrid` returns its inner `<g>` SVG group. Callers store it as `const root = drawGrid(...)`. Then `root.appendChild(...)` adds chart elements. **BUT `drawGrid` also uses `g.appendChild(...)` internally to attach grid lines/text to the same group.**

The bug: a blanket `.replace('g.appendChild', 'root.appendChild')` across the entire viz block also rewrote `drawGrid`'s internal calls → `root is not defined` (root is only in the outer scope).

**Rule:** when renaming a variable across a JS block, scope the replacement to function boundaries:
```python
# WRONG — blanket replace breaks inner function
block = block.replace('g.appendChild(', 'root.appendChild(')

# RIGHT — scope to drawGrid only
start = html.find('function drawGrid(')
end = html.find('\nfunction drawTornado(', start)
drawGrid_func = html[start:end]
drawGrid_func = drawGrid_func.replace('root.appendChild(', 'g.appendChild(')
# outer scope stays root.appendChild
```

Then validate: `node --check <script_content>`.

