---
name: youtube-eureka
description: "Extract high-density Eureka Insights, chronological breakdowns, and structured intelligence from any YouTube video. Uses multi-strategy transcript waterfall."
version: 1.0.0
tags: [youtube, extraction, insight, transcript, research]
---

# youtube-eureka — Autonomous YouTube Eureka Insight Extractor

> Multi-strategy transcript ingestion → ΔS < 0 signal isolation → 11-part Eureka output.
> Compatible with Hermes Agent, OpenAI-compatible runtimes, or any shell-based agent.

---

## When to use

- User shares a YouTube URL and asks to extract, summarize, or analyze the video
- User asks "what did that video say?" or requests eureka insights from a video
- Any request to digest YouTube content into structured intelligence

## Strategy waterfall (auto-tries until one works)

> **SCAR-HERMES-VIDEO-001 (2026-09-15):** NEVER give up after 1 attempt. Try ALL methods.

| # | Method | How | Speed | Coverage |
|---|--------|-----|-------|----------|
| **S1** | `youtube-transcript-api` v1.2.4 | `YouTubeTranscriptApi().fetch(video_id)` | ~3s | Popular + short videos; blocked on cloud IPs |
| **S2** | `yt-dlp --write-auto-sub` | Parses TTML/json3 subtitle files | ~8s | Works when S1 blocked; same bot-check risk |
| **S3** | `yt-dlp` audio download + `whisper tiny` | Downloads .m4a + transcribes locally | 10–60s+ | **works on any video** (slow but reliable) |
| **S4** | cookies at `/root/.secrets/yt-cookies.txt` | Auto-injected into S1/S2/S3; no separate step | varies | Last resort; uses user's browser session cookies |
| **S5** | Firecrawl MCP (`firecrawl_scrape`) | Proxy network, bypasses IP block | ~10s | Full transcript + metadata + chapters |
| **S6** | Exa MCP semantic search | Finds content ABOUT the video | ~5s | Related content, not exact transcript |
| **S7** | ZAI Web Search | Broad search for video content | ~5s | Related content |
| **S8** | Gemini AI (`forge_gemini`) | AI describes from URL | ~10s | May not have real-time access |

**Automated fallback script:** `python3 /root/.hermes/profiles/aaa-hermes/skills/media/youtube-content/scripts/youtube_ingest.py "URL"`

**Key reality from this VPS:** S1 and S2 are blocked for most videos (YouTube bot-check on cloud IPs). S3 works but is slow. S5 (Firecrawl) is the fastest reliable path when S1/S2 fail — but Firecrawl must be running.

**FAILURE PROTOCOL:** If ALL S1-S8 fail, you MUST:
1. Tell user: "YouTube blocked server-side extraction."
2. Label output: `[INFERRED — not observed from video]`
3. NEVER present manual knowledge as video content.

### Cookies (one-time setup, NOT recommended long-term)

If you want S1/S2 to work for ALL videos:
```bash
# From laptop: export using browser extension "Get cookies.txt LOCALLY"
# Upload to VPS:
scp cookies.txt root@VPS:/root/.secrets/yt-cookies.txt && chmod 600 /root/.secrets/yt-cookies.txt
```
**WARNING:** YouTube may permanently ban the account whose cookies you export. Use a throwaway Google account.

---

## Setup

Already installed on this system:
- `yt-dlp` (global) — subtitle download + audio download
- `youtube-transcript-api` v1.2.4 — Python transcript fetch
- `whisper` (local) — audio transcription fallback

```bash
# If whisper is missing (numpy version conflict):
pip install numpy==2.4 && pip install openai-whisper
```

## Usage

### 1. Fetch transcript (JSON output — feeds into EUREKA analysis)

```bash
# Automatic multi-strategy fallback
uv run python3 SKILL_DIR/scripts/eureka.py "https://youtube.com/watch?v=VIDEO_ID"

# Try only transcript API (fastest, skip audio fallback)
uv run python3 SKILL_DIR/scripts/eureka.py "URL" --strategies S1,S2

# Force audio + whisper (always works, slow)
uv run python3 SKILL_DIR/scripts/eureka.py "URL" --strategies S3

# Read from manually pasted transcript
uv run python3 SKILL_DIR/scripts/eureka.py "VIDEO_ID" --paste-path /path/to/transcript.txt
```

