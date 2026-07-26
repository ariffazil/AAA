import React, { useState, useCallback, useMemo } from "react";
import { ShieldAlert, CheckCircle2, XCircle, Eye, Loader2 } from "lucide-react";

export interface ApprovalCardPayload {
  challenge_id: string;
  nonce: string;
  actor: string;
  authorization_session_id: string;
  candidate_hash: string;
  action_class: string;
  reversibility: string;
  blast_radius: string;
  seal_purpose: string;
  authority_effect: string;
  audience: string;
  issued_at: string;
  expires_at: string;
  human_summary: string;
  plan_id?: string;
  target_environment?: string;
}

interface Props {
  authorization_request: ApprovalCardPayload;
  onApprove: (signature_b64: string) => void;
  onReject: () => void;
  signingEndpoint?: string;
}

const SIGNING_URL = "http://127.0.0.1:18900/sign";

function canonicalSerialize(payload: ApprovalCardPayload): string {
  const canonical: Record<string, string> = {
    actor: payload.actor || "",
    authorization_session_id: payload.authorization_session_id || "",
    nonce: payload.nonce || "",
    candidate_hash: payload.candidate_hash || "",
    action_class: payload.action_class || "",
    reversibility: payload.reversibility || "",
    blast_radius: payload.blast_radius || "",
    seal_purpose: payload.seal_purpose || "",
    authority_effect: payload.authority_effect || "",
    audience: payload.audience || "arifOS",
    issued_at: payload.issued_at || "",
    expires_at: payload.expires_at || "",
    plan_id: payload.plan_id || "",
    target_environment: payload.target_environment || "",
  };
  return JSON.stringify(canonical, Object.keys(canonical).sort());
}

function blastBadge(radius: string): { color: string; label: string } {
  const level = (radius || "medium").toUpperCase();
  if (level.includes("CRITICAL") || level.includes("CATASTROPHIC") || level === "R5")
    return { color: "var(--color-danger, #dc2626)", label: "CRITICAL" };
  if (level.includes("HIGH") || level === "R4" || level.includes("IRREVERSIBLE"))
    return { color: "var(--color-warning, #f59e0b)", label: "HIGH" };
  if (level.includes("MEDIUM") || level === "R3")
    return { color: "var(--color-warning, #f59e0b)", label: "MEDIUM" };
  return { color: "var(--color-success, #16a34a)", label: "LOW" };
}

