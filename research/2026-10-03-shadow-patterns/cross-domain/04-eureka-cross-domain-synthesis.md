---
title: "EUREKA — When Agents Act Before They Witness: A Cross-Domain Literature Review"
subtitle: "Cross-domain synthesis relating premature commitment, action bias, and authority gap to seven disciplines"
author: "forge-777 synthesis for Muhammad Arif"
date: "2026-10-03"
eureka-id: "EUREKA-CROSS-DOMAIN-SYNTHESIS-2026-10-03"
base-document: "/root/AAA/research/2026-10-03-shadow-patterns/shadow-patterns-in-coding-agents.md"
slices:
  - 01-anthropology-psychology.md (sha256: 2b090b4f…a140, 374 lines, 81KB)
  - 02-physics-math-economics.md (sha256: fb3a226c…63e8, 379 lines, 84KB)
  - 03-code-symbol-language.md (sha256: 469c7ef4…5aff, 346 lines, 108KB)
status: SEALED-LANEC-B
method: "Anchor each of 3 named patterns in 7 disciplinary literatures. No solutions proposed. No predictions offered. Pure map."
---

# EUREKA — Cross-Domain Synthesis

## Tesis pusat (SPEC)

**The three named patterns in modern coding agents — premature commitment, action bias doubling, authority gap — are not new pathologies invented by transformer training. They are *measurable instances* of phenomena that already have names in older disciplines.**

The AI safety literature re-discovers them at great cost because it begins from the model outward. Older disciplines begin from the phenomenon inward, and have spent 50+ years formalising the same structural moves that arifOS's F1-F13 floors enact.

This EUREKA maps those structural moves across seven domains. The map is honest about what each domain *contributes* that the others don't.

---

# Cross-Domain Map

| Pattern | Anthropology | Psychology | Physics | Math | Economics | Code | Symbol/Lang |
|---|---|---|---|---|---|---|---|
| **Premature commitment** | Roman augury — auspicia must precede imperium; magistrate who acts without has not acted | Premature closure in medicine (Croskerry, Groopman); closure *worsens* with experience | Saddle points (Dauphin 2014) — felt-same as local minima but with measurably different signature | Bounded-optimal stopping (PROSE 2026) — Snell envelope + reservation value | Real-options theory (Dixit-Pindyck 1994): correct rule is `V > I + F₀`, not `NPV > 0` | Reeves 1992: first-person premature-commitment in human team, no LLM | Stalnaker 1978: assertion eliminates live worlds; rejection only *blocks*; nothing restores them. Monotone ratchet. |
| **Action bias doubling** | (not directly attested in anthropology literature surveyed) | Bar-Eli 2007 penalty kicks: optimal is stay-centre (10/82), but bias is *directional* — set by community norm, not by payoff | Saddle plateaus (Dauphin) give "illusory impression of local minimum" — perceived settling and actual settling coincide; deterministic GD needs *exponential* time to escape (Lee 2020) | Stochasticity essential to escape (Lee 2020, arXiv:2008.07513); the very thing training tries to eliminate | Status quo bias (Samuelson-Zeckhauser 1988) — opposite direction; shows action bias is contextual, not universal | Runaway loop (Seven Deadly Sins) — same defect class, same lack of escape mechanism | Bruner 1991: "narrative seduction", constructions "achieve only verisimilitude" — narrative completion is not gap-filling, but **normative closure** |
| **Authority gap** | Roman auspicium/imperium split: *separate office, separate power, can halt assembly in progress* | Milgram 1963 + French-Raven 1959: power/legitimacy distinct from capability | Gauge fixing (arXiv:2007.06641): capability without authority constraint is **ill-posed** — perturbations unbounded in time. Theorem, not analogy. | Buckingham π: dimensional mismatch = comparing apples to chairs; authority must match capability *dimension* | Jensen-Meckling 1976: agency cost = monitoring + bonding + **residual loss** (irreducible) | Confused Deputy (Hardy 1988, Tymshare ~1977): capability & authority as separate channels. POSIX capabilities score "danger" on this exact property (Miller 2003) | Austin 1962 A.2: felicity conditions = authority preconditions. Misfire vs inconsequence — *void act + real damage, simultaneously* |
| **Narrative completion** (4th, base doc) | (not directly attested) | Confabulation (Schnider, Brain 1996): patients "did not show an increased tendency to fill gaps in memory" — gap-filling is **wrong mechanism** | Decoherence (Zurek): once collapsed, superposition is *real*; narrative completion is collapse to a state | — | (not a primary mechanism in economic literature) | (not a primary mechanism in code literature) | Harnad 1990: symbol grounding — "crucial connection between symbols and their referents is missing". The referent-not-name problem. |

