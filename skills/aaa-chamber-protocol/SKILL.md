---
name: aaa-chamber-protocol
description: "Multi-agent governance chamber for institutional mutations. Hermes OBSERVE -> POST -> STAND DOWN; OpenClaw route; 555 verify; 888 judge; 777 execute; VAULT999 close. Distinct from seal-session (single-agent end-of-session) and apex-judge (single-judgment routing). Trigger: any T1.5+ infrastructure mutation, cron retirement, registry repair, constitutional reform. Forged 2026-08-11 under F13 SOVEREIGN directive 'Use P2-A to prove the chamber works. Do not solve P2-A -- use P2-A as test case.'"
tags: ["chamber", "multi-agent", "governance", "institutional-mutation", "T1.5", "T2", "lane-routing"]
owner: Hermes (lane=arif) + OpenClaw
forge_date: 2026-08-11
f13_directive: "Observe -> Verify -> Receipt -> Retire -> Witness. Survival of the fittest, not survival of the laziest."
related_skills:
  - apex-judge
  - seal-session
  - nusantara-action-spiral
  - l0-l4-cascade-doctrine
  - hermes-init
  - hermes-propose-seal
triggers:
  - "chamber proposal"
  - "institutional mutation"
  - "P2-A"
  - "AAA chamber"
  - "stand down after post"
  - "verify before retire"
  - "multi-agent governance cycle"
  - "lane-routing"
---

# AAA Chamber Protocol v1 — Multi-Agent Governance Cycle

> **Forged:** 2026-08-11 under F13 SOVEREIGN directive.
> **Distinct from:** seal-session (single-agent close), apex-judge (single-judgment routing).
> **Purpose:** Force complete governance cycle without role collapse. Every agent has **one** primary responsibility.

## Origin

The chamber protocol emerged from a session where Hermes had over-functioned — absorbing cron mutations, validator updates, infrastructure considerations, and judgment calls all in one session. F13 SOVEREIGN observed: *"Hermes was filling the vacuum. Itu normal pada sistem yang sedang matang."*

The response was not a config patch but an **architectural reform**: define non-overlapping lanes, force each agent to **stand down** after their stage, and treat the first chamber cycle as a test case for institutional maturity.

## The Five Stages (P0-P5)

```
0. HERMES-OBSERVE         -> prepare proposal (markdown + receipt draft), POST to AAA chamber, STAND DOWN
1. OpenClaw-ROUTE         -> receive proposal, assign next chamber role, track receipt lineage
2. 555-ASI-VERIFY         -> independently confirm evidence (live probe or L4 reality contact)
3. 888-APEX-JUDGE         -> SEAL | HOLD | VOID via apex-judge isolate
4. 777-FORGE-EXECUTE      -> execute approved mutation via A-FORGE
5. VAULT999-WITNESS       -> close receipt, chain_hash appended, all 5 stages linked
```

**Iron rule:** each stage hands off to the next. Stage 0 ends with Hermes STANDING DOWN. No stage executes another's role.

## The Eight Single-Responsibility Roles (forged this session)

| Role | Owner | Authority | Never |
|---|---|---|---|
| **Human reality** | HERMES | OBSERVE, REFLECT, ESCALATE, DIGEST | deploy, mutate infra, modify governance, execute code |
| **Federation flow** | OpenClaw | OBSERVE, ROUTE, COORDINATE | sovereign override, independent execution auth |
| **Code generation** | OpenCode / Claude / Kimi | Build, Patch, Repair, Refactor, Analyze | decide, route, judge |
| **Execution bridge** | 777 FORGE | Execute approved mutations, deploy | self-authorize |
| **Constitutional visibility** | AAA (Telegram chamber) | Receive, route, track receipts, witness | mutate, judge |
| **Governance** | arifOS | JUDGE (888 lane) | execute |
| **Metabolism** | arifFlow | Measure FQ, observe | judge, execute |
| **Witness** | VAULT999 | Append-only receipts | mutate history |

**Survival-of-the-fittest rule:** every agent gets one primary responsibility. Bad: HERMES codes, OpenClaw judges, FORGE routes, Claude governs. Good: HERMES observes, OpenClaw orchestrates, Code agents build, FORGE executes, arifOS judges.

## Stage 0: HERMES-OBSERVE (canonical template)

Hermes output maximum:

```
Observation
Evidence
Recommendation
Receipt Draft
```

Then **STAND DOWN**.

