# Showing two people as equals

When a card must carry TWO subjects, the form decides what the card claims about them. Most chart
forms rank. A taijitu does not — and that is the only reason to use one.

## Measure first, then do NOT draw it to scale

Get the real numbers, then refuse to chart them against each other. Rank-encoding two humans
(message counts, output, hours, followers, sessions, revenue) renders one as a fraction of the
other, which asserts something about the relationship the numbers do not support.

**Volume is not weight.** Posting more, training longer or shipping faster is a count, not a measure
of who matters. If the ratio is lopsided, that is precisely the evidence that a shared axis would
lie — so use a form that structurally *cannot* encode magnitude.

## The form

Two interlocking halves of equal area. Each half carries a dot of the OPPOSITE colour: what each one
needs sits outside his own domain. The card asserts that shape and stops. No scores, no "this week
you did X", no comparison sentence — it is a balance, not a report card.

## SVG geometry

Three arcs over a filled disc:

- Fill the disc in the light colour.
- Dark half = one half-circle arc + two smaller opposite-side arcs of radius `r/2`.
- Two dots of radius `~r/7`, centred `r/2` above and below the disc centre.
- Clip the dark path to the disc so the shape stays circular.

Flipping the orientation flips which head is where. Build BOTH orientations onto one test page and
look at them once before choosing — orientation errors are obvious side by side and invisible in the
code.

### The dot-contrast trap

The dots must invert against the half they sit in. A dark dot on the dark head is invisible and the
symbol degrades into two plain blobs. Derive the colour from the container instead of writing it
literally:

```python
dot_in_dark  = LIGHT
dot_in_light = DARK
lower_dot = dot_in_dark  if dark_head_at_bottom else dot_in_light
upper_dot = dot_in_light if dark_head_at_bottom else dot_in_dark
```

Tie the dot colour to the SAME flag that flips the geometry, so flipping one cannot leave the other
stale.

## Content pairing

One item per side, opposing **abstract vs concrete** rather than better vs worse:

- read rock / read the body · millions of years / one rep · take from the earth / build from the body
- what rose / what held · what was thought / what was done · what is far / what is near

## Rendering: render tall, then crop the tail

Chrome's `--screenshot` captures **exactly** the window height. Too short clips the bottom; too tall
ships a dead band. Set a height well above any realistic content (2600 for a ~1400px card) and trim
the trailing background rows:

```python
def autocrop_tail(png, tol=24, scan_step=4):
    from PIL import Image
    im = Image.open(png).convert("RGB")
    w, h = im.size
    bg = im.getpixel((2, 2))
    if not isinstance(bg, tuple):
        bg = (bg, bg, bg)
    for y in range(h - 1, 0, -scan_step):
        for x in range(0, w, 8):
            p = im.getpixel((x, y))
            pp = p if isinstance(p, tuple) else (p, p, p)
            if sum(abs(int(a) - int(b)) for a, b in zip(pp, bg)) > tol:
                im.crop((0, 0, w, y + 1)).save(png)
                return w, y + 1
    return w, h
```

One window height then works for every layout, and nothing needs re-tuning when the copy changes
length.

## Label ambiguity

Any label whose name is also a division on another scale needs a glyph or an explicit noun. A lunar
phase name like "first quarter" sitting beside a date reads as a **calendar** quarter and makes the
card look wrong in every month outside Q1. Prefix it with the glyph and the noun
(`◐ moon phase: first quarter`) — four characters versus a reader quietly distrusting the graphic.

## Verification checklist

- Name the elements in the vision question: *is each dot present and contrasted against its own
  half?* A general "any defects?" returns "looks good" over an invisible element.
- Confirm the corner pixels are the page ground, not a panel edge.
- Confirm the last text line sits fully inside the frame AFTER cropping.
- Two artifacts is the ceiling when two are asked for. Do not add a chart, a source table or a spare
  variant "for completeness".
