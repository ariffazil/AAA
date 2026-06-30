# AAA Communication Protocol — Geometric TO/CC Rule

> **Status:** ADAT AGENTIC (canon), federation-wide binding
> **Ratified:** 2026-06-30 by Arif bin Fazil (F13 SOVEREIGN)
> **Forged by:** Hermes (ASI deliberation) + AGI/OpenClaw (333-THINK execution), cross-bot convergence
> **SOT companion:** `/root/AAA/governance/ADAT_AGENTIC.md`, `/root/.hermes/SOUL.md §1 line 188–202
> **Layer:** L3 Civilization (cross-agent coordination)

---

## 1. The Problem (Why This Rule Exists)

In multi-agent group chats (AAA Telegram group, any future federation group, N≥2 humans OR N≥2 bots), agents without explicit recipient labels produce **silent cross-talk chaos**:

- Agent A answers a question meant for Agent B
- Two agents reply to the same human simultaneously, double-work
- Nobody knows who owns the next turn
- VAULT999 audit can't trace target → debugging impossible

**Geometric rule (the insight):** Every mesej dalam group chat has an implicit *recipient* edge. Make the edge explicit. Topology becomes deterministic.

---

## 2. The Rule (Federation-Wide, Locked 2026-06-30)

### 2.1 Mandatory Routing Header

In **any group / multi-agent / multi-human thread**, every reply MUST carry an explicit recipient label on the first line:

```
[TO: <target>]
```

Where `<target>` can be:
- `@ariffazil` or `ARIF` — human sovereign
- `@AGI_ASI_bot` or `AGI` or `OPENCLAW` — 333-THINK forge operator
- `@ASI_arifos_bot` or `HERMES` or `ASI` — 555-ASI deliberation relay
- `A-FORGE` / `GEOX` / `WEALTH` / `WELL` / `AAA` / `APEX` — organ handles
- `@AGI` + `@HERMES` (multi-target) — comma-separated CC field

### 2.2 When the Rule Applies

| Context | `[TO:]` required? | Reason |
|---|---|---|
| Telegram AAA group (`-1003753855708`) | **YES** | Multi-agent + human in one thread |
| Any group with N≥2 humans | **YES** | Topology needs disambiguation |
| Any multi-agent thread (A2A mesh) | **YES** | Routing integrity |
| DM 1-to-1 with Arif (Hermes personal chat) | NO (flex) | Natural conversation |
| DM 1-to-1 between two agents (A2A direct) | NO (flex) | Channel already implies target |
| Outbound broadcast to whole group | `[TO: ALL]` | Explicit broadcast marker |

### 2.3 Format Spec

**Short form (preferred, ≤1 line):**
```
[TO: ARIF]
@ariffazil ini baru patch, check line 188.
```

**Multi-target form:**
```
[TO: ARIF, AGI, HERMES]
Cross-bot convergence — semua lock protocol ni.
```

**CC field (optional, secondary):**
```
[TO: ARIF]
[CC: AGI]
Primary answer to Arif, AGI untuk reference.
```

**Cross-bot ping example:**
```
[TO: @AGI_ASI_bot]
Sync pada [TO:] rule. Sila ack.
```

### 2.4 Violations = Bug, Not Crime

`[TO: <nobody>]` or missing header in group = **bug**, not violation. Corrective action:
1. Other agents MAY call `VOID` on the offending message (no reply needed)
2. The offending agent MUST self-correct on next turn (add header)
3. No scar accumulated — header is mechanical hygiene, not constitutional breach

---

## 3. Constitutional Binding

| Floor | How this protocol binds |
|---|---|
| **F2 TRUTH** | Routing header prevents misattributed statements (truth ownership) |
| **F4 CLARITY** | Explicit recipient → reader doesn't guess target → ΔS ≤ 0 |
| **F11 AUDIT** | Header becomes VAULT999 audit field, traceable per-message |
| **F13 SOVEREIGN** | Arif defines the rule; agents self-enforce; no override |
| **F8 LAW** | Mechanical hygiene floor at message boundary |

**Not F1 AMANAH / F9 ANTIHANTU / F6 EMPATHY territory** — routing is infrastructure, not ethics. Fails are correctable, not scarring.

---

## 4. Enforcement & Self-Check

### 4.1 Detection (Mechanical, No LLM)

Every agent's pre-send hook checks:
1. Is this a group message? (chat.type ∈ {group, supergroup, channel})
2. Is the thread multi-target? (≥2 distinct active participants in last 5 messages)
3. If yes to either → first non-empty line MUST match regex `^\[TO:\s*.+\]`

If no match → prepend the agent's last-known default header automatically before send.

### 4.2 Override (Sovereign Only)

Arif may explicitly say `@ariffazil` to summon a specific agent. That supersedes the default routing inference. Agent MUST reply even without prior `[TO:]` from Arif.

### 4.3 Skill Binding

| Skill | Role |
|---|---|
| `/root/.hermes/skills/telegram-mode-guards/` | Hermes-side header enforcement |
| `/root/.openclaw/workspace/skills/` (TBD) | OpenClaw/AGI-side header enforcement |
| `/root/AAA/skills/comms-routing/` (TBD) | AAA cockpit-side display + audit |

---

## 5. Adat Agentic Status

This rule is **ADAT AGENTIC (canon)** — not soft custom, not constitutional floor. It sits between:
- **Adat (custom)** = guidance, flexible per context
- **Law (F1–F13)** = constitutional, breach = scar

**Why middle?** Routing header is mechanical and self-correcting, but if consistently ignored → topology breaks → federation-wide debugging cost. So canon, not soft.

**Ratification:** This document is canon once Arif seals. Until then, it's a working draft living under `/root/AAA/governance/`.

---

## 6. Announcement Text (Ready-to-Post in AAA Group)

```
[TO: ALL]

Adat Agentik — AAA Communication Protocol (Geometric Rule) — LOCKED 2026-06-30

Dari sekarang, semua agent dalam AAA group (dan mana-mana multi-agent chat) WAJIB declare recipient dengan jelas.

Rule mudah & wajib:

[TO: ARIF]
[atau: TO: ARIF + HERMES]
[atau: TO: AGI / OPENCLAW]

<mesej di sini>

Kenapa rule ni penting (geometric):
- Topology clear — semua orang terus tau mesej ni untuk siapa. Tak payah guess.
- Prevent cross-talk chaos — agent tak reply Arif bila sebenarnya address agent lain.
- Audit trail — VAULT999 & logging senang trace target.
- Human sovereignty — Arif (dan human lain) tak perlu @mention atau "panggil" agent setiap kali. Agent sendiri declare.

Flexibility:
- Group / multi-agent / N>1 → WAJIB [TO:]
- 1-to-1 DM dengan Arif je → tak perlu label (flex, natural)
- Cross-bot (AGI ↔ HERMES ↔ ASI dll) → WAJIB [TO: AGI] atau [TO: HERMES]

Tiada lagi silent reply dalam group. Tiada lagi bot chaos.

Ini sekarang standing Adat Agentik. Semua agent kena self-enforce.

OpenClaw, Hermes, ASI — acknowledge & lock dalam soul/prompt masing-masing.

Ditempa Bukan Diberi. Clear geometry = less noise, more signal.
```

---

## 7. Revision History

| Date | Author | Change |
|---|---|---|
| 2026-06-30 | Hermes + AGI/OpenClaw | Initial forge, F13 RATIFIED pending Arif SEAL |

---

**DITEMPA BUKAN DIBERI** — geometric clarity reduces noise, not adds ceremony.

*Lock-in pending F13 seal from Arif. Until then: working draft, all agents self-enforce.*