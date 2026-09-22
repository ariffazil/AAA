---
name: credential-exposure-containment
description: "Use when a secret value escaped into logs or indexes."
version: 1.0.0
owner: Hermes (arifOS federation)
risk_tier: high
floor_scope: [F1, F2, F11, F12, F13]
autonomy_tier: T1
tags: [security, secrets, credentials, rotation, blast-radius, incident]
triggers:
  - "secret leaked"
  - "key exposed"
  - "credential exposure"
  - "rotate the key"
  - "api key in the log"
  - "environ dump"
  - "blast radius"
  - "secret in transcript"
  - "over-privileged service"
  - "EnvironmentFile"
  - "excess secrets"
  - "key is burned"
capability_tier: fed-agent-subagent
ecology_state: WARM
---

# Credential Exposure Containment

> A secret once readable is burned. Redaction does not unburn it.

Static secret scanning answers *where secrets are stored*. This skill answers the harder question:
**a secret value has already reached a surface outside its canonical store — how big is the blast
radius, and what closes it permanently.**

## Law 0 — Never emit the value

A command that prints `environ`, an env file, or a credential store discloses the secret the moment
its output is captured. Tool output lands in a session transcript, a terminal cache, and often a
search index. **Printing is disclosure, whether or not a human reads it.**

- Default every environment/secret inspection to **NAME-ONLY**: `cut -d= -f1`, `grep -oE '^[A-Z_]+'`.
- Filter the *predicate*, not the *output*. `environ | grep -iE 'chron|db|path'` still prints
  whatever secret happened to match the pattern — cutting the field first is what makes it safe.
- Expose only: `SECRET_NAME · SERVICE · ISSUER · FINGERPRINT · ROTATION_STATE · ROTATED_AT ·
  DEPENDENTS · TEST_RESULT`.
- A fingerprint (`printf '%s' "$V" | sha256sum | cut -c1-12`) is safe to compare and safe to print.
  The value never is, in any context, including "for the audit".
- Owning the leak does not license re-emitting it. State the incident and the class of value; the
  reader does not need the value to act.

## Law 1 — Blast radius comes from the filter that ran, not from what was noticed

Reconstruct the exact pattern that executed and re-evaluate it over the process environment,
printing only matched NAMES:

```python
PAT = re.compile(r"<the exact pattern that was executed>", re.I)
matched = [k for k in env if PAT.search(f"{k}={env[k]}")]   # NAMES only
```

Classify every credential in scope:

| Class | Meaning |
|---|---|
| `EXPOSED` | matched the filter that ran |
| `POTENTIALLY_EXPOSED` | present in the same process env, not matched |
| `NOT_EXPOSED` | absent from that environment |

**Never assume only the first-noticed value leaked because it was noticed first.** A process env is
all-or-nothing at the point of capture.

## Law 2 — Count copies; rank by retrievability

```bash
for d in ~/.hermes ~/.kimi-code /root/AAA /root/arifOS/VAULT999; do
  printf '%-30s %s\n' "$d" "$(grep -rlF "$VALUE" "$d" 2>/dev/null | wc -l)"
done
```

Report the count and the *kind* of surface. Order of severity:

| Surface | Verdict |
|---|---|
| canonical secret store; a service's own provider config | legitimate home |
| session transcript | leak |
| terminal cache | leak |
| `state.db`, `*-wal` | leak |
| **search index / embeddings / memory export** | leak — **queryable** |

A secret in a dormant log is buried. A secret in a search index can be retrieved by anyone who can
run a local query. That difference, not the raw copy count, should order remediation.

## Law 3 — Rotation is primary; redaction is secondary

Process: identify issuer → issue replacement → update canonical store → reload **only** dependent
services → verify authentication with the replacement → revoke the old credential → verify the old
credential fails where revocation can be tested safely.

- **Do not delete forensic evidence needed to establish what happened.**
- Never present log redaction as the fix. It is second containment — it makes the damage invisible
  while leaving the credential live.

## Law 4 — Fix the injection pattern or it re-leaks

Rotating without narrowing the path guarantees recurrence, because transcripts, caches and indexes
persist whatever passes through a process environment.

```bash
grep -rhE '^EnvironmentFile' /etc/systemd/system/**/*.service | sort | uniq -c | sort -rn
```

A shared flat env file (`kunci-*.env`, `vault.flat.env`, or an equivalent "all secrets" bundle) hands
**every** credential to **every** service that sources it. For each unit:

```
SECRETS_PRESENT   — credential-shaped names in the files it sources
SECRETS_REQUIRED  — names actually referenced in the unit's own tree
EXCESS_SECRETS    — PRESENT − REQUIRED
```

Resolve `SECRETS_REQUIRED` by scanning the unit's `WorkingDirectory` tree and its `ExecStart`
targets for credential variable names, and cross-check the literal `os.environ` / `getenv` reads so a
value read through an alias is not scored as unrequired. A scan returning "none required" for a
service that clearly authenticates somewhere is a **claim to verify**, not a licence to strip the
env file.

Target invariant: `secret(service_i) ∩ unnecessary_credentials = ∅`.

> A compromise of one organ must not imply compromise of every external account.

A timekeeping or temporal organ has no business holding provider, finance, messaging, or federation
keys. Prefer per-service scoped injection over one universal bundle.

## Receipt contract

```
EXPOSED_COUNT · ROTATED_COUNT · REVOKED_COUNT
SERVICES_DE-SCOPED · EXCESS_SECRET_EDGES_REMOVED
REGRESSION_TEST = PASS|FAIL      # env inspection prints ZERO credential values
```

The regression test is the durable half: inspect a process environment and assert the output carries
variable names and **zero** credential values.

## Pitfalls

- **A name-only wrapper is not a control unless it is on the resolution path.** If raw `cat` / `grep`
  on the store still works, the wrapper is a convention. Verify from the side an agent would casually
  run, and confirm no value appears.
- **An env file shared by N services has an edge count, not a file count.** Report the number of
  `(service, unnecessary credential)` edges removed — the file count hides the blast radius.
- **Agent transcripts are leak surfaces, not scratch space.** Any inspection that prints a value
  writes it to the transcript, the terminal cache, and often a search index in one step; assume all
  three, and check all three.
- **Rotation count is not containment.** Report rotated/revoked separately from de-scoped edges;
  either one alone leaves the incident re-openable.

## Authority boundary

Rotation touches live services; de-scoping touches every agent's write path. Treat both as
sovereign-class decisions: identify the exposure, quantify it, present the containment package, and
HOLD for authorization. Never rotate or re-scope a production credential unilaterally.
