---
id: aia-cycle-operator
name: aia-cycle-operator
autonomy_tier: T1
version: 1.0.0
description: Use when operating or auditing the AIA 72h impian cycle.
owner: HERMES
risk_tier: medium
author: HERMES
license: MIT
knowledge_basis:
  language: true
  math: false
  physics: false
metadata:
  hermes:
    tags: [aia, impian, cron, governance, future-reflection, arifos]
    related_skills: [apex-judge, arifos-cron-ops, temporal-awareness]
---

# AIA Cycle Operator — Agentic Impian Architecture (72h)

## When to Use

- The `aia-72h` cron fired and its brief looks wrong, late, silent, or gate-violating.
- Auditing AIA receipts/proposals/quarantine/blindspots for any cycle date.
- The sovereign sends a new ritual/philosophy spec to be made governed + autonomous (use `references/activation-runbook.md`).
- Any question touching IMPIAN vs Dream (VVV) separation, the 222 layer, or the Triad of Governance.

AIA is the federation's future-reflection ritual: a **mode of Hermes** (`Hermes::IMPIAN`), layer **222** — the pre-deliberation horizon BEFORE AAA thinks (333), verifies (555), judges (888), forges (777), seals (999). It runs on cron `aia-72h` (every 72h), is **OBSERVE_ONLY**, and proposes — never builds. Live since 2026-08-15.

> Triad of Governance: **RRR** protects from false reality (hallucination). **AIA** protects from absence of future. **BLINDSPOTS** protects from invisible assumptions.

## Hard separation law (F13)

**Dream (VVV, 72h) = memory organization** (past → present). **Impian (AIA, 72h) = future imagination** (present → future). Same cadence number, different organs of thought. NEVER merge, never mix outputs, never store impian content in VVV or vice versa.

## Canonical map (source of truth = these files, not this skill)

- Doctrine: `/root/AAA/arifOS/RESOURCES/04_DOCTRINES/constrained_imagination.md` (formula, demons, Gödel-Future, triad)
- Policy: `/root/AAA/arifOS/RESOURCES/05_POLICIES/aia-72h.yaml` (OBSERVE_ONLY, max 3 proposals, ≤8-line brief)
- Workflow: `/root/AAA/arifOS/RESOURCES/08_WORKFLOWS/aia_72h_cycle.yaml` + `08_WORKFLOWS/aia/WORKFLOW.md`
- Receipts: `/root/AAA/arifOS/RESOURCES/10_RECEIPTS/AIA/<YYYY-MM-DD>/` (impian_receipt.yaml + future_skills.yaml)
- Quarantine: `/root/AAA/arifOS/RESOURCES/03_EUREKAS/FANTASIES/` — fantasy is quarantined, NEVER deleted
- Blindspots: `/root/AAA/arifOS/RESOURCES/03_EUREKAS/BLINDSPOTS/<date>.yaml` — ≥1 record per cycle, mandatory even with zero proposals
- Cycle driver (sibling-owned): `/root/AAA/arifOS/RESOURCES/forge_aia.py` (`test` subcommand = anti-fantasy suite)
- Cron: Hermes cron `aia-72h` (see `cronjob action=list`); delivers to Arif's DM; 90-day keep-or-kill review ~mid-Nov 2026

## The gate stack (check before believing any AIA output)

1. **Anti-Fantasy formula:** Reality + Scar + Gap + Trend = Impian. Missing reality_anchor OR scar/evidence → FANTASY quarantine.
2. **Goodhart:** success = `later_built` / `false_positive_rate` at 90-day review. Zero proposals is a HEALTHY cycle. Never count volume.
3. **Self-citation ban:** evidence = live probes, receipts, scars ONLY. Never AIA's own past FUTURE/FANTASIES files.
4. **The Line:** Future Reflection, never Future Desire. Every proposal traces to an institution/sovereign need.
5. **No-nagging:** REJECT/DEFER proposals return only with NEW evidence. Rejection is peace, not longing.
6. **Gödel-Future:** AIA dreams, never verifies its own proposals. Classification is advisory; ratification is 888/independent lane.
7. **Entropy budget:** every proposal carries entropy_cost / maintenance_cost / complexity_cost. Impian yang tak bayar bil = tanggungan.
8. **Devil's advocate:** every proposal answers "jika impian ini musnahkan arifOS, macam mana?"
9. **Founder-dependency test:** each cycle scans for capabilities living only in Arif's head → red = canonization priority, not new features.

## Operating procedure (audit / when a cycle looks wrong)

1. `cronjob action=list` — job enabled? last_status ok? next_run sane?
2. Verify receipts ON DISK under `10_RECEIPTS/AIA/<last-cycle-date>/` — **never trust the job's self-report alone**; read the yaml.
3. Check quarantine + blindspot files exist for the same date.
4. Run `python3 /root/AAA/arifOS/RESOURCES/forge_aia.py test` — anti-fantasy suite must be green.
5. If the brief violated a gate: fix the cron PROMPT (cronjob action=update), not the doctrine, unless the sovereign changed the doctrine.
6. Cron cycles write additive files only — receipts must NOT be git-committed by the cron itself.

## Extension procedure (sovereign sends a new spec/philosophy → make it a governed ritual)

Follow the sealed activation pattern (full runbook: `references/activation-runbook.md`):

1. **Substrate first** — doctrine/policy/workflow files in the RESOURCES taxonomy dirs; commit with evidence in the body.
2. **Phase-split** — kernel/constitution changes (floor table, Holy-8 loop limits) go to a separate 888/F13 session, not done unilaterally. Note them as "phase 2 pending".
3. **apex-judge gate** — `apex-judge isolate --doer HERMES --candidate "<claim>" -e <evidence.json> --pretty --human`; quote only independence_class, effective_verdict, session_id, call_hash.
4. **Cron create/update** — bounded prompt embedding the gates; deliver=origin; enabled_toolsets minimal.
5. **Test fire immediately** (`cronjob action=run`) so the sovereign sees real output same-day, then verify receipts on disk before reporting success.
6. **Report** with commit hashes + receipt paths; ringgit framing for cost.

## Pitfalls

- Sibling agents (AAA/OpenCode lanes) work concurrently in `/root/AAA` — uncommitted modified files may be THEIRS. Never commit their work-in-progress; verify their claims by re-running their tests instead.
- Spelling is constitution: **IMPIAN** (never "IMPAIAN"), **AIA = Agentic Impian Architecture** (never "Agent"), 222 is pre-deliberation layer (not an AAA member).
- Historical witness dirs stay immutable — on rename, leave the old dir with a README pointer, never rewrite old receipts.
- Briefs to Arif: Penang BM, ≤8 lines, no floor numbers, no jargon labels. "Tiada proposal layak" is a valid headline.
- Mid-turn out-of-band sovereign corrections (renames, separations) are applied IMMEDIATELY in the same working turn — git mv + doc patch + cron update, then continue.

## References

- `references/aia-governance-map.md` — full gate stack, sealed nomenclature rulings, maturity levels, phase-2 pending queue
- `references/activation-runbook.md` — the 2026-08-15 activation pattern generalized to any new governed ritual
