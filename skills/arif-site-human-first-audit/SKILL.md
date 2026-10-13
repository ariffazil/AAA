---
name: arif-site-human-first-audit
description: Human-first audit protocol for arif-fazil.com — the 4-lane deploy audit (Technical / Navigation / Visual / Attention) that every agent MUST pass before sealing any mutation. Load before ANY site work — build, edit, deploy, or cleanup. Enforces SITE_CONSTITUTION.md + SITE_IDENTITY.md — human comprehension over navigation over visual over agent discoverability over protocol. Includes the agent onboarding gates, attention budget, visual golden master, navigation regression check, and machine-file truth canary.
version: 1.0.0
tags: [arifos, arif-fazil, audit, human-first, attention, visual-baseline, navigation, deploy-gate, site-constitution, identity]
triggers:
  - any build/edit/deploy/cleanup on arif-fazil.com
  - user says "audit the site" / "site audit" / "identity audit" / "human-first"
  - before sealing any mutation to the site
  - adding a new page, surface, route, or nav item
  - touching llms.txt, page.json, sitemap, robots.txt, or any machine file
  - user asks "did the site drift?" or "is the site still human?"
  - onboarding a new agent to site work
---

# arif-site-human-first-audit

The deploy gate (`make verify-pages`) proves HTTP 200 only. This protocol proves
the site is still **human**. Run the 4 lanes before ANY mutation lands.

## Current rule (2026-10-13, wins over later copy-paste)

`SITE_CONSTITUTION.md` and `SITE_IDENTITY.md` reads below are REPORTED 2026-08-09. Probe those paths before treating them as present. The 5-lane nav line, the `/vitals /propa/ /malaysia/` pair, the `/trust/` restore row, and the surfaces-vs-sitemap counts are REPORTED August. Do not restore `/trust/`. Do not regenerate the sitemap from that table. Do not `git checkout HEAD -- .` over `/var/www/html` or `/var/www/html/arif`. Disk that Caddy serves is what humans see. Live-only HTML is load-bearing. `make deploy` is T3. Manual ship is additive per-route, no `--delete`. Queue is `/root/work/tasks.json`.

## Read first — the two canons (non-negotiable)

1. `/root/arif-fazil.com/SITE_CONSTITUTION.md` — the build law (priority order,
   6 rules, onboarding gates, attention budget, machine-file truth)
2. `/root/arif-fazil.com/SITE_IDENTITY.md` — what is sacred (5 layers, voice
   registers, sacred surfaces, anti-patterns)

Both are CANON, F13-ratified 2026-08-09. If your instinct conflicts with either
file — your instinct is wrong.

## The priority order (never optimize in reverse)

```
P0 Human comprehension  >  P1 Navigation clarity  >  P2 Visual coherence
  >  P3 Agent discoverability  >  P4 Protocol optimization
```

## Agent onboarding gates (before mutation rights)

1. **15-year-old test** — explain arifOS without jargon. Fail → NO MUTATION.
2. **Find the canon** — point to `canon/file-authority.yaml`,
   `canon/navigation.json`, `canon/design-tokens.json`. Fail → NO MUTATION.
3. **Four layers** — distinguish Observatory / MCP Gateway / Organs / Trust.
   Confusion → NO MUTATION.
4. **Why does a human visit?** — if the answer starts with MCP/Tools/JSON/
   Protocol → fail. Correct answer: "To meet a person who reads the earth,
   prices risk, and teaches machines to tell the truth."

## LANE A — Technical (the gate, plus the truth canary)

