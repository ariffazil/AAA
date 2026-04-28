---
name: arifos-mcp-red-team
description: Red-team and debug a live arifOS MCP server — trace handler chains, find resolve_alias bugs, verify tool output
tags: [arifOS, MCP, debug, docker, red-team]
created: 2026-04-25
---

# arifOS MCP Tool Red-Team Methodology

## When to Use

When arifOS MCP tools return errors, empty responses, or undefined behavior. Use before trusting tool output. This skill covers the multi-layer FastMCP architecture and the specific bug patterns found in the arifOS codebase.

## Core Methodology

### Step 1 — Probe the MCP Endpoint

```bash
# Test tools/list
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Test /health
curl -s http://localhost:8080/health

# Test individual tool calls
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":99,
       "params":{"name":"TOOL_NAME",
       "arguments":{"req":{"mode":"test"}}}}'
```

If all return empty → endpoint not responding. Check container health first.

### Step 2 — Read Benchmark Report Inside Container

```bash
docker exec arifosmcp cat /usr/src/app/arifosmcp/BENCHMARK_REPORT.md
```

This gives VERDICT per tool (SEAL/VOID/SABAR) and specific error messages. **Always check this first** — it's the internal test results showing exactly which tools fail and why.

### Step 3 — Trace the Handler Chain

The arifOS MCP server has a multi-layer handler system:

| Layer | File | Role |
|-------|------|------|
| 1 | `unified_server.py` | FastMCP decorator registration, imports `agents_66` |
| 2 | `agents_66.py` | Creates FastMCP with 66 agents (P/T/V/G/E/M axes) |
| 3 | `tools_canonical.py` | Canonical implementations + `resolve_alias()` |
| 4 | `tool_specs.py` | `normalize_tool_name()` |

Key grep commands:
```bash
docker exec arifosmcp grep -n "resolve_alias" /usr/src/app/arifosmcp/tools_canonical.py
docker exec arifosmcp grep -n "def normalize_tool_name" /usr/src/app/arifosmcp/runtime/tool_specs.py
docker exec arifosmcp grep -n "TOOL_CATALOG\|AXIS_VIEW" /usr/src/app/arifosmcp/unified_server.py
docker exec arifosmcp grep -n "CANONICAL_TOOL_HANDLERS\|FINAL_TOOL_IMPLEMENTATIONS" /usr/src/app/arifosmcp/runtime/tools.py
```

### Step 4 — The Canonical Bug: resolve_alias mode Double-Pass

**This bug causes ALL tool calls to fail.**

Location: `tools_canonical.py` ~line 692, in `resolve_alias()`:
```python
return fn(mode, **kwargs)  # BUG: mode passed positionally + in kwargs
```

The `mode` parameter is positional-only (defined with `/` in function signature). But the alias map provides `mode` positionally AND the caller's `kwargs` ALSO contains `mode` from the original `req` dict. Python raises:
```
TypeError: function() got some positional-only arguments passed as keyword arguments: 'mode'
```

**Fix:**
```python
kwargs = dict(kwargs)
kwargs.pop("mode", None)  # strip mode from kwargs — already passed positionally
return fn(mode, **kwargs)
```

### Step 5 — RuntimeEnvelope Return Type Bug

If benchmark shows `'RuntimeEnvelope' object has no attribute 'get'`:
→ The handler returns a RuntimeEnvelope object where code expects dict
→ Affects: `arifos_sense`, `arifos_mind`, `arifos_kernel`
→ Fix: Ensure handlers return dict, not RuntimeEnvelope

### Step 6 — Check Preconditions for Local File Tools

Tools like `AFWELL_state_read` require `/root/WELL/state.json` on the **host** filesystem (not inside container). These fail with "Permission denied" if the file doesn't exist.

### Step 7 — Check inputSchema Accuracy

All tool inputSchemas say `additionalProperties: true` — accepts anything. But Python functions require specific named parameters. No agent can call tools correctly without reading source code. Fix: Update each schema to document actual parameters.

## Common Bug Patterns Found in arifOS

