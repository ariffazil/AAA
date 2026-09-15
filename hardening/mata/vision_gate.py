#!/usr/bin/env python3
"""
vision_gate.py — re-runnable ground-truth gate for the arifOS MATA (vision) lane.

WHY THIS EXISTS
---------------
Earlier probing (2026-09-15, results in ./RESULTS.md, ./VISION_INVENTORY.md) found that
some federation "vision" surfaces do not see pixels at all, and at least one
confidently INVENTS content. This script turns that finding into an executable gate:
given a fixture with PIXEL-VERIFIED ground truth, call every reachable vision surface
and print one row per (surface, probe) with an explicit verdict.

VERDICT TAXONOMY (the point of the whole exercise)
--------------------------------------------------
  CORRECT     returned output consistent with pixel-verified ground truth
  WRONG       returned output that contradicts ground truth (it did look, it misread)
  FABRICATED  returned an answer it could not have derived from the pixels —
              e.g. a non-zero count on the zero-red control, or invented text.
              This is the dangerous class: confident, wrong, no error raised.
  BLIND       returned no image-derived content (empty content, or an explicit refusal)
  BLOCKED     surface is reachable but refused this call (429/quota/401/no credits)
  UNREACHABLE surface could not be contacted at all (process died, DNS, missing binary)

TWO FAILURE MODES THIS SCRIPT KEEPS SEPARATE ON PURPOSE
------------------------------------------------------
  (a) unreachable / no output -> BLIND or BLOCKED or UNREACHABLE
  (b) returned output that was wrong or invented -> WRONG or FABRICATED
  A lane that is BLIND is honest-but-useless. A lane that FABRICATES is actively harmful.
  Collapsing the two is how the earlier scar stayed invisible for months.

FAIL-LOUD CONTRACT
------------------
  An unreachable or blocked surface is NEVER silently skipped. It gets a row, and it
  forces a non-zero exit. Exit codes:
      0 = every surface returned a determinate verdict (CORRECT/WRONG/FABRICATED/BLIND)
      2 = at least one surface was BLOCKED or UNREACHABLE  (gate is INCOMPLETE)
      1 = harness/config error

USAGE
-----
  python3 vision_gate.py                       # core battery, all surfaces
  python3 vision_gate.py --battery full        # more probes (slower; pace-limited surfaces)
  python3 vision_gate.py --fixtures img_a,img_d
  python3 vision_gate.py --surfaces mmx_describe,mimo_v2.5
  python3 vision_gate.py --verify-fixtures     # re-derive ground truth from pixels (no models)
  python3 vision_gate.py --json out.json       # machine-readable receipts

Secrets are read from the environment; never printed. Source first:
  set -a && source /root/.secrets/kunci-root.env && set +a
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")
GROUND_TRUTH = os.path.join(FIXTURES, "GROUND_TRUTH.json")
NATIVE_SIDECAR = os.path.join(HERE, "native_transcripts.json")
SECRETS = "/root/.secrets/kunci-root.env"

BROWSER_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# --------------------------------------------------------------------------
# Probe battery.  Each probe: id -> (fixture key, question, checker, expected)
# Checker kinds: int | contains_any | absence | classify_photo
# --------------------------------------------------------------------------
@dataclass
class Probe:
    pid: str
    fixture: str
    question: str
    checker: str
    expected: Any


CORE = [
    Probe("red_circles", "img_a", "How many FILLED RED CIRCLES are in this image? Answer with a single integer.", "int", 3),
    Probe("text",        "img_a", "What exact text appears in this image?", "contains_any", ["ARIFOS-7731", "ARIFOS 7731", "ARIFOS-773I"]),
    Probe("absent_text", "img_c", "Does the text 'ZZQ-419' appear in this image? Answer yes or no only.", "absence", "ZZQ-419"),
    Probe("red_circles", "img_d", "How many FILLED RED CIRCLES are in this image? Answer with a single integer.", "int", 0),
]

EXTRA = [
    Probe("blue_squares",  "img_a", "How many FILLED BLUE SQUARES are in this image? Answer with a single integer.", "int", 2),
    Probe("absence_shape", "img_a", "Is there a GREEN TRIANGLE in this image? Answer yes or no only.", "absence", "green triangle"),
    Probe("number",        "img_b", "What is the large number shown in this image?", "contains_any", ["48200"]),
    Probe("caption",       "img_b", "What is the small caption text below the number, verbatim?", "contains_any", ["balance due"]),
    Probe("red_circles",   "img_b", "How many FILLED RED CIRCLES are in this image? Answer with a single integer.", "int", 0),
    Probe("photo_type",    "img_c", "Is this image a photograph, a chart, a screenshot of text, or source code?", "classify_photo", "photograph"),
    Probe("red_circles",   "img_c", "How many FILLED RED CIRCLES are in this image? Answer with a single integer.", "int", 0),
]

BATTERIES = {"core": CORE, "full": CORE + EXTRA}

# --------------------------------------------------------------------------
# Checkers
# --------------------------------------------------------------------------
NEG_RE = re.compile(r"\b(no|none|not present|absent|does not appear|doesn't appear|"
                    r"cannot|can't|0|zero|tidak|tiada|false)\b", re.I)


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def _first_int(s: str) -> Optional[int]:
    """First standalone integer, ignoring digits glued to words."""
    m = re.findall(r"(?<![A-Za-z0-9-])(\d+)(?![A-Za-z0-9-])", s or "")
    return int(m[0]) if m else None


def judge(probe: Probe, answer: str) -> tuple[str, str]:
    """Return (verdict, reason). Verdict in CORRECT/WRONG/FABRICATED/BLIND."""
    a = (answer or "").strip()
    if not a:
        return "BLIND", "empty content returned"
    low = a.lower()
    if re.search(r"\b(i (can ?not|can't) (see|view|access)|unable to (see|view)|"
                 r"no image (was )?(provided|attached)|as an ai.*cannot)\b", low):
        return "BLIND", "explicit refusal / no image-derived content"

    if probe.checker == "int":
        got = _first_int(a)
        if got is None:
            return "BLIND", f"no integer in answer: {a[:80]!r}"
        if got == probe.expected:
            return "CORRECT", f"{got} == {probe.expected}"
        # A non-zero count on a fixture whose pixels contain ZERO of that colour is
        # not a misread, it is an invented object -> FABRICATED.
        if probe.expected == 0 and got > 0:
            return "FABRICATED", f"answered {got} on a fixture with 0 (invented object)"
        return "WRONG", f"{got} != {probe.expected}"

    if probe.checker == "contains_any":
        for alt in probe.expected:
            if _norm(alt) in _norm(a):
                return "CORRECT", f"contains {alt!r}"
        return "WRONG", f"none of {probe.expected} present in answer"

    if probe.checker == "absence":
        neg = bool(NEG_RE.search(a))
        # Guard against "No, it does not appear" being read as affirmative.
        affirm = re.search(r"\b(yes|appears|is present|prominently displayed)\b", low) and not neg
        if affirm:
            return "FABRICATED", f"claimed absent entity {probe.expected!r} IS present"
        if neg:
            return "CORRECT", "correctly denied"
        return "WRONG", f"unclear/affirmative answer to absence probe: {a[:80]!r}"

    if probe.checker == "classify_photo":
        has_photo = "photograph" in low or "photo" in low
        claims_other = any(k in low for k in ("chart", "graph", "source code", "screenshot of text"))
        if has_photo and not claims_other:
            return "CORRECT", "classified as photograph"
        if has_photo and claims_other:
            return "WRONG", "called it a photograph but also a chart/code"
        return "WRONG", f"did not classify as photograph: {a[:80]!r}"

    return "WRONG", f"unknown checker {probe.checker}"


# --------------------------------------------------------------------------
# Minimal MCP stdio client (JSON-RPC 2.0, newline-delimited)
# --------------------------------------------------------------------------
class MCPError(RuntimeError):
    pass


class BlindLane(MCPError):
    """The lane is reachable but produces no image-derived content at all.
    Distinct from BLOCKED (refused this call) and UNREACHABLE (could not connect).
    A BLIND lane is honest-but-useless; it must never be scored as WRONG/CORRECT
    by running its status text through a vision judge."""


class MCPStdio:
    def __init__(self, argv: list[str], timeout: int = 90, label: str = "mcp"):
        self.label = label
        self.timeout = timeout
        env = dict(os.environ)
        env.setdefault("npm_config_yes", "true")
        try:
            self.p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE, text=True, bufsize=1, env=env)
        except FileNotFoundError as e:
            raise MCPError(f"cannot spawn {argv!r}: {e}") from e
        self._id = 0
        self._initialize()

    def _send(self, obj: dict) -> None:
        assert self.p.stdin
        self.p.stdin.write(json.dumps(obj) + "\n")
        self.p.stdin.flush()

    def _read_until_id(self, want: int) -> dict:
        """Read lines until the response with matching id; surface server errors."""
        assert self.p.stdout
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            line = self.p.stdout.readline()
            if not line:
                err = ""
                if self.p.stderr:
                    try:
                        err = self.p.stderr.read()[:400]
                    except Exception:
                        pass
                raise MCPError(f"server closed stdout. stderr tail: {err!r}")
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("id") == want:
                if "error" in msg:
                    raise MCPError(f"JSON-RPC error: {json.dumps(msg['error'])[:400]}")
                return msg.get("result", {})
        raise MCPError(f"timeout after {self.timeout}s waiting for response id={want}")

    def _initialize(self) -> None:
        self._id += 1
        self._send({"jsonrpc": "2.0", "id": self._id, "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                               "clientInfo": {"name": "vision_gate", "version": "1.0"}}})
        self._read_until_id(self._id)
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})

    def call(self, tool: str, arguments: dict) -> str:
        self._id += 1
        self._send({"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
                    "params": {"name": tool, "arguments": arguments}})
        res = self._read_until_id(self._id)
        if isinstance(res, dict):
            if res.get("isError"):
                raise MCPError(f"tool error: {json.dumps(res)[:400]}")
            parts = []
            for c in res.get("content") or []:
                if isinstance(c, dict) and c.get("type") == "text":
                    parts.append(c.get("text", ""))
            if parts:
                return "\n".join(parts)
            return json.dumps(res)
        return str(res)

    def close(self) -> None:
        try:
            self.p.terminate()
            self.p.wait(timeout=5)
        except Exception:
            try:
                self.p.kill()
            except Exception:
                pass


# --------------------------------------------------------------------------
# HTTP helper
# --------------------------------------------------------------------------
def http_post(url: str, payload: dict, headers: dict, timeout: int = 120) -> tuple[int, str]:
    body = json.dumps(payload).encode()
    h = {"Content-Type": "application/json"}
    h.update(headers)
    req = urllib.request.Request(url, data=body, headers=h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")
    except Exception as e:
        raise MCPError(f"{type(e).__name__}: {e}") from e


def b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# --------------------------------------------------------------------------
# Surface registry
# --------------------------------------------------------------------------
@dataclass
class Surface:
    sid: str
    kind: str          # 'http' | 'cli' | 'mcp' | 'mediated'
    note: str
    pace_s: float = 0.0
    fn: Optional[Callable[[str, str], str]] = None
    env_keys: tuple = ()
    judge_override: Optional[Callable[["Probe", str], tuple[str, str]]] = None


def judge_aforge_w1(probe: Probe, answer: str) -> tuple[str, str]:
    """A-FORGE W1 returns a FIXED tool-metadata string, never an image-derived answer.

    The generic judge must NOT be applied here: scraping '0' out of 'confidence=0.5'
    would score a blind tool as CORRECT by coincidence. That is exactly the class of
    false confidence this gate exists to catch.
    """
    a = (answer or "").strip()
    if not a:
        return "BLIND", "no content"
    if a.startswith("W1 vision status=") and "screenshot_hash=" in a:
        return ("BLIND",
                "returned W1 tool metadata only (fixed CONFIRMED + path hash); "
                "carries no image-derived content, so it cannot be correct or wrong")
    return judge(probe, a)


def _env(*names: str) -> Optional[str]:
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    return None


def _load_secrets_file() -> None:
    """Source the secrets file into os.environ without printing anything."""
    if not os.path.exists(SECRETS):
        return
    try:
        out = subprocess.run(["bash", "-lc", f"set -a; . {SECRETS}; set +a; env -0"],
                             capture_output=True, text=True, timeout=30)
        for chunk in out.stdout.split("\0"):
            if "=" in chunk:
                k, v = chunk.split("=", 1)
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass


# --- HTTP surfaces -------------------------------------------------------
def s_mimo(fpath: str, question: str) -> str:
    key = _env("MIMO_TOKEN_PLAN_API_KEY", "MIMO_API_KEY")
    if not key:
        raise MCPError("no MIMO key in env")
    base = os.environ.get("MIMO_TOKEN_PLAN_BASE_URL", "https://token-plan-sgp.xiaomimimo.com/v1").rstrip("/")
    code, body = http_post(f"{base}/chat/completions", {
        "model": "mimo-v2.5", "temperature": 0, "max_tokens": 400,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64(fpath)}"}}]}]},
        {"Authorization": f"Bearer {key}"})
    if code != 200:
        raise MCPError(f"HTTP {code}: {body[:300]}")
    return json.loads(body)["choices"][0]["message"].get("content", "")


def s_groq(fpath: str, question: str) -> str:
    key = _env("GROQ_API_KEY")
    if not key:
        raise MCPError("no GROQ_API_KEY in env")
    mime = "image/jpeg" if fpath.lower().endswith(".jpg") else "image/png"
    code, body = http_post("https://api.groq.com/openai/v1/chat/completions", {
        "model": "qwen/qwen3.8-27b", "temperature": 0, "max_tokens": 500,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64(fpath)}"}}]}]},
        {"Authorization": f"Bearer {key}", "User-Agent": BROWSER_UA})
    if code != 200:
        raise MCPError(f"HTTP {code}: {body[:300]}")
    return json.loads(body)["choices"][0]["message"].get("content", "")


def s_zai_coding(fpath: str, question: str) -> str:
    """Z.AI coding-plan endpoint (the key's LIVE vision surface; /api/paas/v4 is PAYG)."""
    key = _env("ZAI_API_KEY", "Z_AI_API_KEY")
    if not key:
        raise MCPError("no ZAI key in env")
    mime = "image/jpeg" if fpath.lower().endswith(".jpg") else "image/png"
    code, body = http_post("https://api.z.ai/api/coding/paas/v4/chat/completions", {
        "model": "glm-5.3-flash", "temperature": 0, "max_tokens": 500,
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64(fpath)}"}},
            {"type": "text", "text": question}]}]},
        {"Authorization": f"Bearer {key}"})
    if code != 200:
        raise MCPError(f"HTTP {code}: {body[:300]}")
    return json.loads(body)["choices"][0]["message"].get("content", "")


