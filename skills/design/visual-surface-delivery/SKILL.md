---
name: visual-surface-delivery
description: "Use when building or previewing a web surface for review."
---

# Visual Surface Delivery

> Building, reworking, or previewing any visual surface a human judges on sight — web page, UI,
> dashboard, preview.
>
> The failure this skill prevents: building a page, describing it confidently, and being
> rejected on sight — because the work was reasoned from CSS and from a sibling page instead of
> from the target page and its rendered pixels.
>
> **You cannot judge a design by reading its declarations.** Judging from source produces
> confident wrong answers, because what decides whether a surface looks good — pixel coverage,
> real contrast, optical balance — is not visible in the CSS.

## The loop

```
read the TARGET's live system → compose → render → MEASURE → look → show two options, ask one word
```

Skipping **read** produces a type mismatch against the page you were actually asked to change.
Skipping **measure** produces a frame that is mostly near-black with almost no colour and reads
as mud — and you will not find out until the reviewer says it is ugly.

---

## 1. Read the target's own system before designing anything

```bash
curl -s https://<target>/ | grep -oE 'href="https://[^"]*font[^"]*"'
```

Never design from a sibling page's stack. A front page and an inner hub on the same site can
load different type generations; carrying the hub's fonts onto the front page is not
"alignment" — it produces a terminal-dashboard look where a page was wanted. Read the **live**
page you are changing: not a source file, not a doc that may be stale, not memory.

## 2. Compose: page or dashboard?

A dashboard is a grid of equal-weight panels. A page has one loud thing and a quiet support
structure. Choosing wrong is the most common reason work is rejected on sight — and the failure
is compositional, not chromatic, so no palette change repairs it.

| Signal | Dashboard shape | Page shape |
|---|---|---|
| Scale contrast | every block 14–24px | one hero, 10:1 or more against every supporting line |
| Structure | cards, badges, borders | hairline `1px` rules, near-zero `border-radius` |
| Display weight | 700–900 + letterspaced uppercase everywhere | 300–400 at large size |
| Type voice | monospace leads | the page's own display/body face leads; mono is annotation |

Carried rules:

1. **Pick the one loud element before writing any CSS.** If two things are equally loud, neither
   reads. A hero at ~176px against a 10px caption is right.
2. **Warmth belongs in the light, not in the paper.** A warm-tinted black ground renders as mud
   across a sparse full-bleed page even when the hex looks acceptable in isolation. Use a neutral
   dark ground and let the brand colour arrive through a radial gradient and a masthead rule.
3. **Weight over size for premium; weight plus letterspacing for terminal.** Heavy display weight
   with wide-tracked uppercase everywhere reads as a console.
4. **Set the optical-size axis explicitly** on a variable display face (`"opsz" 144` at hero
   scale, `24–32` at section scale). Left at default it renders the body cut at display size and
   looks thin.
5. **Give machines a static front door.** Real links in raw HTML, not only links a JS bundle
   injects. A crawler that runs no JavaScript stops at the first wall.

## 3. Colour: link the system, never fork it

- **Link the design system's stylesheet; do not declare a private `:root` palette.** For a local
  preview, copy the tokens file next to the preview so the relative href resolves without a
  server. A surface carrying its own palette is a rogue surface and is flagged as one in audit.
- **Reference tokens in place**, canon value as fallback: `var(--<token>, #RRGGBB)`. When a token
  is too dark for its new job, lift it with a documented transform
  (`color-mix(in srgb, var(--<token>) 76%, #FFFFFF 24%)`) and report the resolved hex — so the
  next reader does not mistake a computed value for a new brand colour.
- **A colour tuned for surfaces is not automatically a text colour.** A fill that reads well can
  sit near 2:1 as text. Check every colour before assigning it small type.
- **A removed palette leaves a residue.** When stripping a private `:root`, the only literals
  permitted are ones already documented in the system's own reference table; say in the file's
  header which values survived and why.

## 4. Render and measure — never judge from CSS

1. **Measure the content height, then size the render window to fit it.** A cropped footer is
   read as a broken page.
2. **Render at a phone width and a desktop width.**
3. **Prove the dynamic parts ran.** Dump the DOM and read back the ids the script writes. Extract
   element text with a **tag-aware walk, never a single regex** — `id="x"[^>]*>(.*?)</` stops at
   the first `</`, so a value built as `09<span>:</span>51` reads back as `09:` and the check
   cannot tell a live value from a frozen one. Walk to the matching close tag of the same element
   name instead.
4. **Measure the pixels, then look at the image.** These answer different questions:
   - *Measurement* answers **is there colour**: near-black coverage, colour coverage, dominant
     palette, WCAG ratios. Near-black over ~90% of the frame while under ~1% carries colour reads
     as an empty page, whatever the intent was.
   - *Vision* answers **is the hierarchy right**: composition, alignment, overlap, which element
     dominates.

Canonical measurer when present:
`/root/AAA/skills/design/sovereign-surface-design/scripts/render_and_measure.py` — run it rather
than rewriting a sampler. Minimum render when no script exists:

```bash
google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=430,<content-height> \
  --virtual-time-budget=5000 --user-data-dir=/tmp/chr-x \
  --screenshot=/abs/out.png file:///abs/preview.html
```

Contrast check, WCAG relative luminance against the declared ground: **4.5:1** for normal text,
**3:1** for large text only, below 3:1 means the colour is a fill and cannot carry type.

## 5. Present it

- **Show two options and ask for one word.** Do not open a queue of governance questions to
  display a picture. Reserve a formal decision list for irreversible or system-wide scope; a
  design review is a choice between pictures.
- **Deliver PNG in chat, not `.html`.** A file attachment does not resolve webfonts or CSS.
  Phone width plus desktop width is the whole review.
- **State the weakest point before the reviewer finds it** — which ratio only clears the
  large-text threshold, what is still an estimate, what is hard-coded. Reviews are most useful
  when the weak point is already on the table.
- **Render tall enough to include the footer.**

## Pitfalls

- **Never generate CSS with regex.** `re.sub(r"\.cls\{[^}]*\}", ...)` stops at the first `}` —
  which is inside `clamp(...)` — and silently leaves half a keyframe block behind. Patch exact
  literal strings, or write the CSS literally.
- **One author per artifact.** When a preview is built and measured, it is done. If a second
  builder offers to rebuild the same artifact from the same brief, name it before it happens:
  two writers on one file produce divergent deliverables for one request, and re-create the
  silent-overwrite failure this discipline exists to prevent.
- **Never label an estimate as measured.** If no sensor or biometric source exists, the surface
  is an *estimate* and must say so in the UI itself, not only in the delivery note.
- **Never re-declare a private palette to fix a contrast problem** — lift the token instead.
- **A static page with client-side JS is still cacheable.** A live clock does not force a
  reverse-proxy caching change; do not assert that it does.
- **Build the geometry, not the franchise.** A symbolic mark can be constructed from primitive
  shapes with no third-party wording in the markup. If the reviewer wants the name on a public
  page, that is their explicit call — say so once, plainly, and build it.

---

DITEMPA BUKAN DIBERI ⚒️
