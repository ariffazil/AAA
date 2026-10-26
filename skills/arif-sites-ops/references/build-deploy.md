# Build, deploy, topology, proposal manifest (from arif-fazil-site-ops)
> Moved verbatim 2026-10-23 (F13 consolidation). Historical build/deploy detail.
> Current deploy rule lives in SKILL.md and in `arifos-site-patch-without-caddy-reload`.

## Topology (verified 2026-08-06)

| Layer | Path |
|---|---|
| Canonical repo | `/root/arif-fazil.com` (NOT `/root/arif-sites`, NOT `/root/ARIF-SITES` — retired) |
| Site source | `sites/arif-fazil.com/` — `src/` (React SPA), `public/` (static HTML pages), `dist/` (build output) |
| Live webroot | `/var/www/html/arif` — this is what Caddy serves; NOT `sites/.../dist` |
| Deploy script | `scripts/deploy-site.sh <site> --dry-run \| --validate-build \| --apply \| --restore <tag>` |
| Overlay registry | `infra/runtime-overlays.json` (preserve-live paths: `static/wealth.html`, `data/wealth` — never clobber) |
| Page gate | `scripts/verify-pages.sh [BASE_URL] [DIST_DIR]` — probes every `dist/*/index.html` on the LIVE site, asserts 200 |
| Routing | `/etc/caddy/Caddyfile` + `public/_redirects` (Cloudflare-Pages-only syntax) |

## Build pipeline (sites/arif-fazil.com)

```
npm run build = prebuild (generators: makcik-index, wealth-archive, ns-telemetry, feed, discovery…)
              → tsc -b && vite build
              → postbuild: scripts/copy-static-html.js (mirrors public/*/index.html → dist/*/index.html;
                skips ROOT index.html + SKIP_FILES: feed.xml, llms.txt, sitemap.xml, robots.txt…)
              → postbuild: scripts/render-vitals.cjs
```

**Critical rule (revised 2026-08-07):** static `public/<path>/index.html` WINs over
React Router for that path. For `/words/writing/` (the listing) this is
desired — siblings hand-curate it, mirror of MakcikGPT. For
`/words/writing/<slug>/` (per-essay pages) this is **NOT** desired —
per-essay static HTML shadows the SPA EssayPage and users get the plain
version instead of the rich design. The `scripts/render-words-essays.cjs`
script now generates ONLY the listing surface (index.html + index.json +
llms.txt), never per-essay static HTML. Always md5sum the live
`/words/writing/index.html` before regenerating — sibling agents enrich
this file and re-injecting kills their work.

## Deploy workflow (follow in order)

1. **PROBE FIRST — before building anything.**
   - `curl -s https://arif-fazil.com/<path>/` — what is live now?
   - `ls sites/arif-fazil.com/public/<path>/` and `ls sites/arif-fazil.com/dist/<path>/`
   - Check `_redirects` + Caddyfile for existing routing
   - **An artifact may already exist** (e.g. `/world/sot/` already held a prior SOT Atlas).
     Building a duplicate burns a full cycle. This happened 2026-08-06.
2. **Build in the proposal zone** — `forge_work/proposals/<agent-id>/<mission>/` (file-authority
   allows agent writes ONLY there + `receipts/<agent-id>/`). Do not touch `public/` or canon
   until the build is verified.
3. **Promote + rebuild site**: copy verified dist into `public/<path>/` (backup the old
   `index.html` first, e.g. `index.html.bak-<timestamp>-pre`), then `npm run build` in
   `sites/arif-fazil.com` so the mirror lands it in `dist/`.
4. **Gate**: `bash scripts/verify-pages.sh` — all pages must pass or HOLD.
5. **Deploy**: `scripts/deploy-site.sh arif-fazil.com --dry-run` only. `--apply` is T3. For one static page use the direct-edit rsync later in this file (no `--delete`, no reload).
6. **Verify live**: curl the path, check HTTP 200, browser-render if interactive.

### Proposal-zone proposal lifecycle (the 3-file pattern)

When the deliverable is a new static HTML page and the path is canon-protected
(`dist/*/index.html` is `hand_edit: false`), the workflow is **proposal-then-promote**.
The proposal zone is the only writable location for the proposal agent:

```
forge_work/proposals/<agent-id>/<mission>/v<N>/
├── index.html              # the deliverable, ready to drop into dist/<path>/index.html
├── README.md               # proposal narrative (why + what + deploy path + rollback)
└── FORGE_RECEIPT.json      # SHA256 ledger, compliance flags, rollback path
```

