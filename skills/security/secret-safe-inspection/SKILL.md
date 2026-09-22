---
name: secret-safe-inspection
description: "Use when a probe could emit a secret value."
version: 1.0.0
tags: [security, secrets, credentials, probing, blast-radius]
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Secret-Safe Inspection

> Inspecting an environment or a secret store is a **value-emitting operation by default**. The
> safe path is a different mechanism, not a better keyword.

**Load when:** about to read `/proc/<pid>/environ`, systemd `Environment=`, a `.env`/flat secret
store, or any config that holds credentials — and before reporting what a disclosure contained.
For the containment and rotation side, see `credential-exposure-containment`.

---

## 1. The defect this prevents

```bash
# DEFECT — a whole-line filter over an environment dump prints KEY=VALUE
tr '\0' '\n' < /proc/$PID/environ | grep -iE 'chron|store|db|path'
```

A line-level regex matches **against the value**, not only against the name. A filter containing
`db` matches a key whose material happens to contain those bytes, and the full line prints into the
transcript. The pattern was not the mistake — the *operation* was. A line filter over an environment
dump cannot be made safe by choosing better keywords, because you cannot know in advance which
substring appears inside key material.

The downstream trap: session transcripts, terminal-output caches, state DBs, and search indexes all
persist tool output. A value emitted once is retrievable from an index long after the transcript is
closed.

## 2. Enforce name-only structurally, not by care

- **One emission point** for the whole module; every output line passes through it. A single
  formatting path is auditable; fifty print sites are not.
- The only representation of a value a probe may produce is `<redacted len=N fp=sha256[:12]>`.
  Fingerprints are safe to print, are enough to **compare hosts**, and are enough to confirm a
  rotation landed without ever handling the value.
- **Raw-value mode requires a real tty *and* an explicit env flag.** A non-interactive caller (agent,
  pipe, CI) is refused even with the flag set — because the flag eventually *will* be set in an agent
  context, and that is exactly where the transcript gets written.
- **Write the regression test on the VALUES, not the names.** Run every subcommand with live secrets
  genuinely in scope and assert that no credential value appears in captured stdout. A test that
  only checks the known names are listed does not catch a leak.

Re-runnable probe covering all four commands: `scripts/name_only_env_probe.py`
(`env <pid|unit>`, `file <path>`, `units`, `agentcheck`). Copy it rather than re-deriving the pattern.

## 3. Classify by what was EMITTED, not by what was noticed

If a raw dump was printed, **every** secret in that process's environment is at least
potentially exposed — the one you happened to read is an artefact of which line you looked at.

```
POTENTIALLY_EXPOSED = every credential-shaped name in the affected process env
EXPOSED             = the ones the tool output actually contained
NOT_EXPOSED         = confirmed absent from the emitted output
```

Keep the `POTENTIALLY` set in the report even when the `EXPOSED` set looks small. Reporting only the
noticed name understates the incident and produces a rotation list that is short by design.

## 4. Blast radius — count, never print

```bash
# per-sink file counts
for d in ~/.hermes ~/.kimi-code /root/AAA; do
  printf '%s %s\n' "$d" "$(grep -rlF "$V" "$d" 2>/dev/null | wc -l)"
done
```

Compare hosts by fingerprint, never by value:

```bash
ssh <host> 'grep -m1 "^VAR=" /path/store | cut -d= -f2-' | sha256sum
```

**Measured:** a disclosed key resolved to the **same fingerprint on three hosts**, each holding a
copy of one shared store. Rotating on the host where the leak happened revokes nothing — the other
two keep serving the burned value. Rotation is a **fleet** operation; enumerate hosts before
reporting it as a single action.

Sinks worth counting, because a leak accumulates in more than the store:

| Sink | Why it matters |
|---|---|
| session transcripts | the obvious one; often the smallest count |
| **search indexes** (incl. their WAL) | a secret in an index is *retrievable*, not merely buried |
| terminal-output caches | the record of every previous probe that leaked |
| state DBs (and their WAL) | survives session end |
| vector / embedding exports | indexed, and copied to other nodes |

Report **file count per sink**, including the sinks that came back zero. A zero is evidence too.

## 5. Which services actually need credentials

A shared `EnvironmentFile=` hands every daemon every credential, so one probe on any unit exposes
the fleet's key material. Measure the excess instead of assuming intent:

```
SECRETS_PRESENT           = names in the unit's env files
SECRETS_ACTUALLY_REQUIRED = names referenced anywhere in the service's own code tree
EXCESS_SECRETS            = PRESENT - REQUIRED
```

Scan the service's source for the names. A temporal, compute, or indexing daemon that references
**no** provider key should carry none. De-scope one unit at a time — back up the unit file, remove
the broad `EnvironmentFile` line, `daemon-reload`, restart, then verify **both** that the process env
is clean and that the service still answers its own health. Do not batch-restart gateway or
session-holding units: that drops live work.

## Pitfalls

- **Do not assume the key you noticed is the only one.** A raw dump discloses the whole environment.
- **Grep-for-the-value is a disclosure test, not a reporting step.** Count with `| wc -l`; never
  print matches, and never paste them.
- **A stale copy elsewhere on the box defeats a local rotation.** Date-stamp every copy you find
  (`stat -c '%s %y'`); an older, smaller copy is a second unsynchronised store, not a backup.
- **Environment variables are inherited, not scoped.** Inspecting one unit says nothing about its
  children; check the process tree before declaring a blast radius.
- **Never claim a capability is down from a single read of an empty environment.** An empty or
  partial result is a failed read before it is a fact — see `background-monitor-design` for the
  confirm-probe rule.

## Support files

- `scripts/name_only_env_probe.py` — name-only inspector for `/proc/<pid>/environ`, secret-store
  files, and per-unit secret scope. Enforces the redaction point and refuses raw mode in
  non-interactive contexts.
