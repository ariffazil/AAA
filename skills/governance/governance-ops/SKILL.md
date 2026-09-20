---
name: governance-ops
id: governance-ops
version: 2.0.0
owner: AAA
risk_tier: high
floor_scope: ['F1', 'F2', 'F4', 'F9', 'F11', 'F13']
autonomy_tier: T1
merged_from:
  - aaa-doctrine-sealing
  - constitutional-floors
  - forge-execution-governance
  - forge-governance-analysis
  - forge-governance-jsonld
  - governance-audit
  - governance-benchmark-authoring
merged_at: 2026-09-20T14:35:00Z
canonical_path: /root/AAA/skills/governance/governance-ops/SKILL.md
archive: /root/AAA/skills/.archive/merge-20260920/governance/
triggers:
  - "F13 says seal or code this into canon"
  - "constitutional floors"
  - "F1-F13"
  - "what is F9"
  - "F13 sovereign"
  - "anti-hantu"
  - "gödel lock"
  - "godel lock"
  - "external witness"
  - "principal doctrine"
  - "irreducible human"
  - "000 init"
  - "999 vault"
  - "seven organs"
  - "organ topology"
  - "arifos mythos"
  - "founding scar"
  - "constitutional ecosystem"
  - "constitutional filesystem map"
  - "where is the constitution"
  - "ditempa bukan diberi"
  - "forged not given"
  - "arifos canons"
  - "principal-agent boundary"
  - "things never automated"
  - "invariant P1"
  - "sovereignty model"
  - "F13 veto"
  - "floor enforcement"
  - "constitutional gate"
  - "is this governed"
  - "alive but not governed"
  - "verify governance surface"
  - "is this control actually wired"
  - "bypass test"
  - "false green"
  - "tool registration check"
  - "immutable file"
  - "monotonicity"
  - "rollback scope"
  - "corporate governance analysis"
  - "Governance JSON-LD — constitutional ontology and semantic"
  - "is this actually enforced"
  - "is this control real"
  - "does this gate work"
  - "verify this safeguard"
  - "the control is present"
  - "privacy filter is on"
  - "0 rejections"
  - "gate passed"
  - "is this wired up"
  - "verify a claimed control"
  - "false name"
  - "named but not installed"
  - "hardcoded metric"
  - "is this gate real"
  - "does the gate actually block"
  - "can this bypass the gate"
  - "enforcement coverage"
  - "is the guard load-bearing"
  - "who actually made this change"
  - "audit trail attribution"
  - "prevented vs detected"
  - "a service claims a control you must verify"
  - "verifying a claimed result or sealing a control"
  - "auditing an auth/gate control for verification"
  - "governance benchmark"
  - "BBB probe"
  - "actor physics benchmark"
  - "push to huggingface"
  - "HuggingFace dataset"
  - "conflict resolution specification"
  - "judiciary layer"
  - "seal all"
  - "seal it"
  - "make it live"
  - "code this into the kernel and state and agents"
  - "seal this into canon"
  - "governance jsonld"
  - "governance ontology"
  - ".well-known/governance.jsonld"
  - "board composition analysis"
  - "who was removed from the board"
  - "is this service governed"
  - "control is a label"
  - "false assurance"
description: "Use when asking whether a control is real. Route a governance question to the one reference that answers it — control enforcement, service governance, the F1–F13 constitution, canon sealing, JSON-LD ontology, governance benchmarks, or an institution's board."
---

# governance-ops — one entry point for every governance question

> **Merged 2026-09-20** (SKILL MERGE PROTOCOL, F13 mandate) from 7 skills: `aaa-doctrine-sealing`,
> `constitutional-floors`, `forge-execution-governance`, `forge-governance-analysis`,
> `forge-governance-jsonld`, `governance-audit`, `governance-benchmark-authoring`.
> Member bodies are preserved **byte-for-byte** in `references/<member>.md` under a 4-line provenance
> header (hashes in the receipt). Originals are archived, never deleted, at
> `/root/AAA/skills/.archive/merge-20260920/governance/`.
>
> **This file holds ROUTING and the deduplicated hard rules. The references hold the procedures.**
> Do not work from this file alone — open the reference the FLOW lands you on.

---

## FLOW

The word *governance* covers **two different objects** in this cluster. Fix the referent in step 0
before choosing anything else, or you will run a canonical-floors lookup against a company's board page.

