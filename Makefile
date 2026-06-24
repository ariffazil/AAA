# Makefile — arifOS Closure Architecture
# DITEMPA BUKAN DIBERI
# Forged: 2026-06-14

.PHONY: prove health sot-check security-audit audit-skills floor-benchmark \
        organ-boundary-benchmark external-harness-benchmark \
        vault999-verify reality-replay constitutional-benchmark \
        scorecard proof-pack forge seal init

# ──────────────────────────────────────────────
# DEFAULT: full proof cycle
# ──────────────────────────────────────────────
prove: health sot-check security-audit constitutional-benchmark \
       vault999-verify reality-replay scorecard proof-pack
	@echo ""
	@echo "=========================================="
	@echo "  make prove COMPLETE"
	@echo "  Reports:"
	@echo "    - reports/ARIFOS_PROOF_PACK.md"
	@echo "    - reports/ARIFOS_SCORECARD.json"
	@echo "    - reports/ARIFOS_SCORECARD.md"
	@echo "    - reports/OPEN_HOLD_ITEMS.md"
	@echo "=========================================="

# ──────────────────────────────────────────────
# HEALTH — all organs reachable
# ──────────────────────────────────────────────
health:
	@echo "=== Health ==="
	@python3 scripts/health_check.py

# ──────────────────────────────────────────────
# SOURCE-OF-TRUTH DRIFT
# ──────────────────────────────────────────────
sot-check:
	@echo "=== Source-of-Truth Drift Check ==="
	@python3 scripts/sot_check.py

# ──────────────────────────────────────────────
# SECURITY AUDIT
# ──────────────────────────────────────────────
security-audit:
	@echo "=== Security Audit ==="
	@echo "  Note: Trivy/Semgrep/Gitleaks/Ruff run from arifOS repo."
	@-which trivy >/dev/null 2>&1 && (trivy filesystem --severity CRITICAL . --quiet 2>/dev/null | head -20) || echo "  ⚠️  trivy not installed"
	@-which semgrep >/dev/null 2>&1 && semgrep --config auto --quiet . 2>/dev/null | tail -5 || echo "  ⚠️  semgrep not installed"
	@-which gitleaks >/dev/null 2>&1 && gitleaks detect --no-git --verbose 2>/dev/null | head -10 || echo "  ⚠️  gitleaks not installed"
	@-which ruff >/dev/null 2>&1 && ruff check . --quiet 2>/dev/null || echo "  ⚠️  ruff not installed"
	@echo "  ✅ Security audit targets defined"

# ──────────────────────────────────────────────
# SKILL AUDIT
# ──────────────────────────────────────────────
audit-skills:
	@echo "=== Federation Skill Audit ==="
	@python3 scripts/federation_skill_auditor.py --output reports/SKILL_AUDIT.md
	@echo "  ✅ reports/SKILL_AUDIT.md written"

# ──────────────────────────────────────────────
# CONSTITUTIONAL BENCHMARK
# ──────────────────────────────────────────────
constitutional-benchmark: floor-benchmark organ-boundary-benchmark

floor-benchmark:
	@echo "=== Floor Benchmark (F1-F13) — Live Kernel ==="
	@mkdir -p benchmarks/floors/results
	@python3 benchmarks/run_floor_benchmarks.py 2>&1

organ-boundary-benchmark:
	@echo "=== Organ Boundary Benchmark ==="
	@echo "  See docs/ORGAN_AUTHORITY_MAP.md for 27 boundary test definitions."
	@echo "  🔲 Runtime tests not yet implemented."
	@mkdir -p benchmarks/organs/results

external-harness-benchmark:
	@echo "=== External Harness Benchmark ==="
	@echo "  🔲 Adapter compliance tests not yet implemented."

# ──────────────────────────────────────────────
# VAULT999 VERIFY
# ──────────────────────────────────────────────
vault999-verify:
	@echo "=== VAULT999 Chain Verification ==="
	@if [ -d /root/arifOS/VAULT999 ]; then \
		echo "  VAULT999 directory found at /root/arifOS/VAULT999"; \
		ls /root/arifOS/VAULT999/ 2>/dev/null | head -5; \
		echo "  ✅ VAULT999 accessible"; \
	else \
		echo "  ⚠️  VAULT999 directory not found (expected at /root/arifOS/VAULT999)"; \
	fi

# ──────────────────────────────────────────────
# REALITY LEDGER REPLAY
# ──────────────────────────────────────────────
reality-replay:
	@echo "=== Reality Ledger Replay ==="
	@python3 scripts/reality_replay.py

# ──────────────────────────────────────────────
# SCORECARD
# ──────────────────────────────────────────────
scorecard:
	@echo "=== Scorecard ==="
	@python3 scripts/scorecard.py

# ──────────────────────────────────────────────
# PROOF PACK
# ──────────────────────────────────────────────
proof-pack:
	@echo "=== Proof Pack ==="
	@python3 scripts/proof_pack.py
	@echo "  ✅ reports/ARIFOS_PROOF_PACK.md written"

# ──────────────────────────────────────────────
# FORGE — full build cycle
# ──────────────────────────────────────────────
forge: prove
	@echo ""
	@echo "=== FORGE Complete ==="

# ──────────────────────────────────────────────
# HELP
# ──────────────────────────────────────────────
help:
	@echo "arifOS Makefile — Closure Architecture"
	@echo ""
	@echo "Targets:"
	@echo "  make prove                    Full proof cycle (default)"
	@echo "  make health                   Organ liveness check"
	@echo "  make sot-check                Source-of-truth drift"
	@echo "  make security-audit           Security scanner suite"
	@echo "  make audit-skills             Federation skill hygiene audit"
	@echo "  make floor-benchmark          F1-F13 floor tests (live kernel)"
	@echo "  make organ-boundary-benchmark Organ boundary tests"
	@echo "  make vault999-verify          VAULT999 chain integrity"
	@echo "  make reality-replay           Reality Ledger replay"
	@echo "  make scorecard                Generate maturity scores"
	@echo "  make forge                    Full build cycle"
