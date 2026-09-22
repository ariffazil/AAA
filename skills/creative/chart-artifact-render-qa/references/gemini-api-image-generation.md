# Gemini API Image Generation

Google Gemini models can generate images directly via API. Use this for logos, visual artifacts, and creative images when matplotlib/reportlab output is insufficient.

## Endpoint

```
https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}
```

## Payload Structure

```python
{
    "contents": [{"parts": [{"text": "YOUR DETAILED PROMPT"}]}],
    "generationConfig": {
        "temperature": 0.9,
        "topP": 0.95,
        "topK": 50,
        "maxOutputTokens": 8192,
        "responseModalities": ["IMAGE", "TEXT"]  # CRITICAL: must include IMAGE
    }
}
```

## Response Parsing

Image data arrives as base64 in `response.candidates[0].content.parts[N].inlineData.data`.
Save with `base64.b64decode(part['inlineData']['data'])`.

## Available Image Models (Sept 2026)

- `gemini-2.5-flash-image` — fast, good quality (recommended)
- `gemini-3-pro-image` — higher quality, slower
- `gemini-3.1-flash-image` — latest flash
- `gemini-3.1-flash-image-preview` — preview access

## Prompt Best Practices

- Be specific about dimensions, colors, style, and composition
- State "1024x1024" or "circular crop" for profile pictures
- Reference visual styles: "dark fantasy", "vector-style", "clean illustration"
- For logos: state what NOT to include ("no photographic elements")
- For circular logos: emphasize centering and warn about edge cropping

## Pitfalls

- `gemini-2.5-flash` (text model) returns SVG code, not images. Use `gemini-2.5-flash-image` for actual image output.
- If `responseModalities` omits `IMAGE`, you get text-only response even with image model.
- API key must have generativelanguage.googleapis.com access (not just AI Studio).
- Image output is always 1024x1024 regardless of prompt dimensions.
