import { useState } from "react";
import { motion } from "framer-motion";
import { Compass, Search, ArrowRight, Zap, MapPin, DollarSign, Heart, Scale, GitBranch } from "lucide-react";

interface IntentResult {
  intent_summary?: string;
  loop_class?: string;
  required_organs?: string[];
  blast_radius?: string;
  next_lawful_call?: string;
  irreversible_flag?: boolean;
}

const LOOP_CLASSES: Record<string, { color: string; desc: string }> = {
  EVIDENCE: { color: "var(--green)", desc: "GEOX evidence gathering" },
  CAPITAL: { color: "var(--yellow)", desc: "WEALTH capital analysis" },
  SUBSTRATE: { color: "var(--accent)", desc: "WELL readiness check" },
  EXECUTION: { color: "var(--orange)", desc: "A-FORGE build/deploy" },
  JUDGMENT: { color: "var(--purple)", desc: "arifOS constitutional verdict" },
  COCKPIT: { color: "var(--hint)", desc: "AAA session/state" },
  COMPOSITE: { color: "var(--red)", desc: "Multi-organ pipeline" },
};

export default function InitPage() {
  const [intent, setIntent] = useState("");
  const [result, setResult] = useState<IntentResult | null>(null);
  const [loading, setLoading] = useState(false);

  const classifyIntent = async () => {
    if (!intent.trim()) return;
    setLoading(true);
    setResult(null);

    try {
      const resp = await fetch("/api/init/classify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ intent: intent.trim() }),
      });
      const data = await resp.json();
      setResult(data?.result || data);
    } catch (e: any) {
      setResult({ intent_summary: `Error: ${e.message}` });
    } finally {
      setLoading(false);
    }
  };

  // Simple client-side classification preview
  const guessClass = (text: string): string => {
    const t = text.toLowerCase();
    if (t.match(/seismic|well|basin|petrophys|geolog|prospect|stratigr/)) return "EVIDENCE";
    if (t.match(/npv|irr|cashflow|capital|invest|portfolio|fiscal|oil price|money/)) return "CAPITAL";
    if (t.match(/sleep|fatigue|vitality|ready|health|energy|stress/)) return "SUBSTRATE";
    if (t.match(/build|deploy|docker|git|push|restart|fix|code|script/)) return "EXECUTION";
    if (t.match(/judge|seal|verdict|law|floor|constitution|irreversible/)) return "JUDGMENT";
    if (t.match(/session|status|agent|registry|cockpit/)) return "COCKPIT";
    return "COMPOSITE";
  };

  const previewClass = intent ? guessClass(intent) : null;

  return (
    <div className="app-container">
      <motion.div className="page-header" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <div style={{ fontSize: "48px", marginBottom: "16px" }}>🧭</div>
        <h1>000 INIT</h1>
        <p className="subtitle">Intent Classification — Golden Path Entry</p>
      </motion.div>

      {/* Input */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
        <div className="card">
          <div style={{ fontSize: "13px", fontWeight: "600", marginBottom: "10px", color: "var(--hint)" }}>
            WHAT DO YOU WANT TO DO?
          </div>
          <textarea
            className="search-input"
            style={{ width: "100%", minHeight: "80px", resize: "vertical", fontFamily: "inherit" }}
            placeholder="e.g., 'Screen prospect X in Sarawak basin' or 'Check Malaysia fiscal breakeven at $80'"
            value={intent}
            onChange={(e) => setIntent(e.target.value)}
          />

          {/* Live preview */}
          {previewClass && (
            <div style={{ marginTop: "10px", display: "flex", alignItems: "center", gap: "8px" }}>
              <span style={{ fontSize: "12px", color: "var(--hint)" }}>Detected:</span>
              <span className="badge" style={{
                background: `${LOOP_CLASSES[previewClass]?.color}20`,
                color: LOOP_CLASSES[previewClass]?.color,
              }}>
                {previewClass}
              </span>
              <span style={{ fontSize: "12px", color: "var(--hint)" }}>
                {LOOP_CLASSES[previewClass]?.desc}
              </span>
            </div>
          )}

          <button
            className="btn btn-primary"
            style={{ marginTop: "12px" }}
            onClick={classifyIntent}
            disabled={loading || !intent.trim()}
          >
            {loading ? <><div className="spinner" style={{ width: "16px", height: "16px", borderWidth: "2px" }} /> Classifying...</> : <><Compass size={16} /> Classify Intent</>}
          </button>
        </div>
      </motion.div>

      {/* Result */}
      {result && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          {/* Loop Class */}
          <div className="card">
            <div className="card-header">
              <div className="card-icon" style={{
                background: `${LOOP_CLASSES[result.loop_class || "COMPOSITE"]?.color}15`,
              }}>
                <Zap size={24} style={{ color: LOOP_CLASSES[result.loop_class || "COMPOSITE"]?.color }} />
              </div>
              <div>
                <div className="card-title">{result.loop_class || "UNKNOWN"}</div>
                <div className="card-subtitle">{LOOP_CLASSES[result.loop_class || "COMPOSITE"]?.desc}</div>
              </div>
            </div>

            {result.intent_summary && (
              <div style={{ padding: "12px", background: "rgba(255,255,255,0.03)", borderRadius: "10px", marginBottom: "12px" }}>
                <p style={{ fontSize: "13px", lineHeight: "1.5" }}>{result.intent_summary}</p>
              </div>
            )}

            {/* Required Organs */}
            {result.required_organs && result.required_organs.length > 0 && (
              <div style={{ marginBottom: "12px" }}>
                <div style={{ fontSize: "12px", color: "var(--hint)", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "0.5px" }}>
                  Required Organs
                </div>
                <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                  {result.required_organs.map((organ: string) => (
                    <span key={organ} className="badge badge-blue">{organ}</span>
                  ))}
                </div>
              </div>
            )}

            {/* Blast Radius */}
            {result.blast_radius && (
              <div className="result-item">
                <div className="result-icon">💥</div>
                <div className="result-content">
                  <div className="result-title">Blast Radius</div>
                </div>
                <span className={`badge ${
                  result.blast_radius === "LOW" ? "badge-green" :
                  result.blast_radius === "MEDIUM" ? "badge-yellow" :
                  result.blast_radius === "HIGH" ? "badge-red" : "badge-purple"
                }`}>
                  {result.blast_radius}
                </span>
              </div>
            )}

            {/* Irreversible Flag */}
            {result.irreversible_flag && (
              <div style={{ marginTop: "12px", padding: "12px", background: "rgba(239,68,68,0.1)", borderRadius: "10px", border: "1px solid rgba(239,68,68,0.2)" }}>
                <p style={{ fontSize: "13px", color: "var(--red)", fontWeight: "600" }}>
                  ⚠️ IRREVERSIBLE — Requires 888_HOLD + Sovereign acknowledgment
                </p>
              </div>
            )}

            {/* Next Call */}
            {result.next_lawful_call && (
              <div style={{ marginTop: "12px", display: "flex", alignItems: "center", gap: "8px", padding: "12px", background: "rgba(59,130,246,0.08)", borderRadius: "10px" }}>
                <ArrowRight size={16} style={{ color: "var(--accent)" }} />
                <div>
                  <div style={{ fontSize: "12px", color: "var(--hint)" }}>Next lawful call</div>
                  <div style={{ fontSize: "14px", fontWeight: "600", fontFamily: "monospace" }}>{result.next_lawful_call}</div>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* Quick Examples */}
      {!result && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
          <div className="section-title">Try Examples</div>
          {[
            { text: "Screen prospect in Sarawak basin", class: "EVIDENCE" },
            { text: "Check Malaysia fiscal breakeven", class: "CAPITAL" },
            { text: "Deploy the new GEOX engine", class: "EXECUTION" },
            { text: "Seal this verdict to VAULT999", class: "JUDGMENT" },
            { text: "Am I ready for a 12-hour session?", class: "SUBSTRATE" },
          ].map((ex, i) => (
            <button
              key={i}
              className="card"
              style={{ cursor: "pointer", textAlign: "left", width: "100%", display: "flex", alignItems: "center", gap: "12px" }}
              onClick={() => { setIntent(ex.text); }}
            >
              <span className="badge" style={{
                background: `${LOOP_CLASSES[ex.class]?.color}20`,
                color: LOOP_CLASSES[ex.class]?.color,
                minWidth: "80px",
                justifyContent: "center",
              }}>
                {ex.class}
              </span>
              <span style={{ fontSize: "14px" }}>{ex.text}</span>
            </button>
          ))}
        </motion.div>
      )}
    </div>
  );
}
