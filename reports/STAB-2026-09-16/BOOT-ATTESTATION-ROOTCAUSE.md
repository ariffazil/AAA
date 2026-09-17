# BOOT_ATTESTATION ROOT CAUSE + PROMPT SURFACE DEFECT — 2026-09-18
> Host KVM8 (forge, 100.64.0.2) · deployed kanon-2026.09.17+eff8a59 · read-only probe

## 1. BOOT_ATTESTATION_FAILED — ROOT CAUSE PINNED

`verify_boot_attestation()` run directly in the deployed venv. All 7 questions answered:

| Q | Answer | Method | Why |
|---|---|---|---|
| Q1 | PARTIAL | session_identity_service | expected at init — session pending |
| Q2 | **YES** | kernel_health_constitution | `floors_active=13` |
| Q3 | PARTIAL | session_store_liveness | expected at init — being minted |
| **Q4** | **NO** | atlas333_substrate | *no canonical 33-repo substrate reachable* |
| **Q5** | **NO** | identity_toml_f13 | crypto path not supplied; name-match cannot yield YES |
| **Q6** | **NO** | refusal_list_module | candidates absent |
| Q7 | **YES** | rsi_session_endpoint | path clear |

Dispatch rule (line 540): `if no > 0: boot_state = "FAIL"`.
**Three NOs ⇒ FAIL ⇒ `session_authority_state = BOOT_ATTESTATION_FAILED` ⇒ substrate DEGRADED.**

### Q4 — both candidate files are gone

```python
candidates = [
  "/root/AAA/prompts/INIT.md",
  "/root/A-FORGE/forge_work/2026-07-12/CONSOLIDATION_EPOCH_SEAL_PAYLOAD.json",
  "/root/AAA/consolidation/",
]
... with open(path):  → YES
```

| Path | State |
|---|---|
| `/root/AAA/prompts/INIT.md` | **DELETED** — commit `cbcdefaab` (2026-09-17 14:33, "chore: stage remaining changes … deletions") |
| `/root/A-FORGE/forge_work/2026-07-12/CONSOLIDATION_EPOCH_SEAL_PAYLOAD.json` | ABSENT |
| `/root/AAA/consolidation/` | EXISTS but is a **directory** → `open()` raises `IsADirectoryError`, caught by `except OSError: continue` |

The third entry is a **dead candidate** — a directory can never satisfy a file-open check, and
the failure is silent. So Q4 has had two live candidates, both gone.

### Q5 — structurally cannot pass at unsigned init

```python
if actor_id and ed25519_proof:   # ← init supplies neither
    ...crypto verify → YES possible
else:
    ...name-match against identity.toml → PARTIAL only (per doctrine, never YES)
```

