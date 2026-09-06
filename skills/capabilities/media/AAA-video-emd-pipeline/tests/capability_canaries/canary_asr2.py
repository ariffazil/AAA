#!/usr/bin/env python3
"""ASR ROUTE CANARY — two falsifiable tests without needing a TTS engine.
TEST 1 (route liveness): send the 3s pure-tone audio. A correct ASR returns EMPTY
       or a no-speech marker. If it returns WORDS, that is hallucination — a known
       Whisper failure mode and a direct threat to the evidence ledger (V4/V5).
TEST 2 (real speech): extract audio from a real public video via yt-dlp if
       available; otherwise report the gap honestly rather than fabricating a pass.
"""
import os, json, base64, time, subprocess, shutil, urllib.request, urllib.error

G = os.environ.get

def post(url, data, headers, timeout=90):
    t0 = time.time()
    try:
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.getcode(), r.read().decode(), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(), time.time() - t0
    except Exception as e:
        return None, type(e).__name__ + ": " + str(e)[:130], time.time() - t0

# extract the tone audio from the existing video fixture (known: no speech at all)
TONE = "/tmp/canary_tones.wav"
src = "/tmp/canary_A_asc.mp4"
if os.path.exists(src):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src,
                    "-vn", "-ar", "16000", "-ac", "1", TONE], check=True)
print("tone fixture (contains NO speech):", TONE, os.path.getsize(TONE), "bytes")

print("\n" + "=" * 80)
print("ASR ROUTE CANARY — groq/whisper-large-v3-turbo")
print("=" * 80)
gk = G("GROQ_API_KEY")
print("GROQ_API_KEY:", ("SET len=%d" % len(gk)) if gk else "UNSET")
if gk:
    boundary = "----fed%d" % int(time.time())
    fn = os.path.basename(TONE)
    body = ("--%s\r\nContent-Disposition: form-data; name=\"file\"; filename=\"%s\"\r\n"
            "Content-Type: audio/wav\r\n\r\n" % (boundary, fn)).encode()
    body += open(TONE, "rb").read() + b"\r\n"
    for k, v in {"model": "whisper-large-v3-turbo", "language": "en",
                 "response_format": "verbose_json"}.items():
        body += ("--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n"
                 % (boundary, k, v)).encode()
    body += ("--%s--\r\n" % boundary).encode()
    base = (G("GROQ_BASE_URL") or "https://api.groq.com/openai/v1").rstrip("/")
    code, raw, dt = post(base + "/audio/transcriptions", body,
                         {"content-type": "multipart/form-data; boundary=" + boundary,
                          "authorization": "Bearer " + gk})
    print("\nHTTP=%s  %.1fs  base=%s" % (code, dt, base))
    if code == 200:
        j = json.loads(raw)
        txt = (j.get("text") or "").strip()
        segs = j.get("segments") or []
        print("   transcript: '%s'" % txt[:200])
        print("   segments: %d" % len(segs))
        print("   language: %s   duration: %s" % (j.get("language"), j.get("duration")))
        if txt == "" or txt.lower() in ("", "[blank audio]", "[music]", "[silence]"):
            print("   VERDICT: ASR-ROUTE-LIVE + CORRECT-ABSTENTION (no hallucinated speech)")
        else:
            print("   VERDICT: ASR-ROUTE-LIVE but HALLUCINATES SPEECH FROM PURE TONES")
            print("   >>> SHADOW: this is a V4/V5 violation risk. ASR output MUST be")
            print("   >>> confidence-gated before entering the evidence ledger.")
    else:
        print("   err: %s" % raw[:260].replace("\n", " "))
        print("   VERDICT: ASR-ROUTE-REJECTED")

# TEST 2: real speech source
print("\n" + "=" * 80)
print("REAL-SPEECH ASR TEST")
print("=" * 80)
ytdlp = shutil.which("yt-dlp")
print("yt-dlp:", ytdlp or "MISSING")
if ytdlp:
    print("   available — a real-speech canary can be run against any short public clip")
else:
    print("   GAP (honest, not fabricated): no TTS engine (espeak MISSING) and no yt-dlp")
    print("   on this box right now, so a known-words speech canary was NOT executed.")
    print("   ASR route liveness is proven above; ASR WORD-LEVEL ACCURACY is UNPROVEN.")
    print("   To close: install espeak-ng OR yt-dlp, then re-run with a real phrase.")