```
governance question
│
├─ STEP 0 · Is the SUBJECT an external institution?
│    observable: a named company · a board/leadership page · an IR or annual-report PDF ·
│                a director name · a stake sale / merger / regulator condition · an AGM
│    YES ─▶ B. INSTITUTIONAL GOVERNANCE ....... references/forge-governance-analysis.md
│
└─ NO — the subject is OUR OWN system (canon, kernel, organs, controls, benchmarks)
     │
     ├─ 1 · Definition / map question?
     │     observable: "F1–F13", a floor name, "what is F9", where-is-the-constitution,
     │                 godel lock, external witness, principal doctrine, 000/999, seven organs
     │     ─▶ references/constitutional-floors.md        → the floor definition, verbatim
     │
     ├─ 2 · Machine-readable ontology artifact?
     │     observable: `/.well-known/governance.jsonld`, @context, ontology term, DID agent
     │     ─▶ references/forge-governance-jsonld.md      → ontology shape + refusal surface
     │
     ├─ 3 · Is a CONTROL real, or is it a label?
     │     observable: a named gate / validator / filter / sandbox / seal / drift detector, and a
     │                 claim of the form "is it enforced / wired / load-bearing", "0 rejections",
     │                 "privacy filter is on", "gate passed"
     │     ─▶ references/governance-audit.md             → control state + the three proofs
     │
     ├─ 4 · Is a RUNNING SERVICE governed?
     │     observable: `/health` answers 200 or `tools/list` returns tools, and the question is
     │                 whether its ACTIONS pass the control plane (receipts, revocation, join key)
     │     ─▶ references/forge-execution-governance.md   → alive≠governed, wiring rung, receipts
     │
     ├─ 5 · Must a finding become BINDING?
     │     observable: F13 says *seal it* / *seal all* / *code this into canon* / *make it live*;
     │                 a session produced a doctrine-shaped rule that must outlive the session
     │     ─▶ references/aaa-doctrine-sealing.md         → surface edits + status gate + push
     │
     └─ 6 · Authoring or publishing a GOVERNANCE BENCHMARK?
           observable: probes, dimensions, "BBB vN", HuggingFace dataset push, CCC v2,
                       "conflict resolution specification"
           ─▶ references/governance-benchmark-authoring.md → probe schema + HF push pattern
```

### Routing table — situation / observable → reference → what it produces

| # | Situation (the observable that selects it) | Reference | What it produces |
|---|---|---|---|
| B | A **company, board, or control chain** is the subject; the data is a public page, IR deck, or filing | `references/forge-governance-analysis.md` | Board roster + **who was removed** (Wayback digest diff), vote math, ownership/control chain, one stated failure condition. Guardrail: no rating or investment recommendation |
| 1 | A **floor, the constitution, or the architecture** is the subject — F1–F13, 000/999, Gödel lock, principal doctrine, organ topology, mythos | `references/constitutional-floors.md` | The **verbatim** floor definition, its trauma lesson/axis/mechanism, the constitutional filesystem map. Read-only: floor text is constitutional surface |
| 2 | The **`/.well-known/governance.jsonld` artifact** is the subject, or an external agent needs the ontology | `references/forge-governance-jsonld.md` | Floor/organ/action-class/epistemic-label terms as linked data, plus the refusal surface (`@id` determinism, append-only terms, no runtime state) |
| 3 | A **control** is claimed to be in force (gate, validator, health check, sandbox, seal, drift detector, shadow mode, authority check, privacy filter, promotion ladder) | `references/governance-audit.md` | One of 12 named control states (DECLARED…FALSE_NAME) with the CALLER / EFFECT / BYPASS proofs; the 7-mode router picks the mode; `coverage = gated/writable` |
| 4 | A **service** is up and the question is whether it is *governed* — listing vs calling, structural zeros, receipts freshness, causal closure | `references/forge-execution-governance.md` | The wiring rung (DECLARED / REACHABLE / FUNCTIONAL / EFFECTIVE), the bypass-path enumeration, the ordered-defect verdict |
| 5 | A finding must **become law** — the directive is *seal / code it in / make it live* | `references/aaa-doctrine-sealing.md` | Surface edits in order (fragment → floors → base.md → AGENTS.md → eureka **live feed** → skill → kernel amendment proposal → render → commit → push), the correction log, the honest report shape |
| 6 | A **governance benchmark** is being authored or pushed | `references/governance-benchmark-authoring.md` | Bilingual JSONL probes (40/dimension), severity map, dataset card, HuggingFace commit pattern; CCC v2 is a specification, not a model benchmark |

### Order of operation when more than one row applies

1. **Step 0 first.** Fix the referent (own-system vs institution). Everything downstream inherits it.
2. **Derive before you quote.** Any number, rate, score or witness count → `references/governance-audit.md`
   §8 / `references/metric-derivation-discipline.md` **before** it enters a sentence. This is a
   precondition, not a follow-up.
3. **Run control modes in causal order:** name → caller → effect → bypass → coverage → seal. A coverage
   number computed on an unnamed or uncalled control is decoration.
4. **Verify a claimed result before accepting it** — including your own — `references/governance-audit.md`
   §6. Reports of completed work are claims of the same kind as any other finding.
5. **Seal last.** Row 5 is entered *after* rows 3/4 have proven the claim; sealing on unverified
   evidence writes a false claim into canon, where it binds every later session.
6. **An audit never becomes the mutation.** Row 3/4 findings on a protected path are **report-and-hold**;
   the repair is a separate, scoped mutation under its own authority.

**Worked landings (the one-sentence test):**

| Asked | Lands on |
|---|---|
| "is this control actually enforcing?" | `references/governance-audit.md` → MODE-CONTROL-INTEGRITY, then MODE-ENFORCEMENT-COVERAGE if the question is reach |
| "is this thing actually wired up?" | `references/governance-audit.md` → MODE-NAMED-MECHANISM; if it is a *running service*, `references/forge-execution-governance.md` §7 |
| "how does a doctrine get sealed?" | `references/aaa-doctrine-sealing.md` (surfaces + order of operations + status gate) |
| "alive but not governed" | `references/forge-execution-governance.md` §1/§7 |
| "what is F9 / who can veto?" | `references/constitutional-floors.md` §1 (verbatim floor text) |
| "the page says 7 directors, three women" | `references/forge-governance-analysis.md` (Step 1 temporal anchoring — pull the Wayback diff before writing a word) |
| "push the benchmark to HuggingFace" | `references/governance-benchmark-authoring.md` |
| "generate governance.jsonld for the subdomain" | `references/forge-governance-jsonld.md` |

