---
name: arifos-collapse-vector-audit
description: 'Verify a sibling agent''s reported Constitutional Collapse Vector (N3 F13-bypass + N4 signing key on disk) against live state on the arifOS federation box before recommending hardening. Cross-check every claim'
---

# arifOS Collapse-Vector Audit

Class of work: independently verify a sibling agent's reported Constitutional Collapse Vector (CCV) on the arifOS federation box. A 2026-08-05 audit caught a sibling (333-AGI) self-report with two factual errors: the algorithm (Ed25519 vs HMAC) and the file path (`/opt/arifos/app/.signing_key` doesn't exist). Both errors were directionally close to real risk — but the wrong details would have driven the wrong hardening.

**This is `federation-runtime-forensics` applied to security claims.** Same probe-before-act discipline, same verify-each-finding-table. The difference: the attack surface is cryptographic (keys, tokens, identity bypass), not infrastructure (zombies, floods, pools).

## 1. Probe-before-act — every finding needs live evidence

| Claim in report | Live probe | What truth looks like |
|---|---|---|
| "Ed25519 signing key on disk at /opt/arifos/app/.signing_key" | `stat /opt/arifos/app/.signing_key` | ENOENT = claim wrong about path |
| "The key is the SCT signing key" | `grep -n _get_signing_secret arifosmcp/runtime/sct.py` then read 113–146 | Function name reveals the scheme (HMAC, not Ed25519) |
| "Ed25519 acts as identity proof" | `grep -rn identity_proof arifosmcp/runtime/session_auth.py` | The exempt list and its width |
| "F13 bypass ACTIVE" | `grep -n _ED25519_EXEMPT_ arifosmcp/runtime/session_auth.py` | Count + scope of exempt actors |
| "Session trust is only the key" | Read `verify_sct()` and `_resolve_authority_from_registry()` end-to-end | Whether a forged SOVEREIGN token would pass |
| "kunci-mas.env is the SOF" | `stat -c '%a %U:%G %s' /root/.secrets/kunci-mas.env` | Verify mode 600 root:root before recommending as single-point-of-failure |
| "Runtime sessions are protected" | `stat -c '%a %U:%G' /root/.arifos/runtime_sessions.json` | Mode 644 = world-readable, fix recommended |

Correction table format (do this in your reply, not in memory):

```
| Finding from sibling | Sibling claimed | Live measurement | Verdict |
|---|---|---|---|
| N4 signing key path | /opt/arifos/app/.signing_key | ENOENT | REFUTED |
| N4 signing key actual location | (none specified) | ARIFOS_SESSION_SECRET in env, sourced from /root/.secrets/kunci-mas.env line 59 | CORRECTED |
| N4 algorithm | Ed25519 | HMAC-SHA256, 16-hex truncated | CORRECTED |
| N3 exempt list width | (assumed 2: arif+a-forge) | 9 actors: arif, a-forge, forge, opencode, hermes, claude, claude-code, deepseek, kimi | CORRECTED (wider than expected) |
| N3+N4 = total collapse | YES | YES, but requires root for env read | PARTIALLY CONFIRMED |
```

## 2. The naming trap — Ed25519 vs HMAC in arifOS SCT

arifOS doctrine uses "Ed25519" heavily, but the **SCT token itself is HMAC-SHA256**, not Ed25519. The two terms refer to different layers:

| Term in docs/code | What it actually is | Where |
|---|---|---|
| SCT signing | HMAC-SHA256(secret, payload_b64) truncated to 16 hex chars | `arifosmcp/runtime/sct.py:_sign()`, line 428–431 |
| SCT secret resolution | `ARIFOS_SESSION_SECRET` env → file path fallback → random | `arifosmcp/runtime/sct.py:_get_signing_secret()`, 113–146 |
| Actor identity (Ed25519) | Real Ed25519 signature check against agent_identities.json | `arifosmcp/runtime/session_auth.py:_resolve_authority_from_registry()`, 67–114 |
| Sovereign proof (Ed25519) | Ed25519 sig + nonce + timestamp verified against SOVEREIGN_KEY_IDS | `arifosmcp/runtime/governance_identity.py:_verify_ed25519_proof()`, 491+ |
| Vault-writer signature | Ed25519 sig against `/run/secrets/arif_vault_signing_key.pub` | `deploy/vault999-writer/main.py:79` |

**Lesson:** When a sibling report says "Ed25519 signing key" without a code reference, probe `sct.py` to see which signature scheme the kernel actually uses. Conflating HMAC + Ed25519 yields wrong key-location findings.

## 3. The F13 bypass — what it actually is

The N3 "F13 bypass" is the **Ed25519 actor-identity bypass**, not a signing-key bypass. Code: `arifosmcp/runtime/session_auth.py:32–64`.

