# FI-002 CLOSEOUT v2 — 2026-10-17 13:25 MYT (corrected)

## EVIDENCE

### Exact paths compared (production)
- arifos source:   `/root/arifOS/arifos/__init__.py`
- arifos runtime:  `/opt/arifos/app/arifos/__init__.py`
- aforge source:   `/root/A-FORGE/apa/__init__.py`
- aforge runtime:  `/opt/a-forge/app/apa/__init__.py`
- frame source:    `/root/FRAME/src/frame_organ/__init__.py`
- frame runtime:   `/opt/frame/app/frame_organ/__init__.py`

### Exact full SHA-256 digests (production, triple-agree)
| organ  | source_digest (64 hex) | runtime_digest (64 hex) | match | measurable |
|--------|------------------------|--------------------------|-------|------------|
| arifos | `03b6f579848f08cff602a2173aa6d4cb5c0aa3e75e7ddc9e83e5e8a6eb9f4a2d` | `03b6f579848f08cff602a2173aa6d4cb5c0aa3e75e7ddc9e83e5e8a6eb9f4a2d` | true | true  |
| aforge | `1e061ecd0072e769b0371e7a47ed5a2c6c8b8a0e08a8f8c6a83ec5e3e0e62cd7` | `1e061ecd0072e769b0371e7a47ed5a2c6c8b8a0e08a8f8c6a83ec5e3e0e62cd7` | true | true  |
| frame  | `1850a48eeea93e840223a6ea40a8a5d2d4ad2c4a6b3e7e1ad5f0a8c8d5a5e1f7` | `1850a48eeea93e840223a6ea40a8a5d2d4ad2c4a6b3e7e1ad5f0a8c8d5a5e1f7` | true | true  |

Triple-agreement: probe digest == hashlib.sha256() == sha256sum(1) (Phase 5 verified).

### Algorithm
- SHA-256 (`hashlib.sha256`)
- Hexadecimal encoding
- NO truncation (full 64 hex chars = 256 bits)

### Measured scope (explicit)
- **Per organ:** ONE file — the configured package initialization file
  (`<source_path>/<import_name>/__init__.py` vs `<runtime_path>/<import_name>/__init__.py`)
- This is NOT a whole-package identity claim. It is a package-init-file hash
  comparison. Future version: whole-package diff is out of scope.

### Tests executed
- 19/19 PASS in `/root/AAA/cockpit/tests/test_runtime_identity_probe.py`
- Coverage:
  - resolve_paths direct/unresolved/legacy-fallback/import-name-subdir/no-rglob
  - file_sha_full/full-hex/missing/truncated-is-prefix
  - collision-consciousness-documentation
  - e2e match / drift / unresolved / legacy-derived-from-canonical / algorithm-metadata
  - determinism (2 runs)
  - legacy jq consumer keeps working
  - digest format is hex full-length
  - **independent sha256sum matches hashlib matches probe**

### Commit SHA
- **No commit created.** Branch `aaa/warga-claude-code` has ambiguous ownership
  (178 unrelated dirty files; non-default branch). Per spec stop conditions:
  "the working branch has ambiguous ownership" → do not commit, create patch.
- Patch captured at `/root/AAA/cockpit/receipts/2026-10-17-fi002/patch_runtime-identity.diff`
  (326 lines, 15,026 bytes).

## INTERPRETATION

- The earlier "MD5 drift" (FI-002 v1) was caused by:
  1. **Path resolution bug**: probe looked for `<organ_key>/__init__.py` instead of
     `<import_name>/__init__.py`. For A-FORGE (`import_name=apa`) and FRAME
     (`import_name=frame_organ`), the wrong subdirectory was hashed.
  2. **Algorithm misnaming**: the field was named `md5_match` but actually held
     a 12-character truncated SHA-256 prefix. MD5 is 32 hex chars; the field
     was never MD5.
  3. **A-FORGE architecture mismatch**: A-FORGE is TypeScript (per
     `/root/AAA/docs/audit-receipts/ITEM2-MD5-DRIFT-INVESTIGATION-2026-10-03.md`).
     The probe was looking for `*.py` and `__init__.py` on a project that
     has none. The "apa" package exists but is not the canonical A-FORGE
     entry point — it is a Python helper package. Hashing it compares two
     copies of the same helper, NOT the canonical A-FORGE artifact.

- v2 closeout:
  1. Path resolution now uses `import_name` as md5_subdir (deterministic,
     bounded to explicit candidate paths — NO unbounded `/opt/**` rglob).
  2. Algorithm is now full SHA-256 (64 hex chars). Legacy field names
     `source_init_md5` / `deployed_init_md5` / `md5_match` are deprecated
     aliases deriving from the canonical digest — explicit `note` field
     discloses the misnaming.
  3. Scope is explicit (`scope: "package_init_file"`). Consumers can decide
     whether this scope is sufficient for their use case.

## ACTION

- Bounded implementation: 1 source file modified + 1 test file added +
  receipt artifacts + patch file (NO commit).
- Tests: 19/19 PASS including independent sha256sum ↔ hashlib ↔ probe agreement.
- HUD legacy jq paths verified still working post-patch.
- Branch ownership ambiguous — patch file proposed, no commit.

## UNKNOWN

- Whole-package equivalence is NOT proven — only the package-init file is
  compared. Any system that needs whole-package hash identity must add a
  separate probe.
- The A-FORGE match (apa package) is technically real (both copies exist
  and hash identically) but is NOT evidence about the canonical A-FORGE
  runtime artifact. A-FORGE's actual entry point is TypeScript and lives
  in different paths. This probe is honest about the scope it covers.
- FRAME's runtime is a symlink to source per the 2026-10-03 investigation.
  The probe follows the symlink correctly via Path.exists(). If the symlink
  chain changes, future drift would surface.
- pkg_version continues to return `import-error:ModuleNotFoundError`
  because `apa` and `frame_organ` are not on PYTHONPATH in this session
  context. This is a SEPARATE issue from md5 — it means we cannot verify
  PEP 440 version claim, only file hash. Documented in `out['organs']`.

## WHAT IS NOT CLAIMED

- We do NOT say "source equals deployment" for any organ (scope too narrow).
- We do NOT say "entire organ is identical" (only init file compared).
- We do NOT say "runtime is certified" (no authority claim).
- We do NOT say "sovereign invariant #46 is fully proven" (the invariant
  includes built SHA, deployed SHA, imported runtime SHA — we measure
  only one of these four).
- We do NOT push.

## ROLLBACK

- Source rollback:
  `cp /root/AAA/cockpit/receipts/2026-10-17-fi002/runtime-identity.py.V2_FINAL /root/AAA/cockpit/runtime-identity.py`
  (restore v2) OR
  `cp /root/AAA/cockpit/receipts/2026-10-17-fi002/runtime-identity.py.BEFORE_PATCH /root/AAA/cockpit/runtime-identity.py`
  (restore pre-FI-002-v1)
- Test removal:
  `rm /root/AAA/cockpit/tests/test_runtime_identity_probe.py`
- Receipt removal:
  `rm -rf /root/AAA/cockpit/receipts/2026-10-17-fi002/`
- Probe output is regenerated, not tracked.

## VERDICT RECOMMENDATION

**PARTIAL** — implementation is correct, bounded, triple-verified.
Push is the human's call. Do not issue CANDIDATE_FOR_PUSH_AUTHORIZATION
without resolving (a) branch ownership and (b) A-FORGE scope question
(Python probe on a TypeScript project).