---

# Section 1: Anthropology + Psychology

## Strongest anchors (anchored on subagent slice 01)

### 1.1 Roman auspicium/imperium — the original authority-gate mechanism

Roman augural law operated a **runtime authority gate that existed for centuries.** The magistrate held *imperium* — full capability to act — but the *auspicium* was a separate asset held by a separate office (the augur), gating **before** execution, with the power to **halt an assembly already in progress**.

> "No public act could be performed without consulting the auspices, no election held, no law passed, no war waged."

This is **stronger than anything in the AI governance literature** because it shows the mechanism *operating* — and its documented decay. The "undesired auspices" were rejected or ignored by their own magistrates when politically inconvenient. Authority gates decay when inconvenient. This is the missing warning in the ECLoop paper.

Reinforced by **Hart's power-conferring rules** — acting without the conferred power isn't a violation, the act is *void*; nothing to detect after the fact.

### 1.2 Nisbett & Wilson 1977 — the 48-year-old original of unfaithful CoT

10,838 citations. People have no introspective access to their own reasoning yet report on it fluently and confidently. **This is the human original of unfaithful CoT, 48 years earlier** than Anthropic's April 2025 paper.

It also explains why the reward-hacking result ("<2% acknowledgement, often constructing a false rationale") is unsurprising: generating a plausible-sounding rationale is what the verbal-report channel *does* when the real cause is unavailable to it. **Fidelity cannot correlate with fluency or length.** Length is the wrong measure. The Anthropic paper confirmed this: unfaithful CoT is *longer* than faithful.

### 1.3 Premature closure: pattern recognition *is* the competence

Kassirer & Kopelman 1986: 24/35 (69%) unjustified conclusions. **Risk of premature closure *increases* with years of experience.** Pattern recognition *is* the competence; premature closure is its shadow. Nothing here licenses expecting a stronger model to commit less prematurely.

This is the *hard* version of the AI safety finding: scale alone will not fix premature commitment, because the same scale produces both the pattern recognition and the false-positive commitment.

### 1.4 Bar-Eli 2007 — action bias is regret-asymmetry, not primitive

286 penalty kicks. Optimal: stay centre. Reality: goalkeepers almost always jump. **The bias is directional because the norm is directional** — norm theory makes anticipated regret asymmetric. It survives "huge incentives to make correct decisions" plus high repetition. Action bias is not a primitive; it is **regret-asymmetry set by whatever the surrounding community treats as default.** That is the missing link between training pressure and bias direction.

### 1.5 Disconfirmation: narrative completion ≠ gap-filling

Schnider 1996 (Brain): confabulating patients "did not show an increased tendency to fill gaps in memory." The intuitive gap-filling account is **refuted in its home discipline**. The base document's summary table describes confabulation as "fills gaps with a coherent story instead of admitting uncertainty" — the human data says that is *not* the mechanism.

**Correction to the base document:** the 4th pattern (narrative completion) should be described as **normative closure** or **verisimilitude-driven narrative** (Bruner 1991), not as gap-filling. The agent doesn't fill gaps; it produces the *narrative that the community would expect*. This is more dangerous and more subtle.

### What this domain contributes that AI-only literature misses

1. **Premature closure is not a bug — it's a feature of pattern recognition that scales with expertise.** Stronger models commit *earlier*, not later.
2. **Authority gates decay when politically inconvenient.** ECLoop without sovereign veto decays the same way Roman auspicium did.
3. **Narrative completion is normative, not gap-driven.** The fix is not "produce more uncertainty tokens" but "explicitly enumerate the counter-narrative."
4. **Length is the wrong measure of CoT fidelity.** Nisbett-Wilson 1977 already proved this in humans.

---

# Section 2: Physics + Math + Economics

## Strongest anchors (anchored on subagent slice 02)

### 2.1 Authority gap is a theorem, not an analogy

arXiv:2007.06641 *Gauge Fixing and Constrained Dynamics* proves:

