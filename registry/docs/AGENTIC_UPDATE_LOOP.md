# Agentic Update Loop

```
DISCOVER → PROBE → RECONCILE → VALIDATE → PROPOSE → AUTHORIZE → PUBLISH → WITNESS
```

Implemented by `registry/update.py`. Boundaries are constitutional, not stylistic:

| Stage | May do | May NEVER do |
|---|---|---|
| DISCOVER | read catalogs, SOT, registry | write |
| PROBE | issue the exact four-field probe contract, append one receipt | overwrite/delete old probes; print secrets |
| RECONCILE | compare declared vs catalog vs requested vs resolved | smooth a mismatch into a PASS |
| VALIDATE | schema, references, duplicates, conflation, secrets, append-only | self-certify an unfixable error |
| PROPOSE | emit patch preview + human-readable diff | commit |
| AUTHORIZE | — (HUMAN ONLY: F13 SOVEREIGN) | be self-issued by the updater — there is no authorize verb |
| PUBLISH | governed git-lane commit + mirror-cycle push (by hand) | bypass `mirror-cycle.sh`; mutate production routing |
| WITNESS | verify push parity + generated hashes post-publish | alter what it witnesses |

## Rules (from the sovereign brief)

1. The updater may auto-prepare and auto-validate a patch. That is the ceiling.
2. It must not silently mutate production routing.
3. It must not auto-promote a model into consequential roles.
4. It must not create its own constitutional authorization.
5. VERIFY is implemented in a separate module (`update.py validate`) from the
   proposing logic, and re-runs the compiler's checkers — where full independence is
   required, a second agent (555 lane) re-runs `validate` against the same tree.

## Publish path (governed)

```bash
# after F13 authorization:
bash /root/AAA/scripts/git-lane qwen add registry/ tests/registry_supply_chain/
bash /root/AAA/scripts/git-lane qwen commit -m "registry: <stage> — REPO=AAA"
bash /root/scripts/mirror-cycle.sh /root/aaa-push-mirror /root/AAA https://github.com/ariffazil/AAA.git main
python3 registry/update.py witness
```

The origin re-add invariant inside `mirror-cycle.sh` stays enforced — never bypass it.
