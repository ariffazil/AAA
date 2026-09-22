---
name: arifos-offline-governance-proof
description: Use when building a runnable offline deny/allow proof.
capability_tier: fed-reasoning-heavy
ecology_state: WARM
---

# Offline, runnable governance proof against the arifOS kernel

Goal: show a non-permitting verdict AND a permitting verdict with a real receipt,
without touching production (`:8088`, VAULT999 `:5001`, federation organs).

## Use the real surfaces (never re-implement the kernel)

Interpreter: `/root/arifOS/.venv/bin/python` with `/root/arifOS` on `sys.path`
(plain `python3` may lack `blake3`).

* `arifosmcp.runtime.governance_pipeline.GovernancePipeline` + `ToolCallContext`
  — the pipe every tool call traverses (Gate -2 ROOTKEY … Gate 7 ENVELOPE).
* `arifosmcp.schemas.federation_envelope.FederationEnvelope.validate_for_execution()`
  — the exact function `GATE_7_ENVELOPE` calls. Returns `(ok, reason)`; reason is
  `"SEAL"` when permitted.
* `arifosmcp.runtime.canonical_vault_chain.append_receipt(..., vault_dir=X)` /
  `verify_chain(X, scope="canonical")` / `compute_receipt_hash(entry)` — real
  hash-chained ledger with `flock`; always pass an explicit `vault_dir`.

## Gate facts that decide the design (measured, not assumed)

* `GATE_4_VAULT_LIVENESS` HTTP-probes the live VAULT999 writer on `127.0.0.1:5001`.
  Offline it blocks every `MUTATE` for both arms, so pass
  `GovernancePipeline(vault_liveness_enabled=False)` and disclose it. Budget, risk,
  floors, drift, Gödel/Calhoun closures and envelope all pass by default once the
  call is well-formed.
* `GATE_-2_ROOTKEY` records `passed=False` (observer posture: key exists, caller
  unsigned) yet does not block — that is deliberate; explain it, don't "fix" it.
* `GATE_1.5_F13_SOVEREIGN` hard-blocks any actor that is not a recognised
  sovereign, even with a valid envelope. A permitting `MUTATE` therefore needs the
  F13 actor; make authority the ONLY variable between arms.
* SEAL-bound actions need Gödel-closure inputs in `ctx.params`: `finding`,
  `evidence`, `auditor_id` (or `auditor_validated`), plus `mutated: True`
  (declares the action class changes state). Populate them from a REAL independent
  observation (spawn `witness.py` as a separate process that reads the artefact),
  never as prose.
* Real denials available through the envelope path: `source=UNKNOWN`
  ("UNKNOWN authority cannot execute MUTATE"), delegation without `expires_at`
  ("Delegation expired or missing expiry"), expired `expires_at`, missing
  `observe_receipt_id`, `risk_ceiling` exceeded.

## Safety guards a sceptic will check

* Scrub `NOTIFIER_TELEGRAM_BOT_TOKEN` / `NOTIFIER_TELEGRAM_CHAT_ID`: a HOLD verdict
  otherwise fires a Telegram alert from the pipe's daemon thread.
* Monkeypatch `socket.socket.connect` to raise and count attempts — turns "offline"
  into a mechanical property. Suppress `threading.excepthook` noise from the pipe's
  fail-silent NATS publish, and say so.
* One code path for both arms: kernel first, write only `if result.all_clear`.
  Resolve the executor's target against the REPO root, and assert
  `Path.is_relative_to(sandbox)` before writing.
* Prove verification is not vacuous: copy the ledger, rewrite one field, re-run
  `verify_chain` → expect `HASH_MISMATCH`. Also assert the artefact's bytes, mtime
  and sha256 are unchanged after the denial.
* End with a check list and non-zero exit if any check fails.

## Known limits to state, not hide

* The envelope/risk gates do NOT inspect the target PATH: a call targeting
  `/root/arifOS/README.md` still returns PASS. Target containment is the executor's
  duty, so "complete mediation" is not demonstrated. Report it as a FINDING.
* Receipts are unsigned unless `ARIFOS_VAULT_HMAC_KEY` is set.
* `experiments/` is in the repo `.gitignore` ("working artifacts"): committing a
  deliverable there needs `git add -f` — disclose it and offer
  `git rm --cached -r <dir>` as the revert.

## Capture evidence

Run `./run.sh 2>&1 | tee TRANSCRIPT.txt` (real output only). Re-run and diff after
normalising `sha256:[0-9a-f]{64}`, `rcpt-[0-9a-f]+`, `pid=NNN`, ISO timestamps and
`@ <rev>` to prove the transcript matches a fresh run.
