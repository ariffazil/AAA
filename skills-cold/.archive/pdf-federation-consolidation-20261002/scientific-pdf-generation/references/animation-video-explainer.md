# Animation + Voice Video Explainer — Pattern

## When to Use
When the deliverable is a short animated explainer video (30s–3min) with voice narration — for explaining a technical event, process, or concept to a non-expert audience. Proven use cases: geological hazard explanation (Bhote Koshi GLOF), financial mechanism walkthroughs, public-health briefings, civic explainers.

This is the video counterpart to Mode B intelligence dossiers — same dark theme, same audience tier (working professional, peer, or curious public), but rendered as MOVING VISUALS + NARRATION instead of static PDF pages.

## Three-Stage Pipeline

### Stage 1 — matplotlib Animation → MP4

Use `matplotlib.animation.FuncAnimation` with a single `init()` + frame-driven `animate(frame)`. Define PHASE boundaries at the top of the script so timing is auditable:

```python
PHASE1_END = 90      # ~6s @ 15fps
PHASE2_END = 225     # ~9s
PHASE3_END = 405     # ~12s
PHASE4_END = 810     # ~27s
TOTAL_FRAMES = 900   # 60s total

def animate(frame):
    progress = (frame - PHASE1_END) / (PHASE2_END - PHASE1_END)
    # ... build/clear patches for this phase
```

Render with ffmpeg writer:
```python
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, bitrate=2400, metadata=dict(artist='i-ARIF'))
ani.save('/tmp/output.mp4', writer=writer, dpi=100)
```

**Frame budget rule:** 900 frames × 15fps = 60 seconds. Anything more than 1050 frames starts to feel sluggish during rendering (~10 minutes wall time). Keep narrations under 90 seconds unless the user explicitly wants longer.

### Stage 2 — TTS Voice → OGG

Use the `text_to_speech` tool (already wired to voice pipeline). BM Penang female voice by default. Write for a non-expert audience — short sentences, no jargon, plain analogies (e.g. "macam empangan yang pecah"). Aim for 80–100 words/minute for natural pacing.

Keep the narration self-contained — assume the listener cannot see the visuals. Describe WHAT is happening and WHY, not the chart axes.

### Stage 3 — ffmpeg Combine

When animation < narration duration, LOOP the animation:

```bash
ffmpeg -stream_loop 2 \
  -i /tmp/animation.mp4 \
  -i /tmp/narrative.ogg \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  -shortest \
  -pix_fmt yuv420p \
  -vf "fps=15" \
  /tmp/final_combined.mp4
```

The `-shortest` flag terminates output at the shorter stream — without it, you get extra silence at the end. `-pix_fmt yuv420p` ensures the output plays in standard players (raw matplotlib output can be yuv444p which some players reject).

## Pitfalls (from this session — encode so future runs don't repeat them)

### matplotlib
- **`ax.plot()` returns a LIST, not a single object.** Code like `wave_foam_line.remove()` fails with `TypeError: list.remove() takes exactly one argument (0 given)`. Fix: track foam line as `wave_foam_line, = ax.plot(...)` (note the trailing comma unpacking) OR clear with `for p in wave_foam_line: p.remove()`.
- **Emoji glyphs missing from DejaVu Sans.** `⏱️⚠️💀📋` print as empty boxes in the saved video. Use plain text labels instead: "PHASE 1 (0-15 min)", "PHASE 3 — CRITICAL", "PHASE 4", "AFTERMATH". Cosmetic warning, not fatal — but text looks broken.
- **Aspect ratio trap: `set_aspect('equal')` on tall cross-sections.** Causes matplotlib to stretch the figure canvas vertically until it exceeds 20,000 pixels tall and the saved PNG/MP4 has absurd aspect. Use `set_aspect(0.5)` (width/height ratio) for landscape cross-sections and tune by visual verification.
- **Animation rendering timeout.** 900 frames at 15fps with matplotlib backend takes ~5 minutes wall time. 1800 frames takes 10+ minutes and may hit the 600s foreground timeout. Cap at 900-1050 frames; if you need longer content, loop the shorter base animation rather than extending frame count.
- **Dynamic element cleanup.** Maintain global lists for EVERY patch/text created inside `animate()`. At the top of `animate()`, clear them all (`for p in patches: p.remove()`) before drawing the current frame — otherwise old frames leak into new ones and the figure fills up.

