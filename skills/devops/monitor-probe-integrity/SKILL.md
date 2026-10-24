---
name: monitor-probe-integrity
description: "Use when writing or auditing health probes and monitors."
version: 1.0.0
tags: [monitoring, probes, health-checks, telemetry, parsers]
risk_tier: low
---

# Monitor / Probe Integrity

Rules for probe scripts that turn raw endpoints into OK/DOWN/verdict lines.
A monitor that dies on parsing reports false absence, and false absence gets acted
on like a real outage. Fix scripts; never restart an organ because a parser choked.

## Parsing rules

1. **Capture regexes must accept the widest verdict vocabulary the producer can
   emit.** A capture like `[A-Z]*` silently drops compound verdicts that contain
   underscores (e.g. `INTACT_ACTIVE_DEGRADED_HISTORICAL`); the variable stays empty
   and the monitor prints UNAVAILABLE at HTTP 200. Write `[A-Z_]*`, echo the captured
   string verbatim, and never map an unrecognized verdict to UNAVAILABLE.
2. **When a monitor says UNAVAILABLE, rerun the underlying verifier by hand before
   believing it.** UNAVAILABLE usually means the parser failed, not the producer.
3. **Compound verdicts are active-state, not failure.** Read the producer's scope
   line to know what a compound verdict covers; report the actual string, do not
   collapse it to a clean token or to failure.

## Script robustness

4. **Guard every ratio on a non-empty denominator.** Coverage over set intersections
   crashes (ZeroDivisionError) when namespaces share no keys — and the traceback
   kills every later section of the same monitor, so unrelated sections also read
   UNAVAILABLE. Print an explicit `NO-OVERLAP(<sizeA>v<sizeB>)` sentinel instead;
   an empty overlap is a finding, not a crash. No monitor section may abort siblings.
5. **After editing a monitor script, run it end-to-end once and check every section
   produced output.** A monitor that exits 0 with sections missing is the silent
   failure mode; the receipt is the full output, not the exit code.
6. **Patch monitor scripts at their canonical live path only.** Duplicated copies of
   the same script under different trees drift; confirm which copy the cron/timer
   actually executes before editing, and note the canonical path in a comment.

## Believing numbers

7. **An aggregate scalar must reconcile with its component breakdown before it is
   quoted or acted on.** Pull the per-component breakdown from the producing
   endpoint; if the aggregate cannot be derived from its parts, label it unverified
   and report the discrepancy instead of the number.
8. **A score inherited from another organ without provenance, timestamp, or window
   match is a claim, not a measurement** (MEASURED > DERIVED). Downstream floors,
   verdicts, or alerts keyed on it inherit the defect — gate the inheritance until
   the producer carries provenance.
9. **Name the instrument and its freshness for every number in a health report.**
   Two instruments measuring the same axis can disagree; citing both without the
   source and timestamp reads as a contradiction that is really just staleness.