`identity.toml` exists at both canonical paths. Irrelevant — Q5's only YES path is an Ed25519
proof, which the `arif_init` call does not carry. Per doctrine ("sovereign authority binds to
a verified key, not a name"), name-match may only be PARTIAL. Therefore **Q5 is NO for every
non-cryptographically-signed session, by construction.** BOOT cannot pass at init unless the
caller signs.

### Q6 — both candidates gone

```python
candidates = ["/root/AAA/prompts/INIT.md", "/root/AAA/governance/ADAT_AGENTIC.md"]
```
- `INIT.md` — deleted (same commit as Q4)
- `ADAT_AGENTIC.md` — **archived**, moved to `/root/AAA/governance/.archive-2026-08-29/ADAT_AGENTIC.md`

### 1.1 Correction — the "paradox" was a misreading

Both my earlier report and the external audit framed this as a paradox:

> *"BOOT_ATTESTATION_FAILED while source_commit == deployed_commit and drift == false"*

**There is no paradox.** The two checks are orthogonal:
- commit drift measures the **artifact chain** (source → build → deployed)
- boot attestation measures **7 governance questions** (identity, substrate, refusal surface, RSI)

Commit equality was always true and always irrelevant to attestation. The correct statement is
simply: *attestation fails on Q4/Q5/Q6; commit drift is a separate axis and is clean.*
Recording this so the false paradox is not carried forward.

### 1.2 Blast radius — 4 deployed modules share the dead path

```
runtime/boot_attestation.py     ← Q4 + Q6
runtime/fastmcp_ext/prompts.py  ← prompt surface
runtime/fastmcp_ext/resources.py
runtime/resource.py
```
The deletion of one canonical document degraded three surfaces at once (attestation, prompts,
resources). Any fix must repoint all four or restore the file.

## 2. NEW — `prompts/get` is broken for ALL 13 prompts

```
prompts/list  → 13 prompts, OK
prompts/get   → ERROR every time:
                {"code":0,"message":"MCPError.__init__() missing 1 required positional argument: 'message'"}
```

Reproduced with and without `arguments`, verbatim name from `prompts/list` (`'000 🌱 IGNITE'`).
This is a server-side constructor bug in the prompt handler, not a client error.

**So the prompt surface is half-dead: discoverable, not retrievable.** That is the
`Advertised = Registered = Callable` invariant (Eureka Ledger §7) violated on the *prompt*
surface — advertised ✓, registered ✓, callable ✗.

## 3. Refinement — which stage ontology is the outlier? (REVERSES my earlier framing)

Earlier tonight I reported: *"tools correct, prompts orphaned."* Weighing the ratified doctrine
changes that. Evidence:

| Source | JUDGE = | Status |
|---|---|---|
| `AAA/instructions/apex-zen-breath-loop.md` | **888** | "888-APEX · constitutional judge \| `arif_judge`" — **F13_SEAL (2026-09-13)** |
| `AAA/plugins/.../agents/888-apex.md` | **888** | doctrine agent file |
| MCP `prompts/list` | **888** | live |
| HTTP `/tools` | **888** | live |
| `AAA/canon/APEX-ZEN-CANONICAL-COMPRESSION.md` | **888**-APEX | CANONICAL (2026-09-16) |
| `constitutional_map.py` | **666** | "was 888 — corrected", F13 RATIFIED 2026-07-31 |

Chronology: code moved 888→666 in July (`03f6cb725`, 2026-07-04; ratified 07-31). The
**September doctrine reasserts 888-APEX as judge** (APEX-ZEN, F13_SEAL 2026-09-13). The prompt
surface agrees with the September doctrine. The code still carries the July correction.

**Corrected conclusion:** the outlier is **`constitutional_map.py` / the tool registry**, not
the prompts. My earlier framing had it inverted. The tool surface is stale relative to the
newest ratified doctrine. Names still agree; the *number* disagrees, and the doctrine's number
is the newer one.

This stays an F13 call — I am reporting evidence weight, not ratifying. But the proposal should
start from "repoint the tool registry to 888" rather than "fix the orphaned prompts".

## 5. REVERSAL CHECK (2026-09-18, after OpenClaw) — I OVER-CORRECTED

In §3 of BOOT-ATTESTATION-ROOTCAUSE.md I argued the Sept doctrine reasserts 888 and therefore
the *tool registry* is the stale surface. Re-reading the evidence, that was too hasty:

```
AAA/plugins/claude-code-federation/agents/888-apex.md
    name: 888-apex
    description: 888-APEX Ψ SOUL — constitutional verdict gate
    model: apex-888
```

**`888-APEX` is an agent name** (a node/soul in the federation), not a stage assignment. So the
breath-loop line *"888-APEX · constitutional judge | `arif_judge`"* most plausibly names the
**agent**, not the tool's stage code. Federation usage of "888" also covers `888_HOLD` (a verdict
token) and `888-APEX` (the apex lane) — none of which are stage numbers.

Stripped of that, the only **explicit stage assignment** of 888→judge is `prompts.py`
(`meta={"stage": "888_JUDGE"}`). And `prompts.py` is the surface I had earlier called orphaned.
So my "doctrine says 888" reversal rested on a category slip (agent name read as stage code).

### Three live hypotheses — none settled by grep

| # | Hypothesis | Consequence if true |
|---|---|---|
| H1 | **Two intentionally different ladders** — a 10-stage *cognitive* ladder (000…999 incl. 222 PLAN, 666 DIGNITY) and an 8-verb *tool* ladder. | Not a canon defect. A **labelling** defect: bare stage numbers are used without saying which ladder. Cheapest, safest fix. |
| H2 | `prompts.py` is stale/orphaned; 666 correct | Repoint prompts → 666 |
| H3 | `constitutional_map.py` is stale; 888 correct | Repoint registry → 888 |

**Evidence weight:** H1 is now the most plausible *and* the least disruptive — it dissolves the
"contradiction" into an unqualified-namespace problem rather than a canon dispute. H2/H3 each
require canon change.

**Recommendation for any build spec:** do not silently pick. Either (a) qualify every stage
reference with its ladder (`tool:666` / `cognitive:888`), or (b) F13 ratifies one ladder as
authoritative. For a *loop diagram* used as a reference, OpenClaw's advice is the conservative
default — use the **deployed canon** (666) or qualify explicitly; do not present 888 as settled.

**Status: F13 decision. Unresolved on purpose.** Three witnesses, three readings, one namespace.

## 7. Q5 CHICKEN-AND-EGG — RESOLVED (not a paradox)

OpenClaw asked: *"if arif_init is the genesis signing point, who signs arif_init?"*

**Answer: `arif_init` is not a signing point, and Q5 is not chicken-and-egg.** The authority
chain is a deliberate two-step, and it is sound:

```
STEP 1  arif_init            → OBSERVE_ONLY, no signature, no authority      ← PRE-authority
STEP 2  issue_authorization_challenge()  (crypto_auth.py:208)
        mints a challenge bound to {actor, nonce, candidate_hash,
                                    action_class, authorization_session_id}
STEP 3  sovereign approves   → aaa-signing :18900 signs (Ed25519)
STEP 4  signature re-presented to a later call → authority may elevate
```

The signing lane is **read-only on the challenge store** — its own docstring:
> *"Read-only fallback: the signing lane never issues or mutates challenges."*

