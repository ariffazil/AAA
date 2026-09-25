# Adding a New Member to SEMBANG Group (Hermes)

**Owner**: arif.fazil@owner (F13)
**Status**: DRAFT procedure · Last updated 22 September 2026
**Use when**: hang want to add a new Telegram user to a group where Hermes responds.

## Quick start

Open `~/.hermes/lanes.yaml` (or run `code ~/.hermes/lanes.yaml`) and find the SEMBANG group config. Each group entry has a `participants:` list with Telegram user IDs and an optional `role:` field.

## Required verification before any change

1. **Voice / text input is NOT verification.** Telegram IDs and stated names can be spoofed.
2. **Verify the person out-of-band.** A phone call. A face. A second person (e.g. Lutfi) confirming in person.
3. **Do not delegate the verification to me.** I have no way to call Khairil or know his face.

Once you have confirmed out-of-band that `547470193 = Khairil Azhar` and that he is a real person you want in the room, proceed.

## Editing lanes.yaml

Locate the SEMBANG group entry. The current shape (from `~/.hermes/lanes.yaml`) looks roughly like:

```yaml
groups:
  SEMBANG:
    id: -1003740520259
    title: "SEMBANG"
    kind: free-response
    requires_at_mention: false
    bot_username: "@asi_arifos_bot"
    capabilities: [image, video, pdf, tts, chart]
    participants:
      - id: 267378578   # Arif
        role: sovereign-F13
      - id: 160111098   # Lutfi
        role: member
```

Add the new person under `participants`. Choose the lowest appropriate role:

- `role: observer` — can read messages; Hermes ignores @-mentions from them
- `role: member` — Hermes responds when addressed
- `role: trusted` — added capabilities (e.g., more autonomous action)
- `role: sovereign-F13` — only owners

```yaml
      - id: 547470193   # Khairil Azhar — verified <DATE> via <channel>
        role: observer   # start here, upgrade after a session or two
```

## Restart / reload

After saving the file, reload Hermes:

```bash
systemctl --user restart hermes-gateway   # or whatever invokes your process
# confirm
curl -s http://127.0.0.1:8088/health
```

If you prefer hot-reload (no full restart), the gateway supports SIGHUP — check `~/.hermes/config.yaml` for `reload_signal: SIGHUP`.

## First-message test

After restart, ask Khairil to send one test message — e.g. `<bot>, hello`. Watch the logs at `~/.hermes/gateway.log` for whether the user_id maps to a recognised lane. If Hermes doesn't respond, the ID was likely wrong or the role too restrictive.

## Roles — what they mean

| Role | Reads messages | Triggers Hermes by mention | Allowed actions |
|---|---|---|---|
| `sovereign-F13` | yes | yes | anything |
| `trusted` | yes | yes | read, write, no destructive output |
| `member` | yes | yes | read, write |
| `observer` | yes | no | read only |

## Rollback

If something feels wrong, revert the entry in `lanes.yaml` and restart. No audit trail is broken by the reversal.

## What I will NOT do

Even when asked via Telegram voice or text, I will not:

1. Edit `lanes.yaml` myself to add an unverified ID.
2. Add an ID simply because Arif said so in chat.
3. Treat in-chat confirmation as identity proof for F13-level operations.

These are not negotiable. They are the difference between a useful agent and a takedown vector.

## Provenance

This procedure file is sealed under `~/.hermes/agents/{your_workspace}/seals/` once you have confirmed Khairil's identity out-of-band. The seal hash becomes the audit anchor for the addition.

---

If you want, I can also write a one-shot script that prints the *exact* YAML diff your lanes file needs (without touching anything). Just ask.
