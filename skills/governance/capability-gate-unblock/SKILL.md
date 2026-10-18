---
name: capability-gate-unblock
description: "Use when a capability is HOLD but authorized — open gates."
---

# Capability gate unblocking (governed mutation lanes)

## When to use
Arif says agents must be able to do X (send email, mutate a file, push a repo), but the tool returns HOLD / "not found" / guard error. Opening a governed lane is a MULTI-LAYER job; stopping after the first fix leaves it acah — declared open, still closed.

## The rule (Arif hates acah-acah)
Never claim a capability works from a code diff, a `tools/list` success, or "I re-enabled the handler." A tool can be LISTED and still be gated inside the handler. The ONLY proof a lane is open is a live roundtrip that reaches the real downstream system.

## Trace ALL gate layers before declaring done
A governed mutation in A-FORGE (execution organ, MCP `:7072`) can be held by five independent layers. Check each — a fix to one does not open the others:

1. **aThinkGuard** (`src/domain/governance/aThinkGuard.ts` `check()`) — GOVERN-mode destructive tool returns HOLD ("destructive tool requires human approval") unless it has a mode-aware exemption (the read-only shell/git/docker bypasses). An autonomous mutate/send needs an explicit tool-name exemption here.
2. **actionClassifier + gateMutate** — `actionClassifier.ts` maps `forge_<name>` modes to OBSERVE/EXECUTE_*/IRREVERSIBLE; the capability handler's own `gateMutate()` returns fail-closed `passed:false` for IRREVERSIBLE verbs. Opening the classifier does NOT open `gateMutate` — two separate layers. Also watch `startsWith` classification bugs: a verb named `draft_send` can be misclassified REVERSIBLE and slip past, when it actually mutates.
3. **Registration in core.ts** — `src/interfaces/mcp/core.ts` calls `registerXxxTools(server)`. A past ZEN sweep may have COMMENTED OUT the whole registration, making the tool absent from `tools/list` entirely (not gated — missing). Re-enable the registration line, not just the handler.
4. **Bridge internal gate** — the python bridge may require `actor_id` for mutations (L11 AUTH) and HOLD with "actor_id is required". Default `actor_id` in the handler before `bridgeCall`.
5. **Token/credential wiring** — the bridge's `_load_creds` scans a FIXED path list and uses `Credentials.from_authorized_user_file`. The live token is often in flat `{scope: "...", access_token: ...}` form; convert to `{type:"authorized_user", client_id, client_secret, refresh_token, token, token_uri, scopes:[]}` and write it to one of the scanned paths.

## Verify by reaching the real API (domain error ≠ gate error)
After opening the gates, call the tool with an invalid-but-real payload. The RESULT tells you which layer is still closed:

- **DOMAIN error** (e.g. Gmail "Invalid To header", a 400 from the vendor API) = the request LEFT the building and every gate opened. You're done — the only remaining problem is the fake test payload.
- **HOLD / A_THINK_GUARD / IRREVERSIBLE_VERB / "not found"** = at least one gate layer is still closed. Keep tracing.
- **`bridge_failed: <exception>`** = the bridge RAN and reached the real system (gates open), look at the exception itself, not the gates.

Never declare a gate open from `tools/list` success alone.

## Commit & deploy
After the fix: `tsc` → `copy-handwritten-js` → restart the MCP unit → re-probe the live API with the invalid-payload call. Commits in the federation are identity-gated: use `/root/scripts/git-lane <lane> commit -m "..."` (plain `git commit` is blocked); commits are LOCAL until pushed.
