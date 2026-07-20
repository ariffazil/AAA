#!/usr/bin/env python3
"""Memory Continuity Bridge — TokenRouter synthesis pipeline.
Reads last 3 days of memory logs → TokenRouter → compressed continuity summary.
Output: /root/AAA/docs/CONTINUITY_BRIDGE.md (injected at session start)
Usage: python3 /root/AAA/scripts/memory_bridge.py
"""

import json, os, subprocess, sys
from datetime import datetime, timedelta
from pathlib import Path

MEMORY_DIR = "/root/memory"
SESSION_STATE = "/root/.claude/projects/-root/memory/session-state.md"
CONTEXT = "/root/CONTEXT.md"
OUTPUT = "/root/AAA/docs/CONTINUITY_BRIDGE.md"
TR_URL = "https://api.tokenrouter.com/v1/chat/completions"


def load_secrets():
    env_file = "/root/.secrets/vault.env"
    if os.path.exists(env_file):
        result = subprocess.run(["bash", "-c", f"set -a; . {env_file}; set +a; env"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "=" in line:
                k, _, v = line.partition("=")
                os.environ[k] = v


def read_memory_logs(days=3):
    logs = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        path = f"{MEMORY_DIR}/{date}.md"
        if os.path.exists(path):
            with open(path) as f:
                content = f.read()[:5000]  # First 5KB per day
            logs.append({"date": date, "content": content})
    return logs


def read_context():
    data = {}
    if os.path.exists(CONTEXT):
        with open(CONTEXT) as f:
            data["context"] = f.read()[:2000]
    if os.path.exists(SESSION_STATE):
        with open(SESSION_STATE) as f:
            data["session_state"] = f.read()[:2000]

    # Git activity last 3 days
    try:
        r = subprocess.run(
            [
                "bash",
                "-c",
                "for d in /root/arifOS /root/A-FORGE /root/AAA /root/geox /root/WEALTH /root/WELL; do cd $d 2>/dev/null && git log --oneline --since='3 days ago' 2>/dev/null | head -5; done",
            ],
            capture_output=True,
            text=True,
        )
        data["git_activity"] = r.stdout.strip()[:2000]
    except:
        pass

    return data


def build_prompt(logs, context_data):
    log_text = "\n\n".join([f"=== {l['date']} ===\n{l['content'][:3000]}" for l in logs])
    git = context_data.get("git_activity", "No git data")
    ctx = context_data.get("context", "")[:1000]
    state = context_data.get("session_state", "")[:1000]

    prompt = f"""You are the arifOS Federation continuity engine. Compress the last 3 days into a 400-word summary that an AI coding agent reads at session start.

RECENT MEMORY LOGS:
{log_text}

CURRENT CONTEXT:
{ctx}

SESSION STATE:
{state}

GIT ACTIVITY (last 3 days):
{git}

Rules:
- 400 words maximum. Agents need this as compact context injection.
- Focus on: what was DECIDED, what was BUILT, what is BLOCKED, what is OPEN.
- Use bullet points for clarity.
- Include: "Arif's last directive: [what Arif asked for]"
- Include: "Active blockers: [what's waiting]"
- Include: "Key state changes: [configs modified, services changed]"
- Never include: API keys, floor violation details, internal agent chatter.

CONTINUITY SUMMARY:"""
    return prompt


def call_tokenrouter(prompt):
    TR_KEY = os.getenv("TOKENROUTER_API_KEY", "")
    TR_MODEL = os.getenv("TOKENROUTER_MODEL", "deepseek/deepseek-v4-flash")
    if not TR_KEY:
        return "⚠️ TokenRouter API key not set."

    import urllib.request

    payload = json.dumps(
        {"model": TR_MODEL, "messages": [{"role": "user", "content": prompt}], "max_tokens": 2000, "temperature": 0.3}
    ).encode()

    req = urllib.request.Request(
        TR_URL, data=payload, headers={"Authorization": f"Bearer {TR_KEY}", "Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ TokenRouter: {e}"


def main():
    load_secrets()

    logs = read_memory_logs(days=3)
    context_data = read_context()
    prompt = build_prompt(logs, context_data)
    summary = call_tokenrouter(prompt)

    bridge = f"""# 🧵 Continuity Bridge

> **Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}
> **Source:** {len(logs)} days memory logs + context + git activity
> **Pipeline:** memory logs → TokenRouter → compressed context
> **Usage:** Inject at start of every agent session for continuity.

---

{summary}

---

*Auto-generated. Refreshed on demand. Inject into agent INIT sequence.*
"""

    Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        f.write(bridge)
    print(f"✅ Continuity bridge written to {OUTPUT}")
    print(f"   {len(logs)} days of memory compressed")


if __name__ == "__main__":
    main()
