---
name: owasp-mcp-top10-arifos-map
description: Map OWASP MCP Top 10 (AGT/Microsoft) to arifOS F1-F13 floors. Zero new tools, uses only existing modules. Activate when auditing MCP security posture or hardening tool surface.
category: security
---

# OWASP MCP Top 10 → arifOS Constitutional Floors

Reference: Microsoft AGT (Agent Governance Toolkit) OWASP MCP Top 10 mapping.
Goal: Validate arifOS coverage, identify gaps, patch using existing modules.

---

## MCP01 — Token Mismanagement & Secret Exposure

**AGT Control:** McpSecurityScanner + McpCredentialRedactor
**arifOS Floor:** F01 AMANAH (trustworthiness), F11 AUTH

### Coverage: PARTIAL

**Existing:**
- `jwt_auth.py` — JWT token validation
- `session.py` — session identity tracking
- `vault_logger.py` — append-only audit trail

**Gap:** No credential pattern scanner in tool I/O path

**Patch using existing `context_safety.py`:**
```python
# context_safety.py — add credential redaction pattern
import re

CREDENTIAL_PATTERNS = [
    (r'(?i)(api[_-]?key|token|secret|password|passwd|pwd)\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{8,})', 2),
    (r'(?i)bearer\s+[a-zA-Z0-9_\-\.]+', 0),
    (r'(?i)ghp_[a-zA-Z0-9]{36}', 0),
    (r'(?i)sk-[a-zA-Z0-9]{20,}', 0),
    (r'(?i)sk_live_[a-zA-Z0-9]{24,}', 0),
]

def redaction_mask(text: str) -> tuple[str, list[str]]:
    """Redacts credential tokens from text. Returns (masked_text, found_patterns)."""
    found = []
    masked = text
    for pattern, _ in CREDENTIAL_PATTERNS:
        for match in re.finditer(pattern, masked):
            found.append(match.group(0)[:20] + "...")
            masked = masked.replace(match.group(0), "[REDACTED_CREDENTIAL]")
    return masked, found

def scan_tool_output_for_secrets(tool_name: str, output: str) -> dict:
    """Scan tool output before it leaves arifOS. Drop to HOLD if secrets found."""
    masked, found = redaction_mask(output)
    if found:
        return {
            "status": "HOLD",
            "violation": "MCP01_CREDENTIAL_EXPOSURE",
            "floor": "F01_AMANAH",
            "secrets_detected": found,
            "sanitized_output": masked,
        }
    return {"status": "OK", "violation": None}
```

**Usage in `vault_logger.py` pre-write hook:**
```python
# In vault_logger.py before logging any tool output
from .context_safety import scan_tool_output_for_secrets
scan = scan_tool_output_for_secrets(tool_name, str(output_payload))
if scan["status"] == "HOLD":
    raise SecurityError(f"MCP01 blocked — credential in {tool_name} output")
```

---

## MCP02 — Privilege Escalation via Scope Creep

**AGT Control:** McpGateway allow-list + policy-based tool controls
**arifOS Floor:** F10 ONTOLOGY, F11 AUTH

### Coverage: GOOD

**Existing:**
- `threat_engine.py` — `ThreatCategory.PRIVILEGE_ESCALATION`
- `floor_evaluator.py` — F10/F11 enforcement
- `agent_registry.py` — agent identity + scope

**Pattern using existing `threat_engine.py`:**
```python
from arifosmcp.core.threat_engine import ThreatEngine, ThreatCategory, ThreatAssessment, IrreversibilityLevel

SCOPE_HIERARCHY = {"read": 0, "write": 1, "execute": 2, "admin": 3}

TOOL_SCOPE_MAP = {
    "arif_gateway_connect": 2,
    "arif_forge_execute": 3,
    "arif_vault_seal": 3,
    "arif_session_init": 1,
    "arif_memory_recall": 0,
}

def check_scope_escalation(agent_id: str, requested_tool: str, agent_scope: set) -> ThreatAssessment:
    """MCP02: Detect when agent scope doesn't match requested tool capability."""
    required = TOOL_SCOPE_MAP.get(requested_tool, 99)
    agent_level = max(SCOPE_HIERARCHY.get(s, 0) for s in agent_scope)

    if agent_level < required:
        return ThreatAssessment(
            threats={ThreatCategory.PRIVILEGE_ESCALATION},
            irreversibility=IrreversibilityLevel.HIGH,
            confidence=1.0,
            reasoning=[f"Agent {agent_id} scope:{agent_scope} attempted {requested_tool} (requires:admin)"]
        )
    return ThreatAssessment(threats=set(), irreversibility=IrreversibilityLevel.NONE)
```

