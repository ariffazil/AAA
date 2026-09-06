#!/usr/bin/env python3
"""VISION CANARY v3 — fixes two probe bugs from v2:
  BUG 1: max_tokens=20 starves reasoning models; deepseek emitted reasoning_content
         ("read the word in the image") but empty content. Give it room + read both.
  BUG 2: qwen-vl-max / qwen3-vl-plus are DASHSCOPE models, not token-plan models.
         v2 sent them to the token-plan endpoint -> 404 model_not_found. Wrong endpoint
         is a probe defect, not a model defect. Test them on dashscope-payg.
Also distinguishes QUOTA-EXHAUSTED (429) from NO-VISION (404/empty) — qwen3.8-max
hit 429 on token-plan, meaning the route is LIVE but the budget is spent.
"""
import os, json, base64, time, subprocess, urllib.request, urllib.error

G = os.environ.get
FR = "/tmp/canary_frames"
for word in ["ZIRCON", "BASALT"]:
    out = f"{FR}/{word}.jpg"
    if not os.path.exists(out):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                        "-i", "color=c=black:s=640x360:d=1",
                        "-vf", (f"drawtext=text='{word}':fontcolor=white:fontsize=84:"
                                f"x=(w-text_w)/2:y=(h-text_h)/2"),
                        "-frames:v", "1", out], check=True)
B64 = {w: base64.b64encode(open(f"{FR}/{w}.jpg", "rb").read()).decode()
       for w in ["ZIRCON", "BASALT"]}
Q = ('This image contains exactly one word rendered in large capital letters. Read it. '
     'Reply with ONLY that word in uppercase, nothing else. If you cannot see any text '
     'reply exactly: NO_TEXT_VISIBLE')

def post(url, body, headers, timeout=120):
    t0 = time.time()
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.getcode(), r.read().decode(), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(), time.time() - t0
    except Exception as e:
        return None, type(e).__name__ + ": " + str(e)[:120], time.time() - t0

DASH_PAYG = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

TARGETS = [
    # FIX 1: deepseek with generous max_tokens + reasoning_content capture
    ("deepseek-v4-flash-vision-exp", "https://api.deepseek.com/v1",
     "DEEPSEEK_API_KEY", "deepseek-v4-flash-vision-exp", 600),
    # FIX 2: the vl models on their REAL provider (dashscope payg)
    ("qwen-vl-max @dashscope-payg", DASH_PAYG, "DASHSCOPE_PAYG_API_KEY", "qwen-vl-max", 60),
    ("qwen3-vl-plus @dashscope-payg", DASH_PAYG, "DASHSCOPE_PAYG_API_KEY", "qwen3-vl-plus", 60),
    ("qwen3-vl-flash @dashscope-payg", DASH_PAYG, "DASHSCOPE_PAYG_API_KEY", "qwen3-vl-flash", 60),
    ("qwen3.8-max @dashscope-payg", DASH_PAYG, "DASHSCOPE_PAYG_API_KEY", "qwen3.8-max", 60),
    ("qwen-vl-max @dashscope-free", DASH_PAYG, "DASHSCOPE_API_KEY", "qwen-vl-max", 60),
]

print("=" * 86)
print("VISION CANARY v3 — deepseek reasoning budget fixed + vl models on correct endpoint")
print("=" * 86)
rows = []
for label, base, keyenv, mid, maxtok in TARGETS:
    key = G(keyenv)
    if not key:
        print("\n[SKIP] %-36s %s UNSET" % (label, keyenv)); rows.append((label, "SKIP", 0)); continue
    url = base.rstrip("/") + "/chat/completions"
    ok = 0; detail = []; lat = 0.0
    for word in ["ZIRCON", "BASALT"]:
        body = {"model": mid, "max_tokens": maxtok, "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + B64[word]}},
            {"type": "text", "text": Q}]}]}
        code, raw, dt = post(url, body, {"content-type": "application/json",
                                         "authorization": "Bearer " + key})
        lat += dt
        if code == 429:
            detail.append("HTTP429 QUOTA: " + raw[:120].replace("\n", " ")); break
        if code != 200:
            detail.append("HTTP%s: %s" % (code, raw[:120].replace("\n", " "))); break
        try:
            msg = json.loads(raw)["choices"][0]["message"]
            txt = (msg.get("content") or "").strip().upper()
            rc = (msg.get("reasoning_content") or "").strip()
        except Exception:
            detail.append("parse fail %s" % raw[:120]); break
        if not txt and rc:
            # reasoning model: the answer may be inside reasoning_content
            detail.append("content EMPTY but reasoning sees image: %s" % rc[:130].replace("\n"," "))
            ok += 1 if word in rc.upper() else 0
            continue
        if not txt:
            detail.append("EMPTY content, no reasoning"); break
        ok += 1 if word in txt else 0
        detail.append("%s->'%s'" % (word, txt[:28]))
    if any("QUOTA" in x for x in detail):
        verdict = "QUOTA-EXHAUSTED"
    elif any(x.startswith("HTTP404") or x.startswith("HTTP403") or x.startswith("HTTP4") for x in detail):
        verdict = "ROUTE-REJECTED"
    elif ok == 2:
        verdict = "VISION-VERIFIED"
    elif ok == 1:
        verdict = "PARTIAL 1/2"
    else:
        verdict = "NO-VISION"
    print("\n[%-17s] %-36s %.1fs" % (verdict, label, lat))
    for dd in detail: print("        %s" % dd)
    rows.append((label, verdict, lat))

print("\n" + "=" * 86)
print("SUMMARY")
print("=" * 86)
for r in rows:
    print("  %-18s %-36s %.1fs" % (r[1], r[0], r[2]))
