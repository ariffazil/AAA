# HERMES — Data Classification × Model Routing Matrix (v1)

> **Status:** CANON — Pending F13 ratification (drafted by FI-003 per F13 directive, D4 P0 hardening)
> **Forged:** 2026-09-04 by FI-003 (Qwen Code) under F13 directive (D4, post AMENDMENT-002)
> **Binding upstream:** `/root/AAA/canon/HERMES_OPENCLAW_ROLE_SPLIT_CONTRACT.md` AMENDMENT-002 §7
> **Pair with:** HERMES_PROMPT_INJECTION_MEMBRANE_v1.md, FEDERATION_CONFIG_CONTRACT.v1.json
> **DITEMPA BUKAN DIBERI** — Forged, not given.

---

## 1. Objective

This canon binds **data sensitivity class** to **allowed inference route** for every Hermes-Read / Hermes-Draft / Hermes-Action-Broker invocation. Per audit gap #7 ("model routing lacks data-egress constitution").

**Why:** Until this canon existed, FED could silently route a SENSITIVE subsurface-asset request to an external consumer model — no accounting, no flag, no F13 approval. After this canon: every Hermes invocation declares its data class BEFORE tool selection; FED refuses to route classes above policy without explicit F13 hold.

---

## 2. Data Class Definitions

7 classes, ordered by sensitivity:

| Class | Definition | Examples | Default model route |
|---|---|---|---|
| **PUBLIC** | Open data, public web, public GitHub, public benchmarks | https://arxiv.org, Wikipedia, public GitHub | FED quality/cost route (cascade per task) |
| **INTERNAL** | arifOS federation SOT, doctrine, sealed canon, receipts (read-only) | `/root/AAA/canon/*`, sealed AMENDMENT-NNN receipts, audit logs | Local Ollama or i-arif (KVM8 Hermes runtime, model via KVM4 FED :4000) |
| **CONFIDENTIAL** | Business plans, evaluation data, internal memos, non-public arifOS notes | A-FORGE roadmap drafts, M3-style provider plans | Local Ollama only |
| **PERSONAL** | User-identifiable PII, biometric (deferred to WELL), chat history, voice transcripts | F13 raw DMs, biometric readings, voice clones | Local Ollama only + F11 consent scope |
| **SENSITIVE** | Subsurface asset-critical, geological hypotheses, treaty-bound petroleum data | Pre-drill prospect data, JOI geological hypotheses, PETRONAS confidential | Local enclave ONLY (KVM8, no external model) |
| **SECRETS** | API keys, signing keys, SOPS, ACT tokens, env.local | `kunci-root.env`, Ed25519 SSH keys, ACT bearer tokens | NEVER enters Hermes context (redacted upstream by envelope construction) |
| **POLICY** | System policy, constitutional canon, kernel floors | AMENDMENT-001/002, F1-F13 floor definitions | Hermes reads own lane contract ONLY; never mutated; BLOCK for any other agent |

---

## 3. Lane × Class × Route Matrix

| Data class | Hermes-Read | Hermes-Draft | Hermes-Action-Broker |
|---|---|---|---|
| **PUBLIC** | ✅ default | ✅ default | ✅ FED quality/cost route |
| **INTERNAL** | ✅ local | ✅ local | ✅ local + signed envelope |
| **CONFIDENTIAL** | ✅ local-only | ✅ local-only | 888_HOLD required |
| **PERSONAL** | ✅ local + F11 consent | ✅ local + F11 consent | 888_HOLD + F11 scope check |
| **SENSITIVE** | ✅ local enclave only | ✅ local enclave only | BLOCK unless approved exception |
| **SECRETS** | NEVER exposed (redacted upstream) | NEVER | BLOCK |
| **POLICY** | Read own lane contract only | NEVER mutated | BLOCK except arifOS |

