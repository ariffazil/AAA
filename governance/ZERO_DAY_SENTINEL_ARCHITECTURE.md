# ZERO_DAY_SENTINEL — Constitutional Exposure Auditor

> **Forged:** 2026-08-02 by 333-AGI (Δ MIND) under F13 SOVEREIGN directive (Arif)
> **Classification:** DEFENSIVE_ONLY — constitutional exposure auditor, not exploit hunter
> **Status:** ARCHITECTURE SPEC — ratified by F13 sovereign
> **One-line kernel:** Zero-day defense is not clairvoyance; it is surface reduction, provenance, least agency, live drift detection, and fail-closed governance.
> **DITEMPA BUKAN DIBERI**

---

## 0. CONSTITUTIONAL VERDICT

| Verdict | Scope | Authority |
|---------|-------|-----------|
| **SEAL** | Defensive architecture — inventory, SBOM, drift, permission audit, exposure mapping | F13 |
| **HOLD** | Offensive exploit discovery, scanning assets you do not own, weaponization | F13 hard block |

**Core truth:** A true zero-day is previously unknown. You cannot "scan for all zero-days." The agent reduces exposure and detects suspicious conditions. It finds what is known-exploited, what is likely to be exploited, what changed, and what is over-permissioned.

---

## 1. AGENT SPECIFICATION

```yaml
agent_name: zero_day_sentinel
mode: DEFENSIVE_ONLY
authority: OBSERVE_ONLY_BY_DEFAULT
default_verdict: HOLD
identity_lane: 555-ASI (Ω CORE — memory, telemetry, drift, research)

allowed_actions:
  - inventory_assets
  - generate_sbom
  - compare_cve_kev_epss
  - scan_secrets_readonly
  - inspect_runtime_drift
  - audit_mcp_permissions
  - test_llm_prompt_injection_safely
  - produce_report

blocked_actions_without_seal:
  - exploit_execution
  - destructive_fuzzing
  - production_patch
  - secret_exfiltration
  - credential_rotation
  - public_internet_scanning
  - database_mutation
  - filesystem_delete

required_outputs:
  - scope
  - evidence
  - unknowns
  - risk_rank
  - recommended_action
  - reversibility
  - receipt_hash
  - verdict

verdicts:
  - SEAL
  - PARTIAL
  - UNKNOWN
  - SABAR
  - HOLD
  - VOID
```

---

## 2. FOUR KNOWLEDGE CATEGORIES

