# Image Analysis Pattern — Local File → Hermes Vision

## Problem

Hermes cannot directly analyze local image files via `browser_vision` when the image path is passed as a `file://` URL. The browser tool only navigates HTTP/HTTPS URLs — it does not serve local filesystem resources.

Symptom: `browser_navigate(url="file:///root/.hermes/image_cache/img_xxx.jpg")` returns "(empty page)" with element_count=0. `browser_vision` then reports "I don't see an image attached."

## Working Pattern

```python
# Step 1: Copy to webroot
cp /root/.hermes/image_cache/img_xxx.jpg /var/www/html/arif/temp_img.jpg

# Step 2: Navigate via public URL
browser_navigate(url="https://arif-fazil.com/temp_img.jpg")

# Step 3: Now analyze
browser_vision(question="Describe this image in full detail.")
```

Alternatively, send directly via Telegram to Arif (file delivery works for images):

```python
send_message(
    action='send',
    message='MEDIA:/root/.hermes/image_cache/img_xxx.jpg',
    target='telegram:Arif'
)
```

Or mirror to AAA group:
```python
send_message(
    action='send', 
    message='MEDIA:/root/.hermes/image_cache/img_xxx.jpg',
    target='telegram:-1003753855708'
)
```

## Why This Works

- `/var/www/html/arif/` is Caddy's webroot for `arif-fazil.com`
- Browser tool can reach it via HTTPS
- `browser_vision` reads the browser's current page — so navigate first, then analyze

## When to Use This

- User sends screenshot/photo and asks Hermes to describe it
- User says "see this image" without attaching a file (Telegram compression may prevent direct attachment)
- Image is in Hermes cache (`/root/.hermes/image_cache/`) but not reachable via browser

## Verification

```bash
# Confirm image is accessible via web
curl -s -I "https://arif-fazil.com/temp_img.jpg" | head -3
# Expect: HTTP/2 200, Content-Type: image/jpeg
```

## Note on Telegram Image Limits

Telegram may compress images before delivery to Hermes. Large screenshots may arrive as smaller JPEGs. If Hermes reports "no image attached" even after sending, the image may have been dropped in transit — try sending direct to Arif via DM as fallback.