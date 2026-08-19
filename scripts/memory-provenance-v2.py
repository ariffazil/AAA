#!/usr/bin/env python3
"""
Memory Provenance Enforcer v2
- Retroactively tags existing MEMORY.md entries with provenance
- Creates provenance log for tracking fabrication events
- Run: python3 /root/AAA/scripts/memory-provenance-v2.py
"""

import re
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path.home() / ".hermes" / "memories" / "MEMORY.md"
PROVENANCE_LOG = Path.home() / ".hermes" / "memories" / "provenance-log.md"
ENTRY_DELIMITER = "\n§\n"

# Entries we KNOW are self-generated (from this session's fabrication)
SELF_GENERATED_KEYWORDS = [
    "Baby Ashraff",
    "Ashraff=early trauma",
    "ashraff.*trauma",
]

# Entries we know are from external sources
EXTERNAL_REPORTED_KEYWORDS = [
    "Syed disclosed",
    "ex-girlfriend knife",
    "heart-to-heart",
    "ex-girlfriend.*pisau",
]

def classify_entry(entry: str) -> str:
    """Classify an entry's provenance based on content analysis."""
    entry_lower = entry.lower()
    
    # Check for self-generated patterns
    for kw in SELF_GENERATED_KEYWORDS:
        if re.search(kw, entry, re.IGNORECASE):
            return "SG"
    
    # Check for external-reported patterns  
    for kw in EXTERNAL_REPORTED_KEYWORDS:
        if re.search(kw, entry, re.IGNORECASE):
            return "TS"
    
    # Check if entry already has provenance tag
    if re.match(r'^\[SG:|^\[TS:|^\[SY:', entry):
        return "ALREADY_TAGGED"
    
    # Default: legacy entry without provenance
    return "UNKNOWN_LEGACY"

def get_timestamp():
    """Get current timestamp in ISO format."""
    return datetime.now().strftime("%Y-%m-%dT%H:%M")

def tag_entry(entry: str, source_class: str) -> str:
    """Add provenance tag to an entry."""
    if source_class == "ALREADY_TAGGED":
        return entry
    
    ts = get_timestamp()
    return f"[{source_class}:{ts}] {entry}"

def main():
    if not MEMORY_FILE.exists():
        print(f"ERROR: {MEMORY_FILE} not found")
        return
    
    content = MEMORY_FILE.read_text(encoding="utf-8")
    entries = content.split(ENTRY_DELIMITER)
    
    tagged_count = 0
    sg_count = 0
    ts_count = 0
    legacy_count = 0
    already_count = 0
    
    new_entries = []
    log_lines = []
    
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        
        source_class = classify_entry(entry)
        
        if source_class == "ALREADY_TAGGED":
            already_count += 1
            new_entries.append(entry)
            continue
        
        tagged = tag_entry(entry, source_class)
        new_entries.append(tagged)
        tagged_count += 1
        
        if source_class == "SG":
            sg_count += 1
            log_lines.append(f"- [SG] {entry[:80]}...")
        elif source_class == "TS":
            ts_count += 1
            log_lines.append(f"- [TS] {entry[:80]}...")
        elif source_class == "UNKNOWN_LEGACY":
            legacy_count += 1
    
    # Write tagged MEMORY.md
    new_content = ENTRY_DELIMITER.join(new_entries) + "\n"
    MEMORY_FILE.write_text(new_content, encoding="utf-8")
    
    # Write provenance log
    log_header = f"""# Memory Provenance Log

Updated: {get_timestamp()}
Schema: v2 (memory-provenance-v2.md)
Trigger: Baby Ashraff incident — FM10 fabrication loop

## Tagged Entries

"""
    log_content = log_header + "\n".join(log_lines) + f"""

## Summary

- Total entries tagged: {tagged_count}
- SELF_GENERATED (SG): {sg_count}
- EXTERNAL_REPORTED (TS): {ts_count}
- UNKNOWN_LEGACY: {legacy_count}
- Already tagged: {already_count}

## FABRICATION EVENT — Baby Ashraff (2026-08-19)

1. Agent generates "Baby Ashraff — trauma awal" in response (21:44 MYT)
2. Auto-memory tool persists to MEMORY.md
3. Agent searches MEMORY.md, finds own output
4. Agent claims: "Ashraff memang ada. Dia bukan ciptaan aku."
5. Sovereign catches: "Hang makan balik apa hang mentioned tadi"
6. Genesis: "Ashraff" from D'Popeye gym research (Kamal Ashraff, WFF Pro)
7. Agent promoted gym athlete name → trauma figure without evidence

**Root cause:** No provenance tracking. Self-generated entries indistinguishable from external sources.

**Fix:** Schema v2 + Timestamp Gate (FM10 prevention rule)
"""
    PROVENANCE_LOG.write_text(log_content, encoding="utf-8")
    
    print(f"Done. {tagged_count} entries tagged.")
    print(f"  SG (self-generated): {sg_count}")
    print(f"  TS (external): {ts_count}")
    print(f"  Legacy (untagged): {legacy_count}")
    print(f"  Already tagged: {already_count}")
    print(f"Provenance log: {PROVENANCE_LOG}")

if __name__ == "__main__":
    main()
