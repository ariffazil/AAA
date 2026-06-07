#!/usr/bin/env python3
"""
Prompt Loader — Loads the canonical prompt for each organ at session start.

Used by the bot (e.g., /root/.openclaw/workspace/bots/opencode-bot/bot.py)
to load organ-specific prompts from /root/AAA/agents/prompts/.

Anti-cheat: if a prompt file is missing, the loader raises FileNotFoundError.
The bot MUST HOLD, not fall back to a hardcoded prompt. This is a F1 AMANAH
violation: the system cannot silently substitute a prompt the sovereign
has not approved.
"""

import hashlib
import sys
from pathlib import Path
from typing import Dict, Optional

PROMPTS_DIR = Path("/root/AAA/agents/prompts")

VALID_ORGANS = ("LIBRA", "HERMES", "CLAW", "FORGE")


def file_hash(path: Path) -> str:
    """First 16 chars of SHA-256 of file contents."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def load_prompt(organ: str) -> Dict[str, str]:
    """Load the current prompt file for an organ.

    Returns: {"content": str, "hash": str, "path": str, "organ": str}

    Raises:
        ValueError: if organ is not in VALID_ORGANS.
        FileNotFoundError: if the prompt file does not exist.
            Caller (the bot) MUST HOLD, not fallback.
    """
    if organ not in VALID_ORGANS:
        raise ValueError(
            f"Unknown organ: {organ!r}. "
            f"Valid organs: {VALID_ORGANS}. "
            f"This is a F11 AUTH violation — refusing to load."
        )

    path = PROMPTS_DIR / f"{organ}.md"
    if not path.exists():
        raise FileNotFoundError(
            f"Prompt file missing for {organ}: {path}. "
            f"Bot MUST HOLD, not fall back to hardcoded prompt. "
            f"This is a F1 AMANAH violation."
        )

    content = path.read_text(encoding="utf-8")
    h = file_hash(path)
    return {
        "organ": organ,
        "content": content,
        "hash": h,
        "path": str(path),
    }


def load_all_prompts() -> Dict[str, Dict[str, str]]:
    """Load all four organ prompts. Raises FileNotFoundError on any missing."""
    return {organ: load_prompt(organ) for organ in VALID_ORGANS}


def detect_prompt_change(prev_hash: Optional[str], organ: str) -> bool:
    """Returns True if the current prompt hash differs from prev_hash.
    Used by the bot to detect a SEALed prompt mutation and reload."""
    current = load_prompt(organ)["hash"]
    if prev_hash is None:
        return True
    return current != prev_hash


if __name__ == "__main__":
    # CLI mode: load a prompt and print its metadata
    organ = sys.argv[1] if len(sys.argv) > 1 else "LIBRA"
    try:
        result = load_prompt(organ)
        print(f"organ:    {result['organ']}")
        print(f"path:     {result['path']}")
        print(f"hash:     {result['hash']}")
        print(f"length:   {len(result['content'])} chars")
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)
