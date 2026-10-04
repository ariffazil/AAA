# arifOS Kernel Stabilization — Session Receipt (2026-08-07)

This is the condensed session record for the **8-rule stabilization
doctrine** forged on 2026-08-07. It is not a transcript — it is a
receipt: every claim has a file:line or a probe signature, and any
claim here was either verified live or marked as open.

## Session timeline (8 commits, source = runtime at `2d35ca5a5`)

```
367b4c38f  STAB P0  — 7 invariants forged from Opus 5 + Hermes receipts
a012d7bee  STAB P0b — pin constitutional_check on effective_verdict
77abc7fde  STAB P0c — kill residual 0.65/0.5 fabricated defaults (10 modules)
253f7f342  STAB P0b kernel_intercept — floor_passed from effective_verdict
05b6b433f  STAB P0b floor_passed canonical at last writer (sibling)
371fa711b  STAB P0d — floor_passed reads same source as override (two-writer close)
b893b8933  STAB P0e — kill delta_S=0.0 fabrication in wrapper
2d35ca5a5  STAB P0e — propagate delta_S=None to wrapper math
```

## Live receipts (probed at `2d35ca5a5`, session SEAL-a046990ac3da48d0)

| Invariant | Before | After | File |
|---|---|---|---|
| substrate | DEGRADED | HEALTHY | `/health` |
| drift | `drift_detected` | `aligned` | `/health` |
| floor_passed dual-truth | `True` alongside failed_floors | `False` + `hold_required:True` | `tools.py:4976`, `arif_kernel_intercept.py:750` |
| actor_id persistence | `arif-fazil -> arif` rewrite | `arif-fazil` preserved through observe | `session_standing.py:332` |
| metacognition.confidence | `0.65` fabricated | `None` (UNMEASURED) | `tools.py:8081` |
| metacognition.confidence_band | `ADVISORY_ONLY` | `UNMEASURED` | `tools.py:7810` |
| metacognition.evidence_strength | `medium` on 0 evidence | `unknown` | `tools.py:7856` |
| delta_S | `0.0` fabricated | `None` honest | `tools.py` lines 4868, 5261 |
| EVIDENCE_HASH_MISMATCH gate | absent | rejects with Rule #6 reason | `tools/judge.py:1091` |
| EVIDENCE_EMPTY gate | absent | hard HOLD before LLM | `tools/judge.py:1075` |
| weight tables in payload | SUBSTRATE_WEIGHT visible | `_`-prefixed, hidden | `kernel_envelope.py:591` |
| semantic-parser proposal | (new layer) | declined — fix foundation first | session text |

## Open items (probed, not yet fixed)

- **Mode-routing gap** — `arif_observe mode=entropy_dS` accepts the
  parameter in the MCP schema but the handler receives `mode=None`
  from the dispatcher. Probe shows `result.delta_S:None` even with
  explicit mode. Handler logic is correct; façade mapping needs audit.
- **L11 AUTH drop** — session_id minted by `arif_init` is rejected by
  the validator on the next tool call. Likely session-registry
  thread-local vs process-global state mismatch. Affects `arif_think`,
  `arif_route`, `arif_memory` flow.
- **`arif_forge` / `arif_seal` return shape** — return raw string
  `"888_HOLD: ..."` instead of structured JSON, so the liveness probe
  can't parse `effective_verdict`. Need `verdict` field in the
  response shape, or convert string response into structured envelope.
- **Timestamp type drift** — `standing.issued_at` reported as ISO in
  one tool, epoch int in another (same session, same probe).
- **Silent band downgrade** — `band: FULL -> LIMITED_MUTATE` with
  `state_version` unchanged. No concrete repro yet.
- **Conformance spine exit-1** — `make deploy-local` exits 1 on
  sovereign NON-ISSUE (vault pre-migration gaps, ruled 2026-06-05).
  The make target should not block on ruled anomalies.

## The 8 rules (codified)

See SKILL.md §2. The full live receipt for each is in this file. The
meta-rule (Rule #8: never predict a probe result) emerged from this
session specifically — it caught the agent itself when an external
model proposed a predicted verdict and Hermes relayed it instead of
running the probe.

## Open architecture question: why the agent still has work to do

The kernel now returns honest absences (None) instead of fabricated
numbers (0.0, 0.65, 0.5). But the **envelope is still bloated** with
metacognition boilerplate and nine_signal glossaries. Opus 5's verdict:
"~5% of ~3,300 tokens were load-bearing." That is a token-economics
target for STAB P0f — strip the glossaries, keep the load-bearing
fields, reduce the per-call token cost by ~60%.

## Cross-references

- `references/session-receipt-2026-08-07.md` (this file)
- `scripts/arif_kernel_liveness.py` (Rule #4 enforcement)
- `scripts/probe_kernel_contradictions.py` (Rule #7 enforcement —
  probe-to-witness harness for classes 1-6)
- `kernel-security-claim-audit` §5f for kernel-specific audit pattern
- `mcp-tool-differential-testing` for broader MCP content-sensitivity