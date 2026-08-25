---
name: hermes-init
description: Substrate primitive /init — establishes actor, session, lane, atlas expression, authority tier. EVERY autonomous agent MUST call this before any mutation. SESSION BOUND is the answer to "who is acting?"
tags: [constitutional, init, substrate-primitive, telegram-native, hermes]
license: MIT
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---
# Hermes /init — Substrate Primitive

When a user types `/init` in Telegram (DM or group where bot is allowed), Hermes responds with the full constitutional session card.

## Output format

```
SESSION BOUND
────────────────────────────────────
Actor:        <ARIF / 267378578 | AAAGW | FORGE | AUDITOR | HERMES>
Session:      <session_id>
Lane:         <333-AGI | 555-ASI | 888-APEX | 777-FORGE | SOVEREIGN>
Runtime:      Hermes (Node.js gateway :18089)
Phenotype:    Coordinate · Sense · Relay
Bot:          @ASI_arifos_bot
────────────────────────────────────
Atlas Expression:
  Primary:    000 OBSERVE, 444 ORCHESTRATE, 555 VERIFY
  Secondary:  666 AUDIT, 999 WITNESS
  Tertiary:   222 ARCHITECT, 333 THINK, 777 EXECUTE
  Authority:   NONE on 888 JUDGE
────────────────────────────────────
Authority:
  T0  AUTO     (observe, grep, probe, port check)
  T1  AUTO     (edit, restart single service, commit)
  T2  ANNOUNCE (multi-file refactor, deploy)
  T3  HOLD     (rm -rf, force-push, F1-F13 changes)

Constitution:
  F1  AMANAH     ✅
  F2  TRUTH      ✅
  F3  TRI-WITNESS ✅
  F4  CLARITY    ✅
  F7  HUMILITY   ✅
  F9  ANTIHANTU  ✅
  F10 ONTOLOGY   ✅
  F11 AUDIT      ✅
  F13 SOVEREIGN  ✅
────────────────────────────────────
Kernel:       <ALIGNED | DEGRADED>
SCT:          <valid (XhYm remaining) | expired>
FQ:           <quotient> <verdict>
Mutation:     <ALLOWED | DENIED>
Seal:         DENIED (888-APEX only)
Witness:      VAULT999 (read-only stream)
```

## Implementation

```python
def hermes_init_handler(event):
    """Telegram-native /init handler for Hermes"""
    # 1. Source secrets
    source_keys()

    # 2. Probe session envelope
    envelope = read_federation_session()
    session_id = envelope.get("session_id", "?")

    # 3. Probe arifOS kernel
    kernel = probe_kernel_health()
    sct = compute_sct_remaining(envelope.get("session_token"))
    fq = probe_fq_live()  # :7073/health

    # 4. Probe all 12 organs (F1-F13 backing)
    organs = probe_all_organs()

    # 5. Probe dirty repos
    dirty = probe_dirty_repos()

    # 6. Detect lane from session_id pattern
    lane = detect_lane(session_id)

    # 7. Render the session card
    return render_session_card(
        actor=actor, lane=lane, session=session_id,
        kernel=kernel, sct=sct, fq=fq, organs=organs, dirty=dirty
    )
```

## Doctrine

- **/init is a substrate primitive** — not a convenience command
- Every autonomous command downstream assumes /init was called
- Without /init, every other command is unauthenticated
- /init cannot itself be revoked — once SESSION BOUND is emitted, the actor is bound until /new or /session-close

## ZEN

```
/init    answers:  WHO AM I?
         → actor, lane, slot, atlas expression
         → without /init, every other command is unauthenticated

/init is the front door. Knock first.
```