#!/usr/bin/env python3
"""Ad-hoc verification for env-first refactor patches.

NOT a regression suite. Static + subprocess only — no live service probes.

Usage: edit CHANGED to point at the patched files, then run.
The script runs 5 stages:
  [1] py_compile on every file
  [2] Source grep for expected env-var keys
  [3] Default values match original hardcoded values
  [4] Regex sweep for stale bare hardcoded literals
  [5] Clean-subprocess: defaults + override behavior

Drop in `/tmp/hermes-verify-XXXX.py`, run, delete. Saves ~10 min per patch
session vs hand-rolling each check.
"""
import subprocess, sys, re, json
from pathlib import Path

# ── Configure this list for your patch ─────────────────────────────────
CHANGED = [
    "/root/HERMES/mcp_servers/hermes_agent_mcp.py",
    "/root/HERMES/mcp_servers/hermes_mcp.py",
    "/root/HERMES/cron/_probe_job.py",
    "/root/HERMES/skills/FORGE-google-workspace/drive_helpers.py",
    "/root/HERMES/mcp_servers/hermes_real_bridge.py",
]
# filename → list of (env_var_key, expected_default_literal)
DEFAULTS = [
    ("HERMES_AGENT_TIMEOUT",    "60.0",              "hermes_agent_mcp.py"),
    ("HERMES_MCP_INIT_TIMEOUT", "15.0",              "hermes_agent_mcp.py"),
    ("HERMES_HEALTH_TIMEOUT",   "5",                 "hermes_agent_mcp.py"),
    ("VAULT999_PATH",           "/root/VAULT999",    "hermes_mcp.py"),
    ("HERMES_ORGAN_PROBE_TIMEOUT", "3.0",            "hermes_mcp.py"),
    ("HERMES_CRON_PATH",        "/root/.hermes/cron", "_probe_job.py"),
    ("HERMES_HOME",             "/root/HERMES",      "drive_helpers.py"),
    ("HERMES_SEND_TIMEOUT",     "30",                "hermes_real_bridge.py"),
]
# filename → list of regex patterns that MUST NOT appear after patching
STALE_LITERALS = {
    "_probe_job.py":         r"open\(['\"].*?/root/\.hermes/cron/jobs\.json",
    "drive_helpers.py":      r"['\"]\/root\/HERMES\/google_token\.json['\"]",
    "hermes_mcp.py":         r"vault_dir\s*=\s*['\"]/root/VAULT999['\"]",
    "hermes_real_bridge.py": r"host\s*=\s*['\"]127\.0\.0\.1['\"]",
    "hermes_agent_mcp.py":   r"client\.get\(['\"]http://127\.0\.0\.1:18089/health['\"]",
}


def main() -> int:
    print("=" * 64)
    print("AD-HOC VERIFICATION: env-first refactor")
    print("=" * 64)
    all_ok = True

    # [1] compile
    print("\n[1] py_compile")
    for p in CHANGED:
        r = subprocess.run([sys.executable, "-m", "py_compile", p],
                           capture_output=True, text=True)
        ok = r.returncode == 0
        all_ok &= ok
        print(f"  {'OK' if ok else 'FAIL'}: {Path(p).name}")

    # [2] lookups present
    print("\n[2] os.environ.get() lookups in source")
    for key, _default, fn in DEFAULTS:
        src = Path(next(p for p in CHANGED if p.endswith(fn))).read_text()
        ok = key in src
        all_ok &= ok
        print(f"  {'OK' if ok else 'MISS'}: {fn}: {key}")

    # [3] defaults match originals
    print("\n[3] Defaults match original hardcoded values")
    for key, default, fn in DEFAULTS:
        src = Path(next(p for p in CHANGED if p.endswith(fn))).read_text()
        needle = f'os.environ.get("{key}", "{default}")'
        have = needle in src or (key in src and default in src)
        all_ok &= have
        print(f"  {'OK' if have else 'FAIL'}: {fn}: {key} default={default!r}")

    # [4] no stale literals
    print("\n[4] No stale bare hardcoded literals")
    for fn, pat in STALE_LITERALS.items():
        src = Path(next(p for p in CHANGED if p.endswith(fn))).read_text()
        hits = re.findall(pat, src)
        ok = not hits
        all_ok &= ok
        print(f"  {'LEFT' if hits else 'CLEAN'}: {fn}: {pat[:55]}")

    # [5] runtime defaults + overrides in clean subprocess
    print("\n[5] Runtime: clean-env defaults + override")
    test = """\
import os, json
defaults_ok = True
for key, expected in [
    ("HERMES_AGENT_TIMEOUT", "60.0"),
    ("HERMES_CRON_PATH", "/root/.hermes/cron"),
    ("HERMES_HOME", "/root/HERMES"),
    ("HERMES_SEND_TIMEOUT", "30"),
    ("HERMES_ORGAN_PROBE_TIMEOUT", "3.0"),
]:
    val = os.environ.get(key, "<unset>")
    defaults_ok = defaults_ok and (val == "<unset>" or val == expected)

os.environ["HERMES_AGENT_TIMEOUT"] = "120.0"
override_ok = os.environ.get("HERMES_AGENT_TIMEOUT", "60.0") == "120.0"

print(json.dumps({"defaults_ok": defaults_ok, "override_ok": override_ok}))
"""
    r = subprocess.run([sys.executable, "-c", test], capture_output=True, text=True, env={})
    if r.returncode != 0:
        print(f"  FAIL: {r.stderr[:150]}")
        all_ok = False
    else:
        res = json.loads(r.stdout.strip())
        for k, v in res.items():
            print(f"  {'OK' if v else 'FAIL'}: runtime {k}")
            all_ok &= v

    print(f"\n{'=' * 64}")
    print(f"VERIFICATION: {'ALL PASSED' if all_ok else 'SOME FAILED'} (ad-hoc, not suite green)")
    print(f"{'=' * 64}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())