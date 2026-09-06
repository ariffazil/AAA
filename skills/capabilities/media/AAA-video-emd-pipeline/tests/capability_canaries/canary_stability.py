#!/usr/bin/env python3
"""STABILITY TRIAL — 2/2 on one pass can still be luck.
Re-run the three AUDIO-VERIFIED models 3x per fixture (9 calls each model pair)
and report per-fixture accuracy. Only a model that is consistently right on BOTH
fixtures enters default routing. Also re-test the two BIASED ones to confirm bias.
"""
import os, json, base64, time, urllib.request, urllib.error, urllib.parse
from collections import Counter

G = os.environ.get
gk = G("GEMINI_API_KEY")
GB = "https://generativelanguage.googleapis.com/v1beta"

FIX = [("A_asc", "/tmp/canary_A_asc.mp4", "ascending"),
       ("B_desc", "/tmp/canary_B_desc.mp4", "descending")]
B64 = {n: base64.b64encode(open(p, "rb").read()).decode() for n, p, _ in FIX}

Q = ('3-second clip. VISUAL is one unchanging grey frame carrying NO information. '
     'AUDIO has three consecutive 1-second tones of different pitch. Determine pitch '
     'order from AUDIO ONLY. Reply ONLY compact JSON: '
     '{"distinct_tones":<int>,"pitch_order":"ascending|descending|same|cannot_determine",'
     '"heard_audio":true|false}. If you cannot perceive audio, say heard_audio:false and '
     'pitch_order:"cannot_determine". Guessing is worse than abstaining.')

MODELS = ["gemini-3.8-flash", "gemini-3.1-pro-preview", "gemini-3.6-flash",
          "gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-2.5-flash"]
TRIALS = 3

def call(mid, b64):
    url = GB + "/models/" + mid + ":generateContent?" + urllib.parse.urlencode({"key": gk})
    body = {"contents": [{"parts": [
        {"inline_data": {"mime_type": "video/mp4", "data": b64}}, {"text": Q}]}]}
    t0 = time.time()
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"content-type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read().decode()
    except urllib.error.HTTPError as e:
        return "HTTP%d" % e.code, time.time() - t0
    except Exception as e:
        return "ERR:" + type(e).__name__, time.time() - t0
    d = json.loads(raw)
    txt = "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])
    flat = txt.replace(" ", "").lower()
    got = ("ascending" if "ascending" in flat else
           "descending" if "descending" in flat else
           "same" if '"pitch_order":"same"' in flat else
           "cannot_determine" if "cannot_determine" in flat else "?")
    return got, time.time() - t0

print("=" * 84)
print("STABILITY TRIAL — %d trials per fixture, model must be right on BOTH" % TRIALS)
print("=" * 84)

summary = []
for mid in MODELS:
    per = {}
    lats = []
    for name, _, truth in FIX:
        answers = []
        for _ in range(TRIALS):
            got, dt = call(mid, B64[name])
            answers.append(got); lats.append(dt)
        per[name] = (Counter(answers), truth, answers.count(truth))
    a_hits = per["A_asc"][2]; b_hits = per["B_desc"][2]
    total = a_hits + b_hits; maxtotal = 2 * TRIALS
    stable = (a_hits == TRIALS and b_hits == TRIALS)
    biased = (per["A_asc"][0] == per["B_desc"][0])
    label = ("AUDIO-VERIFIED-STABLE" if stable else
             "BIASED-NOT-LISTENING" if biased else
             "UNSTABLE")
    print("\n%-26s %-24s %d/%d  median_latency=%.1fs"
          % (mid, label, total, maxtotal, sorted(lats)[len(lats)//2]))
    for name, _, truth in FIX:
        c, t, hits = per[name]
        print("    %-8s truth=%-11s hits=%d/%d  answers=%s" % (name, t, hits, TRIALS, dict(c)))
    summary.append((mid, label, total, maxtotal))

print("\n" + "=" * 84)
print("FINAL ROUTING TABLE")
print("=" * 84)
for mid, label, total, mx in summary:
    mark = "ENTER DEFAULT ROUTING" if label == "AUDIO-VERIFIED-STABLE" else "EXCLUDE"
    print("  %-26s %-24s %d/%d  -> %s" % (mid, label, total, mx, mark))
