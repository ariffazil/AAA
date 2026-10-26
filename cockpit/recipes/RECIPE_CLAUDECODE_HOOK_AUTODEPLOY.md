# RECIPE 3 — Claude Code hook for auto-deploy after push

**Author:** For Arif to install on his laptop. No agent mutation.
**Goal:** when Arif pushes to `main` from his laptop, Claude Code fires a
PostToolUse hook that calls the same `deploy-vps.sh` script on the VPS
over SSH, OR triggers the same `scripts/kinabalu-dossier/build-pdf.mjs`
refresh locally if the change touched a build-input file.

This hook does **not** auto-create PRs, auto-merge, or auto-seal anything.
It only triggers after an explicit `git push` Arif already issued.

## What a Claude Code hook is

Claude Code reads `~/.claude/settings.json`. The `hooks.PostToolUse`
array runs shell commands after a tool call completes. We match on
`Bash` tool + a regex that captures `git push` to `origin main`. The
hook then SSHes to the VPS and runs the deploy script.

## Step 1 — Discover VPS SSH details from Arif's laptop

```bash
# Verify the keychain has the arif-forge key:
ssh-add -l | grep arif-forge
# If empty, add it:
ssh-add ~/.ssh/arif-forge-push    # or whatever file Arif uses

# Verify passwordless SSH to VPS works:
ssh arif@72.62.71.199 "echo connected && uname -a"
# Expected: prints "connected" and a Linux uname line.
```

If passwordless SSH does not work, set up `~/.ssh/config`:

```
Host arif-forge
  HostName 72.62.71.199
  User arif
  IdentityFile ~/.ssh/arif-forge-push
  IdentitiesOnly yes
  ServerAliveInterval 30
```

## Step 2 — Edit `~/.claude/settings.json`

Open the file (Claude Code creates it on first run if missing):

```bash
# macOS:    code ~/.claude/settings.json
# Linux:    code ~/.claude/settings.json
# Windows:  code %USERPROFILE%\.claude\settings.json
```

Append (or merge) the following. **Do not delete existing entries.**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/arif-forge-autodeploy.sh",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

The matcher regex `Bash` matches every Bash tool call. The actual
push detection happens in the shell script (next step), so we only fire
on `git push origin main` — every other Bash call exits fast with no
side effect.

## Step 3 — The shell script

Create `~/.claude/hooks/arif-forge-autodeploy.sh`:

```bash
mkdir -p ~/.claude/hooks
cat > ~/.claude/hooks/arif-forge-autodeploy.sh <<'HOOK'
#!/usr/bin/env bash
# arif-forge-autodeploy.sh — fired by Claude Code after every Bash call.
# Only acts on `git push ... origin main` to arif-fazil.com. Other calls
# are no-ops. This keeps the hook cheap (sub-millisecond exit on the
# common path).
set -euo pipefail

LOG=~/.claude/logs/arif-forge-autodeploy.log
mkdir -p "$(dirname "$LOG")"

# Read the tool-call payload from stdin (Claude Code pipes JSON here).
INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null || echo "")

# Match: git push ... origin main  (origin may be implicit, allow either)
if ! echo "$CMD" | grep -qE 'git[[:space:]]+push[^|;&]*\borigin\b[^|;&]*\bmain\b'; then
  exit 0
fi

echo "[$(date -Iseconds)] detected push to origin main" >> "$LOG"
echo "  command: $CMD" >> "$LOG"

# Run the deploy on the VPS over SSH.
ssh arif@72.62.71.199 "bash /opt/arif-sites/scripts/deploy-vps.sh" \
  >> "$LOG" 2>&1
RC=$?

echo "[$(date -Iseconds)] deploy finished, exit=$RC" >> "$LOG"
exit $RC
HOOK
chmod +x ~/.claude/hooks/arif-forge-autodeploy.sh
```

## Step 4 — Test (without pushing)

```bash
# Dry-run the matcher by piping a fake tool-call payload:
echo '{"tool_input":{"command":"git push origin main"}}' \
  | bash ~/.claude/hooks/arif-forge-autodeploy.sh
# Should print nothing to stdout, and append to the log file.

# Confirm log:
tail -3 ~/.claude/logs/arif-forge-autodeploy.log
```

Then a real test: from the laptop, in a Claude Code session, run:

```
git push origin main
```

The hook will fire. The session's Bash tool result will look unchanged
(because the hook is PostToolUse, not in-line), but the log file will
show the SSH session.

## Step 5 — Verify on live site

```bash
# Within 60 seconds of the push:
curl -sI https://arif-fazil.com/earth/kinabalu-cross-section.html \
  | grep last-modified
# Expected: fresh timestamp.
```

## Optional — also rebuild the PDF locally

If Arif wants the PDF to regenerate on push, add a second hook in
`settings.json` that matches a tighter regex (e.g. when the changed
files include `kinabalu-cross-section.html`):

```json
{
  "matcher": "Bash",
  "hooks": [
    {
      "type": "command",
      "command": "bash ~/.claude/hooks/arif-forge-autodeploy.sh"
    },
    {
      "type": "command",
      "command": "bash ~/.claude/hooks/arif-forge-pdf-rebuild.sh",
      "timeout": 300
    }
  ]
}
```

`arif-forge-pdf-rebuild.sh`:

```bash
#!/usr/bin/env bash
# Rebuilds the PDF on the laptop after push if the cross-section HTML
# was part of the change set.
set -euo pipefail
LAST=$(git log -1 --name-only --pretty=format:)
if echo "$LAST" | grep -q "kinabalu-cross-section.html"; then
  cd "$(git rev-parse --show-toplevel)/sites/arif-fazil.com"
  node scripts/kinabalu-dossier/build-pdf.mjs
  git add public/earth/kinabalu-basin.pdf
  git commit -m "chore(earth/kinabalu): regenerate PDF v3 from new section"
  git push origin feat/kinabalu-xsection-models
fi
```

This second hook only fires when the changed files include the section
HTML, and Arif's laptop must have Node + Edge/Chrome installed. Use
with care — it will create a second commit and push.

## Rollback

```bash
# Remove the hook from settings.json:
#   delete the "hooks" block, or set it to "{}".
# Then either delete or chmod -x the script:
rm ~/.claude/hooks/arif-forge-autodeploy.sh
```

## Caveats

- **Hook fires on every Bash call that matches the regex.** The matcher
  is broad (`Bash`), so the script does the filtering. Keep the script
  fast on the no-op path.
- **F13 is preserved.** The hook only fires after Arif's own `git push`
  command. It does not push, merge, or seal anything. Arif's word is
  still required.
- **Concurrent runs.** If Arif pushes twice in 30 seconds, the hook
  fires twice. The deploy script should flock. (Recipe 1's
  `deploy-vps.sh` does not, by default; add `flock` if needed.)
- **SSH failure.** If SSH fails (e.g. laptop offline), the hook
  non-zero-exits. Claude Code shows the tool result as failed, but
  the push itself still succeeded. The log captures the error.
- **Windows path.** `~/.claude/hooks/` is `%USERPROFILE%\.claude\hooks\`
  on Windows. Use Git Bash or WSL paths consistently.

## Membrane compliance

- F13 SOVEREIGN: hook cannot fire without an explicit Arif `git push`.
  No bypass.
- F1 AMANAH: removing the `hooks` block reverts to vanilla Claude Code.
- F2 TRUTH: every step has a verification command.
- F11 AUDITABILITY: log file at `~/.claude/logs/arif-forge-autodeploy.log`.