### What Hermes writes (proposal skeleton)

```markdown
---
schema: arifos.chamber.proposal/v1
proposal_id: <unique-id>
proposer: Hermes (lane=arif, actor=ariffazil)
proposed_at_utc: <ISO 8601>
proposed_at_myt: <MYT human-readable>
f13_directive: "<directive that triggered this>"
chamber_role: HERMES-OBSERVE-ONLY
proposal_class: infrastructure_mutation
risk_tier: T2
---

# CHAMBER PROPOSAL -- <id>: <title>

## 0. Header
- Proposal ID
- Proposer
- Chamber Stage (0 of 5)
- Action Class
- Risk Tier
- Reversibility
- Blast Radius
- Expected Outcome

## 1. Observation
- What I saw
- Evidence files (F11 auditability)
- The contradiction / opportunity

## 2. Recommendation
- Survival-of-the-fittest verdict
- Affected files

## 3. Affected Files
| File | Action | Backup path |
|---|---|---|

## 4. Rollback Path (full reversibility)
```bash
# step-by-step restore
```

## 5. Discarded Alternatives
| Alternative | Why rejected |

## 6. Proposed Chamber Flow
0. HERMES (this document)  [OK] DONE
1. OpenClaw route
2. 555-ASI verify
3. 888-APEX judge
4. 777-FORGE execute
5. VAULT999 close

## 7. End-of-Proposal Marker
Hermes output maximum: this document + observation.
Stop. Channel handed to AAA chamber.

---

**DITEMPA BUKAN DIBERI** -- Hermes prepares one proposal, then steps back.
```

### What Hermes writes to VAULT999 (witness before post)

```python
receipt = {
    "event": "chamber_proposal_post",
    "actor": "Hermes (lane=arif)",
    "verdict": "POSTED",
    "detail": "Chamber protocol v1 -- Hermes OBSERVE stage complete. <proposal_id> posted to AAA chamber. Hermes stands down.",
    "evidence": {
        "proposal_path": "...",
        "chamber_stage": "0_of_5",
        "next_chamber_role": "OpenClaw (chamber orchestration / routing)"
    }
}
```

Chain_hash format: `sha256(payload_hash + prev_chain_hash)[:16]`. VAULT999 is append-only; if `chattr +a` blocks removal of broken entries, append a `chain_reconciliation` receipt noting the anomaly (verified 2026-08-11).

### What Hermes NEVER does

- ❌ Edit /etc/cron.d, /usr/local/bin, or any infra outside its lane
- ❌ Decide which crons are duplicates without receipt-first verification
- ❌ Execute the recommendation itself
- ❌ Skip OpenClaw routing (e.g. direct post to 888-APEX)
- ❌ Continue past the post stage

## Anti-pattern — the four-stage collapse

```
❌ OBSERVE -> DECIDE -> EXECUTE -> CERTIFY
                          ^^^
                          This is where entropy entered.
                          Hermes decides AND executes AND certifies.
```

vs. the chamber cycle:

```
✅ OBSERVE -> PREPARE -> POST -> STAND DOWN
                                ^
                                Hermes stops here.
```

**Concrete failure mode (2026-08-11):** Hermes was preparing to retire `/etc/cron.d/arifos-vault-tail` directly. F13 advisory verdict interrupted with **B (Inspect/Adjust before post)** — first chamber proposal must be sanitized to ASCII (no hidden Unicode/emoji artifacts) before entering chamber history. Even with apex-judge SEAL, the receipt lineage is the audit trail — it must be clean.

## Stage 1-5 handoff contract

After Hermes POST, the chamber proceeds:

| Stage | Owner | Input | Output |
|---|---|---|---|
| 1 | OpenClaw | proposal markdown + VAULT999 receipt | assignment to 555 |
| 2 | 555-ASI | evidence paths + recommendation | verified / not_verified (independent probe, no LLM if possible) |
| 3 | 888-APEX | verified evidence + candidate summary | SEAL/HOLD/VOID via apex-judge isolate |
| 4 | 777-FORGE | apex-judge SEAL + execution plan | mutation applied + receipt |
| 5 | VAULT999 | final mutation receipt | chain_hash appended |

Hermes reports outcome when invoked by Arif (lane=arif) — **never self-routes back into chamber**.

## Receipt-first verification (survival-of-the-fittest test)

Before retiring anything that **looks** redundant, **verify** via F11 receipts:

