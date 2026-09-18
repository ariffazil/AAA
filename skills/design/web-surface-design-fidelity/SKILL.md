---
name: web-surface-design-fidelity
description: "Use when styling a page to match a live site's design."
owner: HERMES
risk_tier: low
floor_scope: [F2, F4, F6, F13]
autonomy_tier: T1
tags: [design, typography, composition, frontend, preview, visual-fidelity]
---

# Web Surface Design Fidelity

> A preview can pass every technical gate — valid markup, tokens wired, JS running, WCAG
> green — and still be rejected on sight. Delivery competence is not design competence.
> This skill is the difference between the two.

**Triggers:** "redo the design", "make it nicer", "not that nice", "use real design
skills", restyle an existing page, build a new front page or landing surface for a site that
already exists, review a rendered design preview.

**Not for:** token-level theme config, CI/CD, cartography — see the constellation's own
web-builder and infra skills.

---

## 1. Read the target before dressing it

The site's own CSS is the specification. Do **not** bring a style from a sibling page, and never
style an editorial surface from a design-token file's generic fallbacks.

```bash
curl -s https://<host>/ -o /tmp/target.html
grep -oE 'href="https://[^"]*font[^"]*"' /tmp/target.html    # the real font import
grep -oE 'font-family:[^;}]+' /tmp/target.html | sort -u
sed -n '1,40p' /tmp/target.html                                # head, meta, theme-color

# sibling surfaces may carry a DIFFERENT, older system — always compare
curl -s https://<host>/<hub>/ | grep -oE 'font-family:[^;}]+' | sort -u
```

Three layers exist on any mature site and they are not interchangeable:

| Layer | Authority |
|---|---|
| The **target page's own import** | the specification — use this |
| A **sibling surface** (hub, section index) | may be an older set; check before copying |
| The **design-token file** (`--font-sans`, `--font-mono`) | canon, but its generic values are often **legacy** for editorial surfaces |

**Pitfall — copying the hub onto the front page.** On a mature site the hub is usually built
first and restyled last. Copying its type set onto the front page is the single most common
cause of a rejected design. Verify per surface, never per site.

## 2. Compose page-shaped, not dashboard-shaped

Every agent asked to "make it nicer" produces the **agent-dashboard cliché** by default. It
reads as *instrument panel*, never as *page*:

| ❌ Dashboard cliché | ✅ Page-shaped |
|---|---|
| Seven-segment / LED-style numerals | Display serif numerals |
| Monospace uppercase captions, wide letter-spacing, on **every** label | Italic serif captions |
| Cards, badges, `border-radius`, box-shadow + glow | 1px hairline rules as structure |
| Eight or more elements of equal visual weight | **One loud element**; everything else quiet |
| Boxes as containers | Negative space as the container |
| Multi-colour segmented blocks | One continuous gradient band |
| Emblem in a rounded badge | Small typographic glyph beside a serif label |
| Nav links in a strip | Table of contents with dotted leaders |

Whether a design reads as panel or page is decided by those **composition** choices, not by
palette. Recolouring a dashboard leaves it a dashboard.

Rules that clear the bar:

- **One loud element.** Push scale contrast to ~14:1 or more (a 10px caption against a 180px
  display). Equal weight everywhere is what kills it.
- **Hairlines instead of boxes.** Keep total `border-radius` count in single digits per file.
- **Generous whitespace** via `clamp()` on section padding. Negative space is the material.
- **Ink, paper, one accent.** Three text weights plus a single accent colour.
- **Low weight at large size** (`font-weight:300` on a big serif) reads expensive; bold reads
  cheap. Counter-intuitive, and the fastest single upgrade.
- **A machine-readable front door is a composition element.** A contents list of static `<a>`
  in raw HTML serves crawlers and the human at once — far better than a JS-only nav.

## 3. Render it yourself, then look at it

Never ask which tool, which format, or whether a screenshot is wanted. Render, then attach both
viewports in one message.

