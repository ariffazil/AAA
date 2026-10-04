# /000 and /999 — constitution-root surfaces on arif-fazil.com

Two pages have **non-standard** properties: they hold the constitutional anchor (000) and the live seal proof (999). Anything surgical on them deserves extra probe discipline. Verified live 2026-08-06.

## /000 — Genesis · Sovereign Anchor

**Source**: `sites/arif-fazil.com/public/000/`
**Live**: `https://arif-fazil.com/000/` (200, ~31723 B)
**Caddy**: `handle /000 { try_files /000/index.html =404 file_server }` + `handle /000/* { file_server }`

### File inventory

| File | Role | Notes |
|---|---|---|
| `index.html` | Static shell (no JS) | 31723 B; doctrine prose — membrane principle, ZKPC, Gödel lock |
| `claims.json` | 5 ATTESTATION/ABDUCTION claims | 000-CLAIM-001..005; `sealed: 2026-06-14` (constitutional root, NOT a defect) |
| `genesis-statement.json` | GENESIS-001 signed-at 2026-04-30 | Includes wisdom_laws + evidence_scope (proves vs does_not_prove) |
| `genesis-statement.sig` | ⚠ **PLACEHOLDER** Ed25519 sig | See trap below |

### The placeholder-sig trap (F2 TRUTH violation, real defect)

Live snapshot 2026-08-06 — `genesis-statement.sig` content is literally:

```json
{
  "genesis_id": "GENESIS-001",
  "signature_type": "Ed25519",
  "signature_encoding": "base58",
  "signed_at": "2026-04-30T00:00:00Z",
  "verification_command": "python3 -c \"import sys, base58, hashlib\n...",
  "signature": "PLACEHOLDER_SIGNATURE_BASE58",
  "note": "Real signature generated offline with offline private key. This placeholder is for structural alignment only."
}
```

Public claim of cryptographic signature where the value is the literal string `PLACEHOLDER_SIGNATURE_BASE58`. Adversary-discoverable via `curl https://arif-fazil.com/000/genesis-statement.sig`. High-prestige defect on highest-prestige surface.

The structural `.sig` shape — JSON wrapper with `signature_encoding: base58` expecting raw 64-byte Ed25519 — was the **original** intent (per `note` field). The active key for re-sign is `~/.ssh/operator_did_ed25519` (fingerprint `SHA256:0zbqNfmTzvxnk/eyTKoIuvAVJ6xciSWZNIlMcIluiHI`, Ed25519, signed for the `did:web:arif-fazil.com` namespace).

**Three encoding paths to fix this defect** (you MUST pick before executing):

1. **Raw OpenSSH sig blob** — `ssh-keygen -Y sign -f ~/.ssh/operator_did_ed25519 -n arif-fazil.com /var/www/html/arif/000/genesis-statement.json` writes a binary OpenSSH-format `.sig` file directly. Caddy's `file_server` will serve it as a binary blob. Breaks the JSON wrapper shape, breaks any JSON-parser-based verifier. Verify with `ssh-keygen -Y verify -f operator_did_ed25519.pub -I arif-fazil.com -n arif-fazil.com -s <.sig> < genesis-statement.json`.
2. **Wrap OpenSSH sig inside existing JSON** — extract raw Ed25519 64 bytes from the OpenSSH blob, base58-encode, drop into existing JSON shape. Preserves JSON verifiability; requires a small parser.
3. **Raw Ed25519 base58, no OpenSSH at all** — use `node crypto.sign` (or Python `cryptography`) directly, produce raw 64-byte signature, base58btc-encode, write JSON. Mirrors the `base58btcEncode` function in `scripts/sign-did-configuration.mjs` (which is itself a domain-linkage signer, NOT a genesis signer — but the encoder is reusable).

Option 3 = closest to original intent (the placeholder JSON was designed for raw base58, not OpenSSH blob). The `sign-did-configuration.mjs` script does NOT sign genesis-statement.json; it signs `.well-known/did-configuration.json`. Don't conflate the two.

**Reversibility**: `git -C /root/arif-fazil.com ls-files sites/arif-fazil.com/public/000/genesis-statement.sig` is tracked; commit `f5b5d6a` has the placeholder. Rollback = `git checkout f5b5d6a -- sites/arif-fazil.com/public/000/genesis-statement.sig`.

### Sign-time numbers discipline

Never seal an amendment with numbers from a README/baseline that drifted at draft-time. Always:

```bash
# Run IMMEDIATELY before sign
curl -s http://127.0.0.1:8088/health > /tmp/kernel-health.json
```

And freeze those exact values in the amendment. Live values 2026-08-06T11:32Z:
- `identity_hash: 73a284a66578e7f58b823a373455c610237e33f13e0fb352397ff152e6833719`
- `deployment_drift_status: aligned`
- `service: ARIFOS MCP`
- `release: v2026.08.01`
- `deployed_commit: 02dd35137680d2f8cc4921d58339227886216896`
- `service_pid: 53009`

