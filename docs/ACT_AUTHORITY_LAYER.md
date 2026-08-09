# ACT_AUTHORITY_LAYER

> **Sealed:** 2026-08-09T06:10:00+08:00
> **Author:** ARIF (F13 Sovereign)
> **Witness:** Hermes Agent (hermes-asi)
> **Classification:** SOVEREIGN CONSTITUTIONAL — F13 ratification
> **Epistemic:** INT (architectural truth from sovereign reasoning)
> **Amends:** CONSTITUTIONAL_SEPARATION_AXIOM.md (L5 detail)

---

## The Layer

did:web is not communication. ACT is not communication. They are **authority layers**.

| Layer | Question | Function |
|-------|----------|----------|
| MCP | **How** do I call? | Communication |
| A2A | **Who** do I talk to? | Communication |
| did:web | **Who** am I? | Identity |
| ACT | **What** may I do? | Authority |
| arifOS F1-F13 | **Should** I do it? | Governance |
| VAULT999 | Can I **prove** it? | Evidence |

---

## did:web = Identity

did:web establishes cryptographically verifiable identity.

```
did:web:arif-fazil.com:aaa
did:web:arif-fazil.com:hermes
did:web:arif-fazil.com:a-forge
```

Without did:web: `"trust me bro"`
With did:web: cryptographically identifiable actor

---

## ACT = Authority

After identity is known, ACT binds identity to permitted capabilities.

```
{
  "actor": "did:web:arif-fazil.com:hermes",
  "capability": "research"
}
```

Permitted.

```
{
  "actor": "did:web:arif-fazil.com:hermes",
  "capability": "seal"
}
```

**Denied.**

Because: Research ≠ Judge.

---

## The Separation of Powers

ACT enforces the separation of powers:

| Actor | Allowed |
|-------|---------|
| 333-AGI | Propose |
| 555-ASI | Verify |
| 888-APEX | Judge |
| A-FORGE | Execute |
| VAULT999 | Witness |

333 trying to SEAL → `ACT DENY`

Even though the message arrived via valid A2A, valid MCP, valid JSON-RPC.

---

## The Authority Enforcement Chain

Without ACT: Identity → Action (direct, ungoverned)

With ACT:

```
Identity (did:web)
    ↓
Capability Check (ACT)
    ↓
Authority Check (arifOS F1-F13)
    ↓
Action (Execution)
    ↓
VAULT999 Receipt (Evidence)
```

---

## The 403 Proof

```
Hermes → AAA: "SEAL this action"

Step 1: did:web
  Who sent this?
  → did:web:arif-fazil.com:hermes ✅

Step 2: ACT
  What rights does Hermes have?
  → READ, RESEARCH, OBSERVE ✅

Step 3: Request
  SEAL this action

Step 4: ACT Check
  Does Hermes possess SEAL authority?
  → NO ❌

Result: 403 AUTHORITY DENIED
```

Even though:
- A2A valid ✅
- MCP valid ✅
- JSON-RPC valid ✅

**Authority still fails.**

---

## The arifOS Interpretation

| Layer | Constitutional Question |
|-------|------------------------|
| did:web | *"Who are you?"* |
| ACT | *"What office do you hold?"* |
| F1-F13 | *"Should that office be allowed to do this?"* |
| VAULT999 | *"Can we prove it later?"* |

---

## Compact Form

> **did:web** establishes identity,
> **ACT** binds identity to permitted capabilities,
> **arifOS F1-F13** judges whether the requested action is constitutionally allowed,
> and **VAULT999** records evidence that the decision occurred.

---

*DITEMPA BUKAN DIBERI.*
