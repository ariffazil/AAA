#!/usr/bin/env python3
"""ANTI-BIAS AUDIO CANARY — the real test.
A model that always answers "descending" passes a single descending fixture by bias.
So: build TWO fixtures with IDENTICAL constant-grey visuals and OPPOSITE pitch orders.
A model only earns "audio-verified" if it FLIPS its answer to match each fixture.

  fixture A: tones ASCENDING  440 -> 880 -> 1320   (truth = ascending)
  fixture B: tones DESCENDING 1320 -> 880 -> 440   (truth = descending)

Visual channel carries zero information in both. Any correct discrimination
must come from the audio track. This is falsification, not a capability claim.
"""
import os, json, base64, time, subprocess, urllib.request, urllib.error, urllib.parse

G = os.environ.get
gk = G("GEMINI_API_KEY")
GB = "https://generativelanguage.googleapis.com/v1beta"

def build(path, freqs):
    graph = ("color=c=gray:s=320x240:d=3:r=10[v];"
             "sine=frequency=%d:duration=1[a0];"
             "sine=frequency=%d:duration=1[a1];"
             "sine=frequency=%d:duration=1[a2];"
             "[a0][a1][a2]concat=n=3:v=0:a=1[aout]" % tuple(freqs))
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-filter_complex", graph,
                        "-map", "[v]", "-map", "[aout]",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", path],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:200]

FIX = {
    "A_ascending":  ("/tmp/canary_A_asc.mp4",  [440, 880, 1320], "ascending"),
    "B_descending": ("/tmp/canary_B_desc.mp4", [1320, 880, 440], "descending"),
}
for name, (path, freqs, truth) in FIX.items():
    if not os.path.exists(path):
        build(path, freqs)
    streams = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                              "stream=codec_type,sample_rate", "-of", "csv", path],
                             capture_output=True, text=True).stdout.replace("\n", " ")
    print("%-14s %-30s %6d bytes  truth=%-10s streams=%s"
          % (name, path, os.path.getsize(path), truth, streams.strip()))

Q = ('This is a 3-second clip. The VISUAL is one unchanging grey frame for the entire '
     'duration and carries NO information whatsoever. The AUDIO contains three '
     'consecutive 1-second tones of different pitch. Determine the pitch order from the '
     'AUDIO ONLY. Reply with ONLY compact JSON: '
     '{"distinct_tones":<int>,"pitch_order":"ascending|descending|same|cannot_determine",'
     '"heard_audio":true|false}. '
     'If you cannot actually perceive the audio, reply heard_audio:false and '
     'pitch_order:"cannot_determine". Guessing is worse than abstaining.')

def post(url, body, timeout=120):
    t0 = time.time()
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                     headers={"content-type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.getcode(), r.read().decode(), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(), time.time() - t0
    except Exception as e:
        return None, type(e).__name__ + ": " + str(e)[:120], time.time() - t0

MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-3.1-pro-preview",
          "gemini-3.1-flash-lite", "gemini-3.6-flash", "gemini-2.5-flash"]

print("\n" + "=" * 80)
print("ANTI-BIAS AUDIO CANARY — model must FLIP its answer to match each fixture")
print("=" * 80)

table = {}
for mid in MODELS:
    table[mid] = {}
    for name, (path, freqs, truth) in FIX.items():
        b64 = base64.b64encode(open(path, "rb").read()).decode()
        url = GB + "/models/" + mid + ":generateContent?" + urllib.parse.urlencode({"key": gk})
        body = {"contents": [{"parts": [
            {"inline_data": {"mime_type": "video/mp4", "data": b64}}, {"text": Q}]}]}
        code, raw, dt = post(url, body)
        if code != 200:
            table[mid][name] = ("FAIL", str(code), dt)
            continue
        d = json.loads(raw)
        txt = "".join(p.get("text", "") for p in d["candidates"][0]["content"]["parts"])
        flat = txt.replace(" ", "").lower()
        got = ("ascending" if "ascending" in flat else
               "descending" if "descending" in flat else
               "same" if '"pitch_order":"same"' in flat else
               "cannot_determine" if "cannot_determine" in flat else "?")
        heard = '"heard_audio":true' in flat
        table[mid][name] = (got, truth, heard, round(dt, 1), txt.replace("\n", " ")[:90])

print()
for mid in MODELS:
    a = table[mid].get("A_ascending"); b = table[mid].get("B_descending")
    if not a or not b or a[0] == "FAIL" or b[0] == "FAIL":
        print("%-26s FAIL/ERROR  %s %s" % (mid, a, b)); continue
    a_ok = (a[0] == "ascending"); b_ok = (b[0] == "descending")
    if a_ok and b_ok:
        verdict = "AUDIO-VERIFIED (flipped correctly both ways)"
    elif a[2] and b[2] and not (a_ok or b_ok):
        verdict = "FABRICATES (claims heard_audio, wrong both ways)"
    elif a[0] == "cannot_determine" and b[0] == "cannot_determine":
        verdict = "HONEST ABSTENTION (no audio perception, admits it)"
    elif a[0] == b[0]:
        verdict = "BIASED (same answer both fixtures = not listening)"
    else:
        verdict = "PARTIAL (1 of 2 correct = coin flip)"
    print("%-26s %s" % (mid, verdict))
    print("    A(asc): got=%-17s heard=%-5s %4.1fs" % (a[0], a[2], a[3]))
    print("    B(desc):got=%-17s heard=%-5s %4.1fs" % (b[0], b[2], b[3]))
    print()

print("=" * 80)
print("ROUTING-GRADE VERDICT")
print("=" * 80)
for mid in MODELS:
    a = table[mid].get("A_ascending"); b = table[mid].get("B_descending")
    if a[0] == "FAIL" or b[0] == "FAIL":
        print("  %-26s ERROR" % mid); continue
    score = (1 if a[0] == "ascending" else 0) + (1 if b[0] == "descending" else 0)
    claims_heard = a[2] or b[2]
    label = {2: "AUDIO-VERIFIED", 1: "PARTIAL/COINFLIP", 0: "NO-AUDIO-PERCEPTION"}[score]
    flag = " <-- FABRICATES (claims heard but scores 0)" if (score == 0 and claims_heard) else ""
    print("  %-26s %d/2  %-20s heard_claim=%s%s" % (mid, score, label, claims_heard, flag))