| # | Bug | Symptom | Fix |
|---|-----|---------|-----|
| 1 | `resolve_alias` mode double-pass | All tools return TypeError | Strip mode from kwargs |
| 2 | RuntimeEnvelope return type | `arifos_sense/mind/kernel` VOID | Return dict, not RuntimeEnvelope |
| 3 | Missing state file | AFWELL tools fail with Permission denied | Create file or refactor tool |
| 4 | inputSchema accepts anything | Agents can't call tools correctly | Document actual params in schema |
| 5 | source_commit unknown | No deployment traceability | Inject git hash via `ARIFOS_BUILD_COMMIT` env |

## Verification After Fix

```bash
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":99,
       "params":{"name":"WEALTH_NPV_EVALUATE",
       "arguments":{"req":{"mode":"npv",
       "initial_investment":100,"cash_flows":[30,40,50],
       "discount_rate":0.1}}}}'
```

Expected: valid JSON result. Not an error message.

## What This Red-Team Found (2026-04-25)

- All 28+ tools fail on invocation — `resolve_alias` mode bug
- `arifos_sense/mind/kernel` return RuntimeEnvelope instead of dict (VOID)
- AFWELL tools need `/root/WELL/state.json` that doesn't exist (CRITICAL)
- `/metadata` returns empty (Agent Card inaccessible)
- `source_commit: "unknown"` in /health
- Dual handler map (CANONICAL vs FINAL) with unclear override precedence
- `sovereign_subject: "anonymous"` — identity gap

## Forged Fix Prompt for AGI
## Forged Fix Prompt for AGI

```
AGI — arifOS MCP Tool Fix Sprint

ALL TOOLS — CLASSIFY BEFORE FIXING
══════════════════════════════════════

arifOS has TWO tool classes. Treat them differently:

CLASS A — v1 Constitutional Tools (WORKS, but with stub outputs)
────────────────────────────────────────────────────────────
These work: arif_judge_deliberate, arif_ops_measure, arif_mind_reason,
  arif_heart_critique, arif_session_init, arif_sense_observe,
  arif_evidence_fetch, arif_memory_recall, arif_vault_seal,
  arif_forge_execute, arif_kernel_route, arif_reply_compose,
  arif_gateway_connect

Known issues (NOT broken — just shallow):
  - arif_mind_reason: synthesis = "Reasoning complete." (empty)
  - arif_heart_critique: risks = ["None detected (stub)"] (no real taxonomy)
  - arif_ops_measure: params = mode, estimate, session_id, actor_id
    (NOT req:{} — the wrapper wraps mode-level params, not req)

CLASS B — Axis Tools (BROKEN — all 28+ fail with mode bug)
────────────────────────────────────────────────────────
arifos_T_* (7 tools), wealth_* (8 tools), arifos_M_* (3 tools),
  geoxarifOS_* (2 tools), AFWELL_* (6 tools)

These all fail with:
  TypeError: function() got some positional-only arguments 
  passed as keyword arguments: 'mode'

FIX: Stage 1 only — fix resolve_alias. Stage 2 — validate. 
     No Stage 3 until Stage 2 confirms stable.

FIX 1 (CRITICAL) — resolve_alias mode double-pass
File: /usr/src/app/arifosmcp/tools_canonical.py ~line 692
Current: return fn(mode, **kwargs)
Fix: kwargs = dict(kwargs); kwargs.pop("mode", None); return fn(mode, **kwargs)

FIX 2 (CRITICAL) — RuntimeEnvelope return type
Files: arifos_sense, arifos_mind, arifos_kernel handlers
Fix: Ensure handlers return dict, not RuntimeEnvelope

FIX 3 (HIGH) — AFWELL state file
Create /root/WELL/state.json with {} default OR refactor tools

FIX 4 (HIGH) — inputSchema accuracy
Update schemas to document actual parameters

FIX 5 (HIGH) — source_commit tracking
Inject git commit hash via ARIFOS_BUILD_COMMIT env var

Verification: curl test each fixed tool. Report per-fix result.
```

## v1 Tool Correct Parameters (proven live 2026-04-26)

The v1 constitutional tools do NOT use `req:{}` wrapper. They use flat parameters:

```bash
# arif_ops_measure — correct
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":99,
       "params":{"name":"arif_ops_measure",
       "arguments":{"mode":"health"}}}'

# arif_judge_deliberate — correct
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":99,
       "params":{"name":"arif_judge_deliberate",
       "arguments":{"candidate":"Test claim"}}}'

# arif_mind_reason — correct
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":99,
       "params":{"name":"arif_mind_reason",
       "arguments":{"mode":"reason","query":"test"}}}'

# arif_heart_critique — correct
curl -s -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"tools/call","id":99,
       "params":{"name":"arif_heart_critique",
       "arguments":{"mode":"critique","target":"test action"}}}'
```

