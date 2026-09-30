---
name: agi-deep-research-loop
description: "USE WHEN running a deep-research task inside an arifOS/Codex harness that must close with VERIFIED evidence (code executed, result measured) and a sealed receipt — not just a cited report. Also load when someone proposes adding a new research or sandbox vendor/plugin/MCP to Codex (E2B, Daytona, Modal, etc.) to decide whether it is a real gap or a duplicate."
license: MIT
metadata:
  author: 333-AGI (arifOS federation)
  version: "1.0.0"
  homepage: https://arif-fazil.com
  note: "Pointer skill — capability lives in the substrate (arifOS kernel + A-FORGE + firecrawl). No new vendor."
---

# AGI Deep Research Loop (research → verify → judge → seal)

Satu masalah. Satu owner. Satu jalan. No new vendors.

## The problem this solves

Arif asked: "deep research must have plugins for Codex." The answer is NOT a
new plugin — the capability already exists across the 14 wired MCPs. This skill
pins the chain so no future agent repeats the phantom-gap drift (e.g. proposing
E2B / Daytona / Modal sandbox MCPs when A-FORGE already sandboxes execution).

## The chain (already wired)

1. **RESEARCH**   → firecrawl (`deep-research`, `agent`, `research-papers`
                    = PubMed/bioRxiv/arXiv, `crawl`, `scrape`, `map`, `monitor`)
                    + brave-search (ranked web/news) + context7 (library docs)
2. **EVIDENCE**   → arif_observe (kernel 111) + hermes claim validation
3. **REASON**     → arif_think (kernel 333) — label OBS / DER / INT / SPEC
4. **VERIFY**     → A-FORGE: `forge_shell` (governed host) ·
                    `forge_sandbox_run` (isolated, absolute timeout) ·
                    `forge_ephemeral` (bwrap) · `forge_sandbox_pause/resume`
                    (persistent). **Run the code. Do not self-certify.**
5. **JUDGE**      → arif_judge (kernel 666) → SEAL / HOLD / SABAR / VOID
6. **SEAL**       → arif_seal (kernel 999) → VAULT999 immutable ledger
7. **METABOLIZE** → arifflow `flow_ingest` + CHRON (prediction → verify → calibrate)

## The anti-drift law (binding on every FI coding agent)

Before proposing a new research or sandbox vendor/plugin to Codex, answer ONE
question: **does A-FORGE already cover it?**

- Sandbox execution  → YES — `forge_sandbox_run` (Firecracker-class isolation,
  absolute timeout) + `forge_ephemeral` (bwrap) + `forge_shell` (governed)
- Deep research      → YES — firecrawl suite (30+ tools)
- Code review        → YES — github MCP + coderabbit/review skills
- Persistent memory  → YES — Codex `memories` feature + arif_memory L1–L6
- Git worktrees      → YES — Codex `worktrees = true` (native, config.toml)

Only a **genuinely absent, F13-approved** capability may be added. Duplicate =
HARAM (ANTI-BANGANG LAW 8: satu masalah, satu owner, satu jalan).

## Exit condition — a deep-research task is DONE only when ALL hold

- every claim carries an OBS / DER / INT / SPEC label
- every number carries a claim state (ESTIMATED → MEASURED → CROSS_VALIDATED)
- verification actually ran (code executed, result observed — not described)
- a sealed receipt exists with `trace_id`

Anything less is a **draft**, not a deliverable. (state-transition-discipline:
PRODUCED ≠ SENT ≠ DELIVERED ≠ OBSERVED ≠ ACKNOWLEDGED.)

DITEMPA BUKAN DIBERI ⚒️