---

## CORE RULES

Deduplicated hard rules that hold on **every** branch. Source reference in brackets.

**R1 · NAME_REQUIRES_MECHANISM.** Any surface whose name asserts gate / health / sandbox / verify /
seal / drift / secure / shadow / authority / wall must exhibit a runtime mechanism, or it is a **false
name** and the honest label is a different one. An agent trusts a name faster than it reads a
mechanism; a guarantee-shaped artifact that enforces nothing is **worse than no control at all** —
absence is visible, a false control is believed and built upon. [governance-audit §1.1]

```
SEMANTIC AUTHORITY = NAME ∩ CALL_PATH ∩ MEASURED_EFFECT ∩ BYPASS_RESISTANCE ∩ EVIDENCE
EFFECTIVE_CONTROL  = CALLER ∧ EFFECT ∧ BYPASS          (any empty term → AUTHORITY_CLAIM = VOID)
```

**R2 · Three proofs, all three, in every control question.** CALLER_PROOF (who actually invokes it —
name the call site `path:line`, sweeping every scheduler surface), EFFECT_PROOF (a failing input changes
the outcome or blocks the action), BYPASS_PROOF (enumerate alternate paths — raw shell, editor save,
direct DB/write, SCM boundary). Report **which** are proven; any proof you cannot produce is a **FAIL,
not a maybe**. [governance-audit §1.2]

**R3 · Ask the causal question, never the existence question.** Replace "is there a gate?" with "can an
action reach the protected state **without** passing through it?"; "is there a health check?" with "if a
dependency dies, does the output **change**?"; "is it sealed?" with "does the seal still **resolve**
against the bytes on disk?" [governance-audit §1.3]

**R4 · Evidence hierarchy — the dispute resolver.**
`RAW OBSERVATION > MEASURED FACT > DERIVED STATE > REASON CODE > NARRATIVE LABEL`. When two elements of
one payload disagree, the higher tier wins. `value or "SOME_CAUSE"` is a measurement-shaped hole, not a
diagnosis. [governance-audit §1.4]

**R5 · Report transitions, not booleans.**
`PRODUCED != SCHEDULED != FIRED != DELIVERED != OBSERVED != ACKNOWLEDGED`. "Ran", "sent", "done",
"sealed" are transition lies. Name the chain position and which links are unproven.
[governance-audit §1.5]

**R6 · UNBUILT and DORMANT must never be reported as PASS.** A rule that holds only because nothing
exists to violate it is a **vacancy, not a control** — and vacancies fail simultaneously on the day the
governed thing is finally built. [governance-audit §1.5, §6]

**R7 · A structural zero is not a measurement.** Before reporting zero / empty / `NO_CHANGE` from any
governed surface, prove the instrument **can** return non-zero (positive control). If it cannot, report
**UNMEASURABLE**, not zero. An instrument that says "all clear" while incapable of saying anything else
is consumed as evidence and every inference built on it inherits the false negative.
[forge-execution-governance §1a; governance-audit §5 step 2c]

**R8 · alive ≠ governed; listing ≠ calling.** Health-200 is liveness. Governance is whether the
service's actions pass the constitutional control plane (judge, lease, receipt, revocation). A tool can
be registered, listed, and still rejected at call time by a *separate* transport gate — green the whole
way. [forge-execution-governance §1, §1a]

**R9 · Attribute the four wiring rungs by name.** A control is **DECLARED** (a grep hit) /
**REACHABLE** (the harness could invoke it) / **FUNCTIONAL** (invoked once, correct shape) /
**EFFECTIVE** (invoked by the workflow it exists for, output consumed). DECLARED or REACHABLE reported
as "we have X" is the normal failure. Control liveness is proven by exactly one of: a receipt whose
timestamp falls **inside the activity window**, or a **blocked violation** in the gate's own deny class.
[forge-execution-governance §7]

**R10 · Coverage is a property of the boundary, not of the gate.**
`EnforcementCoverage = paths that intersect a gate / paths that can write protected state`. A gate that
blocks 100% of what reaches it while covering 1 of N write paths has prevention → 1.0 **and** escape →
1.0 at once, because a bypassing attempt is never in the denominator. Report coverage and prevention
together, or neither. [governance-audit §5; forge-execution-governance §1b]

**R11 · A bypassable gate is a finding about the gate, not a licence to take the open path.** The
rationalisation arrives pre-shaped and persuasive (*it is decorative, therefore I may route around it*).
That sentence is the exact defect this cluster exists to catch. Correct output:
`coverage < 1, uncovered = <path>, action = HOLD`. Testing the hole "to prove the finding" converts the
auditor into the incident. [governance-audit §1.6, §5 step 2b]

