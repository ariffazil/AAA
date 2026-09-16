# HIB Reader Dormancy — Silent False-Negative Filter (2026-08-13)

## The investigation chain

Symptom: Qdrant access log showed ZERO `query_points` calls over 24h, while the
reader code path clearly existed. Diagnosis went through four hypotheses before
landing on the truth.

```
arif_think(mode=reason)
  → tools.py:10681 "reason": ["arif_mind_reason"]
  → tools.py:13369 _arif_mind_reason → tools_internal.py:1157 (mode=="reason")
  → runtime/mind_reason.py
     line 352-382: HIB block wrapped in `try/except Exception: pass`
     line 354:     from arifosmcp.hib.hib_emd_hook import hib_pre_reason_check
     line 356:     await hib_pre_reason_check(query=..., session_id, actor_id)
  → hib/hib_emd_hook.py:36 hib_pre_reason_check
  → hib/hib_gate.py:236 async def interrogate()
  → hib/hib_gate.py:267 self.vectorizer.search(score_threshold=tau_threshold)
  → hib/vault_vectorizer.py:352 self.client.query_points(collection="arifos_precedent",
                                       query_filter=Filter(must=[blast_radius==Lx]))
```

## The false leads (all turned out NOT to be the cause)

1. **"Except Exception: pass swallows HIB"** — line 381-382 does swallow errors
   silently (a real fragility), but it was NOT the cause: the reader fired clean
   and returned a normal `HIB_NONE`, no exception.
2. **"sentence_transformers / fastmcp missing"** — FALSE. Probing from a bare
   `/root` `python3` gave `No module named 'fastmcp'` and a `huggingface-hub`
   version complaint. Running under the kernel's real interpreter
   (`/opt/arifos/venv/bin/python` + `PYTHONPATH=/opt/arifos/app`) both imports
   succeed. **Wrong-env probe ≈ false dormant verdict.**
3. **"tau_threshold=0.95 too strict"** — FALSE. Even at `tau=0.0` (match
   everything) the search returned zero matches.

## The real root cause — silent filter mismatch

```python
# STORED points (from vault_vectorizer._build_payload):
#   blast_radius = entry.get('blast_radius', '') 
#   → stored as <NONE> because the write path never classified/populated it.

# READER (HibGate.interrogate):
#   query_blast_radius = classify_blast_radius(query_text)   # e.g. "L3_CRITICAL"
#   query_filter = Filter(must=[FieldCondition(key="blast_radius",
#                            match=MatchValue(value="L3_CRITICAL"))])
#   → NO stored point has blast_radius ∈ {L1,L2,L3} → 0 hits, HIB_NONE, no error.
```

Every query was classified to a blast radius, the filter required a matching
label, no stored point carried a label. Result: silently empty forever. The
reader was alive, firing, and structurally incapable of returning a hit.

## The disambiguating probe (one pass settles it)

```python
# 1. Fire the reader live under the SERVICE's own env, tau=0.0 (match everything)
import sys, os
sys.path.insert(0, "/opt/arifos/app")
os.environ.setdefault("PYTHONPATH", "/opt/arifos/app")
from arifosmcp.hib import HibGate
gate = HibGate()
r = gate.interrogate_sync(query_text="agent irreversible action identity binding",
                          tau_threshold=0.0, limit=5)
print(r.verdict, r.match_count, r.error)   # → HIB_NONE 0  (no error)

# 2. Dump what's actually STORED on the filter key
curl -s localhost:6333/collections/arifos_precedent/points/scroll | \
  jq '.result.points[].payload.blast_radius'
# → <NONE> for every point

# 3. Verify the query's classified flange
from arifosmcp.hib.hib_gate import classify_blast_radius
classify_blast_radius("agent irreversible action identity binding")  # → "L3_CRITICAL"
```

If stored `blast_radius` is `<NONE>`/absent AND the reader filters on it AND the
query classifies to a real L1/L2/L3 → the filter can never match → silent empty.

## Wrong-env probe — how to find the service's real interpreter

```bash
systemctl cat arifos.service | grep -E 'ExecStart|Environment=PYTHONPATH|WorkingDirectory'
# → ExecStart uses /opt/arifos/venv/bin/python
# → PYTHONPATH=/opt/arifos/app   WorkingDirectory=/opt/arifos/app

# Run probes through that interpreter:
/opt/arifos/venv/bin/python -c 'import fastmcp, sentence_transformers; print("ok")'
```

Never conclude "module missing / reader dead" from your default shell python —
the service lives in its own venv with its own site-packages.

## Fixes (root-cause + fail-safe, do both)

- **A (root cause):** writer (`vault_vectorizer._build_payload`) sets a real
  `blast_radius` from `classify_blast_radius(payload)` at write time, so stored
  labels match what the reader queries.
- **B (fail-safe):** reader (`HibGate.interrogate` / `vectorizer.search`)
  skips the blast-radius filter when no stored point carries the field, so
  legacy/seed points aren't permanently stranded behind the filter.

Do NOT loosen the tau threshold — it is masking the bug, not fixing it.

## Why "reader dormant" vs "reader filter-empty" matters

- Dormant = wiring gap → rewire the call path.
- Filter-empty = writer-reader schema mismatch → align the field at write time.
Wrong diagnosis leads to a pointless pipeline rebuild. The `tau=0.0` probe + a
dump of the stored filter-key disambiguates in one pass.

## Lesson for the class

The reader-layer cousin of the hash-chain-lineage trap: measure against what the
system actually STORES, not what the reading code assumes it stored. A filter on
an unpopulated field is silent — it returns empty success, not an error. Always:
(1) prove the reader runs (service env, tau=0), (2) inspect the stored filter-key
values, (3) only then decide wiring vs schema vs threshold.