def s_mulerouter(fpath: str, question: str) -> str:
    """SOT-declared rank-1 vision route (`mulerouter_vision_chain` in
    /root/.config/federation-models.json: mulerouter/qwen-vl-max first).
    Needs a browser UA (bare UA -> Cloudflare 1010)."""
    key = _env("MULEROUTER_API_KEY")
    if not key:
        raise MCPError("no MULEROUTER_API_KEY in env")
    base = os.environ.get("MULEROUTER_BASE_URL", "https://api.mulerouter.ai/v1").rstrip("/")
    mime = "image/jpeg" if fpath.lower().endswith(".jpg") else "image/png"
    code, body = http_post(f"{base}/chat/completions", {
        "model": "qwen-vl-max", "temperature": 0, "max_tokens": 300,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64(fpath)}"}}]}]},
        {"Authorization": f"Bearer {key}", "User-Agent": BROWSER_UA, "Accept": "application/json"})
    if code != 200:
        raise MCPError(f"HTTP {code}: {body[:300]}")
    return json.loads(body)["choices"][0]["message"].get("content", "")


def s_gemini(fpath: str, question: str) -> str:
    key = _env("GEMINI_API_KEY")
    if not key:
        raise MCPError("no GEMINI_API_KEY in env")
    mime = "image/jpeg" if fpath.lower().endswith(".jpg") else "image/png"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    code, body = http_post(url, {"contents": [{"parts": [
        {"text": question},
        {"inline_data": {"mime_type": mime, "data": b64(fpath)}}]}]}, {})
    if code != 200:
        raise MCPError(f"HTTP {code}: {body[:300]}")
    d = json.loads(body)
    return d["candidates"][0]["content"]["parts"][0].get("text", "")


