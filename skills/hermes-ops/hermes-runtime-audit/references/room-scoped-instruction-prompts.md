# Room-scoped instruction prompts — `telegram.extra.channel_prompts`

Per-chat instruction text in the profile's `config.yaml`, injected when a message arrives from that
chat id. This is the surface that actually carries room-specific rules to the model, independent of any
lane/persona plugin — write the hard limits here when you need them in force in one room, rather than
waiting on a layer that may not be loaded.

## Set one

```bash
hermes config set telegram.extra.channel_prompts.<chat_id> "<instruction text>" --force
```

- `<chat_id>` is the platform's numeric id; negative for Telegram groups. Quote the value.
- `hermes config set` writes the dotted path into the **active** config and echoes the accepted value,
  so it works from inside a running gateway session where a direct file write may be guarded.
- `--force` suppresses the unknown-key notice only; the value is written either way.
- Hand-editing the yaml also works where no writer guard applies. Do not fight a guard — use the CLI.

## What already exists is the template

```bash
hermes config get telegram.extra.channel_prompts
```

Most rooms have **no** entry. Check before assuming a rule is in force anywhere — a chat with no prompt
has no room-level limits at all, whatever the doctrine says.

## Verify the write parsed

A malformed edit can leave the whole map unreadable, which fails quieter than a missing key.

```bash
python3 -c "import yaml;d=yaml.safe_load(open('<profile>/config.yaml'));\
cp=d['telegram']['extra']['channel_prompts'];print(list(cp));print(len(cp['<chat_id>']),'chars')"
```

## Activation

The gateway reads config at **startup**, so a new prompt is inert until the gateway restarts. State that
plainly; do not report the rule as live on the strength of the file. Restarting the gateway from inside a
gateway session kills the session that issued the command — schedule it, or let the principal trigger it.

## What belongs in one

- **HARD LIMITS first** — what must never be surfaced in this room. Room-level leakage is the thing a
  per-room prompt uniquely prevents, so write the prohibitions before the pleasantries.
- Then **register/voice** for the room and **SCOPE** (what to answer there).
- Give each prohibition a mechanism clause, not a bare verb: "never emit a directive about a member's
  body — if the principal wants it said, he says it in his own voice" beats "be careful with health talk".
- Keep it imperative and short; it is injected on every turn of that room.

## What does not belong

- Private-lane facts about named people — a shared room must never carry them.
- Scores, rankings or sentiment about members.
- A directive about a member's body, or a computed schedule aimed at them.
- System/organ/tool vocabulary. The text shapes conduct in a human room; its effect is what the humans in
  the room will experience.