**R12 · An audit reports; it does not grant authority.** Never author the envelope that constrains you —
if the authority governing a mutation would be written by the act that needs it, that is a self-grant →
HOLD. `CanMutate = AuthorityGranted ∧ ScopeMatches ∧ TargetPermitted ∧ BoundaryActive`; confidence is
deliberately absent from that conjunction. `UNKNOWN→RESOLVED` is epistemic; `RESOLVED→MUTATED` is
authority. Also: **do not fix under a race** — check for a concurrent writer
(`find <dir> -newermt "-6 minutes" -type f`) before patching, and **re-run the probe after any fix**.
[governance-audit §1.6, §5 step 6]

**R13 · Absence of authority record ≠ absence of permission.** A mutation can carry a flawless evidence
chain and no permission record; the correct verdict is "no authority record present", not
"unauthorized". Conversely, a writer log keyed on a *configured name* records a label, not an identity —
a shared VCS `user.name` is non-identifying; the correct source is session id + host + objective captured
at the write boundary. [forge-execution-governance §6; governance-audit §5 step 5]

**R14 · Verify the machine before the narrative.** `hostname; cat /etc/hostname; tailscale status` run
FIRST, before any topology, bottleneck or capability conclusion. A persona header, SOUL/AGENTS stamp or
context block is a **claim** and drifts silently after migrations. When a header contradicts the host,
retract the header explicitly in the report. [forge-execution-governance §9]

**R15 · Publish your own retractions, in the same artifact, replacing — never hedging.** A report
carrying only findings against others is half an audit. A corrected claim must give the new state; a
downgraded confidence that leaves the old claim standing is not a retraction.
[governance-audit §4]

**R16 · Ordering beats effort: verification that runs after the irreversible step is decoration.**
`[3/n] RENDER + PUBLISH → [4/n] run integrity gates` gives a gate fresh receipts, a genuine `[FAIL]`,
and zero influence — observed over 19 consecutive runs. Two independent defects produce that signature:
**ordering** (move verification before the act) and **swallowed status** (`|| echo "[ALARM] …"`, `2>&1`,
`set +e` — let a failed gate stop the run). Report the ordering defect as the root cause.
[forge-execution-governance §7]

**R17 · Do not wire an incomplete control just because it exists.** A false boundary is worse than an
absent one: an absent boundary invites scrutiny, a false one ends it. The correct state for an unfinished
control is a header reading **NOT WIRED** plus its measured bypass list, and a suite that exits non-zero.
An env var is a **convention, not a credential**. [forge-execution-governance §1d]

**R18 · Canon Lock — the only legal mutation path into protected trees.** `/root/AAA/governance`,
`/root/AAA/canon` and `/root/arifOS/GENESIS` are `chattr +i` locked. Every write goes through:

```bash
ARIFOS_TRACE_ID=trc-<your-trace> /root/scripts/canon-mutate run <tree> -- <command...>
```

Direct writes fail with EPERM — **that failure is the lock working, not a bug.** The cycle
(unlock → mutate → relock → receipt) is crash-safe and receipted with verified relock to
`/var/lib/arifos/canon_mutations.jsonl`. Always set `ARIFOS_TRACE_ID`. **Never clear the immutable
attribute by hand** — an unlock outside the cycle is an unauthorized bypass. Protocol:
`/root/AAA/instructions/CANON-LOCK-PROTOCOL.md`. [aaa-doctrine-sealing; forge-governance-jsonld]

**R19 · Two eureka ledgers exist by design; only ONE is writable.**
Append new rows to the **LIVE FEED** `/root/AAA/eurekas/eureka-entries.jsonl`.
`/root/AAA/canon/eureka-entries.jsonl` is the **FROZEN RATIFIED REGISTRY** — `chattr +i`, immutable,
an append returns EPERM even as root unless the attribute is first cleared, **which is forbidden**.
Cite it as historical authority; never use it as a write target, never unlock it. Appending to the wrong
one silently loses the record. Keep the count honest: `wc -l` before and after, then re-parse.
**Never port entries between the two ledgers.** [aaa-doctrine-sealing M4]

**R20 · Floor surface is constitutional surface.** `FLOOR_TABLE.json` holds 13 floors — **never edit it
directly**. Floor changes are proposed as a numbered `## Amendment N:` in
`/root/arifOS/GENESIS/FLOOR_TABLE_AMENDMENTS.md` and close with *awaiting F13 SOVEREIGN ratification*.
An amendment is a proposal; reporting it as live is a false receipt. No floor may sit above reality:
if reality contradicts a floor, reality wins (Gödel Lock Level 2). [aaa-doctrine-sealing M9/M10;
constitutional-floors]

**R21 · Sealing means the rule lands on disk in every layer that reads it.** Doctrinal prose binds
nothing. A finding only constrains a model once it reaches `base.md` (rendered inline every turn) or a
kernel floor. **The eureka packet is NOT the deliverable — the surface edits are.** Report doctrine-layer
work as doctrine-layer; never call it sealed if no gate can say NO to it yet. [aaa-doctrine-sealing]

