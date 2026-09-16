# arif-fazil.com repo & live-tree topology (audited 2026-08-14)

## Paths
- `/root/arif-sites` is a SYMLINK to `/root/arif-fazil.com` — one repo, two
  names. Never treat them as separate copies.
- Git repo root = /root/arif-fazil.com (origin github.com/ariffazil/arif-fazil.com;
  main protected → feature branch + PR).
- `/root/web-canon` = separate repo; navigation.json (primary/secondary/machine
  links) is the nav SOT; main protected → PR.

## Source vs live roots (the trap that caused bad rsyncs)
- `/var/www/html/arif/` serves apex + /000 /999 /economics /doctrine-redirects +
  makcikgpt-md (bot+human articles) + agent shells.
- `/var/www/html/{world,work,words}/` (NOT under arif/) serve those prefixes.
  /missions/ and /doctrine/ 308 → /work/missions/ and /words/doctrine/ — edit
  the SERVED files, not the redirect-source ones.
- Live can be AHEAD of git (someone fixed live-only). Before any `rsync --delete`
  deploy: heal baseline first (snapshot → cp live→source → commit).

## Redundancy scan results (2026-08-14)
- Top-level `arif/` (llms.txt, sitemap.xml, robots.txt, page.json, machine/,
  map/, rsl.xml) was a STALE mirror fully shadowed by
  `sites/arif-fazil.com/public/` (newer content; live serves public/; zero refs).
  Quarantined to `_quarantine/2026-08-14-arif-stale-mirror/` (commit a36bb1e).
  If a top-level dir reappears with the same names as public/, suspect stale
  mirror again — diff against public/ and live before trusting either.
- `canon/` (top) vs `sites/arif-fazil.com/canon/` = SPLIT SOT, unresolved:
  top holds design canon (atlas.yaml, design-tokens.json, federation.json),
  sites/canon holds navigation canon consumed by generate-nav-canon.cjs /
  zen-nav.cjs. Pending sovereign decision (proposed: design canon → web-canon).
- `content/essays/*.md` vs `src/data/essays/*.ts` = INTENTIONAL dual-lane
  (bot markdown vs SPA TypeScript), same pattern as makcikgpt-md .md siblings.
  Drift-prone; parity-check like makcik-source.cjs before trusting one side.
- `public/world/makcikgpt/index.html` = dead leftover (no Caddy route serves it;
  humans get makcikgpt-md). Flagged, not deleted.
- `_legacy/ _quarantine/ backups/ deploy/` are retention/infra zones, not dupes.

## Dual-lane serving (audit pitfall)
Bot/headless UA → static lane; real desktop Chrome UA → human surface
(home = SPA; makcikgpt articles = static Primer Dark). Always audit with a real
Chrome UA, and remember `scroll-behavior:smooth` breaks scrollIntoView
screenshots (use behavior:'instant').
