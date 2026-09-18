#!/usr/bin/env python3
"""
LOUD RUNNER for the RASA/SHADOW gate test suites.

Why this exists (2026-09-16, F13 session):
  `.hermes/policy/test_rasa_bench_10.py` is a 355-line assert-only suite. Run directly it emits
  ZERO bytes and exits 0. A suite that cannot be seen to fail is the *metric-gaming* demon
  named in the angel/demon register, caught at birth: "tests pass" with no verdict, no count,
  no visible assertion inventory. This wrapper makes the outcome observable without touching the
  suite itself (concurrency-safe: another session owns that file).

It reports, per suite: assertions found, pass/fail, the first failure verbatim, and whether the
suite printed anything at all. Silence is now itself a reported condition.
"""
import subprocess, sys, re, os

SUITES = [
    ("gate-bench-10 (concurrent session)", "/root/.hermes/policy/test_rasa_bench_10.py"),
    ("rasa-benchmark (this session)",      "/root/AAA/instructions/rasa-benchmark.py"),
]

def run(name, path):
    print(f"\n{'='*78}\n{name}\n{'='*78}")
    if not os.path.exists(path):
        print(f"  MISSING: {path}"); return False, 0, 0
    src = open(path, encoding="utf-8", errors="replace").read()
    asserts = len(re.findall(r'^\s*assert\b', src, re.M))
    p = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=180,
                       cwd=os.path.dirname(path))
    out, err = p.stdout.strip(), p.stderr.strip()
    print(f"  assertions found : {asserts}")
    print(f"  stdout bytes     : {len(out)}")
    print(f"  exit code        : {p.returncode}")
    if out:
        tail = out.splitlines()
        print("  verdict lines    :")
        for l in tail[-6:]:
            print(f"     {l[:118]}")
    else:
        print("  ⚠ SILENT SUITE — passes with no observable verdict. Reported, not hidden.")
    if p.returncode != 0:
        first = [l for l in err.splitlines() if l.startswith(("AssertionError", "  File", "E  "))][:4]
        print("  FAILURE:")
        for l in first or err.splitlines()[-6:]:
            print(f"     {l[:118]}")
    return p.returncode == 0, asserts, len(out)

ok_all = True; tot_a = 0; silent = 0
for n, p in SUITES:
    ok, a, nbytes = run(n, p)
    ok_all &= ok; tot_a += a
    if a and not nbytes: silent += 1

print(f"\n{'='*78}")
print(f"SUITES {'ALL GREEN' if ok_all else 'HAS FAILURES'} · assertions {tot_a} · silent suites {silent}")
print("="*78)
if silent:
    print("""
A green suite with zero output is not evidence the gate works. It is evidence nobody can see
whether it works. Kill-criterion §47 requires a *counted* enforcement event; a silent pass
produces none, so it would trigger the 90-day kill while looking healthy. Report silence loudly.
""")
sys.exit(0 if ok_all else 1)
