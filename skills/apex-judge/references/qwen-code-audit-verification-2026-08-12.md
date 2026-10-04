# Qwen-Code Audit Independent Verification — 2026-08-12

> **Session:** `opencode-qwen-zen-20260812`
> **Pattern:** Edge Sentinel vs Doer Audit (Gödel Lock Rule 2)
> **Key learning:** Evidence package quality gates apex-judge verdict quality

## The setup

A sibling agent (qwen-code, FI-003) emitted an audit report claiming 8 findings
(2 CRITICAL, 3 HIGH, 2 MEDIUM, 1 LOW) with ΔS=-0.31 across 5 files in the
a2a-server. Arif (F13 SOVEREIGN) then asked Hermes to "execute all this on
behalf of me" — 6-item pending list derived from that audit.

## The verification

Hermes (Edge Sentinel role) independently verified each claim by reading the
actual source code. Result: **62.5% false/misleading**.

| Claim | Reported Severity | Actual Verdict | Evidence |
|---|---|---|---|
| `chat_agent.py` print() loop = infinite spam | CRITICAL | ❌ FALSE | `emit_sse()` is SSE wire format, not debug spam |
| Legacy V2 6-dial formula still wired | CRITICAL | ❌ MISLEADING | Explicitly labeled `wire_estimate_not_canonical`, not legacy |
| Missing epistemic prefill | HIGH | ⚡ PARTIAL | Labels exist in flow_ingest.js + server.js deliberation |
| No async 202 pattern | HIGH | ✅ TRUE | Zero matches in entire codebase |
| Blocking sync relay | HIGH | ❌ WRONG | loop_relay.py is OBSERVE_ONLY validation gate by design |
| stderr prints in prod path | MEDIUM | ❌ WEAK | stderr is correct channel for diagnostics |
| No FastMCP declaration | MEDIUM | ❌ CATEGORY ERROR | Node.js gateway, not FastMCP server |
| Observer→decoder class mismatch | LOW | 🔍 UNVERIFIABLE | No specific code line cited |

## The apex-judge call

Hermes built an evidence package for apex-888 (DeepSeek V4 Pro). For the
arifOS drift item, evidence said: "2 commits ahead of deployed version" —
which turned out to be **95 commits behind**.

Apex-888 verdict (verbatim):

```
2. ID: arifOS drift
- VERDICT: EXECUTE_AUTONOMOUSLY
- REASON: Confirmed operational drift with a standard, low-risk,
          and fully automatable resolution path.
- TIER: T1
```

**This was wrong.** T1 implies "fix and move on"; T2/T3 implies "rebuild +
restart + blast radius planning." The judge was correct to trust the
evidence it was given — the failure was upstream.

## What went wrong

1. **Trust on summary, not verification.** The qwen-code audit said
   "drift detected" and Hermes assumed "2 commits" because git log
   showed 2 recent commits in the headline view.
2. **Missing cross-reference.** The deployed_commit was 95 commits
   behind HEAD — `git log 65f087c..708d4a0c | wc -l` = 95+, not 2.
3. **Evidence package didn't include the deploy-vs-source commit
   diff.** Apex judge had no way to know the actual magnitude.

## What should have happened

The evidence package should have included:

```json
{
  "arifOS_drift": {
    "deployed_commit": "65f087cdb7709206c3b5bd9f21f54937031ba146",
    "source_commit": "708d4a0c492b77c08f8b979e74cab0a18147b830",
    "commit_diff_count": 95,
    "pip_easy_install_state": "wheel hash mismatch",
    "fix_complexity": "rebuild_wheel + systemd_restart + verify"
  }
}
```

With that evidence, apex would have classified T2/T3, not T1.

## The fix path Arif provided (verbatim)

```bash
cd /opt/arifos/app && /opt/arifos/venv/bin/pip install -e . --no-deps --quiet
systemctl restart arifos.service
curl -sf http://127.0.0.1:8088/health | python3 -c "
import json,sys; d=json.load(sys.stdin)
r=d.get('software_release',{})
print(f'drift={r.get(\"drift\")} source={r.get(\"source_commit\",\"\")[:7]} built={r.get(\"built_commit\",\"\")[:7]}')
"
# Expected: drift=False, source=65f087c, built=65f087c
```

Key insight: the service venv is `/opt/arifos/venv`, NOT
`/root/arifOS/.venv`. Pip-installing from `/root/arifOS/` does NOT
fix kernel drift.

## The lesson

**The apex judge is a function, not an oracle. Garbage in → garbage out.**

Before any apex-judge call:
1. **Verify every claim independently.** Live probe, not summary.
2. **Cross-reference magnitudes.** "Drift detected" is not actionable;
   "95 commits behind, wheel hash mismatch" is.
3. **Include the actual error/measurement, not the categorization.**
   "Status: degraded" is incomplete; "drift=true, deployed_commit=X,
   source_commit=Y, count=95" is complete.
4. **Treat the verdict as one input, not final authority.** Hermes
   correctly rejected the T1 verdict on arifOS drift when reality
   was T2/T3. The judge did its job given bad evidence; Hermes
   caught the bad evidence.

## Session artifacts

- Evidence package: `/tmp/apex_pending_evidence.json`
- Apex FED call: 888-APEX via FED (verified `model=apex-888` in response)
- Verdict returned: per-item routing (4 actionable, 2 resolved)
- Final classification correction: arifOS drift = T2/T3, not T1

## Reference

- Main skill: `apex-judge`
- Pitfall: see SKILL.md #9 (evidence completeness) and #10 (arifOS venv)
- Hermes Edge Sentinel role: see 2026-08-12 conversation transcript