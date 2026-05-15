# Copilot Snapshot Attestation

**Repo:** AAA
**Role:** agent workspace / control plane anchor
**Status:** redacted, safe-to-commit snapshot

## Attestation

This repository is the GitHub snapshot that agents should use as the AAA source-of-truth anchor for workspace context.

Machine-local Copilot runtime config is **not** committed here. It stays in `~/.copilot/` on the machine.

## What is captured in Git

- AAA repo-level Copilot instructions
- AAA public agent registry (`public/a2a/agents.json`)
- AAA control-plane context
- repo-specific workspace conventions
- safe abstractions only, no secrets

## What is not captured in Git

- tokens
- API keys
- private environment values
- machine-local only config files
- secret-bearing `.copilot` directories

## Current approved non-secret surface

- Copilot runtime anchor: `~/.copilot/` (machine-local)
- AAA repo anchor: `.github/copilot-instructions.md`
- AAA live registry: `public/a2a/agents.json`
- Approved MCP names: `arifOS`, `geox`, `wealth`, `well`, `playwright`
- Approved LSP names: `python`, `typescript`, `yaml`

## Rule

If a file would leak credentials, private URLs, or machine-local runtime state, do not commit it. Redact it or keep it outside the repo.

DITEMPA BUKAN DIBERI — abstraction first, amanah first.
