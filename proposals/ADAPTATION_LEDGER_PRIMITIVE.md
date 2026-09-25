# Adaptation Ledger Primitive (Institutional Memory Specification)

> **Status:** DRAFT_AWAITING_F13 (PROPOSAL_READY)  
> **Target:** Closed-Loop Adaptation Ledger  
> **Date:** 2026-09-26  
> **Canonical Path:** `/var/lib/arifos/adaptation_ledger.jsonl` (Replicated: `/root/AAA/ledger/adaptation_ledger.jsonl`)  
> **Principle:** BEHAVIOR CHANGE WITHOUT AN ADAPTATION LEDGER ENTRY IS INSTITUTIONAL AMNESIA

---

## 1. Problem Statement

Previously, when a failure occurred (such as speaker misattribution in group chats), engineers or agents patched code or configurations, but wrote no institutional ledger entry. When agents vanished or context windows compacted, the institution forgot *why* the code changed, risking regression.

The **Adaptation Ledger** records every permanent behavioral shift triggered by an observed real-world consequence.

---

## 2. Adaptation Record Schema

Every entry in `adaptation_ledger.jsonl` follows:

```json
{
  "adaptation_id": "adapt-YYYYMMDD-seq-topic",
  "timestamp_utc": "ISO-8601 UTC timestamp",
  "subject": "Unique topic / incident tag",
  "incident": "Description of the real-world event or failure that demanded adaptation",
  "trigger_consequence": {
    "observed_failure": "What broke or drifted",
    "impact_class": "Classification (e.g. A2H_ATTENTION_LEAK, INTEGRITY_LOSS)",
    "organ": "Responsible organ"
  },
  "adaptation_mutation": {
    "artifacts": ["list of modified files, configs, or rules"],
    "code_anchor": "Exact file and line range where behavior changed",
    "behavior_delta": "How the system behaves now vs before"
  },
  "verification": {
    "witness": "Verifying agent or human sovereign",
    "proof": "How the new behavior was witnessed active",
    "status": "VERIFIED_ACTIVE"
  },
  "epistemic_label": "OBS"
}
```

---

## 3. Seed Entry: `adapt-20260926-001-speaker-attribution`

The inaugural entry proves the loop:
- **Incident**: Telegram group message from UID 1042200555 in the SADO channel was ungrounded, threatening to collapse into UNKNOWN or misattribution.
- **Consequence**: Human attention distraction and conversational boundary confusion.
- **Mutation**: Wired `channel_aliases.json` overlay into `adapter.py:6545` to dynamically ground UID 1042200555 to "Syed (Abang Sado)".
- **Witness**: Gateway reloaded, running live as PID 3904524 with the alias mapping in memory.
- **Status**: COMMITTED to `/var/lib/arifos/adaptation_ledger.jsonl`.