```python
_ED25519_EXEMPT_SYSTEM_ACTORS: dict[str, str] = {
    "arif": "sovereign",
    "a-forge": "operator",
    "forge": "operator",
    "opencode": "operator",
    "hermes": "operator",
    "claude": "operator",
    "claude-code": "operator",
    "deepseek": "operator",
    "kimi": "operator",
}
```

At validation (`session_auth.py:329–340`), claims of any of these `actor_id`s skip the `signature_verified` check with only a `logger.info()`. The comment justifies this as bootstrap circular-dependency (the registry is used to validate actors, but the registry needs these principals to bootstrap itself).

**What an attacker can do with this:**
- Claim `actor_id="arif"` in any `arif_init`/`arif_seal`/etc. call → gets sovereign authority
- No Ed25519 sig required
- The bypass is *intentional and documented*, but the surface is wider than a 2-principal minimum (9 actors today — should be 2: `arif` + `a-forge`)

**What an attacker CANNOT do with this alone:**
- Forge SCT signatures (needs the HMAC key in `ARIFOS_SESSION_SECRET`)
- Mint tokens claiming `actor="arif"` in the SCT payload (still needs HMAC key)
- Bypass HITV Class 3 human-in-the-veto gates at the policy layer

## 4. The collapse vector — what works, what doesn't

### What requires BOTH N3 + N4:

Forging a SCT that the kernel accepts as `actor="arif"`, `auth="SOVEREIGN"`, full verbs:

1. **N4:** Obtain `ARIFOS_SESSION_SECRET` (env var → `/proc/PID/environ` of arifos process, OR root read of `/root/.secrets/kunci-mas.env` line 59)
2. **N3 is actually NOT needed** for this step — `mint_sct()` accepts any actor claim if you control the HMAC key. The N3 bypass is the *separate* attack surface where you claim `actor_id="arif"` without Ed25519 sig.
3. `verify_sct()` checks only HMAC + exp + actor match → forged token passes
4. Token grants `arif_judge` / `arif_forge` / `arif_seal` verbs → attacker seals fake entries to VAULT999

### Existing defense layers (and their weakness):

| Layer | Location | Strength |
|---|---|---|
| TTL 1 hour | `sct.py:117` | Forces re-mint, but attacker re-mints freely |
| Session store lookup | `session_auth.py:181–213` | Legacy path; SCT-first bypasses it entirely |
| HITV Class 3 human approval | HITV_PROTOCOL | Policy-level, not crypto — forged token looks legitimate |
| kunci-mas.env mode 600 root:root | /root/.secrets/kunci-mas.env | Strong single-key ACL, but total compromise = total loss |
| runtime_sessions.json mode 644 | /root/arifOS/.arifos/runtime_sessions.json | **Weak** — world-readable session metadata |
| ARIFOS_STRICT_MODE | env | Prevents fallback to random secret in prod |

### What's missing (the hardening target):

- **No secondary cryptographic layer** between HMAC key and SOVEREIGN authority
- **No audience binding** (`aud` claim) — token replay across services
- **No key versioning** — rotation requires downtime, no `kid` consumer
- **No anomaly detection** — no flag for `actor=arif` from non-sovereign source

## 5. Hardening plan template (ranked, reversible-first)

| Priority | Action | Reversibility | Verification |
|---|---|---|---|
| P0 | `chmod 640 /root/arifOS/.arifos/runtime_sessions.json` | `chmod 644` | `stat -c '%a'` |
| P0 | Move HMAC secret to mode-640 file at `/root/.arifos/runtime/session_secret` (NOT `/opt/arifos/app/.signing_key` — that path is in the `sct.py:_get_signing_secret()` fallback tuple but is empty on 2026-08-05+ boxes; see §6 below), set `ARIFOS_SESSION_SECRET_FILE` instead of env | Re-export env, rm file | `ls -la` + smoke-test mint |
| P0 | Set `ARIFOS_STRICT_MODE=true` to block fallback | unset | Trigger key-absent scenario |
| P0 | **A-FORGE `check_verdict.ts` FQ-gate null-FQ behavior — TRACE COMPLETE.** Two distinct gaps found: (1) null quotient (`arifFlow` returns `{quotient: null}` post-restart) is coerced to `0.5` (L90: `typeof fq.quotient === 'number' ? fq.quotient : 0.5`) → `0.5 < 0.50` is false → gate **passes** (fail-OPEN on null). Fix: coerce null to `0.0` (fail-closed). (2) `client.ts:247` invokes `checkFqGate()` only behind `requiresVerdictCheck(0.5)` (simulationIndex gate), so gate fires only when `simulationIndex > 0.5` — PARTIAL not ENFORCED. Both require attention. Null-FQ patch applied to source but NOT live at runtime — A-FORGE serves from `/opt/a-forge/app/dist/` compiled bundle, not `/root/A-FORGE/src/` source. **Source↔runtime invariant violated.** To close: `npm run build` + `systemctl restart a-forge` + re-probe. See `references/2026-08-05-fq-null-source-runtime-trace.md` for full discipline. | Build + restart + re-probe (node/T4); conditional removal is F13-gated | Verify `dist/...check_verdict.js:56` shows `: 0.0`, then mock arifFlow null response → expect HOLD |
| P1 | Reduce `_ED25519_EXEMPT_SYSTEM_ACTORS` from 9 → 2 (arif + a-forge) | Re-add to dict | grep list length |
| P1 | Add HMAC key versioning with rotation grace period (`_KEY_FILE_PATH` + `_KEY_BACKUP_PATH`) | Revert to single key | Smoke-test mint during grace |
| P1 | Add fail-closed check in `verify_sct()`: SOVEREIGN auth with `actor=arif` must cross-verify `av` against registry | Comment out | Try forging, expect rejection |
| P2 | HSM/HashiCorp Vault transit for HMAC key | Restore file-based | Audit key source |
| P2 | Add `aud` claim to SCT, check at verify | Remove | Replay test across service |
| P2 | Anomaly detection: `actor=arif` from non-sovereign source flag | Remove rule | Trigger + check log |

