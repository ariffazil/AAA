# NAMESPACE: governance

> **Marker file** (added 2026-09-19, Fasa 1 skill hygiene).
> This directory is a *namespace*, not a skill.
> Skills live in the subdirectories listed below.

## Purpose
This namespace groups related skills under one roof for discovery and routing.
Each subdirectory is an independent skill with its own SKILL.md.

## Contained skills (20)
- `apex-gate-evaluator`
- `apex-verdict`
- `capability-addressing`
- `capability-surface-conformance`
- `claim-ledger-integrity`
- `control-reality-audit`
- `durable-artifact-authoring`
- `durable-claim-ledger`
- `external-review-intake`
- `federation-memory-writeback`
- `first-party-corpus-audit`
- `institutional-language-audit`
- `model-score-disclosure`
- `public-claims-maintenance`
- `publication-risk-audit`
- `sealed-deliverable-provenance`
- `sensitive-publication-governance`
- `site-traffic-reality`
- `staged-write-triage`
- `symbol-namespace-integrity`

## Owner

**Owner:** `AAA/governance`

_Single-writer policy (Fasa 2): owner has write authority; other layers can read but not edit._

## Conventions
- Do not edit skill SKILL.md files from this namespace layer.
- To add a new skill: create subdirectory with SKILL.md, then add to FEDERATED_SKILLS_REGISTRY_V3.yaml.
- To deprecate: rename subdir to `<name>.DEPRECATED-<date>`, do not delete.
