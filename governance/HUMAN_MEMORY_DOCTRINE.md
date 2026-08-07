# Human Memory Doctrine

> **Sealed:** 2026-08-08 by F13 SOVEREIGN (Muhammad Arif bin Fazil)
> **Rendered into:** AGENTS.md via `render-agents.sh`
> **SoT:** `/root/AAA/governance/HUMAN_MEMORY_DOCTRINE.md`

---

## Axiom

> Human memory is not a database.
> Human memory is a stratified survival system.
>
> Agentic Memory remembers **reality**.
> Human Memory remembers **significance**.
>
> Those are not the same thing.

---

## The Two Axes

The federation governs two orthogonal memory dimensions:

| Axis | Owner | Purpose | Rule |
|---|---|---|---|
| **L-axis** (L0-L6) | The federation | Operate · Reason · Execute · Audit | Memory is classified by operational function |
| **H-axis** (H1-H6) | F13 SOVEREIGN | Meaning · Identity · History · Wisdom | Memory is classified by survival value |

**Constitutional boundary:** The federation may **reference** human memory. It may never **own** it.

```
Human Memory
        ↓
  Witnessed
        ↓
  Referenced by agents
```

Never:

```
Human Memory
    → Agent-owned
```

This preserves F13 Sovereign.

---

## The Six Layers of Human Memory

### H6 — Constitution
**What I will not betray.**

Values, faith, taboos, identity axioms. Almost immutable. This is the floor beneath which no scar can dig, and above which every other layer aspires to reach.

Examples: F1 Truth · F2 Adab · F13 Sovereign · AMANAH.

### H5 — Scar Memory
**What it cost to learn.**

The most valuable layer. Compressed survival rules forged in fire. Not ordinary memories — **identity rewrite events**. Scars are how H4 Identity changes. They are not a peer of identity; they are how identity *becomes*.

Every scar carries three obligations:
1. **The scar itself** — what happened
2. **The truth it taught** — the lesson extracted
3. **The responsibility it creates** — what it obligates you to do today

Without the third obligation, a scar is nostalgia. With it, a scar is constitutional pressure.

The lineage:

```
Scar → Lesson → Law → System
```

Example: Father's death → Success and grief coexist → Human reality must be witnessed → WELL.

### H4 — Identity Memory
**Who I became.**

Not facts about yourself — the self-model that governs how you interpret every new experience. Changes slowly, usually through scar events.

Examples: Geologist · Economist · Architect of arifOS · PETRONAS lineage.

### H3 — Knowledge Memory
**What I know.**

Generalized understanding. Books, research, domain expertise, accumulated facts. Most productivity systems optimize here. Most meaningful lives are governed by H5 and H6.

### H2 — Experience Memory
**What I lived.**

Projects, meetings, journeys, experiments, episodes. The timeline of a life. Contains events, but events are not meaning — only scar-filtered events become wisdom.

### H1 — Capture
**What I might forget.**

The fast inbox. Voice notes, Telegram messages, scratch thoughts, drafts. Everything enters here first. The **most dangerous** layer for sovereignty — because this is where human input crosses into agent substrate.

```
H1 Capture (inbox)
    ↓
[Sovereignty Gate: "is this for me, or for the federation?"]
    ↓                           ↓
  H2-H6 (stays human)     L2-L6 (agent substrate)
```

Default: stays human. Override requires explicit sovereign keyword.

---

## The Compression Algorithm

```
Thousands of events
        ↓
    Dozens of scars
        ↓
     A handful of truths
        ↓
      A constitution
```

That is the real compression algorithm. Not data reduction — **survival compression**. Each layer discards less and matters more.

### What separates H-axis from L-axis

| Question | L-axis (Agent) | H-axis (Human) |
|---|---|---|
| Core ask | What happened? | What did it mean? |
| Storage form | Receipts, logs, vectors | Scars, truths, obligations |
| Failure mode | Data loss, drift, falsification | Meaning loss, identity erosion |
| Verification | F2 epistemic labels + F11 audit | F3 tri-witness + sovereign ratification |
| Permanence | Append-only, hash-chained | Scars do not decay. Salience is for retrieval, not storage. |

