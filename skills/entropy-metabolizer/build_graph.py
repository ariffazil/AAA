#!/usr/bin/env python3
"""Build capability-graph-2026-09-30.json from probe evidence.

333-reasoning (FI-002), phase 1 of 4 lower-entropy metabolizer pipeline.
Every edge below is backed by a probe receipt captured 2026-09-30T13:2x-13:41Z.
Read-only construction: this script writes ONLY the output JSON.
"""
import json
import os

OUT = "/root/.claude/skills/entropy-metabolizer/output/capability-graph-2026-09-30.json"

# ---- tension score is decomposed, not a single opaque number ----
# components: authority_conflict(3) runtime_coupling(3) silent_failure(2)
#             audit_claim_refuted(2) no_rollback_path(1) high_inbound_refs(1)
# score = min(10, sum(components))


def t(auth=0, run=0, silent=0, refuted=0, norollback=0, inbound=0):
    return min(10, 3 * auth + 3 * run + 2 * silent + 2 * refuted + 1 * norollback + 1 * inbound)


nodes = [
    # ---------------- TRACKED_DEBRIS ----------------
    {
        "id": "N01",
        "path": "core/cooling_ledger.py",
        "audit_disposition": "DEPRECATE",
        "audit_confidence": 0.92,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "core/__init__.py exists (41 bytes) so core/ IS an importable package - not a stray dir",
                "supabase/migrations/20260628_001_cooling_ledger_core.sql:19 owns the SCHEMA named cooling_ledger (third claimant on the name)",
            ],
            "runtime_shadow": "/opt/arifos/app/core/cooling_ledger.py (sha12 7cf1a421be97 = IDENTICAL to source); also shipped in wheel at /opt/arifos/current/venv/lib/python3.13/site-packages/core/cooling_ledger.py (sha12 7cf1a421be97)",
            "attention_status": "cold (git_last 2026-06-23 = 99d, 0 commits/30d, 2 commits/180d)",
            "e9_payer": "Future agent",
            "graph_tension_score": t(silent=1),
        },
        "evidence": {
            "stub_content": "8 lines; class CoolingLedger with __init__(pass) + record_sabar() only. sha256:7cf1a421be97... (core/cooling_ledger.py:1-8)",
            "real_impl": "arifosmcp/cooling_ledger.py = 462 lines, sha12 5055c288d282, exports CoolingLedgerError:51 / CoolingLedgerClient:67 / CoolingLedgerSession:394",
            "zero_importers": "grep -rn --fixed-strings 'cooling_ledger' over /root/arifOS (excl .git,node_modules,.ua,00_legacy) returns NO import of core.cooling_ledger; only supabase SQL schema hits + kernel_mcp.py:50 (see refutation)",
            "stub_method_dead": "record_sabar has exactly ONE hit box-wide: its own definition at core/cooling_ledger.py:5. Zero callers.",
        },
        "audit_claim_check": {
            "claim": "'The core/ version is a dead skeleton - never imported by arifosmcp/'",
            "verdict": "CONFIRMED but INCOMPLETE",
            "finding": "Audit missed the live consequence. arifosmcp/kernel_mcp.py:50 executes `from arifosmcp.core.cooling_ledger import CoolingLedger` inside try/except Exception -> CoolingLedger = None. That module DOES NOT EXIST (arifosmcp/core/ exists with 14 dirs but no cooling_ledger.py). Verified: deployed venv, cwd=/tmp -> `ModuleNotFoundError: No module named 'arifosmcp.core.cooling_ledger'`. So kernel_mcp silently binds CoolingLedger=None. The real E4/E7 entropy is the PHANTOM THIRD PATH in kernel_mcp.py:50, not the 8-line stub.",
        },
        "tension_components": ["silent_failure: kernel_mcp.py:50 swallows ModuleNotFoundError"],
    },
    {
        "id": "N02",
        "path": ".arifos/REAlITY_LAWS.md",
        "audit_disposition": "ARCHIVE",
        "audit_confidence": 0.88,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "SELF-DECLARED CANONICAL + SOVEREIGN-RATIFIED: header carries 'Status: F13 RATIFIED | BINDING: YES - Tier 5 Governance Doctrine | RATIFIED BY: Muhammad Arif bin Fazil - \"seal and ratify everything\" | SEAL: a624ba3d77796cd8' (.arifos/REAlITY_LAWS.md:6)",
                "competitor .arifos/REALITY_LAWS.md:3 declares 'STATUS: DRAFT - NOT RATIFIED'",
                "ZERO inbound citations from GENESIS/, docs/, or static/ for EITHER file (grep -rn -E 'REALITY_LAWS|REAlITY_LAWS' GENESIS docs static -> 0 hits)",
            ],
            "runtime_shadow": "/opt/arifos/app/.arifos/REAlITY_LAWS.md (sha12 305597bff94d = IDENTICAL) + shipped in deployed wheel site-packages/.arifos/REAlITY_LAWS.md (sha12 305597bff94d)",
            "attention_status": "cold-by-git / warm-by-mtime (NO git history - untracked+ignored; mtime 2026-07-17 = 75d)",
            "e9_payer": "888 APEX",
            "graph_tension_score": t(auth=1, refuted=1, norollback=1),
        },
        "evidence": {
            "size": "693 lines, sha12 305597bff94d",
            "title": "'REALITY LAWS - The Foundation Beneath arifOS', Source: Arif Fazil Telegram DM 2026-06-20, Weight: Foundational",
            "untracked": "git ls-files --error-unmatch -> not tracked. git check-ignore -v -> .gitignore:90:.arifos/",
            "paired_file": ".arifos/REALITY_LAWS.md = 450 lines, sha12 db24e7c5698f, 'Foundation of the Universe: The Invariants You Cannot Lawan Arus', STATUS: DRAFT - NOT RATIFIED",
        },
        "audit_claim_check": {
            "claim": "'Filename typo: REAlITY_LAWS.md ... Two competing documents; likely one should be canonical and the other archived' -> disposition ARCHIVE on the 'typo' file",
            "verdict": "REFUTED - AUTHORITY INVERSION",
            "finding": "The audit's ARCHIVE target is the ONLY F13-RATIFIED, sovereign-sealed document of the pair. The clean-cased REALITY_LAWS.md is the DRAFT. Executing the audit disposition as written would archive ratified law and leave an unratified draft as the survivor - an E5 authority inversion whose payer is 888 APEX (wrong seal = F2 violation). Neither filename is cited anywhere in GENESIS/docs/static, so the casing difference is not a broken-link risk; it is a canonical-selection decision that belongs to the sovereign, not to a filename heuristic.",
        },
        "tension_components": [
            "authority_conflict: two claimants, one ratified one draft, no inbound citation to disambiguate",
            "audit_claim_refuted: disposition would invert authority",
            "no_rollback_path: untracked + gitignored -> git cannot restore if removed (F1 AMANAH gap)",
        ],
    },
    {
        "id": "N03",
        "path": ".arifos/REALITY_LAWS.md",
        "audit_disposition": "NOT-A-SEPARATE-CANDIDATE (audit named it only as N02's counterpart)",
        "audit_confidence": None,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "self-declares 'STATUS: DRAFT - NOT RATIFIED' (.arifos/REALITY_LAWS.md:3)",
                "self-declares 'EPISTEMIC TIER: Tier 0-2 (Physical & Information Constraints)'",
            ],
            "runtime_shadow": "/opt/arifos/app/.arifos/REALITY_LAWS.md (sha12 db24e7c5698f = IDENTICAL) + deployed wheel site-packages/.arifos/REALITY_LAWS.md",
            "attention_status": "cold-by-git / warm-by-mtime (no git history; mtime 2026-07-17)",
            "e9_payer": "888 APEX",
            "graph_tension_score": t(auth=1, norollback=1),
        },
        "evidence": {
            "size": "450 lines, sha12 db24e7c5698f",
            "untracked": ".gitignore:90:.arifos/ ; git ls-files -> untracked",
        },
        "note": "Promoted to a first-class node because the audit treated the pair as ONE candidate while the disposition decision requires both nodes to be visible. This is the graph-tension pair (EUREKA::AUTHORITY_ENTROPY::v1): the tension lives in the EDGE, not in either node.",
        "tension_components": ["authority_conflict (pair with N02)", "no_rollback_path: untracked+ignored"],
    },
    {
        "id": "N04",
        "path": "arifOS_park/deep_research_stub_server.py",
        "audit_disposition": "ARCHIVE",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "arifOS_park IS a recognized archive zone: scripts/asabiyyah_probe.py:76 CER_ARCHIVE_DIRS = frozenset({'archive','_retired','00_legacy_materials','arifOS_park','.archive'})",
                "sole file in arifOS_park/ (count=1, 29879 bytes)",
            ],
            "runtime_shadow": "/opt/arifos/app/arifOS_park/deep_research_stub_server.py (sha12 da49ef619397 = IDENTICAL); NOT in deployed wheel (packaging excludes it)",
            "attention_status": "cool (git_last 2026-08-15 = 46d, 0 commits/30d, 1 commit/180d)",
            "e9_payer": "Future agent",
            "graph_tension_score": t(silent=0),
        },
        "evidence": {
            "self_reference_only": "the single non-audit hit for 'deep_research_stub_server' box-wide is its own explorer_tag at arifOS_park/deep_research_stub_server.py:136",
            "not_in_wheel": "existence probe: dep=- for arifOS_park/deep_research_stub_server.py",
        },
        "audit_claim_check": {
            "claim": "'Not imported, not in Makefile, not in Dockerfile'",
            "verdict": "CONFIRMED, plus one risk the audit did not record",
            "finding": "The stub declares port 8088 at arifOS_park/deep_research_stub_server.py:109 ('port': '8088') - the LIVE arifOS governance kernel port (systemd arifos.service ARIFOS_PORT=8088). Harmless while parked and excluded from the wheel, but if ever executed it would collide with the constitutional kernel. Record as a latent port-collision edge, not as current entropy.",
        },
        "tension_components": ["none scoring; already inside a declared archive zone with an explicit machine-readable policy"],
    },
    {
        "id": "N05",
        "path": "00_legacy_materials/",
        "audit_disposition": "ARCHIVE",
        "audit_confidence": 0.90,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "declared archive zone: scripts/asabiyyah_probe.py:76",
                "declared wheel-excluded: deploy/fhs-map.yaml:58 (packaging.exclude_from_wheel)",
                "declared scan-excluded: scripts/emit_change_receipt.py:38, commands/scripts_archive/audit_charter_naming.py:11",
                "declared atlas node: arifosmcp/resources/atlas_repo.py:377",
                "test dependency: tests/test_registry.py:19 expects REGISTRY_PATH/'00_legacy_materials'/'arifOS-upstream'/'archive'",
                "self-describing policy: 00_legacy_materials/.github/ARCHIVE_METADATA.json retention_policy=COLD_STORAGE, read_only=true, classification='NOISE - do not scan for EUREKA in future passes'",
            ],
            "runtime_shadow": "/opt/arifos/app/00_legacy_materials/ = DIR (present); deployed wheel = DIR (present, despite fhs-map exclude_from_wheel -> packaging rule not honoured)",
            "attention_status": "warm (git_last 2026-09-15 = 15d, 2 commits/30d, 18 commits/180d)",
            "e9_payer": "Future agent",
            "graph_tension_score": t(refuted=1),
        },
        "evidence": {
            "actual_size": "files_on_disk=1, dirs=2, size=12K. Sole tracked file: 00_legacy_materials/.github/ARCHIVE_METADATA.json (git ls-files count=1)",
            "counterpart": "archive/00_legacy_materials = 2 files, 492K",
            "archive_date": "ARCHIVE_METADATA.json: archived 2026-04-26, reason '~2100 files bulk-copy noise', superseded_by 'Current arifOS at /opt/arifos/app', last_accessed 2026-07-26",
        },
        "audit_claim_check": {
            "claim": "audit note 'Main legacy content already in archive/00_legacy_materials/. Double-nesting - top-level is a shell'",
            "verdict": "CONFIRMED for the audit; but TWO LIVE DOCS ARE FALSE and the audit did not flag them",
            "finding": "docs/ARCHITECTURE_TRUTH.md:161 claims '00_legacy_materials/ (562 files)'; docs/AGENT_STATE.md:123 claims 'upstream archive, 118MB, not active'. Measured: 1 file, 12K. Both overstate by ~3 orders of magnitude. This is E2 knowledge entropy that outlives the directory: archiving the shell without correcting the two docs leaves a false map that a future agent will trust. The ARCHIVE_METADATA's own '~2100 files' is a third, different figure.",
        },
        "tension_components": [
            "audit_claim_refuted: doc-vs-disk drift at docs/ARCHITECTURE_TRUTH.md:161 + docs/AGENT_STATE.md:123",
            "packaging_rule_violated: fhs-map.yaml:58 excludes it from wheel yet wheel contains it (scored as observation, not tension)",
        ],
    },
    {
        "id": "N06",
        "path": ".opencode/SPRINT-2026-05-03-DRIFT-LEDGER-CLOSURE.md",
        "audit_disposition": "DEPRECATE",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "referenced as a GATE by its sibling: .opencode/SPRINT-TRACE-SPINE-IMPL.md:4 'Do not begin until DRIFT-LEDGER-CLOSURE sprint is SEALED' and :9 '[ ] DRIFT-LEDGER-CLOSURE all 4 gates PASSED'",
                "self-identifying: own line 1 title + line 158 json 'sprint': 'DRIFT-LEDGER-CLOSURE'",
            ],
            "runtime_shadow": "/opt/arifos/app/.opencode/SPRINT-2026-05-03-DRIFT-LEDGER-CLOSURE.md (sha12 9ddac207fbd7 = IDENTICAL) + deployed wheel (sha12 9ddac207fbd7)",
            "attention_status": "cold (git_last 2026-05-11 = 142d, 0 commits/30d, 3 commits/180d)",
            "e9_payer": "Future agent",
            "graph_tension_score": t(),
        },
        "evidence": {
            "age_correction": "audit said '137 days old' as of 2026-09-17; measured 142d as of 2026-09-30 - consistent",
            "zero_code_refs": "grep --fixed-strings 'DRIFT-LEDGER-CLOSURE' -> 5 hits, all inside the two .opencode/ sprint files + the audit itself",
        },
        "tension_components": ["none: self-contained 2-file cohort, no code/config/CI consumer"],
        "pair_note": "Forms a closed dyad with N07. Deprecate together or not at all - removing one strands the other's gate reference.",
    },
    {
        "id": "N07",
        "path": ".opencode/SPRINT-TRACE-SPINE-IMPL.md",
        "audit_disposition": "DEPRECATE",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": ["gated BY N06 (.opencode/SPRINT-TRACE-SPINE-IMPL.md:4,9); claims no authority over anything else"],
            "runtime_shadow": "/opt/arifos/app/.opencode/SPRINT-TRACE-SPINE-IMPL.md (sha12 9fc819f19c2a = IDENTICAL) + deployed wheel (sha12 9fc819f19c2a)",
            "attention_status": "cold (git_last 2026-05-11 = 142d, 0/30d, 2/180d)",
            "e9_payer": "Future agent",
            "graph_tension_score": t(),
        },
        "evidence": {"zero_external_refs": "grep --fixed-strings 'SPRINT-TRACE-SPINE-IMPL' -> 1 hit box-wide: the audit entry itself. No inbound reference at all."},
        "tension_components": ["none: lowest-tension node in the graph (zero inbound, zero outbound, cold)"],
    },
    # ---------------- INVESTIGATE ----------------
    {
        "id": "N08",
        "path": "arifosmcp/.arifos/adam_agent.py",
        "audit_disposition": "INVESTIGATE",
        "audit_confidence": 0.75,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": ["NONE - the path does not exist and has never existed in git"],
            "runtime_shadow": None,
            "attention_status": "n/a (phantom path)",
            "e9_payer": "Federation",
            "graph_tension_score": t(refuted=1, silent=1),
        },
        "evidence": {
            "tier0_phantom_probe": "test -e arifosmcp/.arifos/adam_agent.py -> MISSING; git ls-files --error-unmatch -> 'did not match any file(s) known to git'; ls arifosmcp/.arifos/ -> 'No such file or directory'; git log --all --oneline -- <path> -> EMPTY (never existed in any branch)",
            "existence_all_trees": "src=- rt=- dep=- (probe matrix)",
            "real_file": "/root/arifOS/.arifos/adam_agent.py = 137 lines, sha12 f8d2bfeccbc7, TRACKED, git_last 2026-05-11, 3 commits/180d",
            "real_file_purpose": "'ADAM Agent (Omega Heart) - arifOS Autoresearch. Stability checks, readability scoring, cooling analysis.' CLI form: `python adam_agent.py --input=/tmp/arif_output.json --output=/tmp/adam_output.json`; ARIFOS_ROOT = Path(__file__).parent.parent; SCOPED_DIRS = ['core/shared','arifosmcp/runtime','tests','ARCH/DOCS']",
            "other_copies": "/opt/arifos/.arifos/adam_agent.py, /opt/arifos/app/.arifos/adam_agent.py, /root/arifOS-wt-record-append/.arifos/, /root/forge_work/sa-fix/.arifos/, /root/forge_work/arifos-rel-b1b2/.arifos/ (6 locations box-wide)",
        },
        "audit_claim_check": {
            "claim": "candidate path 'arifosmcp/.arifos/adam_agent.py' + unknowns[] 'arifosmcp/.arifos/adam_agent.py - purpose unknown, zero references'",
            "verdict": "REFUTED - PHANTOM NODE (path typo propagated into the audit artifact)",
            "finding": "The audit invented a path with a spurious 'arifosmcp/' prefix. The real file is .arifos/adam_agent.py. Consequence: any metabolizer that acts on the audit's path list will no-op on this node - the removal succeeds trivially (nothing to remove) while the real tracked file survives unexamined. That is the exact phantom-evidence failure class this federation has scarred on twice (tier-0-phantom-evidence-2026-09-21; scar-2026-09-30 verifier 'claimed-before-checking'). The audit artifact is itself tracked (git ls-files entropy-audit-2026-09-17.json -> TRACKED), so the phantom path is now durable federation record.",
        },
        "tension_components": [
            "audit_claim_refuted: node identity wrong -> downstream no-op",
            "silent_failure: removal of a nonexistent path reports success",
        ],
        "real_node_substitute": {
            "path": ".arifos/adam_agent.py",
            "static_imports": [],
            "dynamic_loads": ["no importlib/__import__/spec_from_file_location hit for 'adam_agent' anywhere in /root/arifOS (probe returned empty)"],
            "authority_claims": [
                "TRACKED in git despite living under an IGNORED dir: git ls-files .arifos/ -> 11 tracked files (incl. adam_agent.py) while .gitignore:90 declares '.arifos/' ignored. Tracked-beats-ignore means the ignore rule is inert for these 11 files.",
                "member of a Trinity set in the same dir: .arifos/{arif_agent.py, adam_agent.py, apex_judge.py, metrics.py, vault_seal.py}",
            ],
            "runtime_shadow": "/opt/arifos/app/.arifos/adam_agent.py (sha12 f8d2bfeccbc7 = IDENTICAL) + deployed wheel (sha12 f8d2bfeccbc7)",
            "attention_status": "cold (142d, 0/30d, 3/180d)",
            "e9_payer": "Future agent",
            "graph_tension_score": t(refuted=1, silent=1),
        },
    },
    {
        "id": "N09",
        "path": ".arifos/autoresearch.py",
        "audit_disposition": "INVESTIGATE",
        "audit_confidence": 0.70,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [
                "CLI-invoked, not import-loaded: own docstring '.arifos/autoresearch.py:15-17' gives `python autoresearch.py --budget=300` / `--budget=60 --path=core/shared/utils.py`; imports subprocess (:20) to drive children",
                "NO importlib/__import__/spec_from_file_location hit for 'autoresearch' anywhere (probe returned empty)",
            ],
            "authority_claims": [
                "declares the loop it owns: '.arifos/autoresearch.py:4' 'Bounded exploration using Trinity architecture: ARIF -> ADAM -> APEX' (i.e. it is the orchestrator of the N08 sibling set)",
                "a whole test namespace mirrors it: tests/autoresearch/arifos_train.py:5 'Pattern: karpathy/autoresearch train.py'; tests/autoresearch/arifos_program.md:3,10",
                "documented as a live workflow: docs/vibe_coder_brief.md:52 'Read the current run log: logs/autoresearch_2026-04-22.jsonl'",
                "branch-identity claimant: docs/architecture/DISCOVERY.md:3 'Branch: autoresearch/2026-04-22'; docs/architecture/DEPLOYMENT.md:110 deploy_ref 'autoresearch/2026-04-22'; tests/amanah_critical_findings.md:4; docs/REPO_CLEANUP_PLAYBOOK.md:260",
                "upstream provenance: static/arifos/theory/000/000_ARCHITECTURE.md:232 + static/arifos/floors/F0_DUTY_TO_LOOK.md:16 ('Karpathy autoresearch')",
                "log-path coupling: commands/scripts_archive/e2e_runner.py:252 writes f'autoresearch_{date_str}.jsonl'",
            ],
            "runtime_shadow": "/opt/arifos/app/.arifos/autoresearch.py (sha12 efa442e90524 = IDENTICAL) + deployed wheel (sha12 efa442e90524)",
            "attention_status": "cold (git_last 2026-05-11 = 142d, 0/30d, 2/180d)",
            "e9_payer": "Future agent",
            "graph_tension_score": t(refuted=1),
        },
        "evidence": {
            "size": "344 lines, sha12 efa442e90524, TRACKED",
            "string_hits": "23 non-audit hits for 'autoresearch' across tests/, docs/, static/, commands/ - the audit recorded ZERO",
            "economic_guards": "MARGINAL_THRESHOLD / MAX_ITERATIONS / CONVEXITY_CHECK / NPV_GATE documented at .arifos/autoresearch.py:7-11",
        },
        "audit_claim_check": {
            "claim": "'Zero references in arifosmcp/, core/, or server.py. Could be dynamically loaded or CLI-invoked.' confidence 0.70",
            "verdict": "PARTIALLY CONFIRMED, MATERIALLY UNDERSTATED",
            "finding": "'Zero references' is true only for Python import statements inside those three scopes. The scan window was too narrow: 23 string references exist in tests/, docs/, static/, commands/. The file is a documented CLI entrypoint whose name is also a git BRANCH IDENTITY ('autoresearch/2026-04-22') cited by 4 docs including docs/architecture/DEPLOYMENT.md:110 as a deploy_ref. Classifying it dead_code on an import-only scan is a scope error, not a judgement error.",
        },
        "tension_components": [
            "audit_claim_refuted: 'zero references' false outside the import scan window",
            "name_collision: module name == branch namespace == upstream project name (3 referents, one string)",
        ],
    },
    {
        "id": "N10",
        "path": ".collab/COLLAB.md",
        "audit_disposition": "INVESTIGATE",
        "audit_confidence": 0.75,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "claims F13 provenance in its own header: '.collab/COLLAB.md:3' 'Authority: F13 SOVEREIGN (Arif Fazil)', :4 'Branch: main (direct commits - sequential collaboration)', :5 'Date: 2026-06-05', :6 'Agents: Omega-FORGE (OpenCode) + Kimi'",
                "documents a contract that DOES exist in code: 'Shared Contract: FederationEnvelope v1.1' with `from arifosmcp.schemas.federation_envelope import FederationEnvelope` (.collab/COLLAB.md:15)",
                "NO external consumer: grep --fixed-strings '.collab/COLLAB.md' over /root/AAA /root/A-FORGE /root/scripts /root/.claude -> 0 hits",
            ],
            "runtime_shadow": "/opt/arifos/app/.collab/COLLAB.md (sha12 c5e75a42ea22 = IDENTICAL) + deployed wheel (sha12 c5e75a42ea22)",
            "attention_status": "cold (git_last 2026-06-14 = 108d, 0/30d, 3/180d)",
            "e9_payer": "Federation",
            "graph_tension_score": t(),
        },
        "evidence": {"size": "90 lines, sha12 c5e75a42ea22, TRACKED", "zero_code_refs": "only non-audit hits are inside the file itself"},
        "audit_claim_check": {
            "claim": "'Zero references in codebase. Collaboration configuration file - may be consumed by tooling not visible in source.'",
            "verdict": "REFUTED on classification; CONFIRMED on zero-references",
            "finding": "It is not a configuration file - nothing parses it. It is a dated human/agent collaboration LOG (2026-06-05) that records the FederationEnvelope v1.1 contract rollout. Its residual value is historical witness, not capability. Probe found no consumer in any of the four searched trees, so 'tooling not visible in source' has no supporting evidence. Safe to archive as a record; NOT safe to treat as a live config whose removal changes behaviour.",
        },
        "tension_components": ["none scoring; misclassification risk noted but no live consumer exists"],
    },
    # ---------------- HOLD ----------------
    {
        "id": "N11",
        "path": "organ.yaml",
        "audit_disposition": "HOLD",
        "audit_confidence": 0.95,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "SELF-SURRENDERS authority: organ.yaml:1 '# This file is superseded by: /root/AAA/organ.yaml'",
                "canonical successor confirmed present: /root/AAA/organ.yaml exists (ls -la OK)",
                "only in-repo mention is DOCUMENTATION, not a load: arifosmcp/runtime/resource.py:143 is a help string '  6. organ.yaml        - organs' inside a numbered listing",
                "NO yaml.safe_load / open() of organ.yaml anywhere in /root/arifOS or /root/AAA (loader-form probe -> 0 hits)",
            ],
            "runtime_shadow": "/opt/arifos/app/organ.yaml (sha12 644c5181f32f = IDENTICAL) + deployed wheel (sha12 644c5181f32f)",
            "attention_status": "cool (git_last 2026-07-26 = 66d, 0/30d, 3/180d)",
            "e9_payer": "Federation",
            "graph_tension_score": t(auth=0),
        },
        "evidence": {"size": "98 bytes, sha12 644c5181f32f, TRACKED"},
        "audit_claim_check": {
            "claim": "'Self-declared superseded ... HOLD until topology files are consolidated.' confidence 0.95",
            "verdict": "CONFIRMED - and the HOLD is stronger than the audit argued",
            "finding": "The audit hedged with dynamic_loading:'unknown', external_consumer:'unknown'. Both are now resolved to NO: no loader, no consumer, only a help-string mention. This is the LOWEST-risk node among the authority conflicts because the surrender is explicit and machine-readable at line 1. Consolidation is a documentation move, not a capability move. Note the cross-repo edge: the canonical copy lives OUTSIDE this git repo (/root/AAA/), so removing the in-repo pointer does not affect the canonical file - but it does remove the only in-repo signpost to it.",
        },
        "tension_components": ["authority_conflict NOT scored: the conflict is self-resolved by an explicit pointer at organ.yaml:1"],
    },
    {
        "id": "N12",
        "path": "HISTORICAL_NOTICE.md",
        "audit_disposition": "HOLD",
        "audit_confidence": 0.70,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "TWO DISTINCT FILES claim the same name and cover DIFFERENT eras:",
                "  root HISTORICAL_NOTICE.md = 26 lines, sha12 ae01bb121082, title 'HISTORICAL NOTICE - arifOS Tool Naming Eras', :3 'Created: 2026-09-10 by FI-008 (kimi-code) - fixes broken reference from docs/architecture/ARIFOS_TOOL_AUDIT_REPORT.md (banner linked here; file was missing)'",
                "  docs/HISTORICAL_NOTICE.md = 42 lines, sha12 0746ac09d367, title 'HISTORICAL NOTICE - Tool Name Migration (2026-07-03)'",
                "cmp -s -> DIFFERENT (not copies of each other)",
                "54 INBOUND REFERENCES - highest inbound count of any node in this graph. Four INCONSISTENT link forms resolve to two different targets: 23x '../../HISTORICAL_NOTICE.md', 11x '../HISTORICAL_NOTICE.md', 11x './HISTORICAL_NOTICE.md', 7x 'docs/HISTORICAL_NOTICE.md', 1x bare 'HISTORICAL_NOTICE.md'",
                "GENESIS/ constitutional docs point at the DOCS copy by absolute path: GENESIS/000_KERNEL_CANON.md:1, 003_ANDERSEN_CALHOUN_FABLE.md:1, 005b_POST_AGI_ECONOMICS_KERNEL.md:1, 011_FEDERATION_AGI_SUBSTRATE.md:1, 012_CIVILIZATIONAL_INTENT.md:1, 016_ILMU_AKAL_HIKMAH_COGNITIVE_COSMOLOGY.md:1, 019_REALITY_ENGINEERING_PROTOCOL.md:1 all carry 'See [/root/arifOS/docs/HISTORICAL_NOTICE.md]'",
                "docs/ peers point at the ROOT copy relatively: docs/ADVERSARIAL_TESTS.md:1, docs/WELL_ARIFOS_CONTRACT.md:1, docs/MCP_BOUNDARY.md:1, docs/ARIFOS_MACHINE_KERNEL_BLUEPRINT.md:1, docs/T0-T4-2026-06-16-judge-payload.json:1 all carry 'See [HISTORICAL_NOTICE.md](./HISTORICAL_NOTICE.md)'",
                "docs/README.md:174 indexes 'HISTORICAL_NOTICE.md | Historical notice' (the docs copy)",
                "NEITHER file declares itself canonical over the other - no supersession line in either",
            ],
            "runtime_shadow": "/opt/arifos/app/HISTORICAL_NOTICE.md (sha12 ae01bb121082 = IDENTICAL); NOT in deployed wheel (dep=-)",
            "attention_status": "warm (git_last 2026-09-10 = 20d, 1 commit/30d) | docs/ counterpart cool (2026-07-03 = 89d, 0/30d)",
            "e9_payer": "Federation",
            "graph_tension_score": t(auth=1, inbound=1, refuted=1),
        },
        "evidence": {
            "root_file": "26 lines, sha12 ae01bb121082, TRACKED, git_last 2026-09-10",
            "docs_file": "42 lines, sha12 0746ac09d367, TRACKED, git_last 2026-07-03",
            "ref_count": "grep -rn 'HISTORICAL_NOTICE' -> 54 hits excluding the audit and the two files' own bodies",
        },
        "audit_claim_check": {
            "claim": "'Historical notice file. May serve as legal/governance notice. HOLD - not safe to remove without confirming purpose.' confidence 0.70, static_references: []",
            "verdict": "REFUTED - UNDERSTATED BY AN ORDER OF MAGNITUDE",
            "finding": "The audit recorded static_references: [] and treated this as ONE orphaned file. Reality: it is the highest-fan-in node in the graph (54 inbound links, including 7 constitutional GENESIS/ documents), and there are TWO non-identical files under one name with an unresolved canonical question. The root file exists PRECISELY BECAUSE a prior broken reference needed fixing (its own line 3 says so) - so this node has already caused one incident. Removal of either file breaks live documentation links; consolidating them requires editing up to 54 inbound references across constitutional docs. This is the graph's densest authority knot, not a governance orphan.",
        },
        "tension_components": [
            "authority_conflict: two non-identical files, one name, no canonical declaration, 4 link forms",
            "high_inbound_refs: 54 including 7 GENESIS constitutional docs",
            "audit_claim_refuted: static_references [] is false",
        ],
    },
    {
        "id": "N13",
        "path": "smithery.yaml",
        "audit_disposition": "HOLD",
        "audit_confidence": 0.80,
        "edges": {
            "static_imports": [],
            "dynamic_loads": ["machine-generated view, regenerated by scripts/sync_kernel_abi.py:167 'ROOT / \"smithery.yaml\": _smithery(runtime)'"],
            "authority_claims": [
                "CI-VALIDATED: .github/workflows/floor_gate.yml:29-30 'Verify smithery.yaml is valid YAML' -> python -c \"import yaml; yaml.safe_load(open('smithery.yaml'))\"",
                "CI-TRIGGER: .github/workflows/06-mcp-conformance.yml:18 lists 'smithery.yaml' in its path filter",
                "MAKEFILE-GUARDED: Makefile:215 '@test -f smithery.yaml || (echo \"smithery.yaml missing - MCP Registry unreachable\")'",
                "declared a GENERATED VIEW, not authority: docs/MCP_SOURCE_OF_TRUTH.md:36 'Machine authority: arifosmcp/abi/capability_registry.json and policy_registry.json. Generated views: docs/KERNEL_CAPABILITY_ABI.md, smithery.yaml, mcp-arifos.json, static/.well-known/mcp/server.json'",
                "external-facing surface: docs/MCP_SOURCE_OF_TRUTH.md:12 'smithery.yaml for the public Smithery-facing manifest'",
                "documented drift-defect: README.md:405 and README.md:537 both record --check failing on a pristine main worktree as of 2026-09-21, last clean resync 2026-09-15 (eacf0ca01)",
                "packaging-unification target: docs/superpowers/plans/2026-06-19-arifos-packaging-unification-plan.md:272 '[F13 CONFIRM] Update smithery.yaml - package name arifosmcp -> arifos'; specs/...-design.md:401",
                "indexed as governance surface: docs/philosophy/BOUNDARY.md:19; docs/ZEN.md:64",
            ],
            "runtime_shadow": "/opt/arifos/app/smithery.yaml (sha12 ad074201ecd2 = IDENTICAL to source) BUT deployed wheel site-packages/smithery.yaml = sha12 d8b8b8a02b73 -> DIVERGENT FROM SOURCE",
            "attention_status": "active (git_last 2026-09-15 = 15d, 2 commits/30d, 21 commits/180d - WARMEST NODE IN GRAPH; mtime 2026-09-21)",
            "e9_payer": "Federation",
            "graph_tension_score": t(run=1, auth=1),
        },
        "evidence": {
            "src_sha16": "ad074201ecd2b883",
            "deployed_sha16": "d8b8b8a02b73f1ff",
            "drift_guard_live": "python3 scripts/sync_kernel_abi.py --check -> 'Kernel ABI drift: smithery.yaml' (reproduced live 2026-09-30, confirming README.md:405's 2026-09-21 claim is still open 9 days later)",
            "version_lines": "smithery.yaml:3 version: '2026.07.24'; :8 mcp_version: '2025-11-25' - IDENTICAL in both src and deployed (so the version field is NOT where the drift lives)",
            "material_diff": "src line 36 declares tool description 'KERNEL 666 - Constitutional verdict - binding SEAL/HOLD/SABAR/VOID arbitration' while deployed line 37 declares 'KERNEL 888 - Constitutional verdict'. src line 32 'KERNEL 555 - Memory governor' vs deployed line 33 'KERNEL memory governor'. src arif_route schema carries auth_context + mission_id + optional intent; deployed arif_route schema carries 'required: [\"intent\"]' and no mission_id. Deployed arif_kernel_intercept schema uses mode default 'intercept' + epistemic_state/measurement/intent/authority_token; source uses mode default 'judge' + candidate/niat_params/heart_critique/entropy_pathway/actor_Phi/actor_B.",
        },
        "audit_claim_check": {
            "claim": "'Auto-generated by sync_kernel_abi.py. Version pinned at 2026.07.24 - stale if ABI changed since. External consumers (Smithery registry) may depend on it.' confidence 0.80",
            "verdict": "CONFIRMED and ESCALATED - the drift is not staleness, it is a tool-numbering schism",
            "finding": "The audit framed this as a stale version pin. Measured drift is deeper: the SOURCE manifest describes the 33/13 ZEN renumbering (KERNEL 555 memory / KERNEL 666 verdict) and a richer judge schema, while the DEPLOYED WHEEL manifest still describes the older numbering (KERNEL 888 verdict) and an intercept-shaped schema. Two different public tool contracts are being advertised for the same running kernel. Since docs/MCP_SOURCE_OF_TRUTH.md:12 makes this the PUBLIC Smithery-facing manifest, an external consumer reading the deployed copy sees a different ABI than one reading source. Payer is Federation (external contract) and, because verdict-tool naming is involved, 888 APEX. Note the drift guard is currently RED and has been for >=9 days across two audit passes - a known-broken gate left broken is E6 governance entropy.",
        },
        "tension_components": [
            "runtime_coupling: src sha != deployed-wheel sha on a CI-guarded, externally published manifest",
            "authority_conflict: two advertised ABIs for one running kernel; guard RED since <=2026-09-21",
        ],
    },
    {
        "id": "N14",
        "path": "risk_leash.yaml",
        "audit_disposition": "HOLD",
        "audit_confidence": 0.65,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [
                "LIVE RUNTIME LOADER CONFIRMED: arifosmcp/tools/health.py:145 def _check_risk_leash() -> yaml.safe_load over a 4-path candidate list: :148 env ARIFOS_RISK_LEASH_PATH, :154 Path('/app/risk_leash.yaml') 'canonical Docker mount point', :155 Path('/root/arifOS/risk_leash.yaml'), :156 Path(__file__).resolve().parents[3]/'risk_leash.yaml'; :180 falls through to {'status':'missing'}",
                "deployed copy of the loader is IDENTICAL to source: diff arifosmcp/tools/health.py[145:185] vs site-packages/arifosmcp/tools/health.py[145:185] -> IDENTICAL",
                "RUNTIME RESOLUTION MEASURED (deployed venv, cwd=/tmp): health.py __file__ = /opt/arifos/current/venv/lib/python3.13/site-packages/arifosmcp/tools/health.py; parents[3]/risk_leash.yaml = /opt/arifos/current/venv/lib/python3.13/risk_leash.yaml -> EXISTS=False; /app/risk_leash.yaml -> False; /root/arifOS/risk_leash.yaml -> True. RESULT: {'status':'healthy','path':'/root/arifOS/risk_leash.yaml','version':'2026.05.14-v1','rules_count':9}",
                "same result with cwd=/opt/arifos/app (the systemd WorkingDirectory): health.py -> /opt/arifos/app/arifosmcp/tools/health.py, risk_leash -> /root/arifOS/risk_leash.yaml",
            ],
            "authority_claims": [
                "SELF-DECLARED authority over two federation gates: risk_leash.yaml:5 'Applied by 777_WITNESS and 888_JUDGE runtime gates'; :11 'authority: \"777_FORGE | 888_JUDGE\"'",
                "classified SECURITY-SENSITIVE by tooling: .opencode.json:130 lists 'risk_leash.yaml' under 'security_sensitive' alongside '.secrets*', 'secrets/**', 'auth*'",
                "referenced as an operational boundary in AAA doctrine: /root/AAA/agents/_docs/SEED_AGENTS.md:203 'Risk leash: risk_leash.yaml defines operational boundaries.'",
                "already F13-held once: /root/AAA/reports/STAB-2026-09-16/ACTION-LEDGER.md:290 '| HOLD | organ.yaml, report JSONs, risk_leash.yaml, VISION_ORGAN/, smithery.yaml | F13 |'",
                "a SECOND copy is inventoried elsewhere: /root/AAA/archive/2026-07-25/AAA/archive/phase-111/arifos-inventory.json:21507 'path': 'arifosmcp/config/risk_leash.yaml' (vs :96 'path': 'risk_leash.yaml')",
                "prior known defect: /root/AAA/archive/2026-07-25/arifOS/docs/archive/cleanup-2026-07-20/phoenix72/EUREKA_EXTRACT.md:206 'risk_leash.yaml path is hardcoded'",
                "governs irreversible-action gating: :15-21 irreversible_actions.require_human_ack=true, auto_hold=true, examples [vault_seal, git_push_force, docker_system_prune]",
            ],
            "runtime_shadow": "/opt/arifos/app/risk_leash.yaml (sha12 ef3ea55161f6 = IDENTICAL) + deployed wheel site-packages/risk_leash.yaml (sha12 ef3ea55161f6) - but the wheel copy is NEVER READ: parents[3] resolves to /opt/arifos/current/venv/lib/python3.13/risk_leash.yaml which does not exist, so the loader falls through to the SOURCE TREE path",
            "attention_status": "cold (git_last 2026-05-14 = 139d, 0/30d, 1/180d)",
            "e9_payer": "888 APEX",
            "graph_tension_score": t(run=1, auth=1, silent=1),
        },
        "evidence": {
            "size": "sha12 ef3ea55161f6, TRACKED, version '2026.05.14-v1' (risk_leash.yaml:10)",
            "live_probe_receipt": "deployed-venv runtime probe 2026-09-30 returned status=healthy path=/root/arifOS/risk_leash.yaml version=2026.05.14-v1 rules_count=9",
        },
        "audit_claim_check": {
            "claim": "'Version 2026.05.14-v1. May be consumed by 777_FORGE or 888_JUDGE runtime gates. 64 days old. HOLD - verify if consumed at runtime before any action.' confidence 0.65, dynamic_loading:'unknown', external_consumer:'unknown'",
            "verdict": "CONFIRMED - the audit's own verification demand is now discharged, and the answer is worse than 'consumed'",
            "finding": "The audit correctly refused to act pending a runtime check. That check is now done: risk_leash.yaml IS consumed at runtime, by the DEPLOYED WHEEL, and the wheel reads it FROM THE SOURCE TREE. Consequence: /root/arifOS is not merely a source checkout - it is a live runtime dependency of the deployed kernel's security-sensitive risk gating. Editing or removing this file changes deployed gate behaviour with NO redeploy, NO wheel rebuild, NO attestation, and NO CI signal. The coupling direction (deployed -> source) is the inverse of the normal packaging flow declared at deploy/fhs-map.yaml ('wheel = sole production code artifact'), so the packaging doctrine is violated by this one file. The loader also fails silently-open at the file level: health.py:180 returns {'status':'missing'} rather than raising, so a deleted leash degrades to a health-report line, not an error. Age is also mis-stated: 139d by git, not 64d.",
        },
        "tension_components": [
            "runtime_coupling: deployed wheel reads source-tree file (deployed -> source dependency, packaging doctrine inverted)",
            "authority_conflict: self-declares 777_FORGE|888_JUDGE authority while being loaded by arifosmcp/tools/health.py; second copy inventoried at arifosmcp/config/risk_leash.yaml",
            "silent_failure: health.py:180 degrades to {'status':'missing'} instead of failing closed",
        ],
    },
    # ---- 8 top-level report JSONs (audit carried these as ONE candidate) ----
    {
        "id": "N15",
        "path": "surface-evidence.json",
        "audit_disposition": "HOLD (audit: 'top-level report JSONs (8 files)' as one entry)",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "generator: scripts/gen_surface_evidence.py (audit-identified; not re-verified in this pass)",
                "EXPLICITLY gitignored: .gitignore:56 'surface-evidence.json' -> git ls-files: UNTRACKED",
            ],
            "runtime_shadow": "/opt/arifos/app/surface-evidence.json (sha12 e39ab869568a = IDENTICAL); NOT in deployed wheel",
            "attention_status": "cold (NO git history - untracked; therefore no commit-based attention signal available)",
            "e9_payer": "Federation",
            "graph_tension_score": t(refuted=0),
        },
        "evidence": {"sha12": "e39ab869568a", "git_check_ignore": ".gitignore:56:surface-evidence.json"},
        "tension_components": ["none: untracked ephemeral output with a known generator"],
    },
    {
        "id": "N16",
        "path": "semantic-closure-report.json",
        "audit_disposition": "HOLD",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": ["generator: scripts/semantic_closure_scanner.py (audit-identified)", "gitignored via .gitignore:54 '*-report.json' -> UNTRACKED"],
            "runtime_shadow": "/opt/arifos/app/semantic-closure-report.json (sha12 7b37e2d4c40b = IDENTICAL); not in wheel",
            "attention_status": "cold (no git history)",
            "e9_payer": "Federation",
            "graph_tension_score": t(),
        },
        "evidence": {"sha12": "7b37e2d4c40b", "git_check_ignore": ".gitignore:54:*-report.json"},
        "tension_components": ["none"],
    },
    {
        "id": "N17",
        "path": "runtime-attestation-gap-report.json",
        "audit_disposition": "HOLD",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": ["generator: scripts/deployment_boundary_closure.py (audit-identified; the script's own docstring :6-8 lists three of its outputs)", "gitignored via .gitignore:54 -> UNTRACKED"],
            "runtime_shadow": "/opt/arifos/app/runtime-attestation-gap-report.json (sha12 c19a3cbc1eef = IDENTICAL); not in wheel",
            "attention_status": "cold (no git history)",
            "e9_payer": "Federation",
            "graph_tension_score": t(),
        },
        "evidence": {"sha12": "c19a3cbc1eef", "git_check_ignore": ".gitignore:54:*-report.json"},
        "tension_components": ["none"],
    },
    {
        "id": "N18",
        "path": "reachability-report.json",
        "audit_disposition": "HOLD",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": ["generator: scripts/reachability_analysis.py (audit-identified)", "gitignored via .gitignore:54 -> UNTRACKED"],
            "runtime_shadow": "/opt/arifos/app/reachability-report.json (sha12 680523160506 = IDENTICAL); not in wheel",
            "attention_status": "cold (no git history)",
            "e9_payer": "Federation",
            "graph_tension_score": t(),
        },
        "evidence": {"sha12": "680523160506", "git_check_ignore": ".gitignore:54:*-report.json"},
        "tension_components": ["none"],
    },
    {
        "id": "N19",
        "path": "repo-inventory.json",
        "audit_disposition": "HOLD (audit listed generator as UNKNOWN)",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "GENERATOR NOW IDENTIFIED: scripts/repo_inventory.py:5 'Produces repo-inventory.json: disposition buckets + entropy signals + migration plan'; :17 OUT = os.path.join(ROOT, 'repo-inventory.json')",
                "gitignored by NAME: .gitignore:55 'repo-inventory.json' -> UNTRACKED",
                "the generator itself lists '.arifos' as a scanned dir: scripts/repo_inventory.py:31",
            ],
            "runtime_shadow": "/opt/arifos/app/repo-inventory.json (sha12 1df230270d86 = IDENTICAL); not in wheel",
            "attention_status": "cold (no git history)",
            "e9_payer": "Future agent",
            "graph_tension_score": t(refuted=0),
        },
        "evidence": {
            "sha12": "1df230270d86",
            "content_head": "disposition_buckets {ARCHIVE:2, DELETE_AFTER_PROOF:59, GENERATE:6, KEEP_CANON:1, KEEP_RUNTIME:18, MIGRATE:32, UNKNOWN_HOLD:4300}; generated_at 2026-09-15T21:46:20Z; root /root/arifOS",
            "git_check_ignore": ".gitignore:55:repo-inventory.json",
        },
        "audit_claim_check": {
            "claim": "audit unknowns[]: '4 top-level report JSONs whose generator scripts were not identified (repo-inventory.json, ...)'",
            "verdict": "RESOLVED - generator identified",
            "finding": "scripts/repo_inventory.py:17 is the writer. Note its content is itself a prior entropy audit: UNKNOWN_HOLD=4300 dwarfs every other bucket, i.e. an earlier pass classified 4300 files as 'unknown, hold'. That is a standing E2/E3 signal - a 4300-item unresolved bucket is a large latent attention cost, and this graph covers only 22 nodes of it.",
        },
        "tension_components": ["none scoring; flagged for the 4300-item UNKNOWN_HOLD bucket it records"],
    },
    {
        "id": "N20",
        "path": "package-origin-report.json",
        "audit_disposition": "HOLD (audit listed generator as UNKNOWN)",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "GENERATOR NOW IDENTIFIED: scripts/deployment_boundary_closure.py:348 open(os.path.join(ROOT,'package-origin-report.json'),'w'); script docstring :8 lists it as output 3 of 3",
                "gitignored via .gitignore:54 -> UNTRACKED",
            ],
            "runtime_shadow": "/opt/arifos/app/package-origin-report.json (sha12 9d5a05f0ac47 = IDENTICAL); not in wheel",
            "attention_status": "cold (no git history)",
            "e9_payer": "Federation",
            "graph_tension_score": t(),
        },
        "evidence": {
            "sha12": "9d5a05f0ac47",
            "content_head": "records PWD=/opt/arifos/app, PYTHONPATH=/opt/arifos/app, PYTHONNOUSERSITE=1, dist_info_generations=[multidict-6.7.1, hyperframe-6.1.1, dnspython-2.8.0, cffi-2.1.1, ...]",
            "git_check_ignore": ".gitignore:54:*-report.json",
        },
        "audit_claim_check": {
            "claim": "generator unknown",
            "verdict": "RESOLVED - scripts/deployment_boundary_closure.py:348",
            "finding": "This file is EVIDENCE, not debris: it captures the deployed runtime's env (PYTHONPATH=/opt/arifos/app) at generation time. That env is the very thing this graph's E7 analysis depends on. Recommend it be treated as witness material (Federation audit trail) rather than a cleanup target - deleting it destroys a provenance record of the deployment boundary.",
        },
        "tension_components": ["none; E9 note: this is audit-trail witness material"],
    },
    {
        "id": "N21",
        "path": "import-origin-report.json",
        "audit_disposition": "HOLD (audit listed generator as UNKNOWN)",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "GENERATOR NOW IDENTIFIED: scripts/deployment_boundary_closure.py:334; docstring :6 lists it as output 1 of 3",
                "gitignored via .gitignore:54 -> UNTRACKED",
            ],
            "runtime_shadow": "/opt/arifos/app/import-origin-report.json (sha12 0a26782dd732 = IDENTICAL); not in wheel",
            "attention_status": "cold (no git history)",
            "e9_payer": "Federation",
            "graph_tension_score": t(),
        },
        "evidence": {
            "sha12": "0a26782dd732",
            "content_head": "active_sot {active:true, forged_at:2026-07-31T22:30:00Z, path:/root/A-FORGE/forge_work/2026-07-17/APEX-CONCORDANCE-17072026/apex-sot-v2.json, sot_hash:sha256:7146d160e0bc33bed9516cbe..., kernel_reported:true, operational:true}",
            "cross_check": "the live kernel /health reports the SAME active_sot.path (/root/A-FORGE/forge_work/2026-07-17/APEX-CONCORDANCE-17072026/apex-sot-v2.json) - so this report and the running kernel agree as of probe time",
            "git_check_ignore": ".gitignore:54:*-report.json",
        },
        "audit_claim_check": {
            "claim": "generator unknown",
            "verdict": "RESOLVED - scripts/deployment_boundary_closure.py:334",
            "finding": "Cross-validated against the live kernel: this file's active_sot.path matches /health's .active_sot.path exactly. It is a corroborating witness record of import origin, not stale debris.",
        },
        "tension_components": ["none"],
    },
    {
        "id": "N22",
        "path": "execution-roots-report.json",
        "audit_disposition": "HOLD (audit listed generator as UNKNOWN)",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "GENERATOR NOW IDENTIFIED: scripts/deployment_boundary_closure.py:341; docstring :7 lists it as output 2 of 3",
                "gitignored via .gitignore:54 -> UNTRACKED",
            ],
            "runtime_shadow": "/opt/arifos/app/execution-roots-report.json (sha12 a6294bb81aad = IDENTICAL); not in wheel",
            "attention_status": "cold (no git history)",
            "e9_payer": "Federation",
            "graph_tension_score": t(),
        },
        "evidence": {
            "sha12": "a6294bb81aad",
            "content_head": "class_counts {AUTHORIZED_RELEASE_ROOT:11, DEVELOPMENT_ROOT:87, REPO_COPY_ROOT:5, UNKNOWN_ROOT:31}; generated_at 2026-09-15T21:56:23Z; sample root entry class UNKNOWN_ROOT command 'ExecStart=/opt/arifos/venv/bin/python /o...'",
            "git_check_ignore": ".gitignore:54:*-report.json",
        },
        "audit_claim_check": {
            "claim": "generator unknown",
            "verdict": "RESOLVED - scripts/deployment_boundary_closure.py:341",
            "finding": "Its content directly corroborates this graph's E7 finding: 87 DEVELOPMENT_ROOT + 5 REPO_COPY_ROOT + 31 UNKNOWN_ROOT execution roots vs only 11 AUTHORIZED_RELEASE_ROOT. It also records an ExecStart pointing at /opt/arifos/venv (a venv path that is NOT the current /opt/arifos/current/venv), i.e. historical evidence of the same multi-tree divergence measured live in this pass.",
        },
        "tension_components": ["none scoring; high corroborative value for E7"],
    },
    {
        "id": "N23",
        "path": "build-info.json",
        "audit_disposition": "HOLD (audit: 'explicitly gitignored')",
        "audit_confidence": 0.85,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [],
            "authority_claims": [
                "gitignored by NAME with a stated reason: .gitignore:308-309 '# Generated build metadata (regenerated by CI)' / 'build-info.json'",
                "audit already recorded this: 'build-info.json -> .gitignore line 309' - CONFIRMED at .gitignore:309",
            ],
            "runtime_shadow": "/opt/arifos/app/build-info.json (sha12 d26335eb01b6 = IDENTICAL) BUT deployed wheel build-info.json = sha12 8a3e6bbebe2a -> DIVERGENT (expected: wheel copy is regenerated at build time)",
            "attention_status": "warm-ish (git_last 2026-09-15 = 15d, 3 commits/30d, 4 commits/180d) - NOTE: git history exists for a file .gitignore declares ignored, i.e. it was committed before the ignore rule and remains tracked-adjacent",
            "e9_payer": "Federation",
            "graph_tension_score": t(run=0),
        },
        "evidence": {"src_sha12": "d26335eb01b6", "deployed_sha12": "8a3e6bbebe2a", "git_check_ignore": ".gitignore:309:build-info.json"},
        "audit_claim_check": {
            "claim": "'Git-tracked but .gitignore has *-report.json pattern (suggests intent to exclude). build-info.json explicitly gitignored.'",
            "verdict": "PARTIALLY REFUTED",
            "finding": "'Git-tracked' is FALSE for all 9 JSONs in this cohort: every one is UNTRACKED (git ls-files --error-unmatch fails; git check-ignore -v matches a rule for each). The ignore intent the audit inferred from the pattern is already fully implemented - there is no tracked/untracked contradiction to resolve. build-info.json is the only one whose src/deployed sha legitimately differs, and that is correct behaviour for a CI-regenerated artifact, not drift.",
        },
        "tension_components": ["none: src-vs-wheel divergence here is by design (regenerated by CI)"],
    },
    # ---- VISION_ORGAN ----
    {
        "id": "N24",
        "path": "VISION_ORGAN/",
        "audit_disposition": "HOLD",
        "audit_confidence": 0.60,
        "edges": {
            "static_imports": [],
            "dynamic_loads": [
                "NO importer and NO importlib/__import__ hit for any VISION_ORGAN module (probe returned empty for the path token outside the directory itself)",
                "internally self-executing only: VISION_ORGAN/organ_pipeline.py:121 instantiates VisionOrganPipeline(budget_usd=0.005) under a __main__-style block; class defined at :19",
            ],
            "authority_claims": [
                "self-declared owner: VISION_ORGAN/schemas/VISION_INVOKE_DESIGN.md:6 'Owner: VISION_ORGAN / arifOS Federation' - the ONLY non-audit mention of the string 'VISION_ORGAN' outside the directory itself",
                "has a SKILL.md (VISION_ORGAN/SKILL.md) and versioning policy (VISION_ORGAN/schemas/VERSIONING_POLICY.md) but NO registry entry, NO CI workflow, NO Makefile target found",
                "12 files TRACKED in git (git ls-files VISION_ORGAN | wc -l = 12); 16 files on disk (4 untracked, incl. ledger/vision-jobs.jsonl)",
                "already F13-held once: /root/AAA/reports/STAB-2026-09-16/ACTION-LEDGER.md:290",
            ],
            "runtime_shadow": "/opt/arifos/app/VISION_ORGAN = DIR (present); NOT in deployed wheel (dep=-) -> cannot be imported by the running kernel",
            "attention_status": "active (git_last 2026-09-09 = 21d, 3 commits/30d, 3 commits/180d - all of its history is in the last 30 days)",
            "e9_payer": "Future agent",
            "graph_tension_score": t(refuted=1),
        },
        "evidence": {
            "file_inventory": "organ_pipeline.py, SKILL.md, schemas/{vision-invoke-v1.0.0.json, VISION_INVOKE_DESIGN.md, vision-invoke-output-v1.0.0.json, scene-contract.schema.json, ADAPTER_SPECS.md, VERSIONING_POLICY.md, vision-invoke-error-taxonomy-v1.0.0.json, vision_invoke_pydantic_v1.py}, compiler/compile_contract.py, policy/budget_guard.py, adapters/{qwen_vision.py, minimax_image01.py}, ledger/{vision-jobs.jsonl, vision_job_ledger.py}",
            "inbound_scan": "grep -rn -iE 'vision_organ|visionorgan' excluding VISION_ORGAN/ itself -> 0 hits outside the directory",
            "mission_router_scan": "arifosmcp/mission_router.py exists (25644 bytes, mtime Sep 23 07:35); grep -in 'vision' arifosmcp/mission_router.py -> 0 hits",
        },
        "audit_claim_check": {
            "claim": "static_references: ['arifosmcp/mission_router.py (1 reference)']; notes '15 files, 1 reference in mission_router.py. Recently touched (Sep 8). HOLD - may be actively developed vision organ code.' confidence 0.60",
            "verdict": "REFUTED - the claimed edge DOES NOT EXIST",
            "finding": "mission_router.py contains zero occurrences of 'vision' in any case. The audit's sole cited reference is a phantom edge - the same failure class as N08's phantom path, in the same audit. Corrected picture: 16 files on disk / 12 tracked, with ZERO inbound references from anywhere in the repo. It is an ISLAND, not a wired organ. Two readings are both consistent with the evidence and they imply opposite dispositions, so this node must not be metabolized on the graph alone: (a) unwired work-in-progress - all 3 of its commits fall inside the last 30 days, matching the audit's 'actively developed' intuition; (b) stranded capability - complete-looking contract surface (versioned schemas, error taxonomy, budget guard, two provider adapters, a jobs ledger with entries) that nothing can invoke, and that is absent from the deployed wheel so the running kernel cannot reach it even in principle. Distinguishing (a) from (b) requires the author's intent, which is not in the filesystem.",
        },
        "tension_components": [
            "audit_claim_refuted: phantom edge (mission_router.py reference does not exist)",
            "capability_without_route: complete contract surface, no caller, not in wheel -> E4 (capability exists, owner/route unclear)",
        ],
    },
]

