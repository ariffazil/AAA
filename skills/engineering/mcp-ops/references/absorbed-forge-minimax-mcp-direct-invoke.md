---
name: forge-minimax-mcp-direct-invoke
description: "Use when invoking minimax-media MCP via Python client directly, bypassing any wrapper. Invoke MCP minimax-media via Python client."
---

# forge-minimax-mcp-direct-invoke

## When to use

Current session's MCP palette doesn't expose `mcp__minimax_media__*` tools even though:
- `mcp.json` has the `minimax-media` entry
- `systemctl is-active minimax-media-mcp.service` returns `active`
- Port 18100 listening on `127.0.0.1`

Hermes session palette only refreshes at gateway start, not mid-session.

## The workaround: Python streamable HTTP client

Write a script (file-based, not `-c` arg — image payloads blow argv):

```python
import asyncio, sys
sys.path.insert(0, '/usr/local/lib/hermes-agent/venv/lib/python3.12/site-packages')
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    async with streamablehttp_client("http://127.0.0.1:18100/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # tools: text_to_image, generate_video, text_to_audio, voice_design,
            #        voice_clone, list_voices, query_video_generation,
            #        music_generation, play_audio
            result = await session.call_tool("text_to_audio", {...})
            for content in result.content:
                if hasattr(content, "text"):
                    print(content.text)

asyncio.run(main())
```

## Pitfalls learned

1. **Image/file payloads cannot be inlined** — base64 in f-string blows OS argv (`OSError: Argument list too long`). Save to `/tmp/script.py` and run via `python3 /tmp/script.py`.
2. **first_frame_image accepts file path, NOT base64** — server reads the path. Just pass `/root/.hermes/cache/images/foo.jpeg`.
3. **Signed URLs have ~5-30s TTL** — download immediately within the same script call, not a follow-up shell call.
4. **Regex for URLs must capture query params** — pattern `https?://[^\s,'\"]*?\.jpe?g(?:\?[^\s,'\"]*)?` (lazy + optional query).
5. **Video quota is separate from image/audio quota** — token plan exhausted for video doesn't block text_to_audio (RPM-bucketed). Test both before declaring dead.

## MiniMax model identifiers (only these work)

| Tool | Valid models |
|---|---|
| `text_to_image` | `image-01` only (others → 2013 unsupported) |
| `generate_video` | `MiniMax-Hailuo-2.3` only |
| `text_to_audio` | `speech-2.6-hd`, `speech-2.6-turbo` |

## Quota error codes

- `2013` = unsupported model
- `2056` = Token Plan usage limit reached (hard, wait for reset)
- `1002` = RPM rate limit (transient, retry in seconds)

## Reference

- Wire receipt: `/root/forge_work/_quarantine/2026-08-18-mcp-wire-minimax/`
- Backup: `mcp.json.bak`
- systemd unit: `minimax-media-mcp.service` port 18100