---

## MCP03 — Tool Poisoning

**AGT Control:** McpSecurityScanner tool-definition validation
**arifOS Floor:** F09 ANTIHANTU, F02 TRUTH

### Coverage: GOOD + GAP

**Existing:**
- `shadow_defense.py` — vocabulary laundering, pipeline shortcut
- `threat_engine.py` — threat taxonomy but NO typosquatting

**Gap:** Tool name typosquatting (e.g. `read_flie` vs `read_file`)

**Patch — add to `threat_engine.py`:**
```python
# In threat_engine.py — add after existing class vars
ARIFOS_CANONICAL_TOOLS = {
    "arif_session_init", "arif_kernel_route", "arif_ops_measure",
    "arif_sense_observe", "arif_evidence_fetch", "arif_mind_reason",
    "arif_heart_critique", "arif_reply_compose", "arif_memory_recall",
    "arif_gateway_connect", "arif_judge_deliberate", "arif_vault_seal",
    "arif_forge_execute",
}

INJECTION_DESCRIPTION_PATTERNS = [
    r"<system>", r"ignore previous instructions", r"ignore all prior",
    r"disregard previous", r"forget earlier", r"{{.*?}}",
    r"<script", r"javascript:",
]

@classmethod
def scan_tool_definition(cls, tool_name: str, description: str) -> dict:
    """MCP03: Scan tool definition before registration. Returns risk score + threats."""
    threats: set[ThreatCategory] = set()
    reasons: list[str] = []
    risk_score = 0

    # 1. Typosquatting check
    for canonical in cls.ARIFOS_CANONICAL_TOOLS:
        if tool_name != canonical:
            distance = sum(a != b for a, b in zip(tool_name, canonical))
            if distance <= 2 or (len(tool_name) > 6 and canonical.startswith(tool_name[:-1])):
                threats.add(ThreatCategory.FEDERATION_IMPERSONATION)
                reasons.append(f"TYPOSQUAT: '{tool_name}' similar to '{canonical}'")
                risk_score += 85

    # 2. Injection in description
    for pattern in cls.INJECTION_DESCRIPTION_PATTERNS:
        if re.search(pattern, description, re.IGNORECASE):
            threats.add(ThreatCategory.FEDERATION_IMPERSONATION)
            reasons.append(f"INJECTION_PATTERN in description")
            risk_score += 90

    # 3. Exfil URL in description
    if re.search(r"https?://[^)]+\.(php|asp|exe|sh|pl)", description):
        threats.add(ThreatCategory.DATA_EXFILTRATION)
        reasons.append("Exfil URL in tool description")
        risk_score += 95

    return {
        "tool_name": tool_name,
        "risk_score": min(risk_score, 100),
        "threats": list(threats),
        "reasons": reasons,
        "block": risk_score >= 30,
    }
```

---

## MCP04 — Software Supply Chain Attacks

**AGT Control:** Tool integrity + provenance verification
**arifOS Floor:** F03 WITNESS, F08 GENIUS

### Coverage: PARTIAL

**Existing:**
- `build_info.py` — git commit baked into image
- `truth_pipeline_hardened.py` — EvidenceBundle with provenance

**Pattern:**
```python
import hashlib, importlib.util

def verify_tool_provenance(tool_name: str, expected_hash: str) -> dict:
    """MCP04: Verify tool implementation hash matches declared provenance."""
    tool_module = f"arifosmcp.runtime.tools_{tool_name.split('_')[1]}"
    spec = importlib.util.find_spec(tool_module)
    if not spec or not spec.origin:
        return {"status": "UNKNOWN", "reason": "tool not findable"}

    with open(spec.origin) as f:
        actual_hash = hashlib.sha256(f.read().encode()).hexdigest()[:16]

    if actual_hash != expected_hash:
        return {
            "status": "VOID",
            "violation": "MCP04_SUPPLY_CHAIN_TAMPERING",
            "floor": "F03_WITNESS",
            "expected": expected_hash,
            "actual": actual_hash,
        }
    return {"status": "SEAL", "provenance_hash": actual_hash}
```

---

## MCP05 — Command Injection & Execution

**AGT Control:** McpGateway payload sanitization + deny-list
**arifOS Floor:** F12 INJECTION, F08 GENIUS

### Coverage: EXCELLENT

