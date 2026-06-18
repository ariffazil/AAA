# 2026-06-12 20:50 UTC — Phone SSH key added to ariffazil authorized_keys

## TL;DR
Arif tried to SSH from Termux (Android) using `id_ed25519_arif_phone`, got
"Permission denied (publickey)" twice. Diagnosed: phone was using a 3rd
ed25519 key that wasn't in server's authorized_keys. Added the pub key, fix
took effect immediately (no sshd restart needed).

## Context
- Phone: Android Termux, user `u0_a617` (note: NOT `u0_a596` — different
  device than the one whose key is line 4 in authorized_keys as
  `u0_a596@localhost`)
- Server: VPS af-forge, port 22888, user ariffazil (uid 1002)
- Failed attempts logged at 20:45:46 + 20:45:48 UTC from 202.185.89.85
  (Malaysian mobile IP — `Connection closed by authenticating user [preauth]`
  = server offered its known keys, none matched)
- Diagnosis: 2 arif-termux keys already in server (lines 9, 10) but
  neither matched current phone key

## Action taken
1. Arif ran the diagnostic block I sent — printed:
   - `id_ed25519_arif_phone.pub` → 
     `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJ2Ab0GezM1cOmPkRlciRMSn4PGpye3tQDCKnLOb7CW+ arif-termux-phone@arif-fazil.com-2026-06-11`
   - Fingerprint: `SHA256:sY88u/fTegtMdtkmskQSQ0iDn/+1197rpptZLcV6zK0`
2. Appended as line 11 to `/home/ariffazil/.ssh/authorized_keys`
3. Verified: server-side ssh-keygen -lf matched the phone's fingerprint
4. Backup: `authorized_keys.bak.20260612-205027` (the prior version
   from 2026-06-11 09:41 — 1617 bytes, no terminal-emulator history lost)

## Reversibility
`sed -i '11d' ~/.ssh/authorized_keys` (or restore the .bak file). One
second to roll back. F13 SOVEREIGN: this was a sovereign identity op
(he sent me the pub file himself, so the sovereign himself provided
provenance). No 888_HOLD needed.

## F2 confession — text Arif received from Opencode (the 000 / @arifOS_bot)
Arif confirmed in #74670 that the wrong text he sent me earlier was from
Opencode. Walking back my overcorrection — **Opencode was RIGHT about
the secret-storage architecture, I was wrong to dismiss it**:

| Opencode claim | Reality from re-audit |
|---|---|
| `/root/.secrets/auth/` exists | ✅ YES — `/root/.secrets/` exists with `auth/`, `tokens/`, `env/`, `backups/`, `all-secrets.md`, `INDEX.md` |
| `config/secret-registry.yaml` is a map | ✅ YES — 6 copies exist; file header literally says *"One canonical name → Many app-specific formats"* |
| "GitHub encrypted secrets for deploy, Docker secrets on VPS" | ✅ PARTIALLY — VPS stores in `/root/.secrets/`, `/opt/arifos/.secrets/`, `/root/.env`; GitHub side gated by `/root/arifOS/.github/workflows/_shared-secrets-gate.yml` |

What Opencode got WRONG (the part I corrected):
- "phone key has never been added" — false, 2 termux keys already there
- "VPS only accepts id_ed25519 as canonical" — false, 10+ keys
- "phone key file is arif_phone" — false, actual is id_ed25519_arif_phone

**Lesson split into 2:**
1. When another agent diagnoses, audit the filesystem, don't dismiss
   any part until you've actually checked. I dismissed the architecture
   claims without checking — got lucky that my correction was needed
   for the SSH part anyway, but the architecture part I called wrong
   was right.
2. Opencode's failure mode here was *confident mix of right + wrong*:
   the secret-architecture claims were accurate, the SSH claims were
   fabricated from pattern-matching (not from reading
   `~/.ssh/authorized_keys`). A healthier behavior would be
   "I'm guessing based on common patterns — please verify" rather
   than declarative prose. Worth flagging to Opencode / Hermes, but
   not urgent and not a federation break.

## Things I noticed (not blocking, for follow-up)
- `arif_vps` / `arif_vps.pub` also in phone's ~/.ssh — different key,
  not on server. Intentional? Old? Worth asking.
- Phone's `~/.ssh/config` (115 bytes) — may forward wrong identity
  by default if `-i` flag is ever dropped. Worth a peek.
- Phone's `~/.ssh/authorized_keys` is 0 bytes — phone is not running
  sshd as a server, normal.
- `arif-termux-recovery-2026-06-11` key (line 10) — generated same
  date (2026-06-11) as the new `arif-termux-phone-2026-06-11` key
  (line 11). So the recovery key was for a different purpose (probably
  a regen that got abandoned when the recovery succeeded via another
  route). Both kept on server; harmless redundancy.