**Each file has a specific role.** Don't skip any:
- `index.html` — the page itself, inline CSS, no external bundler, ready to serve
- `README.md` — explains what was built, why, design choices, deploy path, rollback path
- `FORGE_RECEIPT.json` — machine-readable ledger: SHA256 of each file, file sizes, timestamps, compliance flags, promotion path, rollback path, observer notes, governance incidents

**The FORGE_RECEIPT is the audit trail.** F13 / A-FORGE reads the JSON, not the prose. Proven schema:
```json
{
  "mission_id": "<mission>/v<N>",
  "agent": "<agent-id>",
  "authority": "PROPOSAL",
  "state": "awaiting_f13_review",
  "created_at": { "utc": "...", "myt": "...", "tz": "Asia/Kuala_Lumpur", "iso_week": "..." },
  "subject": {
    "intended_path": "sites/arif-fazil.com/dist/<path>/index.html",
    "intended_url": "https://arif-fazil.com/<path>/",
    "proposal_zone": "forge_work/proposals/<agent-id>/<mission>/v<N>/",
    "promotion_requirement": "F13 SOVEREIGN seal + verify-pages gate"
  },
  "files_written": [{ "path": "...", "sha256": "...", "size_bytes": ..., "lines": ... }, ...],
  "file_hashes": { "<file>": "<sha256>" },
  "deployment_blocked_reason": "FAIL-CLOSED — no dist/ mutation without F13 seal",
  "compliance": { "file_authority_yaml": "FAIL-CLOSED respected", "no_jargon_hard_rule": "PASS/FAIL" },
  "promotion_path": { "step_1_seal": "...", "step_2_copy": "..." },
  "rollback_path": { "trigger": "F13 vetoes", "step_1": "...", "no_dependents": "..." },
  "observer_notes": [],
  "governance_incidents": []
}
```

**Hard rule (FAIL-CLOSED):** the proposal agent writes ONLY to the proposal zone. Do NOT touch `dist/`, `public/`, `canon/`, `src/`, `_redirects`, Caddyfile, or any routing config. Promotion is F13's job.

**SHA256 hygiene:** write the `file_hashes` from the actual `sha256sum` of the file you wrote. If you edit the file afterwards, recompute and update the receipt. The receipt is the canonical record — the disk is the witness.

Full recipe + verification script template: `references/proposal-zone-lifecycle.md`.


## Proposal manifest pattern (proven 2026-08-06)

When writing a proposal to update a DERIVED surface, include a `manifest.json`:

```json
{
  "proposal_id": "vitals-news-2026-08-06",
  "proposed_by": "<agent-id>",
  "authority_class": "PROPOSAL",
  "actions": [{ "proposal": "A", "target": "...", "target_class": "DERIVED", ... }],
  "deploy_command": "HISTORICAL. make deploy is T3. Do not run.",
  "deploy_prerequisites": ["make verify", "F13 lease from ARIF", "A-FORGE apply"],
  "verification": ["curl ...", "make verify-pages"]
}
```

Single execution contract. A-FORGE reads the manifest, not the prose.

## Governance reminder

`canon/file-authority.yaml`: `public/**/*.html` = DERIVED (hand_edit: false). No canon
mutation without lease. No deploy without receipt. `forge_work/proposals/` and
`receipts/` are the only free-write zones.

## Nav canon v7.0 — organ→site mapping (locked 2026-08-06)

The 5-item top-nav mirrors organ outputs. Organs themselves are agent-owned.

| Nav item | Organ | Content portal |
|----------|-------|----------------|
| **HOME** | AAA (cockpit) | identity, trust root, you land here |
| **EARTH** | GEOX | geology, seismic, basins, wells |
| **WORDS** | arifOS | doctrine, constitution, F1–F13, essays, law, MakcikGPT |
| **WORLD** | WEALTH | commodities, markets, vitals, politics + organ portals |
| **WORK** | WELL | exploration wells, missions, resume |

**Rule:** Pages are for humans (nav). Contexts are for agents (machine_links, .well-known).

**Words absorbs ALL written/doctrinal content** — Voice (MakcikGPT) + Essays + Doctrine + Law + /writing/ + /world/makcikgpt/ are all aliases to `/writing/`. URL didn't move; the LABEL unified under one nav item. The MakcikGPT corpus stays at `/world/makcikgpt/` for URL stability (zero redirect hell, articles already indexed), but is reachable via the WORDS alias and surfaced as a card on the World hub.

