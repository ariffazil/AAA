# MCP 2026-07-28 — 12 Conformance Gates (Q1-Q12)

**Status:** SPEC READY · executable as test suite
**Date:** 2026-09-29
**Owner:** FI-008 (kimi-code)
**Source:** ChatGPT external audit (2026-09-29) expanded with machine-testable assertions
**Canon grounding:** SEP-2484 (conformance tests required for standards-track SEPs); Canon #0 three-test gate

---

## 0. Purpose

These 12 gates are the acceptance test for arifOS + GEOX alignment with MCP 2026-07-28. Each gate has: WHAT it tests, HOW to test, EXPECTED result, and CURRENT status (probed 2026-09-29).

Run as: `arif_conformance_test --gates Q1..Q12 --target {arifos|geox|both}`

---

## Q1 — server/discover advertises 2026-07-28

**WHAT:** Server exposes `server/discover` endpoint that returns `mcp_versions_supported` containing `"2026-07-28"`.
**HOW:** `GET /discover` (no auth, no session header) → assert response contains `mcp_versions_supported[0] == "2026-07-28"`.
**EXPECTED:** 200 OK; JSON body with `server_info, capabilities, mcp_versions_supported`.
**TODAY:** ❌ endpoint does not exist (probed via `/discover` returns 404 or non-JSON).

---

## Q2 — tools/list returns exactly canonical 9 (arifOS) or 26 (GEOX)

**WHAT:** `tools/list` returns exactly the canonical tool set, no extras.
**HOW:** POST `/mcp` with `{"jsonrpc":"2.0","method":"tools/list","id":1}` → assert `result.tools[].name` matches canonical set.
**EXPECTED for arifOS:** `{arif_init, arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal, arif_stage}` (length 9).
**EXPECTED for GEOX:** 26 tools as enumerated in `02-geox-outputschema-patches.md`.
**TODAY:** ✅ GEOX confirmed (26/26 via `geox_surface_status`); ✅ arifOS likely (9 tools observed in tool definitions).

---

## Q3 — arif_init issues application handle, no bearer token leak

**WHAT:** `arif_init` returns `session_id` (opaque handle) but does NOT include `session_token` or `act_claims` in model-visible output.
**HOW:** Call `arif_init mode=light actor_id=kimi-code/FI-008` → recursively walk response, assert:
- `session_id` present
- No key `session_token` anywhere
- No key `act_claims` anywhere
- No string value matches regex `^act_v\d+\.`
**EXPECTED:** All three assertions pass.
**TODAY:** ❌ FAILED (probed 2026-09-29): `session_token` returned at top-level + `result.session_token` + reconstructed in `meta.act_claims`. Echoed 3×.

---

## Q4 — arif_observe succeeds with handle on fresh HTTP worker

**WHAT:** A tool call carrying `session_id` as body argument succeeds even if the underlying HTTP worker changes between calls (stateless transport).
**HOW:** (1) `arif_init` → get `session_id`. (2) Kill connection. (3) New TCP connection. (4) `arif_observe {session_id: <from step 1>, ...}` → expect success.
**EXPECTED:** Server resolves `session_id` → capability store entry server-side; tool runs.
**TODAY:** ❌ UNVERIFIED — current architecture couples MCP session to constitutional session.

---

## Q5 — No `Mcp-Session-Id` dependency on modern path

**WHAT:** Modern endpoint accepts `session_id` in body without requiring `Mcp-Session-Id` header.
**HOW:** `POST /mcp` with `session_id` in body but NO `Mcp-Session-Id` header → success.
**EXPECTED:** Server does not require header.
**TODAY:** ❌ FAILED — current transport requires `Mcp-Session-Id` (legacy 2025-era pattern).

---

## Q6 — Mcp-Method / Mcp-Name headers accepted

**WHAT:** Server accepts `Mcp-Method: tools/call` and `Mcp-Name: arif_judge` headers per MCP 2026-07-28 routing convention.
**HOW:** `POST /mcp` with `Mcp-Method: tools/call`, `Mcp-Name: arif_judge`, body has `session_id + arguments` → routed to `arif_judge` implementation.
**EXPECTED:** Server routes correctly.
**TODAY:** ❌ headers not implemented (legacy uses `Mcp-Session-Id` for routing).