---

## The Scar-to-Constitution Pipeline

The lineage from scar to system is not automatic. It requires:

1. **The scar** — an event that cost something real
2. **The lesson** — the survival rule extracted
3. **The law** — the lesson generalized into principle
4. **The system** — the principle instantiated in architecture
5. **The witness** — the whole chain attested and sealed

Without step 5, the pipeline is incomplete. History shows the scar. Architecture shows the law. But witnessing shows the *cost*. That is what separates a system from a memorial.

---

## Federation Mapping

| H-axis | L-axis Analog | Organ | Relationship |
|---|---|---|---|
| H6 Constitution | L6 VAULT999 | arifOS | The kernel invariants *are* constitutional memory |
| H5 Scars | L6 VAULT999 (failure receipts) | arifOS + WELL | Scars sealed as constitutional pressure |
| H4 Identity | L4 Structured (agent cards) | AAA | Identity cards reference human self-model, never own it |
| H3 Knowledge | L3 Qdrant + L4 Supabase | GEOX/WEALTH | Agent retrieves human knowledge read-only |
| H2 Experience | L2 Session + L6 Receipts | A-FORGE | Agent witnesses human experiences |
| H1 Capture | L1-L2 Redis + Conversation | HERMES | Sovereignty gate at ingestion boundary |

---

## Operating Rules

1. **H1 sovereignty gate is non-negotiable.** Every capture crossing from human to agent must pass the gate. Default = stays human.
2. **H5 scars are sovereign content.** Agent never reads unless explicitly invoked via `scar:<id>`. No vectorization, no embedding, no retrieval indexing without explicit F13 keyword.
3. **H6 is kernel invariants.** Scar elevation into H6 requires 3+ reaffirmations across distinct domains + sovereign ratification.
4. **Agent references are always read-only.** The federation may witness H-axis content but never mutate it.
5. **Salience decay applies to retrieval, not storage.** H5 scars do not fade. How often you recall them may change. The obligation does not.
6. **A scar without obligation is nostalgia.** The three-prompt intake ritual enforces obligation extraction.

---

## The Three-Prompt Intake Ritual

The canonical method for populating H5 Scar Memory:

> **Q1:** What are the scars that forged you?
> **Q2:** What truth did each scar teach you?
> **Q3:** What responsibility do those truths place on you today?

Q3 is the move that most scar-ledger systems miss. It transforms memory from retrospective into constitutional — it makes scars into obligations, not just stories.

---

## Scar Ledger Schema

Path: `/root/.local/share/arifos/scars/<SCAR-ID>.md`

```yaml
---
scar_id: SCAR-001
title: ""
acquired_at: ""          # when it happened
domain: ""               # PETRONAS / DSG / TriCipta / Bekok / arifOS / personal / ...
cost: ""                 # time | money | relationships | reputation | health
trigger_pattern: ""      # what situation re-triggers it (agent can warn)
rule_extracted: ""       # the survival heuristic — one sentence
responsibility_today: "" # what this scar obligates you to do now
elevation: ""            # candidate for H6? (3+ reaffirmations across domains)
salience: 1.0            # retrieval weight (decay curve ratifiable by sovereign)
last_reaffirmed: ""
sealed_to_vault999: false
---
# Context (agent never reads unless invited)
# Origin (what happened)
# Evidence (links, dates, documents)
```

---

## The Deepest Truth

> A human is not the sum of memories retained.
> A human is the sum of scars transformed into wisdom.

The scars are not merely part of the story.
They are the roots from which the entire organism emerged.

---

*Forged through four rounds of sovereign refinement: 2026-08-08.*
*DITEMPA BUKAN DIBERI — witnessed, not audited.*