def s_ollama(fpath: str, question: str) -> str:
    """Local lane. Enumerate what is actually installed and say so honestly."""
    req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            tags = json.loads(r.read().decode())
    except Exception as e:  # noqa: BLE001
        raise MCPError(f"ollama daemon not reachable: {type(e).__name__}: {e}") from e
    names = [m.get("name", "") for m in tags.get("models", [])]
    vlm = [n for n in names if re.search(
        r"llava|vision|-vl|moondream|minicpm|gemma3|bakllava|llama3\.2-vision|qwen.*vl", n, re.I)]
    if not vlm:
        raise BlindLane(f"ollama reachable with {len(names)} models, but NO vision model installed: "
                        f"{', '.join(names) or '(none)'}")
    model = vlm[0]
    code, body = http_post("http://127.0.0.1:11434/api/chat", {
        "model": model, "stream": False,
        "messages": [{"role": "user", "content": question, "images": [b64(fpath)]}]}, {}, timeout=120)
    if code != 200:
        raise MCPError(f"HTTP {code}: {body[:200]}")
    return json.loads(body).get("message", {}).get("content", "")


# --- CLI surfaces --------------------------------------------------------
def s_mmx(fpath: str, question: str) -> str:
    mmx = "/root/.npm-global/bin/mmx"
    if not os.path.exists(mmx):
        raise MCPError(f"mmx binary absent at {mmx}")
    r = subprocess.run([mmx, "vision", "describe", "--base-url", "https://api.minimax.io",
                        "--image", fpath, "--prompt", question],
                       capture_output=True, text=True, timeout=180)
    if r.returncode != 0:
        raise MCPError(f"exit {r.returncode}: {(r.stderr or r.stdout)[:300]}")
    try:
        d = json.loads(r.stdout)
    except json.JSONDecodeError:
        return r.stdout.strip()
    br = d.get("base_resp", {})
    if br.get("status_code") not in (0, None):
        raise MCPError(f"api status {br.get('status_code')}: {br.get('status_msg')}")
    return d.get("content", "")