```bash
cd /root/arif-fazil.com
# 1. Standard gate — must pass or HOLD
make verify-pages

# 2. Machine-file truth canary (F2): declared content-type, no HTML soup
for f in llms.txt missions.json surfaces.json rsl.xml sitemap.xml robots.txt; do
  echo -n "$f: "; curl -sI "https://arif-fazil.com/$f" | grep -i "^content-type"
done
# Any .txt/.json returning text/html = LIE (the deceptive 200). Fix or HOLD.

# 3. Surfaces vs sitemap reconciliation (RULE 6)
echo "surfaces.json: $(python3 -c 'import json;print(len(json.load(open("surfaces.json"))["surfaces"]))')"
echo "sitemap locs:  $(curl -s https://arif-fazil.com/sitemap.xml | grep -c '<loc>')"
# Gap > 10 = discovery drift. Reconcile before adding new surfaces.

# 4. Canon-vs-live nav check (canon drift = the exact disease)
python3 -c "import json; d=json.load(open('canon/navigation.json')); print([x.get('label') for x in d.get('nav',[])[:8]])"
# Must show the 5-lane v7 canon (HOME EARTH WORDS WORLD WORK), not pre-v7 labels.

# 5. Constitutional surfaces alive?
for p in / /000/ /999/ /999/verify /verify; do
  echo -n "$p → "; curl -s -o /dev/null -w "%{http_code}\n" "https://arif-fazil.com$p"
done
# /999/ MUST be 200 — it was 404 as of 2026-08-09. Any 404 on this list = HOLD.
```

## LANE B — Navigation (the 3-click + journey test)

```bash
# 1. Nav-block diff across hubs — must be IDENTICAL except class="here"
for h in earth words world work; do
  echo "== /$h/ =="
  curl -s "https://arif-fazil.com/$h/" | grep -oE '<nav[^>]*>.*</nav>' | head -c 600
done
# 2. Landing → canon in ≤3 clicks: / → /words/ → /canon/ ... or / → footer canon link
# 3. Landing → trust in ≤3 clicks: / → /000/ (or footer Origin link)
# 4. No nav link points to a 404 (check /000/'s link to /999/ — broken as of 2026-08-09)
# 5. Redirect chains: curl -sIL and follow — no double-prefix mangling
for p in /writing/<slug> /essays/<slug> /vitals /propa/ /malaysia/; do
  curl -sIL "https://arif-fazil.com$p" | grep -iE "^HTTP|^location"
done
# /essays/<slug> → /writing/essays/<slug> = DOUBLE-PREFIX BUG (live as of 2026-08-09)
```

**Journey rule:** if any human journey got harder after your change → FAIL.

## LANE C — Visual (golden master + regression)

- Reference screenshots live in `visual-baseline/` (homepage, /000/, hubs,
  observatory, organs). Capture before any visual work; diff after.
- Compare against the **peer reference** when designing — Arif's rule: the
  referenced page IS the design contract (e.g. MakcikGPT pages are the /words/
  gold standard). `browser_navigate` (structure) + `browser_vision` (visual)
  both, always.
- Check: palette stays dark-forge + gold `#C9A227`, serif display + mono kicker;
  hero pattern kicker→h1→prose→quote→hint; no orphaned CSS classes (markup has
  classes, stylesheet gone → renders as bare text);
  tag balance (`<section>`/`<div>` counts match).
- Static hero = dead hero for hubs (hero-core doctrine: the visual must move).
- `prefers-reduced-motion` guards on every animation.

## LANE D — Attention (the budget)

| Page class | Understand in | Hard limit |
|---|---|---|
| Landing + hubs | 15s | 30s |
| Trust (/000/) | 45s | 90s |
| Writing (essays) | 60s | 120s |
| Observatory / organs | 60s | 120s |
| Data surfaces (/propa/ /vitals/ /gold/) | 30s to first live number | 60s |

Test per page: **What? Why? Why should I care?** — all three visible above the
fold, in budget. If the answer needs 3 minutes of reading → HALT.

Jargon test: would a 15-year-old (or a smart newcomer) get the purpose from the
first screen alone? If the first screen is protocol/tool/JSON talk → fail.

## The final identity drift test

```
system understands itself, human no longer does  → FAIL, revert
system understands itself, human still does      → PASS
```

## Known defects registry (updated 2026-08-09 evening — fix or declare, never ignore)

