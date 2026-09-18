# Worked Example — Design Language Fidelity on the arifOS Constellation

Measured from the live site rather than from memory. Re-measure before trusting any value here;
the front page is the authority and it changes.

## The three type systems present on one constellation

| Surface | System | Character |
|---|---|---|
| Front page (`index.html`) | **Fraunces** (variable, optical size 9–144) + **Newsreader** + **IBM Plex Mono** | editorial / printed page |
| `/world/` hub | Archivo Black + Space Grotesk + JetBrains Mono | older hub set, panel-like |
| `/words/` | `var(--font-display)` / `var(--font-sans)` / `var(--font-mono)` | canon tokens |
| `tokens.css` | `--font-sans: 'Inter'`, `--font-mono: 'JetBrains Mono'` | canon, but **legacy** for editorial surfaces |

**The error this table exists to prevent:** styling the front page with the `/world/` hub's older
set. Both are live, both are legitimate, only one belongs on the front page.

Commands used to establish it:

```bash
curl -s https://arif-fazil.com/ -o /tmp/prod.html
grep -oE 'href="https://[^"]*font[^"]*"' /tmp/prod.html
grep -oE 'font-family:[^;}]+' /tmp/prod.html | sort -u
curl -s https://arif-fazil.com/world/ | grep -oE 'font-family:[^;}]+' | sort -u
```

## Fraunces usage

```css
#clock{
  font-family:'Fraunces',Georgia,serif;
  font-variation-settings:"opsz" 144, "SOFT" 0, "WONK" 0;   /* display cut */
  font-weight:300;
  font-size:clamp(3.6rem,15.5vw,11.5rem);
  letter-spacing:-.035em;
  font-variant-numeric:tabular-nums;
  font-feature-settings:"tnum" 1;
}
```

- `opsz 144` = display cut; `opsz 24` = small-heading cut.
- Import pattern: `family=Fraunces:ital,opsz,wght@0,9..144,100..900;1,9..144,100..900`
- `tabular-nums` is mandatory on any ticking numeral grid.
- Self-hosting the two variable fonts removes the network dependency and keeps the design
  identical offline.

## Rejected shape vs accepted shape

| Rejected (dashboard) | Accepted (page) |
|---|---|
| Seven-segment LED digits | Display serif numerals |
| Monospace uppercase caption on every label | Italic serif captions |
| Cards, badges, `border-radius`, shadows | 1px hairline rules |
| Three equal-weight cards in a grid | One hero + a three-column ledger band on hairlines |
| Boxes as containers | Negative space as the container |
| Eight-colour segmented band | One continuous gradient band |
| Emblem inside a rounded badge | Three small typographic glyphs beside serif labels |
| Nav links in a strip | Table of contents with dotted leaders |

Both versions passed markup validation, brace balance and a WCAG pass. Only one was accepted.

## Palette derivation — no private palette

```css
:root{
  --paper: var(--soul-bg,             #1A0A0A);
  --ink:   var(--soul-text,           #F5E8E8);
  --gold:  var(--soul-accent,         #D4AF37);
  --blood: var(--soul-primary,        #8B1A1A);
  --cyan:  var(--mind-primary,        #00D4AA);
}
```

Copy `sites/arif-fazil.com/public/_shared/design-system/tokens.css` beside a local preview so a
relative `href="_shared/design-system/tokens.css"` resolves offline, then reference `var(--soul-*)`
with fallbacks.

## Measured contrast on the deep blood-black paper (`#1A0A0A`)

| Ink | Ratio | Verdict |
|---|---|---|
| `--soul-text` #F5E8E8 | ~16:1 | AA |
| `#A99C95` secondary | ~7.5:1 | AA |
| `--soul-accent` #D4AF37 gold | ~9.5:1 | AA |
| `#6B5F5A` dimmest | ~3.2:1 | **large text only — fails AA for captions** |

The dimmest ink is normally reserved for coordinates, ticks and the colophon. Either lift it
toward `#8A7A73` or declare the exception explicitly.

## Species checks that caught real defects

| Check | Defect it caught |
|---|---|
| Zoom-crop the hero region | A separator rendered as a single period instead of a stacked colon |
| Zoom-crop the progress element | A 1px bar at low opacity read as a static rule, not a fill |
| Grep the glyph inventory | A Greek letter written as the wrong symbol (Σ where Ψ belonged) |
| `--dump-dom` after render | Confirmed the ticking numerals were written by JS, not hard-coded |
| Contrast arithmetic per ink | Established exactly which inks fail AA at caption size |

## Local preview layout

```
<workdir>/
  variant-<design>.html
  _shared/design-system/tokens.css     # copied from the source tree so the link resolves
  render.py                            # headless-Chrome screenshot loop, both viewports
  verify.py                            # static checks + live-DOM grep + contrast arithmetic
  shot-<name>-phone.png / -desk.png
```

Keep every preview inside a dedicated work directory, state that nothing is deployed, and note
that deleting the directory restores a clean state.
