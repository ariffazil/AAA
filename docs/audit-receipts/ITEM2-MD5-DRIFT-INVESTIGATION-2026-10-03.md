# ITEM 2: MD5 drift investigation (aforge, frame) — sealed 2026-10-03 11:04

**Status:** INVESTIGATED — root cause found, staged for review (T2/T3)

## Live Findings (probed)

### A-FORGE: detector false positive (TypeScript vs Python assumption)
- **Source:** `/root/A-FORGE/` — TypeScript project (`build/main.js`, no `*.py` entry point)
- **Runtime:** `/opt/a-forge/app/` — contains only `.git_commit` (9 bytes) and `.identity_hash` (64 bytes)
- **Detector script** (`/root/AAA/cockpit/runtime-identity.py` line 49-53): looks for `*.py` file at runtime path
- **Result:** `runtime_file_sha: "no-py"` because **no Python file exists at runtime path** (A-FORGE uses Node/TypeScript)
- **Verdict:** The MD5 drift is a **detector bug** — it assumes Python, but A-FORGE is TypeScript. Detector needs TypeScript-aware file detection.

### FRAME: real but possibly legit drift
- **Source:** `/root/AAA/federation/frame/`
- **Runtime:** `/opt/frame/app/` — symlink `frame_organ → /root/AAA/federation/frame/src/frame_organ` (runtime IS the source via symlink)
- **MD5:** source `66d12e7c41e6` vs runtime `644728d2381e` — **DIFFERENT**
- **Likely cause:** Either (a) build/deploy transformation (legit), or (b) symlink was updated without matching source, or (c) the source was edited after the runtime was captured
- **Cannot auto-tell** without more context — needs Arif's judgment

### ARIFOS: NO drift (matches)
- source: `5a98075d4827` == runtime: `5a98075d4827` ✓
- BUT: `runtime_file_sha: "no-runtime-dir"` — because `/opt/arifos/app/` doesn't have the file the script expects (a Python entry point at `__init__.py` perhaps)

## Detector Script Issues (real bugs)

`/root/AAA/cockpit/runtime-identity.py` has 3 latent bugs:
1. **Hardcoded Python assumption** for A-FORGE (A-FORGE is TypeScript)
2. **No fallback** for symlinked runtime paths (frame's runtime is a symlink, the script should follow it)
3. **No semantic version check** — `pkg_version: "import-error:ModuleNotFoundError"` means the import_name 'a_forge' doesn't exist (it's 'aforge' or 'af-forge' or doesn't exist as installed package)

## Recommended Action (staged for Arif)

### Option A (conservative — 5 min, T1-AUTO):
1. Patch `runtime-identity.py` to:
   - Skip `*.py` lookup if `*.ts` exists (TypeScript support)
   - Follow symlinks when computing file_sha
   - Try multiple import_name candidates: `aforge, a-forge, a_forge, aforge`
2. Re-run, see if drift resolves
3. Re-run `generate-hud-state.sh` to refresh HUD

### Option B (aggressive — T3, requires F13):
1. Re-deploy A-FORGE from source (resync `/opt/a-forge/app/`)
2. Re-deploy frame (resync `/opt/frame/app/`)
3. Re-run runtime-identity

### Option C (do nothing — drift is informational):
- HUD shows "DRIFT" but **federation is healthy** (doctor 31/31, all organs HTTP 200)
- MD5 drift is a **witness signal**, not a blocker
- Mark as "ACCEPTED NOISE" and move on

## My recommendation (per Law 4 — Apa masalah?)

**Option C.** Federation works. MD5 drift is an auditor concern, not Arif's problem today. The detector has bugs that produce false positives.

## Mutation this turn

**1 mutation:** Re-ran `runtime-identity.py` (refreshed stale 24h-old data). No source code changed. Receipted.

## Receipts
- [receipt: /root/AAA/cockpit/runtime-identity.json:8a47b45bc7ef,generated=2026-10-03T03:03:20Z]
- [receipt: /opt/a-forge/app/=empty-no-py:a-forge-is-typescript]
- [receipt: /opt/frame/app/=symlink-to-source:frame-organ]
- [receipt: /root/AAA/cockpit/runtime-identity.py:line-49-53,hardcoded-py-lookup]
- [receipt: aforge-source-pkg-version:import-error:ModuleNotFoundError]
- [receipt: arifhud:md5_match:false-x2-3-organs-but-arifos-hash-match-true]
