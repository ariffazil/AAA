# Repo Routing Policy — Amanah Rule

> **Authority**: AAA Space Invariants v2026.05.02  
> **Source**: https://github.com/ariffazil/AAA  
> **REPO trailer required**: Every commit must carry `REPO:`, `AGENT:`, `FLOORS:`, `WITNESS:` trailers

---

## Core Principle

Work lands in the correct repo or it does not land at all. The Amanah rule: routing confidence below 0.8 means stop, emit reason, ask Arif.

## Decision Tree

| If the change affects... | Route to... |
|---|---|
| Constitutional law, floors F1-F13, VAULT999, kernel routing | `arifOS` |
| Agent control plane, registries, schemas, A2A contracts, cockpit | `AAA` |
| Execution shell, orchestration, runtime glue, deployment | `A-FORGE` |
| Earth intelligence, seismic, petrophysics, GEOX tools | `GEOX` |
| Capital intelligence, NPV, IRR, EMV, financial flows | `WEALTH` |
| Human substrate, readiness, vitality, mirroring | `WELL` |
| Public websites, rendered surfaces | `arif-sites` |

## Confidence Threshold

**Routing confidence < 0.8 → STOP, emit reason, ask Arif.**

Never route faster than certainty.

## Cross-Repo Actions

- Proposer ≠ Approver for any high-risk change (GL-7)
- Any commit affecting multiple repos or deleting history requires explicit **888 HOLD** clearance
- APEX is the sole judge for holds — no agent may self-authorize overrides

## Commit Discipline

Agents may read, branch, commit, open PRs, run tests. Agents may **NOT** push to `main`, move repos, or delete history without explicit HOLD clearance.

## Required Commit Trailers

```
REPO: <target_repo>
AGENT: <agent_id>
FLOORS: F<01-13>,F<01-13>
WITNESS: {"human":<0|1>,"ai":<0|1>,"earth":<0|1>}
```

## Commit Trailer Examples

```
REPO: AAA
AGENT: hermes
FLOORS: F02,F11
WITNESS: {"human":1,"ai":1,"earth":0}
```

```
REPO: A-FORGE
AGENT: openclaw
FLOORS: F05
WITNESS: {"human":1,"ai":1,"earth":0}
```

```
REPO: arifOS
AGENT: apex
FLOORS: F01,F02,F03,F04,F05,F06,F07,F08,F09,F10,F11,F12,F13
WITNESS: {"human":1,"ai":1,"earth":0}
```

---

*DITEMPA BUKAN DIBERI — 999 SEAL ALIVE*
