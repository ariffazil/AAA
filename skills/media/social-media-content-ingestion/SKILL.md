---
name: social-media-content-ingestion
description: "Use when a shared social-media link must be watched."
version: 1.0.0
metadata:
  hermes:
    tags: [media, video, instagram, youtube, yt-dlp, vision]
capability_tier: fed-long-context
ecology_state: WARM
---

# Social Media Content Ingestion

## When to use

Someone shares an Instagram reel/post, TikTok, or YouTube link and expects you to
actually see it — "watch this", "analyze this", "what do you think of this video".
Also use it when a plain fetch of such a link returns a login wall, "Video
unavailable", "content isn't available", or a bot block.

## Core rule

**Never answer "I can't open that link" before running yt-dlp.** Extract the media
locally, then look at the pixels yourself. A page that looks dead to a fetcher is
routinely still downloadable — a dead-looking page is not evidence of inaccessibility.

## Procedure

1. **Download directly — no cookies needed for public posts:**
   ```bash
   yt-dlp --no-warnings -o "/tmp/<name>.%(ext)s" "<url>"
   ```
   Handles Instagram reels/posts, YouTube, TikTok, X/Twitter. Resolve short links
   as-is; yt-dlp follows them. Do not reach for browser automation first.

2. **Confirm what you got before analysing it:**
   ```bash
   ls -lh /tmp/<name>.mp4
   ffprobe -v quiet -show_entries format=duration -of csv=p=0 /tmp/<name>.mp4
   ```

3. **Extract frames** (1 fps is plenty for talking-head reels):
   ```bash
   mkdir -p /tmp/frames && ffmpeg -v quiet -i /tmp/<name>.mp4 \
     -vf "fps=1" -frames:v 8 /tmp/frames/f_%02d.jpg -y
   ```

4. **Read frames with vision — sample across the clip, not just frame 1.**
   Frame 1 is almost always the hook; the payoff line lands mid-clip. Open at
   least a start frame, a middle frame, and a late frame.

5. **Quote on-screen text verbatim when reporting.** Burned-in captions are the
   actual message. Report what the text says and what the speaker does — do not
   substitute your inference for the caption.

6. **State what the source is** (account/handle, who is on screen) before
   interpreting it, so the human can correct your attribution immediately.

## Pitfalls

- **Don't route through the YouTube transcript path when yt-dlp can fetch the
  media.** Transcript endpoints get refused from datacenter/cloud IPs, and the
  failure looks like "transcripts disabled" rather than a block. If yt-dlp
  succeeds, the transcript detour is wasted turns.
- **Instagram Reels and TikTok have no usable captions** — the message lives in
  burned-in text plus audio. Frames are the only reliable read; a thumbnail
  description is not the content.
- **A chat image that arrives as a refused/"high risk" stub is not content you
  saw.** Say plainly that the pixels never arrived and ask for the file or a
  re-send. Never describe or analyse an attachment you did not actually receive,
  and never claim you did.
- **If the primary vision lane is unavailable, delegate the frame analysis** to a
  subagent and let it find a working vision route, rather than declaring the
  frames unreadable. Hand it the frame paths and the specific observational
  questions.
- **Verify the download landed before trusting it** — check file size and
  duration. A 0-byte or few-hundred-byte "mp4" is an error page, and analysing it
  produces invented content.
- **Don't narrate a workaround you did not run.** If yt-dlp itself refuses, that
  is a real block: report it and stop, rather than presenting an untested
  sequence as the method.

## Reporting shape

Short. What the clip is, who is in it, what it says (verbatim caption), what it
shows visually — then the interpretation. If the human sent it as a statement
about themselves or someone they know, answer the statement, not the link.
