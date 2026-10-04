# Hermes Execution Log — Batch 2 Banda Haram Hardcoded (2026-08-12)

## Context

Follow-up env-first pass on 5 Python source files under `/root/HERMES/`.
Triggered by a request to add `os.environ.get()` resolution for hardcoded
URLs, hosts, paths, and timeouts while preserving backward compatibility.

## Files Modified

| File | What | How |
|------|------|-----|
| `mcp_servers/hermes_agent_mcp.py` | 3 timeouts (60.0, 15.0, 5), health URL, A2A URL | `HERMES_AGENT_TIMEOUT`, `HERMES_MCP_INIT_TIMEOUT`, `HERMES_HEALTH_TIMEOUT`; health URL **derived** from `HERMES_A2A_URL` |
| `mcp_servers/hermes_mcp.py` | 3 × `/root/VAULT999` literals, probe timeout 3.0 | Module-level `VAULT999_PATH` constant; `HERMES_ORGAN_PROBE_TIMEOUT` |
| `cron/_probe_job.py` | `'/root/.hermes/cron/jobs.json'` literal | `os.path.join(os.environ.get("HERMES_CRON_PATH", "/root/.hermes/cron"), "jobs.json")` |
| `skills/FORGE-google-workspace/drive_helpers.py` | `google_token.json` + `google_client_secret.json` paths | `HERMES_HOME` constant + `os.path.join` for both |
| `mcp_servers/hermes_real_bridge.py` | `host="127.0.0.1"`, `timeout=30` | `HERMES_REAL_BRIDGE_HOST`, `HERMES_SEND_TIMEOUT` |

## Pre-existing Corruption Discovered (Bonus Fix)

`mcp_servers/hermes_agent_mcp.py` line 30 contained a syntactically broken
default — a nested `os.environ.get(...)` *inside* the default string of another
`os.environ.get(...)`:

```python
# BROKEN — does not parse as Python
HERMES_A2A_URL = os.environ.get("HERMES_A2A_URL", "os.environ.get("HERMES_AGENT_ENDPOINT", "http://127.0.0.1:18089")/a2a")
```

Likely cause: a previous env-first patch was applied with mismatched quoting.
The file would have failed `py_compile` from that moment. Confirmed by
`git show HEAD:mcp_servers/hermes_agent_mcp.py | sed -n '30p'`.

**Lesson:** When finding suspicious-looking hardcoded values during a refactor,
**always cross-check against git history** (`git log -p` or `git show HEAD:file`)
to distinguish "intent we forgot to extract" from "corruption from a botched
edit". The fix is to recover the original *intent* — not to extend the
corruption pattern.

```bash
# Quick check
git show HEAD:path/to/file | grep -n "pattern" | head -5
```

## New Patterns Discovered This Pass

### 1. URL Derivation — Single Source of Truth

For files that talk to a service on two endpoints (A2A + health), derive the
secondary URL from the primary, not from a separate env var:

```python
# WRONG: two env vars that can disagree
HERMES_A2A_URL = os.environ.get("HERMES_A2A_URL", "http://127.0.0.1:18089/a2a")
# ...later...
client.get(f"{os.environ.get('HERMES_AGENT_ENDPOINT', 'http://127.0.0.1:18089')}/health", ...)

# RIGHT: derive the health URL from the A2A URL
HERMES_A2A_URL = os.environ.get("HERMES_A2A_URL", "http://127.0.0.1:18089/a2a")
# ...later...
client.get(f"{HERMES_A2A_URL.rsplit('/a2a', 1)[0]}/health", ...)
```

Set `HERMES_A2A_URL` once and both endpoints follow. No drift possible.

### 2. Path-Env with `os.path.join` for Files in a Configurable HOME

For tools that read multiple files inside a home directory, hoist the
home to a single env var and join:

```python
HERMES_HOME = os.environ.get("HERMES_HOME", "/root/HERMES")
TOKEN_FILE  = os.path.join(HERMES_HOME, "google_token.json")
CLIENT_FILE = os.path.join(HERMES_HOME, "google_client_secret.json")
```

Avoids two separate `os.environ.get()` calls for paths that share a parent.
Honors `os.path.join` semantics (no double slashes, trailing slash safety).

### 3. Module-Level Constant for Repeated Defaults

When the same fallback appears 3+ times in one file (e.g. `"/root/VAULT999"`),
define it ONCE at module top and reference the constant:

```python
# top of file
VAULT999_PATH = os.environ.get("VAULT999_PATH", "/root/VAULT999")

# later — use the constant, not the literal
vault_dir = VAULT999_PATH
```

Cleaner than three independent `os.environ.get()` calls; one override point
in tests; one grep target for audits.

### 4. Verify Path Before Patching

Task description said files were at `scripts/cron/_probe_job.py` and
`scripts/hermes_real_bridge.py`. Actual locations:
- `/root/HERMES/cron/_probe_job.py`
- `/root/HERMES/mcp_servers/hermes_real_bridge.py`

Always `search_files()` for the file before assuming the task-spec path is
correct. Saves a "file not found" round-trip.

### 5. `float()` Cast Pattern for Default String

`os.environ.get()` always returns `str`. For numeric consumers (`timeout`,
`port`), cast explicitly with the type the consumer expects:

```python
timeout=float(os.environ.get("HERMES_AGENT_TIMEOUT", "60.0"))   # httpx-style
port=int(os.environ.get("HERMES_BRIDGE_PORT", "18091"))         # subprocess-style
```

For `httpx.Client(timeout=...)` — accept `float`.
For `subprocess.run(timeout=...)` — accept `int`.

## Verification Approach

Since no canonical test/lint/build command was detected, ran an ad-hoc
5-stage verification under `/tmp/hermes-verify-patches.py` (cleaned after):

1. `py_compile` on all 5 files
2. Source grep for expected env-var keys
3. Default values match original hardcoded values (substring search)
4. No stale bare hardcoded literals remain (regex sweep)
5. Clean subprocess: defaults + override behavior

**Caveat:** Static + subprocess verification only. No live probe (services
not running). Document this honestly — see `references/verify-script-batch2.py`
for the canonical template to copy.

## Related References
- `references/hermes-execution-2026-08-12.md` — first batch (this is batch 2)
- `references/audit-recipe-2026-08-12.md` — OpenCode scan procedure
- `references/verify-script-batch2.py` — ad-hoc verification script template