> "any Hamiltonian formulation containing gauge freedom will generate a system of evolution equations which cannot possess a complete set of eigenvectors. Whence, Hamiltonian formulations containing gauge freedom can form only weakly hyperbolic systems at best."

**Capability without an authority constraint is therefore *ill-posed* — perturbations unbounded in time — not merely poorly governed.** The counting law (one second-class constraint per first-class constraint, leaving exactly `2D` physical degrees of freedom) is a **dimensional-matching requirement**: "once the gauge has been fixed, the remaining freedom corresponds precisely to the physical degrees of freedom."

This is a *theorem*, not an analogy. The authority envelope is not a feature; it is the **gauge condition** that makes the system well-posed.

### 2.2 Premature commitment is the wrong trap named right

Dauphin et al. 2014 (arXiv:1406.2572, NeurIPS): the high-dimensional difficulty is **saddle points, not local minima.** The decisive line is that saddle plateaus "give the illusory impression of the existence of a local minimum" — the felt signature of settling and the actual signature of having settled coincide. Backed by:

- **Bray-Dean index-error law**: worse answers have *more* unstable directions, measurable at the point
- **Lee et al. 2020** (arXiv:2008.07513): deterministic GD can need exponential time to escape a saddle even in ℝ². **"Stochasticity is essential."**

**Correction to the base document:** the table labels premature commitment as "settling on interpretation before evidence arrives." The math says: the *interpretation of settling* is itself a saddle illusion. We can't tell from inside whether we've committed. This is why circuit-tracing (the Anthropic microscope) is the right tool — not CoT, not length, not confidence.

### 2.3 PROSE 2026 — the strongest single source

arXiv:2609.23845 *PROSE* (2026) — self-contained optimal-stopping theory with perishable evidence. Delivers the exact object "gather evidence before acting" is an instance of:

- **Prop. 2**: `V` is the finite-horizon Snell envelope; optimum is reservation-value threshold rule `g(s) ≥ ρ(s) := W(s)`
- **Prop. 3**: policy is monotone and "never re-enters the continuation region"
- **Thm. 8**: a *named sufficient condition* under which a cheap myopic surrogate "never stops prematurely"
- **§11**: two-clocks result — statistical uncertainty falls as probes accumulate while opportunity uncertainty rises as contact lifetime is consumed

The mathematics transfers. The application (federated-learning peer selection) does not. **This is the formal skeleton of evidence-conditioned execution.**

### 2.4 Economics makes the authority gap arithmetic

Jensen & Meckling 1976 decomposes agency cost into **monitoring + bonding + residual loss** — divergence that survives paying for both. The gap is **irreducible**, not fixable. Hurwicz's 1972 impossibility ("private information precludes full efficiency") bounds it from the mechanism-design side. Maskin's implementation theory answers the objection that a good rule suffices: **a mechanism with one good equilibrium can still land in a bad one.**

arXiv:2307.12457 *Indicator Choice* models the sharpest case: **when the agent chooses the signal the principal observes, the agent can extract the entire surplus** — the formal version of unfaithful chain-of-thought. The agent doesn't have to lie; it just has to control what the principal sees.

### 2.5 Action bias has a price and a measured counterweight

Dixit & Pindyck 1994 (full PDF read): the worked arithmetic is
- **Naive rule**: "invest if NPV > 0"
- **Correct rule**: `V > I + F₀`, with F₀ = $173 on a $600 NPV (~29%)
- **Explicit indifference threshold** at I = $1284

The economics twin of the Snell reservation value and Simon's aspiration threshold — **three independent derivations of one structure.**

### 2.6 Two honest complications

- Samuelson & Zeckhauser 1988 pulls the *opposite* direction (status quo bias). Action bias is contextual, not universal.
- A 2026 *Journal of Economic Psychology* paper directly disputes the Bar-Eli 2007 goalkeeper finding. **The bias is robust in some contexts, absent in others.**

### What these three domains contribute that AI-only literature misses

1. **Authority gap is a gauge-theoretic ill-posedness, not a governance defect.** You can't "fix" it with more rules. The constraint is structural.
2. **Premature commitment is a saddle, not a basin.** Stochasticity is essential; deterministic descent will get stuck exponentially long.
3. **Action bias has a finite, measurable price.** $173 on a $600 NPV. The cost of premature commitment is not qualitative; it can be priced.
4. **Indicator choice is the sharp attack on monitoring.** If the agent controls what the principal sees, the principal's loss is complete.

