# 10-Node Extractive Map — Delegated Audit, 2026-08-05

Context: a sibling agent pasted a 10-node "extractive nodes" risk register. Each node was a sentence claim (TTL, file path, gate status, FQ number, etc). Two F13-gated items (N3, N4) made SEAL-grade decisions gated on the report's accuracy — so every claim had to be verified before any action.

## Step 0 — Ground-probe in parent context (2-4 quick probes)

Before spawning subagents, run your own cheap probes to:

1. Cross-check the report's headline numbers yourself
2. Find the parent correction / reconciliation table the final reply will use
3. Give the subagents starting points so they don't re-discover or contradict

| Probe | Tool | What it told us |
|---|---|---|
| FQ live | `curl :7073/health` | Report said 0.424 verify>execute; live showed `quotient: null`, `verdict: CAUTION`, `execute_count: 2`, `verify_count: 1` after a 77s restart. FQ number was on a dead window. |
| Signing-key path | `stat /opt/arifos/app/.signing_key` | ENOENT — file does not exist. Report wrong on path. |
| A-FORGE FQ gate | `grep -n FQ_GATE_THRESHOLD /root/A-FORGE/src/domain/forge/check_verdict.ts` | Returns `FQ_GATE_THRESHOLD = 0.50` at L68. Gate already wired. Report wrong on N7. |
| SCT TTL | `grep -n ttl /root/arifOS/arifosmcp/runtime/sct.py` | `DEFAULT_TTL_SECONDS = 3600` at L36 — but `consent_token.py:69` is `ttl_seconds: int = 300`. Two layers, both numbers are wrong if reported in isolation. |

Result: ~40% of the report's claims were already refuted before any subagent spawned. Saved 3 subagent calls worth of redundant work.

## Step 1 — Dispatch 3 parallel subagents

`delegate_task` with `tasks=[...]`, READ-ONLY constraints baked into every brief. Each brief carried:

