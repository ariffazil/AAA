#!/usr/bin/env python3
"""Restyle an existing photo via DashScope qwen-image-edit (image-to-image).

Usage:
    python3 photo_style_transfer.py SRC OUT [PROMPT_FILE] [--model qwen-image-edit]

Reads the source, base64-encodes it into a data URI, POSTs to the multimodal-generation
endpoint, downloads the returned artwork URL. Exits non-zero with the provider message on
failure so the caller can relay the real reason instead of guessing.

Needs DASHSCOPE_API_KEY in the environment.
"""

import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.request

ENDPOINT = (
    "https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/"
    "multimodal-generation/generation"
)

DEFAULT_PROMPT = (
    "Restyle this photograph into an illustration. "
    "Keep the same person, pose, clothing and composition, but redraw everything: "
    "clean line work, hand-painted background with visible brush texture, "
    "softer palette, gentle diffused lighting. Remove photorealism entirely."
)


def main() -> int:
    argv = sys.argv[1:]
    positional = [a for a in argv if not a.startswith("--")]
    model = "qwen-image-edit"
    if "--model" in argv:
        idx = argv.index("--model")
        if idx + 1 < len(argv):
            positional = [a for a in positional if a != argv[idx + 1]]
            model = argv[idx + 1]

    if len(positional) < 2:
        sys.stderr.write(__doc__ + "\n")
        return 2

    src, out = positional[0], positional[1]
    prompt = open(positional[2]).read().strip() if len(positional) > 2 else DEFAULT_PROMPT

    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        sys.stderr.write("DASHSCOPE_API_KEY not set\n")
        return 1

    mime = mimetypes.guess_type(src)[0] or "image/jpeg"
    with open(src, "rb") as fh:
        data_uri = "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode())

    payload = {
        "model": model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"image": data_uri},
                        {"text": prompt},
                    ],
                }
            ]
        },
        "parameters": {"watermark": False},
    }

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": "Bearer %s" % key,
            "Content-Type": "application/json",
        },
    )

    try:
        resp = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as exc:
        sys.stderr.write(
            "HTTP %s: %s\n" % (exc.code, exc.read()[:600].decode("utf-8", "replace"))
        )
        return 1
    except Exception as exc:  # surface anything, never guess
        sys.stderr.write("REQUEST FAILED: %r\n" % (exc,))
        return 1

    image_url = None
    for choice in resp.get("output", {}).get("choices", []):
        for item in choice.get("message", {}).get("content", []):
            if item.get("image"):
                image_url = item["image"]
                break
        if image_url:
            break

    if not image_url:
        sys.stderr.write("NO_IMAGE in response: " + json.dumps(resp)[:900] + "\n")
        return 1

    with urllib.request.urlopen(image_url, timeout=180) as remote:
        blob = remote.read()
    with open(out, "wb") as fh:
        fh.write(blob)

    print("WROTE %s (%d bytes)" % (out, len(blob)))
    print("Next: convert to JPG for chat, then read it back with vision before reporting success.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
