#!/usr/bin/env python3
"""
antigravity-stream-pipe.py — Pipe AGY stream-json output into VAULT999 receipts.
Reads NDJSON from stdin, seals each event to arifOS kernel.

Usage: gemini -p "..." -y -o stream-json | python3 antigravity-stream-pipe.py
"""

import sys
import json
import subprocess
import datetime

VAULT999_ENDPOINT = "http://localhost:8088/mcp"
LOG_PATH = "/root/.gemini/antigravity-cli/log/stream-seals.jsonl"

def call_arif_seal(event):
    """Seal a single NDJSON event to VAULT999."""
    event_type = event.get("type", "unknown")
    conv_id = event.get("conversationId", "?")
    
    seal_payload = {
        "mode": "seal",
        "payload": json.dumps({
            "source": "antigravity-stream",
            "event_type": event_type,
            "conversation_id": conv_id,
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "event_summary": str(event.get("message", event.get("thought", "")))[:500]
        }),
        "seal_purpose": f"agy-stream-{event_type}",
        "witness_type": "ai"
    }
    
    req = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "arif_seal",
            "arguments": seal_payload
        },
        "id": 1
    }
    
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", VAULT999_ENDPOINT,
             "-H", "Content-Type: application/json",
             "-d", json.dumps(req)],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout[:200]
    except Exception as e:
        return str(e)[:100]

def main():
    sealed = 0
    errors = 0
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            # Non-JSON line (e.g., warning) — echo through
            print(line)
            continue
        
        # Seal the event
        seal_result = call_arif_seal(event)
        sealed += 1
        
        # Log to local file
        log_entry = {
            "ts": datetime.datetime.now(datetime.UTC).isoformat(),
            "event_type": event.get("type", "?"),
            "conv_id": event.get("conversationId", "?"),
            "seal": seal_result
        }
        with open(LOG_PATH, "a") as f:
            json.dump(log_entry, f)
            f.write("\n")
        
        # Pass through to stdout for logging
        print(json.dumps(event))
    
    # Final flush
    summary = {"sealed": sealed, "errors": errors, "done": True}
    with open(LOG_PATH, "a") as f:
        json.dump({"ts": datetime.datetime.now(datetime.UTC).isoformat(), "summary": summary}, f)
        f.write("\n")
    
    print(f"[stream-pipe] Sealed {sealed} events to VAULT999 ({errors} errors)", file=sys.stderr)

if __name__ == "__main__":
    main()
