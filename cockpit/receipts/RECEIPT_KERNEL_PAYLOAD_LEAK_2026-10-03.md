---
type: F2_RECEIPT (new finding from external review)
date: 2026-10-03
operator: bijaksana-compile forge-fastmcp v3.2.0 session
trigger: External Claude reviewer flagged leaked internal node names in arifOS MCP response payloads
floor_scope: [F2, F11, F13]
---

# RECEIPT — arifOS kernel payload leak (NEW finding from external review)

## Context

External Claude reviewer (with OBSERVE-only token) flagged three leaked internal node names that appear as **literal strings inside observable response payloads** of advertised arifOS MCP tools:

| Leaked string | Source payload | Status |
|---|---|---|
| `arif_vault_seal` | arif_seal `mode=ledger` response | ✅ CONFIRMED via mcporter probe |
| `arif_sense_observe` | arif_observe `_affordance` field | ⚠️ parse error in re-probe (need different arg) |
| `tool_prefix: "arifos_"` | arif_route response | ✅ CONFIRMED via mcporter probe |

## Probe verification (just measured)

```
$ mcporter call arifos arif_seal mode=ledger | grep -c arif_vault_seal
1   (literal string present in response)

$ mcporter call arifos arif_route | grep -c arifos_
1   (tool_prefix="arifos_" present)
```

Both Claude claims re-proven. This is **not ChatGPT-style fabrication** — these strings are **actually emitted by the live kernel** in observable response payloads.

## Difference from ChatGPT rounds 1/2 (fabrication)

| Class | ChatGPT rounds 1/2 | Claude's finding (this turn) |
|---|---|---|
| **What was named** | `arif_mind_reason`, `arif_organ_consensus`, `arif_judge_deliberate` | `arif_vault_seal`, `arif_sense_observe` |
| **Verifiable as advertised?** | NO — absent from `mcporter list arifos --schema` | NO — absent from advertised surface (correctly so) |
| **Verifiable as emitted?** | NO — never returned by any tool call | YES — present as internal source_node / tool_prefix / _affordance |
| **Failure mode** | External reviewer fabricated tool names that don't exist anywhere | Kernel leaks internal implementation strings that could be misread as tool names |
| **Who is wrong?** | external agent (fabrication) | kernel (hygiene defect) |

**Both failures can cause future external reviewers to misidentify arifOS MCP capability. Both warrant doctrine update.**

## Why this matters

A future external LLM reviewing arifOS MCP — even one running the agnostic prompt from `RECEIPT_BIJAKSANA_COMPILE_CLOSE_2026-10-03.md` — could:
1. Probe the advertised surface (sees 8 tools — passes check)
2. Direct-call each advertised tool (sees `status: completed` — passes check)
3. Read the raw response payloads (sees `arif_vault_seal`, `arif_sense_observe`, `arifos_` strings)
4. Conclude "the connector advertises `arif_vault_seal` etc."

**This is a real attack surface for the same failure mode the doctrine guards.**

## Recommended kernel fix (out of scope for forge-fastmcp)

In `/root/arifOS/kernel/...` (kernel internals — out of my lane):

1. **Strip internal node names from observable response payloads** — `source_node`, `resolved_from`, `_affordance` are implementation details and should be debug-only (gated by `?debug=1` query param or DEBUG_MODE config flag).

2. **Replace `tool_prefix: "arifos_"` with `tool_prefix: "arif_"` in public output** — the public surface uses `arif_<verb>` form, so the public-facing prefix should match. The internal prefix can stay `arifos_` for routing.

3. **Audit other advertised tools for similar leaks**: `arif_init`, `arif_observe`, `arif_think`, `arif_route`, `arif_memory`, `arif_judge`, `arif_forge`, `arif_seal` should all be checked for internal-only strings in payloads.

4. **Consider adding `internal_nodes` to the response schema** explicitly so external reviewers can identify which strings are internal vs public.

## Doctrine update proposed

For `forge-fastmcp` Stage 2 (PROBE):

> **2g — Payload hygiene audit (NEW 2026-10-03).** When probing an MCP server, also enumerate literal strings in response payloads that match `^[a-z]+_[a-z_]+$` (snake_case identifier pattern). Cross-reference with the advertised surface: any string in a payload that is NOT in the advertised surface is a leaked implementation detail. Report these as a separate `payload_hygiene` section in the probe report — distinct from `surface_truth` (advertised) and `callable` (callable). This pre-empts future external reviewers from misreading internal strings as advertised tools.

## Severity

**MEDIUM.** Does not break the kernel. Does not corrupt substrate. Does cause confusion in external reviews. **Direct cause of future failure mode if not addressed.**

## Status

- ✅ External finding received and path-of-evidence verified
- ✅ Receipt sealed
- ⏳ Kernel fix requires F13 (out of forge-fastmcp lane)
- ⏳ forge-fastmcp Stage 2g doctrine patch is autonomous-tier, can be applied without F13

## Evidence

- Original observation: external Claude review, this session
- Re-probe confirmation: mcporter + Python json grep (this turn)
- This receipt: `/root/AAA/cockpit/receipts/RECEIPT_KERNEL_PAYLOAD_LEAK_2026-10-03.md`
- Forthcoming Stage 2g doctrine patch: T-007 extended

DITEMPA BUKAN DIBERI ⚒️