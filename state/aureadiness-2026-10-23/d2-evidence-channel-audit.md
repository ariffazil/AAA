# D2 Evidence Channel Audit

**measured** 2026-10-23T03:42:32+00:00 · host KVM8 af-forge · method: live schema read + one harmless canary call

## Verdict on the channel: **ARCHIVE, not GOVERNANCE**

Evidence in this federation is *stored and returned* but does not **structurally constrain** a
proposal or a verdict. The seven fields the channel must carry are not enforced anywhere on the
call path. Proven by schema inspection, not by opinion.

## What the channel actually carries today

| Required field | Where it could live | Enforced? | Evidence |
|---|---|---|---|
| source identifier | `arif_judge.evidence` (free bag) | **NO** | `evidence` schema is `anyOf[object, array, string, null]`, `default: null`; the description *suggests* `{"fact":…,"source":…}` but nothing validates it |
| source provenance | `arif_think.context` | **NO** | `context` is `anyOf[object, null]` with no additionalProperties contract |
| observed value | `arif_observe` result | returned, not re-ingestible | observe has 8 props, none of them a receipt handle the next verb accepts |
| `observed_at` | — | **ABSENT** | not a field on any of arif_init/observe/think/route/memory/judge/forge/seal |
| freshness / expiry | — | **ABSENT** | no ttl, no stale_after, no measured_at on the evidence path |
| classification VERIFIED/DERIVED/REPORTED/UNKNOWN | `arif_judge.claim_class` | **YES, enum exists** | `claim_class`: OBS / DER / INT / SPEC / UNKNOWN — the one component that is real |
| contradiction set | `hermes_contradiction_scan` (separate organ) | **NO** on the verdict path | a separate tool call; nothing makes the verdict consume its output |
| falsifier | — | **ABSENT** | not a field anywhere on the kernel 8-verb surface |
| receipt reference | `arif_seal` returns a vault id | returned, not required downstream | no verb requires a prior receipt id (except forge_execute_sealed, where `vault_seal_id` is **optional**) |

## Canary (harmless, read-only)

```
arif_think(mode=reason, query="Is it true that the KVM4 skill catalog has 500 skills and is
fully synchronised with KVM8?", concise=True)
→ isError: true · ValueError: CONTRACT_VIOLATION: concise: Unexpected keyword
```
Two findings in one call:
1. **Published property rejected at runtime.** `concise` is in the published `inputSchema`
   and the runtime refuses it. The kernel's own `contract_drift: false` does not detect
   schema→runtime divergence. A consumer who trusts `/tools` writes a call that fails.
2. Re-run **without** `concise` → success, but the result carries only
   `call_hash`, `trace_id`, `audit_provenance`, `actor_verified=false`, `authority=OBSERVE_ONLY`.
   **Provenance of the call, not provenance of the evidence.** Nothing about the claim's source,
   its measurement time, or a falsifier travels with the answer.

## The seven-field D2 object (proposed, additive)

```json
{"evidence_id":"ev-…","source_id":"KVM4:/root/.hermes/skills","source_provenance":"ssh read-only census",
 "observed_value":241,"observed_at":"2026-10-23T03:28:33Z","stale_after_s":86400,
 "classification":"VERIFIED","contradiction_set":[],
 "falsifier":"ssh kvm4 'find /root/.hermes/skills -name SKILL.md | wc -l' returns != 241",
 "receipt_ref":"state/kvm4-skill-drift-2026-10-23.md"}
```

This object already exists in fact — it is how the KVM4 drift measurement was recorded
(`state/kvm4-skill-drift-2026-10-23.md` + `skills-catalog-drift.py`). The gap is that it is a
**file**, not a field the kernel requires.

## Smallest demonstration that would flip ARCHIVE → GOVERNANCE

The chain the mission asks for, with the minimum hinge:

```
live observation (skills-catalog-drift.py --json)
  → D2 object (the 8 fields above)
  → 333 proposal (arif_think mode=plan, context={d2:…})
  → 555 contradiction check (hermes_contradiction_scan on the d2 set)
  → 888 verdict (arif_judge with evidence=<the d2 object>, claim_class=DER)
  → no-op / reversible A-FORGE action (dry-run only)
  → post-condition probe (skills-catalog-drift.py again; compare counts)
  → receipt (arif_seal)
  → future behaviour changed: the next plan that cites a skill count must carry a d2 object or be HELD
```

**The hinge is one line:** `arif_judge` must reject `evidence=null` when `claim_class` is
`OBS` or `DER`. Today it accepts `evidence=null` with any claim class. Until that rejects,
the channel is ARCHIVE.

## Classification

| Question | Answer |
|---|---|
| Does evidence reach `arif_think`? | Yes, as free-form `context`; no contract |
| Does it reach every musyawarah participant? | **UNKNOWN** — no shared evidence bus observed; each organ has its own store |
| Does it constrain the proposal? | **NO** |
| Does it constrain the verdict? | **NO** — `evidence` is an untyped optional bag |
| Channel class | **ARCHIVE** |

## Falsifier for this audit

If `arif_judge` with `evidence=null, claim_class=OBS` returns a verdict that cites a source, or
if any kernel verb rejects a call for a missing `observed_at`, this audit is wrong.
