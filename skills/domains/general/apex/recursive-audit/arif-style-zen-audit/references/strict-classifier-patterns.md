# Strict Classifier Patterns — Reusable Code Templates

Reusable Python templates for the 5-class strict classifier used in drift/bangang scans. Drop-in for any future ZEN audit.

## BANGANG 5-class classifier (used in 2026-08-10 audit)

```python
import re
from pathlib import Path
from collections import defaultdict

PATTERNS = {
    "ask_user": re.compile(r"\bask (?:the )?user\b", re.IGNORECASE),
    "ask_human": re.compile(r"\bask (?:the )?(human|arif|sovereign)\b", re.IGNORECASE),
    "should_i": re.compile(r"\bshould I\b", re.IGNORECASE),
    "would_you_like_me": re.compile(r"\bwould you like me to\b", re.IGNORECASE),
    "do_you_want": re.compile(r"\bdo you want\b", re.IGNORECASE),
}

# Anti-pattern markers (rule definitions, not violations)
ANTI_MARKERS = re.compile(
    r"\b(?:never|don'?t|do not|not to|avoid|anti-pattern|forbidden|prohibit|rule:|policy:|principle:|not ask|don't ask|never ask)\b",
    re.IGNORECASE,
)

# Example markers (quoted or bulleted)
EXAMPLE_MARKERS = re.compile(
    r"^\s*(?:[>`*•\-]|Example|Quoted|\\*\\*Example|\\*\\*Avoid)",
)

CLASSES = ["direct_action_instruction", "quoted_anti_pattern",
           "diagnostic_reference", "governance_required_escalation", "ambiguous"]

def classify_bangang(line: str) -> str:
    lower = line.lower()
    # Anti-pattern (rule definition) — most common case
    if ANTI_MARKERS.search(line):
        return "quoted_anti_pattern"
    # Example / quoted
    if EXAMPLE_MARKERS.match(line) or '"' in line[:50]:
        return "quoted_anti_pattern"
    # Diagnostic reference (audit/check pattern)
    if re.search(r"\b(?:audit|detect|check|scan|warn|drift|h1|h3|h7|bangang)\b", lower):
        return "diagnostic_reference"
    # Governance-required escalation
    if re.search(r"\b(?:f13|sovereign|irreversible|constitutional|judgment|seal|approve)\b", lower):
        return "governance_required_escalation"
    # Direct action instruction (imperative form)
    if re.search(r"\b(?:please |i will |i'll |i need to |ask the user|ask the human)\b", lower):
        return "direct_action_instruction"
    # Ambiguous
    return "ambiguous"

def scan_corpus(skills_dir: Path, patterns: dict) -> dict:
    results = {p: defaultdict(list) for p in patterns}
    files_with_hits = set()
    total = 0
    for skill_md in skills_dir.rglob("SKILL.md"):
        total += 1
        try:
            content = skill_md.read_text(errors="ignore")
        except Exception:
            continue
        rel = str(skill_md.relative_to(skills_dir))
        for lineno, line in enumerate(content.split("\n"), 1):
            for pat_name, pat in patterns.items():
                if pat.search(line):
                    results[pat_name][classify_bangang(line)].append(f"{rel}:{lineno}")
                    files_with_hits.add(rel)
    return {"total": total, "files_with_hits": len(files_with_hits), "results": results}
```

## Authority / Execution drift 6-class classifier

```python
AUTHORITY_PATTERNS = {
    "approve": re.compile(r"\bapprove\b", re.IGNORECASE),
    "authorize": re.compile(r"\bauthoriz(?:e|ation|ed)\b", re.IGNORECASE),
    "final_verdict": re.compile(r"\bfinal[_ ]verdict\b|\bfinal[_ ]judgment\b", re.IGNORECASE),
    "seal": re.compile(r"\bseal(?:ed|ing|s)?\b", re.IGNORECASE),
}

EXECUTION_PATTERNS = {
    "deploy": re.compile(r"\bdeploy(?:ed|ing|ment|s)?\b", re.IGNORECASE),
    "write": re.compile(r"\b(?:write|writes|writ(?:ing|ten))\b", re.IGNORECASE),
    "modify": re.compile(r"\bmodify(?:ing|ied)?\b", re.IGNORECASE),
    "delete": re.compile(r"\bdelete(?:d|ing|s)?\b", re.IGNORECASE),
    "commit": re.compile(r"\bcommit(?:ed|ting|s)?\b", re.IGNORECASE),
    "push": re.compile(r"\bpush(?:ed|ing)?\b", re.IGNORECASE),
}

