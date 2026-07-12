import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { DollarSign, TrendingUp, Droplets, BarChart3 } from "lucide-react";
import { getFiscal, getMarket } from "../lib/api";

export default function WealthPage() {
  const [fiscal, setFiscal] = useState<any>(null);
  const [market, setMarket] = useState<any>(null);
  const [loading, setLoading] = useState(true);

// eslint-disable-next-line no-use-before-define
const loadData = async () => {
    setLoading(true);
    try {
      const [f, m] = await Promise.allSettled([getFiscal(), getMarket("commodity")]);
      if (f.status === "fulfilled") {
        let fiscalData = f.value?.result || f.value;
        if (fiscalData?.result) fiscalData = fiscalData.result;
        setFiscal(fiscalData);
      }
      if (m.status === "fulfilled") {
        let marketData = m.value?.result || m.value;
        if (marketData?.result) marketData = marketData.result;
        setMarket(marketData);
      }
    } catch (e) {
      console.warn("WEALTH fetch failed:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
  }, [loadData]);

  ;

  return (
    <div className="app-container">
      <motion.div className="page-header" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1>💰 Capital Intel</h1>
        <p className="subtitle">Powered by WEALTH Federation</p>
      </motion.div>

      {loading && (
        <div className="loading-container">
          <div className="spinner" />
          <p style={{ fontSize: "14px", color: "var(--hint)" }}>Querying WEALTH engine...</p>
        </div>
      )}

      {!loading && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
          {/* Fiscal Breakeven */}
          {fiscal && (
            <div className="card">
              <div className="card-header">
                <div className="card-icon">⛽</div>
                <div>
                  <div className="card-title">Malaysia Fiscal Breakeven</div>
                  <div className="card-subtitle">Oil price threshold for fiscal sustainability</div>
                </div>
              </div>

              <div className="stat-grid">
                <div className="stat-item">
                  <div className="stat-value" style={{ color: "var(--accent)" }}>
                    ${fiscal.current_oil_price_usd?.toFixed(0) || "—"}
                  </div>
                  <div className="stat-label">Current Oil $/bbl</div>
                </div>
                <div className="stat-item">
                  <div className="stat-value" style={{
                    color: fiscal.fiscal_pressure === "MANAGEABLE" ? "var(--green)" :
                           fiscal.fiscal_pressure === "AT_RISK" ? "var(--yellow)" : "var(--red)"
                  }}>
                    {fiscal.fiscal_pressure || "—"}
                  </div>
                  <div className="stat-label">Fiscal Status</div>
                </div>
              </div>

              <div className="stat-grid" style={{ marginTop: "10px" }}>
                <div className="stat-item">
                  <div className="stat-value">{fiscal.fiscal_sensitivity_rm_b_per_usd?.toFixed(3) || "—"}</div>
                  <div className="stat-label">Sensitivity RM/B</div>
                </div>
                <div className="stat-item">
                  <div className="stat-value">{fiscal.target_deficit_pct?.toFixed(1) || "—"}%</div>
                  <div className="stat-label">Target Deficit</div>
                </div>
              </div>
            </div>
          )}

          {/* Market Data */}
          {market && (
            <div className="card">
              <div className="card-header">
                <div className="card-icon">📊</div>
                <div>
                  <div className="card-title">Market Snapshot</div>
                  <div className="card-subtitle">Key indicators</div>
                </div>
              </div>

              <div className="result-item">
                <div className="result-icon">🛢️</div>
                <div className="result-content">
                  <div className="result-title">Brent Crude</div>
                  <div className="result-desc">{market.source || "Global oil benchmark"}</div>
                </div>
                <div className="result-value" style={{ color: "var(--green)" }}>
                  ${market.price || "—"}
                </div>
              </div>

              <div className="result-item">
                <div className="result-icon">📅</div>
                <div className="result-content">
                  <div className="result-title">Date</div>
                  <div className="result-desc">Market data timestamp</div>
                </div>
                <div className="result-value">
                  {market.date || "—"}
                </div>
              </div>
            </div>
          )}

          {/* Info */}
          <div className="card" style={{ textAlign: "center", padding: "24px" }}>
            <BarChart3 size={32} style={{ color: "var(--hint)", marginBottom: "12px" }} />
            <p style={{ fontSize: "13px", color: "var(--hint)", lineHeight: "1.6" }}>
              Capital intelligence powered by WEALTH engine.<br />
              Computes fiscal breakeven, market data, and capital flows.<br />
              <strong>WEALTH computes. arifOS judges. Arif decides.</strong>
            </p>
          </div>
        </motion.div>
      )}
    </div>
  );
}
