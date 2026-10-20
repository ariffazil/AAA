---
name: arif-fazil-site-deploy
description: Use when publishing or editing a page on arif-fazil.com.
---

# Deploying a page on arif-fazil.com

Many agents share this worktree and this webroot. The failure you are most likely to cause is not a bad
page — it is a page that exists in `dist/` but returns 404, or a commit that carries someone else's
uncommitted work under your message.

## When to Use

Any time you add or edit a page under `/root/arif-fazil.com/sites/arif-fazil.com/`, or when a live URL
404s after you believed you published it.

## Procedure

1. **Find the real docroot before writing anything.** The main `/etc/caddy/Caddyfile` only does
   `import /etc/caddy/vhosts/*.conf` — `Caddyfile.live` is stale and editing it changes nothing. Read
   `/etc/caddy/vhosts/arif-fazil.com.conf` and find the `handle` block whose path prefix matches your
   page; that block's `root *` is the actual webroot. Prefixes differ: `/earth*` serves from
   `/var/www/html`, so earth pages live in `/var/www/html/earth/`, not `/var/www/html/arif/earth/`.
   Writing to the wrong root gives a 404 with a perfectly correct file on disk.
2. **Sync three places, in order:** `public/<path>` -> `dist/<path>` -> the webroot from step 1. `public/`
   is the source Vite copies into `dist/`; the webroot is what Caddy serves. All three must match or the
   file silently diverges. `chown www-data:www-data` and `chmod 644` the live copy.
3. **Verify at the origin, not through Cloudflare.** `curl -sk --resolve arif-fazil.com:443:127.0.0.1
   https://arif-fazil.com/<path>` tests the box. A public `200` can come from a cached edge response and
   hide a 404 at origin; an origin `200` plus a public `200` is the only receipt worth quoting.
4. **Run the deploy gate:** `cd /root/arif-fazil.com && ./scripts/verify-pages.sh`. It must end
   `VERDICT: PASS`. Never run the whole `make deploy` just to publish one page — it reloads Caddy.
5. **Check the JS before shipping.** Extract the inline script and syntax-check it:
   `sed -n '/^<script>/,/^<\/script>/p' index.html | sed '1d;$d' > /tmp/chk.js && node --check /tmp/chk.js`.
   A quote mismatch inside a template literal is invisible to the browser until the whole block fails to
   parse, and the page then renders as static HTML with dead controls.
6. **Render it and look.** Headless Chrome screenshot, then crop the region you changed and inspect it:
   `google-chrome --headless=new --disable-gpu --no-sandbox --virtual-time-budget=3500 --window-size=W,H
   --screenshot=out.png file://$PWD/index.html`. Do this at 390 px too — a wide SVG needs an
   `overflow-x:auto` wrapper or it shrinks into unreadable microtext.

## Pitfalls

- **`git add <file>` on a dirty worktree commits other agents' edits.** The tree is shared; another lane
  may have uncommitted changes in the same file. Inspect `git status` and the diff scope first, and verify
  the staged diff touches only what you changed. If a commit already swept in foreign work, do not revert
  it — amend the message to state what is actually inside.
- **A hash-bound deploy manifest is invalidated by any later edit, including a one-line link.** If a
  manifest records `sha256` for a target, editing that target makes the recorded hash wrong forever —
  reverting your edit will not restore it if another agent also changed the file. Never re-hash or
  overwrite another lane's manifest. Write a separate amendment that lists each delta and the final hash.
- **A signed/temporary CDN URL is not provenance.** CloudFront links carrying `Policy=`, `Signature=` or
  `Key-Pair-Id=` expire. Ship stable DOI or relative references in any archived artifact.
- **A frozen HTML snapshot is not an app.** If there is no `<script>`, the buttons are dead: say so in the
  header ("FROZEN SNAPSHOT · controls disabled · model X of N") rather than shipping a page that invites
  clicks it cannot service. Also check that the canvas title and the side label name the same model.
- **Badge claims must match capability.** "OFFLINE READY" is only true for viewing if assets are inlined;
  it is not true for interaction. Word the badge for what actually works.
