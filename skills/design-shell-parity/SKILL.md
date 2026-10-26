---
name: design-shell-parity
description: "Use when a page must match another page's shell."
version: 1.0.0
owner: HERMES
risk_tier: T1
floor_scope: F1 F2 F4 F13
---

# Design Shell Parity

Aligning a page to an existing design language is a **transcription** task, not a design task.
You copy the class vocabulary and the computed result of a reference page; you do not invent.
The same skill covers the inverse failure: a page that renders correctly until a build and then
loses all styling because its stylesheet was a hashed build artifact.

## Trigger

- "Make X aligned with the articles / with the other pages."
- "This page doesn't look like the rest of the site."
- A page renders unstyled, or its CSS 404s, after `npm run build`.
- You are about to restyle a static page that a generator also writes.

## Step 1 — Find the reference, not the ambition

Pick the page family the user means by *the other pages* — usually the most numerous one
(articles, posts, product pages). Census the tree so you know which shell is canonical and which
pages are the drift:

```bash
for d in <webroot>/*/; do n=$(basename "$d"); f="$d/index.html"; [ -f "$f" ] || continue
  printf "%-18s frame=%s dark=%s altcss=%s\n" "$n" \
    "$(grep -c 'site-frame' "$f")" "$(grep -c 'bg-forge-black' "$f")" "$(grep -c 'economics.css' "$f")"
done
```

A page alone in its column is the outlier. Never treat the outlier as the template just because it
is the page under discussion.

## Step 2 — Measure parity numerically (you cannot see screenshots)

Run identical JS against the reference page and the target page, then diff the JSON. Font family,
font size, text-transform, background colour, container max-width, and the presence of the
brand/nav/footer strings are the whole contract.

```js
(() => {
  const h1=document.querySelector('h1'), header=document.querySelector('header'), art=document.querySelector('article');
  const cs=e=>e?getComputedStyle(e):{};
  return JSON.stringify({
    bg: getComputedStyle(document.body).backgroundColor,
    brand: header?.querySelector('a')?.innerText ?? null,
    brandFont: cs(header?.querySelector('a')).fontFamily,
    navFont: cs(header?.querySelector('nav')).fontFamily,
    h1Font: cs(h1).fontFamily, h1Size: cs(h1).fontSize, h1Transform: cs(h1).textTransform,
    bodyFont: cs(art).fontFamily, bodySize: cs(art).fontSize, maxW: cs(art).maxWidth,
    hasFooter: document.body.innerText.includes('Ditempa bukan diberi')
  });
})()
```

Quote both JSON objects side by side in the report. "Looks right" is not evidence; identical
computed values are.

Also count structural drift, not just CSS: `<details>`/`<summary>` collapsibles, missing byline
block, missing footer, wrong nav lane highlighted. A reference shell that is an open document
means hidden sections are drift too — converting them to `h2` + prose **is** part of parity.

## Step 3 — Rebuild in the reference vocabulary

Reuse the classes the reference already loads (utility classes if it uses them) rather than
writing a new `<style>` block. A page-specific `<style>` block is how drift starts.

Section rhythm rule: a `space-y-*` parent spaces siblings but does not open air around headings —
put an explicit top margin on `h2` (`!mt-14`) and on block wrappers (`!mt-8`), or the article
reads as one wall.

Keep every existing content block, number, source link and `data-agent-role`/JSON-LD payload.
Restyling must not silently revert an earlier content patch — grep for a unique sentence from the
previous edit after the restyle.

## Step 4 — Hashed build CSS: copy to a stable path

When the reference page's stylesheet is `/assets/index-<hash>.css`, the hash changes on every
build. A static page that hardcodes it breaks at the next deploy with no error anywhere.

```bash
cp "$SITE/dist/assets/"index-*.css "$SITE/public/<route>/_shell/article.css"
```

Reference `/<route>/_shell/article.css` from the page, and teach the route's generator
(`scripts/render-<route>.cjs`, or postbuild) to redo that copy each build:

```js
const cssName = fs.readdirSync(path.join(ROOT,'dist/assets'))
  .filter(f => /^index-.*\.css$/.test(f)).sort().pop();
if (cssName) {
  fs.mkdirSync(path.join(ROOT,'dist/<route>/_shell'), {recursive:true});
  fs.copyFileSync(path.join(ROOT,'dist/assets',cssName), path.join(ROOT,'dist/<route>/_shell/article.css'));
}
```

Put that block **before** any marker/template check so it runs even when the page body is skipped.

## Step 5 — Ship three copies, in this order

Source, dist and live must agree. Live webroot is usually owned by the web user; a root-owned
`0600` file is invisible to the server.

```bash
S=<site root>
cp -a <webroot>/<route>/index.html <webroot>/<route>/index.html.bak-$(date +%Y%m%d)
cp "$S/public/<route>/index.html" "$S/dist/<route>/index.html"
cp "$S/public/<route>/index.html" <webroot>/<route>/index.html
chown www-data:www-data <webroot>/<route>/index.html && chmod 644 <webroot>/<route>/index.html
mkdir -p <webroot>/<route>/_shell && cp "$S/public/<route>/_shell/article.css" <webroot>/<route>/_shell/article.css
curl -s https://<host>/<route>/ | grep -c '<unique marker from the new version>'
curl -s -o /dev/null -w '%{http_code}\n' https://<host>/<route>/_shell/article.css
```

Run the site's page gate afterwards (`make verify-pages`, `verify-*`, whatever the repo exposes)
and report its verdict line, not an impression.

## Step 6 — Publish without publishing someone else's work

On a public repo an ambiguous push publishes more than you meant:

- **Never `git push origin HEAD`** when the checked-out branch is not the trunk. It creates a new
  **public branch** carrying every commit on that branch — including other agents' unmerged work.
  Push an explicit refspec: `git push origin <sha>:main`.
- **When the worktree belongs to another agent's branch**, do not commit into it. Cherry-pick onto
  a clean worktree of the remote trunk and push from there:

```bash
git worktree add -f /tmp/wt-<topic> origin/main
cd /tmp/wt-<topic> && git fetch -q origin && git reset -q --hard origin/main
git cherry-pick -x <sha>
git push origin HEAD:main
git worktree remove --force /tmp/wt-<topic>
```

After pushing, confirm the remote ref moved: `git fetch -q origin && git log --oneline -1
origin/main`. If a wrong branch did reach the remote, delete it immediately
(`git push origin --delete <branch>`) and state it plainly in the report — do not bury it.

## Pitfalls

- **A coding agent that reports success may have changed nothing.** Verify the effect on disk
  (`git diff --stat`, file mtime) before relaying success. A `subtype: success` result with an
  untouched tree is a failed run.
- **Marker-managed pages.** If a generator replaces `<!--PREFIX-*:...-MARKER-->` regions, prose
  written inside a marker is destroyed on the next build. Write outside the markers, and after a
  rewrite confirm the markers still exist — a page with no markers makes the generator exit
  "leaving it untouched", silently freezing the old template forever.
- **Don't restyle the whole site in one pass.** Align the page the user named; list other drifted
  siblings as a separate follow-up rather than half-converting them.

## Related

Site-specific procedure (routes, proxy config, deploy gates) lives in the repository's own
site-ops skills; this skill is the portable method. Where a site skill and this one disagree
about a specific path, the site skill wins.
