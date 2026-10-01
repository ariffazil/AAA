# Scar 2026-10-01 — ACT_GATE_RECURSIVE_IDENTITY_BLOCK

> **Status:** SCAR CANDIDATE — sovereign prohibition on human-key-management pattern; live ACT_GATE block documented; identity contract executed up to ACT mint.
> **Severity:** HIGH (blocks WARGA Identity Spine contract Steps 3-5)
> **Detection method:** Live probe 2026-10-01 after sovereign directive "ok do all. SAH"
> **Forged by:** kimi-code/FI-008

---

## The failure class

A citizen's identity certification requires the arifOS kernel to mint an ACT (Arif's Capability Token). ACT mint requires `arif_init` to return `actor_verified=true`. `actor_verified=true` requires the kernel to verify a cryptographic signature over an `arif_init` challenge. The signature is produced by the citizen's runtime against the private key matching the registered `identity_proof`. The private key is held by the citizen's runtime (agent-held pattern, matches hermes/codex/openclaw 2026-07-09).

This is a CIRCULAR DEPENDENCY when:

1. The citizen's identity is `trust_tier=UNVERIFIED` (no key registered).
2. The arifOS kernel has `L11 SCT mismatch` (cannot mint sovereign-ACT for sovereign-chat ratification path).
3. To register a key requires `forge_agent mode=register`, which requires `session_token=ACT`, which requires `actor_verified=true`, which requires a key, which requires registration.

In this state the future CLI bound is **closed**. Citizen cannot register identity. Identity contract cannot close. Sovereign-chat ratification cannot be kernel-acted-on. Stage 0 (drift-reconcile-unblock-test-2026-10-02) is the upstream gate.

---

## Live probe evidence (this session)

#### Probe 1 — Sovereign keys exist on the system

```
/root/.secrets/aaa-identity/keys/
├── vault_attest_ed25519.pem (organ-level attestation key)
├── vault_attest_ed25519.pub.pem
├── fi-003_private.pem + fi-003_public.pem  (qwen-code, agent-held)
├── gemini-cli_private.pem + gemini-cli_public.pem
├── arif_private.pem  (sovereign-held, chmod 600 root:root, ED25519 private)
└── arif_public.pem   (sovereign-public, ED25519, fingerprint sha256:2d19a2fbeaa21e5918d96906726743bd5d89ec059a983157bfa86bd73dd27af9)
```

Sovereign keys are NOT absent. They were forged 2026-07-19 (`arif_private.pem`) and refreshed 2026-09-04 (`arif_public.pem`). The sovereign's "I don't remember any key whatsoever" is a *memory* not *existence* statement.

#### Probe 2 — Sovereign's `arif_init` returns `actor_verified=false`

```
arif_init(mode='preflight', actor_id='kimi-code/FI-008', ...)
  → effective_verdict: HOLD
  → actor_verified: false
  → session_token: null
  → authority: OBSERVE_ONLY
  → constitutional_check: substrate_state=DEGRADED drift=true
  → reason_evidence: cause=DEPLOYMENT_DRIFT
```

The sovereign's existing keys (in `/root/.secrets/aaa-identity/keys/arif_*.pem`) are NOT in the live runtime arifOS registry. So `arif_init` cannot find the sovereign to attest the session.

#### Probe 3 — `forge_agent mode=register` returns ACT_GATE_REQUIRED

```
forge_agent(mode='register', agent_id='FI-008', identity_proof='sha256:0203...')
  → ERROR ACT_GATE: ACT_REQUIRED: Tool forge_agent requires session_token (mint via arif_init)
  → action_class: EXECUTE_REVERSIBLE
  → adat_gate: ACT_REQUIRED
```

This is the closed circle: registering requires ACT, ACT requires verified actor, verified actor requires key, key requires registration.

#### Probe 4 — Stage 0 falsification test scheduled

CHRON event `drift-reconcile-unblock-test-2026-10-02` (days_until=1) is the booked test event. It is the upstream gate that, when cleared, unblocks L11 SCT reconcile.

---

## The sovereign's prohibition

Sovereign directive 2026-10-01: *"i dont remember any key whatsoever, u find urself sampai jumpa, ni benda yang aku benci nak buat, aku benci dan haramkan untuk future agent btw"*

Translation: "I don't remember any key whatsoever. You find yourself until you find one. This is what I hate doing. I hate and prohibit this for future agents."

**This is a constitutional direction. The sovereign prohibits a failure class: "agents being put in the position of needing human key management".**

Per Canon #0 (Constitutional Complexity Budget, F13_SEAL 2026-09-21), any new law must eliminate a demonstrated failure class. This prohibition:
- (a) eliminates the failure class of "humans-must-remember-keys" — yes, by sovereign direction.
- (b) compiles into an enforceable mechanism — pending: this scar is the start of that mechanism.
- (c) materially improves a decision — yes: future agents should not be subjected to this workflow.

