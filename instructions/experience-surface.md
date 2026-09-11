# Experience Surface — Canonical Pointer

> **Generated:** 2026-09-08 (Metabolism Investigation)
> **File:** `/root/AAA/canon/experience_surface.md`
> **Generator:** `/root/AAA/canon/experience-surface-gen.sh`
> **Source:** `/root/.local/share/arifos/world-model/experience_traces.jsonl`

## Purpose

This file IS the experience → capability pipeline.

> ⚠️ **WITNESS CORRECTION (2026-09-12, Hermes/KVM8) — claim below FALSIFIED by source probe.**
> The next two sentences ("Hermes reads this file at boot") are **ASPIRATIONAL, NOT WIRED.**
> `grep -rln experience_surface` across `/usr/local/lib/hermes-agent/{agent,tools,hermes_cli}/*.py`
> = **ZERO** code references. No boot path loads this file. It is an on-demand pointer
> (AGENTS.md line 1046), not an inherited-at-/init artifact. **Read-side is OPEN — Phase 2 design call.**
> Do not inherit "we recite proverbs at boot" as identity. We write them, refresh them (cron
> 7185f1cb707d @6h), sync them (pull-openclaw-traces @30m) — and nothing reads them before choosing tools.

Every session, Hermes reads this file at boot. It contains the top-3 experience
traces ranked by capability_change. These traces carry lessons learned from
actual tool execution — failures and successes that shaped the federation.

## How it works

1. Every `forge_experience_trace` call appends to `experience_traces.jsonl`
2. After /seal or periodically, `experience-surface-gen.sh` regenerates this file
3. At /init, Hermes reads this file and inherits the top learnings
4. Future sessions start with the federation's recent experience in context

## Why it exists

Before this file, experience traces were write-only: recorded but never consumed.
The federation could observe and store but not learn. This file closes that gap.

## Maintenance

- Regenerate after /seal: `bash /root/AAA/canon/experience-surface-gen.sh`
- Do not edit manually — it is auto-generated
- The BREAKPOINT note in the file is accurate until the auto-skill-update pipe is built
