# Qwen Image Generation via Direct API — Bypass agy-image CLI Aspect Bug

When the `agy-image` CLI fails with `InvalidParameter` on aspect-ratio mapping,
or when you need an aspect ratio not in the CLI's hardcoded table, call the
Qwen PAYG multimodal-generation API directly. Verified 2026-09-25.

## The bug

`/usr/local/bin/agy-image` maps `--aspect 16:9` to internal size `1792*1024`,
which qwen-payg rejects:

```
ERROR: No image in response: {
  "request_id": "...",
  "code": "InvalidParameter",
  "message": "The size does not match the allowed size
              1664*928, 1472*1104, 1328*1328, 1104*1472, 928*1664."
}
```

The CLI's `ASPECT_TO_SIZE` table contains sizes (e.g. `1792*1024`, `1024*1792`,
`1440*1024`) that the qwen-payg endpoint no longer accepts. The CLI is stale.

## Fix A — patch the CLI

Edit `/usr/local/bin/agy-image`, change the `ASPECT_TO_SIZE` table to use
only qwen-allowed sizes:

```python
ASPECT_TO_SIZE = {
    "1:1": "1024*1024",
    "16:9": "1664*928",
    "9:16": "928*1664",
    "4:3": "1472*1104",
    "3:4": "1104*1472",
    "1:1_lg": "1328*1328",
    "3:2": "1536*1024",
    "2:3": "1024*1536",
    "21:9": "1664*928",
}
```

## Fix B — call the API directly (preferred for one-off)

Bypass the CLI entirely. Drop a Python script next to your generation code:

```python
import os, json, time, urllib.request

API_KEY = os.environ.get("QWEN_PAYG_API_KEY", "")
ENDPOINT = "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
SIZE = "1664*928"   # pick from qwen-allowed set above
MODEL = "qwen-image-plus"

def generate(prompt: str, out_path: str, size: str = SIZE, model: str = MODEL):
    body = json.dumps({
        "model": model,
        "input": {"prompt": prompt},
        "parameters": {"size": size, "n": 1, "prompt_extend": True}
    }).encode()
    req = urllib.request.Request(
        f"{ENDPOINT}?async=true",
        data=body,
        headers={"Authorization": f"Bearer {API_KEY}",
                 "Content-Type": "application/json",
                 "X-DashScope-Async": "enable"},
        method="POST")
    resp = json.loads(urllib.request.urlopen(req, timeout=60).read().decode())
    task_id = resp.get("output", {}).get("task_id")
    for _ in range(40):
        time.sleep(5)
        poll = urllib.request.urlopen(urllib.request.Request(
            f"https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"}), timeout=30).read().decode()
        p = json.loads(poll)
        st = p.get("output", {}).get("task_status")
        if st == "SUCCEEDED":
            url = p["output"]["results"][0]["url"]
            urllib.request.urlretrieve(url, out_path)
            return out_path
        elif st == "FAILED":
            raise RuntimeError(p.get("output", {}).get("message"))
    raise TimeoutError("qwen task polling exceeded 200s")
```

Qwen PAYG key loading order: env var → `/root/.secrets/qwen.env` `source`-ed
for `$QWEN_PAYG_API_KEY`.

## qwen-allowed sizes (verified 2026-09-25)

```
1664*928      16:9-ish landscape, 1792/1024 ≈ 1.79
1472*1104     4:3-ish landscape, 1.33
1328*1328     1:1 square
1104*1472     3:4-ish portrait
928*1664      9:16-ish portrait
```

Don't pass `1664x928` or any `x` separator — the API uses `*` as separator.

## When to bypass vs patch

| Scenario | Approach |
|---|---|
| One-off generation, want to move fast | Direct API (Fix B) |
| Multiple generations, want CLI convenience | Patch + use CLI (Fix A) |
| Need a size not in qwen-allowed set | Direct API with custom size in body (note: qwen rejects unknown sizes) |
| agy-image is producing anything successfully | Leave it, don't fix what's working |

## Pitfalls

- **`X-DashScope-Async: enable` header required** — without it, qwen treats the
  call as synchronous and times out at 60s for any non-trivial generation.
- **Poll every 5s, max ~200s** — long generations (large images, complex
  prompts) can take 60-120s. The 40-iteration cap = ~200s covers the
  practical maximum for qwen-image-plus at standard sizes.
- **`"prompt_extend": True` invokes qwen's prompt optimizer** — extends the
  prompt with style/detail expansion. Disable if you need exact prompt fidelity
  (`"prompt_extend": False`).
- **API key needs `Bearer` prefix** — `Authorization: Bearer <key>`, not just
  `<key>`.
- **Output URL is signed and time-limited** — download within ~30 minutes or
  the URL expires. The `urlretrieve` call usually completes in <10s.
