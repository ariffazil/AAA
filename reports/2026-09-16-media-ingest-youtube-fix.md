# RECEIPT — media-ingest / YouTube capability fix (KVM8)

- When: 2026-09-15T17:45:26.956571+00:00 (UTC) · 2026-09-16 ~01:55 MYT
- Authority: F13 (Arif, DM) — "Fix my Hermes YouTube skills capabilities and intelligence tools"
- Scope: READ-ONLY retrieval tooling + skill docs. No governance/canon/kernel touched.

## Defects found (all reproduced live)
1. **YouTube media lane was audio-only** — `formats:["audio"]` gives an MP3, so frames were
   structurally impossible; and it intermittently returns `SCRAPE_MEDIA_ACCESS_DENIED`.
   The working lane (`formats:["video"]` → MP4 with both streams + duration metadata) was
   not wired. yt-dlp YouTube = intermittent per-request bot check, recorded as permanent.
2. **Fabrication path open** — a 9m32s music-only video produced 87 chars of Whisper
   hallucination ("you you you …") which was written to `transcript` and stamped
   `truth_state=OBSERVED`. Junk read as success.
3. **Frame sampler read the intro only** — `fps=0.5` + `-frames:v 6` = first 12 seconds of a
   9m32s video; no de-dup, no contact sheet. `frames` empty on the real payload.
4. **Receipt cried wolf** — `blocking_reason` carried the yt-dlp bot-check string on a run
   that had in fact read 18 frames (artifact.md said "download blocked" next to a contact sheet).
5. **Skill unloadable** — `youtube-extraction-datacenter-ip` resolved to 2 distinct files in
   the profile skills dir → `skill_view` refused ("Ambiguous skill name") → dead skill.
   Root cause: a stray duplicate directory + a stray nested self-copy.

## Fixes (files)
- `/root/.hermes/tools/media_ingest/media_ingest.py` (backup `.bak-20260915T173816Z`)
  - `_fc_scrape()` retry/backoff for transient Firecrawl media denial
  - `lane_firecrawl_video()` (primary YouTube lane) + `meta_from_firecrawl()` (duration/published)
  - `lane_frames()` rewritten: adaptive whole-timeline fps, 4x4 average-hash de-dup, contact sheet
  - `stt_degenerate_reason()` guard; degenerate STT rejected → `transcript_rejected.txt`
  - Artifact gains `frames[]`, `contact_sheet`, `content_read`, `transcript_state`
  - truth model: OBSERVED = transcript **or** frames; `blocking_reason` cleared on success
  - CLI: `--text-only`, `doctor --deep`
- `/root/.hermes/mcp/media-ingest/server.py` — schema/docstring updates, `text_only` param,
  frames/contact_sheet passthrough, file tool uses the same degeneracy guard
- Skills: `media-ingest-lane` v1.1.0 · `youtube-extraction-datacenter-ip` (rewritten) ·
  `AAA-video-emd-pipeline` (fallback ladder → composed lane) · `FORGE-skill-linter`
  (+`scripts/skill_resolution_audit.py`, L3 Resolution-Failure class)
- Hygiene: removed stray dup dirs; renamed misnamed nested skill dirs
  (`FORGE-onboarding/claude`→`agent-onboarding`, `apex_verdict_hold/claude`→`arifos-act`,
  AAA `forge-onboarding/claude`→`agent-onboarding` via git mv). audit: 383 skills, 0 collisions.

## Verified (live, same URL)
`Mr Enrich On The Go 2026 (Posedown)` — duration 572s (was null), published 2026-09-10,
`firecrawl_video=ok`, 18 frames kept (de-dup), contact_sheet.jpg, STT junk rejected,
`content_read=[media,frames]`, `truth_state=OBSERVED`, `blocking_reason=""`.
MCP surface confirmed live: `media_ingest_url(url,text_only)` · `media_ingest_file` ·
`media_lane_doctor(deep)`.

## Residual / open
- Firecrawl video lane costs ~5 credits/call; cost ledger not yet metered per-run.
- Audio-only sources (podcasts) still route through the flakier audio format — retried, not eliminated.
- x/Twitter lane still untested.