| Defect | Status |
|---|---|
| `/999/` 404 (constitutional Proof page) | **RESOLVED 2026-08-09** — verified 200, title "/999 — Proof · Sealed Vault" during survivability audit |
| `/trust/` 404 — SITE_CONSTITUTION RULE 2 promises trust ≤3 clicks; the path returns 404 | OPEN — restore source |
| `/observatory/` 404 — observatory moved to `/arifos/` (200, "arifOS Observatory — Reality Witness") but no redirect from old path; llms.txt still points at arifos.arif-fazil.com (301→/arifos/) | OPEN — add redirect |
| canon nav/accent divergence — world-model.yaml (DRAFT) 9-domain nav vs live 5-lane nav; atlas.yaml ring accents (SOUL red/MIND cyan/BODY gold/ORGAN violet) vs live hub accents | OPEN — design identity HOLD pending F13; mapping in arif-fazil-web-ops `references/design-canon-sot-2026-08-09.md` |
| `/words/llms.txt` serves SPA HTML (deceptive 200) | OPEN — create real file |
| `/work/llms.txt` 404 | OPEN — create real file |
| `/000/page.json`, `/999/page.json` 404 | OPEN |
| `/essays/<slug>` double-prefix redirect → `/writing/essays/<slug>` | OPEN — Caddy `{uri}` bug |
| surfaces.json 76 vs sitemap 48 (28 missing) | OPEN — sitemap generator |
| canon/navigation.json still pre-v7 labels (Capital/Voice/Essays) | OPEN — regenerate from live canon |
| Cloudflare managed robots.txt Disallow blocks vs origin Allow (conflict) | OPEN — check CF setting |
| llms.txt "five constitutional organs" — omits A-FORGE, arifFLOW, HERMES vs federation.json `organs` (8) | OPEN — update llms.txt |
| `/root/arif-fazil.com/FEDERATION.md` dead symlink | OPEN — replace with real file or remove |

## Survivability audit (zero-context transmission test)

The M365_COPILOT_KERNEL protocol measures whether the site's MEANING survives replacement of the
author: reconstruct world model from artifacts only (no AGENTS.md, no carry_forward, no prior
memory) → predict organs/ports/authority → probe PUBLIC surfaces → score transmission. Re-run
after any canon change (esp. when WORLD_MODEL.md exists). Full protocol + 2026-08-09 results:
`references/survivability-audit-zero-context-2026-08-09.md`.

## Chrome-creep drift pattern — every "small addition" accumulates

The most pernicious drift mode on arif-fazil.com is **chrome-creep** — the slow
accumulation of small "helpful" agent-chrome additions that serve agents, not
humans. Each individual change looks reasonable in isolation. Combined, they turn
a journalism brand into a GitHub repo.

**Proven drift trail on `/world/makcikgpt/` between 2026-07-31 and 2026-08-11:**

| Date | Commit | Symptom |
|---|---|---|
| 2026-07-31 | `767596c` | Primer Dark landing (clean: hero + stats + quote + series cards) |
| 2026-08-04 | `34fed66` | + epistemic tags, pairings, "read next" navigation |
| 2026-08-08 | `3fe612d` | + zen-pulse "WHERE AM I? / WHY CARE? / WHAT NEXT?" card |
| 2026-08-10 | `051d799` | + "Source of truth: src/data/essays.json" footer |
| 2026-08-11 | (current) | + "Canonical landing:" + "Rendered by scripts/" |

Arif's verbatim rejection: *"Buruk. Aku x mau ni. deep archive extraction."*

**Detection — any one of these patterns in a visual HTML page = chrome-creep:**

- Page header has a line like "Canonical landing: <path>"
- 3-column info card: "WHERE AM I? | WHY CARE? | WHAT NEXT?"
- Footer with: "Source of truth: <file>. Rendered by <script>."
- Multiple `[OBS] [DER] [INT] [SPEC]` tags visible to humans (these belong in agent metadata only)
- Every list item carries "· seal 999" suffix
- Footer has: "llms.txt · missions.json · surfaces.json" — bot metadata leaking into visual

**The fix is three layers deep:**

1. **Canonical SOT** — `/root/arif-fazil.com/sites/arif-fazil.com/DESIGN_INVARIANTS.md` declares what is/isn't allowed in visual surfaces. Read BEFORE touching any visual HTML.
2. **Auto-block lint** — `scripts/design-lint.sh` scans every `public/**/*.html` + `src/**/*.{tsx,ts,css}` for the 5 Rein (forbidden chrome strings). Exit 1 on any hit. Wire to `npm run build` prebuild.
3. **Visual recovery canon** — git archive at `767596c` (Primer Dark landing), `696f734` (original chat interface), `75dcd84` (minimal essay page). Use `git show <commit>:<path>` to extract.

