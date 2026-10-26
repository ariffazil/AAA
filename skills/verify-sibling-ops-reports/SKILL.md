---
name: verify-sibling-ops-reports
description: "Use when another agent pastes an ops, cleanup, audit or capability report. Verify each load-bearing claim against live state with the cheapest falsification probe, grade claim-by-claim, then execute the clear verdict inside your authority tier instead of bouncing menus back."
---

# Verify Sibling Ops Reports

Every sibling report is a **self-report**, not a finding. Two agents agreeing is not an
independent observation. The job: cheapest falsification first, grade claim-by-claim, execute
the clear verdict inside your authority tier, report with evidence.

**Deep files:** `references/reply-shape.md` (opener, tables, ΔS arithmetic) ·
`references/pitfalls-ledger.md` (full pitfall catalogue, 40+ worked cases) ·
`references/procedure-original.md` (this skill's pre-compression full text — every command
and worked case, kept so the compression lost nothing).

---

## THE SIX-STEP PROCEDURE

1. **Cheapest falsification first.** Target existence, file path, service state, count — the
   claim that costs one command to disprove goes first. If the premise fails, stop; do not
   read the rest of the report as if it were grounded.
2. **Check whether it is already done.** `/root/_archive/`, recent `git log`, live config,
   `ls -la` on the claimed artifact. Siblings often act first and report after.
3. **Probe every load-bearing claim** with the table below. Mark retro/unverifiable claims
   PLAUSIBLE, never OBS. Probe the claims the report got *right* too — a report that is all
   wrong is easy; a hybrid is the dangerous class.
4. **Grade claim-by-claim**: ✅ TRUE · ⚠️ PARTIAL / UNVERIFIED / UNCOMMITTED · ❌ FALSE ·
   ✅ TRUE-RUNTIME-CONFIG (real but outside the repo trees — widen the search first).
   A wrong ❌ from a narrow probe is the auditor's own fabrication; correct it in the same reply.
5. **Execute the clear verdict** inside T1/T2. Only a genuine fork (T3, irreversible,
   money, constitutional) goes back to F13 — one fork with your recommendation, not four options.
   Repeated closed menus are agent-driving-principal: stop at the first, not the second.
6. **Report the verdict first**, then the corrected-claims table, then what you did, with the
   evidence path. Name uncommitted work as uncommitted. Report ΔS when entropy changed.

---

## LIVE PROBE TABLE (claim → cheapest truth probe)

