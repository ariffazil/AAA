/**
 * HumanPatternReport — Sovereign-only read-only DeepnShadow renderer.
 *
 * Constraints:
 * - No inference logic in UI.
 * - Hard identity gate: renders only for sovereign actor.
 * - Append-only observation display.
 * - Hypotheses shown as hypotheses, not truths.
 *
 * DITEMPA BUKAN DIBERI
 */

import { useMemo } from "react";
import {
  Eye,
  Brain,
  Heart,
  ShieldAlert,
  MessageSquare,
  GitBranch,
  UserX,
  CheckCircle2,
  AlertTriangle,
  Ban,
} from "lucide-react";

export type DignityStatus = "safe" | "guarded" | "hold";
export type InferenceMode = "mirror" | "other" | "team";

export interface DeepnShadowReport {
  report_id: string;
  session_id: string;
  mode: InferenceMode;
  observations: Array<{
    observation_id: string;
    description: string;
    context?: string | null;
    evidence_class: string;
  }>;
  patterns: Array<{
    pattern_id: string;
    recurrence_count: number;
    confidence: number;
    trigger_contexts: string[];
  }>;
  hypotheses: Array<{
    hypothesis_id: string;
    hypothesis_text: string;
    confidence: number;
    uncertainty_band: string;
    dignity_status: DignityStatus;
    alternative_explanations: Array<{
      explanation_text: string;
      likelihood: string;
    }>;
  }>;
  projection_mirrors: Array<{
    mirror_id: string;
    resonance_score: number;
    reflection_text: string;
    safe_self_action?: string | null;
  }>;
  scar_vectors: Array<{
    vector_id: string;
    protected_zone: string;
    confidence: number;
    boundary_type: string;
    safe_action_hint?: string | null;
  }>;
  safe_actions: Array<{
    action_text: string;
    avoids_trigger?: string | null;
    preserves_dignity: boolean;
  }>;
  metabolized_actions: Array<{
    raw_charge: string;
    metabolized_charge: string;
    action: {
      action_text: string;
    };
  }>;
  overall_dignity_status: DignityStatus;
  overall_confidence: number;
  verdict: string;
  constitutional_notes: string[];
}

interface HumanPatternReportProps {
  report: DeepnShadowReport | null;
  sovereignActor: string;
  currentActor: string;
}

