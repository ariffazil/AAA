# ROLLBACK — exact instructions

Mission `LAYER_B_DISCOVERY_CLOSURE_AND_FED_CALIBRATION` · 2026-10-26 · actor 333-AGI
Every mutation below is reversible. Nothing was deployed to a public surface, so **no rollback
touches anything an external reader could have consumed.**

## What was mutated (complete list — 3 files)

| # | path | change | reverse with |
|---|---|---|---|
| 1 | `/root/AAA/federation/organs.yaml` | +16 / −0 (4 interface blocks) | step A |
| 2 | `/root/arif-fazil.com/sites/arif-fazil.com/public/.well-known/capabilities.json` | +1 / −1 (one `protocol` value) | step B |
| 3 | `/root/AAA/ops/capabilities/compile_machine_contract.py` | v1.0 → v1.1 | step C |

Lock status differs by target, and this was corrected after the 888 verify lane flagged the
original wording as self-contradictory:

- The **AAA trees** (`/root/AAA/federation`, `/root/AAA/ops/capabilities`) are locked with
  `chattr +i`. Every write and reversal there must go through `/root/scripts/canon-mutate`,
  never `chattr -i` by hand.
- The **arif-fazil.com site file** is **not** `chattr`-locked, so plain `git checkout --` is the
  sanctioned reversal path for it (confirmed: a direct write there succeeds, a direct write into
  the AAA tree fails with `Operation not permitted`).

## Step A — revert organs.yaml

    export ARIFOS_AGENT_ID=<your-actor> ARIFOS_TRACE_ID=trc-rollback-layerb
    git -C /root/AAA show HEAD:federation/organs.yaml > /tmp/organs.pre.yaml
    SHA=$(sha256sum /tmp/organs.pre.yaml | cut -d' ' -f1)
    /root/scripts/canon-mutate run /root/AAA/federation \
      --expect-target /root/AAA/federation/organs.yaml --expect-sha256-post "$SHA" \
      -- cp /tmp/organs.pre.yaml /root/AAA/federation/organs.yaml

Verify: `git -C /root/AAA diff --stat -- federation/organs.yaml` must print nothing.
Pre-patch blob for cross-check: `0fd38b7a939a65d303e00fe24d6574b26a40ea23`.

## Step B — revert capabilities.json

    git -C /root/arif-fazil.com checkout -- \
      sites/arif-fazil.com/public/.well-known/capabilities.json

This directory is **not** `chattr`-locked, so plain git is the sanctioned path.
Verify: `git -C /root/arif-fazil.com diff --numstat -- sites/arif-fazil.com/public/.well-known/capabilities.json`
must print nothing. Pre-patch blob: `4f457d7eddd50c89a5df68945002ef772a4bc6e7`.

## Step C — restore compiler v1.0 (only if the v1.1 measurement is rejected)

v1.0 is not on disk any more; it is reproducible from the two documented changes:

1. `response_schema` — v1.0 hard-coded `{state: "undeclared", reason: "MCP tools/list exposes no
   outputSchema…"}`. v1.1 calls `response_schema_decl(t)`, which reads the live `outputSchema`.
2. timestamps — v1.0 stamped artifacts with wall-clock `NOW`. v1.1 stamps them with the evidence
   timestamp (probe-cache mtime under `--no-probe`, probe-completion time otherwise). This is what
   makes acceptance gate 10 (byte-identical recompile) satisfiable.

v1.0 sha256 for identification: `ea1bd293fcf82ab3c64f1681395cd06c429bf675aeecea9213afe0124ec853b8` (26080 B).
v1.1 sha256: `48782166194e184126d42695d8d54b498ccb6171bb20e85f1623b1dce0996bca` (28553 B).

    export ARIFOS_AGENT_ID=<your-actor> ARIFOS_TRACE_ID=trc-rollback-layerb
    /root/scripts/canon-mutate run /root/AAA/ops/capabilities \
      --expect-target /root/AAA/ops/capabilities/compile_machine_contract.py \
      --expect-sha256-post <sha-of-the-file-you-place> \
      -- cp <v1.0-file> /root/AAA/ops/capabilities/compile_machine_contract.py

Note: reverting the compiler **re-introduces defect C1** (it will again report
`response_schema 0/258`, which is false — the true value is 138/258). Revert only with that
knowledge.

## Step D — remove mission artifacts (optional; they are inert)

    rm -rf /root/work/mission-layerb-20261026        # staging workspace on disk
    rm -rf /root/work/seal-fix-20261026 /root/work/seal-stage   # later working copies

    # The canonical copies live in a SUBDIRECTORY, not directly in ops/capabilities:
    export ARIFOS_AGENT_ID=<your-actor> ARIFOS_TRACE_ID=trc-rollback-layerb
    /root/scripts/canon-mutate run /root/AAA/ops/capabilities \
      --expect-absent --expect-target /root/AAA/ops/capabilities/layerb-mission-20261026/DISCOVERY-SOT-REPAIR.md \
      -- rm -rf /root/AAA/ops/capabilities/layerb-mission-20261026

    # Also: the doctrine copy and the eureka append are NOT rolled back — they are history.
    #   /root/work/doctrine/EUREKA-HUMAN_TO_AGENTIC_STATE-v1.md   (transcription, not promotion)
    #   /root/memory/eureka-entries.jsonl  entry E-HUMAN_TO_AGENTIC_STATE-v1-20261026
    # And the tmpfs quarantine is intentionally kept: restoring it would re-fill the tmpfs.

The candidate contract and extension schema are **data only** — no runtime reads them, so deleting
them changes no behaviour.

## What does NOT need rollback

- **Live public surface:** untouched. `https://arif-fazil.com/.well-known/capabilities.json` still
  returns `protocol: "mcp"` for `observatory_snapshot` (confirmed HTTP 200 + content check after all
  mutations). `machine-contract.json` and `contract-coverage.json` on the public surface are the
  earlier session's artifacts, sha `7921e5bf…` / `6b5182fe…`, not rewritten by this mission.
- **No service was restarted.** organs.yaml is read by consumers at their own cadence; the added
  keys are additive and match the vocabulary already used by `components[id=arifos]`.
- **No mutating tool was executed.** The only `tools/call` invocations were 6 read/compute-safe FED
  tools. `fed_report_latency` was not called.
- **Memory writeback** (`/root/memory/carry_forward.json`, `eureka-entries.jsonl`) is append-only
  history and is intentionally not rolled back — it records what happened, including the errors.

## Verification after any rollback

    /usr/bin/python3 /root/AAA/ops/capabilities/compile_machine_contract.py --no-probe \
      --out-dir /tmp/rollback-check
    # expect: live tools 258 · organs live 13 · a-forge 118 · fed 7
    # after step A the SOT defect for fed reappears (that is the pre-mission truth)
    # after step B the observatory_snapshot protocol defect reappears (also pre-mission truth)
