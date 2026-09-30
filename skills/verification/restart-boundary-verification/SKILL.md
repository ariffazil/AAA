---
name: restart-boundary-verification
description: Use when a config change only applies after a reload.
version: 1.0.0
tags: [config, deploy, verification, systemd, env, credentials, reload, rename]
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Restart-Boundary Verification

> A passing probe is evidence about the **running** config. Your edit is about the **next** one.
> The gap between the two is where a cosmetic change becomes an outage.

A long-running process keeps its config in memory. Every edit it will not read until it reloads has
two states — the one you can test right now, and the one that starts the moment it restarts. This
skill is about verifying the second without having to bounce the first.

## When to use

Any change a running process will not see until it reloads: an environment variable, a unit file, a
mounted config, an alias or model name, a credential scope, a plugin or schedule list. Also when a
peer lane reports such a change as done because the service still answers — a green service is not
confirmation that an unloaded edit is correct.

## Rule 1 — verify the next state by inspection, not by the current probe

- The probe cannot see an unloaded change. A green probe is therefore not a verdict on your edit; it
  is a verdict on the old one. Keep the two claims apart in the report, explicitly.
- Enumerate the change's **consumers** and check each against the next state: the file, the
  environment, the permission scope, the call-sites. The change is done when every reader agrees, not
  when the writer finished.

## Rule 2 — resolve variable references against the file the unit ACTUALLY loads

```bash
systemctl cat "$UNIT" | grep -E 'EnvironmentFile|Environment='
```

- A literal replaced by an environment reference looks cleaner and can resolve to a **staler** value
  than the literal did, when the unit loads a different file than the one edited. Read the unit; never
  assume the convention path.
- **A secrets file nothing reads is not a runtime input.** Find its readers before treating a path as
  truth — grep the service tree and the systemd unit directory for that filename. A file referenced
  only by backup tooling will absorb writes indefinitely while the runtime reads elsewhere, and both
  writers believe they succeeded.
- A service may also load a dotenv file from its working directory ahead of the unit's
  `EnvironmentFile`. When a variable appears ignored, check both before concluding the edit was wrong.

## Rule 3 — sweep for surviving hardcoded copies

Every hardcoded copy of a value you replaced is a stale one that keeps appearing to work until the
thing behind it disappears. **Count them and drive the count to zero**, rather than fixing the single
occurrence you came for. The count is the evidence; "I updated it" is not.

## Rule 4 — a rename is a SET, not an edit

Renaming an identifier other components name is the highest-yield instance of this class:

```
definition      the alias / name itself
scope           every permission set, allow-list or token that enumerates the old name
client config   defaults, and every FALLBACK entry that names it
call-sites      every script, agent or job passing the old name
```

- **List both names during the transition** wherever the field is a set. Old+new together is safe
  across the reload in either order; a set naming only one of them breaks one side of the boundary,
  and which side is not obvious until the reload happens.
- **Grep call-sites before calling it done.** Scheduled probes, sentinels and selftests fail silently:
  they are off the request path, so nothing surfaces until their next tick. Give them an
  env-overridable default so the old name can be restored without an edit.
- Distinguish identifier from substring. A file name, an unrelated provider key or a session string
  that merely *contains* the old name is a different change — leave it, and say which ones you left.

## Rule 5 — prove a scope change with the status-code tripod

Before reloading, hit the target through the same path the consumer uses, and read three codes:

| Code | Meaning |
|---|---|
| 2xx | served AND permitted — done |
| `400` / not-found | permitted, but the running process does not know the name yet — correct pre-reload |
| `403` | refused by scope — the scope edit did not land |

A `403` where a `400` is expected is the falsifiable signal that the update failed. Always include a
control input that must be refused; without it you have shown the check can pass, not that it
discriminates. Report the three readings together — the contrast is the proof.

## Rule 6 — order the reload, and do not own it alone

- Prefer reloading the **producer before the consumer** when a name changes: a consumer asking for
  something not yet served reads as a broken client, while a producer serving only the new name to an
  old client reads as a broken gateway. Choose the shorter window and name which one you accept.
- State the expected reading on **both sides** of the window so a brief red is not filed as a new
  incident.
- **Neither reload is unilateral** when it disrupts a live service or terminates the session you are
  in. Give the order, the cost, and let the principal call it — that is a service decision, not a
  technical one.

## Rule 7 — back up, then read state back from the store

- Copy every file before editing it, timestamped.
- A tool's success response says the call was **accepted**, not that state changed. Re-read the row,
  file or unit and cite what you read.
- Identify secrets by a truncated digest. Never quote a value, not even truncated — a masked form
  emitted by the service is still a leak, so scrub both shapes.

## Special case — gateway seat credentials (virtual keys)

A gateway resolves two credential kinds from two different places, and that asymmetry is the whole
problem:

- **Provider keys** resolve from the service environment.
- **Seat / virtual keys** resolve from a row in the gateway's own token table.

A wiped or re-initialised token table therefore takes down **only** the seat-key clients while every
master-key client stays healthy. The outage lands on exactly the class nobody probes.

- No row means the key is dead, whatever any config file says. The symptom names the store, not the
  credential.
- The **backend** port is the DB-wired instance; frontend ports are a proxy that injects the master
  key. Mint, read and update against the backend. A frontend answers about everything except the table
  you are editing.
- Mint through the official generate script/API with an **explicit model-scope list**, so the scope is
  declared in tooling rather than inferred later by reading a row back. Prefer re-minting and
  installing the value over hand-writing a row.
- The token table is a shared store with a **unique-name constraint**: a peer minting the same alias
  gets a conflict, and its cheapest recovery is to delete the entry it collided with. Before deleting
  a conflicting entry, read its creation time — anything minutes old is a live peer's work. Prefer a
  distinct alias over deleting to claim one. See `concurrent-agent-writers`.
- Classify the callers before sizing blast radius. A client holding a service token plus an app URL is
  not a client of this gateway, and a master-key client cannot break this way. The exposed class is the
  finding — not the individual credential that failed.
- A seat that authenticates but is refused on the lane is **correctly scoped, not broken**. Report it
  as a scope fact, never as an outage to be routed around by widening the credential.

## Pitfalls

- **Reporting the green probe as a verdict on the edit.** Two claims, two states; keep them apart.
- **Trusting a peer's "after the restart it will stay green" prediction.** A peer's report is a claim
  about a future state. Check it against the readers — the same way you would check your own.
- **Assuming the obvious secrets path is the loaded one.** Convention files and runtime inputs drift
  apart silently, and both look correct in isolation.
- **Fixing the primary block and forgetting the fallback list.** The fallback entries naming the old
  identifier are exactly what a sweep aimed at the primary path misses.
- **Treating a filename or variable that merely mentions the identifier as a call-site.** Renaming it
  is scope creep with a real breakage risk.

## Related

`concurrent-agent-writers` (shared config and stores — re-read before writing, hash the exact field),
`probe-instrument-trust` (making the probe itself trustworthy), `secret-safe-inspection` (reading
config without emitting values), `litellm-proxy-triage` (gateway topology and auth-surface forensics).
