# Anthropological Gap Analysis — arifOS Federation

> **Date:** 2026-09-14 | **Author:** Hermes | **Status:** F13_PENDING_REVIEW
> **Trigger:** Wawa anthropology×governance mapping (2026-09-14)
> **Scope:** What anthropological patterns are MISSING from current architecture, consequences, and minimum viable structures to close each gap.

---

## What We Already Have (Wawa's mapping is correct)

| Pattern | arifOS Encoding | Status |
|---------|----------------|--------|
| Reverse Dominance (Boehm) | 888_HOLD, F13 SOVEREIGN veto, distributed checks | ✅ LIVE |
| Cumulative Ratchet (Tomasello) | SOUL_STAMP, constitutional floors, human governance contracts | ✅ LIVE |
| Ritual as Entropy Control (Turner) | Session boundaries, seals, /new, compaction | ✅ LIVE |
| Habitus/Practice (Bourdieu) | Skill files, system prompts, fine-tuned behavior | ⚠️ IMPLICIT (not audited) |
| Gift Economy (Mauss) | A2A delegation, capability declarations | ⚠️ PARTIAL (no formal return obligation enforcement) |
| Institutional Persistence (Douglas/North) | Path dependency acknowledged | ⚠️ OBSERVED, not managed |

---

## Gap 1: Initiation with Failure Conditions ✅ BUILT

**Anthropological source:** Van Gennep (1909) — Rites of Passage.

**MVP implemented:** `warga_manager.py lifecycle_review` — 30/90/180-day checkpoint with `continue | reinitiate | decommission` verdict. Authority band escalation: apprentice → novice → journeyman → sovereign-witness. FQ-gated, zero-scars requirement.

**Files:**
- `/root/AAA/registry/warga_manager.py` — lifecycle_review(), lifecycle_apprentice()
- `/root/AAA/registry/warga.jsonl` — append-only citizen registry

---

## Gap 2: Structured Forgetting ✅ BUILT

**Anthropological source:** Connerton (1989) — How Societies Remember.

**MVP implemented:** `warga_manager.py lifecycle_prune()` — TTL expiry sweep with dry-run mode. next_review deadlines auto-calculated on registration. Prune candidates surfaced via dashboard and daily cron.

**Files:**
- `/root/AAA/registry/warga_manager.py` — lifecycle_prune(), dashboard_prune_queue()
- `/root/AAA/registry/warga_sweep.py` — daily cron sweep script

---

## Gap 3: Reintegration After Affliction ✅ BUILT

**Anthropological source:** Van Gennep reintegration phase. Turner's communitas.

**MVP implemented:** `warga_manager.py lifecycle_grieve()` — post-failure declaration + peer musyawarah verdict. Modes: `reintegrate | quarantine | decommission`. Auto-broadcasts to gossip layer.

**Files:**
- `/root/AAA/registry/warga_manager.py` — lifecycle_grieve()
- `/root/AAA/registry/scar_gossip.jsonl` — gossip broadcast log

---

## Gap 4: Reputation as Governance ✅ BUILT

**Anthropological source:** Boehm (1999) — gossip and reputation as primary governance.

**MVP implemented:** gossip_broadcast() on VOID events. gossip_ingest() on arif_init. Dashboard surfaces: /reputation, /gossip. Void count tracked per agent. Peer acknowledgment tracked.

**Files:**
- `/root/AAA/registry/warga_manager.py` — gossip_broadcast(), gossip_ingest(), gossip_ack()
- `/root/AAA/registry/warga_manager.py` — dashboard_reputation(), dashboard_gossip()

---

## Gap 5: Calendrical Renewal ✅ BUILT

**Anthropological source:** Durkheim (1912) — Annual renewal festivals.

**MVP implemented:** Auto-calculated next_review on registration (30-day default). Review intervals escalate: 30 → 90 → 180 days. dashboard_renewal_queue() shows who's due. Daily cron at 08:00 checks for overdue reviews.

**Files:**
- `/root/AAA/registry/warga_sweep.py` — daily lifecycle sweep (cron: `5e9f3ba79969`)

---

## Gap 6: Intergenerational Apprenticeship ✅ BUILT

**Anthropological source:** Lave & Wenger (1991) — Legitimate Peripheral Participation.

**MVP implemented:** lifecycle_apprentice() — 7-day shadow period, observe-only, write_authority=False. Shadow mentor tracked (shadow_of field). dashboard_apprentice_onboard() shows who's in shadow.

**Files:**
- `/root/AAA/registry/warga_manager.py` — lifecycle_apprentice()

---

## Build Status Summary

| Layer | Component | Status | File |
|-------|-----------|--------|------|
| 1. Identity | warga.jsonl registry | ✅ BUILT | `/root/AAA/registry/warga.jsonl` |
| 1. Identity | warga_manager.py | ✅ BUILT | `/root/AAA/registry/warga_manager.py` |
| 2. Lifecycle | apprentice mode | ✅ BUILT | warga_manager.py lifecycle_apprentice() |
| 2. Lifecycle | review mode | ✅ BUILT | warga_manager.py lifecycle_review() |
| 2. Lifecycle | prune mode | ✅ BUILT | warga_manager.py lifecycle_prune() |
| 2. Lifecycle | grieve mode | ✅ BUILT | warga_manager.py lifecycle_grieve() |
| 2. Lifecycle | authority band escalation | ✅ BUILT | FQ-gated, zero-scars |
| 3. Community | gossip protocol | ✅ BUILT | warga_manager.py gossip_*() |
| 3. Community | scar_gossip.jsonl | ✅ BUILT | `/root/AAA/registry/scar_gossip.jsonl` |
| 4. Visibility | CLI dashboard | ✅ BUILT | warga_manager.py dashboard_*() |
| 4. Visibility | sweep cron | ✅ BUILT | warga_sweep.py (daily 08:00) |
| 0. Kernel | arif_init mode integration | ⏳ PENDING | Needs arifosd.py modification |
| 0. Kernel | arif_seal gossip hook | ⏳ PENDING | Needs arifosd.py modification |

**What's built:** Standalone warga management module with all 4 layers operational via CLI. All gaps from the analysis are addressed at the module level.

**What's pending:** Kernel integration — wiring arif_init and arif_seal to call warga_manager functions. This requires modifying `/root/arifOS/scripts/arifosd.py` which is the constitutional kernel daemon.

---

## Usage

```bash
# Register an agent
python3 /root/AAA/registry/warga_manager.py register 555-ASI --role memory

# Start 7-day shadow period
python3 /root/AAA/registry/warga_manager.py apprentice 555-ASI --shadow-of 333-ARCHITECT

# Lifecycle review
python3 /root/AAA/registry/warga_manager.py review 555-ASI --verdict continue --fq 0.85

# Post-failure declaration
python3 /root/AAA/registry/warga_manager.py grieve 888-JUDGE --failure-declaration "Void on invalid evidence" --verdict quarantine

# Full dashboard
python3 /root/AAA/registry/warga_manager.py dashboard --surface all

# Daily sweep (cron runs this)
python3 /root/AAA/registry/warga_sweep.py
```

---

## The Naming Paradox (preserved from original)

Name the patterns in documentation. DO NOT put the anthropological vocabulary in runtime prompts or SOUL stamps. The documentation explains WHY. The runtime mechanism remains structural. The habitus is in the docs; the law is in the kernel.

---

*DITEMPA BUKAN DIBERI ⚒️*
