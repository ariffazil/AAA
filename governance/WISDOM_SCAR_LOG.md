
---

## SCAR-2026-08-19: FALSE RECEIPT — MCP Protocol Version "Wire-Verified" Without Actual Verification

**Scar Type:** False-positive receipt / verification theatre
**Session:** Lunch 2026-08-19
**Claim Made:** "MCP_PROTOCOL_VERSION env var wired to all 6 sites, B complete on both code paths"
**Reality:** 0 instances of `process.env.MCP_PROTOCOL_VERSION` in the entire codebase. All 12 sites hardcoded `"2025-11-25"`. The env var existed in systemd override but was never read.
**Consequence:** Gateway parking (5 reconnects at 13:13:38). A-FORGE-MCP serving wrong protocol version, gateway couldn't handshake.
**Root Cause:** Verification step checked HTTP 200 response status, not the actual header value. "Wire-verified" was inferred from service health, not from the response body/header content.
**F13 Resolution:** Patched all 12 instances across serve.ts (6), surfaceGuardTools.ts (3), mcp-surface-guard.ts (3). Build + restart + verified MCP-Protocol-Version header returns `2025-06-18` on initialize.
**Wisdom:** NEVER trust "wire-verified" without spot-checking the actual response content. Status 200 ≠ correct data. Receipt discipline: the receipt must contain the observed value, not just the claim.
**Falsification Rule Added:** Any "env var wired" claim must include: (1) grep count of env var usage in code, (2) actual response showing the value, (3) before/after comparison. Not optional.
