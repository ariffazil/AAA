# bootstrap-load — Kernel Primitive Specification
# Type: IMMUTABLE KERNEL VERB (hardcoded in runtime image)
# This is NOT a skill. This is firmware.
# DITEMPA BUKAN DIBERI.

## Contract

### Name
`bootstrap-load`

### Type
Immutable kernel verb. Cannot be overridden by skills, manifests, or evolvers.

### Input
```
bootstrap_manifest: JSON    # Signed bootstrap manifest (see bootstrap_manifest.json)
```

### Pre-conditions
1. Kernel runtime image is loaded
2. Public root keys are embedded in runtime (not loaded from file)
3. Boot ledger exists and is append-only

### Execution Sequence (DETERMINISTIC — same input = same result on any node)

```
1. PARSE bootstrap_manifest JSON
   - If parse fails → HALT + emit BOOT_PARSE_FAIL to boot_log
   - If schema invalid → HALT + emit BOOT_SCHEMA_FAIL to boot_log

2. VERIFY SIGNATURES
   - For each entry in root_signatures:
     a. Extract key_id and sig
     b. Look up public key from embedded keyring (NOT from manifest)
     c. Verify sig against canonical hash of manifest (excluding signatures block)
     d. If ANY signature fails → HALT + emit BOOT_SIG_FAIL
   - If root_signatures is empty → HALT + emit BOOT_UNSIGNED
   - If at least ONE valid signature → PROCEED

3. SELF-HOST TEST (deterministic)
   a. Parse all 9 universal_skills entries
   b. Verify: name, invariant_id, hash, purpose, enforcement, veto all present
   c. Verify: no duplicate invariant_ids
   d. Verify: hash format matches ^sha256:[a-f0-9]{64}$
   e. Verify: boot_sequence has exactly 7 steps
   f. Compute SHA-256 of manifest file (canonical JSON, sorted keys, no whitespace)
   g. Compare to stored hash (if present)
   h. If ANY check fails → HALT + emit BOOT_SELF_HOST_FAIL
   i. If all pass → emit BOOT_PASS

4. REGISTER INVARIANTS
   - For each universal_skill in manifest:
     a. Create runtime hook: {enforcement_point, veto_flag, check_function}
     b. Hook is IMMUTABLE once registered (cannot be unregistered without kernel restart)
     c. Register in veto hierarchy order: L1 > L2 > L3 > L4 > L5
   - After all 9 registered → emit INVARIANTS_REGISTERED

5. APPEND TO BOOT LEDGER
   - Entry: {timestamp, manifest_hash, signature_status, invariant_count, node_id}
   - Format: JSONL, append-only
   - If append fails → HALT + emit BOOT_LEDGER_FAIL

6. OPEN SKILL LOADING
   - Set runtime flag: skills_loadable = true
   - Emit BOOT_COMPLETE
   - Skills can now be parsed from AAA/skills/
   - Every skill manifest runs through veto_check() against registered invariants

7. SKILL VETO GATE
   - For each skill manifest loaded:
     a. Check INV-9: sovereign_signature present?
     b. Check INV-1: evidence_schema declared?
     c. Check INV-3: reversibility declared?
     d. Check INV-8: does skill claim to veto a universal? (reject if so)
     e. If any veto fails → skill loaded in OBSERVE_ONLY mode (no mutations)
```

### Post-conditions
1. All 9 invariants registered as immutable runtime hooks
2. Boot ledger has new entry
3. External skills can be loaded (subject to veto checks)
4. Runtime is in known-good state

### Failure Modes
| Failure | Action | Recovery |
|---------|--------|----------|
| Parse fail | HALT | Fix manifest JSON |
| Signature fail | HALT | Re-sign with valid key |
| Self-host fail | HALT | Restore manifest integrity |
| Ledger fail | HALT | Check disk/permissions |
| Skill veto fail | QUARANTINE | Fix skill manifest or get sovereign signature |

### Security Properties
- Manifest is DATA (auditable, versionable, ledgerable)
- Root keys are FIRMWARE (embedded in runtime image, not loaded)
- Boot sequence is DETERMINISTIC (same manifest = same result on any node)
- Invariants are IMMUTABLE once registered (kernel restart required to change)
- Skills are GUESTS (subject to veto, can be quarantined)

### Two-Timescale Evolution
- FAST LANE (task skills): CI + canary. No sovereign signature required for non-substrate changes.
- SLOW LANE (substrate/bootstrap): Tri-witness ratification required. 7-day max latency.

### Interface
```python
# Pseudocode — kernel runtime
def bootstrap_load(manifest_path: str) -> BootResult:
    manifest = parse_json(manifest_path)
    
    if not verify_signatures(manifest, EMBEDDED_KEYS):
        return BootResult(status="HALT", reason="BOOT_SIG_FAIL")
    
    if not self_host_test(manifest):
        return BootResult(status="HALT", reason="BOOT_SELF_HOST_FAIL")
    
    hooks = register_invariants(manifest["universal_skills"])
    append_boot_ledger(manifest_hash(manifest))
    
    return BootResult(status="OK", hooks=hooks)

def veto_check(skill_manifest: dict, hooks: list) -> tuple[bool, list]:
    violations = []
    for hook in hooks:
        if hook.veto and not hook.check(skill_manifest):
            violations.append(hook.violation_report(skill_manifest))
    return (len(violations) == 0, violations)
```
