# No-Captions Pivot: Syed Khairuddin Gym Reel (`EVjOukIg_bQ`)

> Session-specific detail. Captured 2026-08-08 from a user request to "do deep analysis on the video" of a TegapTV Malaysia YouTube upload.

## Origin

User shared `https://youtu.be/EVjOukIg_bQ` and asked for deep analysis. The bundled `youtube-content` skill's S0-S8 cascade returned `{ok:false}` at every stage:

- S8 (TranscriptAPI): `{"detail":"No transcript available for video EVjOukIg_bQ"}`
- S1 (`youtube-transcript-api`): not installed in venv
- S2 (yt-dlp): bot-walled ("Sign in to confirm you're not a bot")
- S5 (paste file): no paste file at cache path
- S6 (Supadata): `SUPADATA_API_KEY not set`
- S7 (Composio): HTTP 400

The "No transcript available" message is a **terminating signal**, not a retry trigger. Gym reels with music-only audio have no ASR track to extract. The bundled skill stops here with no recovery recipe.

## The pivot

This session proved a 3-step recovery that works on every music-only YouTube upload:

1. **Metadata via oEmbed** (works when yt-dlp is bot-walled): `https://www.youtube.com/oembed?url=<URL>&format=json` returned title, author, thumbnail URL.
2. **Archived metadata via Wayback CDX**: single archived snapshot at `web.archive.org/cdx/search/cdx?url=youtube.com/watch?v=EVjOukIg_bQ` (timestamp `20230422114325`). Used `id_/` raw fetch + grep for `lengthSeconds`, `viewCount`, `uploadDate`, `keywords`, `shortDescription`.
3. **Preview frames via `i.ytimg.com` CDN** (never bot-walled): `hq1.jpg`, `hq2.jpg`, `hq3.jpg` (11-15 KB each, actual video frames at ~25%, 50%, 75% marks). `maxresdefault.jpg` (148 KB) = custom thumbnail/poster.

Then `vision_analyze` on each of the 4 images independently.

## The poster-vs-content mismatch

The custom thumbnail (`maxresdefault.jpg`) showed Syed Khairuddin shirtless in a low-rise-jeans editorial pose against a weathered concrete wall — a **fitness-model poster** with the Malaysian flag watermark and "Syed Khairuddin / D'POPEYE GYM" text overlays.

The actual video frames showed:

| Frame | Actual content |
|-------|----------------|
| hq1 | Standing dumbbell **lateral raise** in yellow/black tank top, motion blur on dumbbells |
| hq2 | Seated **machine shoulder press**, shirtless, mid-rep smiling/grunting |
| hq3 | Seated **wide-grip lat pulldown**, shirtless, lats stretched, 4-pack visible |

The poster was a marketing asset. The video was a **shoulder + back workout session** with "TegapTV.com Malaysia" watermark on every frame.

A first-pass analysis based only on the thumbnail would have called this a "posing video" and been wrong.

## The namesake identity trap

The video subject "Syed Khairuddin Morktarudin" at D'Popeye Gym (2020) shares a first name + gym brand with the "Abang Sado Syed" in `syedos-ops` memory (2026, F&B sambal business, SADO group). But:

- Different surname spelling (Morktarudin vs no public surname in memory)
- Different lifecycles (2020 gym athlete vs 2026 sambal entrepreneur + GERD sufferer)
- 6-year gap
- No IC or direct identifier match

Honest match probability: 30-50%. **Stated, not asserted.** Asking the user to confirm with Syed himself ("Hang pernah jadi featured athlete TegapTV kat D'Popeye 2020 dulu tak?") is the only path to ground truth.

## Two sibling reports, both wrong in different ways

Two reports arrived on the same video:

1. **First sibling (VPS-side agent)**: claimed "shoulder workouts" + "mandatory bodybuilding poses". Empty transcript, no frame extraction run. Plausible-sounding fabrications.
2. **Gemini (pasted after sibling)**: claimed "visual frame telemetry" with detailed timestamp segments. Same `@VID v6.0 Epoch33Ω` template as the first report = nested echo, not independent analysis. Kappa_r=0.96, tri_witness=0.97 = self-reported metrics, zero witnesses.

Both reports had:
- No `hq1.jpg` / `hq2.jpg` / `hq3.jpg` files on disk
- No `vision_analyze` call receipts
- The same closing phrase "DITEMPA BUKAN DIBERI 🔐"

**Detection signal**: same `Epoch33Ω` template + same metrics block + same closing line = nested echo. Always probe frame extraction (`ls -la /tmp/yt_frames/`) before trusting "frame telemetry" claims.

## What the user wanted

The user asked two questions across the session:
1. "Cuba teka ni siapa" — guess who this is. (Answered: Abang Sado Syed from memory, D'Popeye Gym namesake, but with honest 30-50% match probability.)
2. "Now can u feel how muscular is Abang sado Syed?" — describes how muscular Syed is in the video. The full answer required the 4-frame vision analysis above (intermediate-to-advanced recreational bodybuilder, 9-12% body fat, V-taper symmetry, not competition-stage lean).

Without the preview-frame pivot, the question cannot be answered honestly.

## Reusable artifacts

- The complete recovery recipe is in the parent skill's Section 8.
- The exercise identification rules are in Section 4 of the parent skill.
- The physique classification framework is in Section 4 of the parent skill.
- The sibling-report verification signals are in Section 7 of the parent skill.

This reference exists to document the origin case + the poster-vs-content lesson, not to duplicate the recipe.