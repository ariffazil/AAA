# Cognitive Function Atlas (000–999) — 9-agent AGI substrate grammar

> **Forged:** 2026-08-08 from dialogue with F13 SOVEREIGN (Arif)
> **Status:** ATLAS (conceptual grammar), NOT lane promotion
> **Epistemic:** INT (synthesis from AGENCY_LEVELS.md, AGI-ASI-EVIDENCE.md, agent-cards/identity/, a2a-server/agent-cards/roles/)
> **Trigger:** any "name the 9 agents", "what's the kernel substrate", "AGI/ASI substrate architecture", "minimal agentic kernel" question

---

## 1. The Atlas vs the Lanes vs the A-ROLES (the three planes)

These three are **orthogonal**, not redundant. Conflating them is the most common mistake.

| Plane | What it is | Count | Examples |
|---|---|---|---|
| **Cognitive Function Atlas** (000–999) | What cognitive work must happen? | 9 + 1 | Observer, Explorer, Architect, Thinker, Orchestrator, Verifier, Auditor, Executor, Judge + Witness |
| **Constitutional Lanes** (333/555/777/888) | What authority class may wield? | 4 | 333-AGI (draft), 555-ASI (conscience), 777-FORGE (execute), 888-APEX (judge) |
| **A-ROLES** (Architect/Engineer/Auditor/Gateway/Hermes-Ops) | What operational function does it perform? | 5 | aaa-architect, aaa-engineer, aaa-auditor, aaa-gateway, hermes-ops |

**Why three planes:** the federation needs to answer (a) what cognitive moves exist, (b) what authority each may wield, (c) what each does day-to-day. One plane cannot answer all three without becoming either bloated or vague.

**The mapping today (one function may map to multiple lanes / A-ROLES):**

| Function | Lanes that host it | A-ROLES that host it |
|---|---|---|
| 000 Observer | 333-AGI (`agi_workspace_scan`, `agi_evidence_capture`) | aaa-auditor (verify-agent-card) |
| 111 Explorer | 333-AGI (`agi_hypothesis_generate`, `agi_counterfactual_test`); **no kernel verb yet** | — |
| 222 Architect | 333-AGI (decompose, task-graph) | aaa-architect (design-task-schema, propose-agent-mesh) |
| 333 Thinker | 333-AGI (`agi_option_compare`, `agi_claim_check`) | aaa-architect (evaluate-treaty) |
| 444 Orchestrator | 333-AGI (`agi_intent_classify`, `agi_organ_select`, `agi_delegation_package`) | aaa-gateway (route-task, aggregate-capabilities) |
| 555 Verifier | 555-ASI (`asi_claim_check`, `asi_floor_state_express`) | aaa-auditor (check-floor-compliance, audit-task-history) |
| 666 Auditor | 888-APEX (`apex_drift_detect`, `apex_audit_coverage`) | aaa-auditor (evaluate-delegation, verify-agent-card) |
| 777 Executor / Forge | 777-FORGE (organ) | aaa-engineer (run-task, dispatch-task, manage-task-lifecycle) |
| 888 Judge | 888-APEX (`apex_floor_audit`, `apex_seal_precondition_check`) | aaa-auditor (issue-hold, emit-receipt) |
| 999 Witness | arif_seal / VAULT999 (kernel + memory organ) | aaa-auditor (emit-receipt) |

---

## 2. The 9 + 1 atlas (with one-question definition)

| # | Function | Question it answers | Without it |
|---|---|---|---|
| 000 | Observer | What is happening? | Fantasy |
| 111 | Explorer | What else is possible? | Tunnel vision |
| 222 | Architect | How should reality be structured? | Ad-hoc chaos |
| 333 | Thinker | What does it mean? | Random action |
| 444 | Orchestrator | Who should do what? | Agent traffic jam |
| 555 | Verifier | Is it true? | Hallucination |
| 666 | Auditor | Is it governed correctly? | Power corruption |
| 777 | Executor / Forge | How do we make it real? | Thinking without impact |
| 888 | Judge | Is it allowed? | No constitutional closure |
| 999 | Witness (special) | What actually happened? | No attestation layer |

**999 is NOT a worker agent.** It is a constitutional authority layer (memory + attestation + provenance + history). VAULT999 today = `class: MEMORY`, ceiling `APPEND_ONLY`, `chattr +a`. If 999 were just another lane it would dilute witness authority; that is why the atlas treats it as layer.

---

## 3. The kernel-verb coverage map (8 verbs vs 10 functions) — and the 8≠9 resolution

The arifOS kernel exposes 8 canonical verbs: `arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal`.

