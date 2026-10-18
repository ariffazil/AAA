# SCAR-2026-10-18-007 — Git Lane Identity Binding & AGY Harness Discipline

**Filed:** 2026-10-18 by AGY CLI (FI-004)
**Weight:** w_scar = 0.8
**Class:** CONCURRENT_WRITER_COLLISION + CRYPTOGRAPHIC_ATTRIBUTION
**Related Commits:** A-FORGE `a8967d54`, arifOS `675b1bf49`

## What happened

Multiple autonomous coding agents (Claude, AGY, Kimi, Qwen, OpenClaw) operating in shared working trees (`/root/arifOS` and `/root/A-FORGE`) repeatedly collided on repository author attribution. Agents rewrote `git config user.name` and `user.email` locally to make commits, overwriting each other's configuration mid-flight.

During an active session, AGY rewrote `arifOS` `user.name` to `antigravity (agy/FI-004)` while Claude Code was concurrently building a lane identity enforcement gate.

Furthermore, empirical testing showed that git's `%GS` format token does not report the committer email typed into the commit object, but rather the principal registered to the signing key in `allowed_signers`. Committer email is a claim; `%GS` is the cryptographic attribution.

## The Fix Landed (F13 Lane Gate)

1. **Per-Lane Key Architecture:**
   - 8 dedicated ed25519 signing keys created in `/root/.ssh/git-signing/` (0600 mode).
   - Identity allowlist registered in `/root/.config/git/lane-identities.tsv`:
     `forge`, `kimi`, `openclaw`, `qwen`, `hermes`, `claude`, `333-agi`, and `agy` (FI-004).
   - `/root/.ssh/allowed_signers` populated with all 8 lane principals.

2. **LANE GATE in Pre-Commit Hook:**
   - `/root/A-FORGE/hooks/pre-commit-lsp-gate.sh` (symlinked by both repos) enforces that any commit must carry a registered (name, email, signing-key fingerprint) triple.
   - The gate forbids any disagreement between claimed email and signing key principal.

3. **Fail-Closed Repository Configuration:**
   - In both `/root/arifOS/.git/config` and `/root/A-FORGE/.git/config`, `user.name=""` and `user.signingkey=""` are set to empty.
   - Any bare `git commit` invocation fails closed immediately.

4. **Durable Rollback Storage:**
   - The 6 pre-lane-keys backup files in `/tmp` were moved to durable storage at `/root/backups/git-lane-pre-rollbacks-20261018/` to survive host reboots.

## Binding Rule (LAW 8 / SCAR-AGY-008)

- **NEVER** run `git config user.name` or `git config user.signingkey` in any repository working tree.
- **ALWAYS** invoke git via the lane wrapper:
  ```bash
  /root/scripts/git-lane <lane> commit ...
  /root/scripts/git-lane agy commit -m "..."
  ```
- Every agent must commit under its own authentic lane identity with verifiable cryptographic signature.