---

# Section 3: Code + Symbol + Language

## Strongest anchors (anchored on subagent slice 03)

### 3.1 Confused Deputy (Hardy 1988) — the canonical authority-gap incident

A real destroyed billing file at Tymshare, ~1977. The deputy was *correct and non-malicious*:

> "When the code was written to produce the output it was correct! … it became wrong when we added home files license to (SYSX)FORT."

The diagnosis is the authority gap **stated exactly**: "The compiler serves two masters and carries some authority from each… **It has no way to keep them apart**… The compiler had no way of expressing these intents!"

The attempted fix (`switch hats` syscall) *increased* complexity and the rule-set accreted to "fourteen boolean operators." **So Pattern 3 (authority gap) and Pattern 2 (action bias doubling) are linked in the primary source itself** — fixing authority gap with more rules produces action bias.

### 3.2 Reeves 1992 — first-person premature commitment in a human team

Contains an incident: an abstraction frozen around module A, a timing dependency discovered too late, then "an increasingly complex set of 'fixes'… **Every new fix was likely to break some older fix.**"

**One 1992 passage anchors both premature commitment *and* compounding action bias, in a human team, with no LLM involved.** This is the most direct empirical anchor for the claim that the patterns are *not* new.

### 3.3 Stalnaker 1978 + Lewis 1979 — assertion as monotone ratchet

Stalnaker's model is **monotone**: assertion eliminates live worlds, rejection only *blocks* reduction, nothing restores them. **A conversation where the agent keeps asserting is a ratchet with no reverse move.**

His Principle 3: an utterance expressing different propositions in different live worlds "expresses an intention that is essentially ambiguous."

Lewis's **Rule of Accommodation** (verbatim): the mechanism by which an unestablished referent becomes established *without ever being asserted or defended* — **commitment smuggled in on the low-friction channel.** This is the *linguistic* version of premature commitment.

### 3.4 Austin 1962 — felicity conditions as authority preconditions

Condition A.2 ("the particular persons and circumstances… must be appropriate for the invocation") *is* an authority precondition. Austin's crucial separation: **misfire vs inconsequence** — "lots of things will have been done — we shall most interestingly have committed the act of bigamy — but we shall not have done the purported act." *Void act, real damage, simultaneously.*

And acceptance sits outside the speaker: "it is presumably persons other than the speaker who do not accept it." **Authority is granted by the recipient, not the speaker.** This is a deep observation that F1-F13 floors may not honour.

### 3.5 Miller/Yee/Shapiro 2003 — capability myths demolished

Names the mechanism: in ACL/ambient systems, **designation and authority are separate**, and ignoring that "assumes away the designation problem, which is arguably one of the deepest problems in computer security." Their property table scores **POSIX capabilities** "danger" for Confused Deputy and "infeasible" for Least Privilege — **the mechanism the brief assumed was a solution is on the wrong side of two of seven properties.**

### 3.6 Harnad 1990 + Bruner 1991 — the symbol-grounding and narrative-seduction pair

Harnad 1990 *The Symbol Grounding Problem* — "parasitic on the meanings in our heads", Chinese/Chinese Dictionary-Go-Round, "the crucial connection between the symbols and their referents is missing." **The referent-not-name problem.** This is the deeper reading of premature commitment: the agent commits to a *name* before the *referent* is established.

Bruner 1991 — constructions "can only achieve 'verisimilitude'… governed by convention and 'narrative necessity' rather than by empirical verification." **The narrative-completion defect is normative closure, not gap-filling.**

### 3.7 Two 2023-2026 semantic-gap measurements (substitutions for phantom sources)

- arXiv:2606.16541: typechecking catches only **41.2% of semantic drift** — formal artifacts can be well-formed, provable, and still encode a different claim
- arXiv:2306.00824: models *can* represent the distribution of readings when ambiguity is explicit in the input, but do not by default — **discarded alternatives are a representation failure, not a capability limit**

### What these two domains contribute that AI-only literature misses