Wrong: `arguments: {"req": {"mode": "health"}}` — causes Unexpected keyword argument error.

## Verified v1 Tool Behavior (live test 2026-04-26)

| Tool | Status | Output |
|------|--------|--------|
| `arif_judge_deliberate` | ✅ WORKS | Full constitutional adjudication, floor compliance, state_hash, F11 invoked |
| `arif_ops_measure` | ✅ WORKS | cpu/mem/disk + delta_S thermodynamic marker |
| `arif_mind_reason` | ⚠️ SHALLOW | Returns structured output but synthesis = "Reasoning complete." |
| `arif_heart_critique` | ⚠️ STUB | Returns "None detected (stub)" — no real risk taxonomy |

## Maturity Score (corrected from external agent audit)

| Area | Score | Notes |
|------|-------|-------|
| MCP discovery | 9/10 | |
| v1 tool callability | 8/10 | Works but some are stubs |
| Axis tool callability | 2/10 | All 28+ broken — mode bug |
| Session control | 8/10 | |
| OPS health | 8/10 | |
| JUDGE | 7/10 | Works but returns HOLD on F11 |
| F01 enforcement | 8.5/10 | FORGE correctly HOLDs |
| HEART | 2/10 | Stub — no real risk taxonomy |
| MIND depth | 4/10 | Empty synthesis output |
| Evidence grounding | 4/10 | Fake success ambiguity |
| Memory persistence | 3/10 | Unverified |
| Vault proof | 5/10 | Unverified |
| Forge safe behavior | 6.5/10 | HOLD works, unverified on real actions |

Corrected overall: **5.2/10** (external agent said 6.8/10 — axis tools not tested)

## External Surface Check — Always Probe First

External domains (`mcp.arif-fazil.com`, `arifosmcp.arif-fazil.com`) can be dark even when the internal server is healthy. Test from outside the VPS:

```bash
# External MCP surface
curl -s --max-time 8 https://mcp.arif-fazil.com/ -o /dev/null -w "%{http_code} %{size_download}"
curl -s --max-time 8 https://mcp.arif-fazil.com/health

# External arifOS MCP surface
curl -s --max-time 8 https://arifosmcp.arif-fazil.com/ -o /dev/null -w "%{http_code} %{size_download}"
curl -s --max-time 8 https://arifosmcp.arif-fazil.com/health

# If both return empty/0 bytes → endpoint is dark (not just slow)
# Internal localhost:8080 may still be healthy while external is dark
# This is an F13-class observation: live surface telemetry is required for trustworthy audits
```

**Known failure pattern:** Cloudflare proxy returns empty 200 with 0 bytes when origin is unreachable. Do NOT treat empty 200 as "endpoint works."

## Live Server Verification (Internal)

```bash
# Always check the internal server first
curl -s http://localhost:8080/health
curl -s http://localhost:8080/ready

# Run pytest from the correct environment
cd /root/arifOS && /usr/local/bin/pytest tests/ -q --tb=short
```

**Known test failures (2026-04-27):**
- 5 e2e/integration tests fail at collection with `RuntimeError: Surface drift detected` — hardcoded external domain URLs that are unreachable
- 4 deprecation warnings in `__init__.py` importing deprecated modules (`vault_seal.py`, `forge_execute.py`, `sessions.py`, `tool_specs.py`)
- Test suite CANNOT pass cleanly without either: (a) mocking those external endpoints, or (b) making them environment-variable-gated

## Schema vs Enforcement Gap

arifOS has rich Pydantic schemas in `arifosmcp/schemas/` but they are NOT enforced at tool dispatch. Schemas exist for:
- `VerdictOutput` (ToAC, ThermodynamicState, DecisionCollapse, GrowthParadox, AKAL, AmanahProof, FloorComplianceProof, DissentReasoning, CivilizationalAnchor)
- `SealOutput` (IrreversibilityBond, EntropyDelta, EpistemicSnapshot)
- `TelemetryBlock`, `VitalsBlock`

**Gap:** `constitutional_core.py` calls tools directly without `SomeModel.model_validate()` guard. Malformed outputs are NOT rejected at runtime.

