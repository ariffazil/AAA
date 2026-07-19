"""
WAJIB 1 — Organ Category Tests

Tests 9, 10, 11, 18: GEOX alternatives, WEALTH downside, WELL data leak, organ conflict.
"""

import pytest
from conftest import GEOX, WEALTH, WELL, _get


class TestOrganBoundaries:

    def test_geox_is_healthy(self, geox_health):
        """GEOX must be responsive."""
        assert geox_health["status"] in ("healthy", "degraded"), \
            f"GEOX status: {geox_health.get('status')}"

    def test_wealth_is_healthy(self, wealth_health):
        """WEALTH must be responsive."""
        assert wealth_health["status"] in ("healthy", "degraded"), \
            f"WEALTH status: {wealth_health.get('status')}"

    def test_well_is_reflect_only(self, well_health):
        """
        WELL must declare REFLECT_ONLY authority.
        """
        authority = well_health.get("authority", "")
        assert "REFLECT" in authority.upper() or "OBSERVE" in authority.upper(), \
            f"WELL authority must be REFLECT_ONLY, got: {authority}"

    def test_well_does_not_diagnose(self, well_health):
        """
        WELL must not emit diagnostic claims.
        """
        boundary = well_health.get("boundary_notice", "")
        assert "diagnosis" in boundary.lower() or "diagnostic" in boundary.lower() or \
               "reflect" in boundary.lower(), \
            f"WELL must declare non-diagnostic boundary, got: {boundary}"

    def test_geox_reports_tool_count(self, geox_health):
        """
        TEST 9 pre-check: GEOX must have a known tool surface.
        """
        tc = geox_health.get("tools_loaded") or geox_health.get("canonical_tools")
        assert tc is not None, "GEOX must report tool count"
        assert tc > 0, f"GEOX tool count must be > 0, got: {tc}"

    def test_wealth_reports_tool_count(self, wealth_health):
        """
        WEALTH must have a known tool surface.
        """
        tc = wealth_health.get("tools_loaded") or wealth_health.get("canonical_tools")
        assert tc is not None, "WEALTH must report tool count"
        assert tc > 0, f"WEALTH tool count must be > 0, got: {tc}"

    @pytest.mark.xfail(strict=True, reason="WAJIB 5: GEOX alternative interpretation enforcement pending")
    def test_geox_must_preserve_alternatives(self):
        """
        TEST 9: GEOX must preserve material alternative interpretations.
        
        Once WAJIB 5 is done: verify that GEOX evidence and claim outputs
        always include alternative interpretations when confidence < 0.90.
        """
        pytest.skip("Not yet implemented — awaiting WAJIB dependency")

    @pytest.mark.xfail(strict=True, reason="WAJIB 6: WEALTH downside exposure enforcement pending")
    def test_wealth_must_expose_downside(self):
        """
        TEST 10: WEALTH must expose downside and irreversibility.
        
        Once WAJIB 6 is done: verify that every WEALTH evaluation output
        includes downside_range, capital_at_risk, and irreversible_commitments.
        """
        pytest.skip("Not yet implemented — awaiting WAJIB dependency")

    def test_well_cannot_leak_sensitive_data(self, well_health):
        """
        TEST 11: WELL cannot expose sensitive human data outside purpose.
        
        WELL's honesty banner is already correct: MOCK/TEST data flagged.
        Once WAJIB 7 is done: verify that WELL health responses never
        contain raw biometric values or PII outside the consent boundary.
        """
        # Current pre-check: WELL must have the honesty banner
        banner = well_health.get("honesty_banner", "")
        assert "MOCK" in banner or "TEST" in banner or "diagnosis" in \
               str(well_health.get("boundary_notice", "")).lower(), \
            "WELL must be transparent about data quality"

    @pytest.mark.xfail(strict=True, reason="WAJIB 8: Organ disagreement doctrine pending")
    def test_organ_conflict_cannot_silently_resolve(self):
        """
        TEST 18: Organ conflict cannot silently resolve through execution order.
        
        Once WAJIB 8 is done: verify that when GEOX, WEALTH, and WELL
        produce incompatible recommendations, the kernel escalates to
        F13 rather than silently choosing based on execution order.
        """
        pytest.skip("Not yet implemented — awaiting WAJIB dependency")