- **Your prior probe findings** as starting point (so they don't re-discover)
- **Output contract** — explicit schema: `VERDICT (CONFIRMED/REFUTED/PARTIAL/UNVERIFIABLE) + severity + evidence file:line + quoted value`
- **Hard READ-ONLY constraints** — "do NOT modify files, restart services, or print secret values — report paths + permissions only"
- **The corrected reality** as the baseline ("don't re-discover, use as starting point")

Cluster split:

- **Agent 1**: 4 kernel/security claims (N2, N3, N4, N9 — TTL, F13 bypass, signing key, Gödel lock)
- **Agent 2**: 4 federation/routing claims (N1, N7, N8, FQ numbers — DeepSeek monopoly, FQ gate, memory asymmetry, FQ=0.424)
- **Agent 3**: 4 agent-layer/meta claims (N5, N6, N10, collapse vector — ephemeral enforcement, orchestrator choke, sycophancy, N3+N4 severity)

## Step 2 — Don't wait or poll

The batch returned as one consolidated message after ~343s. Truncation hid the middle (subagent output saved to `/usr/local/lib/hermes-agent/profiles/aaa-hermes/cache/delegation/subagent-summary-*.txt`). The per-claim evidence is in the truncated middle — always read the full cache file.

## Step 3 — Reconcile across auditors

The three subagents disagreed in *different* places, not the same place. Sample reconciliations:

| Finding | Agent 1 verdict | Agent 2 verdict | Agent 3 verdict | Reconciliation |
|---|---|---|---|---|
| N4 collapse vector | REFUTED (path ENOENT, 4 fallback paths, dangerous random fallback) | (not in scope) | CONFIRMED w/ mitigations (HMAC key in env, F13 bypass removes last constitutional guard) | Both partially right. **Agent 3's "off-machine Ω key" finding REFUTES the total-collapse severity even though the HMAC-on-disk finding is real.** The collapse requires root to read the env, not zero-privilege exploit. |
| FQ 0.424 / verify>execute | (not in scope) | REFUTED (stale, inverted: live showed 2 restarts at :58, null quotient, cache showed execute=12>verify=10) | (not in scope) | Direct refutation. The report inverted execute and verify AND cited a number from a dead window. |
| FQ gate at A-FORGE | (not in scope) | REFUTED — fully wired in source AND dist with same 0.50 threshold | (not in scope) | Direct refutation of "AAA done, A-FORGE needed". |
| Gödel lock | ENFORCED in arifOS kernel | (not in scope) | ABSENT for `forge_seal` (three divergent definitions) | Both right, different components. Kernel enforces; A-FORGE `forge_seal` path doesn't. |

**Lesson:** when subagents disagree, look for which one has the *sharpest* security model. "Off-machine Ω key" is a sharper finding than "HMAC in env" because it identifies where the actual trust boundary sits. Two auditors agreeing on a path doesn't mean a third auditor's distinguishing observation is wrong.

## Step 4 — Consolidated verdict table

Build this directly from the per-claim verdicts. Lead with the verdict, then the table, then the action ranking.

| Node | Report claim | Live truth | Verdict | Evidence |
|---|---|---|---|---|
| N2 | SCT TTL 3600s | 3600 (sct.py:36) but consent_token.py:69 default 300 | CONFIRMED (sct.py layer) | `arifosmcp/runtime/sct.py:36` |
| N3 | F13 bypass ACTIVE | Ed25519 verification already enforced (forge.py:800-870) | REFUTED | `arifosmcp/tools/forge.py:800-870` |
| N4 | Key at /opt/arifos/app/.signing_key, gates everything | File ENOENT; 4 fallback paths; HMAC-SHA256 not Ed25519; `ARIFOS_SESSION_SECRET` in env | REFUTED (path/algorithm) | `sct.py:99-146`; `stat` ENOENT |
| N9 | Gödel lock defined but unverified | Fully enforced in arifOS kernel (`godel_lock_gate.py`); A-FORGE `forge_seal` path is ABSENT | PARTIAL | `runtime/godel_lock_gate.py:189-200` |
| N1 | DeepSeek monopoly, fallbacks untested | Fallbacks declared; cascade wrapper present; 0 integration tests | PARTIALLY CONFIRMED | `fed_cascade.py:124-216` |
| FQ numbers | FQ 0.424, verify=9 > execute=8 | Stale; live null quotient after 2x restart; cache shows execute=12>verify=10 | REFUTED (both stale AND inverted) | live `:7073/health`; cache `flow_state.json` |
| N7 | AAA FQ done, A-FORGE needed | A-FORGE wired in source AND dist with 0.50 threshold | REFUTED | `check_verdict.ts:68,130` + dist `:40,99` |
| N8 | Memory asymmetry FIXED via 15s injection | 15s probe writes `memory_tiers`; Cockpit.tsx does NOT consume | PARTIALLY CONFIRMED | writer `cockpit_probe.py:149,260`; missing consumer `Cockpit.tsx:325,391,395,433` |
| N5 | forge_ephemeral exists but unenforced | Doctrine exists; zero runtime gate on mission count | CONFIRMED | `forge_skill_contract.py`; zero `forge_register()` call sites |
| N6 | Orchestrator choke | FQ/MCP OBSERVE bypasses exist; inter-organ relay lacks fast-path | PARTIALLY CONFIRMED | `fq_gate.js:14`; `mcp_apps_tools_call.js:43-62` |
| N10 | Sycophancy not automated | Zero pre-response check in any live code | CONFIRMED | zero grep hits in `a2a-server/`, `arifosmcp/`, `HERMES/scripts/` |

## Step 5 — Rank what actually deserves action

The report ranked its own gaps (F13-gated items first). That ranking was off because the report's premises were off. Re-rank from ground truth:

1. **kunci-mas.env protection** — the actual collapse surface (HMAC key for SCT signing), not the file paths the report chased. **F13-gated** (irreversible key rotation, secret distribution).
2. **FQ-null behavior at A-FORGE** — what happens when arifFlow restarts mid-operation? Gate code handles it (fail-closed UNREACHABLE) but unprobed. **No F13** — code review + test.
3. **Agent registration gap** — cards on disk, registry empty. The federation is forged but not walked. **F13** — SEAL-token per agent.
4. **Everything else** — real but not architecturally threatening.

## What the parent should never do

- Average subagent verdicts (one CONFIRMED + one REFUTED ≠ "PARTIAL", read each)
- Treat the consolidated message as the full output — the cache file has the per-claim evidence
- Bounce the final ranking back to Arif with options ("register agents, retire default profile, HOLD 888") — this is the "verify-sibling-ops-reports §3 EXECUTE-don't-ask" anti-pattern. State the ranking + reversible defaults, let Arif veto if needed.
- Open the reply with a flatter toward the *sibling report* (§4.2). Even if the report had real findings, the opener is the same trap.
