---
name: subagent-execution-verify
category: workflow-automation
description: Diagnose when MiniMax subagents simulate tool calls vs actually executing them
---

# Subagent Execution Verification

## Trigger
When using `delegate_task` with MiniMax M2 subagents and the returned `summary` only describes intended actions without actual execution results (no `api_calls`, `tool_trace`, or concrete data in output).

## Problem
MiniMax subagents in `--yolo --print --no-thinking` mode appear to simulate tool outputs — returning a description of what they *would* do rather than actually executing. The `summary` field shows `"api_calls": 1, "duration_seconds": X` but no real search results, no raw JSON, no concrete data.

## Diagnosis Steps

1. **Check the summary carefully** — if it starts with "I'll search for X" or "Let me run several searches" without returning actual data, it's a simulation
2. **Look for `tool_trace` in response** — if empty or absent, no tools were actually called
3. **Look at `api_calls` count** — if 1 but summary is just intent, it's likely a no-op
4. **Red flag phrases**: "Let me run several searches in parallel", "I'll search for information", any summary that describes a plan rather than results

## Fix
**Do the searches yourself directly via terminal** — use `curl` + Python regex to scrape results, or use `web_search` directly. Do not rely on subagent to find contact info, URLs, or structured data.

## Verified Direct-Search Approach

For finding social media handles / contact info:

```bash
# Check if Twitter handle exists via nitter (Twitter without login)
curl -s "https://nitter.net/HANDLE" -o /dev/null -w "%{http_code}"
# 200 = exists, 000 = doesn't resolve, 404 = not found

# Scrape nitter for bio/contact info
curl -s "https://nitter.net/HANDLE" | python3 -c "
import sys, re
html = sys.stdin.read()
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)
print(text[:2000])
"

# Google search for email addresses (limited by Google blocking)
curl -sL "https://www.google.com/search?q=NAME+email+contact" | python3 -c "
import sys, re
html = sys.stdin.read()
emails = re.findall(r'[\w.+%+-]+@[\w-]+\.[\w.-]+', html)
print(list(set(emails)))
"
```

## Prevention
- For web research tasks (contact finding, claim verification, data extraction): execute directly yourself
- Use subagents only for tasks that produce verifiable code/output that can be checked
- If subagent summary looks like a plan rather than results, discard and do manually
- Subagents work well for: code writing, file transformation, multi-step execution with verifiable outputs
- Subagents fail reliably for: web search without a working tool, finding contact info, browsing

## Learned From
Session: SEARAH × PETROS investigation, 2026-05-07. Subagent described 4 parallel web searches but returned zero actual search results. All 7 contact entries had to be rebuilt manually.
