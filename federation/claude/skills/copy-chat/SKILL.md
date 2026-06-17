---
name: copy-chat
description: Export conversation to clipboard or file — supports full, prompts-only, responses-only, and code-blocks-only formats
user-invocable: true
---

# Copy Chat

Export the current conversation with format filtering.

## Invocation

- `/copy-chat` — Ask user which format, then export
- `/copy-chat full` — Full conversation to clipboard
- `/copy-chat prompts` — User messages only
- `/copy-chat responses` — Claude outputs only
- `/copy-chat code` — Code blocks only
- `/copy-chat file <name>.md` — Save to file instead of clipboard

## Execution Steps

1. **Parse argument** (if provided). If none, ask user with AskUserQuestion:
   - Full (prompts + responses)
   - Prompts Only
   - Responses Only
   - Code Blocks Only

2. **Build export content** based on format:
   - `full`: Reconstruct conversation as markdown with `## User` / `## Claude` headers
   - `prompts`: Extract only user messages
   - `responses`: Extract only Claude messages
   - `code`: Extract fenced code blocks from Claude responses

3. **Export**:
   - If `file <name>` argument: Write to the specified file path
   - Otherwise: Use `/export` to copy full conversation to clipboard
   - Confirm to user what was exported and where

## Output Format

```markdown
# Chat Export — [DATE]
---
[formatted content based on selected mode]
---
*Exported: [timestamp]*
```
