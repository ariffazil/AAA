#!/usr/bin/env python3
import os, sys, json, base64, argparse, requests, pathlib

def main():
    p = argparse.ArgumentParser(description="Gemini image gen (REST Interactions)")
    p.add_argument("prompt", help="Text prompt")
    p.add_argument("--model", default="gemini-3.1-flash-image-preview")
    p.add_argument("--aspect", default="3:4", help="1:1,3:4,4:3,16:9,9:16")
    p.add_argument("--size", default="1K", help="512,1K,2K,4K (model-dependent)")
    p.add_argument("--out", default="out.jpg", help="Output image path")
    args = p.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: Set GEMINI_API_KEY or GOOGLE_API_KEY in environment.", file=sys.stderr)
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{args.model}:generateContent"
    body = {
        "contents": [{"parts": [{"text": args.prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": args.aspect, "imageSize": args.size}
        }
    }
    headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=body, timeout=180)
    if r.status_code != 200:
        print("HTTP", r.status_code, r.text[:1000], file=sys.stderr)
        sys.exit(2)
    try:
        parts = r.json()["candidates"][0]["content"]["parts"]
        img_b64 = next(p["inlineData"]["data"] for p in parts if "inlineData" in p)
    except Exception as e:
        print("Parse error:", e, file=sys.stderr)
        print(json.dumps(r.json())[:1000], file=sys.stderr)
        sys.exit(3)

    pathlib.Path(os.path.dirname(args.out) or ".").mkdir(parents=True, exist_ok=True)
    with open(args.out, "wb") as f:
        f.write(base64.b64decode(img_b64))
    print(args.out)

if __name__ == "__main__":
    main()
