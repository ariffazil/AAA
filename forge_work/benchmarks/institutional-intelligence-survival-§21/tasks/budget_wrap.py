#!/usr/bin/env python3
"""S21 budget wrapper — identical token + wall-clock budget per cohort run (anti-bangang rule 4).
Kills at wall-clock; estimates tokens as ceil(chars/4) of combined output unless --tokens-reported.
Emits budget receipt JSON. Usage: budget_wrap.py --wall-clock 900 --tokens 200000 -- <cmd...>"""
import argparse, json, math, subprocess, sys, time, datetime

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wall-clock", type=int, default=900)
    ap.add_argument("--tokens", type=int, default=200000)
    ap.add_argument("--tokens-reported", type=int, default=-1)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    t0 = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=a.wall_clock)
        rc, out = r.returncode, r.stdout + r.stderr
        killed = False
    except subprocess.TimeoutExpired as e:
        rc, out, killed = 124, (e.stdout or "") + (e.stderr or ""), True
    wall = round(time.time() - t0, 2)
    tokens = a.tokens_reported if a.tokens_reported >= 0 else math.ceil(len(out) / 4)
    over = wall > a.wall_clock or tokens > a.tokens
    receipt = {"cmd": cmd, "wall_clock_s": wall, "wall_budget_s": a.wall_clock,
               "tokens_est": tokens, "token_budget": a.tokens,
               "killed_at_wall": killed, "budget_exceeded": over,
               "verdict": "OVER_BUDGET" if over else "WITHIN_BUDGET",
               "recorded_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    print(json.dumps(receipt, indent=1))
    return 0 if (rc == 0 and not over) else 1

if __name__ == "__main__":
    sys.exit(main())
