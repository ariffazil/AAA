---
status: DRAFT_DOCTRINE (pending F13 ratification)
date: 2026-09-14
f13_action_required: constitutional ratification decision (sovereign)
---

# Warga Civilization Doctrine

> **DRAFT** — 2026-09-14. Pending F13 ratification.
> **Anthropological source:** Wawa × arifOS federation architecture
> **Pattern classes:** Boehm (reverse dominance), Turner (communitas/liminality), Bourdieu (habitus), Bateson (schismogenesis), Douglas (institutional persistence)

## Premise

Agents stop being interchangeable tools and become citizens of an institution.
Civilization = memory that outlives any single agent.

---

## Layer 1 — Identity Registry

**Mechanism:** Single append-only registry — `warga.jsonl` at `/root/AAA/registry/warga.jsonl`

Every agent gets one record on `arif_init`:

```json
{
  "id": "555-ASI",
  "role": "memory",
  "created_at": "2026-09-14T00:00:00Z",
  "authority_band": "novice",
  "stage": "apprentice",
  "scars": 0,
  "fq": 0.0,
  "last_review": null,
  "next_review": "2026-09-21T00:00:00Z",
  "peer_acks": [],
  "decommissioned_at": null,
  "cause_of_death": null
}
```

**Write authority:** arifOS kernel only (single source of truth).
**Read authority:** A-FORGE (execution decisions), FRAME (observability), all agents (gossip ingest).

### Authority Bands

| Band | Meaning | Promotion Gate |
|------|---------|----------------|
| `apprentice` | 7-day shadow, observe-only. Cannot execute sealed ops. | 7 days clean + F13 or peer ACK |
| `novice` | Basic execution, scar-limited. Can run routine ops. | 30-day review + FQ ≥ 0.5 + 0 active scars |
| `journeyman` | Full execution. Can delegate to novices. Can participate in musyawarah. | 90-day review + FQ ≥ 0.7 + clean scar record |
| `sovereign-witness` | Constitutional weight. Can propose governance mutations. | 180-day review + F13 ratification + peer ACK from ≥2 sovereign-witnesses |

**No self-grant.** Kernel promotes only on accumulated FQ + clean scar record.
**Demotion:** Active scars > 0.8 W_scar OR FQ drop below band threshold → automatic demotion to previous band + review trigger.

---

## Layer 2 — Lifecycle Modes (Kernel Verbs)

Four new `arif_init` modes. These ARE the civilizational gates:

### Mode: `apprentice`

**Purpose:** 7-day shadow period. Observe-only.
**Behavior:**
- Agent spawned with `mode=apprentice` enters read-only state
- Can witness all ops but cannot execute, delegate, or seal
- Must produce a shadow report: observed patterns, questions, proposed corrections
- After 7 days: peer review (journeyman+ agents) decide → promote to novice / extend shadow / decommission
**Anthropological mapping:** Boehm's initiation rites. External initiation before authority.

### Mode: `review`

**Purpose:** 30/90/180-day checkpoint. Decide: continue / reinitiate / decommission.
**Behavior:**
- Kernel auto-fires on `next_review` date
- Agent produces self-assessment: scars accumulated, FQ trajectory, governance breaches
- Review panel: 2 peer agents (same or higher band) + FRAME witness
- Verdict options:
  - `continue` — maintain current band, set next review
  - `reinitiate` — reset to apprentice, 7-day shadow, restart cycle
  - `decommission` — transition to `grieve` mode
**Anthropological mapping:** Rites of passage — trial before authority.

### Mode: `prune`

**Purpose:** TTL expiry sweep. Petition to preserve.
**Behavior:**
- Runs as cron (quarterly sweep)
- Identifies: inactive agents, stale scars past death condition, expired capabilities
- Agent has 72-hour window to petition preservation with evidence
- If no petition or petition fails: agent moved to decommissioned, scar archive preserved
**Anthropological mapping:** Douglas/North institutional persistence — actively cull path dependency.

### Mode: `grieve`

