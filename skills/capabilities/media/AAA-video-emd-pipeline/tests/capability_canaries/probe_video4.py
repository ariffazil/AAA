#!/usr/bin/env python3
"""Probe v4 — Gemini CORRECT model names + omni lanes. Evidence for the FED video capability."""
import os, json, base64, time, urllib.request, urllib.error, urllib.parse

G = os.environ.get
VID = "/tmp/fed_video_probe.mp4"
b64 = base64.b64encode(open(VID, "rb").read()).decode()
Q = ('3-second synthetic test video: three 1-second clips, each a solid colour with a '
     'distinct sine tone. Reply ONLY compact JSON '
     '{"c1":"","c2":"","c3":"","tone_hz_order":"ascending|descending|same","saw_video":true,'
     '"heard_audio":true}. If you cannot perceive video reply {"saw_video":false}; '
     'if you cannot hear the audio track reply {"heard_audio":false}.')

gk = G("GEMINI_API_KEY")
GB = "https://generativelanguage.googleapis.com/v1beta"

CANDIDATES = [
    # (label, model_id, kind)
    ("gemini-2.5-flash (baseline, already PASS)", "gemini-2.5-flash", "gemini"),
    ("gemini-3-flash-preview",                    "gemini-3-flash-preview", "gemini"),
    ("gemini-3.1-flash-lite",                     "gemini-3.1-flash-lite", "gemini"),
    ("gemini-3.5-flash",                          "gemini-3.5-flash", "gemini"),
    ("gemini-3.5-flash-lite",                     "gemini-3.5-flash-lite", "gemini"),
    ("gemini-3.6-flash",                          "gemini-3.6-flash", "gemini"),
    ("gemini-3.7-flash",                          "gemini-3.7-flash", "gemini"),
    ("gemini-3.8-flash",                          "gemini-3.8-flash", "gemini"),
    ("gemini-omni-flash-preview",                 "gemini-omni-flash-preview", "gemini"),
    ("gemini-omni-1.1-flash",                     "gemini-omni-1.1-flash", "gemini"),
    ("gemini-3.1-pro-preview",                    "gemini-3.1-pro-preview", "gemini"),
    ("gemini-3.5-transcribe (ASR lane)",          "gemini-3.5-transcribe", "gemini"),
]

def post(url, body, headers, timeout=150):
    t0 = time.time()
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.getcode(), r.read().decode(), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(), time.time() - t0
    except Exception as e:
        return None, type(e).__name__ + ": " + str(e)[:150], time.time() - t0

print("=" * 78)
print("GEMINI NATIVE VIDEO+AUDIO INGESTION PROBE — /tmp/fed_video_probe.mp4 (3s)")
print("ground truth: red(440Hz) -> blue(880Hz) -> green(1320Hz) = ASCENDING, 3 tones")
print("=" * 78)

verdicts = []
for label, mid, kind in CANDIDATES:
    url = GB + "/models/" + mid + ":generateContent" + "?" + urllib.parse.urlencode({"key": gk})
    body = {"contents": [{"parts": [
        {"inline_data": {"mime_type": "video/mp4", "data": b64}}, {"text": Q}]}]}
    code, raw, dt = post(url, body, {"content-type": "application/json"})
    if code != 200:
        msg = ""
        try:
            msg = json.loads(raw).get("error", {}).get("message", "")[:130]
        except Exception:
            msg = raw[:130]
        print("\n[FAIL %s] %-46s %.1fs\n          %s" % (code, mid, dt, msg))
        verdicts.append((mid, "FAIL", code, dt, msg.replace("\n", " ")))
        continue
    d = json.loads(raw)
    txt = ""
    try:
        txt = "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])
    except Exception:
        txt = raw[:200]
    um = d.get("usageMetadata", {})
    mods = {x["modality"]: x["tokenCount"] for x in um.get("promptTokensDetails", [])}
    correct = ('"red"' in txt.lower() and '"blue"' in txt.lower() and '"green"' in txt.lower())
    print("\n[%s] %-46s %.1fs  tokens=%s" % ("PASS" if correct else "WEAK", mid, dt, mods))
    print("          %s" % txt.replace("\n", " ")[:260])
    verdicts.append((mid, "PASS" if correct else "WEAK", code, dt, json.dumps(mods)))

print("\n" + "=" * 78)
print("SUMMARY")
print("=" * 78)
for v in verdicts:
    print("  %-6s %-44s http=%-4s %.1fs %s" % (v[1], v[0], v[2], v[3], v[4]))
