# workflow-agent-onboarding — Execution Summary

> Generated: 2026-05-17 | Owner: arif-fazil | Version: 1.0.0

## Purpose

Onboard a new agent to the federation with full spatial grounding + constitutional binding.
Triggers: new agent detected, Arif command, federation membership request.

## Key Design Decisions

- **step-00 branching:** has existing spatial context → skip to constitutional binding.
- **Idempotent:** rerun skips completed gates. Safe to retry.
- **step-05 verification:** final check that spatial awareness is active before seal.

## Triggers

- New agent detected (new config file found)
- Arif command: 'onboard <agent>'
- Agent requests federation membership

## Gates

- `gates/step-00.json`: AGENT_DISCOVER — test -f <config_path>
- `gates/step-01.json`: SPATIAL_GROUNDING — grep '72.62.71.199\|SPATIAL_LAW' <config_path>
- `gates/step-02.json`: CONSTITUTIONAL_BINDING — grep constitution_hash artifacts/binding-receipt.json
- `gates/step-03.json`: SKILL_REGISTRY — grep agent_id wiki/entities/federation-entities.md
- `gates/step-04.json`: ADAPTER_GENERATION — test -f AAA/skills/<domain>/<agent_type>/SKILL.md
- `gates/step-05.json`: VERIFY_SPATIAL — grep spatial_aware_flag state.json
- `gates/step-06.json`: SEAL_TO_VAULT — grep entry_id state.json
