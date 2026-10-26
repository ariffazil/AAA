#!/usr/bin/env python3
"""Three-mode falsifier for the gate hook's KERNEL CONSULT section (2026-10-24).

Runs the hook as a subprocess with ARIFOS_GATE_URL pointed at a stub server, so
no test touches the real kernel. Asserted modes (sovereign falsifier table
2026-10-24): reject blocks, unreachable blocks (NOT a clean pass), malformed AND
structurally-partial replies block (the parser cannot fail silently into an
allow), allow passes with no stdout, OBSERVE never consults, the kill-switch
disables, and the sibling's fail-closed stdin fix still holds.
"""

import json
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

HOOK = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "federation", "protocols", "arifos-hermes-gate-hook.py"
)


class Stub(BaseHTTPRequestHandler):
    mode = "PASS"  # PASS | reject | malformed | partial
    hits = 0

    def do_GET(self):
        Stub.hits += 1
        if Stub.mode == "reject":
            body = json.dumps({"thermodynamic": {"verdict": "HOLD"}, "floors_active": 13}).encode()
        elif Stub.mode == "malformed":
            body = b"<html>not json</html>"
        elif Stub.mode == "partial":
            body = json.dumps({"status": "ok"}).encode()
        else:
            body = json.dumps({"thermodynamic": {"verdict": "PASS"}, "floors_active": 13}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):  # silence
        pass


def run_hook(payload, env_extra):
    env = dict(os.environ)
    env.update(env_extra)
    p = subprocess.run(
        [sys.executable, HOOK],
        input=json.dumps(payload).encode(),
        capture_output=True,
        env=env,
        timeout=60,
    )
    return p.returncode, p.stdout, p.stderr


MUT = {
    "tool_name": "write_file",
    "tool_input": {"path": "/tmp/gate-test-x.txt", "content": "hi"},
    "session_id": "gate-selftest-kernel",
}
OBS = {"tool_name": "read_file", "tool_input": {"path": "/tmp/gate-test-x.txt"}, "session_id": "gate-selftest-kernel"}


def main():
    srv = HTTPServer(("127.0.0.1", 0), Stub)
    port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = {"ARIFOS_GATE_URL": f"http://127.0.0.1:{port}/health", "ARIFOS_GATE_TIMEOUT_S": "5"}
    results = []

    def check(name, cond, detail=""):
        results.append(bool(cond))
        print(("PASS " if cond else "FAIL ") + name + (f" :: {detail}" if detail and not cond else ""))

    # mode (a): kernel reachable and rejecting -> BLOCK
    Stub.mode = "reject"
    Stub.hits = 0
    rc, out, _ = run_hook(MUT, base)
    check("reject blocks (exit 2, KERNEL_REJECT)", rc == 2 and b"KERNEL_REJECT" in out, f"rc={rc} out={out[:140]}")
    check("reject consulted kernel exactly once", Stub.hits == 1, f"hits={Stub.hits}")

    # mode (b): unreachable -> BLOCK (timeout is not a clean pass)
    rc, out, _ = run_hook(MUT, {**base, "ARIFOS_GATE_URL": "http://127.0.0.1:1/health", "ARIFOS_GATE_TIMEOUT_S": "2"})
    check(
        "unreachable blocks (KERNEL_UNREACHABLE)", rc == 2 and b"KERNEL_UNREACHABLE" in out, f"rc={rc} out={out[:140]}"
    )

    # mode (c1): garbage reply -> BLOCK
    Stub.mode = "malformed"
    Stub.hits = 0
    rc, out, _ = run_hook(MUT, base)
    check(
        "malformed reply blocks (KERNEL_MALFORMED)", rc == 2 and b"KERNEL_MALFORMED" in out, f"rc={rc} out={out[:140]}"
    )

    # mode (c2): structurally partial (200 + JSON, missing fields) -> BLOCK
    Stub.mode = "partial"
    rc, out, _ = run_hook(MUT, base)
    check(
        "structurally partial blocks (KERNEL_MALFORMED)",
        rc == 2 and b"KERNEL_MALFORMED" in out,
        f"rc={rc} out={out[:140]}",
    )

    # allow path: verdict PASS -> no stdout (allow convention), kernel consulted
    Stub.mode = "PASS"
    Stub.hits = 0
    t0 = time.perf_counter()
    rc, out, _ = run_hook(MUT, base)
    dt_ms = (time.perf_counter() - t0) * 1000
    check("allow passes with no stdout", rc == 0 and out.strip() == b"", f"rc={rc} out={out[:140]}")
    check("allow consulted kernel exactly once", Stub.hits == 1, f"hits={Stub.hits}")
    print(f"info: allow-path subprocess total {dt_ms:.0f} ms (includes interpreter boot)")

    # OBSERVE never consults, even when the kernel rejects
    Stub.mode = "reject"
    Stub.hits = 0
    rc, out, _ = run_hook(OBS, base)
    check("observe passthrough without consult", rc == 0 and Stub.hits == 0, f"rc={rc} hits={Stub.hits}")

    # sovereign kill-switch
    Stub.mode = "reject"
    Stub.hits = 0
    rc, out, _ = run_hook(MUT, {**base, "ARIFOS_GATE_KERNEL_CONSULT": "0"})
    check("kill-switch disables consult", rc == 0 and Stub.hits == 0, f"rc={rc} hits={Stub.hits}")

    # regression: sibling's fail-closed stdin fix still holds
    env = dict(os.environ)
    env.update(base)
    p = subprocess.run([sys.executable, HOOK], input=b"", capture_output=True, env=env, timeout=60)
    check(
        "empty stdin fail-closed (regression)",
        p.returncode == 2 and b"unparseable" in p.stdout,
        f"rc={p.returncode} out={p.stdout[:120]}",
    )

    srv.shutdown()
    failed = len(results) - sum(results)
    print(f"\n{sum(results)}/{len(results)} PASS")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