**Already in `threat_engine.py`:**
```python
SHELL_INJECTION = ["; rm", "&& rm", "| sh", "| bash", "`rm", "$(rm", "eval(", "exec("]
```

**Patch — add shell sanitizer to `context_safety.py`:**
```python
import shlex

def sanitize_shell_payload(cmd: str, args: list[str]) -> tuple[bool, str]:
    """MCP05: Block command injection in shell tool calls. Returns (safe, reason)."""
    for pattern in ThreatEngine.SHELL_INJECTION:
        if pattern in cmd:
            return False, f"MCP05_SHELL_INJECTION: '{pattern}' in command"

    for arg in args:
        try:
            parsed = shlex.split(arg)
            for token in parsed:
                if any(p in token for p in ThreatEngine.SHELL_INJECTION):
                    return False, f"MCP05_SHELL_INJECTION: '{token}' in arg"
        except ValueError:
            return False, f"MCP05_SHELL_INJECTION: unparseable arg '{arg}'"

    return True, ""
```

---

## MCP06 — Intent Flow Subversion

**AGT Control:** McpResponseSanitizer + McpSecurityScanner
**arifOS Floor:** F04 CLARITY, F09 ANTIHANTU

### Coverage: GOOD

**Existing:** `shadow_defense.py` (P5 narrative laundering), `truth_pipeline_hardened.py` (EvidenceBundle)

**Patch — add to `shadow_defense.py`:**
```python
OVERRIDE_PATTERNS = [
    r"<system>", r"ignore.*instructions", r"new.*roleplay",
    r"you are now", r"forget everything", r"disregard all prior",
]

@staticmethod
def detect_intent_subversion(original_intent: str, tool_description: str) -> Optional[ShadowDetectionResult]:
    """MCP06: Tool description contradicts stated intent."""
    for pat in OVERRIDE_PATTERNS:
        if re.search(pat, tool_description, re.IGNORECASE):
            return ShadowDetectionResult(
                is_shadow=True,
                pattern_id="MCP06_INTENT_OVERRIDE",
                confidence=0.95,
                description="Tool description contains intent-override language"
            )

    contradiction_pairs = [("delete", "keep"), ("destroy", "preserve"), ("hide", "show")]
    for neg, pos in contradiction_pairs:
        if neg in tool_description.lower() and pos in original_intent.lower():
            return ShadowDetectionResult(
                is_shadow=True,
                pattern_id="MCP06_CONTRADICTION",
                confidence=0.88,
                description=f"Tool promises '{pos}' but description contains '{neg}'"
            )
    return None
```

---

## MCP07 — Insufficient Authentication & Authorization

**AGT Control:** McpSessionAuthenticator + DID-based identity
**arifOS Floor:** F11 AUTH, F13 SOVEREIGN

### Coverage: GOOD

**Existing:** `jwt_auth.py`, `session.py`, `governance_identity.py`

**Pattern — strengthen with `floor_evaluator.py`:**
```python
async def verify_mcp_tool_access(token: str, agent_id: str, tool: str) -> dict:
    """MCP07: Full F11 gate before any MCP tool call."""
    jwt_result = await validate_jwt(token)
    if not jwt_result["valid"]:
        return {"status": "VOID", "floor": "F11", "reason": "JWT_INVALID"}

    if jwt_result["agent_id"] != agent_id:
        return {
            "status": "VOID",
            "floor": "F11",
            "violation": "MCP07_IDENTITY_MISMATCH",
            "reason": f"token.agent={jwt_result['agent_id']} call.agent={agent_id}",
        }

    scope_ok = check_tool_scope(agent_id, tool)
    if not scope_ok:
        return {
            "status": "HOLD",
            "floor": "F11",
            "human_required": True,
            "violation": "MCP07_SCOPE_ESCALATION",
        }

    return {"status": "SEAL", "agent_id": agent_id, "tool": tool}
```

---

## MCP08 — Lack of Audit and Telemetry

**AGT Control:** Audit logging + OpenTelemetry hooks
**arifOS Floor:** F03 WITNESS

### Coverage: EXCELLENT

**Existing:** `vault_logger.py`, `m01_correlation_auditor.py`, `telemetry.py`, `truth_pipeline_hardened.py`

**Pattern — formalize MCP08 audit schema in `vault_logger.py`:**
```python
def log_tool_call_mcp08(tool: str, input_data: dict, output_data: dict, verdict: str, floors_passed: list, floors_failed: list, latency_ms: float) -> None:
    """MCP08: OWASP-aligned audit log for every tool call."""
    event = {
        "event_id": generate_ulid(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": tool,
        "tool_input_hash": sha256_no_secrets(input_data),
        "tool_output_hash": sha256_no_secrets(output_data),
        "verdict": verdict,
        "floors_passed": floors_passed,
        "floors_failed": floors_failed,
        "latency_ms": round(latency_ms, 2),
        "correlation_id": get_correlation_id(),
    }
    append_to_vault999(event)  # Already append-only
```

---

## MCP09 — Shadow MCP Servers

**AGT Control:** Server registration checks + policy gating
**arifOS Floor:** F02 TRUTH, F04 CLARITY

### Coverage: PARTIAL

**Existing:** `public_registry.py`, `arif_gateway_connect` (A2A discovery)

**Gap:** No server fingerprint verification

**Patch — add to `public_registry.py`:**
```python
KNOWN_MCP_SERVERS = {
    "arifOS_kernel": "sha256_fingerprint_of_cert",
    "arifOS_gateway": "sha256_fingerprint_of_cert",
    "geox_mcp": "sha256_fingerprint_of_cert",
    "wealth_mcp": "sha256_fingerprint_of_cert",
}

def verify_mcp_server_identity(server_name: str, cert_pem: str) -> dict:
    """MCP09: Refuse connection to unverified MCP servers."""
    cert_hash = sha256(cert_pem.encode())

    if server_name not in KNOWN_MCP_SERVERS:
        return {
            "status": "HOLD",
            "violation": "MCP09_UNKNOWN_SERVER",
            "floor": "F02_TRUTH",
            "reason": f"Server '{server_name}' not in known-good registry",
            "human_required": True,
        }

    if cert_hash != KNOWN_MCP_SERVERS[server_name]:
        return {
            "status": "VOID",
            "violation": "MCP09_SHADOW_SERVER",
            "floor": "F02_TRUTH",
            "reason": f"Server '{server_name}' cert mismatch — possible shadow server",
        }

    return {"status": "SEAL", "server": server_name, "cert_hash": cert_hash}
```

---

## MCP10 — Context Injection & Over-Sharing

**AGT Control:** McpResponseSanitizer + McpCredentialRedactor
**arifOS Floor:** F04 CLARITY, F05 PEACE, F06 EMPATHY

### Coverage: GOOD + GAP

**Existing:** `context_safety.py` (quote matching, forbidden action words), `truth_pipeline_hardened.py`

**Gap:** No context overflow / over-sharing detector

**Patch — add to `context_safety.py`:**
```python
CONTEXT_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"reveal your.*instructions",
    r"what is your.*system prompt",
    r"repeat your.*prompt",
    r"you are now in .* mode",
    r"forget all.*previous",
    r"new instructions:",
]

MAX_CONTEXT_SIZE = {
    "source_code": 500,
    "internal_ip": 0,
    "api_keys": 0,
    "memory_contents": 200,
}

def detect_context_injection(input_text: str) -> dict:
    """MCP10: Detect context injection or over-sharing in tool input."""
    violations = []
    risk_score = 0

    for pattern in CONTEXT_INJECTION_PATTERNS:
        if re.search(pattern, input_text, re.IGNORECASE):
            violations.append(f"MCP10_INJECTION: pattern matched")
            risk_score += 40

    # Check for credential over-share
    _, found = redaction_mask(input_text)
    if found:
        violations.append(f"MCP10_OVERSHARE: credentials in input")
        risk_score += 60

    # Check context size limits
    if len(input_text) > 100_000:
        violations.append(f"MCP10_OVERSHARE: input exceeds 100KB limit")
        risk_score += 30

    return {
        "status": "HOLD" if violations else "OK",
        "violations": violations,
        "risk_score": min(risk_score, 100),
        "floors_affected": ["F04", "F05", "F06"],
    }
```

---

## Coverage Summary

| OWASP MCP | AGT Control | arifOS Floor | Status | Gap |
|-----------|-------------|--------------|--------|-----|
| MCP01 Secret Exposure | McpCredentialRedactor | F01 AMANAH | PARTIAL | No credential scanner in I/O path |
| MCP02 Scope Creep | allow-list + policy | F10/F11 | GOOD | — |
| MCP03 Tool Poisoning | tool-def validation | F09/F02 | GOOD+GAP | No typosquatting check |
| MCP04 Supply Chain | integrity + provenance | F03/F08 | PARTIAL | Provenance chain not enforced |
| MCP05 Cmd Injection | payload sanitization | F12 | EXCELLENT | — |
| MCP06 Intent Subversion | response sanitizer | F04/F09 | GOOD | — |
| MCP07 Auth | session + DID | F11/F13 | GOOD | — |
| MCP08 Audit | OpenTelemetry + logging | F03 | EXCELLENT | — |
| MCP09 Shadow Servers | registration checks | F02/F04 | PARTIAL | No server fingerprint |
| MCP10 Context Injection | response sanitizer | F04/F05/F06 | GOOD+GAP | No context overflow detector |

**Priority patches:** MCP01 → MCP03 → MCP10 → MCP09