function StatusBadge({ status }: { status: DignityStatus }) {
  const styles = {
    safe: "bg-emerald-100 text-emerald-800 border-emerald-200",
    guarded: "bg-amber-100 text-amber-800 border-amber-200",
    hold: "bg-rose-100 text-rose-800 border-rose-200",
  };
  const icons = {
    safe: <CheckCircle2 className="w-3.5 h-3.5" />,
    guarded: <AlertTriangle className="w-3.5 h-3.5" />,
    hold: <Ban className="w-3.5 h-3.5" />,
  };
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium border ${styles[status]}`}
    >
      {icons[status]}
      {status.toUpperCase()}
    </span>
  );
}

export default function HumanPatternReport({
  report,
  sovereignActor,
  currentActor,
}: HumanPatternReportProps) {
  const isAuthorized = useMemo(
    () => currentActor === sovereignActor,
    [currentActor, sovereignActor],
  );

  if (!isAuthorized) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        <UserX className="w-5 h-5 mr-2" />
        <span className="text-sm">Shadow maps are sovereign-only.</span>
      </div>
    );
  }

  if (!report) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        <Eye className="w-5 h-5 mr-2" />
        <span className="text-sm">No pattern report loaded.</span>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-3xl">
      {/* Header */}
      <div className="border border-slate-200 rounded-lg p-4 bg-slate-50">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-sm font-semibold text-slate-700 flex items-center gap-2">
            <Eye className="w-4 h-4 text-slate-500" />
            Human Pattern Report
          </h2>
          <StatusBadge status={report.overall_dignity_status} />
        </div>
        <p className="text-xs text-slate-500 leading-relaxed">
          Shadow maps are navigation instruments, not verdicts. Observed behaviour ≠ inner truth.
        </p>
        <div className="mt-2 flex items-center gap-3 text-xs text-slate-400">
          <span>Verdict: <strong className="text-slate-600">{report.verdict}</strong></span>
          <span>Mode: <strong className="text-slate-600">{report.mode}</strong></span>
          <span>Confidence: <strong className="text-slate-600">{report.overall_confidence.toFixed(2)}</strong></span>
        </div>
      </div>

      {/* Observations */}
      {report.observations.length > 0 && (
        <Section icon={<Eye className="w-4 h-4" />} title="Observations (DS-111)">
          <ul className="space-y-2">
            {report.observations.map((o) => (
              <li key={o.observation_id} className="text-sm text-slate-700 bg-white border border-slate-200 rounded p-3">
                <p>{o.description}</p>
                {o.context && (
                  <p className="text-xs text-slate-400 mt-1">Context: {o.context}</p>
                )}
                <span className="text-xs text-slate-400 mt-1 inline-block">Evidence: {o.evidence_class}</span>
              </li>
            ))}
          </ul>
        </Section>
      )}

      {/* Patterns */}
      {report.patterns.length > 0 && (
        <Section icon={<GitBranch className="w-4 h-4" />} title="Patterns (DS-222)">
          {report.patterns.map((p) => (
            <div key={p.pattern_id} className="text-sm text-slate-700 bg-white border border-slate-200 rounded p-3">
              <p>Recurrence: {p.recurrence_count} | Confidence: {p.confidence.toFixed(2)}</p>
              {p.trigger_contexts.length > 0 && (
                <p className="text-xs text-slate-400 mt-1">Contexts: {p.trigger_contexts.join(", ")}</p>
              )}
            </div>
          ))}
        </Section>
      )}

      {/* Hypotheses */}
      {report.hypotheses.length > 0 && (
        <Section icon={<Brain className="w-4 h-4" />} title="Hypotheses (DS-333)">
          <div className="space-y-3">
            {report.hypotheses.map((h) => (
              <div key={h.hypothesis_id} className="bg-white border border-slate-200 rounded p-3">
                <div className="flex items-center justify-between mb-1">
                  <p className="text-sm font-medium text-slate-700">{h.hypothesis_text}</p>
                  <StatusBadge status={h.dignity_status} />
                </div>
                <div className="text-xs text-slate-400 mb-2">
                  Confidence: {h.confidence.toFixed(2)} ({h.uncertainty_band})
                </div>
                {h.alternative_explanations.length > 0 && (
                  <div className="bg-slate-50 rounded p-2">
                    <p className="text-xs font-medium text-slate-500 mb-1">Alternative explanations:</p>
                    <ul className="space-y-1">
                      {h.alternative_explanations.map((alt, i) => (
                        <li key={i} className="text-xs text-slate-600 flex items-center gap-1.5">
                          <span className="w-1 h-1 rounded-full bg-slate-300" />
                          {alt.explanation_text} <span className="text-slate-400">({alt.likelihood})</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* Projection Mirrors */}
      {report.projection_mirrors.length > 0 && (
        <Section icon={<ShieldAlert className="w-4 h-4" />} title="Projection Mirror (DS-444)">
          {report.projection_mirrors.map((m) => (
            <div key={m.mirror_id} className="bg-amber-50 border border-amber-200 rounded p-3">
              <p className="text-sm text-amber-800">{m.reflection_text}</p>
              <p className="text-xs text-amber-600 mt-1">Resonance: {(m.resonance_score * 100).toFixed(0)}%</p>
              {m.safe_self_action && (
                <p className="text-xs text-amber-700 mt-1 font-medium">Action: {m.safe_self_action}</p>
              )}
            </div>
          ))}
        </Section>
      )}

      {/* Scar Vectors */}
      {report.scar_vectors.length > 0 && (
        <Section icon={<Heart className="w-4 h-4" />} title="Scar Vectors (DS-555)">
          {report.scar_vectors.map((s) => (
            <div key={s.vector_id} className="text-sm text-slate-700 bg-white border border-slate-200 rounded p-3">
              <p>Protected zone: <strong>{s.protected_zone}</strong> | Boundary: {s.boundary_type}</p>
              <p className="text-xs text-slate-400 mt-1">Confidence: {s.confidence.toFixed(2)}</p>
              {s.safe_action_hint && (
                <p className="text-xs text-emerald-600 mt-1">Hint: {s.safe_action_hint}</p>
              )}
            </div>
          ))}
        </Section>
      )}

      {/* Safe Actions */}
      {report.safe_actions.length > 0 && (
        <Section icon={<MessageSquare className="w-4 h-4" />} title="Safe Actions (DS-777)">
          <ul className="space-y-2">
            {report.safe_actions.map((a, i) => (
              <li key={i} className="text-sm text-slate-700 bg-white border border-slate-200 rounded p-3 flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500 mt-0.5 shrink-0" />
                <div>
                  <p>{a.action_text}</p>
                  {a.avoids_trigger && (
                    <p className="text-xs text-slate-400 mt-1">Avoid: {a.avoids_trigger}</p>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </Section>
      )}

      {/* Metabolized Actions */}
      {report.metabolized_actions.length > 0 && (
        <Section icon={<MessageSquare className="w-4 h-4" />} title="Metabolized Actions (DS-777)">
          {report.metabolized_actions.map((m, i) => (
            <div key={i} className="text-sm text-slate-700 bg-white border border-slate-200 rounded p-3">
              <p>
                <span className="text-slate-400">{m.raw_charge}</span>
                {" → "}
                <span className="font-medium text-slate-700">{m.metabolized_charge}</span>
              </p>
              <p className="text-xs text-slate-500 mt-1">{m.action.action_text}</p>
            </div>
          ))}
        </Section>
      )}

      {/* Constitutional Notes */}
      {report.constitutional_notes.length > 0 && (
        <div className="border-t border-slate-200 pt-4">
          <p className="text-xs font-medium text-slate-500 mb-2">Constitutional Notes</p>
          <ul className="space-y-1">
            {report.constitutional_notes.map((note, i) => (
              <li key={i} className="text-xs text-slate-400 flex items-start gap-1.5">
                <span className="w-1 h-1 rounded-full bg-slate-300 mt-1.5 shrink-0" />
                {note}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function Section({
  icon,
  title,
  children,
}: {
  icon: React.ReactNode;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="border border-slate-200 rounded-lg p-4 bg-white">
      <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider flex items-center gap-2 mb-3">
        {icon}
        {title}
      </h3>
      {children}
    </div>
  );
}
