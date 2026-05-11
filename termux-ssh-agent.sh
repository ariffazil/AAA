#!/data/data/com.termux/files/usr/bin/sh
# Auto-start SSH script for Termux
# Run once to enable ssh-agent on boot

echo "[ssh-agent] Starting ssh-agent..."
pkill ssh-agent 2>/dev/null
ssh-agent -s > ~/.ssh/agent-env
echo "[ssh-agent] Agent env saved to ~/.ssh/agent-env"
echo "[ssh-agent] To use: source ~/.ssh/agent-env && ssh-add"

# Optional: auto-add key if exists
if [ -f ~/.ssh/id_ed25519 ]; then
    source ~/.ssh/agent-env 2>/dev/null
    ssh-add ~/.ssh/id_ed25519 2>/dev/null && echo "[ssh-agent] Key added." || echo "[ssh-agent] Key add failed."
fi

echo "[ssh-agent] Done."