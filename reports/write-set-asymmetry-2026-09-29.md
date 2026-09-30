# Write-Set Asymmetry — Implementation Slice 1 (Landlock guard)

**Date:** 2026-09-29 · **Author:** 333-AGI (FI-003 forger) · **Trigger:** F13 "sah" on the godel-lock survey's ONE next step
**Status:** build receipt — slice 1 (primitive built + verified). NOT yet applied to live agents.

---

## What this slice delivers

The godel-lock survey (`godel-lock-2026-09-29.md`) scored "monotonic tightening in code"
and "kernel-level sandbox on agent processes" as **NOT BUILT**. This slice builds the OS
primitive that fills both, and proves it works before any rollout.

### Artifacts (all reversible — new files, no live mutation)

| Artifact | Path | Role |
|---|---|---|
| Guard | `/root/AAA/governance/landlock-guard.py` | pure-ctypes Landlock wrapper, no pip dep |
| Test policy | `/root/AAA/governance/write-set-asymmetry-test-policy.json` | scratch dirs, proves mechanism |
| Production intent | `/root/AAA/governance/write-set-asymmetry-policy.json` | real protected paths, `allow_write` deliberately empty |
| Falsification test | `/root/AAA/governance/test-landlock-guard.sh` | 6 assertions, includes crash-detection |

### The key mechanism (why this works where chmod does not)

Probed live: **every agent process runs as uid 0** — codex, opencode, kimi, hermes,
qwen, the MCP servers, all of them. `chmod`/ownership is meaningless against root:
root bypasses it (proved by test T1 — unconfined root overwrote a `chmod`-protected file).
`/root/VAULT999` is already owned by uid `arifos`, and that does nothing to stop a root agent.

**Landlock restricts the *process*, not the uid.** A root process that calls
`landlock_restrict_self()` CANNOT lift the restriction — the syscall is monotonic, a
process may only *add* rules. That is the OS form of "policy may only tighten, never
widen" — reading (C) of the lock, the only buildable one.

The guard's policy is deny-by-default on the write set, allow-list on the agent's work
dirs, and asserts the protected paths are *never* inside the allow-list.

## Falsification result — 6/6 PASS (root, kernel 6.17, ABI v6)

| # | Assertion | Result |
|---|---|---|
| T0 | guard execs a child without crashing (catches the "silent crash = false pass" defect) | PASS |
| T1 | baseline: unconfined root overwrites a protected file | PASS (proves the residual is real) |
| T2 | confined process writes to an allow-listed dir | PASS (lock not over-broad) |
| T3 | confined process write → protected path | **DENIED** |
| T4 | confined process truncate → protected path | **DENIED** |
| T5 | confined process remove+replace → protected path | **DENIED** |

### A bug this test caught (and why the test exists)

First run: T3/T4/T5 *looked* like denials but were false — the guard crashed with
`EINVAL` before execing, so nothing ran and "no write happened" masqueraded as "denied".
Root cause: passed `LANDLOCK_CREATE_RULESET_VERSION` as a create flag (it is query-only,
requires `attr=NULL, size=0`) and hardcoded the ABI-v1 struct size while using v3 rights
(`TRUNCATE`, `REFER`). Fixed by querying the ABI live and masking unavailable rights.
This is exactly the defect class the mail-gateway audit warned about — a guard that fails
on the resolution path and still reports green. The test now asserts the guard *exec'd*
(marker on stderr) before trusting any denial.

## Scoring after slice 1 (honest — LIVE / PARTIAL / NOT BUILT)

| Layer | Before | After slice 1 | Note |
|---|---|---|---|
| Monotonic tightening in code | NOT BUILT | **PARTIAL** | primitive built + verified, not yet deployed |
| Kernel sandbox on agent processes | NOT BUILT | **PARTIAL** | tool proven; agents still run unconfined |
| Transparency log for self-modification | NOT BUILT | NOT BUILT | needs eBPF/audit — next slice |

## What slice 1 did NOT do (do not over-claim)

The residual is **unchanged**: agents still run as root, unconfined. The guard is a
verified tool sitting on the shelf. The write-set asymmetry is not *enforced* until the
guard is wired into an agent's launch path.

## Next slices (reversible-first, F13-gated on the cut)

- **Slice 2 — canary:** enumerate ONE agent's real write roots (work trees, logs, caches),
  build its allow-list from the live filesystem, wrap its MCP launcher with the guard,
  run the agent, watch for breakage. The curator process is the right first target — it is
  the specific self-modification risk named in the survey ("skills auto-created by the
  curator with no external witness").
- **Slice 3 — transparency log:** attach eBPF/audit (tracee pattern) so a *denied* write
  attempt to a protected path becomes a VAULT999 receipt with an external witness. Landlock
  denies silently; the attempt must be observed by an instrument the agent cannot edit.
- **Slice 4 — rollout:** apply to all FI agents, one at a time, each with a per-agent
  allow-list derived from the live filesystem. A lock with a wrong allow-list silently
  bricks the agent — so this is the slow, witnessed phase, not a batch cut.

## The one-line answer to "is it locked now?"

No. The *lock mechanism* is built and proven to bind root. The *lock* is not yet in any
agent's path. Enforcing it is the canary + rollout, which needs per-agent write-root
enumeration — reversible work, but it must be done agent-by-agent, not as a batch.
