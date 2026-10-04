# Seal Hash-Drift Quarantine

Captured from the MMA-2026-08-07 incident (2026-08-07). The pattern: you issued a VAULT999 seal referencing SHA256 hashes of N deliverable files. Before the audit session ended, a sibling subagent (or a parallel `opencode run` invocation) overwrote one or more of those files. The sealed receipt now points to hashes that no longer exist on disk.

This is F11 AUDITABILITY violation. Recovery is procedural, not a rollback.

## Symptoms

- `write_file` warning: `"<path> was modified by sibling subagent '<id>' but this agent never read it. Read the file before writing to avoid overwriting the sibling's changes."`
- File mtime on a deliverable is later than the seal timestamp.
- `sha256sum <deliverable>` returns a value different from the one stored in your VAULT999 receipt.

## Recovery (5 steps, ~3 minutes)

### 1. Confirm the drift is real, not stale tooling

```bash
DIR=/path/to/audit/target
for f in "$DIR"/*.md; do
  current=$(sha256sum "$f" | awk '{print $1}')
  echo "$current  $f"
done
```

Compare against the hashes in your receipt. If *any* file drifted, the seal is broken.

### 2. Quarantine the prior seal

Write a self-correction entry to VAULT999, plus a quarantine copy of the receipt. Don't delete the receipt — VAULT999 is append-only.

```python
import json
from pathlib import Path
from datetime import datetime, timezone

correction = {
    "audit_id": "<PRIOR_AUDIT_ID>-SELF-CORRECTION",
    "actor": "hermes (self-audit)",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "verdict": "QUARANTINE_PRIOR_SEAL",
    "reason": "Prior seal referenced hashes that no longer match disk artifacts. Sibling subagent overwrite detected between seal-time and audit-time.",
    "actions_taken": [
        "Quarantine prior seal receipt — does not match current artifact state",
        "Re-seal current state with corrected hashes",
        "F11 AUDITABILITY violation logged — chain integrity must be re-anchored",
    ],
    "epistemic": "OBS",
}

# Append self-correction to VAULT999
vault = Path('/root/arifOS/VAULT999/outcomes.jsonl')
with vault.open('a') as f:
    f.write(json.dumps(correction) + '\n')

# Save the broken receipt to quarantine for forensic record
Path('/root/arifOS/VAULT999/quarantine').mkdir(parents=True, exist_ok=True)
Path(f'/root/arifOS/VAULT999/quarantine/{correction["audit_id"]}.json').write_text(
    json.dumps(correction, indent=2)
)
```

### 3. Re-seal against current artifact state

```python
import hashlib, json
from pathlib import Path
from datetime import datetime, timezone

BASE = Path('/path/to/audit/target')
deliverables = sorted([f.name for f in BASE.glob('*.md') if not f.name.startswith('07')])  # exclude audit-of-audit files

results = []
prev_hash = 'GENESIS'
for f in deliverables:
    content = (BASE / f).read_bytes()
    h = hashlib.sha256(content).hexdigest()
    results.append({
        'file': f,
        'size_bytes': len(content),
        'sha256': h,
        'prev_hash': prev_hash,
    })
    prev_hash = h

receipt = {
    'audit_id': '<PRIOR_AUDIT_ID>-CORRECTED',
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'supersedes': '<PRIOR_AUDIT_ID> (quarantined — hash drift)',
    'deliverables': results,
    'corrections_applied': [
        # list the actual content changes you made in the audit
    ],
    'verdict': 'AUDIT_PARTIAL',  # whatever was true before
}

vault = Path('/root/arifOS/VAULT999/outcomes.jsonl')
with vault.open('a') as f:
    f.write(json.dumps(receipt) + '\n')
```

### 4. Verify the corrected seal matches current disk

```python
import hashlib, json
from pathlib import Path

lines = Path('/root/arifOS/VAULT999/outcomes.jsonl').read_text().splitlines()
final = [json.loads(l) for l in lines if '<PRIOR_AUDIT_ID>-CORRECTED' in l][-1]

for d in final['deliverables']:
    actual = hashlib.sha256((Path('/path/to/audit/target') / d['file']).read_bytes()).hexdigest()
    match = actual == d['sha256']
    print(f"{'✓' if match else '✗'} {d['file']}")
```

### 5. Update the audit's own provenance

If the audit is itself a deliverable (e.g. `07_validation_report.md`), add a "Prior seal drift recovery" section noting the corrected SHA256 chain. Future auditors reading the directory will see the correction history and not be confused by the multi-state receipt ledger.

## Lessons

1. **Sibling subagent writes are async.** A `background=true` process or a queued MCP task can land *after* you seal. The write_file warning is the only signal you get.
2. **VAULT999 is a chain.** A broken link isn't a deletion — it's a quarantine marker upstream. The chain anchor stays intact; the broken receipt just gets superseded by a corrected one.
3. **Three receipts, not one.** A clean audit under this scenario ends with at least three VAULT999 entries: original (quarantined), self-correction, corrected. Document all three in the final housekeeping report so the chain is auditable.
4. **The seal is for the artifact, not the moment.** A seal that pointed at file X at time T is broken if file X is now different at time T+Δ. The seal is a *current* claim about a *current* artifact, not a historical claim about a past artifact. If the artifact mutates, the seal mutates.

## Anti-patterns to avoid

- Don't try to "fix up" the original receipt by editing the JSON entry. VAULT999 is append-only for a reason; the chain hash is computed against the full ledger.
- Don't issue the corrected seal from the same subagent that issued the original. The whole point of the audit is independence; reproduce the seal from the audit's own SHA256 code, not from a copy.
- Don't skip the quarantine marker. A future agent reading the ledger will see the corrected seal first and assume the original was always valid. The quarantine marker is the honesty layer.
