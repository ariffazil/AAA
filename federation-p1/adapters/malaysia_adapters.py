#!/usr/bin/env python3
"""
malaysia_adapters.py — Malaysia/ASEAN-first data adapters for arifOS federation.

P1 sources (Malaysia first):
- BNM OpenAPI (Bank Negara Malaysia)
- OpenDOSM API (DOSM/data.gov.my)
- AMRO (ASEAN+3 surveillance)
- MEIH (Malaysia Energy Information Hub)
- DOE/JAS (Environmental/EIA)
- AGC Laws (Attorney General's Chambers)
- PETRONAS (Public reports)
- Bursa Malaysia (Disclosures — adapter abstraction, no hard-coded API)

All adapters are READ-ONLY. No domain logic. Schema + logging only.
"""

from __future__ import annotations

import hashlib
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)

VERSION = "2026.06.28"


class BaseAdapter(ABC):
    """Base class for all P1 data adapters."""

    def __init__(self, name: str, base_url: str, priority: str = "P1"):
        self.name = name
        self.base_url = base_url
        self.priority = priority
        self.version = VERSION
        self._last_fetch_ts: str | None = None

    def _envelope(self, data: Any, source_url: str) -> dict:
        """Wrap data in a standard adapter envelope."""
        self._last_fetch_ts = datetime.now(timezone.utc).isoformat()
        return {
            "adapter": self.name,
            "version": self.version,
            "priority": self.priority,
            "source_url": source_url,
            "fetched_at": self._last_fetch_ts,
            "data_hash": hashlib.sha256(
                json.dumps(data, sort_keys=True, default=str).encode()
            ).hexdigest()[:16],
            "data": data,
        }

    @abstractmethod
    def fetch(self, endpoint: str, params: dict | None = None) -> dict:
        """Fetch data from the source. Returns envelope."""
        ...

    def health(self) -> dict:
        return {
            "adapter": self.name,
            "base_url": self.base_url,
            "priority": self.priority,
            "version": self.version,
            "last_fetch": self._last_fetch_ts,
            "status": "READY",
        }


