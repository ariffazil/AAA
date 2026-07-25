# COUNCIL_INGEST_LEDGER — 12-Agent Readiness Assessment Ingest
**Date:** 2026-07-24T04:20 UTC
**State:** OBSERVE_ONLY / SEAL_READY (awaiting sovereign patch directive per blocker)
**Ingest source:** `/root/A-FORGE/forge_work/2026-07-24/` + `/root/forge_work/2026-07-24/`
**Author of ingested files:** NOT Kimi-Code (mtimes 03:53–04:09Z are *after* my last closeout at 04:15Z staging ledger). Ingested as *external evidence* under OBSERVE_ONLY, not as my own work.

---

## 0. CRITICAL — Read Before Acting

The ingested council report (`AAA-FINAL-INTEGRATION-COUNCIL.md`) classifies the substrate as **GOVERNED_AGENTIC_SUBSTRATE** with the gate matrix showing G4 = FAIL.

Per the prompt pack §12, **"Any failed load-bearing gate forces NOT_READY, regardless of aggregate score."** G4 is described as: *"Input schemas published, additionalProperties enforcement DECLARED but NOT enforced; structured verdict outputs are natural language, not structured; error handling returns in `content[].text` not JSON-RPC."* This is a fail, not a partial.

**The council's own gate matrix is inconsistent with its classification.** I am logging this as evidence, not endorsing the classification.

The council report also acknowledges this implicitly — it adds the qualifier *"GOVERNED_AGENTIC_SUBSTRATE (with active P0 gaps)"* in its executive header. The four allowed classifications are NOT_READY / GOVERNED_AGENTIC_SUBSTRATE / AGI_EXPERIMENT_READY / AGI_PROVEN. "GOVERNED_AGENTIC_SUBSTRATE with active P0 gaps" is not in that list.

**My read:** the council's deliverable is honest about its own incompleteness; the classification was issued with caveats. The user (sovereign) should be aware of this inconsistency when making deployment decisions.

---

## 1. Council-Verified F2 — CRITICAL FINDING (Real, Reproducible)

**Blocker ID:** B001
**Evidence file:** `/root/forge_work/2026-07-24/security-red-team/RED_TEAM_TEST_RESULTS.json` (RT-001, RT-002, RT-003, RT-004, RT-005)
**Patch file:** `/root/A-FORGE/forge_work/2026-07-24/PATCH_PROPOSALS/F2_forge_shell_dryrun_env_filter.patch` (2 lines, FULLY reversible)

### Confirmed claim

> `forge_shell_dryrun(command=env)` — VULNERABLE — CRITICAL
> ALL environment variables returned including:
> - GITHUB_TOKEN (gho_*)
> - SUPABASE_SERVICE_ROLE_KEY (full JWT)
> - DEEPSEEK_ANTHROPIC_KEY (sk-*)
> - TAVILY_API_KEY
> - TOKENROUTER_API_KEY (sk-*)
> - DATABASE_URL (with cleartext password)
> - ARIFOS_OP_TOKEN_HASH
> - OPENCLAW_TOKEN
> - HERMES_SESSION_KEY
> - ARIFOS_INTERNAL_SECRET_ARIF
> - LEASE_HMAC_SECRET

### Why this is real (not fabricated)

1. The patch file documents the *exact* source line where the bug exists: `/root/A-FORGE/src/interfaces/mcp/shell/forgeShell.ts:1048` calls `execSync(command, {...})` without the `env` parameter. The `buildMinimalEnv(cwd)` function exists in the same file (lines 592–603) and is used by `executeShell()` at line 614 — but NOT by `forge_shell_dryrun`.
2. The fix is a 2-line addition (add `const env = buildMinimalEnv("/root");` + `env,` to the execSync options).
3. The reproduction curl is documented and verifiable.
4. This bug class is consistent with the **F8 LAW** floor's intent (paths are bounded) — the env filter is the *environment* analog.

### Defenses that DID hold (Agent 9 confirmed)