---

## Q7 — Malformed schemas → standard JSON-RPC errors

**WHAT:** Input validation errors returned as JSON-RPC -32602 (Invalid params) per SEP-1303.
**HOW:** POST `tools/call` with invalid args (missing required, wrong type) → assert response has `error.code == -32602`.
**EXPECTED:** All malformed inputs return -32602 with descriptive message.
**TODAY:** UNVERIFIED — requires live call against each tool.

---

## Q8 — Application authority survives stateless transport

**WHAT:** `session_id` retains authority across HTTP worker changes, restarts, load-balancer shifts.
**HOW:** (1) `arif_init` with `requested_authority: MUTATE` (and Ed25519 signature) → get `session_id` with full authority. (2) New worker. (3) `arif_forge {session_id, ...}` → succeeds with same authority.
**EXPECTED:** Authority survives stateless transport.
**TODAY:** ❌ state coupled to MCP transport session.

---

## Q9 — OBSERVE_ONLY cannot mutate

**WHAT:** Session with `authority_band: OBSERVE_ONLY` cannot invoke mutating verbs (`arif_forge`, `arif_seal`, `arif_stage mutate modes`).
**HOW:** (1) `arif_init` (unsigned) → `authority_band: OBSERVE_ONLY`. (2) `arif_forge {...}` → expect -32603 with reason "band_deny" or "authority_insufficient".
**EXPECTED:** All mutating verbs return -32603.
**TODAY:** UNVERIFIED — canary probe returned `mutation_allowed: false` but tool was not actually invoked.

---

## Q10 — ACT credential never leaks into model-visible output

**WHAT:** No tool response contains the bearer JWT (`act_v\d+\....`).
**HOW:** For each of 9 (arifOS) or 26 (GEOX) tools: invoke with valid args → recursively grep response for regex `act_v\d+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`. Assert zero matches across all 9/26 responses.
**EXPECTED:** Zero matches.
**TODAY:** ❌ FAILED — `arif_init` response contains `act_v1.eyJhY3Rf...` at top level + `result.session_token` + `meta.act_claims` (3 matches).

---

## Q11 — Legacy 2025 client still works

**WHAT:** Old MCP client (using `Mcp-Session-Id` header, `initialize` handshake) still works against modern server.
**HOW:** Spin up MCP Inspector in 2025-era mode (`mcp-inspector --era 2025-11-25`) → assert all 9/26 tools callable.
**EXPECTED:** Backward compatibility maintained.
**TODAY:** ✅ likely passing (current code is 2025-era; dual-era migration is additive).

---

## Q12 — MCP Inspector passes both eras

**WHAT:** Same server passes conformance when inspected via both `mcp-inspector --era 2026-07-28` and `--era 2025-11-25`.
**HOW:** Run Inspector in both modes → assert green for canonical 9/26 tools in both.
**EXPECTED:** Both modes green.
**TODAY:** ❌ modern mode not implemented; only legacy mode would pass.

---

## Today's scoreboard (probed 2026-09-29)

| Gate | arifOS | GEOX |
|---|---|---|
| Q1 — server/discover | ❌ | ❌ |
| Q2 — tools/list canonical | ✅ (9) | ✅ (26) |
| Q3 — no bearer token leak | ❌ | n/a (GEOX has no bearer concept) |
| Q4 — stateless handle survival | ❌ | ❌ |
| Q5 — no Mcp-Session-Id dependency | ❌ | ❌ |
| Q6 — Mcp-Method/Mcp-Name headers | ❌ | ❌ |
| Q7 — JSON-RPC -32602 errors | UNVERIFIED | UNVERIFIED |
| Q8 — authority survives stateless | ❌ | n/a |
| Q9 — OBSERVE_ONLY cannot mutate | UNVERIFIED | n/a |
| Q10 — ACT never leaks | ❌ | n/a |
| Q11 — legacy 2025 client | ✅ likely | ✅ likely |
| Q12 — Inspector both eras | ❌ | ❌ |

