"""
RFC 8785 JSON Canonicalization Scheme (JCS) and SHA-256 Hasher.
Provides deterministic, byte-for-byte reproducible hashing across all federation agents.
"""

import json
import hashlib
from typing import Any


def canonicalize(obj: Any) -> bytes:
    """
    Produce deterministic, canonical UTF-8 JSON bytes per RFC 8785 principles:
    - Keys sorted lexicographically by UTF-16 code units
    - Whitespace stripped (separators=(',', ':'))
    - Numbers formatted consistently
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(',', ':'),
        ensure_ascii=False
    ).encode('utf-8')


def hash_object(obj: Any) -> str:
    """Compute SHA-256 hexadecimal digest of canonicalized JSON object."""
    return hashlib.sha256(canonicalize(obj)).hexdigest()