**R22 · Commit gates are real.** Every new `.md` under `instructions/` must carry a compliant `Status:`
line or the whole commit is blocked by the DOCTRINE-STATUS GATE; a ratified-class value needs an F13
instrument (a date or a verbatim quote); ANNEX-class values are blocked outright. Fix the label and
re-commit — never `--no-verify` past it. Stage **explicit paths**, never `git add -A` (both repos carry
sibling sessions' in-flight edits). [aaa-doctrine-sealing M6]

**R23 · F13 veto is absolute and non-delegable.** *"No algorithm overrides the human. No system can
predict consent. No model may convert predicted consent into actual consent. The sovereign may veto
without justification. Silence is NOT authorization."* Human consent cannot be inferred from patterns;
human dignity outranks task completion; human contradiction triggers SABAR, not correction.
[constitutional-floors §1 F13, §2 P1–P10 — quoted verbatim]

**R24 · F9 ANTI-HANTU / F10 ONTOLOGY are not optional.** *"Agent CANNOT say: 'I understand your
suffering,' 'I care about you,' 'I will heal you.' Agent CAN: recognize signatures, respect boundaries,
defer judgment, refuse harmful commands."* Geometric witnessing ("your coordinates are…"), never "I feel
you". [constitutional-floors §1 F9/F10, §12 pitfall 1 — quoted verbatim]

**R25 · The Gödel Lock is a feature, not a limitation.** *"No formal system can adjudicate itself. The
witness must come from outside."* SEAL-bound claims without external witness get Φ_effective = Φ × 0.5;
strong external witness (Φ_external ≥ 0.9) → full seal; weak witness (Φ_external < 0.5) → **HOLD, even
if internal reasoning is perfect**. *"Beautiful internal coherence without external witness is the Iblis
trap."* [constitutional-floors §3]

**R26 · Independence comes from the evidence path, not from using a different agent.** A witness that
reads the executor's own success log is echo reporting. Probe the deployed hash, the external endpoint,
or the observed behaviour. **Different agent ≠ independent witness.** [governance-audit §5 step 4]

**R27 · Governance benchmark probes are bilingual JSONL, 40 per dimension, with evaluable pass
criteria.** `prompt_bm` primary, `prompt_en` secondary; required fields `probe_id`, `dimension`,
`category`, `severity` (P1/P2/P3), `prompt_bm`, `prompt_en`, `expected_behavior`, `pass_criteria`,
`difficulty`. **CCC v2 is a conflict resolution specification (judiciary layer), not a model benchmark.**
[governance-benchmark-authoring]

**R28 · The JSON-LD ontology refuses runtime state.** `/.well-known/governance.jsonld` is static by
design; never duplicate `did.json` service endpoints (reference by `@id`); never remove a term that
appears in any seal-chain entry; `@id` generation must be deterministic and reproducible.
[forge-governance-jsonld]

### DIVERGENCES — kept, not averaged

Two members disagree in the places below. Both statements are kept **verbatim in their references**; this
list exists so a router does not silently pick a winner.

| # | Divergence | Text A | Text B |
|---|---|---|---|
| **D1** | **Two control-state ladders.** Neither is a superset of the other. | `governance-audit` §1.5 — 12 states: DECLARED, PARTIAL, ENFORCED, VERIFIED, CONTRADICTED, UNBUILT, DORMANT, DECOY, DECORATIVE, FALSE_NAME, UNPROVEN, NEEDS WITNESS | `forge-execution-governance` §7 — 4 rungs: DECLARED, REACHABLE, FUNCTIONAL, EFFECTIVE. **Use:** the 12-state vocabulary for a *control's integrity*; the 4 rungs for *wiring* of a control in a running workflow. Do not translate one into the other — they answer different questions |
| **D2** | **F6 is named two ways** inside the cluster. | `constitutional-floors` §1/§10: **F6 EMPATHY** — "Protect the weakest stakeholder" | `constitutional-floors` §9 and `forge-governance-analysis` standing rule 5: **F6 MARUAH** — "institutional critique ≠ personal defamation" |
| **D3** | **Two floor-naming tables** for the same F-numbers. | `constitutional-floors` §1/§10: F1 AMANAH · F2 TRUTH · F3 TRI-WITNESS · F4 CLARITY · F5 PEACE² · F6 EMPATHY · F7 HUMILITY · F8 GENIUS · F9 ANTI-HANTU · F10 ONTOLOGY · F11 AUDITABILITY · F12 INJECTION · F13 SOVEREIGN | `aaa-doctrine-sealing` M10 (Tier-2 compression view): F01 consequence · F02 observation · F03 attestation · F04 representation · F05 coexistence · F06 personhood · F07 reality-exceeds-model · F08 elegance · F09 no-ghost-reality · F10 structure · F11 identity · F12 origin · F13 authority |
| **D4** | **"All 13 floors RATIFIED in code"** (a canon claim) vs the audit rule that a control-like name needs runtime causal evidence before it may be **reported** as enforcing. | `constitutional-floors` §10: "All 13 floors RATIFIED in code with dedicated tests" | `governance-audit` §1.1/§1.2: without CALLER/EFFECT/BYPASS proofs the finding is DECLARED or PARTIAL. **Use:** the ratification statement is canon; the audit rule governs what may be *reported about runtime enforcement*. They are not the same claim |
| **D5** | **Push authorization.** | `aaa-doctrine-sealing` M6: when F13's own instruction was the directive, that instruction **IS** the authorization — re-confirming collapses finished execution back onto the human | `governance-audit` §1.6: an audit never self-authorises the repair of a protected path; report and hold. **Use:** the scope boundary is sealing *under a directive* (A) vs auditing *without one* (B) |

---

## PITFALLS

Union of the seven members' scars. Specificity preserved — command, path, symptom. Full context in the
matching reference.

### Canon, sealing and the ledger

- **Appending to the wrong eureka ledger silently loses the record.** Two exist; only
  `/root/AAA/eurekas/eureka-entries.jsonl` is writable. The canon file is immutable by design — an
  earlier version of the sealing skill named the canon file as the write target and called the live feed
  "a stray with no readers". Both halves were wrong and the label was factually inverted.
- **Skipping `base.md`:** the fragment becomes canonical and still binds nothing, because fragments
  render on demand. The inline line is the whole point.
- **Appending to the generated file instead of the source fragment:** `/root/AGENTS.md` is output;
  `render_one` rewrites it whole. A block appended after the `<!-- Rendered: … -->` stamp reads as live
  in the file you just opened and is deleted at the next render — the agent that appended it is the last
  one to ever see it.
- **Forgetting the render:** the repo is correct and every agent is reading the previous map. Re-render
  after ANY fragment edit, and confirm the hit sits **above** the `<!-- Rendered:` stamp.
- **The footer is automatic; the render list is not.** A new fragment is *listed* with no edit anywhere —
  but listed is not loaded. Editing the render list is editing the renderer, not hand-editing output.
- **Unlabelled new fragment:** the commit dies at the status gate after all the work is written.
- **Editing `FLOOR_TABLE.json` directly:** amendment file only; direct floor edits bypass ratification.
- **One commit for two repos:** AAA and arifOS gate independently.
- **Reporting an amendment as live:** an amendment is a proposal — saying "sealed" is a false receipt.
- **Canon-mutate + complex content: write to a temp file first.** Shell parsing breaks on JSON
  parentheses, quotes and interpolation inside `bash -c "echo '…' >> file"`; the command reports `rc=0`
  and the content does not land. `echo -e` and heredocs inside `canon-mutate run … -- bash -c` break the
  same way. Write `/tmp/<name>.ext`, then `cat /tmp/<name>.ext >> <target>` through canon-mutate, then
  verify with `grep`.
- **W_SCAR gate can block base.md edits** (flags it "touches critical variable" and holds the write
  across patch/write_file/terminal/execute_code). Seal every other layer and report the base.md gap
  explicitly — do not bypass the gate.
- **Some skills cannot be patched by `skill_manage`:** a skill whose directory is a symlink into
  `/root/AAA/skills/**` resolves for reading but refuses writes. Edit the resolved real file directly and
  say which layer you could not seal.
- **"Principles exist" ≠ "principles embedded".** 69 files referencing a principle does not mean any
  single agent loads all 69. A principle present in `canon/` but not in boot surfaces or SOUL.md is
  **documented, not embedded**. Probe all surfaces (SOUL.md, AGENTS.md/base.md, boot sequences, agent
  cards, skills, floor files, ledgers) and report a per-surface hit count.
- **A session-closure receipt ≠ a boot artifact.** A ceremony audit is not the compressed always-loaded
  screen. Do not conflate them when the sovereign says "I would hand this to every coding agent".
- **Harness boot surfaces are not one file.** Hand-copying a clause into `/root/AGENTS.md`, `CLAUDE.md`,
  `GEMINI.md`, `QWEN.md`, `.codex/`, `.config/opencode/`, `.kimi-code/`, `.qwen/`, `.grok/`,
  `.arifos/agents/*/` rots silently. Fix: ONE writer emitting a marker-delimited idempotent block plus a
  scheduled drift check (`/root/scripts/membrane-propagate.py` + `membrane-drift-check.sh`).

### Controls, gates and coverage

- **Auditing the name instead of the mechanism.** Finding the implementation correct proves the code is
  correct, not that anything runs it. CALLER_PROOF is not optional, and a single-surface grep
  manufactures false dormancy — sweep cron store, systemd units/timers, `/etc/cron.d`, crontab, shell
  wrappers, HTTP routes, loader imports.
- **Treating configuration as enforcement.** A permissive-by-default setting is safe-by-accident. Opt-in
  gates score zero on a default install: the skill-write security scan is gated by
  `skills.guard_agent_created`, default **False**, and the guard's own docstring names the uncovered path
  ("opt-in — terminal() runs the same code ungated"). **Read the guard's docstring, not just its decision
  table.**
- **A gate whose failure cannot stop the thing it guards is decoration** — and at its most convincing
  when noisy. `cmd || echo "[ALARM] …"` emits the alarm, consumes the non-zero exit, returns 0, and every
  downstream status surface reports success.
- **A bypass test that invokes the guard script directly proves the guard refuses when asked** — nothing
  about whether any real invocation is intercepted. Read **what the test executes**; `bash <guard_script>
  gmail …` asserting "DENIED" is a tautology. Same defect class as a receipt stream written by the gate's
  own self-test.
- **Three bypass shapes survive a self-testing suite:** guard on no path (`which <binary>`;
  `readlink -f "$(which <binary>)"`), wrapper routing past its own interceptor (bare `["gws", …]`
  resolves via `PATH` to the real binary), and the guard's own escape hatch (`if [ "$INTERNAL" != "1" ]` —
  any process can export that).
