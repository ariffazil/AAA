# Seal Receipt Template — Post-Deploy Non-Mutation Verification

> Use when sealing a "deploy ja la" or "seal semua benda" sovereign instruction.
> The seal receipt is the ONLY artifact that survives after a session ends.
> Treat it as if it will be re-audited by an external Claude / Opus / Gemini
> audit. **Honest disclosures are non-negotiable.**

## Template

```markdown
# SEAL RECEIPT — YYYY-MM-DD Post-Deploy Verification

**Sealed by:** <agent name + role>
**Authorizer:** <Arif / 888 — quote the sovereign instruction verbatim>
**Session:** <session name>
**Timestamp:** <UTC ISO8601>

## Deploy actions taken

| # | Action | Status | Risk | Reversible |
|---|---|---|---|---|
| 1 | <action> | ✅ / ⚠️ / ❌ | Low/Med/High | Yes/No |
| 2 | <action> | ... | ... | ... |

## Source code modifications

<list paths modified, OR write "ZERO modifications">

## VAULT999 chain mutations

<list chain entries written, OR write "ZERO chain writes">

## T3 actions (irreversible)

<list any 888_HOLD-gated actions, OR write "NONE taken">

## What worked

- <bullet: what was actually accomplished>

## What didn't work (honest report)

### Bug X: <name>

**Status before deploy:** <observed>
**Status after deploy:** <observed>

<concrete repro recipe, file:line if known>

This is an open finding. The external auditor should see the same gap.

### Mistake Y: <name>

**What I did:** <description>
**What I should have done:** <description>
**Mitigation:** <description>

## Recommendations for next session

1. <prioritized fix list>

## Artifacts

| Path | Purpose |
|---|---|
| <path> | <what's in it> |
| ... | ... |

## Final state

```
Service:        <name + version>
Commit:         <git SHA, source == runtime if matched>
Protocol:       <advertised + supported>
Tools:          <N/M canonical>
Vault:          <healthy / known gaps>
Hook:           <which hook is active>
Source mods:    <count>
Chain mods:     <count>
Drift:          <aligned / drift_detected, with cause if known>
```

## ΔS

```
entropy_delta: <value>
peace_squared: <value>
vitality_index: <value>
```

DITEMPA BUKAN DIBERI ⚒️

---

**SEAL::<agent>-post-deploy-YYYY-MM-DDTHH:MMZ::ΔS=<value>::<hook>=<name>::source=<untouched|modified>::chain=<untouched|modified>::ready=<for-external-audit|not-ready>**
```

## Worked example (2026-08-07)

The full receipt from the 2026-08-07 session is at
`/root/forge_work/post-deploy/SEAL-RECEIPT-2026-08-07.md`. Key features:

- **5-row deploy actions table** with status + risk + reversibility
- **Source/chain/T3 zero-modification attestations** at the top
- **"What didn't work" section** that explicitly named the
  `floor_passed=True + effective_verdict=HOLD` contradiction still present
  post-deploy (the external Claude audit was expected to find this)
- **Mistake disclosure**: "I overwrote a prior pre-push hook without
  backing up first" — preserved the prior to `RECOVERED-pre-push-pre-my-install.sh`
- **Closing seal line** with ΔS + hook identity + ready state

## What NOT to do

- ❌ Claim "all patched" when audit-confirmed bugs remain
- ❌ Hide mistakes made during the session
- ❌ Synthesize artifacts that weren't actually produced
- ❌ Skip the "still open" section to make the receipt look cleaner
- ❌ Use ceremonial templates that make the receipt look more substantial than it is