export default function ApprovalCard({
  authorization_request: req,
  onApprove,
  onReject,
  signingEndpoint = SIGNING_URL,
}: Props) {
  const [signing, setSigning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);

  const handleApprove = useCallback(async () => {
    setSigning(true);
    setError(null);
    try {
      const canonical = canonicalSerialize(req);
      const res = await fetch(signingEndpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ actor: req.actor, canonical_json: canonical }),
      });
      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}));
        throw new Error(errBody.error || `Signing server returned ${res.status}`);
      }
      const data = await res.json();
      if (!data.signature_b64) throw new Error("No signature in response");
      onApprove(data.signature_b64);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Signing failed");
    } finally {
      setSigning(false);
    }
  }, [req, signingEndpoint, onApprove]);

  const badge = blastBadge(req.blast_radius);
  const expStr = useMemo(() => {
    if (!req.expires_at) return "unknown";
    return new Date(req.expires_at).toLocaleTimeString();
  }, [req.expires_at]);

  return (
    <div
      style={{
        background: "var(--color-surface, #1a1817)",
        border: "1px solid var(--color-border, #2d2b28)",
        borderRadius: "12px",
        padding: "1.5rem",
        maxWidth: "480px",
        fontFamily: "monospace",
        color: "var(--color-text, #d4d0c9)",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", gap: "0.75rem", marginBottom: "1rem" }}>
        <ShieldAlert size={20} color={badge.color} />
        <h3 style={{ margin: 0, fontSize: "1rem", fontWeight: 600, color: badge.color }}>
          Production Authorization Required
        </h3>
      </div>

      {/* Action summary */}
      <p style={{ fontSize: "0.875rem", lineHeight: 1.5, marginBottom: "1rem", color: "#a6a29a" }}>
        {req.human_summary || req.seal_purpose || "Unnamed action"}
      </p>

      {/* Key fields */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.5rem", marginBottom: "1rem", fontSize: "0.8rem" }}>
        <Field label="Requested by" value={req.actor} />
        <Field label="Environment" value={req.target_environment || "production"} />
        <Field label="Reversibility" value={req.reversibility} />
        <Field
          label="Blast radius"
          value={badge.label}
          valueColor={badge.color}
        />
        <Field label="Expires" value={expStr} />
        <Field label="Plan" value={req.plan_id || "ad-hoc"} />
      </div>

      {/* Challenge ID (small) */}
      <div style={{ fontSize: "0.7rem", color: "#6b6560", marginBottom: "1rem" }}>
        Challenge: {req.challenge_id}
      </div>

      {/* Error */}
      {error && (
        <div
          style={{
            background: "rgba(220, 38, 38, 0.1)",
            border: "1px solid rgba(220, 38, 38, 0.3)",
            borderRadius: "6px",
            padding: "0.5rem 0.75rem",
            fontSize: "0.8rem",
            color: "#fca5a5",
            marginBottom: "1rem",
          }}
        >
          {error}
        </div>
      )}

      {/* Actions */}
      <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
        <button
          onClick={handleApprove}
          disabled={signing}
          style={{
            flex: 1,
            padding: "0.625rem 1rem",
            background: badge.color,
            color: "#0d0c0b",
            border: "none",
            borderRadius: "8px",
            cursor: signing ? "wait" : "pointer",
            fontFamily: "monospace",
            fontWeight: 600,
            fontSize: "0.85rem",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "0.5rem",
            opacity: signing ? 0.7 : 1,
          }}
        >
          {signing ? (
            <>
              <Loader2 size={16} style={{ animation: "spin 1s linear infinite" }} />
              Signing...
            </>
          ) : (
            <>
              <CheckCircle2 size={16} />
              Approve
            </>
          )}
        </button>

        <button
          onClick={onReject}
          disabled={signing}
          style={{
            padding: "0.625rem 1rem",
            background: "transparent",
            color: "var(--color-danger, #dc2626)",
            border: "1px solid var(--color-danger, #dc2626)",
            borderRadius: "8px",
            cursor: signing ? "not-allowed" : "pointer",
            fontFamily: "monospace",
            fontWeight: 600,
            fontSize: "0.85rem",
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            opacity: signing ? 0.5 : 1,
          }}
        >
          <XCircle size={16} />
          Reject
        </button>

        <button
          onClick={() => setShowDetails(!showDetails)}
          style={{
            padding: "0.625rem",
            background: "transparent",
            color: "#6b6560",
            border: "1px solid #3d3935",
            borderRadius: "8px",
            cursor: "pointer",
            fontFamily: "monospace",
          }}
          title="Inspect"
        >
          <Eye size={16} />
        </button>
      </div>

      {/* Expandable details */}
      {showDetails && (
        <div
          style={{
            marginTop: "1rem",
            padding: "0.75rem",
            background: "rgba(0,0,0,0.2)",
            borderRadius: "6px",
            fontSize: "0.72rem",
            fontFamily: "monospace",
            lineHeight: 1.6,
            maxHeight: "200px",
            overflow: "auto",
          }}
        >
          <pre style={{ margin: 0, whiteSpace: "pre-wrap", wordBreak: "break-all" }}>
            {JSON.stringify(
              {
                ...req,
                canonical: canonicalSerialize(req),
              },
              null,
              2
            )}
          </pre>
        </div>
      )}
    </div>
  );
}

function Field({
  label,
  value,
  valueColor,
}: {
  label: string;
  value: string;
  valueColor?: string;
}) {
  return (
    <div>
      <div style={{ color: "#6b6560", fontSize: "0.7rem", marginBottom: "2px" }}>{label}</div>
      <div style={{ color: valueColor || "#a6a29a", fontWeight: 500 }}>{value}</div>
    </div>
  );
}
