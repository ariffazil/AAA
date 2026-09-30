#!/data/data/com.termux/files/usr/bin/bash
# ═══════════════════════════════════════════════════════════════════════
# arifOS Phone Bridge — HONOR 600 Pro one-shot installer (Termux)
# Tailscale direct @ 100.64.0.6 • port 8765 • no tunnel
# 2026-09-29 · prepared by HERMES (KVM8)
# ═══════════════════════════════════════════════════════════════════════
set -euo pipefail

echo "── 1/5 packages ──"
pkg update -y >/dev/null 2>&1 || true
pkg install -y python termux-api termux-tools tmux

echo "── 2/5 dirs ──"
mkdir -p "$HOME/.bridge/photos" "$HOME/phone-bridge"
chmod 700 "$HOME/.bridge"

echo "── 3/5 server.py ──"
cat > "$HOME/phone-bridge/server.py" <<'SERVER_PY_EOF'
#!/data/data/com.termux/files/usr/bin/env python
"""Phone Bridge v0 — pure stdlib, no rust, no pydantic.

arifOS phone bridge: Termux:API capability server.
Security model:
  - Bearer token (BRIDGE_TOKEN) on every endpoint except /health
  - Explicit deny list (clipboard/notifications/sms/exec) returns 403
  - Camera photos served once then deleted from phone
  - Tailscale ACL is the network layer; this token is the app layer
"""
import os, sys, json, subprocess, tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

BRIDGE_TOKEN = os.environ.get("BRIDGE_TOKEN", "")
PORT = int(os.environ.get("BRIDGE_PORT", "8765"))
HOST = os.environ.get("BRIDGE_HOST", "0.0.0.0")
PHOTO_DIR = os.path.expanduser("~/.bridge/photos")
AUDIT_LOG = os.path.expanduser("~/.bridge/audit.log")

def audit(action, detail=""):
    from datetime import datetime, timezone
    ts = datetime.now(timezone.utc).isoformat()
    try:
        with open(AUDIT_LOG, "a") as f:
            f.write(f"{ts}\t{action}\t{detail}\n")
    except Exception:
        pass

def run(args, timeout=30):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return True, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", f"timeout after {timeout}s"
    except Exception as e:
        return False, "", str(e)

def parse_json(out):
    try:
        return json.loads(out)
    except Exception:
        return {"raw": out}