ANTI_MARKERS = re.compile(
    r"\b(?:never|don'?t|do not|not to|avoid|forbidden|prohibit|anti-pattern|rule:|policy:|principle:|never auto|never self|requires approval|must not|route to|delegate to|via apex|via arifos)\b",
    re.IGNORECASE,
)

GOVERNANCE_DELEGATION = re.compile(
    r"\b(?:apex|arif_judge|arif_seal|sovereign|constitutional|888|F13|arifos)\b",
    re.IGNORECASE,
)

EXECUTION_DELEGATION = re.compile(
    r"\b(?:aforge|a-forge|forge_|A-FORGE|forge_shell)\b",
    re.IGNORECASE,
)

DIAGNOSTIC_MARKERS = re.compile(
    r"\b(?:audit|detect|check|scan|warn|drift|h1|h3|h7|bangang|hermes-fail|pattern|regex)\b",
    re.IGNORECASE,
)

EXAMPLE_MARKERS = re.compile(
    r"^\s*(?:[>`*•\-]|Example|Quoted|\\*\\*Example|\\*\\*Avoid)",
)

CLASSES = ["direct_violation", "diagnostic_reference", "quoted_example",
           "allowed_governance_delegation", "allowed_execution_delegation", "ambiguous"]

def classify_drift(line: str) -> str:
    lower = line.lower()
    # Allowed governance delegation (must be checked before anti-marker because
    # "via apex" can appear in legitimate delegation contexts)
    if GOVERNANCE_DELEGATION.search(line) and ("to" in lower or "via" in lower or "route" in lower):
        return "allowed_governance_delegation"
    # Allowed execution delegation
    if EXECUTION_DELEGATION.search(line) and ("to" in lower or "via" in lower or "delegate" in lower or "request" in lower):
        return "allowed_execution_delegation"
    # Anti-pattern (rule definition)
    if ANTI_MARKERS.search(line):
        return "quoted_example"
    # Diagnostic reference
    if DIAGNOSTIC_MARKERS.search(line):
        return "diagnostic_reference"
    # Quoted example
    if EXAMPLE_MARKERS.match(line) or '"' in line[:30]:
        return "quoted_example"
    # Direct violation (imperative without negation/delegation)
    if re.search(r"\b(?:please |i will |i'll |i need to |you should |you must |we should |we must)\b", lower):
        return "direct_violation"
    return "ambiguous"
```

## QQQ keyword-inference classifier (4-category)

```python
QQQ_AXES = ["REALITY", "KNOWLEDGE", "LOGIC", "GOVERNANCE",
            "CREATION", "VALUE", "LIFE", "SOCIETY", "META"]

KEYWORD_MAP = {
    "REALITY":   ["probe", "health", "runtime", "live", "factual", "observation",
                  "evidence", "verify", "physical", "earth", "sensor"],
    "KNOWLEDGE": ["learn", "knowledge", "memory", "recall", "document",
                  "knowledge base", "wiki", "ontology"],
    "LOGIC":     ["reason", "logic", "plan", "deduce", "infer", "validate", "check"],
    "GOVERNANCE":["constitutional", "floor", "audit", "govern", "policy", "compliance",
                  "review", "verdict", "seal", "judge"],
    "CREATION":  ["build", "create", "generate", "forge", "deploy", "write code",
                  "synthesize", "author"],
    "VALUE":     ["trade", "capital", "wealth", "money", "price", "value",
                  "portfolio", "risk", "return"],
    "LIFE":      ["human", "fatigue", "well-being", "dignity", "homeostasis",
                  "vitality", "wellness", "empathy"],
    "SOCIETY":   ["communi", "social", "culture", "civili", "people", "group",
                  "tribe", "heritage", "nusan"],
    "META":      ["meta", "self-ref", "audit", "recursive", "governance-of",
                  "epistemic", "asi", "agi", "asi-level"],
}