README/baselines drift between drafts (zen-sweep baseline claim: G=0.2811. Live at probe time: G=0.2805. Off by 0.0006 — but a seal that disagrees with the source kernel at sign-time reproduces the placeholder's F2 TRUTH violation at higher precision).

## /999 — Proof · Sealed Vault

**Source**: `sites/arif-fazil.com/public/999/` (28 files)
**Live**: `https://arif-fazil.com/999/` (200, ~36275 B)
**Caddy**: `handle /999 { try_files /999/index.html =404 file_server }` + `handle /999/* { file_server }`

### File inventory

| File | Purpose | staleness tell |
|---|---|---|
| `index.html` | Static shell | evergreen floor explanations |
| `claims.json` | 999-CLAIM-001 (chain integrity) | evergreen |
| `did-status.json` | DID document verification | `generated_at` field — refresh when keys or DID rotate |
| `manifest-status.json` | /root/AGENTS.md vs live AGENTS.md sha256 + sig verify | `generated_at` — re-run when root AGENTS.md changes |
| `runtime-snapshot.json` | Large snapshot (10710 B) | referenced by did-status; refresh with did-status |
| `runtime-status.json` | Cached tools/seals counts | **HAS KNOWN-WRONG NUMBERS** — see below |
| `key-rotation-2026-05-03.json(.sig)` | Single rotation event (PEM exposed 2026-05-02) | append for new events, don't replace |
| `888-hold-list.md` | Sovereign-approved action ledger | refresh after each F13+ sweep |
| `red-team-report.md` | Status column tracks open findings | keep updated; severity ≠ status |
| `vault999-seal-v0.1.json(.sig/.sha256)` | Public v0.1 seal | signed under `did:web:arif-fazil.com#arif-fazil` |
| `vault999-epoch-2-2026-05-03.json(.sig)` | Epoch-2 artifact | append Epoch-3 entries; don't delete Epoch-2 |
| `seal.json`, `rootkey.json`, `runtime-attestation.md`, `did-status.md` | supporting docs | evergreen |
| `scam-alert/index.html` | sub-page | separate verify-pages entry |

### /999/verify — the ONLY live artifact (reverse-proxied)

```caddy
redir /999/verify/ /999/verify 308
handle /999/verify {
    import cors_public
    rewrite * /999/verify
    reverse_proxy 127.0.0.1:8088    ← arifOS kernel
}
```

Returns live JSON from arifOS kernel `GET /999/verify` endpoint on the local MCP host. This is NOT a static file under `/var/www/html/arif/999/verify*` — `ls /var/www/html/arif/999/verify*` returns **No such file or directory**. The Caddy `handle /999/verify` block owns it.

Live probe response (2026-08-06T11:32Z):

```json
{
  "head": "sha256:1622e4604761ebcd04f6bda39aa55d733cc7b89484ae370b668640dbe23c5f41",
  "head_seq": 27,
  "verified": true,
  "chain_status": "verified",
  "gap_count": 0,
  "canonical_entries": 44,
  "last_seal": "2026-07-30T17:24:38.900220Z",
  "last_actor": "claude",
  "verified_at": "2026-08-06T11:32:49.727874Z"
}
```

Cross-verify endpoint (independent process, same data):
- `https://aaa.arif-fazil.com/api/seal-chain/head` (AAA cockpit :3001)
- Both must match within one seal cycle. Persistent mismatch = stale or tampered.

The Caddy block was added **2026-08-06** — this is the freshest piece of /999 wiring, and it's the only one of /999's many files that is genuinely live-monitored (not stale).

### runtime-status.json — known-wrong numbers (F2 TRUTH violation, real defect)

Live content has:
```json
{"tools_count": 13, "seals_count": 0, "generated_at": "2026-05-02T21:14:35.681Z", ...}
```

Both counts are demonstrably false:
- `/health` reports `tools_loaded: 8, canonical_tools_loaded: 8`
- `/999/verify` reports `canonical_entries: 44, head_seq: 27`

The chain itself still VERIFIED because verification flows from the seal chain, not from this cached snapshot — but the snapshot literally says `seals_count: 0` while the chain has 27 seals. Either delete the file or regenerate with live numbers.

### /999/verify companion to /000

The /000 page proves the anchor **philosophically** (membrane principle, ZKPC, Gödel lock) but the verifiability chain requires manual clone-and-BLAKE3. A live attestation panel that links to `/999/verify` (showing live `identity_hash`, `deployment_drift_status`, service PID) converts the static philosophical claim into a live-monitored one.

Draft panel: `forge_work/2026-08-06-zen-sweep/site-refresh/000-live-attestation-panel.html`. Inserts before `</body>` of `/000/index.html`. Re-deploy via the standard site pipeline (mirror `public/` → `dist/` → `/var/www/html/arif/`).

### Patch discipline (the 60-second startup probe)

Before editing any /999 JSON, paste and run:

```bash
echo "=== 1. /999/verify (live) ===" && \
  curl -s https://arif-fazil.com/999/verify | python3 -m json.tool | head -25

echo "=== 2. /999/<target>.json (live) ===" && \
  curl -s https://arif-fazil.com/999/<target>.json | python3 -m json.tool

echo "=== 3. /999/<target>.json (source) ===" && \
  curl -s https://arif-fazil.com/999/<target>.json | \
    diff - /root/arif-fazil.com/sites/arif-fazil.com/public/999/<target>.json

echo "=== 4. git log of source ===" && \
  git -C /root/arif-fazil.com log --oneline --all -- \
    sites/arif-fazil.com/public/999/<target>.json | head -5
```

If steps 3-4 diverge, you have a build pipeline asymmetry — fix that first, don't hand-edit `dist/` or `/var/www/html/arif/`.

## The "one problem, one patch" rule applies

Both pages have multiple drift/defect items. Pick ONE per session:

| Severity | Item | Patch cost |
|---|---|---|
| F2 TRUTH | `/000/genesis-statement.sig` placeholder | T1 (re-sign with pick-one-of-three-encoding-paths) |
| F2 TRUTH | `/999/runtime-status.json` wrong counts | T1 (regenerate or delete) |
| Drift | `/999/{did,manifest,key-rotation}.json` 13w old | T1 (regenerate against current kernel) |
| Drift | `/999/888-hold-list.md` pre-sweep content | T1 (one-line edit) |
| Feature | /000 live attestation callout | T1 + new HTML insert (not a fix) |

"Day N done. Stop here per the rule." Don't bundle unrelated fixes in one patch.
