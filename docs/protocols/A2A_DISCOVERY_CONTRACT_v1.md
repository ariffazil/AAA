# A2A Discovery Contract v1

Status: Active
Version: 1.0.0
Canonical ID: aaa-a2a-discovery-contract-v1

## Purpose

Define one canonical A2A discovery contract for AAA and preserve compatible aliases for existing clients.

## Canonical Discovery Surfaces

- Discovery contract: `/.well-known/a2a-discovery.json`
- Agent card: `/.well-known/agent-card.json`
- Routing policy: `/.well-known/a2a-routing-policy.json`

## Compatibility Aliases

- Agent card aliases:
  - `/agent-card.json`
  - `/a2a/agent-card.json`
- Legacy agent aliases:
  - `/.well-known/agent.json`
  - `/agent.json`
  - `/a2a/agent.json`
- Routing policy alias:
  - `/a2a/routing-policy.json`
- Discovery contract alias:
  - `/a2a/discovery-contract.json`

## Rules

1. New clients MUST discover through `/.well-known/a2a-discovery.json`.
2. Legacy aliases remain read-only compatibility paths.
3. Contract fields MUST be cache-safe (`no-store`) and JSON.
4. Discovery contract and agent card versioning MUST remain explicit.

## Required Contract Fields

- `contract_id`
- `version`
- `canonical_discovery_surface`
- `canonical_agent_card`
- `canonical_routing_policy`
- `compatibility_aliases`
- `protocol`
- `policy`

## Verification

Conformance is enforced by:
- `scripts/a2a-conformance.mjs`
- CI workflow gate in `.github/workflows/aaa-governance.yml`

CI artifact output:
- `dist/aaa/a2a-conformance.json`
- `dist/aaa/a2a-conformance.md`