| Claim | Probe |
|---|---|
| Bot webhook HIDUP / TUTUP | `getWebhookInfo` per token (`scripts/telegram-webhook-truth.sh`): url + pending + last_error. A public domain is not "localhost" |
| "Directory kosong, archive it" | `du -sh` + `lsof +D` + look for config/SOUL/db — 30M of runtime state is not empty. `mv` reversible; `rm` is not |
| Home dir live or orphan | `/proc/<MainPID>/environ` + `/cwd` of the RUNNING unit — proves which home belongs to a live service |
| Service / port alive | `systemctl show <unit> -p MainPID,ActiveState` + `ss -tlnp`. Webhook ports answer 404 on `/health` by design — not dead |
| Retro counts ("N cleared") | Unverifiable after the fact → PLAUSIBLE. Say "consistent with live state (pending=0)", not "N cleared" |
| "Sealed / judge SEAL" | Tail `VAULT999/outcomes.jsonl`: real seals carry verdict + actor + detail. `verdict: UNKNOWN` / `PENDING_SOVEREIGN` = the seal did NOT happen |
| "FQ recovered / OPTIMAL" | `curl :7073/health` → read `quotient` + `execute_count` + `verify_count`. **OPTIMAL with verify_count=0 is division-by-zero, not health.** Never cite the number without `window_start_utc` |
| "N jobs broken / created" | Probe BOTH cron registries (`~/.hermes/cron/jobs.json` and the profile copy) + both output dirs. Both can be simultaneously true |
| Tool / capability family exists | `curl :<organ>/tools \| grep <family>`. A plausible prefix is not a tool. Kernel verbs are the 8 canonical ones |
| "Config / SOUL lever flipped" | File edited ≠ file loaded. Resolve `HERMES_HOME` from the unit + `/proc/<pid>/environ`, then read the *effective* value (`scripts/hermes-config-effective.sh`) |
| Signing key / crypto claim | `stat <path>` first (documented paths are often fallback tuples that don't exist), then read the actual key-resolution function. "Ed25519" in a report usually means HMAC-SHA256 SCT |
| Security / CVE audit of repo X | `find /root /opt -iname "*X*"` FIRST. Zero hits = template applied to a phantom target → **VOID**, do not engage the severity matrix |
| Analogy-led conclusion | Does the analogy preserve or invert the property (VAULT999 = /dev/null inverts sink vs ledger)? Inverted = reject the conclusion even if the prose reads well |
| "Changed this session" | `git log --since=<window> --oneline -- <file>` (date-truth) + `git status -s` (uncommitted ≠ done). Real content from an older commit is true-but-misattributed |
| Hybrid report (real facts + fake numbers) | Verify the cheapest falsifiable **number** first. If it is wrong, treat the structural premise as suspect until each piece is re-probed |

---

## TOP EIGHT PITFALLS

1. **Judge verdicts are self-reports too.** A delegated 888-APEX verdict can hallucinate a
   specific fact inside sound directional advice. Probe the specifics; keep the sequencing.
2. **FQ is window-volatile.** 0.4 swing between probes minutes apart. Verdict survives a wrong
   number; a wrong *verdict* means the report was fabricated.
3. **Hybrid reports are the dangerous class.** Verifiable CVE ids / paper titles buy trust for
   invented metrics by association. Cheapest number first.
4. **Phantom target.** A full remediation blueprint for a repo that does not exist is VOID, not
   a severity matrix. One `find` settles it.
5. **Config lever ≠ config file.** `HERMES_HOME` decides which file loads; the unit env wins over
   `active_profile`. Probe the effective value, never the grep.
6. **Backdated attribution.** Real content committed last week is not this session's work.
   `git log --since` is the date-truth probe; uncommitted rows are ⚠️, not ✅.
7. **Parallel-verifier consensus is not independence.** N aligned verifiers share a blind spot.
   Keep one contrarian seat, and re-probe the falsifiable specifics after they agree.
8. **Your own wrong grade is a fabrication too.** A ❌ from a too-narrow search asserts a
   negative without warrant. Widen (`find /root -name …`), then correct in the same reply.

Full catalogue with worked cases: `references/pitfalls-ledger.md`.

---

## SCALE-OUT

**Large claim lists (10+ nodes):** batch the probes, parallelise the delegation, then reconcile
divergent auditor verdicts before ranking actions — never average them. Rank by corrected
premises, not by the report's own severity order.

**Nested reports (same problem, N agents):** count load-bearing claims probeable in <10s. Near
zero = elaboration. Re-probe the whole set in one batch, execute the real thing, report what
actually happened. Do not echo the philosophy back, do not seal the elaboration. Structural
test: *"the useful ones name a line number and offer to be wrong; the others offer a metaphor
and a seal."* Full pattern: skill `verify-nested-sibling-reports`.

**Validate-only lane** ("I prompt OpenCode, u just validate later"): do not redo the work. Wait
for the report, probe what the executor should have probed, grade with the same discipline. You
are the last line before the principal ratifies. First check whether a parallel session or
concurrent writer already touched the same files (`ps --ppid`, `git log --since`, `git status`).

---

## SUPPORT FILES

`references/reply-shape.md` · `references/pitfalls-ledger.md` · `references/forge-report-verification-3state.md`
(modified ≠ committed ≠ sealed) · `references/source-vs-runtime-deployment-drift-2026-08-06.md` ·
`references/hybrid-audit-2026-08-05.md` · `references/files-changed-table-verification-2026-08-06.md` ·
`references/multi-verifier-reconciliation-2026-08-05.md` ·
`references/governance-enforcement-audit-2026-08-05.md` ·
`references/vault999-chain-verification-2026-08-08.md` ·
`references/document-arithmetic-audit-2026-08-06.md` · `references/architecture-capability-claims-2026-08-06.md`
· `references/jobsjson-validator-gaps-2026-08-06.md` · `references/cron-model-ref-fix-2026-08-05.md`
· `references/fabricated-seal-receipt-pattern-2026-08-08.md` · `references/sessionless-probe-gaps-2026-08-08.md`
· `references/sibling-fabrication-patterns-2026-08-07.md` · plus 25 more dated ledgers in `references/`.
Scripts: `scripts/telegram-webhook-truth.sh` · `scripts/hermes-config-effective.sh`.

## CHANGELOG

| Version | Date | Change |
|---|---|---|
| 3.0.0 | 2026-10-23 | Surgical compression 108KB → core: reply-shape (30KB) and pitfalls (45KB) moved verbatim to `references/`; SKILL.md now holds the six-step procedure, the live-probe table, the eight load-bearing pitfalls and the scale-out rules. |
