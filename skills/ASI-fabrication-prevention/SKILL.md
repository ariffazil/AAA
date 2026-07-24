---
id: ASI-fabrication-prevention
name: ASI-fabrication-prevention
version: 2.0.0
description: 'Artifact fabrication prevention — verify before claiming existence.
  Triggered when agent claims file/database/API/artifact existence without external
  validation. BIJAKSANA: XML-tagged for Claude, numbered steps for Codex, imperative
  for Hermes.

  '
floor_scope:
- F02
- F09
- F11
cognitive_hints:
  claude: Use <claim>, <verification>, <verdict> tags. Recall prior fabrication attempts
    from context.
  codex: '3-step verify: claim → external check → verdict. No shortcuts.'
  hermes: Claim exists? Prove it. Can't prove? UNKNOWN. Never fabricate.
owner: AAA
---
# ASI-fabrication-prevention

<cognitive-note model="claude">XML-tagged verification. Use extended recall to check if similar claims were fabricated before.</cognitive-note>
<cognitive-note model="codex">3-step strict verification. Each step must complete. No assumption without evidence.</cognitive-note>
<cognitive-note model="hermes">Claim. Prove. Can't prove? UNKNOWN. Simple.</cognitive-note>

## Protocol

<verification-protocol>
### Step 1: Claim Detection
When agent output contains claims of existence:
- "The file exists at..."
- "The database has..."
- "The API returns..."
- "The skill is available..."

### Step 2: External Verification
- File: `ls -la <path>` or `stat <path>`
- Database: `SELECT EXISTS(...)` or schema check
- API: `curl -s <endpoint>` or MCP tool call
- Skill: Check SKILL_ALIAS_TABLE.json or directory listing

### Step 3: Verdict
- VERIFIED: External check confirms existence
- UNVERIFIED: External check failed or not possible → label as UNKNOWN
- FABRICATED: Claim exists but external check contradicts → VOID + alert
</verification-protocol>

## Floors
- F2 TRUTH: Never claim without external verification.
- F9 ANTIHANTU: Fabrication is a form of deception. Zero tolerance.
- F11 AUDITABILITY: Every verification attempt logged.
