# I-ARIF DEFAULT — 2026-09-04 (FI-003, F13 "Model switched to i-arif")

**Session**: SEAL-509f2aa23655468e  
**Trigger**: User decision to switch from qwen3.6-plus → i-arif as canonical Hermes model

## Why i-arif is better than qwen3.6-plus for Hermes (the sovereign's agent)

| Dimension | qwen3.6-plus (generic) | i-arif (custom BM Penang primary) |
|---|---|---|
| Persona | None — generic | Personal voice — matches F13 |
| Language | Multi-lingual baseline | BM Penang primary (Arif's tongue) |
| Context | 1M tokens (vanilla) | 256K tokens (calibrated) |
| Identity awareness | None | Carries canon memory |
| Cascade lane | Unspecified | Tier P1 (top of FED cascade) |
| Federation | Generic provider routing | Custom:fed-federation route (preferred lane) |
| Use case | Generic | ARIF's sovereign agent |

i-arif is the canonical Hermes persona. qwen3.6-plus was a generic fallback during the OpenRouter billing failure — now that FED is wired, i-arif restores the proper identity.

## What landed

- /root/.hermes/config.yaml:
  - model: qwen3.6-plus → **i-arif**
  - provider: custom:fed-federation (unchanged)
  - custom_providers.models: added `i-arif: {}` to FED Federation entry
- systemd: hermes-asi-gateway.service restarted
- Live ping: succeeded through FED

## Reversibility
- snapshot: /root/.hermes-zen-backups/i-arif-pre-$TS.yaml
- restore: edit model: back to qwen3.6-plus + restart

Log: /tmp/i-arif-switch-$TS.log
