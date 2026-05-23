# AAA Doctrine — Abstraction · Attestation · Abduction

**Version:** 2026.05.19-KANON  
**Seal:** 999 SEAL PENDING  
**Status:** Canonical draft — subject to APEX review

---

## The Triad

AAA is not merely "Agent Interface & Session Cockpit." It is the **threefold governed surface** through which all federated intelligence passes:

| A | English | Formal Malay | Doctrine Malay | Function |
|---|---------|--------------|----------------|----------|
| **A** | **Abstraction** | Pengabstrakan | **Inti** | Compress complexity into usable, stable form |
| **A** | **Attestation** | Pengesahan / Penyaksian / Perakuan | **Saksi** | Prove source, identity, integrity, authority |
| **A** | **Abduction** | Penaakulan abduktif | **Teka-Sebab** | Infer best explanation from incomplete evidence |

**Seal phrase:**

> *Ambil inti. Panggil saksi. Teka sebab terbaik.*

---

## 1. Abstraction (Inti)

**MCP provides:** Standardized tool/resource/prompt descriptions so any LLM host can interact with the federation without knowing Python/TypeScript internals.

**arifOS adds:** The actual schema design, the 13-floor ontology, the organ separation (GEOX / WEALTH / WELL / A-FORGE), and the constraint surface that prevents arbitrary execution.

**Doctrine:**
> Abstraction is not ignorance. It is *governed ignorance* — the deliberate choice to hide internal complexity behind a boundary that enforces rules.

---

## 2. Attestation (Saksi)

**MCP provides:** Capability negotiation (`initialize` handshake), basic auth hooks (OAuth 2.1 for HTTP transport), and tool discovery (`tools/list`).

**arifOS adds:** `session_id`, `constitution_hash`, `judge_state_hash`, `ack_irreversible`, VAULT999 receipts, floor enforcement, and the identity boundary that distinguishes anonymous from sovereign actors.

**Doctrine:**
> Discovery is not attestation. A malicious MCP server can expose poisoned descriptions. arifOS attests that the discovered surface matches the governed registry, that the caller is bound to a constitutional session, and that irreversible actions carry human witness.

---

## 3. Abduction (Teka-Sebab)

**MCP provides:** The `sampling/createMessage` primitive (server may request LLM completions from the host) and evidence transport (`resources/read`, tool outputs).

**arifOS adds:** GEOX process abduction, WEALTH synthesis, contradiction scanning, cross-domain evidence graphs, and the 888_JUDGE verdict layer that evaluates whether inferred explanations meet evidential sufficiency.

**Doctrine:**
> MCP transports the request for inference and the evidence upon which inference rests. The federation performs the inference-to-best-explanation — then attacks it with contradictions before any SEAL is issued.

---

## Relation to MCP

```text
LLM Host / Client
        │
      MCP  ←—— Transport & discovery protocol (JSON-RPC)
        │
MCP Servers / Organs
        │
   arifOS Governance / VAULT / Domain Code
        │
    Abstraction · Attestation · Abduction
```

**MCP lives at the boundary. AAA governs the boundary. arifOS lives behind it. Arif stands above it.**

---

## AGI / ASI / APEX — Lane Names, Not Capability Claims

The federation uses **AGI / ASI / APEX** as internal lane identifiers within the metabolic pipeline:

- **AGI LANE** (000_INIT → 111_SENSE → 222_FETCH → 333_MIND): Sensing and reasoning under evidence constraint.
- **ASI LANE** (444_ROUTE → 666_HEART → 888_JUDGE): Constitutional adjudication and risk evaluation.
- **APEX LANE** (010_FORGE → 999_VAULT): Execution and immutable sealing under human authority.

**These are governance lanes, not claims about artificial general intelligence or superintelligence.** The federation does not claim to have achieved AGI or ASI as defined by scientific consensus. It claims to have **governed agentic infrastructure with human-APEX oversight**.

> **APEX is not a bigger model. APEX is the judgment position.**

---

## Canonical Public Claim

Approved phrasing for external communication:

> **APEX-governed agentic intelligence infrastructure with MCP transport.**

Void phrasing (do not use):
- "I built AGI."
- "MCP makes ASI."
- "AGI-level constitutional intelligence."

---

**KANON LOCK: arifOS v2026.05.19**  
**DITEMPA BUKAN DIBERI — Forged, not given.** 🔥