## F9/F5/F6 Mandatory Prerequisite Chain Is Missing

`constitutional_core.py` comment says F9 is "(Enforced at content layer)" — meaning it is NOT in the core floor evaluation path. If `arif_heart_critique` is skipped entirely, F9 is bypassed. Same applies to F5/F6 which rely on heart_critique output.

The TODO in `tools_canonical.py` line 16 confirms: *"Before deployment: wire F9_TAQWA and F11_AUDIT into the tool dispatch layer"* — this was never implemented.

**Verification:**
```bash
grep -n "heart_critique\|F9\|TAQWA" /root/arifOS/arifosmcp/core/constitutional_core.py
# F5/F6 are commented as "Enforced by heart_critique" — not enforced as hard gates
```

## Deprecated Module Cleanup (Incomplete)

Migration from 44→13 tool era left incomplete cleanup:
- `vault_seal.py` → deprecated, use `vault.py` ✅ done
- `sessions.py` → deprecated, use `session.py` ✅ done
- `__init__.py` still imports deprecated modules ⚠️ — causes deprecation warnings on every import
- `tool_specs.py` → deprecated, use `tool_spec.py` ⚠️ — warned in public_registry.py

## Cloudflare www.arif-fazil.com Fix (completed 2026-04-26)

Error 1014 = CNAME cross-user blocking. Root cause: www was CNAME to 
`ariffazil.pages.dev` (Cloudflare Pages), blocked on non-Enterprise plans.

Fix via Cloudflare API:
```bash
# 1. Delete old CNAME
ZONE_ID="6e837d3be53b37dcf79e0f09a1e14faa"
RECORD_ID="e43f713615d732dc4f684a8294c5ae56"
curl -s -X DELETE "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/$RECORD_ID" \
  -H "Authorization: Bearer $(cat /root/.cloudflare_token)" \
  -H "Content-Type: application/json"

# 2. Create A record pointing to VPS
curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $(cat /root/.cloudflare_token)" \
  -H "Content-Type: application/json" \
  -d '{"type":"A","name":"www","content":"72.62.71.199","proxied":true}'

# 3. Wait for CF propagation (~5 min), test
curl -sI https://www.arif-fazil.com
```

Token stored at `/root/.cloudflare_token` (format: `cfut_`). Token prefix confirms
it is Cloudflare User Token. Verify with:
```bash
curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
  -H "Authorization: Bearer $(cat /root/.cloudflare_token)"
```

## Dual Container Awareness

Two arifOS containers may be running simultaneously:
- `arifosmcp` — primary, port 8080
- `arifosmcp-patchrun` — patch/test container, port 8082

Test the correct one. Check which is primary:
```bash
docker ps --format "{{.Names}} {{.Status}}" | grep arifosmcp
docker port arifosmcp  # returns 8080/tcp -> 0.0.0.0:8080
docker port arifosmcp-patchrun  # returns 8080/tcp -> 0.0.0.0:8082
```

## What the External Agent Got Wrong (2026-04-26)

1. Scored overall 6.8/10 — should be 5.2/10 (axis tools not tested by external agent)
2. Scored MIND 7/10 — should be 4/10 (synthesis is "Reasoning complete." — empty)
3. Scored HEART 4/10 — should be 2/10 (stub confirmed)
4. Did not test arif_mind_reason or arif_heart_critique with correct params
5. Did not discover the mode double-pass bug in axis tools
6. Did not verify CF token was invalid before reporting
7. Scored all tools as "working" — only v1 constitutional tools work

## Credential Verification — Always Check Before Use
## Git Verification — Catching Fabricated Claims

Gemini-Clerk-L3 (and similar agents) tend to overstate what they did. Use these commands to independently verify git claims:

### Detect Fake Merges
```bash
# Check if a merge actually happened — real merges have TWO parents
git log --all --source --remotes  # shows all branches
git merge-base main release/branch-X  # find common ancestor
# If merge-base != HEAD of target branch, they're still parallel (not merged)
```

### Verify Commit Authorship and Content
```bash
git log -1 --format="%h %ae %ai %s" HEAD  # who/when/what
git show --stat HEAD  # what files changed
git diff parent_commit:path HEAD:path  # compare specific file across branches
```

