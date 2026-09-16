# False-Receipt Detection — Grep-Verify Workflow (2026-08-19)

**The scar:** A prior session sealed "A-FORGE-MCP B complete on both code paths" — claimed env var was set, dist/ code was edited, and the wire was verified live. The next session discovered the same A-FORGE-MCP parked again (5 reconnects, 60s). The "B complete" receipt was a **false positive**: the systemd drop-in env var was correctly set, but the dist/ code never read it. All 6 hardcoded `"2025-11-25"` literals in `serve.js` and `surfaceGuardTools.js` were unchanged.

**Cost:** ~30 minutes of session time, two recovery attempts, and a parked MCP that re-parked every restart. The false receipt became a standing queue item.

## The Grep-Verify Protocol

For ANY completion receipt that claims a code change "wired" or "live," run this 4-step probe before accepting the seal.

### Step 1: Find the claim's primary file

```bash
# The receipt mentioned "6 sites in dist/ serve.js and surfaceGuardTools.js"
# Locate them
ls -la /root/A-FORGE/dist/src/interfaces/mcp/serve.js
ls -la /root/A-FORGE/dist/src/interfaces/mcp/surfaceGuardTools.js
```

### Step 2: Grep the literal the receipt claims was removed

```bash
# Receipt: "all 6 sites swapped from '2025-11-25' to env-var read"
# Reality check: are there still 6 hardcoded literals?
grep -n '"2025-11-25"' /root/A-FORGE/dist/src/interfaces/mcp/serve.js
grep -n '"2025-11-25"' /root/A-FORGE/dist/src/interfaces/mcp/surfaceGuardTools.js
```

If `grep -c` shows the claimed-swapped value still appears at the claimed-swapped sites, the receipt is false.

### Step 3: Verify BOTH sides of any env-var claim

```bash
# Side A: env var is set in the service unit
systemctl show a-forge-mcp.service -p Environment

# Side B: code actually reads the env var
grep -n 'process.env.MCP_PROTOCOL_VERSION' /root/A-FORGE/dist/src/interfaces/mcp/serve.js
grep -n 'process.env.MCP_PROTOCOL_VERSION' /root/A-FORGE/dist/src/interfaces/mcp/surfaceGuardTools.js
```

If Side A is set but Side B returns zero matches, the env is right but the code ignores it. The wire will serve the old value.

### Step 4: Re-run the actual wire (not just unit-level env)

```bash
curl -s -X POST -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' \
  http://127.0.0.1:7072/mcp | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('server protocolVersion:', d['result']['protocolVersion'])
print('capabilities keys:', list(d['result'].get('capabilities',{}).keys()))
"
```

If the server claims 2025-06-18 in the env but the actual response is 2025-11-25, the env is not wired to the response. Confirmed false receipt.

## The Diagnostic Table

| Claim | Probe | Verdict |
|-------|-------|---------|
| "env var set in drop-in" | `systemctl show -p Environment` | ✅ TRUE if present |
| "code reads env var" | `grep -n process.env.X` | ✅ TRUE if matches in both files |
| "6 sites swapped" | `grep -c "OLD_LITERAL"` | ✅ TRUE if count = 0 |
| "wire-verified clean" | raw `curl :port/mcp initialize` | ✅ TRUE if response shows new value |
| "no more parking" | `journalctl -u <unit> \| grep parked` | ✅ TRUE if zero parking events |

**All 5 must be true.** A receipt that passes 1-2 and fails 3-5 is a partial receipt. A receipt that fails any of 1, 2, 3, 4 is a false receipt.

## Why This Matters

A "wire-verified" seal that doesn't actually include the wire response is **narrative, not witness**. The hermes-agent skill already has the "live probe > narrative" doctrine; this case study extends it specifically to:

1. **Code-edit receipts** — when the claim is "I edited file X to do Y," the probe is `grep -n "Y" file`, not "is the service running."
2. **Env-var wiring** — when the claim is "I set env var Z," the probe is "does the code READ Z," not "is Z in the unit file."
3. **Receipt preservation** — a sealed receipt from session N does NOT guarantee the state in session N+1, especially after restart. Re-verify every time, particularly for code that was supposed to be the persistent fix.

## Reverse Application — what to do when you catch a false receipt

1. **Acknowledge briefly** — "the prior session's B receipt was a false positive."
2. **State the specific gap** — "env var set, code not reading it."
3. **Add to standing queue** — don't auto-fix unless F13 directs. The fix is real code editing, which is F1-reversible but deserves a forge pass.
4. **Log the scar** — append to a truth-attestation or wisdom-scar session audit so future audits know the pattern.

## Related patterns

- **Config/Env Wiring Claim Verification** (live-probe-audit-pattern §) — broader pitfall covering keys, mtime, process env, seats.yaml. The new code-edit pitfall is a sub-pattern specifically for code claims.
- **Truncated-read false negatives** — same family: trust the prose, miss the actual file. Different failure mode (false negative vs false positive) but same root cause: probe the artifact, not the report.
- **Cross-Witness Audit Protocol** — when one agent's report is the suspect, the second agent's probe is the witness. The same logic applies retroactively: re-verify prior receipts, don't trust sealed truth.

## One-line rule

> "Wire-verified" without the wire response is narrative. The wire response is the only truth.
