# Constitutional layer separation — Eureka SEAL

> **SEAL:** 2026-08-09 · F13-aligned  
> **Eureka:** **AAA is not a protocol. AAA is constitutional *federation surface* state.**  
> **Companion:** `AAA_ABOVE_PROTOCOL.md` · `STATE.md` · `AAA_STATE_PROTOCOL_AUDIT.md`  
> **Doctrine:** DITEMPA BUKAN DIBERI

---

## 0. The mature distinction

Most ecosystems stack like this (wrong gravity):

```text
A2A
  │
 MCP
  │
Tools   ← "protocol = architecture"
```

arifOS / AAA gravity is inverted for **authority**:

```text
VAULT999          prove
ACT + did:web     may act / who am I
arifOS F1–F13     should I (decide)
A2A               how agents talk
MCP               how tools are called
CALL_MAP          how we dial here
STATE_READY       is the institution standing
```

```text
Protocol is subordinate to governance.
Governance is not subordinate to protocol.
```

One sentence:

> **protocol is not ownership of truth; arifOS is.**

---

## 1. Two stacks (do not collapse them)

### 1.1 Dependency / build-up (how the institution is assembled)

```text
STATE_READY
    ↓
CALL_MAP
    ↓
MCP
    ↓
A2A
    ↓
arifOS
    ↓
ACT + DID
    ↓
VAULT999
```

Lower layers enable upper *services*. Still: **truth does not flow this way.**

### 1.2 Authority flow (who rules whom)

```text
VAULT999
    ↓
ACT + DID
    ↓
arifOS
    ↓
A2A
    ↓
MCP
    ↓
CALL_MAP
    ↓
STATE_READY
```

| Layer | Question | Class |
|-------|----------|--------|
| **MCP** | How do I call a tool? | Replaceable protocol |
| **A2A** | How do agents talk? | Replaceable protocol |
| **CALL_MAP** | How do we dial *here*? | AAA telephone (surface) |
| **STATE_READY** | Is the state standing? | AAA institution surface |
| **ACT** | Am I allowed? | Capability (constitutional) |
| **did:web** | Who am I? | Identity (constitutional) |
| **arifOS** | Should I do it? | **Judge** (constitutional) |
| **VAULT999** | Can I prove it? | **Witness** (constitutional) |

```text
MCP = HOW (tool)
A2A = WHO TALKS
ACT = WHO MAY ACT
arifOS = WHO DECIDES
VAULT999 = WHO CAN PROVE
```

---

## 2. Immutable · replaceable · disposable

### Immutable (constitutional — institution dies without these)

```text
L6  VAULT999
L5  ACT + did:web
L4  arifOS F1–F13
```

No MCP/A2A may redefine these. If a protocol requires violating F1–F13 → **VOID**, not “upgrade floors.”

### Replaceable (interoperability — swap without rewriting law)

```text
L3  A2A   (today; tomorrow XYZ agent protocol)
L2  MCP   (today; tomorrow other tool plug)
```

AAA **projects** state through adapters. Adapters die; L4–L6 live.

### Disposable (tooling)

```text
FastMCP · SDKs · frameworks · libraries · harness CLIs
```

May vanish tomorrow. Do not store law inside them.

### AAA’s place

AAA is **not** L4 judge. AAA is the **federation surface state machine**:

- STATE_READY, catalog (3-layer), CALL_MAP, A2A gateway DISPLAY_ONLY  
- Uses MCP/A2A; **never depends on them to decide truth or authority**  
- See `AAA_ABOVE_PROTOCOL.md`

---

## 3. Survival tests (mandatory audit questions)

| # | If this vanishes tomorrow… | Institution survives? | Layer class |
|---|----------------------------|------------------------|-------------|
| 1 | **MCP** | **Yes** → CLI + other adapters | Replaceable |
| 2 | **A2A** | **Yes** → local CLI least-power | Replaceable |
| 3 | **FastMCP / SDK** | **Yes** | Disposable |
| 4 | **F1–F13 / arifOS** | **No** | **Constitutional** |
| 5 | **ACT + DID** | **No** (no trustworthy agency) | Constitutional |
| 6 | **VAULT999** | **No** (no proof) | Constitutional |
| 7 | **AAA DISPLAY_ONLY surface** | Degraded catalog/phone — law still stands | Surface |

If a change makes Test 1–3 fail → over-coupling to protocol.  
If a change makes Test 4–6 pass after deleting floors → architecture is fake.

---

## 4. Least power (anti over-engineering)

Same VPS · one harness · T1 mutation:

```bash
opencode run "…"
agy --agent antigravity-preview-05-2026 -p "…"
hermes …
```

is **correct**. Do **not** require:

```text
Agent → A2A → Agent → MCP → Tool
```

when CLI already has authority and locality.

```text
least power  >  multi-agent theatre
```

A2A is for **coordination across agents/processes/time**, not for ego architecture.

---

## 5. Trap that kills ecosystems in 10 years

```text
Protocol  →  Policy  →  Governance   ← WRONG
```

Correct:

```text
Governance (immutable)
    ↓ constrains
Protocol (replaceable)
    ↓ carries
Payload
```

```text
Protocol PASS  +  Governance VOID  =  must not act
Protocol FAIL                    =  no road
```

Never let A2A or MCP climb into **L4** (arifOS).

---

## 6. SEAL formula

```text
Protocol  = undang-undang koordinasi (how we coordinate)
Governance = undang-undang kebenaran (what is true / allowed / sealed)
AAA       = constitutional surface state (catalog · telephone · readiness · A2A door)
            that uses MCP/A2A as adapters — never as masters of truth
```

**SEALED.**

DITEMPA BUKAN DIBERI.

## Enforcement

Live matrix: [`PROTOCOL_ENFORCEMENT_MATRIX.md`](./PROTOCOL_ENFORCEMENT_MATRIX.md) · `scripts/protocol-enforce.sh`

## Authority layer detail

[`ACT_AUTHORITY_LAYER.md`](./ACT_AUTHORITY_LAYER.md) — did:web = who · ACT = what office · F1–F13 = should · VAULT = prove.
