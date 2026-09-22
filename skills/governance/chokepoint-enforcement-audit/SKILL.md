---
name: chokepoint-enforcement-audit
description: "Use when a gate or chokepoint claims to enforce."
owner: A-FORGE
capability_tier: fed-long-context
ecology_state: WARM
---
# Chokepoint Enforcement Audit

> A control is only real on the day you last tested the path that avoids it.

## The defect this exists to catch

A gate is built. It denies correctly. A test suite calls the gate directly and
reports PASS. The boundary is nonetheless wide open, because nothing forces a
caller to pass through the gate.

Real instance (2026-09-20, arifOS Gmail gateway):

```python
# What the suite tested:
run_cmd(["bash", guard_script, "gmail", "users", "labels", "list"])   # PASS

# What it should have tested:
run_cmd(["gws", "gmail", "users", "labels", "list"])                  # wide open
```

The guard was never installed on PATH. The gateway it protected called bare
`gws` at 12 sites, bypassing its own gate. Reported status: **7/7 PASS**.
True status: **0/8 vectors blocked**.

## Rules

1. **Never call the gate in the test.** Run the command a careless or hostile
   actor runs. If the gate must be invoked for the test to pass, the test is
   measuring the gate's logic, not the boundary.
2. **Test at least these vectors:** bare name on PATH, absolute path, direct
   interpreter invocation (skip the wrapper), direct read of the secret/store,
   programmatic read, copy-out, and whether the sanctioned service itself
   bypasses the gate.
3. **Include a meta self-test with a known-open control.** Run the detection
   helper against a file that is definitely readable. If it reports "blocked",
   the suite is blind and every PASS it emits is void.
4. **Include a binary control, not only a text one.** A decode error on binary
   content can be swallowed and reported as "not readable" — a false PASS on a
   file that is fully readable. This exact bug appeared in the first draft.
5. **Classify every open vector:** `DEFECT` (closeable, close it) vs
   `ROOT_RESIDUAL` (structurally unfixable in this configuration — name the
   condition that would fix it). Do not silently merge the two into one score.
6. **Exit non-zero on an open DEFECT** so the suite can gate CI.

## Unfixable residuals — say them out loud

On one host, a root process cannot be denied access to a file on that host. No
DAC permission, LSM profile, or seccomp filter changes this. AppArmor can
constrain root *by default* — it stops the casual path and forces a deliberate
LSM action (`aa-exec`, or writing to `/sys/kernel/security/apparmor/.replace`)
to escape — but it is not absolute.

When that is the situation, the honest report is:

> default-deny for the tool, full receipts, bypass requires a deliberate LSM
> action. The complete fix is non-root citizens or off-box custody.

Not: "the chokepoint is enforced."

## Mechanisms that actually bind (tested)

- **AppArmor profile attached to a script's path** works only when the script is
  exec'd via its shebang. It does **not** attach when an interpreter is handed
  the script as an argument (`node script.js`) — the profile is bypassed by that
  one invocation form. Do not build a boundary on path attachment alone.
- **A profile attached by path will also capture your own privileged service**
  when it execs that path. `/** rwklmix,` alone does NOT reliably prevent the
  transition; you must grant explicit `ix` on the CLI tree and its interpreter,
  or the service silently falls back into the deny profile.
- **The node-launcher pattern defeats profile inheritance.** A wrapper whose
  shebang is `#!/usr/bin/env node` does a two-step exec; under a named profile it
  failed with EACCES on the store while the *native binary* worked. Execute the
  native binary directly from the privileged context.
- **Deny rules always win over allow rules**, so `/** rwklmix,` plus an explicit
  `deny <secret>/** r,` is safe.
- **AppArmor resolves symlinks** — allow the real path, not the symlink.
- **`/** rwklm` without `x` breaks all exec** — include the exec mode.

## The capability boundary that actually closes it

An environment variable is a claim; a UID is a capability. The mechanism that
binds is moving the credential to an identity the citizen does not have:

1. Create a service user; `install -d -m 0700 -o svc -g svc /var/lib/svc`.
2. Run the broker as that user (`User=` in the unit), never as root.
3. Serve warga over a socket group (`/run/svc` 0770 svc:clients) so group access
   to the socket never implies access to credentials.
4. Deploy service code **outside `/root`** — a non-root service cannot traverse a
   0710 home directory.
5. Make every service-path failure graceful: `Path.exists()` on a root-only path
   raises `PermissionError` for a non-root service and will crash it at startup.

Layer order, weakest to strongest: env var → PATH shim → AppArmor deny →
DAC/dedicated UID → separate host.

## Test from the constrained identity, not from inside the gateway

Every adversarial vector must run as the citizen (`sudo -u <warga>`), not as
root and not from within the broker. A boundary tested from the privileged side
is not tested.

## Prefer this order

1. Build the honest suite first, against the current state. Expect it to fail.
   A suite that passes before the fix has not been calibrated.
2. Commit the failing number to the record before building anything.
3. Build the sanctioned path (broker/daemon) so nothing breaks when the deny
   lands.
4. Migrate every existing consumer to it. Grep for the raw invocation; shell
   scripts and cron jobs are the ones that break silently.
5. Only then load the deny. Re-run the suite.
6. Write the spec with what is guaranteed and what is not, in separate sections.

## Companion failure modes

- **Documentation drift:** the agent's own report said "convention gate" under
  UNCERTAINTY and "true physical chokepoint" under CONSEQUENCE. The stronger
  claim took over with no new evidence. When two sections of one report
  disagree, the weaker one is the one to trust until tested.
- **Present tense is a claim, not a status.** "The boundary is enforced" is only
  true on the day the suite last returned a passing verdict.

## A patch to a gate module without a process restart is a no-op

Long-running processes that `import` the gate load it once at start and keep that copy in memory
until the next boot. Editing the source on disk changes nothing until the process restarts.
Measured shape: a dedup gate was patched to fix a window-basis bug (a one-line arithmetic change);
the consumer worker was up for 45 hours and imported the pre-fix module 2 minutes before the patch
landed; 111 identical P1 alerts were emitted over those 45 hours for one unchanged standing
condition. None of the 112 events in the ledger carried the new dedup field that the patched code
always writes — so the defect was visible in receipts that never got a chance to write.

The order is **patch → restart → re-probe**, in that sequence, every time:

1. Patch the source. Diff is meaningless without a reload.
2. Restart the consumer (or signal it to re-import, if it supports it — most don't).
4. Re-probe by triggering the same condition the gate was supposed to suppress. A receipt with the
   new field, or a no-deliver response, is the only proof the patch is live.
3. State the restart in the seal: which PID was retired, which PID is the new one, at what time. A
   patch record without a restart receipt is a receipt for a file change, not for a behaviour change.

For anti-storm gates specifically: the dedup field MUST be written on every emit, not only when
notify=True. A receipt that omits the dedup verdict was produced by code that never ran the gate —
and the gate is the only thing that prevents the next flood. State `delivery_health: SUPPRESSED`
explicitly when notify is skipped, so the ledger shows the gate fired even though no Telegram
message went out.