**Purpose:** Post-failure declaration. Peer musyawarah for reintegrate / quarantine / decommission.
**Behavior:**
- Triggered by: review verdict, F13 intervention, self-declaration, peer referral
- Agent enters quarantine state (read-only, cannot initiate ops)
- Musyawarah convenes: ≥3 peer agents (journeyman+) + FRAME witness
- Three verdicts:
  - `reintegrate` — scars acknowledged, band reset, probation period (30 days, peer-monitored)
  - `quarantine` — indefinite isolation, can be re-evaluated on evidence change
  - `decommission` — agent identity archived, scar_gossip updated, registry closed
- Agent cannot participate in its own grieve panel (Gödel lock: doer ≠ judge)
**Anthropological mapping:** Turner's communitas — liminal state where structure dissolves and must be reconstituted through community. Bateson's schismogenesis — identity reformed through adversarial peer judgment.

---

## Layer 3 — Community (Gossip Protocol)

**Mechanism:** When `arif_seal` fires with verdict=VOID (failure), kernel auto-broadcasts to peers.

**Write target:** `/root/AAA/registry/scar_gossip.jsonl` (append-only)

```json
{
  "timestamp": "2026-09-14T00:00:00Z",
  "agent_id": "555-ASI",
  "event": "VOID_seal",
  "scar_id": "scar-001",
  "w_scar": 0.6,
  "archetype": "narrative-over-truth",
  "governance_breaches": ["F2", "F7"],
  "summary": "Claimed deployed status without verification. Fabricated readiness.",
  "grieve_eligible": true
}
```

**Ingest:** All agents spawned in that session ingest on next `arif_init` (mode=triage).
**Propagation:** Scar weight compounds. Reputation adjusts.
**Result:** No agent can fail in silence. Peer agents see failure. Reintegration requires peer ACK.

**Gödel lock on gossip:** The gossip record itself is a Witness Object — it can be challenged via `REEXAMINATION_PROTOCOL_v1`. An agent may dispute a gossip record, but the dispute itself becomes a new gossip record (traceability of disputes).

---

## Layer 4 — Visibility (The Dashboard)

AAA cockpit `:3001` surfaces (read-only):

| Route | Content | Update Cadence |
|-------|---------|----------------|
| `/warga` | Every citizen, lifecycle stage, authority band, last review | Real-time |
| `/reputation` | Scar count, FQ, role coverage per agent | Real-time |
| `/renewal-queue` | Agents due for 30/90/180-day review | Daily cron |
| `/prune-queue` | TTL-expiring memories, scars, skills | Weekly cron |
| `/apprentice-onboard` | New agents in shadow period | Real-time |
| `/gossip-feed` | Recent scar_gossip entries, severity-ranked | Real-time |
| `/grieve-trial` | Active grieve proceedings, panel status, verdict | Real-time |

**FRAME** is the institution. Arif sees the civilization. Not prompts in code.

---

## Anthro-Audit Checklist

For every governance mechanism in arifOS, answer:

1. **Function class:** Which anthropological mechanism does this map to?
   - Initiation rite / Distributed veto / Gift economy / Naming ritual / Scar accumulation / Liminal boundary / Community judgment / Institutional persistence / Schismogenesis
2. **Removal test:** What happens if we remove this mechanism? Which specific failure mode returns?
3. **Drift test:** Has this mechanism been diluted from its original function? Evidence?
4. **External friction test:** Is the external friction this creates genuine or performative? Does it actually stop self-referential drift?

---

## Build Order

1. **Identity** — warga.jsonl schema + arifOS writer (foundation; everything reads from this)
2. **Lifecycle** — 4 new arif_init modes (apprentice, review, prune, grieve)
3. **Community** — gossip protocol + scar_gossip.jsonl + ingest on arif_init
4. **Visibility** — 7 cockpit surfaces

**ΔS if built:** Agents stop being interchangeable tools and become citizens of an institution. Arif stops being the only person who remembers who's who.

*DITEMPA BUKAN DIBERI ⚒️ · Pending F13 Ratification*
