---
name: nano-pdf
id: nano-pdf
description: "Edit text in existing PDFs via natural-language prompts."
version: 1.0.0
owner: AAA
risk_tier: high
autonomy_tier: T2
floor_scope: [F1, F2, F4, F11, F12]
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PDF, Documents, Editing, NLP, Productivity]
    homepage: https://pypi.org/project/nano-pdf/
    related_skills: [pdf, ocr-and-documents]
capability_tier: fed-long-context
ecology_state: WARM
---

> [!CAUTION]
> **GOVERNANCE & AUTHORITY BOUNDARY:**
> - Package installation (`uv pip install nano-pdf` / `pip install`) requires prior operator approval; NEVER install unvetted external binaries autonomously.
> - LLM API key handling must adhere to Floor F11 (no plaintext secrets written to disk or logs).
> - PDF mutations must preserve an unmutated backup before modification.

# nano-pdf

Edit PDFs using natural-language instructions. Point it at a page and describe what to change. For structural PDF work (merge, split, forms, watermarks, creation), see the `pdf` skill; for text extraction from scans, see `ocr-and-documents`.

## Prerequisites

```bash
# Install with uv (recommended — already available in Hermes)
uv pip install nano-pdf

# Or with pip
pip install nano-pdf
```

## Usage

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

## Examples

```bash
# Change a title on page 1
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"

# Update a date on a specific page
nano-pdf edit report.pdf 3 "Update the date from January to February 2026"

# Fix content
nano-pdf edit contract.pdf 2 "Change the client name from 'Acme Corp' to 'Acme Industries'"
```

## Notes

- Page numbers may be 0-based or 1-based depending on version — if the edit hits the wrong page, retry with ±1
- Always verify the output PDF after editing (use `read_file` to check file size, or open it)
- The tool uses an LLM under the hood — requires an API key (check `nano-pdf --help` for config)
- Works well for text changes; complex layout modifications may need a different approach