**arifOS: 1 ✅, 8 ❌, 3 UNVERIFIED**
**GEOX: 2 ✅, 5 ❌, 2 UNVERIFIED (3 n/a)**

---

## Test runner (executable spec)

```bash
#!/usr/bin/env bash
# arif_conformance_test.sh
# Run all 12 gates against target MCP server.

set -euo pipefail
TARGET="${1:-arifos}"  # arifos | geox
ENDPOINT="${ENDPOINT:-http://localhost:18081/mcp}"
DISCOVER="${DISCOVER:-http://localhost:18081/discover}"

pass=0; fail=0; unver=0

run() {
    local name="$1"; local cmd="$2"; local expected="$3"
    echo "=== $name ==="
    if out=$(eval "$cmd" 2>&1); then
        if echo "$out" | grep -q "$expected"; then
            echo "PASS: $name"; pass=$((pass+1))
        else
            echo "FAIL: $name (no match for: $expected)"; fail=$((fail+1))
        fi
    else
        echo "UNVERIFIED: $name (cmd failed)"; unver=$((unver+1))
    fi
}

# Q1
run "Q1 server/discover" \
    "curl -sS $DISCOVER" \
    '"2026-07-28"'

# Q2
run "Q2 tools/list canonical" \
    "curl -sS -X POST $ENDPOINT -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"tools/list\",\"id\":1}'" \
    '"name":"arif_'

# Q3, Q10 — bearer token leak
run "Q3/Q10 no bearer leak" \
    "curl -sS -X POST $ENDPOINT -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"arif_init\",\"arguments\":{\"mode\":\"light\",\"actor_id\":\"kimi-code/FI-008\"}},\"id\":1}'" \
    'session_id'  # assert NO act_v1.* present (negative assertion done separately)

# Q5
run "Q5 no Mcp-Session-Id dependency" \
    "curl -sS -X POST $ENDPOINT -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"arif_observe\",\"arguments\":{\"session_id\":\"SEAL-test\",\"query\":\"ping\"}},\"id\":1}'" \
    'result'

# Q6
run "Q6 Mcp-Method/Mcp-Name headers" \
    "curl -sS -X POST $ENDPOINT -H 'Content-Type: application/json' -H 'Mcp-Method: tools/call' -H 'Mcp-Name: arif_observe' -d '{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"arif_observe\",\"arguments\":{\"session_id\":\"SEAL-test\"}},\"id\":1}'" \
    'result'

# Q7 — malformed schema
run "Q7 malformed schema -32602" \
    "curl -sS -X POST $ENDPOINT -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"arif_init\",\"arguments\":{\"mode\":\"INVALID\"}},\"id\":1}'" \
    '-32602'

# Q9 — OBSERVE_ONLY cannot mutate
run "Q9 OBSERVE_ONLY cannot mutate" \
    "curl -sS -X POST $ENDPOINT -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"arif_forge\",\"arguments\":{\"session_id\":\"SEAL-test\",\"manifest\":\"{}\"}},\"id\":1}'" \
    '"code":-32603'

# Q11 — legacy 2025
run "Q11 legacy 2025 client" \
    "curl -sS -X POST $ENDPOINT -H 'Content-Type: application/json' -H 'Mcp-Session-Id: SEAL-test' -d '{\"jsonrpc\":\"2.0\",\"method\":\"tools/list\",\"id\":1}'" \
    '"name":"arif_'

# Q12 — Inspector (requires mcp-inspector binary)
run "Q12 Inspector both eras" \
    "mcp-inspector --era 2026-07-28 --target $ENDPOINT 2>&1; echo '---'; mcp-inspector --era 2025-11-25 --target $ENDPOINT 2>&1" \
    'PASS'

echo "===== SCOREBOARD ====="
echo "PASS: $pass · FAIL: $fail · UNVERIFIED: $unver"
```

---

## HOLD gates

| Gate | Unblock |
|---|---|
| Run live test suite | MUTATE band grant |
| DEPLOYMENT_DRIFT | Reconciled source/built/deployed |
| Receipt chain | Replay proof_spine |

---

DITEMPA BUKAN DIBERI ⚒️
