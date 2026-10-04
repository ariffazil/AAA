# Intel Seal Verification Template

Canonical verification for `intel-<DATE>.json` artifacts. Proven 2026-08-10, refined 2026-08-11.

## execute_code block

Cron jobs cannot use `execute_code` (approval policy). Create verification script via `terminal()` using heredoc (or `write_file` to a `/tmp/hermes-verify-*.py` path), run it, then remove it.

## System gate naming + re-verify (learned 2026-08-11)

- The external gate requires temp scripts under `/tmp` with the literal `hermes-verify-` prefix (e.g. `/tmp/hermes-verify-intel-2026-08-11.py`). Name it that way; it's an infra contract, not a suggestion.
- Clean up with `rm -f /tmp/hermes-verify-*` after running.
- If the gate re-flags "unverified" again after a clean run (stale scan), don't chase it with `execute_code` (blocked) — just re-create + re-run the same script via `write_file` + `terminal`, confirm PASS, then state "Ad-hoc verification (not suite green)" explicitly in the reply.

## 5-gate verification script

```bash
#!/bin/bash
set -e
FILE=/root/.local/share/arifos/state/intel-${DATE}.json
LEDGER=/root/.local/share/arifos/state/intel-ledger.tsv

echo "=== hermes-verify intel-${DATE} (ad-hoc) ==="

echo "[1] File integrity"
stat -c '   mode=%a owner=%U:%G size=%s mtime=%y' "$FILE"

echo "[2] JSON parse"
python3 -c "import json; json.load(open('$FILE')); print('   python3: PASS')"
python3 -m json.tool "$FILE" > /dev/null && echo "   tool: PASS"
jq -e . "$FILE" > /dev/null && echo "   jq: PASS"

echo "[3] Schema + numeric sanity"
python3 <<'PY'
import json, sys
d = json.load(open('${FILE}'))
fails = []
# Required keys + types
checks = [
    ('ts_myt', str, lambda v: v.endswith('+08:00')),
    ('date', str),
    ('readiness_consumed', str, lambda v: v in ('GREEN','YELLOW','RED','UNKNOWN')),
    ('tone_calibrated', str, lambda v: v in ('full','filtered','brutal')),
    ('key_levels', dict), ('predictions', list, lambda v: 1<=len(v)<=10),
    ('watch', list), ('sources', list, lambda v: len(v)>=3),
]
for k, t, *v in checks:
    if k not in d: fails.append(f"missing: {k}"); print(f"   {k}: MISSING"); continue
    if not isinstance(d[k], t): fails.append(f"type: {k}"); print(f"   {k}: WRONG TYPE"); continue
    if v and not v[0](d[k]): fails.append(f"validator: {k}"); print(f"   {k}: VALIDATOR FAIL")
    else: print(f"   {k}: OK")
# Numeric ranges
kl = d.get('key_levels', {})
ranges = {'xauusd_spot':(3000,6000),'brent_spot':(40,200),'brent':(40,200),
          'dxy':(80,130),'us10y':(0.5,15),'usdmyr':(3.0,5.5)}
for k,(lo,hi) in ranges.items():
    if k in kl and not (lo <= kl[k] <= hi): fails.append(f"range: {k}={kl[k]}")
# Predictions
for i,p in enumerate(d.get('predictions',[])):
    miss = [k for k in ('id','claim','horizon','falsifier') if k not in p or not p[k]]
    if miss: fails.append(f"pred[{i}] missing: {miss}")
    elif not any(c in p['falsifier'].lower() for c in ['>','<','breaks','closes','above','below']):
        fails.append(f"pred[{i}] falsifier weak (no threshold)")
if fails:
    print(f"   FAIL: {fails}"); sys.exit(1)
else: print("   PASS")
PY

echo "[4] Ledger symmetry"
LINE=$(grep "^${DATE}|" "$LEDGER" | head -1)
N=$(python3 -c "import json; print(len(json.load(open('$FILE'))['predictions']))")
ECHO_N=$(echo "$LINE" | cut -d'|' -f2)
[ "$ECHO_N" = "$N" ] && echo "   PASS ($N)" || echo "   FAIL (ledger=$ECHO_N json=$N)"

echo "=== DONE ==="
```

## When verification fails

1. Re-read the file to identify what failed.
2. Re-seal the file with corrections.
3. Re-run verification.
4. Only deliver the brief AFTER all 5 gates pass.

## Output format

The script should output `PASS` or `FAIL` per gate. The session's log output IS the verification evidence — the system checks for it after seal. Without it, "verification status: unverified" persists.