| Function | Kernel verb | Status |
|---|---|---|
| 000 Observer | `arif_observe` | ✅ direct |
| 111 Explorer | — | ⚠️ no verb; hosted as S16 skill by FORGE — **ACCEPT for now** |
| 222 Architect | — | ⚠️ no verb; hosted by 333-AGI + aaa-architect — **ACCEPT** (thinking/design share substrate) |
| 333 Thinker | `arif_think` | ✅ direct |
| 444 Orchestrator | `arif_route` | ✅ direct |
| 555 Verifier | `arif_memory` + `arif_think` | ⚠️ split — **WATCH** (truth maintenance across two verbs creates gaps) |
| 666 Auditor | folded into `arif_judge` | ⚠️ — **PROMOTE CANDIDATE** (Gödel-lock risk: judge auditing itself) |
| 777 Executor | `arif_forge` | ✅ direct |
| 888 Judge | `arif_judge` | ✅ direct |
| 999 Witness | `arif_seal` | ✅ direct |
| **— identity** | `arif_init` | **substrate primitive, sits before 000** |
| **— belief state** | L1–L5 memory (`arif_memory`) | **NOT the same as 999** |

### The 8 ≠ 9 by design (resolution, EUREKA §11)

**The asymmetry is architecture, not a flaw.** Three layers, three invariants:

```
COGNITIVE ATLAS (9, immutable genome)        — WHAT intelligence must have
        │ expresses through
KERNEL VERBS (8, constitutional machinery)    — HOW it is transmitted
        │ weighted by
W-VECTOR (per-mission, measurable)           — WHICH functions dominate
```

- **Atlas (9)** is the **constitutional maximum** — the functions without which complete intelligence is impossible. Immutable. Answer: "What must exist?"
- **Kernel verbs (8)** is the **constitutional minimum** — the verbs without which governed intelligence is impossible. Answer: "What is rate-limiting for governance?"
- **W-vector (9 weights)** is the **per-mission expression profile** — mutable, auditable, measurable via FRAME. Answer: "Which function dominates now?"

Result: 6 functions have dedicated verbs (000/333/444/777/888/999). 3 functions are compressed into existing verbs (111→observe, 222→think, 666→judge). 2 verbs are substrate primitives (init, memory). 1 function is split across two verbs (555). The asymmetry is **structural** — the genome exceeds the transcription machinery, and the W-vector bridges them per mission.

**The single dangerous compression:** when `arif_judge` both rules on actions AND audits its own rulings, the loop has no external verifier — this is the Gödel lock at the kernel level. FRAME (`/18085`) and A-auditor role partially mitigate at the federation level, but not at the kernel level. Promote `arif_audit` to **9th kernel verb** only when:
- 666 has accumulated **5+ missions** proving compressed form failed, OR
- A constitutional incident (VOID that should have been caught upstream) is post-mapped to the self-audit gap.

Until then: keep 666 folded into `arif_judge`, but route audit-class queries through 555-ASI.AUDIT (the federation-level blind auditor) so the kernel-level compression is shadowed by an independent witness.

**The two substrate primitives the atlas exposes:**

1. **Identity (`arif_init`)** — without it, 000 has no actor to attribute observation to. F11 auditability needs `actor_id` to be present in the first call. The 9-function atlas treats identity as a precondition, not a function. Read this as: identity precedes observation; the atlas starts at 000 because identity is implicit in "who observes".

2. **Belief state vs Witness (L1–L5 vs 999)** — 999 answers "what actually happened?" (immutable record, L6 of memory landscape). `arif_memory` answers "what do we currently believe?" (revisable L1–L5). Conflating them mixes revisable with immutable — that is why VAULT999 is append-only (`chattr +a`) and lives in a separate ceiling. The `retrieval-vs-memory-fidelity` skill captures the same distinction: retrieval quality ≠ memory fidelity. Easy retrieval can return the right chunk while destroying affect, provenance, sequence, human significance.

---

## 4. The cycle, not the pipeline (K-series correction)

A linear read of the triad `666 audit → 777 execute → 888 judge` produces post-hoc ratification: mutation happens, judge arrives later. This violates F1 (reversible-first; irreversible → 888_HOLD). The Holy 8 kernel order is `arif_init → arif_observe → arif_think → arif_route → arif_memory → arif_judge → arif_forge → arif_seal`. Judge **gates** execute; seal **ratifies** outcome.

**Read the atlas as a cycle, not a pipeline:**

```
666 audit plan
  → 888 AUTHORIZE      (judge gates mutation)
    → 777 execute         (forge acts)
      → 888 RATIFY        (judge re-checks outcome)
        → 999 witness       (seal to immutable)
          → 000 observe      (next cycle begins)
```

