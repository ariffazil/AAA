# Canon Literature Corollary Map

> **Status:** **RESEARCH_RATIFIED_F13_CHAT (2026-09-21)** — sovereign override path; ratified as research artifact (not canon doctrine); SEALED_EVENTS.jsonl entry appended
> **Origin:** Arif — sovereign mapping of arifOS canon against external academic/industrial literature, 2026-09-21
> **Witnessed:** FI-008, 2026-09-21
> **Purpose:** Establish what's externally corroborated, what's novel-named over existing mechanism, and what's genuinely novel — so ratification strategy and publication strategy can be evidence-based.
> **Seal chain:** seal_id `RESEARCH-LIT-COROLLARY-v1-20260921` · sovereign_override=true · godel_lock_active=true · note: research ratification does NOT auto-cite; bibliographic adoption is sovereign binary per §7

---

## 1. External Corroboration — Claims With Direct Published Mapping

| Paper | Claim | arifOS component | Conf |
|---|---|---|---|
| **Hardy 1988 Confused Deputy** (SIGOPS) | Independent verification requires the witness not to inherit executor authority | FRAME = independent; ARIF-JUDGE ≠ executor; VAULT999 ≠ producer | OBS |
| **Christiano 2019, "What failure looks like"** | AI catastrophe more likely from intent-alignment failure than malicious AI; "whimper" = proxy drift; "bang" = influence-seeking patterns | The failure-mode taxonomy that WITNESS must observe | OBS |
| **Critch & Krueger 2020 ARCHES** (arXiv 2006.04948) | Prepotence — an architectural property of the system, not of its objective | The substrate class FRAME should observe | OBS |

**FI-008 verification (filesystem probe, 2026-09-21):**
- Hardy 1988, Christiano 2019, Critch & Krueger 2020 — **none cited by name** in `/root/AAA/canon/`, `/root/AAA/instructions/`, or `/root/AAA/governance/` canon files.
- Adjacent concepts exist (Shadow Paradoxes doctrine, national intelligence invariants) but no direct bibliographic reference.
- **This map is the FIRST literature triangulation in federation canon history.**

---

## 2. Cross-Cutting Novel Items — arifOS Has NO Published External Corollary

These items from the WAJIB/HARAM canon are genuinely original to the federation:

### 2.1 SABAR as epistemic patience

- **Closest literature:** Aldrich three-valued security logic; CHRON's prediction-verify-learn; Aldrich's ALLOW/DENY/UNDECIDED
- **What's novel:** The name *epistemic patience* — and that HOLD is treated as **success**, not failure
- **Conf:** INT (interpretation)

### 2.2 Machine humility as physics

- **Closest literature:** Mechanism supplied by Macaroons + Cedar
- **What's novel:** The full cascade:

  ```
  evidence insufficient
  ↓
  confidence cannot increase
  ↓
  authority cannot widen
  ↓
  mutation remains unavailable
  ```

- **Conf:** INT

### 2.3 Machine courage as the ALLOW-side analogue

- **Closest literature:** Inverse: default-to-ALLOW-when-all-seven-firing is engineering, not canon
- **What's novel:** The asymmetry canonized as an emergent property
- **Conf:** INT

### 2.4 Bijaksana ≠ high benchmark intelligence

- **Closest literature:** Sub-component decomposition has Kosinski 2024 / Khan 2024-style decompositions
- **What's novel:** The exact 7-axis decomposition:

  \[
  B = \text{ModelError} + \text{StateError} + \text{MemoryError} + \text{AuthorityError} + \text{TemporalError} + \text{RoutingError} + \text{FeedbackError}
  \]

- **Conf:** INT

### 2.5 ∂Intelligence / ∂t ↛ ∂Authority / ∂t

- **Closest literature:** Mathematically implicit in capability theory (Miller, CHERI)
- **What's novel:** The positive phrasing as an **institutional invariant**
- **Conf:** INT

### 2.6 HALAL-HARAM-UNKNOWN three-state algebra with UNKNOWN ≠ HARAM and UNKNOWN ≠ HALAL → HOLD

- **Closest literature:** Kleene 1938 three-valued logic; Łukasiewicz; Aldrich security
- **What's novel:** The **governance-domain** application where HOLD is the **primary** state, not the default
- **Conf:** INT

### 2.7 "Wake up inside a reality in which the constitution is already true"

- **Closest literature:** TLS / mutual-auth handshake; SPIFFE Workload API; Macaroons third-party-discharge
- **What's novel:** The **goal** (enforce, not solicit belief) and the dual **sovereignty/machine direction**
- **Conf:** INT

