---
id: FORGE-agentic-web-builder
name: forge-agentic-web-builder
version: 1.2.0-2026.09.13
description: "Use when building, deploying, auditing, or repairing arif-fazil.com constellation and federation agentic web apps."
owner: FORGE (000Ω)
risk_tier: T2
floor_scope: [F1, F2, F4, F11]
autonomy_tier: ANNOUNCE
forged_from: INCIDENT-2026-07-23 + MISSIONS-ZEN-2026-07-30
capability_tier: fed-agent-subagent
ecology_state: WARM
---
# 🌐 FORGE — Agentic Web Builder

> One night, three identical failures: `organ_proxy.py` (code), `999/index.html`
> (doctrine), `static/wealth.html` (renderer output) — all lived ONLY in the
> deployed tree, all destroyed or nearly destroyed by deploys. This skill is
> the metabolized scar. **Nothing generated lives only in the deployed tree.**
>
> **2026-07-30:** Stop inventory cosplay. Humans → `/missions`. Agents →
> `web_zen.py doctor` before inventing a new deploy path.

## Fabric (2026-09-13)

Load **`AGI-agentic-web-delivery`** with this skill.
SOT: `/root/arif-fazil.com/docs/agentic-web/README.md`
Canonical source is **`/root/arif-fazil.com`**, not `/root/arif-sites`.
Caddy reload is **T3 HOLD** unless Arif names it. `make deploy` includes reload — do not run the whole target.
Oil/gas doctor 500 is missing `/root/venv/bin/python3` (gold uses WEALTH venv + `PYTHON_PATH`). Units active ≠ ticker 200.
`web_zen.py audit` is documented here and **not in the CLI**. Use doctor + Playwright.
`SITE_CONSTITUTION.md` / `SITE_IDENTITY.md` are cited below and **do not exist** (public 404). Use `docs/agentic-web/` instead.

## The One Law

```
VERSION CONTROL FIRST. LIVE TREE SECOND.
If a file must exist on a public site, it must exist in git first.
rsync --delete is an executioner — anything not in source is sentenced.
Capability ≠ authority. Ephemeral tools die. Permission stays with arifOS/Arif.
Caddy reload ≠ deploy. Public /a2a stays unmatched.
```

---

## OP 0 — DOCTOR (always first · anti-chaos)

```bash
python3 /root/arif-fazil.com/scripts/web-zen/web_zen.py doctor
```

| Mode | Band | Purpose |
|------|------|---------|
| `sense` | GREEN | source/live, Caddy missions routes, commodity :3456–3458 |
| `verify` | GREEN | content-truth crawl (SPA checks JS bundle, not shell HTML only) |
| `orphan` | YELLOW | dry-run `rsync --delete` — fail closed if deletes listed |
| `ephemeral` | GREEN | generate → test → destroy disposable script (no secrets) |
| `caddy-reload-hint` | ORANGE | systemd reload often fails NAMESPACE — use in-process `caddy reload` |

README: `/root/arif-fazil.com/scripts/web-zen/README.md`  
Human cockpit: `https://arif-fazil.com/missions` · Machine: `/missions.json`  
MCP: `forge_web_zen(mode=doctor)` · Kernel: `arif_route(mission_id=…)`  
Caddy reload: `systemctl reload caddy` (PrivateTmp=false fixed 2026-07-30)

### Known failure → fix (do not re-diagnose from zero)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `/missions` 404 | not in Caddy `@spa_routes` | add `/missions*`; `caddy validate`; `/usr/bin/caddy reload --config /etc/caddy/Caddyfile --force` |
| `/missions.json` 404 | not in `@root_static` | add path; reload as above |
| VITALS proxies UNAVAILABLE | gold/oil/gas API down | units may already be active; oil/gas spawn `/root/venv/bin/python3` ENOENT — set `PYTHON_PATH` like gold (WEALTH venv). Not API keys. |
| `systemctl reload caddy` fail NAMESPACE | host /tmp mount bug | in-process caddy reload (above) |
| Doctor fails SPA markers | checking HTML shell only | web_zen reads live `/assets/index-*.js` |

