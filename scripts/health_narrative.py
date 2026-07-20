#!/usr/bin/env python3
"""Federation Health Narrative — TokenRouter synthesis pipeline.
Probes all 6 organs + system metrics → TokenRouter → human-readable health summary.
Output: /root/AAA/docs/FEDERATION_HEALTH.md
Usage: python3 /root/AAA/scripts/health_narrative.py
"""

import json, os, subprocess, sys
from datetime import datetime
from pathlib import Path

OUTPUT = "/root/AAA/docs/FEDERATION_HEALTH.md"
TR_URL = "https://api.tokenrouter.com/v1/chat/completions"
ORGANS = {
    "arifOS": "http://127.0.0.1:8088/health",
    "A-FORGE": "http://127.0.0.1:7071/health",
    "AAA": "http://127.0.0.1:3001/health",
    "GEOX": "http://127.0.0.1:8081/health",
    "WEALTH": "http://127.0.0.1:18082/health",
    "WELL": "http://127.0.0.1:18083/health",
}

def load_secrets():
    env_file = "/root/.secrets/vault.env"
    if os.path.exists(env_file):
        result = subprocess.run(["bash", "-c", f"set -a; . {env_file}; set +a; env"], capture_output=True, text=True)
        for line in result.stdout.split("\n"):
            if "=" in line:
                k, _, v = line.partition("=")
                os.environ[k] = v

def probe_organs():
    import urllib.request
    results = {}
    for name, url in ORGANS.items():
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
                results[name] = {
                    "status": data.get("status", "unknown"),
                    "version": data.get("version", "?"),
                    "uptime": str(data.get("uptime", "?"))[:20]
                }
        except Exception as e:
            results[name] = {"status": "DOWN", "error": str(e)[:100]}
    return results

def get_system_metrics():
    metrics = {}
    try:
        r = subprocess.run(["free", "-h"], capture_output=True, text=True)
        metrics["memory"] = r.stdout.split("\n")[1] if r.stdout else "N/A"
    except: pass
    try:
        r = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
        metrics["disk"] = r.stdout.split("\n")[1] if r.stdout else "N/A"
    except: pass
    try:
        r = subprocess.run(["uptime"], capture_output=True, text=True)
        metrics["uptime"] = r.stdout.strip()
    except: pass
    try:
        r = subprocess.run(["systemctl", "--failed", "--no-legend"], capture_output=True, text=True)
        metrics["failed_services"] = len(r.stdout.strip().split("\n")) if r.stdout.strip() else 0
    except: pass
    try:
        r = subprocess.run(["docker", "ps", "--format", "{{.Names}} {{.Status}}"], capture_output=True, text=True)
        containers = [l for l in r.stdout.strip().split("\n") if l]
        metrics["containers"] = f"{len(containers)} running"
        metrics["container_detail"] = "\n".join(containers[:8])
    except: pass
    return metrics

def build_prompt(organs, metrics):
    organ_text = "\n".join([f"  {k}: {v.get('status','?')} (v{v.get('version','?')})" for k, v in organs.items()])
    down_count = sum(1 for v in organs.values() if v.get("status") == "DOWN")
    
    prompt = f"""You are the arifOS Federation health monitor. Write a plain-English health summary.

CURRENT STATE:
Organs ({len(organs)} total, {down_count} down):
{organ_text}

System:
  Memory: {metrics.get('memory', 'N/A')}
  Disk: {metrics.get('disk', 'N/A')}
  Uptime: {metrics.get('uptime', 'N/A')}
  Failed services: {metrics.get('failed_services', '?')}
  Docker: {metrics.get('containers', 'N/A')}
  {metrics.get('container_detail', '')}

Rules:
- 3-4 sentences maximum. Arif reads this in 10 seconds.
- No jargon. No floor numbers. No JSON.
- If everything is green, say "All clear" and move on.
- If something is down or degraded, lead with that.
- End with a one-line recommendation if anything needs attention.

HEALTH SUMMARY:"""
    return prompt

def call_tokenrouter(prompt):
    TR_KEY = os.getenv("TOKENROUTER_API_KEY", "")
    TR_MODEL = os.getenv("TOKENROUTER_MODEL", "deepseek/deepseek-v4-flash")
    if not TR_KEY:
        return "⚠️ TokenRouter API key not set."
    
    import urllib.request
    payload = json.dumps({
        "model": TR_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.3
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
        return f"⚠️ TokenRouter: {e}"

def main():
    load_secrets()
    
    organs = probe_organs()
    metrics = get_system_metrics()
    prompt = build_prompt(organs, metrics)
    narrative = call_tokenrouter(prompt)
    
    down_organs = [k for k, v in organs.items() if v.get("status") == "DOWN"]
    status_icon = "🔴" if down_organs else "🟢"
    
    report = f"""# {status_icon} Federation Health

> **Probed:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
> **Pipeline:** organ probes → TokenRouter → narrative

---

{narrative}

---

## Raw Probe Data

| Organ | Status | Version |
|-------|--------|---------|
"""
    for name, data in organs.items():
        icon = "✅" if data.get("status") in ("healthy", "ok", "live") else "❌"
        report += f"| {icon} {name} | {data.get('status', '?')} | {data.get('version', data.get('uptime', '?'))} |\n"
    
    report += f"""
**System:** {metrics.get('uptime', 'N/A')}
**Memory:** {metrics.get('memory', 'N/A')}
**Disk:** {metrics.get('disk', 'N/A')}
**Failed services:** {metrics.get('failed_services', 0)}
**Docker:** {metrics.get('containers', 'N/A')}
"""
    
    Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w") as f:
        f.write(report)
    print(f"✅ Health narrative written to {OUTPUT}")
    print(f"   {len(organs)} organs probed, {len(down_organs)} down")

if __name__ == "__main__":
    main()
