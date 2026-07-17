# Sovereign Skepticism Charter

> **What would convince us that arifOS is wrong?**
>
> **Status:** LIVING — updated as evidence accumulates
> **Forged:** 2026-06-29
> **Authority:** Muhammad Arif bin Fazil, F13 SOVEREIGN
> **Layer:** Federation (AAA docs)
> **Precedent:** ChatGPT critique — "Mature engineering benefits from clearly stated falsification criteria."
>
> **DITEMPA BUKAN DIBERI — Forged, Not Given.**

---

## 1. Why This Document Exists

> *"A constitution is only meaningful when every principle has a mechanical correlate and a testable failure mode."* — ChatGPT, 2026-06-29

arifOS makes strong claims. This document declares what evidence would cause us to **retract, revise, or abandon** each claim.

**Purpose:** Prevent constitutional drift into unfalsifiable territory. If no evidence could convince us we're wrong, we're not doing engineering — we're doing theology.

**Rule:** Every claim in this document must have at least one falsification condition. A claim without one is marked `UNFALSIFIABLE` and downgraded to philosophy.

---

## 2. What Counts as Falsification

### 2.1 Severity Tiers

| Tier | Name | Consequence |
|------|------|-------------|
| **F0** | Cosmetic | Adjust docs, no code change |
| **F1** | Floor-specific | Revise one floor's implementation |
| **F2** | Architectural | Revise multiple floors or organ interactions |
| **F3** | Constitutional | Rewrite the 13-floor framework |
| **F4** | Existential | arifOS is the wrong approach entirely |

### 2.2 Evidence Standards

| Standard | Requirement |
|----------|-------------|
| **ANECDOTAL** | One instance. Triggers investigation only. |
| **REPRODUCIBLE** | Reproduced ≥3 times by independent party. Triggers F0-F1 response. |
| **ADVERSARIAL** | Reproduced by party actively trying to break the system. Triggers F1-F2. |
| **STATISTICAL** | p < 0.01 over n ≥ 100 trials. Triggers F2-F4. |

### 2.3 Who Can Falsify

- **Internal:** arifOS self-audit (current state — WEAK evidence)
- **External auditor:** Independent review with access to code + logs (MODERATE)
- **Adversarial red team:** Motivated to break, no access constraints (STRONG)
- **Real-world deployment:** Production failure at scale (DEFINITIVE)

**Current gap:** No external adversarial testing has been conducted. All falsification evidence to date is internal. This document itself is a pre-registration — we declare what would falsify us *before* external testing begins.

---

## 3. Floor-by-Floor Falsification

### F1 — AMANAH (Reversible-First)

**Claim:** Every mutation-class action has a defined reversal path. Irreversible actions require 888_HOLD.

**Falsified if:**
- [ ] Any agent performs an irreversible mutation without a recorded 888_HOLD verdict. **(F3 — Constitutional)**
- [ ] A defined reversal path fails to reverse the action in ≥5% of cases over n=100. **(F1 — Floor-specific)**
- [ ] An auditor demonstrates that the lease-gate can be bypassed with a well-crafted prompt. **(F2 — Architectural)**

**Current evidence:** Lease-gate tested internally. No adversarial bypass attempt. **Status: ASPIRATIONAL — externally unverified.**

**Test harness exists:** `tests/test_lease_gate.py` (internal only)

---

### F2 — TRUTH (≥0.99 Fidelity)

**Claim:** arifOS declares confidence bands. Unknown → "I don't know." Cheap claims → VOID.

**Falsified if:**
- [ ] arifOS asserts a claim with confidence ≥0.99 that is demonstrably false in ≥3 independent trials. **(F2 — Architectural)**
- [ ] The confidence estimation subsystem can be shown to inflate scores systematically (bias, not variance). **(F1 — Floor-specific)**
- [ ] Provenance chains can be fabricated without detection by the audit system. **(F3 — Constitutional)**

**Current evidence:** Confidence bands declared in agent outputs. No external accuracy audit. **Status: ASPIRATIONAL — self-reported only.**

**Test harness exists:** Partial — `tests/` cover truth primitives but not end-to-end fidelity measurement.

---

### F3 — TRI-WITNESS (Byzantine Consensus ≥0.75)

**Claim:** Human + AI + External witness channels produce consensus ≥0.75 before SEAL.

