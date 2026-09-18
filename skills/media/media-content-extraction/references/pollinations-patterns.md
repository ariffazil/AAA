# Pollinations API — Working Patterns

## Endpoint
```
https://image.pollinations.ai/prompt/{encoded_prompt}?width=W&height=H&model=flux&nologo=true
```

## Parameters
- `width` / `height`: Output resolution (1920x1080 for posters, 1024x1024 for square)
- `model`: `flux` (default, best quality)
- `nologo`: `true` to remove watermark
- `seed`: Fixed seed for reproducibility (optional)

## Response handling
- Status 200 = image bytes in body (JPEG)
- Status 500 = transient error, retry once after 5s delay
- Content-type: image/jpeg

## Output verification
ALWAYS verify with vision_analyze before sending to user. Common issues:
- Garbled text in image (AI often misspells)
- NSFW content generated from ambiguous prompts
- Duplicate subjects in image

## Post-processing text overlay
Use PIL/Pillow to add text after Pollinations generation:
```python
from PIL import Image, ImageDraw, ImageFont
# Load generated image, add text overlay, save as final
```

## Known limitations
- Text in generated images is often garbled/gibberish
- Cannot generate specific real people
- No guarantee of output quality consistency
- Rate limits exist but rarely hit (free tier)