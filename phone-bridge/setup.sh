#!/data/data/com.termux/files/usr/bin/env bash
# arifOS Phone Bridge — phone-side setup
# Run once from ~/phone-bridge/ after files are scp'd from VPS.
set -euo pipefail

cd "$(dirname "$0")"

echo "── 1. packages ──"
pkg install -y python termux-api termux-tools openssl-tool tmux 2>&1 | tail -5

echo "── 2. bridge dir ──"
mkdir -p ~/.bridge/photos
chmod 700 ~/.bridge

echo "── 3. env ──"
if [[ ! -f .env ]]; then
  if [[ -z "${BRIDGE_TOKEN:-}" ]]; then
    export BRIDGE_TOKEN="$(openssl rand -hex 16)"
  fi
  cat > .env <<EOF
BRIDGE_TOKEN=$BRIDGE_TOKEN
BRIDGE_PORT=8765
BRIDGE_HOST=0.0.0.0
EOF
  chmod 600 .env
fi
# shellcheck disable=SC1091
set -a; source .env; set +a

echo "── 4. install server.py ──"
install -m 755 server.py /data/data/com.termux/files/home/phone-bridge/server.py
ln -sf /data/data/com.termux/files/home/phone-bridge/server.py ~/phone-bridge/server.py

echo "── 5. validate import ──"
python -c "import ast; ast.parse(open('server.py').read())" && echo "server.py: syntax ok"

echo
echo "── DONE ──"
echo "BRIDGE_TOKEN (full) = $BRIDGE_TOKEN"
echo "Save this token on the VPS at /root/.secrets/phone-bridge.env"
echo
echo "To run foreground:  cd ~/phone-bridge && source .env && python server.py"
echo "To run in tmux:     tmux new -d -s bridge 'cd ~/phone-bridge && source .env && python server.py'"
echo "To attach log tmux: tmux attach -t bridge"