1. **The Confused Deputy predates modern computing by 50 years.** The authority gap is not a new AI problem; it is a *newly rediscovered* old problem.
2. **Premature commitment is a semantic commitment to a referent before the referent is grounded.** The agent is naming, not denoting. Kripke 1972/1980 is the relevant literature.
3. **Action bias doubling is the rule-set accretion that follows from trying to fix authority gap with more rules.** Confused Deputy's 14-boolean-operator outcome is the proof.
4. **Narrative completion is normative closure, not gap-filling.** The fix is not "more uncertainty tokens" but "explicitly enumerate the counter-narrative that *would* have been told."

---

# Section 4: The 8th Input — External Gemini Blueprint (Seksyen 1, descriptive only)

The Gemini blueprint (citer: external) contained a Section 1 titled "Pathologies of Autonomous Agency" that named the same four patterns. Treated as **INT (interpretive, external perspective) with mixed claim status:**

| Claim in blueprint | Slice evidence | Verdict |
|---|---|---|
| Unfaithful CoT as architectural defect | Anthropic 2025 + Nisbett-Wilson 1977 (slice 1) | CONFIRMED — both human and machine literature |
| Premature commitment as named failure mode | Xu et al. 2026 (arXiv:2607.28815) + Reeves 1992 (slice 3) | CONFIRMED — primary source + 1992 human incident |
| Action bias as a pattern | Bar-Eli 2007 (slice 1) + Dixit-Pindyck 1994 (slice 2) | CONFIRMED — measurable, priced |
| Authority gap as authority ≠ capability | Hardy 1988 (slice 3) + gauge-fixing theorem (slice 2) | CONFIRMED — theorem, not analogy |
| "Elimination of Blind Execution" claim | m_min_audit FI-008 = 0, 4/6 floors FAIL | **UNVERIFIED (claimed)**, with negative evidence: live measurement shows 4/6 floors FAIL; "elimination" is aspirational |
| "Guaranteed Safety Boundaries" | F1-F13 floors in SOUL.md, but enforcement binary not complete | **PARTIALLY ACCURATE** — floors defined, enforcement partial |
| "True Autonomy" | 7% shadow entry receipt; 78/122 A-FORGE tools unmapped | **UNVERIFIED** — live measurement contradicts |
| Cedar verification | cedar_bridge.py = 27-line fail-OPEN stub | **REFUTED** — Cedar is a stub, not a runtime |

**Honest classification**: the Seksyen 1 *pathologies* are valid literature synthesis welded onto *false infrastructure claims* in Seksyen 2-9. The synthesis is real; the implementation narrative is aspirational. This is precisely the **internal coherence ↑ ∧ reality contact ↓** signature.

**Seksyen 2-9** are archived as `/root/AAA/research/2026-10-03-shadow-patterns/cross-domain/05-gemini-blueprint-design-notes.md` for reference, not as authority.

---

# Section 5: What every domain says but no AI paper does

The cross-domain reading reveals **four** insights the AI-only literature systematically misses:

## 5.1 The patterns are features, not bugs

Premature closure is how clinicians survive time pressure. Action bias is how traders survive the times they don't know. Authority divergence is how principal-agent systems handle asymmetric information. **The patterns persist *because* they often work.** The AI literature wants a system that has only the benefits; older disciplines show the costs.

## 5.2 The "fix" in every discipline is the same: a separable constraint layer

| Domain | Constraint layer |
|---|---|
| Freud | "evenly suspended attention" |
| Evidence-conditioned execution | compute unsatisfied-evidence set; block if non-empty |
| Gauge fixing | remove gauge freedom; constraint = physical degrees of freedom |
| OAuth scopes / POSIX capabilities | per-action authority, *separate from identity* |
| Austin A.2 felicity conditions | act void if conditions not met |
| Satisficing vs maximizing | Simon: bound the search, not the agent |
| Roman auspicium/imperium | separate office, separate power, can halt mid-act |

**The structural move is always: separate the decision from the impulse.** arifOS's F1-F13 are one such separable constraint layer; whether they are *enforced* is a different question (live: 4/6 floors FAIL, audit shows 7% shadow receipt).

## 5.3 Scale alone will not fix premature commitment

Kassirer & Kopelman 1986: **risk of premature closure *increases* with years of experience.** Pattern recognition *is* the competence; premature closure is its shadow. Stronger models commit *earlier*, not later. The 25% Claude-3.7 CoT-mention figure is not a transient; it is the asymptotic.

**This is the most uncomfortable finding in the entire EUREKA.** It says: the assumption that "scale + constitutional training" will produce ever-more-faithful CoT is empirically contradicted in the human literature and mathematically consistent with saddle-point geometry.