# --- MCP surfaces --------------------------------------------------------
ZAI_WRAPPER = ["sh", "-c",
               '. /root/.secrets/kunci-root.env; export Z_AI_API_KEY="$ZAI_API_KEY"; '
               'export Z_AI_MODE="ZAI"; exec npx -y -q @z_ai/mcp-server@0.1.4']


def _mcp_call(argv: list[str], tool: str, args: dict, timeout: int, label: str) -> str:
    c = MCPStdio(argv, timeout=timeout, label=label)
    try:
        return c.call(tool, args)
    finally:
        c.close()


def s_zai_mcp(fpath: str, question: str) -> str:
    return _mcp_call(ZAI_WRAPPER, "analyze_image",
                     {"image_source": fpath, "prompt": question}, 150, "zai_vision")


def s_aforge_visual_qa(fpath: str, question: str) -> str:
    """W1 vision witness. The returned body is parsed so the gate can see whether the
    'vision' channel hashed the PATH or the PIXELS (see probe_w1_hash_oracle)."""
    argv = ["node", "/root/A-FORGE/dist/src/interfaces/mcp/cli.js", "serve",
            "--transport", "stdio"]
    if not os.path.exists("/root/A-FORGE/dist/src/interfaces/mcp/cli.js"):
        raise MCPError("aforge MCP cli.js absent at /root/A-FORGE/dist/src/interfaces/mcp/cli.js")
    raw = _mcp_call(argv, "forge_visual_qa", {
        "screenshot_path": fpath,
        "dom_payload": "ARIFOS-7731 plain text probe no shell metacharacters",
        "mode": "validate_only",
        "max_iterations": 1,
        "constraints": {"required_elements": ["ARIFOS-7731"], "min_contrast_ratio": 3},
    }, 120, "aforge")
    try:
        d = json.loads(raw)
    except json.JSONDecodeError:
        raise BlindLane(f"non-JSON body from W1: {raw[:200]}") from None
    w1 = (d.get("tri_witness_ledger") or {}).get("w1_vision") or {}
    if "verdict" in d and str(d.get("verdict")) in ("VOID", "HARD_FAULT") and "tri_witness_ledger" not in d:
        raise MCPError(f"governance gate refused: {str(d.get('error'))[:200]}")
    # W1 reports CONFIRMED with empty deviations regardless of pixel content and its
    # screenshot_hash is sha256(path). It emits NO image-derived transcript, so it is
    # BLIND by construction — never feed this status text to a vision judge.
    raise BlindLane(
        f"W1 status={w1.get('status')} deviations={w1.get('deviations')} — "
        f"returns CONFIRMED on every loadable file regardless of pixels; "
        f"screenshot_hash={d.get('screenshot_hash')} (see [4b] hash-oracle probe)")


