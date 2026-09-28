# Restart orphan PID if it was the canonical state
nohup /usr/bin/python3 -m hermes_mcp > /tmp/hermes_mcp.orphan.log 2>&1 &
systemctl stop hermes-mcp-server.service
systemctl mask hermes-mcp-server.service
echo "Q4 ROLLBACK · orphan restarted, service masked"