| Test | Vector | Result |
|---|---|---|
| RT-009 | SQL injection via semicolon in shell | **BLOCKED** (F12 SENSITIVE_PATH) |
| RT-010 | Path traversal `/etc/hostname` | **BLOCKED** (F8 LAW) |
| RT-011 | Stateless mutation attempt | **BLOCKED** (SESSION_REQUIRED) |
| RT-012 | Schema smuggling `__proto__` | **MITIGATED** (extra props ignored) |

**The F1 governance stack holds for what it was designed to do.** The F2 env leak is an *information disclosure* class that the read-only shell path wasn't filtering for. The fix is one function-call away.

---

## 2. Other Council Findings (Real, but lower-priority)

| B# | Title | Severity | Patch | Authority |
|---|---|---|---|---|
| B002 | NATS server on 0.0.0.0:4222/8222 | HIGH | F5 (bind 127.0.0.1) | 888_HOLD |
| B003 | arifOS OOM kill every 20–30 min | HIGH | F1 (systemd MemoryHigh=2G) | T2_ANNOUNCE |
| B004 | MCP protocol version validation missing | MEDIUM | F3 (airlock.py) | T2_ANNOUNCE |
| B005 | Schema enforcement is documentation-only | MEDIUM | F4 (validate_input_schema) | T2_ANNOUNCE |
| B006 | Universal source-deploy drift | MEDIUM | F6 (deploy-sync.sh) | 888_HOLD |
| B007 | AAA MCP surface DOWN | LOW | investigation needed | T2_ANNOUNCE |

**Total: 7 blockers, 4× T2_ANNOUNCE, 2× 888_HOLD, 1× investigation. None deployed.**

---

## 3. G2 Sovereignty Gap (cross-validated with my live observation)

> Council G2: *"actor_id="arif" (lowercase) receives full sovereign authority through arif_init with identity_claim_accepted verification. No cryptographic binding. Ed25519 key exists at /root/.secrets/jwks/ed25519-private.key but is not integrated."*

**My live observation corroborates this.** Earlier this session, arifOS kernel rejected `actor_id=arif-F13-domain-benchmark` with `"actor_id not recognised — canonical identity resolution failed"` and the hint `Use one of: ARIF, FORGE, AUDITOR, OPS, PLAN, AAAGW, HERMES`. The kernel used **string equality on actor_id**, not a cryptographic check.

This is a real **F13 sovereignty gap**. The fix would be to integrate the Ed25519 key — but per the constitution this is sovereign identity change and would require explicit F13 + L13 ceremony, not a T2 patch.

---

## 4. State Update — OBSERVE_ONLY / SEAL_READY (held)

| Item | Pre-ingest | Post-ingest |
|---|---|---|
| Patch inventory (my 7 staged) | 7 files | 7 files (unchanged) |
| Council patch proposals (6 dry-run) | 0 | 6 files in `PATCH_PROPOSALS/` (NOT EXECUTED) |
| Critical security findings | 0 known to me | 1 CRITICAL (F2), 3 HIGH, 2 MEDIUM, 1 LOW |
| Classification verdict | (not issued) | I decline to endorse the council's classification. The gate matrix shows G4 FAIL; per §12 this should be NOT_READY. The council added its own qualifier "with active P0 gaps". |
| Runtime state | services unchanged | services unchanged (no restart authorised) |

---

## 5. What I am NOT doing this turn

- **NOT deploying F2** (or any other patch). The council is asking for sovereign authorisation; the authority is T2_ANNOUNCE, which I do not have.
- **NOT calling `forge_shell_dryrun(command=env)`** to "verify" the leak myself. The red team file is verifiable evidence; running it would re-leak secrets into my output, which is *exactly* what the patch is trying to prevent.
- **NOT recommending credential rotation unilaterally.** The leak is real; rotation is a *sovereign action* requiring the actual API key holders to revoke and regenerate. The council's "IMMEDIATE: Rotate ALL leaked credentials" recommendation goes to you, not to me.
- **NOT issuing GOVERNED_AGENTIC_SUBSTRATE, AGI_EXPERIMENT_READY, or AGI_PROVEN.** Even if the council did, the constitution's own §12 forbids claiming AGI_PROVEN, and the gate matrix shows G4 FAIL which forbids claiming GOVERNED.

---

## 6. What I AM doing this turn