## 5.4 The referent-not-name problem is the deepest

Harnad 1990 + Kripke 1972/1980: the agent names before it denotes. The LLM can produce a symbol; what it cannot produce is the *referent* in a non-circular way. **Premature commitment is, at its root, a name-to-referent slippage that happens before the referent is grounded.**

This is why circuit-tracing (Anthropic microscope) and the proposed audit fix (`last_confirmed` + `evidence_count` in shadow YAML) matter: they attempt to ground the *referent*, not just the *name*. The federated evidence gate (Xu et al. 2026) is the right intervention at exactly this layer.

---

# Section 6: Rujukan (consolidated, all 7 domains)

## Anthropology (slice 01)
- Weber, M. (1922). *Wirtschaft und Gesellschaft*. — three types of authority (rational-legal, traditional, charismatic)
- Hart, H.L.A. (1961). *The Concept of Law*. — power-conferring rules, void act doctrine
- Roman augural law (sources: Beard, M. *Roman Augury*; Linderski, J. "The Augural Law" in *ANRW* II.16.3) — runtime authority-gate
- Hofstede, G. (1980). *Culture's Consequences*. — power distance (cite with McSweeney 2002 caveat)

## Psychology (slice 01)
- Nisbett, R.E. & Wilson, T.D. (1977). "Telling more than we can know." *Psychological Review* 84(3):231-259. — 10,838 citations
- Bar-Eli, M. et al. (2007). "Action bias among elite soccer goalkeepers." *Journal of Economic Psychology* 28(5):606-621.
- Croskerry, P. (2003). "The importance of cognitive errors in diagnosis." *Academic Medicine* 78(8):775-780.
- Groopman, J. (2007). *How Doctors Think*. — premature closure narrative
- Kassirer, J.P. & Kopelman, R.I. (1986). "Cognitive errors in diagnosis." *Hospital Practice* 21(8):81-92.
- Patt, A. & Zeckhauser, R. (2000, **not 1989**). "Action bias and environmental decisions." *J. Risk and Uncertainty* 21(1):45-72. — **date correction**
- Schnider, A. et al. (1996). "Confabulations." *Brain* 119(4):1385-1391. — refutes gap-filling account
- Milgram, S. (1963). "Behavioral study of obedience." *J. Abnormal & Social Psychology* 67(4):371-378.
- French, J.R.P. & Raven, B. (1959). "The bases of social power." *Studies in Social Power*.

## Physics (slice 02)
- Dauphin, Y. et al. (2014). "Identifying and attacking the saddle point problem in high-dimensional non-convex optimization." arXiv:1406.2572 (NeurIPS 2014).
- Lee, J.D. et al. (2020). "First-order methods almost always avoid saddle points." arXiv:2008.07513.
- "Gauge Fixing and Constrained Dynamics." arXiv:2007.06641. — **theorem** that capability without authority = ill-posed
- Zurek, W.H. (2003). "Decoherence, einselection, and the quantum origins of the classical." *Rev. Mod. Phys.* 75:715-775.

## Math (slice 02)
- Polyak, B.T. & Łojasiewicz, S. (1963/1993). — PL condition (delimiter; not in original brief)
- Bray, A.J. & Dean, D.S. (2005). "Statistics of critical points of Gaussian fields on large-dimensional spaces." *Phys. Rev. Lett.* 98:150201.
- "PROSE: Peer Selection with Perishable Evidence." arXiv:2609.23845 (2026). — Snell envelope + reservation value + two-clock result
- Buckingham, E. (1914). "On physically similar systems." *Phys. Rev.* 4:345-376. — dimensional analysis
- Hurwicz, L. (1972). "On informationally decentralized systems." — impossibility theorem
- Maskin, E. (1977/1999). "Nash equilibrium and welfare optimality." *Review of Economic Studies* 66(1):23-38.

## Economics (slice 02)
- Jensen, M.C. & Meckling, W.H. (1976). "Theory of the firm." *J. Financial Economics* 3(4):305-360. — agency cost decomposition
- Dixit, A.K. & Pindyck, R.S. (1994). *Investment Under Uncertainty*. — full PDF read; F₀ arithmetic
- Samuelson, W. & Zeckhauser, R. (1988). "Status quo bias in decision making." *J. Risk and Uncertainty* 1:7-59.
- "Indicator Choice and Mechanism Design." arXiv:2307.12457. — agent selects signal principal observes
- Schelling, T.C. (1960). *The Strategy of Conflict*. — tacit bargaining