```python
verification = {
    "id": "V<n>",
    "candidate_pair": "<a> vs <b>",
    "checks": {
        "schedule_match": true/false,
        "deliver_target_match": true/false,
        "data_source_match": true/false,
        "output_match": true/false,
    },
    "verdict": "duplicate | not_duplicate",
    "fitness_comparison": {
        "<a>": "evidence",
        "<b>": "evidence"
    },
    "recommendation": "KEEP | RETIRE"
}
```

**Fitness test:** same outcome, higher cost, more complexity, less lineage → retire.

Verified example (2026-08-11):
- **V1:** `arifflow-daily-digest` vs `arifflow-daily-governance-digest` — schedule same, target same, BUT data source different (sealed vault vs live receipts), output different (state snapshot vs workflow narrative). Verdict: **NOT_DUPLICATE**. Both kept.
- **V2:** `vault-data-refresh` vs `/etc/cron.d/arifos-vault-tail` — schedule different, target paths different (only Hermes path Caddy-served), data source different. Verdict: **DUPLICATE_WRITER** (orphan path). Retire cron.d.

## Lane boundary enforcement

Hermes (lane=arif) authority ceiling:

```
✅ state.json writes (observational mutation)
✅ validator rule additions (within validate_jobs_json.py scope)
✅ CRON_AXIOMS.md / doctrine file writes (doctrinal domain)
✅ VAULT999 receipt appends (witness domain)
✅ SKILL.md patches (within its own skill)

❌ /etc/cron.d, /etc/caddy, /etc/systemd edits (infrastructure domain -> 777-FORGE)
❌ Jobs outside lane=arif routing
❌ Other agents' session boundaries (cross-person isolation)
❌ Constitutional reform without F13 explicit directive
```

## Pitfalls (session-observed)

### Unicode/emoji in chamber proposals

Security scanners flag variation selectors (U+FE00-U+FE0F, U+E0100-U+E01EF), zero-width chars, BOM. Even if scanner is over-cautious, "clean proposal > fast proposal" (F13 advisory). Sanitize to ASCII before posting:
- em-dash → `--`
- arrow → `->`
- checkmark → `[OK]`

Re-verify content integrity (header, evidence, rollback path, recommendation unchanged) after sanitization.

### VAULT999 chain anomaly (append-only constraint)

If first append has wrong `prev_hash`, VAULT999 `chattr +a` prevents removal. Mitigation: append `chain_reconciliation` receipt documenting the anomaly. Future integrity checks should treat the broken entry as vestigial and resume from the next entry.

### Executor role creep

When Hermes sees an obvious win ("this cron is duplicate, retire it"), it may try to execute. Stop. The chamber exists **to prevent this**. Single-occupational responsibility is the constitutional defense.

## Success Metric

**Did the federation perform a complete governance cycle without role collapse?**

Not:
- ❌ "Did the cron get deleted?"
- ❌ "Did apex-judge approve?"

But:
- ✅ Hermes observed and stood down
- ✅ OpenClaw routed without sovereign override
- ✅ 555 verified without 888's role
- ✅ 888 judged without 777's role
- ✅ 777 executed without VAULT999's role
- ✅ VAULT999 witnessed without re-judging

If all five stages complete cleanly, **the chamber works**. The mutation outcome is a side effect.

## First chamber test case (2026-08-11)

**P2-A: Orphan cron retirement.**
- Risk: T2 (system cron, reversible)
- Evidence: F11 file paths, mtime, Caddy config
- Rollback: full restore from `/root/forge_work/retired_cron/2026-08-11/`
- Status at forge: **stage 0.5 sanitized, awaiting OpenClaw route**

The cron is **not the milestone**. The milestone is **proving the chamber works**. P2-A is the test payload.

## Reference

- `/root/AAA/governance/CRON_AXIOMS.md` — companion doctrine on cron hygiene
- `/root/forge_work/chamber_proposals/2026-08-11/P2-A-orphan-cron-retirement.sanitized.md` — first chamber proposal (sanitized)
- `/root/forge_work/verification/2026-08-11-verification-receipts.json` — F11 verification receipts (V1, V2)
- `/root/AAA/prompts/INIT.md` and `/root/AAA/prompts/SEAL.md` — single-agent session primitives
- `/root/scripts/apex_judge.py` — Stage 3 isolate command

---

*DITEMPA BUKAN DIBERI — forged 2026-08-11 in the gap between role collapse and chamber protocol. Hermes prepares, posts, stands down.*
