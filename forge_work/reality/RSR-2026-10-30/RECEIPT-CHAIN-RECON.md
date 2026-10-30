# RECEIPT-CHAIN-RECON.md — kernel receipt chain "gaps-found" diagnosed with receipts
2026-10-30 ~09:30 MYT, KVM8. Read-only. New probe + existing canon.

## New kernel facts (probe this session, canonical vault replay [PROBE])

- Kernel deployed commit NOW = 84efcec (2026-10-30 09:19 MYT, 2 commits after my
  Phase-0 measurement of 93437e3 at 08:45). Kernel was UPDATED mid-session by another
  actor. Commit message: "kernel: HTTP envelope keeps model_governance (built-then-
  dropped class closed — card joins _SEMANTIC_PRESERVED_FIELDS; trim[minimal] proven
  to preserve card with byte-identical hash in-process)". Working tree clean (0 dirty).
  → paste's "deployed commit 84efcec47 not stated in response" RESOLVED: it is the
  CURRENT deployed identity, newer than every earlier probe in this session.
  One-actor assumption on this host: wrong (third same-session precedent).
- model_governance: my fresh canary [PROBE] also lacks the field, BUT commit 84efcec
  message states the fix preserves the card under verbosity trim=minimal and proves
  byte-identical hash in-process. My canary used default verbosity (no trim=minimal
  arg) and still no card on MCP surface → discrepancy: fix claimed in commit vs card
  absent on MCP canary path. POSSIBLE explanations: fix lives on REST envelope path
  only; or MCP surface needs verbosity arg; or deploy did not pick it up (service
  restart timing unknown). UNRESOLVED — one discriminating read: compare REST path
  response vs MCP response on same canary (deferred, probe-stop).

## Receipt chain: gaps-found diagnosed (not just accepted)

canary payload [PROBE]: receipt_chain_valid:false, intact:false, status:gaps-found,
entries:75, corrupt_lines:0, scope:canonical.

Independent replay of the ACTUAL chain file [PROBE]:
- Path: /root/arifOS/VAULT999/seal_chain.jsonl -> symlink to
  /root/.local/share/arifos/vault999/seal_chain.jsonl (durable, owned arifos:arifos).
- 277 lines total; 4 prev_hash link breaks found at lines 32, 177, 191, 226
  (line 226 is a literal "forge-end-2026-07-24T10:30:10Z" marker entry, not a hash).
- Sequence: 1 -> 58, count 223, ZERO missing integers — seq continuity intact;
  the breaks are HASH-LINK discontinuities at 4 points, incl. 2 entries with seq=7
  (duplicate-seq from an earlier era) and one epoch-marker entry.
- EPOCH_ATTESTATION.json EXISTS in the chain directory.

Canon cross-check [DOC canonical_vault_chain.py]:
- "Historical gaps stay classified and HMAC-bound in EPOCH_ATTESTATION.json; the
  chain keeps growing... Any NEW gap at/after epoch start... → gaps-found (F-004)."
- verification_envelope.py epistemic rename: "intact (integrity) not valid (veracity)";
  receipt_chain_valid is a BACKWARD-COMPAT ALIAS of intact — two names, one measurement.

So the honest reading:
1. gaps-found = 4 historical hash-link breaks (Jul era + epoch markers), zero missing
   seq, zero corrupt lines — consistent with a classified historical-gap state.
2. Whether these 4 gaps are BOUND in EPOCH_ATTESTATION.json (i.e. sanctioned-old)
   or UNBOUND (F-004 violation, someone introduced a new gap) was NOT verified —
   the attestation file exists but its gap-digest vs observed 4 breaks was not
   compared. One read-only digest join closes it. UNVERIFIED, not assumed.
3. Naming trap preserved: intact:false says INTEGRITY of links, not that receipts
   are false. receipt_chain_valid:false is the alias, not a second fact.

## Status-layer mapping (paste's §4 question answered from probe)

Outer (arif_init top level): status=completed, verdict/effective_verdict=HOLD,
execution_state=AWAIT_INPUT, receipt_state=UNSEALED.
Inner (result.verification): final_verdict=DENY, can_mutate=false,
can_claim_success=false, seal_allowed=false.
Mapping (observed, scoped to canary): COMPLETED = the canary check itself ran to a
conclusion; AWAIT_INPUT = workflow wants a bound session next; DENY (inner) = the
mutation-class claim is denied; HOLD (outer) = the session-level verdict lattice
result. DENY and HOLD are not contradictions: different layers, same refusal.
Flatten-to-SUCCESS remains forbidden; both layers agree on: nothing authorized.

## Reconciliation vs paste

| paste claim | probe result | verdict |
|---|---|---|
| deployed 84efcec not stated in response | /health states 84efcec; commit is 09:19 today | RESOLVED (mid-session deploy by other actor) |
| model_governance absent | confirmed absent on MCP canary too | matches paste; fix-vs-surface UNRESOLVED |
| receipt chain gaps-found | INDEPENDENTLY REPRODUCED at file level: 4 link breaks, 0 seq gaps, 0 corrupt | CONFIRMED + localized |
| outer HOLD vs inner DENY conflict | layer mapping read from schema+payload | NOT a contradiction (scoped mapping above) |
| last_proof_mission Jul 2026 = old record | PROOF-SPINE dirs Jul 30-31 on disk | consistent: historical proof, not today's |

## Standing actions (unchanged, awaiting 888)

- Digest-join EPOCH_ATTESTATION.json vs the 4 observed breaks (read-only, cheap).
- REST-vs-MCP model_governance discriminating read (read-only).
- N1-P1 closure + diamond N2/N4/N5 (per PHASE0-2B-INSPECTION-PLAN.md).

STOP: read-only session; no writes to vault, no restarts, no config changes.
