#!/usr/bin/env python3
"""
arifOS Session Title Generator — FLAME-powered, RM0 free.
Generates a 5-8 word title from the first user message of a session.
Stores in Redis + updates carry_forward.json.

Usage:
  python3 session-title.py "what is the user's first message about?"
  
Output: JSON with generated title
"""
import json, sys, os, hashlib, time
from urllib.request import Request, urlopen
from urllib.error import URLError

FLAME_URL = "http://localhost:18901/v1/chat/completions"
REDIS_HOST = "localhost"
REDIS_PORT = 6379
CARRY_FORWARD_PATH = "/root/.local/share/arifos/carry_forward.json"

SYSTEM_PROMPT = """Generate a short 4-7 word title for this AI agent conversation.
Rules:
- Return ONLY the title, no quotes, no explanation
- Be specific about the topic/domain
- Use technical terms where appropriate
- Examples: "Federation Memory Architecture Audit", "VAULT999 Seal Chain Verification", "WELL Biometric Telemetry Wiring"
"""

def generate_title(user_message: str) -> str:
    """Call FLAME to generate a session title."""
    payload = {
        "model": "flame-free",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message[:500]}
        ],
        "max_tokens": 30,
        "temperature": 0.3
    }
    
    try:
        req = Request(FLAME_URL, data=json.dumps(payload).encode(), headers={
            "Content-Type": "application/json"
        })
        resp = urlopen(req, timeout=15)
        data = json.loads(resp.read())
        title = data.get("content", "").strip().strip('"').strip("'")
        return title if title else None
    except Exception as e:
        print(f"FLAME error: {e}", file=sys.stderr)
        return None

def store_title(title: str, source_message: str):
    """Store generated title in Redis and carry_forward.json."""
    # Store in Redis
    try:
        import redis
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        title_key = f"session_title:{int(time.time())}"
        r.hset(title_key, mapping={
            "title": title,
            "source": source_message[:200],
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "generator": "flame-free"
        })
        r.expire(title_key, 86400 * 30)  # 30 day TTL
        print(f"Redis: stored at {title_key}", file=sys.stderr)
    except ImportError:
        print("Redis: redis-py not available, skipping", file=sys.stderr)
    except Exception as e:
        print(f"Redis error: {e}", file=sys.stderr)

    # Update carry_forward.json
    try:
        cf = json.load(open(CARRY_FORWARD_PATH))
        cf["session_title"] = title
        cf["session_title_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        json.dump(cf, open(CARRY_FORWARD_PATH, "w"), indent=2, ensure_ascii=False)
        print(f"carry_forward.json: title stored", file=sys.stderr)
    except Exception as e:
        print(f"carry_forward error: {e}", file=sys.stderr)

def main():
    if len(sys.argv) < 2:
        # Try reading from stdin
        if not sys.stdin.isatty():
            user_message = sys.stdin.read().strip()
        else:
            print(json.dumps({"error": "No message provided. Usage: session-title.py 'message'"}))
            sys.exit(1)
    else:
        user_message = " ".join(sys.argv[1:])
    
    if not user_message:
        print(json.dumps({"error": "Empty message"}))
        sys.exit(1)
    
    title = generate_title(user_message)
    
    if title:
        store_title(title, user_message)
    
    result = {
        "title": title,
        "source_length": len(user_message),
        "generator": "flame-free-rm0",
        "stored_in": ["redis", "carry_forward.json"] if title else []
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0 if title else 1

if __name__ == "__main__":
    sys.exit(main())
