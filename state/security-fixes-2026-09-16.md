# Security fixes — external report (Syed Anas Mohiuddin), 2026-09-15/16

Source report: mcp-safeguard against 1!2026.9.1 — 117 raw hits, 105 noise, 2 real.
CVE request filed by reporter with MITRE CNA-LR. Tracking no. CAN-2026-2037739.
Reporter is satisfiable / already acknowledged; NOT the 2026-08-25 scar.

## Verified by me (probe-first, not taken on the reporter's word)

### 1. Cypher injection — CONFIRMED, REPRODUCED, FIXED (dev tree)
`arifosmcp/runtime/l5_sovereign_forge.py`
Property KEYS interpolated UNQUOTED (`e.{key} = '...'`) while only values were escaped.
Keys come from an LLM JSON extraction of raw memory text -> prompt injection reaches FalkorDB.
Repro: key `x MATCH (n) DETACH DELETE n //` reached the query unquoted -> whole-graph wipe.
Fix: `_prop_key()` whitelist `^[A-Za-z_][A-Za-z0-9_]*$` at all three key sites (423/447/496).
Test: 6 malicious keys rejected, legit keys still build.

### 2. Path traversal — CONFIRMED, REPRODUCED, FIXED (dev tree)
`arifosmcp/server.py:skill_by_name_resource` and `arifosmcp/resources/atlas333.py:scar_by_id`
Repro: name `../../../../root/.secrets` resolved to `/root/.secrets/SKILL.md`.
Fix: resolve + containment check against resolved root (not a char blocklist).
Test: traversal rejected, legit names pass.
NOTE: reporter traced the root cause to fastmcp's match-before-decode order — worth reporting upstream.

### 3. Hardcoded HMAC fallback — CONFIRMED DEAD CODE, HARDENED (dev tree)
`arifosmcp/tools/deliberate.py:_actor_signature` used `os.getenv(..., "default_secret")`.
Not called anywhere; live signer is crypto_auth Ed25519. Now fails closed instead of guessing.

### 4. Dead mock-OAuth endpoint — NOT RE-VERIFIED (low priority, no hole)
Reporter: mints tokens nothing honours. Misleading, not exploitable.

## Deployment boundary — NOT DONE, needs F13
All five fixes exist ONLY in /root/arifOS (dev tree). /opt/arifos/app (live kernel) untouched.
Live kernel still serving :8088, http=200, unchanged. Shipping = push to origin/main ->
deploy-release -> restart arifos.service. That is a kernel mutation, not a bot's call.

## Outstanding — sovereign decisions
1. MITRE: reporter proceeds as reporter, uses our confirmation email as vendor ack.
2. mcp-safeguard scan offer accepted; results now delivered.
3. Public write-up request: arifOS as one of his first, with credit, post-fix, pre-review.