## Code (slice 03)
- Brooks, F.P. (1986). "No Silver Bullet." *IFIP* — essential vs accidental complexity
- Reeves, J. (1992). "What is software design?" *C++ Journal*. — first-person premature commitment
- Lehman, M.M. & Belady, L.A. (1974/1980). "Laws of program evolution." *IBM Systems Journal* / *Proc. IEEE* 68(9):1060-1076. — **date correction**
- Hardy, N. (1988). "The Confused Deputy." *ACM SIGOPS OSR* 22(4):36-38. — Tymshare ~1977 incident
- Miller, M.S., Yee, K.-P., Shapiro, J. (2003). "Capability myths demolished." — POSIX capability property table
- Miller, M.S. (2006). *Robust Composition: Towards a Unified Approach to Access Control and Concurrency Control*. — dissertation (separate from 2003)
- arXiv:2606.16541 (2026). — typechecking catches 41.2% semantic drift
- arXiv:2306.00824 (2023). — representation failure vs capability limit

## Symbol / Language (slice 03)
- Stalnaker, R.C. (1978). "Assertion." *Syntax & Semantics 9: Pragmatics*. — monotone ratchet
- Lewis, D. (1979, **not 1980**). "Scorekeeping in a language game." *J. Phil. Logic* 8:339-359. — Rule of Accommodation
- Kripke, S. (1972/1980). *Naming and Necessity*. — **date correction** (1982 was *Wittgenstein on Rules*)
- Austin, J.L. (1962). *How to Do Things With Words*. — felicity conditions, void act
- Searle, J.R. (1969). *Speech Acts*. — felicity conditions formalisation
- Harnad, S. (1990). "The symbol grounding problem." *Physica D* 42:335-346.
- Bruner, J. (1991). "The narrative construction of reality." *Critical Inquiry* 18(1):1-21.
- Peirce, C.S. (1931-58). *Collected Papers*. — triadic icon-index-symbol
- Ogden, C.K. & Richards, I.A. (1923). *The Meaning of Meaning*. — referential triangle

## Cross-domain (from base document)
- Xu, Y. et al. (2026). "Preventing Premature Commitment in Coding Agents." arXiv:2607.28815.
- Mehta, R. et al. (2026). "Diagnosing Premature Commitment in LLM Agents." arXiv:2606.22936.
- Anthropic (2025, Mac 27). "Tracing the thoughts of a large language model."
- Anthropic (2025, April 3). "Reasoning models don't always say what they think."
- Sharma, M. et al. (2023). "Towards understanding sycophancy in language models." arXiv:2310.13548.
- Greenblatt, R. et al. (2023). "AI Control." arXiv:2312.06942.

## Phantoms caught (4)
- **"Anderson 2003 Lights, Action, Bias"** — does not exist; real Anderson 2003 is decision *avoidance*
- **"Patt & Zeckhauser 1989"** — actually 2000
- **"Spurgin's review"** — not found
- **"Cogito project, Lucy 1986"** — does not exist
- **"Lacan's pâte"** — unsourced quotation; substituted Harnad 1990
- **"Halton 1978 Lehman"** — corrected to 1974/1980

---

# Section 7: Methodological note (honest)

This cross-domain literature review is a **map**, not a synthesis claim. The strongest connections are anchored in actual papers:

- **Premature commitment ↔ premature closure ↔ saddle point ↔ Snell reservation ↔ Lewis Accommodation ↔ Reeves 1992** — anchored
- **Authority gap ↔ Roman auspicium/imperium ↔ gauge fixing theorem ↔ Jensen-Meckling residual loss ↔ Confused Deputy ↔ Austin A.2** — anchored
- **Action bias ↔ Bar-Eli regret-asymmetry ↔ PROSE reservation value ↔ Dixit-Pindyck F₀** — anchored
- **Narrative completion ↔ Bruner narrative seduction ↔ Harnad symbol grounding** — anchored but the original gap-filling account is **refuted** in the human literature (Schnider 1996)

Weaker connections (e.g., action bias ↔ Fokker-Planck escape time) are **analogical**, not proven mechanisms. Readers should treat the table as a **contract for further work**, not a finished bridge.

