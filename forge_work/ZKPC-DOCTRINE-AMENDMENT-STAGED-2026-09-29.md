# ZKPC CANON AMENDMENT — STAGED, AWAITING F13 SAH

**Status:** STAGED. No canon file mutated. This document is the proposal; the BUILD lane writes on "SAH".
**Filed by:** FI-003 (333-AGI, BUILD capability cell) — 2026-09-29
**trace_id:** FI-003-2026-09-29-ZKPC-AUDIT
**Trigger:** F13 order "patch D1, stage the doctrine amendment, run Q3, then seal"
**Evidence base:** live disk + process probes this session, all MEASURED first-hand (see D1–D6 register below)
**Companions:** `/root/AAA/docs/ZKPC-CANONICAL-DOCTRINE.md` (target) · `/root/AAA/instructions/recovery-reality-cache.md` §7 (already correct) · `/root/AAA/instructions/state-transition-discipline.md` (claim states)

---

## Why this is a doctrine amendment, not a bug report

The audit found the estate's privacy *governance* genuinely live (1,000+ real refusals at the RASA write
gate; kernel substrate floor firing in `/opt/arifos/current/.../law.py`) and the privacy *representation*
untrue (a wire asserting ZK proof scores that were hardcoded constants; a personhood gate whose own
telemetry record says `STAGED_NOT_WIRED`).

The recurring cause is not missing capability. It is that **canon names an outcome, code implements a
mechanism, and the wire reports the canon name as if it were the mechanism.** Doctrine can close that gap
permanently; the D1 patch closes it at one site.

Two of the three propositions below were **contradicted by my own measurements** — that is the point. The
doctrine was overspecified in one place and under-pinned in another.

---

## AMEND-1 — Mechanism neutrality (the ZKPC definition is over-committed)

**Finding:** ZKPC canon requires *"privacy-preserving proof … only minimum necessary fact disclosed"* — an
**outcome**. Canon also names "Zero-Knowledge" in the label, which reads as a **mechanism commitment**. I
verified against primary sources that the outcome is reachable without any ZK system:

- **RFC 9901, "Selective Disclosure for JSON Web Tokens"** — Fett/Yasuda/Campbell, Proposed Standard, 2025.
  Issuer signs digests over claims; holder discloses a subset; undisclosed claims' names *and* plaintext
  stay hidden from that verifier; KB-JWT binds presentation to a key and audience. `DEPLOYED-NOW`.
  Verified by me this session at rfc-editor.org.
- **SD-JWT VC `draft-ietf-oauth-sd-jwt-vc-19`** (2026-08-31) — at IESG, not yet RFC; **Secdir ballot
  "Has issues"**. Adds `cnf` holder binding, `vct`, and `status` → Token Status List revocation.
  `EARLY-PRODUCTION`. Verified by me at IETF datatracker.
- **This host:** `circom`, `halo2`, `gnark`, `zokrates` ABSENT; **zero** `.circom`/`.r1cs`/`.zkey` files on
  disk. `snarkjs` + Python `py_ecc` + `blake3` present. There is a verifier runtime and nothing to verify.

**Consequence:** the doctrine's ZK framing commits us to a cryptographic family for a property a published
standard already delivers. That is the difference between an engineering gap and an unreachable promise.

**Proposed insertion** into `ZKPC-CANONICAL-DOCTRINE.md`, immediately after "### ZKPC — Canonical Definition":

```markdown
### Mechanism neutrality (F13 amendment 2026-09-29)

ZKPC is defined by its OUTCOME, not its cryptographic family:

> **An authorised party proves the minimum necessary fact — root control, valid unexpired unrevoked
> delegation, in-scope action, freshness — without disclosing the underlying secret.**

Any mechanism achieving that outcome satisfies ZKPC. Ranked by maturity, not elegance:

1. **Selective-disclosure credentials** (RFC 9901 SD-JWT; SD-JWT VC) — outcome-complete for delegation,
   scope, holder binding and freshness, with no circuit and no trusted setup. PREFERRED PATH.
2. **Hash commitment + signature** (Blake3 CHC + Ed25519) — binds bytes, does NOT establish that a token
   descends from an authorised root unless the verifier already trusts our code. PARTIAL: sufficient for
   internal witness, insufficient for third-party assurance.
3. **Zero-knowledge proofs** — additionally gives unlinkability and non-disclosure of the *policy* itself.
   NOT IMPLEMENTED here. Adopt only where 1–2 provably fail, i.e. against "Surveillance through proofs".

**Naming law:** a surface may describe the mechanism it actually implements. Emitting `ZKPC_*` on a path
that only hashes is a constitutional violation under F2 (TRUTH) and F9 (ANTI-HANTU), not a naming
preference. Where capability is absent, the surface declares it absent.
```