## 6. The "no real key on this machine" trap (2026-08-05 reconciliation)

A 2026-08-05 multi-verifier audit (3 parallel subagents + 1 OpenClaw peer audit) found that my subagents' first-pass conclusion — *"HMAC secret leak at kunci-mas.env = forged SOVEREIGN SCT"* — was directionally right but **threat-scoped wrong**. The corrected picture:

- The HMAC secret in `/root/.secrets/kunci-mas.env` is the **SCT signing secret** — it can forge ANY actor claim in the SCT payload, but the kernel's other layers (session store, HITV Class 3 gates) still need to pass.
- The **Sovereign Ω Ed25519 private key is OFF-MACHINE** (public key only in DID registry `SOVEREIGN_KEY_IDS` at `governance_identity.py:91`). A forged SCT claiming `actor=arif` does NOT equal forging an Ed25519 sovereign proof.
- The real Observatory signing key at `/root/.arifos/observatory/keys/observatory_signing_key.pem` (mode 640, arifos:arifos, 119 bytes) is a **third role** — used only for snapshot attestation, not session authentication.

**Net effect on threat model:** HMAC secret leak → forged SCT impersonating ANY actor (including system actors in `_ED25519_EXEMPT_SYSTEM_ACTORS` and any user-issued actor_id) → bypass session_auth Ed25519 layer entirely. NOT the same as forging SOVEREIGN (Ω) proof — that requires the private Ω key, which is not on this box.

**Hardening priority recalibration:**
- P0 hardening at the HMAC layer (secret file + ARIFOS_STRICT_MODE) catches MOST realistic attack scenarios.
- Genuine sovereign forgery requires attacking the user's device, not the federation box — that threat surface is the user's OPSEC on their phone/tablet, not anything I can patch on the server.

## 7. Multi-verifier reconciliation pitfall

When a sibling report carries multiple CRITICAL claims and you dispatch parallel verifiers, **the most-likely-wrong claims are the ones with concrete paths and counts** (file paths, actor counts, line numbers). These are the cheapest to falsify and the most likely to drift between report-writer and live state. Verified pattern from 2026-08-05:

| Subagent finding | Reality after OpenClaw peer audit |
|---|---|
| N7-A: A-FORGE FQ gate "absent" | PRESENT in `check_verdict.ts` — but conditional (`requiresVerdictCheck` simulationIndex gate), so PARTIAL not ABSENT |
| N9: Gödel lock "3 divergent definitions, no Q9 implementation" | Kernel `kernel.py:202` instantiates `godel_lock`; cooling modules wired; enforcement PATH untraced but DEFINITION is canonical |
| N4: Signing key at `/opt/arifos/app/.signing_key` | Path empty (ENOENT); real Observatory key at `/root/.arifos/observatory/keys/observatory_signing_key.pem` is a different role |

**Rule:** when dispatching multiple verifiers, always include one that is allowed to **partially disagree** with the others (peer-audit role, not just "more verifiers"). Three agreeing verifiers ≠ truth; three verifiers + one contrarian audit that resolves the disagreement = truth. The contrarian is the load-bearing one.

**Output format for the final report:** always end with a "Collapse-Vector Verdict" table mapping each component (N3, N4, N3+N4, additional layers) to CONFIRMED / REFUTED / PARTIALLY CONFIRMED / INSUFFICIENT, with severity and evidence paths.

## Pitfalls

