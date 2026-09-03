#!/bin/bash
# Hermes Breaking News Watchdog
# Runs every 4 hours, sends alert only if threshold met.
# Max 3 alerts per day. Counter resets daily.

ALERT_FILE="/root/.hermes/news_alert_count.txt"
ALERT_LOG="/root/.hermes/news_alerts_today.txt"
MAX_ALERTS=3

# Get current date for reset check
TODAY=$(date +%Y-%m-%d)
STORED_DATE=$(cat $ALERT_FILE 2>/dev/null | head -1)

# Reset counter if new day
if [ "$STORED_DATE" != "$TODAY" ]; then
    echo "$TODAY" > $ALERT_FILE
    echo "0" >> $ALERT_FILE
    > $ALERT_LOG
fi

ALERT_COUNT=$(cat $ALERT_FILE | tail -1)

# Check if already at max
if [ "$ALERT_COUNT" -ge $MAX_ALERTS ]; then
    echo "[$(date)] Alert cap reached ($ALERT_COUNT/$MAX_ALERTS). Skip."
    exit 0
fi

# ===== THRESHOLD CHECK =====

# Check Malaysian political breaking news
政治_news=$(curl -s "https://news.google.com/rss/search?q=Malaysia+politics+breaking&hl=en-MY&gl=MY&ceid=MY:en" 2>/dev/null | grep -o '<title>[^<]*</title>' | head -5 | sed 's/<[^>]*>//g' | tr '\n' '|' | cut -c1-500)

# Check PETRONAS / energy breaking news
petronas_news=$(curl -s "https://news.google.com/rss/search?q=Petronas+OR+MALAYSIA+energy+crisis&hl=en-MY&gl=MY&ceid=MY:en" 2>/dev/null | grep -o '<title>[^<]*</title>' | head -5 | sed 's/<[^>]*>//g' | tr '\n' '|' | cut -c1-500)

# Check South China Sea / regional conflict
regional_news=$(curl -s "https://news.google.com/rss/search?q=South+China+Sea+OR+OPEC+crisis&hl=en-US&gl=US&ceid=US:en" 2>/dev/null | grep -o '<title>[^<]*</title>' | head -5 | sed 's/<[^>]*>//g' | tr '\n' '|' | cut -c1-500)

# Check AI governance / critical AI news
ai_news=$(curl -s "https://news.google.com/rss/search?q=AI+safety+regulation+critical&hl=en-US&gl=US&ceid=US:en" 2>/dev/null | grep -o '<title>[^<]*</title>' | head -3 | sed 's/<[^>]*>//g' | tr '\n' '|' | cut -c1-500)

# Log what we found (debug)
echo "[$(date)] Watchdog ran. Counts: 政治=$政治_news | PETRONAS=$petronas_news | regional=$regional_news | AI=$ai_news" >> /root/.hermes/news_watchdog.log

# Threshold evaluation - critical keyword scan
# Only fires on: crisis, emergency, war, major policy, shocking, death, resignation, scandal, accident, explosion, attack, sanctioned, shutdown, blackout
CRITICAL_WORDS="crisis|emergency|war|resign|scandal|explosion|attack|accident|shutdown|blackout|major|sanction|blast|flood|quake|death|collapse|shutdown|strike|halt|curfew|martial"

BREAKING_TRIGGER=0
ALERT_TITLE=""
ALERT_BODY=""
ALERT_TAG=""

# Evaluate Malaysian politics
if echo "$政治_news" | grep -qiE "$CRITICAL_WORDS"; then
    BREAKING_TRIGGER=1
    ALERT_TAG="POLITIK"
    ALERT_TITLE="🇲🇾 Malaysia Political Alert"
    ALERT_BODY=" Breaking: $政治_news"
fi

# Evaluate PETRONAS / energy
if echo "$petronas_news" | grep -qiE "$CRITICAL_WORDS"; then
    BREAKING_TRIGGER=1
    ALERT_TAG="PETRONAS"
    ALERT_TITLE="⛽ PETRONAS / Energy Alert"
    ALERT_BODY=" Breaking: $petronas_news"
fi

# Evaluate regional
if echo "$regional_news" | grep -qiE "$CRITICAL_WORDS"; then
    BREAKING_TRIGGER=1
    ALERT_TAG="REGIONAL"
    ALERT_TITLE="🌏 Regional Alert"
    ALERT_BODY=" Breaking: $regional_news"
fi

# If trigger hit - send to Hermes via Hermes A2A or direct Telegram
# We'll use a simple Telegram bot message approach via curl

if [ "$BREAKING_TRIGGER" -eq 1 ]; then
    NEW_COUNT=$((ALERT_COUNT + 1))
    echo "$TODAY" > $ALERT_FILE
    echo "$NEW_COUNT" >> $ALERT_FILE
    echo "[$(date)] ALERT SENT [$ALERT_TAG] - Count: $NEW_COUNT/$MAX_ALERTS" >> /root/.hermes/news_alerts_today.txt
    
    # Format alert message
    ALERT_MSG="🚨 NEWS ALERT — $ALERT_TAG

$ALERT_BODY

Suggested: WATCH | ACT

_Counter: $NEW_COUNT/$MAX_ALERTS hari ini_"
    
    # Send via Hermes agent relay (port 3002) or fallback to file
    curl -s -X POST "http://localhost:3002/notify" \
        -H "Content-Type: application/json" \
        -d "{\"message\": \"$ALERT_MSG\", \"target\": \"telegram\"}" \
        >> /root/.hermes/news_alerts_today.txt 2>&1
    
    echo "[$(date)] Alert dispatched."
else
    echo "[$(date)] No threshold trigger. Silent."
fi

exit 0