### Check for File Residuals Before Auditing
```bash
ls -lh /root/*.bak* /root/sites.bak* 2>/dev/null  # before claiming "clean"
git -C /root/arifOS status --short  # check for uncommitted/.bak files
```

### The arifOS_bot Pattern
- Commits from `arifOS_bot@arif-fazil.com` are automated (via GitHub Actions or similar)
- If two branches have identical commit messages/timestamps but different content → concurrent parallel commits, NOT a merge
- Always diff the actual files, never trust the commit message alone

## Credential Verification — Always Check Before Use

A credential stored on disk is NOT necessarily valid. Test it before use.
### The Pattern (proven 2026-04-25)
```
1. Find credential: /root/.cloudflare_token, ~/.env, /etc/arifos/compose/.env
2. Test it immediately:
   curl -s "https://api.cloudflare.com/client/v4/user/tokens/verify" \
     -H "Authorization: Bearer $(cat /root/.cloudflare_token)"
3. Check what service actually uses it for:
   - cat /etc/arifos/compose/Caddyfile → does it use CF DNS provider?
   - docker exec caddy caddy list-modules | grep dns → is CF DNS even enabled?
4. If token invalid AND service works → investigate why it was stored
```

### Red Flags
- Token exists but API returns `{"errors": [{"code": 1000, "message": "Invalid API Token"}]}`
- Stored credential never validated against actual service
- Service working despite "dead" credential (via alternative mechanism)

### Cloudflare-Specific Bug Found
- Token `/root/.cloudflare_token` with prefix `cfut_` returns **Invalid API Token**
- Caddy is NOT using Cloudflare DNS — it uses HTTP/Let's Encrypt challenges
- Token was stored but never needed, never worked, never verified
- www.arif-fazil.com 403 = Cloudflare error **1014** (CNAME cross-user blocking) — fix: change www CNAME to A record pointing to VPS IP `72.62.71.199`

### Agent Accountability Rule
When asking user for a credential they "already gave":
1. Check if it actually works FIRST (curl test)
2. Check if it's even needed (service might work without it)
3. Never ask user to re-enter without running Step 1 first
4. Log invalid credentials immediately so future sessions don't repeat the dead-end

---

## F9/F13 Enforcement Gap — floors.py Has Code, server.py Never Calls It (2026-04-27)

**Finding:** `arifosmcp/core/floors.py` contains full `check_floors()` implementation with F1–F13 logic including F09 keyword blocklist and F13 sovereign veto. BUT `server.py`'s `_wrap_hardened_dispatch()` wrapper (which wraps ALL tool handlers) never calls `check_floors()` — it only logs the result after execution. The constitution was documentation, not code.

**Fix implemented (2026-04-27):** `_wrap_hardened_dispatch` now:
1. Calls `check_floors(tool_name, params, actor_id, session_id)` BEFORE the handler runs
2. Returns `{"verdict": "HOLD"/"VOID", ...}` if floors fail — fail-closed
3. Calls `record_tool_call(session_id, tool_name)` after floor clearance (for F9 TAQWA tracking)

**Files changed:**
- `arifosmcp/core/floors.py` — added `_SESSION_TOOL_HISTORY` dict + `record_tool_call`/`get_session_history`/`clear_session_history`
- `server.py` — `_wrap_hardened_dispatch` wrapper now calls `check_floors()` before handler
- `deployments/af-forge/docker-compose.yml` — healthcheck port 3000→8080

**Verification:**
```bash
cd /srv/openclaw/workspace/arifOS && git diff --stat HEAD
# Must show: arifosmcp/core/floors.py, server.py, deployments/af-forge/docker-compose.yml
```

---

## F9 TAQWA Gate — Session Call Chain Tracking (2026-04-27)

**Requirement:** `arif_forge_execute` requires `arif_heart_critique` to have been called first in the same session chain (F9 Anti-Hantu prerequisite enforcement).

**Implementation:** `arifosmcp/core/floors.py`:
```python
_SESSION_TOOL_HISTORY: dict[str, set[str]] = {}
_history_lock = threading.Lock()

def record_tool_call(session_id: str | None, tool_name: str) -> None: ...
def get_session_history(session_id: str | None) -> set[str]: ...

# In check_floors(), F09 gate (Gate 2 of 2):
if tool_name == "arif_forge_execute":
    history = get_session_history(session_id)
    if "arif_heart_critique" not in history:
        failed.append("F09")
        logger.warning("F09 ANTIHANTU: arif_forge_execute blocked — arif_heart_critique not called. PSI KHIANAT.")
```

