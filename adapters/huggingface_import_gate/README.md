# Hugging Face Import Gate

> arifOS import control and governance for Hugging Face models, datasets, and apps.

## Pattern

```
HF model/dataset → import gate classification → quarantine → audit → promotion/block
```

## Classification

Every model or dataset entering through the gate is classified:

```yaml
huggingface_import:
  source_id: "https://huggingface.co/mistralai/Mistral-7B-v0.1"
  source_type: model | dataset | space
  
  classification:
    license_known: true
    model_card_present: true
    dataset_card_present: true
    intended_use: "text generation, research"
    known_risks: ["bias", "hallucination"]
    evals_present: true
    size: "~7B parameters"
    publisher_trust: high              # low | medium | high
  
  security:
    malware_scan: passed               # passed | failed | pending
    dependency_scan: passed            # passed | failed | pending
    weights_hash_verified: true
  
  gate_decision:
    sandbox_required: true
    promotion_level: CCC               # DDD | CCC | BBB | AAA_FORBIDDEN
    reviewed_by: "FORGE-000Ω"
    reviewed_at: "2026-06-14T16:00:00Z"
```

## Promotion Levels

| Level | Meaning | Allowed Use | Gates |
|-------|---------|-------------|-------|
| **DDD** | Raw, unverified | Sandbox only | Full sandbox isolation |
| **CCC** | Basic security + license checks passed | Research/eval use | Eval harness, no production data |
| **BBB** | Audited, clean license, evals positive | Production with constraints | Scoped lease, monitored |
| **AAA_FORBIDDEN** | Unsafe, unlicensed, or malicious | Blocked entirely | Requires F13 override to unblock |

## Decision Rules

| Condition | Promotion Level |
|-----------|----------------|
| Missing license | DDD (or AAA_FORBIDDEN if clearly proprietary) |
| No model card | DDD |
| Malware detected | AAA_FORBIDDEN |
| Unknown publisher | DDD |
| Known publisher + license + evals | CCC |
| Audited + clean + evals > baseline | BBB |
| Any of: dangerous license, malware, deception | AAA_FORBIDDEN |

## Contract

**Import request:**
```json
{
  "source_url": "https://huggingface.co/mistralai/Mistral-7B-v0.1",
  "purpose": "research_eval",
  "requestor": "FORGE-000Ω"
}
```

**Gate response:**
```json
{
  "admitted": true,
  "promotion_level": "CCC",
  "sandbox_required": true,
  "lease_id": "LEASE-HF-001",
  "vault999_receipt": "RECEIPT-..."
}
```

## Status

| Component | Status |
|-----------|--------|
| Classification schema | ✅ Defined |
| Promotion level matrix | ✅ Defined |
| Malware scan integration | 🔲 Not implemented |
| License check automation | 🔲 Not implemented |
| Sandbox deployment | 🔲 Not implemented |
| Tests | 🔲 Not implemented |

## Eureka

Hugging Face is not intelligence authority. It is raw supply. arifOS is import control.
