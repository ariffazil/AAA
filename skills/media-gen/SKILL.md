---
name: media-gen
description: Media generation including images, video, audio, and text-to-speech. Use when: (1) Generating images via OpenAI/DALL-E, (2) Creating video content or extracting frames, (3) Text-to-speech conversion, (4) Audio transcription, (5) Batch media processing.
---

# Media Generation Skill

Generate and process images, video, audio, and speech.

## Quick Start

### Image Generation (OpenAI)

```json
{
  "tool": "exec",
  "command": "openai-image-gen --prompt \"description\" --count 4 --size 1024x1024"
}
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `prompt` | Image description | required |
| `count` | Images to generate | 1 |
| `size` | 1024x1024, 1792x1024, 1024x1792 | 1024x1024 |
| `quality` | standard or hd | standard |
| `style` | vivid or natural | vivid |

### Text-to-Speech

```json
{
  "tool": "tts",
  "text": "Text to convert to speech"
}
```

Optional parameters:
- `voice`: alloy, echo, fable, onyx, nova, shimmer
- `speed`: 0.25 to 4.0

### Video Frame Extraction

```bash
# Extract frames at interval
video-frames extract --input video.mp4 --interval 5s --output frames/

# Extract specific time range
video-frames extract --input video.mp4 --start 00:01:00 --end 00:02:00

# Create contact sheet
video-frames sheet --input video.mp4 --rows 5 --cols 5
```

### Audio Transcription (Whisper)

```bash
# Transcribe audio file
whisper-api transcribe --file audio.mp3 --language ms

# Translate to English
whisper-api translate --file audio.mp3
```

## Batch Processing

### Image Gallery Generation

```bash
# Generate multiple images and create gallery
openai-image-gen --prompts prompts.txt --count 20 --gallery
```

Creates `index.html` with lightbox gallery.

### Video Clip Extraction

```bash
# Extract short clips from video
video-frames clip --input video.mp4 --timestamps "00:01:00,00:02:30,00:05:00" --duration 10s
```

## Media Formats

### Supported Input

| Type | Formats |
|------|---------|
| Image | JPG, PNG, GIF, WebP |
| Video | MP4, MOV, AVI, MKV |
| Audio | MP3, WAV, M4A, OGG |

### Supported Output

| Type | Formats |
|------|---------|
| Image | PNG, JPG |
| Video | MP4 |
| Audio | MP3, WAV |

## F1 (Reversibility) Notes

- Media generation consumes API credits — irreversible spend
- 888_HOLD for bulk generation >100 images
- Store prompts for reproducibility
