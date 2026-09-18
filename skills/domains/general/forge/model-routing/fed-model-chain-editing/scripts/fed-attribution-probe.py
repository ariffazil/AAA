#!/usr/bin/env python3
"""
fed-attribution-probe.py — lane attribution receipt for FED (LiteLLM).

WHY: the router's own response headers are the only attribution instrument when
`general_settings.disable_spend_logs` is True (LiteLLM_SpendLogs then has no coverage).
This sweeps the live lanes and records, per lane, which deployment actually served and
whether the chain fell through.

Read-only. No mutations. Writes one JSON snapshot per run to /root/forge_work/fed-attribution/.

State machine (never collapse to PASS/FAIL — state-transition discipline):
    SERVED_ON_PRIMARY   http 200, served named, retries=0 and fallbacks=0
    SERVED_OFF_PRIMARY  http 200 but retries>0 or fallbacks>0 — report WHICH rung is dead
    UNATTRIBUTED        http 200 with no x-litellm-model-name header
    ROUTER_ERROR        non-200
    TIMEOUT             no response inside the window

Requires LITELLM_MASTER_KEY in the environment. The 5-R vars are normally already
exported in the session env; do NOT inline a path into the credential store on the command
line, because the T3 gate refuses the whole call when it sees one.

Usage:
    python3 fed-attribution-probe.py --port 4013
    python3 fed-attribution-probe.py --lanes i-arif,agi-333 --port 4013
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("/root/forge_work/fed-attribution")

DEFAULT_LANES = [
    "i-arif", "agi-333", "asi-555", "apex-888", "forge-777",
    "forge-scout", "forge-scout-pro", "forge-builder", "forge-economy",
    "forge-planner", "forge-judge", "openclaw", "hermes-asi",
    "hermes-asi-vision", "fed/vision", "fed/sealion",
    "fed/audio-asr", "fed/audio-tts",
]


def probe(port, lane, key, timeout=45):
    """One nonce'd request; attribution read from response headers only."""
    nonce = f"attrib-{os.getpid()}-{time.time_ns()}"
    body = json.dumps({
        "model": lane,
        "messages": [{"role": "user", "content": f"{nonce} reply with the single word OK"}],
        "max_tokens": 5,
    })
    cmd = [
        "curl", "-s", "-D", "-", "-o", "/dev/null", "--max-time", str(timeout),
        f"http://127.0.0.1:{port}/v1/chat/completions",
        "-H", f"Authorization: Bearer {key}",
        "-H", "Content-Type: application/json",
        "-d", body,
    ]
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        hdr = p.stdout or ""
    except subprocess.TimeoutExpired:
        return {"lane": lane, "state": "TIMEOUT", "latency_s": round(time.time() - t0, 2)}

    def get(name):
        m = re.search(rf"^{name}:\s*(.+)$", hdr, re.I | re.M)
        return m.group(1).strip() if m else None

    http = None
    m = re.search(r"^HTTP/[\d.]+ (\d+)", hdr, re.M)
    if m:
        http = int(m.group(1))

    served = get("x-litellm-model-name")
    retries = get("x-litellm-attempted-retries")
    fbks = get("x-litellm-attempted-fallbacks")

    if http != 200:
        state = "ROUTER_ERROR"
    elif served is None:
        state = "UNATTRIBUTED"
    elif retries not in (None, "0") or fbks not in (None, "0"):
        state = "SERVED_OFF_PRIMARY"
    else:
        state = "SERVED_ON_PRIMARY"

    return {
        "lane": lane, "http": http, "state": state, "served_model": served,
        "attempted_retries": retries, "attempted_fallbacks": fbks,
        "latency_s": round(time.time() - t0, 2), "nonce": nonce,
    }


def declared_primary(cfg_path, lane):
    """First rung by `order:` in the lane body, or None for alias-only lanes."""
    try:
        import yaml
    except ImportError:
        return None
    cfg = yaml.safe_load(Path(cfg_path).read_text()) or {}
    best = None
    for e in cfg.get("model_list", []) or []:
        if str(e.get("model_name")) != lane:
            continue
        o = e.get("order", 0)
        if best is None or o < best[0]:
            best = (o, e.get("model"))
    return best[1] if best else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=4013)
    ap.add_argument("--config", default="/root/A-FORGE/litellm-config.yaml")
    ap.add_argument("--lanes", default=None, help="comma-separated; default = live lane set")
    args = ap.parse_args()

    key = os.environ.get("LITELLM_MASTER_KEY")
    if not key:
        print("REFUSED: LITELLM_MASTER_KEY not in env", file=sys.stderr)
        sys.exit(2)

    lanes = args.lanes.split(",") if args.lanes else DEFAULT_LANES
    rows = []
    for lane in lanes:
        r = probe(args.port, lane, key)
        r["declared_primary"] = declared_primary(args.config, lane)
        rows.append(r)
        flag = {"SERVED_ON_PRIMARY": "  ok ", "SERVED_OFF_PRIMARY": " <!> ",
                "UNATTRIBUTED": " ?? ", "ROUTER_ERROR": " XX ",
                "TIMEOUT": " TT "}.get(r["state"], "  ? ")
        print(f"{flag}{lane:20s} {r['state']:20s} served={r.get('served_model')} "
              f"retries={r.get('attempted_retries')} fallbacks={r.get('attempted_fallbacks')} "
              f"{r.get('latency_s')}s")

    off = [r for r in rows if r["state"] != "SERVED_ON_PRIMARY"]
    summary = {
        "schema": "fed.attribution.receipt.v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "router_port": args.port,
        "config": args.config,
        "lanes_probed": len(rows),
        "lanes_on_primary": len(rows) - len(off),
        "lanes_off_primary": len(off),
        "off_primary": [r["lane"] for r in off],
        "caveat": ("Snapshot attribution only — NOT marginal value. Per-rung marginal value needs a "
                   "temporal ledger; if general_settings.disable_spend_logs is True there is none."),
        "rows": rows,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fp = OUT / f"attribution-{stamp}.json"
    fp.write_text(json.dumps(summary, indent=2))
    (OUT / "latest.json").write_text(json.dumps(summary, indent=2))
    print(f"\n{len(off)}/{len(rows)} lanes OFF-PRIMARY: "
          f"{', '.join(summary['off_primary']) or 'none'}")
    print(f"receipt: {fp}")


if __name__ == "__main__":
    main()
