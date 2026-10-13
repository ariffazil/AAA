# Voice Alias Federation Plumbing — operational quirks

## KVM4 voice_alias.sh depends on env being pre-sourced

`/root/.openclaw/workspace/scripts/voice_alias.sh` declares
`: "${MINIMAX_API_KEY:?MINIMAX_API_KEY not set}"`. The guard means the
script fails fast when the variable is empty — but it does NOT auto-source
it from `/root/.secrets/`. The script is a TRIO dispatcher (ss/sado/pmx)
intended to be called from a shell where the secret has already been loaded.

Wrong way (will fail with `MINIMAX_API_KEY: MINIMAX_API_KEY not set`):

```bash
ssh kvm4 "bash /root/.openclaw/workspace/scripts/voice_alias.sh siti \"$(cat text)\" out.mp3"
```

Right way:

```bash
ssh kvm4 'bash -lc "set -a; source /root/.secrets/kunci-mas.flat.env 2>/dev/null; \
  source /root/.secrets/kunci-root.env 2>/dev/null; set +a; \
  bash /root/.openclaw/workspace/scripts/voice_alias.sh siti \"\$(cat /tmp/text)\" /tmp/out.mp3"'
```

The `bash -lc` matters: it spawns a login shell so `~/.bash_profile` /
`/etc/profile.d/*.sh` fire and any source order is honoured. Without
`-l`, secrets that live in `~/.bashrc` only are missed.

## KVM8 / KVM4 canonical split

KVM4 (OpenClaw, hostname `kvm4-forge`, 100.64.0.5) owns the canonical
SS voice card (`/root/.openclaw/workspace/voice/SS/SS-VOICE-CANONICAL-FEDERATION.json`).
KVM8 (Hermes, hostname `af-forge`, 100.64.0.2) holds a mirror at
`/root/.hermes/voice/SS-VOICE-CANONICAL.json` and is the one resolver
`voice_alias.sh` looks at for seat-token plans.

A request "render SS" from KVM8 should NOT re-clone — it should SSH to
KVM4 and call the canonical resolver. Mirror drift is the failure class.
If you find yourself editing the KVM8 mirror, the fix belongs in KVM4.

## Federation voice_id status file

`/var/lib/arifos/voice_revocations.jsonl` is the append-only revocation
receipt. One JSON line per revoked voice_id, with `ts`, `actor`,
`directive`, `voices[]` (each with `id`/`provider_voice_id`/`reason`),
`registry_path`, and `canonical_card`. Always populate it when flipping a
voice to REVOKED in `/root/AAA/audio/voice-registry.json` so downstream
audits can answer "when was X taken out of service and on whose order".

## Fail-closed behaviour to rely on

`/root/AAA/engines/iarif_tts_pipeline.sh` resolves voice aliases via the
registry and aborts when the resolved id is REVOKED or unknown — no silent
swap to Edge / Piper / MiMo. That is the load-bearing property of the
revocation protocol: dropping aliases without flipping status will not
be enough to stop a render; flipping status without dropping aliases is
also fine because the registry resolution returns REVOKED → exit 1.

Pattern is: keep the alias in place (so pipeline can show the right
error name), flip status to REVOKED. Do not delete alias keys.