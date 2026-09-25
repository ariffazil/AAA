# COMPACT_REINJECT + STOP_ENTROPY — Design v1

> **Status:** DESIGN_F13_APPROVED_CHAT (2026-09-25, SAH — "ya semua, jalan") · FI-003 (BUILD lane)
> **Closes:** the two remaining design binaries from the 2026-09-25 L05 verification
> (COMPACT_REINJECT unwired; STOP_ENTROPY structurally unsupported on Codex).
> **Companion law:** Hook Federation Standard (`instructions/hook-federation-standard.md`, L08 canon).

## A. COMPACT_REINJECT — context survival across compaction

### Defect

When a harness compacts its context window, mid-session constitutional state
(objective, authority envelope, open loops, trace_ids, held binaries) silently
evaporates. Post-compaction agents lose the plot and re-ask or re-probe —
attention waste + authority amnesia at the exact moment consequence is highest.

### Design (adapter pair, never spine changes)

**Event pair:** `PreCompact` → `PostCompact` (exists in codex hooks.json wiring;
qwen/claude carry equivalent compact lifecycle events; adapter maps only).

1. **PRE (capture, ≤2 KB, fail-soft):** shim writes a compact-context manifest to
   `/var/spool/arifos/hook-events/compact/<session>.json`:
   - objective (one line), authority envelope id + expiry, top-3 open loops
     (from carry_forward), active trace_ids (last 5), held F13 binaries if any.
2. **POST (re-inject):** shim emits the manifest as an `aaa.context.reinjected`
   advisory sensor event (R3) on the Hook Mesh spool — harness adapters surface
   it as a system-reminder-class block. **Advisory only (FP-02)** — the hook
   never judges, never blocks; the model sees the manifest and continues.
3. **Budget law:** manifest ≤2 KB. If capture exceeds budget, truncate loops
   first, never the authority envelope or trace_ids.
4. **Hygiene:** manifests expire after 24h (`/var/spool` is tmpfs-class);
   reinjection is idempotent per session (one shot per PostCompact).

### Wiring point

`adapters/compile.py` adds the event pair to the per-harness hook map where the
runtime exposes it. Harnesses without compact events (list them honestly in the
coverage matrix) are marked `ABSENT`, never faked.

## B. STOP_ENTROPY — session-end entropy snapshot

### Defect

Sessions end without measuring what they leave behind (uncommitted files, open
loops, dangling references). STOP_ENTROPY = the measurement, not a judgment.

### The structural fact

**Codex exposes no Stop lifecycle event.** Per the falsification discipline:
do not simulate a capability the platform does not expose.

### Design (two-lane)

1. **Where Stop/SessionEnd exists (qwen, claude):** emit one
   `aaa.session.entropy` sensor event with a tiny estimate:
   `S_stop = dirty_files + open_loops_new + unpushed_branches` (integer count,
   no pseudo-precision), routed to arifFlow via the standard spool.
2. **Where it does not (codex today):** mark `UNSUPPORTED` in the coverage
   matrix. Approximation lane IF F13 later wants it: PostToolUse sampling
   (entropy counter maintained per tool call, flushed at SessionEnd) — but this
   is a second-best; recommended posture is honest absence until codex-rs
   exposes the event.

### Non-goals

- STOP_ENTROPY never blocks a session (sensor, not judge).
- No new cron, no polling — event-driven only (Solution Architecture Preference,
  F13 2026-09-20).

## Implementation order

1. PRE/POST compact capture in the codex + qwen adapter compile step (small).
2. `aaa.context.reinjected` + `aaa.session.entropy` event schemas on the Mesh.
3. Coverage-matrix rows updated (FULL / ABSENT / UNSUPPORTED — FP-04 honesty).

Deferred until this design's BUILD session: all of the above are specification;
no code has been emitted for these hooks yet (truthful state: DESIGNED).
