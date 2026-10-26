---
name: cover-art-pipeline
version: 1.0.0
description: Use when a media list needs real posters embedded.
author: hermes-curator
license: sovereign-internal
metadata:
  hermes:
    tags: [media, posters, html-artifact, api]
    related_skills: [curated-recommendation-artifact, visual-artifact-delivery]
floor_scope: [F2, F4, F9, F12]
autonomy_tier: T1
---

# Cover Art Pipeline (keyless)

Fetch real posters for a list of films/shows, verify each match, shrink, embed as data URIs.
Use alongside `curated-recommendation-artifact` (ranking rules) or any artifact that lists titles.

## When to Use

Any artifact that shows a film/show/book grid: a ranked recommendation page, a watchlist card, a
comparison of two people's picks. Real artwork from a public metadata API — never generate a fake
poster for a real title.

## 1. Fetch (TVMaze, no key, no quota)

```python
import json, urllib.request, urllib.parse

def show(title):
    u = "https://api.tvmaze.com/singlesearch/shows?q=" + urllib.parse.quote(title)
    req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(req, timeout=20))
```

Keep: `name`, `premiered` (year), `genres`, `rating.average`, `network.name` / `webChannel.name`,
`image.medium|original`.

## 2. Verify the match — every single title

`singlesearch` is fuzzy and returns whatever scores closest: a global heist hit resolves to its
regional spin-off, an all-caps sports documentary brand resolves to an unrelated drama sharing one
word. Check returned `name`, `network` and premiere year against what you meant; on mismatch re-query
with a disambiguating string (original-language title, year, full subtitle) and re-verify. A wrong
poster is a fabricated detail attached to a real recommendation.

## 3. Shrink and embed

Originals run 0.5–2 MB each. Never inline them raw.

```python
from PIL import Image
import io, base64

im = Image.open(io.BytesIO(raw)).convert("RGB")
im.thumbnail((300, 450), Image.LANCZOS)          # 2:3 poster
buf = io.BytesIO(); im.save(buf, "JPEG", quality=82, optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode()  # 15-40 KB each
```

33 posters ≈ 0.8 MB total — light enough to forward, heavy enough that the grid looks real.

## 4. Resolve by canonical name, then assert

APIs normalise on the way back (`BEEF` → `Beef`, `MAID` → `Maid`). A dict keyed by your own query
strings raises `KeyError` mid-render, after the whole fetch has already run.

```python
low = {k.lower(): v for k, v in meta.items()}
def resolve(title):
    return meta.get(title) or low[title.lower()]
```

Assert `len(cards) == requested_total` before writing the file, and print the miss list rather than
emitting a card with a blank `<img>`.

## 5. Compose

- Build each card in code, join the rail string, substitute into a `{{RAILS}}` placeholder in a
template file — hand-writing 30+ cards guarantees drift.
- Poster box 2:3 (`202x303` desktop, `170x255` under 640 px), rank numeral behind the left edge,
match badge top-right, platform chip bottom-left, horizontal rail with visible scrollbar.
- Tag the originating network, not the platform you assume carries the title: catalogues differ by
country and change monthly.

## 6. Assert the rendered page

```
document.querySelectorAll('.card').length
document.images.length
Array.from(document.images).filter(i => i.naturalWidth > 0).length
```

All three equal the requested count or the build is broken; a zero on the third with a full first
count means the data URI or the path failed. Screenshot a ~1280 px viewport for the chat preview and
send the HTML file alongside it.