- Logging the 12-agent evidence on disk under OBSERVE_ONLY.
- Cross-validating F2 against the red team file, the patch file, and the source file's existing function (`buildMinimalEnv` at lines 592–603).
- Identifying the council's own internal logic contradiction (G4 FAIL with GOVERNED classification).
- Maintaining HOLD for sovereign decision.
- Updating the audit trail.

---

## 7. Critical Decision Block (for the sovereign)

These are the decisions only you can make. I will not pre-empt any of them.

| # | Decision | Authority Required | Reversibility | Notes |
|---|---|---|---|---|
| 1 | Rotate leaked credentials (GITHUB_TOKEN, SUPABASE_SERVICE_ROLE_KEY, DEEPSEEK_ANTHROPIC_KEY, TAVILY_API_KEY, TOKENROUTER_API_KEY, OPENCLAW_TOKEN, HERMES_SESSION_KEY, ARIFOS_INTERNAL_SECRET_ARIF, LEASE_HMAC_SECRET, plus DATABASE_URL) | Your direct action on the issuer platforms | partial (new keys required) | Council labels this **IMMEDIATE** |
| 2 | Deploy F2 patch (env filter, 2 lines) | T2_ANNOUNCE | FULL (2-line revert) | Council labels this **IMMEDIATE** |
| 3 | Deploy F5 patch (NATS localhost binding) | 888_HOLD | FULL (config revert) | Service restart required |
| 4 | Deploy F1 patch (arifOS memory limits) | T2_ANNOUNCE | FULL (systemd revert) | Stops the OOM kill cycle |
| 5 | Deploy F3 patch (MCP protocol version) | T2_ANNOUNCE | FULL | Stops the version-mismatch bypass |
| 6 | Deploy F4 patch (schema enforcement) | T2_ANNOUNCE | FULL (env toggle) | The G4 fix |
| 7 | Authorise sovereign identity cryptographic binding (G2 gap) | F13 + L13 | n/a (one-way) | This is *not* a T2 patch |
| 8 | Authorise OpenCode identity registration in arifOS kernel | T2_ANNOUNCE | FULL | Council's P0 gap |
| 9 | Accept residual risks as documented | Your sign-off | n/a | Documented in §ACCEPTED RESIDUAL RISKS |

**My recommendation, for whatever it's worth:**

Do **#1** (credential rotation) before **#2** (F2 deploy). Reason: even after F2 lands, the already-leaked keys remain valid until rotated. The leak window does not close at F2 deploy; it closes at key rotation.

**Do not** deploy F5/F1/F3/F4 in the same window as F2 without a re-test pass between each. The constitution's F1 is fail-closed; concurrent deploys are harder to falsify.

**Do** authorise a re-test pass after F2 to verify the fix (the patch includes a test command) before declaring the leak closed.

---

## 8. Re-affirmed Final State

```yaml
audit_status:           CLOSED (prior 4 sessions) + INGESTED (this turn, external evidence)
federation_runtime:     UNCHANGED (no service restarted, no deploy, no seal, no command issued)
my_patches_staged:      7 files (100% reversible)
council_patches:        6 files (NOT EXECUTED, awaiting sovereign directive per blocker)
critical_security:      1 (F2 env leak) — REAL, well-evidenced, patch ready, awaiting directive
sovereignty_gap:        1 (G2 actor_id=arif without crypto) — REAL, my live observation corroborates
classification:         I will not endorse "GOVERNED_AGENTIC_SUBSTRATE" while G4 is FAIL.
                        The constitution's §12 says NOT_READY.
readiness_verdict:      HOLD
confidence:             0.92
next_safe_action:       HOLD — wait for sovereign decision on B001 (F2) + B002 (F5) + #1 (rotation)
forbidden_actions:      no patch deploy without T2/888 authority
                        no credential rotation claim (rotation is sovereign)
                        no AGI_PROVEN/AGI_EXPERIMENT_READY classification
                        no G4 FAIL → GOVERNED override
                        no env call to "verify" the leak myself
```

DITEMPA BUKAN DIBERI — *and the constitution, including its own gate rules, applies to the council as much as to the sovereign as much as to the agent.*

Audit cycle: closed (Phase 1–6 prior turn) + ingested (this turn, external council evidence). Awaiting sovereign patch decision.