class Bridge(BaseHTTPRequestHandler):
    server_version = "PhoneBridge/0.1"

    def log_message(self, fmt, *args):
        sys.stderr.write(f"[bridge] {self.address_string()} {fmt % args}\n")

    def _send_json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file_once(self, path):
        """Serve photo then delete — artifact retention on device = zero."""
        try:
            with open(path, "rb") as f:
                data = f.read()
        finally:
            try:
                os.remove(path)
            except Exception:
                pass
        self.send_response(200)
        self.send_header("Content-Type", "image/jpeg")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Content-Disposition",
                         f'attachment; filename="{os.path.basename(path)}"')
        self.end_headers()
        self.wfile.write(data)

    def _auth_ok(self):
        return self.headers.get("Authorization", "") == f"Bearer {BRIDGE_TOKEN}"

    def _dispatch(self):
        p = urlparse(self.path).path.rstrip("/") or "/"

        # Open liveness probe (no auth, no data)
        if p == "/health":
            self._send_json(200, {"status": "ok", "device": "termux"}); return

        # Everything else requires the bearer token
        if not self._auth_ok():
            audit("AUTH_FAIL", p)
            self._send_json(401, {"error": "unauthorized"}); return

        # Explicit deny list — visible refusal, not silent 404
        if p in ("/clipboard", "/notifications", "/sms", "/sms/send",
                 "/exec", "/shell", "/contacts"):
            audit("DENIED", p)
            self._send_json(403, {"error": "denied_by_policy", "path": p}); return

        audit("CALL", p)

        if p == "/v1/status/battery":
            ok, out, err = run(["termux-battery-status"])
            self._send_json(200 if ok else 500,
                            parse_json(out) if ok else {"error": err}); return

        if p == "/v1/status/device":
            ok, out, err = run(["termux-telephony-deviceinfo"])
            self._send_json(200 if ok else 500,
                            parse_json(out) if ok else {"error": err}); return

        if p == "/v1/location/once":
            ok, out, err = run(["termux-location", "-p", "gps", "-r", "once"],
                               timeout=30)
            self._send_json(200 if ok else 500,
                            parse_json(out) if ok else {"error": err}); return

        if p == "/v1/status/wifi":
            ok, out, err = run(["termux-wifi-connectioninfo"])
            self._send_json(200 if ok else 500,
                            parse_json(out) if ok else {"error": err}); return

        if p == "/v1/sensors/snapshot":
            ok, out, err = run(["termux-sensor", "-s", "1", "-n", "1"], timeout=10)
            self._send_json(200 if ok else 500,
                            parse_json(out) if ok else {"error": err}); return

        if p.startswith("/v1/camera/capture"):
            qs = parse_qs(urlparse(self.path).query)
            cam = "1" if qs.get("lens", ["back"])[0] == "front" else "0"
            os.makedirs(PHOTO_DIR, exist_ok=True)
            fpath = os.path.join(PHOTO_DIR, f"cap_{os.getpid()}_{cam}.jpg")
            ok, out, err = run(["termux-camera-photo", "-c", cam, fpath],
                               timeout=20)
            if not ok or not os.path.exists(fpath):
                self._send_json(500, {"error": err or "capture_failed"}); return
            self._send_file_once(fpath); return

        if p == "/v1/haptics/vibrate":
            run(["termux-vibrate", "-d", "300"])
            self._send_json(200, {"ok": True}); return

        if p == "/v1/toast":
            try:
                n = int(self.headers.get("Content-Length", 0) or 0)
                body = json.loads(self.rfile.read(n) or b"{}") if n else {}
            except Exception:
                body = {}
            msg = str(body.get("message") or "")[:200]
            if not msg:
                self._send_json(400, {"error": "message_required"}); return
            run(["termux-toast", msg])
            self._send_json(200, {"ok": True}); return

        self._send_json(404, {"error": "no_route", "path": p})

    def do_GET(self):
        self._dispatch()

    def do_POST(self):
        self._dispatch()


if __name__ == "__main__":
    if not BRIDGE_TOKEN:
        print("ERROR: BRIDGE_TOKEN unset. source .env first.", file=sys.stderr)
        sys.exit(1)
    os.makedirs(os.path.dirname(AUDIT_LOG), exist_ok=True)
    print(f"[bridge] listening {HOST}:{PORT} token={BRIDGE_TOKEN[:6]}...", file=sys.stderr)
    ThreadingHTTPServer((HOST, PORT), Bridge).serve_forever()
SERVER_PY_EOF
chmod +x "$HOME/phone-bridge/server.py"

echo "── 4/5 env ──"
cat > "$HOME/phone-bridge/.env" <<'ENV_EOF'
export BRIDGE_TOKEN=73c43d31114e1f22ec7822b9bd0b8e7e1bc449d10bb29c1637b14d5dd51db52c
export BRIDGE_SIGNING_SECRET=cffc158c5d7c665642892b241315edee273ee0c471ec59081b02fc43e8edb1d4
export BRIDGE_HOST=0.0.0.0
export BRIDGE_PORT=8765
ENV_EOF
chmod 600 "$HOME/phone-bridge/.env"

echo "── 5/5 start (tmux session: bridge) ──"
termux-wake-lock 2>/dev/null || true
tmux kill-session -t bridge 2>/dev/null || true
tmux new -d -s bridge "cd \$HOME/phone-bridge && source .env && exec python server.py"
sleep 3

echo
echo "── self-check ──"
curl -s -m 5 http://127.0.0.1:8765/health || echo "(local probe failed)"
echo
tmux ls
echo
echo "DONE. Keep Termux open. Bridge binds 0.0.0.0:8765 on the Tailscale interface."
echo "Stop:  tmux kill-session -t bridge"
echo "Logs:  tmux attach -t bridge"