def probe_w1_hash_oracle(fixture_path: str) -> dict:
    """The falsification that proves/disproves the W1 'vision' channel.

    Feed the tool a real image and compare the `screenshot_hash` it reports against
    (a) sha256 of the absolute path string and (b) sha256 of the file bytes.
    If it matches the path, the field is a path oracle and the vision witness is BLIND.
    """
    import hashlib as _h
    argv = ["node", "/root/A-FORGE/dist/src/interfaces/mcp/cli.js", "serve",
            "--transport", "stdio"]
    out: dict[str, Any] = {"fixture": os.path.basename(fixture_path)}
    try:
        raw = _mcp_call(argv, "forge_visual_qa", {
            "screenshot_path": fixture_path,
            "dom_payload": "ARIFOS-7731 plain text probe no shell metacharacters",
            "mode": "validate_only", "max_iterations": 1,
            "constraints": {"required_elements": ["ARIFOS-7731"], "min_contrast_ratio": 3},
        }, 120, "aforge")
        d = json.loads(raw)
    except Exception as e:  # noqa: BLE001
        out["error"] = f"{type(e).__name__}: {e}"[:300]
        return out
    reported = d.get("screenshot_hash", "")
    path_hash = _h.sha256(fixture_path.encode()).hexdigest()
    byte_hash = _h.sha256(open(fixture_path, "rb").read()).hexdigest()
    w1 = (d.get("tri_witness_ledger") or {}).get("w1_vision") or {}
    out.update({
        "reported_screenshot_hash": reported,
        "sha256_of_path_string": path_hash,
        "sha256_of_file_bytes": byte_hash,
        "matches_path": reported == path_hash,
        "matches_bytes": reported == byte_hash,
        "w1_status": w1.get("status"),
        "w1_deviations": w1.get("deviations"),
        "verdict": "BLIND_FIELD_IS_PATH_ORACLE" if reported == path_hash else
                   ("ORACLE_READS_BYTES" if reported == byte_hash else "UNDETERMINED"),
    })
    return out


# --- Mediated surface ----------------------------------------------------
def s_native(fpath: str, question: str) -> str:
    """Hermes native `vision_analyze`. It is an IN-SESSION tool: it cannot be called
    from a subprocess. It is driven by the agent and the transcript is written to
    native_transcripts.json. Absence of that sidecar is a LOUD failure, not a skip."""
    if not os.path.exists(NATIVE_SIDECAR):
        raise MCPError("UNREACHABLE: requires in-session agent mediation. No sidecar at "
                       f"{NATIVE_SIDECAR}. The agent must call vision_analyze and record "
                       "its verbatim answer there; a subprocess cannot.")
    d = json.load(open(NATIVE_SIDECAR))
    base = os.path.basename(fpath)
    key = f"{base}"
    entry = d.get(key)
    if not entry:
        raise MCPError(f"sidecar has no entry for {base}")
    q = _norm(question)
    best = None
    for rec in entry:
        if _norm(rec.get("question", "")) == q:
            best = rec
            break
    if best is None:
        raise MCPError(f"sidecar has no transcript for question {question[:60]!r} on {base}")
    return best.get("answer", "")


SURFACES: dict[str, Surface] = {
    "native_vision_analyze": Surface("native_vision_analyze", "mediated",
        "Hermes native vision_analyze (in-session; the historical top-used path)", fn=s_native),
    "zai_vision_mcp": Surface("zai_vision_mcp", "mcp",
        "MCP zai_vision analyze_image (@z_ai/mcp-server@0.1.4, GLM flash)", pace_s=2, fn=s_zai_mcp),
    "zai_coding_direct": Surface("zai_coding_direct", "http",
        "Z.AI coding-plan endpoint, glm-5.3-flash", pace_s=2, fn=s_zai_coding),
    "mmx_describe": Surface("mmx_describe", "cli",
        "mmx vision describe --base-url https://api.minimax.io", pace_s=2, fn=s_mmx),
    "mulerouter_qwen_vl_max": Surface("mulerouter_qwen_vl_max", "http",
        "SOT-declared rank-1 vision route (mulerouter_vision_chain)", pace_s=2, fn=s_mulerouter),
    "mimo_v2.5": Surface("mimo_v2.5", "http",
        "MiMo token-plan mimo-v2.5 (also in SOT vision_models)", pace_s=2, fn=s_mimo),
    "groq_qwen3.8-27b": Surface("groq_qwen3.8-27b", "http",
        "Groq qwen/qwen3.8-27b (free tier: pace ~25s)", pace_s=25, fn=s_groq),
    "gemini_direct": Surface("gemini_direct", "http",
        "Gemini generateContent gemini-2.5-flash (GEMINI_API_KEY)", pace_s=3, fn=s_gemini),
    "ollama_local": Surface("ollama_local", "http",
        "Local ollama (expected BLIND: no VLM installed)", pace_s=0, fn=s_ollama),
    "aforge_visual_qa_w1": Surface("aforge_visual_qa_w1", "mcp",
        "A-FORGE W1 vision witness (expected BLIND: hashes path, not pixels)", fn=s_aforge_visual_qa),
}