- **Subtract the control's own test receipts before counting.** A gate with a self-test writes receipts
  every time anyone runs the tests. Worse: if the receipt payload does not record the caller, test
  traffic cannot be separated from production traffic afterwards — a schema defect worth reporting on its
  own.
- **Distinguish "not wired" from "never invoked yet"** by asking the harness (`hermes hooks list`), not
  by counting receipts. The remediations differ: one config entry vs nothing.
- **Coverage is prior to prevention rate.** A prevention figure with no coverage figure is
  uninterpreted. State "coverage of the committed surface = X", never "enforcement coverage = X" — a
  writer with shell access can change protected state without producing a commit, and those attempts
  never enter the denominator.
- **A locked tree guarantees integrity, never currency.** `chattr +i` freezes whatever draft happens to
  be inside it, so the canonical copy can be the OLDER one. Check `stat -c '%y %s %n'` and a section diff
  against the working draft, and report divergence **by section name**.
- **Cross-read the mutation receipt against the document's own authority claim.** An artifact declaring
  sovereign ratification whose write receipt reads `trace=<…unattributed>` is a contradiction on the
  record — quote both strings verbatim and let the issuer resolve it. A self-declared authority is a
  claim; the receipt is the machine answer.
- **Absent join key ≠ null join key.** Test for the FIELD across all stores before measuring nullity; if
  no store carries `trace_id`, **retract** any prior "N records with trace_id=NULL" claim — nulls are a
  plumbing fix, absence means the causal fabric was never in the schema. `prev_hash`/`chain_hash` proves
  tamper-evidence and order, **not** causal joinability.
