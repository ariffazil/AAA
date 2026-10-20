---
name: arif-site-publish
description: Use when publishing or editing a page on arif-fazil.com.
---

# Publishing to arif-fazil.com

Any edit to a public page must land in the right places and pass the deploy gate. Skipping a step produces a page that exists on disk and returns 404, or serves stale content to the user.

## Procedure

1. **Edit the source of truth.**
   `/root/arif-fazil.com/sites/arif-fazil.com/public/<path>/index.html`
   Never edit `dist/` or the webroot directly — they are build outputs and get overwritten.

2. **Find the actual serving root for that path before copying.** The vhost does not use one root. Read the handle block:
   ```bash
   grep -n -A8 'handle /earth\*' /etc/caddy/vhosts/arif-fazil.com.conf
   ```
   Top-level pages are served from `root * /var/www/html/arif`. The `/earth*` block overrides with `root * /var/www/html` — so `/earth/x/` must live at `/var/www/html/earth/x/index.html`, **not** `/var/www/html/arif/earth/x/`.

3. **Mirror to all three locations.**
   ```bash
   cp public/<path>/index.html dist/<path>/index.html
   cp dist/<path>/index.html /var/www/html/<ROOT>/<path>/index.html
   chown www-data:www-data /var/www/html/<ROOT>/<path>/index.html
   chmod 644 /var/www/html/<ROOT>/<path>/index.html
   ```
   Use `mkdir -p` and `chmod 755` on a new directory.

4. **Verify live, not local.**
   ```bash
   curl -s -o /dev/null -w "%{http_code} %{size_download}b\n" https://arif-fazil.com/<path>/
   cd /root/arif-fazil.com && ./scripts/verify-pages.sh   # must print VERDICT: PASS
   ```
   A 404 with the file present on disk means you copied to the wrong root — re-read step 2, do not touch routing.

5. **Commit exact paths only.**
   ```bash
   git status --short <path>      # read before staging
   git diff <path>                # confirm the deltas are yours
   git add <exact-path>           # never git add -A / .
   ```

## Pitfalls

- **Other agents edit the same tree.** `git add` of a file whose working copy already contains someone else's uncommitted edits sweeps their work into your commit under your message. Diff the target and stage by path; if foreign hunks are present, either amend the message to name them as carried or leave the file alone.
- **Never run the whole `make deploy`** — it reloads Caddy. Adding a path under an existing handle needs no Caddy change; a genuinely new top-level prefix does, and that is a separate, named decision.
- **`dist/` and the webroot are independent copies.** Updating one and not the other serves stale content silently. Both, every time.
- **Screenshot chrome is not your page.** Android/Chrome link bubbles, "copied to clipboard" toasts and browser UI overlay the render without being part of the DOM. Grep the source for the element's text before "fixing" it: `grep -i "clipboard\|toast\|share" page.html`. Zero hits means the overlay is outside your code.
- **A hash-pinned manifest is invalidated by any later edit.** If a deploy receipt binds a `sha256` to a file and someone else edits that file afterwards, do not re-hash or overwrite their receipt — write a separate amendment listing the deltas and the new digest. Re-binding someone else's manifest rewrites their record of what they shipped.
- **Fetched-HTML digests do not match on-disk digests.** The edge injects script into responses. Compare `md5sum` of the source file against the webroot copy, never against `curl` output.

## Verify the render, not just the HTTP code

```bash
google-chrome --headless=new --disable-gpu --no-sandbox \
  --virtual-time-budget=3500 --window-size=1500,2400 \
  --screenshot=/tmp/shot.png "file://$PWD/index.html"
```

- Check **390 px** as well as desktop: responsive breakpoints hide content that is fine at 1500 px.
- A horizontally-scrollable figure inside a narrow viewport is clipped silently unless you say so — add a visible hint under the breakpoint rather than letting the reader think the figure ended.
- Crop before analysing: `PIL.Image.open(p).crop((x1,y1,x2,y2)).resize(...).save(q)` then analyse the crop. Cropping keeps full resolution and sidesteps region-parameter differences.
- Syntax-check inline JS before deploying:
  ```bash
  sed -n '/^<script>/,/^<\/script>/p' index.html | sed '1d;$d' > /tmp/chk.js && node --check /tmp/chk.js
  ```
  A quote-mismatch inside a concatenated HTML string in JS fails only at runtime; `node --check` catches it in one second.
