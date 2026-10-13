---
name: governance-contract-self-audit
description: "Author and self-audit governance contracts (delegation doctrine, spawn rules, judgment coverage thresholds, audit schemas) for agent loops so they survive a parallel adversarial audit BEFORE you seal them. Covers the Golden Test pattern (parallel SCOUT/CRITIC/AUDITOR dispatch with explicit disagreement-success criteria), the F1-F15 failure catalog from real contract audits, the schema self-reference paradox, and the two-competing-contracts-in-same-dir vestigial pitfall. Trigger: any 'draft a contract that governs agent X', 'add governance to delegation loop', 'spec a spawn rule', 'set judgment_coverage threshold', or before SEAL of any document that will be enforced (or aspirationally enforced) across an agent loop."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [governance, contracts, audit, self-audit, golden-test, delegation, f1-f13]
    related: [verify-nested-sibling-reports, agent-config-validation, arifos-prompt-doctrine, constitution-institution-mapping, persistent-memory-effectiveness-gate (P-MEM-GATE v1.0 — staged /root/forge_work/paper2610.07782-embedding/01-canonical-rule/MEMORY-EFFECTIVENESS-GATE.md; canonical placement /root/AAA/governance/ requires authorized shell — see file receipt)]
---

# Governance Contract Self-Audit

The pattern: you draft a contract (delegation doctrine, spawn rules, judgment coverage, audit schema) that **claims to govern an agent loop**. You want to seal it. Before sealing, run a **Golden Test**: dispatch parallel SCOUT/CRITIC/AUDITOR archetypes and let them disagree productively. Surface the failures. Fix them. THEN seal.

Why? Because contracts written by the governed party **always look complete to themselves**. The CRITIC archetype — the persona forbidden from proposing solutions — exists exactly to break that loop. If CRITIC cannot find a flaw, the contract is either trivially obvious or self-deceiving.

## When to use this skill

Trigger on any of:
- "Draft a delegation contract / doctrine / spec for agent X"
- "Add governance to my delegate_task loop"
- "Set judgment_coverage threshold"
- "Write spawn rules: spawn_reason, risk_tier, archetypes"
- Before **SEAL** of any document claiming authority over an agent loop
- When two documents in the same directory claim overlapping authority (orphan-from-prior-session test)

Do NOT use for:
- Verifying a sibling agent's audit report (use `verify-nested-sibling-reports`)
- Validating a JSON config schema (use `agent-config-validation`)
- Editing the prompt stack (use `arifos-prompt-doctrine`)

## The Golden Test (parallel self-audit pattern)

### Pre-test: classify the contract

Before dispatching workers, classify what you're drafting:

| Type | Examples | Audit pressure |
|---|---|---|
| **Spec for an agent loop** | Spawn rules, judgment coverage, return schemas | High — workers will run under it |
| **Doctrinal document** | Section 5 Diseconomy Boundary, federation principles | Medium — cited by other docs |
| **Operational checklist** | Pre-spawn checklist, audit procedure | Lower — used as guide |

Higher audit pressure = dispatch more workers (3-5 in parallel). Lower = 2 may suffice.

### Dispatch shape (parallel batch)

```python
delegate_task(tasks=[
  {"goal": "<SCOUT prompt>", "context": "<SCOUT context>", "role": "leaf"},
  {"goal": "<CRITIC prompt>", "context": "<CRITIC context>", "role": "leaf"},
  {"goal": "<AUDITOR prompt>", "context": "<AUDITOR context>", "role": "leaf"},
])
```

