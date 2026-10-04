# Organ Placement Evaluation — FED/FLAME/FRAME (2026-08-11)

> Framework for evaluating ANY placement/coupling/consolidation scenario in the
> intelligence plane. Forged while scoring 4 scenarios for FED/FLAME/FRAME.
> Reuse for: "should we merge X into Y?", "should FRAME gate/look upstream?",
> "should FLAME be embedded in FED?" — any "where do these organs sit" question.

## The controlling principle: CHARTERED CEILINGS FIRST

Every organ has a **constitutionally chartered authority ceiling**, not a
convenient one. Any scenario that silently raises/lowers a ceiling is a
**de-facto F13 constitutional amendment**, not an ops change.

| Organ | Surface | Role | Ceiling |
|---|---|---|---|
| **FED** | fed_route :7074 → LiteLLM :4011/:4000 | Cognitive Allocator (which tier/provider/depth) | `777_FORGE` (ranked routes, never hard-blocks) |
| **FLAME** | flame_api :18901 | Free RM0 inference lane (classify/extract/summarise/embed) | `ADVISORY` (RM0, Zero-Fly-Zone, zero constitutional weight) |
| **FRAME** | frame-organ :18085 | Reference & Assessment Measurement Engine (baseline/probe/compare/trend/alert/report; reality-drift) | `OBSERVE_ONLY` / `ADVISORY_ONLY` (measures, never mutates, never adjudicates) |

**FRAME charter (from `/root/FRAME/README.md`):** "drift signal is observation,
not verdict." FRAME probes all 10 organs (ORGAN_PORTS in config.py: arifos 8088,
aforge 7071, geox 8081, wealth 18082, well 18083, aaa 3001, signal 18084,
arifflow 7073, fed 7074, flame 18901). It is NOT an MCP server, NOT an executor,
NOT a judge.

## The 4 canonical placement scenarios (design space)

- **A — Three Sibling Organs (status quo).** Independent peers on 127.0.0.1.
  FED routes to FLAME as a `$0.00` destination (`FLAME_PRICING`). FRAME probes all.
  No organ owns another. **Best constitutional fit, zero new blast radius.**
- **B — FRAME as measurement-governor (closed feedback loop).** FRAME drift signals
  mutate FED weights / FLAME tier order. **Tempting (only real self-correction) but
  breaks OBSERVE_ONLY → F13 amendment required.**
- **C — Merge FLAME into FED (single front-door).** **Rejected:** contradicts FED's
  own "don't merge lanes" doctrine; couples a disposable free lane to the load-bearing
  allocator (FLAME meltdown would take down 666/999 routing).
- **D — FRAME gate upstream (verify before trust).** **Rejected:** turns observer
  into blocking adjudicator; adds sync latency to every call; violates OBSERVE_ONLY + F4.

## Scoring axes (ranked by importance)

1. **Constitutional alignment** — ceilings intact? (controlling; a violation is
   disqualifying unless F13-amended)
2. **Authority separation** — least privilege between organs
3. **Operational risk / blast radius / F1 reversibility**
4. Closed-loop self-correction value (nice-to-have, may conflict with #1)
5. Auditability (F11), Security isolation (F12 / FLAME Zero-Fly-Zone), Cost/complexity

## Charter-safe upgrade pattern

Want the closed-loop insight WITHOUT granting mutation power? Add a **read-only
telemetry tap** from the observer (FRAME) to a human/judgment surface (FED / Arif /
arifOS) so drift reports are *surfaced for judgment*, never *applied by* the observer.
That closes the insight loop while preserving the observer's OBSERVE_ONLY identity.

## Live truth (2026-08-11)

All three healthy: FED :7074 `ADVISORY_ONLY, never judges/hard-blocks`; FLAME :18901
`RM0-TOOLS-FREELOOP, ADVISORY`; FRAME :18085 `total_organs:10 healthy:10 down:0` +
7 chambers active. `frame-organ.service` active 5d. Deliverable written to
`/root/forge_work/fed-flame-frame-placement-eval-2026-08-11.md`.