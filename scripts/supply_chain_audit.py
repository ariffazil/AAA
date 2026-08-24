#!/usr/bin/env python3
"""Supply-chain skill audit — P1, F13-greenlit 2026-08-25.
Monthly manifest hash-check across all skill roots.
Silent when unchanged (exit 0, no output). On anomaly: non-zero exit,
structured report, Telegram alert via bot token from kunci-root.env.

Research base: Zenity Aug-2026 (1.7M-install malicious skill family);
arXiv:2511.19874, arXiv:2510.05159 (agent supply-chain backdoors/poisoning).
"""
import hashlib, json, os, subprocess, sys, datetime

ROOTS = [
    "/root/.hermes/skills",
    "/root/.hermes/profiles/aaa-hermes/skills",
    "/root/.hermes/profiles/hermes_apex/skills",
    "/root/.hermes/profiles/hermes_asi/skills",
    "/root/.hermes/profiles/hermes_forge/skills",
    "/root/.openclaw/skills",
    "/root/.claude/skills",
]
MANIFEST_DIR = "/root/AAA/security"
MANIFEST = os.path.join(MANIFEST_DIR, "skill-manifest.json")
TG_TEXT_MAX = 3500

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def scan():
    m = {}
    for root in ROOTS:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for fn in filenames:
                if fn == "SKILL.md":
                    fp = os.path.join(dirpath, fn)
                    try:
                        m[fp] = sha256(fp)
                    except OSError:
                        m[fp] = "UNREADABLE"
    return m

def alert(text):
    token = os.environ.get("HERMES_TELEGRAM_BOT_TOKEN", "")
    chat = os.environ.get("TELEGRAM_HOME_CHANNEL", "")
    if not token or not chat:
        print("ALERT-NO-CHANNEL", file=sys.stderr); return
    subprocess.run(["curl", "-sS", "--max-time", "15",
        f"https://api.telegram.org/bot{token}/sendMessage",
        "-d", f"chat_id={chat}",
        "-d", f"text={text[:TG_TEXT_MAX]}"],
        capture_output=True, timeout=25)

def main():
    os.makedirs(MANIFEST_DIR, exist_ok=True)
    new = scan()
    if not os.path.exists(MANIFEST):
        with open(MANIFEST, "w") as f:
            json.dump({"baseline_ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                       "skills": new}, f, indent=1)
        print(f"BASELINE written: {len(new)} SKILL.md files hashed.")
        return 0
    with open(MANIFEST) as f:
        old = json.load(f).get("skills", {})
    added = sorted(set(new) - set(old))
    removed = sorted(set(old) - set(new))
    changed = sorted(p for p in set(new) & set(old) if new[p] != old[p])
    # persist new manifest regardless (rolling baseline)
    with open(MANIFEST, "w") as f:
        json.dump({"baseline_ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   "skills": new}, f, indent=1)
    if not (added or removed or changed):
        return 0  # silent — no change
    lines = [f"[P1 supply-chain audit] anomalies at "
             f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')}"]
    for label, lst in (("ADDED", added), ("REMOVED", removed), ("CHANGED", changed)):
        for p in lst[:20]:
            lines.append(f"{label}: {p}")
    if len(added) + len(removed) + len(changed) > 20:
        lines.append(f"... and {len(added)+len(removed)+len(changed)-20} more")
    report = "\n".join(lines)
    print(report)
    alert("⚠️ " + report)
    return 2

if __name__ == "__main__":
    sys.exit(main())
