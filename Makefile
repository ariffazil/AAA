# ARIFOS FLEET COMMAND
# Usage: make status | make up | make logs-zero

# ---------------- CONFIGURATION ----------------
# Adjust these paths to where your actual docker-compose.yaml files are
DIR_AGI = /root/agi-stack
DIR_CLAW = /root/oo0-stack

# ---------------- COMMANDS ----------------
status:
	@echo "📡 Scanning Fleet Status..."
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

up:
	@echo "🚀 Launching The Brain (Agent Zero + Qdrant)..."
	cd $(DIR_AGI) && docker compose up -d
	@echo "🦞 Releasing The Hands (OpenClaw + ArifOS)..."
	cd $(DIR_CLAW) && docker compose up -d
	@echo "✅ All Systems Green."

down:
	@echo "🛑 Shutting down ALL systems..."
	docker stop $$(docker ps -q)

restart-zero:
	@echo "♻️ Rebooting Agent Zero..."
	docker restart agentzero

logs-zero:
	docker logs -f agentzero

logs-claw:
	docker logs -f openclaw

# ---------------- TUNNEL ----------------
tunnel-check:
	systemctl status cloudflared

# Federation forge gate — entropy reducer on every push
include /root/arifOS/scripts/forge.mk
include /root/arifOS/scripts/security_audit.mk
