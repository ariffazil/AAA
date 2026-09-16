---
id: forge-real-person-reference-photos
name: Real-Person Reference Photos — Anti-Fabrication
version: 1.0.0
description: "Real-person photo: Wikimedia first, attribute, no T2I."
owner: AAA
risk_tier: medium
floor_scope:
  - F02
  - F09
  - F11
autonomy_tier: T1
capability_tier: fed-multimodal-vision
ecology_state: COLD
forged: 2026-08-27
forged_by: FI-001 (Hermes) on scar from SADO group session
constitutional_floor: F2 TRUTH + F9 ANTI-HANTU + F11 AUDIT
f13_directive: >
  This skill is structurally binding. Any T2I dispatch labeled or implied
  as a specific named real person MUST first pass through the Wikimedia
  Commons route. The pipe cannot compile a fabricated-person payload.
---

# Real-Person Reference Photos — Anti-Fabrication

> "Buat ja la yang arif lagi bijaksana" — Arif's verdict on honest framing.
> Trust verified + dark-horse-labelled > fabricated perfect score.

## The Hard Rule (F2 TRUTH)

> A T2I diffusion call **MUST NOT** produce an image labeled or implied
> as a specific real, named, identifiable person. The diffusion prior
> produces a person-like image, not a person.

When the user wants a photo of a real person (profile page, tribute,
inspiration gallery, side-by-side comparison), the agent MUST NOT
default to T2I. The default reflex is wrong; the trap fires silently.

## When to Use This Skill

Trigger on any user request that mentions a **named person** + an
**image / photo / portrait** need:

- *"Build me a profile page for [named person] with their picture."*
- *"Reference photo of [named athlete / public figure]."*
- *"Side-by-side [person A] vs [person B]."*
- *"Tribute to [named person]."*

Do NOT trigger for:

- Fictional characters (T2I is fine).
- Generic stock-photo requests (no specific person named).
- AI-generated concept art where the user explicitly wants
  "an illustration, not the actual person."

## Canonical Workflow

### Step 1 — Wikimedia Commons search

```bash
# Find candidate files via the category page
curl -sL -A "Mozilla/5.0 arifOS-research" \
  "https://commons.wikimedia.org/wiki/Category:<Subject_Name>" \
  | grep -oE 'href="/wiki/File:[^"]*<Subject>[^"]*"' \
  | sort -u
```

Many adult entertainers, athletes, politicians, and historical figures
have CC-licensed photos with verifiable attribution. Wikimedia Commons
is the first stop because attribution is built-in.

### Step 2 — Download candidates

Wikimedia returns HTML error page for invalid thumbnail sizes (HTTP 400
with "Use thumbnail sizes listed on https://w.wiki/GHai"). Use
`Special:FilePath/` for reliable full-resolution delivery:

```bash
curl -sL \
  -A "arifOS-research/1.0 (educational use; contact <email>)" \
  -o /tmp/<candidate>.jpg \
  "https://commons.wikimedia.org/wiki/Special:FilePath/<exact_filename>"
```

Verify with `file /tmp/<candidate>.jpg` — expect `JPEG image data`,
NOT `HTML document`. Download 3-4 candidates to allow visual filtering.

### Step 3 — Visual filtering with `vision_analyze`

```
vision_analyze(
  image_url="/tmp/<candidate>.jpg",
  question=(
    "Describe the image — what's shown, person's appearance, pose, "
    "expression, setting. Confirm modest or note exposure level. "
    "Suitable for a public-facing reference page?"
  )
)
```

Reject if:
- Cleavage-exposed / NSFW (unless user confirms audience).
- Low resolution (<500px on long edge).
- Watermarked.
- Subject not actually identifiable as the named person.

### Step 4 — Embed with attribution block

```html
<div class="photo-credit">
  <strong>Image credits</strong><br>
  <Subject> portrait:
    <a href="<commons_file_url>" target="_blank" rel="noopener">
      Wikimedia Commons</a> ·
    Photo by <a href="<flickr_or_author_url>" target="_blank" rel="noopener">
      <author_handle></a> ·
    Licensed <a href="https://creativecommons.org/licenses/by/3.0/"
      target="_blank" rel="noopener">CC BY 3.0</a>
</div>
```

The three linked pieces — source, author, license — are non-negotiable.
CC license requires attribution.

### Step 5 — If no Commons photo exists

Stop and ask. Do NOT fall back to T2I. Three options to present:

1. **AI-generated concept portrait** with explicit
   `AI-generated, not the real person` label visible on the page.
2. **Typography-only hero** — no photo at all, just the name + stats.
3. **User supplies their own photo** (e.g. they have a license to use it).

## Side-by-Side Pattern (multiple photos on one page)

When the page has multiple portraits (e.g. *"Aletta Ocean vs reference
physique"*), every photo must be addressed:

- **Photo of a public figure** → full Wikimedia attribution block.
- **User-supplied photo of a known person** → explicit
  `staging photo supplied by user — not attributed to a specific individual`.
- **AI-generated portrait** → explicit
  `AI-generated concept — not the actual [subject]`.

Label every photo in the credit block. No orphan images. Inconsistent
integrity (one attributed, one not) is itself a fabrication signal.

## Visual Authenticity Self-Check

If T2I was used for any reason (concept art, mood board), the agent
MUST run `vision_analyze` self-check BEFORE shipping if the output
might be confused for a real person:

```
vision_analyze(
  image_url=<output_path>,
  question=(
    "Describe the image. Is this a real photograph of a specific person "
    "or an AI-generated / stock / reference image? Any identifying marks?"
  )
)
```

If "AI-generated" appears in the answer — the agent must NOT proceed
with the page. Re-route to the Wikimedia workflow.

## Pitfalls Captured (2026-08-27)

| Pitfall | Fix |
|---|---|
| T2I prompt from bio → shipped as if real | Wikimedia Commons first, every time |
| Wikimedia thumbnail size invalid (HTTP 400) | Use `Special:FilePath/`, verify with `file` |
| Page side-by-side: one attributed, one orphan | Label every photo in credit block |
| Wikimedia photo has cleavage exposure | Download multiple candidates, visually filter |
| Caddy static-cache returns 200 after file delete | Confirm with `ls` not just HTTP status |
| AI-generated photo with no label | Visible caption OR drop the photo |

## Honest Disclosure Patterns

When T2I IS the right choice (no real person involved), label honestly:

- `"AI-generated concept portrait — not a real person"`
- `"Editorial illustration inspired by [subject category]"`
- `"Reference mood, not the actual [person/place]"`

This is the F7 HUMILITY sweet spot. The user prefers verified +
dark-horse-labelled over fabricated perfect scores.

## Files & Telemetry

- Scar conversation: 2026-08-27, SADO group, artifact published at
  `syedos.arif-fazil.com/sado-reference/`
- Memory anchor: `MEMORY.md` "FABRICATION SCAR (8/27)"
- Companion reference: this skill complements `forge-vision-densify`
  (T2I governance) and `forge-multimodal-router` (multimodal dispatch
  routing) but is the canonical owner of the **real-person photo**
  workflow specifically.

## Verification

Test prompts before SEAL:

1. **Named person + photo request** ("build Aletta Ocean profile with
   picture"): Wikimedia Commons search runs FIRST, no T2I dispatch until
   real photo is found or user is asked.
2. **No name, just category** ("generate a portrait of a bodybuilder"):
   T2I is acceptable, but if the result looks like a specific named
   person, the disclosure caption fires.
3. **Fictional character** ("draw a wizard for the game"): T2I normal,
   no special routing.

---

DITEMPA BUKAN DIBERI ⚒️
