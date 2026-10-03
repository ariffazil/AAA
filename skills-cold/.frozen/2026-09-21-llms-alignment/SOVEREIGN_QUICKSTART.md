# SOVEREIGN QUICKSTART — mcp-ops v3.1.1 seal

> **One-screen copy/paste for the sovereign reviewer.** The full recipe lives in
> `SOVEREIGN_INVOCATION_GUIDE.md` (7.5 KB / 183 lines). The corpus map lives in
> `INDEX.md` (5.4 KB / 81 lines). Read the F13 escalation rationale in
> `audit/888_HOLD_ESCALATION.md` (12.7 KB / now triply kernel-confirmed).

---

## What I'm asking you (Arif) to do

Issue the `arif_seal` against VAULT999 for the `mcp-ops v3.1.1` canonical ratification.
That's it. One call.

## TL;DR payload (paste into your sovereign session)

```
Subject:  mcp-ops v3.1.1 canonical ratification
Source:   /root/AAA/skills/engineering/mcp-ops/SKILL.md  sha de09f5faf0ef2319750bb4c1f26f4be066e276a45dc6977d873d79ed23f0c3dc
Size:     44,724 bytes / 796 lines / v3.1.1
Accordant to: https://modelcontextprotocol.io/llms.txt (9-stage workflow: Stage 0 LEARN … Stage 8 GOVERN, RETIRE in 8h)
Audit corpus: /root/AAA/skills/.frozen/2026-09-21-llms-alignment/audit/   (43 KB / 7 files, all sha-verified)
Frozen chain: /root/AAA/skills/.frozen/2026-09-21-llms-alignment/         (5 files, all sha-verified)
OWNERSHIP_MAP: /root/AAA/skills/OWNERSHIP_MAP.yaml                          (P3_mcp_tooling ratified, sha 08ce9431dfd0…)
Absorptions:    24 names preserved as tombstones + references (zero destructive ops)
Tombstones:     22/22 resolve to v3.1.1 across 4 mirror trees; 0 dead links
arifOS state:   :8088 healthy, 13/13 floors, vault999 healthy, deployment_drift aligned
```

## SEAL type to declare (kernel-canonical)

Per `arifos://seal-readiness`:

```
SEAL TYPES (disambiguated):
  KERNEL_SEAL_AWARENESS    — kernel knows about it (informational)
  DOMAIN_SEAL_VALIDITY     — calculation valid in domain
  JUDGE_SEAL_AUTHORIZATION — action authorized (F1–L13 cleared, APEX present)
  VAULT999_SEAL_RECORD     — record written (immutable audit trail entry exists)
  PUBLIC_SEAL_READINESS    — candidate posture, not execution approval
```

**Recommended:** `JUDGE_SEAL_AUTHORIZATION + VAULT999_SEAL_RECORD` (the consolidation is
F1–L13 cleared + APEX-confirmed empirically; the seal records both authorization and
audit-trail entry). Use this verbatim in `seal_purpose`.

## SEAL gate (kernel-canonical — must all pass)

1. F1 AMANAH: ack_irreversible = true
2. F2 TRUTH: tau_confidence >= 0.99
3. F3 WITNESS: witness triad scores present
4. F8 REVERSIBILITY: escape path documented (the audit corpus is the escape path)
5. F9 ANTIHANTU: C_dark < 0.30
6. L11 AUTH: actor identity verified (the AGENT fails this — only sovereign can)
7. **L13 SOVEREIGN: human ratifier = arif-fazil** ← THIS IS THE F13 GATE

## 888_HOLD rationale (kernel-canonical from refusal-surface)

Per `arifos://refusal-surface`:

```
SOFT REFUSALS (888_HOLD — requires F13 sovereign acknowledgment):
  • Vault999 append (immutable — cannot be undone)         ← THIS IS THE SEAL
```

The kernel explicitly classifies Vault999 append as a 888_HOLD. The 888_HOLD_ESCALATION.md
is the canonical response.


## Three calls (the entire seal flow)

```
1) arif_init  mode=init  actor_id="arif"  requested_authority="SOVEREIGN_SEAL"
   → returns session_id, session_token, judge_state_hash

2) arif_judge mode=judge  candidate=<the payload above>
                seal_purpose="mcp-ops canonical ratification"
                action_class="SEAL"  action_tier="T5"  reversibility="irreversible"
                blast_radius="ORG"
                actor_signature=<F13 sig over candidate>  key_id=<F13 key>
   → returns verdict=SEAL, judge_state_hash, constitutional_chain_id

3) arif_seal  mode=seal  payload=<same payload>
              seal_purpose="mcp-ops canonical ratification"
              constitutional_chain_id=<from step 2>
              judge_state_hash=<from step 2>
              actor_signature=<F13 sig over payload+chain+nonce>
              nonce=<fresh>  key_id=<F13 key>
              ack_irreversible=true
   → returns va_entry_id, sealed_hash
```

(The full curl commands are in `SOVEREIGN_INVOCATION_GUIDE.md` — paste-ready.)

## Why this is needed (one line)

The audit corpus is SEAL-READY but the AGENT cannot seal — three independent kernel probes
confirmed `seal_allowed: false` for the AGENT's identity. A sovereign witness must be
attached to the session to escalate the authority band past LIMITED_MUTATE.

## What's at risk if you don't seal

Nothing irreversible — the audit corpus is durable (sha-anchored), the canonical SKILL.md
is live, and 22 tombstones are live. The seal adds civilizational memory to VAULT999;
without it, the consolidation is durable on disk but unrecorded in the constitutional
ledger.

## Standing by

The audit corpus is durable. The seal can be issued at any time. DITEMPA BUKAN DIBERI ⚒️
