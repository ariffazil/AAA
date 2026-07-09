import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Database, Lock, Hash, Clock, Shield, FileText, ChevronRight } from "lucide-react";

interface SealEntry {
  seq?: number;
  actor?: string;
  verdict?: string;
  timestamp?: string;
  hash?: string;
  payload?: string;
}

export default function SealPage() {
  const [chain, setChain] = useState<SealEntry[]>([]);
  const [head, setHead] = useState<SealEntry | null>(null);
  const [loading, setLoading] = useState(true);
  const [chainValid, setChainValid] = useState<boolean | null>(null);

  useEffect(() => {
    loadChain();
  }, []);

  const loadChain = async () => {
    setLoading(true);
    try {
      const [c, h, v] = await Promise.allSettled([
        fetch("/api/seal/chain").then(r => r.json()),
        fetch("/api/seal/head").then(r => r.json()),
        fetch("/api/seal/verify").then(r => r.json()),
      ]);
      if (c.status === "fulfilled") {
        const data = c.value?.result || c.value;
        setChain(Array.isArray(data) ? data : data?.entries || []);
      }
      if (h.status === "fulfilled") setHead(h.value?.result || h.value);
      if (v.status === "fulfilled") setChainValid(v.value?.valid ?? null);
    } catch (e) {
      console.warn("Seal fetch failed:", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <motion.div className="page-header" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <h1>💎 VAULT999</h1>
        <p className="subtitle">Immutable Audit Ledger — 999 Seal</p>
      </motion.div>

      {loading && (
        <div className="loading-container">
          <div className="spinner" />
          <p style={{ fontSize: "14px", color: "var(--hint)" }}>Reading seal chain...</p>
        </div>
      )}

      {!loading && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }}>
          {/* Chain Status */}
          <div className="card" style={{ textAlign: "center", padding: "28px" }}>
            <div style={{ fontSize: "48px", marginBottom: "12px" }}>💎</div>
            <div style={{
              fontSize: "22px", fontWeight: "700",
              color: chainValid === true ? "var(--green)" : chainValid === false ? "var(--red)" : "var(--hint)",
            }}>
              {chainValid === true ? "CHAIN INTACT" : chainValid === false ? "CHAIN BROKEN" : "UNKNOWN"}
            </div>
            <div style={{ fontSize: "13px", color: "var(--hint)", marginTop: "6px" }}>
              {chain.length} sealed entries • Hash-chained • Append-only
            </div>
          </div>

          {/* Head (Latest Seal) */}
          {head && (
            <div className="card">
              <div className="card-header">
                <div className="card-icon">🔗</div>
                <div>
                  <div className="card-title">Chain Head</div>
                  <div className="card-subtitle">Latest sealed entry</div>
                </div>
                <span className="badge badge-purple"><span className="badge-dot" /> SEALED</span>
              </div>

              <div className="stat-grid">
                {head.seq !== undefined && (
                  <div className="stat-item">
                    <div className="stat-value">#{head.seq}</div>
                    <div className="stat-label">Sequence</div>
                  </div>
                )}
                <div className="stat-item">
                  <div className="stat-value" style={{ fontSize: "14px" }}>{head.verdict || "—"}</div>
                  <div className="stat-label">Verdict</div>
                </div>
              </div>

              {head.actor && (
                <div className="result-item" style={{ marginTop: "10px" }}>
                  <div className="result-icon">👤</div>
                  <div className="result-content">
                    <div className="result-title">Actor</div>
                  </div>
                  <div className="result-value" style={{ fontFamily: "monospace", fontSize: "12px" }}>{head.actor}</div>
                </div>
              )}

              {head.hash && (
                <div style={{ marginTop: "10px", padding: "10px", background: "rgba(255,255,255,0.03)", borderRadius: "8px" }}>
                  <div style={{ fontSize: "11px", color: "var(--hint)", marginBottom: "4px" }}>HASH</div>
                  <div style={{ fontFamily: "monospace", fontSize: "11px", color: "var(--accent)", wordBreak: "break-all" }}>
                    {head.hash}
                  </div>
                </div>
              )}

              {head.timestamp && (
                <div style={{ marginTop: "8px", display: "flex", alignItems: "center", gap: "6px" }}>
                  <Clock size={12} style={{ color: "var(--hint)" }} />
                  <span style={{ fontSize: "12px", color: "var(--hint)" }}>
                    {new Date(head.timestamp).toLocaleString()}
                  </span>
                </div>
              )}
            </div>
          )}

          {/* Chain Properties */}
          <div className="section-title">Properties</div>
          <div className="card">
            {[
              { icon: "🔒", name: "Immutable", desc: "Once sealed, never modified" },
              { icon: "🔗", name: "Hash-chained", desc: "Each entry links to previous" },
              { icon: "📋", name: "Append-only", desc: "New entries never overwrite" },
              { icon: "👁️", name: "Witnessed", desc: "Tri-witness: Human × AI × External" },
              { icon: "⚖️", name: "Governed", desc: "F1-F13 constitutional floors" },
              { icon: "🕐", name: "Monotonic", desc: "Time only advances with seals" },
            ].map((prop, i) => (
              <div key={i} className="result-item">
                <div className="result-icon">{prop.icon}</div>
                <div className="result-content">
                  <div className="result-title">{prop.name}</div>
                  <div className="result-desc">{prop.desc}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Recent Seals */}
          {chain.length > 0 && (
            <>
              <div className="section-title">Recent Seals</div>
              {chain.slice(0, 10).map((entry, i) => (
                <motion.div
                  key={i}
                  className="card"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.03 }}
                  style={{ padding: "14px 16px", marginBottom: "6px" }}
                >
                  <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
                    <div style={{
                      width: "36px", height: "36px", borderRadius: "10px",
                      display: "flex", alignItems: "center", justifyContent: "center",
                      background: "rgba(168,85,247,0.15)", fontSize: "14px", fontWeight: "700",
                      color: "var(--purple)",
                    }}>
                      #{entry.seq ?? "?"}
                    </div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: "14px", fontWeight: "600" }}>{entry.verdict || "SEAL"}</div>
                      <div style={{ fontSize: "12px", color: "var(--hint)" }}>
                        {entry.actor || "unknown"} • {entry.timestamp ? new Date(entry.timestamp).toLocaleDateString() : "—"}
                      </div>
                    </div>
                    <ChevronRight size={16} style={{ color: "var(--hint)" }} />
                  </div>
                </motion.div>
              ))}
            </>
          )}

          {/* Doctrine */}
          <div className="card" style={{ textAlign: "center", padding: "24px", borderTop: "2px solid var(--purple)" }}>
            <p style={{ fontSize: "14px", fontWeight: "600", color: "var(--purple)" }}>
              What is sealed cannot be erased.
            </p>
            <p style={{ fontSize: "12px", color: "var(--hint)", marginTop: "6px" }}>
              What is erased cannot be trusted.
            </p>
          </div>
        </motion.div>
      )}
    </div>
  );
}
