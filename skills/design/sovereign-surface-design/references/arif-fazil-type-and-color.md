# arif-fazil.com — type and colour reference

Depth for `sovereign-surface-design` §1–§5. Load when building or re-skinning any page on
the sovereign's constellation.

## Read the live type system, do not assume it

```bash
curl -s https://arif-fazil.com/ | grep -oE 'href="https://[^"]*font[^"]*"'
```

| Surface | Display | Body | Mono |
|---|---|---|---|
| Front page `/` | Fraunces | Newsreader | IBM Plex Mono |
| `/world/` hub | Archivo Black | Space Grotesk | JetBrains Mono |

The front page is editorial serif. The `/world/` hub is a different generation with a
geometric sans and a heavy display face. Never carry one stack onto the other — pick the
stack the page you are editing actually loads.

Fraunces carries an optical-size axis. Set it explicitly: `"opsz" 144` at hero scale,
`"opsz" 24–32` at section scale. The default renders the body cut at display size.

## Canon tokens → practical role

Link `/_shared/design-system/tokens.css`. Never re-declare `:root`.

| Token | Value | Ring | Practical role |
|---|---|---|---|
| `--soul-primary` | #8B1A1A | SOUL | fill, rule, field — too dark for text |
| `--soul-secondary` | #B33030 | SOUL | display / large text only |
| `--soul-accent` | #D4AF37 | SOUL | text, marks, primary accent |
| `--mind-primary` | #00D4AA | MIND | text, marks |
| `--body-primary` | #D4A853 | BODY | text, marks |
| `--soul-bg` | #1A0A0A | SOUL | ring surface — NOT a full-page ground |
| `--soul-text` | #F5E8E8 | SOUL | body text |

## Contrast against a neutral dark ground (#08080A)

| Colour | Ratio | Verdict |
|---|---|---|
| #F4F1EE — ink | 17.8:1 | AA text |
| #ADA6A1 — ink-2 | 8.3:1 | AA text |
| #867D78 — ink-3 | 5.0:1 | AA text |
| #D4AF37 — gold | 9.5:1 | AA text |
| #E8C55A — gold lifted | 12.0:1 | AA text |
| #B33030 | 3.2:1 | large text only |
| #a75151 — blood mixed 76% with white | 3.8:1 | large text only |
| #8B1A1A — blood | 2.2:1 | field only |

Set the floor for small supporting text at `#867D78` or lighter. Anything darker fails AA at
small sizes even when it looks acceptable on a bright monitor.

If a lifted colour is used as the page primary, it will read as a soft coral rather than as
blood — say that plainly instead of claiming the canon red is on screen. If the canon colour
cannot carry text without leaving the token, recommend the accent that can.

## Composition: rejected versus accepted

**Rejected on sight**

- many equal-weight boxes and badges
- heavy display weight with letterspaced uppercase as the dominant voice
- monospace as the primary typographic voice
- a brown-black ground, described as "dark"
- a ring of flat colour blocks standing in for a gradient

**Accepted**

- one loud element, with a scale contrast ratio of 10:1 or more against everything else
- hairline rules instead of cards; no rounded corners
- restrained display weight (300–400) at large size
- a neutral dark ground with the ring colour arriving as light
- a contents list with dotted leaders — a front door a machine can read without running JS
- the weakest point named in the delivery note before he finds it