---

## OP 1 — DEPLOY (canonical path)

Canonical source: `/root/arif-sites/sites/` → built/synced to `/var/www/html/<site>/`
Canonical script: `/var/www/html/deploy-vps.sh` (mirrored in repo root)

**Pre-deploy checklist (mandatory):**
1. `cp -a /var/www/html /root/backups/www-html-$(date +%Y%m%d)-pre-<reason>` — snapshot BEFORE mutation. Tonight this snapshot saved two restores.
2. **Orphan detection** — before any `rsync --delete`, list what will die:
   ```bash
   rsync -avzn --delete SRC/ DEST/ | grep '^deleting' | head -50
   ```
   Any file you don't recognize = HOLD. Either seed it into source or quarantine it.
3. Verify the deploy script covers the site you're touching (oil/gas/gold/mcp/well were missing until 2026-07-23 — check `grep <site> deploy-vps.sh`).
4. Post-deploy: run OP 2 audit on affected hosts. "Deployed" ≠ "live". Verified = live.

**Host → source map:**
| Host | Live root | Source |
|---|---|---|
| arif-fazil.com | /var/www/html/arif | sites/arif-fazil.com (build → dist → rsync) |
| aaa | /var/www/html/aaa | sites/aaa.arif-fazil.com |
| arifos / geox / wealth | /var/www/html/<organ> | sites/<organ>.arif-fazil.com |
| mcp | /var/www/html/mcp | sites/mcp.arif-fazil.com (rsync, no --delete — .well-known live assets) |
| well | /var/www/html/well | sites/well.arif-fazil.com (llms.txt only) |
| /oil /gas /gold (apex paths) | /var/www/html/{oil,gas,gold} | dist/{oil,gas,gold} — exclude live api/ + vendor/ |

### Agentic Discovery Deployment (ARD v0.91 / Lighthouse 13.5)

When deploying or auditing agentic discovery files, all 4 Lighthouse vectors must pass. See `references/agentic-discovery-deployment.md` for the full spec, Caddy patterns, and verification procedure.

**Quick checklist (every organ deploy):**
1. `/.well-known/ard.json` — ARD v0.91 manifest with domain-anchored URNs and representativeQueries.
2. `/.well-known/ai-catalog.json` — identical content, v0.9 fallback for Lighthouse.
3. `robots.txt` — `Agentmap:` directives pointing to both manifests.
4. HTTP `Link` header — `rel="ard"` and `rel="ai-catalog"` via Caddy `tls_origin` snippet.
5. HTML `<link>` tags in `<head>` — `rel="ard"` and `rel="ai-catalog"`.
6. `Cache-Control: no-cache` on `robots.txt` handler — prevents Cloudflare stale cache (see pitfall below).

**After deploy, verify origin directly (bypass Cloudflare):**
```bash
curl -sI --resolve "DOMAIN:443:72.62.71.199" https://DOMAIN/robots.txt | grep -i "agentmap\|cache-control"
curl -s --resolve "DOMAIN:443:72.62.71.199" https://DOMAIN/.well-known/ard.json | head -5
```

---

## OP 2 — AUDIT (full-crawl methodology)

74-URL method, proven 2026-07-23. Evidence dir pattern:
`/root/A-FORGE/forge_work/<date>/site-audit/`

1. **Enumerate hosts:** `grep -oE "^[a-z0-9.-]+\.arif-fazil\.com \{" /etc/caddy/Caddyfile | sort -u`
2. **Enumerate pages:** sitemap.xml `<loc>` entries + Caddy `@spa_routes` path list + every `handle` target + static handles (`@root_static`).
3. **Probe each:** `curl -s -o body -w "%{http_code}|%{size_download}" -L url`. 0-byte 404 = catch-all respond; 17-byte 404 = explicit respond directive. Both are failures for content pages.
4. **Content truth, not status codes** — a 200 with wrong content is a lie (F2):
   - /000 → BLAKE3 identity hash present
   - /999 → §8 Audit Path + grandfather rule
   - /economics → F2 bands + VOID tiles (patched renderer, not SPA shell)
   - dashboards → price/commodity markers
   - /data/wealth/latest.json → fresh date