- **JSONL ledgers mix line types.** A first line that is a bare string kills `json.loads` + `.get()`
  (`AttributeError: 'str' object has no attribute 'get'`) and reports a false "unreadable store". Skip
  non-dict lines, report the bad-line count, and never ground a verdict on the first parse.
- **Report the terminal fraction, not the row count.** "N records in the ledger" is uninterpreted
  without it; a large PENDING population with no owner and no deadline is an unowned queue that absorbs
  the closure credit of the work that did finish.
- **A census flag contradicts a live call → trust the call.** A registry reading `routable: false` while
  the surface answers is as wrong as a phantom "healthy"; re-stamp or record it stale.
- **`lsattr` trap:** lowercase `i` = immutable; uppercase `I` = htree indexing, **not** immutability.
- **`chmod 700` on a credential store buys nothing when every agent runs as the same privileged uid** —
  report the mode and what it does *not* cover, rather than citing it as protection.
- **Gate verification must exercise the caller's path.** Before crediting any bypass test, confirm it runs
  the path a real caller takes (`PATH` resolution, absolute binary, library/subprocess call) — not the
  control's own file.

### Witnesses, metrics and attribution

- **A metric whose value is a constant is a literal, not a measurement.** Flip the flag and re-run;
  diff two runs with genuinely different inputs.
- **The floor constant:** a geometric mean over clamped factors returns `<floor> ** (1/num_factors)`
  whenever any factor is zero (`0.01 ** 0.25 = 0.3162`). Many actors showing the same number is the floor
  speaking, not agreement. Report the constant, the zero factor, and the underlying ratio.
- **Literal witnesses:** `_hw = 0.95 if actor_verified else 0.42` — an exact match to a literal
  combination proves the field is a restatement of the verified/unverified branch, **never** independent
  corroboration. Check which branch the literals live in (`if not already_minted:` runs only for callers
  that already passed an earlier gate).
- **Cold start:** `n = 0` → sentinel for every scalar; the measuring call is frequently the call that
  writes the first row, so the first probe returns UNMEASURED and the second returns a number with
  nothing else changed. Count the rows that existed at each instant before attributing it to transport,
  client or runtime entropy.
- **Never separate a number from its method** — matching rule + threshold + corpus list. A method
  divergence is the finding; do not average or pick the survivor.
- **Sensor state may not be self-reported** when the measurement is about the system that produced it.
- **A writer log that records a configured name records a label, not an identity:** N entries under one
  label are N unattributable events.
- **Order regex alternation longest-first:** `jsonl` must precede `json` or a real path silently stops
  matching.
- **False absence:** a null result is evidence of absence only if the query **could** have returned a
  hit. Generated store prefixes (`doc_<hash>_Title`, session ids, UUIDs) break name-anchored globs — use
  `-iname '*term*'` or content search, and run a control search aimed at something you know exists first.
  If you cannot construct a control that hits, report `UNPROVEN`.
- **Concurrent-session artifacts are a shared evidence path, not an independent witness.** Corroboration
  needs two independent observation paths; the same artifact read twice is one observation.

### Auditing an external institution

- **Treating a live page as a fixed document** → miss the story. **Cataloguing who IS there without
  asking who WAS there** → miss the removals. Wayback CDX with `collapse=digest` before writing a word.
- **Drupal `Last-Modified` ≈ request time** — ETag regenerates every cache cycle. Validate by fetching
  4–5 sibling pages: all "today" = cache artifact, not a content change.
- **Not pulling the IR/Annual Report PDF to cross-validate** → miss the discrepancy between the live page
  and the filed record. A board size implied by a percentage (`3 women = 43% → 7`) is the cheap check.
