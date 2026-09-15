#!/usr/bin/env python3
"""
iarif_duration_guard.py — render-length guard for the i-ARIF TTS pipeline.

WHY THIS EXISTS
    A synthesis call can return HTTP 200 with a 0.216 s file. That is a *silent*
    failure: the pipeline reports success, the file is written, and any downstream
    ASR (Whisper) transcribes noise and hallucinates fluent prose ("Terima kasih
    kerana menonton!") which then gets attributed to the voice. The guard stops
    that class of artifact at the source: below the floor we do NOT return success
    and we do NOT emit the file.

MODEL
    BM pacing measured on this federation's own renders: 8-12 non-whitespace
    characters per second. From that:
        expected_min_s = chars / 12      (fast speech)
        expected_max_s = chars / 8       (slow speech)
        floor          = max(0.4 * expected_min_s, LONG_TEXT_FLOOR_S if long)
        ceiling        = CEILING_RATIO * expected_max_s
    The floor catches truncation/transient drops; the ceiling catches runaway
    generation (the documented MiMo failure: 202 s for ~50 s of text).

EXIT CODES
    0  pass
    3  below floor
    4  above ceiling
    2  usage / measurement failure
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

CHARS_PER_SEC_MIN = 12.0      # fast BM speech
CHARS_PER_SEC_MAX = 8.0       # slow BM speech
FLOOR_RATIO = 0.4
LONG_TEXT_CHARS = 40
LONG_TEXT_FLOOR_S = 2.0
CEILING_RATIO = 3.0           # documented MiMo runaway is ~4x -> caught


def measure_duration_s(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"ffprobe failed on {path}: {out.stderr.strip()}")
    return float(out.stdout.strip())


def text_chars(text: str) -> int:
    """Speech-bearing characters only: whitespace carries no syllables."""
    return len(re.sub(r"\s+", "", text))


def thresholds(chars: int) -> dict:
    expected_min = chars / CHARS_PER_SEC_MIN
    expected_max = chars / CHARS_PER_SEC_MAX
    floor = FLOOR_RATIO * expected_min
    if chars >= LONG_TEXT_CHARS:
        floor = max(floor, LONG_TEXT_FLOOR_S)
    ceiling = CEILING_RATIO * expected_max
    return {
        "chars": chars,
        "expected_min_s": round(expected_min, 3),
        "expected_max_s": round(expected_max, 3),
        "floor_s": round(floor, 3),
        "ceiling_s": round(ceiling, 3),
    }


def verdict(path: str, text: str) -> dict:
    chars = text_chars(text)
    th = thresholds(chars)
    try:
        dur = measure_duration_s(path)
    except Exception as exc:                                    # noqa: BLE001
        return {"ok": False, "exit": 2, "reason": f"measurement failed: {exc}"}
    ok, code, why = True, 0, "pass"
    if dur < th["floor_s"]:
        ok, code, why = False, 3, "below_floor"
    elif dur > th["ceiling_s"]:
        ok, code, why = False, 4, "above_ceiling"
    return {
        "ok": ok, "exit": code, "reason": why,
        "duration_s": round(dur, 3), "thresholds": th,
        "ratio_to_expected_min": round(dur / th["expected_min_s"], 3) if th["expected_min_s"] else None,
    }


def selftest() -> int:
    cases = [
        # (chars, duration_s, expected_exit, label)
        (88, 0.216, 3, "the real silent failure — 0.216s for 88 chars"),
        (88, 7.5, 0, "88 chars at 11.7 chars/s — healthy"),
        (88, 11.0, 0, "88 chars at 8.0 chars/s — slow but valid"),
        (88, 1.5, 3, "88 chars truncated to 1.5s"),
        (143, 13.35, 0, "this session's measured V9 pipeline render"),
        (143, 11.15, 0, "this session's trimmed V9 render"),
        (143, 202.0, 4, "the documented MiMo runaway"),
        (5, 0.003, 3, "degenerate 0.003s stub"),
    ]
    failures = []
    for chars, dur, want, label in cases:
        th = thresholds(chars)
        if dur < th["floor_s"]:
            got = 3
        elif dur > th["ceiling_s"]:
            got = 4
        else:
            got = 0
        mark = "PASS" if got == want else "FAIL"
        if got != want:
            failures.append(label)
        print(f"  [{mark}] {label:<52} floor={th['floor_s']:<7} ceil={th['ceiling_s']:<7} "
              f"dur={dur:<7} -> exit {got} (want {want})")
    print(json.dumps({"selftest": "ok" if not failures else "failed",
                      "cases": len(cases), "failures": failures}))
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", nargs="?", help="rendered audio file")
    ap.add_argument("--text-file", help="the text that was synthesized")
    ap.add_argument("--text", help="the text inline")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()

    if a.selftest:
        return selftest()

    if not a.audio:
        ap.error("audio path required (or --selftest)")
    if a.text_file:
        text = open(a.text_file, encoding="utf-8").read()
    elif a.text:
        text = a.text
    else:
        ap.error("--text-file or --text required")

    v = verdict(a.audio, text)
    if a.json or True:            # always JSON: the pipeline parses it
        print(json.dumps(v))
    return int(v.get("exit", 2))


if __name__ == "__main__":
    sys.exit(main())