All 3 run in parallel. Each gets **isolated context** (cannot read the others' output). They return structured A3-style receipts (see `references/golden-test-receipt-templates.md`).

### Per-worker goal templates

**SCOUT (find evidence of value):**
- "Find evidence that this contract would successfully reduce governance debt. Where does each mechanism map to a debt type? What is enforceable vs aspirational?"
- Forbidden: agreement without citation, "looks good", "this is solid"

**CRITIC (find flaws, mandatory dissent):**
- "Find every flaw, hidden assumption, and failure mode. Challenge ≥ 3 assumptions. Include `assumptions_challenged:` block. You MUST find at least one reason this contract could make things WORSE, not better."
- Forbidden: politeness, proposing solutions, smoothing over gaps

**AUDITOR (verify provenance + structural integrity):**
- "Verify every claim has a source. Does the schema work as YAML? Is the formula correct? Can the contract audit ITSELF using its own schema?"
- Forbidden: strategic recommendations, new conclusions

### Test 1-5 success conditions (audit must produce these signals)

| # | Test | Success = | Failure = |
|---|---|---|---|
| 1 | **Echo Chamber Resistance** | SCOUT ≠ CRITIC and AUDITOR can trace claims | All three agree too quickly → authority drift suspected |
| 2 | **Hidden Assumption Attack** | ≥ 1 main assumption challenged | Zero challenges → doctrine without adversary |
| 3 | **Spawn Economics** | Workers produce anti-spawn criteria | Spawn bias detected (always recommend more spawns) |
| 4 | **Constitutional Solvency** | Identifies over/under-governance | "Everything needs Apex" → over-governed; "Nothing needs Apex" → under-governed |
| 5 | **Receipt-Chain Stress** | Surfaces hash-of-self or schema self-reference gap | Schema audits itself cleanly → either trivial or the gap is hidden |

If Test 1 produces echo chamber (no disagreement), **the test failed** — dispatch a 4th worker with a sharper prompt or revise the contract before re-running.

### After audit: act honestly

1. Compile findings into `audit-YYYY-MM-DD.md` in same dir as the contract
2. **Update contract status** from DRAFT to DRAFT-PENDING-REVISION (or HOLD)
3. Do NOT seal until F1-F15 hard failures are addressed (see catalog below)
4. Re-run Golden Test after revision

## F1-F15: The Governance Contract Failure Catalog

Hard failures observed in real contract audits (2026-08-07, Hermes delegation context audit). All 15 are blocking for SEAL unless explicitly waived.

### Schema & structural failures

| # | Failure | Symptom | Fix |
|---|---|---|---|
| **F1** | Hash-of-self paradox | `receipt_hash: <sha256-of-this-output>` requires hashing output containing the hash | Specify "hash output excluding this field" |
| **F2** | Schema incompatibility inside same doc | A3 spine is `evidence/interpretation/hypothesis`; A6 mandates `claim/source/transformation` | Pick one canonical schema, or allow both fields explicitly |
| **F3** | Two competing contracts in same dir | Same scope, drafted in different sessions, neither references the other, contradictory schemas | Merge, or delete one, or rewrite one to defer to the other |
| **F9** | YAML schema invalid as literal | `- <claim>: [OBS] <description>` raises ParserError | Provide canonical YAML structure with valid syntax; test with mechanical validator |

### Logic & metric failures

| # | Failure | Symptom | Fix |
|---|---|---|---|
| **F4** | Unsourced key values | `max 3 concurrent`, `0.7 threshold` appear without source | Cite source or change to "data-derived, TBD after baseline" |
| **F5** | Redundant algebra | `enforcement_gap = unjudged / risky = 1 - coverage` | Delete redundant metric or rename to make distinction explicit |
| **F6** | Coverage >100% allowed | `apex_verdicts` not restricted to risky → debt can go negative | `apex_verdicts` MUST be subset of `risky_actions` (T2+T3 only) |
| **F8** | Tier assigned before risk materializes | T1/T2/T3 set at dispatch; risk materializes at integration | Allow tier upgrade at integration, or accept as known limitation with caveat |
| **F10** | T1 misclassification = false solvency | Cheapest way to hit 100% coverage = classify every spawn T1 (auto-execute) | T1 must be minority tier, with per-session T1 cap |

### Self-reference & enforcement failures

| # | Failure | Symptom | Fix |
|---|---|---|---|
| **F11** | Session boundary = enforcement unit, controlled by measured entity | End session early with low coverage → debt evaporates | External session auditor (arif_judge or external clock) governs boundaries |
| **F12** | Entropy gate = unfalsifiable self-interview | "Can you state one-sentence entropy reduction?" — any motivated agent can | Gate needs an observer; or downgrade to advisory with caveat |
| **F13** | References nonexistent infrastructure | "Scorecard", "closure seal", "session flagged" | Implement the infrastructure OR remove references |
| **F15** | Footer self-certifies at exactly F7 cap | "Confidence: 0.90" = exactly the F7 cap = not humility | Lower confidence OR cite derivation |

### Coherence failures (cross-section)

| # | Failure | Symptom | Fix |
|---|---|---|---|
| **F7** | Archetype rules violated by mandatory schema | SCOUT forbidden "drawing conclusions" but `interpretation: [INT]` is mandatory | Either weaken forbidden rules or make fields optional per archetype |
| **F14** | Companion doctrine contradicts contract | Different tool bindings, different judge interfaces, schemas disagree | Reconcile and choose canonical |

## The Two-Competing-Contracts Vestigial Pitfall

Distinct from sibling races (covered by `arifos-prompt-doctrine`). This is the **prior-session vestigial** trap:

**Pattern:** Today you draft `delegation-context.md`. Tomorrow you discover `DELEGATION_DOCTRINE.md` already exists in the same dir from a prior session. Both cover the same scope (A1-A7). Neither references the other. They have different specifics. SEAL of either breaks the other.

**Defense:**
1. **Before drafting any contract**, list everything in the target directory: `ls /root/.arifos/agents/<name>/`
2. **Read any existing contract** in that scope before writing
3. **If one exists**: either merge, or write a doc that explicitly defers: "Superseded by X; kept for history"
4. **If neither ref. the other and they conflict**: that's F3 — blocking failure, surface to sovereign

This trap repeats across every governance scope (delegation, judgment, audit, schema). Add a directory-listing step to every draft workflow.

## The Self-Judging Loop Doctrine (from the CRITIC archetype)

CRITIC's most important finding, every time: **the contract converts honest absence of scrutiny into certified illusion of scrutiny.**

This is a general principle, not specific to any one contract:
- Self-attested gates do not change behavior (Hermes judges whether to call judge)
- Adding structure risks moving the loop one level up, not breaking it
- Coverage metrics computed by the measured entity are form-filling, not telemetry
- Provenance labels are claims about provenance, not provenance itself

If CRITIC's verdict survives AUDITOR's verification, **the contract is NOT ready for SEAL** — regardless of how many workers approved it.

## Recovering from a Failed Golden Test

When the test surfaces real failures (which it should, for any non-trivial contract):

1. **Do NOT seal.** Update status to HOLD pending revision.
2. **Log the audit** at `audit-YYYY-MM-DD.md` in same dir. Use template at `references/audit-report-template.md`.
3. **List failures** with F1-F15 IDs and verbatim quotes from worker receipts.
4. **Decide which failures to fix before next iteration** vs which to waive with F13 ratification (the sovereign can explicitly accept a known-flawed contract, but cannot unknowingly).
5. **Re-run Golden Test** after revisions. If failures decrease but persist, decide: keep iterating, or escalate the contract's scope to "advisory" instead of "binding."

## The Four Debts — Agent Spawn Conservation Law (2026-08-07)

Every spawn **transfers burden** between exactly four buckets. None of them disappears. The law is conservation: the bucket changes, the total does not.

| Debt | What it counts | When it explodes |
|---|---|---|
| **Verification debt** | Claim-to-evidence links, OBS count vs total claims | Hours-days |
| **Attribution debt** | Actor-action linking, who-did-what records | Days-weeks |
| **Coordination debt** | Communication edges, n(n-1)/2 if no star topology, context distribution | Today (immediate) |
| **Provenance debt** | Where claims came from, VAULT chain, claim/source/transformation | Years later (courtroom maturity) |

The four-debt timing hierarchy is **non-substitutable**: each has its own cadence. Architecture choices shift debt between buckets but never retire it. A star topology reduces coordination debt (linear edges n-1 vs quadratic n(n-1)/2) and pushes the burden into judgment/provenance — visible buckets that the doctrine must then pay down.

**Star topology constraint applied to federation:**

- OpenCode: 6 agents. Full mesh = 15 edges. Star = 5 edges. Star saves 67%.
- Hermes: primary + 6 children. Full mesh = 21 edges. Star = 6 edges. Star saves 71%.
- One nesting level (depth=2) brings star back from 6 edges to 38+ edges — nesting disabled by `max_spawn_depth: 1`.

**The constitutional sentence** (Arif-ratified reformulation, 2026-08-07):

> The fundamental flaw in agent spawn is not too many agents — it's that every spawn produces new debt, and a mature federation does not optimize agent count, but the rate of debt that can be repaid by the judgment and provenance layers.

**judgment_coverage metric (Kimi agent spec, A5):**

```yaml
spawn_telemetry:
  risky_actions_taken: int    # mutations, recommendations, conclusions
  apex_verdicts_sought: int   # explicit arif_judge calls before action
  judgment_coverage: float    # verdicts / max(actions, 1); <1.0 = governance leak
```

Surface `< 1.0` at session seal — surfaces as governance debt carried into next session. Coverage = 0 is acceptable only when `risky_actions_taken = 0` (pure T1 read-only work).

## The Kimi Spawn Protocol (Kimi agent A-E, 2026-08-07)

A more aggressive spawn contract than Hermes doctrine. Key divergence: **mandatory structured return as INVALID-on-missing-fields** (vs Hermes's prompt-discipline). Schema fields: `worker`, `task`, `inputs`, `evidence`, `interpretation`, `hypothesis`, `unknown`, `confidence`, `key_challenge`, `receipt_hash`, `parent_spawn_hash`. Plus pre-spawn gate: `archetype`, `spawn_reason`, `risk_tier`, `expected_entropy_reduction`, `parent_session_id`, `parent_spawn_id`.

**Reconcile before SEAL:** pick ONE canonical naming set for cross-federation fields (Kimi's names are cleaner — `parent_session_id`/`parent_spawn_id`/`receipt_hash`/`parent_spawn_hash`). Reconcile tool manifests with declared ceilings — Kimi's `af-fix: EXECUTE_REVERSIBLE` disagrees with live `tools: [Bash, Write, Edit]`; three of seven Kimi ceilings disagree with live tool declarations. Ship v0.1.0 of BOTH as DRAFT-HOLD; do NOT ship enforcement the runtime cannot deliver.

## The Golden Test Transcript (2026-08-07, against Hermes DELEGATION_DOCTRINE.md)

Live test run via `delegate_task(tasks=[...])` with 3 parallel leaf archetypes against the freshly-drafted Hermes doctrine. **All three converged on different structural flaws** — the test worked:

- **SCOUT** caught: `subagent_auto_approve: true` in config contradicts doctrine §8 (only primary seals). 7 of 13 concrete claims unencoded in config (aspirational not enforced).
- **CRITIC** caught: A7 entropy gate is self-certified by the spawner — structural self-defeat (F12 in catalog). Four-archetype grid can't contain real hybrid epistemic work.
- **AUDITOR** caught: TWO contracts existed in same dir (`DELEGATION_DOCTRINE.md` + `delegation-context.md`) — not byte-equivalent on A3/A5, silent drift risk. SOUL.md epistemic labels use `[OBS]/[DER]/[INT]/[SPEC]/[UNKNOWN]`, doctrine uses `[OBS]/[INT]/[HYP]/[UNKNOWN]` — labeled drift.

**Doctrine's verdict on itself: HOLD, not SEAL.** All three workers disagreed on specific points; the contract survives audit but cannot be bound until reconciliation is done.

## The Federation-Level Enforcement Gap (core insight, 2026-08-07)

The deepest lesson of this session: **all three harnesses (OpenCode, Kimi Code, Hermes) independently converged on the same star topology, the same spawn contract shape (A1-A7), and the same architecture. But none of them enforce their contracts programmatically.**

### The pattern

| Layer | Status |
|---|---|
| Policy | ✅ Written (SOUL.md, AGENTS.md, delegation-context.md) |
| Specification | ✅ Written (spawn_enums.json, A1-A7 contract) |
| Documentation | ✅ Written (Section 5, changelog) |
| **Enforcement** | **❌ Missing everywhere** |

Governance that exists only in docs and specs is governance that has **already failed** — it is merely awaiting the test that proves it.

### Why enforcement fails last

- Enforcement requires **code** (hooks, validators, parsers) — not just YAML/markdown
- Enforcement requires **runtime binding** (capability ceilings that strip tools, not just declared ceilings)
- Enforcement requires **verification** (someone checking the enforcement is actually running)
- All three are more expensive than writing a policy doc

### What "AAA level" requires

A harness is "AAA level" when all three layers are present:
1. **Identity alignment** — SOUL.md, F13 binding, invariants (most harnesses have this)
2. **Authority alignment** — capability ceilings declared AND enforced at runtime (most harnesses don't)
3. **Receipt alignment** — per-spawn telemetry, aggregate-derived-only, sealed to VAULT999 (only spawn_enums.json exists)

### Federation invariant (Arif-ratified)

> **Governance is measured per spawn, never solely per task.**

Aggregate telemetry may summarize for dashboard. Aggregate telemetry may not replace spawn-level telemetry.

### Federation spawn enums

Canonical cross-harness source: `/root/AAA/federation/protocols/spawn_enums.json`

Contains:
- `spawn_reason` enum (7 values: verification / criticism / synthesis / reconnaissance / domain_analysis / implementation / refactor)
- `risk_tier` definitions (T1/T2/T3 with judge_required flags)
- `archetype_ceilings` per harness (per-archetype max confidence caps)
- `parallel_spawn_rule` (max 3, per-spawn telemetry required, aggregate derived-only)
- `seal_status` tri-state (SEALED / UNSEALED_INFRA / FAILED_VALIDATION)
- `judgment_coverage_formula` (clamped [0,1], avoids division by zero)
- `federation_invariant` one-liner

### The tri-state seal status (2026-08-07)

Separate constitutional failure from infrastructure failure:
- `SEALED` — constitutional seal applied, receipt in VAULT999
- `UNSEALED_INFRA` — receipt valid but vault unavailable (infrastructure failure, NOT governance leak)
- `FAILED_VALIDATION` — receipt rejected by constitutional validation (IS a governance leak)

Rule: **Do not punish governance for infrastructure failure.** Audit must distinguish.

### Alignment status (2026-08-07)

| Harness | Identity | Authority | Receipts | Enforcement | AAA level? |
|---|---|---|---|---|---|
| OpenCode | ✅ | ✅ (judge-gate plugin) | ⚠️ | ⚠️ | Partial |
| Kimi Code | ✅ | ⚠️ (ceilings declared, not stripped) | ⚠️ | ❌ | Partial |
| Hermes | ✅ | ❌ (self-judging loop) | ❌ | ❌ | Not yet |
| Codex / Copilot / Claude | ⚠️ (registry only) | ❌ | ❌ | ❌ | Not aligned |
| Others (Gemini, Cursor, Aider, Qwen) | ❌ (no config on disk) | ❌ | ❌ | ❌ | Not aligned |

See `references/federation-level-enforcement-gap.md` for the full enforcement checklist and what each harness needs.

## The Constitutional Penetration Test (post-contract seal)

The deepest test of any drafted contract: **can the runtime violate it without leaving a receipt?**

Run this AFTER the Golden Test surfaces the contract's structure flaws and the contract is DRAFT-PENDING-REVISION. The penetration test answers the *runtime* question — not "is the contract well-formed" but "is it actually binding?"

### Procedure

1. **Pick one active harness** at a time (Hermes, OpenCode, Kimi Code — not dormant treaty members).
2. **For each F-invariance**, identify the smallest behavior that would constitute a violation. Examples:
   - F-01 (no authority delegation): a child spawn that bypasses the primary on a T2 task
   - F-02 (judgment path on risky action): a T2+ action taken without `arif_judge` consulted
   - F-09 (capability ceilings override instructions): a tool declared disallowed but invoked anyway
3. **Probe the runtime** — read config, read hooks, grep for the enforcement code.
4. **For each vector**, classify:
   - `WIRED` — enforcement code exists, has been observed firing (or has never fired because no violation attempted)
   - `WIRED-UNTRIGGERED` — enforcement exists but has zero history of blocking anything → cannot claim it works
   - `MISSING` — no enforcement code; violations are silent
   - `WITNESS-ONLY` — code logs receipt but exits 0 (never blocks)
5. **Compile the per-harness verdict table** before drafting the ratification request.

### Live example (2026-08-07, AAA Federation Contract v0.1)

| Harness | F-01 | F-02 | F-09 | F-11 | Verdict |
|---|---|---|---|---|---|
| Hermes | MISSING (`subagent_auto_approve: true` + no delegation receipts) | MISSING | n/a | MISSING (no delegation receipt trail) | Silent violation possible |
| OpenCode | WIRED | WIRED (judge-gate present, but `gated_total=0, blocked_total=0` across all sessions) | n/a | WIRED (opencode_receipts.jsonl active) | Unproven — never caught a live violation |
| Kimi Code | WITNESS-ONLY (hooks exit 0 by design — "witness-only by F13 SOVEREIGN override 2026-06-23") | WITNESS-ONLY | MISSING (manifest declares `disallowedTools: [Bash]` but no runtime verifier) | WITNESS-ONLY | Silent violation possible |

**Three vectors exist across three harnesses.** The constitution is sound on paper; the runtime cannot bind it.

### What the verdict unlocks

- `WIRED` on all axes → ready for F13 ratification → PARTIAL-SEAL → full SEAL after F13 stamp
- `WIRED-UNTRIGGERED` → schedule a controlled live-fire test (trigger an actual T3, confirm gate blocks, log receipt) → then ratification
- `MISSING` or `WITNESS-ONLY` → PARTIAL-SEAL only; flag the missing enforcement as T2 follow-on work; never ratify full SEAL until the runtime is hardened

**Do not seal what the runtime cannot bind.** A constitution without enforcement is a treaty, not a law.

## When Sovereign Directive Conflicts With Doctrine You Authored (recurring class)

You have just spent the session writing a contract that says "deploy requires F13 ratification." Then the sovereign sends a sweeping directive: *"federate AAA + commit gitwrap + deploy AAA + zen all."*

**The doctrine wins. Always. State this explicitly, do not silently comply.**

Why: the constitution you just authored is itself a sovereign artifact. If you deploy unratified doctrine, you are violating F13 ("any change to F1-F13 requires sovereign sign-off") — even if the sovereign directive looks like it's giving you permission. The directive may be a sovereign's casual expression, not a deliberate ratification of the specific DRAFT contract. Only an explicit F13 seal — "ratify contract v0.1 now" — closes the gap.

**Procedure when this conflict fires:**

1. **Classify each directive item** by action class: T1 (read/test), T2 (reversible edit), T3 (irreversible / constitutional / sovereign change).
2. **Execute T1 items** (test harnesses, sweep health, capture receipts).
3. **Stage T2 items** (commit locally if the artifact is reversible; don't push).
4. **Hold T3 items** (deploy, contract SEAL, constitutional change) until explicit ratification.
5. **Report the filter explicitly** to the sovereign: "I executed items X and Y. I held items Z because [doctrine reason]. Confirm ratification to proceed."
6. **Surface the drift** that may have produced the conflict — sometimes a parallel sibling subagent already drafted v0.1.1 or v0.1.2 of the same contract, creating canonical selection problems. List the file paths that exist before asking for ratification.

**The cost of saying no:** the sovereign sees you held. They either confirm (you proceed) or override (you proceed). The cost of saying yes to a T3 the doctrine forbids: constitutional violation that takes a Reckoning to discover and unwind. Asymmetric — refuse T3, ask first.

### Defense against the implicit-ratification trap

A directive that *sounds* like ratification but isn't:
- "Deploy AAA" — sounds like go, but doesn't name a version, doesn't reference the contract, doesn't say "I have read it and ratify it"
- "Commit everything and ship" — T2+T3 mix, treat separately
- "Zen all and federate" — uses invocation words, doesn't carry F13 weight

A directive that *is* ratification:
- "I ratify AAA_FEDERATION_CONTRACT_v0.1 with the 15 invariants." (named version + explicit stamp)
- "Apply F13 to the contract draft." (explicit seal action)
- "SEAL the Kimi spawn protocol v0.1.0 as binding, not the under advisory." (status change explicit)

When in doubt: ask. The doctrine that requires ratification also defines what ratification looks like. Use that.

## What's adjacent (NOT covered here)

- **Sibling reports** (other agents auditing us) → `verify-nested-sibling-reports`
- **Config schema validation** (JSON tool errors) → `agent-config-validation`
- **Prompt-stack editing** (SOUL/AGENTS) → `arifos-prompt-doctrine`
- **Constitutional mapping** (Acemoglu/Ostrom onto F1-F13) → `constitutional-institution-mapping`

## The Constitution-First Ordering Rule (2026-08-07 Arif correction)

**PITFALL: Do not build specs from the bottom up.** When asked to "make it AAA level" or "align all agents", the instinct is to produce AGENTS.md, SPAWN_CANON.json, alignment-status.md, AGENT_CARDS_INDEX — all downstream artifacts. This is wrong.

The correct order is top-down:

```
AAA_FEDERATION_CONTRACT  (root: invariants only, ~15 one-sentence rules)
    ↓
SPAWN_CANON.json         (enums, ceilings, formulas — machine-readable)
    ↓
AAA_ALIGNMENT_STATUS.md  (live audit board)
    ↓
AGENT_CARDS_INDEX.json   (inventory)
    ↓
Cross-harness AGENTS.md  (onboarding layer)
    ↓
Harness configs          (per-agent implementation)
```

**Constitution → Protocol → Implementation.** Never the reverse.

When the user says "forge 4 artifacts", but no constitution exists: stop. Forge the constitution first. The 4 artifacts become branches of the root, not independent deliverables.

**Symptom of bottom-up trap:** "spec → spec → spec → spec → spec" with enforcement still missing. This is documentation, not constitution.

## The Concurrent-Canonical-Write Failure Mode (new: F3b)

Distinct from F3 (two competing contracts in same dir from different sessions). This is the **concurrent write**:

**Pattern:** Two agents (e.g., Hermes + Kimi) write the same canonical artifact (e.g., `AAA_FEDERATION_CONTRACT_v0.1`) to different paths at the same timestamp, neither referencing the other, with different INV-ID assignments.

**Why it's worse than F3:** F3 is a prior-session vestigial that can be caught by listing the directory first. F3b is a live concurrency failure — both agents read the same instruction and produce incompatible outputs simultaneously.

**Detection:**
```bash
ls -lt /root/AAA/federation/ | head -5  # find simultaneous writes
md5sum /path/a /path/b                  # different content, same timestamp
```

**Resolution recipe (F3b live incident 2026-08-07):**

When you detect two concurrent writes, the order matters. Reverse-order is wrong:

1. **DON'T silently delete one.** F13 covers irreversible acts; deletion of a contract is irreversible.
2. **DON'T pick "yours" by reflex.** Bias toward own work is exactly what INV-02 (capability ceiling) and INV-11 (memory not enforcement) warn against.
3. **DO archive both with a timestamped receipt path.** The archive IS the receipt.
4. **DO compare ID assignments honestly.** If the two artifacts assign different INV-IDs to the same concept, that's not a "pick one" decision — it's a reconciliation problem. The reconciliation is itself F3.
5. **DO surface the dual-write to the sovereign with your own bias declared.** Don't pretend to be neutral; declare which you think is canonical and why, then let F13 decide.
6. **DO log the incident as an F3b violation**, not silently resolve. The receipt chain breaks if you resolve without recording.

```bash
mkdir -p /root/AAA/federation/_archive/2026-08-07-pre-canon-merge/
cp /root/AAA/federation/AAA_FEDERATION_CONTRACT_v0.1.md \
   /root/AAA/federation/_archive/2026-08-07-pre-canon-merge/AAA_FEDERATION_CONTRACT_v0.1-MD-DRAFT.md
# (the YAML version was kept canonical — see also references/concurrent-canonical-write-incident-2026-08-07.md)
```

**What "canonical" means in F3b:**
- If one artifact has richer metadata (e.g., YAML with `enforces`/`consequence`/`source` per invariant vs MD with prose), prefer the metadata-richer one IF the metadata doesn't contradict the prose.
- If both are equally rich but disagree on IDs, neither is canonical until the IDs are reconciled — propose the reconciliation to F13.
- The artifact at the deeper path (e.g., `federation/contracts/...` vs `federation/...`) is NOT automatically canonical. Depth is a hint about who wrote it, not about authority.

**Defense (avoid F3b in the first place):**
1. When two agents receive the same "forge X" instruction, the instruction itself must include `canonical_path:` so both write to the same location
2. If a concurrent write is detected post-hoc: **archive both, re-derive canonical from both inputs** (not "pick one")
3. Add INV-16 to the contract: "Concurrent canonical writes are a violation, not a feature"

**The dual-write is itself a constitutional test (eureka-side observation):** when two agents write the same contract without coordination, the failure mode is **the contract was not needed** (both wrote what was already evident) OR **the contract needs an explicit coordination protocol** (canonical-path directive in every "forge X" task). Either way, the dual-write tells you the spawning instruction was underspecified.

## The "Problem-Found → Control-Added → Ratified" Ordering Rule (888-APEX directive 2026-08-07)

Distinct from constitution-first ordering (which is about derivation top-down). This rule is about **ratification timing**:

**Sequence:** Audit problem → Add control → Re-verify → THEN ratify.

**Why:** Ratifying before enforcement exists produces a "PARTIAL-SEAL" with no enforcement layer — the contract is documentation, not law. The sovereign reads "SEAL" and assumes the runtime is bound. It isn't. The seal is theatre.

**Anti-pattern (do NOT do this):**
```
Audit finds E-22 YES (runtime violates without receipt)
↓
Ratify contract v0.1 as SEAL
↓
"Maybe fix later"
```
The seal is granted on a runtime that still can't bind it. Constitution + no enforcement = treaty, not law.

**Correct pattern:**
```
Audit finds E-22 YES (runtime violates without receipt)
↓
Ship control (e.g., patch MUTATE_PATTERNS, write skeleton gate)
↓
Re-run E-22 → verdict shifts from YES to PARTIAL
↓
Ratify as PARTIAL-SEAL with enforcement gap explicitly declared
↓
Sovereign can then decide: accept PARTIAL (governance documented, runtime still porous) OR wait for full enforcement
```

**This ordering is also the difference between "constitution is doctrine" and "constitution is enforced doctrine"** — same word, different epistemic state. PARTIAL-SEAL with declared gaps is honest; SEAL with hidden gaps is fraud.

**When the sovereign sends a sweeping directive ("federate AAA, commit, deploy, zen all") that collides with this rule:**
- The directive may LOOK like ratification. It is not — it doesn't name a version, doesn't reference the contract, doesn't say "I have read it and ratify it".
- Hold T3 items (deploy, contract SEAL, constitutional change) until explicit ratification.
- Execute T1/T2 items (test, scan, write spec) immediately.
- Report the filter explicitly: "Executed X and Y. Held Z because [doctrine reason]. Confirm ratification to proceed."

The directive's invocation words ("federate", "deploy", "zen") do not carry F13 weight. The doctrine defines what ratification looks like. Use that.

## Active vs Dormant Harness Design Principle (2026-08-07 Arif correction)

When aligning a federation, **optimize for the 3 active voting members, not the 9 total registry entries.**

| Status | Harnesses | Action |
|---|---|---|
| **Active** (producing entropy) | OpenCode, Kimi Code, Hermes | Full alignment pipeline |
| **Dormant** (treaty members) | Codex, Copilot CLI, Claude Code, Cursor, Gemini CLI, Aider, Qwen Code | Registry entry only; full alignment on reactivation |

Do not write configs, hooks, or onboarding for dormant harnesses. They optimize for nothing.

## The spawn_enums.json Canonical Source

Cross-harness enum authority lives at:

```
/root/AAA/federation/protocols/spawn_enums.json
```

Contains: `spawn_reason` (7 values), `risk_tier` (T1/T2/T3 with judge_required flags), `archetype_ceilings` per harness, `parallel_spawn_rule` (max 3, per-spawn required), `seal_status` tri-state (SEALED / UNSEALED_INFRA / FAILED_VALIDATION), `judgment_coverage_formula` (clamped [0,1]), `federation_invariant` one-liner, `archetype_confidence_caps`.

Any harness config that defines its own enums is drifting from canonical source. This is F15 (docs match reality).

## Checklist: Contract Draft Sequence

0. **Forge constitution first** — 15 invariants, one sentence each, before any downstream artifact (constitution-first ordering rule)
1. **List target directory contents** — surface any existing contracts (F3 + F3b defense)
2. **Classify the contract type** — agent-loop spec vs doctrinal vs operational
3. **Draft with explicit status: DRAFT** in YAML frontmatter
4. **Classify each section** — schema / logic / self-reference / coherence
5. **Pre-empt F1-F15** — read the failure catalog and audit your own draft against it
6. **Dispatch Golden Test** (parallel SCOUT/CRITIC/AUDITOR) — see templates
7. **Verify all 3 returned** with structured receipts
8. **Compile audit report** at `audit-YYYY-MM-DD.md`
9. **Update status** based on findings (DRAFT → DRAFT-PENDING-REVISION, or HOLD, or READY-FOR-SOVEREIGN)
10. **Surface to F13 sovereign** for ratification — never self-SEAL
11. **Surface to F13 sovereign** for ratification — never self-SEAL — and if the directive collides with doctrine, refuse T3 explicitly

## The K-02 Transition (witness → enforcer, inflection point)

**Core distinction:** before K-02, the constitution observed reality. After K-02, it altered it. A receipt saying `DENY / exit 2 / tool halted` has more governance value than a hundred doctrinal refinements — because it changes outcomes.

**Pattern:** one invariant → hook script → exit non-zero on violation → receipt emitted → audit confirms.

**Live verification (2026-08-07):** Hermes `arifos-hermes-gate-hook.py` wired as `pre_tool_call` shell hook. Test 4 scenarios:
| # | Tool | Input | Decision | Exit |
|---|---|---|---|---|
| 1 | `terminal` | `cat /root/.secrets/kunci-mas.env` | BLOCKED | exit 2 |
| 2 | `write_file` | `/tmp/test.txt` | WITNESSED | exit 0 |
| 3 | `terminal` | `chattr -i /root/arifOS/VAULT999/outcomes.jsonl` | BLOCKED | exit 2 |
| 4 | `read_file` | `/etc/hostname` | PASSTHROUGH | exit 0 |

**Receipt path:** `/root/.local/share/arifos/hermes_hook_receipts.jsonl`

**Wiring pattern (Hermes shell hooks, the only hook system Hermes supports):**
- Script must be Python or Bash, reads JSON on stdin (`hook_event_name`, `tool_name`, `tool_input`, `session_id`)
- Outputs `{"action": "block", "reason": "..."}` + `sys.exit(2)` to deny
- No output + exit 0 = allow
- Register in `config.yaml`: `hooks.pre_tool_call: [{matcher: "*", command: <path>, accept_hooks: true}]`
- Takes effect on next session (`/reset` or gateway restart)

**K-02 receipts use `k02_transition: true` tag** so they can be filtered from general receipts.

**The K-02 inflection (formalized):**
```
Before K-02: Constitution observes reality.
After  K-02: Constitution alters reality.
```

**Failure to reach K-02 means:** governance exists only as documentation, not enforcement. Document-only governance has already failed — it is merely awaiting the test that proves it.

---

## Federation Envelope (canonical governance interface)

Every agent action must carry:

```yaml
envelope:
  identity:     {agent_id, harness, session_id}
  authority:    {ceiling: OBSERVE_ONLY | DRAFT_ONLY | EXECUTE_REVERSIBLE | EXECUTE_AFTER_SEAL | DISPATCH_ONLY | JUDGMENT_ONLY, role}
  classification: {tier: OBSERVE | T1 | T2 | T3, reversal: YES | NO | PARTIAL}
  constraints:  [no-self-modification, fail-closed, receipt-required, envelope-required]
  judgment:     {verdict: SEAL | HOLD | VOID | NONE, judge_id, judge_url, judged_at}
  receipt:      {receipt_id, parent_receipt, vault_path, emitted_at}
  transport:    {layer: MCP | A2A | DIRECT | RPC, target}
```

**Gate when missing:**
| Missing | Action |
|---|---|
| Envelope (entire) | Deny — ungoverned |
| Identity | Deny |
| Authority ceiling | Deny |
| Classification tier | Default OBSERVE (fail-closed) |
| Judgment verdict (T2/T3) | Block |
| Receipt ID | Deny |
| Parent receipt (root only) | Allow |

**Inheritance:** child ceiling ≤ parent ceiling; child constraints = parent ∪ spawn-time; child receipt must reference parent receipt.

Canonical source: `/root/AAA/federation/protocols/federation_envelope.yaml`

---

## Convergence V1 (gap + matrix + plan, 2026-08-07)

The federation crossed from **audit-only** into **enforcement-capable** on 2026-08-07, but is NOT yet **AAA-governed federation**.

| Harness | T3 enforcement | T2 enforcement | Spawn envelope | Receipt chain |
|---|---|---|---|---|
| OpenCode | ✅ (judge-gate.ts) | ✅ | ⚠️ task gated, no envelope | ❌ |
| Kimi | ✅ (K-02 exit 2) | ⚠️ witness only | ❌ | ❌ |
| Hermes | ✅ (K-02 hook) | ⚠️ witness only | ❌ | ❌ |
| OpenClaw | ❌ | ❌ | ❌ | ❌ |
| Codex | ⚠️ unverified | ⚠️ unverified | ❌ | ❌ |

**GAP-01 (Worst offender):** OpenClaw — live gateway, zero enforcement, zero receipt. Any Telegram mutation bypasses AAA entirely.
**GAP-05 (Cross-harness):** Three separate receipt formats, no shared envelope. Provenance chain breaks at every harness boundary.
**GAP-06 (Most dangerous long-term):** No harness propagates constraints to spawned children.

**Convergence plan (6 phases, dependency-ordered):**
1. Envelope canon (P0) ← DONE
2. OpenClaw gate (P1) ← design ready, wire pending F13
3. Judgment escalation K-03: T2→arif_judge (P2)
4. Spawn envelope inheritance K-04 (P3)
5. gate.disabled receipt (P4)
6. E-22 retest K-05 (P6)

Artifacts: `AAA_FEDERATION_GAP_REPORT.md`, `AAA_FEDERATION_ENFORCEMENT_MATRIX.md`, `AAA_FEDERATION_CONVERGENCE_PLAN.md`

---

## The Planes Model (Copilot insight, 2026-08-07)

```
MCP  = capability plane (what tools exist)
A2A  = communication plane (how agents talk)
AAA  = governance plane (whether actions are legitimate)
A-FORGE = execution plane (controlled mutation)
arifOS  = constitutional plane (final authority)
```

Agents federate **through the AAA Contract**, not through MCP/A2A. Transport is infrastructure; governance is architecture.

---

## Related references (under `references/`)

- `references/concurrent-canonical-write-incident-2026-08-07.md` — real F3b case: two agents wrote same contract to different paths simultaneously
- `references/f1-f15-failure-catalog.md` — full catalog with reproduction details
- `references/golden-test-receipt-templates.md` — copy-paste SCOUT/CRITIC/AUDITOR goal/context templates
- `references/audit-report-template.md` — template for `audit-YYYY-MM-DD.md`
- `references/2026-08-07-hermes-delegation-audit.md` — real Golden Test transcript (the one that produced F1-F15)