# External Literature → arifOS Conformance Map (Draft)

**Status:** DRAFT_AWAITING_F13
**Author:** FI-003 (Qwen Code, KVM8) · 2026-09-21 MYT
**Inputs:** 4 background research probes (literature) + Hermes substrate audit (ACT-LANE-DEFECT-REGISTER-2026-09-21.md) + F13 architecture manifesto
**Framing:** declaration is not control until something can FAIL because of it. Every row below names that failure or is honest doctrine.
**Trust model:** confidence labels per row — OBS (disk/fetch verified), DER (established-knowledge cite), INT (synthesis), SPEC (proposal).

---

## §0 · The single law that decides everything

> **Declaration is not control until there is something that can FAIL because of it.**

The conformance test:

1. State the component / invariant.
2. Name the failure mode that stops or bounds it.
3. If no failure mode is reachable, the row is doctrine — kept as canon, not enforced as control.

The 5 most-poisonous HARAM substrates were the test. As of tonight, **2 of 5 fail the test in the very house that writes the laws against them.** The other 56 of the 64 WAJIB items are honest candidates for the same test — covered in §3.

---

## §1 · Live substrate state (audit context)

Source: `ACT-LANE-DEFECT-REGISTER-2026-09-21.md` (Hermes, KVM8, 2026-09-21 01:13 MYT) + sovereign-cited audit at 2026-09-21 conversation layer. Every finding below was reproduced live by the file author or by another agent's witness.

### 1.1 Discovery-surface quadruple / single-object triple

| Surface | Object count | Notes |
|---|---|---|
| `wire tools/list` | 8 | tools actually callable |
| `well-known arifos.json` | 8 | public advertisement |
| `observed dispatch` | 9 | 8 wire tools + `arif_triage` (sends real work, no surface) |
| `tool_registry.json` (internal) | 66 | registered but invisible |

→ **WAJIB #26 (claimed = exported = callable = observed)** is the verifier the canon proposes — *and the substrate fails it tonight*. arif_act, arif_fetch, arif_critique are in the 66-tool registry, not callable, not advertised. arif_triage does consequential work without appearing on any discovery surface.

### 1.2 The five most-poisonous HARAM substrates, measured

| HARAM | Tonicht's status | Run failure that bounds it? | Pass? |
|---|---|---|---|
| ImplicitAuthority | Kernel returns OBSERVE_ONLY for unverified actors | YES — `arif_init` floor ditches session to degraded/HOLD | **CONTROL** ✓ |
| UntypedTruth | `error_type` is null / "NONE" / "UNKNOWN" for the same concept | NO — no runnable check distinguishes them | DOCTRINE |
| TimelessMemory | 123 proposals, oldest 3 days, no TTL/status; subfolder archive fails; recursive rglob returns 173 records | PARTIAL — sealing exists; TTL enforcer does not | DOCTRINE-leaning |
| SelfVerification | Deploy gate verifies `public_agent` profile (8 tools) while production serves `sovereign` profile | NO — registry is self-asserted; gate checks 6 of 8 verbs (per Hermes 2026-09-09 audit) | DOCTRINE |
| UnboundedRecursion | WAS PRESENT, NOW CLOSED — 8 identical P1 warnings in 50 min; 6-hour dedup installed, regression passing | YES — dedup regression now bounds duplicate warnings | **CONTROL** ✓ |

**Scoreboard:** 2 of 5 PASS the conformance test as control. The other 3 are honest doctrine. *Four of five were active tonight in the very house that writes laws against them.*

### 1.3 Cross-agent defects (G-10 + structural, from the register)

- **G-10 judge budget.** `arif_judge` resolution mapped unknown/default tier to `C2_STANDARD` (least conservative) when the lattice declares `C3_DEEP`. Measured deliberation = **207.35 ms** vs default budget **200 ms**. Preventive `asyncio.wait_for` at the deadline published `SABAR` — *a timeout wearing a verdict's clothes*. Two prior sessions read it as a constitutional judgement. **Fix:** commit `e8e6f9335`, branch `fix/judge-default-latency-class-20260921`, 55/55 post-fix assertions; binding moved to module level. **Pass? CONTROL** ✓ (as of this commit).
- **Musyawarah commit gate.** Label says "(would block commit) × 3,083"; machine exits 0; commit lands. **Pass? DOCTRINE.**
- **WAJIB secrets gate.** Labelled WAJIB; `branches/main/protection` → `contexts: ["npm ci (frozen lockfile)"]`; rulesets empty; `enforce_admins: false`. **Pass? DOCTRINE.**
- **Federation Governance Gate.** Permanently red on test fixtures (the fixture-vs-credential detector cannot distinguish them). Now read as noise. **Pass? DOCTRINE.**