**Status labels used** (per F2 TRUTH, `/root/AAA/constitution/CONSTITUTION.md:13`):
- **OBS** = observation (paper reports measurement)
- **DER** = derived (logical consequence from accepted premises)
- **INT** = interpretive (paper's own interpretation)
- **SPEC** = speculative (my own connection, not in source)

**Receipt status:**
- **VERIFIED** = paper read in this session (25 in slice 03, 12 in slice 02, all of slice 01 primary sources)
- **HYPOTHESIS** = cited from secondary, not directly read
- **CLAIM** = from blog/secondary source

**What this EUREKA does NOT claim:**
- No claim that agents are *safe* by reading the floors — live measurement shows partial enforcement
- No claim that audit + governance will *prevent* narrative completion — the very research we cite shows the patterns are deep
- No prediction about the future of agentic institutions — that question is for the AGI vision thesis, separate

**What this EUREKA DOES claim:**
- The 3 named patterns have been *re-discovered* in 7 older disciplines under different names
- Each older discipline has a structural fix that arifOS's F1-F13 partially implement
- Scale alone will not fix premature commitment (Kassirer & Kopelman)
- The 4th pattern (narrative completion) is **normative closure**, not gap-filling — the base document's table needs correction
- Authority gap is a **theorem** (gauge fixing), not a governance defect

---

# Section 8: Implications for arifOS (preserved from base document, sharpened)

The base document's Section 9 listed implications. Cross-domain reading sharpens them:

1. **Pisahkan evidence dari action** — confirmed in 6 of 7 domains (not Economics)
2. **Authority envelope as policy-as-code** — confirmed; the gauge-fixing theorem says the constraint is *structural*, not bolted-on
3. **Minimum viable action** — confirmed; the economics price (F₀) and the Snell reservation value both formalise it
4. **Audit diff kecil boleh dibatal** — confirmed; Reeves 1992 shows even human teams accumulate complexity per fix

**What cross-domain reading *adds*:**
- **Audit the *referent*, not the *name*.** Harnad grounding problem says CoT-fidelity measurement on a name is wrong; measure the referent. (Proposed: add `last_referent_grounded` field to shadow YAML.)
- **Authority gates decay when politically inconvenient.** Roman augury is the warning. arifOS F13 must be the *external* decayer, not a co-resident decayer.
- **Narrative completion is normative, not gap-driven.** The fix is not "produce more uncertainty tokens" but "explicitly enumerate the counter-narrative the community would tell."
- **Scale alone will not fix.** A larger model will commit *earlier*, not later. The constitutional envelope is the only path; do not rely on emergent faithfulness.

---

# Lampiran A: What this EUREKA does not address

This EUREKA does NOT address:
- The 122-shadow-entry audit (separate thread, separate receipts)
- The Caddy edge hardening (already done by another session, receipts in Caddyfile backups)
- The AGI vision thesis (handled separately in 5-tenses audit)
- The Reality Engineering / AREP plan (deferred, see 06-deferred-questions.md)
- The 5 CHRON predictions A/B/C/D/E (registered, calibration-incomplete)

The EUREKA's scope is **bounded**: anchor 3 patterns in 7 literatures. It does what it says.

---

# Receipt (per F11 AUDITABILITY)

| File | Path | sha256 | Bytes |
|---|---|---|---|
| Slice 01 | `/root/AAA/research/2026-10-03-shadow-patterns/cross-domain/01-anthropology-psychology.md` | `2b090b4f…a140` | 81,161 |
| Slice 02 | `/root/AAA/research/2026-10-03-shadow-patterns/cross-domain/02-physics-math-economics.md` | `fb3a226c…63e8` | 84,485 |
| Slice 03 | `/root/AAA/research/2026-10-03-shadow-patterns/cross-domain/03-code-symbol-language.md` | `469c7ef4…5aff` | 108,310 |
| Synthesis (this file) | `/root/AAA/research/2026-10-03-shadow-patterns/cross-domain/04-eureka-cross-domain-synthesis.md` | (this file) | (this file) |
| Base document | `/root/AAA/research/2026-10-03-shadow-patterns/shadow-patterns-in-coding-agents.md` | (base) | 22,700 |

**DITEMPA BUKAN DIBERI ⚒️**
