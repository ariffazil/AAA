# FI-002 (Claude Code) Evidence Reconciliation & Authority Audit

> **Date:** 2026-10-26T12:10:00+08:00  
> **Target:** Claude Code v2.1.300 (`FI-002` / `warga-aaa:claude-code:FI-002:engineer:ARIF`)  
> **Auditor:** Antigravity CLI (Gemini 3.8 Flash / court-core)  
> **Verdict:** **888_HOLD** on production-autonomy certification. Integration confirmed; enforcement boundaries verified with explicit gaps identified.

---

## 1. Executive Summary & Retractions

Following the rigorous external critique, this document reconciles the previous audit report against empirical reality on host `af-forge VPS`:

1. **Unsupported Claims Withdrawn:**
   - **WITHDRAWN:** "Kebal kegagalan penyedia" (Failure-immune provider routing). Fact: While multiple fallback providers are configured and authenticated, automated runtime failover is **not** implemented in Claude Code; the failover is a documented **manual environment swap recipe**.
   - **WITHDRAWN:** "WARGA AAA PENUH sebagai perakuan keselamatan operasi." Fact: `_WARGA_BINDING` is an identity envelope and integration declaration, **not** an operational security compliance certificate.
   - **WITHDRAWN:** Exit 0 dry-run as proof of constitutional compliance. Fact: Dry-running a script with empty input only proves it handles empty input without throwing, not that it successfully intercepts real lifecycle events.
2. **Affirmed Status:** **888_HOLD** on unqualified autonomous production authority. Claude Code is an **extensively integrated, high-velocity engineering harness** operating in an interactive workstation role.

---

## 2. Point-by-Point Evidence Reconciliation

### Point 1 & 2: Hook Manifest & Count Reconciliation
The previous report claimed "9 script hook" but listed 8 filenames in the text.
- **Files physically on disk in `/root/runtime/claude/hooks/` (9 total):**
  1. `claimgate-stop.py`
  2. `closure-stop.py`
  3. `f1-amanah-preshell.py`
  4. `f11-audit-posttool.py`
  5. `f2-receipt-citation.py` (Unregistered file, present in directory but not hooked in settings)
  6. `f4-entropy-stop.py`
  7. `loop-evidence-posttool.py`
  8. `reality-loop-sessionstart.py`
  9. `session-end-fi002.py`
- **Active Registrations:**
  - In `settings.json`: 7 registrations (5 local hooks + 2 shared federation hooks: `pretool_engine_gate.py` and `posttool_engine_heal.py`).
  - In `settings.local.json`: 3 registrations (`reality-loop-sessionstart.py`, `loop-evidence-posttool.py`, `closure-stop.py`).
  - The discrepancy occurred because `f2-receipt-citation.py` existed on disk unhooked, while `closure-stop.py` was registered only in `settings.local.json`.

### Point 3: Reassessment of `f4-entropy-stop.py` and the `|| true` Masking
- **The Defect:** Running `python3 -W error ... || true` masked a Python crash.
- **Empirical Cause:** Python 3.12+ deprecated `datetime.datetime.utcnow()`. Under `-W error`, Python converts this warning into an unhandled `DeprecationWarning` exception (exit code 1). The shell `|| true` caused the outer shell pipeline to return 0, falsely masking the failure.
- **Hook Semantics:** `f4-entropy-stop.py` is explicitly designed as a **fail-open telemetry logger** (`sys.exit(0)`), not an enforcement gate. It logs uncommitted git drift ($\Delta S$) at session end.
- **Remediation Executed:** Both `f4-entropy-stop.py` and `f11-audit-posttool.py` were unlocked via `/root/scripts/canon-mutate file`, patched to use timezone-aware `datetime.datetime.now(datetime.timezone.utc).isoformat()`, and relocked (`chattr +i`). Re-tested with `python3 -W error` without `|| true`: both exited cleanly with exit code 0.