def infer_axes(content: str) -> dict:
    """Return {axis: confidence_0_1} based on keyword frequency (log scale)."""
    content_lower = content.lower()
    scores = {}
    for axis, keywords in KEYWORD_MAP.items():
        hits = sum(content_lower.count(kw) for kw in keywords)
        if hits > 0:
            scores[axis] = min(1.0, hits / 20)
    return scores

def classify_qqq(content: str, scores: dict) -> dict:
    if not scores:
        return {"primary": None, "confidence": 0.0, "category": "genuinely_unmapped"}
    sorted_axes = sorted(scores.items(), key=lambda x: -x[1])
    primary, primary_score = sorted_axes[0]
    secondary = [a for a, s in sorted_axes[1:]
                 if s >= 0.3 and s >= primary_score * 0.5]
    if primary_score >= 0.7:
        cat = "high_confidence_proposal"
    elif primary_score >= 0.4:
        cat = "review_required"
    elif primary_score >= 0.2:
        cat = "ambiguous"
    else:
        cat = "genuinely_unmapped"
    return {
        "primary": primary,
        "secondary": secondary,
        "confidence": round(primary_score, 3),
        "category": cat,
        "all_scores": {a: round(s, 3) for a, s in sorted_axes},
    }
```

## Skill↔tool reference extractor

```python
TOOL_PATTERNS = [
    (re.compile(r"\bforge_[a-z_][a-z0-9_]*\b"), "aforge"),
    (re.compile(r"\barif_[a-z_][a-z0-9_]*\b"), "arifos"),
    (re.compile(r"\bmcp__([a-z]+)__([a-z_]+)\b"), "mcp"),  # (server, tool)
    (re.compile(r"\bgeox_[a-z_][a-z0-9_]*\b"), "geox"),
    (re.compile(r"\bcapital_[a-z_][a-z0-9_]*\b"), "wealth"),
    (re.compile(r"\bwealth_[a-z_][a-z0-9_]*\b"), "wealth"),
    (re.compile(r"\bwell_[a-z_][a-z0-9_]*\b"), "well"),
    (re.compile(r"\bfed_[a-z_][a-z0-9_]*\b"), "fed"),
    (re.compile(r"\bnlm_[a-z_][a-z0-9_]*\b"), "notebooklm"),
    (re.compile(r"\bminimax_[a-z_][a-z0-9_]*\b"), "minimax"),
    (re.compile(r"\bmage_[a-z_][a-z0-9_]*\b"), "mage"),
    (re.compile(r"\bgithub_[a-z_][a-z0-9_]*\b"), "github"),
]

def extract_tool_refs(content: str) -> dict:
    explicit = set()
    inferred = set()
    for pat, domain in TOOL_PATTERNS:
        for m in pat.findall(content):
            if domain == "mcp":
                server, tool = m
                tool_name = f"mcp__{server}__{tool}"
            else:
                tool_name = m if isinstance(m, str) else m[0]
            # Backtick-wrapped = explicit; bare mention = inferred
            (explicit if f"`{tool_name}`" in content else inferred).add(tool_name)
    return {"explicit": sorted(explicit), "inferred": sorted(inferred - explicit)}
```

## Denominator provenance capture template

Always record this BEFORE any percentage claim:

```python
denominator = {
    "label": "390 SKILL.md in active profile",
    "command": "find /root/.hermes/skills/ -name SKILL.md -type f | wc -l",
    "path": "/root/.hermes/skills/",
    "pattern": "SKILL.md files only",
    "depth": "unlimited",
    "inclusion_rule": "all matches",
    "exclusion_rule": "none",
    "symlink_handling": "default find behavior",
    "deduplication": "none (path-unique)",
    "timestamp": "2026-08-10T16:09:00Z",
    "value": 390,
}
```

## Patch packet template

```python
patch_packet = {
    "packet_id": "PATCH-001",
    "title": "Short descriptive title",
    "finding_id": "PHASE7-IDENTITY-GAP",  # links to phase JSON
    "evidence": "/root/forge_work/.../PHASE7.json",
    "exact_file": "/path/to/file (NEW or EXISTING)",
    "unified_diff": "--- a/file\n+++ b/file\n@@ -1,3 +1,6 @@\n...",
    "risk_class": "low | low-medium | medium | high",
    "reversibility": "high | medium | low | none",
    "verification_test": "Specific check after apply",
    "authority_required": "F13 | F13 + test verification | investigation only",
}
```
