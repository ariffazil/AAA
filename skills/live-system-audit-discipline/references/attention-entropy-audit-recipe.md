# Attention / Entropy Audit — recipe

Trigger: "audit yourself", "find the chaos / entropy / drift / attention debt", or an explicit list of
deliverables. The output is a **ranked diagnosis**, and the ranking rule is the whole point. Do not
optimize, propose, or restructure before the diagnosis is written and ranked.

## Guardrails (state these up front, then obey them)

- No optimization suggestions before the diagnosis exists.
- Mark insufficient evidence as UNKNOWN. Never fill a gap with a plausible mechanism.
- Prefer deletion over addition; consolidation over expansion.
- A number you did not measure this session is a citation, and carries the provenance and the age of
  whatever produced it.

## 1. Probe before narrating

Cheap, parallel, and all of it from the box — never from memory. Identity and time first (they anchor
every other claim), then the layers:

- **Machine**: hostname, date, uptime, load, `free -h` (note swap, not just RAM), `df -h`,
  `/proc/pressure/*`.
- **System**: `systemctl --failed` (the only authoritative failure list), `list-units --type=service
  --state=running`, `docker ps`, `ss -tlnp`.
- **Agents**: which CLIs are resident and for how long, with RSS and CPU.
- **Schedulers — count them separately.** systemd timers, `/etc/cron.d/*`, the root crontab, and the
  agent runtime's own job store are four distinct populations with four different counts. Report each,
  plus enabled vs total, plus last-run ages. A schedule that never fires is not neutral: it re-enters
  every later sweep as "status unknown".
- **Log and artifact volume**: the largest log directories, and whether any of them has a rotation
  rule at all. An event-per-tick writer with no rotation rule is a disk leak on a schedule.
- **Duplicate trees and stale copies**: directory sizes ranked, then the duplicate question answered
  by hash — not by name.
- **Open loops**: the carry-forward / issue / task store, grouped by age. An open loop older than a
  few days with no owner is closure debt, not work in progress.
- **Registries and sources of truth**: enumerate every candidate and check whether they agree. Two
  registries claiming the same namespace is the finding; picking the "right" one is the corruption.
- **Declared vs live**: for each advertised count or endpoint, probe it and compare. A banner, a
  dashboard and a config file are narratives.

## 2. Classify the inventory

Every item competing for attention goes into exactly one bucket:

| Bucket | Test |
|---|---|
| ACTIVE | live evidence **and** a consumer |
| WAITING | genuinely blocked on a human decision |
| BLOCKED | stuck on a mechanism, not on a person |
| STALE | alive, but its reported numbers are old |
| ABANDONED | declared somewhere, absent from the machine |
| SHADOW | invisible on any dashboard, present on disk |

SHADOW is the bucket that pays. Walk the filesystem for it: directories nobody's console lists, logs
nobody rotates, copies nobody remembers making.

## 3. Score and rank

For each finding: **attention cost** (L/M/H) and **reality impact** (L/M/H).

Sort by attention cost **descending**, then reality impact **ascending**.

> Highest priority = consumes the most attention while producing the least reality.

## 4. The parasite test (three questions per candidate)

1. **Who reads this?** If nobody, it is archive masquerading as governance.
2. **Has it ever changed a decision?** Sample the WHOLE population, not a convenient slice — a slice
   proves nothing about the population.
3. **Does it have a kill rule?** Rotation, retention, a threshold that retires it, or a human who
   owns deleting it. No kill rule means it grows forever by construction.

An item that fails all three is the top of the ranking regardless of its size in bytes.

## 5. Output shape

1. **Attention map** — the inventory, bucketed.
2. **Chaos register** — each leak as a numbered finding: what, measured cost, measured impact, class.
3. **Parasite ranking** — ranked, cheapest-to-remove first among equals.
4. **Governance drift report** — capability without an owner · owner without a capability · authority
   ambiguity · missing receipts · stale registries · contradictory sources of truth · surfaces that
   bypass the gate.
5. **The one action** — the single removal that releases the most attention, with the reason it won,
   and an explicit split between what is reversible (execute it) and what needs the sovereign.

## Pitfalls

- **Two reviewers agreeing is one witness.** When the principal pastes an external verdict on your own
  audit, adjudicate each of its claims against the box before adopting or rejecting any: confirm some,
  correct some, and say which is which. A peer's confidence is not a second reading.
- **Distinguish "no reader" from "no effect".** No effect is a judgement; no reader is a measurement.
  Publish the measurement, and only infer the judgement from it.
- **A deletion that removes a control surface is not a cleanup, it is a control mutation.** Name the
  authorising lane for anything that changes what the institution can see, even when the file count
  is small.
- **Close out what you executed.** Each removal needs a receipt that states the population removed, a
  manifest hash, what was retained as a witness, and the reversal. Ranked findings you did not touch
  belong in the open-loop store with their evidence, not in the prose.
- **A monitor that has been writing for weeks with a constant verdict and a constant reason class has
  not been monitoring.** One reason class across an entire population is the signature of a stuck
  instrument, not of a stable system.
