# A-FORGE /health GAP REPORT — 2026-09-21

> **Audit target:** A-FORGE /health surface
> **Probe timestamp:** 2026-09-21T02:24 UTC
> **Auditor:** FI-008 (Kimi Code)

## Identity field coverage (5 organs, 17 required fields)

| organ | fields_present | missing |
|---|---|---|
| **arifOS** | 12/17 | wheel_hash, started_at |
| **A-FORGE** | 3/17 | build_commit, surface_hash, wheel_hash, runtime_path, runtime_import_path, service_started_at, deployed_commit, git_branch, drift, runtime_matches_build, deployment_drift_status, git_commit, source_commit |
| **GEOX** | 1/17 | source_commit, build_commit, deployed_commit, surface_hash, wheel_hash, runtime_path, runtime_import_path, service_started_at, git_branch, drift, runtime_matches_build, deployment_drift_status, git_commit, runtime_matches_build |
| **WEALTH** | 1/17 | (same shape as GEOX) |
| **WELL** | 4/17 | build_commit, surface_hash, wheel_hash, runtime_path, runtime_import_path, service_started_at, source_commit(?), git_branch(?), drift(?), runtime_matches_build(?), deployment_drift_status(?), git_commit(?), deployed_commit(?) |

## A-FORGE specifically (3/17)

**Present (3):**
- identity_hash
- service
- version

**Missing (14) — in priority order for closing G0c:**

| field | severity | impact |
|---|---|---|
| `build_commit` | HIGH | A-FORGE runtime_verify strict returns UNKNOWN on source_vs_wheel |
| `surface_hash` | HIGH | federation_root collapses on null for A-FORGE |
| `runtime_path` | HIGH | cannot bind identity_hash tuple fully |
| `service_started_at` | HIGH | identity_hash temporal component missing |
| `deployed_commit` | MEDIUM | cross-verification against `git_commit` impossible |
| `git_commit` | MEDIUM | source-tree vs deployed-tree comparison impossible |
| `source_commit` | MEDIUM | federation_root can't include A-FORGE properly |
| `wheel_hash` | MEDIUM | source_vs_wheel byte-equality impossible |
| `runtime_import_path` | LOW | (alt to runtime_path; one or both fine) |
| `git_branch` | LOW | release identity can't include branch |
| `drift` | LOW | runtime health self-reported status |
| `runtime_matches_build` | LOW | self-reported integrity |
| `deployment_drift_status` | LOW | self-reported integrity |

## Closing-the-gap recipe (cross-organ)

**Each organ's /health should emit the canonical identity tuple:**

```json
{
  "identity": {
    "source_commit":     "<git HEAD full SHA>",
    "build_commit":      "<deployed build SHA>",
    "deployed_commit":   "<running artifact SHA>",
    "git_branch":        "<source branch>",
    "drift":             false,
    "runtime_matches_build": true,
    "surface_hash":      "sha256:...",
    "wheel_hash":        "sha256:...",
    "runtime_path":      "/abs/path/to/entry.py",
    "service_started_at": "<ISO8601 UTC>"
  },
  "identity_hash": "sha256:<derived from above>"
}
```

The `identity` block is the minimum A-FORGE and GEOX and WEALTH and WELL must surface. arifOS already has this shape — it can be the template.

## Why this matters for G0c close

The federation_root in `/etc/arifos/canon/federation-release.json` hashes `(runtime_commit, surface_hash, runtime_path, started_at)` per organ. Today:

- arifOS contributes 4/4 tuple components
- A-FORGE contributes 1/4 (only `runtime_commit`)
- GEOX contributes 0/4 (uses different identifier system)
- WEALTH contributes 1/4 (only `runtime_commit`)
- WELL contributes 1/4 (only `runtime_commit`)

The Merkle root is therefore mostly commit-string. **Closing the gaps makes the federation_root actually cryptographic, not just a hash of commits.**

## Next steps

- T2: A-FORGE /health shape update (code edit, requires `aforge.service` restart)
- T2: same for GEOX, WEALTH, WELL
- All are F13 binaries because they touch organ code paths AND require service restart
- Per AGENTS-AUTONOMY.md §7, the named services `aforge.service`, `geox-mcp.service`, `wealth-organ.service`, `well.service` are known-safe for restart, but the /health surface changes themselves are T3 because they are organ code mutations.

**This report goes to the A-FORGE lane for triage.**
