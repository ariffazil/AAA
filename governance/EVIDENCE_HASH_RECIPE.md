# arif_judge Rule #6 — Evidence Hash Canonicalization Recipe

> **Forged:** 2026-08-21 by 333-AGI (Δ MIND) — reverse-engineered from judge.py:1112-1141
> **Lesson (1373/1374):** a filename is a rumor; a hash is proof. And a hash computed
> with the WRONG canonicalization is a lie you told yourself.
> **Scar source:** 2 judge HOLDs (trc-942207d4aa42, prior) before recipe confirmed.

## The Recipe (VERIFIED live 2026-08-21, trc-c5557e0e23fe)

```python
import hashlib, json

# 1. Build evidence dict (content only)
evidence = {
    "field1": "value1",
    "field2": 42,
    # ... any content fields
}

# 2. Strip meta keys — judge EXCLUDES these from the hash:
#    evidence_hash, in_band, source
content = {k: v for k, v in evidence.items()
           if k not in ("evidence_hash", "in_band", "source")}

# 3. Canonicalize — CRITICAL: DEFAULT separators (", " and ": "),
#    NOT compact. This is where the mismatch happened.
canonical = json.dumps(content, sort_keys=True, default=str)

# 4. Hash
evidence_hash = hashlib.sha256(canonical.encode()).hexdigest()

# 5. Submit — add evidence_hash INTO the evidence dict
evidence["evidence_hash"] = evidence_hash
# → pass as `evidence` param to arif_judge
```

## The Two Traps

| Trap | Wrong | Right |
|------|-------|-------|
| **Separators** | `json.dumps(x, separators=(',', ':'))` (compact) | `json.dumps(x)` — **default separators with spaces** |
| **Hash field** | Hashing the dict INCLUDING `evidence_hash` | Judge strips `evidence_hash`/`in_band`/`source` BEFORE hashing |

## Rules Enforced (judge.py)

1. **Rule #1** — `evidence={}` or all-empty values → `EVIDENCE_EMPTY`, hard HOLD. No LLM call.
2. **Rule #6** — content fields present but no `evidence_hash` (and no `in_band=true`) → `EVIDENCE_HASH_MISSING`
3. **Rule #6** — `evidence_hash` present but ≠ computed → `EVIDENCE_HASH_MISMATCH` ("payload mutated in transit")
4. Hash comparison: `str(supplied).lower().removeprefix("sha256:")` — so `sha256:` prefix is optional.

## Downstream Gates (after Rule #6 passes)

Rule #6 is **not the last gate**. On the validation call it passed, then a NEW hold fired:
- **RASA_DERITA causal_cascade** — L3+/irreversible-classified actions require a
  `causal_cascade` payload. Include it for mutation-class judgments.
- Other known: Gate 1 (actor_id/session_id), Gate 2 (actor_signature for IRREVERSIBLE).

## Verified Hash Chain

- Reverse-engineered: `aeb44da67695ba60...` — reproduced exactly from judge's rejection message
- Live pass: `cf8d70dc0f4aeb79...` — judge accepted, error moved past Rule #6

DITEMPA BUKAN DIBERI ⚒️
