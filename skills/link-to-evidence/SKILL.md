---
name: link-to-evidence
description: "Use when a shared link must be read as evidence."
metadata:
  hermes:
    tags: [fetch, evidence, media, probe]
---

# Link to Evidence

When to use: a person shares a URL, reel, post or attachment and wants it analyzed, summarized or reacted to. Also whenever you are about to say you cannot read something.

## First rule

**Probe the route before declaring the content unreadable.** "I cannot read this" is a claim about your own capability; it is falsifiable and will be checked. Test at least one local path before saying it. A block on one route — an in-app reader, a web extractor — does not mean the content is unavailable.

Only after probing: say plainly what failed and ask for a caption, a screenshot, or a downloaded file. Never invent content to fill the gap.

## Procedure

1. **Identify the class of link**: video/audio post, article, document, paywalled page, or attachment already delivered locally (a file path needs no fetching).
2. **Video/audio → local fetch.**

   ```bash
   yt-dlp -o "/tmp/clip.%(ext)s" "<url>"
   yt-dlp --skip-download --print "%(uploader)s|%(title)s|%(description)s|%(duration)s|%(like_count)s" "<url>"
   ```

   Public Instagram reels, YouTube, TikTok and X resolve without cookies. Add `--cookies-from-browser chrome` only when a public fetch returns a login wall.

3. **Sample media rather than consuming it whole.**

   ```bash
   ffmpeg -v quiet -i clip.mp4 -vf "fps=1" frames/f_%03d.jpg -y   # ~1/s for short clips; fps=1/3 for long
   yt-dlp -x --audio-format mp3 "<url>"                            # when the meaning is spoken
   ```

   Read a **spread** of frames, not just the first — overlay text changes mid-clip and the closing frame often carries the punchline.

4. **Article/document → `web_extract`**, then page the full text from the saved file if the body was truncated.
5. **Local attachment → read the path directly.** Do not ask the person to describe a file you already hold.
6. **Report observation before interpretation.** Who, what, verbatim text, setting — then the reading, labelled as a reading.

## Pitfalls

- Claiming a platform is unreadable without probing. The local CLI path frequently succeeds where an in-app reader will not.
- Inferring content from the title. Titles are marketing; a fetch settles it in seconds.
- Reading only the thumbnail or first frame, then interpreting confidently.
- Confusing the person inside a post with the person who shared it. "This is me" usually means the message, not the face.
- Asking the human to paste or describe something you can fetch yourself. Human attention is the scarcest resource in the loop.
- Treating an edited self-presentation as evidence about a real person's character. Say what the clip asserts; do not launder it into a verdict.

## Troubleshooting

- Blocked fetch: retry with `--cookies-from-browser <browser>`. If it still fails, report it and request the caption or file.
- FFmpeg refuses to write a single image from a filtered stream: add `-update 1`.
- `yt-dlp --print` returns `NA` for a field — the field is genuinely absent, not an error.

## Related

Deeper video-specific handling lives in the `social-video-intelligence` skill (user-owned).
