# Concurrent Write Visibility — PROPOSAL

> **Status:** DRAFT_AWAITING_F13 · **not canon** · no mutation performed
> **Ref:** F-013 in `observability-convergence-2026-09-15/observability-failure-graph.json`
> **Author:** Hermes ASI (i-arif) · 2026-09-15 · KVM8
> **Scope:** every shared- infrastructure write across the federation
> **Reversibility:** total — adopting this adds one directory and one convention

---

## 1. The measured failure

| Time (+08) | Actor | Event |
|---|---|---|
| 13:35 | Hermes audit | probes `:18902/health` → connection refused. Records "no health surface" as a Phase 2 blocker. |
| 13:41:37 | Antigravity CLI (`9d53b0cb`) | writes `/root/scripts/kabarkan_health_server.py` |
| 13:41:45 | Antigravity CLI | installs and starts `kabarkan-health.service` |
| 13:41:5x | Antigravity CLI | adds `kabarkan: 18902` to FRAME's live `ORGAN_PORTS` |
| 13:42:13 | FRAME | next probe cycle reports `organs_up: 10` |
| 13:44 | Hermes audit | re-probes, finds it live. Its receipt is falsified on its central claim, **nine minutes after being written.** |

**Three writers touched one plane that afternoon** (Hermes: collector + frame-probe.timer + digest_inbox; Antigravity: health server + FRAME config; and the FRAME daemon itself, self-healing its baseline). **Zero markers.** Every participant believed it acted on current state. One was already stale.

## 2. Why this outranks the individual defects

Every other finding this session was local and repairable. This one is
**epistemic**: it means an artifact can be true when written and false when read,
with nothing in the artifact to indicate it.

Worse, the failure is **invisible in the artifact**. A stale audit looks exactly
like a fresh one. No error, no warning — just a document that describes a
federation that no longer exists. A system that writes careful receipts and then
silently serves stale ones has built a memory it cannot trust.

## 3. Correction to the framing: this is not a lock

The session called this "disiplin lock". **That name is wrong and would produce
the wrong mechanism.**

A true mutex over federation infrastructure would **serialise** multi-agent work.
Every organ, agent and daemon would queue behind one writer. In a system whose
entire premise is parallel metabolism, that trades a correctness bug for a
throughput collapse — and it would be circumvented within a week by anyone who
found it inconvenient, which is the worst outcome: a lock that is sometimes
honoured is worse than no lock, because it manufactures false confidence.

**What is actually needed is visibility, not exclusion.** Nobody has to wait.
Everyone has to *declare*, and everyone has to *sweep*. Those are cheap,
non-blocking, and cannot deadlock.

Working name: **Concurrent Write Visibility (CWV)**.

## 4. The rule, two halves

> **Writer:** declare intent before mutating shared infrastructure.
> **Reader:** sweep for writes newer than your measurement window before asserting state.

Both halves are required. Declaring without sweeping means the writer is honest
and the reader is still blind. Sweeping without declaring means the reader
catches what it can and misses whatever left no timestamp.

## 5. Mechanism — minimal, non-blocking

### 5.1 Claim record (writer side)

Before mutating a shared surface, append one line:

```
/root/AAA/state/write-claims/<YYYY-MM-DD>.jsonl
```

```json
{"ts":"2026-09-15T05:41:37Z","harness":"antigravity-cli",
 "session":"9d53b0cb-315a-4cde-844d-d7e7ea857b28","pid":1161186,
 "targets":["/etc/systemd/system/kabarkan-health.service",
            "/root/scripts/kabarkan_health_server.py",
            "/root/AAA/federation/frame/src/frame_organ/config.py"],
 "intent":"add Kabarkan health surface :18902 for FRAME probe",
 "class":"ADDITIVE","window_min":10}
```

Append-only via `flock` on the file, so concurrent appends cannot interleave or
lose lines. **Never blocks.** A writer that cannot claim still writes — the claim
is an announcement, not a permission.

### 5.2 Sweep (reader side)

Before asserting current state in any shared artifact:

```bash
find /etc/systemd/system /root/scripts /root/AAA \
     -newermt "$AUDIT_START" -type f 2>/dev/null | grep -vE '__pycache__|\.git/'
```

Any hit must be read before the assertion is published. This single command
would have caught the Antigravity writes — two of the three touched paths were
inside those roots.

### 5.3 Artifact stamping (both sides)

Every shared artifact carries its measurement window:

```
measured_window: 2026-09-15T05:33Z → 2026-09-15T05:44Z
```

Changes discovered after the window close are recorded as an **explicit
addendum**, never as a silent rewrite. This preserves the sequence — which is
itself evidence, as demonstrated in `KABARKAN_WITNESS_RECEIPT.md`, where the
addendum is more informative than the original claim.

## 6. Why this is cheap

| Cost | Value |
|---|---|
| one `mkdir` | falsification becomes detectable |
| one appended JSON line per mutation | stale artifacts announce themselves |
| one `find` before publishing | ~50 ms |
| zero blocking, zero deadlock, zero serialisation | no throughput cost |

There is no coordination protocol to agree, no leader to elect, no lease to
renew. It is a log and a habit.

## 7. Explicit non-goals

- **Not** mutual exclusion. Writers are never blocked.
- **Not** a permission system. No authority is granted or withheld by a claim.
- **Not** a substitute for `git`. It covers non-repo surfaces
  (`/etc/systemd/system`, generated scripts) that git does not track.
- **Not** retroactive. It records from adoption forward; historical writes are
  already lost and cannot be reconstructed.

## 8. Interaction with existing doctrine

| Doctrine | Relationship |
|---|---|
| `probe-before-panic` | CWV **extends** it: probe before *asserting*, not only before *declaring down* |
| `witness-zen-doctrine` | CWV is the mechanical form of "Void Guard" — no-data ≠ all-clear, applied to writers |
| `deploy-drift-verification` | CWV covers the gap that skill leaves: a *correct* deploy can still invalidate someone else's reading |
| `four-layer-separation` | CWV adds no authority to any layer; it is observation infrastructure |

## 9. Adoption

**Minimal viable adoption (recommended first step):**

1. Create `/root/AAA/state/write-claims/`.
2. Declare the sweep in the session-start checklist (`/root/AGENTS.md`), so every
   agent inherits it at boot.
3. Claim record: **optional at first**, mandatory after one week of observation.

Step 3 is deliberately soft. A convention adopted under observation survives; one
imposed in a day gets ignored in a month. The measurable success criterion is not
compliance — it is: **zero stale artifacts discovered after publication in the
following seven days.**

## 10. What F13 is being asked to decide

1. Adopt CWV as a convention (claim directory + sweep in the boot checklist)?
2. Name it — is "Concurrent Write Visibility" acceptable, or does it become a
   numbered fragment under `HUMAN_…` / `CONCURRENT_…` conventions?
3. Mandatory or advisory for the first week?

No mutation has been performed. This document is a proposal only.

*DITEMPA BUKAN DIBERI*
