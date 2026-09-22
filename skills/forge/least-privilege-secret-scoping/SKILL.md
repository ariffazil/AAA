---
name: least-privilege-secret-scoping
id: least-privilege-secret-scoping
version: 1.0.0
description: "Use when services carry excess secrets or a key leaks."
owner: Hermes (curator-managed)
risk_tier: high
autonomy_tier: T1
floor_scope: [F1, F2, F4, F11, F12, F13]
tags: [secrets, credentials, least-privilege, containment, systemd, audit, inspection]
related_skills: [forge-secret-hygiene, security-audit, live-service-ops]
triggers:
  - "a secret got printed"
  - "did I leak a key"
  - "key is in the transcript"
  - "rotate the leaked key"
  - "blast radius of a credential"
  - "service has too many secrets"
  - "per-service secrets"
  - "EnvironmentFile over-scoped"
  - "/proc/environ dumped"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Least-Privilege Secret Scoping

Two jobs, and the second is the one that lasts: **contain an exposure**, and **remove the over-scoping
that let one read reach every credential on the host**. Cleaning up the leaked value while leaving the
shared secret bucket in place guarantees the next incident is the same incident.

> Rotate the burned key. Then remove the edge that made every other key reachable.

Companion to the external `credential-exposure-containment` skill (containment procedure) and
`forge-secret-hygiene` (age/rotation audit) — this skill owns the **inspection-safety rule** and the
**per-service scoping measurement**.

## Rule 0 — an inspection must not be ABLE to emit a value

Reading secrets is the highest-risk moment for them. Any read of `/proc/<pid>/environ`, a
`systemctl show -p Environment`, or a secret store is **NAME-FIRST**: the value never enters tool
output, a transcript, or a log.

The mechanism that bites: **a line-level filter over an environment dump prints whole `KEY=VALUE`
lines, so a regex written for the KEY can match inside the VALUE.** A filter intended to find a
process's data directory matched a provider API key whose value happened to contain the filter
substring, and the matching line went into an LLM tool transcript. The pattern looked reasonable; the
*shape* was wrong. **Anything that prints a matching LINE from an env dump is value-emitting by
construction** — the fix is structural, not a better pattern.

Do not hand-roll this. Run the name-only inspector:

```bash
/opt/arifos/current/venv/bin/python3 /root/scripts/secretsafe.py env   <unit|pid>   # names + fingerprint
/opt/arifos/current/venv/bin/python3 /root/scripts/secretsafe.py file  <store>      # names only
/opt/arifos/current/venv/bin/python3 /root/scripts/secretsafe.py units              # over-broad services
/opt/arifos/current/venv/bin/python3 /root/scripts/secretsafe.py agentcheck         # JSON: cred NAMES per service
/opt/arifos/current/venv/bin/python3 /root/scripts/tests/test_secretsafe.py         # regression
```

The wrapper enforces the property at a **single emission point** and refuses raw mode without a real
tty, so an agent context cannot opt into values. When you write or inherit any inspector, reproduce
the regression assertion: every subcommand runs with live secrets in scope, variable **names**
surface, and **zero** credential values appear in captured stdout. Redaction applied by convention
rather than at one emission point regresses silently.

Report a secret's identity as `{NAME, SERVICE, ISSUER, FINGERPRINT, ROTATION_STATE}`. `sha256(value)[:12]`
is the safe fingerprint. Never the value, never a fragment, never a length-and-prefix sketch.

## Step 1 — Establish the blast radius by SHAPE, not by what you noticed

One emitted value means every secret in that process was at risk. Classify by provenance of the read,
not by which value you happened to spot first:

| class | meaning |
|---|---|
| EXPOSED | the value occurred in the emitted output |
| POTENTIALLY_EXPOSED | present in the same process environment, not observed in output |
| NOT_EXPOSED | provably outside the read |

**If a whole environ dump was emitted, treat EVERY secret in that process as exposed.** Assuming only
the one you noticed leaked is how a seven-credential incident gets reported as a one-credential one.

Enumerate without printing: load the canonical store in-process, then walk the sink trees and count
occurrences.

```python
# values stay in memory; only NAME + file count + occurrence count is printed
for name, val in secrets.items():
    files = tot = 0
    for dp, dn, fn in os.walk(root):
        if '/.git/' in dp or '__pycache__' in dp: continue
        for f in fn:
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 25_000_000: continue
                b = open(p, 'rb').read()
            except OSError: continue
            if val.encode() in b:
                files += 1; tot += b.count(val.encode())
    print(f"{name:26} files={files:4} occurrences={tot:5}")
```

**The deciding probe is whether the value reached DISK, not whether it reached the chat.** A
provider key noticed in one tool output was already in the live state DB and its `-wal`, in terminal
cache snapshots, and across many files on the host — the leak and the persistence are separate
findings, and only the second one is durable.

Sinks to sweep — an agent transcript is one of many: session/state databases **and their
`-wal`/`-shm` sidecars**; terminal and tool-output caches; session trace/experience archives; local
**search indexes** (the worst, because a secret in an index can be *retrieved*, not just stumbled on);
delegation and background-task logs; `.env` files holding live values rather than references.

**Rotation is primary; redaction is secondary.** Scrubbing a transcript does not un-read a key — a key
that was ever readable is burned. Redaction only limits re-discovery; it must never be presented as
the fix, and it must not destroy the forensic record you need to state what happened.

