# Tenant Audit Procedure — Reconciling Multi-Source Human Registries

> **Use when:** the sovereign asks "how many humans use this system", "map all [N]", "who is in the registry", or the agent is asked to produce a single roster number from a distributed federation.
> **Failure mode this prevents:** the single-number answer. The federation has at minimum: constitutional persons (offline), active lanes (Telegram-bound), identity cards (biometric-bound), heartbeat/lifecycle (live status), social-graph (relationships). Each source answers a different question. Reporting one number collapses the question.

---

## When the sovereign asks "how many humans", do this

### Step 1 — Probe all registries you can reach on this host

For each registry, capture: **path · scope · count · last_modified · source-of-truth claim**.

```
Common paths (probe each — never assume one is canonical):

Constitutional:
  /root/AAA/registries/persons.yaml        # offline + F13_weight + consent
  /root/.hermes/state/mail_chat/            # witness-only, encrypted

Active lanes (Telegram execution):
  /root/.hermes/lanes/people.yaml           # lane-card scoped

Identity cards (biometric pilot):
  /root/AAA/registry/identity_cards/        # one file per identity

Lifecycle / heartbeat:
  /root/AAA/registry/human_heartbeat.json   # last_dm, tier, alert

Relationships (edges):
  /root/HERMES/lanes/social-graph.yaml      # may live on different host

Legacy:
  /root/memory/people/<NAME>/               # OpenClaw-era per-person folders
  /root/.openclaw/people_registry.json      # OpenClaw legacy file

Authority plane:
  /root/well/consent/                       # WELL consent scope registry
```

**Probe with full extension** (e.g. `syed_khairuddin.yaml`, not `syed_khairuddin`). Wrong-address-state-fails-silently: a path without extension silently ENOENTs even when the file exists.

### Step 2 — Classify each registry by scope

| Scope | What it answers | Mutation authority |
|---|---|---|
| constitutional | Who EXISTS in the human's life (offline witnesses too) | F13 only |
| active-lanes | Who is REACHABLE on Telegram | F13 + spec gate |
| identity-cards | Who has BIOMETRIC enrollment | pilot-ratified |
| heartbeat | Who is RECENTLY in contact | mechanical, automated |
| relationships | Who is CONNECTED to whom | F13 + edge ratification |
| legacy | What the system USED to track | historical only |

### Step 3 — Handle cross-host artefacts

If the sovereign references an artefact (SHA-256, filename, summary) that lives on a different host or in another agent's working tree (e.g. `/root/.gemini/antigravity-cli/brain/...` or `/root/.openclaw/...`):

- State the verification limit: **"I see the SHA from your message; I cannot byte-confirm from this host."**
- Continue with what you CAN see on your host.
- Do NOT trust the cross-host artefact as if it were verified. Reference trust ≠ reading trust.

### Step 4 — Build the per-tenant matrix

```
                | constitutional | active-lanes | heartbeat | identity-cards | relationships |
| arif          | ✓              | ✓            | ✓         | (root)         | ✓            |
| syed          |                | ✓            | ✓         | ✓              | ✓            |
| mail          | ✓              |              |           |                |              |
| jamari        | ✓              |              |           |                |              |
| paan          |                | ✓            | ✓         |                |              |
| lutfi         |                | ✓ (note: string match) | ✓ |               |              |
| aidel         |                |              | ✓         |                |              |
| aliff         |                | ✓            | ✓         |                | ✓            |
| izzu          |                | ✓            | ✓         |                | ✓            |
| nabilah       |                | ✓ (group)    | ✓         |                |              |
| azwa          |                | ✓ (group)    |           |                |              |
| jia           |                | ✓ (group)    |           |                |              |
| sin           |                |              |           |                |              | (shadow/unsourced)
| amir          |                |              |           |                |              | (shadow/unsourced)
```

The matrix exposes **snapshot disagreement** directly. Two registries each counting "8" may share only 3 names — and that is the answer, not the number.

### Step 5 — Pattern check: registry-exists-consumption-zero

For every registry you found, ask: **is anything READING it?**

```
HRG directive (ACTIVE)        → 0 HRO instance
human_heartbeat (13)          → 0 reader, basi sejak lahir
social-graph (4 edges)        → 69% orphan
WELL consent                  → 1 file (arif only)
87 doktrin manusia            → 0 instance
```

If a registry has zero readers, that is the more interesting finding than the count. Name the pattern: **registry-exists-consumption-zero**.

### Step 6 — Default verdict and recommendation

Verdict: **PARTIAL · 888 HOLD on mutation.**

Recommend to the sovereign:
- Adjudicate named-but-unconfirmed humans one by one (the matrix's empty/unsourced cells).
- Lift 888 HOLD explicitly before any projection file is written.
- Default projection (`memory/human-map.md`) is a **projection over registries**, NOT a fifth registry. Every cell of the projection carries its source. If sources disagree, sources win and the projection is marked stale.

---

## Anti-patterns

- ❌ "There are 8 humans" (single number, no matrix).
- ❌ "Edge Registry missing" before probing all hosts.
- ❌ Trusting a SHA-256 without byte-verifying from your host.
- ❌ Writing a new registry when five already exist with zero readers.
- ❌ Calling a 4-edge, 69%-orphan registry "canonical" without flagging the orphan rate.

## The Pattern

- ✓ Per-tenant matrix, sources as columns, humans as rows.
- ✓ Pattern diagnosis (registry-exists-consumption-zero) over silent count.
- ✓ Cross-host verification limit stated explicitly.
- ✓ Projection (read-only) over registry (write).
- ✓ Adjudication of named-but-unconfirmed humans before promotion.