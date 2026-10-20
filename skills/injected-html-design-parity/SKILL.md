---
name: injected-html-design-parity
description: "Use when a page looks unlike its siblings despite same CSS."
---

# Injected-HTML design parity

For pages whose body is HTML injected into a host component (`dangerouslySetInnerHTML`,
`v-html`, a CMS block, a markdown→HTML pipeline) — and which must look identical to
their siblings.

## The mechanism worth remembering

Host components frequently style injected content with **direct-child** selectors:

```jsx
<div dangerouslySetInnerHTML={{__html}} className="[&>h2]:font-serif [&>h2]:text-2xl
     [&>h2]:border-b [&>blockquote]:border-l-4 [&>ul]:list-disc" />
```

`&>` matches children only. So a body that ships its own `<article>` / `<section>` /
`<div class="cover">` wrappers makes every heading a **grandchild**, all selectors miss,
and the elements fall back to the global element styles (typically the sans display face
at a small size with no rule under it).

The result is a page that *looks like a different site* while loading byte-identical CSS.
That is why "the CSS is the same, so it must be a cache issue" is wrong, and why editing
CSS never fixes it: the defect is the DOM depth of the body, not the stylesheet.

**Rule: the body is flat HTML. Wrappers, `<style>` blocks and typography belong to the
host component, never to the body.** One host = one body shape for every page it renders.

## Diagnosis, in order

1. **Measure, do not eyeball.** Load the suspect page and a known-good sibling and compare
   computed style of the first heading, first paragraph, first list:
   ```js
   (() => { const h = document.querySelector('h2'), g = e => getComputedStyle(e);
     return JSON.stringify({font: g(h).fontFamily.split(',')[0], size: g(h).fontSize,
       border: g(h).borderBottomWidth + ' ' + g(h).borderBottomColor}); })()
   ```
   Different `font` / `size` / `border` under the same page shell means a selector is
   missing — not that the design is "slightly off". Numeric diff is the gate.
2. **Read the host component's selectors.** Find the `[&>…]` / `> h2` / `.content > h2`
   rules; they tell you the exact depth the styles expect.
3. **Inspect the body source for wrappers.** `grep -c '<article\|<section\|class="cover"'`
   on the content module. Any wrapper is the bug.
4. **Check the injection cleaner too.** Components often strip a duplicate cover/title
   before injecting — but only when it can see it at the expected depth. Wrapping also
   hides content from the stripper, so a stray `.cover-title` or duplicate `<h1>` survives.
5. **Fix the body, not the CSS.** Strip the wrappers, re-run the generator, rebuild.

## Do not hand-write what the build already generates

When a page has both a source template (`.ts` module, markdown, data file) and a route shell
emitted by postbuild, writing the final HTML by hand produces a bespoke design that diverges
from every sibling and bypasses the component's chrome (breadcrumb, receipt panel,
prev/next). The hand-written file wins at the webroot and the divergence is invisible in
code review.

- Edit the **source template**, run the generator, install the generated shell.
- Compare the installed shell against a sibling — they should be byte-identical apart from
  edge-injected scripts. A different size means you shipped a bespoke page.

## Generator-owned artefacts revert

A prebuild/postbuild script that reconstructs page X from source Y silently overwrites a
patch applied only to the built output on the next build.

- Patch the source of truth, re-run `node scripts/render-<route>.cjs`, then install the result.
- Never leave the only copy of a fix in `dist/` — the next build erases it.

## Build → live sync is HTML + assets, never assets alone

Every build stamps a new content hash into the shells (`/assets/index-<hash>.js`). Copying
only `assets/` leaves previously-installed HTML pointing at the old hash, so the site serves
a stale bundle beside new assets — invisible when you `curl` any single page.

```bash
rsync -a dist/assets/ /var/www/html/<site>/assets/     # additive, never --delete
while IFS= read -r f; do                               # reinstall changed HTML
  rel="${f#dist/}"; dst="/var/www/html/<site>/$rel"
  [ -f "$dst" ] && ! cmp -s "$f" "$dst" && install -m 644 -o www-data -g www-data "$f" "$dst"
done < <(find dist -name '*.html' | sort)
```

Then assert **one** hash across the webroot, and that every referenced asset exists:

```bash
grep -rho '/assets/index-[A-Za-z0-9_-]*\.js' --include='*.html' /var/www/html/<site> | sort | uniq -c
grep -rho '/assets/[A-Za-z0-9_.-]*\.\(js\|css\)' --include='*.html' /var/www/html/<site> \
  | sed 's#.*/##' | sort -u | while read f; do [ -f /var/www/html/<site>/assets/$f ] || echo "MISSING $f"; done
```

Report pre-existing missing assets separately instead of absorbing them inside an unrelated
deploy — silent absorption hides which change broke what.

## Verification gates

- **Computed style parity** on heading, paragraph, list and opener quote vs a sibling.
- **Chrome parity:** title suffix, breadcrumb, footer byline / receipts / hashtag rows.
- **Both lanes:** human lane and bot/markdown lane each return the right payload.
- **Discovery surfaces regenerated:** listing index, machine manifest, feed, sitemap.
- **Source tests:** the repo's parity test suite passes before you claim done.

## Pitfalls

- **Status code lies.** A wildcard route that falls back to the section index returns 200 for
  a missing page. Compare byte size against a known sibling; 200 alone proves nothing.
- **User-agent routing.** Sites with bot lanes serve markdown to `curl` / `wget` / headless
  UAs. Send a real browser UA for the HTML, or you will debug the wrong document.
- **Link drift compounds parity work.** If internal links point at paths that redirect, every
  click burns a hop. Resolve each redirect once and hardcode the destination.
- **Keep deploy policy where it lives.** Follow the site-ops skill's deploy rules but do not
  fork them here; parity fixes (template shape, depth, verification) live in this skill.
