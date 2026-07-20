import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { getReadiness } from "../lib/api";

export default function WellPage() {
  const [readiness, setReadiness] = useState<any>(null);
  const [loading, setLoading] = useState(true);

 
const loadReadiness = async () => {
    setLoading(true);
    try {
      const data = await getReadiness();
      let readinessData = data?.result || data;
      if (readinessData?.result) readinessData = readinessData.result;
      setReadiness(readinessData);
    } catch (e) {
      console.warn("WELL fetch failed:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadReadiness();
  }, [loadReadiness]);

  ;

  const colorMap: Record<string, string> = {
    GREEN: "var(--green)",
    YELLOW: "var(--yellow)",
    RED: "var(--red)",
    STALE: "var(--hint)",
  };

  return (
    <div className="app-container">
      <motion.div className="page-header" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1>🫀 Readiness</h1>
        <p className="subtitle">Powered by WELL Federation</p>
      </motion.div>

      {loading && (
        <div className="loading-container">
          <div className="spinner" />
          <p style={{ fontSize: "14px", color: "var(--hint)" }}>Assessing readiness...</p>
        </div>
      )}

      {!loading && readiness && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
          {/* Honesty banner — STALE / MOCK / SELF-REPORT (F2 permanent) */}
          {(readiness.honesty_banner || readiness.honesty?.banner || readiness.truth_status === "OPERATOR_REPORTED" || readiness.color === "STALE") && (
            <div className="card" style={{
              borderColor: "var(--yellow)",
              background: "rgba(255, 193, 7, 0.08)",
              marginBottom: "12px",
              padding: "16px",
            }}>
              <div style={{ fontSize: "11px", fontWeight: 700, letterSpacing: "0.08em", color: "var(--yellow)", marginBottom: "6px" }}>
                HONESTY · {readiness.honesty?.code || readiness.truth_status || readiness.color || "NOTICE"}
              </div>
              <div style={{ fontSize: "13px", color: "var(--text)", lineHeight: 1.5 }}>
                {readiness.honesty_banner
                  || readiness.honesty?.banner
                  || (readiness.color === "STALE"
                    ? "STALE — biometrics aged out. Refresh before high-stakes work."
                    : "SELF-REPORT / non-sensor — not wearable-verified body truth.")}
              </div>
            </div>
          )}

          {/* Main Status */}
          <div className="card" style={{ textAlign: "center", padding: "32px" }}>
            <div style={{
              fontSize: "64px",
              marginBottom: "12px",
            }}>
              {readiness.color === "GREEN" ? "✅" : readiness.color === "YELLOW" ? "⚠️" : readiness.color === "RED" ? "🔴" : "⚪"}
            </div>
            <div style={{
              fontSize: "28px",
              fontWeight: "700",
              color: colorMap[readiness.color] || "var(--text)",
              marginBottom: "8px",
            }}>
              {readiness.color || "UNKNOWN"}
            </div>
            <div style={{
              fontSize: "16px",
              fontWeight: "600",
              color: "var(--text)",
              marginBottom: "4px",
            }}>
              Score: {readiness.score ?? "—"}/100
            </div>
            <div style={{ fontSize: "13px", color: "var(--hint)" }}>
              Action: {readiness.action || "—"}
            </div>
          </div>

          {/* Biometrics */}
          {readiness.biometric && (
            <div className="card">
              <div className="card-header">
                <div className="card-icon">📊</div>
                <div>
                  <div className="card-title">Biometric Signals</div>
                  <div className="card-subtitle">Substrate readings</div>
                </div>
              </div>

              <div className="stat-grid">
                {readiness.biometric.sleep_hours !== undefined && (
                  <div className="stat-item">
                    <div className="stat-value">{readiness.biometric.sleep_hours?.toFixed(1)}</div>
                    <div className="stat-label">Sleep Hours</div>
                  </div>
                )}
                {readiness.biometric.peace2 !== undefined && (
                  <div className="stat-item">
                    <div className="stat-value">{readiness.biometric.peace2?.toFixed(2)}</div>
                    <div className="stat-label">PEACE²</div>
                  </div>
                )}
                {readiness.biometric.clarity !== undefined && (
                  <div className="stat-item">
                    <div className="stat-value">{readiness.biometric.clarity?.toFixed(2)}</div>
                    <div className="stat-label">Clarity</div>
                  </div>
                )}
                {readiness.biometric.delta_s !== undefined && (
                  <div className="stat-item">
                    <div className="stat-value">{readiness.biometric.delta_s?.toFixed(2)}</div>
                    <div className="stat-label">ΔS (Entropy)</div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* TTL */}
          {readiness.ttl_hours !== undefined && (
            <div className="card">
              <div className="result-item">
                <div className="result-icon">⏱️</div>
                <div className="result-content">
                  <div className="result-title">Data Freshness</div>
                  <div className="result-desc">Hours since last biometric update</div>
                </div>
                <div className="result-value" style={{
                  color: readiness.ttl_hours < 12 ? "var(--green)" :
                         readiness.ttl_hours < 24 ? "var(--yellow)" : "var(--red)"
                }}>
                  {readiness.ttl_hours?.toFixed(0)}h
                </div>
              </div>
            </div>
          )}

          {/* Info */}
          <div className="card" style={{ textAlign: "center", padding: "24px" }}>
            <p style={{ fontSize: "13px", color: "var(--hint)", lineHeight: "1.6" }}>
              WELL holds a mirror, not a veto.<br />
              Operator sovereignty is invariant.<br />
              <strong>WELL reflects. You decide.</strong>
            </p>
          </div>
        </motion.div>
      )}

      {!loading && !readiness && (
        <div className="empty-state">
          <div className="emoji">🫀</div>
          <p>Could not load readiness data.<br/>WELL organ may be unavailable.</p>
        </div>
      )}
    </div>
  );
}
