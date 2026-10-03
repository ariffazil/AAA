# DIRECTIVE — KVM4 Archive-Branch Sync (F13 APPROVED)

> **Decision:** F13 binary T6 — **LULUS SYNC** · **By:** Arif (via FI-008 structured prompt, sesi `SEAL-9c657ad6a0184085`, trace `trc-7f8bf21c7b9b`) · **Date:** 2026-10-03 ~11:20 MYT · **Executor:** IRFANclaw (KVM4)
> **Status:** F13_APPROVED 2026-10-03 — Arif answered the structured binary directly ("Lulus sync"); instrument = tarikh + sesi SEAL-9c657ad6a0184085

## What is authorized
Resolve KVM4 ↔ origin divergence on all three repos (AAA · A-FORGE · arifFlow) using the **archive-branch path**:

1. Fresh `git fetch origin` on each repo (Scar-2026-10-03-001 — no stale-ref reads).
2. Push local-only commits to archive branches: `kvm4/wip-2026-10-03-<repo>` — **no work lost**.
3. Reset/rebase working branch to `origin/main` per repo.
4. Verify each with `git ls-remote` + report SHAs (Scar-2026-10-03-002 — "pushed" only with remote proof).

## Constraints
- **No force push. No history rewrite on shared branches. No deletion of local commits.**
- KVM4 local AAA ahead-26 content: if any commit carries real work, flag it in the sync report instead of silently archiving.
- Report back with per-repo before/after SHAs; this file gets a completion addendum or a linked receipt.

## Context
Round 5 cross-audit found all three KVM4 repos diverged from origin (AAA ahead 26/behind 2836 · A-FORGE ahead 2/behind 195 · arifFlow ahead 1/behind 45 — behind-counts grew after KVM8 pushes landed 2026-10-03 morning). `pull --ff-only` will **fail** — do not attempt it.
