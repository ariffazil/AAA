#!/usr/bin/env python3
"""Duration guard — catches SILENT synthesis failures (truncation AND runaway).

Motivating incidents (2026-09-15, live):
  - MiniMax returned 0.216 s for an 88-char input with base_resp.status_code == 0.
    The near-empty artifact then transcribed as "Terima kasih kerana menonton!"
    (Whisper non-speech boilerplate) — a silent failure that nearly shipped.
  - emotion=happy/sad/angry on one voice returned 180/216/252 ms, status_code 0.
  - The SAME long text rendered 51.4 s and 169.0 s on two runs (3.3x swing).

Success code alone is not evidence of usable audio. This guard validates duration
against a BHBM pacing model before anything downstream (STT, delivery) sees it.

Exit codes:
  0  duration plausible
  6  duration below floor  (truncated)
  7  duration above ceiling (runaway)

Usage:  python3 audio_duration_guard.py <audio-file> <input-char-count>
"""
import json
import os
import subprocess
import sys

# Bahasa Malaysia pacing model, measured 2026-09-15 across MiniMax + MiMo lanes:
#   observed 3.7 - 14.5 chars/s; nominal 10 chars/s.
NOMINAL_CPS = 10.0
# floor: 0.4x nominal pacing -> catches the 0.216s and 180ms cases decisively
FLOOR_RATIO = 0.4
# absolute floor: any real utterance of >0 chars lasts at least this long
ABS_FLOOR_S = 1.0
# ceiling: 2.5x nominal -> catches the 625-char runaway (169s vs 156s ceiling)
CEIL_RATIO = 2.5


def probe_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", path], capture_output=True, text=True).stdout
    try:
        return float(json.loads(out)["format"]["duration"])
    except Exception:
        return None


def main(argv):
    if len(argv) < 3:
        sys.stderr.write("usage: audio_duration_guard.py <audio-file> <chars>\n")
        return 2
    path, chars = argv[1], int(argv[2])
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        sys.stderr.write(f"duration-guard: BLOCK — missing/empty artifact {path}\n")
        return 6
    dur = probe_duration(path)
    if dur is None:
        sys.stderr.write(f"duration-guard: BLOCK — cannot probe duration of {path}\n")
        return 6

    expected = max(chars, 1) / NOMINAL_CPS
    floor_s = max(ABS_FLOOR_S, FLOOR_RATIO * expected)
    ceil_s = CEIL_RATIO * expected

    verdict = {
        "file": path, "chars": chars, "dur_s": round(dur, 3),
        "expected_s": round(expected, 2), "floor_s": round(floor_s, 2),
        "ceil_s": round(ceil_s, 2), "cps": round(chars / dur, 2) if dur else None,
    }
    if dur < floor_s:
        verdict["verdict"] = "BLOCK_TRUNCATED"
        print(json.dumps(verdict))
        sys.stderr.write(
            f"duration-guard: TRUNCATED — {dur:.3f}s < floor {floor_s:.2f}s "
            f"for {chars} chars. Silent synthesis failure; re-render required.\n")
        return 6
    if dur > ceil_s:
        verdict["verdict"] = "BLOCK_RUNAWAY"
        print(json.dumps(verdict))
        sys.stderr.write(
            f"duration-guard: RUNAWAY — {dur:.3f}s > ceiling {ceil_s:.2f}s "
            f"for {chars} chars. Overflow generation; re-render required.\n")
        return 7
    verdict["verdict"] = "PASS"
    print(json.dumps(verdict))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
