# AAA Workflow Contracts

This directory defines the execution-layer contracts for AAA workflows.

## Rule

- `registries/workflows.yaml` is the compact workflow index used by bundles and agents.
- `contracts/workflows/contracts.yaml` is the detailed execution contract catalog.
- every workflow in the registry must resolve to a workflow contract with the same canonical ID.

## Contract responsibilities

Each workflow contract must declare:

1. trigger mode and preconditions
2. required witnesses and separation of duties
3. step-level required skills, tools, servers, holds, retries, and approval hooks
4. rollback strategy for failure or rejection paths
5. emitted events for observability and replay

## Invariant

If AAA can execute or delegate a workflow, AAA must be able to explain how it is
approved, retried, rolled back, and audited.