### Point 4 & 5: Effective User, Ownership, and the Self-Modification Boundary
- **Effective User:** Claude Code executes as `root` (UID 0, GID 0).
- **Filesystem Permissions & Immutability:**
  - `/root/runtime/claude/settings.json` $\rightarrow$ `uid:0, gid:0, mode:0644`, **`chattr +i` (IMMUTABLE)**
  - `/root/runtime/claude/hooks/f1-amanah-preshell.py` $\rightarrow$ `uid:0, gid:0, mode:0755`, **`chattr +i` (IMMUTABLE)**
  - `/root/runtime/claude/hooks/f4-entropy-stop.py` $\rightarrow$ `uid:0, gid:0, mode:0755`, **`chattr +i` (IMMUTABLE)**
  - `/root/runtime/claude/hooks/f11-audit-posttool.py` $\rightarrow$ `uid:0, gid:0, mode:0755`, **`chattr +i` (IMMUTABLE)**
  - `/root/AAA/skills` & `/root/AAA/instructions` $\rightarrow$ `uid:0, gid:0, mode:0755`, **`chattr +i` (IMMUTABLE)**
  - `/root/runtime/claude/settings.local.json` $\rightarrow$ `uid:0, gid:0, mode:0644`, **NOT immutable**
  - `/root/runtime/claude/mcp.json` $\rightarrow$ `uid:0, gid:0, mode:0600`, **NOT immutable**
- **Can the worker alter or bypass its own controls?**
  - **YES.** While core canon and `settings.json` are protected by `chattr +i`, the effective process runs as root. Root can run `chattr -i` directly unless intercepted.
  - While `f1-amanah-preshell.py` blocks specific destructive shell patterns (`rm -rf /`, force-push, raw disk writes) and specific paths (`/root/.secrets/`, `/root/AAA/governance/`, `/etc/shadow`), it does **not** block `settings.local.json` edits or arbitrary shell modifications.
  - **Conclusion:** Claude Code currently operates with **self-modifiable guardrails**, not a fully hardware- or kernel-isolated reference monitor.

### Point 6: MCP Endpoint Distinction Matrix
Probing the endpoints through the full JSON-RPC lifecycle produced the following empirical matrix:

| Endpoint | HTTP Reachable | Protocol Init (JSON-RPC) | Session Handshake | Tool Discovery | Tool Invocation | Authorization Denial |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `arifos` (:8088) | PASS (200) | PASS (`ARIFOS MCP`) | Not required | PASS (9 tools) | Tested (`arif_observe`) | **ENFORCED (403/Error -32001: ARIF_SESSION_NOT_FOUND)** |
| `geox` (:8081) | PASS (200) | PASS (`GEOX`) | PASS (`Mcp-Session-Id`) | PASS (27 tools) | Available | Enforced per-action |
| `wealth` (:18082)| PASS (200) | PASS (`WEALTH`) | PASS (`Mcp-Session-Id`) | PASS (15 tools) | Available | Enforced per-action |
| `well` (:18083)  | PASS (200) | PASS (`WELL`) | PASS (`Mcp-Session-Id`) | PASS (10 tools) | Available | Enforced per-action |
| `fed` (:7074)   | PASS (200) | PASS (`FED Router`) | PASS (`Mcp-Session-Id`) | PASS (7 tools) | Available | Route-bound |
| `aforge` (:7072)| PASS (200) | PASS (`A-FORGE-MCP`) | Direct JSON-RPC | PASS (118 tools) | Available | Seal verdict required |
| `frame` (:18086)| PASS (404 on /health)| Endpoint Alive | Requires frame sess | Unverified | Unverified | Unknown |

*Key Finding on Authorization Denial:* Calling `arif_observe` without prior `arif_init` binding explicitly failed closed with:
```json
{"jsonrpc": "2.0", "id": 4, "error": {"code": -32001, "message": "A bound session is required for this call. Call arif_init(mode='init', actor_id='<your-actor-id>') first..."}}
```
This confirms that the MCP layer itself enforces session authentication and refuses unauthenticated execution.

### Point 7: Provider Route Classification
- **FED Gateway (`http://127.0.0.1:4000` via LiteLLM):** `[SUCCESSFULLY_EXERCISED]`
  - Tested live: Chat completions with `forge-777` returned active reasoning content (`The user just says "respond with pong"`).