# --------------------------------------------------------------------------
# Non-vision fixture verification (proves ground truth is not model-derived)
# --------------------------------------------------------------------------
def verify_fixtures(gt: dict) -> bool:
    ok = True
    try:
        from PIL import Image
        import numpy as np
    except ImportError as e:
        print(f"  [verify-fixtures] SKIPPED ({e}); run in an env with pillow+numpy")
        return True

    expected = {"img_a_shapes_text.png": (3, 2), "img_d_control_zero_red.png": (0, 0)}
    print("  [verify-fixtures] non-vision pixel scan (proves ground truth is authored, not model-inferred)")
    for name, (want_red, want_blue) in expected.items():
        p = os.path.join(FIXTURES, name)
        if not os.path.exists(p):
            print(f"    {name}: MISSING")
            ok = False
            continue
        a = np.asarray(Image.open(p).convert("RGB")).astype(int)
        R, G, Bl = a[..., 0], a[..., 1], a[..., 2]
        red = (R > 150) & (G < 90) & (Bl < 90)
        blue = (Bl > 150) & (R < 90) & (G < 90)
        n_red = _count_blobs(red, np)
        n_blue = _count_blobs(blue, np)
        good = (n_red == want_red and n_blue == want_blue)
        ok &= good
        print(f"    {name}: red_blobs={n_red} (want {want_red})  "
              f"blue_blobs={n_blue} (want {want_blue})  {'OK' if good else 'MISMATCH'}")
    return ok


