---
name: browser-service-ops
description: "Use when debugging the playwright-mcp browser service."
capability_tier: fed-multimodal-vision
ecology_state: WARM
---
# Browser Service Operations

The federation runs a shared `playwright-mcp` browser server (systemd unit) that agents drive
over MCP HTTP (`/mcp`). It carries a persistent `--user-data-dir` so browser logins survive
restart. Two facts bite anyone configuring or probing it.

## Persistent profile + multiple sessions → add `--shared-browser-context`

A persistent `--user-data-dir` means ONE Chrome singleton owns the profile. Without the flag,
each MCP session spawns its own Chrome against the same profile and every `browser_navigate`
returns `Browser is already in use for <profile>, use --isolated` — while the listener is up and
the unit reads `active` (liveness, not capability). The fix is one line right after
`--user-data-dir` in the unit:

```
    --shared-browser-context \
```

This shares one Chrome across all sessions, so sessions come and go without contending for the
singleton lock. "Run serial / one session at a time" is NOT the fix — it only masks the defect;
any hung session re-leaks the lock.

## A stale/orphan Chrome holds the singleton lock across restarts

If the server or a test run dies without reaping its Chrome children, the orphan keeps the
profile lock and a clean, freshly restarted server still reports "already in use". Before
re-testing after a crash, kill orphan Chrome processes bound to that profile (they are children
of the dead instance, not the new one).

## Verify with a real tool call, not port liveness

"Listening on port" / `systemctl is-active` = transport liveness ONLY. A browser MCP can be
listening yet unable to drive Chrome (singleton lock, dead browser). To claim the lane works,
run the full round-trip — `initialize` → `notifications/initialized` → `tools/call
browser_navigate` to a known URL — and assert the result text contains no `Error`. Three
consecutive sessions passing back-to-back is the concurrency proof.

## Probing an MCP HTTP server in Python: read the SSE stream incrementally

`urllib`'s blocking `read()` on the response hangs because the server keeps the SSE stream open.
Read in chunks with a deadline and break once the buffer contains `"result"` or `"error"`, then
parse the `data: ` line and JSON-decode it.
