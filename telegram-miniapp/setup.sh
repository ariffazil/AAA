#!/bin/bash
# arifOS Federation — Telegram Mini App Setup
# Run this ONCE after creating bots via @BotFather
# Usage: ./setup.sh

set -e

echo "╔══════════════════════════════════════════════╗"
echo "║  arifOS Federation — Telegram Mini App Setup ║"
echo "║  DITEMPA BUKAN DIBERI                        ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Check .env
if [ ! -f .env ]; then
    echo "❌ .env not found. Copy .env.example to .env and fill in BOT_TOKEN"
    exit 1
fi

source .env

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ BOT_TOKEN not set in .env"
    echo ""
    echo "Steps:"
    echo "  1. Open @BotFather on Telegram"
    echo "  2. /newbot → name: 'arifOS Federation'"
    echo "  3. Copy the token"
    echo "  4. Edit .env → BOT_TOKEN=<your token>"
    echo "  5. Run this script again"
    exit 1
fi

echo "✅ BOT_TOKEN found"
echo ""

# Build Mini App
echo "📦 Building Mini App..."
cd app && npx vite build 2>&1 | tail -3
cd ..

# Deploy static files
echo "📁 Deploying to /var/www/html/miniapp..."
rm -rf /var/www/html/miniapp/*
cp -r app/dist/* /var/www/html/miniapp/
echo "✅ Static files deployed"

# Reload Caddy
echo "🔄 Reloading Caddy..."
systemctl reload caddy 2>&1
echo "✅ Caddy reloaded"

# Start services
echo "🚀 Starting services..."
systemctl daemon-reload
systemctl enable miniapp-api miniapp-bot
systemctl restart miniapp-api
sleep 2
systemctl restart miniapp-bot
echo "✅ Services started"

# Health check
echo ""
echo "🏥 Health check..."
sleep 3
curl -sf http://localhost:3100/health >/dev/null 2>&1 && echo "  ✅ API Gateway :3100" || echo "  ❌ API Gateway :3100"
curl -sf https://app.arif-fazil.com/health >/dev/null 2>&1 && echo "  ✅ app.arif-fazil.com" || echo "  ❌ app.arif-fazil.com"

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║  SETUP COMPLETE                              ║"
echo "╠══════════════════════════════════════════════╣"
echo "║  Bot:     https://t.me/<your_bot>            ║"
echo "║  MiniApp: https://app.arif-fazil.com         ║"
echo "║  API:     http://localhost:3100               ║"
echo "╠══════════════════════════════════════════════╣"
echo "║  Next steps:                                 ║"
echo "║  1. Open your bot on Telegram                ║"
echo "║  2. Tap 🌍 Explorer button                   ║"
echo "║  3. Create AIA/SADO/AAA bots (optional)      ║"
echo "╚══════════════════════════════════════════════╝"
