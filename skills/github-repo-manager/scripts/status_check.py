#!/usr/bin/env python3
"""
GitHub Repository Status Checker for arifOS Ecosystem

Fetches and displays status information for all ariffazil repositories.
"""

import os
import json
import urllib.request
from datetime import datetime

REPOSITORIES = [
    "arifOS",
    "GEOX",
    "arifosmcp",
    "arif-sites",
    "waw",
    "agent-workbench",
    "arifOS-model-registry",
    "APEX"
]

OWNER = "ariffazil"

def get_github_token():
    """Get GitHub token from environment."""
    return os.environ.get("GITHUB_TOKEN", "")

def fetch_repo_info(repo_name, token):
    """Fetch repository information from GitHub API."""
    url = f"https://api.github.com/repos/{OWNER}/{repo_name}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {"error": str(e)}

def format_timestamp(ts):
    """Format ISO timestamp to readable format."""
    if not ts:
        return "N/A"
    dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%Y-%m-%d %H:%M")

def print_status_table():
    """Print status table for all repositories."""
    token = get_github_token()

    print(f"\n{'='*80}")
    print(f"GitHub Repository Status - {OWNER}")
    print(f"{'='*80}")
    print(f"{'Repository':<25} {'Stars':<8} {'Forks':<8} {'Open Issues':<12} {'Last Updated':<20}")
    print(f"{'-'*80}")

    for repo in REPOSITORIES:
        info = fetch_repo_info(repo, token)

        if "error" in info:
            print(f"{repo:<25} ERROR: {info['error'][:50]}")
            continue

        stars = info.get("stargazers_count", 0)
        forks = info.get("forks_count", 0)
        issues = info.get("open_issues_count", 0)
        updated = format_timestamp(info.get("updated_at", ""))
        language = info.get("language", "-")

        print(f"{repo:<25} {stars:<8} {forks:<8} {issues:<12} {updated:<20} ({language})")

    print(f"{'='*80}\n")

if __name__ == "__main__":
    print_status_table()
