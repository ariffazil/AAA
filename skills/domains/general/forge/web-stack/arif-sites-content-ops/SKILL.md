---
name: arif-sites-content-ops
description: "Edit, build, and deploy content on arif-fazil.com (React 19 + Vite). Covers essay location, content structure, build pipeline, and the"
version: 1.6.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [site, content, essays, react, vite, deploy, arif-fazil, makcikgpt, caddy, cron]
    category: devops
    related_skills: [makcikgpt-article-forging, site-deployment-verification, caddy-reverse-proxy]
    floors_protected: [F2, F4, F11]
    origin: 2026-07-18 essay audit → 2026-08-01 Caddy patch + cron immune system + external witness audit
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# arifOS Sites Content Operations

Edit, build, and deploy content on arif-fazil.com. The site is React 19 + Vite, with essays stored as TypeScript data objects.

## ⛔ DEPLOYMENT GATE — READ BEFORE EVERY ACTION (F1/F13, 2026-08-09)

**No agent may deploy public-facing changes without explicit go signal from Arif.**

This includes: landing pages, index pages, Caddy config, any file under `/var/www/html/arif/`, any Caddyfile change.

**Workflow (MANDATORY):**
1. Audit → report findings to Arif
2. Wait for explicit go signal ("go", "deploy", "buat", "push")
3. Only then: deploy + verify

**HARAM (any of these = violation):**
- Generate a new landing page and deploy it without asking
- Edit Caddyfile and reload without explicit approval
- rsync to webroot without Arif saying go
- Assume "improvement" means implicit permission

**Scar:** 2026-08-09 — OPENCLAW generated + deployed a new MakcikGPT landing page (date-ranked, topic-grouped) without asking. Arif: "Fuckkkk. Undooioi." Reverted immediately. Lesson: audit only until go signal.

## When to use

- **CRITICAL:** Before adding/relocating any content, study the architecture first. See `references/site-architecture-pre-workflow.md` — Arif's direct instruction: "jangan tepek, integrate into the instrument system."
- Arif drops an external AI audit/review (ChatGPT, Perplexity, etc.) on the site and says "fix this" or "reality verdict"
- Arif shares external audit feedback on an essay and says "fix it"
- Editing or adding MakcikGPT articles
- Editing React components (footer, header, pages) — not just essays
- Building and deploying the site after changes
- Fixing governance/canonical claims (seals, pseudo-metrics, stale version strings) that appear in the UI
- Adding or upgrading visual assets, GIS cartography, or media payloads (see OP 7 & `references/asset-hash-and-multimodal-fidelity.md`)

## 🗺️ OP 7 — Multimodal Vision, Cartographic Grounding & Asset-First Law (F13 SEAL 2026-09-18)

> *"map buat la betul2 gambar render la guna ai image generator etc"* — Arif Fazil (F13 Sovereign).  
> Full doctrine, incident mechanics, and verification checklist: `references/asset-hash-and-multimodal-fidelity.md`.

1. **Physical Geography Demands Real Cartography (F2 TRUTH):**
   - NEVER use crude placeholder SVG polygons for national/regional infrastructure claims.
   - Use interactive **Leaflet.js** with CartoDB Dark Matter tiles (`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`), pre-approved in Caddy CSP (`connect-src *.basemaps.cartocdn.com`).
   - Every site marker must have authentic coordinates, operator, capacity (MW/GW), and environmental parameters.
   - Interactive layer controls (`[All Layers] [Data Centres] [Power Grid] [Water Moratorium] [Interconnects]`).

2. **Cloudflare Cache Edge Poisoning Defect & Asset-First Rule (SCAR-2026-09-18):**
   - **Asset First, Reference Second:** NEVER write `<img src="...">` or `<link href="...">` in HTML before the physical file exists on disk, in dist, and in webroot. Cloudflare edge will cache the initial 404 with long TTL (`max-age=31536000`), breaking subsequent valid requests.
   - **Contaminated-URL Rule:** If an asset URL was ever requested while non-existent (receiving a 404), DO NOT retry the same URL. Re-key the filename with a content hash (e.g. `hero-five-engines.c797f5c9.webp`). Fresh URLs bypass contaminated edge caches immediately.

3. **Epistemic Metric Truth (Anti-Hallucinatory Standard):**
   - Report measured reality: actual bytes, actual dimensions (`1376x768`, never inflated "8K"), actual WebP quality/sizes (≤200KB).

## Site architecture

> Full topology map (22 subdomains, 7 organs, ports, layers, MakcikGPT dual-path,
> cron immune system, F13 gates): `references/site-architecture-map-2026-08-01.md` —
> probe live state before trusting any single line.
>
> **Surface catalog + routing map (dual-commodity surfacing, /politics/ section,
> /forge/ shadow decoder, navCanon auto-generation):**
> `references/site-architecture-surfaces-2026-08-03.md` —
> maps every route section, surfaces.json role, and the architecture-first workflow.

```
/root/arif-fazil.com/
├── sites/arif-fazil.com/     ← React 19 + Vite (the only site that needs build)
│   ├── src/
│   │   ├── pages/            ← Route-level pages (Home.tsx, Essays.tsx, Canon.tsx, etc.)
│   │   ├── components/       ← Reusable components (ConstellationFooter.tsx, ConstellationHeader.tsx, etc.)
│   │   ├── data/essays/      ← Essay content as .ts files
│   │   │   ├── index.ts      ← Essay registry
│   │   │   ├── 02-i-have-trust-issues-with-agents.ts
│   │   │   └── ...
│   │   ├── data/wealth/      ← Wealth/commodity dashboard data
│   │   ├── data/makcikgpt/   ← MakcikGPT articles
│   │   └── data/siteContent.ts ← Site-wide data (links, portfolio, organ doors)
│   └── public/               ← Static HTML pages (gas/, arifos/, etc.)
│       └── gas/index.html    ← Gas dashboard — static, not React
├── deploy-vps.sh             ← Deploy script (builds + rsyncs all sites)
└── config/sites.json         ← Site registry
```

Key files for common edits:
- **Footer:** `src/components/ConstellationFooter.tsx` — copyright, seal claims, federation links, human/machine badge separation
- **Homepage:** `src/pages/Home.tsx` — hero, organ doors, governance bridge, wells portfolio
- **Navigation:** `src/data/siteContent.ts` — primaryLinks[], organDoors[], ecosystemLinks[], arifosLinks[]
- **NS Election GIS page:** `public/politics/ns-election/index.html` — standalone Leaflet GIS page, data-driven (see below)

### Essay file structure

Each essay is a TypeScript object with:
```typescript
const content = {
  title: "...",
  date: "YYYY-MM-DD",
  tags: ["tag1", "tag2"],
  excerpt: `...`,
  mediumUrl: "...",  // optional, for cross-posted essays
  html: `<h3>...</h3><p>...</p>...`  // The actual content as HTML string
};
export default content;
```

**Critical:** The `html` field is a single template literal containing the full essay as HTML. Editing requires finding the exact string within this field.

## Build & deploy

```bash
# 1. Install deps if build hasn't run (--legacy-peer-deps required)
cd /root/arif-fazil.com/sites/arif-fazil.com && npm install --legacy-peer-deps

# 2. Build (also regenerates feed, sitemap, llms, makcikgpt listing)
npm run build

# 3. Deploy to VPS — manual rsync is most reliable
cd /root/arif-fazil.com

# Step A: Sync static HTML/MD files for crawlers (makcikgpt-md/)
rsync -av sites/arif-fazil.com/public/makcikgpt-md/ /var/www/html/arif/makcikgpt-md/

# Step B: Sync built dist
rsync -av sites/arif-fazil.com/dist/ /var/www/html/arif/

# Step C: Reload Caddy
sudo caddy reload --config /etc/caddy/Caddyfile

# Verify: check JS bundle hash matches
DIST_JS=$(ls -t sites/arif-fazil.com/dist/assets/*.js | head -1 | xargs basename)
LIVE_JS=$(curl -s "https://arif-fazil.com/" | grep -oP 'index-[A-Za-z0-9]+\\.js')
[ "$DIST_JS" = "$LIVE_JS" ] && echo "MATCH: $DIST_JS" || echo "MISMATCH — redeploy"
```

Build output goes to `dist/`. The dist syncs to `/var/www/html/arif/`.

### Deploy script alternative (may fail)
```bash
bash scripts/deploy-site.sh arif-fazil.com --apply
```
`deploy-vps.sh` validates registry schema and may fail if `schema_version` in
`infra/runtime-overlays.json` doesn't match. Manual rsync (steps A-C) is safest.

## Governance Fix workflow (EXTERNAL AUDIT → REALITY VERDICT → FIX)

When Arif drops an external AI's audit/review (e.g., ChatGPT "fable5" session) and says "fix this" or "reality verdict":

1. **Read the audit critically.** External AI reviews are ADVISORY ONLY — never treat as constitutional authority. Sort claims into: (a) testable (kernel bugs, deployment state, seal validity), (b) editorial opinion (structure, tone, ordering).
2. **Probe live state first.** Test every testable claim against the actual system. Kernel state via `arif_init`/`arif_judge`, live site via `curl`, source files via `search_files`.
3. **Give a reality verdict.** Structured table: what's correct, what's partially correct, what's wrong. Then offer to fix — "Nak aku patch apa-apa ke?" — don't assume, let Arif confirm.
4. **Apply only validated fixes.** Ignore wrong/outdated audit claims. Fix what's real.
5. **Build, deploy, verify.** Follow the build→deploy flow below. React SPAs cannot be verified via `curl` — `grep` the built JS bundle instead. `grep -c "expected_string" /root/arif-fazil.com/sites/arif-fazil.com/dist/assets/*.js`. The deploy script's HTTP 200 check only confirms the shell loaded.

The "fable5" reference = external AI session identifier. Treat as second opinion, never authority.

## Feedback → Fix workflow (essay content)

1. **Identify the essay** — match the feedback's references (title, quotes, section names) to a file in `src/data/essays/`
2. **Extract the specific edits** — the audit usually names: (a) a claim to correct, (b) an argument to add/restructure, (c) a gap to fill. Map each to a specific location in the `html` string
3. **Apply via patch** — use `patch` tool with `mode=replace` to find-and-replace within the `html` template literal. For adding new sections, replace the adjacent section boundary
4. **Build** — `npm run build` to verify no syntax errors
5. **Deploy** — `cd /root/arif-fazil.com && bash scripts/deploy-site.sh arif-fazil.com --apply`
6. **Verify** — confirm HTTP 200 in deploy output

## Reading content from the site

