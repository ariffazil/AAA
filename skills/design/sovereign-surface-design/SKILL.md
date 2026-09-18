---
name: sovereign-surface-design
description: "Use when designing or re-skinning a sovereign web surface."
---

# Sovereign Surface Design

> Designing a page the sovereign looks at once and accepts.
> The failure this skill exists to prevent: shipping a confidently-described page that gets
> rejected on sight — twice — because the design was reasoned from CSS and from a sibling
> page instead of from the target page and its rendered pixels.

## The loop

```
read the TARGET page's system → build → render → MEASURE → look → show two options
```

Skipping **read** produces a type mismatch. Skipping **measure** produces a page that is
mostly near-black with almost no colour and reads as mud — and you will not find out until
he says it is ugly.

---

## 1. Read the target page's own system before designing anything

```bash
curl -s https://arif-fazil.com/ | grep -oE 'href="https://[^"]*font[^"]*"'
```

**Never design from a sibling page's stack.** The front page loads an editorial serif
system; an inner hub page loads a different, heavier generation. Carrying the hub's fonts
onto the front page is not "alignment" — it produces a terminal-dashboard look where the
page should read as a front page. Read the page you are actually changing.

Verify against the live page. Do not assume the stack from memory, or from a doc that may
be stale.

## 2. Link the canon stylesheet; never declare a private `:root` palette

```html
<link rel="stylesheet" href="/_shared/design-system/tokens.css">
```

Reference tokens in place: `color: var(--soul-accent, #D4AF37)`. A page carrying its own
palette is a rogue surface, and is flagged as one in audit. For a local preview, copy
`tokens.css` next to the preview file so the relative href resolves without a server.

## 3. Know which canon colours may carry text

Ring colours are tuned for surfaces and glows, not for small type. The blood-red primary
sits near 2:1 on a dark ground — it is a fill colour, not a text colour. The gold accent is
the one that carries text comfortably. Full table in
`references/arif-fazil-type-and-color.md`.

When a canon colour is too dark for text, **lift it with a documented transform and say
so**: `color-mix(in srgb, var(--soul-primary) 76%, #FFFFFF 24%)`. Report the resolved hex in
the delivery note, so the next agent does not mistake a computed value for a new brand
colour.

## 4. The page ground must be neutral, not brown

A ring's own `--bg` token is a *brown*-black. Over a sparse full-bleed page that reads as
mud, not as black — even though the hex looks acceptable in isolation. Use a true neutral
ground (e.g. `#08080A`) for the page and let the ring colour supply the warmth through a
radial gradient and a masthead rule. **Warmth belongs in the light, not in the paper.**

## 5. Editorial means one loud element

- Scale contrast ratio of 10:1 or more between the hero and every supporting line (a 176px
  hero against a 10px caption is right).
- Structure with hairline `1px` rules — zero cards, zero badges, near-zero `border-radius`.
- Restrained weight (300–400) in a large serif reads as premium. Heavy weight plus
  letterspaced uppercase everywhere reads as a dashboard.
- Set the optical-size axis explicitly on a variable display face (`"opsz" 144` at hero
  scale, `24–32` at section scale). Left at default it renders the body cut at display size
  and looks thin.
- Give both humans and machines a static front door: real links in raw HTML, not only links
  that a JS bundle injects. A crawler that runs no JavaScript stops at the first wall.

## 6. Verify the render — measure, do not eyeball

```bash
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1440,1250 \
  --virtual-time-budget=5000 --user-data-dir=/tmp/chr-x \
  --screenshot=/abs/out.png file:///abs/preview.html
```

Three checks, in order:

1. **Did the JS run?** Dump the DOM (`--dump-dom`) and grep the ids the script writes. A
   screenshot of a clock that never ticked still looks fine.
2. **Measure the pixels.** Near-black coverage, colour coverage, dominant palette, WCAG
   ratios. "Dark and dull" is a measurement finding: near-black over ~90% of the frame while
   under ~1% carries colour. Run `scripts/render_and_measure.py` rather than rewriting the
   sampler each time.
3. **Then read the image with vision** for composition, alignment, hierarchy. Measurement
   answers "is there colour"; vision answers "is the hierarchy right".

## 7. How to present it

- **Show two options side by side and ask for one word.** Do not open a queue of governance
  questions to display a picture — a design review is a one-word answer, not a governance
  form. Reserve the binary queue for irreversible or canon-wide scope.
- **Deliver PNG in chat, not `.html`.** A file attachment does not resolve webfonts or CSS.
  Phone width plus desktop width is the whole review.
- **State the weakest point of what you shipped** — which ratio only clears the large-text
  threshold, what is still an estimate, what is hard-coded. He corrects most usefully when
  the weak point is already on the table.
- **Render tall enough to include the footer.** Cropping the bottom of a full-page shot
  reads as a broken page; pick the window height to fit the content.

## Pitfalls

- **Never generate CSS with regex.** `re.sub(r"\.cls\{[^}]*\}", ...)` stops at the first
  `}` — which is inside `clamp(...)` — and silently leaves half a keyframe block behind.
  Patch exact literal strings, or write the CSS literally.
- **Never `--check` live values with a regex that ends at the first `</`.** A clock built
  as `09<span>:</span>51` reads as `09:` because the lookahead stops at the inner span's
  closer. `scripts/render_and_measure.py:element_text` walks tags with a depth counter
  so the reported value is the live one. If you copy that function, copy the walker, not
  the regex.
- **Never label an estimate as measured.** If no biometric source exists, the surface is a
  *solar-entrained estimate* and must say so in the UI itself, not only in the delivery note.
- **Never re-declare a private palette to fix a contrast problem** — lift the token instead.
- **A static HTML page with client-side JS is still cacheable.** A live clock does not force
  a reverse-proxy caching change; do not assert that it does.
- **Never hand a preview to another agent lane when you can render it yourself.** The render
  is one command; delegating it adds a round trip and a second opinion that cannot see the
  file.

## Files

- `references/arif-fazil-type-and-color.md` — the live type stack, canon token → practical
  role, contrast table, and composition that was accepted versus rejected.
- `scripts/render_and_measure.py` — render an HTML preview at several widths, then report
  pixel coverage, dominant palette, WCAG ratios, and whether the JS wrote its values.

## See also

- `../web-surface-design-fidelity/` — companion skill for the "match an existing live
  site" lane. Its `references/design-language-fidelity.md` carries the worked example
  the canon tokens here abstract from. Read both before re-skinning any sovereign page.

---

DITEMPA BUKAN DIBERI ⚒️
