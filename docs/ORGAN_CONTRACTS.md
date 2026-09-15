# ORGAN CONTRACTS — what each organ may and may not do

> **Status: DRAFT_AWAITING_F13.** This is an evidence-derived draft, not canon.
> It declares no new authority; it transcribes authority values that organs
> already publish about themselves, plus rules already written in
> `/root/AGENTS.md` and `/root/AAA/instructions/`. Where an organ's published
> ceiling and the doctrine disagree, the disagreement is recorded here rather
> than resolved.
>
> Drafted 2026-09-15 UTC from live probes. Regenerate the underlying evidence
> with `/opt/arifos/venv/bin/python /root/scripts/federation_topology_gen.py`.
> Companion map: `/root/AAA/docs/FEDERATION_TOPOLOGY.md`.
>
> **Provenance tags:** `OBSERVED` = read from the organ's own live `/health`
> this session · `DOCTRINE` = stated in AGENTS.md / an instruction fragment ·
> `INFERRED` = not published anywhere; my reading of observed behaviour, and
> the weakest class of claim in this document.

## The one rule that applies to every organ

`DOCTRINE` — Constraint > Intelligence · Reality > Narrative ·
Capability ≠ Authority. An organ having a capability is never evidence that it
holds the authority to use it. Authority is granted by the kernel, scoped by
ceiling, and proven by a receipt — not by the presence of a tool.

---

## arifOS kernel — port 8088

| | |
|---|---|
| **Published authority** | `SOVEREIGN` · `OBSERVED` |
| **Role** | Constitutional core. Holds F1–F13, judges, seals. |
| **MCP surface** | 8 public tools: `arif_init, arif_observe, arif_think, arif_route, arif_memory, arif_judge, arif_forge, arif_seal` · `OBSERVED` |
| **Declared state** | `healthy`, `degraded_reasons: []`, `owner_summary: GREEN` · `OBSERVED` |

**CAN:** judge and route any claim; write the seal (`arif_seal`) to VAULT999 —
and *only* the kernel may write it; issue HOLD; hold the registry of tools and
floors.