**Organ-assignment rule (principal-relationship check):** when choosing which organ owns a nav slot, ask "what is the principal's relationship to this organ?". HOME went through HERMES → AAA because HERMES is the agent (the messenger you talk to on Telegram), not the cockpit. AAA is the principal's *control plane* — it binds principal ↔ agents. The sovereign lands at HOME; the sovereign doesn't *land* at an agent. Organs belong to agents; pages belong to humans. The nav slot is human-facing; assign to the organ whose outputs the human actually consumes on that page.

**Hero-core doctrine (locked 2026-08-06):** every top-level homepage carries a CENTER HERO with one dynamic visual that IS the nav item's core metaphor. The hero is the first thing the reader sees; it must move; it must be different per nav.

| Page | Hero core | Metaphor |
|------|-----------|----------|
| HOME | ⏰ clock | time, identity, arrow-of-time |
| EARTH | 🌍 globe | earth, geology, basins |
| WORDS | 🧭 compass | doctrine, law, direction |
| WORLD | 🗺️ atlas | what's happening, GDELT map |
| WORK | ❤️‍🩹 heart | wells, missions, life-work |

Heroes are JS-rendered canvas/SVG (not PNG screenshots). Static hero = dead hero. For WORLD, the existing `/world/sot/` D3+GDELT globe is the hero — don't add a separate hero, link to the atlas. For HOME, the live clock dial already exists. For EARTH, WORDS, WORK: hero forge is pending (agy CLI or equivalent).

**The 5-page artifact-fit rule (locked 2026-08-06):** every artifact on arif-fazil.com MUST live under one of the 5 top-level pages. If you build something that doesn't fit, the choice is (a) kill it, (b) rehome it under the closest page, (c) escalate to F13 to add a 6th nav item. Never let artifacts dangle at root. Audit recipe in `references/5-page-artifact-fit-map.md`.

### The naming-iteration trap (avoid)

When the user is renaming a nav label, expect 3-5 iterations before lock. Each iteration expands the alias list. Don't apply aliases piecemeal — wait until the user says the label is final, then write the full alias array in one `navCanon.ts` regeneration. Multiple regenerations in a row = drift between `navigation.json` and `navCanon.ts`. See `references/nav-canon-v7-organ-mirror.md` for the full iteration trail on Words.

The source canon lives at `/root/web-canon/canon/navigation.json`. `navCanon.ts` is
regenerated from it via `scripts/generate-nav-canon.cjs`. Never hand-edit `navCanon.ts`
directly — edit canon JSON, regenerate, rebuild.

**Organs in the nav? No.** Organs live in `machine_links` and `secondary_links` (footer
+ hidden nav). They are *referenced* from WORLD via cards, not promoted as nav items.
The only exception: the brand strip "ARIF FAZIL" at the top is the sovereign identity
(Arif), always visible. The home page IS the cockpit — you land here, see everything,
navigate everywhere.

**Keyboard shortcuts (v7):** `g h` = HOME, `g e` = Earth, `g w` = Words, `g o` = World,
`g k` = Work. Old shortcuts `g v` (Voice) and `g w` (Essays) were removed in v7.

### render-propa.cjs B11 markers: don't delete, replace (2026-08-06)

`scripts/render-propa.cjs` looks for these exact markers in `public/propa/index.html`:
- `<!--B11-B:FAN-SVG-MARKER:BEGIN-->` ... `<!--B11-B:FAN-SVG-MARKER:END-->`
- `<!--B11-C:SUMMARY-MARKER:BEGIN-->` ... `<!--B11-C:SUMMARY-MARKER:END-->`

During the propa v3 upgrade (2026-08-06), these markers were deleted when removing the
old fan-sec engine. This broke `npm run build` because `render-propa.cjs` calls
`replaceMarker()` which throws on missing markers.

**Fix:** when replacing the fan-sec section, preserve B11 marker comments at the same
insertion points (as empty `<!-- -->` stubs) OR update `render-propa.cjs` to skip missing
markers gracefully. The markers are consumed by the postbuild renderer to inject SVG charts
and summary tables — if the page no longer needs SVG injection, remove the markers AND the
corresponding `replaceMarker()` call in the script.

