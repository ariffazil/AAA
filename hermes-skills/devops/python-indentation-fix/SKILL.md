---
name: python-indentation-fix
description: Fix Python indentation-only bugs when the patch tool can't change whitespace levels
triggers:
  - SyntaxError expected except or finally block
  - Python indentation mismatch fix
  - patch tool succeeded but syntax still broken
---

# Python Indentation-Only Fix — When patch Tool Fails

## Problem
The `patch` tool replaces **text content** but cannot change **indentation levels**. If you need to change only the leading whitespace of lines (e.g., 4 spaces → 8 spaces), patch succeeds but syntax remains broken.

## Symptoms
```
SyntaxError: expected 'except' or 'finally' block
```
Python parses the function but sees `verdict` and `return` at wrong indentation — inside/outside the wrong block.

## Solution
Use `execute_code` with Python list manipulation:

```python
with open('/path/to/file.py') as f:
    lines = f.readlines()

# Fix lines 92-107: indent from 4 spaces to 8 spaces
fixed = []
for i, line in enumerate(lines):
    lineno = i + 1
    if 92 <= lineno <= 107:
        if line.startswith('    '):  # 4 spaces
            fixed.append('        ' + line[4:])  # → 8 spaces
        else:
            fixed.append(line)
    else:
        fixed.append(line)

with open('/path/to/file.py', 'w') as f:
    f.writelines(fixed)
```

## Why This Works
Direct line-by-line manipulation changes actual whitespace bytes. The patch tool does regex-style string replacement, which can't distinguish 4-space from 8-space indent as structurally different.

## Verification
Always run after fix:
```bash
python3 -m py_compile /path/to/file.py && echo "SYNTAX_OK"
```

## When to Use
- Indentation-only changes (no text content change)
- Nested `try/except/if` blocks with wrong dedent level
- Converting between tab and space indentation
- Fixing auto-formatter mistakes that break structure
