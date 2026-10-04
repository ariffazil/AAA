# MiniMax Media MCP — API Reference (verified 2026-08-07)

## Streamable-HTTP client pattern

```python
import requests, json, time, socket, os, base64

MCP = "http://127.0.0.1:18100/mcp"
OUT_DIR = "/tmp/minimax-media-output"
os.makedirs(OUT_DIR, exist_ok=True)

def mcp_init():
    r = requests.post(MCP,
        headers={"Content-Type": "application/json",
                 "Accept": "application/json, text/event-stream"},
        json={"jsonrpc":"2.0","method":"initialize",
              "params":{"protocolVersion":"2025-11-25","capabilities":{},
                        "clientInfo":{"name":"hermes","version":"1"}},
              "id":1})
    sid = r.headers["mcp-session-id"].strip()
    requests.post(MCP,
        headers={"Content-Type":"application/json",
                 "Accept":"application/json, text/event-stream",
                 "mcp-session-id": sid},
        json={"jsonrpc":"2.0","method":"notifications/initialized"})
    return sid

def mcp_call(sid, tool_name, arguments):
    t0 = time.time()
    r = requests.post(MCP,
        headers={"Content-Type":"application/json",
                 "Accept":"application/json, text/event-stream",
                 "mcp-session-id": sid},
        json={"jsonrpc":"2.0","method":"tools/call",
              "params":{"name":tool_name,"arguments":arguments},
              "id":int(time.time())})
    elapsed = time.time() - t0
    for line in r.text.splitlines():
        if line.startswith("data: "):
            d = json.loads(line[6:])
            text = d["result"]["content"][0].get("text","")
            return text, elapsed
    raise RuntimeError(f"No SSE data: {r.text[:300]}")
```

## generate_video call (T2V — no first frame)

```python
sid = mcp_init()
text, elapsed = mcp_call(sid, "generate_video", {
    "model": "MiniMax-Hailuo-02",    # best quality, supports 1080P
    "prompt": "Cinematic ...",
    "duration": 6,                    # 6 or 10 seconds (Hailuo only)
    "resolution": "768P",            # "768P" or "1080P" (Hailuo only)
    "output_directory": OUT_DIR,
    "async_mode": False,              # False = poll until done (~107s avg)
})
# text = "Success. Video URL: https://..."
url = text.split("Video URL:")[-1].strip()
# Must download yourself (RESOURCE_MODE=url):
video = requests.get(url).content
open(os.path.join(OUT_DIR, "output.mp4"), "wb").write(video)
```

## generate_video call (I2V — with first frame image)

```python
text, elapsed = mcp_call(sid, "generate_video", {
    "model": "I2V-01-Director",
    "prompt": "[Push in] Cinematic slow-motion ...",
    "first_frame_image": "/root/forge_work/abang_sado_minimax.jpg",
    "output_directory": OUT_DIR,
    "async_mode": False,
})
```

First frame is auto-detected: if local path, base64-encoded as `data:image/jpeg;base64,...`.

## async_mode=True pattern

```python
# Submit (returns immediately):
text, _ = mcp_call(sid, "generate_video", { ..., "async_mode": True })
# text = "Success. Video generation task submitted: Task ID: abc123..."

# Poll:
time.sleep(30)
text, _ = mcp_call(sid, "query_video_generation", {
    "task_id": "abc123",
    "output_directory": OUT_DIR,
})
# If still processing: "Video generation task is still processing: Task ID: abc123"
# If done: "Success. Video saved as: /path/video.mp4" or "Success. Video URL: ..."
```

## Verified facts (2026-08-07)

- **MCP port**: 18100 (not 18090)
- **Response format**: SSE with `event: message\r\ndata: {...}` lines
- **HTTP header requirement**: `Accept: application/json, text/event-stream` (both!)
  — sending only `text/event-stream` → `-32600 Not Acceptable`
- **Hailuo poll ceiling**: `max_retries=60`, interval=20s → max ~20 min wait
- **Minimax API host**: `https://api.minimax.io`
- **RESOURCE_MODE**: `url` → output is a CDN URL, not a saved file
- **CDN URL**: `https://video-product.cdn.minimax.io/...`
- **Typical latency**: 107s for I2V-01-Director; Hailuo likely longer
- **Output size**: ~765 KB for 5.64s 720×720

## Available models

| Model | Type | Notes |
|---|---|---|
| `MiniMax-Hailuo-02` | T2V (best) | 768P/1080P, 6s/10s |
| `I2V-01-Director` | I2V + camera | Supports camera instructions |
| `I2V-01-live` | I2V | Live-action style |
| `T2V-01-Director` | T2V + camera | Camera instructions in prompt |
| `T2V-01` | T2V | Base text-to-video |

## Available tools (all 9)

| Tool | Description |
|---|---|
| `generate_video` | Create video from prompt (T2V) or prompt+first_frame (I2V) |
| `query_video_generation` | Poll async task status |
| `text_to_image` | wan2.7-image/pro — text-to-image |
| `text_to_audio` | qwen-audio-3.0-tts-plus, 200+ voices |
| `list_voices` | Enumerate available voices |
| `voice_clone` | Clone voice from audio sample |
| `voice_design` | Generate voice from description |
| `play_audio` | Play WAV/MP3 |
| `music_generation` | Suno-style music from prompt+lyrics |