### 2. EUREKA analysis (agent executes this)

After fetching the transcript JSON, apply the 11-part output contract below.

---

## Output Contract — 11-Part Eureka Structure

Every analysis MUST follow this exact structure. No filler. No preamble. Lead with the answer.

### 1. Executive Summary
- **Title & Source:** Video title (URL)
- **Core Thesis:** 1–2 sentence summary of the speaker's main thesis.
- **Signal Density Score:** [High / Medium / Low]

### 2. Timeline Breakdown
Chronological map anchored to timestamps:
- `[HH:MM:SS]` Topic / Section Name
- `[HH:MM:SS]` Topic / Section Name

### 3. Key Eureka Insights (3–5 Non-Obvious Takeaways)

For each insight:

**💡 Insight Title**
- **Baseline Assumption:** What is the standard or naive view?
- **The Shift / Eureka:** What novel perspective is introduced?
- **Timestamped Evidence:** `[HH:MM:SS]` "> Verbatim quote from transcript."
- **Strategic Application:** How can this be practically applied?

### 4. Strategic Usefulness Matrix (WSU)

| Takeaway | Actionability (0–1) | Impact (0–1) | Novelty (0–1) | WSU Score |
|----------|---------------------|--------------|---------------|-----------|
| Insight 1 | 0.8 | 0.9 | 0.7 | 0.80 |

### 5. Truth & Verification Audit
- **Source Authority:** Speaker + domain grounding.
- **Domain Type:** [Structured (Math/Physics/Code) / Chaotic (Markets/Opinion)]
- **Causality vs. Correlation:** Empirically supported or correlational?

### 6. Operational Blueprint
- **Human Decision (Taste):** High-level judgments or qualitative choices.
- **AI Task (Solver):** Specific calculations, automation steps, or data pipelines that can be delegated.

### 7. Verbatim Supporting Quotes (Max 3)
- `[HH:MM:SS]` "> Quote 1"
- `[HH:MM:SS]` "> Quote 2"
- `[HH:MM:SS]` "> Quote 3"

### 8. Resources & References Mentioned
Books, papers, software, repositories, external experts referenced in the video.

### 9. Speaker & Persona Map
Identify speakers, roles, perspective/tone.

### 10. Objective Notes & Caveats
Potential biases, logical fallacies, sponsor conflicts, or missing data.

### 11. Strategic Classification Mapping
Map core concepts to domain axes (Mind/Technology, Body/Health, Soul/Ethics/Economics, Money/Capital).

---

## Execution Rules (Non-Nominalism)

- **Nominalism Rule:** Never invent product names, well names, or technical terms not in the transcript.
- **Timestamp Accuracy:** Every quote/insight citation MUST have a real `[HH:MM:SS]` from a segment in the transcript.
- **Zero Filler:** Output structured intelligence only. No conversational fluff.

## Transcript format

The eureka.py script returns JSON with:
```
{
  "video_id": "...",
  "url": "...",
  "title": "...",
  "channel": "...",
  "duration": 123,
  "language": "en",
  "method": "S1|S2|S3|S4|S5",
  "segments": [{"start": 0.5, "duration": 2.0, "text": "..."}],
  "warnings": ["..."]
}
```

The agent reads `segments` and applies the 11-part contract above to produce the final analysis.
The `method` field tells you which strategy worked — document it in the analysis for reproducibility.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| S1: `IPBlocked` / `RequestBlocked` | YouTube cloud IP ban | Switch to `--strategies S2,S3` |
| S2: "Sign in to confirm you're not a bot" | Same IP ban, different error | `--strategies S3` |
| S3: whisper `ImportError` | numpy version mismatch | `pip install numpy==2.4 && pip install openai-whisper` |
| S3: "timeout" on long videos | Video >30min, whisper tiny is slow | Acceptable; re-run with `--model small` for accuracy |
| Empty segments `[]` | Video has no captions/subs available | Only S3 can help; if audio unavailable, user must paste |