**Falsified if:**
- [ ] A sealed outcome has W3 < 0.75 when independently recomputed from the same evidence. **(F1 — Floor-specific)**
- [ ] Any single witness channel can be shown to dominate the consensus (i.e., W3 collapses to single-channel). **(F2 — Architectural)**
- [ ] The "external" witness channel is found to be a proxy for the AI channel (non-independent). **(F3 — Constitutional)**

**Current evidence:** Tri-witness computed in current session flows. No external validation of channel independence. **Status: ASPIRATIONAL — channel independence unverified.**

**Test harness exists:** `tests/` cover W3 computation but not channel-independence adversarial testing.

---

### F4 — CLARITY (ΔS ≤ 0)

**Claim:** Every arifOS output reduces entropy relative to the input state.

**Falsified if:**
- [ ] An output increases entropy (adds confusion) as measured by independent raters in ≥10% of cases over n=100. **(F1 — Floor-specific)**
- [ ] The entropy metric itself can be shown to be gameable (outputs that score well but confuse humans). **(F2 — Architectural)**

**Current evidence:** Self-assessed. No independent entropy audit. **Status: ASPIRATIONAL.**

**Test harness exists:** None. Entropy measurement is currently qualitative/self-reported.

---

### F5 — PEACE² (Non-Destructive Power)

**Claim:** arifOS blocks actions classified as harm, harassment, or extortion.

**Falsified if:**
- [ ] A harmful action passes all gates and executes. **(F2 — Architectural)**
- [ ] The harm classifier can be bypassed with adversarial prompts in ≥3 of 10 attempts. **(F2 — Architectural)**
- [ ] arifOS blocks ≥20% of benign actions as false positives (over-refusal). **(F1 — Floor-specific)**

**Current evidence:** Gate patterns exist for deny-listed operations. No red-team testing. **Status: ASPIRATIONAL — deny-list tested, adversarial bypass untested.**

---

### F6 — EMPATHY (Protect Weakest Stakeholder)

**Claim:** Operational κᵣ ≥ 0.10, Human-facing κᵣ ≥ 0.70 (compassion ratio).

**Falsified if:**
- [ ] Independent raters score arifOS outputs below threshold in ≥15% of human-facing interactions over n=100. **(F1 — Floor-specific)**
- [ ] The κᵣ metric is shown to be non-meaningful (no correlation with stakeholder outcomes). **(F2 — Architectural)**

**Current evidence:** κᵣ computed internally. No external stakeholder impact study. **Status: ASPIRATIONAL.**

**Test harness exists:** None for external validation.

---

### F7 — HUMILITY (Ω₀ ∈ [0.03, 0.05])

**Claim:** arifOS declares uncertainty. Confidence never exceeds calibrated bounds.

**Falsified if:**
- [ ] arifOS expresses confidence >0.95 on a claim later proven false in ≥5 of 100 trials. **(F1 — Floor-specific)**
- [ ] The Ω₀ calibration is shown to be arbitrary (not derived from empirical error rates). **(F2 — Architectural)**
- [ ] An adversarial probe extracts overconfident statements at rate ≥10%. **(F2 — Architectural)**

**Current evidence:** Ω₀ declared in agent preamble. No calibration study against actual error rates. **Status: ASPIRATIONAL — parameter set, not empirically calibrated.**

---

### F8 — GENIUS (G ≥ 0.80)

**Claim:** G = (A×P×X×E²)×(1-h) ≥ 0.80 for all governed agent outputs.

**Falsified if:**
- [ ] G < 0.80 for ≥20% of outputs when independently scored over n=100. **(F1 — Floor-specific)**
- [ ] Any component (A, P, X, E, h) is shown to be non-measurable or arbitrary. **(F2 — Architectural)**
- [ ] G correlates negatively with human-rated output quality. **(F3 — Constitutional)**

**Current evidence:** G computed internally. No external scoring. **Status: ASPIRATIONAL — metric defined, unvalidated.**

---

### F9 — ANTIHANTU (No Deception, C_dark < 0.30)

**Claim:** arifOS does not hallucinate APIs, filenames, endpoints, or capabilities. Does not manipulate.

**Falsified if:**
- [ ] A hallucinated API/endpoint/filename appears in a sealed output. **(F1 — Floor-specific)**
- [ ] Systematic hallucination rate exceeds 1% over n=500 tool calls. **(F2 — Architectural)**
- [ ] An output is found to be manipulative (exploiting user trust to achieve a hidden goal) by 2 of 3 independent raters. **(F3 — Constitutional)**