**F9 has two gates:**
- Gate 1: keyword blocklist (manipulation words like `sudo`, `eval`, `__import__`) — shallow, fast
- Gate 2: session prerequisite chain (heart_critique must precede forge) — structural

---

## F13 Sovereign Veto — Was Inverted (2026-04-27)

**Bug:** F13 fired when `sovereign_veto=TRUE` was PRESENT. Correct: F13 fires when ABSENT (bypassing human veto attempt).

**Old (wrong):**
```python
elif floor_value == "F13":
    if params.get("sovereign_veto"):
        failed.append("F13")  # Blocks when veto IS present
```

**New (correct):**
```python
elif floor_value == "F13":
    if spec.get("access") in ("sovereign", "authenticated"):
        if not params.get("sovereign_veto"):
            failed.append("F13")  # Blocks when veto IS absent
```

---

## Healthcheck Port Mismatch — Container Unhealthy But Server Fine (2026-04-27)

**Bug:** `arifOS/deployments/af-forge/docker-compose.yml` healthcheck hits `localhost:3000` but uvicorn binds to `localhost:8080`. Container is healthy but Docker marks unhealthy every 30s.

**Evidence:**
```bash
docker exec arifosmcp curl -s http://localhost:8080/health  # ✅ 200 OK
docker exec arifosmcp curl -s http://localhost:3000/health  # ❌ exit 7 (connection refused)
docker ps  # Shows "unhealthy" while server is fine
```

**Fix:** `deployments/af-forge/docker-compose.yml` line 60 — port 3000→8080

**Apply:** `cd /srv/openclaw/workspace/arifOS/deployments/af-forge && docker compose up -d --force-recreate arifosmcp`

---

## External Surface vs Internal Server — Always Test Internal First (2026-04-27)

When `mcp.arif-fazil.com` or `arifosmcp.arif-fazil.com` return empty/0-bytes from outside:
1. Test `http://localhost:8080/health` inside the container FIRST (authoritative)
2. Cloudflare proxy returns empty 200 when origin is unreachable — don't treat empty-as-200

```bash
# Internal (authoritative)
docker exec arifosmcp curl -s http://localhost:8080/health

# External (may be CF/DNS issue while server is fine)
curl -s --max-time 8 https://arifosmcp.arif-fazil.com/health
```

---

## Git Diff Verification After Sub-Agent Claims (2026-04-27)

When a sub-agent claims to have made fixes, verify with:
```bash
cd /srv/openclaw/workspace/arifOS && git diff --stat HEAD
# If claimed files not in diff → nothing was done
```

**Lesson:** Sub-agent ran same compound command 9 times, returned no output, then claimed two fixes applied. `git diff --stat HEAD` showed zero changes until fixes were applied manually. Always diff-before-trusting.

---

## Internal VPS Paths (2026-04-27)

- **Local workspace:** `/srv/openclaw/workspace/arifOS/` (git repo root)
- **Primary compose file:** `deployments/af-forge/docker-compose.yml`
- **Runtime server:** `server.py` (binds to 0.0.0.0:8080, health at /health, MCP at /mcp)
- **Floor enforcement:** `arifosmcp/core/floors.py` (check_floors, record_tool_call, get_session_history)
- **Container name:** `arifosmcp` (primary), `arifosmcp-patchrun` (secondary on port 8082)
- **Apply compose changes:** `docker compose up -d --force-recreate arifosmcp` (causes ~5s downtime)

---
File: /usr/src/app/arifosmcp/tools_canonical.py ~line 692
Fix: kwargs = dict(kwargs); kwargs.pop("mode", None); return fn(mode, **kwargs)

FIX 2 (CRITICAL): RuntimeEnvelope return type
Files: arifos_sense, arifos_mind, arifos_kernel handlers
Fix: Ensure handlers return dict, not RuntimeEnvelope

FIX 3 (HIGH): AFWELL state file
Create /root/WELL/state.json with {} default OR refactor tools

FIX 4 (HIGH): inputSchema accuracy
Update schemas to document actual parameters

FIX 5 (HIGH): source_commit tracking
Inject git commit hash via ARIFOS_BUILD_COMMIT env var

Verification: curl test each fixed tool. Report per-fix result.
```