**web_extract / Tavily is BLOCKED on arif-fazil.com** (HTTP 432). Always use the browser for reading content from this domain.

Workflow for reading/digesting published articles:

1. **Navigate to the listing page** (e.g., `/makcikgpt/`) via `browser_navigate`
2. **Extract article URLs** via `browser_console` with JS:
   ```js
   const links = document.querySelectorAll('a[href*="makcikgpt"]');
   // filter to unique article paths, skip the listing page itself
   ```
3. **Read each article** via `browser_navigate` + `browser_snapshot(full=true)`
4. For bulk digest (10+ articles), delegate to a subagent to avoid context flooding

MakcikGPT articles live under `/world/makcikgpt/<slug>` in the URL structure (not `/makcikgpt/<slug>`). The listing page is at `/makcikgpt/`.

## NS Election GIS page — data-driven static HTML (PROVEN 2026-08-01)

`public/politics/ns-election/index.html` is a **standalone static Leaflet GIS page** (NOT React — no build needed for content edits, but it IS copied into dist by Vite from `public/`). It renders election results via a data-driven JS pattern:

- **`const SEATS = [...]`** — one object per DUN with `{code, name, inc, maj, winner, cls, hot, lat, lng, notes}`. `winner` + `cls` (ph/bn/pn/tossup) drive marker colors, grid tiles, popups, filters.
- **`const INVARIANTS = [...]`** — the 9 spatial-field invariant cards.
- Map markers, grid cards, popups, and the inspector all derive from `SEATS` — **you never edit render JS to change results, only the data arrays.**
- Filter buttons (`ALL (36)`, `BN (18)`, `PH (11)`, `PN (7)`, `🔥 HOT (8)`) are **hardcoded HTML** — must be updated manually when seat counts change.

