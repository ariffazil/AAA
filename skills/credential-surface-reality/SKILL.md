---
name: credential-surface-reality
description: Use when counting or retiring plaintext credentials.
version: 1.0.0
author: Hermes Agent
license: proprietary
metadata:
  hermes:
    tags: [secrets, hygiene, audit, federation, kvm4, kvm8]
    related_skills: [forge-secret-hygiene, security, hermes-runtime-audit, openclaw]
---

# Credential Surface Reality

## When to Use

Load when any of these is true:

- A config file holds an inline API key or token (`Authorization: Bearer …`, `"token": "…"`).
- Someone quotes a number of "plaintext secrets" and you are about to repeat it.
- You are about to replace a credential literal with an environment reference.
- You are retiring, rotating, or destroying a credential.
- A service restart or update was declared failed and you are about to act on that verdict.

Do not load for ordinary secret-lookup questions (use `forge-secret-hygiene`) or for MCP server health.

## Why this exists

Two failure modes, both measured on 2026-09-29 across KVM4 (OpenClaw) and KVM8 (HERMES):

1. **A count quoted from a report is not a measurement.** One config file produced five different
   numbers in a single night (14 · 0/16 · 3 · 1 · 18) — each from a different scope, each inherited
   rather than re-derived. A tool's warning wording ("plaintext secret-bearing fields") is a *scope
   description*, not a count of plaintext values: doctor lists every field that *reaches* a secret,
   including properly templated ones, because it cannot verify the template resolves.
2. **Any single-scope sweep lies.** A config-only scan misses standalone secret files sitting next to
   the config. A filesystem scan filtered by file extension misses backups whose names end in a
   timestamp (`openclaw.json.bak-pre-firecrawl-20260924`, `kunci-mas.flat.env.bak-a2a-20260914-231232`).

## Rule 1 — count with two heads, always

Use the two-headed counter at `/root/scripts/secret-surface.py` (KVM8) ≡
`/root/.openclaw/tools/secret-surface.py` (KVM4). Mode 700, JSON *and* YAML, values never printed.

```
python3 secret-surface.py --config <config path> --root <host root>
```

- **HEAD A (config)** classifies every credential-shaped leaf by VALUE SHAPE:
  `${VAR}` env-ref · `{env:VAR}` template · file path · **literal**.
  Both `${...}` and `{env:...}` are references; only the absence of both makes it plaintext.
- **HEAD B (filesystem)** takes each literal, hashes it, and reports every file on the host where that
  value lives. **No extension filter** — that is the whole point.

Confirm a shape claim by arithmetic, not impression. `{env:VAR}` templates carry no `$`, so a
`^\$\{...\}$` classifier drops them into the literal bucket. Measured length settles it:
`{env:MINIMAX_API_KEY}` = 21 characters, and the field measures 21.

Anchor key matching at the end (`token$`, `apikey$`) and exclude non-credentials that merely contain
the word — `maxTokens`, `token_budget`, `defaultSessionKey` are numbers and session identifiers, not
secrets. An unanchored substring match inflates the count; the anchored one is the honest one.

## Rule 2 — a negative needs the same warrant as a positive

"Host B holds no copy of this secret" is a claim. State the sweep: files walked, candidates compared,
what was skipped (size ceiling, vendor trees, symlinks), and that it is a strong negative and not a
formal proof. Then **test your own filter's blind spot** before publishing — if the filter keys on file
extension, go find the timestamp-suffixed files by name and hash-compare them directly.

## Rule 3 — before templating a credential, verify BOTH ends

Replacing a literal with `${VAR}` fails **silently** when the variable is absent from the environment
the *service* reads — not the shell you are in. A systemd unit reads only its `EnvironmentFile=`
entries; an interactive shell's exports are invisible to it.

1. List what the service actually reads (the unit's `EnvironmentFile=` lines).
2. Hash-compare the literal against every variable in those files. No match means a new variable must
   be minted, in a unit-owned file, as a separate deliberate act.
3. Check whether the credential has a **consumer at all** before preserving it. A peer entry with a
   token and no address, whose token exists on one host only, cannot authenticate — templating it just
   preserves an orphan.

## Rule 4 — retire by destroying the value, keeping the hash

For a credential verified dead (no counterpart, no address, no traffic):

1. Snapshot the config first (reversible structure).
2. Remove the consuming entry from the live config; verify **0 occurrences** by hash trace.
3. Redact the value in *every* copy — including historical backups — to
   `<RETIRED-<date> sha256:<hash>>`, preserving file validity, and record each file's before/after
   sha256 in a `REDACTION-INVENTORY.md`.
4. Delete any file whose entire content is the secret (nothing structural to preserve).
5. Re-run the counter and the hash trace. The target is **0 residual occurrences**.

Rationale: archiving a secret *is* the exposure being removed. A dead credential is destroyed; what is
kept is the receipt — where it lived, what it hashed to, why it was retired. If the capability is ever
revived, mint a **new** credential; never revive an exposed one.

## Rule 5 — a restart is not a health verdict

Service startup on these hosts ranged 12–61 s. A single short health poll that returns empty proves
nothing — re-poll, then read service state and journal before declaring anything down. Likewise never
declare an update failed before checking the upstream release: `2026.9.6` was both installed and latest,
and the "failed update" was two unrelated defects in the updater's ability to stop the service.
