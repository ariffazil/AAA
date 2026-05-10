import { useState, useEffect, useCallback } from 'react';
import { Lock, Shield, Clock, Check, X, AlertTriangle } from 'lucide-react';

export interface SessionManifest {
  session_id: string;
  timestamp: string;
  actor_hash: string;
  entropy_0: number;
  capability_claim: string[];
  ai_self_model: 'AGI' | 'ASI' | 'APEX';
  civilization_context: string[];
  consent_type: ConsentType;
  valid_until?: string;
  state: 'VALID' | 'TEMPORAL' | 'EXPIRED';
}

export type ConsentType = 'ABSOLUTE' | 'AMENDABLE' | 'EMERGENCY';

interface ConsentDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConsent: (manifest: SessionManifest) => void;
}

function generateUUIDv4(): string {
  if (typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const hex = Array.from(bytes, (b) => b.toString(16).padStart(2, '0'));
  return `${hex.slice(0, 4).join('')}-${hex.slice(4, 6).join('')}-${hex
    .slice(6, 8)
    .join('')}-${hex.slice(8, 10).join('')}-${hex.slice(10, 16).join('')}`;
}

async function sha256(message: string): Promise<string> {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map((b) => b.toString(16).padStart(2, '0')).join('');
}

function calculateEntropy(): number {
  const array = new Uint32Array(8);
  crypto.getRandomValues(array);
  const noise = Array.from(array)
    .map((v) => Math.abs(v) / 0xffffffff)
    .reduce((a, b) => a + b, 0);
  return Math.round(noise * 1000) / 1000;
}

const CONSENT_TYPES: { type: ConsentType; label: string; description: string; halfLife: string }[] = [
  {
    type: 'ABSOLUTE',
    label: 'Absolute Consent',
    description: 'Permanent binding. Sovereign veto always active. Cannot be revoked without explicit VOID.',
    halfLife: '∞',
  },
  {
    type: 'AMENDABLE',
    label: 'Amendable Consent',
    description: 'Time-bounded consent with decay. Freshness affects authority score. Can be renewed.',
    halfLife: '24h',
  },
  {
    type: 'EMERGENCY',
    label: 'Emergency Consent',
    description: 'Crisis-mode binding. Minimal F11 verification. Auto-expires at window close.',
    halfLife: '1h',
  },
];

const CAPABILITY_CLAIMS = [
  'arif_sense_observe',
  'arif_mind_reason',
  'arif_kernel_route',
  'arif_heart_critique',
  'arif_forge_execute',
  'arif_judge_deliberate',
  'arif_vault_seal',
  'arif_gateway_connect',
  'arif_memory_recall',
  'arif_ops_measure',
  'arif_session_init',
];

const CIVILIZATION_CONTEXTS = [
  'SEAL-DOMAIN: arifOS',
  'SEAL-DOMAIN: GEOX',
  'SEAL-DOMAIN: WEALTH',
  'SEAL-DOMAIN: WELL',
  'SEAL-DOMAIN: AAA',
  'SEAL-DOMAIN: HERMES',
];

export function ConsentDialog({ isOpen, onClose, onConsent }: ConsentDialogProps) {
  const [step, setStep] = useState<'type' | 'capabilities' | 'confirm'>('type');
  const [consentType, setConsentType] = useState<ConsentType>('AMENDABLE');
  const [selectedCapabilities, setSelectedCapabilities] = useState<string[]>([...CAPABILITY_CLAIMS]);
  const [actorId, setActorId] = useState('Arif-Sovereign');
  const [isVerifying, setIsVerifying] = useState(false);
  const [isBound, setIsBound] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      setStep('type');
      setIsBound(false);
    }
  }, [isOpen]);

  const handleCapabilityToggle = useCallback((cap: string) => {
    setSelectedCapabilities((prev) =>
      prev.includes(cap) ? prev.filter((c) => c !== cap) : [...prev, cap]
    );
  }, []);

  const handleSelectAll = useCallback(() => {
    setSelectedCapabilities([...CAPABILITY_CLAIMS]);
  }, []);

  const handleDeselectAll = useCallback(() => {
    setSelectedCapabilities([]);
  }, []);

  const handleVerifyAndBind = useCallback(async () => {
    setIsVerifying(true);

    try {
      const actor_raw = `${actorId}:local-sovereign-session:${crypto.randomUUID?.() ?? generateUUIDv4()}:${Date.now()}`;
      const actor_hash = await sha256(actor_raw);
      const entropy_0 = calculateEntropy();

      const now = new Date();
      const timestamp = now.toISOString();

      let valid_until: string | undefined;
      let state: SessionManifest['state'] = 'VALID';

      if (consentType === 'AMENDABLE') {
        const expiry = new Date(now.getTime() + 24 * 60 * 60 * 1000);
        valid_until = expiry.toISOString();
        state = 'TEMPORAL';
      } else if (consentType === 'EMERGENCY') {
        const expiry = new Date(now.getTime() + 60 * 60 * 1000);
        valid_until = expiry.toISOString();
        state = 'TEMPORAL';
      }

      const manifest: SessionManifest = {
        session_id: generateUUIDv4(),
        timestamp,
        actor_hash,
        entropy_0,
        capability_claim: selectedCapabilities,
        ai_self_model: 'AGI',
        civilization_context: CIVILIZATION_CONTEXTS,
        consent_type: consentType,
        valid_until,
        state,
      };

      setIsBound(true);
      setTimeout(() => {
        onConsent(manifest);
        onClose();
      }, 800);
    } catch {
      // Keep the UI fail-closed without exposing auth internals.
    } finally {
      setIsVerifying(false);
    }
  }, [actorId, consentType, selectedCapabilities, onConsent, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center">
      <div className="absolute inset-0 bg-black/80 backdrop-blur-sm" onClick={onClose} />

      <div className="relative bg-[#0a0a0a] border border-white/10 rounded-lg w-full max-w-2xl max-h-[90vh] overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-white/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-red-500/10 border border-red-500/30 rounded flex items-center justify-center">
              <Lock className="w-5 h-5 text-red-500" />
            </div>
            <div>
              <h2 className="text-lg font-black text-white tracking-tight">000_INIT SESSION ANCHOR</h2>
              <p className="text-[10px] font-mono text-white/40 uppercase tracking-widest">
                {step === 'type' ? 'Select Consent Type' : step === 'capabilities' ? 'Configure Capabilities' : 'Confirm Identity Binding'}
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-white/40 hover:text-white transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Progress */}
        <div className="flex gap-1 px-6 py-3 bg-black/40">
          {['type', 'capabilities', 'confirm'].map((s, i) => (
            <div
              key={s}
              className={`h-1 flex-1 rounded ${
                i <= ['type', 'capabilities', 'confirm'].indexOf(step)
                  ? 'bg-red-500'
                  : 'bg-white/10'
              }`}
            />
          ))}
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {step === 'type' && (
            <div className="space-y-4">
              <p className="text-sm text-white/60 mb-6">
                Select the consent type that governs this session. This determines how identity binding
                and entropy decay are handled per F11 AUTH and F7 HUMILITY floors.
              </p>

              {CONSENT_TYPES.map((ct) => (
                <button
                  key={ct.type}
                  onClick={() => setConsentType(ct.type)}
                  className={`w-full p-4 border rounded-lg text-left transition-all ${
                    consentType === ct.type
                      ? 'border-red-500 bg-red-500/5'
                      : 'border-white/10 hover:border-white/30'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <span className="font-black text-white tracking-tight">{ct.label}</span>
                    <span className="text-[10px] font-mono text-white/40">half-life: {ct.halfLife}</span>
                  </div>
                  <p className="text-xs text-white/50">{ct.description}</p>
                </button>
              ))}

              <div className="pt-4 flex justify-end">
                <button
                  onClick={() => setStep('capabilities')}
                  className="px-6 py-3 bg-white text-black font-black text-sm tracking-tight hover:bg-red-500 hover:text-white transition-all flex items-center gap-2"
                >
                  Next <Check className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {step === 'capabilities' && (
            <div className="space-y-4">
              <p className="text-sm text-white/60 mb-4">
                Declare which tools this session may invoke. Per F12 INJECTION, external content is not
                granted authority — only explicitly claimed capabilities.
              </p>

              <div className="flex gap-4 mb-4">
                <button
                  onClick={handleSelectAll}
                  className="text-[10px] font-mono text-red-500 hover:text-red-400 uppercase tracking-widest"
                >
                  Select All
                </button>
                <button
                  onClick={handleDeselectAll}
                  className="text-[10px] font-mono text-white/40 hover:text-white uppercase tracking-widest"
                >
                  Deselect All
                </button>
              </div>

              <div className="grid grid-cols-2 gap-2">
                {CAPABILITY_CLAIMS.map((cap) => (
                  <button
                    key={cap}
                    onClick={() => handleCapabilityToggle(cap)}
                    className={`p-3 border rounded text-left transition-all ${
                      selectedCapabilities.includes(cap)
                        ? 'border-emerald-500/50 bg-emerald-500/5'
                        : 'border-white/10 hover:border-white/30'
                    }`}
                  >
                    <code className="text-xs font-mono text-white/80">{cap}</code>
                    {selectedCapabilities.includes(cap) && (
                      <Check className="w-3 h-3 text-emerald-500 float-right" />
                    )}
                  </button>
                ))}
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => setStep('type')}
                  className="px-6 py-3 border border-white/20 text-white/60 font-bold text-sm tracking-tight hover:border-white/40 transition-all"
                >
                  Back
                </button>
                <button
                  onClick={() => setStep('confirm')}
                  className="px-6 py-3 bg-white text-black font-black text-sm tracking-tight hover:bg-red-500 hover:text-white transition-all flex items-center gap-2"
                >
                  Next <Check className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}

          {step === 'confirm' && (
            <div className="space-y-6">
              <p className="text-sm text-white/60">
                Verify your identity and review the session manifest. Per F11 AUTH, actor credentials
                must be verified before sovereign tools become available.
              </p>

              {/* Actor ID */}
              <div>
                <label className="text-[10px] font-mono text-white/40 uppercase tracking-widest block mb-2">
                  Actor Identifier
                </label>
                <input
                  type="text"
                  value={actorId}
                  onChange={(e) => setActorId(e.target.value)}
                  className="w-full p-3 bg-black/40 border border-white/20 rounded text-white font-mono text-sm focus:border-red-500 focus:outline-none transition-colors"
                  placeholder="Arif-Sovereign"
                />
              </div>

              {/* Manifest Preview */}
              <div className="p-4 bg-black/60 border border-white/10 rounded">
                <div className="flex items-center gap-2 mb-3">
                  <Shield className="w-4 h-4 text-red-500" />
                  <span className="text-[10px] font-mono text-white/60 uppercase tracking-widest">
                    Session Manifest Preview
                  </span>
                </div>
                <div className="space-y-2 font-mono text-[10px] text-white/50">
                  <div>
                    <span className="text-white/30">session_id:</span>{' '}
                    <span className="text-emerald-500">{generateUUIDv4().slice(0, 18)}...</span>
                  </div>
                  <div>
                    <span className="text-white/30">actor_id:</span> <span className="text-white">{actorId}</span>
                  </div>
                  <div>
                    <span className="text-white/30">consent_type:</span>{' '}
                    <span className="text-red-500">{consentType}</span>
                  </div>
                  <div>
                    <span className="text-white/30">capabilities:</span>{' '}
                    <span className="text-white">{selectedCapabilities.length} claimed</span>
                  </div>
                  <div>
                    <span className="text-white/30">ai_self_model:</span>{' '}
                    <span className="text-blue-400">AGI</span>
                  </div>
                  <div>
                    <span className="text-white/30">state:</span>{' '}
                    <span className={consentType === 'ABSOLUTE' ? 'text-emerald-500' : 'text-amber-500'}>
                      {consentType === 'ABSOLUTE' ? 'VALID' : 'TEMPORAL'}
                    </span>
                  </div>
                  {consentType !== 'ABSOLUTE' && (
                    <div className="flex items-center gap-1 text-amber-500">
                      <Clock className="w-3 h-3" />
                      <span>Auto-expires per {consentType} half-life</span>
                    </div>
                  )}
                </div>
              </div>

              {/* Warnings */}
              <div className="p-4 bg-amber-500/5 border border-amber-500/20 rounded flex gap-3">
                <AlertTriangle className="w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5" />
                <div className="text-xs text-white/60">
                  <p className="font-bold text-amber-500 mb-1">F1 AMANAH Warning</p>
                  <p>
                    This session will be bound to your identity. Irreversible actions require explicit
                    sovereign consent via the Approval Queue. Session entropy (dS_0) has been recorded for
                    audit continuity.
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setStep('capabilities')}
                  className="px-6 py-3 border border-white/20 text-white/60 font-bold text-sm tracking-tight hover:border-white/40 transition-all"
                >
                  Back
                </button>
                <button
                  onClick={handleVerifyAndBind}
                  disabled={isVerifying || isBound}
                  className={`px-8 py-3 font-black text-sm tracking-tight flex items-center gap-2 transition-all ${
                    isBound
                      ? 'bg-emerald-500 text-black'
                      : isVerifying
                      ? 'bg-white/20 text-white/40 cursor-wait'
                      : 'bg-red-500 text-black hover:bg-white'
                  }`}
                >
                  {isBound ? (
                    <>
                      <Check className="w-4 h-4" /> IDENTITY BOUND
                    </>
                  ) : isVerifying ? (
                    'Verifying...'
                  ) : (
                    <>
                      <Lock className="w-4 h-4" /> BIND IDENTITY (F11 AUTH)
                    </>
                  )}
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

interface SessionBadgeProps {
  manifest: SessionManifest | null;
  onRevoke?: () => void;
}

export function SessionBadge({ manifest, onRevoke }: SessionBadgeProps) {
  if (!manifest) {
    return (
      <div className="px-3 py-1.5 border border-white/10 rounded text-[9px] font-mono text-white/40">
        <Lock className="w-3 h-3 inline mr-1.5" />
        UNBOUND SESSION
      </div>
    );
  }

  const isExpired = manifest.valid_until
    ? new Date(manifest.valid_until) < new Date()
    : false;

  const stateColor =
    manifest.state === 'VALID'
      ? 'border-emerald-500/30 text-emerald-500'
      : manifest.state === 'TEMPORAL' && !isExpired
      ? 'border-amber-500/30 text-amber-500'
      : 'border-red-500/30 text-red-500';

  const stateBg =
    manifest.state === 'VALID'
      ? 'bg-emerald-950/20'
      : manifest.state === 'TEMPORAL' && !isExpired
      ? 'bg-amber-950/20'
      : 'bg-red-950/20';

  return (
    <div className={`px-3 py-1.5 border rounded flex items-center gap-2 ${stateBg} ${stateColor}`}>
      <Shield className="w-3 h-3" />
      <div className="flex flex-col">
        <span className="font-mono text-[9px] uppercase tracking-widest">
          {manifest.state === 'VALID' ? 'BOUND' : manifest.state === 'TEMPORAL' && !isExpired ? 'TEMPORAL' : 'EXPIRED'}
        </span>
        <span className="font-mono text-[8px] opacity-60">
          {manifest.session_id.slice(0, 8)}... | dS₀: {manifest.entropy_0}
        </span>
      </div>
      {onRevoke && manifest.state !== 'EXPIRED' && (
        <button
          onClick={onRevoke}
          className="ml-2 text-white/30 hover:text-red-500 transition-colors"
          title="Revoke session"
        >
          <X className="w-3 h-3" />
        </button>
      )}
    </div>
  );
}
