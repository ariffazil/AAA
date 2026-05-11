---
name: pdf-text-extraction-vps
category: data-science
description: Extract text from PDFs on the arifOS VPS when standard tools aren't installed. Handles Unicode filenames and pymupdf workflow.
---

# PDF Text Extraction on VPS

## Context
On this VPS (af-forge / arifOS environment), standard PDF tools are often not pre-installed. `read_file` cannot handle binary files. Must use Python.

## Approach

### Step 1: Find the file (handle special chars in filename)
```python
import glob, os
files = glob.glob('doc_9437e23d3eda*')  # use prefix glob
for f in files:
    print(repr(f))  # check actual filename encoding
```

### Step 2: Install pymupdf if not available
```bash
pip install pymupdf -q
```

### Step 3: Extract text
```python
import fitz  # pymupdf
doc = fitz.open('/full/path/to/file.pdf')
for i, page in enumerate(doc):
    text = page.get_text()
    if text.strip():
        print(f"--- Page {i+1} ---")
        print(text)
```

### Verification: Check if file is actually a PDF
```python
with open(file_path, 'rb') as f:
    header = f.read(5)
    print(header)  # b'%PDF-1.' confirms PDF
```

## Why this works
- `pymupdf` (fitz) is more reliable than `pdfplumber` or `pdftotext` on this VPS
- Python glob avoids shell quoting issues with Unicode filenames
- `rb` mode read confirms it's a real PDF before attempting extraction

## Alternatives that failed here
- `pdftotext` CLI — not installed
- `PyPDF2` — not installed
- `pdfplumber` — not installed
- `read_file` tool — can't handle binary files