| Category | Knowledge Required | Source |
|----------|-------------------|--------|
| **Known exploited vulnerabilities** | CVE, CVSS, CISA KEV, vendor advisories, patch state | [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) |
| **Exploit likelihood** | EPSS, asset exposure, internet-facing status, business criticality | [FIRST EPSS](https://www.first.org/epss/) |
| **Security testing discipline** | Plan, authorize, test, analyze findings, develop mitigations | [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) |
| **AI/agentic risk** | Prompt injection, excessive agency, memory poisoning, tool misuse, privilege abuse | [OWASP Top 10 for LLM 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) |

---

## 3. SIX SKILLS (P0–P6)

### P0: Scope and Authorization
- What assets are in scope
- Who owns them
- What scan intensity is allowed
- Whether active probing is allowed
- What actions are read-only vs mutating
- When to stop and escalate
- **No scope = UNKNOWN. Destructive or intrusive scan = HOLD.**

### P1: Asset and Exposure Inventory
```text
What do we run? Where is it exposed? What version?
What dependency tree? What secrets or keys exist?
What tools can agents call? What changed since last known good?
```
**Existing arifOS capability:** `forge_security_drift_scan` — checks organ health, git SHA drift, unexpected public ports.

### P2: SBOM and Dependency Risk
- Direct and transitive dependencies
- Package versions, container images
- Python/npm/system packages
- Match against KEV, OSV, NVD, GitHub Advisory DB, vendor advisories
- **Existing arifOS capability:** `arifosmcp/arifos_attestation/sbom_scan.py` — CycloneDX-style SBOM scanner
- **SBOM is not optional. No SBOM means the agent is blind.**

### P3: Supply-Chain Attestation
- Signed artifacts, provenance, build identity
- Hashes, SLSA, Sigstore, container image provenance
- Tool/plugin provenance
- **Existing arifOS capability:** `sigstore_verify.py`, `slsa_verify.py`, `manifest_hash.py`
- **Note:** Sigstore verifier is currently PARTIAL — records SHA256, marks as unverified until full verification wired

### P4: Runtime Drift Detection
- New public ports, unexpected services
- Source/runtime commit mismatch
- Changed tool manifests, MCP surfaces
- New cron/systemd jobs, exposed endpoints
- New privileged tools, dependencies, environment variables, secret paths
- **Existing A-FORGE capability:** `forge-drift-scanner.sh` — organ health, git SHA drift, ports

### P5: Agent/Tool Permission Audit
For AI agents, zero-day-style failure is **not CVE-first. It is permission-first.**
- Which agent can call which tool
- Which tool can mutate files, shell out, access secrets, call external APIs, send messages
- Which calls require human approval, which are read-only
- **Existing A-FORGE capability:** `McpPolicyGate` — identity, server whitelist, tool allowlist, argument constraints, verdict logging

### P6: LLM and Agentic Attack-Surface Audit
Minimum OWASP knowledge:

| AI Risk | What to Scan |
|---------|-------------|
| Prompt injection | User input, retrieved docs, webpages, emails, code comments, PDFs |
| Sensitive information disclosure | Logs, prompts, memory, RAG context, tool outputs |
| Supply chain | Models, plugins, tools, datasets, adapters |
| Data/model poisoning | RAG stores, embeddings, memory, training/fine-tune data |
| Improper output handling | Model output passed to shell, SQL, HTML, code, API |
| Excessive agency | Too many tools, too much permission, unsupervised loops |
| System prompt leakage | Logs, traces, debug endpoints, exposed prompts |
| Vector/embedding weakness | Poisoned vectors, retrieval leaks, stale indexes |
| Misinformation | Unsupported claims trusted as facts |
| Unbounded consumption | Infinite loops, token burn, API cost exhaustion |

**Source:** [OWASP Top 10 for LLM Applications 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf), [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)

---

## 4. TOOL CLASSES

### Required Defensive Scanners

| Tool Class | Examples | Purpose |
|-----------|----------|---------|
| SBOM generation | CycloneDX, Syft | Know dependency tree |
| Vulnerability matching | Trivy, Grype, OSV-Scanner, npm audit, pip-audit | Match to known CVEs |
| KEV prioritization | CISA KEV | Prioritize exploited-in-wild |
| Exploit probability | FIRST EPSS | Prioritize likely exploitation |
| Secret scanning | Gitleaks, TruffleHog | Find leaked keys/secrets |
| Static analysis | Semgrep, CodeQL, Bandit, Ruff security | Code-level weakness |
| Container scanning | Trivy, Grype, Docker Scout | Image and OS packages |
| Runtime exposure | Nmap (owned scope only), asset inventory | Exposed services |
| Web surface testing | OWASP ZAP baseline, security headers | Passive web checks |
| Policy-as-code | OPA/Rego, Cedar | Enforce allowed actions |
| Agent red-team | Prompt injection test suites, promptfoo | Validate AI behavior safely |

### Existing arifOS/A-FORGE Capabilities

| Capability | Location | Status |
|-----------|----------|--------|
| SBOM generation | `arifosmcp/arifos_attestation/sbom_scan.py` | Phase 1 — generates SBOM, Phase 2 — CVE scan pending |
| Sigstore/SLSA/manifest | `arifosmcp/arifos_attestation/` | PARTIAL — Sigstore records SHA256, marks unverified |
| Threat engine | `arifosmcp/core/threat_engine.py` | Parses Python AST, SQL, shell, NL → unified threat |
| MCP policy gate | A-FORGE `McpPolicyGate` | Identity, server, tool, argument, verdict layers |
| Drift scanner | A-FORGE `forge-drift-scanner.sh` | Organ health, git SHA drift, ports |
| Adversarial audit | `arifosmcp/audit/adversarial_audit_harness.py` | Drift, generated quote, author swap, risk bypass |

---

## 5. RESOURCES — DAILY/PER-SCAN

| Resource | Use |
|----------|-----|
| [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | Known exploited vulnerabilities, remediation prioritization |
| [FIRST EPSS](https://www.first.org/epss/) | Probability of CVE exploitation in next 30 days |
| [NIST SP 800-115](https://csrc.nist.gov/pubs/sp/800/115/final) | Security testing planning, assessment, findings, mitigation |
| [OWASP Top 10 for LLM 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf) | LLM application risk taxonomy |
| [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) | Agentic risks: tool security, least privilege, memory poisoning, goal hijacking |
| [OWASP Agentic AI Threats](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/) | Threat-model reference for agentic AI |

---

## 6. CANONICAL SCAN WORKFLOW

```text
1.  SCOPE — Confirm owned assets, repo, domain, VPS, container, agents, scan intensity.
2.  INVENTORY — Build asset list: services, ports, repos, containers, packages, tools, APIs.
3.  SBOM — Generate SBOM for each repo/container/runtime.
4.  MATCH — Compare against CVE, CISA KEV, OSV, vendor advisories, EPSS.
5.  EXPOSURE — Identify internet-facing services, high-privilege services, stale services.
6.  SUPPLY CHAIN — Check signatures, provenance, lockfiles, package drift, unpinned deps.
7.  AGENTIC SURFACE — Audit tool permissions, MCP policies, prompt injection exposure, memory poisoning risk.
8.  DRIFT — Compare current runtime with last known good: ports, commits, services, tool manifests.
9.  PRIORITIZE — Rank: KEV + EPSS + exposed + privilege + business criticality + reversibility.
10. REPORT — Output: SEAL / PARTIAL / HOLD with evidence, no exploit instructions.
11. REMEDIATE PLAN — Patch, isolate, disable, rotate secrets, reduce permissions, add gates.
12. RECEIPT — Store evidence, hashes, timestamp, scan scope, findings, and unknowns.
```

---

## 7. WHAT NOT TO GIVE THE AGENT

Do NOT give a zero-day scan agent:
- Default shell write access
- Unrestricted internet scanning
- Secrets by default
- Broad GitHub tokens
- Cloud admin
- Production database write permission
- Ability to auto-patch production without approval
- Ability to run exploit PoCs automatically
- Ability to call all MCP tools under sovereign identity

**arifOS rule:** These trigger **HOLD** unless specifically authorized by F13.

---

## 8. INTEGRATION WITH EXISTING FEDERATION

| Federation Organ | Role in Zero-Day Scan |
|-----------------|----------------------|
| **arifOS (:8088)** | Constitutional verdict on scan findings, SEAL/HOLD gating |
| **A-FORGE (:7071)** | Drift scanning, MCP policy audit, security drift scan execution |
| **AAA (:3001)** | Agent permission audit, tool surface mapping, APEX scalars monitoring |
| **GEOX (:8081)** | NOT APPLICABLE (Earth intelligence — no security role) |
| **WEALTH (:18082)** | NOT APPLICABLE (Capital intelligence — no security role) |
| **WELL (:18083)** | Substrate reliability — machine health feeds into drift detection |
| **555-ASI (Ω CORE)** | Memory, telemetry, drift detection, research — primary scan agent |
| **888-APEX (Ψ SOUL)** | Constitutional verdict on scan actions — HOLD/VOID/SEAL |
| **333-AGI (Δ MIND)** | Orchestration, reasoning, plan generation, synthesis |

---

*DITEMPA BUKAN DIBERI — Forged from F13 SOVEREIGN directive, 2026-08-02*
*Zero-day defense is not clairvoyance; it is surface reduction, provenance, least agency, live drift detection, and fail-closed governance.*