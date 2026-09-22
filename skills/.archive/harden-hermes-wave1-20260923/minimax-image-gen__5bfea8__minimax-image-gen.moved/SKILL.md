---
id: minimax-image-gen
name: MiniMax Image Generation
version: 1.0.0-2026.08.04
description: Generate images, videos, TTS, voice clone, and music via MiniMax MCP server. Use when user asks to "draw", "generate image", "create picture", "make a photo", "text to image", "image generation".
owner: 333-AGI
risk_tier: T1
floor_scope: F2, F4, F7
autonomy_tier: T1
---

# MiniMax Image Generation

Generate images using MiniMax `image-01` model via MCP server.

## When to Use

- User asks to generate, create, or draw an image
- User asks for text-to-image, image generation, picture creation
- User asks for TTS, voice clone, music, or video generation

## How to Call

### Image Generation

```
Tool: minimax-mcp → text_to_image
Parameters:
  - prompt (required): Description of the image to generate
  - model (optional): "image-01" (default)
  - aspect_ratio (optional): "1:1" (default), "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"
  - n (optional): 1-9 images (default: 1)
  - prompt_optimizer (optional): true/false (default: true)
  - output_directory (optional): where to save the file
```

### Video Generation

```
Tool: minimax-mcp → generate_video
Parameters:
  - prompt (required): Description of the video scene
  - model (optional): "MiniMax-Hailuo-02" (latest), "T2V-01", "T2V-01-Director", "I2V-01"
  - duration (optional): 6 or 10 seconds (Hailuo-02 only)
  - resolution (optional): "768P" or "1080P" (Hailuo-02 only)
  - async_mode (optional): true for background generation
```

### Text-to-Speech

```
Tool: minimax-mcp → text_to_audio
Parameters:
  - text (required): Text to convert to speech
  - voice_id (optional): e.g. "male-qn-qingse", "female-shaonv"
  - model (optional): "speech-2.6-hd" (default)
  - speed (optional): 0.5-2.0 (default: 1.0)
  - emotion (optional): "happy", "sad", "angry", etc.
```

### Music Generation

```
Tool: minimax-mcp → music_generation
Parameters:
  - prompt (required): Style/mood description (10-300 chars)
  - lyrics (required): Song lyrics (10-600 chars)
  - format (optional): "mp3" (default), "wav", "pcm"
```

## Cost Warning

All MiniMax tools make API calls that incur costs. Use when explicitly requested by user.

## Transport

stdio via `uvx minimax-mcp -y`. Requires `MINIMAX_API_KEY` + `MINIMAX_API_HOST=https://api.minimax.io`.

## Key Facts

- `image-01` model is MCP-server-only (not in REST API model list)
- MCP server name in config: `minimax-mcp`
- Backup: `minimax-coding-plan-mcp` (web search only, no image gen)
- Both can coexist as separate MCP servers

## Workflow

1. Verify MiniMax MCP is available: check `minimax-mcp` in MCP server list
2. Call `text_to_image` with prompt
3. Download image from returned URL
4. Save to workspace or send to user
5. Report: model, aspect ratio, file path

## Example

```
User: "Generate an image of a sunset over mountains"
→ Call minimax-mcp text_to_image with prompt="A beautiful sunset over mountain peaks, golden hour lighting, photorealistic"
→ Download URL from response
→ Save to /root/forge_work/sunset_$(date +%Y%m%d_%H%M%S).jpg
→ Report: "Generated sunset image via MiniMax image-01. Saved to /root/forge_work/sunset_20260804.jpg"
```
