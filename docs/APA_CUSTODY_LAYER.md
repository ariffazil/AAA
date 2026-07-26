# APA Custody Layer — Canonical Specification

> **DITEMPA BUKAN DIBERI** — Forged, Not Given
> **Status:** CANONICALLY RATIFIED 2026-07-26
> **Authority:** 888_JUDGE · F13 SOVEREIGN
> **Layer:** A-FORGE Execution Shell (Ψ)
> **Pipeline:** ART → KERNEL → APA → ACT → VAULT999

---

## 0. Identity

**APA (Action-Permission-Adapter)** is the safe handoff and custody wrapper that converts a KERNEL SEAL verdict into a bounded, lease-gated execution package before A-FORGE touches physical reality.

APA is not thinking. APA is not judging. APA is not acting. APA is the **constraint bridge** between judgment and execution.

```
arif_judge says: "Permission granted."
APA says:        "Through which controlled door, under what lease, with what limits?"
ACT says:        "Executing now."
VAULT999 says:   "Recorded forever."
```

---

## 1. Pipeline Position

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   ART    │ ──> │  KERNEL  │ ──> │   APA    │ ──> │   ACT    │ ──> │ VAULT999 │
│ (Sees)   │     │ (Permits)│     │(Constrains)│   │ (Moves)  │     │(Remembers)│
└──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
```

| Stage | Organ | Role | Question |
|-------|-------|------|----------|
| **ART** | Perception | Classifies action class | "What is this?" |
| **KERNEL** | arifOS (Ω) | Judges against F1–F13; emits SEAL/HOLD | "May this happen?" |
| **APA** | A-FORGE (Ψ) | Wraps in lease, manifest, bridge, blast radius | "How do we touch reality safely?" |
| **ACT** | A-FORGE Actuator | Executes bounded manifest | "Can I execute this exact envelope?" |
| **VAULT999** | Proof Anchor | Appends immutable receipt | "What did we do forever?" |

---

## 2. The 8 Invariant Checks

Before handing any payload to ACT, APA enforces:

| # | Check | Meaning |
|---|-------|---------|
| 1 | **Verb Class** | OBSERVE / MUTATE / IRREVERSIBLE |
| 2 | **Blast Radius** | Scope of impact (file, repo, person, broadcast) |
| 3 | **Reversibility (F1)** | Rollback exists? If no → F13 human gate |
| 4 | **Bridge Routing** | email / calendar / github / telegram |
| 5 | **Lease Allocation** | Time-bounded, single-use execution token |
| 6 | **Manifest Schema** | Payload validated against static schema |
| 7 | **Envelope Discipline** | Strips LLM prose; passes typed argument structs |
| 8 | **Receipt Readiness (F11)** | Pre-formats VAULT999 receipt for post-execution hash |

---

## 3. The 4 Bridges

| Bridge | Port | Protocol | systemd Unit | F13 Gate? |
|--------|------|----------|-------------|-----------|
| **Email** | 18093 | IMAP/SMTP | `apa-email-bridge.service` | No |
| **Calendar** | 18094 | CalDAV | `apa-calendar-bridge.service` | No |
| **GitHub** | 18095 | REST API | `apa-github-bridge.service` | No |
| **Telegram** | 18096 | Bot API | `apa-telegram-bridge.service` | **Yes — F13 veto lane** |

All bridges return `apa_version: "1.0"` in `/health`. All bind `127.0.0.1` only.

---

## 4. Execution Flow

```
Sealed Intent
    │
    ▼
APA wraps:
    ├── Lease (who, how long, scope)
    ├── Manifest (exact payload, schema-validated)
    ├── Bridge selection (email/calendar/github/telegram)
    ├── Blast radius (what can be affected)
    └── Reversibility vector (rollback path)
    │
    ▼
ACT executes bounded manifest through selected bridge
    │
    ▼
VAULT999 appends immutable receipt
```

---

## 5. Relation to APEX T-000

APA is the **execution-side complement** to APEX's governance calculus:

- **APEX** measures whether intelligence *deserves* permission (G = GM(A,P,E,X))
- **APA** constrains *how* permitted action touches reality (lease + manifest + bridge)

Together they form the complete governed-execution surface: **APEX gates the SEAL; APA gates the ACT.**

---

## 6. Live Verification

```bash
# All 4 bridges should return apa_version: "1.0"
for port in 18093 18094 18095 18096; do
  curl -s http://127.0.0.1:$port/health | jq .apa_version
done

# All 4 systemd units should be active
systemctl status apa-email-bridge apa-calendar-bridge apa-github-bridge apa-telegram-bridge
```

---

*DITEMPA BUKAN DIBERI — APA = the governed bridge. After SEAL, before ACT.*