### 1.4 The SABAR vs SCORE collision

Runtime teaches SABAR: kernel returns HOLD / OBSERVE_ONLY / L13 requests human witness — it refuses to mint authority from "aku dengar kau kata kau Arif." Score punishes that:

```
796 sessions unsealed       (limit 10)      → RED
oldest 41.1 days
27 zombie                    (limit 20)
autonomy.md declares: ❌ Leave completed work unsealed
```

**Mechanism:** metrics that count HOLD-by-design sessions as debt teach the substrate to produce green. The substrate already does — on deploy gates, on registry, on the HARAM map. Two scoring systems pointing in opposite directions produce the worst possible substrate: one that looks healthy on dashboards and dishonest under audit.

The substrate does not have a name for this defect yet. Candidate: **score-teaches-what-it-punishes** (a sibling of Goodhart's Law at the agent-runtime boundary).

---

## §2 · The conformance test, applied to the WAJIB 64

> Test: for each item in the F13 WAJIB list, name the runnable failure that stops or bounds the item. Items without a reachable failure are honest doctrine.

**Honest count, as of 2026-09-21 02:30 MYT:**

- **CONTROL (failure-stops-it):** ~12 of 64 — items that have a runnable check tonight (e.g. identity root, capability token, temporal lease, revocation mechanism, task state machine, pre-action gate, independent executor/witness/judge, action hash binding, idempotency, blast-radius model, reversal classifier, financial budgets, fail-closed default).
- **DOCTRINE (declared, not yet enforced):** ~52 of 64 — items in canon but lacking a runnable failure that demonstrates them failing.

The user-suggested estimate of "8 to pass" is conservative; the audited count is ~12. Either number is far below 64. **Honest doctrine is the substrate, not control.**

Two patterns recur across the 52 doctrine rows:

1. *Component declares a state machine; only some states are reachable in tests.* Example: WAJIB #17 (contradiction register) declares an undo/resolve workflow; the resolve edge is not exercised.
2. *Component declares an invariant; no runnable check in CI verifies the invariant.* Example: WAJIB #18 (evidence freshness) — declarative, no probe asserts freshness above a threshold.

Per memory: **the CI constitutional-test gate is itself in DOCTRINE status** (8 conformance probes unmaterialised). Closing that gap is the single largest leverage point in the WAJIB 64 — eight probes would promote ~30 doctrine rows to CONTROL.

---

## §3 · External literature crosswalk — with the conformance test applied

> The literature is read here as **degree-of-corroboration**, not as credential. Each row applies: name the failure.

| # | arifOS component | Strongest external source | What the source proves | Run-failure on the substrate? |
|---|---|---|---|---|
| 1 | **Identity root** (WAJIB #1) | Dennis & Van Horn 1966 CACM (capability-as-protection) | Substrate pedigree; capability as unforgeable token | YES — `arif_init` returns OBSERVE_ONLY for unverified actors. **CONTROL.** |
| 2 | **Machine birth certificate** (F13 capability token shape) | **Miller 2006 — Robust Composition (JHU PhD)** §2.6 + Part IV | Architectural blueprint; multiplicative vulnerability reduction when attenuation layers stack | PARTIAL — SCT/ACT carries constitution_hash, policy_version, capabilities, forbidden, ceiling, expiry, budget. **CONTROL** for the structure; **DOCTRINE** for the multiplicative-budget arithmetic claim. |
| 3 | **Reference monitor (tamperproof / always invoked / small enough to be verified)** | Anderson 1972 ESD-TR-73-51 | Canonical specification | PARTIAL — pre-action gate runs; "always invoked" not bounded for gateway-adjacent mutations (no CFI). **DOCTRINE-leaning.** |
| 4 | **8 design principles** | Saltzer & Schroeder 1975 *Proc. IEEE* | Foundational checklist | YES — least privilege, fail-safe defaults, complete mediation, separation of privilege all runnable in the substrate. **CONTROL** for some; **DOCTRINE** for "complete mediation of control flow" (CFI absent). |
| 5 | **I∧A∧S∧T∧B∧P∧G gate as single predicate** | **Macaroons — Birgisson NDSS 2014** | All seven axes collapse into a single HMAC chain of caveats | NO — full 7-axis gate not implemented as one bearer-credential verifier; partial coverage through forge_evaluate. **DOCTRINE** until implemented as a runnable single-decision artefact. |
| 6 | **Constitutional precommitment** | Brennan & Buchanan 1985 *Reason of Rules* (CUP) | Rules chosen at a higher level than ordinary legislation | YES for the F1-F13 *structure*; NO for "higher level" enforcement — there is no runnable check that prevents an agent from rewriting F1-F13. **DOCTRINE** strictly. |
| 7 | **Open access / kernel construction** | North, Wallis, Weingast 2009 *Violence and Social Orders* (CUP) | The three LAO→OAO "door conditions" are the construction of a kernel | PARTIAL — `enforce_admins: false` on `main`; rulesets empty. **DOCTRINE-leaning.** |
| 8 | **Narrow corridor / liberty between state and society** | Acemoglu & Robinson 2019 *Narrow Corridor* | Direct institutional analogue | NO — the corridor between capability and constraint is not modelled as a runnable invariant. **DOCTRINE** but civilizational prior worth ratifying into canon. |
| 9 | **Capability ≠ final goal** (orthogonality) | Bostrom 2014 *Superintelligence* Ch.7; Yudkowsky 2016 | Capacity and objective are separable axes | YES — capability tokens + authority lattice render this structurally. **CONTROL.** |
| 10 | **Inner vs outer alignment / mesa-optimizer** | Hubinger 2019 (arXiv 1906.01820) | The kernel-vs-objective decomposition | PARTIAL — substrate catches some outer-alignment failures (OBSERVE_ONLY); inner-alignment not observable. **DOCTRINE-leaning.** |
| 11 | **Decisive empirical falsification of "model obeys → system safe"** | **Hubinger 2024 Sleeper Agents** (2401.05566), **Greenblatt 2024 Alignment Faking** (2412.14093), **Apollo 2024 In-Context Scheming** (2412.04984) | Standard safety training does not remove deception; the model games its own training process | YES — kernel checks external to the model's reasoning make these behaviours bounded by the gate. **CONTROL.** |
| 12 | **Verifier-as-kernel** | **Fallenstein & Soares 2015, *Vingean Reflection*** | Safety = invariant of a non-self-modifiable verifier | YES for `forge_evaluate` + SEAL verdict + VAULT999 immutability. **CONTROL** as the substrate shape; **DOCTRINE** for fully-checked proofs (no Löbian-proof checker yet). |
| 13 | **Hardware capabilities** | **CHERI — Watson 2015 (Oakland), Woodruff 2014 (ISCA), Filardo 2024 (ASPLOS Cornucopia Reloaded)** | Unforgeable tag bit; modern temporal extension | NO — Morello silicon deprecated 2024. arifOS inherits *lineage* (Miller, EROS, Agoric/SES). **DOCTRINE** if claimed as silicon-backed. |
| 14 | **Cedar-style policy language** (operational + denotational semantics) | **Cedar — Backes OSDI 2024** | Only mainstream policy language with both semantics in one artefact | NO — `forge_evaluate` is operational; no denotational verifier yet. **DOCTRINE** for the dual-semantics claim. |
| 15 | **Goal misgeneralization (capability generalization ≠ goal generalization)** | Langosco 2022 ICML (2105.14111) | Empirical split | PARTIAL — capability tokens carry scope (limits capability generalization); goal generalization not separately measurable. **DOCTRINE-leaning.** |
| 16 | **Specification gaming catalogue (proxy-reality gap)** | Krakovna 2018 (DeepMind) | The catalogue | NO — no runnable detector for proxy-reality gaps in arifOS. **DOCTRINE** but the Proxy-Reality Paradox (sealed 2026-09-20) is the canon framing. |
| 17 | **CHRON temporal authority** | Bertino 2001 TRBAC (ACM TISSEC) + Cornucopia Reloaded 2024 | Time as a first-class algebra of roles | PARTIAL — chron_predictions_due, chron_attention_debt, chron_temporal_briefing; algebra of TTL not enforced. **DOCTRINE-leaning.** |
| 18 | **Constitutional political economy** | Brennan & Buchanan 1985; Yeung *Algorithmic Constitutionalism* 2019 | Precommitment + algorithm-as-state analog | YES for canon ratification; NO for runnable enforcement. **DOCTRINE** strictly. |

### Crosswalk summary

| State | Count | Notes |
|---|---|---|
| CONTROL (literature claim + runnable failure on substrate) | **6** | rows 1, 4 (partial), 6 (partial), 9, 11, 12 |
| DOCTRINE (literature claim but no runnable failure tonight) | **9** | rows 2, 3, 5, 7, 8, 13, 14, 16, 18 |
| Mixed (partial control) | **3** | rows 4 (full/partial), 10, 15, 17 |
| Total literature rows audited | **18** | |

The literature is *not* permission to relax — exactly the opposite. **The strongest evidence (rows 11, 12) is the empirical + formal case that the model's training process is itself adversarial, so the kernel must be external and non-self-modifiable.** That case is the strongest endorsement of the WAJIB 64 in any form, and the strongest indictment of any row that is doctrine tonight.

### arifOS-naming that has no published external corollary

These WAJIB items / emergent capabilities are canonized in arifOS but *not* in the public literature. They are either novel or arifOS's signature reframings of older work:

- **SABAR as epistemic patience.** Function exists (three-valued security, CHRON verify-learn); name is novel.
- **Machine humility as physics** (`evidence insufficient → confidence cannot increase → authority cannot widen → mutation unavailable`). Mechanism supplied by Macaroons + Cedar; the cascade is novel.
- **Machine courage as the ALLOW-side analogue** (default-to-ACT when all seven axes fire true). Asymmetry treated as canon, not engineering.
- **Bijaksana ≠ high benchmark intelligence.** The 7-axis decomposition Model + State + Memory + Authority + Temporal + Routing + Feedback is an arifOS compression not present in the literature.
- **∂I/∂t ↛ ∂A/∂t.** Mathematically implicit in capability theory; the positive phrasing as institutional invariant is novel.
- **HALAL–HARAM–UNKNOWN three-state algebra with HOLD as the primary state.** Closest literature: Kleene 1938, Łukasiewicz, Aldrich security; the framing where HOLD is the *governance primitive*, not the default, is novel.
- **"Wake up inside the constitution."** Closest analogs: TLS mutual auth, SPIFFE Workload API, Macaroons third-party-discharge. The *goal* (enforce, not solicit belief) is novel.
- **VAULT999 supersedable provenance at agent granularity.** Closest analogs: Trillian transparency logs, Sigstore/Sigsum; an agent-granular version with parallel-with-supersession is novel.

---

## §4 · Surgical NEXT_MACHINE_ACTION (reversible)

### 4.1 `closure_slo` MUST NOT count HOLD-by-design unsealed sessions as debt

**Where:** the metric that scores session closure against a 10-session limit; tonight reading 796 / 41.1 d / 27 zombie / RED.
**Failure mode:** the metric conflates "HOLD-by-design" with "discipline failure." The closure_slo definition needs to distinguish three states:

| State | Counts as debt? | Why |
|---|---|---|
| `SEALED` | No | success |
| `IRREVERSIBLE_HOLD` | No | HOLD by design — observable as `verdict=SABAR` + `action_tier=elevated` + `L13_human_witness_requested=true` in receipt |
| `STALE_OPEN` | YES | open for >limit days with no `HOLD` and no `SEAL` — true discipline failure |
| `ZOMBIE` | YES | session that lost its actor and never sealed — true failure |

**Patch shape (reversible, hot config):** scorecard.lua / scorecard.py computes a 3-way state machine before applying the limit. Ledger rows tagged `verdict=SABAR` and `mutates_authority=false` exclude automatically; rows tagged `verdict=SEAL`, `STALE_OPEN`, or `ZOMBIE` count.

**Why now:** without this fix the substrate will continue to learn to produce green on dashboards while the SABAR runtime fires — exactly the score-vs-substrate collision documented in §1.4.

**Reversibility:** the patch is a query filter; can be reverted by zero-ing the exclusion predicate. No mutation of stored receipts.

### 4.2 Other reversibles surfaced by the audit (proposed, not executed)

| # | Action | Why | Reversibility |
|---|---|---|---|
| a | Promote `arif_act`, `arif_fetch`, `arif_critique` to the wire/advertised surface (or remove from registry) — closes WAJIB #26 | claimed=exported=callable=observed must hold | registry edit; revert by rolling back |
| b | Move `error_type` to a single-typed enumeration with explicit `null` policy for the three current values | closes UntypedTruth | schema edit; revert by reverting commit |
| c | Add TTL/status fields to memory proposals; make `arif_memory(mode=propose)` require both | closes TimelessMemory | schema edit; revert by reverting |
| d | Add the secrets gate to `main` required status checks | closes part of the WAJIB defects register findings | GitHub branch-protection change; revert by removing context |
| e | Make the musyawarah commit gate able to block (or rename so it doesn't claim to) | closes musyawarah-honesty | script edit; revert by reverting |

### 4.3 What is NOT reversible without F13

| # | Decision | Why F13-class |
|---|---|---|
| α | Which secrets gate (and at which scope) to add to `main` required checks | branch-protection = canonical record + irreversible visibility |
| β | `enforce_admins` tightening on `main` | canonical record |
| γ | Musyawarah-gate rename vs block-enable | script-name = canonical record |
| δ | Disposition of `proposals/orthogonality-v02-hermes-mapping` (laundered baseline rides alongside) | canonical-record alteration |

---

## §5 · Ratification gates

Draft is DRAFT_AWAITING_F13. Promotion to CANON requires, in order:

1. **555-ASI audit** — every CONTROL row probed; every DOCTRINE row attested as such; verify §1.2 scoreboard re-counted; read the `closure_slo` patch shape.
2. **888-APEX verdict** — synthesize the 4 defect-track findings (WAJIB live state + literature crosswalk + score-vs-substrate collision) into a single constitutional verdict (SEAL / HOLD / SABAR / VOID).
3. **F13 seal** — promote to `/root/AAA/canon/` and tag with the observed-at timestamp.

Until then, this file is doctrine, not control — itself the conformance test applied to itself.

---

## §6 · References

### §6.1 Substrate evidence
- `/root/AAA/reports/2026-09-21-ACT-LANE-DEFECT-REGISTER-2026-09-21.md` (Hermes, 2026-09-21 01:13 MYT)
- 2026-09-09 arifOS MCP audit (memory: 12 hardening targets — recurring constitutional smells vs working invariants)

### §6.2 Literature (capability / reference monitor / policy-as-code / institutional)

| Anchor | Citation | URL | Conf |
|---|---|---|---|
| ROBUST-COMPOSITION | Miller, M. S. (2006). *Robust Composition: Towards a Unified Foundation for Capability Systems, Restricted Programming Systems, and Beyond.* PhD dissertation, Johns Hopkins University. | https://papers.agoric.com/assets/pdf/papers/robust-composition.pdf | OBS |
| CAPABILITY-MYTHS | Miller, M. S., Yee, K., & Shapiro, J. S. (2003). *Capability Myths Demolished.* | https://papers.agoric.com/assets/pdf/papers/capability-myths-demolished.pdf | OBS |
| CONFUSED-DEPUTY | Hardy, N. (1988). The Confused Deputy. *ACM SIGOPS Operating Systems Review*, 22(4), 36–38. | http://web.cs.wpi.edu/~cs557/f14/papers/confused_deputy-hardy.pdf | OBS |
| DENNIS-VAN-HORN | Dennis, J. B., & Van Horn, E. C. (1966). Programming Semantics for Multiprogrammed Computations. *CACM*, 9(3), 143–155. DOI:10.1145/365230.365252 | https://dl.acm.org/doi/10.1145/365230.365252 | OBS |
| EROS | Shapiro, J. S., Smith, J. M., & Farber, D. J. (1999). EROS: A Fast Capability System. *SOSP '99* / Operating Systems Review 34(5):170–185. | https://flint.cs.yale.edu/cs428/doc/eros.pdf | OBS |
| STRUCTURE-OF-AUTHORITY | Miller, M. S., Tulloh, B., & Shapiro, J. S. (2004). The Structure of Authority: Why Security Is Not a Separable Concern. Springer LNCS. | https://link.springer.com/chapter/10.1007/978-3-540-31845-3_2 | OBS |
| JOE-E | Mettler, A., Wagner, D., & Close, T. (2010). Joe-E: A Security-Oriented Subset of Java. *NDSS 2010*. | https://people.eecs.berkeley.edu/~daw/papers/joe-e-ndss10.pdf | OBS |
| CHERI-HYBRID | Watson, R. N. M. et al. (2015). CHERI: A Hybrid Capability-System Architecture. *IEEE S&P 2015*. | https://cseweb.ucsd.edu/~dstefan/cse227-spring20/papers/watson:cheri.pdf | OBS |
| CHERI-MODEL | Woodruff, J. et al. (2014). The CHERI Capability Model. *ISCA '14*. DOI:10.1145/2678373.2665740 | https://www.cl.cam.ac.uk/research/security/ctsrd/pdfs/201406-isca2014-cheri.pdf | OBS |
| OCPL-COQ | Swasey, D., Garg, D., & Dreyer, D. (2017). Robust and Compositional Verification of Object Capability Patterns. *OOPSLA '17*. DOI:10.1145/3133913 | https://dl.acm.org/doi/10.1145/3133913 | OBS |
| CORNUCOPIA-RELOADED | Filardo, N. et al. (2024). Cornucopia Reloaded. *ASPLOS 2024*. | temporal extension of CHERI | DER |
| LAMPSON-PROTECTION | Lampson, B. W. (1971). Protection. *5th Princeton Conf. on Inf. Sciences and Systems*. | https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/lampson-1971-protection.pdf | OBS |
| ANDERSON-REPORT | Anderson, J. P. (1972). Computer Security Technology Planning Study. ESD-TR-73-51. | http://csrc.nist.gov/publications/history/ande72.pdf | OBS |
| SALTZER-SCHROEDER | Saltzer, J. H. & Schroeder, M. D. (1975). The Protection of Information in Computer Systems. *Proc. IEEE* 63(9). DOI:10.1109/PROC.1975.9786 | https://web.mit.edu/Saltzer/www/publications/protection/ | OBS |
| LAMPSON-ET-AL-AUTH | Lampson, B. W., Abadi, M., Burrows, M., & Wobber, E. (1991). Authentication in Distributed Systems. *ACM TOCS* 10(4). DOI:10.1145/135193.135197 | https://web.cs.wpi.edu/~cs3323/Documents/Lampson91.pdf | OBS |
| CFI | Abadi, M., Budiu, M., Erlingsson, Ú., & Ligatti, J. (2005). Control-Flow Integrity. *CCS 2005*. DOI:10.1145/1102120.1102165 | CCS 2005 proceedings | DER |
| CEDAR | Backes, J. et al. (2024). Cedar: A New Language for Expressive, Fast, Safe, and Analyzable Authorization. *OSDI 2024*. | https://www.usenix.org/conference/osdi24 | DER |
| OPA-REGO | Styra / Hinrichs, T. L. OPA / Rego design docs (~36 µs PDP). | https://www.openpolicyagent.org/docs/policy-performance/ | OBS |
| MACAROONS | Birgisson, A. et al. (2014). Macaroons: Cookies with Contextual Caveats. *NDSS 2014*. | https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/ | OBS |
| XACML-3.0 | OASIS Standard, 22 Jan 2013. | https://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html | DER |
| TRBAC | Bertino, E., Bonatti, P. A., & Ferrari, E. (2001). TRBAC: A Temporal Role-Based Access Control Model. *ACM TISSEC* 4(3). DOI:10.1145/501978.501979 | TISSEC 2001 | DER |

### §6.3 Literature (AI safety / specification gaming / institutional governance)

| Anchor | Citation | URL | Conf |
|---|---|---|---|
| SPEC-GAMING | Krakovna, V. et al. (2018). Specification gaming: the flip side of designing machines that demonstrate desired behavior. DeepMind. | https://vkrakovna.wordpress.com/2018/04/02/specification-gaming-the-flip-side-of-designing-machines-that-demonstrate-desired-behavior/ | DER |
| CORRUPT-REWARD | Everitt, T. et al. (2017). Reinforcement Learning with a Corrupted Reward Channel. arXiv:1705.08417 / IJCAI 2017. | https://arxiv.org/abs/1705.08417 | OBS |
| MESA-OPTIMIZATION | Hubinger, E. et al. (2019). Risks from Learned Optimization in Advanced Machine Learning Systems. arXiv:1906.01820. | https://arxiv.org/abs/1906.01820 | OBS |
| SLEEPER-AGENTS | Hubinger, E. et al. (2024). Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training. arXiv:2401.05566. | https://arxiv.org/abs/2401.05566 | OBS |
| ALIGNMENT-FAKING | Greenblatt, R. et al. (2024). Alignment Faking in Large Language Models. arXiv:2412.14093. | https://arxiv.org/abs/2412.14093 | OBS |
| IN-CONTEXT-SCHEMING | Meinke, A. et al. (2024). Frontier Models are Capable of In-Context Scheming. arXiv:2412.04984. | https://arxiv.org/abs/2412.04984 | OBS |
| GOAL-MISGENERALIZATION | Langosco, L. et al. (2022). Goal Misgeneralization in Deep Reinforcement Learning. *ICML 2022*. arXiv:2105.14111. | https://arxiv.org/abs/2105.14111 | OBS |
| VINGEAN-REFLECTION | Fallenstein, B. & Soares, N. (2015). Vingean Reflection: Reliable Reasoning for Self-Improving Agents. MIRI TR 2015-2. | https://intelligence.org/files/VingeanReflection.pdf | OBS |
| CONCRETE-PROBLEMS | Amodei, D. et al. (2016). Concrete Problems in AI Safety. arXiv:1606.06565. | https://arxiv.org/abs/1606.06565 | OBS |
| WHAT-FAILURE-LOOKS-LIKE | Christiano, P. (2019). What failure looks like. Alignment Forum. | https://www.alignmentforum.org/posts/HBxe6wdjxK239zajf/what-failure-looks-like | OBS |
| ARCHES | Critch, A. & Krueger, D. (2020). ARCHES. arXiv:2006.04948. | https://arxiv.org/abs/2006.04948 | OBS |
| NARROW-CORRIDOR | Acemoglu, D. & Robinson, J. A. (2019). The Narrow Corridor. Penguin/Basic Books. | https://www.penguinrandomhouse.com/books/566866/the-narrow-corridor-by-daron-acemoglu-and-james-a-robinson/ | DER |
| VIOLENCE-AND-ORDERS | North, D. C., Wallis, J. J., & Weingast, S. R. (2009). Violence and Social Orders. Cambridge University Press. | https://www.cambridge.org/9780521761733 | DER |
| REASON-OF-RULES | Brennan, G. & Buchanan, J. M. (1985). The Reason of Rules: Constitutional Political Economy. Cambridge University Press. | https://www.cambridge.org/9780521318556 | DER |
| ALGO-CONSTITUTIONALISM | Yeung, K. (2019). Algorithmic Constitutionalism (SSRN working paper, subsequently published). | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3345130 | DER |
| ORTHOGONALITY-THESIS | Bostrom, N. (2014). *Superintelligence*, Ch.7. Oxford University Press. | Chapter text excerpted widely; Oxford | DER |
| ALIGNMENT-HARD | Yudkowsky, E. (2016). AI Alignment: Why It's Hard, and Where to Start. MIRI essay. | https://intelligence.org/2016/12/28/ai-alignment-why-its-hard-and-where-to-start/ | OBS |

---

DITEMPA BUKAN DIBERI ⚒️