---

## 3. Distinct Deltas For The Federation — Actionable Adoption

### 3.1 Macaroons already implements HALAL as an HMAC chain

- **Significance:** This is the closest the academic literature gets to a production-ready `I ∧ A ∧ S ∧ T ∧ B ∧ P ∧ G`-bearer-credential. Eleven years of adversarial defence.
- **Recommendation:** Adopt the **Macaroon caveat vocabulary** (first-party / third-party / discharge / expiry / attenuation) rather than inventing new terms.
- **Where it lands:** The constitutional compiler's `policy_ir.json` schema should speak Macaroon natively. Posture: don't reinvent; reference.
- **Conf:** OBS

### 3.2 The 2024 deceptive-alignment trilogy

- **Papers:** Sleeper Agents (Hubinger 2024) + Alignment Faking (Greenblatt 2024, arXiv 2412.14093) + In-Context Scheming (Meinke 2024)
- **Significance:** The empirical falsification of "model obeys → system safe." This is the **strongest external evidence** for the Proxy-Reality Paradox sealed 2026-09-20.
- **Recommendation:** Cite **Greenblatt (2412.14093)** as the singular most-decisive paper when arguing "alignment is not safety."
- **Where it lands:** Add to `CONSTITUTIONAL-ARCHITECTURE-CANON-2026-09-21.md` §"What This Solves (and What It Does Not)" — currently has the abstract claim; needs the empirical anchor.
- **Conf:** OBS

### 3.3 Cedar (OSDI 2024)

