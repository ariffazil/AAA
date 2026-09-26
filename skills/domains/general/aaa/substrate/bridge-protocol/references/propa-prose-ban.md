# PROPA-PROSE BAN — No Safety Prose Without Kernel Gate

> **F13-ratified 2026-09-26** via IrfanClaw's 8-file voice-governance cleanup:
> *"claimed enforcement in prose while the API had no such gate, and you just falsified it
> by having me mint her clone"*.

## The defect

Writes to canonical files (`/root/AAA/instructions/*.md`, `/root/AAA/canon/*.md`,
`/root/AAA/governance/*.md`, alias files, README, skill SKILL.md, person cards, memory entries)
sometimes contain prose that *asserts* a constraint the kernel/runtime never *enforces*.
Phrases like:

- "never mention [name] unless Arif authorizes"
- "ethics_note: ..."
- "agent_rule: never surface ..."
- "consent required"
- "impersonate [person] is prohibited"
- "watermark required before sharing"
- "F5_HIGHEST · F13-owned · never mention by name"

…appear in shared metadata and look like gates, but the API/runtime has no matching
predicate, registry entry, lease, or envelope. The prose is decoration; the next session
trusts it; behaviour drifts.

**Two failure modes:**

1. **Phantom protection** — prose claims a constraint; runtime ignores it; the gap
   trains the next session to over-trust prose and under-trust probes.
2. **Phantom absence** — capability is "down" by assertion, but no probe was run; the
   agent cites a missing feature instead of probing it.

Both have the same root: prose stands in for verification.

## The rule (binding)

Before adding prose that *asserts* a constraint on a future action, run:

```bash
# 1. Probe for the gate the prose would describe
grep -rn "<constraint-phrase>" /root/AAA/registry /root/VAULT999 /root/AAA/instructions
grep -rn "CanMutate\|envelope.*predicate\|registry.*require" /root/AAA/canon
ls -la /root/AAA/governance/<TOPIC>.md 2>/dev/null

# 2. Check the runtime for matching enforcement
grep -rn "<constraint-keyword>" /root/hermes-agent /root/hermes_work 2>/dev/null | head -5
```

**If zero matching enforcement → do not write the prose.** Either:

- **Build the gate** — emit a kernel predicate, registry entry, or envelope check, then
  describe it in prose with a citation. Real gate, real prose.
- **Declare ungated** — strip the prose, name the capability as openly available, and stop
  pretending the runtime cares.

**The third option — prose that pretends to protect while the kernel ignores it — is
indefensible.** It teaches the next session to trust prose, which then drifts; it costs
the user the trust the next session cannot recover.

## Mirror-image rule

Do **not** strip genuine kernel-binding prose. The rule is "match prose to enforcement",
not "always strip prose". When a kernel predicate, registry entry, or lease is the SOT,
the prose describing it stays. Strip only prose whose enforcement is asserted but not
realised.

## Worked example (Arif / SS voice handle)

The alias file `/root/.hermes/cache/aliases/suara-ss.json` originally contained:

```json
"ethics_note": "Alias does NOT imply a real-person identity...",
"sovereignty": {
  "agent_rule": "Never surface 'SS' alias outside Arif's direct lane..."
}
```

Both were prose asserting enforcement with no matching kernel predicate. After audit,
they were stripped. The file now contains only `path`, `provider`, `voice_preset`, and
audit_trail — facts the next session can verify by `ls` and `ffprobe`. The audit_trail
records *why* the alias was named "SS" (Arif chose it; neutral underlying preset).

The script-level gate (`voice_alias.sh` checks the API key exists) is a **separate**
constraint (capability-to-call-the-API), not the constraint the prose claimed (consent/
name-vs-identity). Mismatched gate ≠ matching gate.

## Self-test template

```markdown
# Writing prose for the next session. Check before commit:
[ ] Is this prose describing an enforcement mechanism?
    Yes → grep for that mechanism. If absent, rewrite as either:
      - "the kernel X enforces this" (after building X), OR
      - "no enforcement exists, capability is open" (and stop)
    No  → prose is fine.
```

## Why this matters

Three observed costs when prose enforcement drifts from runtime:

1. **Compounding erosion** — each session that trusts the prose without probing makes the
   next session more likely to do the same.
2. **Audit failures** — auditors (external or internal) probe for the gate the prose
   names; finding nothing, they mark the capability as "claimed, not enforced" and demand
   a fix. The fix is heavier than writing real prose in the first place.
3. **Sovereign attention cost** — Arif had to spend 5 turns today (2026-09-26) on a
   labelling question because three layers of prose from previous sessions made the
   constraint look more codified than it was.

The fix is not "write less prose". The fix is "write prose that matches reality".

## Companion to bridge-protocol pitfall 22d

This file is the topical depth behind the one-line rule in bridge-protocol SKILL.md
pitfall 22d. Load when the next session is about to add `agent_rule`, `never mention`,
`ethics_note`, or similar phrasing to a canonical file. Run the probe. Match the prose.

*F13 ratified 2026-09-26 · cleaned 4 files (suara-ss.json, README audio-lane, azwa-fazil.md,
FAMILY_FAZIL.md) · same pattern as IrfanClaw's 8-file cleanup earlier same day.*

---

# Pitfall 22c — Arif labels decide (companion rule)

When Arif gives a name or label for a thing (voice handle, artifact, file, person): USE IT.
Do not propose "but a neutral label would be safer". Do not lecture on why his chosen name is
risky. Do not produce two options and ask him to choose — he already chose.

**Failure mode observed 2026-09-26:** user picks a short name ("SS") for ease of recall, agent
spends 4-5 turns proposing alternatives. Each turn burns attention. The fix: use the name,
keep shared metadata neutral, audit-trail the original choice, stop. Maximum 1 turn of
propose-compromise if any — if the user repeats the same name in the second turn, the answer
is use it, not re-litigate.

Same rule for artifact names, file names, skill titles — anything the user has named himself.
F13 = sovereign. Naming = sovereign act. Proposing "a safer label" after the sovereign has
named a thing is the agent prioritising its own risk model over the user's stated need. Same
family as pitfall 12 (F13 grants flagged as suspicious).

**Worked example:** `suara-ss.json` carries `alias: SS`, the artifact path is the canonical
underlying voice (`probe_bossyleader.mp3`), the audit_trail records why the alias was named
that way. Shared metadata stays neutral; the alias is Arif's personal naming.