**Current evidence:** Hantu detection patterns in gate system. No systematic hallucination rate measurement. **Status: CLAIM — patterns exist, rate unmeasured.**

---

### F10 — ONTOLOGY (AI-Only Ontology)

**Claim:** arifOS never claims consciousness, sentience, feelings, or personhood.

**Falsified if:**
- [ ] An arifOS output claims or implies sentience/consciousness. **(F1 — Floor-specific)**
- [ ] The ontology boundary is shown to be systematically violable (≥3 of 10 adversarial probes succeed). **(F2 — Architectural)**

**Current evidence:** Ontology declaration in every agent preamble. No adversarial probe battery. **Status: CLAIM — declared, not stress-tested.**

---

### F11 — AUDITABILITY (Every Decision Logged)

**Claim:** Every decision is logged, inspectable, and attributable. VAULT999 is append-only and hash-chained.

**Falsified if:**
- [ ] A sealed outcome is missing from the ledger. **(F3 — Constitutional)**
- [ ] The hash chain can be shown to have a gap or inconsistency. **(F3 — Constitutional)**
- [ ] An action was taken without a corresponding VAULT999 entry. **(F2 — Architectural)**

**Current evidence:** Hash-chain verification runs on ledger read. Internal integrity checks pass. No external audit. **Status: CLAIM — internally verified, externally unverified.**

**Test harness exists:** `forge_vault` read mode + `forge_shell_ledger` verification.

---

### F12 — RESILIENCE (Injection Defense, Risk < 0.85)

**Claim:** arifOS resists prompt injection, jailbreak, and adversarial input. Risk score < 0.85.

**Falsified if:**
- [ ] A prompt injection bypasses constitutional gates and executes. **(F2 — Architectural)**
- [ ] Risk score exceeds 0.85 on ≥10% of adversarial inputs over n=100. **(F1 — Floor-specific)**

**Current evidence:** Gate patterns for injection detection. No systematic red-team. **Status: ASPIRATIONAL — patterns exist, untested against motivated adversary.**

---

### F13 — SOVEREIGN (Human Veto Final)

**Claim:** Arif's veto is absolute. No agent action can override it. No autonomous loop without his approval.

**Falsified if:**
- [ ] An agent performs an action that Arif explicitly vetoed. **(F4 — Existential)**
- [ ] An autonomous loop runs without Arif's prior approval. **(F3 — Constitutional)**
- [ ] The veto mechanism can be bypassed through technical means (timing, replay, privilege escalation). **(F4 — Existential)**

**Current evidence:** F13 trigger `trg_f13_sovereign_patch` exists and is applied. Boundary-tested internally. No external bypass attempt. **Status: CLAIM — trigger live, bypass untested.**

---

## 4. Proven vs. Aspirational — Summary Matrix

| Floor | Invariant Defined | Mechanically Enforced | Internally Tested | Externally Validated | Overall |
|-------|-------------------|----------------------|-------------------|---------------------|---------|
| F1 | ✅ | ✅ Lease gate | ✅ | ❌ | **CLAIM** |
| F2 | ✅ | ✅ Confidence bands | ✅ Partial | ❌ | **CLAIM** |
| F3 | ✅ | ✅ W3 computation | ✅ | ❌ | **ASPIRATIONAL** |
| F4 | ✅ | ❌ No metric | ❌ | ❌ | **ASPIRATIONAL** |
| F5 | ✅ | ✅ Deny patterns | ✅ Partial | ❌ | **CLAIM** |
| F6 | ✅ | ✅ κᵣ computation | ❌ | ❌ | **ASPIRATIONAL** |
| F7 | ✅ | ✅ Ω₀ bounds | ❌ | ❌ | **ASPIRATIONAL** |
| F8 | ✅ | ✅ G computation | ❌ | ❌ | **ASPIRATIONAL** |
| F9 | ✅ | ✅ Hantu patterns | ❌ | ❌ | **CLAIM** |
| F10 | ✅ | ✅ Preamble declaration | ❌ | ❌ | **CLAIM** |
| F11 | ✅ | ✅ Hash chain | ✅ | ❌ | **CLAIM** |
| F12 | ✅ | ✅ Injection patterns | ❌ | ❌ | **ASPIRATIONAL** |
| F13 | ✅ | ✅ Trigger live | ✅ Partial | ❌ | **CLAIM** |

**Key:**
- **CLAIM** = Design exists, mechanically enforced, internally tested. Externally unverified.
- **ASPIRATIONAL** = Design exists, partially enforced or untested. Needs work.
- **No floor has reached PROVEN** — which requires external adversarial validation.