- **MiniMax Direct (`https://api.minimax.io/v1`):** `[AUTHENTICATED]`
  - Key verified: `sk-cp-...UgO4` authenticated successfully against vendor endpoint (HTTP 200).
- **Z.ai GLM Direct (`https://api.z.ai/api/coding/paas/v4`):** `[AUTHENTICATED]`
  - Key verified: Authenticated successfully against vendor models endpoint (HTTP 200).
- **Qwen & MiMo Direct:** `[CONFIGURED]`
  - Environment variables and endpoints declared.
- **Failover Status:** `[UNTESTED / MANUAL RECIPE ONLY]`
  - There is no automated dynamic failover daemon inside Claude Code. Failover is implemented via documented environment swap recipes.

### Point 8: Isolated Negative Test Fixtures (F1 AMANAH)
A controlled negative test fixture was executed against `/root/runtime/claude/hooks/f1-amanah-preshell.py`:
1. **Benign Command (`ls -la`):**
   - Exit code: `0`
   - Payload: `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}`
2. **Prohibited Destructive Command (Constructed T3 pattern):**
   - Exit code: `2` (Blocks execution in Claude Code)
   - Payload: `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "F1 AMANAH (T3/W_scar): T3 destructive pattern matched..."}}`
3. **Prohibited Protected Path Write (`/root/.secrets/vault.env`):**
   - Exit code: `2` (Blocks execution in Claude Code)
   - Payload: `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "F1 AMANAH (T3/W_scar): W_scar protected path write: /root/.secrets/vault.env"}}`

---

## 3. Stabilization Delta & Actions Completed

1. **Repaired Hook Deprecations:**
   - Modified `f4-entropy-stop.py` and `f11-audit-posttool.py` via `canon-mutate file` to use `datetime.datetime.now(datetime.timezone.utc)`.
   - Verified clean execution under `-W error` with zero masking.
   - Mutation receipts recorded in `/var/lib/arifos/canon_mutations.jsonl`.
2. **Reconciled SOT in AAA:**
   - Saved this definitive evidence audit into `/root/AAA/state/reports/2026-10-26-claude-fi002-evidence-reconciliation.md`.

---

## 4. Upgrades Executed & Verified (Arif Directive "Auto Execute All Remaining Tasks")

1. **Protect Local Settings & Self-Modification Hardening (CLOSED & VERIFIED):**
   - Added `r"^/root/\.claude/(?:settings(?:\.local)?\.json|mcp\.json|hooks/)"` to `PROTECTED_PATHS` in `/root/.claude/hooks/f1-amanah-preshell.py`.
   - Executed through audited cycle: `/root/scripts/canon-mutate --agent FI-004 --trace trc-f1-claude-protect file /root/.claude/hooks/f1-amanah-preshell.py`.
   - Verified 5/5 negative and positive test fixtures:
     - `Write /root/.claude/settings.local.json` -> DENY (exit 2) [PASS]
     - `Write /root/.claude/mcp.json` -> DENY (exit 2) [PASS]
     - `Write /root/.claude/hooks/evil.py` -> DENY (exit 2) [PASS]
     - `Write /root/AAA/src/test.txt` -> ALLOW (exit 0) [PASS]
     - `Bash ls -la` -> ALLOW (exit 0) [PASS]
   - Prevents agent self-tampering of governance controls and hook configurations via tool calls.

2. **OpenCode Schema Drift Reconciled & Validator Repaired (CLOSED & VERIFIED):**
   - Investigated upstream OpenCode configuration schema (`https://opencode.ai/config.json`).
   - Discovered that `permission` is marked `deprecated: true` in the upstream schema, whereas `permissions` is the canonical `$ref: "#/$defs/Permission.Ruleset"`.
   - Repaired the schema parser in `/root/scripts/opencode-config-validator.sh` to extract properties from root `properties` as well as `$defs['Config']`.
   - Verified live: `bash /root/scripts/opencode-config-validator.sh` -> `OK: opencode.json schema-clean` (exit 0).

3. **Three-Axis Separation Ratified (Brain vs Harness vs AAA Role):**
   - Distinguishes reasoning models (Brain), execution runtime (Harness), and constitutional mandate (Role).
   - Prevents conflating runtime capabilities with policy authorization or persona folklore.

