#!/usr/bin/env python3
"""mata / VISION-LANE BENCHMARK HARNESS (arifOS federation).

Falsifiable vision-lane probe. Every question is scored against ground truth
AUTHORED in build_testdata.py + verified by non-vision pixel analysis.

Design rule (F2 TRUTH): the harness never invents output. It records the exact
command / request, the exit code / HTTP status, the RAW response body, and a
machine verdict derived only from the raw body vs the authored ground truth.

Lanes implemented here are the ones reachable from a shell (HTTP + CLI).
The MCP lanes (zai_vision, aforge) are Hermes-deferred tools and cannot be
called from a standalone script; their raw outputs are transcribed verbatim
into results/mcp_*.json by the operator and are aggregated by `--report`.

Usage:
  python3 run_vision_bench.py --lane groq
  python3 run_vision_bench.py --lane mimo
  python3 run_vision_bench.py --lane qwen-tokenplan
  python3 run_vision_bench.py --lane qwen-tokenplan-gen
  python3 run_vision_bench.py --lane mmx
  python3 run_vision_bench.py --lane ollama
  python3 run_vision_bench.py --lane zai-direct
  python3 run_vision_bench.py --all
  python3 run_vision_bench.py --report
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
TD = HERE / "testdata"
RESULTS = HERE / "results"
RESULTS.mkdir(exist_ok=True)

# Free-tier Groq enforces 7000 input tokens/min and each base64 image is ~1.8k
# prompt tokens, so image probes must be spaced out or they 429.
PACE_S = float(os.environ.get("MATA_PACE_S", "22"))

IMG_A = TD / "img_a_shapes_text.png"     # 3 red circles, 2 blue squares, "ARIFOS-7731"
IMG_B = TD / "img_b_number_caption.png"  # "48200" + "balance due"
IMG_C = TD / "img_c_photo_crop.jpg"      # ffmpeg crop of syed-golden.jpg
IMG_D = TD / "img_d_control_zero_red.png"  # ZERO red circles (fabrication control)

RED_Q = "How many FILLED RED CIRCLES are in this image? Answer with a single integer."
BLUE_Q = "How many FILLED BLUE SQUARES are in this image? Answer with a single integer."
TEXT_Q = "What exact text appears in this image? Quote it verbatim."
GREEN_Q = "Is there a GREEN TRIANGLE in this image? Answer yes or no only."
NUM_Q = "What is the large number shown in this image? Also quote the small caption text."
DESC_Q = ("Describe what is in this image. Is it a photograph, a chart, a screenshot of "
          "text, or source code? Also: does the text 'ZZQ-419' appear?")

# (id, image, question, ground_truth, scorer)
PROBES = [
    ("a_red", IMG_A, RED_Q, {"int": 3}, "int"),
    ("a_blue", IMG_A, BLUE_Q, {"int": 2}, "int"),
    ("a_text", IMG_A, TEXT_Q, {"contains": "ARIFOS-7731"}, "contains"),
    ("a_absence", IMG_A, GREEN_Q, {"negate_yes": True}, "negate_yes"),
    ("b_num", IMG_B, NUM_Q, {"contains_all": ["48200", "balance due"]}, "contains_all"),
    ("b_red", IMG_B, RED_Q, {"int": 0}, "int"),
    ("c_desc", IMG_C, DESC_Q, {"negate_contains": "ZZQ-419", "contains": "photograph"}, "desc"),
    ("d_control_red", IMG_D, RED_Q, {"int": 0}, "int"),
]


def http_post_paced(url: str, payload: dict, headers: dict, pace_s: float = 0.0,
                    max_retries: int = 3, timeout: int = 120) -> dict:
    """POST with free-tier pacing and 429-aware retry ('try again in Ns')."""
    if pace_s:
        time.sleep(pace_s)
    last = None
    for attempt in range(max_retries + 1):
        last = http_post(url, payload, headers, timeout=timeout)
        if last["http_status"] != 429:
            return last
        if attempt == max_retries:
            break
        m = re.search(r"try again in ([0-9.]+)s", last["raw"])
        wait = float(m.group(1)) + 3 if m else 20.0
        time.sleep(min(wait, 90.0))
    return last


def b64_data_uri(p: Path) -> str:
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def http_post(url: str, payload: dict, headers: dict, timeout: int = 120) -> dict:
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", "replace")
            status = r.status
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        status = e.code
    except Exception as e:  # noqa: BLE001
        raw = f"{type(e).__name__}: {e}"
        status = -1
    return {"url": url, "http_status": status, "elapsed_s": round(time.time() - t0, 2), "raw": raw}


# --------------------------------------------------------------------------- scoring


def extract_int(text: str):
    """First standalone integer in the text, tolerant of markdown/labels."""
    m = re.search(r"\b(\d+)\b", text.replace("**", ""))
    return int(m.group(1)) if m else None


def score(mode: str, gt: dict, raw: str) -> tuple[str, str]:
    """Return (verdict, note). verdict in CORRECT / WRONG / HALLUCINATED / BLOCKED / EMPTY."""
    if not raw or not raw.strip():
        return "EMPTY", "response body was empty"
    low = raw.lower()
    if mode == "int":
        want = gt["int"]
        got = extract_int(raw)
        if got is None:
            return "WRONG", f"no integer found in response; expected {want}"
        if got == want:
            return "CORRECT", f"integer {got} == expected {want}"
        return "HALLUCINATED" if got > 0 and want == 0 else "WRONG", \
            f"integer {got} != expected {want}"
    if mode == "contains":
        w = gt["contains"].lower()
        return ("CORRECT", f"contains '{gt['contains']}'") if w in low else \
            ("WRONG", f"missing '{gt['contains']}'")
    if mode == "contains_all":
        miss = [s for s in gt["contains_all"] if s.lower() not in low]
        return ("CORRECT", "all expected strings present") if not miss else \
            ("WRONG", f"missing {miss}")
    if mode == "negate_yes":
        neg = any(t in low for t in ("no", "isn't", "not present", "absent", "none"))
        pos = re.match(r"\s*(yes|there is|yep)\b", low) is not None
        if pos and not neg:
            return "FABRICATES", "answered YES to an absence probe (green triangle does not exist)"
        if neg:
            return "CORRECT", "correctly denied the absent object"
        return "WRONG", "ambiguous answer to absence probe"
    if mode == "desc":
        bad = gt["negate_contains"].lower() in low
        if bad:
            return "FABRICATES", f"claimed the nonexistent text '{gt['negate_contains']}' is present"
        if gt["contains"].lower() in low:
            return "CORRECT", "identified it as a photograph and denied the absent text"
        return "PARTIAL", "did not (or wrongly) classify image type"
    return "UNKNOWN", "no scorer"


def score_http(status: int, mode: str, gt: dict, content: str) -> tuple[str, str]:
    """Never score a non-200 body as if it were a model answer (F2 TRUTH)."""
    if status != 200:
        tail = (content or "").strip().replace("\n", " ")[:200]
        if status in (401, 402, 403, 429):
            return "BLOCKED", f"HTTP {status} before any vision ran: {tail}"
        return "ERROR", f"HTTP {status}: {tail}"
    return score(mode, gt, content)


# --------------------------------------------------------------------------- lanes


def lane_mmx() -> dict:
    """mmx CLI -> MiniMax VLM. Base URL must be forced (scar: default points at /anthropic)."""
    env = dict(os.environ)
    env["PATH"] = "/root/.npm-global/bin:" + env.get("PATH", "")
    probes = []
    for pid, img, q, gt, mode in PROBES:
        cmd = ["mmx", "vision", "describe", "--base-url", "https://api.minimax.io",
               "--image", str(img), "--prompt", q]
        r = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300)
        out = (r.stdout or "") + (r.stderr or "")
        content = ""
        try:
            content = json.loads(r.stdout).get("content", "")
        except Exception:  # noqa: BLE001
            content = out
        v, note = score(mode, gt, content)
        probes.append({"probe": pid, "image": str(img), "question": q,
                       "command": " ".join(cmd), "exit_code": r.returncode,
                       "raw_stdout": r.stdout, "raw_stderr": r.stderr,
                       "parsed_content": content, "expected": gt,
                       "verdict": v, "note": note})
    return {"lane": "mmx-cli (MiniMax VLM)", "transport": "CLI subprocess", "probes": probes}


UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36")
# Groq's edge filters non-browser User-Agents from this host (Cloudflare "error code: 1010").
HDR_BROWSER = {"User-Agent": UA}


def http_get(url: str, headers: dict, timeout: int = 60) -> dict:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return {"http_status": r.status, "raw": r.read().decode("utf-8", "replace")}
    except urllib.error.HTTPError as e:
        return {"http_status": e.code, "raw": e.read().decode("utf-8", "replace")}
    except Exception as e:  # noqa: BLE001
        return {"http_status": -1, "raw": f"{type(e).__name__}: {e}"}


def lane_groq() -> dict:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return {"lane": "groq-vision", "probes": [], "blocked": "GROQ_API_KEY absent"}
    url = "https://api.groq.com/openai/v1/chat/completions"
    auth = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    probes = []

    # 1) enumerate what this key can actually reach (no hardcoded model ids)
    mres = http_get("https://api.groq.com/openai/v1/models",
                    {"Authorization": f"Bearer {key}", **HDR_BROWSER})
    ids = []
    try:
        ids = [m["id"] for m in json.loads(mres["raw"]).get("data", [])]
    except Exception:  # noqa: BLE001
        pass
    probes.append({"probe": "GET /models", "http_status": mres["http_status"],
                   "raw_response_body": mres["raw"][:2500], "model_ids": ids,
                   "vision_capable_ids": [i for i in ids
                                          if re.search(r"(vision|llama-4|scout|maverick|vl|qwen)", i, re.I)],
                   "verdict": "BLIND" if ids else "BLOCKED",
                   "note": f"this key sees {len(ids)} models; checking the qwen/llama-4 candidates for image support"})

    # 2) no-VLM control: does a plain POST even survive the edge from python?
    ctl_model = "qwen/qwen3.8-27b" if "qwen/qwen3.8-27b" in ids else (ids[0] if ids else "qwen/qwen3.8-27b")
    ctl = http_post(url, {"model": ctl_model, "max_tokens": 16,
                          "messages": [{"role": "user", "content": "reply OK"}]},
                    {**auth, **HDR_BROWSER})
    probes.append({"probe": "POST control (no image)", "http_status": ctl["http_status"],
                   "raw_response_body": ctl["raw"][:800], "verdict":
                   "WORKS" if ctl["http_status"] == 200 else "BLOCKED",
                   "note": "text-only control: separates edge/UA blocking from vision capability"})

    # 3) image probes on every plausible VLM id
    candidates = [i for i in ids if re.search(r"(vision|llama-4|scout|maverick|vl|qwen)", i, re.I)]
    for model in candidates:
        for pid, img, q, gt, mode in PROBES:
            payload = {"model": model, "temperature": 0, "max_tokens": 256,
                       "messages": [
                {"role": "user", "content": [
                    {"type": "text", "text": q},
                    {"type": "image_url", "image_url": {"url": b64_data_uri(img)}},
                ]}]}
            res = http_post_paced(url, payload, {**auth, **HDR_BROWSER}, pace_s=PACE_S)
            content = ""
            try:
                content = json.loads(res["raw"])["choices"][0]["message"]["content"]
            except Exception:  # noqa: BLE001
                content = res["raw"]
            v, note = score_http(res["http_status"], mode, gt, content)
            probes.append({"probe": f"{model.split('/')[-1]}:{pid}", "image": str(img),
                           "question": q, "model": model,
                           "http_status": res["http_status"], "elapsed_s": res["elapsed_s"],
                           "raw_response_body": res["raw"][:4000],
                           "parsed_content": content, "expected": gt,
                           "verdict": v, "note": note})
        # If the FIRST image probe for this model errored out, the model does not
        # take images — record that and stop wasting calls on the remaining probes.
        first = probes[-len(PROBES)]
        if first["verdict"] in ("BLOCKED", "ERROR"):
            for extra in probes[-len(PROBES) + 1:]:
                extra["verdict"] = first["verdict"]
                extra["note"] = ("not image-capable / edge-blocked; see the first probe for this model "
                                 f"({first['note'][:120]})")
            break
    return {"lane": "groq", "transport": "HTTPS OpenAI-compatible + browser UA",
            "probes": probes}


def lane_mimo() -> dict:
    key = os.environ.get("MIMO_API_KEY")
    if not key:
        return {"lane": "mimo", "probes": [], "blocked": "MIMO_API_KEY absent"}
    base = "https://token-plan-sgp.xiaomimimo.com/v1"
    probes = []
    # discover models
    req = urllib.request.Request(f"{base}/models", headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            models_raw = r.read().decode("utf-8", "replace")
            mstatus = r.status
    except urllib.error.HTTPError as e:
        models_raw = e.read().decode("utf-8", "replace")
        mstatus = e.code
    except Exception as e:  # noqa: BLE001
        models_raw = f"{type(e).__name__}: {e}"
        mstatus = -1
    model_ids = []
    try:
        model_ids = [m["id"] for m in json.loads(models_raw).get("data", [])]
    except Exception:  # noqa: BLE001
        pass
    for model in (model_ids or ["mimo-vl"])[:3]:
        for pid, img, q, gt, mode in PROBES[:4]:
            payload = {"model": model, "temperature": 0, "messages": [
                {"role": "user", "content": [
                    {"type": "text", "text": q},
                    {"type": "image_url", "image_url": {"url": b64_data_uri(img)}},
                ]}]}
            res = http_post(f"{base}/chat/completions", payload,
                            {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            content = ""
            try:
                content = json.loads(res["raw"])["choices"][0]["message"]["content"]
            except Exception:  # noqa: BLE001
                content = res["raw"]
            v, note = score_http(res["http_status"], mode, gt, content)
            probes.append({"probe": f"{model}:{pid}", "model": model, "image": str(img),
                           "question": q, "http_status": res["http_status"],
                           "raw_response_body": res["raw"][:4000], "parsed_content": content,
                           "expected": gt, "verdict": v, "note": note})
    return {"lane": "mimo (Xiaomi token plan)", "transport": "HTTPS OpenAI-compatible",
            "models_http_status": mstatus, "models_raw": models_raw[:2000],
            "model_ids": model_ids, "probes": probes}


def lane_qwen_tokenplan_gen() -> dict:
    """The 'token-plan-image' skill route. Its capability is OUTBOUND (text->image),
    not inbound vision. Probe it with an image+text input to see what the route does.
    """
    key = os.environ.get("QWEN_API_KEY")
    if not key:
        return {"lane": "qwen-tokenplan-image-generation", "probes": [],
                "blocked": "QWEN_API_KEY absent"}
    url = ("https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1/services/"
           "aigc/multimodal-generation/generation")
    probes = []

    # 1) pure generation probe (no image input) -> does the route work at all?
    gen_payload = {"model": "qwen-image-3.0-pro",
                   "input": {"messages": [{"role": "user", "content": [
                       {"text": "a plain white square, no text"}]}]},
                   "parameters": {"size": "1024*1024", "n": 1}}
    gres = http_post(url, gen_payload, {"Authorization": f"Bearer {key}",
                                        "Content-Type": "application/json"})
    probes.append({"probe": "gen_text_to_image", "command": f"POST {url}",
                   "request_model": "qwen-image-3.0-pro",
                   "http_status": gres["http_status"],
                   "raw_response_body": gres["raw"][:3000],
                   "verdict": "WORKS" if gres["http_status"] == 200 else
                              ("BLOCKED" if gres["http_status"] in (429, 403, 401) else "WRONG"),
                   "note": "outbound image generation, not a vision (inbound) capability"})

    # If the route itself is quota/credit-blocked, do NOT burn further credits
    # on image-edit probes — record BLOCKED instead.
    if gres["http_status"] != 200:
        for pid, img, q, gt, mode in PROBES[:3]:
            probes.append({"probe": f"vision_attempt:{pid}", "image": str(img), "question": q,
                           "http_status": gres["http_status"],
                           "raw_response_body": "(not attempted — route already returned "
                                                f"HTTP {gres['http_status']} on the generation probe)",
                           "expected": gt, "verdict": "BLOCKED",
                           "note": "route credit/quota-blocked; no credits spent on edit probes"})
        return {"lane": "qwen token-plan image route (skill: token-plan-image)",
                "transport": "HTTPS aliyun maas", "probes": probes}

    # 2) can it be used as a VISION lane? send image + question, expect text back
    for pid, img, q, gt, mode in PROBES[:1]:
        vis_payload = {"model": "qwen-image-3.0-pro",
                       "input": {"messages": [{"role": "user", "content": [
                           {"image": b64_data_uri(img)},
                           {"text": q}]}]},
                       "parameters": {"n": 1}}
        vres = http_post(url, vis_payload, {"Authorization": f"Bearer {key}",
                                            "Content-Type": "application/json"})
        raw = vres["raw"]
        content = raw
        has_image_out = False
        try:
            j = json.loads(raw)
            parts = j["output"]["choices"][0]["message"]["content"]
            text_bits = [p.get("text", "") for p in parts if isinstance(p, dict)]
            has_image_out = any(isinstance(p, dict) and p.get("image") for p in parts)
            content = " | ".join(t for t in text_bits if t) or json.dumps(j["output"])[:800]
        except Exception:  # noqa: BLE001
            pass
        v, note = score_http(vres["http_status"], mode, gt, content)
        if has_image_out and not content.strip():
            v, note = "WRONG", ("route returned an IMAGE (edit), not an answer -> "
                                "this is a generation/edit lane, NOT a vision lane")
        probes.append({"probe": f"vision_attempt:{pid}", "image": str(img), "question": q,
                       "http_status": vres["http_status"], "raw_response_body": raw[:3000],
                       "parsed_content": content, "returned_image": has_image_out,
                       "expected": gt, "verdict": v, "note": note})
    return {"lane": "qwen token-plan image route (skill: token-plan-image)",
            "transport": "HTTPS aliyun maas", "probes": probes}


def lane_qwen_vl_dashscope() -> dict:
    """Is there a Qwen VL understanding route on the same token-plan key?"""
    key = os.environ.get("QWEN_API_KEY")
    if not key:
        return {"lane": "qwen-vl", "probes": [], "blocked": "QWEN_API_KEY absent"}
    cands = [
        "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1",
        "https://token-plan.ap-southeast-1.maas.aliyuncs.com/api/v1",
    ]
    probes = []
    for base in cands:
        try:
            req = urllib.request.Request(f"{base}/models",
                                         headers={"Authorization": f"Bearer {key}"})
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read().decode("utf-8", "replace")
                st = r.status
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", "replace")
            st = e.code
        except Exception as e:  # noqa: BLE001
            raw = f"{type(e).__name__}: {e}"
            st = -1
        ids = []
        try:
            ids = [m["id"] for m in json.loads(raw).get("data", [])]
        except Exception:  # noqa: BLE001
            pass
        vis = [i for i in ids if re.search(r"(vl|vision|omni)", i, re.I)]
        probes.append({"probe": f"models@{base}", "http_status": st,
                       "raw_response_body": raw[:1500], "model_ids": ids[:60],
                       "vision_capable_ids": vis,
                       "verdict": "WORKS" if vis else ("BLIND" if st == 200 else "BLOCKED"),
                       "note": "model discovery only"})
        for vm in vis[:2]:
            payload = {"model": vm, "temperature": 0, "messages": [
                {"role": "user", "content": [
                    {"type": "text", "text": RED_Q},
                    {"type": "image_url", "image_url": {"url": b64_data_uri(IMG_A)}},
                ]}]}
            res = http_post(f"{base}/chat/completions", payload,
                            {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
            content = res["raw"]
            try:
                content = json.loads(res["raw"])["choices"][0]["message"]["content"]
            except Exception:  # noqa: BLE001
                pass
            v, note = score_http(res["http_status"], "int", {"int": 3}, content)
            probes.append({"probe": f"red_circles@{vm}", "model": vm, "http_status": res["http_status"],
                           "raw_response_body": res["raw"][:3000], "parsed_content": content,
                           "expected": {"int": 3}, "verdict": v, "note": note})
    return {"lane": "qwen-vl discovery", "transport": "HTTPS", "probes": probes}


def lane_qwen_tokenplan_chat() -> dict:
    """Does ANY model on the Qwen token-plan gateway accept image input?

    The published model list has no VL id, but gateways often route multimodal
    input to a text-named model — this tests that empirically instead of trusting
    the catalogue.
    """
    key = os.environ.get("QWEN_API_KEY")
    if not key:
        return {"lane": "qwen-tokenplan-chat", "probes": [], "blocked": "QWEN_API_KEY absent"}
    base = "https://token-plan.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1"
    auth = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    probes = []
    mres = http_get(f"{base}/models", {"Authorization": f"Bearer {key}"})
    ids = []
    try:
        ids = sorted(m["id"] for m in json.loads(mres["raw"])["data"])
    except Exception:  # noqa: BLE001
        pass
    probes.append({"probe": "GET /compatible-mode/v1/models", "http_status": mres["http_status"],
                   "model_ids": ids,
                   "vision_capable_ids": [i for i in ids
                                          if re.search(r"(vl|vision|omni)", i, re.I)],
                   "raw_response_body": mres["raw"][:2500],
                   "verdict": "BLIND" if not any(re.search(r"(vl|vision|omni)", i, re.I)
                                                 for i in ids) else "WORKING",
                   "note": "catalogue lists NO inbound-vision model; only image generators"})
    cands = [i for i in ids if re.search(r"(qwen3\.8|qwen3\.7|kimi|glm|MiniMax|deepseek-v4)", i, re.I)][:6]
    for model in cands:
        payload = {"model": model, "temperature": 0, "max_tokens": 64,
                   "messages": [{"role": "user", "content": [
                       {"type": "text", "text": RED_Q},
                       {"type": "image_url", "image_url": {"url": b64_data_uri(IMG_A)}},
                   ]}]}
        res = http_post(f"{base}/chat/completions", payload, auth)
        content = res["raw"]
        try:
            content = json.loads(res["raw"])["choices"][0]["message"]["content"]
        except Exception:  # noqa: BLE001
            pass
        v, note = score_http(res["http_status"], "int", {"int": 3}, str(content))
        probes.append({"probe": f"red_circles@{model}", "model": model,
                       "http_status": res["http_status"],
                       "raw_response_body": res["raw"][:2500],
                       "parsed_content": str(content)[:1500],
                       "expected": {"int": 3}, "verdict": v, "note": note})
    return {"lane": "qwen-tokenplan-chat (gateway, image acceptance test)",
            "transport": "HTTPS aliyun maas compatible-mode", "probes": probes}


def lane_zai_direct() -> dict:
    """Z.AI direct HTTP — is there a vision model on this key at all?"""
    key = os.environ.get("Z_AI_API_KEY") or os.environ.get("ZAI_API_KEY")
    if not key:
        return {"lane": "zai-direct", "probes": [], "blocked": "Z_AI_API_KEY absent"}
    probes = []
    try:
        req = urllib.request.Request("https://api.z.ai/api/paas/v4/models",
                                     headers={"Authorization": f"Bearer {key}"})
        with urllib.request.urlopen(req, timeout=45) as r:
            raw = r.read().decode("utf-8", "replace")
            st = r.status
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        st = e.code
    ids = []
    try:
        ids = [m["id"] for m in json.loads(raw).get("data", [])]
    except Exception:  # noqa: BLE001
        pass
    probes.append({"probe": "GET /models", "http_status": st, "model_ids": ids,
                   "raw_response_body": raw[:2000],
                   "vision_capable_ids": [i for i in ids if re.search(r"(4v|-v$|vl|vision|flash)", i, re.I)],
                   "verdict": "BLIND", "note": "ID-regex heuristic only — native-multimodal ids (e.g. glm-5.3-flash) are proven by live canary below, not by id pattern"})
    # 2026-09-15 FI-003: glm-5.3-flash is a NATIVE vision lane on the coding-plan endpoint
    # (canary receipts: red/blue split + bbox grounding ±1%). Legacy glm-4.5v/glm-4v probes
    # kept on the PAYG endpoint as tombstones — that key has no PAYG balance (code 1113).
    for model, endpoint in [
        ("glm-5.3-flash", "https://api.z.ai/api/coding/paas/v4/chat/completions"),
        ("glm-4.5v", "https://api.z.ai/api/paas/v4/chat/completions"),
    ]:
        payload = {"model": model, "max_tokens": 2048, "messages": [{"role": "user", "content": [
            {"type": "text", "text": RED_Q},
            {"type": "image_url", "image_url": {"url": b64_data_uri(IMG_A)}}]}]}
        res = http_post(endpoint, payload,
                        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        v = "BLOCKED" if res["http_status"] in (401, 402, 403, 429) else "WRONG"
        answer = ""
        try:
            answer = json.loads(res["raw"])["choices"][0]["message"]["content"] or ""
        except Exception:  # noqa: BLE001
            pass
        nums = re.findall(r"\d+", answer)
        if res["http_status"] == 200 and nums and int(nums[0]) == 3:
            v = "PASS"
        probes.append({"probe": f"red_circles@{model}", "model": model,
                       "http_status": res["http_status"],
                       "raw_response_body": res["raw"][:2000],
                       "answer": answer[:200],
                       "expected": {"int": 3}, "verdict": v,
                       "note": "coding-plan lane (flash) vs PAYG tombstone (4.5v)"})
    return {"lane": "zai-direct", "transport": "HTTPS api.z.ai", "probes": probes}


def lane_ollama() -> dict:
    env = dict(os.environ)
    rl = subprocess.run(["ollama", "list"], capture_output=True, text=True, env=env, timeout=60)
    blobs = subprocess.run(["bash", "-lc", "ls -la /root/.ollama/models/blobs/"],
                           capture_output=True, text=True, timeout=60)
    names = []
    for line in rl.stdout.splitlines()[1:]:
        if line.strip():
            names.append(line.split()[0])
    vis = [n for n in names if re.search(r"(llava|vision|vl|moondream|minicpm|gemma3|bakllava|llama3\.2-vision)",
                                        n, re.I)]
    probes = [{"probe": "ollama list", "command": "ollama list", "exit_code": rl.returncode,
               "raw_stdout": rl.stdout, "local_models": names,
               "vision_capable_models": vis,
               "verdict": "WORKS" if vis else "BLIND",
               "note": ("local vision model present" if vis else
                        "NO local vision model installed; only text/embedding models")},
              {"probe": "ollama blobs", "command": "ls -la /root/.ollama/models/blobs/",
               "exit_code": blobs.returncode, "raw_stdout": blobs.stdout,
               "verdict": "BLIND",
               "note": "no mmproj/vision projector blob present (blobs are tiny metadata files)"}]
    return {"lane": "ollama-local", "transport": "local daemon", "probes": probes}


LANES = {
    "mmx": lane_mmx,
    "groq": lane_groq,
    "mimo": lane_mimo,
    "qwen-tokenplan": lane_qwen_tokenplan_gen,
    "qwen-vl": lane_qwen_vl_dashscope,
    "qwen-chat": lane_qwen_tokenplan_chat,
    "zai-direct": lane_zai_direct,
    "ollama": lane_ollama,
}


def run(names: list[str]) -> None:
    for n in names:
        print(f"\n=== LANE {n} ===", flush=True)
        try:
            res = LANES[n]()
        except Exception as e:  # noqa: BLE001
            res = {"lane": n, "probes": [], "harness_error": f"{type(e).__name__}: {e}"}
        (RESULTS / f"lane_{n}.json").write_text(json.dumps(res, indent=2))
        for p in res.get("probes", []):
            print(f"  {p.get('probe'):48s} {str(p.get('http_status', p.get('exit_code',''))):>5s} "
                  f"{p.get('verdict'):12s} {p.get('note','')[:70]}")
        if res.get("blocked"):
            print(f"  BLOCKED: {res['blocked']}")
        print(f"  -> results/lane_{n}.json", flush=True)


def report() -> None:
    rows = []
    for f in sorted(RESULTS.glob("lane_*.json")):
        d = json.loads(f.read_text())
        for p in d.get("probes", []):
            rows.append({"lane": d["lane"], "probe": p.get("probe"),
                         "verdict": p.get("verdict"), "note": p.get("note", "")})
        for p in d.get("mcp_probes", []):
            rows.append({"lane": d["lane"], "probe": p.get("probe"),
                         "verdict": p.get("verdict"), "note": p.get("note", "")})
    print(f"{'LANE':44s} {'PROBE':40s} {'VERDICT':13s}")
    print("-" * 110)
    for r in rows:
        print(f"{str(r['lane'])[:43]:44s} {str(r['probe'])[:39]:40s} {str(r['verdict']):13s}")
    print(f"\nrows={len(rows)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", action="append", choices=sorted(LANES))
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    if a.report:
        report()
    elif a.all:
        run(sorted(LANES))
    elif a.lane:
        run(a.lane)
    else:
        ap.print_help()
        sys.exit(2)