# ---- DERIVED, not hardcoded: edge totals + ranking computed from the nodes ----
# A first draft hardcoded these and disagreed with the per-node scores. Recomputed.
def _edge_totals(ns):
    def cnt(key):
        return sum(len(n["edges"].get(key) or []) for n in ns if isinstance(n["edges"].get(key), list))

    def cnt_present(key):
        return sum(1 for n in ns if n["edges"].get(key) not in (None, "", [], {}))

    return {
        "static_import_edges": cnt("static_imports"),
        "dynamic_load_edges": cnt("dynamic_loads"),
        "authority_claim_edges": cnt("authority_claims"),
        "runtime_shadow_edges_present": cnt_present("runtime_shadow"),
        "runtime_shadow_edges_null": sum(1 for n in ns if n["edges"].get("runtime_shadow") is None),
        "attention_edges": cnt_present("attention_status"),
        "e9_payer_edges": cnt_present("e9_payer"),
        "nodes_with_audit_claim_check": sum(1 for n in ns if "audit_claim_check" in n),
        "audit_claims_refuted": sum(
            1 for n in ns if str(n.get("audit_claim_check", {}).get("verdict", "")).startswith("REFUTED")
        ),
        "audit_claims_confirmed": sum(
            1 for n in ns if str(n.get("audit_claim_check", {}).get("verdict", "")).startswith("CONFIRMED")
        ),
        "audit_claims_partially_confirmed_or_corrected": sum(
            1
            for n in ns
            if str(n.get("audit_claim_check", {}).get("verdict", "")).startswith(("PARTIALLY", "RESOLVED"))
        ),
    }