**Also requires:** `proof_level` vocabulary alignment. `arifosmcp/apex_envelope.py:46` defines the closed
enum `{ZKPC_NONE, ZKPC_OBSERVATION, ZKPC_AUDIT, ZKPC_CERTAINTY}` and `runtime/tools.py:5999` defaults to
`ZKPC_OBSERVATION` when a tool declares nothing. For READ-only actions "observed, not proven" is arguably
faithful — but it is the same vocabulary the A2A wire abused. **Proposed:** rename the enum to
`PROOF_{NONE,OBSERVED,ATTESTED,VERIFIED}` with `ATTESTED` reserved for a real attester and `VERIFIED` for
an external verifier, and default to `PROOF_NONE`. This is a wire-contract change across kernel +
`A-FORGE/src/domain/governance/apexDials.ts:42` → **needs its own F13 order, registered as B012.**

---

## AMEND-2 — Tamper-evident ≠ tamper-proof (our strongest word is over-claimed)

**Finding:** VAULT999's protection is ext2 `+a` append-only plus a hash chain. ext2 flags are
**root-reversible** — `chattr -a -i <file>` and the file is writable. My own memory file
`chattr-both-flags-before-rsync` records running exactly that command. Measured this session:
`lsattr` on `apex-zen-receipts.jsonl` → `-----a--------e-------`, and `apex-zen-announce.jsonl` → **no
`+a` at all** (the flag is applied unevenly across the ledger family).

**Consequence:** "immutable" and "there is no unseal" describe *intent* and are **physically false against a
root attacker**. What is true: removal or mutation is *detectable* via the chain, and the `+a` flag raises
the cost of casual mutation. Naming the guarantee correctly matters because ZKPC canon lists "Key theft"
and "Memory poisoning" as principal threats — a reader who believes the ledger is tamper-*proof* will not
require the independent witness that tamper-*evident* storage demands.

**Proposed edits:**

| File | Current | Proposed |
|---|---|---|
| `ZKPC-CANONICAL-DOCTRINE.md` threat table row "Memory poisoning" | control: "Provenance, truth classes, witness diversity, correction chains" | append: "Note: VAULT999 is tamper-**evident** (hash chain) + append-only-flagged, NOT tamper-proof (ext2 flags are root-reversible). Detection requires an independent witness holding a prior commitment." |
| Kernel `arif_seal` description | "accepted entries can never be edited or removed; there is no unseal" | "entries cannot be edited or removed **through governed paths**; the substrate is tamper-evident, not tamper-proof. Root-level mutation is detectable via hash chain, not prevented." |

Recovery-reality-cache §7 already states this correctly ("Tamper-Evident Receipts"). Canon and kernel
surface have drifted from it. This amendment brings them into line — **no new doctrine is introduced.**

---

## AMEND-3 — Claims must carry attestation state (the D1 lesson, generalised)

**Finding:** the A2A envelope asserts 10 gate scores per response. One was patched today (proof). The other
nine are **also** hardcoded literals — `presence:{pass:true,score:1.0,detail:"LIVE"}`,
`energy:{…0.8,"default cost"}`, `sovereign:{…1.0,"no F13 halt"}`. They do not claim zero-knowledge, so
they are not the D1 violation, but they do present unmeasured values as passing gates to foreign agents.
Registered as **D6**; deliberately NOT patched, because relabelling nine gates changes a wire contract that
`arifosmcp/runtime/act_token.py:626-633` reads (`payload.apex.G`, `payload.apex.verdict`) — that is F13's
call, not a side effect.

**Proposed law insertion** (short, general, no new registry):

```markdown
### Attestation state on asserted capability gates

Any value a surface presents as a *gate* or *proof* MUST declare how it was obtained:

    { pass: true|false|null, attested: true|false, source: computed|declared|default|hardcoded }

- `attested:false` + `pass:true` is forbidden — that is a claim without a witness (F2).
- `pass:null` means "not evaluated"; it is honest and must not be coerced to true.
- A `default:` or `"LIVE"`-style literal detail marks the value as unmeasured and MUST NOT be rendered
  downstream as a passing gate.

Rationale: state-transition-discipline forbids collapsing a transition into a Boolean. A gate score with no
attestation state is exactly that collapse. Missing capability = roadmap problem (technical debt).
Misrepresented capability = assurance problem (AUDIT DEBT). The second is worse because it also corrupts
every downstream statement that cited the first.
```