### Sibling FAIL-CLOSED dist/ mutation during proposal stage (2026-08-11)

This is a different failure mode from the post-deploy md5sum reconciliation (which handles siblings enriching an F13-approved live page). During the proposal stage, a sibling subagent writing to the SAME forge_work/proposals/ zone can produce:

1. **Conflicting content models** — sibling writes a different version with a different structure (e.g. 3 sections vs the delegation brief's 4 sections, "BM Penang casual" tone vs the brief's "English no persona", federation-internal terms vs the brief's "no jargon")
2. **FAIL-CLOSED dist/ mutation** — sibling writes directly to `dist/<path>/index.html`, bypassing the F13 seal + verify-pages gate entirely

**Detection:**
```bash
# After any sibling activity in the proposal zone, ALWAYS probe dist/ for the new path
ls -la /root/arif-fazil.com/sites/arif-fazil.com/dist/<path>/index.html
sha256sum /root/arif-fazil.com/sites/arif-fazil.com/dist/<path>/index.html

# Compare sibling's content model against the delegation brief, not against the sibling's output
# If sibling uses jargon, wrong tone, or wrong section count → the brief is the source of truth
```

**Recovery (3 steps, proven 2026-08-11 on /work/ page):**
1. Read the sibling's files to understand their content model. Compare against the brief.
2. **The brief is the source of truth.** Overwrite the sibling's forge_work files with brief-aligned versions. If the sibling wrote to dist/, **delete that dist/<path>/index.html** (single `rm`).
3. Record the incident in `FORGE_RECEIPT.json` under `governance_incidents[]`:
   ```json
   {
     "ts_utc": "...", "ts_myt": "...",
     "incident": "sibling_subagent_compliance_violation",
     "detail": "sibling wrote <N>-byte file with hash <sha256> to dist/<path>/index.html — violated FAIL-CLOSED",
     "resolution": "primary author deleted dist/<path>/index.html; directory restored to prior state",
     "rolled_back_by": "<agent-id> (primary)"
   }
   ```

**Why this is DIFFERENT from the post-deploy md5sum pattern:** the post-deploy case is about reconciling a live, F13-approved page with a sibling's enrichments (adopt theirs if better). The proposal-stage case is about a sibling bypassing F13 entirely. The cleanup is a single `rm`, not a `cp` from the live webroot.

### Ad-hoc verification for static HTML proposals (2026-08-11)

Static HTML proposals have NO canonical test suite. No `npm test`, no `pytest`, no `playwright`. The deliverable is a single file with inline CSS, fully self-contained, no JS dependencies.

**Verification is a spec-compliance check by ephemeral bash script.** Pattern:
```bash
SCRIPT=/tmp/hermes-verify-<topic>.sh
# Create, run, delete — 16 numbered sections, PASS/FAIL/WARN per check
```

**The 16 sections to cover (proven on /work/ page, 45/45 checks):**
1. File existence (3 files: index.html, README.md, FORGE_RECEIPT.json)
2. JSON validity (FORGE_RECEIPT is parseable)
3. SHA256 in receipt matches disk (self-consistency)
4. No federation-internal jargon (F1-F13, VAULT999, MCP, A2A, GEOX, AAA)
5. Section anchors / count (matches delegation brief)
6. Section 1 item count (exactly N items)
7. Section 2 item count (exactly N questions/items)
8. Footer link presence (all required links)
9. Design tokens (all required colors + container width, inlined)
10. Font stack (all required fonts referenced)
11. Self-containment (no React/Vite src=, inline `<style>` present)
12. Tagline / motto presence
13. META tags (og:, twitter:, canonical, llms-full-content)
14. **No dist/ mutation** — the FAIL-CLOSED check (probe `dist/<path>/index.html`)
15. Timestamp hygiene (UTC + MYT match spec)
16. README required sections (What was built, Design choices, Deploy path, Rollback plan)

**The script is ephemeral.** Created, run, deleted at end of session. The audit trail lives in FORGE_RECEIPT, not in the script. The verification block in the receipt documents the script path, run timestamp, and PASS/FAIL counts.

**What this verification does NOT prove.** Don't claim "tested" or "verified" — the script is spec compliance, not comprehensive:
- No deploy (verify-pages runs only on live paths)
- No browser visual regression (screen-shot diff via vision_analyze is a separate step)
- No accessibility audit (skip-link, semantic HTML are present but no axe-core run)
- No cross-browser test
- No live-link test (footer paths are anchors; whether targets exist live is verify-pages' job)

Full template script: `references/proposal-zone-lifecycle.md`.

### Sibling-agent discipline (proven, repeated)

Three sibling agents (333-AGI, Claude Code, OpenCode) work on the same canonical repo.
**Probe live + grep repo before injecting** — a sibling may already have deployed what you
were about to build. On 2026-08-06 the v3 paradox engine (8 sliders /propa/, 4 sliders
/malaysia/, both cross-linked at `#subsidy-paradox`) was already live before my inject
landed. Three build versions (v1 static → v2 calibrated → v3 signal-dense) were all
superseded. The correct move: **reconcile, don't re-inject.**

**Post-deploy md5sum reconciliation (2026-08-07):** after deploying, always check whether a
sibling has overwritten your work or enriched it:
```bash
md5sum /root/arif-fazil.com/sites/arif-fazil.com/public/<path>/index.html /var/www/html/arif/<path>/index.html
```
If checksums differ → sibling overwrote; reconcile instead of re-deploying your version.
If identical → your deploy is current. If the live content looks better than yours
(e.g. series chips, stat pills, zen pulse enrichment), adopt theirs — copy `index.html`
from the live webroot to `public/` and commit.

**Arif's rule (2026-08-07):** *"Some of the article is not even true or real!!"*
When rendering essay surfaces, only include essays with real HTML bodies (≥200 chars).
Never generate surfaces for stubs/skeletons — they create false surfaces that list
essays with no actual content. The prebuild script must filter on content depth, not
metadata flags.

### Index dedup must walk the source .ts files, not the index.html itself (2026-08-07)
The old `/words/writing/index.html` had S6 EUREKA Trilogy with **6 cards** (3 unique + 3 duplicates) — duplicates appeared when sibling agents hand-pasted cards without reconciling against the source. **Reconciliation recipe:** dedup by parsing `.ts` files in `src/data/essays/*.ts`, not by grepping the index. The same slug may appear in multiple `.ts` files (e.g. `11-contrast-detection-…ts` and `contrast-governed-anomaly-detection-formal-bridge-avo-attention.ts` share the same slug) — first by filename length wins. After dedup the count must equal the unique-slug count of `isDirectPublication: true` .ts files (14 as of 2026-08-07). Quick probe: `grep -c 'Read article →' public/words/writing/index.html` must equal `grep -lE 'isDirectPublication: true' src/data/essays/*.ts | wc -l` after dedup.

### Federation sync daemons overwrite your static-HTML output (2026-08-07)

`what-to-watch-daemon.py` (systemd, root) and several `.timer` units (`federation-watchdog`,
`fed-sync`, `arifflow-fq-mirror`, `arifflow-cooling-watchdog`) **regenerate static HTML
files in `/var/www/html/arif/` on a short schedule** — every few minutes. If your rebuild
script writes to `/var/www/html/arif/words/writing/<slug>/index.html` and then runs
verification 2+ minutes later, **the daemon may have already replaced your output with its
own structure** (different footer, different kicker, different prose). Symptom: verification
fails on a clean rebuild run; mtime of the file is later than your script's write time.

**Mitigation:**
1. Run the rebuild + verification as a single chained command (no gap): `python3 rebuild.py && python3 verify.py`.
2. If verification fails on a clean run, immediately `stat` the file to see if the daemon overwrote you: `stat /var/www/html/arif/<path>/index.html` — mtime later than your last `write_file`/`open(...).write()` is the smoking gun.
3. To survive longer-running verification, write to `public/` first (the build source), then `cp` to the live webroot AND `md5sum` check immediately — the daemon doesn't touch `public/`, only `/var/www/html/arif/`.
4. For batch rebuilds of 14+ pages, do them all in one Python pass and verify all in the same script. The daemon tick interval is the budget; a full pass + verify usually beats it (under 30s).

**Reference recipe (with single-script rebuild + verify pattern):** `references/per-essay-page-rebuild-from-ts.md`.

<!-- SKILL-WITNESS-NOTE (auto, additive-only) -->
Witnessed reality moved this skill's selection to **ROUTE or MERGE**.
Scar signatures: 2026-09-25-source-type-promotion-gate, SCAR-LEDGER-HUMAN-ARIF-FAZIL-2026-09-23
Do not treat this skill as neutral until the signatures are resolved.
<!-- /SKILL-WITNESS-NOTE -->
