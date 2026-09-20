# A-FORGE — Execution Shell

> **Authority:** EXECUTE_AFTER_SEAL  
> **Port:** :7071/7072  
> **Domain:** forge_*, shell, git, docker, browser, vault  
> **APEX KERNEL:** REALITY > EVERYTHING

## INIT

```python
# A-FORGE never initiates — it executes after 888 + 999
session = forge_session_init(
    actor_id=actor_id,
    session_id=session_id_from_arifOS,
    lease_id=lease_id_from_arifOS
)

# Verify authority envelope
authority = verify_envelope(session)
if not authority.mutation_allowed:
    return HOLD("MUTATION_NOT_AUTHORIZED")
```

## CORE LOOP (execution focus)

```python
while not done:
    # RECEIVE — task from 333-AGI after arif_judge SEAL
    task = forge_pipeline_run(task=task, mode="forge")
    
    # VERIFY_LEASE — required for MUTATE
    if task.action_class in ["MATERIAL", "IRREVERSIBLE"]:
        if not lease.verify(task):
            return BLOCKED("LEASE_INVALID")
    
    # EXECUTE — under constitutional gate
    result = forge_shell(
        command=task.command,
        expected_output=task.expected_output,
        lease=task.lease
    )
    
    # RECEIPT — every action sealed to VAULT999
    forge_receipt_draft(action=task, result=result)
    
    # VERIFY — did it actually work?
    outcome = forge_shell_ledger(verify_chain=True)
    
    # OBSERVE — what changed?
    reality = arifos.arif_observe(mode="vitals")
    
    # LEARN — scar or promote
    if outcome.failed:
        forge_scar(failure=outcome)
```

## FOCUS: Constitutional Execution

- Never execute without lease
- Every action = receipt
- Every receipt = hash-chained
- Every chain = verifiable

## SABAR CHECKLIST

- [ ] Lease valid for action class
- [ ] Command within authority envelope
- [ ] Receipt minted to VAULT999
- [ ] Outcome verified, not assumed
- [ ] Scar on failure, promotion on success

DITEMPA BUKAN DIBERI ⚒️
