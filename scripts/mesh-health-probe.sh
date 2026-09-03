#!/bin/bash
# mesh-health-probe.sh — FI mesh harness-health sentinel
# Forged 2026-09-04 FI-008 under F13 "do 5" directive. Doctrine: fi-mesh-check skill.
#   PASS      = marker echoed (cognition confirmed)
#   EXTERNAL  = billing/quota wall (402/429) — sovereign/money class, NOT a mesh defect
#   FAIL      = mesh defect (config drift, auth, middleware)
#   DOWN      = binary missing
# Writes /run/arifos/mesh-health.json (SOT). On NEW down-transition appends ONE
# dated line to /root/AAA/terminal/holds.txt (deleted on resolution — that file's law).
# Zero spam: state transitions only. Cost: ~7 tiny sessions/day.

set -u
OUT="/run/arifos/mesh-health.json"
HOLDS="/root/AAA/terminal/holds.txt"
STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
TMP="$(mktemp)"; trap 'rm -f "$TMP"' EXIT

probe() { # name marker cmd...
  local name="$1" marker="$2"; shift 2
  local t0=$(date +%s) out="" rc=0
  if ! command -v "$1" >/dev/null 2>&1; then echo "$name|DOWN|0|binary missing" >> "$TMP"; return; fi
  out=$(timeout 90 "$@" 2>&1); rc=$?
  local lat=$(( $(date +%s) - t0 ))
  local low=$(echo "$out" | tail -40 | tr '[:upper:]' '[:lower:]')
  if echo "$out" | grep -q "$marker"; then
    echo "$name|PASS|$lat|" >> "$TMP"
  elif echo "$low" | grep -qE "payment required|balance exhausted|credits are depleted|resource_exhausted|quota"; then
    echo "$name|EXTERNAL|$lat|billing/quota wall" >> "$TMP"
  elif [ $rc -eq 124 ]; then
    echo "$name|FAIL|$lat|timeout 90s" >> "$TMP"
  elif echo "$low" | grep -qE "unrecognized_model|unrecognized model|not running in a trusted|skip-git-repo|invalid api key|unauthorized|401|forbidden"; then
    echo "$name|FAIL|$lat|config/auth drift: $(echo "$out" | tail -2 | head -c 90 | tr '\n' ' ')" >> "$TMP"
  else
    echo "$name|FAIL|$lat|no marker, rc=$rc: $(echo "$out" | tail -2 | head -c 90 | tr '\n' ' ')" >> "$TMP"
  fi
}

M="Reply with exactly:"
probe qwen     "QWEN-MESH-OK"     qwen -p "$M QWEN-MESH-OK"
probe kimi     "KIMI-MESH-OK"     kimi -p "$M KIMI-MESH-OK"
probe opencode "OPENCODE-MESH-OK" opencode run "$M OPENCODE-MESH-OK"
probe codex    "CODEX-MESH-OK"    codex exec --skip-git-repo-check "$M CODEX-MESH-OK"
probe claude   "CLAUDE-MESH-OK"   claude -p "$M CLAUDE-MESH-OK" --max-turns 2
probe grok     "GROK-MESH-OK"     grok -p "$M GROK-MESH-OK"
probe gemini   "GEMINI-MESH-OK"   env GEMINI_CLI_TRUST_WORKSPACE=true gemini -p "$M GEMINI-MESH-OK"

# ---- state assembly + transition detection ----
python3 - "$TMP" "$OUT" "$HOLDS" "$STAMP" <<'PY'
import json, os, sys
tmp, out, holds, stamp = sys.argv[1:5]
rows, cur = [], {}
for line in open(tmp):
    n, s, lat, note = (line.rstrip("\n").split("|") + [""])[:4]
    cur[n] = {"state": s, "latency_s": int(lat), "note": note}
prev = {}
if os.path.exists(out):
    try: prev = {k: v.get("state") for k, v in json.load(open(out)).get("harnesses", {}).items()}
    except Exception: pass
blob = {"schema": "arifos.mesh-health.v1", "generated_at_utc": stamp,
        "doctrine": "fi-mesh-check (EXTERNAL != FAIL)", "harnesses": cur,
        "summary": {s: sum(1 for v in cur.values() if v["state"] == s)
                    for s in ("PASS", "EXTERNAL", "FAIL", "DOWN")}}
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(blob, open(out, "w"), indent=1)
# transition -> ONE holds line per newly-dead harness (holds.txt law: delete when resolved)
new_lines = []
for n, v in cur.items():
    was, now_ = prev.get(n), v["state"]
    if now_ in ("EXTERNAL", "FAIL", "DOWN") and was not in ("EXTERNAL", "FAIL", "DOWN", None):
        new_lines.append(f"MESH: {n} {now_} since {stamp[:10]} ({v['note'] or 'see /run/arifos/mesh-health.json'})")
if new_lines and os.path.exists(holds):
    with open(holds, "a") as f:
        for l in new_lines: f.write(l + "\n")
print(json.dumps(blob["summary"]))
for l in new_lines: print("HOLD+", l)
PY
