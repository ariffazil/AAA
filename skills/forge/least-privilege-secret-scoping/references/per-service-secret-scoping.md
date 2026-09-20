# Per-Service Secret Scoping — method and de-scope procedure

Depth for Step 2 of `least-privilege-secret-scoping`. Read when you are about to remove a shared
`EnvironmentFile=` edge, or when you need to justify how many services actually need de-scoping.

---

## 1. Compute the three numbers per unit

The invariant is `SECRETS_PRESENT ∩ unnecessary = ∅`. Two of the three numbers are cheap; the middle
one is the one that requires reading code, and it is the one that carries the finding.

**SECRETS_PRESENT** — parse the unit's `EnvironmentFile=` targets and count credential-shaped variable
names in each store. Credential-shaped means the name matches
`(APIKEY|API_KEY|_KEY$|TOKEN|SECRET|PASSWORD|_PWD|CREDENTIAL)` case-insensitively. Do **not** count
flags, URLs, ports or paths — counting `ARIFOS_STRICT_MODE` as a credential inflates the number and
the number is the argument.

**SECRETS_REQUIRED** — this is the whole method. It is a claim about the code, so the unit file
cannot answer it:

1. Read `WorkingDirectory=` from the unit (falls back to `/` when absent).
2. Read the `ExecStart=` payload. The Python module is relative to `WorkingDirectory`, so resolve it
   against that, not the calling shell's cwd.
3. Walk that tree for `**/*.py` (skip `__pycache__`, `.backup-*`, and vendored dirs), skip files above
   a few hundred KB, and concatenate.
4. Also scan the unit file text itself — occasionally a credential is referenced in an
   `Environment=` line.
5. `REQUIRED = {credential names appearing anywhere in that blob}`.

Two cautions that change the answer:

- **A name appearing in a comment or a docstring is not a use.** Read the hit's enclosing scope before
  concluding the service needs that credential. A grep hit is not an edge.
- **An import-time read is still a read.** `os.environ.get(...)` at module top counts; a lazily-read
  value configured but never reached may not, so state your interpretation explicitly rather than
  silently choosing the generous one.

**EXCESS_SECRETS** = PRESENT − REQUIRED. Report all three; the raw excess count is what makes the
finding legible.

---

## 2. Enumerate units by canonical identity

A glob over `/etc/systemd/system/**/*.service` counts symlinks and duplicated unit directories. That
inflates the work estimate and makes the scope claim wrong in the direction that discourages action.

```bash
# canonical pass: unit name -> resolved FragmentPath, deduped
for n in $(systemctl list-unit-files --type=service --no-legend --plain | awk '{print $1}'); do
  fp=$(systemctl show "$n" -p FragmentPath --value 2>/dev/null)
  [ -n "$fp" ] && [ -f "$fp" ] && echo "$n $fp"
done | sort -u -k2,2
```

A raw-glob pass and a `systemctl`-resolved pass disagree; the resolved pass is the one you quote. Also
resolve `load_state=masked` units — a masked unit is a deliberate retirement, not a de-scoping target.

---

## 3. De-scope one unit

The change is one line. The risk is the restart.

```bash
UNIT=/etc/systemd/system/<unit>.service
TS=$(date +%Y%m%dT%H%M%S)
cp -p "$UNIT" "/root/chron/.unit-backup-$(basename "$UNIT" .service)-${TS}.service"
```

Remove only the broad store line. **Leave `Environment=` lines, `ReadWritePaths`, `NoNewPrivileges`,
`ProtectSystem` and every other hardening directive untouched** — the de-scope is about which secrets
arrive, not about privileges.

```bash
systemctl daemon-reload
systemctl restart "<unit>"
sleep 4
systemctl is-active "<unit>"
systemctl show "<unit>" -p MainPID --value
```

Then assert the invariant on the *new* process, names only:

```bash
python3 /root/scripts/secretsafe.py env <unit>
# expect: credential_vars=0, and the service's own config vars still present
```

**Verify service behaviour, not just unit state.** `is-active` is satisfied by a process that came up
with the wrong working directory. Re-read the same surface you captured before the change — a health
endpoint's JSON, a row count, a listening port — and compare. A unit that lost a credential it
actually needed fails at first use, not at start, so exercise one real tool call before declaring the
edge unused.

**Rollback** is `cp -p` the backup over the unit, `daemon-reload`, restart. Chose one-unit-at-a-time
because the batch contains the transport you are talking through.

---

## 4. Stage the rollout around the transport

The list of over-scoped units will include the messaging gateway, the model router, and the agent
runtime conducting the audit. Restarting all of them at once can terminate the session mid-flight and
leave the host in a half-migrated state with no one watching.

Order:

1. Organs whose failure is contained and reversible (a temporal organ, an internal worker).
2. Infrastructure the session does not depend on.
3. Transport and gateway units **last**, one at a time, each verified before the next.

If a unit genuinely needs a credential, give it a **per-service file** containing only that
credential, and record the edge as intentional. `SECRETS_PRESENT > 0` is not a failure — an unreviewed
edge is.

---

## 5. Regression test shape

Any inspector written for this work must be tested against live secrets, and the assertion must be
about values, not about formatting:

1. Load every credential genuinely reachable on the host.
2. Run each subcommand of the inspector with those secrets in scope.
3. Assert **zero** credential values appear in captured stdout.
4. Assert the variable **names** DO appear — a tool that prints nothing passes a
   values-absent test trivially and is useless.
5. Assert raw mode is refused when stdout is not a tty.
6. Static check: no code path formats an env value into output.

Test 4 is the one that is usually missing. A redaction so aggressive that it hides the names satisfies
"no values leaked" while destroying the tool's purpose.