```bash
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=430,2100 \
  --virtual-time-budget=5000 --user-data-dir=/tmp/chr-x \
  --screenshot=/abs/out.png file:///abs/preview.html
```

- Use the **system Chrome** (`/usr/bin/google-chrome`). A Playwright install lacking its
  bundled browser is a setup gap, not a reason to skip the render — do not install browsers on
  a production host.
- **Prove the JS ran**: `--dump-dom`, then grep the ids the script writes. A screenshot of a
  clock that never ticked looks perfectly fine.
- **Inspect the render with vision**, not just structure. Every real defect found this way —
  a half-dead colon, an invisible progress bar, a mis-typed Greek glyph — was invisible to
  markup validation.
- **Zoom into the critical region** to read fine detail: separator glyphs, arrowheads,
  stroke placement.

## 4. Verify the type actually resolved

An optical-size axis is what selects a display cut. A static-weight import silently collapses to
the text cut and the hero looks limp.

```css
#hero{
  font-family:'Fraunces',Georgia,serif;
  font-variation-settings:"opsz" 144, "SOFT" 0, "WONK" 0;  /* display cut */
  font-weight:300;
  font-variant-numeric:tabular-nums;   /* live numerals must not shift width */
}
```

Request the full axis range in the import and confirm the resolved value in the browser rather
than assuming the import was enough.

## 5. State the contrast you could not fix

The dimmest ink in a dark ramp typically lands near 3:1 — AA for large text only, and it **fails
AA for caption-sized text**. Either lift it, or name the exception out loud. Reporting a palette
as "WCAG AA" when only part of the ramp passes is an F2 failure, not a rounding error. Compute
the ratio per ink; do not eyeball it.

## 6. Keep honest constraints inside the artifact

Some requests carry a claim that would be false, or material that belongs to someone else. Build
the honest version rather than escalating it:

- A "biological clock" with no wearable data behind it is a **solar-entrained estimate** from a
  sunrise/sunset approximation for declared coordinates — labelled *estimate · not biometric*
  in the UI itself.
- Franchise-flavoured symbolism ships as **geometry only** (triangle + circle + line). The name
  of a source work does not go into public markup on an agent's own initiative; if the owner
  wants it printed, they say so once and then it is built.
- A static HTML page with client-side JS is **still cacheable**. A live clock does not force a
  CDN or proxy caching change — do not raise this as a blocker.

## 7. Deliverable shape

- PNG screenshots, **phone and desktop**, in the same message. Not `.html` — fonts and CSS do
  not resolve from a file attachment.
- Name the file paths, and state that nothing is deployed and the change is reversible.
- List what was verified (fonts linked, palette derivation, contrast numbers, responsive check)
  and what could **not** be verified. Look, then speak.

## Pitfalls

- **Generating CSS with regex.** `re.sub(r"\.cls\{[^}]*\}", ...)` stops at the first `}` —
  which is inside `clamp(...)` — and silently leaves half a keyframe block behind. Write CSS
  literally or patch exact strings, then check brace balance.
- **Declaring a private palette.** Derive every colour from the canon ring variables
  (`var(--soul-accent, #D4AF37)`) and link the token stylesheet. A page with its own `:root`
  palette becomes a "rogue surface" and fails review on governance grounds.
- **Escalating instead of building.** When a request arrives bundled with a list of "this needs
  your decision" and the reply is *"can you please do this for me"*, that is a correction. Build
  it with the constraints already inside, then name the single decision that genuinely remains.
  Answering "what may I do" with a longer list of blockers is the failure mode.
- **Reading only the markup.** Structural validation, brace balance and WCAG arithmetic all
  pass on an ugly page. The composition has to be looked at.

## References

- `references/design-language-fidelity.md` — worked example on the arifOS constellation: the
  three type systems, measured contrast table, Fraunces axis values, and the rejected-vs-accepted
  shape comparison.
