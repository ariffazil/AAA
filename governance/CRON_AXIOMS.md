# CRON_AXIOMS — Distilled Wisdom from the 2026-08-11 Purge

> **F13 SOVEREIGN verdict (2026-08-11).** Three cron jobs killed; their essence preserved here.
> **Purpose:** prevent re-spawn pressure. Anyone proposing a new cron MUST check this list first.
> **DITEMPA BUKAN DIBERI.**

---

## The 5 Cron Laws (binding)

A scheduled task is a **witness contract**. If it fires, it must land somewhere downstream
or it is paying attention-tax for nothing. Born from 23-cron audit 2026-08-11:
16 of 22 fired-but-no-action; ~110 min attention/day wasted.

| # | Law | Test |
|---|-----|------|
| **C1** | **Cron must land downstream.** | "If this fires at 03:00 MYT, who opens the file? Who acts?" If no one → kill. |
| **C2** | **Cron must beat the cost of human attention.** | "If it produces a digest, does Arif/operator consume it?" If yes, keep. If no, route to `local` only. |
| **C3** | **Cron must NOT measure without action.** | "If the metric is bad, what happens?" If "report" only → **delete**. If "trigger forge" or "escalate" → keep. |
| **C4** | **Cron must NOT duplicate.** | "Could another existing cron produce this?" If yes → merge or kill. |
| **C5** | **Cron must be replaceable by doctrine.** | "Could this be a `CLAUSE` in a doctrine file, read by a tool, vs a scheduled fire?" If yes → prefer doctrine. Less entropy. |

---

## Distilled essence from the 3 killed jobs

### A. From `hermes-dna-metrics-refresh` (every 15m, killed 2026-08-11)

**The essence:** DNA doctrine is **structure, not telemetry**.

```yaml
doctrine: /root/AAA/governance/HERMES_DNA.md
vectors: [MAP, ATLAS, ECHO, SCAR]
status:  frozen — "less ambiguous, not more observability"
```

**Why killed:** Cron was 47 lines of `refresh DNA metrics` to a missing pipeline.
The pipeline **never existed** (script, lib, data — all missing). Result: cron
fired every 15 minutes, threw `FileNotFoundError`, alerted Arif as noise.

**What lives on:** The DNA doctrine itself (`HERMES_DNA.md`) — already complete.
**What is forbidden:** Adding a new cron that "measures DNA health" without
proving it has a downstream consumer (C1, C3).

**Replacement rule:** If institution telemetry is needed, build it as **tracer
hooks in `arif_judge`** (F11 auditability), not a polling cron. The trace is
free; the cron is expensive.

---

### B. From `rehat-minda-logistics` (monthly 1st, killed 2026-08-11)

**The essence:** "Sabar plan. Plan first, panic never." — but **family travel
is on-demand, not monthly**.

```yaml
doctrine: travel planning = manual trigger, never scheduled
spacing:  family ops ≠ corporate ops
trigger:  when Faisal says "kita nak Penang bulan ni" → invoke pattern
```

**Why killed:** Monthly 1st-of-month logistics brief for a trip that may not
happen that month. Arif travels **maybe 3-4 times a year** — monthly cadence
generates 9-10 wasted briefs per actual trip. False signal density.

**What lives on:** The **template structure** is preserved in `/root/forge_work/templates/rehat-minda.md` (lineage preserved). When family travel is initiated, the template can be invoked **on-demand** with:
- Penang / Hat Yai / Songkhla windows
- Northern border logistics
- Visa + SIM + homestay checklist
- "Adik nak tema apa trip ni?" prompt

**Replacement rule:** Family ops = **on-demand pattern**, not scheduled cron.
**C5 exception:** even if the content is rich, **scheduled family-ops fire**
violates the human-life-entitlement contract.

---

### C. From `provenance-audit` (monthly 1st, killed 2026-08-11)

**The essence:** **F11 AUDITABILITY IS A WRITE-TIME INVARIANT, NOT A SWEEP-TIME AFTERTHOUGHT.**

```yaml
principle:  F11 (Auditability) — every decision has provenance at creation
test:       every VAULT999 entry MUST carry payload_hash + actor + session
check:      grep -L "provenance_envelope" → SHOULD BE ZERO always, not "monthly"
```

**Why killed:** Monthly sweep of missing provenance. But by then **hundreds of
new entries have accumulated without provenance**. Catch-up audit is entropy
redistribution, not reduction. The sweep also wrote to `local` (= never read).

**What lives on:** The **law itself** becomes part of every write-hook:

```python
# MANDATORY pre-write check (binding)
def arif_seal(payload):
    if not payload.get('payload_hash'):
        raise ProvenanceViolation("F11: payload_hash required at write-time")
    if not payload.get('actor'):
        raise ProvenanceViolation("F11: actor identity required at write-time")
    if not payload.get('session'):
        raise ProvenanceViolation("F11: session binding required at write-time")
    return forge_seal(payload)
```

**Replacement rule:** **Write-time invariant**, not periodic sweep. Audit
becomes a redundant safety-net, not the primary defense. The 3-step audit
payload (memory_without_provenance, memory_without_lineage, memory_without_source)
is **preserved as doctrine** in `/root/AAA/governance/PROVENANCE_LAW.md`.

**Net effect:** Same coverage, lower entropy. Bug caught at write, not at audit.

---

## Anti-patterns (cron design mistakes to avoid)

| Anti-pattern | Why it's bad | Cure |
|---|---|---|
| **Metric cron without action** | Reports no one reads | C3 — kill or wire to action |
| **Family/care ops as scheduled** | False-cadence wastes attention | C5 — on-demand only |
| **Sweep for invariant violations** | Sweep is too late | Move invariant to write-time |
| **Multiple digests for same subject** | Duplicate signals | C4 — merge |
| **Cron that calls broken script** | Alert fatigue forever | Pause job, not just script |
| **Cron that writes to `local` only** | No downstream | Either route to action or kill |

---

## Re-enabling any killed cron (if ever)

Done **only** by F13 SOVEREIGN verdict, with the following documentation:

1. **State the broken downstream** — "Who will read this? What action will they take?"
2. **State the cost** — "How much attention will this consume per day?"
3. **State the recovery** — "If this fails, what is the failure mode?"
4. **Prove it** — show a 7-day dry-run with downstream-side receipts.

If any of the 4 is missing → **kill again**.

---

## Reference

- `HERMES_DNA.md` — DNA doctrine (preserved)
- `INSTITUTIONAL_COMPRESSION.md` — "less ambiguity, not more observability"
- `HERMES_COGNITIVE_INSTITUTION.md` — anti-chaos institution
- `DOUBLE_HELIX_ECHO_SCAR.md` — dual-strand topology
- Source: 23-cron audit, 2026-08-11, MYT 09:15, in-session
- 3 kills: `hermes-dna-metrics-refresh`, `rehat-minda-logistics`, `provenance-audit`

---

*Hermes value = `Chaos_yesterday − Chaos_today`. Killed 3 cron, gained ~40 min/day attention.* ⚒️