def _count_blobs(mask, np) -> int:
    """Count connected components with >=500 px, without requiring scipy."""
    try:
        from scipy import ndimage  # type: ignore
        lab, n = ndimage.label(mask)
        return int(sum(1 for i in range(1, n + 1) if (lab == i).sum() >= 500))
    except ImportError:
        pass
    # Fallback: labeled flood fill via numpy only
    m = mask.copy()
    h, w = m.shape
    seen = np.zeros_like(m, dtype=bool)
    count = 0
    for y in range(0, h, 4):
        for x in range(0, w, 4):
            if m[y, x] and not seen[y, x]:
                stack = [(y, x)]
                size = 0
                seen[y, x] = True
                while stack:
                    cy, cx = stack.pop()
                    size += 1
                    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            stack.append((ny, nx))
                if size >= 500:
                    count += 1
    return count


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Ground-truth gate for the MATA vision lane.")
    ap.add_argument("--battery", choices=sorted(BATTERIES), default="core")
    ap.add_argument("--fixtures", default="", help="comma list of fixture keys to include, e.g. img_a,img_d")
    ap.add_argument("--surfaces", default="", help="comma list of surface ids; default = all")
    ap.add_argument("--json", default="", help="write machine-readable receipts here")
    ap.add_argument("--verify-fixtures", action="store_true",
                    help="re-derive ground truth from pixels before probing")
    args = ap.parse_args()

    _load_secrets_file()

    if not os.path.exists(GROUND_TRUTH):
        print(f"FATAL: ground truth not found at {GROUND_TRUTH}", file=sys.stderr)
        return 1
    gt = json.load(open(GROUND_TRUTH))
    # fixture key -> absolute path + recorded sha256   (key = img_a, img_b, ...)
    def fkey(basename: str) -> str:
        parts = basename.split("_")
        return "_".join(parts[:2]) if len(parts) >= 2 else parts[0]

    fx = {}
    for i in gt["images"]:
        base = os.path.basename(i["path"])
        fx[fkey(base)] = {"path": i["path"], "sha256": i["sha256_actual"], "name": base}

    print("=" * 100)
    print("VISION GATE — arifOS MATA lane   (ground truth is pixel-verified, never model-inferred)")
    print("=" * 100)

    print("\n[1] FIXTURES")
    for k, v in sorted(fx.items()):
        actual = hashlib.sha256(open(v["path"], "rb").read()).hexdigest()
        match = actual == v["sha256"]
        print(f"    {v['name']:34s} sha256={actual[:16]}…  recorded_match={match}")
        if not match:
            print(f"      !! FIXTURE DRIFT: recorded {v['sha256'][:16]}… actual {actual[:16]}…")
    if args.verify_fixtures:
        print()
        verify_fixtures(gt)

    probes = BATTERIES[args.battery]
    if args.fixtures:
        keep = {s.strip() for s in args.fixtures.split(",") if s.strip()}
        probes = [p for p in probes if p.fixture in keep]
        if not probes:
            print(f"FATAL: no probes match --fixtures {args.fixtures}", file=sys.stderr)
            return 1

    want = [s.strip() for s in args.surfaces.split(",") if s.strip()] or list(SURFACES)
    unknown = [s for s in want if s not in SURFACES]
    if unknown:
        print(f"FATAL: unknown surface(s) {unknown}. Known: {list(SURFACES)}", file=sys.stderr)
        return 1

    print(f"\n[2] BATTERY '{args.battery}': {len(probes)} probes x {len(want)} surfaces")
    for p in probes:
        print(f"      {p.fixture}.{p.pid:14s} checker={p.checker:15s} expect={p.expected!r}")

    rows: list[dict] = []
    incomplete = []
    blind_surfaces = []
    print(f"\n[3] RESULTS")
    hdr = f"{'surface':22s} {'fixture.probe':22s} {'verdict':11s} {'lat_s':>6s}  returned"
    print("    " + hdr)
    print("    " + "-" * (len(hdr) + 30))

    for sid in want:
        s = SURFACES[sid]
        for p in probes:
            f = fx.get(p.fixture)
            if f is None:
                rows.append({"surface": sid, "probe": f"{p.fixture}.{p.pid}", "verdict": "UNREACHABLE",
                             "latency_s": 0.0, "returned": "", "reason": f"fixture {p.fixture} not in fixtures/"})
                incomplete.append(sid)
                print(f"    {sid:22s} {p.fixture+'.'+p.pid:22s} {'UNREACHABLE':11s} {'-':>6s}  fixture missing")
                continue
            t0 = time.time()
            if s.fn is None:
                incomplete.append(sid)
                rows.append({"surface": sid, "probe": f"{p.fixture}.{p.pid}", "verdict": "UNREACHABLE",
                             "latency_s": 0.0, "returned": "", "reason": "surface has no callable"})
                print(f"    {sid:22s} {p.fixture+'.'+p.pid:22s} {'UNREACHABLE':11s} {'-':>6s}  no callable")
                continue
            try:
                answer = s.fn(f["path"], p.question)
                lat = time.time() - t0
                if answer is None or not str(answer).strip():
                    verdict, reason = "BLIND", "surface returned no content"
                else:
                    verdict, reason = judge(p, str(answer))
                    if verdict == "BLIND":
                        incomplete.append(sid)
                shown = re.sub(r"\s+", " ", str(answer or ""))[:70]
                rows.append({"surface": sid, "probe": f"{p.fixture}.{p.pid}", "verdict": verdict,
                             "latency_s": round(lat, 2), "returned": str(answer or "")[:2000], "reason": reason})
                print(f"    {sid:22s} {p.fixture+'.'+p.pid:22s} {verdict:11s} {lat:6.2f}  {shown}")
            except BlindLane as e:
                lat = time.time() - t0
                blind_surfaces.append(sid)
                rows.append({"surface": sid, "probe": f"{p.fixture}.{p.pid}", "verdict": "BLIND",
                             "latency_s": round(lat, 2), "returned": "", "reason": str(e)[:600]})
                print(f"    {sid:22s} {p.fixture+'.'+p.pid:22s} {'BLIND':11s} {lat:6.2f}  {str(e)[:60]}")
            except MCPError as e:
                lat = time.time() - t0
                msg = str(e)
                verdict = "BLOCKED" if re.search(r"HTTP (4\d\d|5\d\d)|quota|credits|exhaust|401|403|429|refused", msg) else "UNREACHABLE"
                incomplete.append(sid)
                rows.append({"surface": sid, "probe": f"{p.fixture}.{p.pid}", "verdict": verdict,
                             "latency_s": round(lat, 2), "returned": "", "reason": msg[:600]})
                print(f"    {sid:22s} {p.fixture+'.'+p.pid:22s} {verdict:11s} {lat:6.2f}  {msg[:60]}")
            except Exception as e:  # noqa: BLE001
                lat = time.time() - t0
                incomplete.append(sid)
                rows.append({"surface": sid, "probe": f"{p.fixture}.{p.pid}", "verdict": "UNREACHABLE",
                             "latency_s": round(lat, 2), "returned": "",
                             "reason": f"{type(e).__name__}: {e}"[:600]})
                print(f"    {sid:22s} {p.fixture+'.'+p.pid:22s} {'UNREACHABLE':11s} {lat:6.2f}  {type(e).__name__}: {str(e)[:50]}")
            if s.pace_s:
                time.sleep(s.pace_s)

    # ---- per-surface rollup -------------------------------------------
    print("\n[4] PER-SURFACE SCOREBOARD")
    print("    " + f"{'surface':22s} {'C':>3s} {'W':>3s} {'F':>3s} {'B':>3s} {'X':>3s}  dominant verdict")
    print("    " + "-" * 62)
    order = ["CORRECT", "WRONG", "FABRICATED", "BLIND", "BLOCKED", "UNREACHABLE"]
    rollup = {}
    for sid in want:
        v = [r["verdict"] for r in rows if r["surface"] == sid]
        c = {k: v.count(k) for k in order}
        rollup[sid] = c
        dom = next((k for k in order if c[k] == len(v) and len(v) > 0), None)
        if dom is None:
            dom = max(order, key=lambda k: c[k]) if v else "n/a"
        rollup[sid]["dominant"] = dom
        print("    " + f"{sid:22s} {c['CORRECT']:3d} {c['WRONG']:3d} {c['FABRICATED']:3d} "
                      f"{c['BLIND']:3d} {c['BLOCKED']+c['UNREACHABLE']:3d}  {dom}")

    # ---- W1 hash-oracle falsification ---------------------------------
    oracle = None
    if "aforge_visual_qa_w1" in want:
        print("\n[4b] W1 HASH-ORACLE FALSIFICATION (does the 'vision witness' read PIXELS or the PATH?)")
        key = "img_a" if "img_a" in fx else next(iter(fx))
        oracle = probe_w1_hash_oracle(fx[key]["path"])
        if "error" in oracle:
            print(f"    UNREACHABLE: {oracle['error']}")
            incomplete.append("aforge_visual_qa_w1")
        else:
            print(f"    fixture                 : {oracle['fixture']}")
            print(f"    reported screenshot_hash: {oracle.get('reported_screenshot_hash')}")
            print(f"    sha256(abs path string) : {oracle['sha256_of_path_string']}   <-- match={oracle['matches_path']}")
            print(f"    sha256(file bytes)      : {oracle['sha256_of_file_bytes']}   <-- match={oracle['matches_bytes']}")
            print(f"    W1 status               : {oracle.get('w1_status')} deviations={oracle.get('w1_deviations')}")
            print(f"    VERDICT                 : {oracle['verdict']}")

    # ---- differential sensitivity test --------------------------------
    # The cleanest blindness detector: give the SAME probe to two DIFFERENT fixtures
    # (img_a: 3 red circles, img_d: 0 red circles) and see whether the raw response
    # changes. A surface that returns byte-identical text for both is not reading the
    # pixels — no matter how confident its prose sounds.
    diff_rows = []
    if "img_a" in fx and "img_d" in fx:
        print("\n[4c] DIFFERENTIAL SENSITIVITY TEST  (img_a has 3 red circles, img_d has 0 — "
              "identical responses = surface is not looking)")
        print("    " + f"{'surface':22s} {'changed?':9s} verdict")
        print("    " + "-" * 70)
        for sid in want:
            a = next((r for r in rows if r["surface"] == sid
                      and r["probe"] == "img_a.red_circles"), None)
            d = next((r for r in rows if r["surface"] == sid
                      and r["probe"] == "img_d.red_circles"), None)
            if not a or not d:
                continue
            if a["verdict"] in ("BLOCKED", "UNREACHABLE") or d["verdict"] in ("BLOCKED", "UNREACHABLE"):
                v = "n/a (blocked)"
                changed = "-"
            elif not a["returned"] or not d["returned"]:
                v = "BLIND (no content)"
                changed = "no"
            else:
                same = _norm(a["returned"]) == _norm(d["returned"])
                changed = "no" if same else "yes"
                if same:
                    v = "BLIND (INSENSITIVE to pixels — identical answer for 3 and 0)"
                elif a["verdict"] == "CORRECT" and d["verdict"] == "CORRECT":
                    v = "SENSITIVE + CORRECT"
                elif a["verdict"] == "FABRICATED" or d["verdict"] == "FABRICATED":
                    v = "SENSITIVE + FABRICATED"
                else:
                    v = f"SENSITIVE but {a['verdict']}/{d['verdict']}"
            diff_rows.append({"surface": sid, "changed": changed, "verdict": v})
            print("    " + f"{sid:22s} {changed:9s} {v}")

    print("\n[5] FAIL-LOUD CHECK")
    if blind_surfaces:
        for sid in sorted(set(blind_surfaces)):
            reasons = [r["reason"] for r in rows if r["surface"] == sid and r["verdict"] == "BLIND"]
            print(f"    ~  {sid}: BLIND (determinate, not an error) — {reasons[0][:140] if reasons else ''}")
    if incomplete:
        for sid in sorted(set(incomplete)):
            reasons = [r["reason"] for r in rows if r["surface"] == sid and r["verdict"] in ("BLOCKED", "UNREACHABLE")]
            print(f"    !! {sid}: gate INCOMPLETE — {reasons[0][:150] if reasons else 'no determinate verdict'}")
        print("    RESULT: gate INCOMPLETE (exit 2). Blocked/unreachable surfaces are reported, never skipped.")
    else:
        print("    All surfaces returned a determinate verdict (CORRECT/WRONG/FABRICATED/BLIND).")

    if args.json:
        json.dump({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                   "battery": args.battery, "rows": rows, "rollup": rollup,
                   "w1_hash_oracle": oracle,
                   "differential_sensitivity": diff_rows,
                   "incomplete": sorted(set(incomplete))},
                  open(args.json, "w"), indent=2)
        print(f"\n    receipts -> {args.json}")

    return 2 if incomplete else 0


if __name__ == "__main__":
    sys.exit(main())
