# Federation Architecture Audit — Pattern from AAA-SESSION-20260808

Origin: 2026-08-08 session audit-validated a complete federation topology
(arifOS, A-FORGE, GEOX, WEALTH, WELL, AAA, FED, FLAME, arifFlow, SIGNAL, FRAME,
APEX, i-ARIF-CANON). Eight audits, all live-probed, all receipt-backed.

## Session shape (anchors)

When bang asks "what is X?" or "audit X", the request is NOT a documentation
question. It is a **runtime architecture question**. The response contract is:

1. **Probe live runtime first.** `curl :8088/health`, `ps aux`, `ss -tlnp`,
   `find /root -iname '*<thing>*'`. NOT doc reads.
2. **Layer the probe table.** Show the live values (port, process, status,
   tools, version) in a grid. No prose only.
3. **Then interpret.** Map the runtime evidence to the doctrinal categories.
4. **Then verdict.** One word — SEAL / PARTIAL / HOLD / VOID.
5. **Then zen.** What to delete or merge next.

If instead the response leads with documentation, the next session will
be dominated by a re-correction. The user's pattern: "Show me, don't tell
me about it."

## The 5-axis verdict for federation audits

For any "what is this service / role / corpus" question:

| Axis | Question to answer |
|---|---|
| **Implementation** | What file/process/port/runtime backs it? |
| **Constitutional role** | What responsibility does it serve? |
| **Layer** | In the canonical stack, where does it sit? |
| **Drift** | What diverged from declared canon? |
| **Minimum irreducible** | What stays if everything else is deleted? |

Every audit answer covers all 5 axes. The "minimum irreducible" question is
the one bang keeps asking — keep it short.

## Concrete patterns to record

### Pattern: "Show me the 8 tools, not the docs"

User asked for "all arifOS tools". Right answer was a probe + table, not a
docs summary. The probe was:

```bash
SID=$(curl -si :8088/mcp -X POST \
  -H 'Content-Type: application/json' -H 'Accept: application/json' \
  -H 'MCP-Protocol-Version: 2025-11-25' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize",...}' | grep -i 'mcp-session-id' | ...)
curl -s :8088/mcp -X POST -H '...' -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'
```

Note the session-handshake dance: AAA rejects without `Accept: application/json`,
and many servers use `mcp-session-id` header for the session. The probe MUST
include the post-`init` notification or the second call fails.

### Pattern: "AAA has 0 MCP tools — say so directly"

This came up several times. The right answer: probe and report "0 tools" — not
"AAA IS a registry" (which is interpretation, not observation). The
interpretation comes AFTER the count.

### Pattern: "Show the drift, don't describe it"

User asked about platform drift: `curl :8088/health` returns
`deployment_drift_status: aligned`. The right answer: paste the live value, name
the source_commit and deployed_commit, show whether they match. Don't just
say "consistent" — show the SHA.

### Pattern: "Verify the 2-pair drift is real"

When HF page says 119, local says 117 — the right answer is to surface the
discrepancy explicitly, not paper over it. 2-pair drift between local build
and HF upload is typical corpus-evolution drift. Note it as a finding, not
an error.

## Pitfalls (verified this session)

- **Documentation is a hypothesis, not evidence.** `AGENTS.md` says FED is at
  `:7074`. Reality is `:7074` for the MCP server, `:4001` for the clean
  proxy, `:4000` for the LiteLLM gateway (via Tailscale). Three different
  things, one name. The doc is wrong about at least one. Probe all three.

- **"Healthy" health response is not a verdict.** All 8 organs could be
  "healthy" and still be drift_detected. Read the `deployment_drift_status`
  field separately from `status`. The kernel can be "status: healthy +
  drift_detected" simultaneously. Both fields matter.

- **AAA has 0 MCP tools but 38 A2A agents.** The "AAA is the federation
  hub" framing is wrong when measured by tool surface. Surface only the
  observations, then interpret. Don't lead with interpretation.

- **The kanon (ORGAN.md) is wrong about 30% of the substrate.** SIGNAL
  :18084, FRAME :18085, FLAME's ADVISORY authority, FED's true port
  (:4001, not :7074) — all absent from the canonical map. The audit
  surfaced this. The "kanon" is a working draft, not oracle. Always
  cross-check against `:8088/health` and `ss -tlnp`.

- **MCP session requirement is server-specific.** Some servers accept
  bare `tools/list` (GEOX, WEALTH). Others require `Mcp-Session-Id`
  (arifOS, A-FORGE). Some require `Accept: application/json, text/event-stream`
  header. The probe must enumerate these — first call 406, second call
  200 is normal, NOT a server bug.

## The 8 real moving parts (zen reduction)

When asked "what's the smallest architecture," the answer is:

1. arifOS :8088 (kernel — 8 tools, gates enforced)
2. A-FORGE :7071/7072 (executor — 124 tools)
3. GEOX :8081 (earth — 35 tools)
4. WEALTH :18082 (capital — 8 tools)
5. WELL :18083 (vitality — 10 tools)
6. arifFlow :7073 (metabolism — FQ monitoring)
7. VAULT999 (filesystem — immutable)
8. FED :4001 (intelligence allocation — 14 tools)

Everything else (AAA, FLAME, SIGNAL, FRAME, i-ARIF-CANON, AGI/ASI/APEX labels)
is either a substrate, a registry, or a corpus. They don't authorize.

## Anti-patterns to avoid

- **Don't say "kernel" if it's an envelope.** arifOS is the kernel.
  i-ARIF-CANON is the corpus. AAA is the registry. Words matter.
- **Don't conflate 888_HOLD with rejection.** 888_HOLD is a sovereign
  signal — the human must approve. Rejection is automatic. Different
  mechanics, different status codes.
- **Don't inflate ΔS.** Real ΔS this session: -0.3156 (governance health
  measured). Reported: -0.6 (flagged as inflated by user). The skill
  prescribes `match reported × [0.0-0.5]` for inflation-factor adjustment.

## Verification recipes (saved for next session)

Live recipe: arifOS tools (8 canonical verbs):

```bash
curl -si :8088/mcp -X POST \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'MCP-Protocol-Version: 2025-11-25' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize",
       "params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"probe","version":"1.0"}}}' \
  | grep -i 'mcp-session-id' | awk '{print $2}' | tr -d '\r'
```

(Note: arifOS does NOT require `Accept: application/json, text/event-stream`
but including it doesn't hurt. The 406 issue was AAA, not arifOS.)

Live recipe: APEX apex_scalars:

```bash
curl -sf :8088/health | python3 -c "import sys,json; print(json.load(sys.stdin)['apex_scalars'])"
```

Returns: G, C_dark, W3, h, QDF with value+status.

Live recipe: federation port scan:

```bash
ss -tlnp | grep -E 'LISTEN' | awk '{print $4}' | sed 's/.*://' | sort -n | uniq
```

This session: 76 listening ports. The audit identified 8 critical, 6
relevant, and 62 entropy.

## Carry-forward

The session closed with these open items remaining for the next session:

- `pre_execution_gate.py` working tree has undefined helper calls
  (`_resolve_independent_evidence`, `_resolve_previous_stage_verified`)
  that NameError on first MUTATE call. Recommend Option B: commit safe
  parts, revert broken parts.
- BIJAKSANA exists in essay but `h: UNMEASURED` in apex_scalars. Either
  implement or document.
- I-ARIF-CANON Phase 2 QLoRA fine-tune pending.
- 6 audit items (A1/A4/A5/A6/B1/B4) carry-over.

These are session-end state, not retention patterns. New session should
re-probe rather than trust carry-over.