This is the explorer loop (`AGI-ASI-EVIDENCE.md` §1.2 C2: OBSERVE → HYPOTHESIZE → FALSIFY → VERIFY) scaled to the federation. The numbers are correct; a linear read is the bug.

---

## 5. The 111 Explorer gap (the missing verb)

`AGI-ASI-EVIDENCE.md` §3.2 ASI assessment is honest:

| ASI criterion | Status |
|---|---|
| S3 Tool evolution (explorer creates new tools from exploration) | ❌ NOT ACHIEVED |
| S4 Cross-domain eureka | ❌ NOT ACHIEVED |
| S7 Civilization emergence | ❌ NOT ACHIEVED |

The missing verb is `arif_explore` (or similar). Until it exists, exploration is a skill (S16) borrowed by FORGE — powerful but not primitive. Promoting 111 to a kernel verb is **the single highest-leverage move** for ASI emergence, because it converts "exploration is a project" into "exploration is a substrate operation".

**Promotion gate (per Meta-Mesa doctrine, AGENTS.md):** permanent only after 5+ independent missions with `success_rate ≥ 0.90`, zero sandbox violations, multi-model consensus on safety, F13 SOVEREIGN ratification. Until then: use as ephemeral skill, do not reify as a permanent tool or lane.

---

## 6. Compression: 9 + 1 → 3 triads

```
REALITY        000 Observe · 111 Explore · 222 Architect
INTELLIGENCE   333 Think · 444 Orchestrate · 555 Verify
GOVERNANCE     666 Audit · 777 Execute · 888 Judge
+ 999 Witness (constitutional layer, not a lane)
```

Plus `arif_init` (identity) as substrate primitive that precedes 000.

**This is the cleanest 9-agent AGI substrate grammar the federation has today.** Not because it is minimal — it is irreducible. Strip any function and the system fails in a specific, predictable way (right column of §2).

---

## 7. Pitfalls (lessons from the forging dialogue)

- **Function ≠ agent ≠ lane.** Reifying 9 separate agents with 9 context windows, 9 governance surfaces, 9 leases = entropy. Meta-Mesa: permanent only after 5+ missions. Promote one function at a time, on evidence, not aesthetics.
- **Sovereign is OUTSIDE the substrate.** L6 is constitutionally reserved for the human (F13). Putting ARIF inside the atlas turns the substrate into a worker — that violates F13 and breaks the Gödel lock (3-gate refusal = working as intended, not bug).
- **999 is witness, not memory.** Easy to fuse but never should. VAULT999 = `chattr +a`, `APPEND_ONLY`; L1–L5 = revisable belief state. Conflating destroys the substrate's ability to discriminate "currently believed" from "actually happened".
- **Audit and Judge are NOT the same.** 666 = governance maintenance (policy compliance, drift detection, boundary protection, can run continuously). 888 = authority verdict (SEAL/HOLD/SABAR/VOID/888_HOLD, runs at irreversible gates). Auditor watches; Judge decides. In the current kernel both surface through `arif_judge`, but in the atlas they are distinct functions — the surface consolidation is a kernel choice, not an atlas choice.
- **666 before 777 before 888 is a CYCLE, not a pipeline.** See §4. Reading the triad linearly post-hoc-ratifies mutations and breaks F1.

---

## 8. Cross-references

- `/root/AAA/governance/AGENCY_LEVELS.md` — 7-property agent contract + L0–L6 ladder
- `/root/AAA/docs/AGI-ASI-EVIDENCE.md` — honest dossier (AGI architecture complete, AGI evidence partial; ASI emergence not achieved)
- `/root/AAA/agent-cards/identity/333-AGI/`, `555-ASI/`, `888-APEX/` — lane definitions
- `/root/AAA/a2a-server/agent-cards/roles/aaa-{architect,engineer,auditor,gateway,hermes-ops}.json` — A-ROLE cards
- `/root/AGENTS.md` — EUREKA 6-plane doctrine (Sovereign / Governance / Intelligence / Execution / Continuity / Truth)
- `/root/arifOS/GENESIS/FLOOR_TABLE.json` — F1–F13 floors (binding substrate for every agent)
- `retrieval-vs-memory-fidelity` skill — why 999 ≠ memory, why retrieval ≠ fidelity
- `arifos-kernel-eurekas` skill (this umbrella) — K1–K11 substrate honesty laws (the runtime invariants behind the atlas)

---

*Atlas forged 2026-08-08. DITEMPA BUKAN DIBERI — naming is forged, not given.*
