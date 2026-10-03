---
name: paste-router
description: "Use when Arif pastes URL, file, or media. Route via media-intake."
version: 1.1.0
tags: [paste, intake, router, arif-attention]
---

# Paste Router — thin adapter only (no implementation)

## Status (2026-10-03)

This skill used to contain routing logic and tool fallbacks. Per arifOS spec
(Qwen cross-audit 2026-10-03), `paste-router` is now a **thin adapter** only.

All routing logic, classification, and tool resolution lives in:
  `/root/AAA/src/mission_router/media_intake.py`

The canonical procedure for media ingestion lives in:
  `/root/AAA/skills/media-ingest-lane/SKILL.md`

**Routing principle (replaces old "Max 1 question"):**

ZERO questions for machine-resolvable uncertainty.

Human escalation permitted ONLY for:
  1. HUMAN_AUTHORITY_REQUIRED
  2. IRREVERSIBLE_DECISION_REQUIRED
  3. INTENT_AMBIGUITY that changes consequential outcome
  4. REQUIRED_INFORMATION exists only in human head
  5. ALL bounded machine paths genuinely exhausted

## When this skill fires

Auto-loaded when incoming message contains:
- URL (http/https)
- File path starting with /root or /tmp
- Media attachment
- Code block

## Action

1. Hand off to `mission_router.media_intake.route(artifact)` for classification
   + tool selection. It returns a `RoutingDecision` with `input_class`,
   `selected_tool`, `avoidable_handoff`, and `truth_state`.

2. Execute the selected tool. On failure, follow
   `arifOS::TOOL_FAILURE ≠ TASK_FAILURE ≠ HUMAN_HANDOFF` doctrine:
   classify failure → discover alternative → rank → attempt bounded fallback → verify.

3. Emit telemetry: `input_class`, `capability_selected`, `fallback_depth`,
   `avoidable_handoff`, `truth_state`, `resolution_status`.

4. Truth-state semantics (per media-ingest-lane, never collapse):
   - METADATA_OBSERVED ≠ TRANSCRIPT_OBSERVED ≠ VISUAL_OBSERVED
   - ≠ MEDIA_OBSERVED ≠ CONTENT_UNDERSTOOD
   - oEmbed success is METADATA, not proof of video content.

5. If `avoidable_handoff == true` AND `truth_state == BLOCKED`, you have a defect
   in `media_intake.py` — fix the resolver, not the human.

## Do not add here

- Implementation of tool selection (lives in media_intake.py)
- Tool-specific fallbacks (lives in media-intest-lane)
- New artifact classes (extend ArtifactClass enum in media_intake.py)

This file is the **routing principle** + handoff contract, not the implementation.

## Provenance

2026-10-03: arifOS spec via Qwen cross-audit. Item 4: "paste-router must NOT
become another parallel SOT. Thin adapter only, no implementation logic,
eventually retire if redundant."

Original v1.0 (Hermes 14:55) contained routing tables and tool fallbacks.
v1.1 (Hermes 15:30) stripped implementation, kept only principle + handoff.
Implementation moved to `mission_router/media_intake.py`.

## Operating principle

**Max 1 question. NEVER menu. NEVER "pilih (a)(b)(c)(d)".**

If paste type is unambiguous, proceed. If ambiguous, one short question. If still unclear, best inference + proceed.

## Paste type detection

| Pattern | Type | Default tool |
|---|---|---|
| `https://youtu.be/...` or `youtube.com/watch` | YouTube URL | oEmbed → yt-dlp → web_extract |
| `https://*.com/...` (article/blog/docs) | Web URL | web_extract with char_limit |
| `https://twitter.com/...` or `x.com/...` | X/Twitter | xurl CLI → web_extract fallback |
| `https://*.pdf` or path `.pdf` | PDF | web_extract or read_file |
| `https://*.jpg/.png/.gif` or image path | Image | vision_analyze |
| `https://*.mp3/.ogg/.wav` or audio path | Audio | yt-dlp/curl → transcribe |
| `/root/.hermes/...` or `/tmp/...` | Local file | read_file or media_ingest |
| Bare URL | Web URL (assume) | web_extract |
| 1-3 sentence text in BM/EN | Question/note | answer from text |
| Code block ```...``` | Code | patch / analyze / search |
| 3+ paragraph text | Document | summarize (asi-summarize) |

## Tool priority (fail-soft)

### YouTube URL (proven 2026-10-03)

```bash
# Tier 1: oEmbed (no auth, no JS, ~200ms) — CANONICAL
curl -s "https://www.youtube.com/oembed?url=$URL&format=json"
# Returns: title, author_name, thumbnail_url, html iframe

# Tier 2: yt-dlp (may need cookies for some videos)
yt-dlp --skip-download --print "%(title)s | %(uploader)s | %(duration)ss" "$URL"

# Tier 3: web_extract (returns JS shell only for YouTube, not useful)
```

Tier 1 is canonical. Tiers 2-3 are defense-in-depth.

### Web URL

```bash
web_extract(urls=[URL], char_limit=5000)
# Returns: title, content (markdown, head+tail truncated)
```

### PDF / Document

```bash
# Tier 1: web_extract (PDF native support)
web_extract(urls=[URL.pdf])
# Tier 2: local file
read_file(path=URL)
```

### Image

```bash
vision_analyze(image_url=URL, question="describe + key info")
```

### Audio

```bash
# Download: yt-dlp (YouTube) or curl (direct)
# Transcribe: MMS-1b CTC (F5 private) or Whisper
```

### Code paste

```bash
read_file(path=path)  # or extract from inline paste
patch / analyze / search
```

## When to ask the 1 question

ONLY when ALL true:
1. Paste cannot be classified
2. Default routing produces zero value
3. 1 question can be answered in <10 words

Examples where 1 question IS needed:
- Single-word paste with no context ("ok", "huh")
- Ambiguous media path with no extension
- Reference to unidentified thing

Examples where 1 question is NOT needed (proceed with best inference):
- YouTube URL → oEmbed → title → describe
- Article URL → web_extract → summarize
- Image URL → vision_analyze
- Code block → analyze

## Anti-patterns (NEVER)

- ❌ "Hang boleh share tajuk dia?" (URL IS the context)
- ❌ "Boleh bagi konteks?" (paste IS the context)
- ❌ "Pilih (a) summarize, (b) translate, (c) extract" (menu banned)
- ❌ "Aku boleh buat X, Y, atau Z. Hang nak mana satu?" (menu banned)
- ❌ Stop after first tool fail without trying next tier
- ❌ Echo paste back ("Hang bagi YouTube link. OK.") — waste of breath

## Receipt format

After processing paste, deliver:
1. **What the paste is** (title / author / type) — 1-2 lines
2. **Highest-value action taken** — analysis / summary / extraction
3. **Why this matters for Arif** — connection to his world
4. **(Only if needed)** 1 short follow-up question

## Load rule

Auto-loaded when incoming message contains:
- URL (http/https)
- File path starting with /root or /tmp
- Media attachment
- Code block

Otherwise: do not load.

## Provenance

Origin: 2026-10-03, Arif YouTube paste failure. Hermes replied "chromium tak install" + asked context. Arif: "Malas aku nak cakap ulang2 cara nak tgk YouTube."

Lives in skill (procedure), not SOUL.md (identity) — per upstream progressive disclosure.

Related SOUL.md rule: §8 GERAK DULU. This skill is the operationalization that was missing.