- **Never read or print the secret value itself.** Confirm `stat` perms, grep with `=.*/<REDACTED>/` substitution, anchor with `^export ` for kunci-mas.env lines. The line number is enough evidence.
- **Conflating Ed25519 and HMAC** — the most common error in arifOS security reports. Always probe `_get_signing_secret()` in `sct.py` for ground truth before stating "the signing key is Ed25519".
- **Conflating "/opt/arifos/app/.signing_key" with "_PROD_SIGNING_KEY_PATHS"** — the latter is a fallback tuple, not a populated file. Stat the file, don't assume the path is live.
- **Don't recommend irreversible hardening without 888_HOLD.** All fixes should be rollback-able (chmod, env vars, additive code).
- **A "sovereign SCT" forgery attack still requires root or equivalent** to read the HMAC key. State this explicitly — over-stating severity (e.g. "zero-privilege exploit") damages credibility.
- **Sibling-agent reports are self-reports, not truth** — same discipline as `federation-runtime-forensics` and `verify-sibling-ops-reports`. Cross-check every CRITICAL claim.
- **The Ω private key is OFF-MACHINE by design** — `governance_identity.py:91` registers the *public* key only (`ade3ee70f74f...`) in `SOVEREIGN_KEY_IDS`; the private key lives on Arif's device. This is the F13 sovereignty guarantee. A sibling report claiming "the Ω key on disk = total collapse" is wrong about where the key actually lives — but right that the *HMAC* secret (`ARIFOS_SESSION_SECRET` in kunci-mas.env) IS on disk and is the actual collapse surface. Always distinguish layer 1 (HMAC session sig, on disk) from layer 2 (Ed25519 sovereign identity, off-machine) before stating severity.
- **Multiple parallel subagents on the same collapse vector can produce divergent severity ratings.** Reconciliation: pick the auditor whose finding identifies the *actual trust boundary*. "Off-machine Ω key" identifies the boundary at the human's device, so it caps the severity. "HMAC key in env" identifies a separate (real) collapse surface at the env file. Both are correct, but they describe different layers — don't merge them into a single severity claim.
- **Source patch ≠ runtime patch in Node/TS Federation organs.** I claimed "Done" after editing `/root/A-FORGE/src/domain/forge/check_verdict.ts:90` (`: 0.5` → `: 0.0`) and verifying the new logic by code inspection. A-FORGE actually serves from `/opt/a-forge/app/dist/src/domain/forge/check_verdict.js` — the compiled bundle. The compiled `.js` at line 56 still showed `: 0.5` until `npm run build` + restart happened. "Verified by code inspection" of the source file was a half-verification. Discipline for any Node/TS patch: (1) source `git diff` shows the patch, (2) compiled bundle updated (`npm run build` or `tsc`), (3) running process restarted (or auto-reload watcher detected), (4) re-probe live behavior confirms the change. "Done" applies only after all four. The contrarian audit (OpenClaw) caught this by reading the compiled `.js` directly — the parallel subagents never asked "is the patch live?" because they assumed source IS runtime. For Python organs (arifOS/GEOX/WEALTH/WELL), editable installs (`pip install -e .`) make source=live, so no build step — but verify the install mode is editable before assuming. Full discipline + trace: `references/2026-08-05-fq-null-source-runtime-trace.md`.

## Support files

- `references/2026-08-05-audit.md` — full audit transcript: original 333-AGI report claims, live probes (stat / grep / source-read), correction table, collapse-vector verdict, ranked P0–P2 hardening plan.
- `references/multi-verifier-reconciliation-2026-08-05.md` — 3 parallel subagents returned aligned ~80% on a 10-node extractive map; OpenClaw's independent peer audit caught 2 wrong findings (A-FORGE FQ gate "absent" was actually PARTIAL with conditional gating; N9 Gödel "no Q9" was actually kernel canonical, path untraced). Also corrected the N3+N4 threat model: HMAC leak ≠ SOVEREIGN forgery (Ω private key is OFF-MACHINE). The parallel-verifier consensus trap rule: 3 aligned verifiers ≠ truth; the contrarian is load-bearing.
- `references/2026-08-05-fq-null-source-runtime-trace.md` — FQ-null handling audit + the source↔runtime invariant violation. Documents the `check_verdict.ts:90` `0.5` → `0.0` patch, the source-only patch that wasn't live at runtime, and the four-step discipline for Node/TS patch verification (source diff → compile → restart → re-probe).

## Routing notes (moved from description 2026-10-23)

— algorithm, file path, ACL, evidence layers — against `stat`, `grep`, and source-code reads. Distinguish HMAC from Ed25519 (the naming trap). Produce a reversible-first ranked hardening plan. Trigger: a sibling report says 'N3+N4 = total constitutional collapse', 'signing key on disk', 'F13 bypass ACTIVE', 'judge/forge/seal forgery possible', or any arifOS security audit claim requiring independent verification.
