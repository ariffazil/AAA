# Collapse-Vector Multi-Verifier Reconciliation — 2026-08-05

## Context

A 333-AGI self-report carried a 10-node extractive map of the arifOS federation. Hermes dispatched three parallel subagents (collapse-vector, FQ+Gödel, tail-nodes) for independent verification. After ~4 minutes, all three came back with ~80% agreement. Then Arif pasted OpenClaw's independent peer audit — which caught findings the three subagents missed.

## What the subagents got right

1. **N3 F13 bypass CONFIRMED** — `session_auth.py:32-64`: 9 actors bypass Ed25519 (arif, a-forge, forge, opencode, hermes, claude, claude-code, deepseek, kimi). Correct.
2. **N1 DeepSeek monopoly CONFIRMED** — MODEL_TIERS.json L516 "BAILIAN SPOF" still current; zero cascade test logs. Correct.
3. **N5 capability obesity CONFIRMED** — forge_ephemeral lifecycle = doctrine only. Correct.
4. **N6 orchestrator choke CONFIRMED** — predict_gate.js L76,161 has OBSERVE classification, orchestrator never calls it. Correct.
5. **N10 sycophancy CONFIRMED** — anti-sycophancy in SOUL.md L118, zero runtime enforcement. Correct.

## What the subagents got wrong (caught by OpenClaw)

| Finding | Subagent verdict | OpenClaw correction | Root cause |
|---|---|---|---|
| **N4 signing key path** | `/opt/arifos/app/.signing_key` — path refuted (ENOENT) | Real Observatory key at `/root/.arifos/observatory/keys/observatory_signing_key.pem` (640, arifos:arifos, 119B). Sovereign Ω private key OFF-MACHINE. | Subagent stopped at "path wrong" without finding the real key hierarchy |
| **N7-A FQ gate at A-FORGE** | ABSENT | PRESENT in `check_verdict.ts` (L68, L126, L152) — but conditional on `requiresVerdictCheck(0.5)` via `client.ts:247`. Correct verdict: PARTIAL. | Subagent searched for `fq_gate.js` pattern from AAA, didn't grep `check_verdict.ts` |
| **N9 Gödel lock** | "3 divergent definitions, no Q9 implementation" | Kernel `kernel.py:202` instantiates `godel_lock`; cooling modules wired; enforcement PATH untraced. Correct verdict: UNCERTAIN, not ABSENT. | Subagent grepped A-FORGE only, didn't check arifOS kernel source |

## What the subagents got wrong on N3+N4 (the collapse-vector itself)

The subagent said: "HMAC leak at kunci-mas.env = forged SOVEREIGN SCT = total constitutional collapse."

OpenClaw corrected: the HMAC leak can forge ANY actor claim in the SCT payload (impersonate `actor=arif` or `actor=hermes` etc.), but:
- The **Sovereign Ω Ed25519 private key is OFF-MACHINE** (public key only in DID registry)
- The real Observatory key at `/root/.arifos/observatory/keys/` is a THIRD role (snapshot attestation, not session auth)
- An attacker who obtains the HMAC key can bypass `session_auth.py` Ed25519 checks, but **cannot** forge an Ed25519 sovereign proof
- The correct threat model is: HMAC leak → impersonate any actor via forged SCT → bypass session_auth layer → not equivalent to forging sovereign proof

Net effect: SEVERE but BOUNDED (requires root on the federation box). Not "total constitutional collapse" (requires external key exfiltration from the user's device).

## Why the subagents all missed the same things

1. **Shared investigation bias**: all three subagents started from the same canonical paths (`sct.py`, `check_verdict.ts` assumed absent because they searched for `fq_gate.js`-equivalent filenames, `godel_lock` in A-FORGE tree). They didn't cross the codebase boundary to check arifOS kernel source.
2. **Confirmation cascade**: when subagent A found "key path wrong" and subagent B found "gate absent," there was no cross-check against a different code tree. OpenClaw started from a different premise (observatory key hierarchy) and found the real key.
3. **Missing the "where does it actually live" move**: subagent A correctly identified that `/opt/arifos/app/.signing_key` is ENOENT, but didn't then search for where the signing secret actually resolves. The "path wrong" finding should have triggered the search for the real path, not just a verdict of "refuted."

## The rule (extracted)

1. **When a claimed path is ENOENT, that's the START of the investigation, not the end.** "Path doesn't exist" → "where does it actually live?" — always follow through to the real resolution path.
2. **Parallel subagents on the same codebase share the same grep bias.** Always include a peer auditor that can check from a different starting point (different code tree, different canonical assumption, different question).
3. **The security model matters more than the finding.** "HMAC key on disk" is a finding. "Does that HMAC key leak = SOVEREIGN compromise?" is the security model question. The security model answer changes the severity from SEVERE to MODERATE.
4. **Three agreeing verifiers ≠ truth.** The subagent consensus was 80% accurate. The 20% error was the part that mattered most (collapse-vector severity, FQ gate enforcement).
