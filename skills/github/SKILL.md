---
name: github
description: Native GitHub MCP for repo/PR/issue management — direct tool calls vs skill overhead
category: development
---

# GitHub MCP Skill

## Trigger
Any task involving GitHub repositories, issues, PRs, or code search.

## Credentials
`GITHUB_PERSONAL_ACCESS_TOKEN` — set in `/root/.hermes/.env`

Token needs: `repo`, `issues`, `read:user` scopes

Get PAT: https://github.com/settings/tokens → New token (classic)

## What it does
- **Repository management** — list, search, get repo info
- **Issues** — create, list, get, close, comment
- **Pull Requests** — list, get, create, merge
- **Code search** — search code across repos
- **File operations** — read files, get contents

## Usage
```python
# Via MCP tool calls (native — no skill overhead)
# Hermes routes GitHub queries to the github MCP server directly

# Example tools:
# - github_list_issues (owner, repo, state)
# - github_create_issue (owner, repo, title, body)
# - github_search_code (query)
# - github_search_repositories (query)
# - github_get_issue (owner, repo, issue_number)
```

## Notes
- Native MCP connection — cleaner than GitHub skill overhead
- PAT stored in env var, not hardcoded
- Rate limit: 5,000 requests/hour for authenticated
- Tools filtered to safe subset: create_issue, list_issues, get_issue, search_code, search_repositories