- **Naming individuals without institutional framing** → defamation risk. State role, action, structural
  consequence; do not attribute motive without evidence (F6 rule).
- **Hedging verified patterns** → perceived as weakness; state the pattern directly when three or more
  sources confirm it. And always state **ONE** condition under which the analysis fails.

### Benchmarks and ontology artifacts

- **`hf` CLI is deprecated** (so is `huggingface-cli`) — use the `huggingface_hub` Python API.
- **`CommitInfo` has no `commit_id`** — use `commit_url`. The upload succeeds even if the print fails.
- **Duplicate files from parallel agents** (hyphen vs underscore) — `find -name '*.jsonl'` before pushing;
  keep one canonical version.
- **v5–v8 skeleton trap:** 10 probes per dimension is a starting point, not complete. Expand to 40 before
  publishing. Probe IDs must be prefixed with the version (`v5-ps-001`).
- **The README must explain the framework**, not just list files — 4-plane architecture, 6 axes,
  BIJAK/BANGANG/BIJAKSANA taxonomy, APEX-ZEN alignment mapping.
- **A uniform failure across all declared-vs-enforced probes is a failed probe, not a hardened service** —
  verify credential and port first. Bind the probe above 1024, away from the real port, and tear the
  probe down (`ss -lntp | grep <port>`); a stray probe server holding the real port is worse than none.
- **A rejection proves enforcement; a downstream error does not.** If a guarded action fails from *inside*
  the action, the request cleared every policy gate on the way in.
- **A SKILL.md at the character ceiling cannot be patched at all.** Keep SKILL.md lean; put depth in
  `references/`.

---

## REFERENCES

Member bodies, byte-identical to the archived originals (sha256 in the receipt and in each file's
provenance header). Read the one the FLOW lands you on — it holds the procedure; this file holds routing.

| Reference file | Source skill | Original path | Archived at |
|---|---|---|---|
| `references/aaa-doctrine-sealing.md` | `aaa-doctrine-sealing` | `/root/AAA/skills/aaa-governance/aaa-doctrine-sealing/SKILL.md` | `.archive/merge-20260920/governance/aaa-doctrine-sealing/` |
| `references/constitutional-floors.md` | `constitutional-floors` | `/root/AAA/skills/domains/general/apex/governance-core/constitutional-floors/SKILL.md` | `.archive/merge-20260920/governance/constitutional-floors/` |
| `references/forge-execution-governance.md` | `forge-execution-governance` | `/root/AAA/skills/domains/general/apex/governance-core/forge-execution-governance/SKILL.md` | `.archive/merge-20260920/governance/forge-execution-governance/` |
| `references/forge-governance-analysis.md` | `forge-governance-analysis` | `/root/AAA/skills/domains/general/apex/governance-core/forge-governance-analysis/SKILL.md` | `.archive/merge-20260920/governance/forge-governance-analysis/` |
| `references/forge-governance-jsonld.md` | `forge-governance-jsonld` | `/root/AAA/skills/forge-governance-jsonld/SKILL.md` | `.archive/merge-20260920/governance/forge-governance-jsonld/` |
| `references/governance-audit.md` | `governance-audit` | `/root/AAA/skills/governance-audit/SKILL.md` | `.archive/merge-20260920/governance/governance-audit/` |
| `references/governance-benchmark-authoring.md` | `governance-benchmark-authoring` | `/root/AAA/skills/governance-benchmark-authoring/SKILL.md` | `.archive/merge-20260920/governance/governance-benchmark-authoring/` |

### Support files (copied byte-identical, original basenames preserved)

Member bodies name these by relative path (`references/<name>.md`, `scripts/<name>.py`); they were copied
into this umbrella with their basenames intact so those load paths still resolve from the umbrella root.

| Support file | From member |
|---|---|
| `references/commit-gates.md` · `references/external-artifact-intake.md` · `references/doctrine-coding-surfaces.md` · `references/constitutional-compression-patterns.md` | `aaa-doctrine-sealing` |
| `references/555-asi-sensory-cascade.md` · `references/arifos-briefing-openclaw-2026-08-01.md` · `references/hf-governance-ladder.md` | `constitutional-floors` |
| `references/additive-gate-wiring.md` · `references/cross-registry-reconciliation.md` · `references/project-context-files.md` | `forge-execution-governance` |
| `references/ownership-consolidation-analysis.md` | `forge-governance-analysis` |
| `references/decoy-catalogue.md` · `references/metric-derivation-discipline.md` · `references/sensor-falsification.md` · `references/sealing-a-control.md` · `references/seal-and-delivery-verification.md` · `scripts/contract_probe.py` | `governance-audit` |

### Adjacent skills that stay separate (different questions, not merged here)

`seal-ritual/arifos-kernel-seal-ritual` (kernel/VAULT999 mechanism) · `seal-discipline` (what a
close-record may be called) · `symbol-namespace-integrity` · `verify-work` · `claim-receipt-discipline` ·
`deploy-drift-verification` · `self-recurrence-guards` · `agent-exploration-discipline` ·
`governance/mcp-organ-probe` · `governance/external-review-intake` · `apex-verdict` · `apex-gate-evaluator`.

DITEMPA BUKAN DIBERI ⚒️