### ffmpeg
- **SearXNG blocks web_extract but works for firecrawl.** When researching events to narrate (`web_search`), if the result is a Malaysian news site (Kosmo, Harian Metro, Berita Harian), use `mcp__firecrawl__firecrawl_scrape` directly with `maxAge` parameter — `web_extract` returns "SearXNG is a search-only backend" error for those domains.
- **`-shortest` is mandatory when combining video + voice of different lengths.** Without it, the output extends to the longer stream (whichever is looped via `-stream_loop`), and you get either silent trailing video or cut-off narration.
- **Loop visibility.** When narration > animation duration and you loop, viewers see Phase 1 → 2 → 3 → 4 → 5 → 1 → 2 → 3... The second-loop start of Phase 1 is jarring. Mitigation: end the animation with a stable "OUTRO" hold frame (no further phase changes) for the last 10-15 seconds, so the loop seam falls inside the outro hold rather than mid-action.

### Delivery
- **Telegram voice bubble vs file attachment.** The voice note must be `.ogg` for Telegram voice bubble, `.mp3`/`.wav` for regular attachment. The `text_to_speech` tool returns `.ogg` by default — good.
- **Telegram video size cap.** Videos delivered as documents have a 50MB cap. Keep combined outputs under 25MB to leave headroom for caption text. 60s × 15fps × 100dpi typically lands 2–4MB.

## Voice Script Template (BM, makcik-friendly)

```
Hari ni makcik aku nak cerita satu [event] yang berlaku kat [place], [date].
Bayangkan macam ni — [analogy from familiar world].
[What happened, step by step, plain language]
[Why it happened, root cause]
[Consequence — casualties/damage, plain numbers]
Jadi kat sini ada pengajaran penting. [Take-away]
Apa yang [audience] boleh buat — [concrete advice].
```

## Visual Theme Defaults (matches Mode B dossier)

Same dark background as Mode B for visual consistency across the federation's explainer content:

```python
SKY_TOP = '#1e3a5f'
SKY_BOT = '#4a6b8a'
BG = '#0a1929'
TEXT = '#ecf0f1'
GOLD = '#f1c40f'
RED = '#e74c3c'
ORANGE = '#d68910'
BLUE = '#2874a6'
GREEN = '#2ecc71'
```

Phase color coding:
- Phase 1 (initiator event) → RED
- Phase 2 (build-up) → ORANGE/GOLD
- Phase 3 (critical breach) → RED + warning emoji
- Phase 4 (cascade) → RED + skull (use plain text — see pitfall above)
- Phase 5 (aftermath) → GREY/dim

## Verification (visual QA — same pattern as Mode B figures)

After generation:
1. `ffmpeg -i final.mp4 -vf "select=eq(n\,N)" -frames:v 1 -update 1 frame_N.png` — extract 4-5 representative frames (one per phase).
2. `vision_analyze(image_url=frame_N.png, question="Honest assessment: is this clear and readable for a non-expert? Any visual errors?")`.
3. Verify the audio is intelligible by checking the duration matches expected narration length and the AAC bitrate is reasonable (≥96kbps for speech).
4. Verify the combined MP4 plays in a standard player (QuickTime, VLC) by checking `-pix_fmt yuv420p` is set.

Cost: ~4 vision calls + 1 ffmpeg probe + 1 final MP4 render. ~7-10 minutes total wall time for a 60-second explainer.

## Proven Templates

- `templates/animation_geological_event.py` — Bhote Koshi GLOF cross-section animation (5 phases, ~60s) — see this session's `/tmp/nepal_animation.py` as reference.
- `templates/animation_financial_concept.py` — to be added when second financial explainer is built.
