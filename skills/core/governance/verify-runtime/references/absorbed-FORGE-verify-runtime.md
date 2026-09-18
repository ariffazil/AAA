# Absorbed: FORGE-verify-runtime

> **Provenance.** Pre-merge body of the `FORGE-verify-runtime` skill, tombstoned 2026-09-16T22:46:00Z by Wave 2 (`moved_to: core/governance/verify-runtime/SKILL.md`).
> Recovered verbatim from `/root/.hermes@entropy-wave2-pre-act-20260916T144144Z:skills/FORGE-verify-runtime/SKILL.md` — content was never carried into the target by the
> original consolidation; recovered 2026-09-17 to complete the recorded merge.
> Original sha256 (tombstone `sha256_before`): `19d695c89fdc4ddfd411d95eb13e748176f0ee4cf061de3ddcb8ddb2583f62d1`
> Recovery sha256: `19d695c89fdc4ddfd411d95eb13e748176f0ee4cf061de3ddcb8ddb2583f62d1`
> The `FORGE-verify-runtime` routing name stays retired — this file is a reference, not a skill.

---

# Verify Runtime — Verification Is the Terminal State

> **"I changed it" is not done. "It's fixed and confirmed" is done.**
> **Lower entropy = verify every claim before accepting it.**

A task is done when tests pass, health checks green, and behavior is proven. This skill enforces the third leg — the terminal step that separates assumed-done from actually-done.

## The Verification Contract

Every agent that performs a mutation MUST run verification before claiming completion.

```
Mutation → Self-check → Health probe → Behavior smoke → REPORT
  ^                                                        |
  └────────────── NOT DONE until REPORT says GREEN ────────┘
```

**Rules:**
1. Never stop at "I applied the fix" — stop at "I confirmed the fix works"
2. If you cannot verify the result, you have not finished
3. If verification fails, revert the change and diagnose, don't patch over it
4. The verifier agent (Auditor) must be DIFFERENT from the mutator agent (Engineer) for critical systems

## Steps
1. `/root/apex-health.sh` — federation-wide port probe (all 8 organs)
2. Per-organ health probes (parallel where possible):
   - arifOS:   `curl -s :8088/health | python3 -m json.tool`
   - GEOX:     `curl -s :8081/health | python3 -m json.tool`
   - WEALTH:   `curl -s :18082/health | python3 -m json.tool`
   - WELL:     `curl -s :18083/health | python3 -m json.tool`
   - A-FORGE:  `curl -s :7071/health | python3 -m json.tool`
3. Drift check: compare git source SHA vs runtime (`git log -1 --format=%H` vs installed artifact)
4. One behavior smoke per touched organ (e.g. for arifOS: session init round-trip)
5. Report: green/yellow/red per organ + 1-line summary

## Verification Loop
- **All green → claim done** with structured receipt
- **Any yellow** → log cause + continue, flag in summary. Do not leave yellow uninvestigated.
- **Any red** → 888 HOLD, rollback via organ's deploy-local, log `{who, what, why, result}`

## Output Format
```json
{
  "who": "<agent_id>",
  "what": "verify-runtime",
  "why": "post-deploy verification",
  "result": {
    "organs": {"arifos": "green", "aforge": "green", ...},
    "drift": "none",
    "smoke_tests": {"arif_init": "pass"},
    "verdict": "done"
  }
}
```

## Failure Modes
| Mode | Action |
|------|--------|
| Service slow to start | 30s grace, then red |
| Port collision | Check Caddy/port registry, surface to human |
| Drift detected | Run `make deploy-local` in the affected organ |
| Health endpoint missing | Check organ's main.py / server.js for `/health` route |
| Smoke test fails | Revert the change, diagnose root cause |
| Cannot verify | Do not claim done. Escalate. |

## Reference
- Federation health: `/root/apex-health.sh`
- Per-organ runbooks: `/root/RUNBOOK.md`
- Drift detection: `drift-watch` skill


## Lessons (auto)

*Auto-ingested from agent learning. F2-gated: every entry carries evidence.*
- **[2026-09-15] kimi-code/FI-008** (evidence: 2026-09-04: opencode-db-pre-purge .gz showed mtime Aug 24 + vanished process mid-verify; gzip -t OK, gzip -l = exact 6014107648B payload. Documented gzip behavior (mode+timestamps ): gzip copies the SOURCE file's mtime onto the compressed output. A .gz whose mtime predates your session is NOT evidence of corruption or a stalled job — check process, payload size (gzip -l), and CRC (gzip -t) before declaring failure. Forensic cost when unknown: 3 tool calls.
- **[2026-09-15] hermes-rsi-loop** (evidence: [{"layer": "artifact", "source": "session:tool:terminal", "excerpt": "+++ b//root/.hermes/scripts/apex-zen-bridge-score.py\\\\\\\\\\\\\\\\n@@ -149,11 +149,26 @@\\\\\\\\\\\\\\\\n \\): DEAD_POINTER observed 3x — impact=unresolved_ref. First surface: session:tool:terminal — all four checks passed, but independence is NAME-LEVEL ONLY (same author) — verdict is PROVISIONAL: may enter the capability graph, may NOT record a survival event
- **[2026-09-15] hermes-rsi-loop** (evidence: [{"layer": "artifact", "source": "session:tool:terminal", "excerpt": "+++ b//root/.hermes/scripts/apex-zen-bridge-score.py\\\\\\\\\\\\\\\\n@@ -149,11 +149,26 @@\\\\\\\\\\\\\\\\n \\): DEAD_POINTER observed 3x — impact=unresolved_ref. First surface: session:tool:terminal — all four checks passed, but independence is NAME-LEVEL ONLY (same author) — verdict is PROVISIONAL: may enter the capability graph, may NOT record a survival event
- **[2026-09-15] hermes-rsi-loop** (evidence: [{"layer": "artifact", "source": "session:tool:terminal", "excerpt": "+++ b//root/.hermes/scripts/apex-zen-bridge-score.py\\\\\\\\\\\\\\\\n@@ -149,11 +149,26 @@\\\\\\\\\\\\\\\\n \\): DEAD_POINTER observed 3x — impact=unresolved_ref. First surface: session:tool:terminal — all four checks passed, but independence is NAME-LEVEL ONLY (same author) — verdict is PROVISIONAL: may enter the capability graph, may NOT record a survival event
- **[2026-09-15] hermes-rsi-loop** (evidence: [{"layer": "artifact", "source": "session:assistant", "excerpt": "ib/arifos/vault/outcomes.jsonl.DEPRECATED (2026-05-14); /root/VAULT999/vault999_legacy.jsonl (read-only, 2026-05-2): DEAD_POINTER observed 1x — impact=unresolved_ref. First surface: session:assistant — all four checks passed, but independence is NAME-LEVEL ONLY (same author) — verdict is PROVISIONAL: may enter the capability graph, may NOT record a survival event
- **[2026-09-15] hermes-rsi-loop** (evidence: [{"layer": "artifact", "source": "session:tool:terminal", "excerpt": "/forge_work/ and /root/forge_work/ for items from this week that never got resolved\\\\n4. SYSTEM EVOLUTION — ): DEAD_POINTER observed 1x — impact=unresolved_ref. First surface: session:tool:terminal — all four checks passed, but independence is NAME-LEVEL ONLY (same author) — verdict is PROVISIONAL: may enter the capability graph, may NOT record a survival event
