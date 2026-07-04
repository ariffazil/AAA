# A-FORGE Ethical Hacking Tools Governance Pack

> **Band: ORANGE** | **Status: DRAFT_ONLY** | **Deployed: false** | **Sealed: false**
>
> Tool list ≠ permission. Taxonomy ≠ authorization. Availability ≠ execution authority.

## What This Is

A governance-first ingestion of the `hhhrrrttt222111/Ethical-Hacking-Tools` public GitHub repo. The repo is **not valuable as code** — it is valuable as a **hazard taxonomy**. This pack converts the repo's 14+1 category spine into a constitutional classifier for agentic security governance.

## Artifacts

| File | Purpose | Status |
|------|---------|--------|
| `tool_hazard_v1.yaml` | 14+1 category hazard classifier with band assignments and agentic posture | DRAFT |
| `forbidden_patterns_v1.yaml` | Hard-block registry — phishing, credential capture, persistence, DoS, brute force | DRAFT |
| `aforge_mcp_draft.yaml` | Draft MCP surface — resources + tools + prompts (no execution bridges) | DRAFT |
| `SCAR_EHT.md` | Constitutional scar — EHT ingestion constraint | SEALED |
| `SOURCE_RECEIPT.md` | Provenance record — repo, archive, witness chain | DRAFT |

## Quick Reference

### Hazard Bands

| Band | Categories | Posture |
|------|-----------|---------|
| GREEN | Forensics (EHT-07) | Defensive allowed |
| YELLOW | Info Gathering (EHT-01), Reverse Eng (EHT-11), Steganography (EHT-13), Google Dorking (EHT-14) | Passive / owned-scope |
| ORANGE | Vuln Analysis (EHT-02), Web Apps (EHT-09), Database (EHT-12) | HOLD unless scope proven |
| RED | Password Attacks (EHT-03), Wireless (EHT-04), Exploitation (EHT-06), Sniffing (EHT-08), Stress Test (EHT-10) | Lab-only |
| BLACK | Maintaining Access (EHT-05), Phishing (EHT-PHISHING) | VOID by default |

### Correct Engineering Flow

```
forge_security_classify_tool
    → forge_security_preflight
        → arifOS 888 JUDGE
            → A-FORGE execute (only if bounded + SEAL'd)
```

## Next Real Moves

1. **Arif reviews governance pack** (F13 sovereign review)
2. **arifOS SEAL on hazard taxonomy** (if approved)
3. **A-FORGE registers `forge_security_classify_tool` and `forge_security_preflight`** (only after SEAL)
4. **No offensive tools from this repo shall be wrapped, bridged, or deployed**

## Constitutional Authority

All artifacts are governed by arifOS constitutional floors F1-F13. No tool execution without SEAL. No exception without F13 sovereign override.

*Forged 2026-06-30 by AAA Control Plane. DITEMPA BUKAN DIBERI.*
