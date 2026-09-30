---
name: kvm8-artifact-render
description: "Use when rendering PDF or poster artifacts on KVM8."
version: 1.0.0
tags: [render, pdf, poster, chrome, weasyprint, kvm8]
---

# KVM8 Artifact Render — host-measured quirks

Companion to the external, read-only `forge-pdf-delivery` and `generated-media-delivery` skills (they own the pipeline doctrine; this file records what actually works on **this** host, because both external skills are read-only to autonomous patching).

## Measured 2026-09-29

1. **Headless Chrome as root requires `--no-sandbox`.** Without it the process exits with `Running as root without --no-sandbox is not supported` and writes **no file at all** — the shell returns quietly and the screenshot silently does not exist. Always `ls -l <out>.png` before claiming a render. Working call:

```bash
google-chrome --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1080,2160 \
  --screenshot=poster.png poster.html
```

2. **WeasyPrint CLI lives at `/usr/local/lib/hermes-agent/venv/bin/weasyprint`.** The system `python3` has neither `markdown` nor `weasyprint` (import fails). Working flow:

```bash
pandoc in.md -o out.html --standalone      # OMIT --metadata title or the title prints twice
/usr/local/lib/hermes-agent/venv/bin/weasyprint -s style.css out.html out.pdf
```

`pandoc` is installed and can only go md → html (never read a PDF). PIL exists only inside the hermes venv python.

3. **`write_file` refuses to overwrite a file created earlier in the same session** (written-only, never read back). Do not fight the guard — write the revision to a new name (`poster_v2.html`) and render from that.

4. **Text on posters is deterministic, always.** Generate or draw a text-free plate for mood (inline SVG emblems — bat/keris/crescent arcs — read cleanly at poster scale), then lay out **every word** in HTML/CSS→Chrome or with PIL. Never let the image model write the words.

5. **Verify then deliver:** read the finished artifact with `media_ingest media_vision_read` (or `pdftotext -f N -l N` for PDFs), copy to `/root/AAA/forge_work/<date>-<slug>/`, then send `MEDIA:/abs/path`.

## Layout defaults that survived review

- Portrait canvas 1080×1620 (A4-ish) or 1080×2160 (long jadual). Dark `#0a0a0e` page, gold `#d4af37` accents, deep red `#7a1f1f`, DejaVu Serif headline / DejaVu Sans body.
- One accent per meaning: gold = time/values, warm cream = meals, muted red = the row that must not move.
- Keep the row list ≤ 13 lines; more than that and a phone reader scrolls past it.
