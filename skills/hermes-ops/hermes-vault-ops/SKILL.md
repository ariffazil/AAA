---
name: hermes-vault-ops
description: "Use when adding or listing Hermes vault logins."
version: 1.0.0
floors: [F1]
tags: [vault, password, autofill, login, credential, browser]
triggers:
  - "add a login to the vault"
  - "hermes vault add"
  - "save this password"
  - "browser autofill login"
  - "vault EOFError / EOF when reading a line"
capability_tier: fed-long-context
ecology_state: WARM
---

# Hermes Vault CLI

The encrypted vault backs the browser autofill tools (`browser_vault_list` / `browser_vault_fill` /
`browser_vault_save_login` / `browser_vault_enter_code`). The agent sees handles and identifiers but
never a password — the password is encrypted at rest and filled server-side.

## The one rule that bites first

`hermes vault add` is an **interactive tty wizard**, and the password is read via `getpass` —
**never from argv, never from a stdin pipe.** Piping `printf 'label\norigin\n' | hermes vault add`
feeds two lines into a six-prompt wizard and dies with `EOFError: EOF when reading a line` on the
third prompt; and the password could not come through the pipe anyway, because `getpass` reads the
terminal directly so the secret never lands in shell history or the process list.

Do not fight the wizard. For one-shot non-interactive adds, use the argv helper:

```bash
bash /root/scripts/vault-add-login.sh "<label>" "<origin-url>" "<identifier>" [identifier_type]
# prompts ONLY the password (hidden) and optional authenticator key
```

## Add a login — the two shapes

**Interactive (fine for a human at a tty):**

```bash
hermes vault add --kind login
# 1 Label           e.g. Google Arif
# 2 Site origin     e.g. https://accounts.google.com   (a URL, NOT the email)
# 3 Identifier type [Enter] = email
# 4 Email/phone     the login identifier
# 5 Password        hidden
# 6 Authenticator   [Enter] to skip 2FA
```

**Non-interactive (one-shot):**

```bash
bash /root/scripts/vault-add-login.sh "Google Arif" "https://accounts.google.com" "user@example.com"
```

## Pitfalls

- **Origin ≠ identifier.** The `Site origin` prompt wants the URL the item autofills on
  (`https://accounts.google.com`), not the login email. Putting the email as origin is the classic
  mix-up — the email belongs in the identifier prompt (step 4).
- **`--kind login` is the only kind that needs an identifier type.** Payment and address kinds read
  field values (card/address) via their own prompts; login is the one with the email/phone/username
  selector.
- **Password can never be piped.** Any attempt to script the password via stdin will hang or EOF on
  `getpass`. The argv helper keeps password out of argv too — it prompts via `getpass` and only
  metadata (label/origin/identifier) rides argv, which is visible but non-secret.
- **`hermes vault list` shows metadata only** — handle, source, kind, label, identifier, origin.
  Passwords are never printed. Use the handle from `list` to `hermes vault rm <handle>`.

## Browser autofill flow (how the vault actually gets used)

1. `browser_vault_list` — find the saved item (or `locked` managers that need unlock).
2. Type the identifier yourself into the login form via the browser input tool.
3. `browser_vault_fill` with the handle — fills the password server-side, never into chat.
4. `browser_vault_enter_code` for a 2FA/OTP prompt (generates from a saved authenticator key, or
   asks the user in their UI).

The helper script lives at `/root/scripts/vault-add-login.sh` (imports `agent.vault_store` from the
hermes-agent install venv; the `get_vault_store().add_item(kind, label, secret, origin)` call is the
programmatic path when the wizard is the wrong instrument).