5. **Dual-lane bot surfaces** (makcikgpt): test with bot UA (`GPTBot/1.0`, `curl/x`) AND browser UA (`Mozilla` + `Accept: text/html`). Bot lane serves .md/.html from `makcikgpt-md/`; browser lane gets SPA. Both must 200.
6. **404 triage:** file missing from live tree? handler missing from Caddy? matcher gap (`@root_static` list)? file never built (pre-existing gap — label it, don't fake-fix)?

---

## OP 3 — REPAIR (source/live convergence)

The drift detector for deployed content:

```bash
diff -rq <snapshot-or-source>/ <live>/ | grep "^Only in"
```

- **"Only in live"** = orphan. Seed into `public/` (survives build) → commit → redeploy. Never hand-edit live-only.
- **"Only in source"** = deploy gap. Check deploy script covers it.
- **Dual-copy divergence** (e.g. `999/index.html` vs `public/999/index.html`): converge to one canonical, sync, commit. Both copies must carry both truths.
- **Nested-dir restore error** (`cp -a src dst` when dst exists → `dst/src`): verify with `ls dst` after every restore; flatten with `cp -a dst/src/. dst/` then `mv dst/src quarantine/`.
- **Never `rm -rf`** — F1 tripwire will (correctly) block. Quarantine: `mkdir -p /root/backups/quarantine-<date> && mv target quarantine-<date>/`.

**Spawn coding agent for system-path mutations, do not retry from main agent.** The `patch` and `write_file` tools refuse paths under `/etc/`, `/var/`, and other root-owned trees — this is a hard refusal, not a recoverable error. When the OP 3 recipe requires editing `/etc/caddy/vhosts/*.conf`, `/etc/caddy/Caddyfile`, or other system files needing sudo, **delegate to a coding subagent in the first call**, not the third. Each retry from the main agent burns the user's tokens without making progress. Pass the exact diff template and the reload command (e.g. `sudo caddy validate --config /etc/caddy/Caddyfile && sudo systemctl reload caddy`) inside the delegation context. Verify with `curl` from the main agent after the subagent reports done.

**Never declare a fix failed from `curl -sI` alone.** HTTP/2 framing often omits `Content-Length` on responses that DO carry a full body; `curl -sI` reports whatever fell into the small HEAD buffer and may show 20 bytes for a working 16 KB article. Always verify with a full body GET and a content signature (`curl -s URL -o /tmp/x && wc -c /tmp/x && grep -c <distinctive-phrase> /tmp/x`) before dispatching a debug subagent. A 200 with zero signature matches is the real silent failure mode; a low or zero `content-length` from HEAD alone is not.

- **Caddy edits:** python exact-string patch → `caddy validate` → `systemctl reload` → verify affected URLs. Backup exists at `/etc/caddy/Caddyfile.bak.*`. Reload is T3-class: only under sovereign directive or incident repair with immediate verification.

### Stale-slug / URL drift recovery (Caddy 301 redirect)

When a deployed page has a wrong slug — wrong URL returns 200 but renders the SPA fallback ("Artikel Tidak Dijumpai"), right URL serves the real article — the surgical fix is a Caddy 301 redirect in `/etc/caddy/vhosts/arif-fazil.com.conf`. NOT a code revert. NOT a rebuild hoping the SPA falls back differently.

Template (place near the existing legacy-redirect blocks):
```
# <date>: Stale-slug typo — <stale-slug> → <correct-slug>
@<tag> path /world/makcikgpt/<stale-slug>
handle @<tag> {
	header Location https://arif-fazil.com/world/makcikgpt/<correct-slug>
	respond "" 301
}
```

Sequence: python `str.replace()` patch → `caddy validate --config /etc/caddy/Caddyfile` → `caddy reload --config /etc/caddy/Caddyfile` → `curl -sI` on the stale URL (must return `HTTP/2 301` with the right Location header) AND on the correct URL (must return `HTTP/2 200` with article signature present, not just SPA fallback).

The user clicks the wrong URL → 301 → working URL → article. ~3 minutes total. Compare to: rebuild + rsync with a fresh slug = ~30 minutes plus the risk of breaking other articles.

Verify by content, not by status code: `curl -s <correct-url> | grep -c <distinctive-word-from-the-article>`. A 200 with zero signature matches = the page is still serving the SPA fallback. Status-200 + content-wrong is the silent failure mode this recipe exists to catch.

### Cloudflare cache stale after deploy

New files deployed to origin (robots.txt, .well-known/*) may be served stale by Cloudflare for up to the TTL (typically 4 hours). Verify via direct origin access:

```bash
curl -s --resolve "DOMAIN:443:72.62.71.199" https://DOMAIN/robots.txt | grep -i agentmap
```

If origin is correct but live site is stale:
1. Add `Cache-Control: no-cache, no-store, must-revalidate` to the Caddy handler for that file.
2. Reload Caddy.
3. Cloudflare will revalidate on next fetch. If instant purge is needed, use the Cloudflare dashboard (API token may lack `Cache Purge` permission).

**Never hand-edit live tree to fix a cache issue.** Fix the Caddy config, not the served content.

---

## OP 4 — SEAL (evidence discipline)

1. Prefer `web_zen.py doctor --json` receipt under `forge_work/<date>/web-zen/`.
2. Crawl data (`results.tsv`), URL list, truth-check output → `forge_work/<date>/site-audit/AUDIT-REPORT.md`.
3. Source commits BEFORE seal (seal references commit hashes, not intentions).
4. `forge_vault(mode="seal")` with: scope, pass count, content-truth table, gaps closed, commits, skill.
5. Session-end: one seal, not two. F4.

## OP 6 — AUDIT · SITE CONSTITUTION LANES (SEAL 2026-08-09)

```bash
python3 /root/arif-fazil.com/scripts/web-zen/web_zen.py audit
```

Four lanes — **Lane A** = existing doctor/verify (technical). **Lane B** = navigation
(crawl; canon/trust/observatory/organs reachable ≤3 clicks from landing → else FAIL_NAVIGATION;
SPA-aware: routes live in JS bundle). **Lane C** = visual surface (h1/nav/content mass →
FAIL_VISUAL). **Lane D** = attention cost (human markers vs jargon → HALT if a page can't
answer What/Why/Care; redirect stubs score their destination).

**Mandatory read before ANY mutation of the constellation:**
- `/root/arif-fazil.com/SITE_CONSTITUTION.md` — RULE 1–6 (human understanding > protocol
  exposure; navigation clarity > feature growth; visual coherence > cleverness; agent
  surfaces secondary; every page answers What/Why/Care; no new surface before auditing).
- `/root/arif-fazil.com/SITE_IDENTITY.md` — what is sacred (the human, the motive, the
  motto, the system line, the visual identity, the canon, MakcikGPT, the organs).
- Both also live at `https://arif-fazil.com/SITE_CONSTITUTION.md` and
  `https://arif-fazil.com/SITE_IDENTITY.md` (public/ copies, served to agents).

Deploy gate: `deploy-vps.sh` runs `web_zen.py audit` after truth verification.
`human_clarity: required: true` is a build artifact. FAIL = no deploy.

## OP 5 — EPHEMERAL TOOL GENESIS (capability ≠ authority)

```bash
python3 /root/arif-fazil.com/scripts/web-zen/web_zen.py ephemeral \
  --task "mission gap: why needed" \
  --code-file /path/to/temp_tool.py
```

Loop: gap → search existing → reuse → generate → sandbox test → invoke → verify → **destroy** → promote only if repeated + human-approved.

GREEN: parsers, converters, disposable analysis. RED never self-grant: secrets, production deploy, persistent MCP, force-push, Caddy authority, payments. No `arif_create_random_tool` — modes under forge only.

## Anti-patterns (each cost real breakage)

- ❌ `rsync --delete` without orphan preview — destroyed 36 files 2026-07-23
- ❌ "Deployed" claimed without crawl verification — 7 landing pages were 404
- ❌ Generated content living only in live tree — organ_proxy/999/wealth.html
- ❌ Hand-editing live tree to "fix" — fix source, redeploy
- ❌ Status-200 audit without content grep — SPA soft-404 lies
- ❌ `rm -rf` for cleanup — quarantine instead
- ❌ Advertising 128 tools as intelligence — six missions + Canonical 8
- ❌ Deploying .well-known/robots.txt without no-cache header — Cloudflare serves stale Agentmap directives for hours, all 4 Lighthouse vectors appear broken from CDN while origin is correct
- ❌ Fixing CDN stale by hand-editing live tree instead of fixing Caddy config — the Caddy config IS the source of truth
---

## OP 9 — SURGICAL SPA PAGE UPDATE (no Caddy reload)

When the change is a single React page inside the arif-fazil.com SPA (e.g. a commodity terminal, a markdown article renderer, a state-machine visualisation), do NOT run `make deploy`. Caddy is irrelevant — the page is JS-routed, not server-routed. Surgical patch path:

**Source of truth:** `/root/arif-fazil.com/sites/arif-fazil.com/src/pages/<Page>.tsx`
**Built shell:** `/root/arif-fazil.com/sites/arif-fazil.com/dist/index.html` + `dist/assets/`
**Live webroot:** `/var/www/html/arif/index.html` + `assets/`
**Caddy handler:** `@spa_routes` in `/etc/caddy/vhosts/arif-fazil.com.conf` line ~2313 — fallthrough to `/var/www/html/arif/index.html` for any SPA route (incl. `/world/economics/gold/`, `/oil/`, `/gas/`, `/klci/`).

Sequence:

1. **Backup before edit** — `cp -a src/pages/<Page>.tsx src/pages/<Page>.tsx.bak-<reason>` (skill-internal; not a git commit until verified).
2. **Edit the .tsx** — the build will tree-shake unused symbols, so unused-variable warnings are noise; function-level errors block the build.
3. **Build only the SPA** (skip `make deploy`, skip Caddy):
   ```bash
   cd /root/arif-fazil.com/sites/arif-fazil.com && npm run build
   ```
   The build prints the new chunk hash, e.g. `CommodityPage-BcuuLmdL.js`. Note it.
4. **Sync to live webroot WITHOUT triggering Caddy reload:**
   ```bash
   rsync -av --update /root/arif-fazil.com/sites/arif-fazil.com/dist/index.html /var/www/html/arif/index.html
   rsync -av --update --delete /root/arif-fazil.com/sites/arif-fazil.com/dist/assets/ /var/www/html/arif/assets/
   ```
   `--update` on `index.html` keeps other content untouched; `--delete` is safe on `assets/` because the directory is owned by the build (no orphan pages live there).
5. **Verify by content signature, not by status code.** SPA soft-404 trap:
   ```bash
   curl -s https://arif-fazil.com/assets/<NewChunkHash>.js | grep -c '<distinctive-new-string>'
   ```
   A zero count means Cloudflare is serving a stale chunk or your build never landed. The new chunk hash must appear in the live assets.
6. **Cloudflare caveat:** the SPA shell returns `cf-cache-status: DYNAMIC` but asset chunks may linger on the edge for the TTL (typically 4 hours). Verify by content signature, not by chunk filename appearance.

**Why this beats `make deploy`:** no Caddy reload, no other pages touched, ~10-second cycle. A full `make deploy` reloads Caddy (T3 HOLD unless named) and triggers AAron-of-the-Cascade risk on unrelated handlers.

### Patch-from-stale-page (the trap that costs 30 minutes)

If you only update `/var/www/html/arif/assets/` and forget `/var/www/html/arif/index.html`, browsers cache the old SPA shell and the new chunk is never requested. **Always update both.** Verify both:
```bash
stat -c '%y %n' /var/www/html/arif/index.html /var/www/html/arif/assets/<NewChunkHash>.js
```
Both timestamps must be in this session.

### Live-data commodity page pattern

For pages that display live API data with static fallback (gold/oil/gas/klci/usdmyr):
- Type the live API response (e.g. `TickerLive`, `ApexLive` in the React file).
- Replace each hardcoded display value with `liveValue ?? staticFallback`.
- Add `useEffect` with `setInterval(fetchLive, 60000)` and `clearInterval` cleanup on unmount.
- Display a "last updated HH:MM:SS" timestamp + "AWAITING DATA" until the first fetch resolves.
- Live fallback must be invisible: the page should look identical whether live or static until the live data arrives.

Full recipe and idioms: see `references/live-data-commodity-pages.md`.

When F13 asks for a visual change and wants to *see* it before any deploy:

1. **Render it yourself — do not ask him which bot or format.** Headless Chrome on KVM8 is
   `/usr/bin/google-chrome`. Playwright's bundled browser is usually NOT installed
   (`chromium_headless_shell` missing) — do not `playwright install` on a production host;
   use system Chrome:
   ```
   google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
     --force-device-scale-factor=1 --window-size=430,2100 \
     --virtual-time-budget=5000 --user-data-dir=/tmp/chr-x \
     --screenshot=/abs/out.png file:///abs/preview.html
   ```
   Send PNG, not `.html` — fonts and CSS do not resolve from a file attachment.

2. **Verify the JS actually ran** before shipping: `--dump-dom`, then grep the ids the script
   writes. A screenshot of a clock that never ticked still looks fine.

3. **Link the canon tokens; never re-declare `:root`.** Copy
   `public/_shared/design-system/tokens.css` next to the preview so a relative
   `href="_shared/design-system/tokens.css"` resolves locally, then use
   `var(--soul-accent, #D4AF37)`. A private palette is how a page becomes a "rogue surface"
   (auditor finding, F13-Q2).

4. **Never generate CSS with regex.** `re.sub(r"\.cls\{[^}]*\}", ...)` stops at the first `}`
   — which is inside `clamp(...)` — and silently leaves half a keyframe block behind. Write CSS
   literally, or patch exact strings.

5. **Trademark:** build the *geometry*, not the franchise. A trinity emblem (triangle + circle
   + line) needs no franchise wording in the markup. If F13 wants the name on a public page,
   that is his explicit call — say so once, plainly, and build it.

6. **Never label an estimate as biometric.** If WELL holds no wearable or sleep data, the
   circadian surface is a *solar-entrained estimate* from the NOAA sunrise/sunset approximation
   for declared home coordinates — labelled "estimate · not biometric" in the UI itself.

7. A static HTML page with client-side JS is **still cacheable**. A live clock does not force a
   Caddy/Cloudflare caching change. Correct that claim when it is raised.

## OP 7 — MULTIMODAL VISION & CARTOGRAPHIC FIDELITY STANDARD (2026-09-18 F13 SEAL)

> "map buat la betul2 gambar render la guna ai image generator etc" — Arif Fazil (F13 Sovereign, 2026-09-18).
> A crude 15-point SVG polygon pretending to be Peninsular Malaysia is an F2 failure (TRUTH).
> A text-only dossier without visual evidence is an F4 failure (CLARITY).

1. **Physical Geography Demands Real Cartography:**
   - NEVER draw crude placeholder polygons for national or regional infrastructure claims.
   - For regional, Earth, infrastructure, and energy slices (e.g. Johor Data Centre Corridor, TNB 500kV Transmission Grid, water moratorium basins), embed interactive **Leaflet.js** or Mapbox GIS cartography.
   - Base tiles: **CartoDB Dark Matter** (`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`), pre-approved in Caddy CSP (`connect-src *.basemaps.cartocdn.com`).
   - Every site marker must contain verified coordinates, operator identity, capacity metrics (MW), grid interconnect, and water dissipation parameters.
   - Layer toggles must be interactive (`[All] [Data Centres] [Power Grid] [Water Stress]`).

2. **Generative Multimodal Asset Pipeline:**
   - High-impact editorial intelligence dossiers require high-fidelity visual representations.
   - Generate bespoke 16:9 cinematic editorial hero visuals (`generate_image` / `minimax` / `token-plan-image`) with precise architectural, telemetry, and lighting prompts.
   - Compress all generated imagery via Pillow to high-efficiency WebP (quality 80–82, ≤160KB per image).
   - Triple-Sync rule:
     1. Source repository: `/root/arif-fazil.com/sites/arif-fazil.com/public/<path>/images/`
     2. Build distribution: `/root/arif-fazil.com/sites/arif-fazil.com/dist/<path>/images/`
     3. Live web root: `/var/www/html/arif/<path>/images/`
     4. Base64 fallback embedded in standalone distribution files for 100% offline and cross-proxy reliability.

3. **Interactive Evidence & Receipt Layers:**
   - Sourced claims and receipts pages must NEVER be static, unsearchable HTML tables.
   - Implement client-side instant filtering by grade (`[All] [Grade A] [Grade B] [Grade C]`) and dynamic keyword search.
   - Every receipt must display: Grade badge, empirical claim summary, verified primary source link, and verification date.
   - Display the complete **Musyawarah Convergence Audit Trail** (333-AGI Δ MIND → 555-ASI Φ SENSE → CONVERGE → 888-APEX Ψ SOUL → F13 Sovereign Seal).

4. **Resilient Doctor Telemetry:**
   - `web_zen.py doctor` must always wrap receipt writes in an EROFS/OSError handler falling back to `/tmp/`, ensuring execution in restricted or sandboxed container environments.

DITEMPA BUKAN DIBERI.


---

## 🛑 Sovereign Execution Constraints (arifOS CAP)

> Injected 2026-08-20 by FI-003 (Qwen Code) under F13 "execute all" directive.
> Backup: /root/backups/skill-backup-20260820-pre-sovereign-injection/
> Derived from: Grammar Doctrine §10, Nusantara AI Paradox (MakcikGPT), BBB dataset, Nusantara Validator.

Before executing this web operation, the agent MUST enforce the following constraints:

1. **Corpus Priority (Paradoks 1):** If the topic touches regional identity, politics, or history, the agent must check for sovereign corpus availability first. If corpus is available, route there. If not, proceed with external search BUT flag the output as `UNVALIDATED_CORPUS` and require Nusantara rubrik evaluation before publication.

2. **BM Token Optimization (Paradoks 2):** When ingesting Bahasa Melayu web content, the agent must employ semantic caching and strict context chunking to manage the **1.5x–2.0x token penalty** (register-dependent: formal BM ≈ 1.5x, dialect/loghat ≈ 2.0x). Do not load raw HTML into the context window.

3. **Falsification Gate (Paradoks 3):** All synthesized outputs touching **regional identity, politics, history, or cultural narrative** must be evaluated against the Nusantara 3-Tier Rubrik (GAGAL/LULUS/KUAT). Outputs classified as GAGAL are rejected and halted. Outputs on non-contested topics (data, technical, commodity) proceed but carry a `CORPUS_UNTESTED` epistemic label.

**Rubric reference:** `huggingface.co/spaces/ariffazil/nusantara-validator` (live, 28 probes, 7 phases)
**Claim schema:** `claim-schema.json` on the Nusantara Validator Space
**Grammar Doctrine:** §10 Validator Sovereignty at `/root/AAA/instructions/grammar-doctrine.md`