# ═══════════════════════════════════════════════════════════════════════════
# BNM OpenAPI — Bank Negara Malaysia
# https://api.bnm.gov.my
# ═══════════════════════════════════════════════════════════════════════════
class BNMAdapter(BaseAdapter):
    """Bank Negara Malaysia OpenAPI adapter.

    Domains: monetary policy, exchange rates, reserves, interest rates,
    banking statistics, Islamic finance, payment systems.
    """

    def __init__(self):
        super().__init__(
            name="bnm",
            base_url="https://api.bnm.gov.my",
            priority="P1",
        )

    def fetch(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._envelope(
            {"endpoint": endpoint, "params": params or {}, "status": "STUB"},
            url,
        )

    # Canonical endpoints
    def exchange_rates(self, currency: str = "USD") -> dict:
        return self.fetch(f"/exchange-rate/{currency}")

    def base_rate(self) -> dict:
        return self.fetch("/base-rate")

    def overnight_rate(self) -> dict:
        return self.fetch("/overnight-policy-rate")

    def reserves(self) -> dict:
        return self.fetch("/reserves")

    def money_supply(self) -> dict:
        return self.fetch("/msb")


# ═══════════════════════════════════════════════════════════════════════════
# OpenDOSM API — DOSM / data.gov.my
# https://api.data.gov.my/opendosm
# ═══════════════════════════════════════════════════════════════════════════
class OpenDOSMAdapter(BaseAdapter):
    """OpenDOSM API adapter — Malaysia national statistics.

    Domains: demographics, CPI, GDP, labor, production, trade.
    """

    def __init__(self):
        super().__init__(
            name="opendosm",
            base_url="https://api.data.gov.my/opendosm",
            priority="P1",
        )

    def fetch(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._envelope(
            {"endpoint": endpoint, "params": params or {}, "status": "STUB"},
            url,
        )

    def cpi(self, year: int | None = None) -> dict:
        params = {"year": year} if year else {}
        return self.fetch("/cpi", params)

    def gdp(self, year: int | None = None) -> dict:
        params = {"year": year} if year else {}
        return self.fetch("/gdp", params)

    def labour(self) -> dict:
        return self.fetch("/labour")

    def population(self) -> dict:
        return self.fetch("/population")

    def trade(self) -> dict:
        return self.fetch("/trade")


# ═══════════════════════════════════════════════════════════════════════════
# AMRO — ASEAN+3 Macroeconomic Research Office
# https://www.amro-asia.org
# ═══════════════════════════════════════════════════════════════════════════
class AMROAdapter(BaseAdapter):
    """AMRO adapter — ASEAN+3 surveillance and macro context.

    Domains: regional macro, financial resilience, consultation reports.
    """

    def __init__(self):
        super().__init__(
            name="amro",
            base_url="https://www.amro-asia.org",
            priority="P1",
        )

    def fetch(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._envelope(
            {"endpoint": endpoint, "params": params or {}, "status": "STUB"},
            url,
        )

    def publications(self) -> dict:
        return self.fetch("/publications")

    def annual_consultation(self, country: str = "malaysia") -> dict:
        return self.fetch(f"/annual-consultation/{country}")

    def regional_outlook(self) -> dict:
        return self.fetch("/regional-outlook")


# ═══════════════════════════════════════════════════════════════════════════
# MEIH — Malaysia Energy Information Hub
# https://meih.st.gov.my
# ═══════════════════════════════════════════════════════════════════════════
class MEIHAdapter(BaseAdapter):
    """MEIH adapter — Malaysia energy statistics.

    Domains: energy balances, power/gas statistics, grid emission factors.
    """

    def __init__(self):
        super().__init__(
            name="meih",
            base_url="https://meih.st.gov.my",
            priority="P1",
        )

    def fetch(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._envelope(
            {"endpoint": endpoint, "params": params or {}, "status": "STUB"},
            url,
        )

    def energy_balance(self, year: int | None = None) -> dict:
        return self.fetch("/energy-balance", {"year": year} if year else {})

    def electricity_stats(self) -> dict:
        return self.fetch("/electricity")

    def gas_stats(self) -> dict:
        return self.fetch("/gas")

    def emission_factors(self) -> dict:
        return self.fetch("/emission-factors")


# ═══════════════════════════════════════════════════════════════════════════
# DOE/JAS — Department of Environment Malaysia
# https://www.doe.gov.my
# ═══════════════════════════════════════════════════════════════════════════
class DOEAdapter(BaseAdapter):
    """DOE/JAS adapter — environmental legislation and EIA.

    Domains: EIA reports, environmental quality, permitting.
    """

    def __init__(self):
        super().__init__(
            name="doe",
            base_url="https://www.doe.gov.my",
            priority="P1",
        )

    def fetch(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._envelope(
            {"endpoint": endpoint, "params": params or {}, "status": "STUB"},
            url,
        )

    def eia_reports(self, project_type: str | None = None) -> dict:
        return self.fetch("/eia", {"type": project_type} if project_type else {})

    def environmental_quality(self) -> dict:
        return self.fetch("/environmental-quality")

    def legislation(self) -> dict:
        return self.fetch("/legislation")


# ═══════════════════════════════════════════════════════════════════════════
# AGC Laws — Attorney General's Chambers of Malaysia
# https://www.agc.gov.my
# ═══════════════════════════════════════════════════════════════════════════
class AGCAdapter(BaseAdapter):
    """AGC Laws adapter — Malaysian legislation.

    Domains: Federal Constitution, principal acts, subsidiary legislation.
    """

    def __init__(self):
        super().__init__(
            name="agc",
            base_url="https://www.agc.gov.my",
            priority="P1",
        )

    def fetch(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._envelope(
            {"endpoint": endpoint, "params": params or {}, "status": "STUB"},
            url,
        )

    def federal_constitution(self) -> dict:
        return self.fetch("/A0137131/constitution")

    def acts(self, act_name: str | None = None) -> dict:
        return self.fetch(f"/Acts/{act_name}" if act_name else "/Acts")

    def subsidiary_legislation(self) -> dict:
        return self.fetch("/Subsidiary-Legislation")

    def amendments(self) -> dict:
        return self.fetch("/Amendments")


# ═══════════════════════════════════════════════════════════════════════════
# PETRONAS — Public Reports Adapter
# Note: No single canonical API endpoint verified. This is an adapter
# abstraction for public annual reports and disclosures.
# ═══════════════════════════════════════════════════════════════════════════
class PetronasAdapter(BaseAdapter):
    """PETRONAS public reports adapter.

    Domains: annual reports, sustainability reports, disclosures.
    Note: Adapter abstraction — no hard-coded API claim.
    """

    def __init__(self):
        super().__init__(
            name="petronas",
            base_url="https://www.petronas.com",
            priority="P1",
        )

    def fetch(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._envelope(
            {"endpoint": endpoint, "params": params or {}, "status": "STUB"},
            url,
        )

    def annual_reports(self, year: int | None = None) -> dict:
        return self.fetch("/reports/annual", {"year": year} if year else {})

    def sustainability_reports(self) -> dict:
        return self.fetch("/reports/sustainability")

    def disclosures(self) -> dict:
        return self.fetch("/disclosures")


# ═══════════════════════════════════════════════════════════════════════════
# Bursa Malaysia — Disclosure Adapter (Abstraction)
# Note: No stable public official API endpoint verified.
# This is an adapter abstraction for Bursa disclosures.
# ═══════════════════════════════════════════════════════════════════════════
class BursaAdapter(BaseAdapter):
    """Bursa Malaysia disclosure adapter.

    Domains: listed company filings, announcements, financial results.
    Note: Adapter abstraction — no hard-coded API claim.
    """

    def __init__(self):
        super().__init__(
            name="bursa",
            base_url="https://www.bursamalaysia.com",
            priority="P1",
        )

    def fetch(self, endpoint: str, params: dict | None = None) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._envelope(
            {"endpoint": endpoint, "params": params or {}, "status": "STUB"},
            url,
        )

    def company_filings(self, company_code: str | None = None) -> dict:
        return self.fetch(
            f"/listed_companies/company_filing/{company_code}"
            if company_code
            else "/listed_companies/company_filing"
        )

    def announcements(self, sector: str | None = None) -> dict:
        return self.fetch("/announcements", {"sector": sector} if sector else {})

    def financial_results(self, company_code: str | None = None) -> dict:
        return self.fetch(
            f"/financial_results/{company_code}"
            if company_code
            else "/financial_results"
        )


# ═══════════════════════════════════════════════════════════════════════════
# REGISTRY — All adapters
# ═══════════════════════════════════════════════════════════════════════════
ADAPTERS: dict[str, BaseAdapter] = {
    "bnm": BNMAdapter(),
    "opendosm": OpenDOSMAdapter(),
    "amro": AMROAdapter(),
    "meih": MEIHAdapter(),
    "doe": DOEAdapter(),
    "agc": AGCAdapter(),
    "petronas": PetronasAdapter(),
    "bursa": BursaAdapter(),
}


def health_all() -> list[dict]:
    """Health check all adapters."""
    return [adapter.health() for adapter in ADAPTERS.values()]


if __name__ == "__main__":
    print("Malaysia/ASEAN Adapters:")
    for name, adapter in ADAPTERS.items():
        h = adapter.health()
        print(f"  [{h['priority']}] {h['adapter']:12s} → {h['base_url']}")