# one-line rationale per scored node (kept separate so ranking stays derived)
REASONS = {
    "N14": "deployed wheel reads this SOURCE-tree file at runtime for security-sensitive risk gating; loader fails open to {'status':'missing'}; inverts the 'wheel = sole production artifact' packaging doctrine",
    "N13": "source vs deployed-wheel manifests advertise two different tool contracts (KERNEL 666 vs KERNEL 888 verdict; judge vs intercept schemas) on the PUBLIC Smithery surface; drift guard RED since <=2026-09-21",
    "N12": "two non-identical files under one name, 54 inbound refs in 4 inconsistent link forms incl. 7 GENESIS constitutional docs, no canonical declaration",
    "N02": "audit's ARCHIVE target is the ONLY F13-ratified sovereign-sealed doc of the pair (SEAL a624ba3d77796cd8); its clean-cased twin is DRAFT-NOT-RATIFIED; both untracked+gitignored so no rollback path",
    "N08": "PHANTOM NODE - path never existed in git; real file is .arifos/adam_agent.py (tracked); acting on the audit path silently no-ops",
    "N03": "the DRAFT-NOT-RATIFIED twin of N02; same untracked+gitignored no-rollback condition; the tension lives in the N02<->N03 EDGE, not in either node",
    "N01": "stub itself is inert, but kernel_mcp.py:50 imports a nonexistent third path arifosmcp.core.cooling_ledger and swallows the ModuleNotFoundError into CoolingLedger=None",
    "N24": "audit's sole cited edge (mission_router.py) does not exist; complete contract surface with zero callers and absent from the deployed wheel",
    "N09": "'zero references' is false - 23 string refs incl. a git branch identity used as a deploy_ref in docs/architecture/DEPLOYMENT.md:110",
    "N05": "docs/ARCHITECTURE_TRUTH.md:161 claims 562 files and docs/AGENT_STATE.md:123 claims 118MB; measured 1 file / 12K - two live docs are false and outlive the directory",
}

