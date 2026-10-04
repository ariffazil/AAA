#!/usr/bin/env bash
# Webhook truth probe: getWebhookInfo for every federation bot token.
# Usage: bash scripts/telegram-webhook-truth.sh
# Sources /root/.secrets/kunci-mas.env (5-R Protocol). Prints url / pending / last_error per bot.
# Never trust a pasted "bot HIDUP/TUTUP" claim — this is the live truth.
set -a && source /root/.secrets/kunci-mas.env && set +a
for v in ASI_ARIFOS_BOT_TOKEN AGI_ASI_BOT_TOKEN FORGE_BOT_TOKEN; do
  tok="${!v}"
  if [ -n "$tok" ]; then
    info=$(curl -s --max-time 10 "https://api.telegram.org/bot${tok}/getWebhookInfo")
    echo "== $v: $(echo "$info" | python3 -c 'import json,sys; d=json.load(sys.stdin); r=d.get("result",{}); print("url=",r.get("url"),"pending=",r.get("pending_update_count"),"err=",r.get("last_error_message"))' 2>/dev/null || echo "$info" | head -c 200)"
  else
    echo "== $v: NOT SET in vault"
  fi
done
