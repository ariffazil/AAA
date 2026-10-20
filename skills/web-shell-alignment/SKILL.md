---
name: web-shell-alignment
description: "Use when a page must match the site's article shell."
version: 1.0.0
owner: HERMES
risk_tier: T2
autonomy_tier: T1.5
---

# Web shell alignment

One shell across the whole site. When the sovereign says *"make the design aligned with all other articles"*, an existing page is running its own chrome and should read as the same document as every other page. This is a **chrome swap**, never a content rewrite.

Deploy mechanics (webroot layout, additive copy, page gate, proxy config) live in `arif-sites-ops` and `arifos-site-patch-without-caddy-reload` — read those for the ship step. This skill covers the alignment itself.

## The shell, exactly

| Element | Value |
|---|---|
| Display font | `Fraunces, Georgia, serif` — h1 uppercase, `clamp` up to 60px, black weight, tight tracking |
| Body font | `Newsreader, Georgia, serif` — 18px, relaxed leading |
| Mono | `IBM Plex Mono`, falling back to `JetBrains Mono` |
| Hub chrome pair | `Cabinet Grotesk` display + `Satoshi` body |
| Background | `#0A0B0D`; surfaces `#0F1116` / `#13161C`; hover `#171B22` |
| Text | ink `#EDE9E0`, muted `#9AA3B2`, dim `#6B7484` |
| Accents | gold `#C9A227`, ember `#E4572E`, blue `#4AA8FF`, seal green `#31C48D` |
| Hairline | `#1F2733` |
| Frame | `.site-frame` — max-width 1400px, `padding-inline: 2rem` |
| Reading column | `max-w-3xl` = 768px |
| Header | sticky 56px: `Ψ ARIF FAZIL` brand → mono uppercase nav → MYT clock with green dot |
| Footer | `Forged, not given.` creed → four link columns → base row with the Ditempa line |

## Procedure

1. **Probe which layer serves the route before editing a file.**
   ```bash
   curl -s -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36' \
     -o /dev/null -w '%{size_download}\n' https://<host>/<route>/
   stat -c%s <repo>/sites/<site>/public/<route>/index.html
   ```
   Roughly equal → the static shell is serving; edit it. Five to ten times larger → an SPA shell is serving and a static edit reaches nobody. Report which layer won before touching anything.
2. **Extract the reference chrome live**, never from memory. On a known-good article page:
   ```js
   document.querySelector('header')?.outerHTML
   document.querySelector('footer')?.outerHTML
   ```
3. **Rewrite only the page's own `<style>` block onto the tokens above, then replace the header and footer markup.** Every content section, number, chart and caption stays byte-identical.
4. **Ship additively**: source → `dist/<route>/` → live webroot, `chown` the web user, `chmod 644`, keep `index.html.bak-<date>-shell`. Then run the project's page gate.
5. **Prove alignment with measurements, not adjectives.** Run the identical probe on a reference article and on the edited page and diff them:
   ```js
   (() => { const h1=document.querySelector('h1'), a=document.querySelector('article');
     const cs=e=>e?getComputedStyle(e):{};
     return JSON.stringify({bg:getComputedStyle(document.body).backgroundColor,
       h1Font:cs(h1).fontFamily, h1Size:cs(h1).fontSize, h1Transform:cs(h1).textTransform,
       bodyFont:cs(a).fontFamily, bodySize:cs(a).fontSize, maxW:cs(a).maxWidth,
       header:!!document.querySelector('header'), creed:document.body.innerText.includes('Forged')}); })()
   ```
   Font family, size, transform, max-width, background and header presence must match field for field. "Looks aligned" is not a verdict.

## Pitfalls

- **Never link a hashed build asset directly.** `/assets/index-<hash>.css` changes on every build and takes the page's styling with it. Copy the current hash to a stable path (`<route>/_shell/article.css`) and link only that. If the page has a build renderer, add a shell-sync step that re-copies `dist/assets/index-*.css` into the stable path on each build so the copy cannot go stale.
- **Converting collapsed sections to open sections is a visibility change, not a style change.** Turning `<details>` blocks into `<h2>` sections reveals content the reader previously had to open. State it in the commit message and the report; never let it ride in as a styling side effect. Ask first if the page is sealed.
- **Full-file rewrites fight the read-before-write guard.** A rewrite is refused when the file was last read with `offset`/`limit`. Either read the whole file in one call (no pagination) before rewriting, or compose the new version in scratch and `cp` it into place — the second route also yields a byte diff and a `.bak` for free.
- **Do not sweep sibling pages in the same pass.** Analysis siblings usually belong to a different shell family and each needs its own probe and its own approval. Align the page that was asked for, name the remaining ones, stop.
- **A styled page with a broken nav is not aligned.** Check nav items and the active item against the site canon, and confirm the clock script actually ticks — a clock stuck at `--:--:--` is an unhandled script error, not cosmetics.
- **Do not change the page's editorial accent mid-swap.** If the page carries a domain colour (organ identity), keep it for emphasis and let the shell own the base palette. Recolouring meaning is a redesign.
- **Reference the shell by behaviour, not by a stored template.** The live article page is the template. Extracting header/footer from the rendered DOM in step 2 beats any stored copy, which drifts the moment the build changes.