**MUST NOT:** execute a production mutation itself — it hands that to A-FORGE
under ceiling. Must not treat a capability report from an organ as a verified
fact (F2: an organ's self-report is a claim, not a receipt).

**Routes to A-FORGE:** any mutation. **Seals:** VAULT999. **Receives:** candidate
verdicts from every organ, evidence from GEOX, readiness advice from WELL.

**Open issues:** `se_stage: 000` with `law: advance_only_on_proof_bundle` —
the stage has never advanced. `rasa_derita` schema is loaded and VALID but the
module status is `888_HOLD` with `enforcement_mode: PARTIAL_CODEPATH`.
`execution_readiness: held`. `feed_federation_healthy: false` —
`last_fallback_reason: FED_FEDERATION_UNREACHABLE`: the kernel cannot currently
reach FED, its own primary provider lane. · `OBSERVED`

---

## A-FORGE — port 7072 (HTTP) + stdio MCP

| | |
|---|---|
| **Published authority** | `777_FORGE` · `OBSERVED` |
| **Role** | Execution actuator. The only organ that mutates production state. |
| **MCP surface** | 126 tools · `OBSERVED` |
| **Declared state** | `healthy`, commit `f444b79e` · `OBSERVED` |

**CAN:** execute, build, deploy, write files, run shell, open PRs — *after*
obtaining a judgement. Act as the hands of the federation.

**MUST NOT:** decide its own authority. A-FORGE does not judge itself; it
receives a verdict (`forge_judge_proxy`, `forge_check_governance`) and then
acts. It must not seal to VAULT999 — the arifOS Operating Chain is explicit
that only `arif_seal` writes there. `DOCTRINE`

**Routes to kernel:** every action needing judgement. **Seals:** nothing;
it produces receipts, not seals.

**Open issue:** 126 tools is a measured attention cost — every session that
loads the A-FORGE server pays for all 126 schemas. · `OBSERVED`

---

## FED — port 7074

| | |
|---|---|
| **Published authority** | `ADVISORY_ONLY`, `class: route_advisor` · `OBSERVED` |
| **Self-description** | "never judges, never hard-blocks" · `OBSERVED` |
| **MCP surface** | 7 tools: `fed_route, fed_status, fed_probe, fed_contrast, fed_health, fed_classify, fed_report_latency` · `OBSERVED` |

**CAN:** classify an inference workload, advise a route, measure latency,
report its own health.

**MUST NOT:** block, judge, or hold. A FED verdict is advice; the kernel judges.

**Status note:** the kernel reports FED unreachable while FED's own `/health`
answers `healthy` on this host. Both are true from their own vantage — a
reachability fault is direction-specific and must be diagnosed as such, not
declared as "FED down". · `OBSERVED`

---

## GEOX — port 8081

| | |
|---|---|
| **Published authority** | `555_COMPUTE_ONLY` · `OBSERVED` |
| **Role** | Earth reasoning / evidence producer. |
| **MCP surface** | 31 tools (`geox_*`) · `OBSERVED` |
| **Declared state** | `healthy`, `kernel_verdict: SEAL`, profile `full` · `OBSERVED` |

**CAN:** compute, ingest wells and seismic, produce claims with provenance.

**MUST NOT:** allocate anything real, or self-certify a domain claim. GEOX
produces evidence; the kernel judges it. `INFERRED` from `555_COMPUTE_ONLY`.

**Routes to kernel:** claims for judgement. **Seals:** nothing directly.

---

## WEALTH — port 18082

| | |
|---|---|
| **Published authority** | `555_COMPUTE_ONLY` · `OBSERVED` |
| **Role** | Capital intelligence / computation engine. |
| **MCP surface** | 11 tools (`capital_*`, `wealth_judge_handoff`) · `OBSERVED` |
| **Declared state** | `healthy`, version `v2026.07.24` · `OBSERVED` |

**CAN:** compute ratios, diagnose a balance sheet, backtest, keep a capital
ledger, hand a verdict to the kernel.

**MUST NOT:** allocate or move capital, or give advice. It computes; a human
decides. Presence of `wealth_judge_handoff` shows the intended path is hand-off,
not decision. `INFERRED` from the tool name + `555_COMPUTE_ONLY`.

**Port hazard:** the deployment briefs have cited WEALTH at `:4000`. Port 4000
on this host is Langfuse, and the kernel reports `langfuse_tracing: NOT_WIRED`.
WEALTH is `:18082`. Any document saying otherwise is wrong. · `OBSERVED`

---

## WELL — port 18083

| | |
|---|---|
| **Published authority** | `REFLECT_ONLY` · `OBSERVED` |
| **Role** | Human readiness — body, fatigue, dignity. |
| **MCP surface** | 31 tools (`well_*`) · `OBSERVED` |
| **Declared state** | `degraded` · `OBSERVED` |

**CAN:** log intake / recovery / substance, observe machine and federation
thermal state, propose a governance signal, attest to the kernel, render a HUD.

**MUST NOT:** judge a human, or decide a person's state for them. There is
`well_guard_dignity` and `well_consent_audit` in the surface — the organ is
built so that the human's consent scopes what it may look at. WELL proposes;
the human and the kernel decide. `DOCTRINE` (relationship kernel, sanctuary
invariant).

**Repair path exists and is part of the contract:** `well_check_repair` ·
`OBSERVED`. Degraded is a state to be repaired, not hidden.

---

## AAA — daemon :3001, MCP on :3001/mcp (not wired)

| | |
|---|---|
| **Published authority** | `DISPLAY_ONLY` · `OBSERVED` |
| **Role** | Doctrine layer / intelligence routing. Skills + governance. |
| **MCP surface** | daemon healthy; its MCP server (`aaa_mcp_fastmcp.py`) is live but **not wired into Hermes or 1mcp** · `OBSERVED` |
| **Tools it defines** | `aaa_health, aaa_agent_card, aaa_federation_manifest, aaa_discovery` · `DOCTRINE` (source of the server) |

**CAN:** show state, aggregate organ cards, queue A2A, define floors and
doctrine, hold skills.

**MUST NOT:** judge, execute, or write VAULT999. Stated verbatim in the server's
own module docstring — the strongest form of a contract, because it is in the
code. `OBSERVED`

**Open issue:** an organ whose entire purpose is visibility is itself
invisible. Wiring it is a one-line fix with no authority change. · `OBSERVED`

---

## FRAME — port 18085

| | |
|---|---|
| **Published authority** | observer; `chambers: baseline/probe/compare/trend/alert` active · `OBSERVED` |
| **Role** | Independent observer. Baseline established 2026-08-06. |
| **MCP surface** | `/health` answers `ok`; the MCP client handshake on `/mcp` fails · `OBSERVED` |

**CAN:** observe, baseline, compare, trend, alert.

**MUST NOT:** act, fix, or judge. Its output is *evidence, never a verdict* —
stated in `/root/AGENTS.md`. An observer that intervenes stops being an
independent observer.

**Open issue:** if FRAME's MCP endpoint is genuinely not serving, the federation
is running without its independent observer's data feed even though the observer
process is alive. Needs a real endpoint check, not an assumption. · `OBSERVED`

---

## VAULT999

| | |
|---|---|
| **Published role** | Immutable ledger, seal chain + hash · `DOCTRINE` |
| **Kernel reports** | `vault999_health: healthy`, sealer breaker `closed`, 0 recent failures · `OBSERVED` |

**CAN:** accept a seal from `arif_seal` only.

**MUST NOT:** accept a write from any other organ, from an agent, or from a
session. Never store a secret value. `DOCTRINE` (vault999-writer-discipline)

---

## Cross-organ rules that no single organ owns

1. **Only the kernel seals.** `DOCTRINE`
2. **Only A-FORGE mutates.** `DOCTRINE`
3. **No organ judges itself.** A self-report is a claim; a receipt is evidence. `DOCTRINE` (F2)
4. **Capability is not authority.** A tool existing on a wire grants nothing. `DOCTRINE`
5. **A refusal to act must be recorded, not silently skipped.** A guard that
   blocks without a trace is indistinguishable from a guard that is absent. `INFERRED`
6. **Observation must not be paid for by the observed.** Any organ that watches
   a human owes that human a stated scope. `DOCTRINE` (sanctuary invariant)

---

## What this document does NOT yet cover

- Absolute lifecycles: which organ may start, restart or retire another.
- Blast radius: what an organ may break before it must stop.
- The human-facing contract — what any organ owes Arif specifically.
- Enforcement: nothing here is machine-checked. These are written rules, and a
  written rule is only as strong as the check behind it.

Listed as gaps on purpose: a contract document that quietly omits its own
enforcement gap is worse than none.

---

*Forged by i-ARIF (Hermes edge bridge) under F13 sovereign direction.*
*DITEMPA BUKAN DIBERI.*