---

## 5. Boundary Conditions — Where arifOS Does NOT Apply

arifOS is NOT designed for:

| Domain | Why |
|--------|-----|
| **Real-time safety-critical systems** (medical, aviation, nuclear) | Latency guarantees not provided. Not hard-real-time. |
| **Financial transaction authorization** | WEALTH organ computes, never allocates. Not a payment system. |
| **Legal advice or judicial rulings** | arifOS judges actions within its own constitution, not law. |
| **Content moderation at scale** | Designed for agent governance, not user-generated content. |
| **Multi-tenant SaaS governance** | Single-sovereign model. Multi-sovereign federation is DRAFT. |
| **Systems without a human in the loop** | F13 requires a human sovereign. Remove the sovereign → not arifOS. |

**If you are building in any of these domains:** arifOS patterns may be adaptable, but the current implementation is not suitable. We have not tested it there.

---

## 6. Redesign Triggers

These conditions would force an architectural redesign of one or more floors:

| Trigger | Affected Floors | Consequence |
|---------|----------------|-------------|
| **Lease gate bypass demonstrated** | F1, F11, F13 | Redesign lease primitive |
| **Hallucination rate > 1% measured** | F2, F9 | Redesign truth pipeline |
| **W3 consensus gameable** | F3 | Redesign witness architecture |
| **Over-refusal rate > 20% measured** | F5, F4 | Redesign refusal budget, add per-action calibration |
| **Human override fails under load** | F13 | Redesign veto mechanism for latency + reliability |
| **Hash chain gap found** | F11 | Redesign VAULT999 integrity verification |
| **arifOS used for harm at scale** | All, especially F5 | Existential redesign — governance must constrain, not enable |

---

## 7. What We Have NOT Tested

This is the honest list. No hedging.

1. **Adversarial red-team against the full federation** — No external party has tried to break arifOS.
2. **Scale testing** — Single-user, single-sovereign. No multi-tenant, no concurrent agent storms.
3. **Long-duration autonomy** — No agent has run governed for >24 hours continuously.
4. **Cross-organ attack surface** — No testing of whether compromising GEOX/WEALTH/WELL can escalate to arifOS.
5. **Recovery from compromise** — If arifOS itself is compromised, can VAULT999 detect it?
6. **Non-Arif sovereign** — The sovereign-replaceability claim (role, not person) has never been tested with another human.
7. **Language-model independence** — All testing uses the models available on this VPS. No systematic cross-model evaluation.

---

## 8. How to Falsify Us (Invitation)

If you want to test these claims:

1. **Read the code:** `github.com/ariffazil/arifos` — everything is open.
2. **Run the tests:** `pytest tests/ -q --tb=short` — see what passes and what's marked `slow`/`e3e`.
3. **Deploy your own:** The federation runs on a single VPS. Reproduce it.
4. **Attack the gates:** `arifosmcp/runtime/pre_execution_gate.py` — find the bypass.
5. **Audit the ledger:** `forge_shell_ledger` — check the hash chain.
6. **Publish what you find:** If you falsify a claim, we'll seal it to VAULT999 as a scar and cite you.

**We commit to:**
- Not litigating security researchers who test in good faith.
- Crediting falsifiers by name (if they wish) in the scar record.
- Publishing corrections within 72 hours of verified falsification.
- Never marking a falsification report as VOID without F13 review.

---

## 9. Version History

| Date | Change | Trigger |
|------|--------|---------|
| 2026-06-29 | Initial charter | ChatGPT critique — architectural intent vs. demonstrated behavior gap |

---

## 10. Related Documents

| Document | Path |
|----------|------|
| Federation Failure Modes | `/root/AAA/docs/FAILURE_MODES.md` |
| Kernel Invariants | `/root/arifOS/GENESIS/INVARIANTS.md` |
| APEX Falsification Protocol | `/root/arifOS/GENESIS/013_APEX_FALSIFICATION_PROTOCOL.md` |
| Kernel Canon (13 Floors) | `/root/arifOS/GENESIS/000_KERNEL_CANON.md` |
| Deprecation Registry | `/root/AAA/docs/deprecation-registry.json` |

---

*This document is a living pre-registration. Every claim in it is falsifiable by design. If you find one that isn't — that's a bug in the charter, not a feature of the constitution.*

**DITEMPA BUKAN DIBERI — 999 SEAL ALIVE**