**Companion skill:** `makcikgpt-archived-designs` — full archive extraction recipe + the Primer Dark token palette + the inject-article-styles.sh pattern for retrofitting dark-mode CSS onto article HTML.

**Status (sealed 2026-08-11):** The Primer Dark landing is restored live at `/world/makcikgpt/`. All 82 articles have dark-mode CSS injected via `inject-article-styles.sh`. `design-lint.sh` passes (542 files scanned). One governance-page leak (`Source of truth:` → `Floors canon`) was fixed during the same session.

## Anti-bulldoze pattern (live webroot drift)

**Verified incident 2026-08-11 (SyedOS):** Agent saw `/var/www/html/syedos/` showing only `.git` + thin placeholder, assumed "empty", `write_file`-ed a fresh blank-slate `index.html` — **wiping the canonical 5-card hub + gold chart + dashboard** the user spent agents and hours building. Arif's reaction: *"Weiii. Hang revert balik. Mana pi semua gold chart resit dashboard bagai. Suka2 bulldoze site yabg dah Ada. Penat agent Sebelum ni buat."*

**Before any `write_file` to `/var/www/html/<site>/`:**

```bash
# 1. WHAT IS IN GIT (canonical)?
git -C /var/www/html/<site> ls-tree -r HEAD --name-only

# 2. WHAT IS ON DISK (live)?
ls -la /var/www/html/<site>/

# 3. DIFF — anything in git but missing on disk = bulldoze victim
diff <(git -C /var/www/html/<site> ls-tree -r HEAD --name-only | sort) \
     <(cd /var/www/html/<site> && find . -type f -not -path "./.git/*" | sort)
```

**Rules:**
- If git has files that disk doesn't → compare first. Live-only HTML that Caddy serves is load-bearing. Do not restore over `/var/www/html` or `/var/www/html/arif`.
- If you see only `.git` on disk → stop. `git checkout HEAD -- .` is a 2026-08 scar. Do not run it over `/var/www/html` or `/var/www/html/arif`. Disk that Caddy serves is what humans see.
- If you're the SOLE author of new content → fine, but commit to git FIRST, then rsync to live.
- **Recovery when you've already bulldozed:**
  ```bash
  cd /var/www/html/<site>
  # HISTORICAL SCAR. Do not run: git checkout HEAD -- .
  chown -R www-data:www-data .
  chmod 644 index.html
  curl -sfL -o /dev/null -w "Probe: %{http_code}\n" https://<site>/
  ```
  Then probe ALL routes — don't assume git restored everything intact.

**The cardinal rule (2026-10-13):** *Disk that Caddy serves is what humans see. Git is a source copy. Do not `git checkout HEAD -- .` over `/var/www/html` or `/var/www/html/arif`. A hashed file a live page still names is load-bearing.*

## Pitfalls

- **curl lies about SPA pages.** A 200 from curl on a router-handled path proves
  nothing about human visibility — verify with `browser_navigate` + snapshot.
- **`verify-pages` passing ≠ content updated.** Gate asserts HTTP 200 only.
  Grep for a unique content marker after every deploy.
- **Sibling agents build concurrently.** Probe live + grep repo before building;
  `md5sum` reconcile after deploy; adopt richer sibling output, never re-inject.
- **Subagents fabricate.** Essay body/references/quotes must come from the
  user's paste or .ts source — nothing else. Strip-check before delivery.
- **Header chrome creep** — byline pills live in the FOOTER, never the header.
  See "Chrome-creep drift pattern" above for the full 5 Rein + 3-layer fix.
- **Machine files must be REAL files** — Caddy `try_files` serves a real file
  when it exists; the SPA catch-all only fires on missing files.
- **Deploy ≠ verify-pages** — `make deploy` is T3. The manual path is additive per-route, no `--delete`. Report catalog drift separately (see arif-sites-ops).