EDGE_TOTALS = _edge_totals(nodes)

# explicit deterministic tiebreak: score desc, then escalation-required first, then id asc.
# (An earlier version left ties to insertion order, which disagreed with a score-desc/id-desc
#  verifier sort. Tiebreak is now written down once and used by both sides.)
ESCALATION_IDS = {"N02", "N03", "N12", "N13", "N14", "N24"}


def _rank_key(n):
    return (-n["edges"]["graph_tension_score"], 0 if n["id"] in ESCALATION_IDS else 1, n["id"])


RANKED = sorted(nodes, key=_rank_key)
TOP = [n for n in RANKED if n["edges"]["graph_tension_score"] > 0]
PAYER_DIST = {}
for n in nodes:
    PAYER_DIST[n["edges"]["e9_payer"]] = PAYER_DIST.get(n["edges"]["e9_payer"], 0) + 1

graph = {
    "produced_by": "claude-code/FI-002 - 333-reasoning subagent (capability graph build), Trinity 333 lane",
    "produced_at": "2026-09-30T13:41:45Z",
    "audit_source": "/root/arifOS/entropy-audit-2026-09-17.json",
    "audit_source_sha": "a033a0dab37ff0b71b53c23847454afd4430fb6f (audit's own git_sha, 2026-09-17T16:28:49Z)",
    "scope": "24 nodes covering the 16 declared candidates (TRACKED_DEBRIS 6 + INVESTIGATE 3 + HOLD 7, with the HOLD cohort's 'top-level report JSONs (8 files)' expanded per-file and .arifos/REALITY_LAWS.md promoted to a first-class node). KEEP skipped: formal/, GENESIS/, npm-wrapper/.",
    "node_count_reconciliation": "The task enumerated 16 candidates but its own numbering ran to 22 (items 14-21 are the 8 report JSONs). The audit file itself carries them as ONE entry, giving 15 non-KEEP audit entries. This graph emits 24 nodes: 22 from expanding the report JSONs, +N03 (.arifos/REALITY_LAWS.md, the counterpart the audit named but did not node-ify) and +N23 (build-info.json, listed in the audit's evidence but outside its '8 files' count). Every node is individually evidenced.",
    "graph_construction_method": "static filesystem probe + dynamic string scan + LIVE runtime probe (3 trees) + git attention history + deployed-venv behavioural execution. Read-only; no tracked file modified in any tree.",
    "live_runtime_probed": "yes",
    "nodes": nodes,
    "runtime_topology": {
        "three_distinct_trees": [
            {
                "role": "SOURCE",
                "path": "/root/arifOS",
                "git_head": "21f6de1062842934c99fe3f868a91721b0ec6ab7",
                "git_head_date": "2026-09-30 18:13:55 +0800",
                "git_head_subject": "docs(registry): stop tool_registry.json claiming a derivation that would corrupt it, and pin the divergence",
                "tracked_modifications": 0,
                "note": "13 days AHEAD of the audit's pinned sha a033a0da (2026-09-17) - the audit baseline is stale relative to current HEAD",
            },
            {
                "role": "RUNTIME WORKING TREE (systemd WorkingDirectory)",
                "path": "/opt/arifos/app",
                "is_symlink": False,
                "readlink_f": "/opt/arifos/app (a real directory, NOT a symlink to source)",
                "git_head": "0e8e66a4869814e08e9bf6bcacbe3bd1afb53559",
                "git_head_date": "2026-09-28 12:37:02 +0800",
                "git_head_subject": "fix(arifosmcp/crypto_auth): assemble redis URL from REDIS_PASSWORD when ARIFOS_REDIS_URL unset",
                "dirty_files": ["arifosmcp/static/llms.txt", "llms.txt", "static/llms.txt"],
                "note": "2 days BEHIND source HEAD; 3 pre-existing dirty files (present before this probe began and unchanged by it)",
            },
            {
                "role": "DEPLOYED WHEEL (what the live kernel actually imports)",
                "path": "/opt/arifos/current/venv/lib/python3.13/site-packages",
                "dist_version": "arifos 1!2026.9.6 (arifos-1!2026.9.6.dist-info); arifosmcp has NO dist metadata ('No package metadata was found for arifosmcp')",
                "wheel_built": "2026-09-30 18:14 (/opt/arifos/releases/arifos-1!2026.9.6-py3-none-any.whl)",
                "deployed_commit_stamp": "21f6de1062842934c99fe3f868a91721b0ec6ab7 (/opt/arifos/releases/deployed-commit) == source HEAD",
                "no_pth_files": "no *.pth in site-packages -> sys.path is not being redirected by a path-config file",
            },
        ],
        "live_kernel_service": {
            "unit": "arifos.service",
            "MainPID": 2552760,
            "exe": "/usr/bin/python3.13",
            "cwd": "/var/lib/arifos (systemd override; the stock unit declares WorkingDirectory=/opt/arifos/app)",
            "cmdline": "/opt/arifos/current/venv/bin/python -c 'from arifosmcp.runtime.__main__ import main; main()'",
            "PYTHONPATH": "unset in the service environment (no PYTHONPATH line in /proc/2552760/environ) -> import origin is decided by the venv, not by cwd",
            "health_runtime_import_path": "/opt/arifos/current/venv/lib/python3.13/site-packages/arifosmcp/__init__.py",
            "health_deployment_drift_status": "aligned",
            "health_source_commit": "21f6de1",
            "health_deployed_commit": "21f6de1062842934c99fe3f868a91721b0ec6ab7",
            "health_software_release_drift": False,
            "health_origin_enforced": True,
            "health_release_name": "v1!2026.9.6",
        },
        "import_origin_is_cwd_dependent": {
            "finding": "Module resolution differs by cwd, which is why a naive probe misreports origin.",
            "measurements": [
                "cwd=/tmp, deployed venv python -> arifosmcp loads from site-packages (the wheel)",
                "cwd=/opt/arifos/app, deployed venv python -> arifosmcp loads from /opt/arifos/app/arifosmcp/__init__.py (the runtime working tree shadows the wheel via sys.path[0]='')",
                "cwd=/root/arifOS, ANY python (incl. /usr/bin/python3) -> arifosmcp loads from /root/arifOS/arifosmcp/__init__.py (source shadows everything)",
            ],
            "methodology_note": "An early probe in this pass ran with cwd=/root/arifOS and falsely reported the source tree as the import origin. It was re-run from a neutral cwd (/tmp) before any conclusion was drawn. Per scar-edited-source-not-live-binary-2026-09-27, import-origin claims are only admissible from a neutral cwd.",
        },
        "divergence_verdict": "The kernel's own /health reports deployment_drift_status='aligned' and runtime_drift=False, and the deployed-commit stamp does equal source HEAD. That self-report is TRUE for the Python package and FALSE for two non-Python artifacts measured in this pass: smithery.yaml (source sha ad074201ecd2b883 vs wheel sha d8b8b8a02b73f1ff, materially different tool contracts) and risk_leash.yaml (wheel code reads the SOURCE-tree file at runtime). The kernel's drift sensor does not cover generated manifests or runtime config loaded by absolute path.",
    },
    "tension_scoring_model": {
        "principle": "graph_tension_score is DECOMPOSED into named binary components so 555-ASI can falsify any single component instead of arguing with an opaque number. It is a heuristic ordering device, NOT a measurement of entropy.",
        "components": {
            "authority_conflict": 3,
            "runtime_coupling": 3,
            "silent_failure": 2,
            "audit_claim_refuted": 2,
            "no_rollback_path": 1,
            "high_inbound_refs": 1,
        },
        "formula": "score = min(10, 3*authority_conflict + 3*runtime_coupling + 2*silent_failure + 2*audit_claim_refuted + 1*no_rollback_path + 1*high_inbound_refs)",
        "authority_conflict_def": "two or more artifacts claim canonical status over the same referent with no machine-readable supersession pointer",
        "runtime_coupling_def": "deployed runtime reads/diverges from the source tree in a way no CI gate or attestation observes",
        "silent_failure_def": "removal or corruption degrades behaviour without raising (swallowed exception, fail-open default, no-op path)",
        "audit_claim_refuted_def": "a specific evidence claim in entropy-audit-2026-09-17.json is contradicted by direct probe",
        "no_rollback_path_def": "artifact is untracked AND gitignored, so git cannot restore it (F1 AMANAH gap)",
        "high_inbound_refs_def": ">20 inbound references from other artifacts",
    },
    "edge_totals": EDGE_TOTALS,
    "tension_summary": {
        "ranking_is_derived": "highest_tension_nodes is COMPUTED from the per-node graph_tension_score values (sorted desc), not hand-written. An earlier draft hardcoded 9 for N02/N14 while the component formula produced 6 and 8; the formula is authoritative and the summary now derives from it.",
        "highest_tension_nodes": [
            {"id": n["id"], "path": n["path"], "score": n["edges"]["graph_tension_score"],
             "e9_payer": n["edges"]["e9_payer"],
             "components": n.get("tension_components", []),
             "reason": REASONS[n["id"]]}
            for n in TOP
        ],
        "silent_failure_candidates": [
            {"id": "N14", "mechanism": "arifosmcp/tools/health.py:180 returns {'status':'missing'} instead of raising; a deleted/edited risk leash degrades to one health-report line, and the deployed wheel reads the SOURCE path so no redeploy is needed for the change to take effect"},
            {"id": "N01", "mechanism": "arifosmcp/kernel_mcp.py:50 try/except Exception -> CoolingLedger = None; ModuleNotFoundError on arifosmcp.core.cooling_ledger is swallowed, verified live in the deployed venv"},
            {"id": "N08", "mechanism": "acting on the audit's phantom path arifosmcp/.arifos/adam_agent.py succeeds vacuously (nothing to remove) while the real tracked file .arifos/adam_agent.py survives unexamined"},
            {"id": "N24", "mechanism": "VISION_ORGAN is absent from the deployed wheel, so no runtime error can ever surface its non-integration; it looks complete on disk and is unreachable in principle"},
            {"id": "N13", "mechanism": "smithery.yaml passes .github/workflows/floor_gate.yml:29-30 (valid YAML) while its CONTENT diverges from source - the CI gate validates parseability, not agreement, so the drift is invisible to CI"},
        ],
        "live_runtime_divergence_detected": True,
        "live_runtime_divergence_detail": {
            "kernel_self_report": "deployment_drift_status='aligned', software_release.drift=False, runtime_drift=False, origin_enforced=True - and this is CORRECT for the Python package (deployed-commit stamp == source HEAD 21f6de10)",
            "actual_divergences_found": [
                "smithery.yaml: source sha16 ad074201ecd2b883 != deployed-wheel sha16 d8b8b8a02b73f1ff; drift guard scripts/sync_kernel_abi.py --check reproduces 'Kernel ABI drift: smithery.yaml' live",
                "risk_leash.yaml: all three trees carry identical bytes (ef3ea55161f6) but the deployed wheel's loader cannot find its own packaged copy (parents[3] -> /opt/arifos/current/venv/lib/python3.13/risk_leash.yaml, nonexistent) and falls through to /root/arifOS/risk_leash.yaml -> the source tree is a live runtime dependency of the deployed kernel",
                "/opt/arifos/app: git HEAD 0e8e66a4 (2026-09-28) is 2 days behind source HEAD 21f6de10 (2026-09-30), with 3 dirty llms.txt files",
                "build-info.json: source d26335eb01b6 vs wheel 8a3e6bbebe2a - divergence is BY DESIGN (CI-regenerated per .gitignore:308), recorded for completeness, not scored as tension",
            ],
            "blind_spot": "The kernel's drift sensor compares Python package provenance only. It does not cover (a) generated manifests shipped in the wheel, or (b) config files the deployed code loads by absolute source path. Both blind spots are exercised by nodes in this graph.",
        },
    },
    "audit_quality_findings": {
        "note": "The 2026-09-17 audit is the input to this pipeline, so its own defect rate is a first-class finding. 9 of its evidence claims are refuted or materially corrected by direct probe.",
        "phantom_evidence_instances": [
            {"id": "N08", "claim": "candidate path 'arifosmcp/.arifos/adam_agent.py'", "reality": "path never existed; real path .arifos/adam_agent.py; git log --all -- <claimed path> is EMPTY"},
            {"id": "N24", "claim": "static_references ['arifosmcp/mission_router.py (1 reference)']", "reality": "grep -in 'vision' arifosmcp/mission_router.py -> 0 hits"},
        ],
        "authority_inversion": [
            {"id": "N02/N03", "claim": "REAlITY_LAWS.md is a 'filename typo' to ARCHIVE", "reality": "it is the F13-RATIFIED doc; the clean-cased twin is DRAFT-NOT-RATIFIED. The disposition inverts authority."},
        ],
        "tracking_status_false": [
            {"id": "N15-N23", "claim": "'Git-tracked but .gitignore has *-report.json pattern (suggests intent to exclude)'", "reality": "all 9 are UNTRACKED and matched by .gitignore:54/55/56/309. The exclude intent is already fully implemented."},
        ],
        "understated_nodes": [
            {"id": "N12", "claim": "static_references [], confidence 0.70, 'may serve as legal notice'", "reality": "54 inbound refs, two non-identical files, 7 GENESIS constitutional links - the densest authority knot in the graph"},
            {"id": "N14", "claim": "'may be consumed ... verify if consumed at runtime before any action', confidence 0.65", "reality": "CONFIRMED consumed, and by the deployed wheel reading the source tree - the audit's own precondition is discharged with a worse answer than expected"},
            {"id": "N09", "claim": "'Zero references'", "reality": "23 string references across tests/, docs/, static/, commands/"},
        ],
        "overstated_nodes": [
            {"id": "N05", "claim": "docs say 562 files/118MB (audit repeated the 'shell' framing correctly, but did not flag the false docs)", "reality": "1 file, 12K; docs/ARCHITECTURE_TRUTH.md:161 and docs/AGENT_STATE.md:123 are both false"},
        ],
        "resolved_unknowns": [
            "audit unknowns[0] arifosmcp/.arifos/adam_agent.py -> RESOLVED: phantom path; real file .arifos/adam_agent.py = ADAM Agent (Omega Heart) autoresearch stability/readability/cooling checker, 137 lines, tracked",
            "audit unknowns[1] .arifos/autoresearch.py -> RESOLVED: 344-line CLI Trinity loop orchestrator (ARIF->ADAM->APEX) with NPV/convexity guards; name also denotes git branch autoresearch/2026-04-22 cited as a deploy_ref",
            "audit unknowns[2] .collab/COLLAB.md -> RESOLVED: 90-line dated collaboration log (2026-06-05) recording the FederationEnvelope v1.1 contract; no consumer found in /root/AAA, /root/A-FORGE, /root/scripts, /root/.claude",
            "audit unknowns[3] 4 unidentified report generators -> ALL RESOLVED: repo-inventory.json <- scripts/repo_inventory.py:17; package-origin-report.json <- scripts/deployment_boundary_closure.py:348; import-origin-report.json <- scripts/deployment_boundary_closure.py:334; execution-roots-report.json <- scripts/deployment_boundary_closure.py:341",
        ],
        "net_assessment": "The audit's DISPOSITIONS are broadly defensible; its EVIDENCE is not. 4 of 15 non-KEEP entries carry at least one false or materially understated evidence claim, including 2 phantom edges. Any metabolizer that trusts the audit's evidence fields without re-probing will act on at least two nodes that do not exist as described.",
    },
    "structural_findings": {
        "tracked_inside_ignored_dir": {
            "finding": ".gitignore:90 declares '.arifos/' ignored, yet git ls-files .arifos/ returns 11 TRACKED files (EQUATIONS.md, SUBSTRATE_REFERENCE_LAYER.md, adam_agent.py, apex_judge.py, arif_agent.py, autoresearch.py, metrics.py, root-entropy-audit-2026-06-20.md, substrate-coded-reality-map-2026-06-20.md, substrate-gap-map-2026-06-20.md, vault_seal.py) against 16 files on disk.",
            "consequence": "The ignore rule is inert for those 11 (git ignore does not apply to already-tracked paths). So .arifos/ is simultaneously 'ignored internals' and 'tracked canon' - which is exactly why the two REALITY_LAWS files inside it have NO git history and NO rollback path while their siblings do. Two files in one directory carry opposite reversibility guarantees.",
            "e9_payer": "Continuity",
        },
        "no_rollback_path_nodes": [
            ".arifos/REAlITY_LAWS.md (untracked + .gitignore:90)",
            ".arifos/REALITY_LAWS.md (untracked + .gitignore:90)",
        ],
        "cooling_ledger_three_way_name_collision": {
            "claimants": [
                "core/cooling_ledger.py - 8-line stub, sha12 7cf1a421be97, class CoolingLedger, sole method record_sabar, ZERO callers",
                "arifosmcp/cooling_ledger.py - 462-line real Postgres impl, sha12 5055c288d282, CoolingLedgerError:51 / CoolingLedgerClient:67 / CoolingLedgerSession:394",
                "arifosmcp.core.cooling_ledger - referenced at arifosmcp/kernel_mcp.py:50, DOES NOT EXIST (arifosmcp/core/ has 14 dirs, no cooling_ledger.py)",
                "supabase/migrations/20260628_001_cooling_ledger_core.sql:19 - a Postgres SCHEMA named cooling_ledger (the substrate the 462-line impl targets)",
                "arifosmcp/runtime/cooling_ledger_chain.py:5 - explicitly distinguishes itself: 'seal_chain_ref. Distinct from the Postgres CoolingLedgerClient substrate'",
            ],
            "finding": "Five artifacts share the 'cooling ledger' name across four different substrates (Python stub, Python real, phantom Python module, SQL schema, plus a chain module that must disclaim confusion). The audit saw two of the five. This is the graph's clearest instance of EUREKA::GRAPH_TENSION_THEORY::v1 - the entropy is in the NAME COLLISION, not in any single file, so deleting the stub does not resolve it.",
            "e9_payer": "Future agent",
        },
        "cross_repo_canonical_dependency": {
            "finding": "organ.yaml:1 surrenders canonicality to /root/AAA/organ.yaml - a file OUTSIDE this git repo. The in-repo artifact is a pointer to an out-of-repo authority, so this repo's git history cannot witness changes to its own declared canonical topology.",
            "e9_payer": "Federation",
        },
        "wheel_exclusion_not_honoured": {
            "finding": "deploy/fhs-map.yaml:57-58 lists 00_legacy_materials/ under packaging.exclude_from_wheel, yet the deployed wheel contains 00_legacy_materials/ (probe: dep=DIR). The packaging rule and the built artifact disagree.",
            "e9_payer": "Federation",
        },
    },
    "e9_payer_distribution": {
        "counts_derived_from_nodes": PAYER_DIST,
        "Arif": PAYER_DIST.get("Arif", 0),
        "888 APEX": PAYER_DIST.get("888 APEX", 0),
        "Federation": PAYER_DIST.get("Federation", 0),
        "Future agent": PAYER_DIST.get("Future agent", 0),
        "Continuity": PAYER_DIST.get("Continuity", 0),
        "note": "DERIVED counts are authoritative: %s. No node was scored payer='Arif' and none payer='Continuity' - Continuity appears only in structural_findings (the tracked-inside-ignored .arifos/ contradiction and the cross-repo organ.yaml pointer), which are graph-level properties rather than single nodes, so they carry no node-level payer. An earlier hand-written draft claimed 'Continuity: 2'; that was wrong and is corrected by deriving the counts. Two nodes carry an F13-class sovereign decision that only Arif can make, but the CONSEQUENCE of getting them wrong lands on 888 APEX and Federation respectively: N02/N03 (which REALITY_LAWS is law - a canonical-record binary) and N24 (VISION_ORGAN intent - a direction binary). Per the doctrine, E9='888 APEX' means ESCALATE, not clean."
        % json.dumps(PAYER_DIST, sort_keys=True),
        "escalation_rule": "escalate when e9_payer is in {888 APEX, Continuity}, OR when the node carries an unresolved F13-class binary (canonical-record choice / direction choice) that the filesystem cannot settle",
        "escalation_by_payer_derived": sorted(
            n["id"] for n in nodes if n["edges"]["e9_payer"] in ("888 APEX", "Continuity")
        ),
        "escalation_by_unresolved_f13_binary": {
            "N02": "canonical-record binary: which REALITY_LAWS is law (Arif's ratification, not a filename heuristic)",
            "N03": "same binary as N02 - the pair is one decision",
            "N13": "direction binary: is the 33/13 renumbering the intended public ABI, or is the deployed numbering correct? Determines whether source or wheel gets regenerated",
            "N14": "irreversible-mutation class: this file gates deployed risk behaviour; any edit is a live constitutional change with no redeploy step",
            "N24": "direction binary: unwired work-in-progress vs stranded capability - observationally identical, opposite actions",
            "N12": "canonical-record binary: two non-identical files under one name are linked from 7 GENESIS constitutional docs; consolidating means editing up to 54 inbound references across canonical material",
        },
        "escalation_required_nodes": sorted(ESCALATION_IDS),
        "escalation_reconciliation": "escalation_by_payer_derived (888 APEX/Continuity payers) is a SUBSET of escalation_required_nodes. N12/N13/N24 escalate on the second limb (unresolved F13-class binary touching canonical records, external contract, or direction) despite payer=Federation/Future agent. Both limbs are recorded separately above so 555-ASI can challenge either.",
    },
    "mutation_attestation": {
        "source_tree": "/root/arifOS - tracked_modified_count=0, HEAD unchanged at 21f6de106 before and after the full probe",
        "runtime_tree": "/opt/arifos/app - 3 dirty files (arifosmcp/static/llms.txt, llms.txt, static/llms.txt) PRESENT AT FIRST PROBE and unchanged at final attestation; HEAD unchanged at 0e8e66a48",
        "writes_performed": ["mkdir -p /root/.claude/skills/entropy-metabolizer/output", "this JSON file", "the builder script /root/.claude/skills/entropy-metabolizer/build_graph.py"]
    },
    "limits": [
        "static scan only; dynamic import via plugin systems not exhaustively traced - importlib/__import__/spec_from_file_location were grepped by candidate basename, but a plugin loader that constructs module names by string concatenation at runtime would not appear",
        "E9 payer assessment is heuristic, not authoritative - it encodes the doctrine's payer table, not a measured consequence",
        "graph_tension_score is a heuristic ordering device, not a measurement of entropy; it is decomposed into named components precisely so a component can be falsified without discarding the node",
        "attention_status for untracked nodes (.arifos/REAlITY_LAWS.md, .arifos/REALITY_LAWS.md, all 9 report JSONs) falls back to filesystem mtime, which is weak evidence - mtime does not record who touched a file or why, and a bulk copy resets it",
        "the audit's static_references for the 4 report JSONs whose generators it DID name (surface-evidence, semantic-closure, runtime-attestation-gap, reachability) were not re-verified; only the 4 'unknown' generators were confirmed",
        "N24 VISION_ORGAN's disposition cannot be resolved from the filesystem: 'unwired work-in-progress' and 'stranded capability' are observationally identical here and imply opposite actions. Author intent is required.",
        "no process-level confirmation of which .py files the live kernel (PID 2552760) has loaded: /proc/PID/maps and /proc/PID/fd returned no arifosmcp paths (normal - CPython mmaps then closes). Import origin is established from /health's runtime_import_path plus neutral-cwd venv probes, not from the process image.",
        "N15-N18 generator attribution is carried from the audit, not independently re-probed",
        "the live kernel /health endpoint was read but not mutated; no MCP tool call, no arif_judge, no arif_seal was invoked in this pass - this is a phase-1 graph build, not a verdict",
    ],
    "next_phase": "555-ASI verification + edge falsification",
    "recommended_verification_focus_for_555": [
        "PRIORITY 1 - falsify the authority inversion at N02/N03 before ANY metabolism touches .arifos/. Confirm by independent read that .arifos/REAlITY_LAWS.md:6 carries 'F13 RATIFIED | BINDING: YES | SEAL: a624ba3d77796cd8' and .arifos/REALITY_LAWS.md:3 carries 'STATUS: DRAFT - NOT RATIFIED', then locate SEAL a624ba3d77796cd8 in VAULT999 to confirm the ratification is real and not a self-asserted header string. A self-written 'F13 RATIFIED' header is not the same as a sealed record - this is the single check that decides whether the audit's ARCHIVE disposition is a documentation cleanup or the destruction of ratified law.",
        "PRIORITY 2 - falsify the N14 deployed->source runtime coupling independently. Re-run the deployed-venv probe from a neutral cwd and confirm _check_risk_leash() resolves to /root/arifOS/risk_leash.yaml. If confirmed, this is a live constitutional defect independent of any entropy question: the deployed kernel's risk gating depends on a mutable source-tree file, with no attestation and a fail-open default.",
        "PRIORITY 3 - re-derive the two phantom edges (N08 path, N24 mission_router reference) from the audit file itself and confirm the audit is the sole origin of both, so the correction is recorded against the artifact rather than against this graph.",
        "PRIORITY 4 - decide whether N13's smithery.yaml drift is source-ahead-of-wheel (renumbering landed in source, wheel not rebuilt) or wheel-ahead-of-source, by checking which of the two matches arifosmcp/abi/capability_registry.json - the file docs/MCP_SOURCE_OF_TRUTH.md:36 names as the actual machine authority.",
    ],
    "doctrine_compliance": {
        "E1_E9_decomposed": True,
        "scalar_remaining_entropy_reported": False,
        "auto_delete_of_tracked_files": False,
        "f13_hold_scaffolding_preserved": "no *.bak-version-drift-* artifact was touched; all 4 snapshots named in scar-2026-09-30-forgel-init-seal-refused-deployment-drift remain in place",
        "four_tests_applied_per_node": "capability / authority / attention / reality recorded as edge categories per node",
        "pipeline_stage": "DISCOVER+CLASSIFY+MAP (333 lane) complete; VERIFY (555) -> PRICE -> JUDGE (888) -> METABOLIZE (A-FORGE) -> WITNESS -> RE-MEASURE not started",
        "seal_claimed": False,
        "seal_note": "No SEAL is claimed by this artifact. Per apex_verdict_seal and the session precedent in session-final-honest-status-2026-09-27, a phase-1 graph build is a precondition for judgement, not a verdict.",
    },
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(graph, f, indent=2, ensure_ascii=False)
    f.write("\n")

# ---- self-verification ----
with open(OUT, encoding="utf-8") as f:
    back = json.load(f)
print("WROTE", OUT)
print("valid_json=True nodes=%d" % len(back["nodes"]))
ids = [n["id"] for n in back["nodes"]]
print("ids=", ",".join(ids))
print("duplicate_ids=", len(ids) != len(set(ids)))
missing = [n["id"] for n in back["nodes"] if set(n["edges"]) != {
    "static_imports", "dynamic_loads", "authority_claims", "runtime_shadow",
    "attention_status", "e9_payer", "graph_tension_score"}]
print("nodes_missing_required_edge_keys=", missing)
print("nodes_without_evidence=", [n["id"] for n in back["nodes"] if "evidence" not in n])
# re-derive the ranking INDEPENDENTLY of the builder (same documented tiebreak) and compare
ESC = set(back["e9_payer_distribution"]["escalation_required_nodes"])


def vkey(n):
    return (-n["edges"]["graph_tension_score"], 0 if n["id"] in ESC else 1, n["id"])


VORDER = [n["id"] for n in sorted(back["nodes"], key=vkey)]
VSORTED = sorted(back["nodes"], key=vkey)
print("top_tension=", [(n["edges"]["graph_tension_score"], n["id"]) for n in VSORTED][:5])
allscores = [n["edges"]["graph_tension_score"] for n in back["nodes"]]
print("score_range=", min(allscores), "..", max(allscores))
print("out_of_range_scores=", [n["id"] for n in back["nodes"] if not (0 <= n["edges"]["graph_tension_score"] <= 10)])

# ---- consistency assertions: summary must agree with nodes ----
errs = []
node_scores = {n["id"]: n["edges"]["graph_tension_score"] for n in back["nodes"]}
for row in back["tension_summary"]["highest_tension_nodes"]:
    if node_scores.get(row["id"]) != row["score"]:
        errs.append("summary score != node score for %s (%s vs %s)" % (row["id"], row["score"], node_scores.get(row["id"])))
summary_order = [r["id"] for r in back["tension_summary"]["highest_tension_nodes"]]
if summary_order != [i for i in VORDER if node_scores[i] > 0]:
    errs.append("summary ranking order %s != independently derived order %s" % (summary_order, [i for i in VORDER if node_scores[i] > 0]))
if len(summary_order) != len(set(summary_order)):
    errs.append("duplicate ids in highest_tension_nodes")
et = back["edge_totals"]
if et["e9_payer_edges"] != len(back["nodes"]):
    errs.append("e9_payer_edges %d != node count %d" % (et["e9_payer_edges"], len(back["nodes"])))
if et["attention_edges"] != len(back["nodes"]):
    errs.append("attention_edges %d != node count %d" % (et["attention_edges"], len(back["nodes"])))
if sum(back["e9_payer_distribution"]["counts_derived_from_nodes"].values()) != len(back["nodes"]):
    errs.append("payer distribution does not sum to node count")
if not all(isinstance(n["edges"]["graph_tension_score"], int) for n in back["nodes"]):
    errs.append("non-int tension score present")
for n in back["nodes"]:
    if n["edges"]["graph_tension_score"] > 0 and n["id"] not in REASONS:
        errs.append("scored node %s has no rationale in REASONS" % n["id"])
    if n["edges"]["graph_tension_score"] > 0 and not n.get("tension_components"):
        errs.append("scored node %s has no tension_components" % n["id"])
print("consistency_errors=", errs if errs else "NONE")
print("edge_totals=", json.dumps(et))
print("payer_dist=", json.dumps(back["e9_payer_distribution"]["counts_derived_from_nodes"]))
print("escalation_nodes=", back["e9_payer_distribution"]["escalation_required_nodes"])
print("ranking=", [(n["edges"]["graph_tension_score"], n["id"]) for n in VSORTED])
print("bytes=", os.path.getsize(OUT))
print("ALL_CHECKS_PASS=", not errs and not missing)