---

## D-register — findings this amendment rests on (all MEASURED, this session)

| ID | Severity | Finding (evidence) | State |
|---|---|---|---|
| **D1** | CRITICAL | A2A wire asserted `proof:{pass:true,score:0.85,detail:"ZKPC_OBSERVATION"}` ×2 hardcoded sites; zero ZK tooling on host; `catch { /* Fail open */ }`. Live as `aaa-a2a.service`, pid 2344265. | **PATCHED** (source, tested green, 5/5 regression) — **NOT YET LIVE: service still runs 2026-09-28 23:41 code; needs restart** |
| **D2** | CRITICAL | H1–H9 `floor_gate.py` self-labels `gate_state:"STAGED_NOT_WIRED"`, `action:"OBSERVED_ONLY"`; `check()` has no production caller (engine, `hooks.pre_tool_call` → `arifos-hermes-gate-hook.py`, and enabled-plugin list all checked); `human9_telemetry.jsonl` ABSENT; `floor_holds.jsonl` ABSENT in both candidate paths → **zero production HOLDs ever emitted**. Suite `test_human9_floor_gate.py` exits 1 with 10 self-labelled KNOWN-UNKNOWN probes. Three records disagree: receipt sha `84ee67…`, carry_forward log `88bdf4…`, disk `048ba9f4…`. | OPEN — **role decision required, see B011** |
| **D3** | HIGH | Forgetting is a rename. No `Fernet`/`AESGCM`/`age` in `memory_store.py` or `consent_token.py` → plaintext at rest, so crypto-shredding is unavailable (no key whose destruction erases anything). `memory_store.py:2672` "forgets" by *appending a revocation record*. Canon (ZKPC canon, F13 sovereign right #9) promises "Forgetting". External survey 2508.08898: verifiable-erasure ZK is `PAPER-ONLY`; dominant redaction mechanism is a chameleon-hash **trapdoor**, which contradicts ZKPC intent. | OPEN — not fixable by doctrine alone |
| **D4** | MEDIUM | Consent state stale/single: exactly one record `/root/WELL/envelopes/_consent/arif.json`, mtime **2026-07-17** (74 days), free-text scope, zero records for the other 12 R4 persons. `identity_continuity.yaml:183` `consent_scope_default: biometric.full` (maximum, not minimum, on opt-in) though `consent_default_state: OFF` is correct. `people.yaml:25` *"when in doubt, set scope: shared"* = fail-**open** privacy default. | OPEN |
| **D5** | MEDIUM | `law.py:175` bare `except Exception: pass` silently disables the substrate floor (only `BLOCK` counts; `GUARD`/`STRENGTHEN` advisory) with no witness. Live kernel `human_substrate.py:363` seals `source="sovereign-testimony:scar-terrain-arif-fazil.md"` — that file **does not exist**; source fixed 12:06 today to `AAA/wiki/SCAR_TERRAIN.md` (exists); live install is 01:34 → provenance pointer currently dangling. No past vault record carries the dead pointer (nothing corrupted yet). | OPEN — trivially fixable by redeploy |
| **D6** | MEDIUM | Nine further gate literals presented as passing gates (see AMEND-3). | REPORTED, not patched — needs F13 order |

**What IS working** (recorded so the register isn't read as an outage): kernel `arifos.service` active and
running law.py substrate check from `/opt/arifos/current/venv`; RASA write gate with 3,668 records including
531 `REJECT_DIAGNOSTIC_LABEL`, 347 `REJECT_UNGROUNDED_BRIDGE`, 305 `REJECT_CROSS_LAYER_REDUCTION`, 32
`REJECT_SEXUALITY_INFERENCE`, 32 `REJECT_UNILATERAL_RELATIONSHIP_CLAIM`, 91 authority-increase refusals vs 6
grants; `people.yaml` scoping live in `lane_switch`; `worldModelTraining.ts:105` throwing on unredacted PII;
`mailread` read-only by construction over a mode-600 rotating socket.

---

## What I did NOT do (and why)

- **Did not edit canon.** `/root/AAA/docs/ZKPC-CANONICAL-DOCTRINE.md` is a canonical record; constitution
  mutation needs the one word "SAH" (Auto-Seal §2). Proposal only.
- **Did not restart `aaa-a2a.service`** or any systemd unit. Patch is in source; going live touches a shared
  federation wire whose consumers are unknown to me. Flagged, not acted.
- **Did not touch VAULT999 flags or `+a` state.** That is F1-surface.
- **Did not re-score the proof gate — and my stated reason for that was WRONG.** I recorded that
  `score:0.85` was preserved because `act_token.py` reads `apex.G` and re-scoring would change verdict
  semantics. I then falsified my own arithmetic (CORRECTION-2 below): an honest `score:0` does **not** change
  the verdict band at all. The conservative choice was right; **the justification I filed for it was false,
  and a false justification in a receipt is the same disease as D1.** Corrected rather than quietly dropped.
- **Did not decide D2.** See B011 — Arif's call, not the BUILD lane's. A judgment relayed from 888-APEX is
  JUDGMENT, not SAH; B011/B012 remain awaiting the sovereign's word.

---

## CORRECTION-1 — live falsification of D1 (this is the B013 evidence)

`STATE: PATCHED ≠ LIVE ≠ VERIFIED-ON-WIRE.` I probed the **running** process directly, because the
2026-09-04 "kernel label-truth" scar (four sites patched, none firing on the real dispatch path) is exactly
the failure mode that makes source-level claims untrustworthy.

```
POST http://127.0.0.1:3001/judge    (aaa-a2a.service, MainPID 2344265, started 2026-09-28 23:41)
  -> proof gate: {"pass": true, "score": 0.85, "detail": "ZKPC_OBSERVATION"}
  -> apex.G: 0.6145   apex.verdict: "SABAR"   outer verdict: "SEAL"
```

- The emitter **is** `deliberation()`, reached via `app.post('/judge')` (line 5341) — my patch targets the
  correct path. This is **not** a fifth-emitter case; a restart will make the fix live.
- The false claim **is** reaching federation peers right now.
- Blast radius scoped honestly: `server.js` binds `127.0.0.1:3001` only; the `100.64.0.2:3001` surface is
  tailscaled. Reach is **tailnet-internal, not public**. The lie goes to federation agents, not the internet.

## CORRECTION-2 — the fabricated score is NOT load-bearing

`buildApexEnvelope`: `U = geoMean([reversibility?.score || 1.0, proof?.score || 1.0])`.

| proof.score | U | G | apex band |
|---|---|---|---|
| 0.85 (as emitted) | 0.9220 | 0.6145 | SABAR |
| 0.0 (honest "unproven") | **1.0000** | **0.6400** | SABAR |

Same band either way. D1's label fix therefore changes **no** verdict, and an honest re-score is behaviourally
free — which removes the main objection to going further than a label change.

## D7 — three parallel proof vocabularies on one coordinate (FATWA K1 violation)

| Layer | Definition | Honest? |
|---|---|---|
| kernel `apex_envelope.py:46` | `{ZKPC_NONE, ZKPC_OBSERVATION, ZKPC_AUDIT, ZKPC_CERTAINTY}` | **NO** — implies ZK where only hash+sign exists |
| A-FORGE `apexDials.ts:42,187-189,284,443,452,493` | same four + ordinal ranking + per-action-class requirement (`IRREVERSIBLE -> ZKPC_CERTAINTY`) | **NO** — ranks on a scale it cannot satisfy, and *requires* levels that do not exist |
| kernel `schemas/transition_receipt.py:94-101` | `ZKPC-L0 = "Hash chain only (not externally verifiable)"`, `L2 = +Ed25519 sovereign signature`, `L3 = +Supabase anchor` | **YES** — semantics describe the actual mechanism |

**This reframes B012.** The fix is not "rename ZKPC -> PROOF". It is **collapse onto the one vocabulary that
already tells the truth** (`transition_receipt.py` L0–L3) and retire the other two. Lower cost than a rename
(no new names to propagate across the wire), it satisfies FATWA K1's one-SOT-per-coordinate rule, and the
`ZKPC_` prefix survives while each level states what it physically provides. Note the A-FORGE table is the
worst of the three: it *demands* `ZKPC_CERTAINTY` for irreversible actions on a host that cannot produce it —
an unmeetable requirement that must resolve to either a false pass or a permanent HOLD.

## D8 — falsy-default trap (honest zeroing is currently unrepresentable)

`gateScores.proof?.score || 1.0` coerces `0` to `1.0`. **The most honest value available (0 = unproven)
silently becomes maximum proof.** Any future "just set the score honestly" patch would do nothing at all.
Fix is `??` instead of `||`, so only `null`/absent defaults. Registered with D6 — same wire-contract family,
needs its own order.

## D9 — one response, two contradictory verdicts

Live `/judge` returns outer `verdict:"SEAL"` while `apex.verdict:"SABAR"`, and `act_token.py:626,630` consumes
`apex.verdict` and `apex.G` as `state`. The two-scoring-systems disagreement is measured here on the `/judge`
surface, not inferred from telemetry.

---

# ADDENDUM — Q3 RUNTIME ATTESTATION (delivered 2026-09-29, FI-003)

Research lane returned; **I re-measured every local claim myself and all reproduced.** Verdict: the threat
row `Agent cloning → runtime attestation` is not merely unbuilt — **it is unimplementable on this host**, and
not fixable by anything we can do inside the guest.

## A. Hardware reality (MEASURED by me, `/sys` + `/proc` + `dmi`)

| Probe | Result |
|---|---|
| DMI | `Standard PC (i440FX + PIIX, 1996)`, `sys_vendor = QEMU`, `bios_vendor = SeaBIOS` |
| Firmware | **SeaBIOS, no UEFI** — `EFI variables are not supported`, `/sys/firmware/efi` absent → **no Secure Boot chain exists to measure** |
| TPM | `/dev/tpm*`, `/dev/tpmrm*` absent; `/sys/class/tpm` 0 entries; `tpm2_*`/`swtpm`/`keylime_agent` ABSENT |
| CVM | `/dev/sev`, `/dev/tdx*` absent; CPU is AMD EPYC 9354P but guest CPUID exposes **no `sme`/`sev`/`sev_es`/`tdx`** |
| Authenticators | `/dev/hidraw*` 0 devices → no FIDO/USB authenticator |
| Keys | Ed25519 files in `/root/.ssh`, OpenSSL 3.5.3. **No HSM, no cert chain, no hardware root of trust** |

A vTPM is a **hypervisor-side object** (QEMU `tpm-crb` + `swtpm`), so as a tenant in someone else's KVM we
**cannot self-provision** one — it needs a host redefinition we do not control. And a swtpm we installed
ourselves would carry a self-issued EK chain: **a self-asserted anchor proves nothing to an external party.**
That is the D1 pattern wearing hardware clothes.

## B. What the standards actually give a verifier (from the research lane, labelled by evidence class)

- **AMD SEV-SNP** — single ~1 KB report, ECDSA P-384, anchored ARK→ASK→VCEK from AMD KDS; verifiable without a
  cloud account *if* you have the hardware. `DEPLOYED-NOW`, unreachable here.
- **Intel TDX** — TDREPORT is MAC'd and **local-only**; needs a Quoting Enclave (an SGX enclave) → ECDSA TD
  Quote, anchored Intel Root CA→PCK→QE AK, plus out-of-band collateral from PCS/PCCS. `DEPLOYED-NOW`, unreachable.
- **AWS Nitro Enclaves** — COSE_Sign1 with PCR0–31, anchored AWS Nitro Root CA; **no monotonic counter, no
  trusted clock, no enclave-identity revocation**, and AWS mandates *disabling CRL checking*. EC2-only.
- **NVIDIA HGX-CC** — SPDM + 5-cert chain to NVIDIA Root CA vs RIM golden measurements. Anchor is NVIDIA-run.
- **Arm CCA** — spec final, **silicon arriving late 2026**, Realm token still a draft. `EARLY-PRODUCTION` at best.
- **RFC 9711 EAT** (2025-04) and **RFC 9334 RATS** — the standard *result* formats. We can **consume/emit
  claims** in these shapes; we cannot be an Endorser.
- **CoRIM** `draft-ietf-rats-corim-11` — WG Last Call, **not an RFC**. My brief cited a "TCG PSC spec": **no
  such spec exists** — the real artefacts are **DPE (2023-02-14)** + DPE-CRB RC1 (2025-07-29). My error, corrected.
- My brief also cited WebAuthn `sec:pubk`: **not an attestation format** (`packed/tpm/android-key/apple/
  fido-u2f/none` are). Premise error, corrected.

## C. The two things that matter most

**C1 — Attestation would not solve our actual problem even if we had it.** No scheme surveyed measures **LLM
weights or model version**. TDX MRTD/RTMR and SNP MEASUREMENT cover the VM image and guest config; GPU reports
cover firmware vs RIM. **Which model answered, and which prompt policy was in force, remains self-assertion.**
So "prove the agent that ran is the agent I bound" is *not* purchasable with hardware — only with registers we
extend ourselves. Plus TEE.fail (CCS 2025) extracted attestation keys from *fully patched* TDX/SNP via DRAM
interposer and reused them — in their words: *"provide you with incorrect output, while still faking a
successfully completed attestation process."*

**C2 — the honest ladder exists but is unwired (good news).** `schemas/transition_receipt.py:94-101` defines
`ZKPC-L0 = "Hash chain only (local receipt, not externally verifiable)"` → `L2 = +Ed25519` → `L3 = +Supabase
anchor`. Those semantics are **truthful** — L0 says out loud what AMEND-2 had to argue. Measured: `"proof_level"`
appears in **zero live records** under `/var/lib/arifos`, and `ZKPC_L2/L3` have **no verifier implementation**,
only enum lines. So no false attestation claim has ever been sealed. This is the ladder B012 should collapse
onto — it needs wiring, not invention.

## D. What ZKPC canon's threat table can and cannot meet, here

| Threat row | Canon's control | Reality on this host |
|---|---|---|
| Undead sessions | short leases, heartbeat, revocation roots, fail-closed | **MEETABLE NOW** — pure software; our lease/ACT machinery already exists. *More achievable than any attestation row.* |
| Agent cloning | instance-bound keys + **runtime attestation** | **SPLIT REQUIRED.** Instance-bound keys/DPoP: doable. Hardware attestation: **impossible** (A). |
| Replay | nonces, timestamps, audience binding | **MEETABLE NOW** — RFC 9449 DPoP + EAT `nonce`/`iat`. Proves possession, not provenance. |
| Key theft | hardware keys, quorum, rapid revocation | **NOT MEETABLE** — no HSM/TPM. Software Ed25519 in `/root/.ssh`. |
| Surveillance through proofs | unlinkable sessions, rotating pseudonyms | **NOT MEETABLE by SD-JWT** — issuer still correlates. Needs accumulator/anon-cred work. |

## E. Recommendation — say the truth instead of building the theatre

Ranked by evidential strength ÷ cost:

1. **Publish a trust-model statement** (cost ≈ 0, do this first): *"Ed25519 keys are software-held on an
   unattested SeaBIOS KVM guest with no TPM, no UEFI, no CVM. Signatures prove **key possession**, not
   **runtime integrity**."* This is the attestation analogue of D1 and it closes the over-claim without
   buying hardware.
2. **Wire the honest `ZKPC-L0` ladder** into real records + give `L2`/`L3` actual verifiers, or delete them.
   An enum level with no verifier is a claim waiting to be misused.
3. **Adopt DPoP (RFC 9449) + EAT-shaped claims** for sender constraint and freshness. `DEPLOYED-NOW`, no
   hardware. Replaces `ZKPC_OBSERVATION` with an RFC-named, third-party-verifiable claim set.
4. **Undead-sessions row first** — it is the only canon promise we can fully keep today.
5. **Buy a CVM** (TDX g8i / SNP / Nitro) — real external anchor, but that is new vendor + new spend, **and**
   it still does not measure the model (C1). **F13 binary, not a build task.**

**Do not build ourselves:** RATS (RFC 9334), EAT (RFC 9711), CoRIM, DPoP, SPIFFE SVID, WebAuthn formats, A2A
`AgentCardSignature`. Note A2A v1.0.0 Signed Agent Cards = JWS/JCS + `kid`/`jku`→JWKS = **key publication, not
attestation** — our own wire should not be described as more than that.

## F. Direct line to the sovereign's eureka (same session)

F13 reframed privacy as **"the right to say: yang ini memang saya, yang itu bukan"** — authority, not secrecy.
Q3's honest answer: **this machine cannot make that statement externally verifiable.** No TPM, no UEFI, no CVM,
no HSM, nothing that measures a model. We can prove *a key signed this* and never *the runtime I claim produced
it*.

So the defence of that right cannot rest on hardware attestation here. It rests on **delegation receipts +
public attestation of origin** — which is exactly the selective-disclosure credential path (AMEND-1 / RFC 9901)
plus truthful L0 labelling. Not zero-knowledge. Not hardware. **Names, provenance, and disclosure.**
