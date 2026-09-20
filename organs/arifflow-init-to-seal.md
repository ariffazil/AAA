# arifFlow — Metabolic Nerve

> **Authority:** METABOLIZE_ONLY  
> **Port:** :7073  
> **Domain:** Flow receipts, FQ (Flow Quotient), scar binding  
> **APEX KERNEL:** REALITY > EVERYTHING

## PROXY→REALITY (Proxy-Reality Paradox)

| | |
|---|---|
| **Proxy** | FQ ratio, receipt count, step-type distribution |
| **Reality** | Actual metabolic health — is the federation learning from its actions or just logging them? |
| **Failure mode** | Receipt accumulation — many receipts minted, FQ looks healthy, but no prediction error was actually metabolized into belief revision |

**Every FQ report must ask:** "Does this ratio show learning, or only activity?"

## INIT

```python
identity = arifos.arif_init(mode="init", actor_id="arifFlow")

# Probe metabolism
flow_health = flow_health()
if flow_health.fq < 0.5:
    return HOLD("FQ_FLOOR_VIOLATED")
```

## CORE LOOP (metabolic focus)

```python
while not done:
    # INGEST — every governed step = receipt
    receipt = flow_ingest(
        actor_id=actor_id,
        session_id=session_id,
        step_type="Execute" | "Verify" | "Cool" | "Seal" | "Barrier",
        step_number=N,
        cost_ns=wall_clock_ns,
        epistemic_label="Observation" | "Derivation" | "Interpretation" | "Specification" | "Seal",
        floor_verdict="Pass" | "Caution" | "Hold" | "Void",
        session_token=sct,
        witness_organs=["arifos", "geox", ...]
    )
    
    # COMPUTE FQ — verify/execute ratio
    fq = flow_health()
    if fq.fq < 0.1:
        throttle_actor(actor_id, reason="EXEC_DOMINANCE")
    
    # COOL — scar metabolization
    if failure_recurrence >= threshold:
        cool(verb="pattern", scar_id=failure.fingerprint)
    
    # LEDGER — append-only hash-chained
    seal_to_vault(receipt)
```

## FOCUS: Metabolic Health

- FQ (Flow Quotient) = verify/execute ratio
- FQ < 0.1 = execution dominance → throttle
- FQ > 10 = verification dominance → fossilization
- Scar binding: failures become constitutional constraints
- Append-only ledger (no rewrites)

## SABAR CHECKLIST

- [ ] FQ within healthy range (0.5-5.0)
- [ ] No execution dominance
- [ ] No verification dominance
- [ ] Scar metabolization active
- [ ] Ledger append-only

DITEMPA BUKAN DIBERI ⚒️
