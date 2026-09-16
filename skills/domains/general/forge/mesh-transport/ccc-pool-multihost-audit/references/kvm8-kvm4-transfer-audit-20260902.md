# KVM8 ↔ KVM4 CCC Transfer Audit — 2026-09-02

Session: Arif asked "contrast analysis of CCC FI coding agent in KVM8 and
KVM4 — any remaining agents or cards not complete transfer yet?"

## Verdict at audit time

Core 5-harness transfer COMPLETE and healthy. Half-migrated: grok, antigravity.
Card registry stale for individuals. Minor repo/overlay drift.

## Fully transferred (all axes green)

| Harness | KVM8 ver | KVM4 ver | Probe | Notes |
|---|---|---|---|---|
| opencode | 1.18.11 | 1.18.26 | OPENCODE-KVM4-OK PASS | rules/ overlay present on KVM4 |
| codex | 0.149.1 | 0.152.0 | CODEX-KVM4-OK PASS | no AGENTS.md overlay on KVM4 |
| qwen | 0.22.2 | 0.22.3 | QWEN-KVM4-OK PASS | no AGENTS.md overlay on KVM4 |
| kimi | (older) | 0.39.1 | KIMI-KVM4-OK PASS | config.toml → fed-gateway/forge-777 |
| aider | 0.86.2 | 0.86.2 | AIDER-KVM4-OK PASS | gateway flags auto-injected by ccc-remote |

All KVM4 harness configs route via http://100.64.0.2:4000 (haproxy auth
injection, zero local secrets). KVM4 versions NEWER than KVM8 same day.

## Half-migrated

- **grok** — binary on KVM4 (/usr/local/bin/grok → /root/.grok/bin/grok,
  symlink dated 2026-09-02) but: no `ccc-remote` case entry, not in
  kvm4-ccc-pool.json, never probe-marked.
- **antigravity (agy)** — `ccc-remote` accepts `agy` (BOOT path
  /root/.local/bin) and binary exists on KVM4, but no `~/.antigravity`
  config dir; not in pool card; never probe-marked.

## KVM8-only by design (not defects)

claude (/root/.local/bin/claude), gemini (/usr/bin/gemini), copilot,
continue-cli (cn), openclaw. Cards exist on KVM8 for each.

## Card registry findings (KVM8 AAA/a2a-server/agent-cards/harnesses/)

- `kvm4-ccc-pool.json` — registered 2026-09-02, correct (5 harnesses, FED
  routing, attestation KVM4-CCC-ATTESTED-20260902, 8/8 zen scorecard).
- Individual cards (opencode.json, codex.json, qwen-code.json, kimi-code.json,
  aider.json, grok-build.json, antigravity.json, etc.) — still describe KVM8
  binary paths only, zero KVM4 mention (grep confirmed only kvm4-ccc-pool.json
  references 100.64.0.5). Router reading individual cards mis-routes.
- KVM4 has NO a2a-server dir — registry is KVM8-only by architecture.

## Repo / governance drift

- KVM4 AAA repo behind origin/main by 1 commit (4d97b41 "pre-migration
  registries") at audit time; KVM8 HEAD = 4d97b418 clean.
- Skills: KVM8 218 vs KVM4 214 (4-skill delta).
- KVM4 AGENTS.md is a proper CCC-worker-node rewrite (execution-only, never
  judge) — good.
- KVM4 kimi config.toml has 0 [mcp_servers] (KVM8 codex has 11) — workers
  intentionally lean; MCP organs stay on KVM8.

## Probe technique notes

- One SSH call batching multiple probes beats per-command SSH (a 120s timeout
  hit when version checks ran unbatched with kimi --version hanging).
- `timeout 30 <cli> --version` mandatory for node CLIs under load.
- KVM4 skills dir includes fi-mesh-check, fi-qwen-upgrade, fi-zai-probe —
  FI skills already mirrored.

## Open gaps offered to Arif (single pass)

1. Add grok + agy to ccc-remote case list (or explicitly descope).
2. Probe-mark grok/agy if kept; add to pool card.
3. Update 5 individual harness cards with KVM4 routing note.
4. `git pull` KVM4 AAA to HEAD; reconcile 4-skill delta.

Awaiting F13 green light — not executed in this session.
