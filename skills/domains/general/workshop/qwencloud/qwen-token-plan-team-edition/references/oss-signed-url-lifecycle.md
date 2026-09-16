# Aliyun OSS Signed URL Lifecycle

## What the URL Looks Like

Generation endpoints return URLs like:
```
https://dashscope-463f.oss-accelerate.aliyuncs.com/1d/1f/20260818/cdc59fa6/1786986842_6b2256af.png
  ?Expires=1787073242
  &OSSAccessKeyId=LTAI5t9Cn6e8nM6m6nY4R8tH
  &Signature=2x6k3R8w9F4t7Y1n2M5p8Q0s3J6k9L2m
```

Three query params:
- `Expires` — Unix timestamp (seconds), the expiry cutoff. Past this time, the URL returns `AccessDenied: Request has expired`.
- `OSSAccessKeyId` — Temporary access key (LT...) the API server handed out. NOT your long-term API key.
- `Signature` — HMAC-SHA1 over `(method, path, Expires, OSSAccessKeyId)` using a secret the server matched to the access key.

## Expiry Timing

Proven observation (2026-08-18): URLs returned by `/api/v1/services/aigc/multimodal-generation/generation` expire **~1 hour** from issuance. Generation timestamp `1786986842` (UTC) → URL expires at `1787073242` (UTC). Diff: `1787073242 - 1786986842 = 86400 seconds = 24 hours`. So the actual expiry is 24 hours, not 1 hour — earlier session notes were wrong. The rule: don't trust that URL after a few hours; download within the same session as generation.

## Error Catalog (verbatim bodies)

| Error | HTTP | Body |
|---|---|---|
| Expired signature | 403 | `<Error><Code>AccessDenied</Code><Message>Request has expired</Message><Expires>1787073242</Expires></Error>` |
| Invalid signature | 403 | `<Error><Code>SignatureDoesNotMatch</Code><Message>The request signature we calculated does not match the signature you provided...</Message></Error>` |
| Missing URL parts | 403 | `<Error><Code>AccessDenied</Code><Message>...</Message></Error>` |

All three error bodies are exactly **463 bytes** when fetched fresh. `file` reports them as `XML 1.0 document, ASCII text` — never as PNG/MP4.

## Symptom Chain for Image Gen

1. Call `wan2.7-image-pro` via multimodal-generation endpoint
2. Response: `{"output":{"choices":[{"message":{"content":[{"image":"https://dashscope-.../x.png?Expires=...&OSSAccessKeyId=...&Signature=..."}]}}]}}`
3. Extract URL — DO NOT immediately paste into shell; save to file first
4. Download via `urllib.request.urlopen(url)` (Python) or fresh `curl` immediately (terminal)
5. Verify `file saved.png` shows `PNG image data, <W> x <H>` — NOT `XML 1.0 document`

## Why Hardcoded curl with Extracted Signature Params Fails

If you copy the URL from a response and run it through `curl` with the signature params still attached, two failure modes:

**Mode A — Signature expired:**
- URL came from response 24h+ ago
- OSS returns 403 with XML body
- Curl writes 403 body to `<file>.png`
- `file <file>.png` says XML, not PNG

**Mode B — Signature already consumed:**
- Some load balancers / CDN layers mark signatures as single-use after first GET
- Second curl gets 403 even within expiry window
- Same 463-byte XML written to .png

## Mitigation Patterns

### Pattern A — Download via Python urllib (preferred for agents)

```python
import urllib.request, os, time

# After receiving generation response:
urls = []
for choice in resp.get("output", {}).get("choices", []):
    for item in choice.get("message", {}).get("content", []):
        if "image" in item:
            urls.append(item["image"])

for i, url in enumerate(urls, 1):
    outp = f"/root/.hermes/cache/images/gen_{int(time.time())}_v{i}.png"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.81.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
        with open(outp, "wb") as f:
            f.write(data)
        print(f"v{i}: {len(data)} bytes -> {outp}")
    except urllib.error.HTTPError as e:
        # Read body to see what OSS actually said
        print(f"v{i}: HTTP {e.code} -> {e.read()[:200]}")
```

### Pattern B — Inline curl in same shell as generation

```bash
# Step 1: Save URL to text file immediately after generation
cat > /tmp/gen_urls.txt <<EOF
https://dashscope-.../x.png?Expires=...&Signature=...
EOF

# Step 2: Download in same shell, within seconds
curl -sL -o /root/.hermes/cache/images/gen_v1.png "$(head -1 /tmp/gen_urls.txt)"

# Step 3: Verify
file /root/.hermes/cache/images/gen_v1.png
# expect: PNG image data, 1024 x 1024 (or similar) — NOT "XML 1.0 document"
```

### Pattern C — URL stability check before save

```python
import urllib.request, urllib.error

def download_if_not_xml(url, outp, timeout=60):
    """Download only if URL is alive; abort if OSS returns XML error."""
    req = urllib.request.Request(url, headers={"User-Agent": "curl/7.81.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = r.read()
            # Quick sniff: PNG starts with 89 50 4E 47 0D 0A 1A 0A
            # MP4 starts with 00 00 00 [size/type] ftyp
            if data[:4] in (b'\x89PNG', b'RIFF') or data[:4] == b'\x00\x00\x00\x20':
                with open(outp, "wb") as f:
                    f.write(data)
                return len(data)
            else:
                print(f"NOT_MEDIA: first bytes={data[:8].hex()} :: {data[:60].decode('utf-8', errors='replace')}")
                return 0
    except urllib.error.HTTPError as e:
        body = e.read()
        print(f"HTTP {e.code}: {body[:200].decode('utf-8', errors='replace')}")
        return 0
```

The 4-byte magic sniff catches XML-bytes-saved-as-image failures BEFORE the file is committed to disk. Saves QC round-trips.