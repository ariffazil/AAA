# RunPod Jupyter WebSocket Execution Pattern

Arif session 2026-08-10 — ComfyUI deployed on RunPod RTX 4090, SSH unavailable, Jupyter used as shell replacement.

## Why this exists

RunPod pods may not have SSH keys registered (public key not pasted into RunPod UI). When SSH port is unreachable but Jupyter :8888 is exposed, you can execute arbitrary commands via Jupyter's REST + WebSocket API. This is a **full shell replacement** — not a toy.

## Prerequisites

- JUPYTER_PASSWORD from pod env (fetch via REST API: `curl -H "Authorization: Bearer $RUNPOD_API_KEY" "https://rest.runpod.io/v1/pods/$POD_ID"`)
- Pod HTTP proxy URL: `https://{pod-id}-8888.proxy.runpod.net`

## The 5-step pattern

### Step 1: Login (get _xsrf cookie)

```python
import urllib.request, urllib.parse, http.cookiejar, json
TOKEN = "pod_jupyter_password"
HOST = "pod-id-8888.proxy.runpod.net"
BASE = f"https://{HOST}"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
jar = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

op.open(urllib.request.Request(f"{BASE}/login", headers=UA), timeout=15).read()
xrf = [c.value for c in jar if c.name == "_xsrf"][0]
op.open(urllib.request.Request(f"{BASE}/login",
    data=urllib.parse.urlencode({"password": TOKEN, "_xsrf": xrf}).encode(),
    method="POST", headers={**UA, "Content-Type": "application/x-www-form-urlencoded"}), timeout=15).read()
xrf = [c.value for c in jar if c.name == "_xsrf"][0]
```

**CRITICAL:** Must include browser User-Agent header. urllib default gets 403 from RunPod proxy.

### Step 2: Create kernel + WebSocket + execute

```python
import websocket, uuid, time
k = json.loads(op.open(urllib.request.Request(f"{BASE}/api/kernels",
    data=b'{"name":"python3"}', headers={**UA, "Content-Type": "application/json", "X-XSRFToken": xrf},
    method="POST"), timeout=15).read())
kid = k["id"]
cookie_str = "; ".join(f"{c.name}={c.value}" for c in jar)
ws = websocket.create_connection(f"wss://{HOST}/api/kernels/{kid}/channels?token={TOKEN}",
    timeout=30, header=[f"Cookie: {cookie_str}", f"User-Agent: {UA['User-Agent']}"])
time.sleep(1.5)
try:
    for _ in range(5): ws.settimeout(1); ws.recv()
except: pass

mid = uuid.uuid4().hex
ws.send(json.dumps({
    "header": {"msg_id": mid, "msg_type": "execute_request", "username": "", "session": mid, "version": "5.3", "date": ""},
    "parent_header": {}, "metadata": {}, "channel": "shell",
    "content": {"code": "! hostname", "silent": False, "store_history": False,
                "user_expressions": {}, "allow_stdin": False, "stop_on_error": True}, "buffers": []
}))
ws.settimeout(60)
out = []
try:
    while True:
        m = json.loads(ws.recv())
        mt = m.get("msg_type", "")
        if mt == "stream": out.append(m["content"]["text"])
        elif mt == "execute_result": out.append(m["content"].get("data", {}).get("text_plain", ""))
        elif mt == "error": out.append("\n".join(m["content"].get("traceback", [])))
        elif mt == "status" and m["content"].get("execution_state") == "idle": break
except Exception as e: out.append(f"\n[ws:{e}]")
finally:
    try: ws.close()
    except: pass
    try: op.open(urllib.request.Request(f"{BASE}/api/kernels/{kid}",
        headers={**UA, "Content-Type": "application/json", "X-XSRFToken": xrf}, method="DELETE"), timeout=10)
    except: pass
result = "".join(out)
```

### Output types

- `iopub/stream` → stdout/stderr from print() or `! command`
- `iopub/execute_result` → Python expression result
- `iopub/error` → exception traceback
- `iopub/status` → kernel busy/idle

## Shell quoting pitfall

IPython `!` escape adds quoting layer. Multi-layer escaping (Python -> WebSocket -> IPython -> bash) is fragile.

**Rule:** Write scripts to file first (via base64), then `! python3 /tmp/script.py`. Never embed complex scripts inline.

```python
import base64
b64 = base64.b64encode(script_content.encode()).decode()
# Write + run on pod:
jp_exec(f"import base64; open('/tmp/script.py','wb').write(base64.b64decode('{b64}'))")
jp_exec("! python3 /tmp/script.py")
```

## ComfyUI operational notes

- **Output directory:** ComfyUI outputs to its own `output/` dir, NOT /workspace. Use `--output-directory /workspace/output` or symlink.
- **Model filename exact match:** Must match disk filename exactly. Verify with `ls models/checkpoints/`.
- **Start:** `cd /root/ComfyUI && nohup python3 main.py --listen 127.0.0.1 --port 8188 > /tmp/comfyui.log 2>&1 &`
- **Health:** `curl -sf http://127.0.0.1:8188/system_stats`
- **API:** `POST http://127.0.0.1:8188/prompt` with workflow JSON

## Civitai download pitfall

Civitai returns 0-byte files without auth:
```bash
wget -O model.safetensors "https://civitai.com/api/download/models/290640?token=YOUR_CIVITAI_TOKEN"
```
HuggingFace models work with HF_TOKEN from kunci-mas.env.

## Verified results (2026-08-10)

- Pod: RTX 4090, 24GB VRAM, $0.74/hr
- ComfyUI v0.31.0, PyTorch 2.8.0+cu128
- RealVisXL V4.0: 832x1216 PNG, ~40s render, 1.57MB
- Download via Jupyter REST API: GET /api/contents/{path} -> base64 -> local save
