#!/usr/bin/env python3
"""Submit one txt2img job to LOCAL ComfyUI (:8188) and wait robustly.

Local-CPU renders take 13-16 min per 512px SD1.5 image. The ComfyUI HTTP
thread starves while the sampler saturates the CPU, so every request here
uses long timeouts and completion is detected via /queue, not /history
polling (see references/comfyui-local-cpu-route.md pitfall 2).

Prereq: server already running:
  cd /root/comfy/ComfyUI && .venv/bin/python main.py --cpu --listen 127.0.0.1 --port 8188 --use-split-cross-attention

Usage:
  python3 comfy_local_submit.py "prompt text" [--negative "..."] [--steps 20] [--seed 42] [--out DIR]
"""
import argparse, json, os, sys, time, urllib.request, uuid

SRV = "http://127.0.0.1:8188"


def req(path, data=None, timeout=180):
    r = urllib.request.Request(
        SRV + path,
        headers={"Content-Type": "application/json"},
        data=json.dumps(data).encode() if data else None,
    )
    return json.load(urllib.request.urlopen(r, timeout=timeout))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--negative", default="blurry, low quality, deformed, extra limbs, text, watermark")
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="/root/forge_work/comfy-local-out")
    a = ap.parse_args()

    wf = {
        "3": {"class_type": "KSampler", "inputs": {
            "seed": a.seed, "steps": a.steps, "cfg": 7.0,
            "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0,
            "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0],
            "latent_image": ["5", 0]}},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {
            "ckpt_name": "v1-5-pruned-emaonly.safetensors"}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {
            "width": 512, "height": 512, "batch_size": 1}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["4", 1], "text": a.prompt}},   # clip MUST be wired -> else 400
        "7": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["4", 1], "text": a.negative}},
        "8": {"class_type": "VAEDecode", "inputs": {
            "samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {
            "filename_prefix": "hermes_local", "images": ["8", 0]}},
    }

    t0 = time.time()
    pid = req("/prompt", {"prompt": wf, "client_id": str(uuid.uuid4())})["prompt_id"]
    print(f"queued {pid} — expect ~13-16 min on CPU; poll failures below are retried, not fatal", flush=True)

    while True:
        time.sleep(20)
        try:
            q = req("/queue", timeout=90)
            running, pending = q.get("queue_running", []), q.get("queue_pending", [])
            if not running and not pending:
                break
            print(f"  {time.time()-t0:5.0f}s queue running={len(running)} pending={len(pending)}", flush=True)
        except Exception as e:
            print(f"  {time.time()-t0:5.0f}s poll retry ({type(e).__name__})", flush=True)
        if time.time() - t0 > 2400:
            sys.exit("TIMEOUT after 40min — check server still alive (earlyoom?)")

    h = req(f"/history/{pid}", timeout=300).get(pid, {})
    st = h.get("status", {}).get("status_str")
    if st != "success":
        msgs = h.get("status", {}).get("messages", [])
        sys.exit(f"render status={st} msgs={msgs} — 'execution_interrupted' = another "
                 "session/port-owner cancelled; real traceback = check server log")
    os.makedirs(a.out, exist_ok=True)
    for node, o in h.get("outputs", {}).items():
        for im in o.get("images", []):
            url = (f"{SRV}/view?filename={im['filename']}"
                   f"&subfolder={im.get('subfolder','')}&type={im['type']}")
            data = urllib.request.urlopen(url, timeout=600).read()
            p = os.path.join(a.out, im["filename"])
            with open(p, "wb") as f:
                f.write(data)
            print(f"DONE {time.time()-t0:.0f}s -> {p} ({len(data)//1024} KB)")


if __name__ == "__main__":
    main()