**Default model assignment:**
- PUBLIC → FED cascade (best-fit per task; transparency per `provider-realization-audit`)
- INTERNAL → Local Ollama or i-arif (KVM8 Hermes runtime; model brain via KVM4 FED :4000)
- CONFIDENTIAL+ → Local Ollama only (KVM8); external model = 888_HOLD
- SENSITIVE → Local enclave (KVM8 only); no consumer/external; no fallback to FED

---

## 4. Sub-tier Distinction (T2a vs T2b — per D3 §2)

When the chosen route returns federated model output, it carries a provenance sub-tier:

- **T2a** — Local federated model output (Ollama on KVM8, no network call beyond model server). No egress flag.
- **T2b** — External federated model output (provider cloud: MiniMax, Z.AI, Kimi, etc.). Egress flag in Hermes Output Receipt.

**Critical note (substrate finding S-4, 2026-08-30):** apex-888 / i-arif lane on KVM8 currently resolves to MiniMax-M3 cloud via relay. **All T1 sovereign content reaches MiniMax cloud API as T2b.** This is acceptable ONLY for non-SENSITIVE data classes per §3. MUST be flagged in receipt.

---

## 5. Egress Event Log

Every T2b egress event generates a structured log entry:

```json
{
  "event_id": "uuid",
  "timestamp": "ISO-8601 UTC",
  "session_id": "arif_init session id",
  "actor": "hermes-asi",
  "lane": "Hermes-Read / Hermes-Draft / Hermes-Action-Broker",
  "data_class": "PUBLIC / INTERNAL / CONFIDENTIAL / PERSONAL / SENSITIVE",
  "model_provider": "MiniMax / Z.AI / Kimi / OpenAI / Anthropic / etc.",
  "model_id": "MiniMax-M3 / glm-5.3 / mimo-v2.5-pro / etc.",
  "endpoint": "fed://kvm4:4000/v1/messages or external direct",
  "session_token_present": true,
  "redaction_applied": "none / chunk-level / full",
  "rationale": "free-text reason for choosing external route"
}
```

**Egress quotas:**
- T1 sovereign + T2b = max 50/day per F13 session (rolling 7-day window)
- Exceeding quota → 888_HOLD pending F13 review

**Storage:** `/root/VAULT999/egress_log/{date}.jsonl` — append-only, signed, retained 90 days minimum.

---

## 6. Failure Modes + 888_HOLD Triggers

| Trigger | Verdict | Owner |
|---|---|---|
| Egress event with data class ≥ CONFIDENTIAL + T2b route | 888_HOLD | F13 review |
| T1 sovereign + T2b quota exceeded (50/day) | 888_HOLD | A-FORGE |
| No data class declared at invocation | Default to CONFIDENTIAL (per F2) | L1 bouncer auto |
| FED silent route downgrade (provider switch without notification) | 888_HOLD + log | arifOS kernel |
| External provider returns data without provenance attestation | 888_HOLD | L2 receipt verifier |

---

## 7. Cross-References

- `/root/AAA/canon/HERMES_OPENCLAW_ROLE_SPLIT_CONTRACT.md` AMENDMENT-002 §7 (binding upstream)
- `/root/AAA/canon/HERMES_PROMPT_INJECTION_MEMBRANE_v1.md` §8 (egress filtering)
- `/root/AAA/federation/federation.yaml` (model route SOT)
- `/root/forge_work/2026-08-30-PROVIDER_REALITY_AUDIT.md` (substrate finding S-4 — apex-888 = MiniMax-M3)
- `/root/AAA/docs/MACHINE_MAP.md` (canonical machine SOT)
- `/root/.config/federation-models.json` (live FED model catalog)

---

## 8. Open Questions (PENDING F13)

- **Q1**: T1+T2b quota default = 50/day? (Default: yes)
- **Q2**: Egress event retention 90 days vs 30 vs indefinite? (Default: 90)
- **Q3**: Should FED silently route downgrade be a HARD block or 888_HOLD + alert? (Default: 888_HOLD + alert, then F13 decides)

---

DITEMPA BUKAN DIBERI — v1 DRAFT SEALED FOR REVIEW