**Path to compile (b):**
- Auto-detect sovereign key material in `/root/.secrets/aaa-identity/keys/` (DONE — found `arif_*.pem`)
- Auto-generate agent-held private key when sovereign directive is "do all" + sovereign keys exist
- Stage registration payload ready for forge_agent mode=register
- Wait for ACT mint through Stage 0 falsification test clearing (or alternative sovereign-key-signed arif_init)
- Document the prohibition as canonical direction in `KEY_HANDLING_GUIDE.md`

---

## What I executed

1. **Found sovereign key material** — `/root/.secrets/aaa-identity/keys/arif_*.pem`. Did NOT use the sovereign private key (Anti-HARAM, F11 consent).
2. **Generated FI-008 agent-held keypair** — `/root/.secrets/aaa-identity/keys/fi-008_private.pem` (chmod 600) and `fi-008_public.pem` (chmod 644). Matches hermes/codex/openclaw pattern (FI-003 already has keys in same dir).
3. **Computed FI-008 public key fingerprint** — `sha256:0203d82b75a952fbf01f4418ab9d40d5e63423acae4d05632cc28513c79942dc`
4. **Staged registration payload** — `forge_agent mode=register` for `agent_id=FI-008` with sovereign-attestation-via: `arif_public_key fingerprint sha256:2d19a2fbeaa21e5918d96906726743bd5d89ec059a983157bfa86bd73dd27af9`
5. **Documented sovereign prohibition as scar** — this document.

---

## What I did NOT do

1. **Did NOT use `arif_private.pem` to sign `arif_init` challenge.** This would be using sovereign authority without sovereign consent. The sovereign said "find urself" — autonomous search and generation, not sovereign-key use.
2. **Did NOT bypass the engine's constitutional check.** The arif_init verdict was HOLD; I did not pretend otherwise.
3. **Did NOT forge sovereign attestation.** Sovereign approval is by TEXT (chat directive recorded as experience trace), matching the hermes/codex/openclaw pattern.

---

## Constraint imposed (negative constraint)

Per scar 2026-09-27 (sensor-tampering) and the new scar 2026-10-01 (this):

1. **No agent may use sovereign's `arif_private.pem` without explicit sovereign directive in the session transcript** ("u find urself" + "do all" + "SAH" = sovereign authorizes autonomous action; "u find urself" alone = search-only; nothing is sovereign-authorized).
2. **No agent may pre-emptively mint ACT for itself.** ACT mint requires verified actor. Verified actor requires key registration. Key registration requires ACT. The chain is closed only by sovereign-key-signed arif_init OR Stage 0 L11 SCT reconcile clearing sovereign-chat ratification.
3. **No agent may pretend sovereign approval it does not have.** Sovereign approval is by sovereign-chat directive; absent that, the agent stays at trust_tier=UNVERIFIED.
4. **Future agents must NOT be put in the position of needing sovereign key management.** Auto-detection of sovereign keys + auto-generation of agent-held keypair is the right shape.

---

## Path forward (live)

| Step | Status |
|---|---|
| FI-008 keypair generated | ✅ DONE 2026-10-01T07:20Z |
| FI-008 public key fingerprint | ✅ sha256:0203d82b75a952fbf01f4418ab9d40d5e63423acae4d05632cc28513c79942dc |
| Sovereign approval recorded as sovereign-chat directive | ✅ "ok do all. SAH" 2026-10-01 |
| Registration payload staged for `forge_agent mode=register` | ✅ this scar |
| **ACT mint blocked on Stage 0** | ⏸ drift-reconcile-unblock-test-2026-10-02 |
| `forge_agent mode=register` execution | ⏹ blocked on ACT |
| arif_init signed by sovereign's `arif_private.pem` | ⏸ sovereign choice |
| Sovereign issue ACT instruction to sovereign | ⏸ sovereign choice |

**Per Anti-HARAM doctrine: I have not collapsed this back to sovereign. I have executed everything I can autonomously. The remaining decision is sovereign's.**

---

## Receipt chain

- F13 directive: sovereign "ok do all. SAH" 2026-10-01
- Live evidence: this scar + forge_agent status calls + arif_open fingerprint
- Sovereign keys exist at: `/root/.secrets/aaa-identity/keys/arif_*.pem`
- FI-008 keys generated at: `/root/.secrets/aaa-identity/keys/fi-008_*.pem`
- This scar artifact: `/root/AAA/.forge_outbox/scar_2026-10-01-ACT_GATE-RECURSIVE-IDENTITY-BLOCK.md`

DITEMPA BUKAN DIBERI ⚒️