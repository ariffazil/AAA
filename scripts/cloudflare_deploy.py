#!/usr/bin/env python3
import os
import subprocess
import sys

ACCOUNT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "22cc94b77b6481d2b054bee7952710e6")
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")

if not TOKEN:
    print("Missing required environment variable: CLOUDFLARE_API_TOKEN", file=sys.stderr)
    sys.exit(1)

env = {
    **os.environ,
    "CLOUDFLARE_API_TOKEN": TOKEN,
    "CLOUDFLARE_ACCOUNT_ID": ACCOUNT,
}

r = subprocess.run(
    [
        "wrangler",
        "pages",
        "deploy",
        "/root/arif-sites/arif/dist",
        "--project-name",
        "arifOS",
        "--branch",
        "main",
    ],
    env=env,
    capture_output=True,
    text=True,
    timeout=90,
)
print("RC:", r.returncode)
print("STDOUT:", r.stdout[-800:] if r.stdout else "none")
print("STDERR:", r.stderr[-800:] if r.stderr else "none")