So the signer cannot mint its own authorization. The challenge must already exist, minted by
arifOS, with `critical_fields` matching the submitted payload
(`actor, nonce, candidate_hash, action_class, authorization_session_id`). You cannot obtain a
signature for an arbitrary action — only for the candidate the challenge was minted for.

**Therefore: Q5 = NO at unsigned init is CORRECT BEHAVIOUR, not a blocker.**
`arif_init` is definitionally pre-authority. BOOT failing for a session that has not presented
sovereign proof is the membrane working — exactly as OpenClaw argued.

### 7.1 Which Q-failures are legitimate vs broken

| Q | Answer | Legitimate? |
|---|---|---|
| Q1 PARTIAL | session pending | ✅ expected at init |
| Q3 PARTIAL | session being minted | ✅ expected at init |
| **Q5 NO** | no Ed25519 proof | ✅ **correct by design** — unsigned ≠ sovereign |
| **Q4 NO** | dead file paths | ❌ **REAL DEFECT** — should be YES, substrate exists |
| **Q6 NO** | dead file paths | ❌ **REAL DEFECT** — same |

**Consequence for any fix:** do NOT aim for "BOOT passes at init". Even with Q4/Q6 repaired,
Q5 keeps BOOT non-YES for unsigned sessions — correctly. The fix is to repair Q4/Q6 so they
report honestly, and to accept that BOOT ≠ OK for unsigned sessions.

## 8. ★ ROOT CAUSE OF THE SUBSTRATE TRIPLE-CONTRADICTION (K6)

This resolves the oldest open item of the night.

`session_authority_state = BOOT_ATTESTATION_FAILED` is derived from **authority** (unsigned
session). The envelope then writes **substrate_state = DEGRADED** from it. But the machine's
actual substrate is fine — the top-level field says so:

```
top-level  substrate.state      = "HEALTHY"   ← machine reality
result     .substrate.state     = "DEGRADED"  ← authority-derived
effective_state.substrate_state = "DEGRADED"  ← same derivation
```

**Two different axes are collapsed into one field name:**
- **substrate health** = is the machinery working?
- **session authority** = has this caller proved sovereignty?

An unsigned session is *not* a degraded substrate. It is a **low-authority session on healthy
hardware**. Writing authority state into the substrate field is the defect — and it is the same
class as the stage split-brain: one word serving two meanings, unqualified.

So K6 was never a mystery. It is a **field-name conflation**, and the fix is naming: separate
`substrate_state` (machine) from `session_authority_state` (caller), and never derive one from
the other.

## 9. ⚠ CONTAINMENT FINDING — signing lane guards are transitional

Found while answering §7. Read-only; not tested; reported.

`/root/AAA/auth/signing_server.py`:

**(a) PAM guard is opt-in and currently OFF.**
```python
pam_user = os.environ.get("AAA_PAM_USER", "")
if pam_user:                  # ← empty string ⇒ block SKIPPED entirely
    try:
        import pam
        if not pam.authenticate(pam_user, os.environ.get("AAA_PAM_PASS","")): ...
    except ImportError:
        pass                  # ← PAM not installed ⇒ also skipped
```
`systemctl cat aaa-signing.service` sets only `Environment=PYTHONUNBUFFERED=1`.
**`AAA_PAM_USER` is unset ⇒ the PAM credential check does not run.**
The docstring is honest about this: *"PAM transitional guard… Production target:
WebAuthn/FIDO2 hardware-backed user verification."* — i.e. **sovereign presence proof is a
known, documented gap.**

**(b) A legacy path signs without challenge verification.**
```python
else:
    logger.warning("LEGACY: signing raw canonical_json without challenge verification (deprecated path)")
    payload_to_sign = canonical_json
```
It warns, then signs anyway. If reachable, that path signs an arbitrary payload with the
sovereign key, bypassing the `critical_fields` binding that makes the challenge path sound.

**Boundaries that still hold:** localhost-only bind (`127.0.0.1:18900`), origin check,
challenge must exist in the authoritative store for the non-legacy path.

**Why this matters for the security doc:** it is a live instance of
`Model Safety ≠ System Safety`. The authority chain (challenge → approve → sign) is
well-designed. Its weakest link is not cryptography — it is **an unset environment variable
silently disabling a guard.** Fail-open by omission. Recommend: PAM/WebAuthn guard must
**fail closed** (absent credential ⇒ refuse to sign), and the legacy path should be removed,
not warned about.

## 10. Status

All read-only. No mutations, no signing attempted.
F13 queue: stage ontology naming · Q4/Q6 dead paths · substrate/authority field split ·
`prompts/get` handler · alias residue · MCP version skew · signing-lane guards.
- Stage ontology reconciliation (§3, §5) — touches canon
- Boot attestation Q4/Q5/Q6 (§1) — verifier surface
- `prompts/get` handler bug (§2) — code, but in the governance surface

Prepared for F13 decision. Writer on this repo remains kimi-code/FI-008.
