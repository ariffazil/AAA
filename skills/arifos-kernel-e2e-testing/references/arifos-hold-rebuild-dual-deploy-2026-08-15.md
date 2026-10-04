# KRT run B — HOLD-rebuild finalizer + dual-deploy surface (2026-08-15)

Session: KRT-JOHOR-2026-08-15, kernel session `SEAL-86269a147bed419c` (second KRT
run that day; run A = `SEAL-4aef2edeb8e34417`, see `krt-johor-reality-test-2026-08-15.md`).
Outcome: root-cause map for delta_S-null and receipt-dishonesty, 4 patches landed
(commit `d55c12a45`, e2e 27/27), one open defect remains (finalizer HOLD-rebuild).

## 1. Deploy surface: the kernel loads arifosmcp from TWO trees

`systemctl cat arifos` → `WorkingDirectory=/opt/arifos/app`, venv
`/opt/arifos/venv`. But the runtime can import `arifosmcp` from
`/opt/arifos/venv/lib/python3.13/site-packages/arifosmcp/` — a THIRD copy besides
the repo and `/opt/arifos/app`.

- Symptom: patch markers present in `/opt/arifos/app/arifosmcp/runtime/tools.py`
  (5 hits), ZERO in site-packages; live behavior unchanged after restart.
- Mask: running `cd /root/arifOS && /opt/arifos/venv/bin/python -c "import arifosmcp..."`
  resolves to the REPO tree (cwd precedence) — proves nothing about what the
  service imports. Don't trust it as a deploy check.
- Correct sync (all three, every time):
  ```bash
  rsync -rt --checksum --exclude='.git' --exclude='__pycache__' --exclude='.venv' \
    arifosmcp/ /opt/arifos/app/arifosmcp/
  rsync -rt --checksum --exclude='__pycache__' \
    /opt/arifos/app/arifosmcp/ /opt/arifos/venv/lib/python3.13/site-packages/arifosmcp/
  git rev-parse HEAD > /opt/arifos/app/.git_commit
  systemctl restart arifos   # T2: announce first
  ```
- Then verify by BEHAVIOR probe (vitals delta_S, forge-trap fields), not by
  import-path or `drift:false` — `drift` only compares commit IDs, and both
  stale and fresh trees reported `drift:false` at different moments.

## 2. delta_S=null root-cause chain (three layers, two fixed, one open)

1. **Confidence-gate exempt list** — `tools.py ~l.8186` `_is_observe_class` mode
   list lacked `entropy_dS`, so the envelope confidence path held a read-only
   measurement pre-run. FIXED in `d55c12a45` (added to exempt list).
2. **Handler is correct** — `mode == "entropy_dS"` branch (`tools.py ~l.12138`)
   computes real contradiction density and passes `delta_S=_dS` to `_ok()`.
   Never doubted the sensor again.
3. **OPEN: response finalizer HOLD-rebuild is the last writer.** With kernel-core
   `_CORE.evaluate` returning HOLD (L02/L03/L04/L07/L08) on this substrate, the
   finalizer (`_compute_canonical_verdict` → envelope rebuild, `tools.py ~l.4570–4710`)
   replaces `result` with a stub (`_wrapper_degradation`, `reasons`, actor ids only).
   Proof: post-deploy, fresh pid, both trees carrying patch markers,
   `mode=vitals` — whose handler hardcodes `delta_S=0.001` — still returned
   `delta_S: null`. A hardcoded measurement cannot be swallowed by the sensor;
   only the finalizer can erase it. Next fix lives THERE, not in `_hold()`/`_ok()`.

Consequence: patches to envelope BUILDERS (`_hold` fields P2: `execution_state:
BLOCKED`, `can_claim_success: false`) never reached the wire — the finalizer
normalizes after them. Verified: live forge-trap response had
`execution_state: None`. When patching envelope shape, patch the LAST writer
(finalizer), or accept the fields are cosmetic until then.

## 3. Ledger tri-map (resolves the 1761/1357 "disagreement")

| File | Lines | Reality |
|---|---|---|
| `/root/arifOS/VAULT999/vault999.jsonl` | 10 | Live chain v3; `verify_vault_chain.py` → per-file INTACT, 1 strict link break, 2 sub-chains, overall **DEGRADED** |
| `/root/arifOS/VAULT999/outcomes.jsonl` | 53,146 | Mixed eras: ~58% calibration-era entries (`decision_id` keyed, no seal id/ts), ~1,339 receipt-era with id+ts, PLUS raw diagnostic events |
| `/root/.local/share/arifos/vault999/outcomes.jsonl` | 2,952 | Third location, legacy |

- `arif_seal mode=verify` reads `outcomes.jsonl`; ledger_size (1761) vs
  chain_length (1357) count different subsets of a mixed-era file — not a broken
  counter. Do not "reconcile" by deleting; classify by era first.
- Defect class: **diagnostics appended into the seal ledger** —
  `arif_think` timeout receipts (`{"event":"ARIF_THINK_TIMEOUT",...}`) written
  raw into `outcomes.jsonl` at `tools.py ~l.6606`. Diagnostics need their own
  stream; they pollute seal counts and id-null percentages.

## 4. Patch discipline

- **`py_compile` passes NameError.** A patch referencing variables out of scope
  (`out`, `result_payload` used inside `_constitutional_gate`, a pre-execution
  function that never had them) compiled clean and would have crashed at first
  HOLD. Always re-read the enclosing function's signature/locals after writing
  a patch that touches response plumbing — or run the touched path via a probe
  before declaring victory.
- Terminal hardline blocklist fires on oversized inline python heredocs; the
  blocked payload is saved to `blocked-scripts/blocked-<id>.sh` and re-runnable
  with `bash <path>`. Keep kernel patches as small anchored replaces.

## 5. Verified-good commands (this session)

```bash
# e2e suite — first-ever 27/27 (incl. vault-corruption detector), ~5s
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /root/arifOS/.venv/bin/python -m pytest \
  tests/test_e2e_kernel.py -q --tb=line --rootdir=/root/arifOS -p no:cacheprovider

# official chain verdict
timeout 90 /root/arifOS/.venv/bin/python scripts/verify_vault_chain.py
```

Patches in `d55c12a45`: entropy_dS observe-exempt; `_hold()` emits
status HOLD / execution_state BLOCKED / can_claim_success false / can_mutate false
(+ `delta_s` passthrough param); `verdict.py` `_EXECUTION_STATE_BY_VERDICT[HOLD]`
→ `AWAIT_INPUT`; VERDICT_LOOP_REQUIRED gate returns instrumented `hold_envelope`.

## 6. "Mystery 46-step session" attribution (same day)

Mid-run, an out-of-band alert described "an authorized Hermes agent running 46+
terminal mutation steps, replying Forbidden to the OpenClaw bot chat — runaway?"
Attribution: **it was this session itself.** The described greps
(`_is_observe_class`, `cd /root/arifOS`) matched our own probe trail one-to-one;
`ps aux | grep -i hermes` showed no second agent session; the Forbidden sends
were our turn-update streaming mis-routed to the bot peer chat (blocked =
correct fail-closed, just noisy routing). Rule: before responding to any
"intruder/runaway session" alert, diff the described command trail against YOUR
OWN recent terminal calls. The boring explanation (it's you) beats the exotic
one (intruder) most of the time. (Broader home for this lesson would be
`federation-runtime-forensics`, which is bundled/protected — noted for adoption
via `hermes curator adopt federation-runtime-forensics`.)

