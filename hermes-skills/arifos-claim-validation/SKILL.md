---
name: arifos-claim-validation
category: governance
description: Validate external AI claims about arifOS against PyPI ground truth — package contents, versions, CLI entrypoints, and class existence. Use when external agents claim things about arifOS PyPI packages or product features.
---

# arifOS External Claim Validation

## When to use
When an external AI or agent makes claims about arifOS architecture, capabilities, or products — especially citing PyPI packages, CLI interfaces, or specific class/method names. Validate against ground truth via live inspection, not assumptions.

## Trigger conditions
Any external claim about:
- `pip install arifos` or `arifosmcp` package contents
- CLI entrypoints (`arifos`, `arifos-mcp`, `aaa-mcp`, `aclip-cai`)
- Python classes (`AuthorityGate`, `Kernel`, `RiskClassifier`, etc.)
- Version numbers or PyPI upload dates
- arifOS product thesis (pip install as governance kernel)

## Step-by-step method

### Step 1 — PyPI JSON API (fastest ground truth)
```bash
curl -sL "https://pypi.org/pypi/{PACKAGE}/json" -H "User-Agent: arifOS/1.0" | python3 -c "
import sys, json
d = json.load(sys.stdin)
info = d['info']
print('Name:', info['name'])
print('Version:', info['version'])
print('Summary:', info['summary'])
print('Files:', [f['filename'] for f in d['urls']])
print('Upload time:', [f['upload_time'] for f in d['urls']])
"
```

### Step 2 — Download and inspect wheel contents
```bash
pip download {PACKAGE}=={VERSION} --no-deps -d /tmp/{pkg} 2>/dev/null
unzip -l /tmp/{pkg}/*.whl   # list all files in wheel
```

### Step 3 — Extract and read specific files
```bash
mkdir -p /tmp/{pkg}_extract
unzip -o /tmp/{pkg}/*.whl -d /tmp/{pkg}_extract/
cat /tmp/{pkg}_extract/path/to/file.py   # read specific module
```

### Step 4 — Check CLI entrypoints
```bash
which {CLI_NAME}
{CLI_NAME} --help
# Also check entry_points.txt inside wheel:
unzip -p /tmp/{pkg}/*.whl '*.dist-info/entry_points.txt'
```

### Step 5 — Compare with live VPS/installed version
```bash
pip show {PACKAGE}    # shows installed version + location
pip show arifos      # specific check for arifos kernel package
```

### Step 6 — Cross-reference git source
Search `/root/arifOS/` for matching class names or version strings to confirm source alignment.

## Key ground-truth findings from this session

| Claim tested | Ground truth |
|-------------|-------------|
| `pip install arifos` | EXISTS — arifos v2026.5.4 on PyPI, uploaded 2026-05-04 |
| `AuthorityGate` class | IN WHEEL — `core/authority_gate.py` with exact `verify()` method |
| `AuthorityProof` model | EXACT MATCH — `{authorized, requires_human, witness_type, plan_approved, reason}` |
| `Kernel.preflight()` | NOT IN WHEEL — conceptual API, not yet built |
| `RiskClass.C0-C5` | NOT IN WHEEL — schema atoms exist, tier table missing |
| VPS installed version | OLD — VPS has 0.1.1 (editable), PyPI has 2026.5.4 |
| CLI aliases | `arifos`, `arifos-mcp`, `aaa-mcp`, `aclip-cai` confirmed in entry_points.txt |

## Critical lesson
PyPI version can be AHEAD of VPS installed version. Always check both `pip show` and PyPI JSON API. An external AI can correctly reason about arifOS from first principles even without internal source access — the gap between PyPI kernel and described product API reveals the actual feature roadmap.

## Pitfalls
- Don't trust `pip show` alone — it only shows the installed version, not PyPI latest
- Don't trust external agent claims about package contents without wheel inspection
- Wheel `entry_points.txt` is the canonical source of truth for CLI aliases