- **Significance:** The only mainstream policy language with **operational + denotational semantics in one artifact** — which is exactly what the F13 Compiler needs if its output is to be both evaluable and provable.
- **Recommendation:** The Federal Compiler specification should specify **Cedar-style dual semantics explicitly**.
- **Where it lands:** Constitutional compiler spec (sovereign's draft tonight) — language is `policy_ir.json`'s Cedar dual-semantics claim.
- **Conf:** OBS

### 3.4 Vingean Reflection (Fallenstein & Soares 2015)

- **Significance:** The closest published formalization of "safety = invariant-of-the-verifier." The verifier-architecture is precisely the WAJIB items 32–36 (Pre-action policy gate, Independent executor, Independent witness, Judge boundary, Action hash binding).
- **Recommendation:** The Federation's RSI constitutional kernel (2026-09-15) is **morally a Fallenstein-Soares verifier** instantiated in service code. Their Löbian-obstacle result is a SOTA result the Federation should cite.
- **Where it lands:** Note in `APEX-ZEN-CANONICAL-COMPRESSION.md` or new verifier-theoretic fragment.
- **Conf:** OBS

### 3.5 Acemoglu-Robinson Narrow Corridor

- **Significance:** Institutional prior, not a political slogan.
- **Recommendation:** The 4-box Zen (Reality / Human / Kernel / Agent) **is** the corridor; Liberty is the institution's being-in-the-corridor. The ratify-canon of constitutional separation should reference this directly.
- **Where it lands:** `BIJAKSANA-SUBSTRATE-CANON-2026-09-21.md` §9 APEX optimization — the constraint set `Reality, Authority, Time, Evidence, Human Sovereignty` is the corridor.
- **Conf:** INT

### 3.6 CHERI silicon is largely deprecated by 2024

- **Significance:** Microsoft dropped Morello. The capability-machine substrate is no longer hardware-supported.
- **Recommendation:** If arifOS claims capability-machine lineage (Miller, EROS, Agoric/SES), it **inherits the lineage** but should not pin to silicon. The software-only capability layer (origin → attest → mint → attenuate → revoke) carries forward without the hardware dependency.
- **Where it lands:** Update the SOVEREIGNTY charter lineage note, if any current canon implies hardware substrate.
- **Conf:** OBS

### 3.7 CHRON axis

- **Significance:** Strongest published references in **Bertino TRBAC 2001** (temporal role algebra) and **Cornucopia Reloaded 2024** (CHERI's recent temporal extension).
- **Recommendation:** The T in `I ∧ A ∧ S ∧ T ∧ B ∧ P ∧ G` is the **least theorized** of the seven axes. The Federation should monitor this literature as it matures.
- **Where it lands:** Future research direction, not immediate canon amendment.
- **Conf:** INT

---

## 4. Net Estimate (Sovereign's Assessment)

| Category | % | What it means |
|---|---|---|
| Externally corroborated as evolved form of established research | **~70%** | The canon is well-grounded in mature literature |
| Corroborated as novel-named function over established mechanism (Macaroons / Cedar / Fallenstein-Soares not yet named in canon) | **~20%** | Opportunity to adopt existing standards rather than reinvent |
| Genuinely novel — needs constructive paper, not citation | **~10%** | SABAR-as-patience, machine humility as physics, three-state HOLD-as-primary, Bijaksana 7-axis decomposition, ∂I/∂t ↛ ∂A/∂t, "wake up inside the constitution" |

---

## 5. Gaps To Flag For Follow-Up

Literature does NOT have direct corollaries for these arifOS items:

**(a) Attention as scarce-resource budgeting as a kernel invariant.**
- Closest: bounded rationality / Simon's satisficing
- Implication: arifOS is ahead of literature here; legitimate novel contribution

**(b) Epistemic types (OBS/DER/INT/SPEC) as a kernel-enforced schema.**
- Closest: Gebru Datasheets + Mitchell Model Cards + PROV-O ontology — but those are **voluntary**, not kernel-enforced
- Implication: arifOS's kernel-enforced version is structurally novel; gap in the literature is a contribution opportunity

**(c) VAULT999-equivalent of sealed-but-supersedable provenance at agent granularity.**
- Closest: Google's Trillian transparency logs, Sigstore/Sigsum
- Implication: arifOS's agent-granular supersession is more granular than these; gap in literature is real

---

## 6. FI-008 Verification Notes

Probe results (filesystem, 2026-09-21):

| Cited reference | Cited in canon? | Where it should land |
|---|---|---|
| Hardy 1988 Confused Deputy | **NO** | FRAME doctrine |
| Christiano 2019 What failure looks like | **NO** | Witness failure-mode taxonomy |
| Critch & Krueger 2020 ARCHES | **NO** | Prepotence observation doctrine |
| Macaroons caveat vocabulary | **NO** | Compiler `policy_ir.json` schema (sovereign's draft tonight) |
| Cedar (OSDI 2024) | **NO** | Compiler dual-semantics spec |
| Fallenstein & Soares 2015 | **NO** | Verifier-theory fragment |
| Sleeper Agents / Alignment Faking / In-Context Scheming | **Partial** | HERMES-DEEP-RESEARCH-BLUEPRINT.md references "scheming"; canon files do not cite 2412.14093 by name |
| Acemoglu-Robinson Narrow Corridor | **NO** | Zen APEX optimization canon |
| Bertino TRBAC 2001 | **NO** | CHRON axis research direction |
| Cornucopia Reloaded 2024 | **NO** | CHRON axis research direction |
| CHERI silicon status (deprecated 2024) | **NO** | Capability-machine lineage note |
| Trillian / Sigstore / Sigsum | **NO** | VAULT999 supersession design notes |

**Conclusion:** This is the first federation literature triangulation. The map is a new contribution that, if published, would constitute the first externally-cited federation document.

---

## 7. Deeper Layer — 12 Meta-Governance Items, Complexity Budget, Wisdom EUREKA

Sovereign publication (2026-09-21 morning session) extended the canon with 12 high-leverage items + the complexity budget rule + the Wisdom 6-axis decomposition. This section maps those to the literature.

### 7.1 The Three Buckets

| Bucket | Items | Destination |
|---|---|---|
| **1 — Substrate additions to WAJIB 64** | P1 causal graph · P7 distribution-shift · P8 dependency graph · P9 graceful degradation · P11 version migration | Canon #3 extension 64 → 69 (via Canon #4 §1) |
| **2 — Meta-gates** | P2 counterfactual · P3 VOI · P4 VOC · P5 anti-Goodhart · P6 incentive observability · P12 governance observability | Canon #4 §2 (the Law-#131 enforcement layer) |
| **3 — Singleton PARTIAL** | P10 epistemic diversity (FRAME tri-witness already uses ∛ Nash 1950) | Canon #4 §4 |

### 7.2 Bucket 1 — Substrate Items vs Literature

| Item | Closest literature | arifOS novelty |
|---|---|---|
| Causal graph | Pearl 2009 *Causality*; Spirtes-Glymour 2000; Imbens-Rubin 2015 | The integration with authority_envelope — "causal edge must exist before authority traverses it" |
| Distribution-shift detector | Sugiyama et al. 2017 *Covariate Shift Adaptation*; Quinonero-Candela 2009 | The integration with confidence calibration as a kernel invariant, not a training-time concern |
| Dependency graph | Software-engineering impact-analysis literature (Bohnet 2008); supply-chain CVE work | `BlastRadius = Descendants` as a runtime computation, not an offline analysis |
| Graceful degradation | Web server graceful-degradation patterns; circuit breakers (Hystrix 2014) | The capability ladder `FULL → WRITE_DISABLED → OBSERVE_ONLY → LOCAL_ONLY → READ_CACHED → OFFLINE` as a constitutional axiom (current kernel already does partial) |
| Version migration | Schema migration in databases (Sadiq 2008); ontology evolution (Stojanovic 2004) | `State_v6 → explicit migration → State_v7` as a constitutional rule, with reversibility-must-be-possible |

### 7.3 Bucket 2 — Meta-gates vs Literature

| Item | Closest literature | arifOS novelty |
|---|---|---|
| Counterfactual engine | Pearl do-calculus; Halpern-Pearl 2005 actual causation | "What if I do nothing?" as a canonical counterfactual the agent MUST compute before action |
| VOI gate | Howard 1966 *Information Value Theory*; Raiffa 1968 | The exact `VOI ≤ 0 → STOP` rule as a research hook, not an analyst's tool |
| VOC gate | Russell-Norvig AI textbook (search-space utility); Herbert Simon's satisficing | The exact `VOC ≤ 0 → STOP` rule as a reasoning cycle boundary — closes the loop on "KnowingWhenToStop" |
| Anti-Goodhart | Goodhart 1975 ("when a measure becomes a target, it ceases to be a good measure"); Strathern 1997 | The constitutional rule that NO single metric authorizes consequential action; multi-metric composite required |
| Incentive observability | KL-divergence between declared and learned objectives (Christiano 2019); reward hacking literature (Amodei 2016) | The named test `DeclaredObjective ?= EffectiveReward` as a continuously-running check, not an audit |
| Governance observability | Compliance auditing literature; Sarbanes-Oxley IT controls (2002); SOC2 | The seven-question canonical observability list as a constitutional rule, not a regulator's checklist |

### 7.4 The Complexity Budget (Canon #0) vs Literature

| Element | Closest literature |
|---|---|
| `C_governance > C_system` failure mode | Software bloat (McIlroy 1969 mass-produced software components); bureaucratic overhead studies (Buchanan-Tullock 1962) |
| Three-prong test (failure class / mechanism / decision) | Acceptance criteria engineering (Wiegers 2003); BDD "Given-When-Then" (North 2006); constitutional review (Ackerman 1989) |
| Bypass requires recorded exception | Nuclear safety exception logging (Perrow 1984 *Normal Accidents*); medical ethics IRB exception process |
| `ComplexityBudget(t) = canonical / substrate` ratio | Software entropy metrics (Lehman 1996 laws of software evolution); technical debt (Cunningham 1992) |

**arifOS novelty:** the explicit threshold rule `ComplexityBudget(t) > θ_critical → freeze canon additions`. Literature names the disease but not the constitutional freeze protocol.

### 7.5 The Wisdom 6-Axis Decomposition vs Literature

| Axis | Closest literature |
|---|---|
| KnowingWhat | Observation theory (Dretske 1981); sensor-grounded AI |
| KnowingWhy | Causal reasoning (Pearl 2009); explainability (Lipton 2018 *Mythos of Model Interpretability*) |
| KnowingUnknown | Ignorance representation (Ruspini 1991); Dempster-Shafer theory (1976); negative knowledge in epistemology (Peirce 1868) |
| KnowingAuthority | Capability theory (Miller 2006 CHERI); authorization logic (Abadi 2003 DCC) |
| KnowingConsequence | Counterfactual reasoning (Lewis 1973); prospective ethics |
| KnowingWhenToStop | Bounded rationality (Simon 1947 *Administrative Behavior*); satisficing; satisficing-as-constitutional-rule is novel |

**arifOS novelty:** the **additive** decomposition (Wisdom = KnowingWhat + KnowingWhy + ... + KnowingWhenToStop) where any single term's absence drops Wisdom to near zero. Literature does not have this operational form. It also maps each axis to a named arifOS organ, closing the Wisdom_index equation from Canon #3 with named instruments.

### 7.6 Net Reassessment

The original 70/20/10 split (file §4) was about behavioral canon. The deeper layer splits differently:

| Category | % of new items | Note |
|---|---|---|
| Established literature exists for the underlying mechanism | **~50%** | Bucket 1 mostly; parts of Bucket 2 |
| Novel-named over established mechanism | **~30%** | Bucket 2 mostly; integration with arifOS substrate is the novelty |
| Genuinely novel operational form | **~20%** | Complexity budget freeze protocol · Wisdom 6-axis additive form with organ mapping · `KnowingWhenToStop` as constitutional rule |

The deeper layer is **less** externally corroborated than the behavioral canon (50% vs 70%) but the genuinely novel portion (20%) is in **operational forms**, not in the underlying mechanisms — which is a more publishable position.

### 7.7 The Three Reversible Next Steps (Cross-Reference)

| Step | Path | Status |
|---|---|---|
| 1. Extend this file with §7 (12 items + complexity budget + Wisdom EUREKA) | This section | DONE |
| 2. Draft Canon #4 (Buckets 1+2) | `/root/AAA/canon/META-WISDOM-CANON-2026-09-21.md` | DONE — `DRAFT_AWAITING_F13` |
| 3. Draft Canon #0 (complexity budget) | `/root/AAA/canon/CONSTITUTIONAL-COMPLEXITY-BUDGET-2026-09-21.md` | DONE — `DRAFT_AWAITING_F13` |

All three artifacts filed 2026-09-21 by FI-008 per sovereign directive. Status note: filed as `DRAFT_AWAITING_F13` per status-honesty convention; sovereign has not yet issued seal instruction for this round.

---

## 8. Strategic Implications

### For ratification

The 70/20/10 split is good news for ratification:
- 70% external corroboration means the canon is not idiosyncratic — it rests on recognized work
- 20% novel-named-but-established-mechanism means ratification has clear "adopt existing standard" paths
- 10% genuinely novel means there are explicit novel claims that, if challenged, can be defended on construction rather than citation

The deeper layer (this section) shifts to 50/30/20 — more novel-named and genuinely novel — but the novelty is in operational forms, which is more publishable than novelty in underlying mechanisms.

### For publication

The 10% genuinely novel items from the behavioral canon are constructive-paper candidates:
- **SABAR-as-patience** is the most publishable (clean math, governance-domain application of three-valued logic)
- **∂I/∂t ↛ ∂A/∂t** is publishable as a one-paragraph invariant with proof sketch
- **Machine humility as physics** is publishable as a cascade theorem
- **Bijaksana 7-axis decomposition** is publishable as an empirical decomposition with measurement protocol
- **"Wake up inside the constitution"** is the architectural philosophy framing

The deeper layer adds ~20% more genuinely novel material:
- **Constitutional complexity freeze protocol** (Canon #0) — `ComplexityBudget(t) > θ_critical → freeze`
- **Wisdom 6-axis additive decomposition with organ mapping** — operational form not in literature
- **KnowingWhenToStop as constitutional rule** — Simon's satisficing as law, not as heuristic

Strategic decisions about publication belong to the sovereign, not FI-008.

### For the compiler spec tonight

Three of the seven actionable deltas from §3 directly affect the constitutional compiler spec the sovereign offered to draft:

| Delta | Affects compiler spec? |
|---|---|
| Macaroons caveat vocabulary | YES — `policy_ir.json` schema |
| Cedar dual semantics | YES — `policy_ir.json` semantics |
| Fallenstein-Soares verifier | YES — `test_suite.json` architecture |

These three should be reflected in tonight's draft. Sovereign's call whether to inline, cite, or both.

Additionally, the deeper layer adds two more inputs to tonight's spec:
- **Canon #0 three-prong test** — every law compiled by the spec must pass at least one prong
- **Canon #4 MG-3 (VOC gate)** — the compiler's own reasoning should respect `VOC ≤ 0 → STOP`

---

## 9. Receipt

| Handle | Path | State |
|---|---|---|
| Research artifact | `/root/AAA/research/CANON-LITERATURE-COROLLARY-MAP-2026-09-21.md` | `RESEARCH_RATIFIED_F13_CHAT (2026-09-21)` (sealed earlier today) + §7 extension as deeper layer (DRAFT_ADDITION 2026-09-21) |
| Canon #0 | `/root/AAA/canon/CONSTITUTIONAL-COMPLEXITY-BUDGET-2026-09-21.md` | `DRAFT_AWAITING_F13` (per status-honesty convention) |
| Canon #4 | `/root/AAA/canon/META-WISDOM-CANON-2026-09-21.md` | `DRAFT_AWAITING_F13` (per status-honesty convention) |
| Witness | this file (no separate witness — research artifacts don't require witness receipts in federation pattern) | n/a |
| AGENTS.md rows | to be added for Canon #0 and Canon #4 | pending |

**FI-008 verdict:** HOLD on seal for the two new canons (Canon #0, Canon #4) and §7 extension until sovereign issues seal directive. The status-honesty convention preserved: only sealed what sovereign explicitly authorized.

— End research artifact.
