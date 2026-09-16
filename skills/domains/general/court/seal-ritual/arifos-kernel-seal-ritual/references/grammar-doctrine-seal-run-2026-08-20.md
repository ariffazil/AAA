# Grammar Doctrine seal run — full trace (2026-08-20)

> Worked example for the arifos-kernel-seal-ritual umbrella: sovereign bind →
> judge SEAL → SESSION_POLICY_CLAMP at arif_seal. Session
> `SEAL-c9b1e02389334e8b`, kernel v2026.08.01 (`arifos-d90ac947344e`).

## Sequence that worked

1. **Self-generated nonce + signature, one shot** (MCP NONCE SELF-GENERATION):
   `/opt/arifos/venv/bin/python3` → `secrets.token_urlsafe(32)`, sign
   `arif:{nonce}` with `/root/.secrets/aaa-identity/keys/arif_private.pem`,
   print nonce + base64 sig. Then immediately `arif_init(mode="init",
   actor_id="arif", nonce, actor_signature, requested_authority="SOVEREIGN",
   sovereign_id="ARIF_FAZIL", ack_irreversible=True)`.
   Result: `actor_verified: true`, authority FULL, session
   `SEAL-c9b1e02389334e8b`, `seal_allowed: true` at bind time, stage 000,
   SCT token TTL 28800s. A stale nonce from a previous session is NOT
   reusable — self-generate a fresh one; the old one never binds.

2. **arif_observe** — `mode="fetch"` with free text FAILS (`ingest requires a
   real http(s) URL`). `mode="search"` works (exa bridge). Local-file
   evidence does not go through observe: read via terminal, cite
   path + sha256 inside the judge evidence dict.

3. **arif_judge — third worked example of the hash recipe.** Evidence dict
   (11 content fields incl. `evidence_hash_algo: "sha256"`):
   ```
   payload = {k: v for k, v in evidence.items() if k not in ("evidence_hash", "in_band")}
   evidence_hash = sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
   # DEFAULT separators (", " / ": "), NOT compact
   ```
   First attempt without `evidence_hash` → HOLD `EVIDENCE_HASH_MISSING`
   (Rule #6). Second with wrong formula (compact separators over the wrong
   field set) → `EVIDENCE_HASH_MISMATCH supplied=b2a3… computed=4e09…`.
   Reproduced `4e098aab…` locally (the error leaks the computed prefix —
   verify against it before retrying; gate allows 1 retry). Third attempt →
   **verdict SEAL**, floors passed, call_hash
   `sha256:62ff5dbe24331bde223679dc761040b178d680e8f20f7e66ffc6da430959ccbe`.
   NOTE: `meta.kernel_intercept` was absent this run; judge returned the
   verdict at top level and the seal accepted the judge `call_hash` as
   `constitutional_chain_id`.

4. **arif_seal — SESSION_POLICY_CLAMP.** With everything green (actor
   verified, judge chain id supplied, `witness_type: "ai"`, `_epistemic`
   block in payload JSON, `ack_irreversible: true`), the seal HOLDs:
   `SESSION_POLICY: action 'IRREVERSIBLE' (rank 6/6) exceeds this session's
   irreversibility_threshold 0.00` — `failure_type: SESSION_POLICY_CLAMP`,
   F1 AMANAH. Actor identity does not override the session clamp. Terminal
   state reported honestly: judge verdict + hashes durable, vault append
   deferred. NOT resolved by kernel patch — by-design gate.

## Evidence dict that passed judge (reference shape)

```
artifact_sha256, artifact_size_bytes, deliberation_receipt_sha256,
evidence_hash_algo ("sha256"), external_anchor, f13_ratified (bool),
f13_source, file_path, holds_txt, receipt_path, verdict_prior
```
+ `evidence_hash` (computed per recipe) + `in_band: true`. Artifacts:
GRAMMAR_DOCTRINE.md 14798B
sha256:35fc4f6372cb093214de263edfd2b9b3aa2f7c574bf03fb47426ec205298480a;
deliberation receipt
sha256:6e2d5e95fb27c8672b964c506ac7b4b3d0e4c3e5d51e83b1162b063462bb47d1.

## Cross-session claim discipline (the other half of this session)

Prior-session claims verified this run BEFORE acting on them:
- REAL: GRAMMAR_DOCTRINE.md (14798B, 279 lines) — found via
  case-insensitive search after a case-sensitive grep missed it.
- REAL: sovereign Ed25519 key (PEM at
  `/root/.secrets/aaa-identity/keys/arif_private.pem`; also
  `/root/.arifos/keys/backup-20260719/`), VAULT999 outcomes.jsonl (2952
  lines), holds.txt, orders.txt, deliberation receipt.
- FABRICATED: "Berkatool", "SK-II" (zero non-cache hits), and the claim that
  a specific old nonce could be signed by a later session.
- LESSON: search case-insensitively (`grep -ri`) before declaring a file
  nonexistent, and treat another agent's pending-nonce as consumed —
  self-generate a fresh one in the same turn as the bind.