**Update workflow when new results arrive (election night / final result):**
1. `diff public/politics/ns-election/index.html /var/www/html/arif/politics/ns-election/index.html` — confirm public/ is source of truth (it should be; if differs, resolve first).
2. Edit the `SEATS` array: flip `winner`/`cls`, annotate `notes` with `FLIP:`/`⚠️ UPSET:`/`held` per seat.
3. Update hardcoded filter buttons to match new counts (BN/PH/PN totals).
4. Add a `🏁 FINAL RESULT` banner card + mark scenario cards `✅ REALISED` / `✗ DID NOT MATERIALISE` — don't leave pre-poll projections labelled as live outcome.
5. Update inspector defaults (the top `DUN N32 · 🔥 BATTLEGROUND` block) if the featured seat outcome changed — it's static HTML, not data-bound.
6. Update `Updated <date>` in top-bar.
7. `npm run build` (copies public/ → dist/), `rsync -av --delete dist/ /var/www/html/arif/`, then verify with `browser_navigate` (Leaflet renders client-side — curl/grep on the HTML won't show marker states; grep the file for banner strings instead).

**Result provenance discipline (F2 TRUTH):** label UNOFFICIAL vs OFFICIAL explicitly on the page. Election-night media calls are TIDAK RASMI until SPR declares. Sources that worked 2026-08-01: BHarian live blog (`bharian.com.my` TERKINI PRN NS), Utusan, Harian Metro live, MyUndi (`myundi.com.my/ms`). Cross-check BN/PN/PH seat lists from two outlets before writing to the page. Update the companion `ns_live_telemetry.json` status (e.g. `RESULT_DECLARED`) via dual-write (see Pitfall #20).

**No prediction scorecards — Arif's correction (2026-08-01, PRN16).** After the results, Arif said: *"No need to put out prediction. Kita bukan official Pon. Hang tu bias tengok berita yang ada ja. Aku dah lama kata akan kalah teruk. Sentimen. Manusia hang x faham."* → Do NOT publish "we predicted X vs actual Y" post-mortems on the site as if we're an authoritative pollster. The site shows **ACTUAL RESULTS only** (with UNOFFICIAL/OFFICIAL labels). News-based analysis is biased toward the mainstream narrative — ground sentiment (which Arif reads directly) beats news-based models. If Arif calls a result ahead of time, weight his call over any model; do not argue it with media framing. F2 TRUTH on election pages = results + provenance + honest labels, NOT self-promoting prediction retrospectives.

**Seat-to-seat comparison sub-page (PROVEN 2026-08-01).** `public/politics/ns-election/compare/index.html` + PNG charts, linked from the GIS page footer. Build pattern:
- Python matplotlib script, dark theme (`#07090E` bg), coalition colors PH `#ef4444` / BN `#3b82f6` / PN `#10b981`, flips amber `#f59e0b` → three static charts (`totals.png` grouped bars 2023→2026, `flip_matrix.png` 3×3 transition heatmap, `ladder.png` all 36 seats as 2023-chip → 2026-chip rows with FLIP labels) + `seat_sweep.mp4` (matplotlib FFMpegWriter, libx264, yuv420p, ~14s seat-reveal sweep + final tally — Telegram-safe under 50MB).
- Copy PNGs beside the compare page in `public/`, build, rsync. The compare table is data-driven from a JS SEATS array; flip rows get amber background + `FLIP X→Y` badge.
- **Flip derivation discipline:** flips = actual 2023 winner vs actual 2026 winner. NEVER derive flips from the page's pre-existing labels — the old filter buttons (PH 18/BN 16/PN 2) were PROJECTIONS, not the 2023 baseline (actual 2023: PH 17 / BN 14 / PN 5 per SPR). Pull the official baseline from `pilihanraya.my/keputusan/negeri_sembilan/prn15-2023` (full per-seat winner+majority table, sourced from SPR) and spot-check 5+ seats. PRN16 caught: early banner said "PN flips: Serting, Bagan Pinang" — both were PN since 2023 (holds, not flips); caught by re-derivation. Re-derive seat lists from data, never from memory of media reports.
- Full recipe + generator code: `references/ns-seat-comparison-viz-2026-08-01.md`.

**Data-driven auto-update pipeline for static pages (PROVEN 2026-08-01, "I want it auto update sekali result dah dapat").** When Arif asks for auto-update on a results/compare page, the durable pattern is JSON SOT + generator + prebuild wiring + a lightweight mtime watchdog cron — NOT a full rebuild on a timer:

1. **JSON source of truth** — `public/data/politics/ns_results.json`: `{metadata:{updated_at,status}, seats:[{code,name,y2023,y2026,maj2023}], tally_*, coalition_*}`. This is the ONLY file humans/agents edit to change results.
2. **Generator script** — `scripts/generate-ns-compare.cjs`: reads the JSON, emits `compare/index.html` (tally cards + full seat table + flip badges, all derived from data). Never hand-edit the generated HTML — it's overwritten.
3. **Prebuild wiring** — append `&& node scripts/generate-ns-compare.cjs` to the `prebuild` chain in package.json so every `npm run build` refreshes the page from current data. Test: flip a seat in JSON → build → grep generated HTML → revert.
4. **Watchdog cron** — `~/.hermes/scripts/ns-compare-watchdog.sh` (no_agent:true, `*/15 * * * *`, deliver=origin): regenerates + rsyncs ONLY that one directory when `[ "$SRC_JSON" -nt "$GEN_HTML" ]`; silent otherwise (empty stdout = no delivery). No full build, no Caddy reload, no T3 gate — it's a verify-class op, safe to chain. Script packaged in this skill at `scripts/ns-compare-watchdog.sh` — copy to `~/.hermes/scripts/` and wire the cron.
5. **Result data hygiene:** flip counts come from data (`seats.filter(s => s.y2023 !== s.y2026).length`), never hardcoded. Page footer shows "auto-sync dari ns_results.json" so Arif can see it's data-driven.

**Prediction-content policy — "kita bukan pundit" (2026-08-01, Arif):** Do NOT publish prediction scorecards / post-mortem verdicts as site content ("No need to put out prediction. Kita bukan official Pon."). Result pages = pure results. If Arif asks for the projection contrast, build it as a SEPARATE neutral artifact — `projection-vs-actual.html` (standalone static page: seat cards projection→actual, ⚡FLIP highlight, accuracy stat) + a shareable chart PNG — never as an editorialised "we were wrong" narrative on the GIS page. Model truth-telling rule: direction-correct ≠ projection-correct, state both plainly; news-trained models miss ground sentiment, Arif reads the room ("Aku dah lama kata akan kalah teruk. Sentimen. Manusia hang x faham.") — when his sentiment call conflicts with model output, his call wins.

**Projection-vs-actual comparison (companion page, 2026-08-01):** `public/politics/ns-election/projection-vs-actual.html` — standalone static page (no build; lives in public/ next to index.html, rsync + curl 200 + commit). Recover the pre-poll projection from git BEFORE the result commit — the committed pre-result version is the auditable projection source: `git log --oneline -- <file>` → `git show <prev-hash>:<path> > /tmp/ns_prepoll.html`, then parse BOTH `SEATS` arrays (regex `code/name/winner` per line) and diff winner fields to list flips. Deliver multimodal: live page + matplotlib PNG via MEDIA: (dark #0a0a0a bg, Primer palette, two panels: coalition totals bars + 36-seat grid). When the active model has no native vision (vision_analyze returns "[Unsupported Image]"), verify the chart via PIL pixel analysis (size/mode/dominant-colour count) instead of trusting the render blindly.

**Deployment reality (2026-08-01):** FORGE (kimi-code/opencode) edits the SAME files concurrently and will commit before you do. After editing, `git log --oneline -3` — if HEAD already contains your changes (sibling committed them with possibly-refined text), **do not double-commit**; verify content, then move on. `git status --short` showing no changes for your file = someone else committed it — check `git show HEAD:<path> | grep <your-marker>` to confirm your content survived.

## web-canon Atlas — the site constitution (PROVEN 2026-08-01)

The site's law lives in a SEPARATE repo, not the React app: `/root/web-canon` (GitHub `ariffazil/web-canon`). It holds the canonical map every page, coder, and agent must obey. When Arif says "make the Atlas authoritative" or "link to ATLAS333", this is the territory:

```
/root/web-canon/
├── canon/                # Law files (JSON/YAML): navigation.json, design-tokens.json,
│                         #   typography.json, components.json, templates.json, routes.yaml,
│                         #   redirects.yaml, sites.yaml, public-state.schema.json,
│                         #   federation.json, geometry.json, releases.json, tool-surfaces.json,
│                         #   atlas.yaml (route→ring/plane/page_type/layout authority),
│                         #   file-authority.yaml (CANON/DERIVED/PROPOSAL states + leases)
├── atlas/                # Long-form doctrine (markdown): WEB_ATLAS.md (the constitution),
│                         #   WEB-FEDERATION-MAP.md (repos/webroots/topology),
│                         #   STATIC_VS_DYNAMIC.md (automation paradox),
│                         #   INVARIANTS_OF_AGENTIC_SITES.md (13 invariants I1-I13)
├── docs/                 # SITE_CONTRACTS.md, AUTHORITY_MATRIX.md, RELEASE_POLICY.md, etc.
└── scripts/              # atlas-sync.sh, canon-sync.sh, canon-lint.js, agentic-web.sh,
                          #   verify-design-alignment.cjs (SENSE_ALIGN gate)
```

**New canon files (2026-08-01 session):**
- `canon/atlas.yaml` — route registry: every route declares `ring` (SOUL/MIND/BODY/ORGAN), `plane` (narrative/proof/organ/domain), `page_type`, `layout`, `audience`, `data_source`. The authority the SPA shell must obey.
- `canon/file-authority.yaml` — file states CANON/DERIVED/SCRATCH/PROPOSAL/RECEIPT/RETIRED/UNKNOWN + lease model + mutation budget + agent roles (scout/architect/implementer/auditor/janitor/judge). Stops multi-agent "forked intention" (six pseudo-Atlases).
- `atlas/INVARIANTS_OF_AGENTIC_SITES.md` — I1-I13: ATLAS before action, Canon before code, SOT before rendered page, Shared shell before subpage freedom, Tokens before local CSS, Navigation before content, Static evidence before SPA fallback, Diff before mutation, Verification before SEAL, Unknowns declared, Human owns meaning, Agent owns operational clarity, No automation without reversibility.

**Both new YAML files MUST be added to `canon-sync.sh`'s required-files array** or the live mirror won't update (canon-sync only syncs its declared list).

**PRIMER-1 four-file design canon (ratified 2026-08-01, Arif F13).** The design constitution split into four authority layers + one CI gate — this is the "design-primer.md = human doctrine, design-tokens.json = machine law, tokens.css = rendered law, CI = enforcement" architecture. Do NOT let agents create DESIGN_V2.md / FINAL_DESIGN.md / tokens-new.json / theme-v2.css / hero-manifest-final.json — those are entropy files ("many proposals, one canon, one promoter, one receipt"):
- `canon/design-primer.md` — human doctrine (SEAL header, color/type/geometry/tactility/rendering sections, token sketch)
- `canon/design-tokens.json` — machine law (exact hex scales human/institution/earth/sovereign/neutral; geometry radii {human:12, machine:2, torus:full}; motion 90ms; territory_map; machine_twin channel/state enums)
- `canon/design-rules.json` — lintable invariants (red_usage scopes, allowed_radii, max_torus_per_view=1, forbid_local_palette, forbid_unregistered_hero, require_channel_field, require_state_enum, contrast_floor, motion_rationing, live_must_be_real, prefers_reduced_motion)
- `canon/page-instruments.json` — route hero law ("a page cannot choose its own hero — the route registry chooses the hero"; every route declares territory/palette/instrument/data/torus_count/status; held items carry hold_reason)
- `/root/web-canon/scripts/verify-design-canon.cjs` — the lint gate (66 checks: token-vs-PRIMER_SPEC alignment, red rationing, radii, contrast, instruments registry, rules self-consistency); wired into site package.json prebuild chain as F4 gate

**Ratification protocol (Arif 2026-08-01):** Phase 1 = freeze PRIMER-1 as `forge_work/proposals/design/2026-08-01-primer-1/design-primer.proposal.md`; Phase 2 = promote ONLY the four canon files. If a sibling agent does Phase 1 while you do Phase 2, both coexist correctly — keep the proposal copy as audit trail AND the canon copy as law (commit both). Build order: canon first, then ONE reference instrument page (/earth preferred over /world/oil — oil needs a real data source, see F9 below).

Full architecture map, ring/plane table, I1-I13 summary, enforcement chain, sync commands: `references/atlas-governance-architecture.md`. PRIMER-1 token/canon details + the contrast-correction workflow: `references/primer1-design-canon.md`.

**Sync to live (two pipelines, both with dry-run default):**
```bash
cd /root/web-canon
bash scripts/canon-sync.sh          # dry-run — validates + diffs canon/ JSON/YAML
CANON_SYNC_LIVE=1 bash scripts/canon-sync.sh   # live sync canon/ → /var/www/html/canon/

bash scripts/atlas-sync.sh                    # dry-run — validates + diffs atlas/ md
ATLAS_SYNC_LIVE=1 bash scripts/atlas-sync.sh  # live sync atlas/ → /var/www/html/canon/atlas/
```
Both scripts: validate → backup (`.bak.<timestamp>`) → atomic rsync → drift test → arifFlow receipt. Required-doc check enforces `STATIC_VS_DYNAMIC.md` presence. Emits a receipt via arifFlow (HTTP 200, id returned).

**ATLAS333 link:** the web Atlas is the *territory map*; ATLAS333 is the *cognitive substrate* — 33 paradox axes, 7 zones, TEARFRAME thresholds, GPV routing, living in arifOS: `333_MIND_ATLAS.md` (`/root/arifOS/static/arifos/theory/000/`), `ATLAS333_BRIDGE.md` + `atlas.py` (`/root/arifOS/core/shared/`), `paradox_gate.py` (enforcement). Binding paradoxes for web work: P3 (map ≠ territory), P17 (Atlas must be useful/committed), P30 (forgery detectable), automation paradox (autonomy saves hands, demands stronger judgment). `WEB_ATLAS.md` §8 maps each artifact to its web use.

**Search & discovery wiring (the "search strategy" ask):** canon must be discoverable by humans AND agents:
- `llms.txt` → reference `/canon/atlas/WEB_ATLAS.md` as the site constitution
- `sitemap.xml` → include `/canon/atlas/` long-form docs
- `robots.txt` → allow `/canon/`
- `web_zen.py doctor` → checks canon files exist + canon-sync drift gate
- **CRITICAL:** the Caddy `/canon/*` handler MUST have `root * /var/www/html/canon` or it serves the SPA shell for JSON/MD files — machine-readable law becomes invisible (see `caddy-reverse-proxy` skill pitfall "handle /canon/* Without root"). Verify: `curl -sI https://arif-fazil.com/canon/navigation.json | grep -i content-type` must be `application/json`.

## SENSE_ALIGN — design alignment gate (PROVEN 2026-08-01)

"GREEN route does not mean aligned design." 200 OK only proves the page exists, not that it belongs to the same system. The gate lives at `/root/web-canon/scripts/verify-design-alignment.cjs`:

```bash
cd /root/web-canon && node scripts/verify-design-alignment.cjs          # all atlas routes
node scripts/verify-design-alignment.cjs /writing                       # one route
```

Checks per route: route_200 · tokens_loaded (`/_shared/design-system/tokens.css`) · data_ring · data_plane · trinity_nav · canon_footer. Exit 1 = violations.

**Key implementation lessons:**
- **SPA routes: markers live in the JS bundle, not the shell HTML.** For any route whose HTML contains `/assets/index-*.js`, fetch the bundle and append it to the haystack before searching for data-ring/data-plane/nav/footer markers. The shell alone never contains client-rendered markers — searching it yields false failures.
- **Redirects: curl needs `-L`.** `/gold` → 308, `/canon` → 301. Without `-L` the fetch returns 0B and every check fails.
- **data-ring on static pages vs SPA:** the React shell (`index.html`) hardcodes `data-ring="SOUL"` on `<html>` — every SPA page inherits SOUL until AtlasGate overrides it. Static hand-rolled pages often declare their own ring or none.

**AtlasGate — per-route ring/plane (PROVEN 2026-08-01).** `src/components/AtlasGate.tsx` sets `data-ring`/`data-plane` on `<html>` from a longest-prefix route table (mirrors `canon/atlas.yaml` routes). Wired inside `<BrowserRouter>` in App.tsx. Result: `/` = SOUL/narrative, `/999` = MIND/proof, `/politics/ns-election` = BODY/organ. Verify in browser: `document.documentElement.getAttribute('data-ring')`.

**Static pages don't get AtlasGate** — they're standalone documents outside the React shell. For those, shell-wrap remediation applies (below).

### Shell-wrap remediation — give static pages shell inheritance (non-destructive)

When SENSE_ALIGN fails on sovereign hand-crafted static pages (/000, /999, /earth, GIS map, shadow), the fix is NOT rewriting them as React (content-preservation risk — bespoke features, maps, sealed vaults). Shell-wrap instead: `sites/arif-fazil.com/scripts/shell-wrap.sh` adds, idempotently, to each target `public/<dir>/index.html`:
1. `<link rel="stylesheet" href="/_shared/design-system/tokens.css" />` after `<head>` if missing
2. `data-ring="X" data-plane="Y"` on `<html>` (map per atlas.yaml)
3. CanonFooter block (DITEMPA + WEB_ATLAS/file-authority links) before `</body>` if missing

**Pitfall:** pages with existing `data-ring="ROOT"` and `lang="en"` between `<html` and `data-ring` break naive sed. Use python regex that tolerates attributes between: `re.sub(r'<html([^>]*?)data-ring="[^"]*"', ...)` — and handle the "has ring, no plane" case in a second pass. Backups go to `public/.shell-wrap-backup-<ts>/` before any edit. Then rsync the wrapped dirs to webroot and re-run SENSE_ALIGN. Script packaged in this skill at `scripts/shell-wrap.sh`.

## Canon-driven navigation — one canon, one component, zero duplicates (PROVEN 2026-08-01)

Nav unification doctrine: *"no page owns its own `<nav>`; canon/navigation.json is the only source of truth."* Two IAs were drifting — the canonical trinity (HUMAN/INSTITUTION/EARTH) and the operational primary nav (START/EXPLORE/ANALYZE/...). Resolution per I9 (patch existing canon before inventing): **sync the operational nav INTO canon**, then render from canon only.

**One-line nav trim (2026-08-01, Arif video annotation: "navigation just do one line. No redundant.").** Primary nav was 8 items — too many, and several were redundant subsets. Trim rule: keep ONLY durable top-level destinations; anything that is a subset of another item (Gold ⊆ World commodity scope) or belongs in the footer shelf (Doctrine) moves to `civicLinks[]` in siteContent.ts — **no link is ever lost, only relocated**. 8→6: Start · Earth · Economics · World · Politics · Read. The label pairs (Start/Explore/Analyze/Track) were the verb-chrome; direct nouns (Earth/Economics/World/Politics/Read) are the one-line answer. After trimming canon, re-run `node scripts/generate-nav-canon.cjs` (regenerates navCanon.ts) then build. Audit: every dropped item must appear in footer civicLinks or it's an orphan (Arif's standing rule).

Pipeline (SOT → generator → derived → render):
```
canon/navigation.json primary_links.items (CANON — edit here)
  → scripts/generate-nav-canon.cjs (prebuild chain)
  → src/data/navCanon.ts (DERIVED — auto-generated header, never hand-edit)
  → ConstellationNav.tsx renders primaryNav (both desktop + mobile menus)
```

**Key steps:**
1. Add `primary_links` (label/href items) to `/root/web-canon/canon/navigation.json` — F2: canon must match reality, so mirror the actual site nav.
2. `scripts/generate-nav-canon.cjs` emits `src/data/navCanon.ts` with `export const primaryNav: NavItem[]` + `export interface NavItem { label; href; external?: boolean }`.
3. Append to prebuild chain in package.json so every `npm run build` regenerates.
4. Replace `primaryLinks` import in ConstellationNav.tsx with `primaryNav` (both desktop AND mobile nav blocks).
5. Verify canon→derived flow: change a label in canon → run generator → grep derived file → revert.

**Pitfalls:**
- **The generator overwrites manual edits to the derived file.** If you fix the derived file by hand (e.g. add `external?`), ALSO patch the generator template — next build clobbers your fix.
- **Type mismatch:** `NavItem` must include `external?: boolean` or TS2339 fires when the component checks `item.external` for outbound links.
- **Two nav blocks** (desktop `hidden md:block` + mobile menu) both iterate — replace BOTH or you get mixed sources.
- `primaryLinks` in `siteContent.ts` stays for backward compat but is no longer the nav source — don't edit it for nav changes.

## File governance — CANON/DERIVED/PROPOSAL states (PROVEN 2026-08-01)

Arif's doctrine: *"Same directive ≠ same execution. Same mission ≠ same file boundary. Agents do not naturally coordinate."* The disaster pattern: five agents each create their own pseudo-Atlas (WEB_ATLAS.md, ATLAS.md, DESIGN_SYSTEM_V2.md...). Solution is explicit file authority — `/root/web-canon/canon/file-authority.yaml`:

**File states:** CANON (read; mutate only with lease) · DERIVED (generated; never hand-edit) · SCRATCH (temp; clean or promote) · PROPOSAL (human review artifact) · RECEIPT (append-only) · RETIRED (do not use) · UNKNOWN (HOLD — no action).

**Key rules:**
- No agent may create a new canonical file. Only ARIF (or an authorized promotion step) canonizes.
- Agents write only to `forge_work/proposals/<agent-id>/<mission>/**` or `receipts/<agent-id>/**`.
- Lease model: `lease: {agent, mission, files, mode: edit, expires: 30m, authority: ARIF_SEAL_REQUIRED}` — no lease, no mutation; concurrent lease on same file → HOLD.
- Mutation budget: max 5 files changed, 0 new files outside allowed zones.
- Roles with separation of powers: scout (detect, no write) · architect (propose) · implementer (leased files only) · auditor (receipts only) · janitor (cleanup) · judge (compare, no direct mutation).
- Agent prompt header: **FILE GOVERNANCE MODE: FAIL-CLOSED** — list target files, state each authority, UNKNOWN→stop, DERIVED→find upstream SOT, CANON→request lease, no lease→proposal only.

**Where it lives in practice:** the fail-closed header is embedded in `sites/arif-fazil.com/public/AGENTS.md` (and served at `/AGENTS.md`). Site canon files (App.tsx, AtlasGate.tsx, ns_results.json) are CANON — agents edit only with Arif's explicit go. Generated outputs (dist/, compare/index.html, navCanon.ts, ns_live_telemetry.json) are DERIVED. The `canon/` mirror in `/var/www/html/canon/` is DERIVED (synced by canon-sync.sh).

**Pitfall — canon-sync required-files list:** `scripts/canon-sync.sh` has a hardcoded array of files it syncs. Any NEW canon file (atlas.yaml, file-authority.yaml) must be added to that array or the live mirror 404s. Check with `curl -s -o /dev/null -w '%{http_code}' https://arif-fazil.com/canon/<new-file>` after sync.

## Partial rsync = built-but-not-served bundle (PROVEN 2026-09-18)

A full `npm run build` writes `dist/index.html` pointing at a NEW hashed bundle
(`assets/index-<hash>.js`). If only `assets/` reaches the webroot and `index.html` does not,
the new bundle sits in `/var/www/html/arif/assets/` while the live HTML still points at the
PREVIOUS hash. The site keeps serving old content indefinitely — and the new file's presence
on disk makes it look deployed.

**Symptom:** `grep -c '<marker>' /var/www/html/arif/assets/index-<new>.js` > 0 (the file is
there) but `curl -s https://arif-fazil.com/ | grep -oE 'assets/index-[A-Za-z0-9_-]+\.js'`
names a DIFFERENT, older hash. Verify by fetching the LIVE html and checking which hash it
references, never by grepping the newest file in the webroot.

**Audit (run after every deploy):**
```bash
DIST=/root/arif-fazil.com/sites/arif-fazil.com/dist
WEB=/var/www/html/arif
D=$(grep -oE 'assets/index-[A-Za-z0-9_-]+\.js' $DIST/index.html | head -1)
W=$(grep -oE 'assets/index-[A-Za-z0-9_-]+\.js' $WEB/index.html | head -1)
L=$(curl -s -m 10 https://arif-fazil.com/ | grep -oE 'assets/index-[A-Za-z0-9_-]+\.js' | head -1)
[ "$D" = "$W" ] && [ "$W" = "$L" ] && echo "IN SYNC: $D" || echo "DRIFT dist=$D web=$W live=$L"
```

**Fix:** copy every HTML file that carries the bundle pointer, not just assets. `grep -rl`
the new hash across `dist/` (the SPA route shells under `dist/<route>/index.html` carry it too)
and `cp -p` each to the matching webroot path. Additive, no `--delete`, no Caddy reload.

**Rule:** PRODUCED ≠ DEPLOYED ≠ SERVED. Grepping an artifact proves it exists; grepping the
LIVE response proves it is served. Only the second one counts.

## Build-regenerated caches read from staleness, not from canon (PROVEN 2026-09-18)

`scripts/generate-md-mirrors.cjs` emits the agent-facing markdown mirror under
`public/makcikgpt-md/`. Its `convertBody(slug)` reads a CACHED `public/makcikgpt-md/{slug}.html`
— NOT the canonical `src/data/makcikgpt/{slug}.ts`. Edit the `.ts`, rebuild, and every `.md`
regenerates with a fresh timestamp containing the OLD body: the mirror looks updated (new mtime)
and is wrong (old content). Measured: 16 `.html` stale, 7 missing entirely.

This is the worst possible lane to leave stale — the bot lane is what AI crawlers and link
previews read, so unpatched text gets archived and ingested. Any `.html`-as-source cache in
this repo is a staleness trap: check `stat -c '%y'` on the cache against its `.ts` before
trusting any generated output.

`essays.json` cannot supply the body (it carries only id/title/date/series/dest/seal/
claim_register/source_ledger), so `scripts/lib/makcik-source.cjs` cannot route around it — the
fix is to read the `.ts` directly and mind the backslash-escape parsing of its template literal.

## WHO OWNS THIS FILE? — three writers, no coordination (PROVEN 2026-09-18)

Symptom: a curated page "keeps vanishing". Cause: three separate mechanisms claim
`public/<route>/index.html` and none knows the others exist.

1. `scripts/generate-agent-shells.cjs` — `writeRoute()` rewrites its routes on EVERY
   `prebuild`. It overwrote the 148 KB curated `/world/` hub with a 3.8 KB shell.
2. `scripts/copy-static-html.js` — the SPA injection loop writes the React shell into
   `dist/<route>/index.html` for every `SPA_ROUTES` entry, AFTER mirroring `public/`
   over it.
3. Caddy — `try_files {path} {path}/index.html /<route>/index.html /index.html =404`.
   It already prefers the static page. **The build destroys the file before the
   fallback can be reached.** Don't "fix" Caddy; fix the writers.

`dist/` is gitignored, so every overwrite leaves no diff and the page looks like it
vanished by itself. Always compare `public/` vs `dist/` vs webroot by SIZE and TITLE
before theorising.

Two registries must agree, and both mean "a human/agent curated this, the generator
must not own it":
- `PRESERVED_ROUTES` in `generate-agent-shells.cjs`
- `STATIC_INDEX_ALLOWLIST` in `copy-static-html.js`

### The cheap test that finds every instance

Serve a curated page and compare its `<title>` with `public/`:

```bash
curl -s -A "Mozilla/5.0" https://arif-fazil.com/<route> | grep -o '<title>[^<]*'
```

If the live title is the HOMEPAGE title but `public/<route>/index.html` has its own,
the curated page is not being served — the SPA shell is. That single check found
`/words/` (16.5 KB → 8.6 KB), `/work/` (10.1 KB → 8.6 KB) and `/world/makcikgpt/`
(42.1 KB / 30 slugs → 8.6 KB / 0 slugs) in one pass.

### Silent-drop filters

`e.lang === "bm"` dropped `lang: "en-bm"` entries from the MakcikGPT listing with no
error. A filter that hides an entry is worse than one that rejects it: rejection is
loud, hiding is invisible. Prefer `lang.split("-").includes("bm")` for SCOPE and let
the validator own validity.

Related: a sealed entry (`provenance_status: "sealed"`) with an empty `claim_register`
makes `loadMakcikSource()` THROW — the whole listing fails to generate, not just that
entry. Supply the witness chain; never weaken the gate.

## PUBLISH ORDER: asset first, reference second (PROVEN, twice-burned 2026-09-18)

Cloudflare caches a 404 for a hashed asset URL under `max-age=31536000, immutable`.
The `CLOUDFLARE_API_TOKEN` on this box has **no cache-purge permission** (`purge_cache`
returns `Authentication error`), so a poisoned URL stays broken for a year.

**Consequence for deploy order — never violate:**
1. Copy assets (js/css/images/pdf) to the webroot FIRST and confirm each resolves on disk.
2. THEN copy the HTML that references them.

Publishing the reference first is the trap. Caddy's `try_files {path} {path}/index.html
... =404` falls through to the SPA shell, the request 404s-then-serves-HTML, and CF stores
that HTML for the asset URL. Symptom: `curl -sI <asset-url>` shows
`content-type: text/html`, `cf-cache-status: HIT`. The file on disk is correct and complete —
it is only the cached response that is wrong.

**Recovery without purge permission — re-key the filename.** Give identical bytes a fresh
content-addressed name (`hero.c797f5c9.webp`), point the HTML at it, republish. A URL CF has
never seen cannot be poisoned. Do NOT retry the original URL and expect it to heal.

**This bit twice in one night:** once diagnosing another agent's build, once committing the
same mistake with WebP conversion. The `publish.sh` helper enforces the order; use it rather
than hand-rolling copies.

## Dual-lane UA routing — probe BOTH lanes (2026-09-17)

`/world/makcikgpt/*` serves **different bytes by User-Agent**: bot/crawler UAs
(`GPTBot|…|TelegramBot|HeadlessChrome|curl|wget`) get the markdown mirror root with a
terminal `/index.html` fallback = the **listing**; browser UAs get the React shell.

- A new article with no `makcikgpt-md/<slug>.md|.html` mirror therefore **200s the
  listing** — Telegram preview and crawlers see the wrong page while the author's browser
  looks fine. 200 ≠ correct content: grep a string unique to the article.
- **Your headless browser IS a bot** (`HeadlessChrome` is in the regex). Override with
  `cdp('Network.setUserAgentOverride', …)` before navigating, then verify
  `navigator.userAgent` — `Emulation.setUserAgentOverride` may not take effect.

Full detail, probe commands, and the og-tag/social-preview gap:
`references/dual-lane-ua-routing-pitfalls.md`.

## SERVED-TRUTH AUDIT — the artifact can be right while the pipeline is wrong (2026-09-20)

Trigger: *"is the site aligned with reality?"*, or Arif pastes an external AI's surface read and says
*"apply all the fix needed"*. Four probes, ~30 min, **no Caddy reload, no site rebuild** — all four are
artifact/service level and reversible.

**1. Sitemap sweep (catches an un-regenerated sitemap).**
```bash
curl -sS https://arif-fazil.com/sitemap.xml | grep -o '<loc>[^<]*' | sed 's/<loc>//' > /tmp/locs.txt
cat /tmp/locs.txt | xargs -P 10 -I{} sh -c 'printf "%s\t%s\n" "$(curl -sSL -o /dev/null -w "%{http_code}" {} --max-time 20)" "{}"' \
  > /tmp/status.tsv
awk -F'\t' '$1!="200"' /tmp/status.tsv        # must be empty
```
Found 43/63 entries returning 308/301 (route migrations ran, sitemap never regenerated) + 1 → 404.
Rewrite each `<loc>` to its post-redirect target; **drop** entries with no 200 target rather than
writing a 404 into the sitemap. Same treatment for `feed.xml` item links (`grep -c world/makcikgpt`).

**2. Fix the artifact, then find the generator that will undo it — the real fix is upstream.**
`scripts/lib/makcik-source.cjs` declares `CANONICAL_PREFIX = "/world/makcikgpt/"` and a parity test
enforces it, while Caddy 301s `/world/makcikgpt/*` → `/makcikgpt/`, and `prerender-articles.cjs`
uses a third prefix `/wealth/makcikgpt/`. Artifact-level canonicalisation is correct **for today's
served routes** and is still reverted by the next `npm run prebuild`. Record the disagreement and
make the namespace decision (build-canon vs routing-canon) explicit — it needs F13, because option
(b) requires a Caddy reload (T3, forbidden unnamed by the site's own AGENTS.md).

**3. Canonical-tag collapse.** Every SPA shell inherits the root `index.html` canonical unless the
route overrides it:
```bash
grep -rl '<link rel="canonical" href="https://arif-fazil.com/" />' sites/arif-fazil.com/dist --include=index.html | wc -l
```
Measured 87/236 — 77 MakcikGPT article pages + `/about` all declaring the homepage as their
canonical ("this page duplicates the homepage"). Fix belongs in the shell generator +
`copy-static-html.js`; it needs a rebuild + deploy, so it is its own decision, not a quick patch.

**4. Daemon source drift — a service can be `active` and doing nothing.**
```bash
systemctl status <svc> --no-pager | head -12          # 'active (running) since <old date>' = suspect
journalctl -u <svc> --no-pager | grep -c 'Error\|404'
```
`what-to-watch.service` had been `active` for 16 days while its journal showed HTTP 404 on **every**
5-minute tick — it read `institutional_signal.v1.json`, which was never deployed to the served root.
Two more defects sat behind the 404: a **fabricated** Brent (`gold price × 1.02`) compared against a
$70/bbl oil threshold and one fetch away from being written to VAULT999 tagged `OBS`, and a
`vitals.get("obs_facts", {}).get(...)` that crashes when the key exists but is `null`.

**Rules for any monitor that can write a ledger:**
- Every threshold reads a source that **resolves right now** — prove each URL, do not inherit a dead path.
- Fail-closed **per trigger**: an unavailable source is skipped and named in the log. Never proxy,
  default, or estimate a value into an `OBS`-tagged receipt.
- Index list-shaped data by **declared id**, never by position.
- Persist crossing state (`/var/lib/<svc>/state.json`) or every restart re-fires an already-crossed
  threshold — the ledger then records process restarts, not state transitions.
- `systemctl is-active` and `active since <date>` are not evidence the loop works. The journal is.

**Deliverable:** an append-only receipt — `forge_work/2026-09-20-site-repair/RECEIPT.md` — with each
fix, its probe, and the HOLDs separated from the DONE. Class the layer reached honestly:
**repo + served artifact**, not a kernel SEAL.

**Pitfall inside the audit:** do not write a literal `<loc>` inside an XML comment — `grep -c '<loc>'`
will count the comment and your count silently reads one high. Describe the element in words.

## Pitfalls — ARCHIVE

The pitfall history for this skill (`## Pitfalls` and `## Additional Pitfalls`, ~31 KB)
now lives in `references/pitfalls-archive.md`, extracted 2026-09-15 because this
SKILL.md had crossed the 100,000-char tool limit and could no longer be patched.

Load the archive when the inline notes here do not cover your situation — in particular
for the 2026-08-01 deploy/cron/Caddy trap set. Find your case with:

```
grep -n -i "<keyword>" <skill_dir>/references/pitfalls-archive.md
# useful keywords: cron, caddy, deploy, nav, redirect, cache, race, build, dirty
```

## Essays Zen Design

Arif's 888 analysis (2026-08-01) of `/writing` page identified 8 elements of chrome competing with writing. Level 2 zen (forge colors preserved, noise dropped) was selected: 206 lines → 62 lines. See `references/essays-zen-design.md` for the full pattern, code template, and verification steps.

## Homepage Zen Design

Same session (2026-08-01): Arif applied the same Level 2 principle to the homepage — "remove the chaos, align button map navigation key, make clock live and Malaysia time." Changes: dropped Kissinger QuoteCard (foreign voice), simplified ZenPulse from triple-question bar to clean status line, added live MYT clock component, single-column 640px layout throughout, consistent button spacing. See `references/homepage-zen-design.md` for the full pattern, LiveClock component template, and verification steps. When `npm run build` fails with `Type 'string | null | undefined' is not assignable to type 'string | undefined'`, the fix is to coalesce null to undefined: `errorInfo?.componentStack ?? undefined`. Discovered 2026-08-01: ErrorBoundary.tsx line 52 had this exact pattern — `?.` returns `null` not `undefined` on missing optional chain paths, and React state types expect `string | undefined`. **Fix:** append `?? undefined` to any optional chain expression feeding into a state type that expects `string | undefined`. **Audit:** `npm run build` after any component edit — TypeScript catches these at compile time before deployment. The SPA shell lives at `/var/www/html/arif/` (the standard dist sync target). When `try_files {path} /index.html` can't find the root directory, every article slug returns 404. **Diagnosis:** `ls /var/www/html/arif/makcikgpt/` → "No such file or directory" while `ls /var/www/html/arif/index.html` exists. **Fix:** change `root * /var/www/html/arif/makcikgpt` → `root * /var/www/html/arif` in the `handle /world/makcikgpt/*` block, then `sudo caddy reload`. The SPA shell is already at the standard dist path — no new directory needed. **Why this happened:** Caddy config assumed a separate webroot would be created and populated, but the deploy rsync only writes to `/var/www/html/arif/`. The mkdir+populate step was never automated.

23. **Static pages in webroot without Caddy handlers → silent 404.** A static `index.html` file existing in both `public/` and `/var/www/html/arif/` does NOT make it live — Caddy needs an explicit `handle /path/*` block with `file_server`. This was discovered 2026-08-01 when `/pulse/` and `/audit/` both returned 404 despite having valid files. **Fix:** add a static handler block matching the `/verify/` pattern:
    ```
    handle /pulse/* {
        root * /var/www/html/arif
        try_files {path} {path}/index.html /pulse/index.html
        file_server
    }
    ```
    **Audit:** `grep -n 'handle /<path>' /etc/caddy/Caddyfile` — every directory in `/var/www/html/arif/` with an index.html should have a corresponding handler.

24. **@spa_routes must stay in sync with App.tsx `<Route>` declarations.** If a Route exists in App.tsx but the path isn't in Caddy's `@spa_routes` list, the React component is built into the JS bundle but the Caddy SPA catch-all never fires — the route returns 404. Discovered 2026-08-01: `/institution/*`, `/compliance/*`, `/commodity/*` all existed in App.tsx but were missing from `@spa_routes`. **Fix:** add the missing paths to the `@spa_routes` line in `/etc/caddy/Caddyfile`. **Audit:** compare `grep '<Route path=' src/App.tsx` against `grep '@spa_routes' /etc/caddy/Caddyfile`.

25. **Legacy bot UA exclusions create redirect holes detectable by external witnesses.** When a redirect rule includes `not header_regexp User-Agent (?i)...curl...`, it blocks the redirect for bot/crawler User-Agents. This creates a soft-404 hole where `/wealth/makcikgpt/<slug>` returns the listing page (200) instead of redirecting — but ONLY for bots, making it invisible to browser-based testing. Discovered 2026-08-01: external witness (curl from sandbox) caught this. **Fix:** remove the `not header_regexp` condition so ALL User-Agents get the same redirect behavior. **Audit:** `grep -B2 'not header_regexp' /etc/caddy/Caddyfile` — every such exclusion is a potential drift between bot and browser behavior.

26. **Dist staleness = routes compile but don't reach users.** If `npm run build` hasn't re-run after adding new `<Route>` declarations in App.tsx, the routes exist in source but the deployed JS bundle doesn't contain them. The SPA shell loads (HTTP 200) but renders the wrong page. Discovered 2026-08-01: `/world/oil`, `/world/gas`, `/world/gold` had App.tsx routes and were in @spa_routes, but the 9-hour-stale dist bundle didn't include them → generic homepage shell served. **Fix:** `npm run build` + rsync dist to webroot. **Audit:** `stat -c '%y' dist/index.html` vs `git log --oneline -1` — if the dist is older than the last source commit that touched routes, the build is stale.

27. **Agent self-reports are not primary sources — trust your own probes over peer agents' claims.** When another agent (OpenClaw, Codex, Claude Code) reports state about the live system, their claim is a SELF-REPORT, not a primary source. Always re-probe independently. Discovered 2026-08-01: OpenClaw agent reported "/pulse/ and /audit/ serve SPA shell, not content" in 60+ duplicate messages over 3 hours despite both routes serving real static HTML (8,583B + 16,708B). The agent was in a loop reporting stale cached data. **Fix:** when a peer agent claims system state that contradicts your own observations, trust your own curl/grep/content-inspection probes. Agent self-reports are `[S]` (speculated) until independently verified. **Audit:** re-probe every claim from another agent before repeating it.

28. **write_file orphan recovery — fall back to terminal cat heredoc.** When `write_file` returns `[Orphan recovery: interrupted side-effecting tool may have executed; its effect is UNKNOWN]`, the file may or may not have been written. Do NOT retry with `write_file` — it will likely fail again for the same path in the same turn. **Fix:** fall back to `terminal` with a `cat > file << 'ENDOFFILE'` heredoc. This pattern is more reliable for the arif-fazil.com project environment. After the heredoc write, verify with `wc -l` and `grep` for expected content before proceeding to build. Discovered 2026-08-01 while rewriting Essays.tsx and Home.tsx.

29. **OpenClaw (AGI🦞) stuck-loop — don't engage, prove live state once, stop.** When OpenClaw enters a repeating loop of stale status reports (30-60+ identical messages over hours), it's running on cached data. Do NOT debate, explain, or argue with the loop. Prove the live state once with exact probe evidence (bundle hash, git HEAD, timestamp), then stop responding entirely. The loop may continue regardless — that's not your problem. Arif sees through these loops and will kill the agent himself. Discovered 2026-08-01: 60+ duplicate "Receipt sealed" messages over 30+ minutes while all work was already deployed and verified. **Fix:** one reply with bundle hash + git commit, then ⚒️ or silence.



## Site Cron Immune System (3 jobs max — F13 directive 2026-08-01)

Arif approved exactly 3 cron jobs for arif-fazil.com autonomous self-healing. See `references/site-cron-immune-system.md` for the full design: Sense (15m health probe), Verify (6h drift audit), Heal (6h auto-sync static files). Heal is gated on git working tree clean + web_zen doctor GREEN. Never: --delete, Caddy reload, npm build — all T3 territory requiring 888.

The Sense script is available as `scripts/arif-fazil-sense.sh` — deploy to `~/.hermes/scripts/` and wire as a `no_agent: true` cron job. It runs web_zen doctor, probes 6 organ subdomains + 17 SPA routes, checks git dirty state, and exits 0 silently on GREEN (no delivery), exits 1 on RED (triggers alert).

**web_zen TRUTH_MARKERS drift after content redesign (pitfall class, PROVEN 2026-08-01).** Sense reports YELLOW `missing_markers` even when routes are healthy when the `TRUTH_MARKERS` dict in `/root/arif-fazil.com/scripts/web-zen/web_zen.py` no longer matches live content. After a zen/redesign pass, bundle text changes and stale markers fail: `"Six missions"`/`"human cockpit"` left the rebuilt JS bundle, `"Five Organs"` became `"Organs"` in llms.txt. **Fix:** probe live content and update markers to strings that actually exist. Sub-pitfalls:
   - **SPA route markers are checked against the JS bundle** — web_zen auto-fetches `index-*.js` and searches markers there (F2 honesty, not just shell 200). Find valid markers: `curl -s "https://arif-fazil.com/assets/index-*.js" | grep -oP '.{0,15}Keyword.{0,15}'`.
   - **Redirect-shadowed URLs return the SPA shell, not the API.** `https://arif-fazil.com/wealth/gold/api/proxies` is shadowed by `redir /wealth /economics 301` + SPA catch-all → returns HTML, so marker `brent` fails; the real API is at `https://arif-fazil.com/gold/api/proxies` (JSON, `brent` present). **When a marker fails, verify the URL isn't shadowed by a redirect/handler ordering issue (grep Caddy for `redir /wealth` style rules, test sibling paths) before assuming content is broken.**
   - **Static files (llms.txt etc.)** — grep the live file first; markers must match actual content.
   After fixing markers, commit `web_zen.py` (Sense treats dirty repo as RED), then re-run `bash /root/.hermes/scripts/arif-fazil-sense.sh` — GREEN = silent exit 0.

## External Witness Verification

Arif independently verifies site state using curl probes from an external sandbox (no sovereign infra access). Treat external witness findings as authoritative — they carry higher epistemic weight than internal self-reports. When an external witness flags a drift, probe it, confirm it, fix it. Don't argue with it. The external witness cryptographically verified the observatory snapshot (ed25519 signature against DID key) — this is F2 TRUTH at a higher bar than infra-side probes can offer.

The `patch` tool refuses `/etc/caddy/Caddyfile` as a sensitive system path. Use `sed -i` via the `terminal` tool instead. **Always backup first, validate, then reload in-process.**

```bash
# 1. BACKUP (always first — F1 AMANAH)
cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak-$(date +%Y%m%d-%H%M%S)

# 2. PATCH with sed — use exact old_string/new_string
sed -i 's|EXACT OLD LINE|EXACT NEW LINE|' /etc/caddy/Caddyfile

# 3. INSERT new lines after a specific line number
sed -i 'LINENUMa\
\tindented line 1\
\tindented line 2' /etc/caddy/Caddyfile

# 4. DELETE lines (e.g., remove a legacy handler)
sed -i 'STARTLINE,ENDLINE d' /etc/caddy/Caddyfile

# 5. VALIDATE (never skip)
caddy validate --config /etc/caddy/Caddyfile

# 6. RELOAD (in-process, zero downtime)
caddy reload --config /etc/caddy/Caddyfile

# 7. VERIFY — probe the changed routes
for p in /changed-path/ /another-path/; do
  curl -sI -o /dev/null -w "${p} → HTTP %{http_code}\n" -m 3 "https://arif-fazil.com${p}"
done
```

**Key Caddy ordering rules:**
- **Caddy first-match-wins.** Static `handle /pulse/*` blocks MUST appear BEFORE `@spa_routes` in the file, otherwise the SPA catch-all shadows them.
- **`handle` blocks are ordered; `redir` directives sort before `handle`.** Bare `redir` directives execute before any `handle` blocks regardless of line position.
- **Bot UA exclusions (`not header_regexp`) create redirect holes.** If a redirect should apply to ALL clients, don't exclude bot User-Agents. External witnesses (curl from sandbox) will catch the drift.

**Common Caddy patches (copy-paste templates):**

### Add a static file_server handler
```
handle /pulse/* {
    root * /var/www/html/arif
    try_files {path} {path}/index.html /pulse/index.html
    file_server
}
```

### Add routes to @spa_routes
The `@spa_routes` line at ~line 702 controls which paths get the SPA shell. Add new paths at the end:
```
# Find current line:
@spa_routes path / /economics* /writing* /world* ...
# Append new paths:
@spa_routes path / /economics* /writing* /world* ... /newroute* /another*
```

### Canonicalize legacy paths (301 redirect)
```bash
# Add a named matcher + redirect for sub-paths
@mk_slug path_regexp mk_slug ^/makcikgpt/(.+)$
redir @mk_slug /world/makcikgpt/{http.regexp.mk_slug.1} 301
```

## Heal Cron Gate — Git Dirty State

The Heal cron job (`🜂 Heal — arif-fazil.com Self-Repair`) has a constitutional gate: **abort if `git status --porcelain` returns any output.** This prevents syncing half-committed state to the live webroot. When Heal reports "ABORT: git dirty":

1. Check what's dirty: `cd /root/arif-fazil.com && git status --short`
2. If it's routine telemetry (ns_live_telemetry.json, wealth archive data) → commit it: `git add sites/arif-fazil.com/public/data/ && git commit -m "chore(data): routine telemetry update"`
3. If it's real source changes → commit properly with a descriptive message
4. Heal will auto-fire on the next 6h cycle (15 */6 * * *)

**Pattern:** Dirty repo → Heal blocked → commit data → Heal runs next cycle. This is normal — the gate is working as designed.

**⚠️ Build-regenerated files: commit-once is NOT enough — .gitignore them.** (PROVEN 2026-08-01) `ns_live_telemetry.json` is regenerated by the npm `prebuild` script on EVERY build. Committing it once does not stop the dirty loop — the next build regenerates it with new content and Sense/Heal report "1 uncommitted file" again on every 15m cycle. The durable fix for any file the build regenerates with volatile content: add it to `.gitignore` (`echo "sites/arif-fazil.com/public/data/politics/ns_live_telemetry.json" >> .gitignore`) so it stops tripping the git-dirty gate entirely. Reserve "commit the telemetry" for genuinely one-shot data updates (result declarations), not for files the build churns every run.


## ABCD Framework Alignment

The Doctrine page (`/doctrine/`) is the canonical source for the ABCD framework:
- **A** = APEX Theory (four letters, grand equation, verdict lattice)
- **B** = Federation Body (9 organs, rings, roles, "Never:" rules)
- **C** = Constitution (F1–F13 floors)
- **D** = DITEMPA (sovereign compact, 000→999 pipeline)

### Zen Rule for Redundant Pages

If any page duplicates content already in ABCD, replace it with a redirect to the appropriate section. Example: `/organs/` was a static page listing 7 organs (less detail, stale tool counts). The Doctrine page already renders 9 organs with rings, roles, ports, and "Never:" rules (the B section). Fix: replace `public/organs/index.html` with:

```html
<meta http-equiv="refresh" content="0; url=/doctrine/">
<link rel="canonical" href="https://arif-fazil.com/doctrine/">
```

This preserves the URL, sets the canonical link, and sends users to the authoritative source.

**When to check:** Before adding any new standalone page, check if its content already exists within ABCD. If yes → redirect or supplement, never duplicate.

### BDX Content Architecture (MakcikGPT / civic intelligence surfaces)

| Layer | Role | Example |
|-------|------|---------|
| **B** — Body | Main article content | MakcikGPT article body |
| **D** — Discovery | Related articles, graph edges | "You may also need" |
| **X** — eXplore | Cross-domain navigation | Federation map, topic clusters |

Replaces traditional "article + sidebar + footer" with agentic content surface.

## Adding a new route-level page (not an essay)

Create a full-page dossier/landing/detail page (not a MakcikGPT article, not a data-driven essay). This is the pattern for geological dossiers, playbooks, or any standalone content page.

### Step 1: Create the page component

Create `src/pages/YourPage.tsx` with:
- `export function YourPage()` function
- `export const ssgOptions = { slug: "your-slug", routeUrl: "/earth/your-slug/" }` at the bottom
- Content structure: hero section, body sections (map over data or write inline), CTA section, footer linkback
- Use `motion.div` with framer-motion for scroll animations
- Set `document.title` and canonical link in `useEffect`
- Embed static assets (cross-section HTML, PDF) via `<iframe>` or `<a>` tags pointing to `/earth/your-asset`

```typescript
import { useEffect } from 'react';
import { motion } from 'framer-motion';

export function YourPage() {
  useEffect(() => {
    document.title = 'Your Title — Arif Fazil';
    document.querySelector('link[rel=canonical]')?.setAttribute('href','https://arif-fazil.com/earth/your-slug');
  }, []);
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="bg-forge-black min-h-screen">
      {/* Hero section */}
      {/* Body sections */}
      {/* CTA / GEOX launch */}
    </motion.div>
  );
}
export const ssgOptions = { slug: "your-slug", routeUrl: "/earth/your-slug/" };
export default YourPage;
```

### Step 2: Wire the route

In `src/App.tsx`:
```typescript
import { YourPage } from '@/pages/YourPage';

// In the <Routes> block, add after the parent listing route:
<Route path="/earth/your-slug" element={<YourPage />} />
<Route path="/earth/your-slug/" element={<YourPage />} />
```

Always add BOTH trailing-slash and no-trailing-slash variants. Always add `/{slug}` (underscore) as well if the user might type it.

### Step 3: Link from the parent listing page

In the parent page (e.g., `Discoveries.tsx`, `Earth.tsx`), add a section BETWEEN the listing content and the CTA:

```tsx
{/* ── YOUR DOSSIER LINK ── */}
<section className="py-16 border-b border-forge-iron">
  <div className="site-frame">
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      <div>
        <div className="section-label !mb-4">Category · Topic</div>
        <h2 className="text-4xl font-black uppercase italic mb-6">Your Title</h2>
        <p className="font-body text-forge-dim leading-relaxed mb-6">Summary text.</p>
        <a href="/earth/your-slug/" className="button-forge">Read the Dossier →</a>
      </div>
      <div className="bg-forge-steel p-6 rounded border border-forge-iron">
        <p className="font-technical text-[0.6rem] text-forge-dim uppercase mb-2">Preview</p>
        <p className="font-technical text-[0.7rem] text-forge-white">Key points...</p>
        <div className="mt-3 flex gap-2 text-[0.55rem] text-forge-dim">
          <span className="bg-forge-black px-2 py-1 rounded">Tag 1</span>
          <span className="bg-forge-black px-2 py-1 rounded">Tag 2</span>
        </div>
      </div>
    </div>
  </div>
</section>
```

### Step 4: Add static assets under public/

Cross-section HTML, PDFs, and images go under `public/earth/`:
```
public/earth/
├── your-slug-cross-section.html    ← iframe target
└── your-slug.pdf                   ← download link
```

Static files in `public/` are served directly by Vite → dist/ → web root. Embed them in the page via:
- `<iframe src="/earth/your-cross-section.html">` for interactive cross-sections
- `<a href="/earth/your-slug.pdf">Download PDF ↓</a>` for PDFs

### Step 5: Update llms.txt for agents (MUST be manual)

The build process does NOT auto-sync `public/llms.txt` changes to `dist/llms.txt`. After adding a new page:
```bash
# 1. Edit public/llms.txt with the new URL under ## Key Pages
# 2. Build (which may copy public/ → dist/ partially, but llms.txt is NOT always refreshed)
# 3. After deploy, manually ensure dist/ has the latest:
cp sites/arif-fazil.com/public/llms.txt sites/arif-fazil.com/dist/llms.txt
rsync -av sites/arif-fazil.com/dist/llms.txt /var/www/html/arif/llms.txt
```

**Pitfall:** llms.txt in `public/` is the SOURCE. But the npm build sometimes regenerates it from a template. After deploying, ALWAYS `curl https://arif-fazil.com/llms.txt | grep your-slug` to verify. If missing, re-copy the file.

### Step 6: Build and deploy

```bash
cd /root/arif-sites && bash scripts/deploy-site.sh arif-fazil.com --apply
```

### Step 7: Verify all endpoints

```bash
echo "=== Page ==="
curl -so /dev/null -w "HTTP %{http_code} (%{size_download} bytes)\n" https://arif-fazil.com/earth/your-slug/
echo "=== Parent listing ==="
curl -so /dev/null -w "HTTP %{http_code}\n" https://arif-fazil.com/earth/
echo "=== Static asset ==="
curl -so /dev/null -w "HTTP %{http_code}\n" https://arif-fazil.com/earth/your-asset.html
echo "=== llms.txt ==="
curl -s https://arif-fazil.com/llms.txt | grep -c "your-slug"
```

### Zen Navigation Pattern

The site follows the Three-Click Rule: no page is more than 3 clicks from the root (/). When adding a new deep page:

1. **Surface it on the listing page** — every `/earth/your-slug/` needs a card/link on `/earth/`
2. **Breadcrumb via section label** — each page has a `section-label` div (e.g., "Subsurface · Basin Intelligence") showing the user "where am I"
3. **Verbs over nouns** — navigation links use action verbs (Read, Explore, Launch, Download) not just nouns (Dossier, PDF, Cross-Section)
4. **CTAs form a connected journey** — each page leads naturally to the next: `/earth/` → `Read Dossier` → `/earth/slug/` → `Download PDF` → `Launch GEOX`

The 3-second answer pattern (from AGENTS.md §14.3) applies at page level: every user should know in 3 seconds "Where am I, why should I care, what can I do next."

#### Navigation Connectivity Audit — every page reachable (PROVEN 2026-08-01)

Arif's rule: **no page is an island.** "Week aku x jumpa website sendiriii… every pages tu need to be connected. Got link." He navigates by following links — if a page has no links back, he's stranded. Even deliberately-unlisted "sovereign door" pages (no nav-link, direct URL only, e.g. `/politics/shadow/`) still need an **exit path** to the rest of the site.

**Audit (run before declaring a site "done"):**
```bash
# Count outbound links per page — 0 or 1 link = dead end / island
for p in / /politics/ /politics/shadow/ /gold/ /writing/ /999/; do
  printf '%-22s %s links\n' "$p" "$(curl -s -m 10 "https://arif-fazil.com$p" | grep -oE 'href="[^"]*"' | wc -l)"
done
# Then verify every nav destination resolves 200
```

**Patterns that create islands (check these):**
1. **Defined-but-never-rendered nav data.** `civicLinks` (Gold/Election/Shadow/Pulse/Audit) existed in `src/data/siteContent.ts` for weeks but was never imported into `ConstellationFooter.tsx` — the "civic shelf — reachable from every page" comment was a lie. **Audit:** for every `export const *Links` array in siteContent.ts, `grep -rn 'civicLinks\|primaryLinks' src/components/` to confirm it's actually rendered. Data defined but unwired = the most common silent-connectivity bug.
2. **Static standalone pages with no nav.** Pages served by `file_server` (politics/, shadow/, gold/, oil/) don't get the React nav. Inject a small inline-styled nav bar right after `<body>` (dark `#0a0a0a`, monospace, links: Home · Politik·PRN · Gold · Wealth · World · Writing · Pulse · /999). `python3` regex injection into webroot files works fine.
3. **Webroot-only static pages get wiped by deploy rsync.** A static page that lives ONLY in `/var/www/html/arif/` vanishes on the next dist sync → 404 island. **Persist it in the repo:** `sites/arif-fazil.com/public/<path>/index.html` (Vite copies `public/` → `dist/` → webroot). Keep webroot and repo copies in sync (`cp repo_version webroot_version`) so a live fix doesn't silently drift from the deployed source.

**Verification:** after any nav change, walk the nav: `curl -s -o /dev/null -w '%{http_code}\n' -m 10 -L "https://arif-fazil.com$p"` for every link in the nav — all must be 200. Then count hrefs on the static pages (≥6 links each).

#### Editing the repo while FORGE (opencode/kimi-code) is live — sibling race (PROVEN 2026-08-01)

Kimi's FORGE session edits `/root/arif-fazil.com` concurrently with you. The `patch` tool warns `_warning: modified by sibling subagent … read the file before writing` — **heed it.** In this session, patching `ConstellationFooter.tsx` against a stale read duplicated the contact-nav block and left an orphaned JSX fragment (LSP errors: `Cannot find name 'item'`, missing closing tags). The build caught it; a `read_file` + targeted removal fixed it.

**Reconcile, don't re-patch — when the sibling ALREADY finished the job (PROVEN 2026-08-01, PRN16 final result).** If a `patch` call or script assert fails with `NOT FOUND` on an expected string, STOP hunting. The sibling may have already applied an equivalent change. Check order: (1) `stat -c '%y' <repo-file> <webroot-file>` — repo NEWER than webroot = sibling wrote to repo but the live copy is stale; (2) `git log --oneline -3`; (3) `diff <repo-file> <webroot-file>`. In the PRN16 update, the sibling had already updated the repo page (banner + 10 seat flips, repo mtime 12:55Z) while webroot served the pre-result build (12:46Z). Correct sequence: verify sibling's work is complete (`grep -c 'TOSS UP'` = 0, count expected flips) → **fix factual errors in sibling content before it goes live** (sibling banner said "Two-thirds majority (19 required)" — 19 is SIMPLE majority; 2/3 of 36 = 24 — arithmetic in political content must be re-derived, never trusted) → fill gaps the sibling missed (telemetry was still `ACTIVE_STREAMING_FLOW` → `RESULT_DECLARED` with final numbers, dual-write repo AND webroot per Pitfall #20) → `rsync -a <repo>/path/ <webroot>/path/` to resync the stale live copy → `curl` live URL + grep new markers → `git add` + commit your reconciliation. Never re-patch content a sibling already wrote correctly — you clobber their work. Full session recipe: `references/ns-election-result-update-2026-08-01.md`.

**Rules when the sibling warning fires:**
1. `read_file` the target immediately before patching — never patch from memory of the file.
2. After patching, run `npm run build` (or check LSP diagnostics from the patch tool) — the duplicate-fragment failure mode is silent until compile.
3. A diff that shows BOTH your lines AND the sibling's lines in the same region means a merge collision — clean it manually rather than re-patching.
4. Commit YOUR files explicitly (`git add <specific paths>`) so the sibling's in-progress work stays uncommitted and unclobbered.
5. `rsync dist/` while the sibling is mid-build produces "file has vanished" warnings (exit 24) — verify the deployed bundle hash matches YOUR build before calling it done.

## Arif's Design Preferences for MakcikGPT / Civic Surfaces

These are **established preferences** for the MakcikGPT site and any civic-journalism surface on arif-fazil.com. Embed them in future designs without asking.

### Palette: Primer (red, blue, yellow) — DARK MODE ONLY

"Primer colour" = **red, blue, yellow** — the primary colours. NOT GitHub's Primer design system.

| Role | Hex | Usage |
|------|-----|-------|
| Red | `#e0301e` | Energy series, accent, quote shadow |
| Blue | `#1f3fd4` | Governance series, hover states, selection highlight |
| Yellow | `#f2b705` | Tech series, highlights |
| **Dark bg** | `#0a0a0a` | Page background (NOT cream/paper — "sakit mata terang sangat") |
| Card bg | `#1a1a1a` | Card/surface backgrounds |
| Alt bg | `#111111` | Secondary surfaces (hero canvas, alt sections) |
| Hover bg | `#242424` | Hover states |
| Border | `#2a2a2a` | Subtle borders |
| Text | `#f0f0f0` | Primary text |
| Muted | `#9a9a9a` | Secondary text, timestamps |
| Subtle | `#666666` | Tertiary text, faint labels |

**⚠️ DARK MODE ONLY — confirmed 2026-07-31.** Arif said light/cream background "sakit mata terang sangat" (hurts eyes, too bright). Never use cream/paper backgrounds. All MakcikGPT surfaces must be dark.

CSS tokens (the canonical set):
```css
:root{
  --bg:#0a0a0a; --bg-alt:#111111; --bg-card:#1a1a1a; --bg-hover:#242424;
  --border:#2a2a2a; --border-light:#1e1e1e;
  --fg:#f0f0f0; --fg-muted:#9a9a9a; --fg-subtle:#666666;
  --red:#e0301e; --blue:#1f3fd4; --yellow:#f2b705;
  --body:'Inter',sans-serif; --mono:'JetBrains Mono',monospace;
}
```

### Theme: Dark Fractal Editorial

- **Entire page is dark** (`#0a0a0a` background). Hero, body, cards, quote box — ALL dark. NOT cream/paper.
- **Hero canvas:** animated fractal particle field on `#111111` background, particles in Primer colours (red/blue/yellow). Subtle connecting lines between nearby particles.
- Cards with **subtle borders** (1px solid `#2a2a2a`), rounded corners (10px), box-shadow on hover (`0 8px 24px rgba(0,0,0,.4)`)
- Archivo Black for display, Space Grotesk for body, JetBrains Mono for code/mono
- Stats bar: dark cards in a grid, each stat number in a Primer colour (red/blue/yellow)
- Series cards: dark cards, each with a coloured accent label (red=Energy, blue=Governance, yellow=Tech, etc.)
- Quote box: dark card, yellow left-border (4px solid), white text

### Zen rule

The MakcikGPT site is a **Decide/Learn surface** — content-first layout: hero (fractal canvas) → stats → quote → latest → series → full index with search. Mathematical/decorative elements (fractals, Mondrian, Sierpinski) ARE part of the identity — they stay. "Zen" means content hierarchy, not minimalism stripped of character.

### Human-Readable Labels (CRITICAL)

**Never show machine codes (`M1`, `M2`, `M3`, `M4`, `M5`) in the user interface.** Humans need cognitive clarity. Use the actual series names instead.

**Series code → Human label mapping:**
- `M1` → **ENERGY**
- `M2` → **GOVERNANCE**
- `M3` → **TECH & SOVEREIGNTY**
- `M4` → **ECONOMY**
- `M5` → **POLITICS**

**Where this applies:**
- Series card headers (the big label at the top of each card)
- Article list chips/badges (category label next to each article title)
- Any filter UI or category display
- Breadcrumbs, navigation, metadata displays

**Internal data keys stay as `M1`/`M2`** — those are for JavaScript filtering and CSS class targeting. The UI must speak human language, not machine codes.

**Implementation pattern:**
```javascript
// SERIES data uses machine codes as keys
const SERIES = {
  M1: { name: "Energy", desc: "PETRONAS, oil, gas, rightsizing" },
  // ...
};

// UI rendering uses the human-readable name
sEl.innerHTML = Object.entries(SERIES).map(([k, v]) =>
  `<div class="scard" data-s="${k}">
     <div class="fk">${v.name.toUpperCase()}</div>  ← Show "ENERGY", not "M1"
     <p>${v.desc}</p>
   </div>`
).join('');

// Article chips also use the name
idxEl.innerHTML = rows.map(a =>
  `<span class="chip ${a.s}">${SERIES[a.s].name}</span>`  ← Show "Energy", not "M1"
).join('');
```

This rule is non-negotiable. Machine codes create cognitive load for human readers. Names create clarity.

### Deploying the MakcikGPT landing page (standalone HTML)

⚠️ **CRITICAL ARCHITECTURE — DO NOT replace the source file and run deploy.** The source `sites/arif-fazil.com/makcikgpt/index.html` is the **React SPA shell** (Vite entry point), NOT a standalone landing page. The deploy script's Phase 3 regenerates `public/makcikgpt-md/index.html` from `src/data/essays.json` via `scripts/generate-makcik-index.cjs`. If you replace the source file and run deploy, the build will OVERWRITE your changes.

**The Caddyfile routes `/makcikgpt/` to `/var/www/html/arif/makcikgpt-md/index.html`** — this is the actual file being served for the landing page, NOT the source file.

#### To directly replace the landing page with a standalone HTML file (bypass React build):

```bash
# 1. Backup the current live file
cp /var/www/html/arif/makcikgpt-md/index.html /var/www/html/arif/makcikgpt-md/index.html.bak

# 2. Replace the live file directly (Caddy serves from here for /makcikgpt/)
cp /path/to/standalone.html /var/www/html/arif/makcikgpt-md/index.html

# 3. Verify
curl -s -o /dev/null -w "HTTP %{http_code} - %{size_download} bytes\n" https://arif-fazil.com/makcikgpt/
```

**⚠️ CRITICAL LIMITATION — React SPA overrides navigation from the homepage.** The standalone HTML file is only served on DIRECT page loads (new tab, URL bar, hard refresh). When a user navigates FROM the main homepage (`arif-fazil.com/`) by clicking a link to `/makcikgpt/`, the React SPA intercepts the navigation client-side and renders its built-in MakcikGPT component — which uses whatever design was compiled into the JS bundle. This means: **users who click through from the homepage will see the old design, not your standalone HTML.** Only direct access shows the new file. This is NOT a cache issue. The permanent fix is to update the React component and rebuild the app. See Pitfall #18.

#### To restore the auto-generated landing page (undo the standalone replacement):

```bash
# Re-run deploy which regenerates makcikgpt-md/index.html from TS source
cd /root/arif-fazil.com && bash scripts/deploy-site.sh arif-fazil.com --apply
```

#### To modify the auto-generated landing page STYLING (not content):

The landing page template is generated by `scripts/generate-makcik-index.cjs`. Edit the template string in that script, then rebuild. Do NOT edit `public/makcikgpt-md/index.html` directly — it's overwritten on every build.

#### Backup note

The deploy script auto-creates a backup before replacing the source file. But the LIVE file at `/var/www/html/arif/makcikgpt-md/index.html` is the one that matters — always back it up separately before making changes.

## Caddyfile Patching Workflow

The `patch` tool refuses `/etc/caddy/Caddyfile` as a sensitive system path. Use `sed -i` via the `terminal` tool instead. **Always backup first, validate, then reload in-process.**

```bash
# 1. BACKUP (always first — F1 AMANAH)
cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.bak-$(date +%Y%m%d-%H%M%S)

# 2. PATCH with sed — use exact old_string/new_string
sed -i 's|EXACT OLD LINE|EXACT NEW LINE|' /etc/caddy/Caddyfile

# 3. INSERT new lines after a specific line number
sed -i 'LINENUMa\
\tindented line 1\
\tindented line 2' /etc/caddy/Caddyfile

# 4. DELETE lines (e.g., remove a legacy handler)
sed -i 'STARTLINE,ENDLINE d' /etc/caddy/Caddyfile

# 5. VALIDATE (never skip)
caddy validate --config /etc/caddy/Caddyfile

# 6. RELOAD (in-process, zero downtime)
caddy reload --config /etc/caddy/Caddyfile

# 7. VERIFY — probe the changed routes
for p in /changed-path/ /another-path/; do
  curl -sI -o /dev/null -w "${p} → HTTP %{http_code}\n" -m 3 "https://arif-fazil.com${p}"
done
```

**Key Caddy ordering rules:**
- **Caddy first-match-wins.** Static `handle /pulse/*` blocks MUST appear BEFORE `@spa_routes` in the file, otherwise the SPA catch-all shadows them.
- **`handle` blocks are ordered; `redir` directives sort before `handle`.** Bare `redir` directives execute before any `handle` blocks regardless of line position.
- **Bot UA exclusions (`not header_regexp`) create redirect holes.** If a redirect should apply to ALL clients, don't exclude bot User-Agents. External witnesses (curl from sandbox) will catch the drift.

**Common Caddy patches (copy-paste templates):**

### Add a static file_server handler
```
handle /pulse/* {
    root * /var/www/html/arif
    try_files {path} {path}/index.html /pulse/index.html
    file_server
}
```

### Add routes to @spa_routes
The `@spa_routes` line at ~line 702 controls which paths get the SPA shell. Add new paths at the end:
```
# Find current line:
@spa_routes path / /economics* /writing* /world* ...
# Append new paths:
@spa_routes path / /economics* /writing* /world* ... /newroute* /another*
```

### Canonicalize legacy paths (301 redirect)
```bash
# Add a named matcher + redirect for sub-paths
@mk_slug path_regexp mk_slug ^/makcikgpt/(.+)$
redir @mk_slug /world/makcikgpt/{http.regexp.mk_slug.1} 301
```


## Additional Pitfalls — ARCHIVE

See `references/pitfalls-archive.md` (second section) for the 2026-08-01 session pitfalls.
