#!/usr/bin/env python3
"""VAULT999 Weekly Chronicle — TokenRouter synthesis pipeline.
Reads seal chain → TokenRouter → human-readable weekly digest.
Output: /root/AAA/docs/WEEKLY_CHRONICLE.md
Usage: python3 /root/AAA/scripts/chronicle_vault999.py
"""

import json, os, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path

SEAL_CHAIN = "/root/.local/share/arifos/vault999/seal_chain.jsonl"
OUTPUT = "/root/AAA/docs/WEEKLY_CHRONICLE.md"
TR_URL = "https://api.tokenrouter.com/v1/chat/completions"
TR_KEY = os.getenv("TOKENROUTER_API_KEY", "")
TR_MODEL = os.getenv("TOKENROUTER_MODEL", "deepseek/deepseek-v4-flash")

def load_secrets():
    env_file = "/root/.secrets/vault.env"
    if os.path.exists(env_file):
        result = subprocess.run(["bash", "-c", f"set -a; . {env_file}; set +a; env"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "=" in line:
                k, _, v = line.partition("=")
                os.environ[k] = v

def read_recent_seals(days=7):
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    seals = []
    if not os.path.exists(SEAL_CHAIN):
        return seals
    with open(SEAL_CHAIN) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if isinstance(entry, str):
                    try:
                        entry = json.loads(entry)
                    except:
                        continue
                ts = entry.get("timestamp", entry.get("sealed_at", ""))
                if ts and ts > cutoff:
                    seals.append(entry)
            except json.JSONDecodeError:
                continue
    return seals

def build_prompt(seals):
    if not seals:
        return None, "No seals found in the last 7 days."
    
    summary = []
    for i, s in enumerate(seals[:50]):
        verdict = s.get("verdict", s.get("type", "UNKNOWN"))
        desc = s.get("summary", s.get("description", s.get("content", "")))[:200]
        actor = s.get("actor_id", s.get("actor_signature", "unknown"))[:40]
        ts = s.get("timestamp", s.get("sealed_at", ""))[:19]
        summary.append(f"[{ts}] {verdict} | {actor} | {desc}")
    
    seal_text = "\n".join(summary)
    count = len(seals)
    
    prompt = f"""You are the arifOS Federation archivist. Write a weekly chronicle of what happened.

Below are {count} seal events recorded in VAULT999 this week. Write a narrative in plain English (3-5 paragraphs) that a non-technical sovereign can read in 60 seconds.

Rules:
- No jargon. No code. No floor numbers. No receipt IDs.
- Group related events into themes (e.g., "Agent Alignment", "Infrastructure", "Fixes")
- Mention what was DONE, not how
- If nothing notable, say so honestly
- End with: "Seals this week: {count}"

SEAL EVENTS:
{seal_text}

WEEKLY CHRONICLE:"""
    return prompt, f"Generated from {count} seal events"

def call_tokenrouter(prompt):
    if not TR_KEY:
        return "⚠️ TokenRouter API key not set. Set TOKENROUTER_API_KEY."
    
    import urllib.request
    payload = json.dumps({
        "model": TR_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500,
        "temperature": 0.5
    }).encode()
    
    req = urllib.request.Request(TR_URL, data=payload, headers={
        "Authorization": f"Bearer {TR_KEY}",
        "Content-Type": "application/json"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ TokenRouter call failed: {e}"

def main():
    load_secrets()
    global TR_KEY
    TR_KEY = os.getenv("TOKENROUTER_API_KEY", TR_KEY)
    
    seals = read_recent_seals(days=7)
    prompt, note = build_prompt(seals)
    
    header = f"""# 📜 VAULT999 Weekly Chronicle

> **Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
> **Source:** {len(seals)} seal events from VAULT999
> **Pipeline:** seal_chain.jsonl → TokenRouter ({TR_MODEL}) → narrative

---

"""
    
    if prompt is None:
        chronicle = header + f"_{note}_\n"
    else:
        narrative = call_tokenrouter(prompt)
        chronicle = header + narrative + f"\n\n---\n*{note}*\n"
    
    Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        f.write(chronicle)
    print(f"✅ Chronicle written to {OUTPUT}")
    print(f"   {len(seals)} seal events processed")

if __name__ == "__main__":
    main()
