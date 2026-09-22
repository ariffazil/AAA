#!/usr/bin/env python3
"""CHRON Seasonal Bias Calendar — Commodity & Macro Cyclical Patterns.

Tracks multi-month and cyclical seasonal bias patterns across:
  - OIL (CL=F): Q4 Northern Hemisphere winter heating demand bias, spring refinery turnaround
  - GAS (NG=F): Injection season (Apr-Oct), Winter withdrawal season (Nov-Mar), Shoulder months
  - GOLD (XAUUSD): Indian wedding / Diwali & Lunar New Year physical demand, Sept historical weakness
  - KLCI (^KLSE): Year-end window dressing (Dec), pre-Chinese New Year rally, post-results drag
  - USMYR (MYR=X): Q4 fiscal budget announcements, dividend repatriation season

Provides temporal bias priors for CHRON predictions and confluence scoring.

DITEMPA BUKAN DIBERI ⚒️
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

MYT = timezone(timedelta(hours=8))


@dataclass
class SeasonalBias:
    instrument: str
    month: int
    bias: str  # BULLISH | BEARISH | NEUTRAL | VOLATILE
    strength: float  # 0.0 to 1.0
    rationale: str
    historical_tendency: str
    edge_recommendation: str

    def to_dict(self) -> dict:
        return asdict(self)


# Canonical Seasonal Map by Instrument & Month (1-12)
SEASONAL_REGISTRY: dict[str, dict[int, SeasonalBias]] = {
    "OIL": {
        1: SeasonalBias("OIL", 1, "VOLATILE", 0.60, "Post-holiday demand reset vs winter heating", "Choppy", "Trade confirmed breakouts only"),
        2: SeasonalBias("OIL", 2, "BEARISH", 0.65, "US refinery maintenance / turnaround season starts", "Refinery crude demand dips", "Fade rallies to major resistance"),
        3: SeasonalBias("OIL", 3, "NEUTRAL", 0.50, "Transition from winter heating to driving season prep", "Range-bound", "Range trading on S/R extremes"),
        4: SeasonalBias("OIL", 4, "BULLISH", 0.70, "Pre-driving season restocking & refinery ramp-up", "Consistent accumulation", "Buy dips in UPTREND"),
        5: SeasonalBias("OIL", 5, "BULLISH", 0.75, "Memorial Day kickoff for US summer driving", "High physical demand", "Long bias with trailing stops"),
        6: SeasonalBias("OIL", 6, "BULLISH", 0.70, "Peak summer driving consumption", "Physical drawdown", "Ride momentum"),
        7: SeasonalBias("OIL", 7, "NEUTRAL", 0.55, "Mid-summer peak; hurricane risk emergence in US Gulf", "High event risk", "Reduce position size on storms"),
        8: SeasonalBias("OIL", 8, "VOLATILE", 0.65, "Peak Gulf hurricane season", "Supply disruption spikes", "Tighten stops on long positions"),
        9: SeasonalBias("OIL", 9, "BEARISH", 0.70, "End of summer driving season, autumn refinery turnaround", "Historical seasonal weakness", "Look for short setups at resistance"),
        10: SeasonalBias("OIL", 10, "BULLISH", 0.65, "Northern Hemisphere winter fuel procurement begins", "Early heating oil bid", "Accumulate in buy zones"),
        11: SeasonalBias("OIL", 11, "BULLISH", 0.75, "Peak heating demand ramp + OPEC+ year-end meeting positioning", "Bullish drift into OPEC", "Long bias on OPEC pre-announcement drift"),
        12: SeasonalBias("OIL", 12, "BULLISH", 0.70, "Winter heating peak consumption", "Supportive physical backdrop", "Buy pullbacks to EMA50"),
    },
    "GAS": {
        1: SeasonalBias("GAS", 1, "VOLATILE", 0.85, "Peak winter heating withdrawals; polar vortex risk", "Violent weather-driven spikes", "Wider stops mandatory; check weather forecasts"),
        2: SeasonalBias("GAS", 2, "VOLATILE", 0.80, "Late winter freezes vs early warming forecasts", "Sharp gap risk", "Trade half-size due to extreme volatility"),
        3: SeasonalBias("GAS", 3, "BEARISH", 0.75, "End of withdrawal season, transition to shoulder month", "Demand falls off cliff", "Sell rallies into shoulder lull"),
        4: SeasonalBias("GAS", 4, "BEARISH", 0.70, "Shoulder season: injection season officially starts", "Mild weather, storage builds", "Range-bound or downward drift"),
        5: SeasonalBias("GAS", 5, "NEUTRAL", 0.50, "Steady storage injection; mild ambient temperatures", "Low power burn demand", "Range fade at Bollinger Bands"),
        6: SeasonalBias("GAS", 6, "BULLISH", 0.65, "Early summer cooling demand (air conditioning burn)", "Power burn starts lifting spot", "Buy dips above EMA20"),
        7: SeasonalBias("GAS", 7, "BULLISH", 0.75, "Peak summer heat waves, high electric utility gas burn", "High power demand burn", "Momentum continuation"),
        8: SeasonalBias("GAS", 8, "BULLISH", 0.70, "Late summer cooling demand", "Persistent electric burn", "Ride trend with profit targets"),
        9: SeasonalBias("GAS", 9, "BEARISH", 0.75, "Autumn shoulder season; cooling drops, heating not started", "Storage injection max rate", "Expect price weakness"),
        10: SeasonalBias("GAS", 10, "NEUTRAL", 0.60, "Pre-winter positioning; European storage injection completion", "Speculative bid starts forming", "Watch for winter strip buildup"),
        11: SeasonalBias("GAS", 11, "BULLISH", 0.80, "Official start of withdrawal season (Nov 1)", "Cold weather premium priced in", "Buy pullbacks to strong support"),
        12: SeasonalBias("GAS", 12, "VOLATILE", 0.85, "Winter heating demand in full swing; freeze-offs", "Severe upside spikes on blizzards", "Trade with defined risk options/tight SL"),
    },
    "GOLD": {
        1: SeasonalBias("GOLD", 1, "BULLISH", 0.80, "New Year portfolio rebalancing & Lunar New Year physical buying", "Strongest historical month for gold", "High win-rate long bias"),
        2: SeasonalBias("GOLD", 2, "BULLISH", 0.65, "Lunar New Year continuation followed by late-month pause", "Physical Asian accumulation", "Hold longs into mid-month"),
        3: SeasonalBias("GOLD", 3, "BEARISH", 0.60, "Post-New Year physical buying lull; Q1 fiscal profit-taking", "Seasonal consolidation", "Look for range support entries"),
        4: SeasonalBias("GOLD", 4, "NEUTRAL", 0.50, "Akshaya Tritiya (India) buying balanced by tax-selling", "Sideways consolidation", "Fade range extremes"),
        5: SeasonalBias("GOLD", 5, "BEARISH", 0.60, "Summer doldrums approach; physical demand quiet", "Low volatility lull", "Range trade; tight targets"),
        6: SeasonalBias("GOLD", 6, "NEUTRAL", 0.50, "Mid-year lull; central bank purchases provide floor", "Range-bound trading", "Support bounces only"),
        7: SeasonalBias("GOLD", 7, "BULLISH", 0.60, "Late July safe-haven positioning", "Modest seasonal lift", "Look for trend resumption"),
        8: SeasonalBias("GOLD", 8, "BULLISH", 0.70, "Pre-Indian festival season inventory accumulation", "Jewelers restocking", "Accumulate in buy zones"),
        9: SeasonalBias("GOLD", 9, "BEARISH", 0.75, "Historically gold's weakest month (FOMC + fiscal resets)", "High probability of pullback", "Avoid aggressive longs; wait for deep dips"),
        10: SeasonalBias("GOLD", 10, "BULLISH", 0.70, "Diwali festival & Indian wedding season demand surge", "Heavy physical coin/bar buying", "Buy dip into festival window"),
        11: SeasonalBias("GOLD", 11, "BULLISH", 0.75, "Wedding season continuation + Western holiday gifting", "Persistent physical bid", "Long bias with trailing stops"),
        12: SeasonalBias("GOLD", 12, "BULLISH", 0.70, "Late December pre-January effect accumulation", "Santa rally across hard assets", "Position for January surge"),
    },
    "KLCI": {
        1: SeasonalBias("KLCI", 1, "BULLISH", 0.70, "January effect + pre-Chinese New Year rally", "Retail & local institution buying", "Focus on GLC & banking counters"),
        2: SeasonalBias("KLCI", 2, "NEUTRAL", 0.55, "Post-CNY digestion + Q4 corporate earnings release", "Earnings volatility", "Selective on counters beating earnings"),
        3: SeasonalBias("KLCI", 3, "BEARISH", 0.65, "Post-earnings season hangover, annual report releases", "Consolidation/pullback", "Wait for lower support levels"),
        4: SeasonalBias("KLCI", 4, "BULLISH", 0.60, "Dividend reinvestment flows + AGM season", "Local fund support", "Buy high-dividend yield counters"),
        5: SeasonalBias("KLCI", 5, "BEARISH", 0.70, "'Sell in May and go away' global macro risk-off", "Foreign fund outflows", "Reduce exposure or hedge"),
        6: SeasonalBias("KLCI", 6, "NEUTRAL", 0.50, "Mid-year portfolio rebalancing", "Flat to choppy", "Range trading only"),
        7: SeasonalBias("KLCI", 7, "BULLISH", 0.60, "Q3 start; post-H1 performance catch-up", "Institutional accumulation", "Selective entry on dips"),
        8: SeasonalBias("KLCI", 8, "BEARISH", 0.65, "Q2 corporate earnings season (historically cautious)", "Corporate results drag", "Defensive positioning"),
        9: SeasonalBias("KLCI", 9, "BEARISH", 0.70, "Global September effect + pre-budget speculation", "Uncertainty discount", "Hold cash or accumulate value"),
        10: SeasonalBias("KLCI", 10, "VOLATILE", 0.75, "Malaysian National Budget (Belanjawan) announcement", "Sector rotation on budget beneficiaries", "Trade specific beneficiary sectors (infra/tech)"),
        11: SeasonalBias("KLCI", 11, "NEUTRAL", 0.55, "Post-budget digestion + Q3 earnings announcements", "Sector-specific divergence", "Focus on confirmed beneficiaries"),
        12: SeasonalBias("KLCI", 12, "BULLISH", 0.85, "Year-end institutional window dressing (high win rate)", "GLCs & funds bid up index", "High-confidence long bias last 2 weeks of Dec"),
    },
    "USMYR": {
        1: SeasonalBias("USMYR", 1, "BEARISH", 0.65, "MYR strength: repatriation of funds for CNY & taxes", "USD/MYR tends to drift lower", "Fade USD rallies against MYR"),
        2: SeasonalBias("USMYR", 2, "NEUTRAL", 0.50, "Post-CNY lull", "Consolidation", "Trade within technical channels"),
        3: SeasonalBias("USMYR", 3, "BULLISH", 0.60, "USD strength: corporate tax payments & dividend outflows abroad", "USD/MYR drifts higher", "Supportive for USD/MYR"),
        4: SeasonalBias("USMYR", 4, "NEUTRAL", 0.55, "Tax season balancing", "Range-bound", "Range-bound strategies"),
        5: SeasonalBias("USMYR", 5, "BULLISH", 0.65, "Global risk-off: USD safe haven demand strengthens", "EM currency pressure", "Long USD/MYR on macro dips"),
        6: SeasonalBias("USMYR", 6, "NEUTRAL", 0.50, "Mid-year foreign portfolio adjustments", "Sideways", "Monitor BNM intervention levels"),
        7: SeasonalBias("USMYR", 7, "NEUTRAL", 0.50, "Quiet summer flow period", "Low volatility", "Range trade"),
        8: SeasonalBias("USMYR", 8, "BULLISH", 0.60, "Pre-September global USD strength", "EM FX softness", "Watch 4.40/4.60 resistance levels"),
        9: SeasonalBias("USMYR", 9, "BULLISH", 0.70, "September USD funding squeeze & global risk aversion", "USD typically strong vs MYR", "Long USD/MYR on EM risk-off"),
        10: SeasonalBias("USMYR", 10, "BEARISH", 0.65, "National Budget fiscal clarity usually stabilizes/strengthens MYR", "Post-budget fiscal confidence", "Look for USD/MYR topping signs"),
        11: SeasonalBias("USMYR", 11, "NEUTRAL", 0.55, "Year-end export proceeds repatriation begins", "Steady MYR support", "Trade range boundaries"),
        12: SeasonalBias("USMYR", 12, "BEARISH", 0.70, "Heavy export proceeds conversion to MYR for year-end books", "Strongest seasonal month for Ringgit", "Short USD/MYR (expect MYR strength)"),
    },
}


def get_seasonal_bias(instrument: str, dt: Optional[datetime] = None) -> SeasonalBias:
    """Retrieve the seasonal bias for a given instrument and datetime."""
    inst = instrument.upper()
    if inst == "XAUUSD":
        inst = "GOLD"
    if inst not in SEASONAL_REGISTRY:
        raise ValueError(f"Unknown instrument: {instrument}. Valid: {list(SEASONAL_REGISTRY.keys())}")
    
    if dt is None:
        dt = datetime.now(MYT)
    
    month = dt.month
    return SEASONAL_REGISTRY[inst][month]


def get_all_seasonal_biases(dt: Optional[datetime] = None) -> dict[str, dict]:
    """Retrieve current seasonal biases across all 5 instruments."""
    if dt is None:
        dt = datetime.now(MYT)
    return {inst: get_seasonal_bias(inst, dt).to_dict() for inst in SEASONAL_REGISTRY}


if __name__ == "__main__":
    now = datetime.now(MYT)
    print(f"=== CHRON Seasonal Bias Calendar ({now.strftime('%B %Y')}) ===")
    for inst, data in get_all_seasonal_biases(now).items():
        print(f"[{inst}] {data['bias']} (strength={data['strength']:.2f})")
        print(f"  Rationale: {data['rationale']}")
        print(f"  Action:    {data['edge_recommendation']}\n")
