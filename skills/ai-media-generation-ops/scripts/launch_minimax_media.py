#!/usr/bin/env python3
"""
Idempotent MiniMax Media MCP launcher for port 18100.
Run once per session/reboot. Checks port first — starts only if unbound.
Also ensures run_v2.py exists (regenerated from known-good if deleted).

Usage:
    python3 scripts/launch_minimax_media.py
    # exit 0 + prints "ALIVE on :18100" on success
    # exit 1 if already running on 18090 (not our port) or failed to start
"""
import os, sys, socket, time, subprocess, json

PORT = 18100
SCRIPT = "/opt/minimax-mcp-media/run_v2.py"
PYTHON = "/opt/minimax-mcp-media/venv/bin/python3"
WORKDIR = "/opt/minimax-mcp-media"

def port_alive(p):
    try:
        s = socket.create_connection(("127.0.0.1", p), timeout=1)
        s.close(); return True
    except: return False

def ensure_run_v2():
    if os.path.exists(SCRIPT): return
    with open(SCRIPT, "w") as f:
        f.write("""#!/usr/bin/env python3
import os, sys
os.chdir("/opt/minimax-mcp-media")
for k in ("FASTMCP_HOST","FASTMCP_PORT"): os.environ.pop(k,None)
os.environ["FASTMCP_HOST"]="127.0.0.1"; os.environ["FASTMCP_PORT"]="18100"
from dotenv import load_dotenv; load_dotenv("/opt/minimax-mcp-media/.env", override=True)
os.environ["FASTMCP_PORT"]="18100"
from minimax_mcp.server import mcp
mcp.settings.host="127.0.0.1"; mcp.settings.port=18100
print("[minimax-media-v2] Streamable HTTP on 127.0.0.1:18100/mcp",file=sys.stderr)
mcp.run(transport="streamable-http")
""")
    print(f"[launch] Created {SCRIPT}")

if port_alive(PORT):
    print(f"ALREADY ALIVE on :{PORT}")
    sys.exit(0)

ensure_run_v2()

if not os.path.exists(PYTHON):
    print(f"ERROR: python venv not found at {PYTHON}"); sys.exit(1)

print(f"[launch] Starting MiniMax Media MCP on :{PORT}...")
log = open("/tmp/minimax-media.log", "wb")
proc = subprocess.Popen([PYTHON, SCRIPT], env=os.environ.copy(),
                        cwd=WORKDIR, stdout=log, stderr=log)

for i in range(40):
    time.sleep(0.5)
    if port_alive(PORT):
        print(f"ALIVE on :{PORT} after {i*0.5:.1f}s  PID={proc.pid}")
        sys.exit(0)

print(f"FAILED to bind :{PORT} in 20s. Check /tmp/minimax-media.log")
sys.exit(1)
