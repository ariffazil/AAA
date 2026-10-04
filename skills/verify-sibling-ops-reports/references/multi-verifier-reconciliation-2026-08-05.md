# Multi-Verifier Reconciliation — 2026-08-05

## The Trap

When a sibling dispatch fans out to N parallel verifiers and they return
similar verdicts, the consensus is **not independent confirmation** — they
may share the same blind spot. Three aligned subagents on the same problem
produce one conclusion, not three. The fact that they "agree" tells you
nothing about whether they were wrong together or right together.

## The Pattern (worked example)

A 333-AGI self-report on 2026-08-05 carried a 10-node extractive map of
the arifOS federation. Hermes dispatched three parallel subagents
(collapse-vector, FQ+Gödel, tail-nodes), each given a slice of the map to
verify. All three came back ~80 minutes later with aligned verdicts:

| Node | Self-report claim | Three subagents agreed | OpenClaw peer audit |
|---|---|---|---|
| N4 | "Signing key at /opt/arifos/app/.signing_key, 32 bytes gate everything" | Path ENOENT; real key is `ARIFOS_SESSION_SECRET` env from kunci-mas.env | **CORRECTED** further: the Observatory key at `/root/.arifos/observatory/keys/observatory_signing_key.pem` (119B, 0640, arifos:arifos) is a *third role* — snapshot attestation, not session auth. HMAC leak ≠ sovereign forgery. |
| N7-A | "FQ gate at A-FORGE — absent" | All three agreed: ABSENT | **REFUTED**: `A-FORGE/src/domain/forge/check_verdict.ts:68,126,152` exists, but conditional on `requiresVerdictCheck(0.5)` in `client.ts:247`. Correct verdict is PARTIAL. |
| N9 | "Gödel lock — defined, runtime unenforced" | All three said: 3 divergent definitions, no Q9 implementation | **REFRAMED**: kernel `kernel.py:202` instantiates `godel_lock`; cooling modules wired; enforcement PATH through `arif_seal` is untraced but DEFINITION is canonical. Verdict should be UNCERTAIN, not ABSENT. |

## What the contrarian audit caught

Three things that the three aligned verifiers all missed:

1. **A-FORGE FQ gate EXISTS** — my subagents stopped at "no `fq_gate.js`-equivalent file" and concluded absent. OpenClaw grepped `check_verdict.ts` and found the gate with explicit "constitutional, not advisory" doctrine comment. The conditional invocation (`requiresVerdictCheck`) is what makes it PARTIAL, but the gate function exists.

2. **Threat-scoping was wrong** — my subagents all said "HMAC leak = forged SOVEREIGN SCT = constitutional collapse." OpenClaw correctly distinguished the three key roles (SCT HMAC, F13 Ed25519 sovereign, Observatory attestation) and noted the sovereign Ω private key is OFF-MACHINE. The attack surface is impersonate any actor via forged SCT, not forge sovereign proof.

3. **The path-empty finding mattered more than the path-named finding** — when the claimed path doesn't exist (`/opt/arifos/app/.signing_key` ENOENT), the next move is to ask "where does the real key live?" not "the claim is wrong, ship the P0 hardening." The real key location changed the entire hardening template.

## The Rule

When dispatching parallel verifiers on a multi-claim report:

1. **Give each verifier a slice, not the whole.** Cross-coverage wastes tokens.
2. **Include one peer-audit-role verifier** that is *expected to disagree* — i.e., one verifier whose job is to challenge the others' conclusions, not produce its own independent audit. This is the contrarian seat.
3. **After parallel verifiers return, run the contrarian audit on their consensus** — read each verdict, identify which claims have falsifiable specifics (file paths, line numbers, counts), and probe those specifics against live state.
4. **The most-likely-wrong claims are the ones with concrete paths and counts.** These are the cheapest to falsify and the most likely to drift between report-writer and live state. Probe them first.

## When the rule doesn't apply

- Single-source report with no time pressure → verify yourself, don't fan out
- The claim is conceptual / not falsifiable in the moment → fan-out is fine, but each verifier should attack from a different angle
- The risk is reversible → ship the hardening on the consensus and audit after

## Cost note

Parallel-verifier fan-out costs ~$0.10–0.30 per verifier (LLM calls + token
overhead). The contrarian audit costs ~$0.05–0.10 (smaller, targeted
probes). The discipline is worth it when the report drives F13-gated
decisions — those are the ones where a wrong premise becomes a sealed
wrong hardening.

## Reference

- The collapse-vector skill §6 and §7 were added to capture this exact pattern
- The collapse-vector threat-model correction (HMAC vs Ed25519 vs Observatory roles) is now embedded in `arifos-collapse-vector-audit` §2 and §6
