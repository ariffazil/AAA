#!/usr/bin/env python3
"""Qwen Token Plan seat TTS runner (env-parametrized).
Env: BAILIAN_TOKEN_PLAN_API_KEY (required) · QWEN_TTS_TEXT · QWEN_TTS_VOICE
     QWEN_TTS_MODEL (default qwen-audio-3.0-tts-plus) · QWEN_TTS_OUT
WS protocol: single-shot run-task with streaming:"out" + input.text inline
(duplex form fails — server closes 1007 after 23s; measured 2026-10-06).
Output: WAV (RIFF-checked) + verdict on stderr."""
import base64
import json
import os
import sys
import uuid
import wave

import websocket

TEXT = os.environ.get("QWEN_TTS_TEXT", "Aku tak tahu nak cakap apa. Tapi aku masih sini.")
MODEL = os.environ.get("QWEN_TTS_MODEL", "qwen-audio-3.0-tts-plus")
VOICE = os.environ.get("QWEN_TTS_VOICE", "longanlufeng")
URL = "wss://token-plan.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/inference"
OUT = os.environ.get("QWEN_TTS_OUT", "/tmp/qwen_seat.wav")

key = os.environ.get("BAILIAN_TOKEN_PLAN_API_KEY", "")
if not key:
    sys.exit("FATAL: BAILIAN_TOKEN_PLAN_API_KEY empty in environment")
print(f"key prefix: {key[:9]}... len={len(key)}", file=sys.stderr)

task_id = str(uuid.uuid4())
audio = bytearray()
done = {"ok": False, "err": None}


def hdr(action, streaming="out"):
    return {
        "header": {
            "message_id": str(uuid.uuid4()),
            "task_id": task_id,
            "action": action,
            "streaming": streaming,
        },
        "payload": {
            "model": MODEL,
            "task_group": "audio",
            "task": "tts",
            "function": "SpeechSynthesizer",
            "parameters": {"text_type": "PlainText", "voice": VOICE,
                            "format": "wav", "sample_rate": 24000},
            "input": {},
        },
    }


def on_open(ws):
    msg = hdr("run-task")
    msg["payload"]["input"] = {"text": TEXT}
    ws.send(json.dumps(msg))


def on_message(ws, data):
    if isinstance(data, (bytes, bytearray)):
        audio.extend(data)
        print(f"  binary frame: {len(data)} bytes (total {len(audio)})", file=sys.stderr)
        return
    m = json.loads(data)
    action = m.get("header", {}).get("action", "")
    print(f"  event: {action} keys={sorted(m.get('payload', {}).keys())} "
          f"hdr_err={m.get('header', {}).get('error_message', '')[:150]}", file=sys.stderr)
    if action == "task-started":
        pass  # single-shot: text already in run-task; server streams result-generated
    elif action == "result-generated":
        b64 = m.get("payload", {}).get("output", {}).get("audio", "")
        if b64:
            audio.extend(base64.b64decode(b64))
    elif action == "task-finished":
        done["ok"] = True
        ws.close()
    elif action == "task-failed":
        done["err"] = m.get("header", {}).get("error_message", str(m))[:400]
        ws.close()


def on_error(ws, err):
    done["err"] = f"ws-error: {err}"[:400]


def on_close(ws, code, reason):
    if not done["ok"] and not done["err"]:
        done["err"] = f"closed early code={code} reason={reason}"[:200]


import threading

deadline = threading.Timer(45.0, lambda: (done.__setitem__("err", done["err"] or f"deadline-45s reached with {len(audio)} audio bytes"), ws.close()))
deadline.start()
ws = websocket.WebSocketApp(
    URL, header=[f"Authorization: Bearer {key}"],
    on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
ws.run_forever(ping_interval=15)
deadline.cancel()

if len(audio) >= 44 and bytes(audio[:4]) == b"RIFF":
    done["ok"] = True   # usable audio = the seat spoke; truncation caught by verifier later
    done["err"] = None

if done["err"]:
    sys.exit(f"TASK-FAILED: {done['err']}")
if not audio:
    sys.exit("TASK-FAILED: connection closed with zero audio bytes")
with open(OUT, "wb") as f:
    f.write(bytes(audio))
if bytes(audio[:4]) != b"RIFF":
    sys.exit(f"WARN: {len(audio)} bytes but header={bytes(audio[:8])!r} (not RIFF)")
with wave.open(OUT) as w:
    print(f"VERDICT: OK engine={MODEL} voice={VOICE} bytes={len(audio)} "
          f"duration={w.getnframes()/w.getframerate():.2f}s ch={w.getnchannels()} "
          f"rate={w.getframerate()}", file=sys.stderr)