## Step 2 — Measure per-service over-scoping (the actual defect)

The reason one read could reach unrelated provider, finance, messaging and federation credentials is
that **every service loads a shared flat secret file**. One daemon then inherits every credential on
the host, so a single one-line `EnvironmentFile=` change leaks all of them at once. Every compromised
service, memory dump, or env print is cumulative: one organ leaking means every account in that file
leaked.

Compute three numbers per unit:

```
SECRETS_PRESENT   credential-shaped names in the unit's EnvironmentFile(s)
SECRETS_REQUIRED  credential names referenced anywhere in the service's own code tree
EXCESS_SECRETS    PRESENT - REQUIRED        target invariant: SECRETS_PRESENT ∩ unnecessary = ∅
```

```bash
# which units load a broad store, and how many credentials ride along
for u in /etc/systemd/system/*.service; do
  grep -qE '^EnvironmentFile=.*(kunci|vault|flat)' "$u" 2>/dev/null || continue
  printf '%s <- %s\n' "$(basename "$u")" "$(grep -oE '^EnvironmentFile=-?\S+' "$u" | tr '\n' ',')"
done
```

`SECRETS_REQUIRED` needs the code tree, not the unit file: resolve `WorkingDirectory` and the
`ExecStart` payload, then scan that tree for the credential names. A temporal/intelligence organ
measured **PRESENT=7, REQUIRED=0** — seven provider credentials it never reads. Expect the same shape
in any organ whose responsibility is not model routing; the worst offenders on this host carried
**141 credentials each**. **A service carrying a credential it does not read is not harmless
configurability; it is an unreviewed edge.**

**Count units by canonical identity, not by glob.** Symlinked and duplicated unit files inflate the
work estimate: a raw glob over `/etc/systemd/system/**/*.service` double-counted entries and reported
30 units where a `systemctl`-resolved pass was needed to state the real number. Enumerate via
`systemctl list-unit-files`, resolve each `FragmentPath`, and dedupe by canonical path before quoting
a count.

Full method and the de-scope procedure: `references/per-service-secret-scoping.md`.

## Step 3 — Make the class unwitnessable-to-leak, not just the instance clean

Prefer per-service secret injection over any "all secrets into every daemon" convenience. When you
remove an edge, back the change up first, change one unit, and verify the service still serves:

```bash
cp -p /etc/systemd/system/<unit>.service /root/<somewhere>/.unit-backup-<unit>-<ts>.service
# edit: delete the broad EnvironmentFile= line, leave Environment= lines and hardening intact
systemctl daemon-reload && systemctl restart <unit> && sleep 4 && systemctl is-active <unit>
# then re-read the process env NAMES and assert the target invariant
```

The verification is a before/after on the invariant, not an exit code: **pre-change env carried N
secrets; post-change env must contain zero**, while health endpoint, ports and persisted state are
unchanged. Record the before/after shape (episode/row counts, health JSON fields), because a unit that
comes back with the wrong working directory still reports `active`.

## Step 4 — Rotation crosses an authority boundary you probably do not own

Provider keys live in the principal's accounts. An agent can mint a key for its own account but **not
for his**, so rotation is not "work not yet done" — it is work no agent can do. Consequences:

- Never report rotation as a task you deferred. Report the boundary: this needs the issuer.
- **Bundle rotation with the scoping fix as ONE decision.** Rotation alone leaves the host in the same
  shape, so next week's leak is the same leak.
- If a rotation policy file exists, read it for its own gate before proposing anything — a policy
  marked `DRAFT` with an irreversibility note is review-only, and a destructive-class change needs an
  explicit sovereign approval, not an inference from urgency.

## Reporting shape

```
EXPOSED_COUNT · POTENTIALLY_EXPOSED_COUNT · ROTATED_COUNT · REVOKED_COUNT
SERVICES_DE-SCOPED · EXCESS_SECRET_EDGES_REMOVED · REGRESSION_TEST=PASS|FAIL
```

Never the secrets themselves. State separately: what was emitted, where it persisted, what the
issuer-gated step is, and what you changed.

## Pitfalls

- **Filtering an env dump by line is the defect, not the pattern.** Any regex over `KEY=VALUE` lines
  can match inside a value; read names on their own, never the line (Rule 0).
- **Assuming only the noticed secret leaked.** If the dump was whole, every secret in that process is
  exposed until proven otherwise (Step 1).
- **Fixing the leak and calling it containment.** The over-scoped `EnvironmentFile` is the cause; the
  exposed value is a symptom (Step 2).
- **\"The key is in the chat\" is not the finding.** Check whether it reached disk: state DB + `-wal`,
  caches, and search indexes. Deletion does not undo a read (Step 1).
- **Redaction presented as repair.** The key stays burned until the issuer rotates it (Step 1).
- **Assuming `EnvironmentFile` load implies use.** Compare against the code tree; most services carry
  far more than they read (Step 2).
- **Globbed unit paths over-count.** Dedupe by resolved `FragmentPath` before quoting how many services
  need de-scoping (Step 2).
- **Restarting every affected service in one batch.** Gateway and messaging units may be in the list,
  so a blanket restart can terminate the session conducting the audit — de-scope in stages and never
  restart the transport you are talking through.
- **Deleting the shared store to \"fix\" it.** That is a data-loss action across every dependent
  service; remove per-unit edges and keep the store intact.
- **Reporting a rotation you did not perform.** State the boundary, not a completion.
