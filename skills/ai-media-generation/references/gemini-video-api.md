# Gemini Video Generation — Quick Reference

## Routes

### 1. Omni Flash (fast, recommended)
```bash
python3 /root/HERMES/scripts/gemini-video.py "prompt" --output /tmp/video.mp4 --aspect 9:16
```
- Model: `gemini-omni-flash-preview`
- Endpoint: `/v1beta/interactions` (synchronous)
- Output: 720p, ~10s, ~2.5MB, H264 + AAC audio
- Prompt limit: **<100 words** (longer prompts → 400 error)

### 2. Veo 3.1 (higher quality, async)
```python
import requests, json, os, time, base64
API_KEY = os.environ['GEMINI_API_KEY']
BASE = "https://generativelanguage.googleapis.com/v1beta"

# Start generation
resp = requests.post(f"{BASE}/models/veo-3.1-generate-preview:predictLongRunning?key={API_KEY}",
    json={"instances": [{"prompt": "Short prompt here"}],
          "parameters": {"sampleCount": 1, "aspectRatio": "9:16", "durationSeconds": 5}})
op_name = resp.json()["name"]

# Poll until done
while True:
    status = requests.get(f"{BASE}/{op_name}?key={API_KEY}").json()
    if status.get("done"): break
    time.sleep(10)

# Download
uri = status["response"]["generateVideoResponse"]["generatedSamples"][0]["video"]["uri"]
video = requests.get(f"{uri}&key={API_KEY}").content
with open("output.mp4", "wb") as f: f.write(video)
```
- Model: `veo-3.1-generate-preview`
- Endpoint: `predictLongRunning` (async poll)
- Output: 720p/1080p/4K, 5-8s, native audio
- `durationSeconds` must be 4-8 (inclusive)

## PITFALL: Long prompts cause 400 on Omni Flash
Keep prompts under 100 words. Strip em dashes, complex punctuation. The interactions API is stricter than the image gen API.

## PITFALL: Shared credit pool
ALL Gemini generation (image + Omni Flash + Veo) shares one prepayment credit pool. One heavy session can exhaust all routes.

## Aspect Ratios
- `16:9` — landscape (default)
- `9:16` — portrait (TikTok/Reels style)

## vs MiniMax
| | Gemini Omni Flash | Gemini Veo 3.1 | MiniMax Hailuo-02 |
|---|---|---|---|
| Setup | Just API key | Just API key | MCP server on :18100 |
| Stability | Always available | Always available | Crashes, needs relaunch |
| Camera control | ❌ | ❌ | ✅ Director models |
| Resolution | 720p | 720p-4K | 768p/1080p |
| Duration | ~10s | 5-8s | 6-10s |
| Audio | AAC included | Native audio | Separate |
| Cost | Billable | Billable | ~$0.30/clip |
