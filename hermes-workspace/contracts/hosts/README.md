# AAA Host Contracts

This directory defines the machine-readable adapter layer between AAA and the hosts
that actually run agents, expose tools, or consume generated config.

## Rule

- `registries/hosts.yaml` is the compact index used by other registries.
- `contracts/hosts/contracts.yaml` is the detailed source contract for runtime behavior.
- host summaries in the registry must match the corresponding detailed contract entry.

## Current host families

- `gateway` - OpenClaw-facing routing and export surface
- `cli` - terminal-native operators such as Copilot CLI, Codex, Gemini CLI, and OpenCode
- `ide` - editor-hosted agent surfaces such as Claude Code and Cursor
- `domain-witness` - bounded domain ACP hosts for GEOX and WEALTH

## Invariant

If a host appears in `registries/hosts.yaml`, AAA must describe:

1. where its config lives
2. how AAA installs or generates artifacts for it
3. which transports and protocols it may use
4. what approval profile caps its risk
5. when arifOS judgment or vault sealing is mandatory
